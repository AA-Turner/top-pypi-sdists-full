# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for Project Lighthouse trigger processing."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import google.auth.exceptions
import pytest

from airbyte_ops_mcp.lighthouse import job

RUN_DATE = date(2026, 10, 22)
ORG_ID = "11111111-1111-1111-1111-111111111111"
WORKSPACE_ID = "22222222-2222-2222-2222-222222222222"


def _connection(**overrides: Any) -> dict[str, Any]:
    return {
        "connection_id": "connection-1",
        "workspace_id": WORKSPACE_ID,
        "connection_name": "Orders",
        "source_connector_name": "Postgres",
        "destination_connector_name": "Snowflake",
        "cloud_url": "https://cloud.airbyte.com/workspaces/workspace/connections/connection",
        "last_error": "A sync failed",
        "usd_ok_30d": 125.5,
        "days_of_syncs": 45,
        "conn_rank": 2,
        **overrides,
    }


def _fire(trigger_type: str, **overrides: Any) -> dict[str, Any]:
    return {
        "organization_id": ORG_ID,
        "trigger_type": trigger_type,
        "fire_date": RUN_DATE,
        "profile_month_end": date(2026, 9, 30),
        "account_id": "account-1",
        "account_name": "Example Account",
        "is_personal_email": False,
        "self_serve_arr": 12500.2,
        "n_connections_with_jobs": 4,
        "n_connections_failing": 2,
        "connections": [_connection()],
        **overrides,
    }


def test_prod_db_credentials_unavailable_without_default_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing_credentials() -> None:
        raise google.auth.exceptions.DefaultCredentialsError(
            "No default credentials available"
        )

    monkeypatch.setattr(
        job, "get_gcp_credentials_for_prod_db_replica", missing_credentials
    )

    assert job._prod_db_credentials_available() is False


def test_prod_db_credentials_available_with_resolved_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(job, "get_gcp_credentials_for_prod_db_replica", object)

    assert job._prod_db_credentials_available() is True


@pytest.mark.parametrize(
    ("trigger_type", "reason", "subject", "draft_fragment"),
    [
        (
            "biggest_off",
            "biggest connection (Postgres → Snowflake) turned off after 45 days of syncs",
            "Airbyte // Checking in on your Postgres → Snowflake connection",
            "turned off on 2026-10-19",
        ),
        (
            "top3_failing",
            "#2 connection (Postgres → Snowflake) failing 3 days in a row",
            "Airbyte // Your Postgres → Snowflake connection is failing",
            "failed every sync since 2026-10-20",
        ),
        (
            "half_failing",
            "2 of 4 connections failing for 3 days",
            "Airbyte // Several of your connections are failing",
            "2 of your 4 connections",
        ),
    ],
)
def test_reason_subject_and_draft(
    trigger_type: str, reason: str, subject: str, draft_fragment: str
) -> None:
    fire = _fire(trigger_type)
    assert job.render_reason(fire) == reason
    assert job.render_subject(fire) == subject
    assert draft_fragment in job.render_draft(fire, requester_name="Alex Example")
    assert job.render_draft(fire, requester_name="Alex Example").startswith("Hi Alex,")


def test_biggest_off_renders_three_plus_months() -> None:
    fire = _fire("biggest_off", connections=[_connection(days_of_syncs=90)])
    assert "after 3+ months of syncs" in job.render_reason(fire)


def test_top3_draft_omits_empty_last_error_sentence() -> None:
    fire = _fire("top3_failing", connections=[_connection(last_error="")])
    draft = job.render_draft(fire)
    assert "latest error" not in draft
    assert "failed every sync since 2026-10-20." in draft


