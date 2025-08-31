from __future__ import annotations
from typing import Tuple, List

import random
from enum import Enum

from constants import *
from utils import *


class CellState(Enum):
    OPENED = 0
    CLOSED = 1
    FLAGGED = 2

class Cell:
    __state: CellState = CellState.CLOSED

    __game: Minesweeper
    __position: Tuple[int, int]
    __has_mine: bool = False

    @property
    def state(self) -> CellState:
        return self.__state

    @property
    def is_opened(self) -> bool:
        return self.__state == CellState.OPENED
    
    @property
    def is_flagged(self) -> bool:
        return self.__state == CellState.FLAGGED

    def set_opened(self):
        self.__state = CellState.OPENED

    @property
    def game(self) -> Minesweeper:
        return self.__game

    @property
    def x(self) -> int:
        return self.__position[0]

    @property
    def y(self) -> int:
        return self.__position[1]

    @property
    def has_mine(self) -> bool:
        return self.__has_mine

    def add_mine(self):
        self.__has_mine = True

    @property
    def is_safe(self) -> bool:
        return not self.__has_mine

    @property
    def mines(self) -> int:
        mines = 0
        for direction in DIRECTIONS:
            _x = self.x + direction[0]
            _y = self.y + direction[1]
            cell = self.game.get_cell(_x, _y)
            if cell != None and cell.has_mine:
                mines += 1
        return mines

    def __init__(self, game: Minesweeper, x: int, y: int):
        self.__position = (x, y)
        self.__game = game

    def set_flagged(self):
        self.__state = CellState.FLAGGED if self.state == CellState.CLOSED else CellState.CLOSED

    def get_char(self) -> str:
        state = self.__state
        if self.state == CellState.CLOSED:
            return TILE_UNKNOWN
        if self.state == CellState.FLAGGED:
            if self.game.is_exploded and self.is_safe:
                return TILE_WRONGFLAG
            return TILE_FLAG
        if self.state == CellState.OPENED:
            if self.has_mine:
                return TILE_EXPLODED if self.game.is_exploded else TILE_MINE
            return TILES[self.mines]
        raise Exception()


class Minesweeper:
    width: int
    height: int
    mines: int

    __cells: List[Cell] = []
    __mines: List[Cell] = []

    __flag_count: int = 0
    __is_first_click: bool = True
    __is_exploded: bool = False

    @property
    def flag_count(self) -> int:
        return self.__flag_count

    @property
    def mine_count(self) -> int:
        return self.mines - self.flag_count

    @property
    def is_fisrt_click(self) -> bool:
        return self.__is_first_click

    @property
    def is_exploded(self) -> bool:
        return self.__is_exploded
    
    @property
    def is_win(self) -> bool:
        ...

    def __init__(self, width: int, height: int, mines: int):
        self.width = width
        self.height = height
        self.mines = mines

        for x in range(self.width):
            for y in range(self.height):
                self.__cells.append(Cell(self, x, y))

    @show_latency
    def init_mines(self, x: int, y: int):
        n = 0
        while n < self.mines:
            cell = random.choice(self.__cells)
            if cell.has_mine:
                continue
            if not (x - 1 <= cell.x < x + 2 and y - 1 <= cell.y < y + 2):
                cell.add_mine()
                self.__mines.append(cell)
                n += 1
                debug("add mine at", cell.x, cell.y)

    # @show_latency
    # def display(self):
    #     rows = [[' ' for x in range(self.width)] for y in range(self.height)]
    #     for cell in self.__cells:
    #         rows[cell.y][cell.x] = cell.get_char()
    #     for row in rows:
    #         print("".join(row))

    def foreach_cell(self, func: Callable):
        for cell in self.__cells:
            func(cell=cell)

    def open_at(self, x: int, y: int):
        cell = self.get_cell(x, y)
        if cell != None:
            if cell.is_opened or cell.is_flagged:
                return
            if self.is_fisrt_click:
                self.init_mines(x, y)
                self.__is_first_click = False
            if cell.has_mine:
                self.__is_exploded = True
                self.showall_mines()
                return
                # TODO: Handle when get exploded
            cell.set_opened()
            if cell.mines == 0:
                for direction in DIRECTIONS:
                    _x = x + direction[0]
                    _y = y + direction[1]

                    if 0 <= _x < self.width and 0 <= _y < self.height:
                        self.open_at(_x, _y)

    # TODO: Auto flagged
    # def update_mines(self):
    #     for mine in self._mines:
    #         for direction in DIRECTIONS:
    #             _x = mine.x + direction[0]
    #             _y = mine.y + direction[1]
    #             _b = False
    #             _m = 1
    #             if 0 <= _x < self.width and 0 <= _y < self.height:
    #                 cell = self.get_cell(_x, _y)
    #                 if cell != None and not cell.is_safe:
    #                     _b = True

    def flag_at(self, x: int, y: int):
        cell = self.get_cell(x, y)
        if cell != None:
            cell.set_flagged()
            
        self.__flag_count = 0
        
        def func(cell: Cell):
            if cell.is_flagged:
                self.__flag_count += 1
        self.foreach_cell(func)

    def get_cell(self, x: int, y: int):
        for cell in self.__cells:
            if cell.x == x and cell.y == y:
                return cell
        return None

    def showall_mines(self):
        for mine in self.__mines:
            if mine.is_flagged:
                continue
            mine.set_opened()

    @staticmethod
    def init_from_level(level: Level) -> Minesweeper:
        return Minesweeper(level.width, level.height, level.mines)


class Level:
    __width: int
    __height: int
    __mines: int

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def mines(self) -> int:
        return self.__mines

    def __init__(self, width: int, height: int, mines: int) -> None:
        self.__width = width
        self.__height = height
        self.__mines = mines


class Levels:
    BEGINER = Level(9, 9, 10)
    INTERMEDIATE = Level(16, 16, 40)
    EXPERT = Level(30, 16, 99)
    IMPOSSIBLE = Level(60, 30, 399)
    SO_FUCKING_IMPOSSIBLE = Level(165, 30, 990)


class Game: ...
