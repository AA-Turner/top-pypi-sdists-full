"""`X-Probe-Hide-Session-Work`: the hosted MCP's opt-in to leave out the work
the caller's own coding-agent session created (research-os 0291).

The Probe daemon's reader reads beside a session the writer is recording as it
goes. Without this it found the session's own fresh projects and runs and
reported them as the team's prior work. The header plus a known session turns
into the backend's `exclude_origin_session` on `/v1/search` and `/v1/browse`;
a caller without the header sends exactly the request it always sent.
"""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import Iterator
from contextlib import contextmanager

import pytest

from probe.mcp import accounting
from probe.mcp.contract import MissingMarker
from probe.sdk import errors
from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk.agent_session import AGENT_HEADER, AGENT_SESSION_HEADER, HIDE_SESSION_WORK_HEADER
from tests.conftest import search_response

SESSION = str(uuid.uuid4())
OTHER = str(uuid.uuid4())


@contextmanager
def _request(*, hide: bool, agent: str | None = "claude_code", session: str | None = SESSION
             ) -> Iterator[None]:
    """One hosted request's holder, bound exactly as `with_auth_and_health` binds it."""
    state = accounting.begin_request(agent, session, {}, hide_session_work=hide)
    try:
        yield
    finally:
        accounting.end_request(state)


# -- the header -----------------------------------------------------------------


def test_the_header_name_is_the_one_the_daemon_reader_sends() -> None:
    assert HIDE_SESSION_WORK_HEADER == "X-Probe-Hide-Session-Work"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [(b"1", True), (b" 1 ", True), (b"0", False), (b"true", False), (b"yes", False), (b"", False)],
)
def test_only_exactly_one_opts_in(raw: bytes, expected: bool) -> None:
    headers = {HIDE_SESSION_WORK_HEADER.lower().encode(): raw}
    assert accounting.hide_session_work_from_headers(headers) is expected


def test_an_absent_header_opts_nothing_in() -> None:
    assert accounting.hide_session_work_from_headers({}) is False


def test_nothing_is_hidden_outside_a_hosted_request() -> None:
    """stdio and tests bind no holder: the opt-in cannot exist there."""
    assert accounting.session_work_to_hide() is None


def test_the_header_alone_hides_nothing_without_a_session() -> None:
    with _request(hide=True, agent=None, session=None):
        assert accounting.session_work_to_hide() is None


def test_the_ambient_session_is_hidden_when_opted_in() -> None:
    with _request(hide=True):
        assert accounting.session_work_to_hide() == SESSION


def test_a_session_without_the_opt_in_hides_nothing() -> None:
    with _request(hide=False):
        assert accounting.session_work_to_hide() is None


def test_the_opt_in_is_request_state_not_telemetry() -> None:
    """`emit` builds the analytics event from the holder; the flag must not ride it."""
    state = accounting.begin_request("claude_code", SESSION, {}, hide_session_work=True)
    try:
        assert state["holder"]["hide_session_work"] is True
    finally:
        accounting.end_request(state)


def test_the_edge_reads_the_header_into_the_request(monkeypatch: pytest.MonkeyPatch) -> None:
    """`with_auth_and_health` is where the header becomes request state."""
    from probe.mcp.server import with_auth_and_health

    monkeypatch.setenv("PROBE_MCP_OAUTH", "0")
    monkeypatch.setenv("PROBE_MCP_VERIFY_TOKEN", "0")

    seen: dict = {}

    async def inner(scope, receive, send):
        seen["hide"] = accounting.session_work_to_hide()
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"{}"})

    app = with_auth_and_health(inner, token_rejected=None)
    sent: list = []

    async def send(message):
        sent.append(message)

    async def receive():
        return {"type": "http.request", "body": b""}

    base = [
        (AGENT_HEADER.lower().encode(), b"claude_code"),
        (AGENT_SESSION_HEADER.lower().encode(), SESSION.encode()),
    ]
    for headers, expected in (
        (base + [(HIDE_SESSION_WORK_HEADER.lower().encode(), b"1")], SESSION),
        (base, None),
    ):
        seen.clear()
        asyncio.run(app({"type": "http", "path": "/mcp", "headers": headers}, receive, send))
        assert seen["hide"] == expected


