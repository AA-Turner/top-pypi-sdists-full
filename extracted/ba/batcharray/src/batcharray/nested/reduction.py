r"""Contain some reduction functions for arrays."""

from __future__ import annotations

__all__ = [
    "amax_along_batch",
    "amax_along_seq",
    "amin_along_batch",
    "amin_along_seq",
    "argmax_along_batch",
    "argmax_along_seq",
    "argmin_along_batch",
    "argmin_along_seq",
    "max_along_batch",
    "max_along_seq",
    "mean_along_batch",
    "mean_along_seq",
    "median_along_batch",
    "median_along_seq",
    "min_along_batch",
    "min_along_seq",
    "prod_along_batch",
    "prod_along_seq",
    "sum_along_batch",
    "sum_along_seq",
]

from functools import partial
from typing import Any

from coola.recursive import recursive_apply

from batcharray import array as ba


def amax_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the maximum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The maximum of all elements along the batch dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import amax_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = amax_along_batch(data)
        >>> out
        {'a': array([8, 9]), 'b': np.int64(4)}
        >>> out = amax_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[8, 9]]), 'b': array([4])}

        ```
    """
    return recursive_apply(data, partial(ba.amax_along_batch, keepdims=keepdims))


def amax_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the maximum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The maximum of all elements along the sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import amax_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = amax_along_seq(data)
        >>> out
        {'a': array([4, 9]), 'b': array([4])}
        >>> out = amax_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[4], [9]]), 'b': array([[4]])}

        ```
    """
    return recursive_apply(data, partial(ba.amax_along_seq, keepdims=keepdims))


def amin_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the minimum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The minimum of all elements along the batch dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import amin_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = amin_along_batch(data)
        >>> out
        {'a': array([0, 1]), 'b': np.int64(0)}
        >>> out = amin_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[0, 1]]), 'b': array([0])}

        ```
    """
    return recursive_apply(data, partial(ba.amin_along_batch, keepdims=keepdims))


def amin_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the minimum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The minimum of all elements along the sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import amin_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = amin_along_seq(data)
        >>> out
        {'a': array([0, 5]), 'b': array([0])}
        >>> out = amin_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[0], [5]]), 'b': array([[0]])}

        ```
    """
    return recursive_apply(data, partial(ba.amin_along_seq, keepdims=keepdims))


def argmax_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the indices of the maximum value of all elements along the
    batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The indices of the maximum value of all elements along the
            batch dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import argmax_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = argmax_along_batch(data)
        >>> out
        {'a': array([4, 4]), 'b': np.int64(0)}
        >>> out = argmax_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[4, 4]]), 'b': array([0])}

        ```
    """
    return recursive_apply(data, partial(ba.argmax_along_batch, keepdims=keepdims))


def argmax_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the indices of the maximum value of all elements along the
    sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The indices of the maximum value of all elements along the
            sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import argmax_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = argmax_along_seq(data)
        >>> out
        {'a': array([4, 4]), 'b': array([0])}
        >>> out = argmax_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[4], [4]]), 'b': array([[0]])}

        ```
    """
    return recursive_apply(data, partial(ba.argmax_along_seq, keepdims=keepdims))


def argmin_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the indices of the minimum value of all elements along the
    batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The indices of the minimum value of all elements along the
            batch dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import argmin_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = argmin_along_batch(data)
        >>> out
        {'a': array([0, 0]), 'b': np.int64(4)}
        >>> out = argmin_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[0, 0]]), 'b': array([4])}

        ```
    """
    return recursive_apply(data, partial(ba.argmin_along_batch, keepdims=keepdims))


def argmin_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the indices of the minimum value of all elements along the
    sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The indices of the minimum value of all elements along the
            sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import argmin_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = argmin_along_seq(data)
        >>> out
        {'a': array([0, 0]), 'b': array([4])}
        >>> out = argmin_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[0], [0]]), 'b': array([[4]])}

        ```
    """
    return recursive_apply(data, partial(ba.argmin_along_seq, keepdims=keepdims))


def max_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the maximum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The maximum of all elements along the batch dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import max_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = max_along_batch(data)
        >>> out
        {'a': array([8, 9]), 'b': np.int64(4)}
        >>> out = max_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[8, 9]]), 'b': array([4])}

        ```
    """
    return recursive_apply(data, partial(ba.max_along_batch, keepdims=keepdims))


