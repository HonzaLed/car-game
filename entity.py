import pygame
import random
import numpy


def get_image_path(image):
    return "./assets/tiles/" + image
def load_image(image, scalex, scaley):
    return pygame.transform.scale( pygame.image.load(get_image_path(image)), (scalex, scaley) )

class Sprite(pygame.sprite.Sprite): # Helper class
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
        self.scrolled = False

    def progress(self): # "scrolls" back and forward, thus creating an infinite scrolling effect
        if self.scrolled:
            self.move(0, 8)
        else:
            self.move(0, -8)
        self.scrolled = not self.scrolled

    def move(self, x, y):  # move local (from current coords)
        self.rect.move_ip([x, y])

class Person(Sprite):
    def __init__(self, startx, starty, scalex=39, scaley=60, images=["person1.png"], value=1, multiplier=1):
        super().__init__(random.choice(images), startx, starty, scalex, scaley)
        self.value = value # point value of this person
        self.multiplier = multiplier
        
    def progress(self, pixels, car):
        self.move(0,8) # move down
        if self.check_collision(car): # if coolliding with the car, add score and kill self
            car.score += self.value
            car.score *= self.multiplier
            self.kill()
            return
        
        
    def move(self, x, y):  # move local (from current coords)
        self.rect.move_ip([x, y])
            
    def check_collision(self, rect):
        return self.rect.colliderect(rect.rect)

class Car(Sprite):
    def __init__(self, startx, starty, scalex=70, scaley=70):
        super().__init__("car.png", startx, starty, scalex, scaley)
        self.still_image = self.image
        self.speed = 4
        self.score = 0

        # we could add images for going left and right
        # self.left_image  = load_image("car_left.png",  self.scalex, self.scaley)
        # self.right_image = load_image("car_right.png", self.scalex, self.scaley)

    def update(self, width):
        # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            #self.image = self.left_image
            self.move(-self.speed, 0, width) # move left
        elif key[pygame.K_RIGHT]:
            #self.image = self.right_image
            self.move(self.speed, 0, width) # move right
        else:
            self.image = self.still_image

    def move(self, x, y, width):  # move local (from current coords)
        globalx = self.rect.x + x
        if (not globalx < 0) and (not globalx + self.rect[2] - 1 > width): # check if not at the left/right boundary
            self.rect.move_ip([x, y])

    def tp(self, x, y):  # teleport (move global)
        self.rect.move([x, y])

    def check_collision(self, x, y, group):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, group)
        self.rect.move_ip([-x, -y])
        return collide

    def progress(self, pixels):
        pass # has no progress functionality
