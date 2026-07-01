"""Tests for search, seeding, and egress behavior across Jira and Linear connectors.

Covers:
- Jira search (query_text, query_key, precedence)  [T011]
- Jira custom field blob write/skip                 [T012]
- Linear search (query_text, query_key, wrong team) [T013]
- Linear custom field skip warning                  [T014]
- Mission seeding from canonical issues             [T015]
- Mission egress comment format and transitions     [T016]
"""

from __future__ import annotations

import json
import logging
from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx
import pytest

from spec_kitty_tracker.connectors.in_memory import InMemoryConnector
from spec_kitty_tracker.connectors.jira import JiraConnector, JiraConnectorConfig
from spec_kitty_tracker.connectors.linear import LinearConnector, LinearConnectorConfig
from spec_kitty_tracker.mission_sync import (
    BidirectionalIssueSync,
    DecisionReference,
    MissionUpdate,
    _render_mission_comment,
    mission_seed_from_issue,
)
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalStatus,
    ExternalRef,
)

# ---------------------------------------------------------------------------
# Canned responses
# ---------------------------------------------------------------------------

_CANNED_JIRA_ISSUE: dict[str, Any] = {
    "id": "10001",
    "key": "IAM-42",
    "fields": {
        "summary": "SCIM provisioning",
        "description": None,
        "status": {"name": "To Do"},
        "priority": {"name": "Medium"},
        "assignee": None,
        "labels": [],
        "issuetype": {"name": "Task"},
        "parent": None,
        "created": "2026-03-01T10:00:00.000+0000",
        "updated": "2026-03-15T14:00:00.000+0000",
    },
}

_CANNED_JIRA_SEARCH_RESPONSE: dict[str, Any] = {
    "issues": [_CANNED_JIRA_ISSUE],
    "total": 1,
}

_CANNED_LINEAR_ISSUE: dict[str, Any] = {
    "id": "issue-uuid-1",
    "identifier": "WEB-123",
    "title": "Add Clerk auth",
    "description": "Implement Clerk authentication",
    "priority": 2,
    "createdAt": "2026-03-01T10:00:00.000Z",
    "updatedAt": "2026-03-15T14:00:00.000Z",
    "url": "https://linear.app/acme/issue/WEB-123",
    "state": {"id": "state-1", "name": "Todo", "type": "unstarted"},
    "labels": {"nodes": [{"name": "backend"}]},
    "assignee": {"id": "user-1"},
    "parent": None,
    "team": {"id": "team-uuid-1"},
}


# ---------------------------------------------------------------------------
# Connector factory helpers
# ---------------------------------------------------------------------------


def _jira_connector(handler, **config_overrides) -> JiraConnector:
    transport = httpx.MockTransport(handler)
    client = httpx.AsyncClient(transport=transport)
    config = JiraConnectorConfig(
        base_url="https://test.atlassian.net",
        email="test@example.com",
        api_token="test-token",
        project_key="IAM",
        **config_overrides,
    )
    return JiraConnector(config, client=client)


def _linear_connector(handler, team_id: str = "team-uuid-1") -> LinearConnector:
    transport = httpx.MockTransport(handler)
    client = httpx.AsyncClient(transport=transport)
    config = LinearConnectorConfig(api_key="test-key", team_id=team_id)
    return LinearConnector(config, client=client)


# ===========================================================================
# T011 — Jira search tests
# ===========================================================================


async def test_jira_list_issues_query_text() -> None:
    """Verify JQL contains text ~ and project = IAM for query_text filter."""
    captured_jql: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET" and "/rest/api/3/search/jql" in str(request.url):
            parsed = urlparse(str(request.url))
            params = parse_qs(parsed.query)
            jql = params["jql"][0]
            captured_jql.append(jql)
            return httpx.Response(200, json=_CANNED_JIRA_SEARCH_RESPONSE)
        return httpx.Response(404)

    connector = _jira_connector(handler)
    page = await connector.list_issues(
        updated_since=None,
        cursor=None,
        limit=50,
        filters={"query_text": "SCIM provisioning"},
    )

    assert len(captured_jql) == 1
    assert 'text ~ "SCIM provisioning"' in captured_jql[0]
    assert "project = IAM" in captured_jql[0]
    assert len(page.items) == 1
    assert page.items[0].ref.key == "IAM-42"


