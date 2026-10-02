"""`session:` refs on research_get: the transcript is READABLE, boundedly.

The gap these guard against was live in every release before this one: a
captured session was metadata riding on other entities (`sessions` on a
project, `foreign_keys` on a run) — its transcript searchable as ranked chunks
and renderable on the dashboard, but not readable through the MCP at all. An
agent asking "why was this designed this way" could locate the session that
knew and then not open it.

Shape rules pinned here:
  * the transcript is NEVER served whole — line sections through the ordinary
    rows machinery, cursor-walked;
  * `filters.grep` is search WITHIN one document, and an empty grep is
    state="no_match" (the whole document was read; no line contains it), not
    an error and not partial;
  * a bare `session:<id>` resolves the recording agent instead of defaulting
    to one — a claude_code default would read every codex session as "never
    captured";
  * `/work` answering empty is "not observed", never proof of absence, and
    the transcript 404 stays the honest existence signal.
"""

from __future__ import annotations

import pytest

from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors

_SID = "22222222-2222-2222-2222-222222222222"


def _service(client) -> ResearchReadService:
    return ResearchReadService(ResearchOSSource(client))


def _seed(app, *, agent: str = "claude_code", lines: int = 10) -> None:
    content = "\n".join(f"line {n}: the quick brown fox" for n in range(1, lines + 1))
    app.session_work[_SID] = {
        "session_id": _SID,
        "agent": agent,
        "name": "design session",
        "device_label": None,
        "device_hostname": "laptop",
        "projects": [{"id": "p-1", "name": "folding"}],
        "experiments": [],
        "runs": [],
        "artifacts": [],
    }
    app.session_transcripts[(_SID, agent)] = {
        "session_id": _SID,
        "agent": agent,
        "title": "design session",
        "content": content,
        "chunk_count": 2,
        "body_size_bytes": len(content.encode()),
    }
    app.session_digests[_SID] = {
        "session_id": _SID,
        "agent": agent,
        "status": "ready",
        "digest": {"title": "design session"},
        "generated_at": "2026-07-16T00:00:00Z",
        "model": "test-model",
        "project_id": None,
        "skip_reason": None,
    }


# -- the headline gap: a transcript is readable at all ------------------------


def test_transcript_view_reads_the_actual_content(client, app):
    _seed(app, lines=5)
    result = _service(client).get_entity(f"session:{_SID}", view="transcript")

    sections = result["data"]["sections"]
    assert sections[0]["line_start"] == 1
    assert "line 1: the quick brown fox" in sections[0]["text"]
    assert result["data"]["total_lines"] == 5
    assert "completeness" not in result


def test_transcript_is_sectioned_and_cursor_walked_never_whole(client, app):
    """A long transcript arrives as line sections the token budget bounds, with
    a cursor for the rest — the document must not be dumped whole into one
    response just because it exists whole server-side."""
    _seed(app, lines=400)  # 10 sections of 40 lines
    service = _service(client)

    first = service.get_entity(f"session:{_SID}", view="transcript", token_budget=600)
    assert first["completeness"]["state"] == "partial"
    assert "truncated_by_token_budget" in first["completeness"]["missing"]
    assert first["next_cursor"]
    got = list(first["data"]["sections"])
    assert 0 < len(got) < 10

    cursor = first["next_cursor"]
    while cursor:
        page = service.get_entity(
            f"session:{_SID}", view="transcript", token_budget=600, cursor=cursor
        )
        got.extend(page["data"]["sections"])
        cursor = page.get("next_cursor")
    assert [s["line_start"] for s in got] == list(range(1, 401, 40))
    assert got[-1]["line_end"] == 400


def test_transcript_grep_returns_matches_with_context(client, app):
    _seed(app, lines=10)
    result = _service(client).get_entity(
        f"session:{_SID}",
        view="transcript",
        filters={"grep": "LINE 7", "context_lines": 1},  # case-insensitive, literal
    )
    sections = result["data"]["sections"]
    assert [s["line"] for s in sections] == [7]
    assert sections[0]["line_start"] == 6 and sections[0]["line_end"] == 8
    assert "line 6" in sections[0]["text"] and "line 8" in sections[0]["text"]


def test_transcript_grep_miss_is_no_match_not_partial(client, app):
    """The whole document was read and no line contains the needle — that is an
    ANSWER (with total_lines as its denominator), not a degraded response."""
    _seed(app, lines=10)
    result = _service(client).get_entity(
        f"session:{_SID}", view="transcript", filters={"grep": "dockq"}
    )
    assert result["completeness"]["state"] == "no_match"
    assert result["data"]["sections"] == []
    assert result["data"]["total_lines"] == 10


def test_context_lines_without_grep_is_rejected_not_ignored(client, app):
    _seed(app)
    with pytest.raises(errors.ValidationError, match="context_lines"):
        _service(client).get_entity(
            f"session:{_SID}", view="transcript", filters={"context_lines": 3}
        )


def test_start_line_windows_the_plain_read(client, app):
    _seed(app, lines=100)
    result = _service(client).get_entity(
        f"session:{_SID}", view="transcript", filters={"start_line": 81}
    )
    sections = result["data"]["sections"]
    assert [s["line_start"] for s in sections] == [81]
    assert sections[0]["line_end"] == 100


