from fa_purity import (
    FrozenDict,
)


def test_hashable() -> None:
    a = FrozenDict({"test": 99})
    b = FrozenDict({"test": 99})
    assert frozenset([a, b]) == frozenset([a])


def test_innmutable() -> None:
    raw = {"test": 99}
    a = FrozenDict(raw)
    raw["test"] = 100
    b = FrozenDict(raw)
    assert a != b


def test_from_items() -> None:
    raw = {"test": 99}
    a = FrozenDict(raw)
    b = FrozenDict.from_items(raw.items())
    c = FrozenDict.from_items(tuple(raw.items()))
    assert a == b
    assert b == c


def test_map() -> None:
    a = FrozenDict({"test": 99})
    b = a.map(lambda k: k + "_1", lambda v: v + 1)
    expected = FrozenDict({"test_1": 100})
    assert b == expected