async def test_jira_list_issues_query_key() -> None:
    """Verify JQL is key = "IAM-42" for query_key filter."""
    captured_jql: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET" and "/rest/api/3/search/jql" in str(request.url):
            parsed = urlparse(str(request.url))
            params = parse_qs(parsed.query)
            jql = params["jql"][0]
            captured_jql.append(jql)
            return httpx.Response(200, json=_CANNED_JIRA_SEARCH_RESPONSE)
        return httpx.Response(404)

    connector = _jira_connector(handler)
    page = await connector.list_issues(
        updated_since=None,
        cursor=None,
        limit=50,
        filters={"query_key": "IAM-42"},
    )

    assert len(captured_jql) == 1
    assert captured_jql[0] == 'key = "IAM-42"'
    assert len(page.items) == 1
    assert page.items[0].ref.key == "IAM-42"


async def test_jira_query_key_precedence() -> None:
    """When both query_key and query_text are present, query_key wins."""
    captured_jql: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET" and "/rest/api/3/search/jql" in str(request.url):
            parsed = urlparse(str(request.url))
            params = parse_qs(parsed.query)
            jql = params["jql"][0]
            captured_jql.append(jql)
            return httpx.Response(200, json=_CANNED_JIRA_SEARCH_RESPONSE)
        return httpx.Response(404)

    connector = _jira_connector(handler)
    page = await connector.list_issues(
        updated_since=None,
        cursor=None,
        limit=50,
        filters={"query_key": "IAM-42", "query_text": "foo", "jql": "bar"},
    )

    assert len(captured_jql) == 1
    assert captured_jql[0] == 'key = "IAM-42"'
    assert "text ~" not in captured_jql[0]
    assert "bar" not in captured_jql[0]
    assert len(page.items) == 1


async def test_jira_list_issues_uses_jql_token_pagination() -> None:
    """Jira Cloud search uses /search/jql and nextPageToken pagination."""
    captured_paths: list[str] = []
    captured_tokens: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        parsed = urlparse(str(request.url))
        if request.method == "GET" and parsed.path == "/rest/api/3/search/jql":
            params = parse_qs(parsed.query)
            captured_paths.append(parsed.path)
            captured_tokens.append(params.get("nextPageToken", [None])[0])
            return httpx.Response(
                200,
                json={**_CANNED_JIRA_SEARCH_RESPONSE, "nextPageToken": "page-2"},
            )
        return httpx.Response(404)

    connector = _jira_connector(handler)
    page = await connector.list_issues(
        updated_since=None,
        cursor="page-1",
        limit=50,
        filters={"jql": "project = IAM"},
    )

    assert captured_paths == ["/rest/api/3/search/jql"]
    assert captured_tokens == ["page-1"]
    assert page.next_cursor == "page-2"


# ===========================================================================
# T012 — Jira custom field tests
# ===========================================================================


async def test_jira_custom_field_blob_write() -> None:
    """Connector with spec_kitty_mission_field_id writes custom field in PUT body."""
    captured_put_body: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        if request.method == "PUT" and "/rest/api/3/issue/IAM-42" in url_str:
            body = json.loads(request.content)
            captured_put_body.append(body)
            return httpx.Response(204)
        if request.method == "GET" and "/rest/api/3/issue/IAM-42" in url_str:
            return httpx.Response(200, json=_CANNED_JIRA_ISSUE)
        return httpx.Response(404)

    connector = _jira_connector(handler, spec_kitty_mission_field_id="customfield_10042")
    ref = ExternalRef(
        system="jira",
        workspace="https://test.atlassian.net",
        id="10001",
        key="IAM-42",
        url="https://test.atlassian.net/browse/IAM-42",
    )
    await connector.update_issue(
        ref,
        patch={
            "custom_fields": {
                "spec_kitty_mission": {
                    "mission_id": "m:1",
                    "mission_state": "implement",
                },
            },
        },
        idempotency_key="test-key",
    )

    assert len(captured_put_body) == 1
    fields = captured_put_body[0]["fields"]
    assert "customfield_10042" in fields
    blob = json.loads(fields["customfield_10042"])
    assert blob["mission_id"] == "m:1"
    assert blob["mission_state"] == "implement"


