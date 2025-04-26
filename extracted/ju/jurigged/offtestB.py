import sys
import time
import traceback
from pathlib import Path

this = Path(__file__)
here = this.parent


def identity(f):
    return f


def g(x):
    raise Exception("helloX")


def oo(x):
    return g(x + 1)


def f(x):
    cool_beans = oo(x + 1)
    cool_beans += 34


def main():
    f(10)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()

    (here / "BACKUP").write_text(this.read_text())
    this.write_text((here / sys.argv[1]).read_text())

    time.sleep(0.5)
    try:
        main()
    except Exception:
        traceback.print_exc()

    this.write_text((here / "BACKUP").read_text())

    time.sleep(0.5)
    try:
        main()
    except Exception:
        traceback.print_exc()
