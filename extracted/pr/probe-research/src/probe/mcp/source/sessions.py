"""captured-session reads: sessions behind a project, experiment or file, one session, its transcript."""

from __future__ import annotations
import re
from typing import Any

from ...sdk import errors
from probe.mcp.source.people import PeopleFilters
from ..delivery.context import current_delivery, source_changed

# The agents whose sessions the capture pipeline records, in the order a bare
# `session:<id>` ref tries them. Mirrors the backend's TranscriptAgent literal:
# `source` is part of the transcript document's identity, so an unqualified id
# has to be resolved by asking, not by guessing one and reading its 404 as
# "never captured".
def _transcript_agents() -> tuple[str, ...]:
    from probe.foundation.harness_registry import get_registry

    return tuple(h.id for h in get_registry().captured())


_TRANSCRIPT_AGENTS = _transcript_agents()

# The session-id SHAPE, byte-for-byte the backend's `_SESSION_RE`
# (app/runs/agent_session.py): the id lands in a URL path segment
# (`/v1/sessions/{id}/...`), so a value carrying `/`, `?`, `#`, `..` or
# whitespace would silently re-steer the request -- `?` truncates the path and
# turns a real read into a bogus empty one, `..` walks out of `/sessions/` onto
# another GET route under the same read token. Validating the shape here, at the
# one point every session ref resolves through, closes that off with the SAME
# gate the write path already enforces, so a value that could never have been
# stored never reaches the wire.
_SESSION_ID_RE = re.compile(r"\A[A-Za-z0-9._:-]{8,200}\Z")