# -- search_knowledge -------------------------------------------------------------


def test_search_without_the_opt_in_sends_the_request_it_always_sent(app, client) -> None:
    app.search_response = search_response()
    service = ResearchReadService(ResearchOSSource(client))
    with _request(hide=False):
        service.search_knowledge("dockq")
    body = app.search_requests[-1]
    assert "exclude_origin_session" not in body
    # The transcript self-exclusion is untouched by this change.
    assert body["exclude_agent_session"] == SESSION


def test_search_with_the_opt_in_hides_the_callers_session_work(app, client) -> None:
    app.search_response = {**search_response(), "origin_exclusion_applied": True}
    service = ResearchReadService(ResearchOSSource(client))
    with _request(hide=True):
        answer = service.search_knowledge("dockq")
    assert app.search_requests[-1]["exclude_origin_session"] == SESSION
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED not in answer["completeness"]["missing"]


def test_the_model_cannot_redirect_which_session_is_hidden(app, client) -> None:
    """`exclude_session` is a tool argument, i.e. the MODEL's. It still drives the
    transcript self-exclusion, but the work filter always names the AMBIENT
    session the reader's process put on the header -- or the model could name
    another id and see its own session's work again."""
    app.search_response = {**search_response(), "origin_exclusion_applied": True}
    service = ResearchReadService(ResearchOSSource(client))
    with _request(hide=True):
        service.search_knowledge("dockq", exclude_session=OTHER)
    assert app.search_requests[-1]["exclude_origin_session"] == SESSION
    assert app.search_requests[-1]["exclude_agent_session"] == OTHER


def test_a_server_that_did_not_echo_is_reported_not_assumed(app, client) -> None:
    """A backend predating the field accepts it, ignores it and answers 200 with
    the session's own projects and runs still in the results."""
    app.search_response = search_response()
    service = ResearchReadService(ResearchOSSource(client))
    with _request(hide=True):
        answer = service.search_knowledge("dockq")
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED in answer["completeness"]["missing"]
    assert answer["completeness"]["state"] == "partial"


def test_no_marker_for_a_caller_that_did_not_ask(app, client) -> None:
    app.search_response = search_response()
    service = ResearchReadService(ResearchOSSource(client))
    with _request(hide=False):
        answer = service.search_knowledge("dockq")
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED not in answer["completeness"]["missing"]


# -- browse -------------------------------------------------------------------------


def _browse() -> dict:
    return {
        "projects": [],
        "experiments": None,
        "runs": None,
        "cursor": None,
        "depth": 1,
        "limit": 50,
        "truncated": False,
    }


def _browse_params(app) -> dict:
    [request] = [r for r in app.requests if r.url.path == "/v1/browse"][-1:]
    return dict(request.url.params)


def test_browse_without_the_opt_in_sends_the_request_it_always_sent(app, client) -> None:
    app.browse_response = _browse()
    service = ResearchReadService(ResearchOSSource(client))
    with _request(hide=False):
        envelope = service.browse_research()
    assert "exclude_origin_session" not in _browse_params(app)
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED not in envelope.get("completeness", {}).get("missing", [])


def test_browse_with_the_opt_in_hides_the_callers_session_work(app, client) -> None:
    app.browse_response = {**_browse(), "origin_exclusion_applied": True}
    service = ResearchReadService(ResearchOSSource(client))
    with _request(hide=True):
        envelope = service.browse_research(scope="project:x")
    assert _browse_params(app)["exclude_origin_session"] == SESSION
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED not in envelope.get("completeness", {}).get("missing", [])


def test_browse_marks_a_server_that_ignored_the_filter(app, client) -> None:
    app.browse_response = _browse()
    service = ResearchReadService(ResearchOSSource(client))
    with _request(hide=True):
        envelope = service.browse_research(scope="project:x")
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED in envelope["completeness"]["missing"]


