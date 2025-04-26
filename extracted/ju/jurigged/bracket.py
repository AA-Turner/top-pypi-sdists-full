import time

from asbestos import deco, f1, f2


@deco
def f3(x):
    return x * x


def step():
    while True:
        print("f1", f1(6))
        print("f2", f2(6))
        print("f3", f3(6))
        time.sleep(1)


step()
