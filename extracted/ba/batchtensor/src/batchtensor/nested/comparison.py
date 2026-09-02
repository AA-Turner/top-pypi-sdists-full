r"""Contain some tensor comparison functions for nested data."""

from __future__ import annotations

__all__ = ["argsort_along_batch", "argsort_along_seq", "sort_along_batch", "sort_along_seq"]

from functools import partial
from typing import Any

from batchtensor import tensor as bt
from batchtensor.recursive import recursive_apply


def argsort_along_batch(data: Any, descending: bool = False, **kwargs: Any) -> Any:
    r"""Return the indices that sort a tensor along the batch dimension
    in ascending order by value.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        descending: Controls the sorting order (ascending or
            descending).
        kwargs: Additional keywords arguments for ``torch.argsort``.

    Returns:
        The indices that sort each tensor along the batch dimension

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import argsort_along_batch
    >>> data = {
    ...     "a": torch.tensor([[2, 6], [0, 3], [4, 9], [8, 1], [5, 7]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = argsort_along_batch(data)
    >>> out
    {'a': tensor([[1, 3], [0, 1], [2, 0], [4, 4], [3, 2]]), 'b': tensor([4, 3, 2, 1, 0])}
    >>> out = argsort_along_batch(data, descending=True)
    >>> out
    {'a': tensor([[3, 2], [4, 4], [2, 0], [0, 1], [1, 3]]), 'b': tensor([0, 1, 2, 3, 4])}

    ```
    """
    return recursive_apply(data, partial(bt.argsort_along_batch, descending=descending, **kwargs))


def argsort_along_seq(data: Any, descending: bool = False, **kwargs: Any) -> Any:
    r"""Return the indices that sort each tensor along the sequence
    dimension in ascending order by value.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        descending: Controls the sorting order (ascending or
            descending).
        kwargs: Additional keywords arguments for ``torch.argsort``.

    Returns:
        The indices that sort each tensor along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import argsort_along_seq
    >>> data = {
    ...     "a": torch.tensor([[7, 3, 0, 8, 5], [1, 9, 6, 4, 2]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = argsort_along_seq(data)
    >>> out
    {'a': tensor([[2, 1, 4, 0, 3], [0, 4, 3, 2, 1]]), 'b': tensor([[4, 3, 2, 1, 0]])}
    >>> out = argsort_along_seq(data, descending=True)
    >>> out
    {'a': tensor([[3, 0, 4, 1, 2], [1, 2, 3, 4, 0]]), 'b': tensor([[0, 1, 2, 3, 4]])}

    ```
    """
    return recursive_apply(data, partial(bt.argsort_along_seq, descending=descending, **kwargs))


def sort_along_batch(data: Any, descending: bool = False, **kwargs: Any) -> Any:
    r"""Sort the elements of the input tensor along the batch dimension
    in ascending order by value.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        descending: Controls the sorting order (ascending or
            descending).
        kwargs: Additional keywords arguments for ``torch.sort``.

    Returns:
        A similar object where each tensor is replaced by a namedtuple
            of (values, indices), where the values are the sorted
            values and indices are the indices of the elements in the
            original input tensor.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import sort_along_batch
    >>> data = {
    ...     "a": torch.tensor([[2, 6], [0, 3], [4, 9], [8, 1], [5, 7]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = sort_along_batch(data)
    >>> out
    {'a': torch.return_types.sort(
    values=tensor([[0, 1], [2, 3], [4, 6], [5, 7], [8, 9]]),
    indices=tensor([[1, 3], [0, 1], [2, 0], [4, 4], [3, 2]])),
    'b': torch.return_types.sort(
    values=tensor([0, 1, 2, 3, 4]),
    indices=tensor([4, 3, 2, 1, 0]))}
    >>> out = sort_along_batch(data, descending=True)
    >>> out
    {'a': torch.return_types.sort(
    values=tensor([[8, 9], [5, 7], [4, 6], [2, 3], [0, 1]]),
    indices=tensor([[3, 2], [4, 4], [2, 0], [0, 1], [1, 3]])),
    'b': torch.return_types.sort(
    values=tensor([4, 3, 2, 1, 0]),
    indices=tensor([0, 1, 2, 3, 4]))}

    ```
    """
    return recursive_apply(data, partial(bt.sort_along_batch, descending=descending, **kwargs))


def sort_along_seq(data: Any, descending: bool = False, **kwargs: Any) -> Any:
    r"""Sort the elements of the input tensor along the sequence
    dimension in ascending order by value.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        descending: Controls the sorting order (ascending or
            descending).
        kwargs: Additional keywords arguments for ``torch.sort``.

    Returns:
        A similar object where each tensor is replaced by a namedtuple
            of (values, indices), where the values are the sorted
            values and indices are the indices of the elements in the
            original input tensor.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import sort_along_seq
    >>> data = {
    ...     "a": torch.tensor([[7, 3, 0, 8, 5], [1, 9, 6, 4, 2]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = sort_along_seq(data)
    >>> out
    {'a': torch.return_types.sort(
    values=tensor([[0, 3, 5, 7, 8], [1, 2, 4, 6, 9]]),
    indices=tensor([[2, 1, 4, 0, 3], [0, 4, 3, 2, 1]])),
    'b': torch.return_types.sort(
    values=tensor([[0, 1, 2, 3, 4]]),
    indices=tensor([[4, 3, 2, 1, 0]]))}
    >>> out = sort_along_seq(data, descending=True)
    >>> out
    {'a': torch.return_types.sort(
    values=tensor([[8, 7, 5, 3, 0], [9, 6, 4, 2, 1]]),
    indices=tensor([[3, 0, 4, 1, 2], [1, 2, 3, 4, 0]])),
    'b': torch.return_types.sort(
    values=tensor([[4, 3, 2, 1, 0]]),
    indices=tensor([[0, 1, 2, 3, 4]]))}

    ```
    """
    return recursive_apply(data, partial(bt.sort_along_seq, descending=descending, **kwargs))