class _Source(ResearchOSSource):
    """The real adapter over the fake backend, with the two 0291 reads the fake
    does not serve stubbed: the created set and the server-side unfiled filter."""

    def __init__(self, client, *, created=None, unfiled=None):
        super().__init__(client)
        self.created = created
        self.unfiled = unfiled or []
        self.unfiled_calls: list[dict] = []
        self.created_calls = 0

    def session_created(self, session_id):
        self.created_calls += 1
        if self.created is None:
            raise errors.NotFoundError("no such route")
        return self.created

    def unfiled_runs(self, *, limit=10, exclude_origin_session=None):
        self.unfiled_calls.append({"limit": limit, "exclude_origin_session": exclude_origin_session})
        return list(self.unfiled)


def _run_row(rid: str) -> dict:
    return {"id": rid, "name": rid[:8], "status": "running", "created_at": "2026-09-28T00:00:00Z"}


def test_the_unfiled_list_is_filtered_server_side(app, client) -> None:
    """P3: the filter runs inside the backend page, so the session's own floating
    runs cannot empty the ten the reader is shown."""
    app.browse_response = {**_browse(), "origin_exclusion_applied": True}
    theirs = str(uuid.uuid4())
    source = _Source(client, created={"project_ids": [], "run_ids": []}, unfiled=[_run_row(theirs)])
    with _request(hide=True):
        data = ResearchReadService(source).browse_research()["data"]
    assert source.unfiled_calls == [{"limit": 10, "exclude_origin_session": SESSION}]
    assert [n["uuid"] for n in data["unfiled"]] == [f"run:{theirs}"]


def test_the_unfiled_list_is_checked_against_the_created_set(app, client) -> None:
    app.browse_response = {**_browse(), "origin_exclusion_applied": True}
    mine, theirs = str(uuid.uuid4()), str(uuid.uuid4())
    source = _Source(
        client,
        created={"project_ids": [], "run_ids": [mine.upper()]},
        unfiled=[_run_row(mine), _run_row(theirs)],
    )
    with _request(hide=True):
        data = ResearchReadService(source).browse_research()["data"]
    assert [n["uuid"] for n in data["unfiled"]] == [f"run:{theirs}"]


def test_an_unverifiable_unfiled_list_is_withheld_and_marked(app, client) -> None:
    """A backend that cannot give the created set predates the filter too."""
    app.browse_response = {**_browse(), "origin_exclusion_applied": True}
    source = _Source(client, created=None, unfiled=[_run_row(str(uuid.uuid4()))])
    with _request(hide=True):
        envelope = ResearchReadService(source).browse_research()
    assert "unfiled" not in envelope["data"]
    assert MissingMarker.UNFILED_RUNS in envelope["completeness"]["missing"]


def test_without_the_opt_in_the_unfiled_read_is_unchanged(app, client) -> None:
    app.browse_response = _browse()
    source = _Source(client, created=None, unfiled=[_run_row(str(uuid.uuid4()))])
    with _request(hide=False):
        ResearchReadService(source).browse_research()
    assert source.unfiled_calls == [{"limit": 10, "exclude_origin_session": None}]
    assert source.created_calls == 0


# -- entity: the views that list children ----------------------------------------------

PRIOR = str(uuid.uuid4())
MY_EXPERIMENT, MY_RUN, THEIR_RUN, THEIR_EXPERIMENT = (str(uuid.uuid4()) for _ in range(4))


