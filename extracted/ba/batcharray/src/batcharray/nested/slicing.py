r"""Contain some array slicing functions for nested data."""

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

from coola.recursive import recursive_apply

from batcharray import array as ba

if TYPE_CHECKING:
    from collections.abc import Hashable, Sequence

    import numpy as np


def chunk_along_batch(
    data: dict[Hashable, np.ndarray], chunks: int
) -> list[dict[Hashable, np.ndarray]]:
    r"""Split all the arrays into chunks along the batch axis.

    Each chunk is a view of the input array.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array.
        chunks: Number of chunks to return.

    Returns:
        The data chuncks.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import chunk_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> outputs = chunk_along_batch(data, chunks=3)
        >>> outputs
        [{'a': array([[0, 1], [2, 3]]), 'b': array([4, 3])},
         {'a': array([[4, 5], [6, 7]]), 'b': array([2, 1])},
         {'a': array([[8, 9]]), 'b': array([0])}]

        ```
    """
    keys = data.keys()
    return [
        dict(zip(keys, values))
        for values in zip(*[ba.chunk_along_batch(array, chunks) for array in data.values()])
    ]


def chunk_along_seq(
    data: dict[Hashable, np.ndarray], chunks: int
) -> list[dict[Hashable, np.ndarray]]:
    r"""Split all the arrays into chunks along the sequence axis.

    Each chunk is a view of the input array.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.
        chunks: Number of chunks to return.

    Returns:
        The data chunks.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import chunk_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> outputs = chunk_along_seq(data, chunks=3)
        >>> outputs
        [{'a': array([[0, 1], [5, 6]]), 'b': array([[4, 3]])},
         {'a': array([[2, 3], [7, 8]]), 'b': array([[2, 1]])},
         {'a': array([[4], [9]]), 'b': array([[0]])}]

        ```
    """
    keys = data.keys()
    return [
        dict(zip(keys, values))
        for values in zip(*[ba.chunk_along_seq(array, chunks) for array in data.values()])
    ]


def select_along_batch(data: Any, index: int) -> Any:
    r"""Slice the arrays along the batch axis at the given index.

    This function returns a view of the original array with the batch
    axis removed.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array.
        index: The index to select with.

    Returns:
        The sliced arrays along the batch axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import select_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = select_along_batch(data, index=2)
        >>> out
        {'a': array([4, 5]), 'b': np.int64(2)}

        ```
    """
    return recursive_apply(data, partial(ba.select_along_batch, index=index))


def select_along_seq(data: Any, index: int) -> Any:
    r"""Slice the arrays along the sequence axis at the given index.

    This function returns a view of the original array with the
    sequence axis removed.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.
        index: The index to select with.

    Returns:
        The sliced arrays along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import select_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = select_along_seq(data, index=2)
        >>> out
        {'a': array([2, 7]), 'b': array([2])}

        ```
    """
    return recursive_apply(data, partial(ba.select_along_seq, index=index))


def slice_along_batch(data: Any, start: int = 0, stop: int | None = None, step: int = 1) -> Any:
    r"""Slice all the arrays along the batch axis.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array.
        start: The index where the slicing of object starts.
        stop: The index where the slicing of object stops.
            ``None`` means last.
        step: The increment between each index for slicing.

    Returns:
        The sliced arrays along the batch axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import slice_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> out = slice_along_batch(data, start=2)
        >>> out
        {'a': array([[4, 5], [6, 7], [8, 9]]), 'b': array([2, 1, 0])}
        >>> out = slice_along_batch(data, stop=3)
        >>> out
        {'a': array([[0, 1], [2, 3], [4, 5]]), 'b': array([4, 3, 2])}
        >>> out = slice_along_batch(data, step=2)
        >>> out
        {'a': array([[0, 1], [4, 5], [8, 9]]), 'b': array([4, 2, 0])}

        ```
    """
    return recursive_apply(data, partial(ba.slice_along_batch, start=start, stop=stop, step=step))


def slice_along_seq(data: Any, start: int = 0, stop: int | None = None, step: int = 1) -> Any:
    r"""Slice all the arrays along the sequence axis.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.
        start: The index where the slicing of object starts.
        stop: The index where the slicing of object stops.
            ``None`` means last.
        step: The increment between each index for slicing.

    Returns:
        The sliced arrays along the sequence axis.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import slice_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> out = slice_along_seq(data, start=2)
        >>> out
        {'a': array([[2, 3, 4], [7, 8, 9]]), 'b': array([[2, 1, 0]])}
        >>> out = slice_along_seq(data, stop=3)
        >>> out
        {'a': array([[0, 1, 2], [5, 6, 7]]), 'b': array([[4, 3, 2]])}
        >>> out = slice_along_seq(data, step=2)
        >>> out
        {'a': array([[0, 2, 4], [5, 7, 9]]), 'b': array([[4, 2, 0]])}

        ```
    """
    return recursive_apply(data, partial(ba.slice_along_seq, start=start, stop=stop, step=step))


def split_along_batch(
    data: dict[Hashable, np.ndarray], split_size_or_sections: int | Sequence[int]
) -> list[dict[Hashable, np.ndarray]]:
    r"""Split all the arrays into chunks along the batch axis.

    Each chunk is a view of the original array.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array.
        split_size_or_sections: Size of a single chunk or list of
            sizes for each chunk

    Returns:
        The data chunks.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import split_along_batch
        >>> data = {
        ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
        ...     "b": np.array([4, 3, 2, 1, 0]),
        ... }
        >>> outputs = split_along_batch(data, split_size_or_sections=2)
        >>> outputs
        [{'a': array([[0, 1], [2, 3]]), 'b': array([4, 3])},
         {'a': array([[4, 5], [6, 7]]), 'b': array([2, 1])},
         {'a': array([[8, 9]]), 'b': array([0])}]

        ```
    """
    keys = data.keys()
    return [
        dict(zip(keys, values))
        for values in zip(
            *[ba.split_along_batch(array, split_size_or_sections) for array in data.values()]
        )
    ]


def split_along_seq(
    data: dict[Hashable, np.ndarray], split_size_or_sections: int | Sequence[int]
) -> list[dict[Hashable, np.ndarray]]:
    r"""Split all the arrays into chunks along the sequence axis.

    Each chunk is a view of the original array.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.
        split_size_or_sections: Size of a single chunk or list of
            sizes for each chunk

    Returns:
        The data chunks.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import split_along_seq
        >>> data = {
        ...     "a": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        ...     "b": np.array([[4, 3, 2, 1, 0]]),
        ... }
        >>> outputs = split_along_seq(data, split_size_or_sections=2)
        >>> outputs
        [{'a': array([[0, 1], [5, 6]]), 'b': array([[4, 3]])},
         {'a': array([[2, 3], [7, 8]]), 'b': array([[2, 1]])},
         {'a': array([[4], [9]]), 'b': array([[0]])}]

        ```
    """
    keys = data.keys()
    return [
        dict(zip(keys, values))
        for values in zip(
            *[ba.split_along_seq(array, split_size_or_sections) for array in data.values()]
        )
    ]
