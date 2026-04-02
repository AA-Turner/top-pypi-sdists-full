import pytest
import copy
import apyds


@pytest.fixture
def v() -> apyds.Variable:
    return apyds.Variable("`variable")


def test_str(v: apyds.Variable) -> None:
    assert str(v) == "`variable"

    with apyds.scoped_buffer_size(4):
        with pytest.raises(ValueError):
            str(v)


def test_repr(v: apyds.Variable) -> None:
    assert repr(v) == "Variable[`variable]"


def test_copy_hash_and_equality(v: apyds.Variable) -> None:
    other = copy.copy(v)
    assert other == v
    assert hash(other) == hash(v)
    assert 1 != v


def test_create_from_same(v: apyds.Variable) -> None:
    variable = apyds.Variable(v)
    assert str(variable) == "`variable"

    with pytest.raises(ValueError):
        variable = apyds.Variable(v, 100)


def test_create_from_base(v: apyds.Variable) -> None:
    variable = apyds.Variable(v.value)
    assert str(variable) == "`variable"


def test_create_from_text() -> None:
    variable = apyds.Variable("`variable")
    assert str(variable) == "`variable"

    # variable never fails


def test_create_from_bytes(v: apyds.Variable) -> None:
    variable = apyds.Variable(v.data())
    assert str(variable) == "`variable"

    with pytest.raises(ValueError):
        variable = apyds.Variable(v.data(), 100)


def test_create_fail() -> None:
    with pytest.raises(TypeError):
        variable = apyds.Variable(100)


def test_name(v: apyds.Variable) -> None:
    assert str(v.name) == "variable"
