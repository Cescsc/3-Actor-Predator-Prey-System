# Francesc Pei Purroy
# Final Project, Simulation and Modelling


import numpy as np
import random
from time import sleep
from itertools import count

from Grid import Grid

FPS = 10
SIZE = 50


class Environment:
    """
    "2D Environment.
    """

    class Matrix:
        def __init__(self):
            self.mat = np.zeros(shape=(SIZE, SIZE)).tolist()

        def _clear(self):
            self.__init__()

        def update(self):
            for row in range(SIZE):
                for col in range(SIZE):
                    self.mat[row,col]
            self._clear()

    def __init__(self):
        self.grid = self.create_grid()

        self.env = self.Matrix()

        self.herds = []
        self.step = count(0, 1)

    @staticmethod
    def create_grid():
        grid = Grid(
            bg="white",
            env_size=SIZE
        )
        return grid

    def update(self, skip):
        b = next(self.step) % skip == 0

        if b: self.grid.clear()
        for h in self.herds:
            h.walk()
            if b: h.blit(self.grid)

        self.game_check()

        self.grid.update()
        sleep(1 / FPS)

    def add_herd(self, herd):
        self.herds.append(herd)

    def game_check(self):
        pass


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

        self.pos[0] %= SIZE
        self.pos[1] %= SIZE

    def blit(self, grid):
        grid.blit_rect(self)

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
        speed = 1
        color = "grey"
        super().__init__(color, speed=speed, pos=pos)

        self.priority = 1


class LowPredator(Creature):
    """
    Eats Herbivores.
    """

    def __init__(self, pos):
        speed = 1
        size = 2
        color = "black"
        super().__init__(color, speed=speed, pos=pos, size=size)

        self.priority = 2


class Herd:
    """
    List of creatures.
    """

    def __init__(self, ctype, num, matrix, env_size=SIZE):
        self.lst = [None] * num
        self.matrix = matrix
        for i in range(num):
            self.lst[i] = ctype(pos=self.random_pos_dist(env_size))

    def update_grid_pos(self):
        for creature in self.lst:
            for r in range(SIZE):
                for c in range(SIZE):
                    self.matrix[r,c].append(creature)

    def blit(self, grid):
        for e in self.lst:
            e.blit(grid)

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
    herd = Herd(Herbivore, 20)
    pred = Herd(LowPredator, 10)
    env.add_herd(herd)
    env.add_herd(pred)

    loop = True
    while loop:
        env.update(1)
    env.grid.quit()


if __name__ == '__main__':
    main()
