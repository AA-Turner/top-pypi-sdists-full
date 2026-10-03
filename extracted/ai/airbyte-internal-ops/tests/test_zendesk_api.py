# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Zendesk API client and MCP tool."""

from __future__ import annotations

from typing import Any

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
def test_request_422_error_includes_only_safe_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Response:
        status_code = 422

        def json(self) -> dict[str, object]:
            return {
                "error": "RecordInvalid",
                "description": "Record validation errors",
                "details": {
                    "requester": [
                        {
                            "error": "InvalidValue",
                            "description": "Requester: jane@example.com is invalid",
                        }
                    ],
                    "assignee": [{"error": "Blank"}],
                },
            }

    monkeypatch.setattr(
        zendesk_api.requests,
        "request",
        lambda *args, **kwargs: _Response(),
    )
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    with pytest.raises(ZendeskAPIError) as exc_info:
        zendesk_api._request(creds, "POST", "/tickets.json")

    message = str(exc_info.value)
    assert "Error: RecordInvalid" in message
    assert "requester (InvalidValue)" in message
    assert "assignee (Blank)" in message
    assert "jane@example.com" not in message
    assert "is invalid" not in message


@pytest.mark.unit
def test_request_non_json_error_has_no_summary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Response:
        status_code = 500

        def json(self) -> dict[str, object]:
            raise ValueError("not JSON")

    monkeypatch.setattr(
        zendesk_api.requests,
        "request",
        lambda *args, **kwargs: _Response(),
    )
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    with pytest.raises(ZendeskAPIError) as exc_info:
        zendesk_api._request(creds, "POST", "/tickets.json")

    assert str(exc_info.value) == "Zendesk POST /tickets.json failed with status 500."


@pytest.mark.unit
def test_request_error_drops_unsafe_detail_field_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Response:
        status_code = 422

        def json(self) -> dict[str, object]:
            return {
                "details": {
                    "jane@example.com": [{"error": "InvalidValue"}],
                    "requester": [{"error": "InvalidValue"}],
                }
            }

    monkeypatch.setattr(
        zendesk_api.requests,
        "request",
        lambda *args, **kwargs: _Response(),
    )
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    with pytest.raises(ZendeskAPIError) as exc_info:
        zendesk_api._request(creds, "POST", "/tickets.json")

    message = str(exc_info.value)
    assert "jane@example.com" not in message
    assert "Fields: requester (InvalidValue)." in message


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
        "type": "problem",
        "problem_id": None,
        "assignee_id": 8,
        "submitter_id": 9,
        "ticket_form_id": 10,
        "email_cc_ids": [11, 12],
        "external_id": "outreach:example",
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
    assert result.type == "problem"
    assert result.assignee_id == 8
    assert result.submitter_id == 9
    assert result.ticket_form_id == 10
    assert result.email_cc_ids == [11, 12]
    assert result.external_id == "outreach:example"
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

    zendesk_api.add_internal_note(
        42, "<strong>internal</strong> note", credentials=creds
    )

    assert captured["path"] == "/tickets/42.json"
    assert captured["json_body"] == {
        "ticket": {
            "comment": {
                "html_body": "<strong>internal</strong> note",
                "public": False,
            }
        }
    }


@pytest.mark.unit
def test_post_zendesk_internal_comment_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _fake_add(ticket_id: int, html_body: str) -> dict:
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

    result = zendesk_ops.post_zendesk_internal_comment(
        ticket_id=42, html_body="<p>hi</p>"
    )

    assert result.success is True
    assert result.ticket_id == 42
    assert result.comment_id == 999
    assert result.public is False
    assert "internal-only" in result.message
    assert "not visible to the customer" in result.message


@pytest.mark.unit
def test_post_zendesk_internal_comment_reports_api_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(ticket_id: int, html_body: str) -> dict:
        raise zendesk_api.ZendeskAPIError("Internal note body must not be empty.")

    monkeypatch.setattr(zendesk_ops, "add_internal_note", _raise)

    result = zendesk_ops.post_zendesk_internal_comment(ticket_id=42, html_body="")

    assert result.success is False
    assert result.ticket_id == 42
    assert result.comment_id is None
    assert "must not be empty" in result.message


