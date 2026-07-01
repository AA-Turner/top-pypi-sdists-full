# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .span_type import SpanType
from .span_status import SpanStatus

__all__ = ["SpanCreateParams"]


class SpanCreateParams(TypedDict, total=False):
    name: Required[str]

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    trace_id: Required[str]
    """id for grouping traces together, uuid is recommended"""

    id: str
    """The id of the span"""

    application_interaction_id: str
    """The optional application interaction ID this span belongs to"""

    application_variant_id: str
    """The optional application variant ID this span belongs to"""

    end_timestamp: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    group_id: str
    """Reference to a group_id"""

    input: Dict[str, object]

    metadata: Dict[str, object]

    output: Dict[str, object]

    parent_id: str
    """Reference to a parent span_id"""

    status: SpanStatus

    type: SpanType
