# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .browser_event_source import BrowserEventSource

__all__ = ["BrowserCaptchaSolveResultEvent", "Data"]


class Data(BaseModel):
    captcha_type: Literal["hcaptcha", "recaptcha_v2", "recaptcha_v3", "turnstile", "geetest", "press_and_hold", "other"]
    """Captcha kind.

    Enterprise reCAPTCHA variants are grouped into their version bucket
    (recaptcha_v2 or recaptcha_v3), press-and-hold challenges use press_and_hold,
    and unlisted kinds use other.
    """

    duration_ms: float
    """Wall-clock duration from solve start to terminal outcome.

    Authoritative solve timing; do not derive it from the gap to a
    captcha_solve_started event, whose delivery and ordering are not guaranteed.
    """

    status: Literal["success", "failure", "timeout", "abandoned"]
    """Terminal outcome.

    success: solver returned a usable solution. failure: solver returned an error
    (see error_code). timeout: solver did not return within the caller's wait
    budget. abandoned: caller cancelled or the page navigated away mid-solve.
    """

    challenge_id: Optional[str] = None
    """Opaque identifier shared by events for one visible challenge.

    An image-grid captcha may create multiple task_id values for one challenge_id.
    The same value may continue across a page reload when the challenge episode
    continues. It does not indicate task ordering or challenge completion.
    """

    error_code: Optional[str] = None
    """Solver-specific error code on failure (e.g.

    ERROR_CAPTCHA_UNSOLVABLE). Absent on success.
    """

    task_id: Optional[str] = None
    """Opaque identifier shared with the matching captcha_solve_started."""

    website_host: Optional[str] = None
    """Host of the page where the captcha was solved."""

    website_path: Optional[str] = None
    """Path of the page where the captcha was solved. Query string excluded."""


class BrowserCaptchaSolveResultEvent(BaseModel):
    """A captcha solve attempt reached a terminal outcome."""

    category: Literal["captcha"]

    source: BrowserEventSource
    """Provenance metadata identifying which producer emitted the event."""

    ts: int
    """Event timestamp in Unix microseconds."""

    type: Literal["captcha_solve_result"]

    data: Optional[Data] = None

    truncated: Optional[bool] = None
    """True if the data field was truncated due to size limits."""
