"""Implement base classes for metric definitions"""

from __future__ import annotations

import abc
from collections.abc import Mapping, Sequence
from typing import Any, get_type_hints

from dlt.common.utils import simple_repr, without_none

from dlthub.data_quality.typing import TMetricLevel


class _BaseMetricDefinition:
    def __init__(self, **kwargs: Any):
        """Initialize the metric with the given arguments"""
        self._arguments = without_none(kwargs)

    @property
    @abc.abstractmethod
    def level(self) -> TMetricLevel:
        """Metric level"""

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def description(self) -> str:
        return self.__doc__.format(**self.arguments)

    @abc.abstractmethod
    def expr(self, *args: Any, **kwargs: Any) -> Any:
        """SQL, SQLGlot, or Ibis expression underlying the check"""

    @property
    def return_type(self) -> type:
        """Return type of the metric"""
        return get_type_hints(self.expr)["return"]  # type: ignore[no-any-return]

    # @abc.abstractmethod
    # @property
    # def is_variant(self) -> bool:
    #     """True if the metric return type depends on the input type."""

    @property
    def parameters(self) -> Sequence[str]:
        return tuple(
            [k for k in self.__init__.__annotations__.keys() if k != "return"]  # type: ignore[misc]
        )

    @property
    def arguments(self) -> Mapping[str, Any]:
        return self._arguments

    def __repr__(self) -> str:
        return simple_repr(
            self.name, **{k: v for k, v in self.arguments.items() if k != "true_is_success"}
        )

    def __eq__(self, other: Any) -> bool:
        return bool(
            self.name == getattr(other, "name", None)
            and self.level == getattr(other, "level", None)
            and self.arguments == getattr(other, "arguments", None)
        )


class ColumnMetricDefinition(_BaseMetricDefinition):
    def __init__(self, column: str) -> None:
        self._column = column
        self._arguments = {}

    @property
    def column(self) -> str:
        return self._column

    @property
    def level(self) -> TMetricLevel:
        return "column"


class TableMetricDefinition(_BaseMetricDefinition):
    @property
    def level(self) -> TMetricLevel:
        return "table"


class DatasetMetricDefinition(_BaseMetricDefinition):
    @property
    def level(self) -> TMetricLevel:
        return "dataset"
