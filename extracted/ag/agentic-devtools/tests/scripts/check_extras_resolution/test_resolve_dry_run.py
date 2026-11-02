"""Tests for check_extras_resolution.resolve_dry_run."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

import pytest

from tests.scripts.check_extras_resolution import checker


def test_resolve_dry_run_parses_successful_output():
    """A zero exit code returns the parsed {name: version} mapping."""
    completed = subprocess.CompletedProcess(
        args=["uv"], returncode=0, stdout="", stderr=" + requests==2.31.0\n + langgraph==1.2.11\n"
    )
    with patch("subprocess.run", return_value=completed):
        result = checker.resolve_dry_run(".", "/tmp/venv/bin/python")

    assert result == {"requests": "2.31.0", "langgraph": "1.2.11"}


def test_resolve_dry_run_raises_on_nonzero_exit():
    """A non-zero exit code raises RuntimeError including the requirement and output."""
    completed = subprocess.CompletedProcess(args=["uv"], returncode=1, stdout="", stderr="No solution found")
    with patch("subprocess.run", return_value=completed):
        with pytest.raises(RuntimeError, match="No solution found"):
            checker.resolve_dry_run(".[browser]", "/tmp/venv/bin/python")


def test_resolve_dry_run_raises_when_no_packages_parsed():
    """A zero exit code with unrecognised output raises RuntimeError (fail-closed guard)."""
    completed = subprocess.CompletedProcess(
        args=["uv"], returncode=0, stdout="Some unexpected output format\n", stderr=""
    )
    with patch("subprocess.run", return_value=completed):
        with pytest.raises(RuntimeError, match="no packages could be parsed"):
            checker.resolve_dry_run(".", "/tmp/venv/bin/python")
