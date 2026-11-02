"""decide (`/v1/decide`) — one-shot calibrated decisions: `decide()` sends a state plus typed
questions and returns probabilities."""

from __future__ import annotations

from .infer import decide
from .types import DecideResult

__all__ = ["decide", "DecideResult"]
