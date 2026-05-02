# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime

from .._models import BaseModel

__all__ = ["TraceInsightSearchSpanAnalysisResponse", "SpanAnalysis"]


class SpanAnalysis(BaseModel):
    analysis: str

    created_at: datetime

    job_id: str

    span_id: str

    trace_id: str


class TraceInsightSearchSpanAnalysisResponse(BaseModel):
    span_analysis: List[SpanAnalysis]
