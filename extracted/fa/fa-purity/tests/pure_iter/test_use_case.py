from fa_purity import (
    PureIterFactory,
)
from tests.pure_iter._utils import (
    assert_immutability,
    assert_immutability_inf,
)


def test_use_case_1() -> None:
    items = PureIterFactory.from_range(range(10))
    mapped = items.map(lambda i: i + 2)
    assert mapped.to_list() == tuple(range(2, 12))
    r = items.map(lambda x: x * 2).chunked(3)
    expected = ((0, 2, 4), (6, 8, 10), (12, 14, 16), (18,))
    assert r.to_list() == expected
    assert_immutability(items)
    assert_immutability(mapped)


def test_inf() -> None:
    items = PureIterFactory.infinite_range(4, 10)
    for n, v in enumerate(items):
        assert v == 4 + (n * 10)
        if n > 15:
            break
    assert_immutability_inf(items)
