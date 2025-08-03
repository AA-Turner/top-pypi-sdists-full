import rustmodels
import pytest

@pytest.mark.parametrize("number", [
    '5', '238743289749823'
])
def test_is_numeric_true(number):
    value = rustmodels._is_numeric(number)
    assert value

@pytest.mark.parametrize("string", [
    'a', '16a', '!', 'njhwbds523?'
])
def test_is_numeric_false(string):
    value = rustmodels._is_numeric('a')
    assert not value
