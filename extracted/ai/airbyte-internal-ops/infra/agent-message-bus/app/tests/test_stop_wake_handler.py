# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for Devin Stop hook wake processing."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, call, patch

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

import agent_message_bus.app as app_module
import agent_message_bus.github_app as github_app
import agent_message_bus.stop_wake_handler as stop_wake_handler
from agent_message_bus.models import DevinStopEvent


def _event(prompt_id: str = "prompt-1") -> DevinStopEvent:
    return DevinStopEvent(
        hook_event_name="Stop",
        session_id="devin-session-1",
        prompt_id=prompt_id,
        extra="ignored",
    )


def _session(
    tags: list[str] | None = None,
    pull_requests: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    return {
        "service_user_id": stop_wake_handler.HYDRA_SERVICE_USER_ID,
        "tags": tags if tags is not None else ["ai-oncall", "airbyte-pr-123"],
        "pull_requests": pull_requests or [],
    }


def _pull_request(
    state: str = "open",
    labels: list[str] | None = None,
    sha: str = "sha-1",
) -> dict[str, Any]:
    return {
        "state": state,
        "labels": [{"name": label} for label in labels or ["hyd-chain-v2"]],
        "head": {"sha": sha},
    }


def _response(status_code: int, body: dict[str, Any] | None = None, text: str = "") -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = body or {}
    response.text = text
    return response


def _dispatch_api_response(
    method: str,
    *_args: Any,
    **_kwargs: Any,
) -> MagicMock:
    if method == "GET":
        return _response(200, _pull_request())
    if method == "POST":
        return _response(204)
    raise AssertionError(f"Unexpected GitHub request method: {method}")


class InMemoryStore:
    def __init__(self) -> None:
        self.events: set[tuple[str, str]] = set()

    def claim_event(self, session_id: str, prompt_id: str) -> bool:
        key = (session_id, prompt_id)
        if key in self.events:
            return False
        self.events.add(key)
        return True


def _handle_with(
    monkeypatch: pytest.MonkeyPatch,
    *,
    session: dict[str, Any] | None = None,
    github_response: MagicMock | None = None,
    store: InMemoryStore | None = None,
    event: DevinStopEvent | None = None,
) -> tuple[dict[str, Any], MagicMock, InMemoryStore]:
    fake_store = store or InMemoryStore()
    api = MagicMock(return_value=github_response or _response(200, _pull_request()))
    monkeypatch.setattr(stop_wake_handler, "get_session", lambda session_id: session)
    monkeypatch.setattr(stop_wake_handler, "_github_request", api)
    result = stop_wake_handler.handle_stop_event(event or _event(), fake_store)
    return result, api, fake_store


def test_not_hydra_session_is_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    result, api, _ = _handle_with(
        monkeypatch,
        session={"service_user_id": "other", "tags": ["ai-oncall"], "pull_requests": []},
    )

    assert result["outcome"] == "not_hydra"
    api.assert_not_called()


def test_duplicate_event_is_not_processed(monkeypatch: pytest.MonkeyPatch) -> None:
    store = InMemoryStore()
    store.claim_event("session-1", "prompt-1")
    result, api, _ = _handle_with(monkeypatch, session=_session(), store=store)

    assert result["outcome"] == "duplicate"
    api.assert_not_called()


def test_no_pr_ignores_enterprise_and_other_repository_urls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _session(
        tags=["ai-oncall"],
        pull_requests=[
            {"pr_url": "https://github.com/airbytehq/airbyte-enterprise/pull/12"},
            {"pr_url": "https://github.com/other/repo/pull/13"},
        ],
    )
    result, api, _ = _handle_with(monkeypatch, session=session)

    assert result["outcome"] == "no_pr"
    api.assert_not_called()


def test_ambiguous_pr_tags_are_not_processed(monkeypatch: pytest.MonkeyPatch) -> None:
    result, api, _ = _handle_with(
        monkeypatch,
        session=_session(tags=["ai-oncall", "airbyte-pr-123", "airbyte-pr-456"]),
    )

    assert result["outcome"] == "ambiguous_pr"
    api.assert_not_called()


def test_ambiguous_pull_request_urls_are_not_processed(monkeypatch: pytest.MonkeyPatch) -> None:
    result, api, _ = _handle_with(
        monkeypatch,
        session=_session(
            tags=["ai-oncall"],
            pull_requests=[
                {"pr_url": "https://github.com/airbytehq/airbyte/pull/123"},
                {"pr_url": "https://github.com/airbytehq/airbyte/pull/456"},
            ],
        ),
    )

    assert result["outcome"] == "ambiguous_pr"
    api.assert_not_called()


def test_closed_pr_is_not_woken(monkeypatch: pytest.MonkeyPatch) -> None:
    result, api, _ = _handle_with(
        monkeypatch,
        session=_session(),
        github_response=_response(200, _pull_request(state="closed")),
    )

    assert result["outcome"] == "closed"
    api.assert_called_once_with("GET", "/repos/airbytehq/airbyte/pulls/123")


def test_pr_without_hydra_label_is_not_woken(monkeypatch: pytest.MonkeyPatch) -> None:
    result, api, _ = _handle_with(
        monkeypatch,
        session=_session(),
        github_response=_response(200, _pull_request(labels=["bug"])),
    )

    assert result["outcome"] == "no_label"
    api.assert_called_once_with("GET", "/repos/airbytehq/airbyte/pulls/123")


def test_repeat_prompt_on_same_sha_still_dispatches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = InMemoryStore()
    api = MagicMock(side_effect=_dispatch_api_response)
    monkeypatch.setattr(stop_wake_handler, "get_session", lambda session_id: _session())
    monkeypatch.setattr(stop_wake_handler, "_github_request", api)

    first = stop_wake_handler.handle_stop_event(_event("prompt-1"), store)
    second = stop_wake_handler.handle_stop_event(_event("prompt-2"), store)

    assert first["outcome"] == "dispatched"
    assert second["outcome"] == "dispatched"
    assert first["dispatch_request"]["client_payload"]["head_sha"] == "sha-1"
    assert second["dispatch_request"]["client_payload"]["head_sha"] == "sha-1"
    post_calls = [api_call for api_call in api.call_args_list if api_call.args[0] == "POST"]
    assert post_calls == [
        call(
            "POST",
            "/repos/airbytehq/airbyte/dispatches",
            json=first["dispatch_request"],
        ),
        call(
            "POST",
            "/repos/airbytehq/airbyte/dispatches",
            json=second["dispatch_request"],
        ),
    ]


def test_pr_tag_is_preferred_over_pull_request_urls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    api = MagicMock(side_effect=_dispatch_api_response)
    session = _session(
        tags=["ai-oncall", "airbyte-pr-123"],
        pull_requests=[{"pr_url": "https://github.com/airbytehq/airbyte/pull/456"}],
    )
    monkeypatch.setattr(stop_wake_handler, "get_session", lambda session_id: session)
    monkeypatch.setattr(stop_wake_handler, "_github_request", api)
    result = stop_wake_handler.handle_stop_event(_event(), InMemoryStore())

    expected = {
        "event_type": "handoff",
        "client_payload": {"pr": 123, "head_sha": "sha-1", "source_stage": "ai-prove-fix"},
    }
    assert result["outcome"] == "dispatched"
    assert result["dispatch_request"] == expected
    assert api.call_args_list == [
        call("GET", "/repos/airbytehq/airbyte/pulls/123"),
        call("POST", "/repos/airbytehq/airbyte/dispatches", json=expected),
    ]


def test_dispatch_sends_exact_body(monkeypatch: pytest.MonkeyPatch) -> None:
    api = MagicMock(
        side_effect=[
            _response(200, _pull_request()),
            _response(204),
        ]
    )
    monkeypatch.setattr(stop_wake_handler, "get_session", lambda session_id: _session())
    monkeypatch.setattr(stop_wake_handler, "_github_request", api)
    result = stop_wake_handler.handle_stop_event(_event(), InMemoryStore())

    body = {
        "event_type": "handoff",
        "client_payload": {"pr": 123, "head_sha": "sha-1", "source_stage": "ai-prove-fix"},
    }
    assert result["outcome"] == "dispatched"
    assert api.call_args_list == [
        call("GET", "/repos/airbytehq/airbyte/pulls/123"),
        call("POST", "/repos/airbytehq/airbyte/dispatches", json=body),
    ]


def test_github_error_returns_error_with_status_and_truncated_body(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result, _, _ = _handle_with(
        monkeypatch,
        session=_session(),
        github_response=_response(503, text="x" * 250),
    )

    assert result["outcome"] == "error"
    assert result["status_code"] == 503
    assert len(result["body"]) == 200


def test_devin_lookup_exception_returns_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_lookup(session_id: str) -> None:
        raise RuntimeError("lookup failed")

    monkeypatch.setattr(stop_wake_handler, "get_session", fail_lookup)
    result = stop_wake_handler.handle_stop_event(_event(), InMemoryStore())

    assert result["outcome"] == "error"


@pytest.mark.parametrize(
    ("tags", "expected"),
    [
        (["pr-review", "conflict-resolution", "oncall-issue-123", "airbyte-pr-1"], "ai-review"),
        (["conflict-resolution", "oncall-issue-123", "airbyte-pr-1"], "ai-resolve-conflicts"),
        (["oncall-issue-123", "airbyte-pr-1"], "ai-fix"),
        (["airbyte-pr-1"], "ai-prove-fix"),
        (["oncall-issue-invalid"], "unknown"),
        (["ai-oncall"], "unknown"),
    ],
)
def test_source_stage_mapping(tags: list[str], expected: str) -> None:
    has_pr_tag = any(tag.startswith("airbyte-pr-") for tag in tags)
    assert stop_wake_handler._source_stage(tags, has_pr_tag) == expected


def test_stop_endpoint_authentication_and_background_processing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEVIN_STOP_HOOK_BEARER_TOKEN", "valid-token")
    client = TestClient(app_module.app)
    payload = {
        "hook_event_name": "Stop",
        "session_id": "devin-session-1",
        "prompt_id": "prompt-1",
        "stop_hook_active": False,
    }

    assert client.post("/devin/stop", json=payload).status_code == 401
    assert (
        client.post(
            "/devin/stop",
            json=payload,
            headers={"Authorization": "Bearer wrong-token"},
        ).status_code
        == 403
    )
    with patch("agent_message_bus.app._process_stop_event") as process_event:
        response = client.post(
            "/devin/stop",
            json=payload,
            headers={"Authorization": "Bearer valid-token"},
        )
        assert response.status_code == 200
        assert response.json() == {"status": "accepted"}
        process_event.assert_called_once()


def test_non_stop_hook_event_is_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEVIN_STOP_HOOK_BEARER_TOKEN", "valid-token")
    client = TestClient(app_module.app)
    with patch("agent_message_bus.app._process_stop_event") as process_event:
        response = client.post(
            "/devin/stop",
            json={
                "hook_event_name": "SessionStart",
                "session_id": "devin-session-1",
                "prompt_id": "prompt-1",
            },
            headers={"Authorization": "Bearer valid-token"},
        )
    assert response.status_code == 200
    assert response.json() == {"status": "ignored"}
    process_event.assert_not_called()


def test_github_app_installation_token_is_minted_and_cached(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    monkeypatch.setenv("HYDRA_HANDOFF_BOT_APP_ID", "12345")
    monkeypatch.setenv("HYDRA_HANDOFF_BOT_PRIVATE_KEY", private_key_pem)
    monkeypatch.setattr(github_app, "_token", None)
    monkeypatch.setattr(github_app, "_token_expires_at", None)
    installation_response = _response(200, {"id": 67890})
    token_response = _response(
        201,
        {"token": "installation-token", "expires_at": "2099-01-01T00:00:00Z"},
    )

    with (
        patch(
            "agent_message_bus.github_app.requests.get", return_value=installation_response
        ) as get,
        patch("agent_message_bus.github_app.requests.post", return_value=token_response) as post,
    ):
        assert github_app.get_installation_token() == "installation-token"
        assert github_app.get_installation_token() == "installation-token"

    get.assert_called_once()
    assert get.call_args.kwargs["headers"]["Accept"] == "application/vnd.github+json"
    assert get.call_args.kwargs["headers"]["X-GitHub-Api-Version"] == "2022-11-28"
    post.assert_called_once_with(
        "https://api.github.com/app/installations/67890/access_tokens",
        headers=post.call_args.kwargs["headers"],
        json={
            "repositories": ["airbyte"],
            "permissions": {
                "contents": "write",
                "pull_requests": "read",
                "metadata": "read",
            },
        },
        timeout=10,
    )
    jwt_value = get.call_args.kwargs["headers"]["Authorization"].removeprefix("Bearer ")
    assert github_app.jwt.get_unverified_header(jwt_value)["alg"] == "RS256"
    claims = github_app.jwt.decode(
        jwt_value,
        private_key.public_key(),
        algorithms=["RS256"],
        options={"verify_exp": False},
    )
    assert claims["iss"] == "12345"
    assert github_app._token == "installation-token"
