from __future__ import annotations

from typing import Any, List, Literal, Tuple, Type, Union, overload

import numpy as np
import pyarrow as pa

from chalk.features.filter import Filter


class Vector:
    """The Vector class can be used type annotation to denote a Vector feature.

    Instances of this class will be provided when working with raw vectors inside of resolvers.
    Generally, you do not need to construct instances of this class directly, as Chalk will
    automatically convert list-like features into `Vector` instances when working with a `Vector`
    annotation.

    Parameters
    ----------
    data: numpy.Array | list[float] | pyarrow.FixedSizeListScalar
        The vector values

    Examples
    --------
    >>> from chalk.features import Vector, features
    >>> @features
    ... class Document:
    ...     embedding: Vector[1536]
    """

    precision: Literal["fp16", "fp32", "fp64"]
    """The precision of the Vector"""

    num_dimensions: int
    """The number of dimensions in the vector"""

    dtype: pa.DataType
    """The PyArrow data type for the Vector feature. It will be an pa.FixedSizeListType()"""

    def __init__(self, data: Union[pa.FixedSizeListScalar, np.ndarray]):
        super().__init__()
        if not isinstance(data, pa.FixedSizeListScalar):
            if isinstance(data, np.ndarray):
                if data.dtype.name == "float16":
                    dtype = pa.float16()
                elif data.dtype.name == "float32":
                    dtype = pa.float32()
                elif data.dtype.name == "float64":
                    dtype = pa.float64()
                else:
                    raise TypeError(
                        f"Unsupported type '{data.dtype.name}'. Vector features must be float16, float32, or float64."
                    )
                data_converted = pa.scalar(data, pa.list_(dtype, len(data)))
                assert isinstance(data_converted, pa.FixedSizeListScalar)
                data = data_converted
            else:
                raise TypeError(
                    f"When constructing a vector, the value must be a pa.FixedSizeListScalar or a numpy array. Got {data}"
                )
        self._data: pa.FixedSizeListScalar = data
        self.dtype = self._data.type
        value_type = self._data.type.value_type
        self.num_dimensions = self._data.type.list_size
        if value_type == pa.float16():
            self.precision = "fp16"
        elif value_type == pa.float32():
            self.precision = "fp32"
        elif value_type == pa.float64():
            self.precision = "fp64"
        else:
            raise TypeError(f"Value type {value_type} is unsupported. It must be a float16, float32, or float64.")

    def to_arrow_scalar(self) -> pa.FixedSizeListScalar:
        """Convert a vector to a PyArrow array.

        Returns
        -------
        pa.FixedSizeListArray
            The vector, as a PyArrow array.
        """
        return self._data

    def to_arrow_array(self) -> pa.Array:
        """Convert a vector to a PyArrow array.

        Returns
        -------
        pa.FixedSizeListArray
            The vector, as a PyArrow array.
        """
        return self._data.values

    def to_numpy(self, writable: bool = False) -> np.ndarray:
        """Convert the vector to a Numpy array.

        Parameters
        ----------
        writable: bool
            Whether the numpy array should be writable. If so, an extra copy of the vector data will be made.

        Returns
        -------
        np.ndarray
            The vector, as a numpy array.
        """
        return self._data.values.to_numpy(writable=writable)

    def to_pylist(self) -> List[float]:
        """Convert the vector to a Python list.

        Returns
        -------
        List[float]
            The vector, as a list of Python floats
        """
        return self._data.as_py()

    @overload
    def __class_getitem__(cls, item: Tuple[Literal["fp32", "fp64", "fp16"], int], /) -> Type[Vector]:
        """Create a Vector type with the specified precision and number of dimensions.

        Parameters
        ----------
        item: Tuple[Literal["fp32", "fp64", "fp16"], int]
            The first element is the precision, and the second element is the number of dimensions.

        Returns
        -------
        Type[Vector]
            A vector type
        """
        ...

    @overload
    def __class_getitem__(cls, item: int, /) -> Type[Vector]:
        """Create a Vector type of with float-16 precision and the specified number of dimensions.
        This helper is equivalent to `Vector['fp16', N]`.

        Parameters
        ----------
        item: int
            The number of dimensions.

        Returns
        -------
        Type[Vector]
            A vector type
        """
        ...

    def __class_getitem__(cls, item: Union[Tuple[Literal["fp32", "fp64", "fp16"], int], int], /) -> Type[Vector]:
        if isinstance(item, int):
            dimensions = item
            _precision = "fp16"
        elif isinstance(item, tuple) and len(item) == 2:  # pyright: ignore[reportUnnecessaryIsInstance]
            _precision, dimensions = item
        else:
            raise ValueError(
                f"Expected the Vector type argument to be the dimensions (e.g. Vector[1536]) or the dtype and dimensions (e.g. Vector['fp32', 1536]); got {item}"
            )

        if _precision == "fp16":
            _dtype = pa.list_(pa.float16(), dimensions)
        elif _precision == "fp32":
            _dtype = pa.list_(pa.float32(), dimensions)
        elif _precision == "fp64":
            _dtype = pa.list_(pa.float64(), dimensions)
        else:
            raise ValueError(f"Expected the dtype to be one of 'fp16', 'fp32', or 'fp64'; got {_precision}.")
        if not isinstance(dimensions, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Expected the dimensions to be an integer; got {dimensions}.")

        class SubclassedVector(Vector):
            precision = _precision
            num_dimensions = dimensions
            dtype = _dtype

            def __new__(cls, *args: Any, **kwargs: Any):
                return Vector(*args, **kwargs)

        return SubclassedVector

    @classmethod
    def is_near(
        cls,
        other: Any,
        metric: Literal["l2", "ip", "cos"] = "l2",
    ) -> Filter:
        """Define a nearest neighbor relationship for performing Vector similarity search.

        Parameters
        ----------
        other: Type[Vector]
            The other vector feature. This vector must have the same dtype and dimensions.

        metric: "l2" | "ip" | "cos"
            The metric to use to compute distance between two vectors. L2 Norm ("l2"), Inner Product ("ip"),
            and Cosine ("cos") are supported. Defaults to "l2".

        Returns
        -------
        Filter:
            A nearest neighbor relationship filter.
        """
        # This method is never called, since is_near is always called on the FeatureWrapper
        # Defining it here for type checking support
        raise NotImplementedError
