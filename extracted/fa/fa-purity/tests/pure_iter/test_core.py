from collections.abc import Callable

from fa_purity import (
    Maybe,
    PureIter,
    PureIterFactory,
)
from tests.pure_iter._utils import (
    assert_immutability,
)


def test_map() -> None:
    items = PureIterFactory.from_range(range(10)).map(lambda i: i + 1)
    assert_immutability(items)


def test_chunked() -> None:
    items = PureIterFactory.from_range(range(10)).chunked(2)
    assert_immutability(items)


def test_find_first() -> None:
    items = PureIterFactory.from_range(range(10))
    assert_immutability(items)
    assert items.find_first(lambda n: n > 6).value_or(-1) == 7
    assert items.find_first(lambda n: n > 99) == Maybe.empty()


def test_bind() -> None:
    items = PureIterFactory.from_range(range(5))
    items2: Callable[[int], PureIter[int]] = lambda n: PureIterFactory.from_list((n, n))
    expected = (0, 0, 1, 1, 2, 2, 3, 3, 4, 4)
    result = items.bind(items2)
    assert_immutability(result)
    assert result.to_list() == expected
