# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .span_type import SpanType
from .span_status import SpanStatus
from .shared.identity import Identity

__all__ = ["Span"]


class Span(BaseModel):
    id: str

    account_id: str

    name: str

    start_timestamp: datetime

    trace_id: str
    """id for grouping traces together, uuid is recommended"""

    application_interaction_id: Optional[str] = None
    """The interaction ID this span belongs to"""

    application_variant_id: Optional[str] = None
    """The id of the application variant this span belongs to"""

    created_by: Optional[Identity] = None
    """The identity that created the entity."""

    end_timestamp: Optional[datetime] = None

    expected: Optional[Dict[str, object]] = None

    group_id: Optional[str] = None
    """Reference to a group_id"""

    input: Optional[Dict[str, object]] = None

    input_tokens: Optional[int] = None
    """Prompt tokens the producer reported for this span, absent when it reported none.

    Same quantity the input_tokens sort orders by.
    """

    metadata: Optional[Dict[str, object]] = None

    object: Optional[Literal["span"]] = None

    obs_span_id: Optional[str] = None
    """W3C span id of the observability span this span executed in."""

    obs_trace_id: Optional[str] = None
    """W3C trace id of the observability trace this span executed in.

    Null for spans written without the edge, and for accounts still served by the
    legacy trace store.
    """

    output: Optional[Dict[str, builtins.object]] = None

    output_tokens: Optional[int] = None
    """
    Completion tokens the producer reported for this span, absent when it reported
    none. Same quantity the output_tokens sort orders by.
    """

    parent_id: Optional[str] = None
    """Reference to a parent span_id"""

    status: Optional[SpanStatus] = None

    type: Optional[SpanType] = None
