import pytest
import copy
import apyds


@pytest.fixture
def i() -> apyds.Item:
    return apyds.Item("item")


def test_str(i: apyds.Item) -> None:
    assert str(i) == "item"

    with apyds.scoped_buffer_size(4):
        with pytest.raises(ValueError):
            str(i)


def test_repr(i: apyds.Item) -> None:
    assert repr(i) == "Item[item]"


def test_copy_hash_and_equality(i: apyds.Item) -> None:
    other = copy.copy(i)
    assert other == i
    assert hash(other) == hash(i)
    assert 1 != i


def test_create_from_same(i: apyds.Item) -> None:
    item = apyds.Item(i)
    assert str(item) == "item"

    with pytest.raises(ValueError):
        item = apyds.Item(i, 100)


def test_create_from_base(i: apyds.Item) -> None:
    item = apyds.Item(i.value)
    assert str(item) == "item"


def test_create_from_text() -> None:
    item = apyds.Item("item")
    assert str(item) == "item"

    # item never fails


def test_create_from_bytes(i: apyds.Item) -> None:
    item = apyds.Item(i.data())
    assert str(item) == "item"

    with pytest.raises(ValueError):
        item = apyds.Item(i.data(), 100)


def test_create_fail() -> None:
    with pytest.raises(TypeError):
        item = apyds.Item(100)


def test_name(i: apyds.Item) -> None:
    assert str(i.name) == "item"
