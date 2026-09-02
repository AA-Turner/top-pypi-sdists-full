"""Tests for search, seeding, and egress behavior across Jira and Linear connectors.

Covers:
- Jira search (query_text, query_key, precedence)  [T011]
- Jira custom field blob write/skip                 [T012]
- Linear search (query_text, query_key, wrong team) [T013]
- Linear custom field skip warning                  [T014]
- Mission seeding from canonical issues             [T015]
- Mission egress comment format and transitions     [T016]
- Jira transition_issue determinism (WP01 T006)
- Jira list_transitions + update_issue independence (WP01 T007)
"""

from __future__ import annotations

import json
import logging
from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx
import pytest

from spec_kitty_tracker.connectors.in_memory import InMemoryConnector
from spec_kitty_tracker.connectors.jira import (
    JiraConnector,
    JiraConnectorConfig,
    JiraTransition,
)
from spec_kitty_tracker.connectors.linear import LinearConnector, LinearConnectorConfig
from spec_kitty_tracker.errors import CapabilityNotSupportedError
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


# ===========================================================================
# WP01 T006 — Jira transition_issue determinism tests
# ===========================================================================


def _iam42_ref() -> ExternalRef:
    return ExternalRef(
        system="jira",
        workspace="https://test.atlassian.net",
        id="10001",
        key="IAM-42",
        url="https://test.atlassian.net/browse/IAM-42",
    )


def _jira_issue_with_status(status_name: str) -> dict[str, Any]:
    """Build a canned Jira issue payload with a given raw status name."""
    return {
        "id": "10001",
        "key": "IAM-42",
        "fields": {
            "summary": "SCIM provisioning",
            "description": None,
            "status": {"name": status_name},
            "priority": {"name": "Medium"},
            "assignee": None,
            "labels": [],
            "issuetype": {"name": "Task"},
            "parent": None,
            "created": "2026-03-01T10:00:00.000+0000",
            "updated": "2026-03-15T14:00:00.000+0000",
        },
    }


async def test_jira_transition_issue_matches_and_posts() -> None:
    """C1.2: an available transition's name matches the desired name -> POSTs exactly that
    transition id and returns the refreshed issue."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(
                200,
                json={
                    "transitions": [
                        {"id": "11", "name": "Backlog"},
                        {"id": "21", "name": "In Progress"},
                    ]
                },
            )
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_PROGRESS)

    assert recorded_posts == [{"transition": {"id": "21"}}]
    assert result.ref.key == "IAM-42"


async def test_jira_transition_issue_no_match_raises() -> None:
    """C1.3: transitions are present but none named the desired status, and the ticket is
    not already at target -> raises with capability='status'; no POST is issued; the message
    names the requested status, the resolved desired name, and the available transition names."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(
                200,
                json={
                    "transitions": [
                        {"id": "11", "name": "Backlog"},
                        {"id": "31", "name": "Blocked"},
                    ]
                },
            )
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)

    with pytest.raises(CapabilityNotSupportedError) as exc_info:
        await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_PROGRESS)

    assert exc_info.value.capability == "status"
    message = str(exc_info.value)
    assert "in_progress" in message
    assert "in progress" in message
    assert "Backlog" in message
    assert "Blocked" in message
    assert recorded_posts == []


async def test_jira_transition_issue_empty_transitions_raises() -> None:
    """C1.4: the ticket reports an empty transitions list and is not at target -> raises;
    no POST is issued."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": []})
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)

    with pytest.raises(CapabilityNotSupportedError) as exc_info:
        await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_PROGRESS)

    assert exc_info.value.capability == "status"
    assert recorded_posts == []


async def test_jira_transition_issue_idempotent_noop() -> None:
    """C1.1: the ticket's raw status name already equals the resolved desired name ->
    returns the issue without ever issuing a GET transitions or POST call (idempotent no-op
    precedes match-or-raise)."""
    recorded_posts: list[dict[str, Any]] = []
    transitions_get_calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal transitions_get_calls
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            transitions_get_calls += 1
            return httpx.Response(
                200, json={"transitions": [{"id": "99", "name": "Should Not Be Used"}]}
            )
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("In Progress"))
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_PROGRESS)

    assert result.ref.key == "IAM-42"
    assert recorded_posts == []
    assert transitions_get_calls == 0


async def test_jira_transition_issue_retry_after_partial_success_noop() -> None:
    """C1.5: a prior transition succeeded server-side but the response was lost; a retried
    call resolves as an idempotent no-op success (not a false refusal) even though the
    transitions list is now empty (the ticket already moved past this status)."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": []})
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("Done"))
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.transition_issue(_iam42_ref(), CanonicalStatus.DONE)

    assert result.ref.key == "IAM-42"
    assert recorded_posts == []


