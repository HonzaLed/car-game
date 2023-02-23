import asyncio
from plugins import PluginManager
import console
import entity

import pygame, pygame.freetype
import numpy

aspect_ratio = [9, 16]

WIDTH = 480  # 9
HEIGHT = (WIDTH // aspect_ratio[0]) * aspect_ratio[1]  # 16

BACKGROUND = (0, 0, 0)

car = None
road = None
obstacles_group = None


def init_pygame():
    global screen, clock, GAME_FONT
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    GAME_FONT = pygame.freetype.Font("assets/BACKTO1982.TTF", 24)
    clock = pygame.time.Clock()


def spawn_initial_entities():
    global road, car, obstacles_group, plugins
    road = entity.Road(WIDTH // 2, (HEIGHT // 2)-4, WIDTH, HEIGHT + 8)
    car = entity.Car(WIDTH // 2, HEIGHT - (HEIGHT // 3), 72, 128)

    obstacles_group = pygame.sprite.Group()
    obstacles_group.add(entity.Person(WIDTH//3*2, 1))
    obstacles_group.add(entity.Person(WIDTH//3  , 1), value=50)
    plugins.run_hook("on_init", obstacles_group)


async def main():
    global plugins
    plugins = PluginManager(path="plugins")  # initialize plugin system
    # register hooks
    plugins.register_hook("on_screen_draw")
    plugins.register_hook("on_progress")
    plugins.register_hook("on_init")
    plugins.search_plugins()  # load plugins from the folder
    plugins.enable_all((WIDTH, HEIGHT))  # plugins started

    init_pygame()
    spawn_initial_entities()
    frame = 0
    while True:
        break_now = False
        ### GAME LOOP ###
        pygame.event.pump()

        # Draw loop
        screen.fill(BACKGROUND)

        if frame % 10 == 0:
            road.progress()
            road.draw(screen)
            for i in obstacles_group:
                i.progress(8, car)
            plugins.run_hook("on_progress", car)
        else:
            road.draw(screen)
            
        obstacles_group.draw(screen)
        car.draw(screen)
        car.update(WIDTH)

        score_text, rect = GAME_FONT.render("Score: "+str(car.score), (0, 0, 0))
        screen.blit(score_text, (WIDTH*0.1, HEIGHT*0.95))
        plugins.run_hook("on_screen_draw", screen)
        pygame.display.flip()
        clock.tick(60)

        # if pygame.sprite.spritecollideany(player, doors):
        #     console.log("Touched, level completed!")
        #     break_now = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    break_now = True
        if break_now:
            break
        frame += 1


asyncio.run(main())
