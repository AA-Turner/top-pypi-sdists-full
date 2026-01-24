"""The standard `length` function extension."""

from collections.abc import Sized
from typing import Union

from jsonpath_rfc9535.filter_expressions import NOTHING
from jsonpath_rfc9535.filter_expressions import Nothing
from jsonpath_rfc9535.function_extensions import ExpressionType
from jsonpath_rfc9535.function_extensions import FilterFunction


class Length(FilterFunction):
    """The standard `length` function."""

    arg_types = [ExpressionType.VALUE]
    return_type = ExpressionType.VALUE

    def __call__(self, obj: Sized) -> Union[int, Nothing]:
        """Return an object's length.

        If the object does not have a length, the special _Nothing_ value is
        returned.
        """
        try:
            return len(obj)
        except TypeError:
            return NOTHING