# -- agent resolution: source is identity, not a default ----------------------


def test_bare_ref_resolves_a_codex_session_instead_of_404ing(client, app):
    """The transcript route's `source` defaults to claude_code server-side, so a
    naive passthrough would read every codex session as "never captured". A bare
    ref must resolve the agent — here /work knows it."""
    _seed(app, agent="codex")
    result = _service(client).get_entity(f"session:{_SID}", view="transcript")
    assert result["data"]["agent"] == "codex"
    assert result["data"]["sections"]


def test_bare_ref_tries_both_agents_when_work_never_saw_the_session(client, app):
    """A session can have a transcript and NO observed work (capture on, no
    entity links). With /work answering agent=None the source must probe each
    known agent rather than defaulting."""
    _seed(app, agent="codex")
    del app.session_work[_SID]  # /work now answers its empty not-an-oracle shape
    result = _service(client).get_entity(f"session:{_SID}", view="transcript")
    assert result["data"]["agent"] == "codex"


def test_qualified_ref_names_the_agent_directly(client, app):
    _seed(app, agent="codex")
    result = _service(client).get_entity(f"session:codex/{_SID}", view="transcript")
    assert result["data"]["agent"] == "codex"


def test_unknown_agent_in_ref_is_rejected_by_name(client, app):
    with pytest.raises(errors.ValidationError, match="cursor|claude_code") as excinfo:
        _service(client).get_entity(f"session:cursor/{_SID}")
    assert "claude_code" in str(excinfo.value)  # names the real vocabulary


def test_missing_transcript_says_capture_may_be_off_not_absent_session(client, app):
    """A session listed on a project can have no captured transcript at all.
    The error must say so — "no transcript" read as "no session" would send an
    agent away from work that demonstrably happened."""
    _seed(app)
    del app.session_transcripts[(_SID, "claude_code")]
    with pytest.raises(errors.NotFoundError, match="capture"):
        _service(client).get_entity(f"session:{_SID}", view="transcript")


# -- card ----------------------------------------------------------


def test_card_is_the_work_read_with_views_and_url(client, app, monkeypatch):
    monkeypatch.setenv("PROBE_DASHBOARD_URL", "https://research.example.com")
    _seed(app)
    result = _service(client).get_entity(f"session:{_SID}")

    entity = result["data"]["entity"]
    assert entity["id"] == _SID
    # `name` is the server-derived headline (`/work` carries it since sessions
    # gained one); `digest_title` left with the digest lane and no response
    # carries it, so a card field by that name would always be absent.
    assert entity["name"] == "design session"
    assert entity["projects"] == [{"id": "p-1", "name": "folding"}]
    assert result["data"]["available_views"] == ["card", "record", "transcript"]
    # No url. The digest cutover deleted `/sessions/[id]`, and a link to a route
    # that 404s is worse than telling the caller there is none; the transcript
    # view is how a session's content is read now.
    assert result["data"].get("url") is None


def test_empty_work_card_still_answers(client, app):
    """/work is not an oracle: an unknown well-formed id answers empty, and the
    card passes that through as "not observed" rather than 404ing an id another
    read (the transcript) may still resolve."""
    result = _service(client).get_entity(f"session:{_SID}")
    assert result["data"]["entity"]["id"] == _SID
    assert result["data"]["entity"]["runs"] == []


# `test_digest_view_is_the_structured_digest` stood here. The digest view, the
# kind behind it and its route all retired in the cutover; a session's views are
# now card, record and transcript.


def test_unknown_filter_on_transcript_is_rejected(client, app):
    _seed(app)
    with pytest.raises(errors.ValidationError, match="grep"):
        _service(client).get_entity(
            f"session:{_SID}", view="transcript", filters={"pattern": "fox"}
        )


# -- review hardening: the fixes from the pre-merge review ----------------------


@pytest.mark.parametrize(
    "bad_id",
    [
        "codex/../../v1/me",  # path traversal out of /sessions/
        "abc?source=evil",  # query-string truncation of the path
        "abc#frag",  # fragment truncation
        "has space",  # whitespace
        "short",  # under the 8-char floor
    ],
)
def test_malformed_session_id_is_rejected_before_the_wire(client, app, bad_id):
    """A session id becomes a URL path segment, so a value carrying '/', '?',
    '#', or whitespace could re-steer the request to another route or silently
    truncate it. The shape gate refuses it before any request is made."""
    _seed(app)
    before = len(app.requests)
    with pytest.raises(errors.ValidationError, match="session id"):
        _service(client).get_entity(f"session:codex/{bad_id}", view="transcript")
    # Nothing was sent: the malformed id never reached the transport.
    assert all("/sessions/" not in str(r.url) or bad_id not in str(r.url) for r in app.requests[before:])


def test_traversal_id_does_not_reach_the_transport(client, app):
    """The sharpest case: the id that would escape /sessions/ onto another GET
    route must not produce any request at all."""
    with pytest.raises(errors.ValidationError):
        _service(client).get_entity("session:codex/x/../../v1/me")
    assert not any("v1/me" in str(r.url) for r in app.requests)