def test_render_markdown_links_only_airbyte_cloud_connection_urls() -> None:
    markdown = job.render_markdown(
        [
            {"connection_url": "https://cloud.airbyte.com/workspaces/a"},
            {"connection_url": "https://cloud.airbyte.io/workspaces/b"},
            {"connection_url": "https://cloud.airbyte.com.evil.example/workspaces/c"},
        ]
    )

    assert "[connection](https://cloud.airbyte.com/workspaces/a)" in markdown
    assert "[connection](https://cloud.airbyte.io/workspaces/b)" in markdown
    assert (
        "[connection](https://cloud.airbyte.com.evil.example/workspaces/c)"
        not in markdown
    )
    assert "`https://cloud.airbyte.com.evil.example/workspaces/c`" in markdown


def test_half_failing_draft_lists_each_connection() -> None:
    fire = _fire(
        "half_failing",
        connections=[
            _connection(connection_name="Orders"),
            _connection(
                connection_id="connection-2",
                connection_name="Users",
                source_connector_name="MySQL",
                destination_connector_name="BigQuery",
            ),
        ],
    )
    draft = job.render_draft(fire)
    assert "- Postgres → Snowflake (Orders)" in draft
    assert "- MySQL → BigQuery (Users)" in draft


def test_action_decision_ordering_and_cooldown() -> None:
    fire = _fire("biggest_off")
    existing = {"id": 11, "external_id": "lighthouse:some:key"}
    assert job.choose_action(
        fire,
        existing_for_key=[existing],
        indexed_tickets=[],
        run_date=RUN_DATE,
    ) == ("skip_exists", existing)
    open_ticket = {
        "id": 12,
        "status": "open",
        "external_id": f"lighthouse:{ORG_ID}:top3_failing:2026-10-01",
    }
    assert job.choose_action(
        fire,
        existing_for_key=[],
        indexed_tickets=[open_ticket],
        run_date=RUN_DATE,
    ) == ("note", open_ticket)
    recently_closed_same_trigger = {
        "id": 13,
        "status": "solved",
        "updated_at": "2026-10-01T12:00:00Z",
        "external_id": f"lighthouse:{ORG_ID}:biggest_off:2026-10-01",
    }
    assert job.choose_action(
        fire,
        existing_for_key=[],
        indexed_tickets=[recently_closed_same_trigger],
        run_date=RUN_DATE,
    ) == ("skip_cooldown", None)
    different_trigger = {
        **recently_closed_same_trigger,
        "external_id": f"lighthouse:{ORG_ID}:top3_failing:2026-10-01",
    }
    assert job.choose_action(
        fire,
        existing_for_key=[],
        indexed_tickets=[different_trigger],
        run_date=RUN_DATE,
    ) == ("create", None)


def test_cooldown_expires_at_30_days_and_ignores_future_updates() -> None:
    fire = _fire("top3_failing")
    ticket = {
        "status": "closed",
        "updated_at": "2026-09-21T00:00:00Z",
        "external_id": f"lighthouse:{ORG_ID}:top3_failing:2026-09-01",
    }
    assert job.choose_action(
        fire, existing_for_key=[], indexed_tickets=[ticket], run_date=RUN_DATE
    ) == ("create", None)
    ticket["updated_at"] = "2026-10-23T00:00:00Z"
    assert job.choose_action(
        fire, existing_for_key=[], indexed_tickets=[ticket], run_date=RUN_DATE
    ) == ("create", None)


def test_note_idempotence_checks_lighthouse_key() -> None:
    key = f"lighthouse:{ORG_ID}:biggest_off:2026-10-22"
    assert job.has_lighthouse_key(
        [{"body": f"Existing note\nLighthouse key: {key}"}], key
    )
    assert not job.has_lighthouse_key([{"body": "Another note"}], key)


