# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for paused-rollout investigation sessions."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest
import requests

from airbyte_ops_mcp import devin_api
from airbyte_ops_mcp.connector_ops.rollouts import paused_report
from airbyte_ops_mcp.connector_ops.rollouts._helpers import HealthGateResult
from airbyte_ops_mcp.connector_ops.rollouts.models import ConnectorRolloutRecord
from airbyte_ops_mcp.slack_posting import SlackPostResult

SESSION_ID = "0123456789abcdef0123456789abcdef"
SESSION_URL = f"https://app.devin.ai/sessions/{SESSION_ID}"
GATE_REASON = "30 of 584 connectors failing (5.1% >= 5%, floor=2)"
THREAD = SlackPostResult(channel_id="C0HITL", ts="1789000000.123456")
ROLLOUT_ID = "rollout-1"
EXPECTED_TAGS = ["rollout-autopilot", "paused-rollout-report", f"rollout:{ROLLOUT_ID}"]


def _rollout() -> ConnectorRolloutRecord:
    return ConnectorRolloutRecord(
        rollout_id=ROLLOUT_ID,
        actor_definition_id="actor-def-1",
        state="in_progress",
        current_target_rollout_pct=50,
        rc_docker_image_tag="1.2.3",
        rc_docker_repository="airbyte/source-test",
        initial_docker_image_tag="1.2.2",
        tier="TIER_2",
    )


def _gate() -> HealthGateResult:
    return HealthGateResult(
        passed=False,
        reason=GATE_REASON,
        failure_count=30,
        failed_actor_count=30,
        actors_with_sync_signal=584,
        failure_percent=30 / 584,
        should_rollback=True,
    )


@dataclass
class FakeDevinApi:
    """Records calls to the `devin_api` functions `paused_report` uses."""

    existing: list[devin_api.DevinSessionRef] = field(default_factory=list)
    fail: str | None = None
    list_calls: list[dict[str, object]] = field(default_factory=list)
    create_calls: list[dict[str, object]] = field(default_factory=list)
    unarchive_calls: list[str] = field(default_factory=list)
    messages: list[tuple[str, str]] = field(default_factory=list)

    def _maybe_fail(self, op: str) -> None:
        if self.fail == op:
            raise requests.ConnectionError(f"{op} failed")

    def list_sessions(
        self, *, tags: list[str], limit: int = 20
    ) -> list[devin_api.DevinSessionRef]:
        self._maybe_fail("list")
        self.list_calls.append({"tags": tags, "limit": limit})
        return list(self.existing)

    def create_session(
        self, prompt: str, **kwargs: object
    ) -> devin_api.DevinSessionRef:
        self._maybe_fail("create")
        self.create_calls.append({"prompt": prompt, **kwargs})
        return devin_api.DevinSessionRef(SESSION_ID, SESSION_URL, status="new")

    def unarchive_session(self, session_id: str) -> devin_api.DevinSessionRef:
        self._maybe_fail("unarchive")
        self.unarchive_calls.append(session_id)
        return devin_api.DevinSessionRef(session_id, SESSION_URL, status="exited")

    def send_session_message(self, session_id: str, message: str) -> None:
        self._maybe_fail("message")
        self.messages.append((session_id, message))


@pytest.fixture
def fake_api(monkeypatch: pytest.MonkeyPatch) -> FakeDevinApi:
    monkeypatch.setenv("DEVIN_AI_ADMIN_SERVICE_TOKEN", "test-token")
    monkeypatch.setenv("DEVIN_AI_ORG_ID", "test-org")
    fake = FakeDevinApi()
    for name in (
        "list_sessions",
        "create_session",
        "unarchive_session",
        "send_session_message",
    ):
        monkeypatch.setattr(devin_api, name, getattr(fake, name))
    return fake


@pytest.fixture
def no_devin_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in devin_api._TOKEN_ENV_VARS + devin_api._ORG_ID_ENV_VARS:
        monkeypatch.delenv(var, raising=False)


def test_rollout_tag() -> None:
    assert paused_report.rollout_tag("abc") == "rollout:abc"


def test_structured_output_schema_has_required_fields() -> None:
    schema = paused_report.STRUCTURED_OUTPUT_SCHEMA
    assert schema["required"] == ["summary", "groups", "recommendation", "caveats"]
    assert set(schema["properties"]) == set(schema["required"])


