"""Tests for provider-neutral pull-request comment command."""

from __future__ import annotations

import pytest

from agentic_devtools.cli import pull_request_comments as commands


def test_as_int_and_provider_validation() -> None:
    assert commands._as_int(None, "id") is None
    assert commands._as_int("", "id") is None
    assert commands._as_int("4", "id") == 4
    with pytest.raises(ValueError, match="positive"):
        commands._as_int(True, "id")
    with pytest.raises(ValueError, match="positive"):
        commands._as_int("bad", "id")
    with pytest.raises(ValueError, match="positive"):
        commands._as_int(0, "id")
