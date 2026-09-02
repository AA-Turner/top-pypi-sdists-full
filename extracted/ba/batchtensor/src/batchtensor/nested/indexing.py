r"""Contain some tensor indexing functions for nested data."""

from __future__ import annotations

__all__ = ["index_select_along_batch", "index_select_along_seq"]


from functools import partial
from typing import TYPE_CHECKING, Any, TypeVar

from batchtensor import tensor
from batchtensor.recursive import recursive_apply

if TYPE_CHECKING:
    import torch

T = TypeVar("T")


def index_select_along_batch(data: Any, index: torch.Tensor) -> Any:
    r"""Return the tensors which indexes the ``input`` tensor along the
    batch dimension using the entries in ``index`` which is a
    ``LongTensor``.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        index: The 1-D tensor containing the indices to index.

    Returns:
        The indexed tensors along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import index_select_along_batch
    >>> tensors = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = index_select_along_batch(tensors, torch.tensor([2, 4]))
    >>> out
    {'a': tensor([[4, 5], [8, 9]]), 'b': tensor([2, 0])}
    >>> out = index_select_along_batch(tensors, torch.tensor([4, 3, 2, 1, 0]))
    >>> out
    {'a': tensor([[8, 9], [6, 7], [4, 5], [2, 3], [0, 1]]), 'b': tensor([0, 1, 2, 3, 4])}

    ```
    """
    return recursive_apply(data, partial(tensor.index_select_along_batch, index=index))


def index_select_along_seq(data: Any, index: torch.Tensor) -> Any:
    r"""Return the tensors which indexes the ``input`` tensor along the
    sequence dimension using the entries in ``index`` which is a
    ``LongTensor``.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        index: The 1-D tensor containing the indices to index.

    Returns:
        The indexed tensors along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import index_select_along_seq
    >>> tensors = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = index_select_along_seq(tensors, torch.tensor([2, 4]))
    >>> out
    {'a': tensor([[2, 4], [7, 9]]), 'b': tensor([[2, 0]])}
    >>> out = index_select_along_seq(tensors, torch.tensor([4, 3, 2, 1, 0]))
    >>> out
    {'a': tensor([[4, 3, 2, 1, 0], [9, 8, 7, 6, 5]]), 'b': tensor([[0, 1, 2, 3, 4]])}

    ```
    """
    return recursive_apply(data, partial(tensor.index_select_along_seq, index=index))
