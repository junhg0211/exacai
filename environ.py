def createboard():
    return \
        [[2, 2, 2, 2, 2, 2, 2],
         [2, 2, 2, 2, 2, 2, 2],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1]]


def boardhash(board):
    result = 0
    for i in range(49):
        j, k = divmod(i, 7)
        result += 3**i * board[j][k]
    return result


def hashtoboard(number):
    board = createboard()
    for i in range(49):
        j, k = divmod(i, 7)
        board[j][k] = number // 3**i % 3
    return board


def printboard(board):
    print("    0 1 2 3 4 5 6")
    print()
    for i, row in enumerate(board):
        print(i, end="   ")
        for cell in row:
            print(cell, end=" ")
        print()


def movehash(y1, x1, y2, x2):
    return y1*1 + x1*7 + y2*49 + x2*343


def hashtomove(number):
    y1 = number // 1 % 7
    x1 = number // 7 % 7
    y2 = number // 49 % 7
    x2 = number // 343 % 7
    return y1, x1, y2, x2


def flipopponent(board):
    result = createboard()
    for i in range(49):
        j, k = divmod(i, 7)
        result[7-j-1][7-k-1] = 0 if board[j][k] == 0 else (1 if board[j][k] == 2 else 2)
    return result


def isvalidmove(board, y1, x1, y2, x2):
    if board[y1][x1] != 1:
        return False

    if board[y2][x2] == 1:
        return False

    dy = y2 - y1
    dx = x2 - x1
    
    # poluis
    if (dy, dx) in [(-1,0), (0,-1), (0,1)]:
        return True

    # lapah
    if y1 == 3 and (dy == dx or dx == -dy or dy == 0 or dx == 0):
        return True

    # potysin
    if y1 == 6 and x1 in [1,3,5] and (dx == dy or dx == -dy):
        return True

    # pyriç
    if y1 in [0, 6] and dx == 0 or x1 in [0,6] and dy == 0:
        return True

    # adriv
    if (dy, dx) == (3, 0) and board[y1+1][x1] == 1 \
            or (dy, dx) == (-3, 0) and board[y1-1][x1] == 1 \
            or (dy, dx) == (0, 3) and board[y1][x1+1] == 1 \
            or (dy, dx) == (0, -3) and board[y1][x1-1] == 1:
        return True

    return False


def applymove(board, y1, x1, y2, x2):
    board[y1][x1] = 0
    board[y2][x2] = 1
    return board


if __name__ == "__main__":
    b = createboard()
    b = applymove(b, 6, 0, 0, 0)
    c = flipopponent(b)
    printboard(c)

