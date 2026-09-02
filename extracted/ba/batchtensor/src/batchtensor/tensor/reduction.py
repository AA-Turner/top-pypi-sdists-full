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


import torch

from batchtensor.constants import BATCH_DIM, SEQ_DIM


def amax_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the maximum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The maximum of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import amax_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = amax_along_batch(tensor)
    >>> out
    tensor([8, 9])
    >>> out = amax_along_batch(tensor, keepdim=True)
    >>> out
    tensor([[8, 9]])

    ```
    """
    return torch.amax(tensor, dim=BATCH_DIM, keepdim=keepdim)


def amax_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the maximum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The maximum of all elements along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import amax_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = amax_along_seq(tensor)
    >>> out
    tensor([4, 9])
    >>> out = amax_along_seq(tensor, keepdim=True)
    >>> out
    tensor([[4], [9]])

    ```
    """
    return torch.amax(tensor, dim=SEQ_DIM, keepdim=keepdim)


def amin_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the minimum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The minimum of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import amin_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = amin_along_batch(tensor)
    >>> out
    tensor([0, 1])
    >>> out = amin_along_batch(tensor, keepdim=True)
    >>> out
    tensor([[0, 1]])

    ```
    """
    return torch.amin(tensor, dim=BATCH_DIM, keepdim=keepdim)


def amin_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the minimum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The minimum of all elements along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import amin_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = amin_along_seq(tensor)
    >>> out
    tensor([0, 5])
    >>> out = amin_along_seq(tensor, keepdim=True)
    >>> out
    tensor([[0], [5]])

    ```
    """
    return torch.amin(tensor, dim=SEQ_DIM, keepdim=keepdim)


def argmax_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the indices of the maximum value of all elements along the
    batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The indices of the maximum value of all elements along the
            batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import argmax_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = argmax_along_batch(tensor)
    >>> out
    tensor([4, 4])
    >>> out = argmax_along_batch(tensor, keepdim=True)
    >>> out
    tensor([[4, 4]])

    ```
    """
    return torch.argmax(tensor, dim=BATCH_DIM, keepdim=keepdim)


def argmax_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the indices of the maximum value of all elements along the
    sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The indices of the maximum value of all elements along the
            sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import argmax_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = argmax_along_seq(tensor)
    >>> out
    tensor([4, 4])
    >>> out = argmax_along_seq(tensor, keepdim=True)
    >>> out
    tensor([[4], [4]])

    ```
    """
    return torch.argmax(tensor, dim=SEQ_DIM, keepdim=keepdim)


def argmin_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the indices of the minimum value of all elements along the
    batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The indices of the minimum value of all elements along the
            batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import argmin_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = argmin_along_batch(tensor)
    >>> out
    tensor([0, 0])
    >>> out = argmin_along_batch(tensor, keepdim=True)
    >>> out
    tensor([[0, 0]])

    ```
    """
    return torch.argmin(tensor, dim=BATCH_DIM, keepdim=keepdim)


def argmin_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the indices of the minimum value of all elements along the
    sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The indices of the minimum value of all elements along the
            sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import argmin_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = argmin_along_seq(tensor)
    >>> out
    tensor([0, 0])
    >>> out = argmin_along_seq(tensor, keepdim=True)
    >>> out
    tensor([[0], [0]])

    ```
    """
    return torch.argmin(tensor, dim=SEQ_DIM, keepdim=keepdim)


def max_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.return_types.max:
    r"""Return the maximum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the maximum values and
            the second tensor, which must have dtype long, with their
            indices in the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import max_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = max_along_batch(tensor)
    >>> out
    torch.return_types.max(
    values=tensor([8, 9]),
    indices=tensor([4, 4]))
    >>> out = max_along_batch(tensor, keepdim=True)
    >>> out
    torch.return_types.max(
    values=tensor([[8, 9]]),
    indices=tensor([[4, 4]]))

    ```
    """
    return torch.max(tensor, dim=BATCH_DIM, keepdim=keepdim)


def max_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.return_types.max:
    r"""Return the maximum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the maximum values and
            the second tensor, which must have dtype long, with their
            indices in the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import max_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = max_along_seq(tensor)
    >>> out
    torch.return_types.max(
    values=tensor([4, 9]),
    indices=tensor([4, 4]))
    >>> out = max_along_seq(tensor, keepdim=True)
    >>> out
    torch.return_types.max(
    values=tensor([[4], [9]]),
    indices=tensor([[4], [4]]))

    ```
    """
    return torch.max(tensor, dim=SEQ_DIM, keepdim=keepdim)


def mean_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the mean of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The mean of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import mean_along_batch
    >>> tensor = torch.tensor([[0.0, 1.0], [2.0, 3.0], [4.0, 5.0], [6.0, 7.0], [8.0, 9.0]])
    >>> out = mean_along_batch(tensor)
    >>> out
    tensor([4., 5.])
    >>> out = mean_along_batch(tensor, keepdim=True)
    >>> out
    tensor([[4., 5.]])

    ```
    """
    return torch.mean(tensor, dim=BATCH_DIM, keepdim=keepdim)


