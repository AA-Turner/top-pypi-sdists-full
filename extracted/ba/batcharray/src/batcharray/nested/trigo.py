r"""Contain some array trigonometric functions for nested data."""

from __future__ import annotations

__all__ = [
    "arccos",
    "arccosh",
    "arcsin",
    "arcsinh",
    "arctan",
    "arctanh",
    "cos",
    "cosh",
    "sin",
    "sinh",
    "tan",
    "tanh",
]

from typing import Any

import numpy as np
from coola.recursive import recursive_apply


def arccos(data: Any) -> Any:
    r"""Return new arrays with the inverse cosine of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The inverse cosine of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import arccos
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = arccos(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.arccos)


def arccosh(data: Any) -> Any:
    r"""Return new arrays with the inverse hyperbolic cosine of each
    element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The inverse hyperbolic cosine of the elements. The output has
            the same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import arccosh
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = arccosh(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.arccosh)


def arcsin(data: Any) -> Any:
    r"""Return new arrays with the arcsine of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The arcsine of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import arcsin
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = arcsin(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.arcsin)


def arcsinh(data: Any) -> Any:
    r"""Return new arrays with the inverse hyperbolic sine of each
    element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The inverse hyperbolic sine of the elements. The output has
            the same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import arcsinh
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = arcsinh(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.arcsinh)


def arctan(data: Any) -> Any:
    r"""Return new arrays with the arctangent of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The arctangent of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import arctan
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = arctan(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.arctan)


def arctanh(data: Any) -> Any:
    r"""Return new arrays with the inverse hyperbolic tangent of each
    element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The inverse hyperbolic tangent of the elements. The output has
            the same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import arctanh
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = arctanh(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.arctanh)


def cos(data: Any) -> Any:
    r"""Return new arrays with the cosine of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The cosine of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import cos
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = cos(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.cos)


def cosh(data: Any) -> Any:
    r"""Return new arrays with the hyperbolic cosine of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The hyperbolic cosine of the elements. The output has
            the same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import cosh
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = cosh(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.cosh)


def sin(data: Any) -> Any:
    r"""Return new arrays with the sine of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The sine of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import sin
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = sin(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.sin)


def sinh(data: Any) -> Any:
    r"""Return new arrays with the hyperbolic sine of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The hyperbolic sine of the elements. The output has
            the same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import sinh
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = sinh(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.sinh)


def tan(data: Any) -> Any:
    r"""Return new arrays with the tangent of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The tangent of the elements. The output has the same
            structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import tan
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = tan(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.tan)


def tanh(data: Any) -> Any:
    r"""Return new arrays with the hyperbolic tangent of each element.

    Args:
        data: The input data. Each item must be an array .

    Returns:
        The hyperbolic tangent of the elements. The output has
            the same structure as the input.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.nested import tanh
        >>> data = {"a": np.ones((2, 3)), "b": np.arange(5)}
        >>> out = tanh(data)
        >>> out
        {'a': array([[...]]), 'b': array([...])}

        ```
    """
    return recursive_apply(data, np.tanh)
