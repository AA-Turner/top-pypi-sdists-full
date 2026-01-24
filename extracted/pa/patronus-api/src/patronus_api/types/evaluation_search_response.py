# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["EvaluationSearchResponse", "Evaluation"]


class Evaluation(BaseModel):
    id: str

    log_id: str

    annotation_criteria_id: Optional[str] = None

    app: Optional[str] = None

    created_at: Optional[datetime] = None

    criteria: Optional[str] = None

    criteria_id: Optional[str] = None

    criteria_revision: Optional[int] = None

    dataset_id: Optional[str] = None

    dataset_sample_id: Optional[str] = None

    evaluation_duration: Optional[str] = None

    evaluation_type: Optional[Literal["patronus_evaluation", "client_evaluation", "annotation"]] = None

    evaluator_family: Optional[str] = None

    evaluator_id: Optional[str] = None

    experiment_id: Optional[int] = None

    explain_strategy: Optional[str] = None

    explanation: Optional[str] = None

    explanation_duration: Optional[str] = None

    feedback: Optional[Literal["positive", "negative"]] = None

    metadata: Optional[object] = None

    metric_description: Optional[str] = None

    metric_name: Optional[str] = None

    pass_: Optional[bool] = FieldInfo(alias="pass", default=None)

    project_id: Optional[str] = None

    score: Optional[float] = None

    span_id: Optional[str] = None

    tags: Optional[object] = None

    text_output: Optional[str] = None

    trace_id: Optional[str] = None

    usage: Optional[object] = None


class EvaluationSearchResponse(BaseModel):
    evaluations: List[Evaluation]
