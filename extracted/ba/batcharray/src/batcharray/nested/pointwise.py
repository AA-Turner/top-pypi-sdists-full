r"""Contain some array point-wise functions for nested data."""

from __future__ import annotations

__all__ = [
    "abs",
    "clip",
    "exp",
    "exp2",
    "expm1",
    "log",
    "log1p",
    "log2",
    "log10",
]

from functools import partial
from typing import Any

import numpy as np
from coola.recursive import recursive_apply


def abs(data: Any) -> Any:  # noqa: A001
    r"""Return new arrays with the absolute value of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The absolute value of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import abs
        >>> data = {
        ...     "a": np.array([[-4, -3], [-2, -1], [0, 1], [2, 3], [4, 5]]),
        ...     "b": np.array([2, 1, 0, -1, -2]),
        ... }
        >>> out = abs(data)
        >>> out
        {'a': array([[4, 3], [2, 1], [0, 1], [2, 3], [4, 5]]), 'b': array([2, 1, 0, 1, 2])}

        ```
    """
    return recursive_apply(data, np.abs)


def clip(data: Any, a_min: float | None = None, a_max: float | None = None) -> Any:
    r"""Clamp all elements in input into the range ``[min, max]``.

    Args:
        data: The input data. Each item must be an array .
        a_min: The lower-bound of the range to be clamped to.
        a_max: The upper-bound of the range to be clamped to.

    Returns:
        The clamp value of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import clip
        >>> data = {
        ...     "a": np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
        ...     "b": np.array([5, 4, 3, 2, 1]),
        ... }
        >>> out = clip(data, a_min=1, a_max=5)
        >>> out
        {'a': array([[1, 2], [3, 4], [5, 5], [5, 5], [5, 5]]), 'b': array([5, 4, 3, 2, 1])}

        ```
    """
    return recursive_apply(data, partial(np.clip, a_min=a_min, a_max=a_max))


def exp(data: Any) -> Any:
    r"""Return new arrays with the exponential of the elements.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The exponential of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import exp
        >>> data = {
        ...     "a": np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
        ...     "b": np.array([5, 4, 3, 2, 1]),
        ... }
        >>> out = exp(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.exp)


def exp2(data: Any) -> Any:
    r"""Return new arrays with the base two exponential of the elements.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The base two exponential of the elements. The output has the
            same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import exp2
        >>> data = {
        ...     "a": np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
        ...     "b": np.array([5, 4, 3, 2, 1]),
        ... }
        >>> out = exp2(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.exp2)


def expm1(data: Any) -> Any:
    r"""Return new arrays with the exponential of the elements minus 1.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The exponential of the elements minus 1. The output has the
            same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import expm1
        >>> data = {
        ...     "a": np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
        ...     "b": np.array([5, 4, 3, 2, 1]),
        ... }
        >>> out = expm1(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.expm1)


def log(data: Any) -> Any:
    r"""Return new arrays with the natural logarithm of the elements.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The natural logarithm of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import log
        >>> data = {
        ...     "a": np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
        ...     "b": np.array([5, 4, 3, 2, 1]),
        ... }
        >>> out = log(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.log)


def log2(data: Any) -> Any:
    r"""Return new arrays with the logarithm to the base 2 of the
    elements.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The logarithm to the base 2 of the elements. The output has
            the same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import log2
        >>> data = {
        ...     "a": np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
        ...     "b": np.array([5, 4, 3, 2, 1]),
        ... }
        >>> out = log2(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.log2)


def log10(data: Any) -> Any:
    r"""Return new arrays with the logarithm to the base 10 of the
    elements.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The with the logarithm to the base 10 of the elements. The
            output has the same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import log10
        >>> data = {
        ...     "a": np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
        ...     "b": np.array([5, 4, 3, 2, 1]),
        ... }
        >>> out = log10(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.log10)


def log1p(data: Any) -> Any:
    r"""Return new arrays with the natural logarithm of ``(1 + input)``.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The natural logarithm of ``(1 + input)``. The output has the
            same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import log1p
        >>> data = {
        ...     "a": np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
        ...     "b": np.array([5, 4, 3, 2, 1]),
        ... }
        >>> out = log1p(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.log1p)
