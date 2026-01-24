import pytest

from fa_purity import (
    Cmd,
    PureIterFactory,
    PureIterTransform,
)
from tests.pure_iter._utils import (
    assert_immutability,
)


def test_chain() -> None:
    base = (4, 78, 6)
    items = PureIterFactory.from_range(range(5)).map(lambda _: PureIterFactory.from_list(base))
    chained = PureIterTransform.chain(items)
    assert_immutability(chained)
    assert tuple(chained) == base * 5


def test_consume() -> None:
    mutable_obj = [0]

    def _mutate(num: int) -> None:
        mutable_obj[0] = num

    items = PureIterFactory.from_list(tuple(range(5))).map(
        lambda i: Cmd.wrap_impure(lambda: _mutate(i)),
    )
    assert_immutability(items, True)
    cmd = PureIterTransform.consume(items)
    assert mutable_obj[0] == 0

    def _verify(_: None) -> None:
        assert mutable_obj[0] == 4

    with pytest.raises(SystemExit):
        cmd.map(_verify).compute()


def test_filter_opt() -> None:
    items = (0, 1, 2, 3, None, 4, 5, 6)
    result = PureIterTransform.filter_opt(PureIterFactory.from_list(items))
    assert_immutability(result)
    assert tuple(result) == tuple(range(7))


def test_until_none() -> None:
    items = (0, 1, 2, 3, None, 4, 5, 6)
    result = PureIterTransform.until_none(PureIterFactory.from_list(items))
    assert_immutability(result)
    assert tuple(result) == tuple(range(4))
