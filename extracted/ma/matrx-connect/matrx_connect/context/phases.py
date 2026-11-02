"""Phase definitions for the streaming event system.

Phases represent state machine transitions — the frontend renders a progress
indicator by switching on the phase value. No metadata, no messages.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


Phase = Literal[
    "connected",
    "processing",
    "generating",
    "using_tools",
    "persisting",
    "searching",
    "scraping",
    "analyzing",
    "synthesizing",
    "retrying",
    "executing",
    "complete",
]


class PhasePayload(BaseModel):
    model_config = {"extra": "forbid"}
    phase: Phase
