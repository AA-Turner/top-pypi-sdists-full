# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .sort_order import SortOrder
from .inference_model_vendor import InferenceModelVendor

__all__ = ["CompletionModelsParams"]


class CompletionModelsParams(TypedDict, total=False):
    ending_before: str

    limit: int

    model_vendor: InferenceModelVendor

    sort_by: str

    sort_order: SortOrder

    starting_after: str
