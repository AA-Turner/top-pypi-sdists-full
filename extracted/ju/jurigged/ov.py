import time

from ovld import ovld, recurse

# @ovld
# def f(self, xs: list):
#     return [self(x) for x in xs]

# @ovld
# def f(self, x: int):
#     return x * 1


@ovld
def f(xs: list):
    return [recurse(x) for x in xs]


@ovld
def f(x: int):
    return x * 1


def main():
    for i in range(1000):
        print(f([i, i]))
        time.sleep(1)


if __name__ == "__main__":
    main()
