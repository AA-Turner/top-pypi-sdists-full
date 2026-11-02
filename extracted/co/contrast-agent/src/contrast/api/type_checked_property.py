# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
class _NoConstructorArg:
    pass


class TypeCheckedProperty:
    """
    A property that performs a type-check when set. If `__get__` is called before
    `__set__`, a value is created using the type's default constructor. This sort of
    mimics protobuf behavior.

    Note that type-checking is only performed on the top-level type. There is no
    recursive checking for nested data structures.
    """

    def __init__(self, _type, *, constructor_arg: object = _NoConstructorArg):
        self._type = _type
        self._constructor_args = (
            [] if constructor_arg is _NoConstructorArg else [constructor_arg]
        )

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if self.name not in obj.__dict__:
            self.__set__(obj, self._type(*self._constructor_args))
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if not isinstance(value, self._type):
            raise TypeError(
                f"Bad type when setting TypeCheckedProperty "
                f'"{self.name}" on {type(obj)} - '
                f"expected: {self._type}, found: {type(value)}"
            )
        obj.__dict__[self.name] = value
