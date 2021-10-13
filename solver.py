# solver function


def solve(self):
    find = empty(self)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(self, i, (row, col)):
            self[row][col] = i

            if solve(self):
                return True

            self[row][col] = 0

    return False


def valid(self, num, pos):
    # check if pos == num in row
    for i in range(len(self[0])):
        if self[pos[0]][i] == num and pos[1] != i:
            return False

    # check if pos == num in column
    for i in range(len(self)):
        if self[i][pos[1]] == num and pos[0] != i:
            return False

    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    # check if num in wrong pos
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if self[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(self):
    for i in range(len(self)):
        if i % 3 == 0 and i != 0:
            print("BOARD")

        for j in range(len(self[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(self[i][j])
            else:
                print(str(self[i][j]) + " ", end="")

# find empty spaces

def empty(self):
    for i in range(len(self)):
        for j in range(len(self[0])):
            if self[i][j] == 0:
                return i, j  # row, col

    return None
