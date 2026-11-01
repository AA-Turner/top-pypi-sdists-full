"""SessionsResource (client.sessions, typed reads) and SessionsMixin, Client's methods: captured
coding-agent sessions, their transcripts and ATIF export (twin: app/sessions)."""

from __future__ import annotations
from ....generated.models import (
    SessionCreatedOut,
    SessionTrajectoryOut,
    SessionTranscriptOut,
    SessionWorkOut,
)
from ..resource import Resource

from ... import errors


#: The agent a captured session belongs to when a caller names none: the
#: harness that was first and is still the most common. Part of the session
#: document's identity server-side, not a filter.
DEFAULT_SESSION_SOURCE = "claude_code"


class SessionsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- captured coding-agent sessions ---------------------------------------

    def session_work(self, session_id: str, *, limit: int | None = None) -> dict:
        """``GET /v1/sessions/{id}/work`` — everything one captured session
        touched, grouped by entity type.

        An unknown well-formed id answers EMPTY rather than 404 (the route is
        deliberately not an oracle for another product's ids), so absence of
        work is not proof the session never existed -- the transcript read is
        the existence check.
        """
        params = {"limit": limit} if limit is not None else None
        return self.transport.get(f"/v1/sessions/{session_id}/work", params=params)

    def send_session_message(self, session_id: str, body: str) -> dict:
        """``POST /v1/sessions/{id}/messages`` — a message for a running session
        of your own: its Probe daemon hands it to the agent at the agent's next
        prompt or tool call (and wakes an idle Claude Code or pi). Sent with a
        token, it reaches the agent as from one of your agent sessions (this
        one, when the request names it), never as from you. 403 for another
        person's session, 429 past 20 a minute. Returns the message with its
        ``state`` (``queued``, ``unreachable``: no Probe daemon polled in 2 min,
        ...) and ``reachable``. Never retried: a lost answer is no reason to say
        it twice."""
        return self.transport.post(f"/v1/sessions/{session_id}/messages", {"body": body})

    def delete_session(self, session_id: str, *, dry_run: bool = False) -> dict:
        """``DELETE /v1/sessions/{id}`` -- delete one of your captured sessions
        (research-os 0411). It is hidden from search at once and deleted for
        good after ``purge_after`` (7 days), unless ``undelete_session`` undoes
        it first; the owner is emailed. Answers the request (``state``,
        ``purge_after``, ``can_undo``, ``note``); an existing request is
        answered again, never doubled. ``dry_run`` checks and describes, and
        writes nothing. 403 for a teammate's session or an agent's credential,
        and (``detail.code`` ``workspace_write_denied``) for one linked to a
        project you cannot write: its deletion would roll that project's page
        back, so ask one of its writers or an admin. 404 for an id the team has
        never seen."""
        resp = self.transport.request(
            "DELETE",
            f"/v1/sessions/{session_id}",
            params={"dry_run": "true"} if dry_run else None,
            idempotent=True,
        )
        return resp.json()

    def undelete_session(self, session_id: str) -> dict:
        """``POST /v1/sessions/{id}/undelete`` -- undo ``delete_session`` while
        its window is open. 409 once the deletion has started."""
        return self.transport.post(f"/v1/sessions/{session_id}/undelete", None, idempotent=True)

    def session_deletion(self, session_id: str) -> dict:
        """``GET /v1/sessions/{id}/deletion`` -- where your deletion of this
        session stands. 404 when you asked for none."""
        return self.transport.get(f"/v1/sessions/{session_id}/deletion")

    def session_created(self, session_id: str) -> dict:
        """``GET /v1/sessions/{id}/created`` — the ids of every project,
        experiment and run that session CREATED (research-os 0291), not merely
        touched: ``{session_id, project_ids, run_ids, truncated}``. An unknown
        well-formed id answers empty, as ``session_work`` does."""
        return self.transport.get(f"/v1/sessions/{session_id}/created")

    def session_transcript(self, session_id: str, *, source: str = DEFAULT_SESSION_SOURCE) -> dict:
        """``GET /v1/sessions/{id}/transcript`` — the complete normalized
        transcript captured for one session.

        ``source`` names the agent that recorded it (``claude_code`` /
        ``codex``) and is part of the document's identity, not a filter: the
        same id under the wrong source 404s. The content is the normalized,
        secret-gated document the engine indexed, not the agent's raw local
        JSONL -- the capture pipeline strips bookkeeping payloads first.
        """
        return self.transport.get(
            f"/v1/sessions/{session_id}/transcript", params={"source": source}
        )

    def session_trajectory(
        self,
        session_id: str,
        *,
        source: str = DEFAULT_SESSION_SOURCE,
        step_from: int = 1,
        step_limit: int = 200,
    ) -> dict:
        """``GET /v1/sessions/{id}/trajectory`` — one page of the session as an
        ATIF trajectory (Harbor's Agent Trajectory Interchange Format), written
        when the session ends: ``{session_id, agent, total_steps, step_from,
        next_step_from, trajectory}``. 404 with ``reason`` ``not_built`` means
        there is none to serve (still running, or too large); read the transcript."""
        return self.transport.get(
            f"/v1/sessions/{session_id}/trajectory",
            params={"source": source, "step_from": step_from, "step_limit": step_limit},
        )

    def export_session_trajectory(self, session_id: str, *, source: str = DEFAULT_SESSION_SOURCE) -> dict:
        """The whole trajectory as one ATIF document: every page of
        ``session_trajectory`` with the steps joined in order. Valid ATIF for
        Harbor, Phoenix or Transluce. The trajectory never carries tool
        arguments or tool output. Raises ``errors.ServerError`` when the pages
        do not add up to the document (a cursor that stops early, or a
        trajectory rewritten between pages), never a silently partial one."""
        step_from = 1
        document: dict | None = None
        total: int | None = None
        steps: list = []
        while True:
            page = self.session_trajectory(
                session_id, source=source, step_from=step_from, step_limit=2000
            )
            trajectory = page["trajectory"]
            if document is None:
                document = {k: v for k, v in trajectory.items() if k != "steps"}
                total = page.get("total_steps")
            elif page.get("total_steps") != total:
                raise errors.ServerError("the session's trajectory changed while it was read")
            steps.extend(trajectory.get("steps") or [])
            following = page.get("next_step_from")
            if following is None:
                break
            if following <= step_from:
                raise errors.ServerError(f"trajectory paging stopped at step {step_from}")
            step_from = following
        assert document is not None
        if total is not None and len(steps) != total:
            raise errors.ServerError(f"trajectory pages held {len(steps)} of {total} steps")
        document["steps"] = steps
        return document


