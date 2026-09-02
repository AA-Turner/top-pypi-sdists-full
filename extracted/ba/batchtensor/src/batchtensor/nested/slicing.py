r"""Contain some tensor slicing functions for nested data."""

from __future__ import annotations

__all__ = [
    "chunk_along_batch",
    "chunk_along_seq",
    "select_along_batch",
    "select_along_seq",
    "slice_along_batch",
    "slice_along_seq",
    "split_along_batch",
    "split_along_seq",
]

from functools import partial
from typing import TYPE_CHECKING, Any

from batchtensor import tensor as bt
from batchtensor.recursive import recursive_apply

if TYPE_CHECKING:
    from collections.abc import Hashable, Sequence

    import torch


def chunk_along_batch(
    data: dict[Hashable, torch.Tensor], chunks: int
) -> tuple[dict[Hashable, torch.Tensor], ...]:
    r"""Split all the tensors into chunks along the batch dimension.

    Each chunk is a view of the input tensor.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        chunks: Number of chunks to return.

    Returns:
        The data chuncks.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import chunk_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> outputs = chunk_along_batch(data, chunks=3)
    >>> outputs
    ({'a': tensor([[0, 1], [2, 3]]), 'b': tensor([4, 3])},
     {'a': tensor([[4, 5], [6, 7]]), 'b': tensor([2, 1])},
     {'a': tensor([[8, 9]]), 'b': tensor([0])})

    ```
    """
    keys = data.keys()
    return tuple(
        dict(zip(keys, values))
        for values in zip(*[bt.chunk_along_batch(tensor, chunks) for tensor in data.values()])
    )


def chunk_along_seq(
    data: dict[Hashable, torch.Tensor], chunks: int
) -> tuple[dict[Hashable, torch.Tensor], ...]:
    r"""Split all the tensors into chunks along the sequence dimension.

    Each chunk is a view of the input tensor.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        chunks: Number of chunks to return.

    Returns:
        The data chuncks.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import chunk_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> outputs = chunk_along_seq(data, chunks=3)
    >>> outputs
    ({'a': tensor([[0, 1], [5, 6]]), 'b': tensor([[4, 3]])},
     {'a': tensor([[2, 3], [7, 8]]), 'b': tensor([[2, 1]])},
     {'a': tensor([[4], [9]]), 'b': tensor([[0]])})

    ```
    """
    keys = data.keys()
    return tuple(
        dict(zip(keys, values))
        for values in zip(*[bt.chunk_along_seq(tensor, chunks) for tensor in data.values()])
    )


def select_along_batch(data: Any, index: int) -> Any:
    r"""Slice the tensors along the batch dimension at the given index.

    This function returns a view of the original tensor with the batch
    dimension removed.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        index: The index to select with.

    Returns:
        The sliced tensors along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import select_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = select_along_batch(data, index=2)
    >>> out
    {'a': tensor([4, 5]), 'b': tensor(2)}

    ```
    """
    return recursive_apply(data, partial(bt.select_along_batch, index=index))


def select_along_seq(data: Any, index: int) -> Any:
    r"""Slice the tensors along the sequence dimension at the given
    index.

    This function returns a view of the original tensor with the
    sequence dimension removed.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        index: The index to select with.

    Returns:
        The sliced tensors along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import select_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = select_along_seq(data, index=2)
    >>> out
    {'a': tensor([2, 7]), 'b': tensor([2])}

    ```
    """
    return recursive_apply(data, partial(bt.select_along_seq, index=index))


def slice_along_batch(data: Any, start: int = 0, stop: int | None = None, step: int = 1) -> Any:
    r"""Slice all the tensors along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        start: The index where the slicing of object starts.
        stop: The index where the slicing of object stops.
            ``None`` means last.
        step: The increment between each index for slicing.

    Returns:
        The sliced tensor along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import slice_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> out = slice_along_batch(data, start=2)
    >>> out
    {'a': tensor([[4, 5], [6, 7], [8, 9]]), 'b': tensor([2, 1, 0])}
    >>> out = slice_along_batch(data, stop=3)
    >>> out
    {'a': tensor([[0, 1], [2, 3], [4, 5]]), 'b': tensor([4, 3, 2])}
    >>> out = slice_along_batch(data, step=2)
    >>> out
    {'a': tensor([[0, 1], [4, 5], [8, 9]]), 'b': tensor([4, 2, 0])}

    ```
    """
    return recursive_apply(data, partial(bt.slice_along_batch, start=start, stop=stop, step=step))


