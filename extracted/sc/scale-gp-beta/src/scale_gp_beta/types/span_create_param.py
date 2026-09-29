# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .span_type import SpanType
from .span_status import SpanStatus

__all__ = ["SpanCreateParam"]


class SpanCreateParam(TypedDict, total=False):
    name: Required[str]

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """When the span started.

    With trace_id and id it forms the span's storage identity, so a span re-sent
    with a start_timestamp on another UTC day is stored as a second row that the
    store never collapses. Get span and trace detail return the newest version.
    Search returns the newest version whose start_timestamp falls in the queried
    window. Export, metrics and facets count both rows until the trace is deleted
    and re-sent.
    """

    trace_id: Required[str]
    """id for grouping traces together, uuid is recommended"""

    id: str
    """The id of the span, at most 256 bytes.

    A value longer than 256 characters is refused here with a 422 before it is
    forwarded; a value within that count whose UTF-8 form exceeds 256 bytes is
    refused with a 400 naming the field once the tracing service is the account's
    primary store, and accepted for accounts still written primarily to the legacy
    trace store.
    """

    application_interaction_id: str
    """The optional application interaction ID this span belongs to"""

    application_variant_id: str
    """The optional application variant ID this span belongs to"""

    end_timestamp: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expected: Dict[str, object]

    group_id: str
    """Reference to a group_id, at most 256 bytes.

    A value longer than 256 characters is refused here with a 422 before it is
    forwarded; a value within that count whose UTF-8 form exceeds 256 bytes is
    refused with a 400 naming the field once the tracing service is the account's
    primary store, and accepted for accounts still written primarily to the legacy
    trace store.
    """

    input: Dict[str, object]

    metadata: Dict[str, object]

    obs_span_id: str
    """
    W3C span id (16 lowercase hex chars) of the observability span this span
    executed in. Requires obs_trace_id.
    """

    obs_trace_id: str
    """
    W3C trace id (32 lowercase hex chars) of the observability trace this span
    executed in, for correlating a business span with the infrastructure work it
    caused. Stored only by the sgp-traces service, so accounts still served by the
    legacy store accept the field and read it back as null.
    """

    output: Dict[str, object]

    parent_id: str
    """Reference to a parent span_id"""

    status: SpanStatus

    type: SpanType
