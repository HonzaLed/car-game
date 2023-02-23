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

    def progress(self, pixels):
        self.rect.move_ip([0, pixels])

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Road(Sprite):
    def __init__(self, startx, starty, scalex=1080, scaley=1920):
        super().__init__("road.png", startx, starty, scalex, scaley)
    def progress(self, pixels):
        pass

class Car(Sprite):
    def __init__(self, startx, starty, scalex=70, scaley=70):
        super().__init__("car.png", startx, starty, scalex, scaley)
        self.still_image = self.image
        
        # self.left_image  = load_image("car_left.png",  self.scalex, self.scaley)
        # self.right_image = load_image("car_right.png", self.scalex, self.scaley)

        self.speed = 4
        # self.prev_key = pygame.key.get_pressed()

    def update(self, width):
        # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            #self.image = self.left_image
            self.move(-self.speed, 0, width)
        elif key[pygame.K_RIGHT]:
            #self.image = self.right_image
            self.move(self.speed, 0, width)
        else:
            self.image = self.still_image

    def move(self, x, y, width): # move local (from current coords)
        globalx = self.rect.x + x
        if (not globalx < 0) and (not globalx+self.rect[2]-1 > width):
            self.rect.move_ip([x, y])

    def tp(self, x, y): # teleport (move global)
        self.rect.move([x, y])

    def check_collision(self, x, y, group):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, group)
        self.rect.move_ip([-x, -y])
        return collide
    def progress(self, pixels):
        pass


class Box(Sprite):
    def __init__(self, startx, starty, coords=False):
        if not coords:
            super().__init__("box.png", 35+(70*startx), 35+(70*starty))
        else:
            super().__init__("box.png", startx, starty)
