# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ....._utils import PropertyInfo
from ....._models import BaseModel

__all__ = [
    "ResultListResponse",
    "GroupBy",
    "Metric",
    "MetricPer",
    "MetricPerVariantEvaluationColumn",
    "MetricPerDatasetFieldEvaluationColumn",
    "MetricPerScoreEvaluationColumn",
    "MetricPerDepthEvaluationColumn",
    "MetricPerParentTrajectoryIDEvaluationColumn",
    "Row",
    "RowMetric",
]


class GroupBy(BaseModel):
    kind: Literal["variant", "dataset_field", "score", "depth", "parent_trajectory_id"]

    value_type: Literal["boolean", "integer", "number", "string"]

    name: Optional[str] = None

    source: Optional[Literal["input", "output"]] = None


class MetricPerVariantEvaluationColumn(BaseModel):
    kind: Literal["variant"]


class MetricPerDatasetFieldEvaluationColumn(BaseModel):
    kind: Literal["dataset_field"]

    name: str
    """Name of the input or output field to use as a column."""

    source: Literal["input", "output"]
    """Whether the field belongs to the case's input or output."""


class MetricPerScoreEvaluationColumn(BaseModel):
    kind: Literal["score"]

    name: str
    """Name of the scorer whose score supplies this column."""


class MetricPerDepthEvaluationColumn(BaseModel):
    """Trajectory queries only.

    Groups by depth, an integer that is 0 for a top-level trajectory.
    """

    kind: Literal["depth"]


class MetricPerParentTrajectoryIDEvaluationColumn(BaseModel):
    """Trajectory queries only.

    Groups by the parent trajectory's ID. Top-level trajectories form the null group.
    """

    kind: Literal["parent_trajectory_id"]


MetricPer: TypeAlias = Annotated[
    Union[
        MetricPerVariantEvaluationColumn,
        MetricPerDatasetFieldEvaluationColumn,
        MetricPerScoreEvaluationColumn,
        MetricPerDepthEvaluationColumn,
        MetricPerParentTrajectoryIDEvaluationColumn,
    ],
    PropertyInfo(discriminator="kind"),
]


class Metric(BaseModel):
    aggregation: Literal["mean", "sum", "min", "max", "count", "pass_at_k"]

    name: str

    scorer_id: str

    scorer_version_id: str

    value_type: Literal["boolean", "integer", "number", "string"]
    """
    Aggregation output type: number for mean and pass_at_k, integer for count and
    boolean sum, and the scorer's type otherwise.
    """

    k: Optional[int] = None

    missing: Optional[Literal["skip", "zero"]] = None

    per: Optional[MetricPer] = None
    """Trajectory queries only.

    Groups by depth, an integer that is 0 for a top-level trajectory.
    """


class RowMetric(BaseModel):
    name: str

    value: Union[Optional[bool], Optional[int], Optional[float], Optional[str]]
    """Calculated metric value.

    If no target has a non-null latest visible score, count returns 0 and other
    aggregations return null.
    """


class Row(BaseModel):
    group: List[Union[Optional[bool], Optional[int], Optional[float], Optional[str]]]
    """Values in group_by order, with null for missing or null fields.

    Empty for an ungrouped query.
    """

    metrics: List[RowMetric]

    targets: int
    """Number of targets in this group: cases, or trajectories in a trajectory query."""


class ResultListResponse(BaseModel):
    dataset_version_id: str
    """Dataset version supplying the cases or trajectories.

    For a live evaluation queried on latest data, this is the dataset head selected
    for the first page.
    """

    evaluation_id: str

    evaluation_query_id: str

    group_by: List[GroupBy]

    metrics: List[Metric]

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    published_commit_id: int
    """Publication cutoff shared by every page of these results.

    Scores published later are excluded. For a live evaluation's latest data, cases
    and trajectories published later are also excluded.
    """

    rows: List[Row]

    scope_ref: str

    target_kind: Literal["case", "trajectory"]
    """Kind of target that each row's targets field counts."""

    evaluation_version_id: Optional[str] = None
    """Frozen evaluation version supplying the data.

    Omitted when querying the evaluation's latest data.
    """

    next_cursor: Optional[str] = None
    """Cursor for the next page. Absent on the last page."""