def test_requester_order_filters_disabled_internal_and_sorts_activity() -> None:
    contacts = [
        {
            "user_id": "workspace-recent",
            "user_name": "Workspace Recent",
            "user_email": "workspace-recent@example.com",
            "user_status": "active",
            "user_updated_at": "2026-10-01T00:00:00Z",
            "admin_role": "workspace_admin",
        },
        {
            "user_id": "org-later",
            "user_name": "Org Later",
            "user_email": "org-later@example.com",
            "user_status": "active",
            "user_updated_at": "2026-10-02T00:00:00Z",
            "admin_role": "organization_admin",
        },
        {
            "user_id": "org-recent",
            "user_name": "Org Recent",
            "user_email": "org-recent@example.com",
            "user_status": "active",
            "user_updated_at": "2026-09-30T00:00:00Z",
            "admin_role": "organization_admin",
        },
        {
            "user_id": "disabled",
            "user_name": "Disabled",
            "user_email": "disabled@example.com",
            "user_status": "disabled",
            "admin_role": "organization_admin",
        },
        {
            "user_id": "internal",
            "user_name": "Internal",
            "user_email": "internal@airbyte.io",
            "user_status": "active",
            "admin_role": "organization_admin",
        },
    ]
    activities = [
        {"user_id": "org-later", "last_connection_event_at": "2026-10-20T00:00:00Z"},
        {"user_id": "org-recent", "last_connection_event_at": "2026-10-21T00:00:00Z"},
        {
            "user_id": "workspace-recent",
            "last_connection_event_at": "2026-10-22T00:00:00Z",
        },
    ]
    requester, others = job.select_requesters(contacts, activities)
    assert requester is not None
    assert requester["email"] == "org-recent@example.com"
    assert others == ["org-later@example.com", "workspace-recent@example.com"]


def test_requester_selection_keeps_null_status_and_prefers_org_admin() -> None:
    contacts = [
        {
            "user_id": "workspace-admin",
            "user_name": "Workspace Admin",
            "user_email": "workspace@example.com",
            "user_status": None,
            "admin_role": "workspace_admin",
        },
        {
            "user_id": "org-admin",
            "user_name": "Organization Admin",
            "user_email": "organization@example.com",
            "user_status": None,
            "admin_role": "organization_admin",
        },
    ]
    activities = [
        {
            "user_id": "workspace-admin",
            "last_connection_event_at": "2026-10-22T00:00:00Z",
        }
    ]

    requester, others = job.select_requesters(contacts, activities)

    assert requester is not None
    assert requester["email"] == "organization@example.com"
    assert others == ["workspace@example.com"]


def test_no_contact_falls_back_to_moonbot_and_note_warning() -> None:
    requester, others = job.select_requesters([], [])
    assert requester is None
    assert others == []
    note = job.render_internal_note(
        _fire("biggest_off"),
        display_name="Example Account",
        requester_name=None,
        other_admin_emails=[],
        no_contact=True,
    )
    assert "No admin contact found — set the requester before replying." in note
    assert "Hi there," in note


