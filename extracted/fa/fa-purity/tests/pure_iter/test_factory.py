from fa_purity import (
    PureIterFactory,
)
from tests.pure_iter._utils import (
    assert_immutability,
    assert_immutability_inf,
    to_tuple,
)


def test_flist() -> None:
    items = tuple(range(10))
    assert_immutability(PureIterFactory.from_list(items))


def test_range() -> None:
    assert_immutability(PureIterFactory.from_range(range(10)))


def test_inf_range() -> None:
    assert_immutability_inf(PureIterFactory.infinite_range(3, 5))


def test_infinite_gen() -> None:
    items = PureIterFactory.infinite_gen(lambda x: x + 1, 0)
    assert_immutability_inf(items)
    assert to_tuple(items, 10) == tuple(range(10))
