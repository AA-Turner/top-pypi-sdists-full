from fa_purity import Result, ResultE

from .typing import Callable, TypeVar

_T = TypeVar("_T")


def handle_value_error(process: Callable[[], _T]) -> ResultE[_T]:
    try:
        return Result.success(process())
    except ValueError as e:
        return Result.failure(e)