async def test_jira_custom_field_blob_skip(caplog: pytest.LogCaptureFixture) -> None:
    """Connector without spec_kitty_mission_field_id skips custom field and logs warning."""
    captured_put_body: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        if request.method == "PUT" and "/rest/api/3/issue/IAM-42" in url_str:
            body = json.loads(request.content)
            captured_put_body.append(body)
            return httpx.Response(204)
        if request.method == "GET" and "/rest/api/3/issue/IAM-42" in url_str:
            return httpx.Response(200, json=_CANNED_JIRA_ISSUE)
        return httpx.Response(404)

    connector = _jira_connector(handler)  # no spec_kitty_mission_field_id
    ref = ExternalRef(
        system="jira",
        workspace="https://test.atlassian.net",
        id="10001",
        key="IAM-42",
        url="https://test.atlassian.net/browse/IAM-42",
    )
    with caplog.at_level(logging.WARNING):
        await connector.update_issue(
            ref,
            patch={
                "custom_fields": {
                    "spec_kitty_mission": {
                        "mission_id": "m:1",
                        "mission_state": "implement",
                    },
                },
            },
            idempotency_key="test-key",
        )

    # No PUT should be sent since custom_fields was the only field and it was skipped
    assert len(captured_put_body) == 0
    assert any("spec_kitty_mission_field_id not configured" in r.message for r in caplog.records)


# ===========================================================================
# T013 — Linear search tests
# ===========================================================================


async def test_linear_list_issues_query_text() -> None:
    """Verify GraphQL variables contain filter with title.containsIgnoreCase."""
    captured_variables: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        captured_variables.append(body.get("variables", {}))
        return httpx.Response(
            200,
            json={
                "data": {
                    "issues": {
                        "nodes": [_CANNED_LINEAR_ISSUE],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    }
                }
            },
        )

    connector = _linear_connector(handler)
    page = await connector.list_issues(
        updated_since=None,
        cursor=None,
        limit=50,
        filters={"query_text": "Clerk"},
    )

    assert len(captured_variables) == 1
    filter_expr = captured_variables[0]["filter"]
    assert filter_expr["title"]["containsIgnoreCase"] == "Clerk"
    assert len(page.items) == 1


async def test_linear_list_issues_query_key() -> None:
    """Verify GraphQL query uses GetIssue (not ListIssues) for query_key, with team validation."""
    captured_bodies: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        captured_bodies.append(body)
        return httpx.Response(
            200,
            json={"data": {"issue": _CANNED_LINEAR_ISSUE}},
        )

    connector = _linear_connector(handler)
    page = await connector.list_issues(
        updated_since=None,
        cursor=None,
        limit=50,
        filters={"query_key": "WEB-123"},
    )

    assert len(captured_bodies) == 1
    query_str = captured_bodies[0]["query"]
    assert "GetIssue" in query_str
    assert "issue(id:" in query_str.replace(" ", "").replace("\n", "")
    variables = captured_bodies[0]["variables"]
    assert variables["id"] == "WEB-123"
    assert len(page.items) == 1
    assert page.items[0].ref.key == "WEB-123"


async def test_linear_query_key_wrong_team() -> None:
    """Issue exists but team.id differs from config; returns empty page."""

    def handler(request: httpx.Request) -> httpx.Response:
        wrong_team_issue = dict(_CANNED_LINEAR_ISSUE)
        wrong_team_issue["team"] = {"id": "other-team-uuid"}
        return httpx.Response(
            200,
            json={"data": {"issue": wrong_team_issue}},
        )

    connector = _linear_connector(handler, team_id="team-uuid-1")
    page = await connector.list_issues(
        updated_since=None,
        cursor=None,
        limit=50,
        filters={"query_key": "WEB-123"},
    )

    assert len(page.items) == 0


# ===========================================================================
# T014 — Linear custom field skip test
# ===========================================================================


