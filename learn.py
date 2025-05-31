from random import random
from time import time
from pickle import load, dump
from os import system

from environ import *


def loadq(filename="q.pickle"):
    try:
        with open(filename, "rb") as file:
            q = load(file)
    except:
        q = {}
    return q


def dumpq(q, filename="q.pickle"):
    system(f"cp {filename} b.pickle")
    with open(filename, "wb") as file:
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
    return max(range(7**4), key=lambda i: getq(q, board, i) + random() * 0.2)


def doonce(q, bh, a, g):
    board = hashtoboard(bh)

    while True:
        bm = getbestmove(q, bh)
        # print(bh, bm, getq(q, bh, bm), sep="\t")
        y1, x1, y2, x2 = hashtomove(bm)
        
        if not isvalidmove(board, *hashtomove(bm)):
            updateq(q, bh, bm, -1e300)
            # print("  Dax")
            continue

        break

    rate = 0
    if board[y2][x2] == 2:
        rate += 2
    n1 = 0
    n2 = 0
    for i in range(7):
        for j in range(7):
            if board[i][j] == 1:
                n1 += 1
            if board[i][j] == 2:
                n2 += 1
    if n2 == 1:
        rate = 1e300
    if n1 == 1:
        rate = -1e300

    newboard = flipopponent(applymove(board, *hashtomove(bm)))
    nbh = boardhash(newboard)

    wow = getq(q, nbh, getbestmove(q, nbh))
    newq = (1-a) * getq(q, bh, bm) + a * (rate + g * wow)
    updateq(q, bh, bm, newq)

    return bm, nbh


def learn(q, a, g):
    board = createboard()
    bh = boardhash(board)
    game = 0
    turn = 0

    while True:

        print("#", game, "(", turn, ")")
        printboard(board if turn % 2 else flipopponent(board))
        turn += 1

        bm, nbh = doonce(q, bh, a, g)
        print(hashtomove(bm))

        board = hashtoboard(nbh)
        bh = nbh

        n1 = 0
        n2 = 0
        for i in range(7):
            for j in range(7):
                if board[i][j] == 1:
                    n1 += 1
                if board[i][j] == 2:
                    n2 += 1

        if n1 == 1 or n2 == 1:
            board = createboard()
            bh = boardhash(board)
            turn = 1
            game += 1

            dumpq(q)


if __name__ == "__main__":
    learn(loadq(), 0.1, 0.4)
