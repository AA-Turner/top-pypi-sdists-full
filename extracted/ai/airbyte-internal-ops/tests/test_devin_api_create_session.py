"""Tests for the `devin_api` session client against a mocked HTTP layer."""

from __future__ import annotations

from typing import Any

import pytest
import requests

from airbyte_ops_mcp import devin_api

_SID = "0123456789abcdef0123456789abcdef"
_URL = f"https://app.devin.ai/sessions/{_SID}"


class _FakeResponse:
    def __init__(self, body: Any, status_code: int = 200) -> None:
        self._body = body
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")

    def json(self) -> Any:
        return self._body


@pytest.fixture
def creds(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in devin_api._TOKEN_ENV_VARS + devin_api._ORG_ID_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("DEVIN_API_KEY", "tok-123")
    monkeypatch.setenv("DEVIN_ORG_ID", "org_abc")


def _capture_post(
    monkeypatch: pytest.MonkeyPatch, response: _FakeResponse
) -> dict[str, Any]:
    captured: dict[str, Any] = {}

    def fake_post(url: str, **kwargs: Any) -> _FakeResponse:
        captured["url"] = url
        captured.update(kwargs)
        return response

    monkeypatch.setattr(devin_api.requests, "post", fake_post)
    return captured


def test_create_session_calls_v3_endpoint(
    creds: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = _capture_post(
        monkeypatch,
        _FakeResponse(
            {
                "session_id": f"devin-{_SID}",
                "url": _URL,
            }
        ),
    )
    schema = {"type": "object", "properties": {"summary": {"type": "string"}}}
    ref = devin_api.create_session(
        "do the thing",
        title="Title",
        tags=["a", "b"],
        playbook_id="pb-1",
        max_acu_limit=5,
        structured_output_schema=schema,
    )
    assert captured["url"] == "https://api.devin.ai/v3/organizations/org_abc/sessions"
    assert captured["headers"]["Authorization"] == "Bearer tok-123"
    assert captured["json"] == {
        "prompt": "do the thing",
        "title": "Title",
        "tags": ["a", "b"],
        "playbook_id": "pb-1",
        "max_acu_limit": 5,
        "structured_output_schema": schema,
    }
    assert captured["timeout"] == 30
    assert ref == devin_api.DevinSessionRef(session_id=_SID, url=_URL)


def test_create_session_omits_optional_fields(
    creds: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = _capture_post(monkeypatch, _FakeResponse({"session_id": _SID}))
    devin_api.create_session("p")
    assert captured["json"] == {"prompt": "p"}


@pytest.mark.parametrize(
    "body,expected",
    [
        pytest.param(
            {"id": f"devin-{_SID}"},
            devin_api.DevinSessionRef(_SID, _URL),
            id="id_key_url_fallback",
        ),
        pytest.param(
            {"session_id": _SID, "url": ""},
            devin_api.DevinSessionRef(_SID, _URL),
            id="empty_url_fallback",
        ),
        pytest.param(
            {"session_id": _SID, "status": "exited", "is_archived": True},
            devin_api.DevinSessionRef(_SID, _URL, status="exited", is_archived=True),
            id="status_and_archived",
        ),
        pytest.param(
            {"session_id": _SID, "status": None, "is_archived": "yes"},
            devin_api.DevinSessionRef(_SID, _URL),
            id="non_bool_archived_ignored",
        ),
    ],
)
def test_create_session_parses_response(
    creds: None,
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, Any],
    expected: devin_api.DevinSessionRef,
) -> None:
    _capture_post(monkeypatch, _FakeResponse(body))
    assert devin_api.create_session("p") == expected


@pytest.mark.parametrize(
    "body,match",
    [
        pytest.param({}, "no session_id", id="no_id"),
        pytest.param({"session_id": 42}, "no session_id", id="non_string_id"),
        pytest.param({"session_id": ""}, "no session_id", id="empty_id"),
        pytest.param(None, "non-object body", id="null_body"),
        pytest.param([{"session_id": "x"}], "non-object body", id="list_body"),
        pytest.param("abc", "non-object body", id="string_body"),
    ],
)
def test_create_session_rejects_malformed_response(
    creds: None, monkeypatch: pytest.MonkeyPatch, body: Any, match: str
) -> None:
    _capture_post(monkeypatch, _FakeResponse(body))
    with pytest.raises(RuntimeError, match=match):
        devin_api.create_session("p")


def test_create_session_raises_on_http_error(
    creds: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    _capture_post(monkeypatch, _FakeResponse({}, status_code=500))
    with pytest.raises(requests.HTTPError):
        devin_api.create_session("p")


@pytest.mark.parametrize(
    "missing",
    [
        pytest.param("DEVIN_API_KEY", id="missing_token"),
        pytest.param("DEVIN_ORG_ID", id="missing_org"),
    ],
)
def test_create_session_requires_credentials(
    creds: None, monkeypatch: pytest.MonkeyPatch, missing: str
) -> None:
    monkeypatch.delenv(missing)
    monkeypatch.setattr(
        devin_api.requests,
        "post",
        lambda *a, **k: pytest.fail("must not call the API without credentials"),
    )
    with pytest.raises(RuntimeError):
        devin_api.create_session("p")


def _capture_get(
    monkeypatch: pytest.MonkeyPatch, response: _FakeResponse
) -> dict[str, Any]:
    captured: dict[str, Any] = {}

    def fake_get(url: str, **kwargs: Any) -> _FakeResponse:
        captured["url"] = url
        captured.update(kwargs)
        return response

    monkeypatch.setattr(devin_api.requests, "get", fake_get)
    return captured


def test_list_sessions_filters_by_tags(
    creds: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = _capture_get(
        monkeypatch,
        _FakeResponse(
            {
                "items": [
                    {
                        "session_id": f"devin-{_SID}",
                        "status": "running",
                        "tags": ["rollout:r1", 7],
                    },
                    {"session_id": "devin-" + "f" * 32, "is_archived": True},
                ]
            }
        ),
    )
    refs = devin_api.list_sessions(tags=["rollout-autopilot", "rollout:r1"], limit=5)
    assert captured["url"] == "https://api.devin.ai/v3/organizations/org_abc/sessions"
    assert captured["params"] == {
        "tags": ["rollout-autopilot", "rollout:r1"],
        "limit": 5,
    }
    assert [r.session_id for r in refs] == [_SID, "f" * 32]
    assert refs[0].status == "running" and not refs[0].is_archived
    assert refs[0].tags == ("rollout:r1",)
    assert refs[1].is_archived and refs[1].tags == ()


@pytest.mark.parametrize(
    "body",
    [
        pytest.param({}, id="no_items"),
        pytest.param({"items": None}, id="null_items"),
        pytest.param([], id="list_body"),
    ],
)
def test_list_sessions_rejects_malformed_response(
    creds: None, monkeypatch: pytest.MonkeyPatch, body: Any
) -> None:
    _capture_get(monkeypatch, _FakeResponse(body))
    with pytest.raises(RuntimeError, match="items"):
        devin_api.list_sessions(tags=["t"])


@pytest.mark.parametrize(
    "session_id",
    [pytest.param(_SID, id="bare_id"), pytest.param(f"devin-{_SID}", id="prefixed")],
)
def test_unarchive_session_posts_to_unarchive_endpoint(
    creds: None, monkeypatch: pytest.MonkeyPatch, session_id: str
) -> None:
    captured = _capture_post(
        monkeypatch,
        _FakeResponse({"session_id": f"devin-{_SID}", "is_archived": False}),
    )
    ref = devin_api.unarchive_session(session_id)
    assert captured["url"] == (
        f"https://api.devin.ai/v3/organizations/org_abc/sessions/devin-{_SID}/unarchive"
    )
    assert "json" not in captured
    assert ref.session_id == _SID and not ref.is_archived


def test_send_session_message_posts_to_messages_endpoint(
    creds: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = _capture_post(monkeypatch, _FakeResponse({}))
    devin_api.send_session_message(_SID, "hello")
    assert captured["url"] == (
        f"https://api.devin.ai/v3/organizations/org_abc/sessions/devin-{_SID}/messages"
    )
    assert captured["json"] == {"message": "hello"}
