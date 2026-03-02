import random
import typing


def samplify(*args) -> typing.Iterator[typing.Any]:
    while args:
        yield random.choice(args)