@pytest.mark.unit
def test_add_ticket_tags_merges_and_puts_full_union(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def _fake_get(ticket_id: int, credentials: ZendeskCredentials) -> dict:
        return {"id": ticket_id, "tags": ["p3", "severity_3", "new"]}

    def _fake_put(credentials: ZendeskCredentials, path: str, json_body: dict) -> dict:
        captured["path"] = path
        captured["json_body"] = json_body
        return {"ticket": {"id": 42, "tags": json_body["ticket"]["tags"]}}

    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")
    monkeypatch.setattr(zendesk_api, "get_ticket", _fake_get)
    monkeypatch.setattr(zendesk_api, "_put", _fake_put)

    # "new" already exists (deduped); "triaged" is appended; existing tagger
    # tags (p3, severity_3) are preserved in the full-union PUT.
    result = zendesk_api.add_ticket_tags(42, ["new", "triaged"], credentials=creds)

    assert captured["path"] == "/tickets/42.json"
    assert captured["json_body"] == {
        "ticket": {"tags": ["p3", "severity_3", "new", "triaged"]}
    }
    assert result == ["p3", "severity_3", "new", "triaged"]


@pytest.mark.unit
def test_add_ticket_tags_rejects_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("ZENDESK_SUBDOMAIN", "ZENDESK_EMAIL", "ZENDESK_API_TOKEN"):
        monkeypatch.setenv(key, "x")

    with pytest.raises(ZendeskAPIError, match="non-empty tag"):
        zendesk_api.add_ticket_tags(42, ["  ", ""])


@pytest.mark.unit
def test_set_ticket_email_ccs_puts_only_email_ccs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    email_ccs = [{"user_email": "cc@example.com", "user_name": "CC", "action": "put"}]
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    def _fake_put(
        credentials: ZendeskCredentials,
        path: str,
        json_body: dict[str, Any],
    ) -> dict[str, Any]:
        captured["path"] = path
        captured["json_body"] = json_body
        return {"ticket": {"id": 42, "email_cc_ids": [101]}}

    monkeypatch.setattr(zendesk_api, "_put", _fake_put)

    result = zendesk_api.set_ticket_email_ccs(42, email_ccs, credentials=creds)

    assert captured["path"] == "/tickets/42.json"
    assert captured["json_body"] == {"ticket": {"email_ccs": email_ccs}}
    assert result == {"id": 42, "email_cc_ids": [101]}


@pytest.mark.unit
def test_set_ticket_email_ccs_rejects_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_api,
        "_put",
        lambda *args, **kwargs: pytest.fail(
            "empty CC lists must not make an API request"
        ),
    )

    with pytest.raises(ZendeskAPIError, match="email CC"):
        zendesk_api.set_ticket_email_ccs(42, [])


@pytest.mark.unit
def test_set_ticket_email_ccs_rejects_missing_ticket_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(zendesk_api, "_put", lambda *args, **kwargs: {})
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    with pytest.raises(ZendeskAPIError, match="missing a `ticket` object"):
        zendesk_api.set_ticket_email_ccs(
            42,
            [{"user_email": "cc@example.com", "user_name": "CC", "action": "put"}],
            credentials=creds,
        )


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


