from __future__ import annotations

from enum import Enum
from typing import Any, Tuple, Type, TypeGuard, Union, overload

import numpy as np
import pyarrow as pa

TensorDimension = Union[int, str]


def is_tensor_dimension(dim: Any) -> TypeGuard[TensorDimension]:
    return isinstance(dim, (int, str))


class TensorLayout(str, Enum):
    DENSE = "dense"


class Tensor:
    """The Tensor class can be used as a type annotation to denote a Tensor feature.

    Tensors are useful for representing multidimensional arrays, such as images or other high-dimensional data.
    Certain operations in Chalk, such as inference with machine learning models, may require tensor inputs and output
    tensors.
    """

    shape: Tuple[TensorDimension, ...]
    """The dimensions of the Tensor. Each dimension can be an integer (fixed size) or a string (variable size)."""

    dtype: pa.DataType
    """The base type of the Tensor, should be floating point or integer."""

    layout: TensorLayout
    """The memory layout of the Tensor. Currently, only "dense" layout is supported."""

    def __init__(self, data: Union[pa.Tensor, np.ndarray]):
        super().__init__()
        if not isinstance(data, pa.Tensor):
            if isinstance(data, np.ndarray):
                if data.dtype.name in ["float16", "float32", "float64", "int8", "int16", "int32", "int64"]:
                    data = pa.Tensor.from_numpy(data)
                else:
                    raise TypeError(
                        f"Unsupported type '{data.dtype.name}'. Tensor features must be floating point or integer types."
                    )
            else:
                raise TypeError(
                    f"When constructing a tensor, the value must be a pa.Tensor or a numpy array. Got {data}"
                )
        self._data: pa.Tensor = data
        self.shape = tuple(self._data.shape)
        self.dtype = self._data.type
        self.layout = TensorLayout.DENSE

    def to_arrow_tensor(self) -> pa.Tensor:
        """Convert the Tensor to a PyArrow Tensor.

        Returns
        -------
        pa.Tensor
            The PyArrow Tensor representation of this Tensor.
        """
        return self._data

    def to_numpy(self) -> np.ndarray:
        """Convert the Tensor to a NumPy array.

        Returns
        -------
        np.ndarray
            The NumPy array representation of this Tensor.
        """
        return self._data.to_numpy()

    @overload
    def __class_getitem__(cls, item: TensorDimension, /) -> Type[Tensor]:
        """
        Get a 1-dimensional tensor with the specified shape, with float-16 precision and dense layout by default.

        Parameters
        ----------
        item: int | str
            The singular dimension of the Tensor.
            Should be an integer (fixed size) or a string (variable size).

        Returns
        -------
        Type[Tensor]
            A tensor type
        """
        ...

    @overload
    def __class_getitem__(cls, item: Tuple[TensorDimension | pa.DataType | TensorLayout, ...], /) -> Type[Tensor]:
        """
        Get a Tensor type with the specified shape, precision, and layout.

        Parameters
        ----------
        item: Tuple[int | str | pa.DataType | TensorLayout, ...]
            A tuple specifying the dimensions of the Tensor, followed optionally by the data type and layout.
            Each dimension can be an integer (fixed size) or a string (variable size).
            The data type can be one of pa.float16(), pa.float32(), pa.float64(), pa.int8(), pa.int16(), pa.int32(), or pa.int64().
            The layout can be TensorLayout.DENSE.

            The data type and layout are optional.
            If not provided, the data type defaults to pa.float16() and the layout defaults to TensorLayout.DENSE.

            The data type and layout, if provided, must be the last one or two elements of the tuple, in that order.

        Returns
        -------
        Type[Tensor]
            A tensor type

        Examples
        --------
        >>> from chalk.features import Tensor, TensorLayout, features
        >>> import pyarrow as pa
        >>> @features
        ... class MyFeatures:
        ...     image: Tensor[3, 224, 224, pa.float32(), TensorLayout.DENSE]
        ...     variable_length_tensor: Tensor["var_length", 128, pa.float64()]

        """
        ...

    def __class_getitem__(
        cls, item: Union[Tuple[TensorDimension | pa.DataType | TensorLayout, ...], TensorDimension], /
    ) -> Type[Tensor]:
        if is_tensor_dimension(item):
            item = (item,)
        if not isinstance(item, tuple):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("Tensor[...] must be indexed with a dimension or a tuple of dimensions.")
        if len(item) < 1:
            raise ValueError("Tensor[...] must have at least one dimension specified.")
        *shape, last = item
        _dtype: pa.DataType = pa.float16()
        _layout: TensorLayout = TensorLayout.DENSE

        if isinstance(last, TensorLayout):
            _layout = last
            if len(shape) == 0:
                raise ValueError("Tensor[...] must have at least one dimension specified.")
            *shape, last = shape

        if isinstance(last, pa.DataType):
            if last not in [pa.float16(), pa.float32(), pa.float64(), pa.int8(), pa.int16(), pa.int32(), pa.int64()]:
                raise ValueError(
                    f"Unsupported data type '{last}'. Tensor features must be floating point or integer types."
                )
            _dtype = last
            if len(shape) == 0:
                raise ValueError("Tensor[...] must have at least one dimension specified.")
            *shape, last = shape

        _shape = (*shape, last)
        for dim in _shape:
            if not is_tensor_dimension(dim):
                raise TypeError(
                    f"All dimensions in Tensor[...] must be integers or strings, except for the optional data type and layout at the end. Found {dim} of type {type(dim)}."
                )
            if isinstance(dim, int) and dim <= 0:
                raise ValueError(
                    "All integer dimensions in Tensor[...] must be positive. If you are trying to create a variadic dimension, use a string instead."
                )

        class SubclassedTensor(Tensor):
            shape = _shape
            dtype = _dtype
            layout = _layout

            def __new__(cls, *args: Any, **kwargs: Any):
                return Tensor(*args, **kwargs)

        return SubclassedTensor

    @classmethod
    def to_pyarrow_dtype(cls) -> pa.DataType:
        dtype = cls.dtype
        for dim in reversed(cls.shape):
            if isinstance(dim, int):
                # Intentionally not fixed size-- it is non-trivial to promote from a fixed size list
                # to a variable size list.
                dtype = pa.list_(dtype)
            else:
                # Variadic, cannot use fixed size list here
                dtype = pa.list_(dtype)
        return dtype