async def test_linear_custom_field_skip_warn(caplog: pytest.LogCaptureFixture) -> None:
    """Linear logs warning for custom_fields and excludes them from GraphQL mutation."""
    captured_mutations: list[dict[str, Any]] = []
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        body = json.loads(request.content)
        query_str = body.get("query", "")
        call_count += 1

        if "issueUpdate" in query_str:
            captured_mutations.append(body)
            return httpx.Response(
                200,
                json={"data": {"issueUpdate": {"success": True}}},
            )
        # Re-fetch after update (get_issue call)
        if "GetIssue" in query_str or "issue(id:" in query_str.replace(" ", ""):
            # Return issue without team field (not needed for get_issue)
            issue_without_team = {k: v for k, v in _CANNED_LINEAR_ISSUE.items() if k != "team"}
            return httpx.Response(
                200,
                json={"data": {"issue": issue_without_team}},
            )
        return httpx.Response(400, json={"errors": [{"message": "unexpected query"}]})

    connector = _linear_connector(handler)
    ref = ExternalRef(
        system="linear",
        workspace="linear",
        id="issue-uuid-1",
        key="WEB-123",
        url="https://linear.app/acme/issue/WEB-123",
    )
    with caplog.at_level(logging.WARNING):
        await connector.update_issue(
            ref,
            patch={
                "title": "Updated",
                "custom_fields": {
                    "spec_kitty_mission": {
                        "mission_id": "m:1",
                        "mission_state": "implement",
                    },
                },
            },
            idempotency_key="test-key",
        )

    # Verify warning logged
    assert any("Linear does not support custom field" in r.message for r in caplog.records)

    # Verify mutation was sent with title but NOT custom fields
    assert len(captured_mutations) == 1
    mutation_input = captured_mutations[0]["variables"]["input"]
    assert mutation_input["title"] == "Updated"
    assert "custom_fields" not in mutation_input
    assert "spec_kitty_mission" not in mutation_input


# ===========================================================================
# T015 — Mission seeding tests
# ===========================================================================


async def test_mission_seed_from_jira_issue() -> None:
    """mission_seed_from_issue produces complete ref fields for a Jira issue."""
    issue = CanonicalIssue(
        ref=ExternalRef(
            system="jira",
            workspace="https://test.atlassian.net",
            id="10001",
            key="IAM-42",
            url="https://test.atlassian.net/browse/IAM-42",
        ),
        title="SCIM provisioning",
        body="Implement SCIM",
        status=CanonicalStatus.TODO,
        issue_type=CanonicalIssueType.TASK,
    )

    seed = mission_seed_from_issue(issue)

    assert seed.source_issue_ref.system == "jira"
    assert seed.source_issue_ref.key == "IAM-42"
    assert seed.source_issue_ref.url is not None
    assert seed.source_issue_ref.url == "https://test.atlassian.net/browse/IAM-42"
    assert seed.title == "SCIM provisioning"
    assert seed.mission_id == "mission:jira:https://test.atlassian.net:10001"


async def test_mission_seed_from_linear_issue() -> None:
    """mission_seed_from_issue produces complete ref fields for a Linear issue."""
    issue = CanonicalIssue(
        ref=ExternalRef(
            system="linear",
            workspace="linear",
            id="issue-uuid-1",
            key="WEB-123",
            url="https://linear.app/acme/issue/WEB-123",
        ),
        title="Add Clerk auth",
        body="Implement Clerk authentication",
        status=CanonicalStatus.TODO,
        issue_type=CanonicalIssueType.TASK,
    )

    seed = mission_seed_from_issue(issue)

    assert seed.source_issue_ref.system == "linear"
    assert seed.source_issue_ref.key == "WEB-123"
    assert seed.source_issue_ref.url is not None
    assert seed.source_issue_ref.url == "https://linear.app/acme/issue/WEB-123"
    assert seed.title == "Add Clerk auth"


# ===========================================================================
# T016 — Mission egress tests
# ===========================================================================


