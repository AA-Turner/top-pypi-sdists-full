"""Per-conversation observer state for the Pipecat integration.

Split out of `native_callback.py` to keep that module inside the 500-line policy.
State only: no behaviour, and no Pipecat import (unavailable on Python 3.10).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aigie.tracing.workflow_root import WorkflowRoot


@dataclass
class _Boundary:
    trace_id: str
    root: WorkflowRoot
    ambient_token: Any = None
    turn_run_id: str | None = None
    open_spans: dict[str, str] = field(default_factory=dict)
    # Deltas straddle transcript boundaries, so no one span's value is "the"
    # total, but the provider bills per connection — so the running sum is.
    stt_audio_seconds_total: float = 0.0
    tts_character_count_total: float = 0.0
    # STT usage lands before the final TranscriptionFrame that opens-and-closes
    # its span, so there is nowhere else to hold it.
    pending_stt_usage: Any = None
    # The STT usage frame *after* a final transcript bills trailing silence;
    # discard it rather than misattach it to the next utterance. See `_media`.
    discard_next_stt_usage: bool = False
    # An LLM call's usage frame can land after its text phase closed, possibly
    # after the next call has started. FIFO, oldest first.
    pending_llm: list[str] = field(default_factory=list)
    # LLMContextFrame precedes the span it belongs to. Overwritten, not
    # appended: only the most recent context is relevant to the next call.
    pending_llm_context: list[dict[str, Any]] | None = None
    # Set only by a barge-in InterruptionFrame, so the normal end frames Pipecat
    # still pushes close their span as "interrupted" rather than "success".
    interrupted: bool = False
