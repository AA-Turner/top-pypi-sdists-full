# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["TraceInsightGetErrorAggregationsResponse", "Error"]


class Error(BaseModel):
    error_type: str

    number_of_errors: int

    number_of_high_failures: int

    number_of_low_failures: int

    number_of_medium_failures: int

    percentage_of_failures: float


class TraceInsightGetErrorAggregationsResponse(BaseModel):
    errors: List[Error]
