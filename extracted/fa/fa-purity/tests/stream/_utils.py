from secrets import (
    randbelow,
)
from typing import (
    TypeVar,
)

from fa_purity import (
    Cmd,
    Stream,
    Unsafe,
)

_T = TypeVar("_T")


def rand_int() -> Cmd[int]:
    return Cmd.wrap_impure(lambda: randbelow(11))


def assert_different_iter(stm: Stream[_T]) -> None:
    iter1 = Unsafe.compute(Unsafe.stream_to_iter(stm))
    iter2 = Unsafe.compute(Unsafe.stream_to_iter(stm))
    assert id(iter1) != id(iter2)
