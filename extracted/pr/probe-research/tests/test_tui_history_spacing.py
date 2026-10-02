"""History choices keep their borders and yield extra spacing on small screens."""

import pytest

from probe.cli import backfill_transcripts as bt, tui
from tests.test_tui_review import _run

pytestmark = pytest.mark.tui


def test_empty_history_selection_can_skip_but_cannot_start_an_import(monkeypatch):
    answer, frames = _run(
        monkeypatch, ["i", "\x1b[C", "\x13"],
        render=lambda: bt.choose_sources((bt.CLAUDE, bt.CODEX)),
    )
    assert answer is tui.SKIP
    assert "Choose a history, or Skip sessions." in "\n".join(frames[-1])


