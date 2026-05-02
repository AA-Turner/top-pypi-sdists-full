from typing import TypeVar, Callable, Iterable

T = TypeVar("T")


def merge(left: list[T], right: list[T], comp: Callable[[T, T], int]) -> Iterable[T]:
    i = 0
    j = 0
    n1 = len(left)
    n2 = len(right)

    while i < n1 and j < n2:
        c = comp(left[i], right[j])
        if c > 0:
            yield left[i]
            i += 1
        else:
            yield right[j]
            j += 1

    while i < n1:
        yield left[i]
        i += 1

    while j < n2:
        yield right[j]
        j += 1
