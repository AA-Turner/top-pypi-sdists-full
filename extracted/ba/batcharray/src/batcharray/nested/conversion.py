r"""Contain functions to convert nested data."""

from __future__ import annotations

__all__ = ["to_list"]

from typing import Any

import numpy as np
from coola.recursive import recursive_apply


def to_list(data: Any) -> Any:
    r"""Create a new nested data structure where the ``numpy.ndarray``s
    are converted to lists.

    Args:
        data: The input data. Each item must be a ``numpy.ndarray``.

    Returns:
        A nested data structure with lists instead of
            ``numpy.ndarray``s. The output data has the same structure
            as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import to_list
        >>> data = {"a": np.ones((2, 5)), "b": np.array([0, 1, 2, 3, 4])}
        >>> out = to_list(data)
        >>> out
        {'a': [[1.0, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0, 1.0]], 'b': [0, 1, 2, 3, 4]}

        ```
    """
    return recursive_apply(
        data, lambda item: item.tolist() if isinstance(item, np.ndarray) else item
    )