@pytest.mark.unit
def test_zendesk_search_follows_pages_and_caps_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested_pages: list[int] = []

    def _fake_get(
        credentials: ZendeskCredentials,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict:
        assert path == "/search.json"
        params = params or {}
        page = int(params.get("page", ["1"])[0])
        requested_pages.append(page)
        return {
            "results": [{"id": (page - 1) * 100 + i} for i in range(1, 101)],
            "next_page": (
                f"https://airbyte1416.zendesk.com/api/v2/search.json?page={page + 1}"
                if page < 20
                else None
            ),
        }

    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")
    monkeypatch.setattr(zendesk_api, "_get", _fake_get)

    results = zendesk_api.search(
        "type:ticket",
        max_results=1500,
        credentials=creds,
    )

    assert len(results) == 1000
    assert requested_pages == list(range(1, 11))


@pytest.mark.unit
@pytest.mark.parametrize(
    "forms,error_text",
    [
        pytest.param([], "No active", id="not-found"),
        pytest.param(
            [
                {"id": 1, "name": "Support Outreach", "active": True},
                {"id": 2, "name": "support outreach", "active": True},
            ],
            "Multiple active",
            id="ambiguous",
        ),
    ],
)
def test_find_ticket_form_id_requires_unique_active_match(
    monkeypatch: pytest.MonkeyPatch,
    forms: list[dict[str, object]],
    error_text: str,
) -> None:
    monkeypatch.setattr(
        zendesk_api,
        "_get",
        lambda credentials, path, params=None: {"ticket_forms": forms},
    )
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    with pytest.raises(ZendeskAPIError, match=error_text):
        zendesk_api.find_ticket_form_id("Support Outreach", credentials=creds)


@pytest.mark.unit
def test_find_ticket_form_id_uses_active_case_insensitive_exact_match(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_api,
        "_get",
        lambda credentials, path, params=None: {
            "ticket_forms": [
                {"id": 1, "name": "Support Outreach old", "active": True},
                {"id": 2, "name": "support outreach", "active": True},
                {"id": 3, "name": "Support Outreach", "active": False},
            ]
        },
    )
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    assert zendesk_api.find_ticket_form_id("Support Outreach", credentials=creds) == 2


@pytest.mark.unit
def test_find_organizations_by_airbyte_org_id_validates_and_searches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def _fake_search(
        query: str,
        *,
        credentials: ZendeskCredentials | None = None,
    ) -> list[dict]:
        calls.append(query)
        return [{"id": 42, "name": "Airbyte", "url": "https://example.org/42"}]

    monkeypatch.setattr(zendesk_api, "search", _fake_search)
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    with pytest.raises(ZendeskAPIError, match="valid UUID"):
        zendesk_api.find_organizations_by_airbyte_org_id("not-a-uuid", creds)
    assert calls == []

    result = zendesk_api.find_organizations_by_airbyte_org_id(
        "11111111-1111-1111-1111-111111111111",
        creds,
    )

    assert result == [{"id": 42, "name": "Airbyte", "url": "https://example.org/42"}]
    assert calls == [
        "type:organization airbyte_org_id:11111111-1111-1111-1111-111111111111"
    ]


@pytest.mark.unit
def test_get_current_user_and_create_ticket_use_expected_endpoints(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests_seen: list[tuple[str, str, dict[str, object] | None]] = []

    def _fake_request(
        credentials: ZendeskCredentials,
        method: str,
        path: str,
        *,
        params: dict[str, object] | None = None,
        json_body: dict[str, object] | None = None,
    ) -> dict:
        requests_seen.append((method, path, json_body))
        if method == "GET":
            return {"user": {"id": 7, "email": "moonbot@example.com"}}
        return {"ticket": {"id": 42}}

    monkeypatch.setattr(zendesk_api, "_request", _fake_request)
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    assert zendesk_api.get_current_user(creds)["id"] == 7
    assert zendesk_api.create_ticket({"subject": "x"}, creds) == {"id": 42}
    assert requests_seen == [
        ("GET", "/users/me.json", None),
        ("POST", "/tickets.json", {"ticket": {"subject": "x"}}),
    ]


@pytest.mark.unit
def test_list_tickets_by_external_id_uses_filter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def _fake_get(
        credentials: ZendeskCredentials,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict:
        captured.update(path=path, params=params)
        return {"tickets": [{"id": 42, "external_id": "outreach:test"}]}

    monkeypatch.setattr(zendesk_api, "_get", _fake_get)
    creds = ZendeskCredentials(subdomain="s", email="e@a.io", api_token="t")

    result = zendesk_api.list_tickets_by_external_id("outreach:test", creds)

    assert result == [{"id": 42, "external_id": "outreach:test"}]
    assert captured["path"] == "/tickets.json"
    assert captured["params"] == {"external_id": "outreach:test", "per_page": 100}


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_builds_private_idempotent_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    cc_update_calls: list[dict[str, object]] = []
    monkeypatch.setattr(zendesk_ops, "list_tickets_by_external_id", lambda value: [])
    monkeypatch.setattr(
        zendesk_ops,
        "get_current_user",
        lambda: {"id": 7, "email": "moonbot@example.com"},
    )
    monkeypatch.setattr(zendesk_ops, "find_ticket_form_id", lambda name: 11)

    def _create(payload: dict[str, object]) -> dict:
        captured["payload"] = payload
        return {
            "id": 42,
            "url": "https://airbyte1416.zendesk.com/api/v2/tickets/42.json",
            "status": "new",
            "type": "incident",
            "requester_id": 21,
            "submitter_id": 7,
            "ticket_form_id": 11,
            "tags": ["outreach", "prospect"],
        }

    def _set_ccs(ticket_id: int | str, email_ccs: list[dict[str, str]]) -> dict:
        cc_update_calls.append({"ticket_id": ticket_id, "email_ccs": email_ccs})
        return {
            "id": ticket_id,
            "url": "https://airbyte1416.zendesk.com/api/v2/tickets/42.json",
            "status": "new",
            "type": "incident",
            "requester_id": 21,
            "submitter_id": 7,
            "ticket_form_id": 11,
            "email_cc_ids": [101],
            "tags": ["outreach", "prospect"],
        }

    monkeypatch.setattr(zendesk_ops, "create_ticket", _create)
    monkeypatch.setattr(zendesk_ops, "set_ticket_email_ccs", _set_ccs)

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:airbyte-org-1",
        ticket_type="incident",
        problem_id=99,
        subject="Support outreach",
        internal_note_html="<p>Private context</p>",
        tags=[" prospect ", "OUTREACH", "prospect"],
        requester=zendesk_ops.OutreachContact(
            email="requester@example.com",
            name="Requester",
        ),
        cc=[
            zendesk_ops.OutreachContact(
                email="Requester@example.com",
                name="Requester duplicate",
            ),
            zendesk_ops.OutreachContact(email="cc@example.com", name="CC"),
            zendesk_ops.OutreachContact(email="CC@example.com", name="Duplicate CC"),
        ],
        assignee_email="agent@example.com",
    )

    payload = captured["payload"]
    assert isinstance(payload, dict)
    assert payload == {
        "subject": "Support outreach",
        "comment": {"html_body": "<p>Private context</p>", "public": False},
        "status": "new",
        "priority": "normal",
        "type": "incident",
        "problem_id": 99,
        "tags": ["prospect", "outreach"],
        "external_id": "outreach:airbyte-org-1",
        "ticket_form_id": 11,
        "submitter_id": 7,
        "requester": {"name": "Requester", "email": "requester@example.com"},
        "assignee_email": "agent@example.com",
    }
    assert "organization_id" not in payload
    assert cc_update_calls == [
        {
            "ticket_id": 42,
            "email_ccs": [
                {"user_email": "cc@example.com", "user_name": "CC", "action": "put"}
            ],
        }
    ]
    assert result.success is True
    assert result.created is True
    assert result.ticket_id == 42
    assert result.submitter_id == 7
    assert result.email_cc_ids == [101]
    assert result.url == "https://airbyte1416.zendesk.com/agent/tickets/42"


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_reports_cc_update_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(zendesk_ops, "list_tickets_by_external_id", lambda value: [])
    monkeypatch.setattr(
        zendesk_ops,
        "get_current_user",
        lambda: {"id": 7, "email": "agent@example.com"},
    )
    monkeypatch.setattr(zendesk_ops, "find_ticket_form_id", lambda name: 11)
    monkeypatch.setattr(zendesk_ops, "create_ticket", lambda payload: {"id": 42})

    def _fail_cc_update(
        ticket_id: int | str,
        email_ccs: list[dict[str, str]],
    ) -> dict:
        raise ZendeskAPIError("Zendesk unavailable")

    monkeypatch.setattr(zendesk_ops, "set_ticket_email_ccs", _fail_cc_update)

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:cc-update-failure",
        ticket_type="incident",
        problem_id=99,
        subject="Support outreach",
        internal_note_html="<p>Private context</p>",
        requester=zendesk_ops.OutreachContact(
            email="requester@example.com",
            name="Requester",
        ),
        cc=[zendesk_ops.OutreachContact(email="cc@example.com", name="CC")],
    )

    assert result.success is False
    assert result.created is True
    assert result.ticket_id == 42
    assert result.message == (
        "Created ticket 42 but failed to add CCs: Zendesk unavailable; re-run to retry."
    )


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_existing_external_id_is_idempotent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    existing = {"id": 42, "status": "new", "external_id": "outreach:test"}
    monkeypatch.setattr(
        zendesk_ops,
        "list_tickets_by_external_id",
        lambda external_id: [existing],
    )
    monkeypatch.setattr(
        zendesk_ops,
        "get_current_user",
        lambda: pytest.fail("existing tickets must not call current-user lookup"),
    )
    monkeypatch.setattr(
        zendesk_ops,
        "find_ticket_form_id",
        lambda name: pytest.fail("existing tickets must not resolve a form"),
    )
    monkeypatch.setattr(
        zendesk_ops,
        "create_ticket",
        lambda payload: pytest.fail("existing tickets must not be created again"),
    )
    monkeypatch.setattr(
        zendesk_ops,
        "set_ticket_email_ccs",
        lambda *args, **kwargs: pytest.fail("tickets without CCs must not be updated"),
    )

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:test",
        ticket_type="problem",
        subject="A subject",
        internal_note_html="<p>A note</p>",
    )

    assert result.success is True
    assert result.created is False
    assert result.ticket_id == 42


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_existing_incident_ensures_ccs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    existing = {"id": 42, "status": "open", "external_id": "outreach:test"}
    cc_update_calls: list[dict[str, object]] = []
    monkeypatch.setattr(
        zendesk_ops,
        "list_tickets_by_external_id",
        lambda external_id: [existing],
    )
    monkeypatch.setattr(
        zendesk_ops,
        "create_ticket",
        lambda payload: pytest.fail("existing tickets must not be created again"),
    )

    def _set_ccs(ticket_id: int | str, email_ccs: list[dict[str, str]]) -> dict:
        cc_update_calls.append({"ticket_id": ticket_id, "email_ccs": email_ccs})
        return {
            "id": 42,
            "status": "open",
            "type": "incident",
            "problem_id": 99,
            "email_cc_ids": [101],
        }

    monkeypatch.setattr(zendesk_ops, "set_ticket_email_ccs", _set_ccs)

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:test",
        ticket_type="incident",
        problem_id=99,
        subject="A subject",
        internal_note_html="<p>A note</p>",
        requester=zendesk_ops.OutreachContact(
            email=" requester@example.com ", name="Requester"
        ),
        cc=[
            zendesk_ops.OutreachContact(email=" CC@example.com ", name="CC"),
            zendesk_ops.OutreachContact(
                email="requester@example.com", name="Requester"
            ),
            zendesk_ops.OutreachContact(email="cc@example.com", name="Duplicate"),
        ],
    )

    assert cc_update_calls == [
        {
            "ticket_id": 42,
            "email_ccs": [
                {"user_email": "CC@example.com", "user_name": "CC", "action": "put"}
            ],
        }
    ]
    assert result.success is True
    assert result.created is False
    assert result.message == "Found existing Zendesk ticket 42; ensured 1 CCs."
    assert result.email_cc_ids == [101]


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_existing_incident_requires_requester_for_ccs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cc_update_calls: list[dict[str, object]] = []
    monkeypatch.setattr(
        zendesk_ops,
        "list_tickets_by_external_id",
        lambda external_id: [{"id": 42, "external_id": "outreach:test"}],
    )

    def _set_ccs(ticket_id: int | str, email_ccs: list[dict[str, str]]) -> dict:
        cc_update_calls.append({"ticket_id": ticket_id, "email_ccs": email_ccs})
        return {"id": ticket_id, "email_cc_ids": [101]}

    monkeypatch.setattr(zendesk_ops, "set_ticket_email_ccs", _set_ccs)

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:test",
        ticket_type="incident",
        problem_id=99,
        subject="A subject",
        internal_note_html="<p>A note</p>",
        cc=[zendesk_ops.OutreachContact(email="cc@example.com", name="CC")],
    )

    assert result.success is False
    assert result.created is False
    assert result.message == "`requester` is required for an incident."
    assert cc_update_calls == []


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_existing_incident_skips_requester_cc(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_ops,
        "list_tickets_by_external_id",
        lambda external_id: [{"id": 42, "external_id": "outreach:test"}],
    )
    monkeypatch.setattr(
        zendesk_ops,
        "set_ticket_email_ccs",
        lambda *args, **kwargs: pytest.fail("empty CC updates must be skipped"),
    )

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:test",
        ticket_type="incident",
        problem_id=99,
        subject="A subject",
        internal_note_html="<p>A note</p>",
        requester=zendesk_ops.OutreachContact(
            email="cc@example.com",
            name="Requester",
        ),
        cc=[zendesk_ops.OutreachContact(email="CC@example.com", name="CC")],
    )

    assert result.success is True
    assert result.created is False
    assert result.message == "Found existing Zendesk ticket 42; ensured 0 CCs."


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_existing_incident_reports_cc_update_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_ops,
        "list_tickets_by_external_id",
        lambda external_id: [{"id": 42, "external_id": "outreach:test"}],
    )

    def _fail_cc_update(
        ticket_id: int | str,
        email_ccs: list[dict[str, str]],
    ) -> dict:
        raise ZendeskAPIError("Zendesk unavailable")

    monkeypatch.setattr(zendesk_ops, "set_ticket_email_ccs", _fail_cc_update)

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:test",
        ticket_type="incident",
        problem_id=99,
        subject="A subject",
        internal_note_html="<p>A note</p>",
        requester=zendesk_ops.OutreachContact(
            email="requester@example.com",
            name="Requester",
        ),
        cc=[zendesk_ops.OutreachContact(email="cc@example.com", name="CC")],
    )

    assert result.success is False
    assert result.created is False
    assert result.ticket_id == 42
    assert "Zendesk unavailable" in result.message


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_reports_duplicate_external_ids(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_ops,
        "list_tickets_by_external_id",
        lambda external_id: [{"id": 42}, {"id": 43}],
    )
    monkeypatch.setattr(
        zendesk_ops,
        "create_ticket",
        lambda payload: pytest.fail("duplicate tickets must not be created"),
    )

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:duplicate",
        ticket_type="problem",
        subject="A subject",
        internal_note_html="<p>A note</p>",
    )

    assert result.success is False
    assert result.created is False
    assert result.duplicate_ticket_ids == [42, 43]


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_detects_post_create_duplicates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    external_id_lookups: list[str] = []

    def _list_tickets(external_id: str) -> list[dict]:
        external_id_lookups.append(external_id)
        if len(external_id_lookups) == 1:
            return []
        return [{"id": 42}, {"id": 43}]

    monkeypatch.setattr(zendesk_ops, "list_tickets_by_external_id", _list_tickets)
    monkeypatch.setattr(
        zendesk_ops,
        "get_current_user",
        lambda: {"id": 7, "email": "moonbot@example.com"},
    )
    monkeypatch.setattr(zendesk_ops, "find_ticket_form_id", lambda name: 11)
    monkeypatch.setattr(zendesk_ops, "create_ticket", lambda payload: {"id": 42})

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:post-create-duplicate",
        ticket_type="problem",
        subject="A subject",
        internal_note_html="<p>A note</p>",
    )

    assert external_id_lookups == [
        "outreach:post-create-duplicate",
        "outreach:post-create-duplicate",
    ]
    assert result.success is False
    assert result.created is True
    assert result.ticket_id == 42
    assert result.duplicate_ticket_ids == [42, 43]
    assert result.message == (
        "Created ticket 42 but found duplicate tickets for this external ID: "
        "42, 43; resolve manually."
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "ticket_type,problem_id,requester,error_text",
    [
        pytest.param(
            "incident",
            None,
            {"email": "r@e.io", "name": "R"},
            "required",
            id="incident-needs-problem",
        ),
        pytest.param("problem", 42, None, "not allowed", id="problem-forbids-problem"),
        pytest.param(
            "problem",
            None,
            {"email": "r@e.io", "name": "R"},
            "not allowed for a problem",
            id="problem-forbids-requester",
        ),
        pytest.param("incident", 42, None, "requester", id="incident-needs-requester"),
    ],
)
def test_create_zendesk_outreach_ticket_rejects_invalid_problem_inputs(
    monkeypatch: pytest.MonkeyPatch,
    ticket_type: str,
    problem_id: int | None,
    requester: dict[str, str] | None,
    error_text: str,
) -> None:
    monkeypatch.setattr(zendesk_ops, "list_tickets_by_external_id", lambda value: [])
    monkeypatch.setattr(
        zendesk_ops,
        "get_current_user",
        lambda: pytest.fail("invalid inputs must be rejected before user lookup"),
    )

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:invalid",
        ticket_type=ticket_type,  # type: ignore[arg-type]
        subject="A subject",
        internal_note_html="<p>A note</p>",
        problem_id=problem_id,
        requester=(
            zendesk_ops.OutreachContact(**requester) if requester is not None else None
        ),
    )

    assert result.success is False
    assert error_text in result.message


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_rejects_cc_for_problem(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_calls: list[dict[str, object]] = []
    monkeypatch.setattr(zendesk_ops, "list_tickets_by_external_id", lambda value: [])
    monkeypatch.setattr(
        zendesk_ops,
        "get_current_user",
        lambda: pytest.fail("invalid inputs must be rejected before user lookup"),
    )
    monkeypatch.setattr(
        zendesk_ops,
        "create_ticket",
        lambda payload: create_calls.append(payload),
    )

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:problem-cc",
        ticket_type="problem",
        subject="A subject",
        internal_note_html="<p>A note</p>",
        cc=[zendesk_ops.OutreachContact(email="customer@example.com", name="Customer")],
    )

    assert result.success is False
    assert "`cc` is not allowed for a problem ticket." in result.message
    assert create_calls == []


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_problem_uses_current_user_as_requester(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    monkeypatch.setattr(zendesk_ops, "list_tickets_by_external_id", lambda value: [])
    monkeypatch.setattr(
        zendesk_ops,
        "get_current_user",
        lambda: {"id": 7, "email": "moonbot@example.com"},
    )
    monkeypatch.setattr(zendesk_ops, "find_ticket_form_id", lambda name: 11)
    monkeypatch.setattr(
        zendesk_ops,
        "set_ticket_email_ccs",
        lambda *args, **kwargs: pytest.fail("tickets without CCs must not be updated"),
    )

    def _create(payload: dict[str, object]) -> dict:
        captured["payload"] = payload
        return {"id": 42}

    monkeypatch.setattr(zendesk_ops, "create_ticket", _create)

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:problem",
        ticket_type="problem",
        subject="A subject",
        internal_note_html="<p>A note</p>",
    )

    payload = captured["payload"]
    assert isinstance(payload, dict)
    assert payload["requester_id"] == 7
    assert payload["submitter_id"] == 7
    assert result.requester_id == 7
    assert result.submitter_id == 7


