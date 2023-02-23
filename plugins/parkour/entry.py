from plugins import PluginTemplate, on_initialization
from random import randint
from entity import Box

class parkour(PluginTemplate):
    def enable(self, size):
        super().enable()
        self.WIDTH  = size[0]
        self.HEIGHT = size[1]

    @on_initialization
    def func_on_initialization(self, boxes):
        for i in range(35):
            x = randint(1, 18)
            y = randint(1, 10)
            if x == 9 and y == 9:
                continue
            boxes.add(Box(x, y))