# Francesc Pei Purroy
# Final Project, Simulation and Modelling


import numpy as np
import random
from time import sleep
from itertools import count

from Grid import Grid

FPS = 10
SIZE = 20


class Environment:
    """
    "2D Environment.
    """

    class Matrix:
        def __init__(self):
            self.mat = [[] for _ in range(SIZE)]
            for i in range(SIZE):
                self.mat[i] = [list() for _ in range(SIZE)]

        def _clear(self):
            self.__init__()

    def __init__(self):
        self.grid = self.create_grid()

        self.matrix = self.matrix_init()

        self.herds = []
        self.step = count(0, 1)

    @staticmethod
    def matrix_init():
        mat = [[] for _ in range(SIZE)]
        for i in range(SIZE):
            mat[i] = [list() for _ in range(SIZE)]
        return mat

    def update_matrix(self):
        self.matrix = self.matrix_init()
        for herd in self.herds:
            herd.add_grid_pos(self.matrix)

    @staticmethod
    def create_grid():
        grid = Grid(
            bg="white",
            env_size=SIZE
        )
        return grid

    def update(self, skip):
        if skip == 0:
            b = 1
        else:
            b = (next(self.step) % skip == 0)

        if b:
            self.grid.clear()
        for h in self.herds:
            h.update()
            if b:
                h.blit(self.grid)

        self.update_matrix()
        self.game_check()

        self.grid.update()
        sleep(1 / FPS)

    def add_herd(self, herd):
        self.herds.append(herd)

    def game_check(self):
        for r in range(SIZE):
            for c in range(SIZE):
                temp = self.matrix[r][c]
                if len(temp) < 2:
                    continue
                else:
                    max_p = max([crea.priority for crea in temp])
                    predators = []
                    nutri_gain = []
                    for crea in temp:
                        if crea.priority == max_p:
                            predators.append(crea)
                        else:
                            nutri_gain.append(crea.nutri)
                            crea.die()
                    nutri_split = sum(nutri_gain)//len(predators)
                    for pred in predators:
                        pred.hunger += nutri_split


class Creature:
    """
    Parent class to all creatures.
    """
    DEPLETION = 2

    def __init__(
            self,
            color,
            priority,
            herd,
            regen,
            nutri,
            size=1,
            speed=1,
            pos=None
    ):
        # General attributes
        if pos is None:
            pos = [10, 10]
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed
        self.priority = priority
        self.herd = herd
        self.hunger = 100  # Current hunger value
        self.regen = regen  # Passive hunger regeneration
        self.nutri = nutri  # Hunger points given when eaten

    def die(self):
        if self in self.herd:
            self.herd.remove(self)

    def life_update(self):
        self.hunger += self.regen - self.DEPLETION
        if self.hunger <= 0:
            self.die()

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


class Herbivore(Creature):
    """
    Weaklings.
    """

    def __init__(self, pos, herd):
        speed = 1
        color = "grey"
        priority = 0
        regen = 1
        nutri = 50
        super().__init__(
            color,
            priority=priority,
            herd=herd,
            regen=regen,
            nutri=nutri,
            speed=speed,
            pos=pos
        )


class LowPredator(Creature):
    """
    Eats Herbivores.
    """

    def __init__(self, pos, herd):
        speed = 1
        size = 2
        color = "black"
        priority = 1
        regen = 0
        nutri = 100
        super().__init__(
            color,
            priority=priority,
            herd=herd,
            regen=regen,
            nutri=nutri,
            speed=speed,
            pos=pos,
            size=size
        )


class Herd:
    """
    List of creatures.
    """

    def __init__(self, ctype, num, env_size=SIZE):
        self.lst = [None] * num
        for i in range(num):
            self.lst[i] = ctype(pos=self.random_pos_dist(env_size), herd=self.lst)

    def add_grid_pos(self, matrix):
        for creature in self.lst:
            matrix[creature.pos[0]][creature.pos[1]].append(creature)

    def blit(self, grid):
        for e in self.lst:
            e.blit(grid)

    def update(self):
        for e in self.lst:
            e.walk()
            e.life_update()

    @staticmethod
    def random_pos_dist(env_size):
        x = int(random.random() * env_size)
        y = int(random.random() * env_size)
        return [x, y]


def main():
    env = Environment()
    herd = Herd(Herbivore, 20)
    pred = Herd(LowPredator, 20)
    env.add_herd(herd)
    env.add_herd(pred)

    loop = True
    while loop:
        env.update(2)
    env.grid.quit()


if __name__ == '__main__':
    main()