async def test_jira_transition_issue_todo_guard_unrecognized_status() -> None:
    """C1.6: an unrecognized current status (e.g. 'Triage') with target_status=TODO must NOT
    be treated as already-at-target via the lossy canonical `_status_from_jira` round-trip
    (which defaults unrecognized names to TODO) -> proceeds to match-or-raise instead of a
    silent false no-op. This must fail against a naive canonical-status implementation."""
    recorded_posts: list[dict[str, Any]] = []
    transitions_get_calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal transitions_get_calls
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            transitions_get_calls += 1
            return httpx.Response(200, json={"transitions": [{"id": "5", "name": "Backlog"}]})
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("Triage"))
        return httpx.Response(404)

    connector = _jira_connector(handler)

    with pytest.raises(CapabilityNotSupportedError) as exc_info:
        await connector.transition_issue(_iam42_ref(), CanonicalStatus.TODO)

    assert exc_info.value.capability == "status"
    assert transitions_get_calls == 1
    assert recorded_posts == []


async def test_jira_transition_issue_duplicate_name_picks_first() -> None:
    """C1.7: two available transitions share the same case-insensitive name (different ids)
    -> the connector deterministically POSTs the first one Jira returned."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(
                200,
                json={
                    "transitions": [
                        {"id": "41", "name": "Done"},
                        {"id": "42", "name": "DONE"},
                    ]
                },
            )
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)
    await connector.transition_issue(_iam42_ref(), CanonicalStatus.DONE)

    assert recorded_posts == [{"transition": {"id": "41"}}]


async def test_jira_transition_issue_matches_classic_workflow_destination_status() -> None:
    """A company-managed project on a classic workflow names transitions for the action
    ("Start Progress"), never for the destination status. The desired name is a *status*
    name, so the match must read each transition's destination (``to.name``) -> POSTs the
    transition whose destination is the desired status."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(
                200,
                json={
                    "transitions": [
                        {"id": "11", "name": "Stop Progress", "to": {"name": "To Do"}},
                        {"id": "21", "name": "Start Progress", "to": {"name": "In Progress"}},
                        {"id": "31", "name": "Resolve Issue", "to": {"name": "Done"}},
                    ]
                },
            )
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)
    await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_PROGRESS)

    assert recorded_posts == [{"transition": {"id": "21"}}]


async def test_jira_transition_issue_destination_status_beats_transition_name() -> None:
    """When one transition is *named* the desired status but lands somewhere else, and a
    later one actually lands on the desired status, destination wins regardless of order."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(
                200,
                json={
                    "transitions": [
                        {"id": "11", "name": "Done", "to": {"name": "Awaiting Release"}},
                        {"id": "21", "name": "Resolve Issue", "to": {"name": "Done"}},
                    ]
                },
            )
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)
    await connector.transition_issue(_iam42_ref(), CanonicalStatus.DONE)

    assert recorded_posts == [{"transition": {"id": "21"}}]


async def test_jira_transition_issue_falls_back_to_transition_name_without_to() -> None:
    """Backward compatibility: a payload carrying no ``to`` (and an operator whose
    ``status_name_map`` holds transition names) still matches on the transition's own
    name, so team-managed projects and existing configs keep working."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(
                200,
                json={
                    "transitions": [
                        {"id": "11", "name": "Backlog"},
                        {"id": "21", "name": "In Progress"},
                    ]
                },
            )
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)
    await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_PROGRESS)

    assert recorded_posts == [{"transition": {"id": "21"}}]


