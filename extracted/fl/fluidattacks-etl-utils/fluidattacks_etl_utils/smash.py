from collections.abc import Callable
from typing import (
    TypeVar,
)

from fa_purity import (
    Cmd,
    Coproduct,
    CoproductFactory,
    Result,
)

_A = TypeVar("_A")
_B = TypeVar("_B")
_C = TypeVar("_C")
_D = TypeVar("_D")
_E = TypeVar("_E")
_S = TypeVar("_S")
_F = TypeVar("_F")
_Err = TypeVar("_Err")

_T = TypeVar("_T")
_L = TypeVar("_L")
_R = TypeVar("_R")


def bind_chain(
    result: Result[_S, _F],
    transform: Callable[[_S], Result[_A, _B]],
) -> Result[_A, Coproduct[_B, _F]]:
    _factory: CoproductFactory[_B, _F] = CoproductFactory()
    return result.alt(_factory.inr).bind(lambda s: transform(s).alt(_factory.inl))


def smash_cmds_2(
    cmd_1: Cmd[_A],
    cmd_2: Cmd[_B],
) -> Cmd[tuple[_A, _B]]:
    return cmd_1.bind(lambda a: cmd_2.map(lambda b: (a, b)))


def smash_cmds_3(
    cmd_1: Cmd[_A],
    cmd_2: Cmd[_B],
    cmd_3: Cmd[_C],
) -> Cmd[tuple[_A, _B, _C]]:
    return smash_cmds_2(cmd_1, cmd_2).bind(lambda t: cmd_3.map(lambda c: (*t, c)))


def smash_cmds_4(
    cmd_1: Cmd[_A],
    cmd_2: Cmd[_B],
    cmd_3: Cmd[_C],
    cmd_4: Cmd[_D],
) -> Cmd[tuple[_A, _B, _C, _D]]:
    return smash_cmds_3(cmd_1, cmd_2, cmd_3).bind(lambda t: cmd_4.map(lambda d: (*t, d)))


def smash_cmds_5(
    cmd_1: Cmd[_A],
    cmd_2: Cmd[_B],
    cmd_3: Cmd[_C],
    cmd_4: Cmd[_D],
    cmd_5: Cmd[_E],
) -> Cmd[tuple[_A, _B, _C, _D, _E]]:
    return smash_cmds_4(cmd_1, cmd_2, cmd_3, cmd_4).bind(lambda t: cmd_5.map(lambda e: (*t, e)))


def smash_result_2(
    result_1: Result[_A, _Err],
    result_2: Result[_B, _Err],
) -> Result[tuple[_A, _B], _Err]:
    return result_1.bind(lambda a: result_2.map(lambda b: (a, b)))


def smash_result_3(
    result_1: Result[_A, _Err],
    result_2: Result[_B, _Err],
    result_3: Result[_C, _Err],
) -> Result[tuple[_A, _B, _C], _Err]:
    return smash_result_2(result_1, result_2).bind(lambda t: result_3.map(lambda e: (*t, e)))


def smash_result_4(
    result_1: Result[_A, _Err],
    result_2: Result[_B, _Err],
    result_3: Result[_C, _Err],
    result_4: Result[_D, _Err],
) -> Result[tuple[_A, _B, _C, _D], _Err]:
    return smash_result_3(result_1, result_2, result_3).bind(
        lambda t: result_4.map(lambda e: (*t, e)),
    )


def smash_result_5(
    result_1: Result[_A, _Err],
    result_2: Result[_B, _Err],
    result_3: Result[_C, _Err],
    result_4: Result[_D, _Err],
    result_5: Result[_E, _Err],
) -> Result[tuple[_A, _B, _C, _D, _E], _Err]:
    return smash_result_4(result_1, result_2, result_3, result_4).bind(
        lambda t: result_5.map(lambda e: (*t, e)),
    )


def merge_coproduct(item: Coproduct[_A, _A]) -> _A:
    return item.map(lambda x: x, lambda x: x)


def left_map(item: Coproduct[_L, _R], function: Callable[[_L], _T]) -> Coproduct[_T, _R]:
    return item.map(
        lambda v: Coproduct.inl(function(v)),
        Coproduct.inr,
    )


def right_map(item: Coproduct[_L, _R], function: Callable[[_R], _T]) -> Coproduct[_L, _T]:
    return item.map(
        Coproduct.inl,
        lambda v: Coproduct.inr(function(v)),
    )
