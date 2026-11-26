"""decisions view: the choices that changed a project's, experiment's or run's work, each row naming what it
touched as `name (id:<uuid>)`; also the row `browse(mode="decisions")` lists."""

from __future__ import annotations
import hashlib
import json
import logging
from datetime import datetime
from typing import Any
from ....sdk import errors
from ...delivery.context import SNAPSHOT_SOURCE_LIMIT, current_delivery, source_changed
from ....shared.reads.search_contract import EntityType
from probe.mcp.tools.shaping.shaping import _fit
from probe.mcp.tools.view import _Req, _ViewData

#: What a team without decisions is told: one plain line, never an error a reader retries.
DECISIONS_OFF_NOTE = "Decisions are not on for this team: there are none to read."
#: Rows one route read asks for (the routes' own cap); a view call reads one route page.
_DECISIONS_PAGE = 500
#: The filters `view_options` passes to the route as given; the server reads the dates and the words.
_FILTER_NAMES = ("since", "until", "words")
#: The date filters a continuation pins to the bounds the first page resolved (`applied`).
_WINDOW_NAMES = ("since", "until")
#: The delivery snapshot `source` a first page's resolved window and next page ride in, for its fragment re-reads.
_WINDOW_SNAPSHOT = "decisions-window:"
_logger = logging.getLogger("probe.mcp.views.decisions")
#: A cursor from the view before #5463: an offset past the one route page this view reads.
_OLD_CURSOR_MESSAGE = ("cursor is from an older Probe and can no longer be continued: re-run this read without "
                       "a cursor")


def build_decision_row(row: dict[str, Any]) -> dict[str, Any]:
    """One decision as a reader quotes it: when, the choice, why, who, where it was filed and what it touched,
    each place, target and session `name (id:<uuid>)` (the form `probe` commands take; never a link, #5344)."""
    decided_by = row.get("decided_by") or {}
    out: dict[str, Any] = {
        "id": row.get("id"),
        "decided_at": row.get("decided_at"),
        "title": row.get("title"),
        "why": row.get("detail"),
    }
    if row.get("rejected"):
        out["instead_of"] = row["rejected"]
    out["by"] = decided_by.get("name") or decided_by.get("kind")
    for key, name_key, id_key in (("project", "project_name", "project_id"),
                                  ("experiment", "experiment_name", "experiment_id")):
        if row.get(id_key):
            out[key] = _get_name_with_id(row.get(name_key), row[id_key])
    targets = [
        f"{target.get('effect')}: {target.get('type')} {_get_name_with_id(target.get('name'), target.get('id'))}"
        for target in row.get("targets") or []
        if isinstance(target, dict)
    ]
    if targets:
        out["affects"] = targets
    session = row.get("session") or {}
    if session.get("id"):
        out["session"] = _get_name_with_id(session.get("title") or session.get("agent"), session["id"])
    if row.get("follows"):
        out["follows"] = row["follows"]
    return {key: value for key, value in out.items() if value is not None}


def _get_name_with_id(name: Any, ident: Any) -> str:
    return f"{name} (id:{ident})" if name else f"id:{ident}"


def read_view_filters(filters: dict[str, Any]) -> dict[str, str]:
    """`view_options` since / until / words as the route's filters, each a string, refused otherwise."""
    out: dict[str, str] = {}
    for name in _FILTER_NAMES:
        value = filters.get(name)
        if value is None or value == "":
            continue
        if isinstance(value, list) and name == "words" and all(isinstance(word, str) for word in value):
            value = " ".join(value)
        if not isinstance(value, str):
            raise errors.ValidationError(f"view_options.{name} must be a string", status=422)
        out[name] = value
    return out


def get_pinned_window(applied: dict[str, Any] | None) -> dict[str, str]:
    """The absolute `since` / `until` a first page resolved (`applied`), to send again on a re-read of it: a
    span like `7d` re-read later would move the window, and the server pins one only inside its cursor."""
    return {name: str(applied[name]) for name in _WINDOW_NAMES if applied and applied.get(name)}


def _make_page_position(cursor: str | None, window: dict[str, str]) -> str | None:
    """Where a decisions view page reads from: the route's cursor and the window pinned with it; None = the
    first page as asked."""
    if not cursor and not window:
        return None
    return json.dumps({"c": cursor, "w": window}, sort_keys=True)


def _is_window(value: Any) -> bool:
    return isinstance(value, dict) and all(
        name in _WINDOW_NAMES and isinstance(bound, str) for name, bound in value.items())


def _read_page_position(after: str | None) -> tuple[str | None, dict[str, str]]:
    """`_make_page_position`'s `(cursor, window)` back, refused when it is not one."""
    if not after:
        return None, {}
    try:
        position = json.loads(after)
        cursor, window = position["c"], position["w"]
        if (cursor is not None and not isinstance(cursor, str)) or not _is_window(window):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        raise errors.ValidationError(
            "malformed cursor: pass the next_cursor value from a previous research_get call", status=422) from None
    return cursor, window