def _make_full_update() -> MissionUpdate:
    """Build a MissionUpdate with all fields populated."""
    return MissionUpdate(
        mission_id="mission:test:1",
        mission_state="implement",
        target_status=CanonicalStatus.IN_PROGRESS,
        summary="Work is in progress",
        mission_url="https://missions.example.com/m/1",
        decision_references=[
            DecisionReference(decision_id="DEC-001", summary="Approved approach"),
            DecisionReference(decision_id="DEC-002", summary="Budget OK"),
        ],
    )


def _make_in_memory_connector_with_issue() -> tuple[InMemoryConnector, ExternalRef]:
    """Create an InMemoryConnector with a pre-seeded issue, return (connector, ref)."""
    connector = InMemoryConnector(name="test", workspace="test-ws")
    ref = ExternalRef(system="test", workspace="test-ws", id="issue-1", key="TST-1")
    issue = CanonicalIssue(
        ref=ref,
        title="Test issue",
        body="Body text",
        status=CanonicalStatus.TODO,
        issue_type=CanonicalIssueType.TASK,
    )
    connector._issues[ref.identity] = issue
    return connector, ref


async def test_publish_mission_update_comment_format() -> None:
    """Verify _render_mission_comment line ordering for a full update."""
    update = _make_full_update()
    comment = _render_mission_comment(update)
    lines = comment.split("\n")

    assert len(lines) == 5
    assert lines[0] == "Spec Kitty mission update: mission:test:1"
    assert lines[1] == "State: implement"
    assert lines[2] == "Summary: Work is in progress"
    assert lines[3] == "Mission: https://missions.example.com/m/1"
    assert lines[4] == "Decision refs: DEC-001, DEC-002"

    # Verify minimal update (only required fields)
    minimal_update = MissionUpdate(
        mission_id="mission:test:2",
        mission_state="specify",
    )
    minimal_comment = _render_mission_comment(minimal_update)
    minimal_lines = minimal_comment.split("\n")
    assert len(minimal_lines) == 2
    assert minimal_lines[0] == "Spec Kitty mission update: mission:test:2"
    assert minimal_lines[1] == "State: specify"

    # Verify empty strings treated as absent
    empty_update = MissionUpdate(
        mission_id="mission:test:3",
        mission_state="plan",
        summary="",
        mission_url="",
    )
    empty_comment = _render_mission_comment(empty_update)
    empty_lines = empty_comment.split("\n")
    assert len(empty_lines) == 2


async def test_publish_mission_update_status_transition() -> None:
    """publish_mission_update with target_status calls update_issue with status in patch."""
    connector, ref = _make_in_memory_connector_with_issue()
    sync = BidirectionalIssueSync(connector=connector)

    update = _make_full_update()  # target_status = IN_PROGRESS
    result = await sync.publish_mission_update(issue_ref=ref, update=update)

    # Status should have been updated
    assert result.status == CanonicalStatus.IN_PROGRESS

    # Verify comment was posted
    stored_issue = connector._issues[ref.identity]
    comments = stored_issue.custom_fields.get("comments", [])
    assert len(comments) == 1
    assert "Spec Kitty mission update:" in comments[0]
    assert "State: implement" in comments[0]


async def test_publish_mission_update_no_status() -> None:
    """publish_mission_update with target_status=None still posts comment but no status change."""
    connector, ref = _make_in_memory_connector_with_issue()
    sync = BidirectionalIssueSync(connector=connector)

    update = MissionUpdate(
        mission_id="mission:test:1",
        mission_state="specify",
        target_status=None,
        summary="Specification phase",
    )
    result = await sync.publish_mission_update(issue_ref=ref, update=update)

    # Status should NOT have changed (still TODO)
    assert result.status == CanonicalStatus.TODO

    # Verify comment was still posted
    stored_issue = connector._issues[ref.identity]
    comments = stored_issue.custom_fields.get("comments", [])
    assert len(comments) == 1
    assert "Spec Kitty mission update:" in comments[0]
    assert "State: specify" in comments[0]

    # Verify update_issue was called (for custom_fields) but patch had no status
    events = connector._events
    update_events = [e for e in events if e.event_type.value == "updated"]
    assert len(update_events) >= 1
    update_payload = update_events[0].payload
    patch = update_payload.get("patch", {})
    assert "status" not in patch
