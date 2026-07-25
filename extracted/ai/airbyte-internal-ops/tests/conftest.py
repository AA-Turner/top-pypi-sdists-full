# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Global safety guards for the test suite."""

from __future__ import annotations

import pytest
import requests

from airbyte_ops_mcp import slack_posting
from airbyte_ops_mcp.mcp import human_in_the_loop


@pytest.fixture(autouse=True)
def prevent_outbound_notifications(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail loudly if a test attempts an outbound Slack or HITL notification."""

    def fail(message: str) -> None:
        raise AssertionError(f"Outbound notification attempted during tests: {message}")

    monkeypatch.setattr(
        slack_posting,
        "fetch_roster",
        lambda *_args, **_kwargs: fail("Slack roster lookup"),
    )
    monkeypatch.setattr(
        slack_posting,
        "_post_message",
        lambda *_args, **_kwargs: fail("Slack message post"),
    )
    monkeypatch.setattr(
        human_in_the_loop,
        "dispatch_escalation",
        lambda *_args, **_kwargs: fail("HITL escalation dispatch"),
    )
    monkeypatch.setattr(
        requests.sessions.Session,
        "request",
        lambda *_args, **_kwargs: fail("HTTP request"),
    )