def max_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the maximum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The maximum of all elements along the sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import max_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = max_along_seq(data)
        >>> out
        {'a': array([4, 9]), 'b': array([4])}
        >>> out = max_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[4], [9]]), 'b': array([[4]])}

        ```
    """
    return recursive_apply(data, partial(ba.max_along_seq, keepdims=keepdims))


def mean_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the mean of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The mean of all elements along the batch dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import mean_along_batch
        >>> data = {
        ...     "a": np.array([[0.0, 1.0], [2.0, 3.0], [4.0, 5.0], [6.0, 7.0], [8.0, 9.0]]),
        ...     "b": np.array([4, 3, 2, 1, 0], dtype=np.float32),
        ... }
        >>> out = mean_along_batch(data)
        >>> out
        {'a': array([4., 5.]), 'b': np.float32(2.0)}
        >>> out = mean_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[4., 5.]]), 'b': array([2.], dtype=float32)}

        ```
    """
    return recursive_apply(data, partial(ba.mean_along_batch, keepdims=keepdims))


def mean_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the mean of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The mean of all elements along the sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import mean_along_seq
        >>> data = {
        ...     "a": np.array([[0.0, 1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0, 9.0]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]], dtype=np.float32),
        ... }
        >>> out = mean_along_seq(data)
        >>> out
        {'a': array([2., 7.]), 'b': array([2.], dtype=float32)}
        >>> out = mean_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[2.], [7.]]), 'b': array([[2.]], dtype=float32)}

        ```
    """
    return recursive_apply(data, partial(ba.mean_along_seq, keepdims=keepdims))


def median_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the median of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        A new array holding the result. If the input contains integers
            or floats smaller than ``np.float64``, then the output
            data-type is ``np.float64``. Otherwise, the data-type of
            the output is the same as that of the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import median_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = median_along_batch(data)
        >>> out
        {'a': array([4., 5.]), 'b': np.float64(2.0)}
        >>> out = median_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[4., 5.]]), 'b': array([2.])}

        ```
    """
    return recursive_apply(data, partial(ba.median_along_batch, keepdims=keepdims))


def median_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the median of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        A new array holding the result. If the input contains integers
            or floats smaller than ``np.float64``, then the output
            data-type is ``np.float64``. Otherwise, the data-type of
            the output is the same as that of the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import median_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = median_along_seq(data)
        >>> out
        {'a': array([2., 7.]), 'b': array([2.])}
        >>> out = median_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[2.], [7.]]), 'b': array([[2.]])}

        ```
    """
    return recursive_apply(data, partial(ba.median_along_seq, keepdims=keepdims))


def min_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the minimum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The minimum of all elements along the batch dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import min_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = min_along_batch(data)
        >>> out
        {'a': array([0, 1]), 'b': np.int64(0)}
        >>> out = min_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[0, 1]]), 'b': array([0])}

        ```
    """
    return recursive_apply(data, partial(ba.min_along_batch, keepdims=keepdims))


def min_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the minimum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The minimum of all elements along the sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import min_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = min_along_seq(data)
        >>> out
        {'a': array([0, 5]), 'b': array([0])}
        >>> out = min_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[0], [5]]), 'b': array([[0]])}

        ```
    """
    return recursive_apply(data, partial(ba.min_along_seq, keepdims=keepdims))


def prod_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the product of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The product of all elements along the batch dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import prod_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([5, 4, 3, 2, 1]),
        ... }
        >>> out = prod_along_batch(data)
        >>> out
        {'a': array([  0, 945]), 'b': np.int64(120)}
        >>> out = prod_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[  0, 945]]), 'b': array([120])}

        ```
    """
    return recursive_apply(data, partial(ba.prod_along_batch, keepdims=keepdims))


def prod_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the product of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The product of all elements along the sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import prod_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[5, 4, 3, 2, 1]]),
        ... }
        >>> out = prod_along_seq(data)
        >>> out
        {'a': array([    0, 15120]), 'b': array([120])}
        >>> out = prod_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[    0], [15120]]), 'b': array([[120]])}

        ```
    """
    return recursive_apply(data, partial(ba.prod_along_seq, keepdims=keepdims))


def sum_along_batch(data: Any, keepdims: bool = False) -> Any:
    r"""Return the sum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The sum of all elements along the batch dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import sum_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = sum_along_batch(data)
        >>> out
        {'a': array([20, 25]), 'b': np.int64(10)}
        >>> out = sum_along_batch(data, keepdims=True)
        >>> out
        {'a': array([[20, 25]]), 'b': array([10])}

        ```
    """
    return recursive_apply(data, partial(ba.sum_along_batch, keepdims=keepdims))


def sum_along_seq(data: Any, keepdims: bool = False) -> Any:
    r"""Return the sum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a array.
        keepdims: Whether the output array has dim retained or not.

    Returns:
        The sum of all elements along the sequence dimension.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import sum_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = sum_along_seq(data)
        >>> out
        {'a': array([10, 35]), 'b': array([10])}
        >>> out = sum_along_seq(data, keepdims=True)
        >>> out
        {'a': array([[10], [35]]), 'b': array([[10]])}

        ```
    """
    return recursive_apply(data, partial(ba.sum_along_seq, keepdims=keepdims))
