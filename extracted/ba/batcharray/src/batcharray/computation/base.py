r"""Contain the base class for computation models."""

from __future__ import annotations

__all__ = ["BaseComputationModel"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Sequence

    from numpy.typing import DTypeLike

    from batcharray.types import SortKind

T = TypeVar("T", bound=np.ndarray)


class BaseComputationModel(ABC, Generic[T]):
    r"""Define the base class for computation models.

    This class provides the interface that all computation models must
    implement. It can be extended to create custom computation models
    for different array types.
    """

    @abstractmethod
    def argmax(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        r"""Return the array of indices of the maximum values along the
        given axis.

        Args:
            arr: The input array.
            axis: Axis along which the argmax are computed.
                The default (``None``) is to compute the argmax along
                a flattened version of the array.
            keepdims: If this is set to True, the axes which are
                reduced are left in the result as dimensions with size
                one. With this option, the result will broadcast
                correctly against the input array.

        Returns:
            The array of indices of the maximum values along the given
                axis.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import ArrayComputationModel
            >>> comp_model = ArrayComputationModel()
            >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
            >>> out = comp_model.argmax(array, axis=0)
            >>> out
            array([4, 4])
            >>> out = comp_model.argmax(array, axis=1)
            >>> out
            array([1, 1, 1, 1, 1])
            >>> out = comp_model.argmax(array, axis=0, keepdims=True)
            >>> out
            array([[4, 4]])

            ```
        """

    @abstractmethod
    def argmin(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        r"""Return the array of indices of the minimum values along the
        given axis.

        Args:
            arr: The input array.
            axis: Axis along which the argmin are computed.
                The default (``None``) is to compute the argmin along
                a flattened version of the array.
            keepdims: If this is set to True, the axes which are
                reduced are left in the result as dimensions with size
                one. With this option, the result will broadcast
                correctly against the input array.

        Returns:
            The array of indices of the minimum values along the given
                axis.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import ArrayComputationModel
            >>> comp_model = ArrayComputationModel()
            >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
            >>> out = comp_model.argmin(array, axis=0)
            >>> out
            array([0, 0])
            >>> out = comp_model.argmin(array, axis=1)
            >>> out
            array([0, 0, 0, 0, 0])
            >>> out = comp_model.argmin(array, axis=0, keepdims=True)
            >>> out
            array([[0, 0]])

            ```
        """

    @abstractmethod
    def argsort(self, arr: T, axis: int | None = None, *, kind: SortKind | None = None) -> T:
        r"""Return the indices that sort an array along the given axis in
        ascending order by value.

        Args:
            arr: The input array.
            axis: Axis along which to sort. The default (``None``) is
                to sort along a flattened version of the array.
            kind: Sorting algorithm. The default is `quicksort`.
                Note that both `stable` and `mergesort` use timsort
                under the covers and, in general, the actual
                implementation will vary with datatype.
                The `mergesort` option is retained for backwards
                compatibility.

        Returns:
            The indices that sort the array along the given axis.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import ArrayComputationModel
            >>> comp_model = ArrayComputationModel()
            >>> array = np.array([[3, 5, 0, 2, 4], [4, 7, 8, 9, 5], [7, 5, 8, 9, 0]])
            >>> out = comp_model.argsort(array, axis=0)
            >>> out
            array([[0, 0, 0, 0, 2],
                   [1, 2, 1, 1, 0],
                   [2, 1, 2, 2, 1]])
            >>> out = comp_model.argsort(array, axis=1)
            >>> out
            array([[2, 3, 0, 4, 1],
                   [0, 4, 1, 2, 3],
                   [4, 1, 0, 2, 3]])

            ```
        """

    @abstractmethod
    def concatenate(
        self, arrays: Sequence[T], axis: int | None = None, *, dtype: DTypeLike = None
    ) -> T:
        r"""Concatenate a sequence of arrays along an existing axis.

        Args:
            arrays: The arrays to concatenate.
            axis: The axis along which the arrays will be joined.
                If ``axis`` is None, arrays are flattened before use.
            dtype: If provided, the destination array will have this
                data type.

        Returns:
            The concatenated array.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import ArrayComputationModel
            >>> comp_model = ArrayComputationModel()
            >>> arrays = [
            ...     np.array([[0, 1, 2], [4, 5, 6]]),
            ...     np.array([[10, 11, 12], [13, 14, 15]]),
            ... ]
            >>> out = comp_model.concatenate(arrays, axis=0)
            >>> out
            array([[ 0,  1,  2],
                   [ 4,  5,  6],
                   [10, 11, 12],
                   [13, 14, 15]])
            >>> out = comp_model.concatenate(arrays, axis=1)
            >>> out
            array([[ 0,  1,  2, 10, 11, 12],
                   [ 4,  5,  6, 13, 14, 15]])

            ```
        """

    @abstractmethod
    def max(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        r"""Return the maximum along the specified axis.

        Args:
            arr: The input array.
            axis: Axis along which the maximum values are computed.
                The default (``None``) is to compute the maximum along
                a flattened version of the array.
            keepdims: If this is set to True, the axes which are
                reduced are left in the result as dimensions with size
                one. With this option, the result will broadcast
                correctly against the input array.

        Returns:
            The maximum of the input array along the given axis.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import ArrayComputationModel
            >>> comp_model = ArrayComputationModel()
            >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
            >>> out = comp_model.max(array, axis=0)
            >>> out
            array([8, 9])
            >>> out = comp_model.max(array, axis=1)
            >>> out
            array([1, 3, 5, 7, 9])
            >>> out = comp_model.max(array, axis=0, keepdims=True)
            >>> out
            array([[8, 9]])

            ```
        """

    @abstractmethod
    def mean(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        r"""Return the mean along the specified axis.

        Args:
            arr: The input array.
            axis: Axis along which the means are computed.
                The default (``None``) is to compute the mean along
                a flattened version of the array.
            keepdims: If this is set to True, the axes which are
                reduced are left in the result as dimensions with size
                one. With this option, the result will broadcast
                correctly against the input array.

        Returns:
            A new array holding the result. If the input contains integers
                or floats smaller than ``np.float64``, then the output
                data-type is ``np.float64``. Otherwise, the data-type of
                the output is the same as that of the input.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import ArrayComputationModel
            >>> comp_model = ArrayComputationModel()
            >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
            >>> out = comp_model.mean(array, axis=0)
            >>> out
            array([4., 5.])
            >>> out = comp_model.mean(array, axis=1)
            >>> out
            array([0.5, 2.5, 4.5, 6.5, 8.5])
            >>> out = comp_model.mean(array, axis=0, keepdims=True)
            >>> out
            array([[4., 5.]])

            ```
        """

    @abstractmethod
    def median(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        r"""Return the median along the specified axis.

        Args:
            arr: The input array.
            axis: Axis along which the medians are computed.
                The default (``None``) is to compute the median along
                a flattened version of the array.
            keepdims: If this is set to True, the axes which are
                reduced are left in the result as dimensions with size
                one. With this option, the result will broadcast
                correctly against the input array.

        Returns:
            A new array holding the result. If the input contains integers
                or floats smaller than ``np.float64``, then the output
                data-type is ``np.float64``. Otherwise, the data-type of
                the output is the same as that of the input.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import ArrayComputationModel
            >>> comp_model = ArrayComputationModel()
            >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
            >>> out = comp_model.median(array, axis=0)
            >>> out
            array([4., 5.])
            >>> out = comp_model.median(array, axis=1)
            >>> out
            array([0.5, 2.5, 4.5, 6.5, 8.5])
            >>> out = comp_model.median(array, axis=0, keepdims=True)
            >>> out
            array([[4., 5.]])

            ```
        """

    @abstractmethod
    def min(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        r"""Return the minimum along the specified axis.

        Args:
            arr: The input array.
            axis: Axis along which the minimum values are computed.
                The default (``None``) is to compute the minimum along
                a flattened version of the array.
            keepdims: If this is set to True, the axes which are
                reduced are left in the result as dimensions with size
                one. With this option, the result will broadcast
                correctly against the input array.

        Returns:
            The minimum of the input array along the given axis.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import ArrayComputationModel
            >>> comp_model = ArrayComputationModel()
            >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
            >>> out = comp_model.min(array, axis=0)
            >>> out
            array([0, 1])
            >>> out = comp_model.min(array, axis=1)
            >>> out
            array([0, 2, 4, 6, 8])
            >>> out = comp_model.min(array, axis=0, keepdims=True)
            >>> out
            array([[0, 1]])

            ```
        """

    @abstractmethod
    def sort(self, arr: T, axis: int | None = None, *, kind: SortKind | None = None) -> T:
        r"""Sort the elements of the input array along the given axis in
        ascending order by value.

        Args:
            arr: The input array.
            axis: Axis along which to sort. The default (``None``) is
                to sort along a flattened version of the array.
            kind: Sorting algorithm. The default is `quicksort`.
                Note that both `stable` and `mergesort` use timsort
                under the covers and, in general, the actual
                implementation will vary with datatype.
                The `mergesort` option is retained for backwards
                compatibility.

        Returns:
            The sorted array along the given axis.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import ArrayComputationModel
            >>> comp_model = ArrayComputationModel()
            >>> array = np.array([[3, 5, 0, 2, 4], [4, 7, 8, 8, 5], [8, 5, 8, 8, 0]])
            >>> out = comp_model.sort(array, axis=0)
            >>> out
            array([[3, 5, 0, 2, 0],
                   [4, 5, 8, 8, 4],
                   [8, 7, 8, 8, 5]])
            >>> out = comp_model.sort(array, axis=1)
            >>> out
            array([[0, 2, 3, 4, 5],
                   [4, 5, 7, 8, 8],
                   [0, 5, 8, 8, 8]])

            ```
        """
