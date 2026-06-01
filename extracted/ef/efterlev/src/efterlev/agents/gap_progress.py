"""Streaming progress reporter for the Gap Agent (v0.1.86).

The Gap Agent is a single batched LLM call that returns ALL N KSI
classifications at once (DECISIONS 2026-04-22 — batched-by-design;
classification needs cross-KSI reasoning, not per-KSI isolation).
That single call takes ~60-90s on Sonnet, longer on Opus, with no
intermediate output — the user stares at a blank prompt wondering
if the process is hung.

This module surfaces progress by:

1. Buffering streaming text-deltas as they arrive from the LLM.
2. Regex-extracting `"ksi_id": "KSI-XXX-YYY"` patterns from the
   in-flight JSON as the model emits classifications.
3. Printing a per-KSI line when each new KSI ID is detected:
       [gap] classifying KSI 12/60: KSI-CNA-RNT
4. Falling back to a token-count heartbeat (one line every ~2s)
   when no KSI has been emitted yet — covers the model's preamble
   (`{"reasoning_summary": ...`) before the classification loop
   actually begins.

JSON-streaming is not safe-to-parse incrementally (truncation =
ValueError). Regex pattern-matching on the cumulative text is the
right shape: a `"ksi_id"` token is unambiguous inside the agent's
output schema (the only places it appears are inside per-KSI
classification objects), so regex matches are guaranteed-real even
on partial JSON.
"""

from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass, field
from typing import TextIO

# Pattern: `"ksi_id": "KSI-FAM-CODE"` with whitespace tolerance. The
# JSON serializer the agent uses is deterministic about field order
# (pydantic), so each classification opens with `"ksi_id"` early in
# its dict — letting us anchor on this token. KSI IDs follow the FRMR
# convention `KSI-<3-letter-family>-<3-letter-code>` (e.g. KSI-CNA-RNT,
# KSI-AFR-UCM); the regex character class matches that shape only.
_KSI_ID_PATTERN = re.compile(r'"ksi_id"\s*:\s*"(KSI-[A-Z]{3}-[A-Z]{3})"')

# Heartbeat throttle: emit a "still working" line at most every 2s
# during the no-KSI-yet preamble phase. Avoids spam while keeping
# the user informed the process isn't hung.
_HEARTBEAT_INTERVAL_SECONDS = 2.0

# Braille spinner frames — cycled across heartbeat emissions so the user
# sees motion (each heartbeat line picks the next frame). Same set rich
# uses for its built-in `dots` spinner.
_SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")


@dataclass
class GapProgressReporter:
    """Stateful per-call reporter; install via `LLMClient.complete(on_chunk=...)`.

    Usage from the CLI:
        reporter = GapProgressReporter(total_ksis=60, stream=sys.stderr)
        report, response, prompt = self._invoke_llm(
            user_message=...,
            max_tokens=...,
            on_chunk=reporter,
        )
        reporter.finish()  # final summary line

    The reporter is invoked per text-delta with cumulative-text-so-far.
    Stateful: tracks which KSI IDs have already been reported so
    duplicate emissions in retried JSON don't double-print.
    """

    total_ksis: int
    stream: TextIO = field(default_factory=lambda: sys.stderr)
    seen_ksi_ids: set[str] = field(default_factory=set)
    seen_ksi_count: int = 0
    last_heartbeat_at: float = 0.0
    started_at: float = field(default_factory=time.monotonic)
    heartbeat_frame: int = 0
    # When set, the heartbeat line is prefixed with this label — used by the
    # retry layer (v0.1.141 / #346) to surface "Retry 2/3" during retries
    # so the user understands why the previous burst of per-KSI lines didn't
    # repeat. Cleared after the first per-KSI line of the next attempt prints.
    attempt_label: str = ""

    def __call__(self, cumulative_text: str) -> None:
        """Stream-progress callback. Idempotent on re-emitted text."""
        # Walk every KSI-ID match in the cumulative text. Set semantics
        # mean re-emitting the same delta (or the same KSI on a retry)
        # doesn't double-print.
        new_ids: list[str] = []
        for match in _KSI_ID_PATTERN.finditer(cumulative_text):
            ksi_id = match.group(1)
            if ksi_id not in self.seen_ksi_ids:
                self.seen_ksi_ids.add(ksi_id)
                new_ids.append(ksi_id)

        for ksi_id in new_ids:
            self.seen_ksi_count += 1
            self._emit(f"[gap] classifying KSI {self.seen_ksi_count}/{self.total_ksis}: {ksi_id}")
            # Once real per-KSI progress is flowing, drop the attempt label —
            # the user can see things are happening.
            self.attempt_label = ""

        # Heartbeat path: if no KSI emitted yet OR we're between attempts
        # (reset_for_next_attempt cleared the seen set), print a "still
        # working" line periodically so the user sees the process is alive.
        if self.seen_ksi_count == 0:
            now = time.monotonic()
            if now - self.last_heartbeat_at >= _HEARTBEAT_INTERVAL_SECONDS:
                elapsed = int(now - self.started_at)
                spinner = _SPINNER_FRAMES[self.heartbeat_frame % len(_SPINNER_FRAMES)]
                self.heartbeat_frame += 1
                label = self.attempt_label or "Analyzing KSIs against your scan evidence"
                self._emit(f"[gap] {spinner} {label}... ({elapsed}s)")
                self.last_heartbeat_at = now

    def reset_for_next_attempt(self, attempt_label: str) -> None:
        """Reset per-attempt state before a retry call.

        Without this, attempt 2's same 60 KSI IDs hit the dedup set from
        attempt 1 and emit nothing — the user sees silence during the entire
        retry. After reset, the heartbeat fires again and per-KSI lines
        re-emit with re-numbered counts. The `attempt_label` ("Retry 2/3
        with stricter instructions" etc.) replaces the default heartbeat
        phrase so the user knows a retry is in flight (v0.1.141 / #346).
        """
        self.seen_ksi_ids = set()
        self.seen_ksi_count = 0
        self.last_heartbeat_at = 0.0
        self.started_at = time.monotonic()
        self.attempt_label = attempt_label

    def finish(self) -> None:
        """Final summary after the run completes."""
        elapsed = time.monotonic() - self.started_at
        if self.seen_ksi_count > 0:
            self._emit(
                f"[gap] done in {elapsed:.1f}s — "
                f"{self.seen_ksi_count}/{self.total_ksis} KSIs classified"
            )

    def _emit(self, line: str) -> None:
        print(line, file=self.stream, flush=True)


def make_reporter_if_tty(total_ksis: int) -> GapProgressReporter | None:
    """Return a GapProgressReporter only when stderr is a TTY.

    CI runs (where stderr is piped to a log file) get None — the
    progress lines would just clutter logs without giving any
    interactive value. Local terminal runs get the live reporter.

    Returns the concrete reporter class (not the abstract callable
    type) so callers can invoke `.finish()` after the agent run.
    GapProgressReporter is itself a `Callable[[str], None]` via its
    `__call__`, so it satisfies `LLMClient.on_chunk` directly.
    """
    if not sys.stderr.isatty():
        return None
    return GapProgressReporter(total_ksis=total_ksis, stream=sys.stderr)
