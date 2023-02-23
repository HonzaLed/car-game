import pygame
import numpy

def get_image_path(image):
    return "./assets/tiles/"+image
def load_image(image, scalex, scaley):
    return pygame.transform.scale(pygame.image.load(get_image_path(image)), (scalex, scaley))

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty, scalex=70, scaley=70):
        super().__init__()
        self.scalex = scalex
        self.scaley = scaley

        self.image = load_image(image, self.scalex, self.scaley)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Locked_door_down(Sprite):
    def __init__(self, startx, starty, scalex=70, scaley=70):
        coordsx = 35+(startx*70)
        coordsy = 35+(starty*70)
        super().__init__("locked_door_down.png", coordsx, coordsy)

class Locked_door_top(Sprite):
    def __init__(self, startx, starty, scalex=70, scaley=70):
        coordsx = 35+(startx*70)
        coordsy = 35+(starty*70)
        super().__init__("locked_door_top.png", coordsx, coordsy-70)

class Road(Sprite):
    def __init__(self, startx, starty, scalex=1080, scaley=1920):
        super().__init__("road.png", startx, starty, scalex, scaley)
# class Locked_door(Sprite):
#     def __init__(self, startx, starty, scalex=70, scaley=70):
#         self.scalex = scalex
#         self.scaley = scaley

#         self.image_down = load_image("locked_door_down.png", self.scalex, self.scaley)
#         self.image_top  = load_image("locked_door_top.png",  self.scalex, self.scaley)

#         self.rect_down = self.image_down.get_rect()
#         self.rect_top  = self.image_top .get_rect()

#         coordsx = 35+(startx*70)
#         coordsy = 35+(starty*70)
#         self.rect_down.center = [coordsx, coordsy]
#         self.rect_top .center = [coordsx, coordsy-70]

#     def update(self):
#         pass

#     def draw(self, screen):
#         screen.blit(self.image_down, self.rect_down)
#         screen.blit(self.image_top,  self.rect_top)

class Car(Sprite):
    def __init__(self, startx, starty, scalex=70, scaley=70):
        super().__init__("p_front.png", startx, starty, scalex, scaley)
        self.stand_image = self.image
        self.jump_image = load_image("p_jump.png", self.scalex, self.scaley)

        self.walk_cycle = [load_image(f"p_walk{i:0>2}.png", self.scalex, self.scaley) for i in range(1,2)] # pygame.image.load(get_image_path(f"p_walk{i:0>2}.png")) 
        self.animation_index = 0
        self.facing_left = False

        self.speed = 4
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 1
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, boxes):
        hsp = 0
        onground = self.check_collision(0, 1, boxes)
        # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            hsp = self.speed
        else:
            self.image = self.stand_image

        if key[pygame.K_UP] and onground:
            self.vsp = -self.jumpspeed

        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = key

        # gravity
        if self.vsp < 10 and not onground:  # 9.8 rounded up
            self.jump_animation()
            self.vsp += self.gravity

        if onground and self.vsp > 0:
            self.vsp = 0

        # movement
        self.move(hsp, self.vsp, boxes)

    def move(self, x, y, boxes): # move local (from current coords)
        dx = x
        dy = y

        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])

    def tp(self, x, y, boxes): # teleport (move global)
        dx = x
        dy = y

        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)

        self.rect.move([dx, dy])

    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide


class Box(Sprite):
    def __init__(self, startx, starty, coords=False):
        if not coords:
            super().__init__("box.png", 35+(70*startx), 35+(70*starty))
        else:
            super().__init__("box.png", startx, starty)
