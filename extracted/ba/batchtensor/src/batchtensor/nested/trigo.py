r"""Contain some tensor trigonometric functions for nested data."""

from __future__ import annotations

__all__ = [
    "acos",
    "acosh",
    "asin",
    "asinh",
    "atan",
    "atanh",
    "cos",
    "cosh",
    "sin",
    "sinh",
    "tan",
    "tanh",
]

from typing import Any

import torch

from batchtensor.recursive import recursive_apply


def acos(data: Any) -> Any:
    r"""Return new tensors with the inverse cosine of each element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The inverse cosine of the elements. The output has the same
            structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import acos
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = acos(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.acos)


def acosh(data: Any) -> Any:
    r"""Return new tensors with the inverse hyperbolic cosine of each
    element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The inverse hyperbolic cosine of the elements. The output has
            the same structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import acosh
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = acosh(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.acosh)


def asin(data: Any) -> Any:
    r"""Return new tensors with the arcsine of each element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The arcsine of the elements. The output has the same
            structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import asin
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = asin(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.asin)


def asinh(data: Any) -> Any:
    r"""Return new tensors with the inverse hyperbolic sine of each
    element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The inverse hyperbolic sine of the elements. The output has
            the same structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import asinh
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = asinh(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.asinh)


def atan(data: Any) -> Any:
    r"""Return new tensors with the arctangent of each element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The arctangent of the elements. The output has the same
            structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import atan
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = atan(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.atan)


def atanh(data: Any) -> Any:
    r"""Return new tensors with the inverse hyperbolic tangent of each
    element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The inverse hyperbolic tangent of the elements. The output has
            the same structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import atanh
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = atanh(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.atanh)


def cos(data: Any) -> Any:
    r"""Return new tensors with the cosine of each element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The cosine of the elements. The output has the same
            structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import cos
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = cos(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.cos)


def cosh(data: Any) -> Any:
    r"""Return new tensors with the hyperbolic cosine of each element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The inverse cosine of the elements. The output has
            the same structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import cosh
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = cosh(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.cosh)


def sin(data: Any) -> Any:
    r"""Return new tensors with the sine of each element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The sine of the elements. The output has the same
            structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import sin
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = sin(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.sin)


def sinh(data: Any) -> Any:
    r"""Return new tensors with the hyperbolic sine of each element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The hyperbolic sine of the elements. The output has
            the same structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import sinh
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = sinh(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.sinh)


def tan(data: Any) -> Any:
    r"""Return new tensors with the tangent of each element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The tangent of the elements. The output has the same
            structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import tan
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = tan(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.tan)


def tanh(data: Any) -> Any:
    r"""Return new tensors with the hyperbolic tangent of each element.

    Args:
        data: The input data. Each item must be a tensor.

    Returns:
        The hyperbolic tangent of the elements. The output has
            the same structure as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from batchtensor.nested import tanh
    >>> data = {"a": torch.randn(5, 2), "b": torch.rand(5)}
    >>> out = tanh(data)
    >>> out
    {'a': tensor([[...]]), 'b': tensor([...])}

    ```
    """
    return recursive_apply(data, torch.tanh)
