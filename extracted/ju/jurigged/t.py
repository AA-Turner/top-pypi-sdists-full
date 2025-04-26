import time


def crunch(fn):
    def deco(*args):
        return fn(*args) + 1

    return deco


@crunch
@crunch
def munch(x):
    return x * 4


if __name__ == "__main__":
    while True:
        print(munch(10))
        time.sleep(0.25)