@pytest.mark.unit
def test_create_zendesk_outreach_incident_includes_problem_and_requester(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    monkeypatch.setattr(zendesk_ops, "list_tickets_by_external_id", lambda value: [])
    monkeypatch.setattr(
        zendesk_ops,
        "get_current_user",
        lambda: {"id": 7, "email": "moonbot@example.com"},
    )
    monkeypatch.setattr(zendesk_ops, "find_ticket_form_id", lambda name: 11)

    def _create(payload: dict[str, object]) -> dict:
        captured["payload"] = payload
        return {"id": 42, "problem_id": 99}

    monkeypatch.setattr(zendesk_ops, "create_ticket", _create)

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:incident",
        ticket_type="incident",
        problem_id=99,
        subject="A subject",
        internal_note_html="<p>A note</p>",
        requester=zendesk_ops.OutreachContact(
            email="requester@example.com",
            name="Requester",
        ),
    )

    payload = captured["payload"]
    assert isinstance(payload, dict)
    assert payload["problem_id"] == 99
    assert payload["requester"] == {
        "name": "Requester",
        "email": "requester@example.com",
    }
    assert result.success is True
    assert result.problem_id == 99


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_rejects_more_than_48_unique_ccs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(zendesk_ops, "list_tickets_by_external_id", lambda value: [])
    monkeypatch.setattr(
        zendesk_ops,
        "get_current_user",
        lambda: {"id": 7, "email": "moonbot@example.com"},
    )
    monkeypatch.setattr(
        zendesk_ops,
        "find_ticket_form_id",
        lambda name: pytest.fail("too many CCs must be rejected before form lookup"),
    )
    contacts = [
        zendesk_ops.OutreachContact(email=f"user{index}@example.com", name=str(index))
        for index in range(49)
    ]

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="outreach:too-many-ccs",
        ticket_type="incident",
        problem_id=99,
        subject="A subject",
        internal_note_html="<p>A note</p>",
        requester=zendesk_ops.OutreachContact(
            email="requester@example.com",
            name="Requester",
        ),
        cc=contacts,
    )

    assert result.success is False
    assert "48" in result.message


