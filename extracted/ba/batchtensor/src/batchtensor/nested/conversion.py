r"""Contain functions to convert nested data."""

from __future__ import annotations

__all__ = ["as_tensor", "from_numpy", "to_numpy"]

from functools import partial
from typing import Any

import torch

from batchtensor.recursive import recursive_apply


def as_tensor(
    data: Any, dtype: torch.dtype | None = None, device: torch.device | None = None
) -> Any:
    r"""Create a new nested data structure with ``torch.Tensor``s.

    Args:
        data: The input data. Each item must be a ``torch.Tensor``
            compatible value.
        dtype: The desired data type of returned tensors. If ``None``,
            it infers data type from data.
        device: The device of the constructed tensors. If ``None``
            and data is a tensor then the device of data is used.
            If ``None`` and data is not a tensor then the result
            tensor is constructed on the current device.

    Returns:
        A nested data structure with ``torch.Tensor``s. The output data
            has the same structure as the input.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from batchtensor.nested import as_tensor
    >>> data = {"a": np.ones((2, 5), dtype=np.float32), "b": np.arange(5), "c": 42}
    >>> out = as_tensor(data)
    >>> out
    {'a': tensor([[1., 1., 1., 1., 1.], [1., 1., 1., 1., 1.]]),
     'b': tensor([0, 1, 2, 3, 4]),
     'c': tensor(42)}

    ```
    """
    return recursive_apply(data, partial(torch.as_tensor, dtype=dtype, device=device))


def from_numpy(data: Any) -> Any:
    r"""Create a new nested data structure where the ``numpy.ndarray``s
    are converted to ``torch.Tensor``s.

    Note:
        The returned ``torch.Tensor``s and ``numpy.ndarray``s share the
        same memory. Modifications to the ``torch.Tensor``s will be
        reflected in the ``numpy.ndarray``s and vice versa.

    Args:
        data: The input data. Each item must be a ``numpy.ndarray``.

    Returns:
        A nested data structure with ``torch.Tensor``s instead of
            ``numpy.ndarray``s. The output data has the same structure
            as the input.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from batchtensor.nested import from_numpy
    >>> data = {"a": np.ones((2, 5), dtype=np.float32), "b": np.arange(5)}
    >>> out = from_numpy(data)
    >>> out
    {'a': tensor([[1., 1., 1., 1., 1.], [1., 1., 1., 1., 1.]]), 'b': tensor([0, 1, 2, 3, 4])}

    ```
    """
    return recursive_apply(data, torch.from_numpy)


def to_numpy(data: Any) -> Any:
    r"""Create a new nested data structure where the ``torch.Tensor``s
    are converted to ``numpy.ndarray``s.

    Note:
        The returned ``torch.Tensor``s and ``numpy.ndarray``s share the
        same memory. Modifications to the ``torch.Tensor``s will be
        reflected in the ``numpy.ndarray``s and vice versa.

    Args:
        data: The input data. Each item must be a ``torch.Tensor``.

    Returns:
        A nested data structure with ``numpy.ndarray``s instead of
            ``torch.Tensor``s. The output data has the same structure
            as the input.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from batchtensor.nested import to_numpy
    >>> data = {"a": torch.ones(2, 5), "b": torch.tensor([0, 1, 2, 3, 4])}
    >>> out = to_numpy(data)
    >>> out
    {'a': array([[1., 1., 1., 1., 1.], [1., 1., 1., 1., 1.]], dtype=float32), 'b': array([0, 1, 2, 3, 4])}

    ```
    """
    return recursive_apply(data, lambda tensor: tensor.numpy())
