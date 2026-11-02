"""Tests for PhaseMarkerEmitter."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.setup.phase_markers import (
    GENERATION_END,
    GENERATION_START,
    PhaseMarkerEmitter,
)


class TestPhaseMarkerEmitter:
    """Tests for PhaseMarkerEmitter."""

    def test_emits_marker_once(self, capsys: pytest.CaptureFixture[str]) -> None:
        """The first emit of a marker writes it to stdout."""
        emitter = PhaseMarkerEmitter()

        emitter.emit(GENERATION_START)

        assert capsys.readouterr().out == f"{GENERATION_START}\n"

    def test_repeated_emit_is_suppressed(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Emitting the same marker again is a no-op (idempotent safety nets)."""
        emitter = PhaseMarkerEmitter()

        emitter.emit(GENERATION_END)
        emitter.emit(GENERATION_END)

        assert capsys.readouterr().out == f"{GENERATION_END}\n"

    def test_distinct_markers_are_all_emitted(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Dedup is per marker, not global."""
        emitter = PhaseMarkerEmitter()

        emitter.emit(GENERATION_START)
        emitter.emit(GENERATION_END)

        assert capsys.readouterr().out == f"{GENERATION_START}\n{GENERATION_END}\n"

    def test_instances_track_markers_independently(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Each emitter has its own emitted-marker set."""
        first = PhaseMarkerEmitter()
        second = PhaseMarkerEmitter()

        first.emit(GENERATION_START)
        second.emit(GENERATION_START)

        assert capsys.readouterr().out == f"{GENERATION_START}\n{GENERATION_START}\n"