def slice_along_seq(data: Any, start: int = 0, stop: int | None = None, step: int = 1) -> Any:
    r"""Slice all the tensors along the batch dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        start: The index where the slicing of object starts.
        stop: The index where the slicing of object stops.
            ``None`` means last.
        step: The increment between each index for slicing.

    Returns:
        The sliced tensor along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import slice_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> out = slice_along_seq(data, start=2)
    >>> out
    {'a': tensor([[2, 3, 4], [7, 8, 9]]), 'b': tensor([[2, 1, 0]])}
    >>> out = slice_along_seq(data, stop=3)
    >>> out
    {'a': tensor([[0, 1, 2], [5, 6, 7]]), 'b': tensor([[4, 3, 2]])}
    >>> out = slice_along_seq(data, step=2)
    >>> out
    {'a': tensor([[0, 2, 4], [5, 7, 9]]), 'b': tensor([[4, 2, 0]])}

    ```
    """
    return recursive_apply(data, partial(bt.slice_along_seq, start=start, stop=stop, step=step))


def split_along_batch(
    data: dict[Hashable, torch.Tensor], split_size_or_sections: int | Sequence[int]
) -> tuple[dict[Hashable, torch.Tensor], ...]:
    r"""Split all the tensors into chunks along the batch dimension.

    Each chunk is a view of the original tensor.

    Note:
        This function assumes the batch dimension is the first
            dimension of the tensors. All the tensors should have the
            same batch size.

    Args:
        data: The input data. Each item must be a tensor.
        split_size_or_sections: Size of a single chunk or list of
            sizes for each chunk

    Returns:
        The data chuncks.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import split_along_batch
    >>> data = {
    ...     "a": torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": torch.tensor([4, 3, 2, 1, 0]),
    ... }
    >>> outputs = split_along_batch(data, split_size_or_sections=2)
    >>> outputs
    ({'a': tensor([[0, 1], [2, 3]]), 'b': tensor([4, 3])},
     {'a': tensor([[4, 5], [6, 7]]), 'b': tensor([2, 1])},
     {'a': tensor([[8, 9]]), 'b': tensor([0])})

    ```
    """
    keys = data.keys()
    return tuple(
        dict(zip(keys, values))
        for values in zip(
            *[bt.split_along_batch(tensor, split_size_or_sections) for tensor in data.values()]
        )
    )


def split_along_seq(
    data: dict[Hashable, torch.Tensor], split_size_or_sections: int | Sequence[int]
) -> tuple[dict[Hashable, torch.Tensor], ...]:
    r"""Split all the tensors into chunks along the sequence dimension.

    Each chunk is a view of the original tensor.

    Note:
        This function assumes the sequence dimension is the second
            dimension of the tensors. All the tensors should have the
            same sequence size.

    Args:
        data: The input data. Each item must be a tensor.
        split_size_or_sections: Size of a single chunk or list of
            sizes for each chunk

    Returns:
        The data chuncks.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import split_along_seq
    >>> data = {
    ...     "a": torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    ...     "b": torch.tensor([[4, 3, 2, 1, 0]]),
    ... }
    >>> outputs = split_along_seq(data, split_size_or_sections=2)
    >>> outputs
    ({'a': tensor([[0, 1], [5, 6]]), 'b': tensor([[4, 3]])},
     {'a': tensor([[2, 3], [7, 8]]), 'b': tensor([[2, 1]])},
     {'a': tensor([[4], [9]]), 'b': tensor([[0]])})

    ```
    """
    keys = data.keys()
    return tuple(
        dict(zip(keys, values))
        for values in zip(
            *[bt.split_along_seq(tensor, split_size_or_sections) for tensor in data.values()]
        )
    )
