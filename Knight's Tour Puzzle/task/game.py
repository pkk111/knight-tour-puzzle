# Write your code here

def validate(message, e_message, x_size=1e3, y_size=1e3, end="\n"):
    while True:
        print(message, end=end)
        try:
            x, y = input().split()
            x = int(x)
            y = int(y)
            assert 1 <= x <= x_size and 1 <= y <= y_size
            return x, y
        except TypeError:
            print(e_message, end=end)
        except ValueError:
            print(e_message, end=end)
        except AssertionError:
            print(e_message, end=end)


def get_number_of_moves(board, x, y, x_size, y_size):
    count = 0
    for i in range(1, x_size + 1):
        for j in range(1, y_size + 1):
            x_diff = abs(x - i)
            y_diff = abs(y - j)
            if not board[j][i].endswith("X") and not board[j][i].endswith("*") and x_diff + y_diff == 3 and x_diff != 0 and y_diff != 0:
                count += 1
    return count


def mark_board(board, x, y, x_size, y_size, placeholder_len):
    for j in range(1, y_size + 1):
        for i in range(1, x_size + 1):
            x_diff = abs(x - i)
            y_diff = abs(y - j)
            if x_diff == 0 and y_diff == 0:
                board[j][i] = (" " * (placeholder_len - 1)) + "X"
    for j in range(1, y_size + 1):
        for i in range(1, x_size + 1):
            x_diff = abs(x - i)
            y_diff = abs(y - j)
            if x_diff + y_diff == 3 and x_diff != 0 and y_diff != 0 and board[j][i].endswith("_"):
                board[j][i] = (" " * (placeholder_len - 1)) + str(get_number_of_moves(board, i, j, x_size, y_size))
    return board


def show_board(board, x_size, y_size, placeholder_len, trial=True):
    division = "-" * (x_size * (placeholder_len + 1) + 3)
    division = ' ' + division
    lastline = " " * 3

    print(division)
    if trial:
        for j in range(y_size, 0, -1):
            print(f"{j}|", *board[j][1:], "|")
    else:
        for j in range(y_size, 0, -1):
            print(f"{j}|", *board[j][1:], "|")
    for i in range(1, x_size + 1):
        lastline += f"{' ' * (placeholder_len - 1)}{i} "
    print(division)
    print(lastline)


def reset_moves(board, x_size, y_size, placeholder_len):
    for i in range(1, x_size + 1):
        for j in range(1, y_size + 1):
            cell = board[j][i].strip()
            if cell.isdigit():
                board[j][i] = "_" * placeholder_len
            if cell == "X":
                board[j][i] = " " * (placeholder_len - 1) + "*"


def has_finished(board, x_size, y_size):
    for i in range(1, x_size + 1):
        for j in range(1, y_size + 1):
            if board[j][i].endswith("_"):
                return False
    return True


def play(board, x, y, x_size, y_size, placeholder_len, moves):
    if get_number_of_moves(board, x, y, x_size, y_size) == 0:
        if has_finished(board, x_size, y_size):
            print("What a great tour! Congratulations!")
        else:
            print("No more possible moves!")
            print(f"Your knight visited {moves} squares!")
        return
    x, y = validate("Enter your next move: ", "Invalid move!", x_size, y_size, end=' ')
    if board[y][x].strip().isdigit():
        reset_moves(board, x_size, y_size, placeholder_len)
        board[y][x] = " " * (placeholder_len - 1) + "X"
        board = mark_board(board, x, y, x_size, y_size, placeholder_len)
        show_board(board, x_size, y_size, placeholder_len)
    else:
        print("Invalid move!", end=' ')
        play(board, x, y, x_size, y_size, placeholder_len, moves)
        return
    play(board, x, y, x_size, y_size, placeholder_len, moves + 1)


def find_solution(board, x, y, x_size, y_size, pos):
    if pos > x_size * y_size:
        return board
    x_move = [2, 2, -1, -1, -2, -2, 1, 1]
    y_move = [1, -1, 2, -2, 1, -1, 2, -2]
    for i in range(8):
        xx = x + x_move[i]
        yy = y + y_move[i]
        if 0 < xx <= x_size and 0 < yy <= y_size and type(board[yy][xx]) is str and board[yy][xx].startswith("_"):
            board[yy][xx] = pos
            sol = find_solution(board, xx, yy, x_size, y_size, pos + 1)
            if sol != -1:
                return sol
            board[yy][xx] = "_"
    return -1


def start(x_size, y_size):
    x, y = validate("Enter the knight's starting position:", "Invalid position!", x_size, y_size)
    trial = True
    while True:
        print("Do you want to try the puzzle? (y/n):")
        tryit = input()
        if tryit == 'n':
            trial = False
            break
        if tryit == 'y':
            break
        print("Invalid input!")

    placeholder_len = len(str(x_size * y_size))

    board = [[]] * (y_size + 1)
    for j in range(1, y_size + 1):
        board[j] = ["_" * placeholder_len] * (x_size + 1)
    if get_number_of_moves(board, x, y, x_size, y_size) == 0:
        print("No solution exists!")
        return

    pos = 1
    sol = list(board)
    for i in range(0, len(board)):
        sol[i] = list(board[i])

    sol[y][x] = pos
    sol = find_solution(sol, x, y, x_size, y_size, pos + 1)
    if sol == -1:
        print("No solution exists!")
        return
    if trial:
        board = mark_board(board, x, y, x_size, y_size, placeholder_len)
        show_board(board, x_size, y_size, placeholder_len)
        play(board, x, y, x_size, y_size, placeholder_len, 1)
    else:
        print("Here's the solution!")
        show_board(sol, x_size, y_size, placeholder_len, False)


def get_board_size():
    x, y = validate("Enter your board dimensions:", "Invalid dimensions!")
    start(x, y)


get_board_size()
