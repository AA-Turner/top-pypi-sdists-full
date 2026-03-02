from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal, TYPE_CHECKING
from typing_extensions import NotRequired

from dlt.common.typing import TypedDict
from dlt.common.data_types import TDataType

if TYPE_CHECKING:
    from dlthub.data_quality.metrics._base import (
        TableMetricDefinition,
        ColumnMetricDefinition,
        DatasetMetricDefinition,
    )
    from dlthub.data_quality.checks._base import LazyCheck


METRICS_HINT_KEY = "x-dq-metrics"
CHECKS_HINT_KEY = "x-dq-checks"

TMetricsConfig = Sequence[str]
TColumnMetricsConfig = Sequence[str]
TTableMetricsConfig = Sequence[str]

TMetricLevel = Literal["column", "table", "dataset"]

TCheckLevel = Literal["row", "table", "dataset"]
"""Used to specify how to aggregate check results:
- row-level: returns `(i rows, j checks)` all associated with a single table
- table-level: returns `(1, j checks)` all associated with a single table
- dataset-level: `(j checks, 4)` associated with one or more tables
"""


# TODO create TMetricHintInline to set on `dlt.Schema.tables[table_name]`
# TODO create TMetricHintStandalone to set on `dlt.Schema.metrics`


class TMetricHint(TypedDict):
    level: TMetricLevel
    name: str
    return_type: TDataType
    is_variant: bool
    args: dict[str, str]


class TResourceMetricsHints(TypedDict):
    table: list[TMetricHint]
    columns: dict[str, list[TMetricHint]]


class TSourceMetricsHints(TypedDict):
    dataset: list[TMetricHint]
    tables: dict[str, list[TMetricHint]]
    columns: dict[str, dict[str, list[TMetricHint]]]


class TSourceMetricsDefinitions(TypedDict):
    dataset: list[DatasetMetricDefinition]
    tables: dict[str, list[TableMetricDefinition]]
    columns: dict[str, dict[str, list[ColumnMetricDefinition]]]


class TMetricsResult(TypedDict):
    level: Literal["column", "table", "dataset"]
    table_name: str | None
    column_name: str | None
    metric_name: str
    metric_value: Any


class TCheckHint(TypedDict):
    name: str
    # TODO ensure JSON-serializable args
    args: dict[str, Any]
    qualified_name: NotRequired[str]
    explanation: NotRequired[str]


class TCheckHintStandalone(TypedDict, TCheckHint):
    table_name: str
    column_name: str


class TSourceChecksHints(TypedDict):
    """Checks as stored on the schema (serialized hints)."""

    dataset: list[TCheckHint]
    tables: dict[str, list[TCheckHint]]


class TSourceChecksDefinitions(TypedDict):
    dataset: list[LazyCheck]
    tables: dict[str, list[LazyCheck]]
