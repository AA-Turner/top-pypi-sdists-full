"""Tests for SDK world Slack completion notifications."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest

from plato.chronos.models import SessionResponse, SessionWorldInfo, UserInfo
from plato.worlds import (
    BaseWorld,
    DevConfig,
    Observation,
    RunConfig,
    SessionConfig,
    SlackNotificationConfig,
    StepResult,
)
from plato.worlds.slack import _build_completion_message, send_slack_world_completion_notification


class _DummyWorld(BaseWorld[RunConfig]):
    name = "dummy-world"

    async def reset(self) -> Observation:
        return Observation()

    async def step(self) -> StepResult:
        return StepResult(observation=Observation(), done=True)


class _FakeChronosSession:
    def __init__(self, details: SessionResponse):
        self._details = details

    async def get_details(self) -> SessionResponse:
        return self._details


class _FakeChronos:
    def __init__(self, details: SessionResponse):
        self._details = details

    async def __aenter__(self) -> _FakeChronos:
        return self

    async def __aexit__(self, *args) -> None:
        return None

    async def get_session(self, session_id: str) -> _FakeChronosSession:
        return _FakeChronosSession(self._details)


class _FakeResponse:
    def __init__(self, payload: dict, *, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code
        self.text = str(payload)

    @property
    def is_success(self) -> bool:
        return self.status_code < 400

    def json(self) -> dict:
        return self._payload


class _FakeSlackClient:
    def __init__(self):
        self.posts: list[dict] = []

    async def __aenter__(self) -> _FakeSlackClient:
        return self

    async def __aexit__(self, *args) -> None:
        return None

    async def get(self, url: str, *, params: dict, headers: dict) -> _FakeResponse:
        assert params["email"] == "alice@example.com"
        return _FakeResponse({"ok": True, "user": {"id": "U123"}})

    async def post(self, url: str, *, json: dict, headers: dict) -> _FakeResponse:
        self.posts.append({"url": url, "json": json, "headers": headers})
        return _FakeResponse({"ok": True})


def _session_details() -> SessionResponse:
    return SessionResponse(
        public_id="chronos-123",
        status="completed",
        created_at=datetime.now(UTC),
        ended_at=datetime.now(UTC),
        logs_url="https://chronos.example/logs/chronos-123",
        world=SessionWorldInfo(
            name="dummy-world",
            package_name="plato-world-dummy",
            version="1.2.3",
        ),
        created_by=UserInfo(
            id="user-1",
            name="Alice",
            email="alice@example.com",
        ),
    )


def test_run_config_slack_notifications_default_to_disabled() -> None:
    """Slack notifications should stay opt-in."""
    config = RunConfig()
    assert config.slack_notifications.enabled is False


def test_build_completion_message_includes_error_and_logs() -> None:
    """Slack message should include the creator ref, logs URL, and error details."""
    text = _build_completion_message(
        creator_ref="<@U123>",
        details=_session_details(),
        world_name="dummy-world",
        world_version="1.2.3",
        status="failed",
        error_message="RuntimeError: boom",
        step_count=7,
    )

    assert "<@U123> world session `chronos-123` finished." in text
    assert "*Logs:* https://chronos.example/logs/chronos-123" in text
    assert "RuntimeError: boom" in text


@pytest.mark.asyncio
async def test_send_slack_world_completion_notification_posts_creator_mention(monkeypatch) -> None:
    """Notifier should resolve the creator by email and mention them in Slack."""
    fake_client = _FakeSlackClient()

    monkeypatch.setattr(
        "plato.worlds.slack.AsyncChronos",
        lambda api_key, base_url: _FakeChronos(_session_details()),
    )
    monkeypatch.setattr("plato.worlds.slack.httpx.AsyncClient", lambda timeout=15.0: fake_client)
    monkeypatch.setenv("PLATO_API_KEY", "plato-key")
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test")

    await send_slack_world_completion_notification(
        config=SlackNotificationConfig(enabled=True, channel_id="C123"),
        session=SessionConfig(session_id="chronos-123", chronos_url="https://chronos.example"),
        world_name="dummy-world",
        world_version="1.2.3",
        status="failed",
        error_message="RuntimeError: boom",
        step_count=4,
    )

    assert len(fake_client.posts) == 1
    posted = fake_client.posts[0]["json"]
    assert posted["channel"] == "C123"
    assert "<@U123> world session `chronos-123` finished." in posted["text"]
    assert "RuntimeError: boom" in posted["text"]


@pytest.mark.asyncio
async def test_finalize_skips_slack_notifications_in_dev_mode(monkeypatch) -> None:
    """BaseWorld finalization should never emit Slack notifications in dev mode."""
    world = _DummyWorld()
    world.config = RunConfig(slack_notifications=SlackNotificationConfig(enabled=True, channel_id="C123"))
    world.session = SessionConfig(session_id="chronos-123", chronos_url="https://chronos.example")
    world.dev = DevConfig(world=Path("/tmp/dev-world"))

    notify = AsyncMock()
    monkeypatch.setattr("plato.worlds.base.send_slack_world_completion_notification", notify)
    monkeypatch.setattr("plato.worlds.base.shutdown_metrics", AsyncMock())
    monkeypatch.setattr("plato.worlds.base.shutdown_tracing", Mock())
    world._complete_chronos_session = AsyncMock()
    monkeypatch.setenv("PLATO_WORLD_DEV_MODE", "1")

    await world._finalize(None)

    notify.assert_not_awaited()
    world._complete_chronos_session.assert_not_awaited()


def test_chronos_dev_runner_sets_world_dev_mode_flag() -> None:
    """Chronos dev runner should mark the remote world process as actual dev mode."""
    runner_path = Path("/Users/pranavputta/Github/plato-client/python-sdk/plato/cli/chronos/dev/runner.py")
    content = runner_path.read_text()
    assert "PLATO_WORLD_DEV_MODE='1'" in content


@pytest.mark.asyncio
async def test_finalize_sends_failure_message_when_world_errors(monkeypatch) -> None:
    """BaseWorld finalization should pass failed status and error text to the notifier."""
    world = _DummyWorld()
    world.config = RunConfig(slack_notifications=SlackNotificationConfig(enabled=True, channel_id="C123"))
    world.session = SessionConfig(session_id="chronos-123", chronos_url="https://chronos.example")
    world.dev = DevConfig()

    notify = AsyncMock()
    monkeypatch.setattr("plato.worlds.base.send_slack_world_completion_notification", notify)
    monkeypatch.setattr("plato.worlds.base.shutdown_metrics", AsyncMock())
    monkeypatch.setattr("plato.worlds.base.shutdown_tracing", Mock())
    world._complete_chronos_session = AsyncMock()

    with pytest.raises(RuntimeError, match="boom"):
        await world._finalize(RuntimeError("boom"))

    notify.assert_awaited_once()
    kwargs = notify.await_args.kwargs
    assert kwargs["status"] == "failed"
    assert kwargs["error_message"] == "RuntimeError: boom"
