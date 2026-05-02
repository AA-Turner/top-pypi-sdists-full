# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["TraceInsightListParams"]


class TraceInsightListParams(TypedDict, total=False):
    app: Optional[str]

    experiment_id: Optional[str]

    job_id: Optional[str]

    limit: int

    offset: int

    project_id: Optional[str]

    trace_id: Optional[str]