def test_start_line_with_grep_is_rejected_not_ignored(client, app):
    """start_line is a plain-read control the grep scan never reads; accepting
    it beside grep would be the accepted-but-inert lie the filter table guards
    against (symmetric with context_lines-without-grep)."""
    _seed(app, lines=50)
    with pytest.raises(errors.ValidationError, match="start_line"):
        _service(client).get_entity(
            f"session:{_SID}", view="transcript", filters={"grep": "fox", "start_line": 20}
        )


@pytest.mark.parametrize("bad_grep", [["a", "b"], 123, {"x": 1}])
def test_non_string_grep_is_rejected(client, app, bad_grep):
    """A list/dict/int would str()-coerce into a surprising literal search, so
    the view refuses a non-string needle rather than answering one."""
    _seed(app, lines=10)
    with pytest.raises(errors.ValidationError, match="non-empty string"):
        _service(client).get_entity(
            f"session:{_SID}", view="transcript", filters={"grep": bad_grep}
        )


def test_empty_grep_degrades_to_a_plain_read(client, app):
    """An empty-string filter value is dropped by the service before the view
    sees it, so `grep=""` is a plain sectioned read (bounded), NOT a whole-
    document match-every-line scan -- the empty-needle DoS never forms."""
    _seed(app, lines=10)
    result = _service(client).get_entity(
        f"session:{_SID}", view="transcript", filters={"grep": ""}
    )
    assert "completeness" not in result
    # Plain-read sections (line_start/line_end tiling), not per-match rows.
    assert result["data"]["sections"][0]["line_start"] == 1
    assert "line" not in result["data"]["sections"][0]


def test_source_filter_is_no_longer_accepted(client, app):
    """`source` was dropped: `session:<agent>/<id>` already names the agent on
    the ref, so a source filter could only contradict it and have one side win
    silently."""
    _seed(app)
    with pytest.raises(errors.ValidationError, match="grep"):
        _service(client).get_entity(
            f"session:{_SID}", view="transcript", filters={"source": "codex"}
        )


def test_line_numbering_splits_on_newline_only_and_preserves_content(client, app):
    """splitlines() breaks on \\r, \\f, NEL and U+2028/9 too, which renumbers
    lines away from the backend's \\n counting and drops those bytes from the
    exact-content read. A bare \\r inside a line must stay one line, verbatim."""
    content = "alpha\rbeta\ngamma\ndelta"  # 3 newline-lines; line 1 holds a bare \r
    app.session_transcripts[(_SID, "claude_code")] = {
        "session_id": _SID,
        "agent": "claude_code",
        "title": "cr test",
        "content": content,
        "chunk_count": 1,
        "body_size_bytes": len(content.encode()),
    }
    app.session_work[_SID] = {
        "session_id": _SID,
        "agent": "claude_code",
        "projects": [],
        "experiments": [],
        "runs": [],
        "artifacts": [],
    }
    result = _service(client).get_entity(f"session:{_SID}", view="transcript")
    assert result["data"]["total_lines"] == 3
    assert "alpha\rbeta" in result["data"]["sections"][0]["text"]


def test_grep_pages_multiple_matches_with_more_beyond(client, app):
    """Every line matches, so grep produces one section per line; the page is
    bounded and the cursor walks the rest with more_beyond driving continuation."""
    _seed(app, lines=500)  # every line contains "fox"
    service = _service(client)
    first = service.get_entity(
        f"session:{_SID}", view="transcript", filters={"grep": "fox"}, token_budget=600
    )
    assert first["completeness"]["state"] == "partial"
    assert first["next_cursor"]
    seen = [s["line"] for s in first["data"]["sections"]]
    cursor = first["next_cursor"]
    while cursor:
        page = service.get_entity(
            f"session:{_SID}",
            view="transcript",
            filters={"grep": "fox"},
            token_budget=600,
            cursor=cursor,
        )
        seen.extend(s["line"] for s in page["data"]["sections"])
        cursor = page.get("next_cursor")
    assert seen == list(range(1, 501))  # every match, in order, exactly once


def test_pre_sessions_backend_reads_as_predates_not_absent(client, app):
    """A backend without the /v1/sessions/* routes 404s /work raw. That must
    read as 'upgrade the server', not 'this session does not exist' -- a current
    backend answers an unknown session with an EMPTY work read, never a 404."""
    app.sessions_route_absent = True
    with pytest.raises(errors.NotFoundError, match="predates"):
        _service(client).get_entity(f"session:{_SID}")


def test_transcript_agents_cover_every_capture_source():
    """The 2026-08-28 straggler, pinned: the 44-branch audit swept cli/ and
    missed mcp/source.py's private two-source tuple, so the read surface
    rejected 'pi' transcripts the backend was happily storing. Tie the tuple
    to the capture-source vocabulary so source #4 cannot repeat this."""
    from probe.mcp.source import _TRANSCRIPT_AGENTS

    assert set(_TRANSCRIPT_AGENTS) == {"claude_code", "codex", "pi"}
