from typing import TypeVar, Union

from typing_extensions import TypeGuard


class Omit:
    """
    Sentinel class for parameters that were not explicitly provided by the user.
    It is used to explicitly omit something from being sent in a request.
    """

    def __bool__(self) -> bool:
        return False


OMIT = Omit()
Omittable = Union[Omit, object]

T = TypeVar("T")


def is_given(value: Union[T, Omit]) -> TypeGuard[T]:
    """True unless the caller left the argument out entirely.

    The sentinel decides whether a field is sent. `None` is an ordinary value
    that means "no value": on a filter it reads the same as leaving the
    argument out, and on a field the server lets you clear, it clears.
    """
    return not isinstance(value, Omit)
