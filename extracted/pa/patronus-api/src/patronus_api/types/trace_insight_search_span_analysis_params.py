# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TraceInsightSearchSpanAnalysisParams"]


class TraceInsightSearchSpanAnalysisParams(TypedDict, total=False):
    end_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    limit: int

    offset: int

    span_id: Optional[str]

    start_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    trace_id: Optional[str]
