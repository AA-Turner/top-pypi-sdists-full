r"""Contain a computation model that automatically finds the right
computation model based on the array type."""

from __future__ import annotations

__all__ = ["AutoComputationModel", "register_computation_models"]

from typing import TYPE_CHECKING, ClassVar, TypeVar

import numpy as np
from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping

from batcharray.computation.base import BaseComputationModel

if TYPE_CHECKING:
    from collections.abc import Sequence

    from numpy.typing import DTypeLike

    from batcharray.types import SortKind

T = TypeVar("T", bound=np.ndarray)


class AutoComputationModel(BaseComputationModel[T]):
    r"""Implement a computation model that automatically finds the right
    computation model based on the array type.

    Example:
        ```pycon
        >>> import numpy as np
        >>> from batcharray.computation import AutoComputationModel
        >>> comp_model = AutoComputationModel()
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

        ```
    """

    registry: ClassVar[dict[type, BaseComputationModel[T]]] = {}

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {repr_indent(repr_mapping(self.registry))}\n)"

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(\n  {str_indent(str_mapping(self.registry))}\n)"

    @classmethod
    def add_computation_model(
        cls,
        array_type: type[np.ndarray],
        comp_model: BaseComputationModel[T],
        exist_ok: bool = False,
    ) -> None:
        r"""Add a computation model for a given array type.

        Args:
            array_type: The array type.
            comp_model: The computation model to use for the given array
                type.
            exist_ok: If ``False``, ``RuntimeError`` is raised if the
                data type already exists. This parameter should be set
                to ``True`` to overwrite the computation model for an array
                type.

        Raises:
            RuntimeError: if a computation model is already registered for
                the array type and ``exist_ok=False``.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import AutoComputationModel, ArrayComputationModel
            >>> AutoComputationModel.add_computation_model(
            ...     np.ndarray, ArrayComputationModel(), exist_ok=True
            ... )

            ```
        """
        if array_type in cls.registry and not exist_ok:
            msg = (
                f"A computation model {cls.registry[array_type]} is already registered for the "
                f"array type {array_type}. Please use `exist_ok=True` if you want to overwrite "
                "the computation model for this array type"
            )
            raise RuntimeError(msg)
        cls.registry[array_type] = comp_model

    @classmethod
    def has_computation_model(cls, array_type: type[np.ndarray]) -> bool:
        r"""Indicate if a computation model is registered for the given
        array type.

        Args:
            array_type: The array type.

        Returns:
            ``True`` if a computation model is registered,
                otherwise ``False``.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import AutoComputationModel
            >>> AutoComputationModel.has_computation_model(np.ndarray)
            True
            >>> AutoComputationModel.has_computation_model(str)
            False

            ```
        """
        return array_type in cls.registry

    @classmethod
    def find_computation_model(cls, array_type: type[np.ndarray]) -> BaseComputationModel[T]:
        r"""Find the computation model associated to an array type.

        Args:
            array_type: The array type.

        Returns:
            The computation model associated to the array type.

        Example:
            ```pycon
            >>> import numpy as np
            >>> from batcharray.computation import AutoComputationModel
            >>> AutoComputationModel.find_computation_model(np.ndarray)
            ArrayComputationModel()
            >>> AutoComputationModel.find_computation_model(np.ma.MaskedArray)
            MaskedArrayComputationModel()

            ```
        """
        for object_type in array_type.__mro__:
            comp_model = cls.registry.get(object_type, None)
            if comp_model is not None:
                return comp_model
        msg = f"Incorrect array type: {array_type}"
        raise TypeError(msg)

    def argmax(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        return self.find_computation_model(type(arr)).argmax(arr=arr, axis=axis, keepdims=keepdims)

    def argmin(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        return self.find_computation_model(type(arr)).argmin(arr=arr, axis=axis, keepdims=keepdims)

    def argsort(
        self, arr: np.ndarray, axis: int | None = None, *, kind: SortKind | None = None
    ) -> np.ndarray:
        return self.find_computation_model(type(arr)).argsort(arr, axis=axis, kind=kind)

    def concatenate(
        self, arrays: Sequence[T], axis: int | None = None, *, dtype: DTypeLike = None
    ) -> T:
        return self.find_computation_model(type(arrays[0])).concatenate(
            arrays=arrays, axis=axis, dtype=dtype
        )

    def max(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        return self.find_computation_model(type(arr)).max(arr=arr, axis=axis, keepdims=keepdims)

    def mean(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        return self.find_computation_model(type(arr)).mean(arr=arr, axis=axis, keepdims=keepdims)

    def median(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        return self.find_computation_model(type(arr)).median(arr=arr, axis=axis, keepdims=keepdims)

    def min(self, arr: T, axis: int | None = None, *, keepdims: bool = False) -> T:
        return self.find_computation_model(type(arr)).min(arr=arr, axis=axis, keepdims=keepdims)

    def sort(self, arr: T, axis: int | None = None, *, kind: SortKind | None = None) -> T:
        return self.find_computation_model(type(arr)).sort(arr, axis=axis, kind=kind)


def register_computation_models() -> None:
    r"""Register computation models to ``AutoComputationModel``.

    Example:
        ```pycon
        >>> from batcharray.computation import AutoComputationModel, register_computation_models
        >>> register_computation_models()
        >>> comp_model = AutoComputationModel()
        >>> comp_model
        AutoComputationModel(
          ...
        )

        ```
    """
    # Local import to avoid cyclic dependency
    from batcharray import computation as cmpt  # noqa: PLC0415

    comp_models = {
        np.ndarray: cmpt.ArrayComputationModel(),
        np.ma.MaskedArray: cmpt.MaskedArrayComputationModel(),
    }

    for array_type, comp_model in comp_models.items():
        if not AutoComputationModel.has_computation_model(array_type):  # pragma: no cover
            AutoComputationModel.add_computation_model(array_type, comp_model)
