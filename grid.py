import pygame


GRID_COLOR = (127, 127, 127)


class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # 1 is alive, 0 is dead
        self.cells = [[0 for _ in range(self.width // self.cell_size)]
                      for _ in range(self.height // self.cell_size)]
        self.neighbours = [[0 for _ in range(self.width // self.cell_size)]
                           for _ in range(self.height // self.cell_size)]

    def add_cell(self, x, y):
        x //= self.cell_size
        y //= self.cell_size
        self.cells[y][x] = 1

    def remove_cell(self, x, y):
        x //= self.cell_size
        y //= self.cell_size
        self.cells[y][x] = 0

    def update(self):
        # neighbours
        self.neighbours = [[0 for _ in range(self.width // self.cell_size)]
                           for _ in range(self.height // self.cell_size)]
        for y in range(self.height // self.cell_size):
            for x in range(self.width // self.cell_size):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if 0 <= x + i < self.width // self.cell_size and \
                                0 <= y + j < self.height // self.cell_size:
                            if self.cells[y + j][x + i] == 1:
                                self.neighbours[y][x] += 1

        # update cells
        for y in range(self.height // self.cell_size):
            for x in range(self.width // self.cell_size):
                if self.cells[y][x] == 1:
                    if self.neighbours[y][x] < 2 or self.neighbours[y][x] > 3:
                        self.cells[y][x] = 0
                else:
                    if self.neighbours[y][x] == 3:
                        self.cells[y][x] = 1

    def draw(self, surface):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(surface, GRID_COLOR, (0, y), (self.width, y))

        for y in range(self.height // self.cell_size):
            for x in range(self.width // self.cell_size):
                if self.cells[y][x] == 1:
                    pygame.draw.rect(surface, (0, 0, 0),
                                     (x * self.cell_size, y * self.cell_size,
                                      self.cell_size, self.cell_size))

