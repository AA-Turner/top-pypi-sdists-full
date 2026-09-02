"""Tests for emit_phase_marker."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.phase_markers import (
    EXECUTION_END,
    EXECUTION_START,
    GENERATION_END,
    GENERATION_START,
    emit_phase_marker,
)


class TestPhaseMarkerConstants:
    """The literal marker strings are part of the public output contract (FR-008)."""

    def test_marker_literals_match_contract(self) -> None:
        """Markers are emitted verbatim as specified by the output contract."""
        assert GENERATION_START == "AGDT_SETUP_PHASE: generation:start"
        assert GENERATION_END == "AGDT_SETUP_PHASE: generation:end"
        assert EXECUTION_START == "AGDT_SETUP_PHASE: execution:start"
        assert EXECUTION_END == "AGDT_SETUP_PHASE: execution:end"


class TestEmitPhaseMarker:
    """Tests for emit_phase_marker."""

    def test_writes_marker_verbatim_to_stdout(self, capsys: pytest.CaptureFixture[str]) -> None:
        """The marker is printed to stdout on a line of its own."""
        emit_phase_marker(GENERATION_START)

        captured = capsys.readouterr()
        assert captured.out == f"{GENERATION_START}\n"
        assert captured.err == ""

    def test_flushes_stdout_immediately(self) -> None:
        """stdout is flushed so markers stay ordered against child-process output."""
        with patch("builtins.print") as mock_print:
            emit_phase_marker(EXECUTION_START)

        mock_print.assert_called_once_with(EXECUTION_START, flush=True)
