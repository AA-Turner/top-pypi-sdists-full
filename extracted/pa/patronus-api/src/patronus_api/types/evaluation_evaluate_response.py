# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "EvaluationEvaluateResponse",
    "Result",
    "ResultEvaluationResult",
    "ResultEvaluationResultAdditionalInfo",
    "ResultEvaluationResultAdditionalInfoConfidenceInterval",
    "ResultEvaluationResultEvaluatedModelAttachment",
]


class ResultEvaluationResultAdditionalInfoConfidenceInterval(BaseModel):
    alpha: float

    lower: Optional[float] = None

    median: Optional[float] = None

    strategy: str

    upper: Optional[float] = None


class ResultEvaluationResultAdditionalInfo(BaseModel):
    confidence_interval: Optional[ResultEvaluationResultAdditionalInfoConfidenceInterval] = None

    extra: Optional[object] = None

    positions: Optional[List[List[float]]] = None


class ResultEvaluationResultEvaluatedModelAttachment(BaseModel):
    media_type: str

    url: str

    usage_type: str


class ResultEvaluationResult(BaseModel):
    id: Optional[str] = None

    additional_info: ResultEvaluationResultAdditionalInfo

    app: Optional[str] = None

    created_at: Optional[datetime] = None

    criteria: Optional[str] = None

    criteria_revision: Optional[int] = None

    dataset_id: Optional[str] = None

    dataset_sample_id: Optional[int] = None

    evaluated_model_gold_answer: Optional[str] = None

    evaluated_model_id: Optional[str] = None

    evaluated_model_input: Optional[str] = None

    evaluated_model_name: Optional[str] = None

    evaluated_model_output: Optional[str] = None

    evaluated_model_params: Optional[object] = None

    evaluated_model_provider: Optional[str] = None

    evaluated_model_retrieved_context: Optional[List[str]] = None

    evaluated_model_selected_model: Optional[str] = None

    evaluated_model_system_prompt: Optional[str] = None

    evaluation_duration: Optional[str] = None

    evaluation_feedback: Optional[bool] = None

    evaluation_run_id: Optional[int] = None

    evaluator_family: Optional[str] = None

    evaluator_id: Optional[str] = None

    evaluator_profile_public_id: Optional[str] = None

    experiment_id: Optional[str] = None

    explain_strategy: Optional[Literal["never", "on-fail", "on-success", "always"]] = None

    explanation: Optional[str] = None

    explanation_duration: Optional[str] = None

    external: bool

    favorite: Optional[bool] = None

    log_id: Optional[str] = None

    profile_name: Optional[str] = None

    project_id: Optional[str] = None

    tags: Optional[Dict[str, str]] = None

    annotation_criteria_id: Optional[str] = None

    evaluated_model_attachments: Optional[List[ResultEvaluationResultEvaluatedModelAttachment]] = None

    evaluation_metadata: Optional[object] = None

    evaluation_type: Optional[str] = None

    metric_description: Optional[str] = None

    metric_name: Optional[str] = None

    pass_: Optional[bool] = FieldInfo(alias="pass", default=None)

    score_raw: Optional[float] = None

    text_output: Optional[str] = None

    usage_tokens: Optional[int] = None


class Result(BaseModel):
    criteria: Optional[str] = None

    error_message: Optional[str] = None

    evaluation_result: Optional[ResultEvaluationResult] = None

    evaluator_id: str

    status: str
    """Status of the criterion evaluation. "success" indicates successful evaluation."""


class EvaluationEvaluateResponse(BaseModel):
    results: List[Result]
