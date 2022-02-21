# Author: Paldin Bet Eivaz
# Description: A terminal-based Sudoku puzzle with a solver.

from math import sqrt


def print_board(board):
    """
    Takes as input a 9x9 2-dimensional list and prints it as a Sudoku board
    Code adapted from: https://stackoverflow.com/questions/37952851/formating-sudoku-grids-python-3
    """

    # print column numbers
    print((' c{} ' * 9).format(*[x for x in range(1, 10)]))

    # print top edge of board
    print("-" * 37)

    for i, row in enumerate(board):

        # for each row in the 2d list, print the nonzero values
        # otherwise print an empty space
        print(("|" + " {}   {}   {} |" * 3).format(*[x if x != 0 else " " for x in row]), ('r' + str(i + 1)))

        # print bottom edge of board
        if i == 8:
            print("-" * 37)
        # print dividers for each grouping of 3 3x3 boxes
        elif i % 3 == 2:
            print("|" + "---" * 11 + "--|")
        # print dividers for each 3x3 box
        else:
            print("|" + "    " * 8 + "   |")


def make_move(board, row, col, num):
    """
    Places the user inputted number onto the specified row and column of the Sudoku board
    """
    board[row][col] = num


def input_valid(row, col, num):
    """
    Validates the user input
    """

    # row and column must be in [0, 8]
    if row < 0 or row > 8 or col < 0 or col > 8:
        return False

    # number must be in [1, 9]
    if num < 1 or num > 9:
        return False

    return True


def is_valid(board):
    """
    Given a completed n x n Sudoku board, returns True if solution is correct
    Returns False otherwise
    """

    # iterate over every space on the n x n board
    for row in range(len(board)):
        for col in range(len(board[0])):

            # get number at each space
            num = board[row][col]

            # check that selected number is distinct in its row
            for i in range(len(board[0])):
                if i != col:
                    if board[row][i] == num:
                        return False

            # check that selected number is distinct in its column
            for i in range(len(board)):
                if i != row:
                    if board[i][col] == num:
                        return False

            # get the index of the top left corner of
            # the √n x √n box the selected number is in
            box_size = int(sqrt(len(board)))
            box_y = (row // box_size) * box_size
            box_x = (col // box_size) * box_size

            # check that the selected number is distinct in its √n x √n box
            for i in range(box_size):
                for j in range(box_size):
                    if not ((box_y + i) == row and (box_x + j) == col):
                        if board[box_y + i][box_x + j] == num:
                            return False

    return True


def is_complete(board):
    """
    Returns True if the Sudoku board is completely filled
    Returns False otherwise
    """

    # check if there are any empty spaces on the board
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return False

    return True


def solver(board):
    """
    Solves a given 9x9 Sudoku board
    """

    # iterate over the board until we find an empty space
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:

                # check which number in [1, 9] we can place at the empty space
                for num in range(1, 10):
                    if move_valid(board, row, col, num):
                        board[row][col] = num  # if valid, fill space with number

                        # recursively fill in remaining empty spaces
                        solver(board)

                # if unable to fill current space with any number in [1, 9],
                # then we must have made an error in a previous step.
                # So backtrack and explore other possibilities in previous steps.
                board[row][col] = 0
                return

    # if we reach here then no empty spaces remain on the board
    # and so we can simply print the solved board
    print_board(board)


def move_valid(board, row, col, num):
    """
    Checks if given number can be placed on board at specified row and column
    """

    # check that number is distinct in its row
    for i in range(len(board[0])):
        if i != col:
            if board[row][i] == num:
                return False

    # check that number is distinct in its column
    for i in range(len(board)):
        if i != row:
            if board[i][col] == num:
                return False

    # get the index of the top left corner of
    # the √n x √n box the number is in
    box_size = int(sqrt(len(board)))
    box_y = (row // box_size) * box_size
    box_x = (col // box_size) * box_size

    # check that the number is distinct in its √n x √n box
    for i in range(box_size):
        for j in range(box_size):
            if not ((box_y + i) == row and (box_x + j) == col):
                if board[box_y + i][box_x + j] == num:
                    return False

    return True


if __name__ == "__main__":

    # a 2d list representation of a solvable 9x9 Sudoku board
    grid = [
        [1, 0, 0, 4, 8, 9, 0, 0, 6],
        [7, 3, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 1, 2, 9, 5],
        [0, 0, 7, 1, 2, 0, 6, 0, 0],
        [5, 0, 0, 7, 0, 3, 0, 0, 8],
        [0, 0, 6, 0, 9, 5, 7, 0, 0],
        [9, 1, 4, 6, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 3, 7],
        [8, 0, 0, 5, 1, 2, 0, 0, 4]
    ]

    print_board(grid)

    # get player input until all spaces on board are filled
    while not is_complete(grid):
        print('Board is incomplete!')
        try:
            c = int(input('Select which column (c1-c9) to place number: ')[1:]) - 1
            r = int(input('Select which row (r1-r9) to place number: ')[1:]) - 1
            n = int(input('Enter an integer from 1-9 to place on the board: '))
        except ValueError:
            print('Input not valid!')
            continue

        # if input is valid, make move
        if input_valid(r, c, n):
            make_move(grid, r, c, n)
            print_board(grid)
        else:
            print('Input not valid!')

    # check if completed Sudoku board is correct
    if is_valid(grid):
        print('Solution Correct')
    # if incorrect, solve and provide solution
    else:
        print('Solution Incorrect. The correct solution is:\n')
        grid = [
            [1, 0, 0, 4, 8, 9, 0, 0, 6],
            [7, 3, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 1, 2, 9, 5],
            [0, 0, 7, 1, 2, 0, 6, 0, 0],
            [5, 0, 0, 7, 0, 3, 0, 0, 8],
            [0, 0, 6, 0, 9, 5, 7, 0, 0],
            [9, 1, 4, 6, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 3, 7],
            [8, 0, 0, 5, 1, 2, 0, 0, 4]
        ]
        solver(grid)
