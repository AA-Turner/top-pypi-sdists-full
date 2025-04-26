def squook(x):
    return x * x * 3


coco = {
    "a": 1,
    "b": squook,
}


def wood(fn):
    def flower(arg):
        return fn(arg) * 4

    return flower


@wood
def square(x):
    return x * x * 5


@wood
def plus(x):
    return x + 1


# import argparse


# a = argparse.ArgumentParser()
# a.add_argument("--model", nargs=argparse.REMAINDER)
# a.add_argument("--mayday", nargs=argparse.REMAINDER)

# print(a.parse_args())