class SessionReadsMixin:
    """Part of ResearchOSSource: its methods run with `self` the ResearchOSSource; compose() folds them into ResearchOSSource."""

    def session_created(self, session_id: str) -> dict:
        """``GET /v1/sessions/{id}/created``: what that session CREATED (0291)."""
        return self.client.session_created(session_id)

    def artifact_sessions(self, artifact_id: str, *, limit: int) -> dict:
        """``GET /v1/artifacts/{id}/sessions``: `{sessions, session_total}`, the
        captured sessions that registered or touched the file."""
        return self.client.transport.get(
            f"/v1/artifacts/{artifact_id}/sessions", params={"limit": limit}
        )

    def fetch_sessions(
        self,
        *,
        filters: PeopleFilters,
        project_id: str | None = None,
        cursor: str | None = None,
        limit: int,
    ) -> dict:
        """``GET /v1/sessions``: one page of the team's agent sessions, newest activity first:
        `{sessions, next_cursor, owner_matched?, unowned_count?}` (people and time filters B1)."""
        parameters: dict[str, Any] = {"limit": limit, **filters.to_query()}
        if project_id:
            parameters["project_id"] = project_id
        if cursor:
            parameters["cursor"] = cursor
        return self.client.transport.get("/v1/sessions", params=parameters) or {}

    # -- an entity's sessions, one page at a time ------------------------------

    def project_sessions(
        self, project_id: str, *, order: str, limit: int, after: str | None = None
    ) -> dict:
        """``GET /v1/projects/{P}/sessions``: `{sessions, session_total,
        next_after}`, the captured sessions that worked on the project or on
        something in it, in `order` (`newest` | `oldest`), past `after`."""
        return self.client.list_project_sessions(project_id, order=order, after=after, limit=limit)

    def experiment_sessions(
        self,
        experiment_id: str,
        *,
        project_id: str | None,
        order: str,
        limit: int,
        after: str | None = None,
    ) -> dict:
        """``GET /v1/projects/{P}/experiments/{E}/sessions``: the same page as
        `project_sessions`, for an experiment."""
        return self.client.list_experiment_sessions(
            experiment_id, project_id=project_id, order=order, after=after, limit=limit
        )

    # -- captured coding-agent sessions ----------------------------------------

    def _session_entity(self, value: str) -> dict:
        """Resolve ``session:<id>`` or ``session:<agent>/<id>`` to its entity.

        The entity is the session's WORK read -- what it touched, grouped by
        entity type -- because that is a session's identity to a reader: "the
        session that produced run X" is how one is ever referred to. The
        transcript stays behind ``view="transcript"``; inlining megabytes of it
        on the card would make the cheap glance the most expensive read here.

        `/work` answers EMPTY for an unknown well-formed id (deliberately not an
        oracle for another product's ids), so an all-empty entity is "not
        observed here", not proof of absence -- the transcript view is the
        existence check, and its 404 is honest.
        """
        agent, sep, session_id = value.partition("/")
        if not sep:
            agent, session_id = "", value
        elif agent not in _TRANSCRIPT_AGENTS:
            raise errors.ValidationError(
                f"unknown session agent {agent!r}: a qualified session ref is "
                f"session:<agent>/<id> with agent one of {sorted(_TRANSCRIPT_AGENTS)}, "
                f"and a bare session:<id> resolves the agent itself",
                status=422,
            )
        if not session_id:
            raise errors.ValidationError(
                "a session ref needs an id: session:<id> or session:<agent>/<id> "
                "(ids ride on the `sessions` field of project/experiment/run reads)",
                status=422,
            )
        if not _SESSION_ID_RE.match(session_id):
            # The id becomes a URL path segment; a value the backend could never
            # have stored must be refused HERE rather than sent to re-steer the
            # request. Same shape the write path enforces (backend `_SESSION_RE`).
            raise errors.ValidationError(
                f"{session_id!r} is not a session id: ids are 8-200 chars of "
                f"letters, digits, and '.', '_', ':', '-' (a URL path segment, so "
                f"'/', '?', '#', and whitespace are rejected)",
                status=422,
            )
        try:
            entity = dict(self.client.session_work(session_id))
        except errors.NotFoundError as exc:
            # `/work` never 404s a well-formed id on a backend that HAS the route
            # -- an unobserved id answers EMPTY by design. So a 404 here is not
            # "no such session", it is "this backend predates the session routes",
            # and resolution gates ALL three views. Say that instead of letting a
            # raw 404 read as data loss (the browse/search pattern).
            raise errors.NotFoundError(
                f"this Probe backend predates the agent-session routes "
                f"(GET /v1/sessions/{{id}}/work): upgrade the server to read "
                f"session {session_id}. A current backend answers an unknown "
                f"session with an empty work read, never a 404."
            ) from exc
        entity["id"] = session_id
        if agent:
            # The caller's explicit agent outranks the observation: /work reports
            # `agent: null` for a session it never saw an entity link from, and
            # the transcript read needs the value to address the document.
            entity["agent"] = agent
        return entity

    def session_transcript(self, session_id: str, *, agent: str | None = None) -> dict:
        """The complete normalized transcript, resolving the agent if unnamed.

        ``source`` is part of the document's identity server-side, so a bare id
        is tried under each known agent rather than defaulting to one -- a
        default would read every codex session as "never captured". A probe per agent,
        bounded by the size of ``_TRANSCRIPT_AGENTS``, and only on refs that
        did not name the agent.
        """
        context = current_delivery()
        if context and context.snapshot:
            # Resolve once. Later pages must not fall through to another
            # recording agent when the original transcript is deleted.
            prefix = f"transcript:{session_id}:"
            if not context.snapshot["source"].startswith(prefix):
                raise source_changed("document identity changed")
            agent = context.snapshot["source"][len(prefix) :]
        if agent is not None and agent not in _TRANSCRIPT_AGENTS:
            # Caught here, not left to the backend's literal-validation 422:
            # that error names a Pydantic type, and the fix is a value.
            raise errors.ValidationError(
                f"unknown transcript source {agent!r}: one of {sorted(_TRANSCRIPT_AGENTS)}",
                status=422,
            )
        candidates = (agent,) if agent is not None else _TRANSCRIPT_AGENTS
        last: errors.NotFoundError | None = None
        for candidate in candidates:
            try:
                return self.client.session_transcript(session_id, source=candidate)
            except errors.NotFoundError as exc:
                last = exc
        # One message for both the named-agent and probed paths: the backend's
        # bare "transcript not found" reads as "no such session", and sending an
        # agent away from work that demonstrably happened is the expensive
        # misreading.
        tried = agent or f"any known agent ({', '.join(_TRANSCRIPT_AGENTS)})"
        raise errors.NotFoundError(
            f"no captured transcript for session {session_id} under {tried}. "
            f"A session listed on a project or run can still have no "
            f"transcript: capture may not have been enabled on the machine "
            f"that ran it."
        ) from last
