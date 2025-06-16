import pytest

from typed_envs import EnvVarFactory


def test_register_string_converter():
    class MyType:
        def __init__(self, value: int): ...

    factory = EnvVarFactory("TEST")
    assert not factory.default_string_converters

    factory.register_string_converter(MyType, int)
    assert MyType in factory.default_string_converters
    assert factory.default_string_converters[MyType] is int

    # Cannot register if one is already registered
    with pytest.raises(ValueError):
        factory.register_string_converter(MyType, int)
