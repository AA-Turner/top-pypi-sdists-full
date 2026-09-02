r"""Contain some reduction functions for tensors."""

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

from batchtensor import tensor as bt
from batchtensor.recursive import recursive_apply


def amax_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the maximum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The maximum of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import amax_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = amax_along_batch(data)
    >>> out
    {'a': tensor([8, 9]), 'b': tensor(4)}
    >>> out = amax_along_batch(data, keepdim=True)
    >>> out
    {'a': tensor([[8, 9]]), 'b': tensor([4])}

    ```
    """
    return recursive_apply(data, partial(bt.amax_along_batch, keepdim=keepdim))


def amax_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the maximum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The maximum of all elements along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import amax_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = amax_along_seq(data)
    >>> out
    {'a': tensor([4, 9]), 'b': tensor([4])}
    >>> out = amax_along_seq(data, keepdim=True)
    >>> out
    {'a': tensor([[4], [9]]), 'b': tensor([[4]])}

    ```
    """
    return recursive_apply(data, partial(bt.amax_along_seq, keepdim=keepdim))


def amin_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the minimum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The minimum of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import amin_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = amin_along_batch(data)
    >>> out
    {'a': tensor([0, 1]), 'b': tensor(0)}
    >>> out = amin_along_batch(data, keepdim=True)
    >>> out
    {'a': tensor([[0, 1]]), 'b': tensor([0])}

    ```
    """
    return recursive_apply(data, partial(bt.amin_along_batch, keepdim=keepdim))


def amin_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the minimum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The minimum of all elements along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import amin_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = amin_along_seq(data)
    >>> out
    {'a': tensor([0, 5]), 'b': tensor([0])}
    >>> out = amin_along_seq(data, keepdim=True)
    >>> out
    {'a': tensor([[0], [5]]), 'b': tensor([[0]])}

    ```
    """
    return recursive_apply(data, partial(bt.amin_along_seq, keepdim=keepdim))


def argmax_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the indices of the maximum value of all elements along the
    batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The indices of the maximum value of all elements along the
            batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import argmax_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = argmax_along_batch(data)
    >>> out
    {'a': tensor([4, 4]), 'b': tensor(0)}
    >>> out = argmax_along_batch(data, keepdim=True)
    >>> out
    {'a': tensor([[4, 4]]), 'b': tensor([0])}

    ```
    """
    return recursive_apply(data, partial(bt.argmax_along_batch, keepdim=keepdim))


def argmax_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the indices of the maximum value of all elements along the
    sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The indices of the maximum value of all elements along the
            sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import argmax_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = argmax_along_seq(data)
    >>> out
    {'a': tensor([4, 4]), 'b': tensor([0])}
    >>> out = argmax_along_seq(data, keepdim=True)
    >>> out
    {'a': tensor([[4], [4]]), 'b': tensor([[0]])}

    ```
    """
    return recursive_apply(data, partial(bt.argmax_along_seq, keepdim=keepdim))


def argmin_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the indices of the minimum value of all elements along the
    batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The indices of the minimum value of all elements along the
            batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import argmin_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = argmin_along_batch(data)
    >>> out
    {'a': tensor([0, 0]), 'b': tensor(4)}
    >>> out = argmin_along_batch(data, keepdim=True)
    >>> out
    {'a': tensor([[0, 0]]), 'b': tensor([4])}

    ```
    """
    return recursive_apply(data, partial(bt.argmin_along_batch, keepdim=keepdim))


def argmin_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the indices of the minimum value of all elements along the
    sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The indices of the minimum value of all elements along the
            sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import argmin_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = argmin_along_seq(data)
    >>> out
    {'a': tensor([0, 0]), 'b': tensor([4])}
    >>> out = argmin_along_seq(data, keepdim=True)
    >>> out
    {'a': tensor([[0], [0]]), 'b': tensor([[4]])}

    ```
    """
    return recursive_apply(data, partial(bt.argmin_along_seq, keepdim=keepdim))


def max_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the maximum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the maximum values and
             the second tensor, which must have dtype long, with their
             indices in the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import max_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = max_along_batch(data)
    >>> out
    {'a': torch.return_types.max(
    values=tensor([8, 9]),
    indices=tensor([4, 4])),
    'b': torch.return_types.max(
    values=tensor(4),
    indices=tensor(0))}
    >>> out = max_along_batch(data, keepdim=True)
    >>> out
    {'a': torch.return_types.max(
    values=tensor([[8, 9]]),
    indices=tensor([[4, 4]])),
    'b': torch.return_types.max(
    values=tensor([4]),
    indices=tensor([0]))}

    ```
    """
    return recursive_apply(data, partial(bt.max_along_batch, keepdim=keepdim))