def mean_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the mean of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The mean of all elements along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import mean_along_seq
    >>> tensor = torch.tensor([[0.0, 1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0, 9.0]])
    >>> out = mean_along_seq(tensor)
    >>> out
    tensor([2., 7.])
    >>> out = mean_along_seq(tensor, keepdim=True)
    >>> out
    tensor([[2.], [7.]])

    ```
    """
    return torch.mean(tensor, dim=SEQ_DIM, keepdim=keepdim)


def median_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.return_types.median:
    r"""Return the median of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the median values and
            the second tensor, which must have dtype long, with their
            indices in the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import median_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = median_along_batch(tensor)
    >>> out
    torch.return_types.median(
    values=tensor([4, 5]),
    indices=tensor([2, 2]))
    >>> out = median_along_batch(tensor, keepdim=True)
    >>> out
    torch.return_types.median(
    values=tensor([[4, 5]]),
    indices=tensor([[2, 2]]))

    ```
    """
    return torch.median(tensor, dim=BATCH_DIM, keepdim=keepdim)


def median_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.return_types.median:
    r"""Return the median of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the median values and
            the second tensor, which must have dtype long, with their
            indices in the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import median_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = median_along_seq(tensor)
    >>> out
    torch.return_types.median(
    values=tensor([2, 7]),
    indices=tensor([2, 2]))
    >>> out = median_along_seq(tensor, keepdim=True)
    >>> out
    torch.return_types.median(
    values=tensor([[2], [7]]),
    indices=tensor([[2], [2]]))

    ```
    """
    return torch.median(tensor, dim=SEQ_DIM, keepdim=keepdim)


def min_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.return_types.min:
    r"""Return the minimum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the minimum values and
            the second tensor, which must have dtype long, with their
            indices in the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import min_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = min_along_batch(tensor)
    >>> out
    torch.return_types.min(
    values=tensor([0, 1]),
    indices=tensor([0, 0]))
    >>> out = min_along_batch(tensor, keepdim=True)
    >>> out
    torch.return_types.min(
    values=tensor([[0, 1]]),
    indices=tensor([[0, 0]]))

    ```
    """
    return torch.min(tensor, dim=BATCH_DIM, keepdim=keepdim)


def min_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.return_types.min:
    r"""Return the minimum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The first tensor will be populated with the minimum values and
            the second tensor, which must have dtype long, with their
            indices in the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import min_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = min_along_seq(tensor)
    >>> out
    torch.return_types.min(
    values=tensor([0, 5]),
    indices=tensor([0, 0]))
    >>> out = min_along_seq(tensor, keepdim=True)
    >>> out
    torch.return_types.min(
    values=tensor([[0], [5]]),
    indices=tensor([[0], [0]]))

    ```
    """
    return torch.min(tensor, dim=SEQ_DIM, keepdim=keepdim)


def prod_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the product of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The product of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import prod_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = prod_along_batch(tensor)
    >>> out
    tensor([  0, 945])
    >>> out = prod_along_batch(tensor, keepdim=True)
    >>> out
    tensor([[  0, 945]])

    ```
    """
    return torch.prod(tensor, dim=BATCH_DIM, keepdim=keepdim)


def prod_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the product of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The product of all elements along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import prod_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = prod_along_seq(tensor)
    >>> out
    tensor([    0, 15120])
    >>> out = prod_along_seq(tensor, keepdim=True)
    >>> out
    tensor([[    0], [15120]])

    ```
    """
    return torch.prod(tensor, dim=SEQ_DIM, keepdim=keepdim)


def sum_along_batch(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the sum of all elements along the batch dimension.

    Note:
        This function assumes the batch dimension is the first
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The sum of all elements along the batch dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import sum_along_batch
    >>> tensor = torch.tensor([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = sum_along_batch(tensor)
    >>> out
    tensor([20, 25])
    >>> out = sum_along_batch(tensor, keepdim=True)
    >>> out
    tensor([[20, 25]])

    ```
    """
    return torch.sum(tensor, dim=BATCH_DIM, keepdim=keepdim)


def sum_along_seq(tensor: torch.Tensor, keepdim: bool = False) -> torch.Tensor:
    r"""Return the sum of all elements along the sequence dimension.

    Note:
        This function assumes the sequence dimension is the second
            dimension.

    Args:
        tensor: The input tensor.
        keepdim: Whether the output tensor has dim retained or not.

    Returns:
        The sum of all elements along the sequence dimension.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.tensor import sum_along_seq
    >>> tensor = torch.tensor([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = sum_along_seq(tensor)
    >>> out
    tensor([10, 35])
    >>> out = sum_along_seq(tensor, keepdim=True)
    >>> out
    tensor([[10], [35]])

    ```
    """
    return torch.sum(tensor, dim=SEQ_DIM, keepdim=keepdim)
