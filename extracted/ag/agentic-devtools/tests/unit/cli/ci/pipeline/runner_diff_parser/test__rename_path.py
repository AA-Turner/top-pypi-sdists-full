"""Tests for rename metadata path parsing."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _rename_path


def test_parses_rename_source_and_destination() -> None:
    assert _rename_path("rename from old.py") == ("rename from ", "old.py")
    assert _rename_path("rename to new.py") == ("rename to ", "new.py")


def test_rejects_malformed_rename_path() -> None:
    assert _rename_path('rename from "unfinished') is None
