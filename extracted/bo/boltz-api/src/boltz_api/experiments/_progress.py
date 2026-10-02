from __future__ import annotations

import sys
import time
from typing_extensions import override


class ProgressSink:
    def info(self, message: str) -> None:
        raise NotImplementedError

    def maybe_running_summary(self, message: str, *, interval_seconds: float = 30.0) -> None:
        raise NotImplementedError


class StdoutProgressSink(ProgressSink):
    def __init__(self) -> None:
        self._last_running_summary_at = 0.0

    @override
    def info(self, message: str) -> None:
        sys.stdout.write(f"{message}\n")
        sys.stdout.flush()

    @override
    def maybe_running_summary(self, message: str, *, interval_seconds: float = 30.0) -> None:
        now = time.monotonic()
        if now - self._last_running_summary_at < interval_seconds:
            return
        self._last_running_summary_at = now
        self.info(message)


class NullProgressSink(ProgressSink):
    @override
    def info(self, message: str) -> None:
        del message
        return None

    @override
    def maybe_running_summary(self, message: str, *, interval_seconds: float = 30.0) -> None:
        del message
        del interval_seconds
        return None


def build_progress_sink(*, quiet: bool) -> ProgressSink:
    if quiet:
        return NullProgressSink()
    return StdoutProgressSink()
