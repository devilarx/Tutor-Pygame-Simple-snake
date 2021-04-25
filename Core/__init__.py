import random
from itertools import product
from enum import Enum
import pygame.draw


class GameState(Enum):
    CONTINUE = 0,
    WIN = 1,
    LOSE = 2


class SnakeDirection(Enum):
    ERROR_DIRECTION = 0
    UP = 1
    LEFT = 2
    DOWN = -1
    RIGHT = -2


class CellType(Enum):
    EMPTY = 0
    SNAKE = 1
    SNAKE_HEAD = 2
    FOOD = 3
    WALL = 4


COLOR_SNAKE_HEAD = (153, 250, 255)
COLOR_SNAKE = (68, 133, 143)
COLOR_EMPTY = (183, 191, 178)
COLOR_WALL = (0, 0, 0)
COLOR_APPLE = (232, 44, 44)
COLOR_ERROR = (0, 0, 255)


class Game:
    def __init__(self, width: int, height: int, b_size: int):
        self.field = None
        self.width = width
        self.height = height
        self.b_size = b_size

    def create(self):
        self.field = Field(self.width, self.height)
        self.field.generate()

    def update(self) -> GameState:
        hx, hy = self.field.snake.get_head()
        x, y = self.field.snake.get_next_position()
        is_empty = self.field.is_empty(x, y)
        is_food = self.field.is_food(x, y)
        last_position = self.field.snake.move()
        self.field.set_cell(hx, hy, CellType.SNAKE)
        hx, hy = self.field.snake.get_head()
        self.field.set_cell(hx, hy, CellType.SNAKE_HEAD)
        if is_empty:
            self.field.empty_cells.remove((hx,hy))
        self.field.set_cell(last_position[0], last_position[1], CellType.EMPTY)
        self.field.empty_cells.append(last_position)
        if is_empty:
            return GameState.CONTINUE
        if is_food:
            self.field.snake.grow()
            state = self.field.regenerate_food()
            if state:
                return GameState.CONTINUE
            else:
                return GameState.WIN
        return GameState.LOSE

    def change_direction(self, direct: SnakeDirection):
        self.field.snake.change_direction(direct)

    def draw(self, display):
        for y in range(self.height):
            for x in range(self.width):
                c_type = self.field.get_cell(x, y)
                sx = x*(self.b_size+2)
                csx = sx+1
                sy = y*(self.b_size+2)
                csy = sy + 1
                if c_type == CellType.EMPTY:
                    color = COLOR_EMPTY
                elif c_type == CellType.SNAKE_HEAD:
                    color = COLOR_SNAKE_HEAD
                elif c_type == CellType.SNAKE:
                    color = COLOR_SNAKE
                elif c_type == CellType.WALL:
                    color = COLOR_WALL
                elif c_type == CellType.FOOD:
                    color = COLOR_APPLE
                else:
                    color = COLOR_ERROR
                pygame.draw.rect(display, color, [csx, csy, self.b_size, self.b_size])


class Field:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.__clear()
        self.snake = None
        self.food_coord = None
        self.cells = []
        self.empty_cells = []

    def generate(self):
        self.cells = []
        for i in range(self.height):
            self.cells.append([])
            for j in range(self.width):
                self.cells[i].append(CellType.EMPTY)
                self.empty_cells.append((j, i))

        self.snake = Snake(self.width, self.height, random.randint(0, self.width-1), random.randint(0, self.height-1))
        hx, hy = self.snake.get_head()
        self.set_cell(hx, hy, CellType.SNAKE_HEAD)
        self.regenerate_food()
        self.set_cell(self.food_coord[0], self.food_coord[1], CellType.FOOD)
        self.empty_cells.remove((hx, hy))

    def regenerate_food(self) -> bool:
        e_cells = self.__get_empty_cells()
        if len(e_cells) == 0:
            return False
        self.food_coord = e_cells[random.randint(0, len(e_cells)-1)]
        self.set_cell(self.food_coord[0], self.food_coord[1], CellType.FOOD)
        self.empty_cells.remove(self.food_coord)
        return True

    def is_empty(self, x, y):
        return self.get_cell(x, y) == CellType.EMPTY

    def is_food(self, x, y):
        return self.get_cell(x, y) == CellType.FOOD

    def __clear(self):
        self.field = []
        for i in range(self.height):
            self.field.append([])
            for j in range(self.width):
                self.field[i].append(CellType.EMPTY)

    def set_cell(self, x: int, y: int, c_type: CellType):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = c_type

    def get_cell(self, x: int, y: int) -> CellType:
        return self.cells[y][x]

    def __get_empty_cells(self):
        return self.empty_cells.copy()


class Snake:
    def __init__(self, width: int, height: int, s_x: int, s_y: int):
        self.direction = SnakeDirection.UP
        self.f_width = width
        self.f_height = height
        self.cells = [(s_x, s_y)]

    def change_direction(self, new_direct: SnakeDirection):
        if self.direction.value + new_direct.value != 0:
            self.direction = new_direct

    def grow(self):
        self.cells.append(self.cells[-1])

    def get_next_position(self):
        x, y = self.cells[0]
        if self.direction == SnakeDirection.UP:
            if y == 0:
                y = self.f_height - 1
            else:
                y -= 1
        elif self.direction == SnakeDirection.DOWN:
            if y == self.f_height - 1:
                y = 0
            else:
                y += 1
        if self.direction == SnakeDirection.LEFT:
            if x == 0:
                x = self.f_width - 1
            else:
                x -= 1
        elif self.direction == SnakeDirection.RIGHT:
            if x == self.f_width - 1:
                x = 0
            else:
                x += 1
        return x, y

    def move(self) -> (int, int):
        prev_cell = None
        for i in range(len(self.cells)):
            if prev_cell is None:
                x, y = self.get_next_position()
                prev_cell = self.cells[i]
                self.cells[i] = (x, y)
            else:
                self.cells[i], prev_cell = prev_cell, self.cells[i]
        return prev_cell

    def get_coords(self) -> [(int, int)]:
        return self.cells.copy()

    def get_head(self) -> (int, int):
        return self.cells[0]
