from typing import TypeVar, TypeGuard, Type
from ratio.router.route import Route

_T = TypeVar("_T", bound=type)


def is_route(value: _T) -> TypeGuard[Type[Route]]:
    try:
        return issubclass(value, Route) and value is not Route
    except TypeError:
        return False
