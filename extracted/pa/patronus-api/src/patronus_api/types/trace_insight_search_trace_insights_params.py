# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TraceInsightSearchTraceInsightsParams"]


class TraceInsightSearchTraceInsightsParams(TypedDict, total=False):
    app: Optional[str]

    end_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    error_types: Optional[List[str]]

    experiment_id: Optional[int]

    limit: int

    offset: int

    project_id: Optional[str]

    redis_job_id: Optional[str]

    start_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    trace_id: Optional[str]
