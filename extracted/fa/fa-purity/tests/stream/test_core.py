from collections.abc import Callable

from fa_purity import (
    Cmd,
    Maybe,
    PureIterFactory,
    Stream,
    StreamFactory,
    Unsafe,
)
from tests.stream._utils import (
    assert_different_iter,
    rand_int,
)


def test_map() -> None:
    items = PureIterFactory.from_range(range(10)).map(lambda _: rand_int())
    stm = StreamFactory.from_commands(items).map(lambda i: i + 1)
    assert_different_iter(stm)


def test_chunked() -> None:
    items = PureIterFactory.from_range(range(10)).map(lambda _: rand_int())
    stm = StreamFactory.from_commands(items).chunked(2)
    assert_different_iter(stm)


def test_find_first() -> None:
    items = StreamFactory.from_commands(
        PureIterFactory.from_range(range(10)).map(lambda _: rand_int()),
    )
    assert_different_iter(items)
    assert Unsafe.compute(items.find_first(lambda n: n >= 0)).value_or(-1) >= 0
    assert Unsafe.compute(items.find_first(lambda n: n > 9999)) == Maybe.empty()


def test_bind() -> None:
    items = StreamFactory.from_commands(
        PureIterFactory.from_range(range(5)).map(lambda i: Cmd.wrap_impure(lambda: i)),
    )
    items2: Callable[[int], Stream[int]] = lambda n: StreamFactory.from_commands(
        PureIterFactory.from_list((n, n)).map(lambda i: Cmd.wrap_impure(lambda: i)),
    )
    expected = (0, 0, 1, 1, 2, 2, 3, 3, 4, 4)
    result = items.bind(items2)
    assert_different_iter(result)
    assert Unsafe.compute(result.to_list()) == expected
