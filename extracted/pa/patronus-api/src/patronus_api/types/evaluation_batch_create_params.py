# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EvaluationBatchCreateParams", "Evaluation"]


class EvaluationBatchCreateParams(TypedDict, total=False):
    evaluations: Required[Iterable[Evaluation]]


_EvaluationReservedKeywords = TypedDict(
    "_EvaluationReservedKeywords",
    {
        "pass": Optional[bool],
    },
    total=False,
)


class Evaluation(_EvaluationReservedKeywords, total=False):
    evaluator_id: Required[str]

    log_id: Required[str]

    app: Optional[str]
    """Attach app to the evaluation."""

    created_at: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    criteria: Optional[str]

    dataset_id: Optional[str]

    dataset_sample_id: Optional[str]

    evaluation_duration: Optional[str]

    experiment_id: Optional[str]

    explanation: Optional[str]

    explanation_duration: Optional[str]

    metadata: Optional[object]

    metric_description: Optional[str]

    metric_name: Optional[str]

    project_id: Optional[str]
    """
    Attach project with given ID to the evaluation. **Note**: This parameter is
    ignored in case project_name is provided.
    """

    project_name: Optional[str]
    """
    Attach project with given name to the evaluation. If project with given name
    doesn't exist, one will be created. **Note:** This parameter takes precedence
    over project_id.
    """

    score: Optional[float]

    span_id: Optional[str]

    tags: Optional[object]
    """Tags are key-value pairs used to label resources"""

    text_output: Optional[str]

    trace_id: Optional[str]
