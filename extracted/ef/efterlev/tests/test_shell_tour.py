"""Tests for `efterlev.shell.tour` — guided walkthrough for new users."""

from __future__ import annotations

from pathlib import Path

from efterlev.shell.tour import (
    TOUR_STEPS,
    _document_done,
    _gap_done,
    _init_done,
    _poam_done,
    _scan_done,
)


def test_tour_has_five_steps() -> None:
    """The pipeline is init → scan → gap → document → poam — five steps."""
    assert len(TOUR_STEPS) == 5


def test_tour_steps_are_numbered_consecutively() -> None:
    for i, step in enumerate(TOUR_STEPS, start=1):
        assert step.number == i


def test_tour_steps_map_to_real_commands() -> None:
    """Every TourStep.handler_name must exist in the shell command registry."""
    from efterlev.shell.commands import find_command

    for step in TOUR_STEPS:
        assert find_command(step.handler_name) is not None, (
            f"step {step.number} references unknown command {step.handler_name!r}"
        )


def test_tour_steps_have_what_and_why_paragraphs() -> None:
    """The walkthrough's value is the explanation; assert both fields are non-trivial."""
    for step in TOUR_STEPS:
        assert len(step.what) > 60, f"step {step.number} 'what' too short"
        assert len(step.why) > 40, f"step {step.number} 'why' too short"


def test_init_done_detects_efterlev_directory(tmp_path: Path) -> None:
    assert _init_done(tmp_path) is False
    (tmp_path / ".efterlev").mkdir()
    assert _init_done(tmp_path) is True


def test_scan_done_returns_false_when_no_store(tmp_path: Path) -> None:
    assert _scan_done(tmp_path) is False


def test_gap_done_returns_false_when_no_store(tmp_path: Path) -> None:
    assert _gap_done(tmp_path) is False


def test_document_done_returns_false_when_no_attestation(tmp_path: Path) -> None:
    (tmp_path / ".efterlev").mkdir()
    assert _document_done(tmp_path) is False


def test_poam_done_returns_false_when_no_poam(tmp_path: Path) -> None:
    (tmp_path / ".efterlev").mkdir()
    assert _poam_done(tmp_path) is False
