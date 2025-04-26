import sys
import termios
import time
import tty
from contextlib import contextmanager

import rx
from giving import ObservableProxy, give, given


@contextmanager
def cbreak():
    old_attrs = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    try:
        yield
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attrs)


def read_chars():
    while True:
        yield {"$command": sys.stdin.read(1)}


def woop():
    for i in range(100):
        give(i)
        time.sleep(1)


with cbreak():
    sch = rx.scheduler.EventLoopScheduler()
    sin = ObservableProxy(rx.from_iterable(read_chars(), scheduler=sch))
    with given() as gv:
        (gv | sin) >> print
        # gv >> print
        woop()

    # sin = ObservableProxy(rx.from_iterable(sys.stdin))
    # sin >> sys.stdout.write
    # sin >> print
