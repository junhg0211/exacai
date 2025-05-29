from environ import *
from learn import *


def main():
    q = loadq()
    board = createboard()

    while True:
        printboard(board)
        move = map(int, input("move> ").split())

        new_board = flipopponent(applymove(board, *move))
        nbh = boardhash(new_board)
        printboard(flipopponent(new_board))

        mh, bh = doonce(q, nbh, 0.3, 0.5)
        move = hashtomove(mh)
        print(move)
        
        board = hashtoboard(bh)


if __name__ == "__main__":
    main()
