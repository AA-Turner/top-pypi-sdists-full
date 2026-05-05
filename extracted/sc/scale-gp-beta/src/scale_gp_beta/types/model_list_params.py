# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .chat.sort_order import SortOrder
from .chat.inference_model_vendor import InferenceModelVendor

__all__ = ["ModelListParams"]


class ModelListParams(TypedDict, total=False):
    ending_before: str

    limit: int

    model_vendor: InferenceModelVendor

    name: str

    sort_by: str

    sort_order: SortOrder

    starting_after: str
