import asyncio
from plugins import PluginManager
import console
import entity

import pygame, pygame.freetype

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


async def spawn_initial_entities():
    global road, car, obstacles_group, plugins
    road = entity.Road(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT + 16) # spawn road
    car = entity.Car(WIDTH // 2, HEIGHT - (HEIGHT // 3), 64, 96) # spawn car at the bottom center

    obstacles_group = pygame.sprite.Group()
    obstacles_group.add(entity.Person(WIDTH//3*2, 1)) # Spawn person on the 2/3 of width
    obstacles_group.add(entity.Person(WIDTH//3  , 1, value=50)) # spawn person 1/3 width with 50 point value
    await plugins.run_hook("on_init", obstacles_group)


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
    await spawn_initial_entities()
    frame = 0
    while True:
        break_now = False
        ### GAME LOOP ###
        pygame.event.pump()

        # Draw loop
        screen.fill(BACKGROUND)

        if frame % 10 == 0: # once every 10 frames
            road.progress() # scroll road
            road.draw(screen) # we must render the road first otherwise everything will be "under" the road and we will see nothing
            for i in obstacles_group:
                i.progress(8, car) # call progress on everything that is not car or road
            await plugins.run_hook("on_progress", car)
        else:
            road.draw(screen)
            
        obstacles_group.draw(screen) # draw the progressed obstacles
        car.draw(screen)
        car.update(WIDTH)

        score_text, rect = GAME_FONT.render("Score: "+str(car.score), (0, 0, 0))
        screen.blit(score_text, (WIDTH*0.1, HEIGHT*0.05)) # display score in the left bottom corner
        
        await plugins.run_hook("on_screen_draw", screen)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break_now = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    break_now = True
        if break_now:
            break
        frame += 1 # increment the frame counter (we could use this to get FPS)

asyncio.run(main()) # run the main program as async task (we need this if we want to export to WebAssembly)
