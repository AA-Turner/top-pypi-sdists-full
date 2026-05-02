# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .annotation_config import AnnotationConfig
from .evaluation_dataset import EvaluationDataset
from .question_set_with_questions import QuestionSetWithQuestions
from .shared.auto_evaluation_parameters import AutoEvaluationParameters
from .shared.question_set_question_config import QuestionSetQuestionConfig

__all__ = [
    "EvaluationListResponse",
    "ApplicationSpec",
    "AsyncJob",
    "EvaluationConfigExpanded",
    "EvaluationConfigExpandedEvaluationConfigExpanded",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpanded",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSet",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestion",
    "MetricConfig",
    "MetricConfigComponent",
]


class ApplicationSpec(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    description: str
    """The description of the Application Spec"""

    name: str
    """The name of the Application Spec"""

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    created_by_identity_type: Optional[Literal["user", "service_account"]] = None
    """The type of identity that created the entity."""

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    parent_application_spec_id: Optional[str] = None
    """
    Application spec ID of the parent application from which the variants and
    deployments are inherited.
    """

    run_online_evaluation: Optional[bool] = None
    """Whether the application spec should run online evaluation, default is `false`"""

    theme_id: Optional[str] = None


class AsyncJob(BaseModel):
    id: str
    """The unique identifier of the entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    status: str

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    job_metadata: Optional[Dict[str, object]] = None

    job_type: Optional[str] = None

    parent_job_id: Optional[str] = None

    progress: Optional[Dict[str, object]] = None

    status_reason: Optional[str] = None


class EvaluationConfigExpandedEvaluationConfigExpanded(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_type: Literal["studio", "llm_auto", "human", "llm_benchmark"]
    """Evaluation type"""

    question_set: QuestionSetWithQuestions

    question_set_id: str

    auto_evaluation_model: Optional[
        Literal[
            "gpt-4-32k-0613",
            "gpt-4-turbo-preview",
            "gpt-4-turbo-2024-04-09",
            "gpt-4o-2024-05-13",
            "gpt-4o",
            "gpt-4o-mini-2024-07-18",
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano",
            "o1",
            "o1-mini",
            "o3",
            "o3-mini",
            "o3-mini-2025-01-31",
            "o4-mini",
            "gpt-oss-120b",
            "gpt-oss-20b",
            "llama-3-70b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-70b-instruct-bedrock",
        ]
    ] = None
    """The name of the model to be used for auto-evaluation"""

    auto_evaluation_parameters: Optional[AutoEvaluationParameters] = None
    """Execution parameters for auto-evaluation"""

    studio_project_id: Optional[str] = None


class EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestion(BaseModel):
    id: str
    """The unique identifier of the entity."""

    prompt: str

    title: str

    type: Literal["categorical", "free_text", "rating", "number", "form", "timestamp"]

    choices: Optional[List[Dict[str, object]]] = None
    """List of choices for the question. Required for CATEGORICAL questions."""

    conditions: Optional[List[Dict[str, object]]] = None
    """Conditions for the question to be shown."""

    multi: Optional[bool] = None
    """Whether the question allows multiple answers."""

    required: Optional[bool] = None
    """Whether the question is required."""


class EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSet(BaseModel):
    questions: List[EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestion]

    question_id_to_config: Optional[Dict[str, QuestionSetQuestionConfig]] = None


class EvaluationConfigExpandedLegacyEvaluationConfigExpanded(BaseModel):
    evaluation_type: Literal["studio", "llm_auto", "human", "llm_benchmark"]

    question_set: EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSet

    studio_project_id: Optional[str] = None


EvaluationConfigExpanded: TypeAlias = Union[
    EvaluationConfigExpandedEvaluationConfigExpanded, EvaluationConfigExpandedLegacyEvaluationConfigExpanded
]


class MetricConfigComponent(BaseModel):
    name: str

    type: Literal["rouge", "rouge1", "rouge2", "rougeL", "bleu", "meteor", "cosine_similarity", "f1"]

    mappings: Optional[Dict[str, List[str]]] = None

    params: Optional[Dict[str, object]] = None


class MetricConfig(BaseModel):
    """Specifies the config for the metrics to be computed."""

    components: List[MetricConfigComponent]


class EvaluationListResponse(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    completed_test_case_result_count: int
    """The number of test case results that have been completed for the evaluation"""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    description: str

    name: str

    status: Literal["PENDING", "COMPLETED", "FAILED"]

    total_test_case_result_count: int
    """The total number of test case results for the evaluation"""

    annotation_config: Optional[AnnotationConfig] = None
    """Annotation configuration for tasking"""

    application_spec: Optional[ApplicationSpec] = None

    application_variant_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    async_jobs: Optional[List[AsyncJob]] = None

    completed_at: Optional[datetime] = None
    """
    The date and time that all test case results for the evaluation were completed
    for the evaluation in ISO format.
    """

    evaluation_config: Optional[Dict[str, object]] = None

    evaluation_config_expanded: Optional[EvaluationConfigExpanded] = None

    evaluation_config_id: Optional[str] = None
    """The ID of the associated evaluation config."""

    evaluation_datasets: Optional[List[EvaluationDataset]] = None

    metric_config: Optional[MetricConfig] = None
    """Specifies the config for the metrics to be computed."""

    question_id_to_annotation_config: Optional[Dict[str, AnnotationConfig]] = None
    """Specifies the annotation configuration to use for specific questions."""

    tags: Optional[Dict[str, object]] = None
