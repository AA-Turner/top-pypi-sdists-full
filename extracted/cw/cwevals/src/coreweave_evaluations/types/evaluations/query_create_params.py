# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "QueryCreateParams",
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


class QueryCreateParams(TypedDict, total=False):
    namespace: str
    """Namespace that assigned the scope reference."""

    scope_id: str
    """Project reference assigned by the namespace.

    For wandb, use the internal W&B project ID, not the project name or
    entity/project path.

    Percent-encode reserved characters so the reference occupies one URL path
    segment. Only printable ASCII is accepted. References are compared exactly,
    without parsing.
    """

    definition: Required[Definition]

    name: Required[str]


class DefinitionMetricPerVariantEvaluationColumn(TypedDict, total=False):
    kind: Required[Literal["variant"]]


class DefinitionMetricPerDatasetFieldEvaluationColumn(TypedDict, total=False):
    kind: Required[Literal["dataset_field"]]

    name: Required[str]
    """Name of the input or output field to use as a column."""

    source: Required[Literal["input", "output"]]
    """Whether the field belongs to the case's input or output."""


class DefinitionMetricPerScoreEvaluationColumn(TypedDict, total=False):
    kind: Required[Literal["score"]]

    name: Required[str]
    """Name of the scorer whose score supplies this column."""


class DefinitionMetricPerDepthEvaluationColumn(TypedDict, total=False):
    """Trajectory queries only.

    Groups by depth, an integer that is 0 for a top-level trajectory.
    """

    kind: Required[Literal["depth"]]


class DefinitionMetricPerParentTrajectoryIDEvaluationColumn(TypedDict, total=False):
    """Trajectory queries only.

    Groups by the parent trajectory's ID. Top-level trajectories form the null group.
    """

    kind: Required[Literal["parent_trajectory_id"]]


DefinitionMetricPer: TypeAlias = Union[
    DefinitionMetricPerVariantEvaluationColumn,
    DefinitionMetricPerDatasetFieldEvaluationColumn,
    DefinitionMetricPerScoreEvaluationColumn,
    DefinitionMetricPerDepthEvaluationColumn,
    DefinitionMetricPerParentTrajectoryIDEvaluationColumn,
]


class DefinitionMetric(TypedDict, total=False):
    aggregation: Required[Literal["mean", "sum", "min", "max", "count", "pass_at_k"]]
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

    name: Required[str]
    """Unique name for this metric within the query. Result cells use this name."""

    scorer_version_id: Required[str]
    """Version of the scorer whose values this metric aggregates.

    It must be registered on the evaluation.
    """

    k: int
    """Number of attempts per task for pass_at_k.

    Required for pass_at_k and rejected for other aggregations.
    """

    missing: Literal["skip", "zero"]
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

    per: DefinitionMetricPer
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


class DefinitionGroupByVariantEvaluationColumn(TypedDict, total=False):
    kind: Required[Literal["variant"]]


class DefinitionGroupByDatasetFieldEvaluationColumn(TypedDict, total=False):
    kind: Required[Literal["dataset_field"]]

    name: Required[str]
    """Name of the input or output field to use as a column."""

    source: Required[Literal["input", "output"]]
    """Whether the field belongs to the case's input or output."""


class DefinitionGroupByScoreEvaluationColumn(TypedDict, total=False):
    kind: Required[Literal["score"]]

    name: Required[str]
    """Name of the scorer whose score supplies this column."""


class DefinitionGroupByDepthEvaluationColumn(TypedDict, total=False):
    """Trajectory queries only.

    Groups by depth, an integer that is 0 for a top-level trajectory.
    """

    kind: Required[Literal["depth"]]


class DefinitionGroupByParentTrajectoryIDEvaluationColumn(TypedDict, total=False):
    """Trajectory queries only.

    Groups by the parent trajectory's ID. Top-level trajectories form the null group.
    """

    kind: Required[Literal["parent_trajectory_id"]]


DefinitionGroupBy: TypeAlias = Union[
    DefinitionGroupByVariantEvaluationColumn,
    DefinitionGroupByDatasetFieldEvaluationColumn,
    DefinitionGroupByScoreEvaluationColumn,
    DefinitionGroupByDepthEvaluationColumn,
    DefinitionGroupByParentTrajectoryIDEvaluationColumn,
]


class Definition(TypedDict, total=False):
    metrics: Required[Iterable[DefinitionMetric]]
    """Calculations to run for each group.

    Metric names must be unique, and scorer versions must be registered on the
    evaluation.
    """

    group_by: Optional[Iterable[DefinitionGroupBy]]
    """Columns whose distinct value combinations form result groups.

    Choose variant, dataset fields, or score columns. Result group values follow
    this column order. Omit, send null, or use an empty list to calculate metrics
    across all targets. A trajectory query reads dataset fields from each
    trajectory's root case and scores from the trajectory, and can also group by the
    trajectory's depth and parent_trajectory_id.
    """

    target_kind: Literal["case", "trajectory"]
    """Targets whose scores the query aggregates.

    Omit or use case to aggregate the dataset's cases. trajectory aggregates scores
    on the dataset's trajectories and groups each trajectory by its root case's
    variant and fields.
    """

    v: int
    """Definition version."""
