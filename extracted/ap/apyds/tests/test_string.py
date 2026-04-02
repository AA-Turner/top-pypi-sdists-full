import pytest
import copy
import apyds


@pytest.fixture
def s() -> apyds.String:
    return apyds.String("string")


def test_str(s: apyds.String) -> None:
    assert str(s) == "string"

    with apyds.scoped_buffer_size(4):
        with pytest.raises(ValueError):
            str(s)


def test_repr(s: apyds.String) -> None:
    assert repr(s) == "String[string]"


def test_copy_hash_and_equality(s: apyds.String) -> None:
    other = copy.copy(s)
    assert other == s
    assert hash(other) == hash(s)
    assert 1 != s


def test_create_from_same(s: apyds.String) -> None:
    string = apyds.String(s)
    assert str(string) == "string"

    with pytest.raises(ValueError):
        string = apyds.String(s, 100)


def test_create_from_base(s: apyds.String) -> None:
    string = apyds.String(s.value)
    assert str(string) == "string"


def test_create_from_text() -> None:
    string = apyds.String("string")
    assert str(string) == "string"

    # string never fails


def test_create_from_bytes(s: apyds.String) -> None:
    string = apyds.String(s.data())
    assert str(string) == "string"

    with pytest.raises(ValueError):
        string = apyds.String(s.data(), 100)


def test_create_fail() -> None:
    with pytest.raises(TypeError):
        string = apyds.String(100)
