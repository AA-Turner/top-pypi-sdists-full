"""The reader's gate (daemon cost round 4, D).

Most unasked reader turns end with nothing to send (6,199 of 6,464 turns on
2026-10-12), and each one pays the reader's model to read the new events and
decide so. Before an unasked turn, a cheap model -- the server's `gate` alias,
on its own lane (`model.LANE_GATE`) -- reads the reader's own job description
and the same new events, and says whether the reader should look.

- SHADOW: the reader looks anyway; the verdict rides on its turn's trace, so a
  skip on a turn that sent a message is a measured miss.
- ON: a skip closes the wake as a SKIPPED turn costing the gate's call alone. The
  reader's cursor stays where it was, so its next turn -- or an ask -- reads the
  skipped events too (`ReaderLane`, bounded by its usual window).
- An ask never goes through the gate, and any failure of it -- an error, a
  refusal (the server answers one with an error on this lane, never a
  fallback's answer), a timeout -- is a LOOK. The gate can only save a turn.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field

from probe._compat import StrEnum

log = logging.getLogger("probe.daemon")

#: One gate call's time limit: past it the reader looks. A call answers in about
#: 1.3 s (p95 1.7 s, 1,315 prod wakes replayed 10-13); in SHADOW every reader
#: turn waits for it, so a stalled one costs a turn at most this much.
GATE_TIMEOUT_S = 20.0

#: The gate's own instructions, after the reader's job description (verbatim, so
#: both judge by the same WHEN TO LOOK, and the prefix caches across wakes).
GATE_INSTRUCTIONS = """### YOU ARE THE READER'S GATE:

- You do not call Probe and you send nothing. You decide only whether the reader should take a turn on the new events below.
- `look: true` when, by WHEN TO LOOK above, the reader would look something up or send the main agent a message now. `look: false` when nothing below calls for it.
- When unsure, `look: true`."""


class Decision(StrEnum):
    LOOK = "look"
    SKIP = "skip"
    #: The gate failed (error, refusal, timeout): the reader looks.
    ERROR = "error"


class GateVerdict(BaseModel):
    """Ends the gate's decision."""

    look: bool = Field(description="true: the reader should take a turn now. false: nothing below calls for one.")
    why: str = Field(description="ONE short line - why.")


@dataclass
class Verdict:
    decision: Decision
    why: str = ""
    error: str | None = None
    model: str | None = None
    input_tokens: int = 0
    cached_tokens: int = 0
    output_tokens: int = 0
    usd: float = 0.0
    latency_ms: int = 0

    @property
    def look(self) -> bool:
        return self.decision != Decision.SKIP

    @property
    def uncached_tokens(self) -> int:
        """Fresh input plus output, as the device meter counts a response."""
        return max(0, self.input_tokens - self.cached_tokens) + self.output_tokens

    def spent(self) -> dict[str, Any]:
        """The gate's spend, in `close_read_turn`'s terms."""
        return {"input_tokens": self.input_tokens, "cached_tokens": self.cached_tokens,
                "output_tokens": self.output_tokens, "usd": self.usd}

    def trace_line(self, events: list[int | None], mode: str) -> dict[str, Any]:
        return {"type": "reader_gate", "decision": str(self.decision), "why": self.why[:300], "error": self.error,
                "events": events, "mode": mode, "model": self.model, "input_tokens": self.input_tokens,
                "cached_tokens": self.cached_tokens, "output_tokens": self.output_tokens, "usd": self.usd,
                "latency_ms": self.latency_ms}


def instructions(read_session: str) -> str:
    return f"{read_session}\n\n{GATE_INSTRUCTIONS}"


async def decide(model: Any, read_session: str, prompt: str, *, timeout_s: float = GATE_TIMEOUT_S) -> Verdict:
    """The gate's verdict on `prompt` (the reader's already-sent messages, then
    the new events). Never raises: any failure is `Decision.ERROR`, a look."""
    from pydantic_ai import Agent, capture_run_messages
    from pydantic_ai.messages import ModelResponse
    from pydantic_ai.usage import UsageLimits

    from probe.daemon import usage as usage_mod

    started = time.monotonic()
    out = Verdict(Decision.ERROR, model=str(getattr(model, "model_name", "") or "") or None)
    # Every response's usage counts, a run that then failed included: those were
    # billed too (review 10-13).
    with capture_run_messages() as messages:
        try:
            agent = Agent(model, instructions=instructions(read_session), output_type=GateVerdict, retries=1)
            result = await asyncio.wait_for(agent.run(prompt, usage_limits=UsageLimits(request_limit=3)),
                                            timeout=timeout_s)
            out.decision = Decision.LOOK if result.output.look else Decision.SKIP
            out.why = (result.output.why or "").strip()
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 -- the gate never stops the reader: a failure is a look
            out.error = f"{type(exc).__name__}: {exc}"[:300]
            log.info("reader gate failed, the reader looks: %s", out.error)
    for m in messages:
        if isinstance(m, ModelResponse):
            u = m.usage
            out.input_tokens += int(u.input_tokens or 0)
            out.cached_tokens += int(u.cache_read_tokens or 0)
            out.output_tokens += int(u.output_tokens or 0)
            out.usd += float(usage_mod.response_cost(m) or 0.0)
            out.model = m.model_name or out.model
    out.latency_ms = int((time.monotonic() - started) * 1000)
    return out