def max_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the maximum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the maximum values and
            the second tensor, which must have dtype long, with their
            indices in the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import max_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = max_along_seq(data)
    >>> out
    {'a': torch.return_types.max(
    values=tensor([4, 9]),
    indices=tensor([4, 4])),
    'b': torch.return_types.max(
    values=tensor([4]),
    indices=tensor([0]))}
    >>> out = max_along_seq(data, keepdim=True)
    >>> out
    {'a': torch.return_types.max(
    values=tensor([[4], [9]]),
    indices=tensor([[4], [4]])),
    'b': torch.return_types.max(
    values=tensor([[4]]),
    indices=tensor([[0]]))}

    ```
    """
    return recursive_apply(data, partial(bt.max_along_seq, keepdim=keepdim))


def mean_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the mean of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The mean of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import mean_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0.0, 1.0], [2.0, 3.0], [4.0, 5.0], [6.0, 7.0], [8.0, 9.0]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0], dtype=torch.float),
    ... }
    >>> out = mean_along_batch(data)
    >>> out
    {'a': tensor([4., 5.]), 'b': tensor(2.)}
    >>> out = mean_along_batch(data, keepdim=True)
    >>> out
    {'a': tensor([[4., 5.]]), 'b': tensor([2.])}

    ```
    """
    return recursive_apply(data, partial(bt.mean_along_batch, keepdim=keepdim))


def mean_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the mean of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import mean_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0.0, 1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0, 9.0]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]], dtype=torch.float),
    ... }
    >>> out = mean_along_seq(data)
    >>> out
    {'a': tensor([2., 7.]), 'b': tensor([2.])}
    >>> out = mean_along_seq(data, keepdim=True)
    >>> out
    {'a': tensor([[2.], [7.]]), 'b': tensor([[2.]])}

    ```
    """
    return recursive_apply(data, partial(bt.mean_along_seq, keepdim=keepdim))


def median_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the median of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the median values and
            the second tensor, which must have dtype long, with their
            indices in the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import median_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = median_along_batch(data)
    >>> out
    {'a': torch.return_types.median(
    values=tensor([4, 5]),
    indices=tensor([2, 2])),
    'b': torch.return_types.median(
    values=tensor(2),
    indices=tensor(2))}
    >>> out = median_along_batch(data, keepdim=True)
    >>> out
    {'a': torch.return_types.median(
    values=tensor([[4, 5]]),
    indices=tensor([[2, 2]])),
    'b': torch.return_types.median(
    values=tensor([2]),
    indices=tensor([2]))}

    ```
    """
    return recursive_apply(data, partial(bt.median_along_batch, keepdim=keepdim))


def median_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the median of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the median values and
            the second tensor, which must have dtype long, with their
            indices in the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import median_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = median_along_seq(data)
    >>> out
    {'a': torch.return_types.median(
    values=tensor([2, 7]),
    indices=tensor([2, 2])),
    'b': torch.return_types.median(
    values=tensor([2]),
    indices=tensor([2]))}
    >>> out = median_along_seq(data, keepdim=True)
    >>> out
    {'a': torch.return_types.median(
    values=tensor([[2], [7]]),
    indices=tensor([[2], [2]])),
    'b': torch.return_types.median(
    values=tensor([[2]]),
    indices=tensor([[2]]))}

    ```
    """
    return recursive_apply(data, partial(bt.median_along_seq, keepdim=keepdim))


def min_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the minimum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the minimum values and
            the second tensor, which must have dtype long, with their
            indices in the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import min_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = min_along_batch(data)
    >>> out
    {'a': torch.return_types.min(
    values=tensor([0, 1]),
    indices=tensor([0, 0])),
    'b': torch.return_types.min(
    values=tensor(0),
    indices=tensor(4))}
    >>> out = min_along_batch(data, keepdim=True)
    >>> out
    {'a': torch.return_types.min(
    values=tensor([[0, 1]]),
    indices=tensor([[0, 0]])),
    'b': torch.return_types.min(
    values=tensor([0]),
    indices=tensor([4]))}

    ```
    """
    return recursive_apply(data, partial(bt.min_along_batch, keepdim=keepdim))


