import pathlib
import random

from typing import List, Optional, Tuple
from copy import deepcopy

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        grid = [[None] * self.cols for _ in range(self.rows)]
        if randomize != 0:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = 0
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        cells = []
        if col > 0:
            cells.append(self.curr_generation[row][col - 1])
            if row > 0:
                cells.append(self.curr_generation[row - 1][col - 1])
            if row < (self.rows - 1):
                cells.append(self.curr_generation[row + 1][col - 1])
        if col < (self.cols - 1):
            cells.append(self.curr_generation[row][col + 1])
            if row > 0:
                cells.append(self.curr_generation[row - 1][col + 1])
            if row < (self.rows - 1):
                cells.append(self.curr_generation[row + 1][col + 1])
        if row > 0:
            cells.append(self.curr_generation[row - 1][col])
        if row < (self.rows - 1):
            cells.append(self.curr_generation[row + 1][col])
        return cells

    def get_next_generation(self) -> Grid:
        grid = deepcopy(self.curr_generation)
        dead = []
        alive = []
        for i in range(self.rows):
            for j in range(self.cols):
                if (sum(self.get_neighbours((i, j))) == 3) and (self.curr_generation[i][j] == 0):
                    alive.append((i, j))
                elif (sum(self.get_neighbours((i, j))) < 2) or (sum(self.get_neighbours((i, j))) > 3):
                    dead.append((i, j))
        for i in alive:
            grid[i[0]][i[1]] = 1
        for i in dead:
            grid[i[0]][i[1]] = 0
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.n_generation >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation != self.prev_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename, 'r')
        ln = f.readlines()
        for i in range(len(ln)):
            ln[i].strip()
            for j in range(len(ln[0].strip())):
                GameOfLife((len(ln), len(ln[0].strip())), False).curr_generation[i][j] = int(ln[i][j])
        f.close()
        return GameOfLife

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, 'w')
        for row in self.curr_generation:
            for ch in row:
                f.write(''.join(str(ch)) + '\n')
        f.close()
