"""
Helper functions for validation of dtype.

For literal dtypes intended for use by end-users, see :mod:`numpydantic.dtype`
"""

import sys
from typing import Any, Union, get_args, get_origin

import numpy as np

from numpydantic.types import DtypeType

if sys.version_info >= (3, 10):
    from types import UnionType
else:
    UnionType = None


def validate_dtype(dtype: Any, target: DtypeType) -> bool:
    """
    Validate a dtype against the target dtype.

    If `dtype` or `target` are `Any`, validation passes trivially.
    The `dtype` may be `Any` when the dtype can't be determined,
    but failure to determine dtype shouldn't be fatal
    (e.g. BaseModel dtypes for empty arrays).

    Args:
        dtype: The dtype to validate
        target (:class:`.DtypeType`): The target dtype

    Returns:
        bool: ``True`` if valid, ``False`` otherwise
    """
    if target is Any or dtype is Any:
        return True

    if isinstance(target, tuple):
        valid = any(validate_dtype(dtype, target_dt) for target_dt in target)
    elif is_union(target):
        valid = any(
            [validate_dtype(dtype, target_dt) for target_dt in get_args(target)]
        )
    elif target is np.str_:
        valid = getattr(dtype, "type", None) in (np.str_, str) or dtype in (
            np.str_,
            str,
        )
    else:
        # try to match as any subclass, if target is a class
        try:
            valid = issubclass(dtype, target)
        except TypeError:
            # error expected if dtype or target is not a class
            # main type check - directly test dtype identity
            valid = dtype == target or getattr(dtype, "type", None) == target

    return valid


def is_union(dtype: DtypeType) -> bool:
    """
    Check if a dtype is a union
    """
    if UnionType is None:
        return get_origin(dtype) is Union
    else:
        return get_origin(dtype) in (Union, UnionType)