class _LineageSource(_Source):
    def get(self, ref):
        return "project", {"id": PRIOR, "name": "prior", "slug": "prior", "kind": "general"}

    def project_lineage(self, project_id):
        assert project_id == PRIOR
        return {
            "project_id": PRIOR,
            "kind": "general",
            "origin": {"type": "project", "id": MY_EXPERIMENT},
            "edges": [
                {"source_type": "run", "source_id": MY_RUN, "relation": "derived_from",
                 "target_type": "project", "target_id": PRIOR},
                {"source_type": "run", "source_id": THEIR_RUN, "relation": "derived_from",
                 "target_type": "project", "target_id": PRIOR},
            ],
            "nodes": [
                {"type": "experiment", "id": MY_EXPERIMENT, "name": "mine"},
                {"type": "experiment", "id": THEIR_EXPERIMENT, "name": "theirs"},
                {"type": "run", "id": MY_RUN, "name": "my run"},
                {"type": "run", "id": THEIR_RUN, "name": "their run"},
                {"type": "project", "id": PRIOR, "name": "the entity itself"},
            ],
            "truncated": False,
        }


def _lineage(client, *, hide: bool, created) -> dict:
    source = _LineageSource(client, created=created)
    with _request(hide=hide):
        envelope = ResearchReadService(source).get_entity(
            f"project:{PRIOR}", view="lineage", token_budget=8000
        )
    return envelope, source


def test_an_entity_view_drops_the_sessions_own_children(client) -> None:
    """P2: after browse, a prior project's lineage is where the session's new
    experiments and runs filed under it would surface."""
    created = {"project_ids": [MY_EXPERIMENT], "run_ids": [MY_RUN], "truncated": False}
    envelope, _ = _lineage(client, hide=True, created=created)
    data = envelope["data"]
    names = {node.get("name") for node in data["nodes"]}
    assert names == {"theirs", "their run", "the entity itself"}
    assert [e["source_id"] for e in data["edges"]] == [THEIR_RUN]
    assert data["origin"] is None
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED not in envelope.get("completeness", {}).get("missing", [])


def test_the_sessions_own_work_opened_by_address_is_shown_whole(client) -> None:
    """Opened by address (the reader takes refs from the session it reads
    beside), the session's own work is not scrubbed out of its own view -- that
    would empty it with nothing saying so."""
    created = {"project_ids": [PRIOR, MY_EXPERIMENT], "run_ids": [MY_RUN], "truncated": False}
    envelope, _ = _lineage(client, hide=True, created=created)
    assert len(envelope["data"]["nodes"]) == 5 and len(envelope["data"]["edges"]) == 2


def test_an_entity_view_without_the_opt_in_is_untouched(client) -> None:
    envelope, source = _lineage(client, hide=False, created=None)
    assert len(envelope["data"]["nodes"]) == 5 and len(envelope["data"]["edges"]) == 2
    assert source.created_calls == 0


def test_an_entity_view_that_cannot_be_filtered_says_so(client) -> None:
    envelope, _ = _lineage(client, hide=True, created=None)
    assert len(envelope["data"]["nodes"]) == 5
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED in envelope["completeness"]["missing"]


def test_a_truncated_created_set_is_marked(client) -> None:
    created = {"project_ids": [MY_EXPERIMENT], "run_ids": [], "truncated": True}
    envelope, _ = _lineage(client, hide=True, created=created)
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED in envelope["completeness"]["missing"]


# -- the SDK client -----------------------------------------------------------------


def test_the_sdk_omits_the_field_unless_asked(app, client) -> None:
    app.search_response = search_response()
    client.search("q")
    assert "exclude_origin_session" not in app.search_requests[-1]
    client.search("q", exclude_origin_session=SESSION)
    assert app.search_requests[-1]["exclude_origin_session"] == SESSION

    app.browse_response = _browse()
    client.browse()
    assert "exclude_origin_session" not in _browse_params(app)
    client.browse(exclude_origin_session=SESSION)
    assert _browse_params(app)["exclude_origin_session"] == SESSION

    # The run list and the created set (0291).
    client.list_runs(unfiled=True, exclude_origin_session=SESSION)
    runs = [r for r in app.requests if r.url.path == "/v1/runs"][-1]
    assert runs.url.params["exclude_origin_session"] == SESSION
    with pytest.raises(errors.RosError):
        client.session_created(SESSION)  # the fake backend does not serve it
    assert app.requests[-1].url.path == f"/v1/sessions/{SESSION}/created"
