"""Overview and summary views: the saved page, the authored Markdown and its version history."""

from __future__ import annotations
from typing import Any
from ....sdk import errors
from ....shared.reads.search_contract import EntityType
from probe.mcp.tools.shaping.cards import _notes_excerpt
from probe.mcp.tools.view import _Req, _ViewData

#: One page of a summary's version history (GET …/summary/versions): the
#: route's own cap, and the page this view walks one at a time.
_SUMMARY_VERSIONS_PAGE = 50

#: A summary_history row: who wrote the version, when, through what, and how
#: big it is -- never the text, which is one `view_options.version` read away.
_SUMMARY_HISTORY_ROW_FIELDS = (
    "version",
    "created_at",
    "created_by",
    "source",
    "via",
    "mode",
    "session_title",
    "size_chars",
)

#: One summary version (GET …/summary/versions/{v}), `markdown` last.
_SUMMARY_VERSION_FIELDS = (
    "version",
    "created_at",
    "created_by",
    "source",
    "via",
    "mode",
    "markdown",
)


def _experiment_project_id(entity: dict) -> str | None:
    """The project an experiment card says it is filed under, under either
    spelling the two reads use; None lets the SDK locate it."""
    found = entity.get("project_id") or entity.get("parent_project_id")
    return str(found) if found else None


#: The page counter's column type (`entity_overviews.version`, int4): a number
#: past it binds nowhere, so it is refused here rather than as a server 500.
_INT4_MAX = 2_147_483_647


def _summary_version_number(value: Any) -> int | None:
    """A summary version as the routes take it -- a whole number, 0 or more,
    within int4 -- from a `view_options.version` or a cursor's `after`; None for
    anything else. `str.isdecimal`, not `isdigit`: "²" is a digit that `int()`
    refuses, and a bool is an int that is not a version."""
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        if not value.isdecimal():
            return None
        value = int(value)
    if not isinstance(value, int) or not 0 <= value <= _INT4_MAX:
        return None
    return value


class OverviewViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    @staticmethod
    def _saved_overview(page: dict) -> _ViewData:
        """Saved page only: live job/ETA/freshness must not invalidate cursors.

        Worker basis is mutable even when the page/version is unchanged and is
        deliberately excluded. Full HTML includes generated and authored edits. A null
        HTML value honestly reports that no saved page is available. Generic
        MCP continuation delivers oversized pages without dropping their tail.
        """
        fields = (
            "anchor_type",
            "anchor_id",
            "html",
            "plan",
            "blurb",
            "series",
            "source",
            "model",
            "prompt_version",
            "generated_at",
            "version",
        )
        saved = {key: page.get(key) for key in fields}
        if page.get("content") == "absent" and page.get("saved_page_readable") is not True:
            # Older API pods marked restricted family pages absent while still
            # returning their bytes. An explicit permission-checked verdict
            # distinguishes authored-only pages from those old responses.
            saved = {key: None for key in fields}
            saved.update(anchor_type=page.get("anchor_type"), anchor_id=page.get("anchor_id"), version=0)
        return _ViewData(payload={"overview": saved})

    def _view_project_overview(self, entity: dict, request: _Req) -> _ViewData:
        view = self._saved_overview(self.source.project_overview(str(entity["id"])))
        return self._with_summary_markdown(view, EntityType.PROJECT, entity)

    def _view_experiment_overview(self, entity: dict, request: _Req) -> _ViewData:
        view = self._saved_overview(
            self.source.experiment_overview(
                str(entity["id"]),
                project_id=_experiment_project_id(entity),
            )
        )
        return self._with_summary_markdown(view, EntityType.EXPERIMENT, entity)

    def _with_summary_markdown(self, view: _ViewData, kind: str, entity: dict) -> _ViewData:
        """`overview.markdown`: the page as the recorders read and write it
        (GET …/summary), beside the `html` the dashboard renders. `""` is a
        page with no summary. On a server predating the summary route the read
        is a 404, and the key is left OUT rather than set to null: absent says
        "this server cannot say", null would say "there is none"."""
        try:
            summary = self.source.summary(
                kind, str(entity["id"]), project_id=_experiment_project_id(entity)
            )
        except errors.NotFoundError:
            return view
        markdown = summary.get("markdown") if isinstance(summary, dict) else None
        if isinstance(markdown, str):
            view.payload["overview"]["markdown"] = markdown
        return view

    def _view_project_summary_history(self, entity: dict, request: _Req) -> _ViewData:
        return self._summary_history(EntityType.PROJECT, entity, request)

    def _view_experiment_summary_history(self, entity: dict, request: _Req) -> _ViewData:
        return self._summary_history(EntityType.EXPERIMENT, entity, request)

    def _summary_history(self, kind: str, entity: dict, request: _Req) -> _ViewData:
        """The summary's versions, newest first, one route page per call and the
        walk past it on the route's own `before` (`resume_key="version"`); or,
        with `view_options.version`, ONE version with its markdown -- atomic,
        so delivery fragments a long one rather than cutting it."""
        entity_id = str(entity["id"])
        project_id = _experiment_project_id(entity) if kind == EntityType.EXPERIMENT else None
        version = request.filters.get("version")
        if version is not None:
            # 0 is a recorded version: pages written before the counter existed
            # sit there (`app/overviews/history.py`), and the list shows them.
            wanted = _summary_version_number(version)
            if wanted is None:
                raise errors.ValidationError(
                    "view_options.version must be a whole number, 0 or more: a `version` "
                    "from this view's rows",
                    status=422,
                )
            try:
                row = self.source.summary_version(kind, entity_id, wanted, project_id=project_id)
            except errors.NotFoundError as exc:
                # The entity resolved a moment ago, so this is the version or the
                # route, never the entity -- say which the reader should doubt.
                raise errors.NotFoundError(
                    f"no version {wanted} of this {kind}'s summary ({exc}): a `version` "
                    "from this view's rows, on a server with the summary routes"
                ) from exc
            shaped = {key: row.get(key) for key in _SUMMARY_VERSION_FIELDS if isinstance(row, dict)}
            return _ViewData(payload={"summary_version": shaped, "filters": request.filters})
        before: int | None = None
        if request.after is not None:
            # The cursor carries the last version SENT (`resume_key`); anything
            # else is not a cursor of this view, and serving the first page again
            # would walk forever rather than say so.
            before = _summary_version_number(request.after)
            if before is None:
                raise errors.ValidationError(
                    "malformed cursor: pass the next_cursor value from a previous "
                    "research_get call",
                    status=422,
                )
        try:
            page = self.source.summary_versions(
                kind, entity_id, project_id=project_id, before=before, limit=_SUMMARY_VERSIONS_PAGE
            )
        except errors.NotFoundError as exc:
            raise errors.NotFoundError(
                f"no summary history for this {kind} ({exc}): the server predates the "
                "summary routes, or the page is withheld from this reader"
            ) from exc
        versions = [v for v in (page.get("versions") or []) if isinstance(v, dict)]
        rows = [
            {key: v[key] for key in _SUMMARY_HISTORY_ROW_FIELDS if v.get(key) is not None}
            for v in versions
        ]
        return _ViewData(
            rows=rows,
            rows_key="versions",
            more_beyond=page.get("next_before") is not None and bool(rows),
            resume_key="version",
        )

    def _view_project_summary(self, entity: dict, request: _Req) -> _ViewData:
        """Compatibility-shaped project read for authored Overview Markdown."""
        return self._view_entity_summary(EntityType.PROJECT, entity)

    def _view_experiment_summary(self, entity: dict, request: _Req) -> _ViewData:
        """The experiment's authored, dashboard-visible Markdown document.

        The experiment detail carries it (`document`, a block of the Overview
        page; server X21); a row read from a list does not, and this view
        then reads it on its own -- one request, only when asked for."""
        if "document" not in entity:
            entity = {
                **entity,
                "document": self.source.experiment_document(
                    str(entity["id"]), project_id=entity.get("project_id")
                ),
            }
        return self._view_entity_summary(EntityType.EXPERIMENT, entity)

    @staticmethod
    def _view_entity_summary(kind: str, entity: dict) -> _ViewData:
        """Return visible authored Markdown without conflating it with Notes.

        ``project_summary`` remains the project payload key for compatibility;
        the experiment and run variants use their own nouns. The semantics are
        identical: one complete visible document, distinct from the entity's
        private operational Notes. It lives INSIDE the Overview page, as a
        block the page's AI writer may not rewrite, so what comes back is the
        page's rendering of it rather than the bytes anyone sent.

        0220: PROJECT AND EXPERIMENT ONLY. A run was never on the page lane, so
        when the column went there was nothing left for its `summary` view to
        read and the view went with it -- rather than answering "" for ever.
        """
        noun = str(kind)
        payload = {f"{noun}_summary": {"document": entity.get("document") or ""}}
        caveat = _notes_excerpt(entity.get("notes"))
        if caveat is not None:
            payload["notes"] = caveat
        return _ViewData(payload=payload)
