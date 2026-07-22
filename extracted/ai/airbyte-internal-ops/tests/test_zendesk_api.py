# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Zendesk API client and MCP tool."""

from __future__ import annotations

import pytest

from airbyte_ops_mcp import zendesk_api
from airbyte_ops_mcp.mcp import zendesk_ops
from airbyte_ops_mcp.zendesk_api import (
    ZendeskAPIError,
    ZendeskCredentials,
    resolve_zendesk_credentials,
)


@pytest.mark.unit
def test_credentials_base_url_and_auth() -> None:
    creds = ZendeskCredentials(
        subdomain="airbyte1416",
        email="agent@airbyte.io",
        api_token="tok",
    )
    assert creds.base_url == "https://airbyte1416.zendesk.com/api/v2"
    assert creds.auth == ("agent@airbyte.io/token", "tok")


@pytest.mark.unit
@pytest.mark.parametrize(
    "env,expected_missing",
    [
        pytest.param(
            {
                "ZENDESK_SUBDOMAIN": "airbyte1416",
                "ZENDESK_EMAIL": "agent@airbyte.io",
                "ZENDESK_API_TOKEN": "tok",
            },
            None,
            id="all_present",
        ),
        pytest.param(
            {"ZENDESK_EMAIL": "agent@airbyte.io", "ZENDESK_API_TOKEN": "tok"},
            "ZENDESK_SUBDOMAIN",
            id="missing_subdomain",
        ),
        pytest.param(
            {
                "ZENDESK_SUBDOMAIN": "airbyte1416",
                "ZENDESK_EMAIL": "agent@airbyte.io",
                "ZENDESK_API_TOKEN": "  ",
            },
            "ZENDESK_API_TOKEN",
            id="blank_token",
        ),
    ],
)
def test_resolve_zendesk_credentials(
    monkeypatch: pytest.MonkeyPatch,
    env: dict[str, str],
    expected_missing: str | None,
) -> None:
    for key in ("ZENDESK_SUBDOMAIN", "ZENDESK_EMAIL", "ZENDESK_API_TOKEN"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    if expected_missing is None:
        creds = resolve_zendesk_credentials()
        assert creds.subdomain == "airbyte1416"
    else:
        with pytest.raises(ZendeskAPIError, match=expected_missing):
            resolve_zendesk_credentials()


@pytest.mark.unit
@pytest.mark.parametrize(
    "raw_url,ticket_id,expected",
    [
        pytest.param(
            "https://airbyte1416.zendesk.com/api/v2/tickets/42.json",
            42,
            "https://airbyte1416.zendesk.com/agent/tickets/42",
            id="standard_api_url",
        ),
        pytest.param(None, 42, None, id="no_url"),
        pytest.param(
            "https://airbyte1416.zendesk.com/api/v2/tickets/42.json",
            None,
            None,
            id="no_ticket_id",
        ),
        pytest.param(
            "https://airbyte1416.zendesk.com/hc/tickets/42",
            42,
            None,
            id="missing_api_segment",
        ),
    ],
)
def test_agent_ticket_url(
    raw_url: str | None, ticket_id: int | None, expected: str | None
) -> None:
    assert zendesk_ops._agent_ticket_url(raw_url, ticket_id) == expected


@pytest.mark.unit
def test_get_zendesk_ticket_maps_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    ticket = {
        "id": 42,
        "subject": "Sync failing",
        "status": "open",
        "description": "It broke",
        "priority": "high",
        "tags": ["coral_agents"],
        "requester_id": 7,
        "organization_id": 9,
        "created_at": "2026-07-01T00:00:00Z",
        "updated_at": "2026-07-02T00:00:00Z",
        "url": "https://airbyte1416.zendesk.com/api/v2/tickets/42.json",
    }
    monkeypatch.setattr(zendesk_ops, "get_ticket", lambda ticket_id: ticket)

    result = zendesk_ops.get_zendesk_ticket(ticket_id=42)

    assert result.success is True
    assert result.ticket_id == 42
    assert result.subject == "Sync failing"
    assert result.tags == ["coral_agents"]
    assert result.url == "https://airbyte1416.zendesk.com/agent/tickets/42"
    assert result.comments == []


@pytest.mark.unit
def test_get_zendesk_ticket_reports_api_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(ticket_id: int) -> dict:
        raise zendesk_api.ZendeskAPIError("Zendesk resource not found: /tickets/1.json")

    monkeypatch.setattr(zendesk_ops, "get_ticket", _raise)

    result = zendesk_ops.get_zendesk_ticket(ticket_id=1)

    assert result.success is False
    assert "not found" in result.message
    assert result.ticket_id == 1


@pytest.mark.unit
def test_get_zendesk_ticket_includes_comments_and_attachments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ticket = {"id": 42, "url": "https://airbyte1416.zendesk.com/api/v2/tickets/42.json"}
    raw_comments = [
        {
            "id": 100,
            "author_id": 7,
            "public": True,
            "plain_body": "First reply",
            "created_at": "2026-07-01T00:00:00Z",
            "attachments": [
                {
                    "id": 500,
                    "file_name": "log.txt",
                    "content_type": "text/plain",
                    "content_url": "https://airbyte1416.zendesk.com/attachments/500",
                    "size": 1234,
                }
            ],
        },
        {"id": 101, "body": "Note", "public": False},
    ]
    monkeypatch.setattr(zendesk_ops, "get_ticket", lambda ticket_id: ticket)
    monkeypatch.setattr(
        zendesk_ops, "get_ticket_comments", lambda ticket_id: raw_comments
    )

    result = zendesk_ops.get_zendesk_ticket(ticket_id=42, include_comments=True)

    assert result.success is True
    assert [c.body for c in result.comments] == ["First reply", "Note"]
    assert result.comments[0].attachments[0].file_name == "log.txt"
    assert result.comments[0].attachments[0].size == 1234
    assert result.comments[1].attachments == []


@pytest.mark.unit
def test_get_zendesk_ticket_maps_via_and_custom_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ticket = {
        "id": 42,
        "url": "https://airbyte1416.zendesk.com/api/v2/tickets/42.json",
        "via": {
            "channel": "web",
            "source": {"rel": "follow_up", "from": {"ticket_id": 7}},
        },
        "custom_fields": [
            {"id": 52734849292827, "value": "Answered - how-to / guidance / docs"},
            {"id": 16158730855451, "value": None},
        ],
    }
    monkeypatch.setattr(zendesk_ops, "get_ticket", lambda ticket_id: ticket)

    result = zendesk_ops.get_zendesk_ticket(ticket_id=42)

    assert result.via_channel == "web"
    assert result.via_source_rel == "follow_up"
    assert result.follow_up_source_ticket_id == 7
    assert result.custom_fields[0].id == 52734849292827
    assert result.custom_fields[0].value == "Answered - how-to / guidance / docs"
    assert result.custom_fields[1].value is None


@pytest.mark.unit
def test_get_zendesk_ticket_non_follow_up_has_no_source_ticket(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ticket = {
        "id": 42,
        "via": {"channel": "email", "source": {"rel": "web_form"}},
    }
    monkeypatch.setattr(zendesk_ops, "get_ticket", lambda ticket_id: ticket)

    result = zendesk_ops.get_zendesk_ticket(ticket_id=42)

    assert result.via_channel == "email"
    assert result.via_source_rel == "web_form"
    assert result.follow_up_source_ticket_id is None


@pytest.mark.unit
def test_get_zendesk_ticket_notes_comment_fetch_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ticket = {"id": 42, "url": "https://airbyte1416.zendesk.com/api/v2/tickets/42.json"}

    def _raise(ticket_id: int) -> list:
        raise zendesk_api.ZendeskAPIError("Zendesk request failed")

    monkeypatch.setattr(zendesk_ops, "get_ticket", lambda ticket_id: ticket)
    monkeypatch.setattr(zendesk_ops, "get_ticket_comments", _raise)

    result = zendesk_ops.get_zendesk_ticket(ticket_id=42, include_comments=True)

    assert result.success is True
    assert result.comments == []
    assert "comments could not be retrieved" in result.message


@pytest.mark.unit
def test_add_internal_note_rejects_empty_body(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for key in ("ZENDESK_SUBDOMAIN", "ZENDESK_EMAIL", "ZENDESK_API_TOKEN"):
        monkeypatch.setenv(key, "x")

    with pytest.raises(ZendeskAPIError, match="must not be empty"):
        zendesk_api.add_internal_note(42, "   ")


@pytest.mark.unit
def test_add_internal_note_posts_private_comment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def _fake_put(credentials: ZendeskCredentials, path: str, json_body: dict) -> dict:
        captured["path"] = path
        captured["json_body"] = json_body
        return {"ticket": {"id": 42}, "audit": {"events": []}}

    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")
    monkeypatch.setattr(zendesk_api, "_put", _fake_put)

    zendesk_api.add_internal_note(42, "internal note", credentials=creds)

    assert captured["path"] == "/tickets/42.json"
    assert captured["json_body"] == {
        "ticket": {"comment": {"body": "internal note", "public": False}}
    }


@pytest.mark.unit
def test_post_zendesk_internal_comment_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _fake_add(ticket_id: int, body: str, *, add_tags=None) -> dict:
        return {
            "ticket": {"id": ticket_id},
            "audit": {
                "events": [
                    {"type": "Notification", "id": 1},
                    {"type": "Comment", "id": 999, "public": False},
                ]
            },
        }

    monkeypatch.setattr(zendesk_ops, "add_internal_note", _fake_add)

    result = zendesk_ops.post_zendesk_internal_comment(ticket_id=42, body="hi")

    assert result.success is True
    assert result.ticket_id == 42
    assert result.comment_id == 999
    assert result.public is False


@pytest.mark.unit
def test_post_zendesk_internal_comment_reports_api_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(ticket_id: int, body: str, *, add_tags=None) -> dict:
        raise zendesk_api.ZendeskAPIError("Internal note body must not be empty.")

    monkeypatch.setattr(zendesk_ops, "add_internal_note", _raise)

    result = zendesk_ops.post_zendesk_internal_comment(ticket_id=42, body="")

    assert result.success is False
    assert result.ticket_id == 42
    assert result.comment_id is None
    assert "must not be empty" in result.message


@pytest.mark.unit
def test_add_internal_note_appends_tags(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def _fake_put(credentials: ZendeskCredentials, path: str, json_body: dict) -> dict:
        captured["json_body"] = json_body
        return {"ticket": {"id": 42, "tags": ["existing", "triage"]}}

    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")
    monkeypatch.setattr(zendesk_api, "_put", _fake_put)

    zendesk_api.add_internal_note(
        42, "note", credentials=creds, add_tags=["triage", "  ", ""]
    )

    assert captured["json_body"] == {
        "ticket": {
            "comment": {"body": "note", "public": False},
            "additional_tags": ["triage"],
        }
    }


@pytest.mark.unit
def test_add_ticket_tags_uses_additive_endpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def _fake_post(credentials: ZendeskCredentials, path: str, json_body: dict) -> dict:
        captured["path"] = path
        captured["json_body"] = json_body
        return {"tags": ["existing", "new"]}

    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")
    monkeypatch.setattr(zendesk_api, "_post", _fake_post)

    result = zendesk_api.add_ticket_tags(42, ["new"], credentials=creds)

    assert captured["path"] == "/tickets/42/tags.json"
    assert captured["json_body"] == {"tags": ["new"]}
    assert result == ["existing", "new"]


@pytest.mark.unit
def test_add_ticket_tags_rejects_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("ZENDESK_SUBDOMAIN", "ZENDESK_EMAIL", "ZENDESK_API_TOKEN"):
        monkeypatch.setenv(key, "x")

    with pytest.raises(ZendeskAPIError, match="non-empty tag"):
        zendesk_api.add_ticket_tags(42, ["  ", ""])


@pytest.mark.unit
def test_add_zendesk_ticket_tags_tool_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_ops,
        "add_ticket_tags",
        lambda ticket_id, tags: ["existing", "escalated"],
    )

    result = zendesk_ops.add_zendesk_ticket_tags(ticket_id=42, tags=["escalated"])

    assert result.success is True
    assert result.ticket_id == 42
    assert result.tags == ["existing", "escalated"]


@pytest.mark.unit
def test_add_zendesk_ticket_tags_tool_reports_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(ticket_id: int, tags: list) -> list:
        raise zendesk_api.ZendeskAPIError("At least one non-empty tag is required.")

    monkeypatch.setattr(zendesk_ops, "add_ticket_tags", _raise)

    result = zendesk_ops.add_zendesk_ticket_tags(ticket_id=42, tags=[])

    assert result.success is False
    assert result.ticket_id == 42
    assert result.tags == []
    assert "non-empty tag" in result.message
