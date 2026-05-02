# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .flexible_test_case_schema_param import FlexibleTestCaseSchemaParam
from .artifact_schema_generation_param import ArtifactSchemaGenerationParam
from .generation_test_case_schema_param import GenerationTestCaseSchemaParam

__all__ = [
    "TestCaseUpdateParams",
    "PartialTestCaseVersionRequest",
    "PartialTestCaseVersionRequestTestCaseData",
    "RestoreRequest",
]


class PartialTestCaseVersionRequest(TypedDict, total=False):
    evaluation_dataset_id: Required[str]

    account_id: str

    chat_history: Dict[str, object]

    restore: Literal[False]
    """Set to true to restore the entity from the database."""

    test_case_data: PartialTestCaseVersionRequestTestCaseData

    test_case_metadata: Dict[str, object]


PartialTestCaseVersionRequestTestCaseData: TypeAlias = Union[
    ArtifactSchemaGenerationParam, GenerationTestCaseSchemaParam, FlexibleTestCaseSchemaParam
]


class RestoreRequest(TypedDict, total=False):
    evaluation_dataset_id: Required[str]

    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""


TestCaseUpdateParams: TypeAlias = Union[PartialTestCaseVersionRequest, RestoreRequest]
