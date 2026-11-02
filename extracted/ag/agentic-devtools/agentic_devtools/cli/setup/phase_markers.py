"""Stable phase markers delineating the two observable phases of ``agdt-setup``.

``agdt-setup`` first *generates* the managed repository artifacts (including
``setup-dev-tools.py``) and then, when auto-run is enabled, *executes* that
generated script as a child process. Both humans and log parsers need to know
which phase produced a given line of output, so the markers defined here are
printed verbatim to stdout around each phase.

The ``execution:*`` markers are emitted only when the generated script is
actually invoked — they are absent whenever auto-run is skipped.
"""

from __future__ import annotations

MARKER_PREFIX = "AGDT_SETUP_PHASE:"

GENERATION_START = f"{MARKER_PREFIX} generation:start"
GENERATION_END = f"{MARKER_PREFIX} generation:end"
EXECUTION_START = f"{MARKER_PREFIX} execution:start"
EXECUTION_END = f"{MARKER_PREFIX} execution:end"


def emit_phase_marker(marker: str) -> None:
    """Print *marker* verbatim to stdout.

    stdout is flushed immediately so the marker keeps its position relative to
    the output of the auto-run child process, which inherits the parent's
    stdout and therefore writes independently of the parent's buffer.
    """
    print(marker, flush=True)


class PhaseMarkerEmitter:
    """Emit each phase marker at most once.

    Callers can therefore place idempotent "safety net" emissions on paths that
    may or may not have already emitted a marker (for example a ``finally``
    block covering early exits) without risking duplicate markers.
    """

    def __init__(self) -> None:
        self._emitted: set[str] = set()

    def emit(self, marker: str) -> None:
        """Emit *marker* unless this instance already emitted it."""
        if marker in self._emitted:
            return
        self._emitted.add(marker)
        emit_phase_marker(marker)
