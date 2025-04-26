import sys
import time

from executing import Source


def zazz():
    1
    2
    3
    return Source.executing(sys._getframe(1))


def rook():
    1
    2
    3
    4
    5
    6
    node = zazz()


def main():
    while True:
        rook()
        print("=" * 20)
        time.sleep(1)


main()
