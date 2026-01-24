# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["TraceInsightListJobsParams"]


class TraceInsightListJobsParams(TypedDict, total=False):
    app: Optional[str]

    experiment_id: Optional[str]

    job_id: Optional[str]

    job_status: Optional[Literal["pending", "success", "failed", "cancelled"]]

    limit: int

    offset: int

    project_id: Optional[str]

    trace_id: Optional[str]