def test_build_investigation_prompt_with_thread() -> None:
    prompt = paused_report.build_investigation_prompt(
        _rollout(), "1.2.3", _gate(), THREAD
    )
    assert ROLLOUT_ID in prompt
    assert GATE_REASON in prompt
    assert "30 of 584 actors" in prompt
    assert f"thread_ts `{THREAD.ts}`" in prompt
    assert THREAD.channel_id in prompt
    assert THREAD.permalink in prompt
    assert "provide_structured_output" in prompt
    assert "lookup_customer_tiers" in prompt
    assert "escalate_to_human" in prompt
    assert "query_prod_failed_sync_attempts_for_connector" in prompt
    assert "default `TIER_2`" in prompt
    assert "Do NOT call `query_prod_actors_by_pinned_connector_version`" in prompt
    assert "Do NOT unpause, finalize, cancel, unpin" in prompt
    assert "Connector Version Manager" not in prompt
    assert "default to `lookback_days=7` and `limit=100`" in prompt
    assert "mark the affected groups incomplete" in prompt
    assert "`UNKNOWN` tier" in prompt
    assert "absence alone tells you" in prompt


def test_build_investigation_prompt_without_thread() -> None:
    prompt = paused_report.build_investigation_prompt(
        _rollout(), "1.2.3", _gate(), None
    )
    assert "no thread to reply in" in prompt
    assert "thread_ts" not in prompt


def test_build_repause_message() -> None:
    message = paused_report.build_repause_message(_rollout(), "1.2.3", _gate(), THREAD)
    assert "paused again" in message
    assert GATE_REASON in message
    assert f"thread_ts `{THREAD.ts}`" in message
    assert "provide_structured_output" in message
    assert "no rollout or pin mutations without HITL approval" in message


def _run() -> devin_api.DevinSessionRef | None:
    """Mirror AutoPilot: look the session up, then start or continue it."""
    lookup = paused_report.lookup_investigation_session(ROLLOUT_ID)
    return paused_report.start_investigation_session(
        _rollout(), "1.2.3", _gate(), THREAD, lookup
    )


def test_start_investigation_session_creates_when_none_tagged(
    fake_api: FakeDevinApi,
) -> None:
    ref = _run()
    assert ref is not None and ref.url == SESSION_URL
    assert fake_api.list_calls == [{"tags": [f"rollout:{ROLLOUT_ID}"], "limit": 5}]
    assert len(fake_api.create_calls) == 1
    created = fake_api.create_calls[0]
    assert created["tags"] == EXPECTED_TAGS
    assert created["max_acu_limit"] == paused_report.MAX_ACU_LIMIT
    assert created["structured_output_schema"] is paused_report.STRUCTURED_OUTPUT_SCHEMA
    assert "source-test 1.2.3" in str(created["title"])
    assert THREAD.ts in str(created["prompt"])
    assert fake_api.messages == []
    assert fake_api.unarchive_calls == []


@pytest.mark.parametrize(
    "archived",
    [pytest.param(False, id="live"), pytest.param(True, id="archived")],
)
def test_start_investigation_session_reuses_tagged_session(
    fake_api: FakeDevinApi, archived: bool
) -> None:
    fake_api.existing = [
        devin_api.DevinSessionRef(
            SESSION_ID, SESSION_URL, "exited", archived, tuple(EXPECTED_TAGS)
        )
    ]
    ref = _run()
    assert ref is not None and ref.session_id == SESSION_ID
    assert fake_api.create_calls == []
    assert fake_api.unarchive_calls == ([SESSION_ID] if archived else [])
    ((session_id, message),) = fake_api.messages
    assert session_id == SESSION_ID
    assert "paused again" in message
    assert THREAD.ts in message


def test_start_investigation_session_ignores_sessions_without_rollout_tag(
    fake_api: FakeDevinApi,
) -> None:
    fake_api.existing = [
        devin_api.DevinSessionRef(
            "f" * 32, SESSION_URL, "running", False, ("rollout-autopilot",)
        )
    ]
    _run()
    assert len(fake_api.create_calls) == 1
    assert fake_api.messages == []


def test_start_investigation_session_skips_without_devin_config(
    no_devin_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        devin_api,
        "list_sessions",
        lambda **_: pytest.fail("must not call the API without credentials"),
    )
    assert _run() is None


@pytest.mark.parametrize(
    "fail,existing",
    [
        pytest.param("list", [], id="list_fails"),
        pytest.param("create", [], id="create_fails"),
        pytest.param(
            "unarchive",
            [
                devin_api.DevinSessionRef(
                    SESSION_ID, SESSION_URL, "exited", True, tuple(EXPECTED_TAGS)
                )
            ],
            id="unarchive_fails",
        ),
        pytest.param(
            "message",
            [
                devin_api.DevinSessionRef(
                    SESSION_ID, SESSION_URL, "running", False, tuple(EXPECTED_TAGS)
                )
            ],
            id="message_fails",
        ),
    ],
)
def test_start_investigation_session_swallows_api_errors(
    fake_api: FakeDevinApi,
    fail: str,
    existing: list[devin_api.DevinSessionRef],
) -> None:
    fake_api.fail = fail
    fake_api.existing = existing
    assert _run() is None
