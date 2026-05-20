from __future__ import annotations

import math
import time
from typing import ClassVar

from textual.message import Message

from drydock.cli.textual_ui.widgets.spinner import SpinnerType
from drydock.cli.textual_ui.widgets.status_message import StatusMessage
from drydock.core.utils import compact_reduction_display

_BAR_WIDTH = 40
_BAR_FULL = "▰"
_BAR_EMPTY = "▱"
# Compaction is a single LLM call; we don't get real progress signal
# from the model. Instead show an asymptotic time-based estimate that
# climbs fast then slows, capped below 100% so we never claim done
# before CompactEndEvent arrives. Gemma 4 compactions typically take
# 30-180s; tau=60s reaches ~95% at 3*tau = 180s.
_TAU_SEC = 60.0
_MAX_PROGRESS = 0.95


def _fmt_tokens(n: int) -> str:
    if n < 1000:
        return f"{n}"
    if n < 100_000:
        return f"{n / 1000:.1f}k"
    return f"{round(n / 1000)}k"


def _fmt_elapsed(secs: float) -> str:
    m, s = divmod(int(secs), 60)
    if m == 0:
        return f"{s}s"
    return f"{m}m {s}s"


class CompactMessage(StatusMessage):
    SPINNER_TYPE: ClassVar[SpinnerType] = SpinnerType.BRAILLE

    class Completed(Message):
        def __init__(self, compact_widget: CompactMessage) -> None:
            super().__init__()
            self.compact_widget = compact_widget

    def __init__(self, input_tokens: int | None = None) -> None:
        super().__init__()
        self.add_class("compact-message")
        self.old_tokens: int | None = None
        self.new_tokens: int | None = None
        self.error_message: str | None = None
        self.input_tokens: int | None = input_tokens
        self._start_time: float = time.monotonic()

    def _progress_line(self) -> str:
        elapsed = max(0.0, time.monotonic() - self._start_time)
        frac = _MAX_PROGRESS * (1.0 - math.exp(-elapsed / _TAU_SEC))
        filled = max(0, min(_BAR_WIDTH, int(round(frac * _BAR_WIDTH))))
        bar = _BAR_FULL * filled + _BAR_EMPTY * (_BAR_WIDTH - filled)
        return f"{bar} {int(frac * 100)}%"

    def get_content(self) -> str:
        if self._is_spinning:
            elapsed = max(0.0, time.monotonic() - self._start_time)
            parts = [f"Compacting conversation… ({_fmt_elapsed(elapsed)}"]
            if self.input_tokens:
                parts.append(f"↑ {_fmt_tokens(self.input_tokens)} tokens")
            header = " · ".join(parts) + ")"
            return f"{header}\n{self._progress_line()}"

        if self.error_message:
            return f"Error: {self.error_message}"

        return compact_reduction_display(self.old_tokens, self.new_tokens)

    def set_complete(
        self, old_tokens: int | None = None, new_tokens: int | None = None
    ) -> None:
        self.old_tokens = old_tokens
        self.new_tokens = new_tokens
        self.stop_spinning(success=True)
        self.post_message(self.Completed(self))

    def set_error(self, error_message: str) -> None:
        self.error_message = error_message
        self.stop_spinning(success=False)