def test_dry_run_writes_plan_without_any_external_writes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(job, "_prod_db_credentials_available", lambda: False)
    monkeypatch.delenv("ZENDESK_SUBDOMAIN", raising=False)
    monkeypatch.delenv("ZENDESK_EMAIL", raising=False)
    monkeypatch.delenv("ZENDESK_API_TOKEN", raising=False)
    monkeypatch.setattr(job, "query_fires", lambda _run_date: [_fire("biggest_off")])
    credentials = object()
    monkeypatch.setattr(job, "resolve_zendesk_credentials", lambda: credentials)
    monkeypatch.setattr(job, "search", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(
        job, "find_organizations_by_airbyte_org_id", lambda *_args, **_kwargs: []
    )
    monkeypatch.setattr(
        job, "list_tickets_by_external_id", lambda *_args, **_kwargs: []
    )
    monkeypatch.setattr(job, "get_current_user", lambda **_kwargs: {"name": "MoonBot"})
    monkeypatch.setattr(job, "find_ticket_form_id", lambda *_args, **_kwargs: 1)
    monkeypatch.setattr(job, "create_ticket", lambda *_args, **_kwargs: pytest.fail())
    monkeypatch.setattr(
        job, "add_internal_note", lambda *_args, **_kwargs: pytest.fail()
    )
    monkeypatch.setattr(job, "add_ticket_tags", lambda *_args, **_kwargs: pytest.fail())
    monkeypatch.setattr(
        job.slack_posting,
        "post_channel_message",
        lambda *_args, **_kwargs: pytest.fail(),
    )
    plan_path = tmp_path / "lighthouse_plan.json"

    result = job.run_lighthouse(RUN_DATE, plan_path=plan_path)

    assert not result.failed
    assert result.actions[0]["action"] == "create"
    assert result.actions[0]["status"] == "dry_run"
    assert plan_path.exists()
    assert json.loads(plan_path.read_text())["actions"][0]["action"] == "create"


def test_plan_and_markdown_redact_admin_pii_only_when_serialized(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    summary_path = tmp_path / "step-summary.md"
    plan_path = tmp_path / "lighthouse_plan.json"

    def missing_zendesk_credentials() -> None:
        raise job.ZendeskAPIError("Zendesk credentials unavailable")

    monkeypatch.setattr(job, "_prod_db_credentials_available", lambda: True)
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary_path))
    monkeypatch.setattr(job, "query_fires", lambda _run_date: [_fire("biggest_off")])
    monkeypatch.setattr(job, "resolve_zendesk_credentials", missing_zendesk_credentials)
    monkeypatch.setattr(
        job,
        "_requester_for_fire",
        lambda *_args: (
            {"name": "Primary Admin Person", "email": "primary@example.com"},
            ["other@example.net"],
        ),
    )

    result = job.run_lighthouse(RUN_DATE, plan_path=plan_path)

    assert result.failed
    assert result.errors == ["Zendesk credentials unavailable (ZendeskAPIError)."]
    assert result.errors[0] in caplog.text
    plan_text = plan_path.read_text()
    summary_text = summary_path.read_text()
    serialized_action = json.loads(plan_text)["actions"][0]
    ticket_payload = serialized_action["ticket_payload"]
    assert "@" not in result.markdown
    assert "@" not in summary_text
    assert "@" not in plan_text
    assert "Primary Admin Person" not in summary_text
    assert "Primary Admin Person" not in plan_text
    assert "other@example.net" not in plan_text
    requester_row = next(
        row
        for row in result.markdown.splitlines()
        if row.startswith("| ") and "| biggest_off |" in row
    )
    requester_cells = [cell.strip() for cell in requester_row.split("|")]
    assert requester_cells[7] == "example.com"
    assert serialized_action["requester_email"] == "example.com"
    assert serialized_action["other_admin_emails"] == ["example.net"]
    assert "requester_name" not in serialized_action
    assert "internal_note_html" not in serialized_action
    assert "draft" not in serialized_action
    assert "requester" not in ticket_payload
    assert ticket_payload["comment"]["html_body"] == "[redacted]"
    assert result.actions[0]["requester_email"] == "primary@example.com"
    assert (
        result.actions[0]["ticket_payload"]["requester"]["email"]
        == "primary@example.com"
    )


