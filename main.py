from maze import Maze
from graphics import Window

def main():
    win = Window(800, 600)

    maze = Maze(10, 10, 25, 25, 15, 15, win)
    maze.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()