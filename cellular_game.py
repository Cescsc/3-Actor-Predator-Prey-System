# Francesc Pei Purroy
# Final Project, Simulation and Modelling


import numpy as np
import tkinter as tk
import random
from time import sleep
from itertools import count

from _Grid import _Grid

WIDTH = 500
HEIGHT = 500
FPS = 10
GRID_LENGTH = 3


class Environment:
    """
    "2D Environment.
    """
    SIZE = 100

    def __init__(self):
        self.grid = self._create_grid()
        self.herds = []
        self.step = count(0, 1)

    def _create_grid(self):
        root = tk.Tk()
        grid = _Grid(
            master=root,
            width=WIDTH,
            height=HEIGHT,
            bg="dark blue",
            grid_len=GRID_LENGTH,
            env_size=self.SIZE
        )
        return grid

    def update(self, skip):
        b = next(self.step) % skip == 0
        if b: self.grid.clear()
        for h in self.herds:
            h.walk()
            if b: h.blit(self.grid)
        self.grid.update()
        sleep(1 / FPS)

    def add_herd(self, herd):
        self.herds.append(herd)


class Creature:
    """
    Parent class to all creatures.
    """

    def __init__(self, color, size=1, speed=1, pos=None):
        # General attributes
        if pos is None:
            pos = [10, 10]
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed

    def walk(self):
        rng = self.rng()
        if rng == 0:
            self.pos[0] += self.speed
        if rng == 1:
            self.pos[0] -= self.speed
        if rng == 2:
            self.pos[1] += self.speed
        if rng == 3:
            self.pos[1] -= self.speed

    def blit_circle(self, grid):
        grid._blit_circle(self)

    @staticmethod
    def rng():
        """Returns 0, 1, 2 or 3 with uniform probability."""
        return int(random.random() * 4)


class Plant(Creature):
    """
    Pathetic.
    """

    def __init__(self, pos):
        speed = 0
        color = "light green"
        super().__init__(color, speed=speed, pos=pos)


class Herbivore(Creature):
    """
    Weaklings.
    """

    def __init__(self, pos):
        speed = self.rng() + 1
        color = "brown"
        super().__init__(color, speed=speed, pos=pos)


class LowPredator(Creature):
    """
    Eats Herbivores.
    """

    def __init__(self, pos):
        speed = self.rng() + 1
        size = 2
        color = "yellow"
        super().__init__(color, speed=speed, pos=pos, size=size)


class Herd:
    """
    List of creatures.
    """

    def __init__(self, ctype, num, env_size=100):
        self.lst = [None] * num
        for i in range(num):
            self.lst[i] = ctype(pos=self.random_pos_dist(env_size))

    def blit(self, grid):
        for e in self.lst:
            e.blit_circle(grid)

    def walk(self):
        for e in self.lst:
            e.walk()

    @staticmethod
    def random_pos_dist(env_size):
        x = int(random.random() * env_size)
        y = int(random.random() * env_size)
        return [x, y]


def main():
    env = Environment()
    herd = Herd(Herbivore, 50)
    pred = Herd(LowPredator, 10)
    env.add_herd(herd)
    env.add_herd(pred)

    loop = True
    while loop:
        env.update(3)
    env.grid.quit()


if __name__ == '__main__':
    main()
