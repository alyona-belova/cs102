import pathlib
import random

from typing import List, Optional, Tuple


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
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        # Copy from previous assignment
        grid = [[None] * self.cell_width for _ in range(self.cell_height)]
        if randomize != 0:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = random.randint(0, 1)
        else:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = 0
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        row, col = cell
        cells = []
        if col > 0:
            cells.append(self.grid[row][col - 1])
            if row > 0:
                cells.append(self.grid[row - 1][col - 1])
            if row < (self.cell_height - 1):
                cells.append(self.grid[row + 1][col - 1])
        if col < (self.cell_width - 1):
            cells.append(self.grid[row][col + 1])
            if row > 0:
                cells.append(self.grid[row - 1][col + 1])
            if row < (self.cell_height - 1):
                cells.append(self.grid[row + 1][col + 1])
        if row > 0:
            cells.append(self.grid[row - 1][col])
        if row < (self.cell_height - 1):
            cells.append(self.grid[row + 1][col])
        return cells

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        dead = []
        alive = []
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if (sum(self.get_neighbours((i, j))) == 3) and (self.grid[i][j] == 0):
                    alive.append((i, j))
                elif (sum(self.get_neighbours((i, j))) < 2) or (sum(self.get_neighbours((i, j))) > 3):
                    dead.append((i, j))
        for i in alive:
            self.grid[i[0]][i[1]] = 1
        for i in dead:
            self.grid[i[0]][i[1]] = 0
        return self.grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations > self.max_generations:
            return True
        else:
            return False


    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        pass

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        pass

    def save(filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        pass