import pygame
import time
pygame.font.init()


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
        self._rows = rows
        self._cols = cols
        self._cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self._width = width
        self._height = height
        self._model = None
        self.update_model()
        self._selected = None
        self._win = win

    def update_model(self):
        self._model = [[self._cubes[i][j]._value for j in range(self._cols)] for i in range(self._rows)]

    def place(self, val):
        row, col = self._selected
        if self._cubes[row][col]._value == 0:
            self._cubes[row][col].set(val)
            self.update_model()

            if valid(self._model, val, (row, col)) and self.solve():
                return True
            else:
                self._cubes[row][col].set(0)
                self._cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self._selected
        self._cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self._width / 9
        for i in range(self._rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self._win, (0, 0, 0), (0, i*gap), (self._width, i*gap), thick)
            pygame.draw.line(self._win, (0, 0, 0), (i * gap, 0), (i * gap, self._height), thick)

        # Draw Cubes
        for i in range(self._rows):
            for j in range(self._cols):
                self._cubes[i][j].draw(self._win)

    def select(self, row, col):
        # Reset all other
        for i in range(self._rows):
            for j in range(self._cols):
                self._cubes[i][j]._selected = False

        self._cubes[row][col]._selected = True
        self._selected = (row, col)

    def clear(self):
        row, col = self._selected
        if self._cubes[row][col]._value == 0:
            self._cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self._width and pos[1] < self._height:
            gap = self._width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self._rows):
            for j in range(self._cols):
                if self._cubes[i][j]._value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self._model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self._model, i, (row, col)):
                self._model[row][col] = i

                if self.solve():
                    return True

                self._model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = find_empty(self._model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self._model, i, (row, col)):
                self._model[row][col] = i
                self._cubes[row][col].set(i)
                self._cubes[row][col].draw_change(self._win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self._model[row][col] = 0
                self._cubes[row][col].set(0)
                self.update_model()
                self._cubes[row][col].draw_change(self._win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self._value = value
        self._temp = 0
        self._row = row
        self._col = col
        self._width = width
        self._height = height
        self._selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("georgia", 40, italic=True)

        gap = self._width / 9
        x = self._col * gap
        y = self._row * gap

        if self._temp != 0 and self._value == 0:
            text = fnt.render(str(self._temp), True, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not(self._value == 0):
            text = fnt.render(str(self._value), True, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self._selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("georgia", 40)

        gap = self._width / 9
        x = self._col * gap
        y = self._row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self._value), True, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self._value = val

    def set_temp(self, val):
        self._temp = val


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j  # row, col

    return None


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("georgia", 40)
    text = fnt.render("Time: " + format_time(time), True, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, True, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs % 60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    # Title and Icon
    pygame.display.set_caption("Sudoku")
    icon = pygame.image.load("sudoku.png")
    pygame.display.set_icon(icon)
    win = pygame.display.set_mode((540, 600))

    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board._selected
                    if board._cubes[i][j]._temp != 0:
                        if board.place(board._cubes[i][j]._temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board._selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
