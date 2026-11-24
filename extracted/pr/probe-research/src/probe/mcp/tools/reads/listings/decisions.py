"""browse mode=decisions: the team's decisions, oldest first, narrowed by date (`since` / `until`) and words."""

from __future__ import annotations

from .....sdk import errors
from probe.mcp.source.people import PeopleFilters
from probe.mcp.tools.shaping.cursors import _unpack_cursor
from probe.mcp.tools.views.decisions import DECISIONS_OFF_NOTE, build_decision_row, get_pinned_window


class DecisionRowsMixin:
    """Part of BrowseListMixin: fold_parts() copies its methods in, and they run with `self` the ResearchReadService."""

    def _list_decisions_page(
        self, *, backend_cursor, cursor, data, last_sent, mode, page_size, people: PeopleFilters, query, sent,
    ) -> str | None:
        """mode=decisions: one page after the last row sent; the cursor after the page. The route's keyset
        cursor is opaque here, so a cut inside a page re-reads that page from the same position and resumes
        after the decision sent last (refused, never guessed, if it is gone). A re-read of a first page sends
        the dates it resolved (`applied`), and every later read the same, since the route binds its cursors
        to the dates as sent. A team without decisions answers one plain `note`, not an error."""
        from .....sdk.client import is_decisions_off

        pinned = _read_pinned_window(cursor)
        since, until = (pinned.get("since"), pinned.get("until")) if pinned else (people.since, people.until)
        try:
            page = self.source.fetch_decisions(
                None, since=since, until=until, words=query or None, cursor=backend_cursor, limit=page_size,
            )
        except errors.RosError as exc:
            if not is_decisions_off(exc):
                raise
            data["note"] = DECISIONS_OFF_NOTE
            return None
        if page.applied:
            data["applied"] = page.applied
        rows = [row for row in page.decisions if isinstance(row, dict) and row.get("id")]
        start = 0
        if last_sent is not None:
            found = next((i for i, row in enumerate(rows) if str(row["id"]) == last_sent), None)
            if found is None:
                raise self._gone("decision")
            start = found + 1
        # Re-reading this page: a first page asked as given pins the window it resolved.
        reread_window = pinned if pinned or backend_cursor else get_pinned_window(page.applied)
        fetched_end = self._list_cursor(mode, page.next_cursor, window=pinned) if page.next_cursor else None
        window = rows[start : start + page_size]
        for offset, row in enumerate(window, start=start):
            after = (fetched_end if offset + 1 == len(rows)
                     else self._list_cursor(mode, backend_cursor, str(row["id"]), window=reread_window))
            sent.append((build_decision_row(row), after))
        return sent[-1][1] if sent else fetched_end


def _read_pinned_window(cursor: str | None) -> dict[str, str]:
    """The absolute `since` / `until` a decisions continuation sends in place of the ones asked; {} for none."""
    window = _unpack_cursor(cursor, hint="browse").get("w") if cursor else None
    if window is None:
        return {}
    if not isinstance(window, dict) or not all(
            name in ("since", "until") and isinstance(value, str) for name, value in window.items()):
        raise errors.ValidationError(
            "this cursor does not continue browse(mode='decisions'): pass the next_cursor value from a previous "
            "call with the same arguments", status=422)
    return window
