"""document reads: the notes catalog, Overview pages, authored summaries and their versions, pinned notes."""

from __future__ import annotations
import base64

from ...sdk import errors
from ...shared.reads.search_contract import EntityType, NoteCatalogKind
from ..delivery.context import current_delivery, document_hint, pin_document, source_changed
from probe.mcp.source.people import PeopleFilters

#: `kind_rank` per notes-catalog kind, exactly as the catalog's SQL arms number
#: them (app/notes_catalog/service.py): the tiebreak inside one `created_at`,
#: and the middle third of its cursor. The team note has none -- it is never in
#: a keyset page. Groups (2) and artifacts (1) no longer carry notes; a row of
#: either from an older server has no rank, and the caller finds it instead.
_NOTE_KIND_RANK: dict[str, int] = {
    NoteCatalogKind.PROJECT: 6,
    NoteCatalogKind.EXPERIMENT: 5,
    NoteCatalogKind.RUN: 4,
    NoteCatalogKind.SUB_NOTE: 3,
}


class DocumentReadsMixin:
    """Part of ResearchOSSource: its methods run with `self` the ResearchOSSource; compose() folds them into ResearchOSSource."""

    @staticmethod
    def note_cursor_after(row: dict) -> str | None:
        """The `GET /v1/notes` cursor that resumes AFTER `row`: the catalog's
        own keyset, base64 of `<created_at>|<kind_rank>|<id>`
        (app/notes_catalog/service.py `encode_cursor`), read by the server as
        `(created_at, kind_rank, id) < (that row's)`.

        Built from the row for the reason `run_cursor_after` is: a mid-page cut
        must resume after the last row SENT. Finding that row again in a
        re-read page failed whenever newer notes had pushed it off the page.

        None for the team note (a first-page singleton with no keyset) and for
        a kind with no rank here -- the caller falls back to finding the row."""
        rank = _NOTE_KIND_RANK.get(row.get("kind"))
        created_at, row_id = row.get("created_at"), row.get("id")
        if rank is None or not isinstance(created_at, str) or not created_at or not row_id:
            return None
        if created_at.endswith("Z"):
            created_at = created_at[:-1] + "+00:00"
        return base64.urlsafe_b64encode(f"{created_at}|{rank}|{row_id}".encode()).decode()

    def notes_catalog(
        self,
        *,
        query: str | None = None,
        cursor: str | None = None,
        limit: int,
        filters: PeopleFilters = PeopleFilters(),
    ) -> dict:
        """``GET /v1/notes``, the tenant-wide catalog: `{items, next_cursor}`.

        Always with a `limit` (a bare call answers the dashboard's lazy ROOT
        tree, see `Client.list_notes`) and with sub-notes included: they are
        openable here now (`sub_note:<id>`), so hiding them would hide the one
        row a search was most likely looking for."""
        return self.client.list_notes(
            query=query, cursor=cursor, limit=limit, include_sub_notes=True, **filters.to_query()
        )

    def project_overview(self, project_id: str) -> dict:
        return self.client.get_project_overview(project_id)

    def experiment_overview(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        return self.client.get_experiment_overview(experiment_id, project_id=project_id)

    def experiment_document(
        self, experiment_id: str, *, project_id: str | None = None
    ) -> str | None:
        """The experiment's authored Markdown, as its Overview page holds it:
        the experiment detail's ``document`` (server X21)."""
        return self.client.get_experiment_document(experiment_id, project_id=project_id)

    # -- the recorder-written summary ------------------------------------------
    #
    # `kind` is `project` or `experiment`; an experiment is located by its id
    # and, when the card carried it, its project (the SDK locates it otherwise).

    @staticmethod
    def _summary_anchor(kind: str, entity_id: str, project_id: str | None) -> dict[str, str]:
        if kind == EntityType.EXPERIMENT:
            anchor = {"experiment": entity_id}
            if project_id:
                anchor["project"] = project_id
            return anchor
        return {"project": entity_id}

    def summary(self, kind: str, entity_id: str, *, project_id: str | None = None) -> dict:
        """``GET …/summary``: `{markdown, version, edited_at, edited_by, via,
        session_title, you, today, mode}`. A 404 is the SDK's `NotFoundError`: detail
        "summary not found" is a page withheld from the caller (0223); any other is an
        address that did not resolve (or, on a server predating the route, no route)."""
        return self.client.get_summary(**self._summary_anchor(kind, entity_id, project_id))

    def summary_versions(
        self,
        kind: str,
        entity_id: str,
        *,
        project_id: str | None = None,
        before: int | None = None,
        limit: int,
    ) -> dict:
        """``GET …/summary/versions``: `{versions, next_before}`, newest first."""
        return self.client.list_summary_versions(
            **self._summary_anchor(kind, entity_id, project_id), before=before, limit=limit
        )

    def summary_version(
        self, kind: str, entity_id: str, version: int, *, project_id: str | None = None
    ) -> dict:
        """``GET …/summary/versions/{v}``: one version, `markdown` included."""
        return self.client.get_summary_version(
            version, **self._summary_anchor(kind, entity_id, project_id)
        )

    # -- versioned note documents ---------------------------------------------

    def notes_document(self, kind: str, entity: dict) -> tuple[str | None, int | None]:
        """Pin an explicit notes read, using an already-known saved version.

        Detail schemas that omit ``notes_version`` use the original-prefix
        fallback. Do not list history to decorate ordinary cards or discover a
        version: the body already fetched is enough for honest consistency.
        A resumed known version is read directly under the same API auth/RLS.
        """
        body, version = entity.get("notes"), entity.get("notes_version")
        if current_delivery() is None:
            return body, version
        source = f"notes:{kind}:{entity['id']}"
        hint = document_hint(source)
        if hint and "version" in hint:
            version = hint["version"]
            entity_id = entity["id"]
            try:
                if kind == "project":
                    saved = self.client.transport.get(f"/v1/projects/{entity_id}/notes/versions/{version}")
                elif kind == "experiment":
                    # The experiment API's note history (server X21), under the
                    # project the experiment is filed in -- which its row names.
                    project_id = entity.get("project_id") or entity.get("parent_project_id")
                    if not project_id:
                        project_id = self.client.get_scope(str(entity_id))["project_id"]
                    saved = self.client.transport.get(
                        f"/v1/projects/{project_id}/experiments/{entity_id}"
                        f"/notes/versions/{version}"
                    )
                elif kind == "run":
                    saved = self.client.transport.get(f"/v1/runs/{entity_id}/notes/versions/{version}")
                else:
                    raise errors.ValidationError("Unsupported notes document kind", status=422)
            except errors.NotFoundError as exc:
                raise source_changed("saved notes version is unavailable") from exc
            body = saved.get("body")
            if saved.get("version") != version or not isinstance(body, str):
                raise source_changed("saved notes version is unavailable")
        pinned = pin_document(body or "", source, version=version)
        return (None if body is None and not pinned else pinned), version
