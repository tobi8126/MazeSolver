import random
import time
from typing import List

from cell import Cell
from graphics import Window, Point


class Maze:
    def __init__(
            self,
            x1: int,
            y1: int,
            num_rows: int,
            num_cols: int,
            cell_size_x: float,
            cell_size_y: float,
            win: Window = None,
            seed : int = None
            ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        if seed is not None: random.seed(seed)

        self.__cells: list[list[Cell]] = [[Cell(self.__win) for _ in range(num_rows)] for _ in range(num_cols)]
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range (self.__num_cols):
            for j in range (self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i: int, j: int):
        x1 = self.__x1 + (i * self.__cell_size_x)
        y1 = self.__y1 + (j * self.__cell_size_y)
        self.__cells[i][j].draw(x1*1.1, y1*1.1, x1*1.1 + self.__cell_size_x, y1*1.1 + self.__cell_size_y)
        self.__animate()

    def __animate(self):
        if self.__win is not None: self.__win.redraw()
        time.sleep(0.005)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols-1][self.__num_rows-1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols-1, self.__num_rows-1)

    def __break_walls_r(self, i, j):

        self.__cells[i][j].visited = True

        while True:
            open_ways = []
            if i > 0 and not self.__cells[i-1][j].visited:
                open_ways.append(Point(i-1, j))
            if j > 0 and not self.__cells[i][j-1].visited:
                open_ways.append(Point(i, j-1))
            if i < self.__num_cols-1 and not self.__cells[i+1][j].visited:
                open_ways.append(Point(i+1, j))
            if j < self.__num_rows-1 and not self.__cells[i][j+1].visited:
                open_ways.append(Point(i, j+1))


            if len(open_ways) == 0:
                self.__draw_cell(i, j)
                return

            point = open_ways[random.randint(0, len(open_ways)-1)]

            if point.x < i:
                self.__cells[i][j].has_left_wall = False
                self.__cells[point.x][point.y].has_right_wall = False

            elif point.x > i:
                self.__cells[i][j].has_right_wall = False
                self.__cells[point.x][point.y].has_left_wall = False

            elif point.y < j:
                self.__cells[i][j].has_top_wall = False
                self.__cells[point.x][point.y].has_bottom_wall = False

            elif point.y > j:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[point.x][point.y].has_top_wall = False

            self.__draw_cell(i, j)

            self.__break_walls_r(point.x, point.y)

    def __reset_cells_visited(self):
        for i in range (self.__num_cols):
            for j in range (self.__num_rows):
                self.__cells[i][j].visited = False

    def solve(self):
        print(self._solve_r(0, 0))

    def _solve_r(self, i, j):
        self.__animate()
        self.__cells[i][j].visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        # LINKS
        if i > 0 and not self.__cells[i - 1][j].visited and not self.__cells[i][j].has_left_wall and not \
        self.__cells[i - 1][j].has_right_wall:
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                # Wird NUR ausgeführt, wenn der Weg nach links eine Sackgasse war.
                # Zeichnet exakt diese Linie sofort wieder grau.
                self.__cells[i][j].draw_move(self.__cells[i - 1][j], True)

        # OBEN
        if j > 0 and not self.__cells[i][j - 1].visited and not self.__cells[i][j].has_top_wall and not \
        self.__cells[i][j - 1].has_bottom_wall:
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j - 1], True)

        # RECHTS
        if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited and not self.__cells[i][
            j].has_right_wall and not self.__cells[i + 1][j].has_left_wall:
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i + 1][j], True)

        # UNTEN
        if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited and not self.__cells[i][
            j].has_bottom_wall and not self.__cells[i][j + 1].has_top_wall:
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j + 1], True)

        # Wenn kein Weg zum Ziel geführt hat, gebe False zurück,
        # damit die vorherige Zelle ihren else-Block ausführt.
        return False