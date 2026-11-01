"""session views: the captured sessions behind a run, file, project or experiment, and a transcript in line sections."""

from __future__ import annotations
from typing import Any
from ....sdk import errors
from ...delivery import accounting
from ....shared.reads.search_contract import (
    EntityType,
    MissingMarker)
from ...delivery.context import current_delivery, pin_document, source_changed
from ...source.sessions import _TRANSCRIPT_AGENTS
from probe.mcp.tools.view import _Req, _ViewData
from probe.mcp.tools.views.overview import _experiment_project_id

#: The artifact sessions route caps `limit` at 50, and the run bundle's session
#: list is capped server-side at the same number; neither takes an offset.
_SESSIONS_ROUTE_MAX = 50

#: What a captured-session row keeps (AgentSessionOut). The OWNER is the point:
#: "who made this" is answered by a person, not a session id.
_SESSION_ROW_FIELDS = (
    "name",
    "title",
    "agent",
    "owner_name",
    "owner_email",
    "device_label",
    "first_seen_at",
    "last_seen_at",
)


def _session_row(row: dict) -> dict:
    """One captured session as a row an agent can OPEN: `uuid` is the
    `session:` address `entity` takes, qualified by its agent when the agent is
    one the transcript read knows (a bare id is resolved by probing each)."""
    session_id = row.get("session_id")
    agent = row.get("agent")
    address = (
        f"{EntityType.SESSION.value}:{agent}/{session_id}"
        if agent in _TRANSCRIPT_AGENTS
        else f"{EntityType.SESSION.value}:{session_id}"
    )
    out: dict = {"uuid": address}
    out.update({key: row[key] for key in _SESSION_ROW_FIELDS if row.get(key) is not None})
    if row.get("direct") is False:
        # Reached through a child (a run's session seen on its project, say).
        # Absent means direct, the common case, so only the exception is said.
        out["direct"] = False
    return out


def _sessions_view(sessions: Any, total: Any) -> _ViewData:
    """A `sessions` view: the rows the server returned, plus its exact total.

    Both routes cap the list server-side and take no offset, so a total above
    the rows is reported (`sessions_beyond_server_limit`) rather than paged --
    a cursor here would walk an already-cut list and call its end the end.

    Under `X-Probe-Hide-Session-Work` the WATCHED session is left out, like its
    work in every other view: asked "which session made this run", the daemon's
    reader must not answer with the session it is reading beside. The total is
    lowered with it, so the count still says what the rows can add up to --
    and when the list was cut before the watched session would have appeared,
    whether the server's total counted it is unknowable, so the count is a
    floor (`session_total_at_least`), never a number that may be one too high."""
    watched = accounting.session_work_to_hide()
    listed = [s for s in sessions or [] if isinstance(s, dict) and s.get("session_id")]
    count = total if isinstance(total, int) and not isinstance(total, bool) else len(listed)
    floor = False
    if watched is not None:
        kept = [s for s in listed if str(s["session_id"]).lower() != watched.lower()]
        if len(kept) < len(listed):
            count = max(len(kept), count - (len(listed) - len(kept)))
        elif count > len(listed):
            # Capped, and the watched session was not in the part returned: it
            # may be among the rest, or may never have touched this entity.
            count, floor = max(len(kept), count - 1), True
        listed = kept
    rows = [_session_row(s) for s in listed]
    return _ViewData(
        payload={"session_total_at_least" if floor else "session_total": count},
        rows=rows,
        rows_key="sessions",
        missing=(
            [MissingMarker.SESSIONS_BEYOND_SERVER_LIMIT]
            if count > len(rows) or floor
            else []
        ),
    )


def _session_id_of(address: str) -> str:
    """The bare session id from a `session:` address as `_session_row` writes
    it (`session:<agent>/<id>` or `session:<id>`) -- what the sessions routes
    take as `after`. A bare id passes through."""
    rest = (
        address.split(":", 1)[1] if address.startswith(f"{EntityType.SESSION.value}:") else address
    )
    return rest.rsplit("/", 1)[-1]


def _paged_sessions_view(page: dict) -> _ViewData:
    """A `sessions` view over a route that PAGES (a project's or an experiment's):
    one route page of rows, newest first, the exact total, and the walk past
    it on the route's own key -- each row's `uuid` is the `after` the next
    page starts from (`resume_key`).

    Under `X-Probe-Hide-Session-Work` the WATCHED session is left out, as in
    `_sessions_view`. The total is lowered when it was on this page; when it
    was not, whether it sits on another page is unknowable from here, so the
    count is a floor (`session_total_at_least`). `resume_fetched` names the
    last row FETCHED, so a page the exclusion empties still advances."""
    if "next_after" not in page:
        # A server before the paged routes: the experiment route ignored
        # `order` and `after` and answered the leaf door's oldest-first 50 with
        # no page key. That is the capped, uncursored list `_sessions_view` was
        # written for; read as a page it would claim a 300-session entity
        # complete at 50 rows. (The hosted MCP and the API deploy apart.)
        return _sessions_view(page.get("sessions"), page.get("session_total"))
    watched = accounting.session_work_to_hide()
    listed = [s for s in page.get("sessions") or [] if isinstance(s, dict) and s.get("session_id")]
    total = page.get("session_total")
    count = total if isinstance(total, int) and not isinstance(total, bool) else len(listed)
    more = bool(page.get("next_after")) and bool(listed)
    fetched_last = _session_row(listed[-1])["uuid"] if listed else None
    floor = False
    if watched is not None:
        kept = [s for s in listed if str(s["session_id"]).lower() != watched.lower()]
        if len(kept) < len(listed):
            count = max(len(kept), count - (len(listed) - len(kept)))
        elif more or count > len(listed):
            count, floor = max(len(kept), count - 1), True
        listed = kept
    return _ViewData(
        payload={"session_total_at_least" if floor else "session_total": count},
        rows=[_session_row(s) for s in listed],
        rows_key="sessions",
        more_beyond=more,
        resume_key="uuid",
        resume_fetched=fetched_last,
    )


class SessionsViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def _view_run_sessions(self, entity: dict, request: _Req) -> _ViewData:
        """The captured coding sessions that produced this run, read off the run
        BUNDLE -- the only route that carries them."""
        bundle = self.source.bundle(str(entity["id"]))
        return _sessions_view(bundle.get("sessions"), bundle.get("session_total"))

    def _view_artifact_sessions(self, entity: dict, request: _Req) -> _ViewData:
        """The captured sessions that registered or touched this file."""
        out = self.source.artifact_sessions(str(entity["id"]), limit=_SESSIONS_ROUTE_MAX)
        return _sessions_view(out.get("sessions"), out.get("session_total"))

    def _view_project_sessions(self, entity: dict, request: _Req) -> _ViewData:
        """The captured sessions that worked on the project or on anything in it
        (`direct` false names the child), NEWEST first, one route page per call
        and the walk past it by `cursor`. Each row's `uuid` opens the session;
        `view_options.grep` on its transcript is the project-scoped search
        that `search` cannot do over transcripts."""
        page = self.source.project_sessions(
            str(entity["id"]),
            order="newest",
            limit=_SESSIONS_ROUTE_MAX,
            after=_session_id_of(request.after) if request.after else None,
        )
        return _paged_sessions_view(page)

    def _view_experiment_sessions(self, entity: dict, request: _Req) -> _ViewData:
        """The experiment's sessions: the same page as a project's."""
        page = self.source.experiment_sessions(
            str(entity["id"]),
            project_id=_experiment_project_id(entity),
            order="newest",
            limit=_SESSIONS_ROUTE_MAX,
            after=_session_id_of(request.after) if request.after else None,
        )
        return _paged_sessions_view(page)

    @staticmethod
    def _transcript_int(filters: dict[str, Any], name: str, *, default: int, floor: int) -> int:
        """One transcript filter as an int, rejected loudly when it is not one.

        Coerced here rather than trusted: filters arrive as arbitrary JSON, and
        a string "3" silently comparing False against every int would make the
        filter a no-op wearing the caller's value -- the silent-ignore failure
        the _VIEW_OPTIONS table exists to prevent.
        """
        value = filters.get(name, default)
        if isinstance(value, bool) or not isinstance(value, int) or value < floor:
            raise errors.ValidationError(
                f"{name} must be an integer >= {floor}, got {value!r}",
                status=422,
            )
        return value

    def _view_session_transcript(self, entity: dict, request: _Req) -> _ViewData:
        """The transcript itself, in bounded line sections -- never whole.

        The backend returns ONE complete normalized document (the dashboard's
        read), so every narrowing here is client-side over content the call
        already paid for -- the same honesty class as the artifact
        `requirement` filter. Plain reads section the document from
        `start_line`; `grep` (literal, case-insensitive) returns one section
        per matching line with `context_lines` of surroundings, which is the
        "search within THIS session" read that chunk-ranked search
        cannot promise. Either shape rides the ordinary rows machinery, so
        token_budget bounds what one response carries and the cursor walks the
        rest.
        """
        agent = entity.get("agent") or None
        try:
            doc = self.source.session_transcript(str(entity["id"]), agent=agent)
        except errors.NotFoundError as exc:
            context = current_delivery()
            if context and context.snapshot:
                raise source_changed("captured transcript is unavailable") from exc
            raise
        content = pin_document(
            doc.get("content") or "",
            f"transcript:{entity['id']}:{doc.get('agent') or agent or ''}",
        )
        # split on "\n" ONLY. str.splitlines() also breaks on \r, \f, NEL, and
        # U+2028/9 -- ordinary bytes inside captured terminal output and code
        # blocks -- which would (a) renumber lines away from the backend's own
        # \n counting, so a `line`/`start_line` coordinate points at different
        # text on the dashboard, and (b) drop those bytes from the rejoined
        # section, corrupting what is meant to be an exact-content read.
        lines = content.split("\n")
        total = len(lines)
        payload: dict[str, Any] = {
            "agent": doc.get("agent"),
            "title": doc.get("title"),
            "total_lines": total,
            "body_size_bytes": (
                len(content.encode("utf-8")) if current_delivery() else doc.get("body_size_bytes")
            ),
            "filters": request.filters or None,
        }
        # Build ONLY the caller's window (offset + one page) plus a lookahead,
        # never a section per 40 lines of the whole document: a multi-MB
        # transcript is tens of thousands of sections, each re-joining its lines
        # into a second full copy of the content, and _fit emits a handful. The
        # per-page re-fetch of the whole document stays (the backend transcript
        # route has no line-range parameter) -- TODO(backend): a start_line/limit
        # query would make a full walk linear instead of O(pages * doc), the same
        # shape as the _bounded() span-walk TODO.
        return self._line_sections(lines, request, payload, noun="transcript")