def min_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the minimum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the minimum values and
            the second tensor, which must have dtype long, with their
            indices in the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import min_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = min_along_seq(data)
    >>> out
    {'a': torch.return_types.min(
    values=tensor([0, 5]),
    indices=tensor([0, 0])),
    'b': torch.return_types.min(
    values=tensor([0]),
    indices=tensor([4]))}
    >>> out = min_along_seq(data, keepdim=True)
    >>> out
    {'a': torch.return_types.min(
    values=tensor([[0], [5]]),
    indices=tensor([[0], [0]])),
    'b': torch.return_types.min(
    values=tensor([[0]]),
    indices=tensor([[4]]))}

    ```
    """
    return recursive_apply(data, partial(bt.min_along_seq, keepdim=keepdim))


def prod_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the product of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The product of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import prod_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([5, 4, 3, 2, 1]),
    ... }
    >>> out = prod_along_batch(data)
    >>> out
    {'a': tensor([  0, 945]), 'b': tensor(120)}
    >>> out = prod_along_batch(data, keepdim=True)
    >>> out
    {'a': tensor([[  0, 945]]), 'b': tensor([120])}

    ```
    """
    return recursive_apply(data, partial(bt.prod_along_batch, keepdim=keepdim))


def prod_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the product of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The product of all elements along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import prod_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[5, 4, 3, 2, 1]]),
    ... }
    >>> out = prod_along_seq(data)
    >>> out
    {'a': tensor([    0, 15120]), 'b': tensor([120])}
    >>> out = prod_along_seq(data, keepdim=True)
    >>> out
    {'a': tensor([[    0], [15120]]), 'b': tensor([[120]])}

    ```
    """
    return recursive_apply(data, partial(bt.prod_along_seq, keepdim=keepdim))


def sum_along_batch(data: Any, keepdim: bool = False) -> Any:
    r"""Return the sum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The sum of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import sum_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = sum_along_batch(data)
    >>> out
    {'a': tensor([20, 25]), 'b': tensor(10)}
    >>> out = sum_along_batch(data, keepdim=True)
    >>> out
    {'a': tensor([[20, 25]]), 'b': tensor([10])}

    ```
    """
    return recursive_apply(data, partial(bt.sum_along_batch, keepdim=keepdim))


def sum_along_seq(data: Any, keepdim: bool = False) -> Any:
    r"""Return the sum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The sum of all elements along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import sum_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = sum_along_seq(data)
    >>> out
    {'a': tensor([10, 35]), 'b': tensor([10])}
    >>> out = sum_along_seq(data, keepdim=True)
    >>> out
    {'a': tensor([[10], [35]]), 'b': tensor([[10]])}

    ```
    """
    return recursive_apply(data, partial(bt.sum_along_seq, keepdim=keepdim))
