"""TransportObserver: what hears about each request. Transport reports to it instead of
importing diagnostics, a layer above; the SDK client hands diagnostics down at import."""

from __future__ import annotations

import importlib
from typing import Protocol


class TransportObserver(Protocol):
    """Hears about each request: its start, its end, and how it went (diagnostics' ring buffer)."""

    def begin_transport(self, method: str, path: str, *, base: str | None = None) -> None: ...

    def end_transport(self) -> None: ...

    def record_transport(
        self, method: str, path: str, *, seconds: float, status: int | None = None,
        error: str | None = None, base: str | None = None,
    ) -> None: ...


#: Who hears about requests unless told otherwise: the crash reports' ring buffer. The SDK client
#: hands it down at import; a process with only a Transport loads it on its first request.
DEFAULT_OBSERVER = "probe.sdk.diagnostics"
_observer: TransportObserver | None = None


def observe_with(observer: TransportObserver | None) -> None:
    """Report every request to ``observer``; None goes back to the default."""
    global _observer
    _observer = observer


def observer() -> TransportObserver:
    """The current observer, the default loaded on first use."""
    global _observer
    if _observer is None:
        _observer = importlib.import_module(DEFAULT_OBSERVER)
    return _observer