def test_bigquery_failure_includes_exception_text(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    def fail_query(_run_date: Any) -> list[dict[str, Any]]:
        raise Exception("Access Denied: Table x")

    plan_path = tmp_path / "lighthouse_plan.json"
    monkeypatch.setattr(job, "query_fires", fail_query)

    result = job.run_lighthouse(RUN_DATE, plan_path=plan_path)

    message = "BigQuery trigger query failed (Exception: Access Denied: Table x)."
    assert result.errors == [message]
    assert message in caplog.text
    assert "Access Denied" in plan_path.read_text()


def test_bigquery_failure_truncates_exception_text(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    exception_text = "Access Denied: " + "x" * 600

    def fail_query(_run_date: Any) -> list[dict[str, Any]]:
        raise Exception(exception_text)

    monkeypatch.setattr(
        job,
        "query_fires",
        fail_query,
    )

    result = job.run_lighthouse(RUN_DATE, plan_path=tmp_path / "plan.json")

    assert result.errors == [
        f"BigQuery trigger query failed (Exception: {exception_text[:500]})."
    ]


def test_live_run_without_slack_token_does_not_change_tickets(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    for name in (
        "SLACK_BOT_TOKEN",
        "SLACK_BOT_TOKEN_HITL",
        "SLACK_BOT_TOKEN_AIRBYTE_TEAM",
        "SLACK_HYDRA_BOT_TOKEN",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(job, "_prod_db_credentials_available", lambda: False)
    credentials = type("Credentials", (), {"subdomain": "example"})()
    monkeypatch.setattr(job, "query_fires", lambda _run_date: [_fire("biggest_off")])
    monkeypatch.setattr(job, "resolve_zendesk_credentials", lambda: credentials)
    monkeypatch.setattr(job, "search", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(
        job, "find_organizations_by_airbyte_org_id", lambda *_args, **_kwargs: []
    )
    monkeypatch.setattr(
        job, "list_tickets_by_external_id", lambda *_args, **_kwargs: []
    )
    monkeypatch.setattr(
        job,
        "create_ticket",
        lambda *_args, **_kwargs: pytest.fail("ticket creation must not run"),
    )
    monkeypatch.setattr(
        job,
        "add_internal_note",
        lambda *_args, **_kwargs: pytest.fail("ticket note must not run"),
    )
    monkeypatch.setattr(
        job,
        "add_ticket_tags",
        lambda *_args, **_kwargs: pytest.fail("ticket tagging must not run"),
    )

    result = job.run_lighthouse(RUN_DATE, live=True, plan_path=tmp_path / "plan.json")

    assert result.failed
    assert result.actions[0]["action"] == "error"
    assert "Slack bot token is unavailable" in result.actions[0]["error"]


def test_search_indexes_older_open_tickets_and_deduplicates_by_id(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    fire = _fire("biggest_off")
    credentials = type("Credentials", (), {"subdomain": "example"})()
    recent_ticket = {
        "id": 101,
        "external_id": "lighthouse:another-org:top3_failing:2026-10-22",
        "status": "open",
        "updated_at": "2026-10-21T00:00:00Z",
    }
    old_open_ticket = {
        "id": 202,
        "external_id": (
            f"lighthouse:{fire['organization_id']}:top3_failing:2025-01-01"
        ),
        "status": "hold",
        "updated_at": "2026-01-01T00:00:00Z",
    }
    search_queries: list[str] = []
    indexed_ticket_ids: list[int] = []
    original_choose_action = job.choose_action

    def fake_search(query: str, **_kwargs: Any) -> list[dict[str, Any]]:
        search_queries.append(query)
        if "status<solved" in query:
            return [recent_ticket, old_open_ticket, old_open_ticket]
        return [recent_ticket]

    def capture_index(
        fire: dict[str, Any],
        *,
        existing_for_key: list[dict[str, Any]],
        indexed_tickets: list[dict[str, Any]],
        run_date: Any,
    ) -> tuple[str, dict[str, Any] | None]:
        indexed_ticket_ids.extend(ticket["id"] for ticket in indexed_tickets)
        return original_choose_action(
            fire,
            existing_for_key=existing_for_key,
            indexed_tickets=indexed_tickets,
            run_date=run_date,
        )

    monkeypatch.setattr(job, "_prod_db_credentials_available", lambda: False)
    monkeypatch.setattr(job, "query_fires", lambda _run_date: [fire])
    monkeypatch.setattr(job, "resolve_zendesk_credentials", lambda: credentials)
    monkeypatch.setattr(job, "search", fake_search)
    monkeypatch.setattr(job, "choose_action", capture_index)
    monkeypatch.setattr(
        job, "list_tickets_by_external_id", lambda *_args, **_kwargs: []
    )
    monkeypatch.setattr(job, "get_ticket_comments", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(
        job, "get_current_user", lambda **_kwargs: {"id": 99, "name": "MoonBot"}
    )
    monkeypatch.setattr(
        job, "find_organizations_by_airbyte_org_id", lambda *_args, **_kwargs: []
    )

    result = job.run_lighthouse(RUN_DATE, plan_path=tmp_path / "plan.json")

    assert len(search_queries) == 2
    assert search_queries[1] == "type:ticket tags:lighthouse status<solved"
    assert indexed_ticket_ids == [101, 202]
    assert result.actions[0]["action"] == "note"
    assert result.actions[0]["ticket_id"] == 202


def test_second_trigger_notes_on_ticket_created_earlier_in_same_run(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    fire_one = _fire("biggest_off")
    fire_two = _fire("top3_failing")
    tickets: list[dict[str, Any]] = []
    notes: list[tuple[Any, str]] = []
    tagged: list[tuple[Any, list[str]]] = []
    posted: list[tuple[str, str | None]] = []
    credentials = type("Credentials", (), {"subdomain": "example"})()
    monkeypatch.setattr(job, "_prod_db_credentials_available", lambda: False)
    monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)
    monkeypatch.delenv("SLACK_BOT_TOKEN_HITL", raising=False)
    monkeypatch.delenv("SLACK_BOT_TOKEN_AIRBYTE_TEAM", raising=False)
    monkeypatch.setenv("SLACK_HYDRA_BOT_TOKEN", "xoxb-test-hydra")
    monkeypatch.setattr(job, "query_fires", lambda _run_date: [fire_one, fire_two])
    monkeypatch.setattr(job, "resolve_zendesk_credentials", lambda: credentials)
    monkeypatch.setattr(job, "search", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(
        job,
        "find_organizations_by_airbyte_org_id",
        lambda *_args, **_kwargs: [{"id": 23, "name": "Zendesk Org"}],
    )
    monkeypatch.setattr(
        job,
        "get_current_user",
        lambda **_kwargs: {"id": 99, "name": "MoonBot", "email": "moonbot@example.com"},
    )
    monkeypatch.setattr(job, "find_ticket_form_id", lambda *_args, **_kwargs: 45)

    def find_by_key(key: str, **_kwargs: Any) -> list[dict[str, Any]]:
        return [ticket for ticket in tickets if ticket["external_id"] == key]

    def create(payload: dict[str, Any], **_kwargs: Any) -> dict[str, Any]:
        ticket = {
            **payload,
            "id": 100,
            "status": "new",
        }
        tickets.append(ticket)
        return ticket

    monkeypatch.setattr(job, "list_tickets_by_external_id", find_by_key)
    monkeypatch.setattr(job, "create_ticket", create)
    monkeypatch.setattr(
        job,
        "get_ticket_comments",
        lambda *_args, **_kwargs: [
            {"body": ticket["comment"]["html_body"]}
            for ticket in tickets
            if ticket["id"] == 100
        ],
    )
    monkeypatch.setattr(
        job,
        "add_internal_note",
        lambda ticket_id, note, **_kwargs: notes.append((ticket_id, note)),
    )
    monkeypatch.setattr(
        job,
        "add_ticket_tags",
        lambda ticket_id, tags, **_kwargs: tagged.append((ticket_id, tags)),
    )
    monkeypatch.setattr(
        job.slack_posting,
        "post_channel_message",
        lambda _channel, text, *, token: posted.append((text, token)),
    )

    result = job.run_lighthouse(RUN_DATE, live=True, plan_path=tmp_path / "plan.json")

    assert not result.failed
    assert [action["action"] for action in result.actions] == ["create", "note"]
    assert len(tickets) == 1
    assert len(notes) == 1
    assert notes[0][0] == 100
    assert "top3_failing" in notes[0][1]
    assert tagged == [(100, ["lighthouse_top3_failing"])]
    assert len(posted) == 2
    assert [token for _, token in posted] == ["xoxb-test-hydra"] * 2
    assert "(added to open ticket)" in posted[1][0]


def test_resource_sql_loads_and_has_date_parameter() -> None:
    sql = job.load_trigger_sql()
    assert "DECLARE me DATE" in sql
    assert "@run_date" in sql
