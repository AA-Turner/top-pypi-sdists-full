# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["EvaluationDatasetUpdateParams", "PatchEvaluationDatasetRequest", "RestoreRequest"]


class PatchEvaluationDatasetRequest(TypedDict, total=False):
    name: Required[str]
    """The name of the dataset"""

    restore: Literal[False]
    """Set to true to restore the entity from the database."""


class RestoreRequest(TypedDict, total=False):
    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""


EvaluationDatasetUpdateParams: TypeAlias = Union[PatchEvaluationDatasetRequest, RestoreRequest]
