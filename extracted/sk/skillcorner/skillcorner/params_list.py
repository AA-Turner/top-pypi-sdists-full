from collections.abc import Callable, Iterable
from typing import Any

import makefun


def _join_if_necessary(value: Any) -> Any:
    """
    Determine if the given value should be converted into a string by joining its elements,
    and perform the conversion if required.
    """
    if isinstance(value, Iterable) and not isinstance(value, str | dict):
        return ','.join(map(str, value))
    return value


def params_list(fit_request: Callable) -> Callable:
    """
    Convert parameters that are lists into a single string where the list elements are joined together.
    This is necessary because the server expects a string input rather than a conventional parameter list.
    """

    @makefun.wraps(fit_request)
    def wrapper(*args, **kwargs) -> Any:
        if params := kwargs.pop('params', {}):
            params = {field: _join_if_necessary(value) for field, value in params.items()}

        return fit_request(*args, **kwargs, params=params)

    return wrapper
