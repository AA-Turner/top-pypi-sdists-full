from collections.abc import Callable
from tempfile import (
    TemporaryFile,
)
from typing import (
    IO,
    NoReturn,
)

import pytest

from fa_purity import (
    Cmd,
    CmdUnwrapper,
)
from fa_purity._core.unsafe import (
    Unsafe,
)


def _do_not_call() -> NoReturn:
    msg = "Cmd action should be only executed on compute phase"
    raise ValueError(msg)


def test_from_cmd() -> None:
    Cmd.wrap_impure(_do_not_call)


def test_map() -> None:
    cmd = Cmd.wrap_impure(lambda: 44).map(lambda i: i + 5)
    cmd.map(lambda _: _do_not_call())
    Cmd.wrap_impure(_do_not_call).map(lambda _: _)

    def _verify(num: int) -> None:
        assert num == 49

    with pytest.raises(SystemExit):
        cmd.map(_verify).compute()


def test_bind() -> None:
    cmd = Cmd.wrap_impure(lambda: 50)
    cmd2 = Cmd.wrap_impure(lambda: 44).bind(lambda i: cmd.map(lambda x: x + i))
    cmd2.bind(lambda _: Cmd.wrap_impure(_do_not_call))
    Cmd.wrap_impure(_do_not_call).bind(lambda _: cmd)

    def _verify(num: int) -> None:
        assert num == 94

    with pytest.raises(SystemExit):
        cmd2.map(_verify).compute()


def test_apply() -> None:
    cmd = Cmd.wrap_impure(lambda: 1)
    wrapped: Cmd[Callable[[int], int]] = Cmd.wrap_impure(lambda: lambda x: x + 10)

    dead_end: Cmd[Callable[[int], NoReturn]] = Cmd.wrap_impure(
        lambda: lambda _: _do_not_call(),  # type: ignore[misc]
    )
    ex_falso_quodlibet: Callable[[NoReturn], int] = lambda _: 1
    wrap_no_return: Cmd[Callable[[NoReturn], int]] = Cmd.wrap_impure(lambda: ex_falso_quodlibet)

    cmd.apply(dead_end)
    Cmd.wrap_impure(_do_not_call).apply(wrap_no_return)

    def _verify(num: int) -> None:
        assert num == 11

    with pytest.raises(SystemExit):
        cmd.apply(wrapped).map(_verify).compute()


def _print_msg(msg: str, target: IO[str]) -> Cmd[None]:
    return Cmd.wrap_impure(lambda: print(msg, file=target))


def test_use_case_1() -> None:
    with TemporaryFile("r+") as file:

        def _print(msg: str) -> Cmd[None]:
            return _print_msg(msg, file)

        in_val = Cmd.wrap_impure(lambda: 245)
        some = in_val.map(lambda i: i + 1).map(str).bind(_print)
        _print("not called")
        pre = _print("Hello World!")
        try:
            pre.bind(lambda _: some).compute()
        except SystemExit:
            file.seek(0)
            assert file.readlines() == ["Hello World!\n", "246\n"]


def test_new_cmd() -> None:
    state = {}

    def _mutate(val: int) -> None:
        state["temp"] = val

    change_1 = Cmd.wrap_impure(lambda: _mutate(99)).map(lambda _: "1")
    change_2 = Cmd.wrap_impure(lambda: _mutate(2)).map(lambda _: 2)

    def _action(unwrapper: CmdUnwrapper) -> int:
        x = unwrapper.act(change_2)
        y = unwrapper.act(change_1)
        return x + int(y)

    cmd1 = Cmd.new_cmd(_action)
    assert state.get("temp") is None
    assert Unsafe.compute(cmd1) == 3
    assert state["temp"] == 99
