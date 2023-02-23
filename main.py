import asyncio
from plugins import PluginManager
import console
import entity

import pygame
import numpy

aspect_ratio = [9, 16]

WIDTH  = 480  # 9
HEIGHT = (WIDTH // aspect_ratio[0]) * aspect_ratio[1]  # 16

BACKGROUND = (0, 0, 0)

car  = None
road = None


def init_pygame():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()


def spawn_initial_entities():
    global road, car
    road = entity.Road(WIDTH//2, HEIGHT//2, WIDTH, HEIGHT)
    car = entity.Car(WIDTH // 2, HEIGHT - (HEIGHT//3), 72, 128)

    # boxes = pygame.sprite.Group()
    # for bx in range(35, WIDTH, 70):
    #     boxes.add(entity.Box(bx, HEIGHT - 35, True))

    # doors = pygame.sprite.Group()
    # doors.add(entity.Locked_door_down(1, 1))
    # doors.add(entity.Locked_door_top(1, 1))

    #plugins.run_hook("on_initialization")


async def main():
    plugins = PluginManager(path="plugins")  # initialize plugin system
    # register hooks
    plugins.register_hook("on_screen_draw")
    plugins.register_hook("on_initialization")

    plugins.search_plugins()  # load plugins from the folder
    plugins.enable_all((WIDTH, HEIGHT))  # plugins started

    init_pygame()
    spawn_initial_entities()
    while True:
        break_now = False
        ### GAME LOOP ###
        pygame.event.pump()

        # Draw loop
        screen.fill(BACKGROUND)
        
        road.draw(screen)
        
        car.draw(screen)
        car.update(WIDTH)
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


asyncio.run(main())