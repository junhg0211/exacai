from random import random
from time import time
from json import load, dump

from environ import *


def loadq(filename="q.json"):
    try:
        with open(filename, "r") as file:
            q = load(file)
    except:
        q = {}
    for k, v in list(q.items()):
        del q[k]
        q[int(k)] = v
    return q


def dumpq(q, filename="q.json"):
    with open(filename, "w") as file:
        dump(q, file)


def updateq(q, state, move, value):
    q[state][move] = value


def defaultq(q, state):
    q[state] = [random() for _ in range(7**4)]


def getq(q, state, move):
    if state not in q:
        defaultq(q, state)
    return q.get(state)[move]


def getbestmove(q, board):
    return max(range(7**4), key=lambda i: getq(q, board, i) + random() * 0.1)


def learn(q, a, g):
    board = createboard()
    bh = boardhash(board)
    recordtime = time()

    while True:
        if time() > recordtime + 60:
            dumpq(q)
            recordtime = time()

        bm = getbestmove(q, bh)
        print(bh, bm, getq(q, bh, bm))
        y1, x1, y2, x2 = hashtomove(bm)
        
        if not isvalidmove(board, *hashtomove(bm)):
            updateq(q, bh, bm, -1e300)
            board = createboard()
            bh = boardhash(board)
            print("  Newgame")
            continue

        rate = 2
        if board[y2][x2] == 2:
            rate += 10
        n1 = 0
        n2 = 0
        for i in range(7):
            for j in range(7):
                if board[i][j] == 1:
                    n1 += 1
                if board[i][j] == 2:
                    n2 += 1
        if n2 == 0:
            rate = 1e300
        if n1 == 0:
            rate = -1e300

        newboard = flipopponent(applymove(board, *hashtomove(bm)))
        nbh = boardhash(newboard)

        wow = getq(q, nbh, getbestmove(q, nbh))
        newq = (1-a) * getq(q, bh, bm) + a * (rate + g * wow)
        updateq(q, bh, bm, newq)

        board = newboard
        bh = nbh


if __name__ == "__main__":
    learn(loadq(), 0.1, 0.4)