def _get_first_page_snapshot() -> tuple[dict[str, str], str | None] | None:
    """`(window, next_page_after)` a first read saved in the delivery snapshot: a fragment re-read of that page
    sends the window's absolute dates and emits the saved next page, so its rows and cursors match the first
    read's byte for byte (#5463). None outside delivery or on a first read."""
    context = current_delivery()
    if context is None or context.snapshot is None:
        return None
    source = context.snapshot["source"]
    if not source.startswith(_WINDOW_SNAPSHOT):
        raise source_changed("document identity changed")
    try:
        saved = json.loads(source[len(_WINDOW_SNAPSHOT):])
        window, next_page_after = saved["w"], saved["n"]
        if not window or not _is_window(window) or (next_page_after is not None
                                                    and not isinstance(next_page_after, str)):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        raise source_changed("document identity changed") from None
    return window, next_page_after


def _drop_first_page_snapshot() -> None:
    """A read past the first page carries its window in `after` and never reads the first page's snapshot. Kept,
    it cost every later cursor ~600 chars, enough that one fragment's cursor alone overflowed a 512-token budget
    now and then, and a walk took 4x the calls (review of #5471)."""
    context = current_delivery()
    if context is not None and context.snapshot is not None and context.snapshot["source"].startswith(
            _WINDOW_SNAPSHOT):
        context.snapshot = None


def _is_absolute_window(filters: dict[str, str]) -> bool:
    """Every date sent is an ISO date or time: a re-read sending the same text reads the same rows and gets the
    same route cursor, so it needs no snapshot. Anything else (`7d`) may be a span the server resolves from now."""
    try:
        for name in _WINDOW_NAMES:
            if name in filters:
                datetime.fromisoformat(filters[name].strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _save_first_page_snapshot(window: dict[str, str], next_page_after: str | None) -> None:
    """Save a first read's resolved window and next page in the delivery snapshot (`_get_first_page_snapshot`)."""
    context = current_delivery()
    if context is None or not window:
        return
    source = _WINDOW_SNAPSHOT + json.dumps({"w": window, "n": next_page_after}, sort_keys=True)
    if len(source) > SNAPSHOT_SOURCE_LIMIT:
        # Unsaved, a fragment re-read resolves the dates again and may be refused `source_changed`.
        _logger.warning("decisions first page too long to pin for fragments: %d chars", len(source))
        return
    context.snapshot = {"source": source, "end": 0, "sha256": hashlib.sha256(source.encode()).hexdigest()}


class DecisionsViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def _build_project_decisions_view(self, entity: dict, request: _Req) -> _ViewData:
        """A project's decisions and its experiments', oldest first (an experiment-kind row: its own)."""
        return self._list_decisions(request, scope_id=str(entity["id"]),
                                    should_include_experiments=entity.get("kind") != "experiment")

    def _build_experiment_decisions_view(self, entity: dict, request: _Req) -> _ViewData:
        """Decisions filed under the experiment or naming it (a project's "start E" among them)."""
        return self._list_decisions(request, about=f"{EntityType.EXPERIMENT.value}:{entity['id']}")

    def _build_run_decisions_view(self, entity: dict, request: _Req) -> _ViewData:
        """Decisions naming the run (stopped it, changed it, based on it)."""
        return self._list_decisions(request, about=f"{EntityType.RUN.value}:{entity['id']}")

    def _list_decisions(self, request: _Req, **scope: Any) -> _ViewData:
        """One route page, oldest first, walked by offset; the next page from the route's cursor (`more_beyond`:
        narrow with `since` / `until` / `words`). A re-read of a first page sends the window it resolved. A team
        without decisions answers one plain line, not an error."""
        from ....sdk.client import is_decisions_off

        filters = read_view_filters(request.filters or {})
        scope_id = scope.pop("scope_id", None)
        cursor, window = _read_page_position(request.after)
        if cursor is None and request.offset >= _DECISIONS_PAGE:
            # Offset-only into the old view's 1,000 rows: past this view's first route page, it cannot be placed.
            raise errors.ValidationError(_OLD_CURSOR_MESSAGE, status=422)
        if request.after:
            _drop_first_page_snapshot()
        saved = None if request.after else _get_first_page_snapshot()
        if saved:
            window = saved[0]
        if window:
            filters = {**{name: value for name, value in filters.items() if name not in _WINDOW_NAMES}, **window}
        try:
            page = self.source.fetch_decisions(scope_id, cursor=cursor, limit=_DECISIONS_PAGE, **scope, **filters)
        except errors.RosError as exc:
            if not is_decisions_off(exc):
                raise
            return _ViewData(payload={"note": DECISIONS_OFF_NOTE}, rows=[], rows_key="decisions")
        rows = [build_decision_row(row) for row in page.decisions if isinstance(row, dict)]
        # The server's cursors are bound to the dates as sent: every page after this one sends this page's.
        next_page_after = _make_page_position(page.next_cursor, window) if page.next_cursor else None
        if saved:
            next_page_after = saved[1]  # minted under the dates the first read sent, as its next page needs
        elif not request.after and not _is_absolute_window(filters):
            # The next page is only sent when every row from here is: else saving it costs every fragment's
            # cursor ~240 chars it never uses, enough to stop one fitting a small budget (Devin on #5468).
            window_rows = rows[request.offset:]
            is_whole = len(_fit(window_rows, request.token_budget)) == len(window_rows)
            _save_first_page_snapshot(get_pinned_window(page.applied), next_page_after if is_whole else None)
        return _ViewData(
            rows=rows, rows_key="decisions", more_beyond=bool(page.next_cursor),
            no_match=not rows and bool(filters),
            page_after=request.after or _make_page_position(None, window or get_pinned_window(page.applied)),
            next_page_after=next_page_after,
        )
