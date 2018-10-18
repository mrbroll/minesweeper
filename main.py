from argparse import ArgumentParser
import random
from sys import (stdin, stdout)

class Board(object):
    def __init__(self, width, height, bomb_count=None, test=False):
        self.test = test
        # cover 1/3 of the board with bombs
        bomb_count = bomb_count or int((width * height) / 3)
        bombs = [BoardCell(is_bomb=True) for _ in range(bomb_count)]
        non_bombs = [BoardCell() for _ in range((width * height) - bomb_count)]
        board_1d = bombs + non_bombs
        random.shuffle(board_1d)
        self.board = [[board_1d[(i * width) + j] for j in range(width)] for i in range(height)]
        # mark adjacents
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                # search each adjacent cell
                if cell.is_bomb:
                    continue
                adjacent_bombs = 0
                for dx, dy in [(i, j) for j in range(-1, 2) for i in range(-1, 2)]:
                    if dx == 0 and dy == 0:
                        continue
                    if (0 <= (y + dy) < height) and (0 <= (x + dx) < width) and self.board[y+dy][x+dx].is_bomb:
                        adjacent_bombs += 1

                self.board[y][x].set_adjacent_bombs(adjacent_bombs)

        self.exploded = False

    def display(self):
        for row in self.board:
            for cell in row:
                if self.test:
                    stdout.write(cell.char)
                else:
                    stdout.write(cell.display())
            stdout.write('\n')

    def uncover_cell(self, x, y):
        if not self.board[y][x].uncover():
            self.exploded = True

    def flag_cell(self, x, y):
        self.board[y][x].flag()


class BoardCell(object):
    def __init__(self, adjacent_bombs=0, is_bomb=False):
        self.is_bomb = is_bomb
        self.char = '*' if is_bomb else str(adjacent_bombs)
        self.uncovered = False
        self.flagged = False

    def set_adjacent_bombs(self, num_bombs):
        self.char = str(num_bombs)

    def flag(self):
        self.flagged = True

    def unflag(self):
        self.flagged = False
        
    def display(self):
        if self.flagged:
            return 'F'
        elif self.uncovered:
            return self.char
        return '#'

    def uncover(self):
        self.uncovered = True
        self.flagged = False
        return not self.char == '*'


def main():
    parser = ArgumentParser(description='CLI Minesweeper')
    parser.add_argument('--test', dest='test', default=False, action='store_true')
    args = parser.parse_args()

    # initialize board
    stdout.write("Welcome to Minesweeper\n")
    stdout.write("Please enter a board width: \n")
    width = int(stdin.readline())
    stdout.write("Please enter a board heght: \n")
    height = int(stdin.readline())

    # build board
    board = Board(width, height, test=args.test)
    board.display()

    # main game loop
    while not board.exploded:
        stdout.write("U X Y to reveal, F X Y to flag:\n")
        # TODO: validate input
        [command, x, y] = stdin.readline().split(' ')
        x, y = int(x), int(y)
        if command == 'U':
            board.uncover_cell(x, y)
        elif command == 'F':
            board.flag_cell(x, y)

        board.display()


if __name__ == '__main__':
    main()
