# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SessionSignalCatalogResponse", "Signal"]


class Signal(BaseModel):
    description: str

    label: str

    severity: Literal["info", "warning", "danger", "success"]

    source: Literal["manual", "derived"]

    value: Literal[
        "captcha_encountered",
        "proxy_connection_failed",
        "session_timeout_exceeded",
        "bot_detection_triggered",
        "context_restored",
    ]


class SessionSignalCatalogResponse(BaseModel):
    """Current customer-visible signal definitions, not per-session detection evidence"""

    semantics: str
    """Interpretation and coverage limitations of session signals"""

    signals: List[Signal]
