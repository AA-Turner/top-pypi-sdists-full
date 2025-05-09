import pytest
from parametrized import parametrized

data = parametrized.fixture('one', 'two')


def test_options():
    fixture = parametrized.fixture(name='override')
    assert fixture._pytestfixturefunction.name == 'override'
    assert parametrized(lambda x='': x, scope='module').kwargs == {'scope': 'module'}


def test_fixture(data):
    assert data in ('one', 'two')


@parametrized
def test_single(name='abc'):
    assert name in set('abc')


@parametrized.zip
def test_zip(name='abc', value=range(3)):
    assert (value, name) in enumerate('abc')


@parametrized.product
def test_product(name='abc', value=range(3)):
    assert name in set('abc') and value in (0, 1, 2)


def test_error():
    with pytest.raises(ValueError):

        @parametrized
        def _(name=(), value=()): ...

    @parametrized.zip
    def strict(name='abc', value=()): ...

    with pytest.raises(ValueError):
        list(strict.pytestmark[0].args[1])


@parametrized.product
def test_param(key=[0], value=[0, pytest.param(1, marks=pytest.mark.xfail())]):
    assert key == value
