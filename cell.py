from graphics import Line, Point, Window

class Cell:
    def __init__(self, win: Window = None):
        self.__win = win
        self.has_left_wall, self.has_right_wall, self.has_top_wall, self.has_bottom_wall = True, True, True, True
        self.__x1, self.__x2, self.__y1, self.__y2 = -1.0, -1.0, -1.0, -1.0
        self.visited = False

    def draw(self, x1: float, y1: float, x2: float, y2: float, fill_color : str = "black"):
        self.__x1, self.__x2, self.__y1, self.__y2 = x1, x2, y1, y2

        line = Line(Point(x1, y1), Point(x1, y2))
        if self.__win is not None: self.__win.draw_line(line, fill_color if self.has_left_wall else "#d9d9d9")


        line = Line(Point(x2, y1), Point(x2, y2))
        if self.__win is not None: self.__win.draw_line(line, fill_color if self.has_right_wall else "#d9d9d9")


        line = Line(Point(x1, y1), Point(x2, y1))
        if self.__win is not None: self.__win.draw_line(line, fill_color if self.has_top_wall else "#d9d9d9")


        line = Line(Point(x1, y2), Point(x2, y2))
        if self.__win is not None: self.__win.draw_line(line, fill_color if self.has_bottom_wall else "#d9d9d9")

    def draw_move(self, to_cell: Cell, undo: bool = False):
        color = "red"
        if undo: color = "gray"

        p1 = Point(self.__x1 + (self.__x2 - self.__x1) / 2 ,self.__y1 + (self.__y2 - self.__y1) / 2)
        p2 = Point(to_cell.__x1 + (to_cell.__x2 - to_cell.__x1) / 2 ,to_cell.__y1 + (to_cell.__y2 - to_cell.__y1) / 2)

        if self.__win is not None: self.__win.draw_line(Line(p1, p2), color)