class SessionsResource(Resource):
    """`client.sessions`: typed reads of one captured coding-agent session."""

    __slots__ = ()

    def get_work(self, session_id: str, *, limit: int | None = None) -> SessionWorkOut:
        """`Client.session_work` as a `SessionWorkOut`."""
        return self._to_model(SessionWorkOut, self._client.session_work(session_id, limit=limit))

    def get_created(self, session_id: str) -> SessionCreatedOut:
        """`Client.session_created` as a `SessionCreatedOut`."""
        return self._to_model(SessionCreatedOut, self._client.session_created(session_id))

    def get_transcript(
        self, session_id: str, *, source: str = DEFAULT_SESSION_SOURCE,
    ) -> SessionTranscriptOut:
        """`Client.session_transcript` as a `SessionTranscriptOut`."""
        return self._to_model(
            SessionTranscriptOut,
            self._client.session_transcript(session_id, source=source),
        )

    def get_trajectory(
        self, session_id: str, *, source: str = DEFAULT_SESSION_SOURCE, step_from: int = 1,
        step_limit: int = 200,
    ) -> SessionTrajectoryOut:
        """`Client.session_trajectory` as a `SessionTrajectoryOut`."""
        return self._to_model(
            SessionTrajectoryOut,
            self._client.session_trajectory(
                session_id, source=source, step_from=step_from, step_limit=step_limit,
            ),
        )
