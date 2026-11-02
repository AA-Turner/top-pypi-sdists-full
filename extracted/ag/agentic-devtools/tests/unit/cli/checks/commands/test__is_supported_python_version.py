"""Tests for Python version support detection."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.checks.commands import _is_supported_python_version


@pytest.mark.parametrize(
    ("version_info", "expected"),
    [
        ((3, 13), False),
        ((3, 14), True),
        ((3, 15), True),
    ],
)
def test_is_supported_python_version(version_info: tuple[int, ...], expected: bool):
    assert _is_supported_python_version(version_info) is expected
