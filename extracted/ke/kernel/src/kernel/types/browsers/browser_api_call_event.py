# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .browser_event_source import BrowserEventSource

__all__ = ["BrowserAPICallEvent", "Data"]


class Data(BaseModel):
    duration_ms: float
    """Wall-clock duration of the handler in milliseconds."""

    operation_id: str
    """Matched route's operation, named as the in-VM API names its handler (e.g.

    ProcessExec, TakeScreenshot).
    """

    request_id: str
    """Per-request identifier from the in-VM API request middleware."""

    status: int
    """HTTP response status code."""

    code: Optional[str] = None
    """
    Source submitted to the Playwright code-execution endpoint, capped at 8192 bytes
    like every other captured string. A capped value is cut on a character boundary
    and ends in `...[truncated]`. Absent for every other operation.
    """


class BrowserAPICallEvent(BaseModel):
    """
    An agent-driven HTTP call that drives the browser, handled by the in-VM API server. Calls that manage the VM instead emit platform_api_call.
    """

    category: Literal["control"]

    source: BrowserEventSource
    """Provenance metadata identifying which producer emitted the event."""

    ts: int
    """Event timestamp in Unix microseconds."""

    type: Literal["api_call"]

    data: Optional[Data] = None

    truncated: Optional[bool] = None
    """True if the data field was truncated due to size limits."""
