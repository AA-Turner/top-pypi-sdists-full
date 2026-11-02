"""Tests for matching Git path pairs against the expected inventory."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _matching_path_pair


def test_selects_the_inventory_path_pair() -> None:
    lines = ["diff --git a/file.py b/file.py"]

    assert _matching_path_pair("a/file.py b/file.py", lines, 0, {"file.py"}) == ("a/file.py", "b/file.py")


def test_rejects_pairs_outside_the_inventory() -> None:
    lines = ["diff --git a/file.py b/file.py"]

    assert _matching_path_pair("a/file.py b/file.py", lines, 0, {"other.py"}) is None