@pytest.mark.unit
def test_create_zendesk_outreach_ticket_rejects_bad_external_id_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_ops,
        "list_tickets_by_external_id",
        lambda value: pytest.fail("bad idempotency keys must be rejected first"),
    )

    result = zendesk_ops.create_zendesk_outreach_ticket(
        external_id="support:bad",
        ticket_type="problem",
        subject="A subject",
        internal_note_html="<p>A note</p>",
    )

    assert result.success is False
    assert "outreach:" in result.message


@pytest.mark.unit
def test_search_zendesk_tickets_prefixes_ticket_type_and_rejects_other_types(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    queries: list[str] = []

    def _fake_search(
        query: str,
        *,
        sort_by: str | None = None,
        sort_order: str = "desc",
        max_results: int = 100,
    ) -> list[dict]:
        queries.append(query)
        return [
            {
                "id": 42,
                "subject": "Support",
                "url": "https://airbyte1416.zendesk.com/api/v2/tickets/42.json",
            }
        ]

    monkeypatch.setattr(zendesk_ops, "search", _fake_search)

    result = zendesk_ops.search_zendesk_tickets(query="status:open", limit=10)
    explicit_type = zendesk_ops.search_zendesk_tickets(query="type:ticket status:open")
    rejected = zendesk_ops.search_zendesk_tickets(query="type:organization foo")

    assert result.success is True
    assert result.count == 1
    assert result.tickets[0].url == "https://airbyte1416.zendesk.com/agent/tickets/42"
    assert explicit_type.success is True
    assert queries == ["type:ticket status:open", "type:ticket status:open"]
    assert rejected.success is False
    assert "type:ticket" in rejected.message


@pytest.mark.unit
def test_search_zendesk_tickets_rejects_negated_type_without_search(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_ops,
        "search",
        lambda *args, **kwargs: pytest.fail("negated types must not be searched"),
    )

    result = zendesk_ops.search_zendesk_tickets(query="-type:ticket foo")

    assert result.success is False
    assert result.count == 0
    assert "negated type" in result.message


@pytest.mark.unit
def test_search_zendesk_tickets_rejects_user_type_without_search(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_ops,
        "search",
        lambda *args, **kwargs: pytest.fail("non-ticket types must not be searched"),
    )

    result = zendesk_ops.search_zendesk_tickets(query="type:user")

    assert result.success is False
    assert result.count == 0
    assert "type:ticket" in result.message


@pytest.mark.unit
def test_find_zendesk_organization_by_airbyte_org_id_maps_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        zendesk_ops,
        "find_organizations_by_airbyte_org_id",
        lambda org_id: [{"id": 42, "name": "Airbyte", "url": "https://example.org/42"}],
    )

    result = zendesk_ops.find_zendesk_organization_by_airbyte_org_id(
        "11111111-1111-1111-1111-111111111111"
    )

    assert result.success is True
    assert len(result.organizations) == 1
    assert result.organizations[0].id == 42
    assert result.organizations[0].name == "Airbyte"