async def test_jira_transition_issue_classic_workflow_refusal_names_both_namespaces() -> None:
    """A genuine refusal on a classic workflow renders each candidate as
    ``name -> destination`` so the operator can see why nothing matched."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(
                200,
                json={
                    "transitions": [
                        {"id": "11", "name": "Stop Progress", "to": {"name": "To Do"}},
                        {"id": "31", "name": "Resolve Issue", "to": {"name": "Done"}},
                    ]
                },
            )
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)

    with pytest.raises(CapabilityNotSupportedError) as exc_info:
        await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_REVIEW)

    assert exc_info.value.capability == "status"
    message = str(exc_info.value)
    assert "Stop Progress -> To Do" in message
    assert "Resolve Issue -> Done" in message
    assert recorded_posts == []


# ===========================================================================
# WP01 T007 — list_transitions + update_issue independence tests
# ===========================================================================


async def test_jira_list_transitions_returns_items() -> None:
    """C2.1/C2.3: list_transitions returns JiraTransition items produced by a single GET;
    the ticket is unchanged (no mutating request)."""
    request_log: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        request_log.append((request.method, url))
        if request.method == "GET" and url.endswith("/transitions"):
            return httpx.Response(
                200,
                json={
                    "transitions": [
                        {"id": "11", "name": "Backlog"},
                        {"id": "21", "name": "In Progress"},
                    ]
                },
            )
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.list_transitions(_iam42_ref())

    assert result == [
        JiraTransition(id="11", name="Backlog"),
        JiraTransition(id="21", name="In Progress"),
    ]
    assert len(request_log) == 1
    assert request_log[0][0] == "GET"


async def test_jira_list_transitions_empty() -> None:
    """C2.2: a ticket with no transitions -> returns []."""

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if request.method == "GET" and url.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": []})
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.list_transitions(_iam42_ref())

    assert result == []


async def test_jira_list_transitions_null_transitions_key_returns_empty() -> None:
    """MAJOR regression: a malformed payload with `"transitions": null` (present but null,
    unlike the merely-missing-key case covered by C2.2) must not raise a bare TypeError from
    iterating None -- `.get("transitions", [])` only defaults on a *missing* key, so a null
    value needs an explicit isinstance guard. Returns [] instead of crashing."""

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if request.method == "GET" and url.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": None})
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.list_transitions(_iam42_ref())

    assert result == []


async def test_jira_list_transitions_skips_malformed_items() -> None:
    """MAJOR regression: individual malformed items (non-Mapping `null`, or a Mapping missing
    `id`) must be skipped rather than raising a bare TypeError/KeyError while indexing -- only
    well-formed items are returned."""

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if request.method == "GET" and url.endswith("/transitions"):
            return httpx.Response(
                200,
                json={"transitions": [None, {"name": "NoId"}, {"id": "9", "name": "Go"}]},
            )
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.list_transitions(_iam42_ref())

    assert result == [JiraTransition(id="9", name="Go")]


async def test_jira_update_issue_persists_non_status_before_transition_raises() -> None:
    """C3.1: a patch with non-status fields (labels) plus a `status` with no matching
    transition PUTs the non-status fields FIRST, then the transition raises
    CapabilityNotSupportedError — the non-status writes are not lost. Ordering is asserted
    from the recorded request sequence (PUT observed before the raise)."""
    call_order: list[str] = []
    recorded_put_bodies: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "PUT" and "/rest/api/3/issue/IAM-42" in url:
            call_order.append("put")
            recorded_put_bodies.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and url.endswith("/transitions"):
            call_order.append("get_transitions")
            return httpx.Response(200, json={"transitions": [{"id": "5", "name": "Backlog"}]})
        if method == "POST" and url.endswith("/transitions"):
            call_order.append("post_transition")
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            call_order.append("get_issue")
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)

    with pytest.raises(CapabilityNotSupportedError) as exc_info:
        await connector.update_issue(
            _iam42_ref(),
            patch={"labels": ["urgent"], "status": CanonicalStatus.DONE.value},
            idempotency_key="test-key",
        )

    assert exc_info.value.capability == "status"
    assert recorded_put_bodies == [{"fields": {"labels": ["urgent"]}}]
    assert "put" in call_order
    assert "post_transition" not in call_order
    assert call_order.index("put") < call_order.index("get_transitions")


async def test_jira_transition_issue_null_fields_refuses_not_crashes() -> None:
    """HIGH regression: a malformed payload with `"fields": null` (e.g. a permission-scoped or
    partially-hydrated Jira response) must not raise a bare AttributeError from the raw-status
    parse. The idempotent no-op parse is null-safe like `_to_canonical`, so a null `fields`
    resolves to an empty current raw name, falls through to match-or-refuse, and raises
    CapabilityNotSupportedError when no matching transition exists -- the refuse-loudly contract
    holds even on malformed shapes."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": [{"id": "11", "name": "Backlog"}]})
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json={"id": "10001", "key": "IAM-42", "fields": None})
        return httpx.Response(404)

    connector = _jira_connector(handler)

    with pytest.raises(CapabilityNotSupportedError) as exc_info:
        await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_PROGRESS)

    assert exc_info.value.capability == "status"
    assert recorded_posts == []


