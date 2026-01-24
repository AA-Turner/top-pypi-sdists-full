from fa_purity import (
    FrozenTools,
)
from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
)


def test_chain() -> None:
    a: FrozenList[FrozenList[int]] = ((1, 2), (), (3, 4, 5), (6,))
    expected = tuple(range(1, 7))
    assert FrozenTools.chain(a) == expected


def test_freeze() -> None:
    assert FrozenTools.freeze([1, 2, 3]) == (1, 2, 3)
    assert FrozenTools.freeze({"test": 99}) == FrozenDict({"test": 99})
    assert FrozenTools.unfreeze((1, 2, 3)) == [1, 2, 3]
    assert FrozenTools.unfreeze(FrozenDict({"test": 99})) == {"test": 99}
