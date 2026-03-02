import itertools as it
import random
from signal import SIG_BLOCK, SIGPIPE, signal
import sys
import typing


def generate_test_cases() -> typing.Iterable[typing.Tuple[int, int]]:
    rand = random.Random(1)
    for s, T in it.product(range(21), range(3840)):
        S = 1 << s
        capacity_bound = 1 << min(S, 32)
        yield S, T
        if T < 100:
            yield S, rand.randint(0, capacity_bound - 1)
            yield S, rand.randint(0, 2**32 - 1)

    # test extended domains (e.g., for circular, compressing, and sticky)
    for S, T in it.product((6, 7), range(960)):
        capacity_bound = 1 << min(S, 32)
        yield S, T
        if T < 100:
            yield S, rand.randint(0, capacity_bound - 1)
            yield S, rand.randint(0, 2**32 - 1)

    # test multiples of 3 (e.g., for 3-chunk hybrid algos)
    for S, T in it.product((24, 48, 96), range(960)):
        capacity_bound = 1 << min(S, 32)
        yield S, T
        if T < 100:
            yield S, rand.randint(0, capacity_bound - 1)
            yield S, rand.randint(0, 2**32 - 1)

    # test at edges of unsigned integer representations
    for s, t in it.product(range(21), range(3, 21)):
        S = 1 << s
        T = 1 << t
        for T_ in range(T - 7, T + 8):
            yield S, T_

    for S, t in it.product((6, 7), range(3, 21)):
        T = 1 << t
        for T_ in range(T - 7, T + 8):
            yield S, T_

    for S, t in it.product((24, 48, 96), range(3, 21)):
        T = 1 << t
        for T_ in range(T - 7, T + 8):
            yield S, T_


if __name__ == "__main__":
    signal(SIGPIPE, SIG_BLOCK)
    for T, S in generate_test_cases():
        sys.stdout.write(f"{T} {S}\n")
