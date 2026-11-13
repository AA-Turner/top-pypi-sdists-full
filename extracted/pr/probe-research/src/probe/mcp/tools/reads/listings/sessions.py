"""browse mode=sessions: the team's agent sessions, newest activity first, each with whose it is and what it touched."""

from __future__ import annotations

from .....shared.reads.search_contract import EntityType
from ....delivery import accounting
from probe.mcp.source.people import PeopleFilters
from probe.mcp.tools.shaping.people import get_owner_echo, to_person_card


class SessionRowsMixin:
    """Part of BrowseListMixin: fold_parts() copies its methods in, and they run with `self` the ResearchReadService."""

    #: `GET /v1/sessions` caps `limit` at 50: what a continuation re-reads to find the row it stopped after.
    _SESSIONS_REREAD_LIMIT = 50
    #: The digest line a row carries, cut to this many characters (the full one is entity(view="card")).
    _SESSION_SUMMARY_CHARS = 280
    #: Work links a row carries (the route sends at most 5); a row is never split, so it stays bounded.
    _SESSION_WORK_MAX = 5

    @staticmethod
    def _get_session_identity(row: dict) -> str:
        agent, session_id = row.get("agent"), row.get("session_id")
        return f"{agent}/{session_id}" if agent else str(session_id)

    def _build_session_row(self, row: dict) -> dict:
        """One session as an `entity` address plus who, when and what: `ref` opens it
        (`view="transcript"` reads the conversation). `summary` only when the server has one: session
        digests stopped being written on 2026-09-11, so most newer sessions have none."""
        out: dict = {"ref": f"{EntityType.SESSION.value}:{self._get_session_identity(row)}"}
        out.update({key: row[key] for key in ("name", "title", "agent") if row.get(key)})
        owner = to_person_card(row.get("owner"))
        if owner:
            out["owner"] = owner
        out.update(
            {key: row[key] for key in ("device_label", "first_seen_at", "last_seen_at") if row.get(key)}
        )
        summary = row.get("summary")
        if isinstance(summary, str) and summary.strip():
            out["summary"] = summary.strip()[: self._SESSION_SUMMARY_CHARS]
            if len(summary.strip()) > self._SESSION_SUMMARY_CHARS:
                out["summary_truncated"] = True
        work = [
            {
                **{key: item[key] for key in ("kind", "name") if item.get(key)},
                "ref": f"{item['kind']}:{item['id']}",
            }
            for item in row.get("work") or []
            if isinstance(item, dict) and item.get("kind") and item.get("id")
        ]
        if work:
            out["work"] = work[: self._SESSION_WORK_MAX]
            if len(work) > self._SESSION_WORK_MAX:
                out["work_truncated"] = True
        out["entity_type"] = EntityType.SESSION.value
        return out

    def _list_sessions_page(
        self, *, backend_cursor, cursor, data, last_sent, mode, page_size, people: PeopleFilters, scope, sent,
    ) -> str | None:
        """mode=sessions: one page after the last row sent; the cursor after the page. The route's
        cursor is its own and opaque here, so a cut inside a page resumes by finding the last row sent
        again from the same position (refused, never guessed, if it is gone), as the catalog modes do."""
        project_id = None
        if scope is not None:
            _, project_id = self._uuid_ref(
                scope, (EntityType.PROJECT.value,), what="browse(mode='sessions') scope"
            )
            data["scope"] = scope
        position, resume_after = backend_cursor, last_sent
        page = self.source.fetch_sessions(
            filters=people,
            project_id=project_id,
            cursor=position,
            limit=page_size if resume_after is None else self._SESSIONS_REREAD_LIMIT,
        )
        data.update(get_owner_echo(page))
        rows = [
            row for row in (page or {}).get("sessions") or [] if isinstance(row, dict) and row.get("session_id")
        ]
        # The caller's own session is the conversation asking, left out as search leaves out its
        # transcript (the ambient `X-Probe-Agent-Session`); said, so a short page is not read as all.
        own = accounting.calling_agent_session()
        if own is not None and any(row.get("session_id") == own[1] for row in rows):
            data["own_session_left_out"] = True
            rows = [row for row in rows if row.get("session_id") != own[1]]
        start = 0
        if resume_after is not None:
            found = next(
                (i for i, row in enumerate(rows) if self._get_session_identity(row) == resume_after), None
            )
            if found is None:
                raise self._gone("session")
            # Newest activity first moves rows: refused, never skipped, once the last row sent moved.
            self._check_resume_index(cursor, found, "sessions")
            start = found + 1
        backend_next = (page or {}).get("next_cursor")
        fetched_end = self._list_cursor(mode, backend_next) if backend_next else None
        window = rows[start : start + page_size]
        for offset, row in enumerate(window, start=start):
            after = (
                fetched_end
                if offset + 1 == len(rows)
                else self._list_cursor(mode, position, self._get_session_identity(row), index=offset)
            )
            sent.append((self._build_session_row(row), after))
        return sent[-1][1] if sent else fetched_end