async def test_jira_transition_issue_null_fields_matches_and_posts() -> None:
    """Same malformed `"fields": null` payload, but this time an available transition matches
    the desired name -> the null-safe parse never mistakes the null status for a match, falls
    through to the match step, and transitions normally."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": [{"id": "21", "name": "In Progress"}]})
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json={"id": "10001", "key": "IAM-42", "fields": None})
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_PROGRESS)

    assert recorded_posts == [{"transition": {"id": "21"}}]
    assert result.ref.key == "IAM-42"


async def test_jira_transition_issue_null_transitions_key_refuses_not_crashes() -> None:
    """MAJOR regression: the GET transitions response itself has `"transitions": null`
    (present but null). `.get("transitions", [])` only defaults on a *missing* key, so this
    must not raise a bare TypeError from iterating None. The current status does not match
    the desired one, so match-or-refuse must raise CapabilityNotSupportedError -- never a
    TypeError -- and no POST is issued."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": None})
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)

    with pytest.raises(CapabilityNotSupportedError) as exc_info:
        await connector.transition_issue(_iam42_ref(), CanonicalStatus.IN_PROGRESS)

    assert exc_info.value.capability == "status"
    assert recorded_posts == []


async def test_jira_transition_issue_skips_malformed_item_matches_later_valid_one() -> None:
    """MEDIUM regression: the available transitions list contains a malformed leading item
    (`null`) followed by a valid matching one -- the malformed item must be skipped rather
    than raising, and the scan must continue (no early break) so the later valid match is
    still found and POSTed."""
    recorded_posts: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        method = request.method
        if method == "GET" and url.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": [None, {"id": "5", "name": "Done"}]})
        if method == "POST" and url.endswith("/transitions"):
            recorded_posts.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            return httpx.Response(200, json=_jira_issue_with_status("To Do"))
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.transition_issue(_iam42_ref(), CanonicalStatus.DONE)

    assert recorded_posts == [{"transition": {"id": "5"}}]
    assert result.ref.key == "IAM-42"


async def test_jira_update_issue_already_at_target_composes_with_field_put() -> None:
    """C3.2: a patch bundling non-status fields (labels) with a `status` that already matches
    the ticket's current raw status name -> the non-status fields PUT is issued, and the status
    write takes the idempotent no-op path (no GET transitions, no POST transition), proving the
    no-op composes correctly with the write-reordering. update_issue still returns the freshly
    refetched issue."""
    call_order: list[str] = []
    recorded_put_bodies: list[dict[str, Any]] = []
    transitions_get_calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal transitions_get_calls
        url = str(request.url)
        method = request.method
        if method == "PUT" and "/rest/api/3/issue/IAM-42" in url:
            call_order.append("put")
            recorded_put_bodies.append(json.loads(request.content))
            return httpx.Response(204)
        if method == "GET" and url.endswith("/transitions"):
            transitions_get_calls += 1
            call_order.append("get_transitions")
            return httpx.Response(
                200, json={"transitions": [{"id": "99", "name": "Should Not Be Used"}]}
            )
        if method == "POST" and url.endswith("/transitions"):
            call_order.append("post_transition")
            return httpx.Response(204)
        if method == "GET" and "/rest/api/3/issue/IAM-42" in url:
            call_order.append("get_issue")
            return httpx.Response(200, json=_jira_issue_with_status("In Progress"))
        return httpx.Response(404)

    connector = _jira_connector(handler)
    result = await connector.update_issue(
        _iam42_ref(),
        patch={"labels": ["urgent"], "status": CanonicalStatus.IN_PROGRESS.value},
        idempotency_key="test-key",
    )

    assert recorded_put_bodies == [{"fields": {"labels": ["urgent"]}}]
    assert "put" in call_order
    assert transitions_get_calls == 0
    assert "post_transition" not in call_order
    assert call_order.count("get_issue") == 2
    assert result.ref.key == "IAM-42"


async def test_jira_get_issue_null_priority_does_not_crash() -> None:
    """Regression: a Jira payload with ``fields.priority == null`` (key present,
    value null) must not crash ``_to_canonical``. ``get_issue`` is on the
    ``transition_issue`` idempotent-no-op path, so a raw AttributeError here would
    abort ``SyncEngine.push`` the same way the transitions-null bugs did."""
    payload = _jira_issue_with_status("To Do")
    payload["fields"]["priority"] = None

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    connector = _jira_connector(handler)
    issue = await connector.get_issue(_iam42_ref())
    assert issue.priority is None
