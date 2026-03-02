import random
import typing


def shufflify(*args) -> typing.Iterator[typing.Any]:
    args_list = [*args]
    random.shuffle(args_list)
    return iter(args_list)
