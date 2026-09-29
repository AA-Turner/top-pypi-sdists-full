# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the Zendesk webhook handler."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from typing import Any
from unittest.mock import MagicMock, patch

from agent_message_bus.zendesk_handler import (
    ZENDESK_RESOLUTION_PLAYBOOK_ID,
    ZENDESK_TRIAGE_PLAYBOOK_ID,
    ZendeskAction,
    extract_ticket_data,
    handle_zendesk_webhook,
    verify_zendesk_signature,
)


def _session_response() -> MagicMock:
    response = MagicMock()
    response.ok = True
    response.json.return_value = {
        "session_id": "sess-123",
        "url": "https://app.devin.ai/sessions/sess-123",
    }
    return response


def _trigger_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "ticket_id": "19403",
        "subject": "Sync failing",
        "status": "Solved",
        "latest_comment": "Thanks, that fixed it!",
    }
    payload.update(overrides)
    return payload


def _run_webhook(payload: dict[str, Any]) -> tuple[Any, MagicMock]:
    with (
        patch(
            "agent_message_bus.zendesk_handler._get_devin_api_key",
            return_value="key",
        ),
        patch(
            "agent_message_bus.zendesk_handler._get_devin_org_id",
            return_value="org",
        ),
        patch(
            "agent_message_bus.zendesk_handler.requests.post",
            return_value=_session_response(),
        ) as post,
    ):
        return handle_zendesk_webhook(payload), post


def test_event_subscription_payload_extracts_ticket() -> None:
    payload = {
        "type": "zen:event-type:ticket.created",
        "id": "01JABCDEF",
        "subject": "zen:ticket:19499",
        "detail": {
            "id": "19499",
            "subject": "Cannot connect source",
            "description": "Source fails on check",
            "status": "new",
        },
        "event": {},
    }

    ticket = extract_ticket_data(payload)

    assert ticket is not None
    assert ticket.ticket_id == "19499"
    assert ticket.subject == "Cannot connect source"
    assert ticket.status == "new"
    assert ticket.action == ZendeskAction.triage
    assert ticket.comments == ["Source fails on check"]


def test_trigger_subject_with_zen_ticket_prefix_still_uses_ticket_id() -> None:
    # A trigger payload whose subject happens to start with `zen:ticket:`
    # must still be treated as a trigger payload (honoring action/ticket_id),
    # not as an event-subscription payload.
    payload = _trigger_payload(action="resolution", ticket_id=19403, subject="zen:ticket:42")

    ticket = extract_ticket_data(payload)

    assert ticket is not None
    assert ticket.ticket_id == "19403"
    assert ticket.action == ZendeskAction.resolution


def test_resolution_action_routes_to_resolution_playbook() -> None:
    result, post = _run_webhook(_trigger_payload(action="resolution", ticket_id=19403))

    assert result.status == "ok"
    assert result.action == "resolution"
    assert result.ticket_id == "19403"
    post.assert_called_once()
    body = post.call_args.kwargs["json"]
    assert body["playbook_id"] == ZENDESK_RESOLUTION_PLAYBOOK_ID
    assert body["tags"] == ["zendesk-resolution"]
    assert body["prompt"].startswith("Run the MoonBot Resolution playbook")
    assert "Status: Solved" in body["prompt"]
    assert "Thanks, that fixed it!" in body["prompt"]


def _zendesk_env(**overrides: str) -> dict[str, str]:
    env = {
        "ZENDESK_SUBDOMAIN": "airbyte1416",
        "ZENDESK_EMAIL": "support.ops@airbyte.io",
        "ZENDESK_API_TOKEN": "zd-token",
    }
    env.update(overrides)
    return env


def test_resolution_session_secrets_injected() -> None:
    with patch.dict("os.environ", _zendesk_env(), clear=False):
        result, post = _run_webhook(_trigger_payload(action="resolution"))

    assert result.status == "ok"
    body = post.call_args.kwargs["json"]
    assert body["session_secrets"] == [
        {"key": "ZENDESK_SUBDOMAIN", "value": "airbyte1416", "sensitive": False},
        {"key": "ZENDESK_EMAIL", "value": "support.ops@airbyte.io", "sensitive": False},
        {"key": "ZENDESK_API_TOKEN", "value": "zd-token", "sensitive": True},
    ]


def test_resolution_without_token_sends_no_session_secrets() -> None:
    with patch.dict("os.environ", _zendesk_env(ZENDESK_API_TOKEN=""), clear=False):
        result, post = _run_webhook(_trigger_payload(action="resolution"))

    assert result.status == "ok"
    body = post.call_args.kwargs["json"]
    assert "session_secrets" not in body


def test_triage_never_sends_session_secrets() -> None:
    with patch.dict("os.environ", _zendesk_env(), clear=False):
        result, post = _run_webhook(_trigger_payload())

    assert result.status == "ok"
    body = post.call_args.kwargs["json"]
    assert "session_secrets" not in body


def test_missing_action_defaults_to_triage() -> None:
    payload = _trigger_payload()
    del payload["status"]

    result, post = _run_webhook(payload)

    assert result.status == "ok"
    assert result.action == "triage"
    body = post.call_args.kwargs["json"]
    assert body["playbook_id"] == ZENDESK_TRIAGE_PLAYBOOK_ID
    assert body["tags"] == ["zendesk-triage"]
    assert "zendesk_triage" in body["prompt"]


def test_unknown_action_is_skipped() -> None:
    result, post = _run_webhook(_trigger_payload(action="explode"))

    assert result.status == "skipped"
    assert result.reason == "unknown_action"
    post.assert_not_called()


def _sign(body: bytes, timestamp: str, secret: str) -> str:
    return base64.b64encode(
        hmac.new(secret.encode(), timestamp.encode() + body, hashlib.sha256).digest()
    ).decode()


def test_signature_accepts_second_secret() -> None:
    body = json.dumps({"ticket_id": "1"}).encode()
    ts = datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")
    sig = _sign(body, ts, "secret-b")

    assert verify_zendesk_signature(body, sig, ts, ["secret-a", "secret-b"]) is True


def test_signature_rejects_when_no_secret_matches() -> None:
    body = json.dumps({"ticket_id": "1"}).encode()
    ts = datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")
    sig = _sign(body, ts, "secret-c")

    assert verify_zendesk_signature(body, sig, ts, ["secret-a", "secret-b"]) is False


def test_signature_rejects_stale_timestamp() -> None:
    body = json.dumps({"ticket_id": "1"}).encode()
    ts = (datetime.now(tz=timezone.utc) - timedelta(minutes=10)).isoformat().replace("+00:00", "Z")
    sig = _sign(body, ts, "secret-a")

    assert verify_zendesk_signature(body, sig, ts, ["secret-a"]) is False
