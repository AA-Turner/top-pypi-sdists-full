r"""Contain some mathematical functions for tensors."""

from __future__ import annotations

__all__ = [
    "cumprod_along_batch",
    "cumprod_along_seq",
    "cumsum_along_batch",
    "cumsum_along_seq",
]

from typing import TYPE_CHECKING

from batchtensor.constants import BATCH_DIM, SEQ_DIM

if TYPE_CHECKING:
    import torch


def cumprod_along_batch(tensor: torch.Tensor) -> torch.Tensor:
    r"""Return the cumulative product of elements of input in the batch
    dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.

    Returns:
        The cumulative product of elements of input in the batch
            dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import cumprod_along_batch
    >>> tensor = torch.tensor([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
    >>> out = cumprod_along_batch(tensor)
    >>> out
    tensor([[   1,    2], [   3,    8], [  15,   48], [ 105,  384], [ 945, 3840]])

    ```
    """
    return tensor.cumprod(dim=BATCH_DIM)


def cumprod_along_seq(tensor: torch.Tensor) -> torch.Tensor:
    r"""Return the cumulative product of elements of input in the
    sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.

    Returns:
        The cumulative product of elements of input in the sequence
            dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import cumprod_along_seq
    >>> tensor = torch.tensor([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
    >>> out = cumprod_along_seq(tensor)
    >>> out
    tensor([[    1,     2,     6,    24,   120],
            [    6,    42,   336,  3024, 30240]])

    ```
    """
    return tensor.cumprod(dim=SEQ_DIM)


def cumsum_along_batch(tensor: torch.Tensor) -> torch.Tensor:
    r"""Return the cumulative sum of elements of input in the batch
    dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.

    Returns:
        The cumulative sum of elements of input in the batch
            dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import cumsum_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = cumsum_along_batch(tensor)
    >>> out
    tensor([[ 0,  1], [ 2,  4], [ 6,  9], [12, 16], [20, 25]])

    ```
    """
    return tensor.cumsum(dim=BATCH_DIM)


def cumsum_along_seq(tensor: torch.Tensor) -> torch.Tensor:
    r"""Return the cumulative sum of elements of input in the sequence
    dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.

    Returns:
        The cumulative sum of elements of input in the sequence
            dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import cumsum_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = cumsum_along_seq(tensor)
    >>> out
    tensor([[ 0,  1,  3,  6, 10],
            [ 5, 11, 18, 26, 35]])

    ```
    """
    return tensor.cumsum(dim=SEQ_DIM)
