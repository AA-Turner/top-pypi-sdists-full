r"""Contain some indexing functions for tensors."""

from __future__ import annotations

__all__ = ["index_select_along_batch", "index_select_along_seq"]


import torch

from batchtensor.constants import BATCH_DIM, SEQ_DIM


def index_select_along_batch(tensor: torch.Tensor, index: torch.Tensor) -> torch.Tensor:
    r"""Return a new tensor which indexes the ``input`` tensor along the
    batch dimension using the entries in ``index`` which is a
    ``LongTensor``.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        index: The 1-D tensor containing the indices to index.

    Returns:
        The indexed tensor along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import index_select_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = index_select_along_batch(tensor, torch.tensor([2, 4]))
    >>> out
    tensor([[4, 5],
            [8, 9]])
    >>> out = index_select_along_batch(tensor, torch.tensor([4, 3, 2, 1, 0]))
    >>> out
    tensor([[8, 9],
            [6, 7],
            [4, 5],
            [2, 3],
            [0, 1]])

    ```
    """
    return tensor.index_select(dim=BATCH_DIM, index=index)


def index_select_along_seq(tensor: torch.Tensor, index: torch.Tensor) -> torch.Tensor:
    r"""Return a new tensor which indexes the ``input`` tensor along the
    sequence dimension using the entries in ``index`` which is a
    ``LongTensor``.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        index: The 1-D tensor containing the indices to index.

    Returns:
        The indexed tensor along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import index_select_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = index_select_along_seq(tensor, torch.tensor([2, 4]))
    >>> out
    tensor([[2, 4],
            [7, 9]])
    >>> out = index_select_along_seq(tensor, torch.tensor([4, 3, 2, 1, 0]))
    >>> out
    tensor([[4, 3, 2, 1, 0],
            [9, 8, 7, 6, 5]])

    ```
    """
    if index.ndim == 1:
        return tensor.index_select(dim=SEQ_DIM, index=index)
    batch_size, seq_len = index.shape[:2]
    batch_index = torch.arange(batch_size).repeat_interleave(seq_len)
    index = index.flatten().long()
    return tensor[batch_index, index].view(batch_size, seq_len, *tensor.shape[2:])
