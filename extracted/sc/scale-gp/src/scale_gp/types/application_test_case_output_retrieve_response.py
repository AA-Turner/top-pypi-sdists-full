# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .result_schema_flexible import ResultSchemaFlexible
from .application_metric_score import ApplicationMetricScore
from .evaluation_datasets.test_case import TestCase
from .shared.result_schema_generation import ResultSchemaGeneration
from .shared.application_interaction_with_spans_response import ApplicationInteractionWithSpansResponse

__all__ = [
    "ApplicationTestCaseOutputRetrieveResponse",
    "ApplicationTestCaseGenerationOutputResponseWithViews",
    "ApplicationTestCaseFlexibleOutputResponseWithViews",
]


class ApplicationTestCaseGenerationOutputResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ResultSchemaGeneration

    test_case_id: str

    application_interaction_id: Optional[str] = None

    application_test_case_output_group_id: Optional[str] = None

    interaction: Optional[ApplicationInteractionWithSpansResponse] = None

    metric_scores: Optional[List[ApplicationMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["GENERATION"]] = None

    test_case_version: Optional[TestCase] = None


class ApplicationTestCaseFlexibleOutputResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ResultSchemaFlexible

    test_case_id: str

    application_interaction_id: Optional[str] = None

    application_test_case_output_group_id: Optional[str] = None

    interaction: Optional[ApplicationInteractionWithSpansResponse] = None

    metric_scores: Optional[List[ApplicationMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["FLEXIBLE"]] = None

    test_case_version: Optional[TestCase] = None


ApplicationTestCaseOutputRetrieveResponse: TypeAlias = Annotated[
    Union[ApplicationTestCaseGenerationOutputResponseWithViews, ApplicationTestCaseFlexibleOutputResponseWithViews],
    PropertyInfo(discriminator="schema_type"),
]
