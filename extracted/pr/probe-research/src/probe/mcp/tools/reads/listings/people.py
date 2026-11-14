"""browse mode=people: the team's members with the user ids `owner` takes, one page of the roster (or of the ones `query` names)."""

from __future__ import annotations
import json

from .....sdk import errors
from probe.mcp.tools.shaping.people import to_person_card


class PeopleRowsMixin:
    """Part of BrowseListMixin: fold_parts() copies its methods in, and they run with `self` the ResearchReadService."""

    @staticmethod
    def _get_person_key(row: dict) -> tuple[str, str]:
        """This listing's own order, name then id: the roster route does not page, so every call reads the
        whole list and resumes past the last key sent (a teammate who joins mid-walk is never skipped)."""
        name = str(row.get("name") or row.get("email") or "").casefold()
        return name, str(row.get("user_id") or "").lower()

    @staticmethod
    def _build_person_row(row: dict) -> dict:
        out = to_person_card(row) or {}
        out.update({key: row[key] for key in ("role", "joined_at") if row.get(key) is not None})
        return out

    def _list_people_page(
        self, *, last_sent: str | None, mode, page_size: int, sent: list, query: str | None = None
    ) -> str | None:
        """mode=people: `page_size` rows of the roster after `last_sent`; the cursor after the page. With
        `query`, the server's rows in its order (best match first), resumed after the last row sent."""
        query = (query or "").strip() or None  # blank lists everyone, as the server reads it
        rows = [row for row in self.source.fetch_people(query) if row.get("user_id")]
        if not query:
            rows.sort(key=self._get_person_key)
        start = 0
        if last_sent is not None:
            try:
                name, ident = json.loads(last_sent)
                resume = (str(name), str(ident))
            except (ValueError, TypeError):
                raise errors.ValidationError(
                    "malformed browse cursor: pass the next_cursor value from a previous call with "
                    "the same arguments",
                    status=422,
                ) from None
            keys = [self._get_person_key(row) for row in rows]
            if query:
                # Ranked, not sorted: resume after that row, or refuse when it is gone (never guess).
                if resume not in keys:
                    raise self._gone("teammate")
                start = keys.index(resume) + 1
            else:
                start = next((i for i, key in enumerate(keys) if key > resume), len(rows))
        window = rows[start : start + page_size]
        for offset, row in enumerate(window, start=start):
            after = (
                self._list_cursor(mode, last=json.dumps(list(self._get_person_key(row))))
                if offset + 1 < len(rows)
                else None
            )
            sent.append((self._build_person_row(row), after))
        return sent[-1][1] if sent else None
