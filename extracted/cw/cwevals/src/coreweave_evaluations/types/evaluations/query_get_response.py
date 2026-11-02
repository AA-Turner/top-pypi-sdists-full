# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = [
    "QueryGetResponse",
    "Definition",
    "DefinitionMetric",
    "DefinitionMetricPer",
    "DefinitionMetricPerVariantEvaluationColumn",
    "DefinitionMetricPerDatasetFieldEvaluationColumn",
    "DefinitionMetricPerScoreEvaluationColumn",
    "DefinitionMetricPerDepthEvaluationColumn",
    "DefinitionMetricPerParentTrajectoryIDEvaluationColumn",
    "DefinitionGroupBy",
    "DefinitionGroupByVariantEvaluationColumn",
    "DefinitionGroupByDatasetFieldEvaluationColumn",
    "DefinitionGroupByScoreEvaluationColumn",
    "DefinitionGroupByDepthEvaluationColumn",
    "DefinitionGroupByParentTrajectoryIDEvaluationColumn",
]


class DefinitionMetricPerVariantEvaluationColumn(BaseModel):
    kind: Literal["variant"]


class DefinitionMetricPerDatasetFieldEvaluationColumn(BaseModel):
    kind: Literal["dataset_field"]

    name: str
    """Name of the input or output field to use as a column."""

    source: Literal["input", "output"]
    """Whether the field belongs to the case's input or output."""


class DefinitionMetricPerScoreEvaluationColumn(BaseModel):
    kind: Literal["score"]

    name: str
    """Name of the scorer whose score supplies this column."""


class DefinitionMetricPerDepthEvaluationColumn(BaseModel):
    """Trajectory queries only.

    Groups by depth, an integer that is 0 for a top-level trajectory.
    """

    kind: Literal["depth"]


class DefinitionMetricPerParentTrajectoryIDEvaluationColumn(BaseModel):
    """Trajectory queries only.

    Groups by the parent trajectory's ID. Top-level trajectories form the null group.
    """

    kind: Literal["parent_trajectory_id"]


DefinitionMetricPer: TypeAlias = Annotated[
    Union[
        DefinitionMetricPerVariantEvaluationColumn,
        DefinitionMetricPerDatasetFieldEvaluationColumn,
        DefinitionMetricPerScoreEvaluationColumn,
        DefinitionMetricPerDepthEvaluationColumn,
        DefinitionMetricPerParentTrajectoryIDEvaluationColumn,
    ],
    PropertyInfo(discriminator="kind"),
]


class DefinitionMetric(BaseModel):
    aggregation: Literal["mean", "sum", "min", "max", "count", "pass_at_k"]
    """
    Calculation to apply to the latest visible score for each case, or for each
    trajectory in a trajectory query.

    - **mean**: Average of integer or number scores, or the fraction of true boolean
      scores.
    - **sum**: Sum of integer or number scores, or the number of true boolean
      scores.
    - **min / max**: Smallest or largest integer, number, boolean, or string score.
      Strings compare lexicographically.
    - **count**: Number of non-null integer, number, boolean, or string scores. Zero
      and false are counted.
    - **pass_at_k**: Estimated probability that at least one of k attempts at a task
      succeeds. Requires boolean scores, k, and per.

    For pass_at_k, per identifies each task. A task with n attempts and c true
    scores contributes 1 - C(n-c, k) / C(n, k), and the result averages the tasks.
    The result is null when a task has fewer than k attempts.
    """

    name: str
    """Unique name for this metric within the query. Result cells use this name."""

    scorer_version_id: str
    """Version of the scorer whose values this metric aggregates.

    It must be registered on the evaluation.
    """

    k: Optional[int] = None
    """Number of attempts per task for pass_at_k.

    Required for pass_at_k and rejected for other aggregations.
    """

    missing: Optional[Literal["skip", "zero"]] = None
    """How to handle a target with no non-null latest visible score.

    A target is a case, or a trajectory in a trajectory query.

    - **skip**: Exclude the target. A mean divides by the number of scored targets,
      and pass_at_k does not count it as an attempt. This also applies when missing
      is omitted.
    - **zero**: Include the target as 0, or false for boolean scores. A mean divides
      by every target in the group, and pass_at_k counts it as a failed attempt.

    Only mean, sum, and pass_at_k support zero. min, max, and count accept only
    skip.
    """

    per: Optional[DefinitionMetricPer] = None
    """
    Column that identifies the task for each case, or for each trajectory in a
    trajectory query, such as an input task field.

    - Required for pass_at_k and rejected for other aggregations.
    - Must not also appear in group_by, and must not be depth or
      parent_trajectory_id.
    - Targets with no value in this column form one task.
    - A page returns 400 if the number of groups multiplied by their tasks exceeds
      the result row limit.
    """


class DefinitionGroupByVariantEvaluationColumn(BaseModel):
    kind: Literal["variant"]


class DefinitionGroupByDatasetFieldEvaluationColumn(BaseModel):
    kind: Literal["dataset_field"]

    name: str
    """Name of the input or output field to use as a column."""

    source: Literal["input", "output"]
    """Whether the field belongs to the case's input or output."""


class DefinitionGroupByScoreEvaluationColumn(BaseModel):
    kind: Literal["score"]

    name: str
    """Name of the scorer whose score supplies this column."""


class DefinitionGroupByDepthEvaluationColumn(BaseModel):
    """Trajectory queries only.

    Groups by depth, an integer that is 0 for a top-level trajectory.
    """

    kind: Literal["depth"]


class DefinitionGroupByParentTrajectoryIDEvaluationColumn(BaseModel):
    """Trajectory queries only.

    Groups by the parent trajectory's ID. Top-level trajectories form the null group.
    """

    kind: Literal["parent_trajectory_id"]


DefinitionGroupBy: TypeAlias = Annotated[
    Union[
        DefinitionGroupByVariantEvaluationColumn,
        DefinitionGroupByDatasetFieldEvaluationColumn,
        DefinitionGroupByScoreEvaluationColumn,
        DefinitionGroupByDepthEvaluationColumn,
        DefinitionGroupByParentTrajectoryIDEvaluationColumn,
    ],
    PropertyInfo(discriminator="kind"),
]


class Definition(BaseModel):
    metrics: List[DefinitionMetric]

    v: int
    """Stored definition version. Always present in responses."""

    group_by: Optional[List[DefinitionGroupBy]] = None

    target_kind: Optional[Literal["trajectory"]] = None
    """Absent for a query over cases."""


class QueryGetResponse(BaseModel):
    definition: Definition

    evaluation_id: str

    evaluation_query_id: str

    name: str

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    scope_ref: str
