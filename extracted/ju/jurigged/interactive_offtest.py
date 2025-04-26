import time
import traceback
from pathlib import Path

this = Path(__file__)
here = this.parent


def identity(f):
    return f


@identity
def g(x):
    1
    raise Exception("hello")


def oo(x):
    return g(x + 1)


@identity
def f(x):
    cool_beans = oo(x + 1)
    cool_beans += 34


def main():
    f(10)


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception:
            traceback.print_exc()
        time.sleep(0.5)
