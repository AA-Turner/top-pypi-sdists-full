# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .result_schema_flexible import ResultSchemaFlexible
from .shared.result_schema_generation import ResultSchemaGeneration

__all__ = [
    "ApplicationTestCaseOutput",
    "ApplicationTestCaseGenerationOutputResponse",
    "ApplicationTestCaseFlexibleOutputResponse",
]


class ApplicationTestCaseGenerationOutputResponse(BaseModel):
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

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["GENERATION"]] = None


class ApplicationTestCaseFlexibleOutputResponse(BaseModel):
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

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["FLEXIBLE"]] = None


ApplicationTestCaseOutput: TypeAlias = Annotated[
    Union[ApplicationTestCaseGenerationOutputResponse, ApplicationTestCaseFlexibleOutputResponse],
    PropertyInfo(discriminator="schema_type"),
]
