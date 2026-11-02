"""ExperimentAdminMixin, Client's methods: list, update, move and delete experiments, their edges,
and the run groups inside them (twins: app/projects/experiments, app/runs/groups)."""

from __future__ import annotations
import warnings
from typing import Any
from .....models import (
    RunGroupCreate,
    RunGroupPatch)
from ....delivery.transport.transport import Page
_EXPERIMENT_PAGE_DEFAULT = 100


class ExperimentAdminMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def update_experiment(
        self,
        experiment_id: str,
        *,
        question: str | None = None,
        conclusion: str | None = None,
        name: str | None = None,
        description: str | None = None,
        document: str | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        summary: dict | None = None,
        authored_by: str | None = None,
        project_id: str | None = None,
        dead_end: str | None = None,
        clear_dead_end: bool = False,
    ) -> dict:
        """Amend an experiment's question, conclusion, name or visible Markdown,
        or mark it a dead end.

        ``question``, ``conclusion`` and ``name`` go to
        ``PATCH /v1/projects/{P}/experiments/{E}``. ``conclusion`` is the
        experiment's answer; ``""`` clears it. The server answers 409 when an
        agent's write would replace a person's conclusion.

        ``dead_end`` marks the experiment a dead end and says why (the server's
        ``outcome: dead_end`` with ``outcome_reason``); ``clear_dead_end`` clears
        the mark. Its branch then reads ``dead_end`` until a run of it is live;
        it still ranks. An agent's mark never replaces a person's (409).

        ``document`` replaces the authored Markdown that lives INSIDE the
        experiment's Overview page, as a block the page's AI writer may not
        rewrite. It is whole-document and last-write-wins, separate from the
        experiment's private Notes. Read immediately before editing and preserve
        useful sections; ``""`` clears it. A line containing only
        ``[README](https://github.com/owner/repo)`` embeds that README and derives
        the experiment's read-only ``repo`` field. It travels in the SAME PATCH
        as the question and name, so the edit lands whole or not at all.

        DO NOT expect a read-back to be byte-identical: a detail GET answers
        from the page, which renders the document -- see :meth:`update_project`.

        ``tags``, ``metadata`` and ``summary`` are refused: the server keeps an
        experiment's tags and metadata read-only since it moved to its own
        record. ``description`` is refused too: the question replaced it."""
        if description is not None:
            raise ValueError(_EXPERIMENT_DESCRIPTION_RETIRED)
        _refuse_read_only_experiment_fields(tags=tags, metadata=metadata, summary=summary)
        if dead_end is not None and clear_dead_end:
            raise ValueError("dead_end marks the experiment and clear_dead_end clears it: pass one")
        if dead_end is not None and not dead_end.strip():
            raise ValueError("dead_end takes the reason: say why the experiment is a dead end")
        identity = {
            key: value
            for key, value in {
                "question": question,
                "conclusion": conclusion,
                "name": name,
            }.items()
            if value is not None
        }
        if not identity and document is None and dead_end is None and not clear_dead_end:
            raise ValueError("update_experiment needs at least one field to set")
        project, experiment = self._experiment_ids(experiment_id, project_id)
        body: dict[str, Any] = dict(identity)
        if document is not None:
            body["document"] = document
        if dead_end is not None:
            body["outcome"], body["outcome_reason"] = "dead_end", dead_end
        elif clear_dead_end:
            body["outcome"] = None
        # AFTER the emptiness check, deliberately. `authored_by` declares who
        # wrote the OTHER fields; on its own it declares authorship of nothing.
        _put_authorship(body, authored_by)
        written = self.transport.patch(f"/v1/projects/{project}/experiments/{experiment}", body)
        if document is not None:
            self._verify_entity_markdown_written(
                "experiment", document, written, "PATCH /v1/projects/{P}/experiments/{E}"
            )
        row = _from_experiment_api(written)
        if document is None and isinstance(row, dict):
            # The write answers `document` only when it wrote one.
            row.pop("document", None)
        return row

    def move_experiment(
        self, experiment_id: str, project_id: str, *, from_project_id: str | None = None
    ) -> dict:
        """Move an experiment, with its runs, files and groups, to another project.

        ``PATCH /v1/projects/{from}/experiments/{E}`` with ``{project_id}``: one
        statement on the server. Needs edit access on both projects (403); a
        target that is an experiment is 422, one in the trash 410, a project
        being purged 409, and a move under a restricted project revokes the
        experiment's public share. Answers the experiment filed under its new
        project. ``project_id`` is the TARGET's uuid; ``from_project_id`` saves
        the lookup of where it is now."""
        if not project_id:
            raise ValueError("move_experiment needs the target project's id")
        project, experiment = self._experiment_ids(experiment_id, from_project_id)
        return _from_experiment_api(
            self.transport.patch(
                f"/v1/projects/{project}/experiments/{experiment}",
                {"project_id": str(project_id)},
            )
        )

    def list_experiments(
        self,
        *,
        project_id: str | None = None,
        tags: list[str] | None = None,
        name: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        **params,
    ) -> Page:
        """A project's experiments, newest first; with no ``project_id``, every
        project's.

        ``GET /v1/projects/{project_id}/experiments``, offset paged (at most 500
        per page): pass a page's ``next_cursor`` back as cursor= for the next one,
        an opaque token. Without a
        project, the caller's projects are walked (:meth:`_tenant_experiments`):
        one request per project, sorted newest first, then paged here.

        ``name`` keeps rows whose name matches exactly (case-insensitive).
        ``tags`` is refused: an experiment's tags are read-only since it moved to
        its own record, and the experiment API filters on none."""
        if tags:
            _refuse_read_only_experiment_fields(tags=tags)
        if params:
            raise ValueError(
                f"list_experiments takes project_id, name, limit and cursor; "
                f"{', '.join(sorted(params))} is not a filter of the experiment list"
            )
        offset = _offset_cursor(cursor)
        if project_id is not None:
            query: dict[str, Any] = {"offset": offset}
            if limit is not None:
                query["limit"] = limit
            page = self.transport.get(f"/v1/projects/{project_id}/experiments", params=query)
            items = [_from_experiment_api(item) for item in page.get("items") or []]
            if name is not None:
                items = [row for row in items if _same_name(row, name)]
            next_offset = page.get("next_offset")
            return Page(items=items, next_cursor=None if next_offset is None else str(next_offset))
        rows = self._tenant_experiments()
        if name is not None:
            rows = [row for row in rows if _same_name(row, name)]
        rows.sort(key=lambda row: (str(row.get("created_at") or ""), str(row["id"])), reverse=True)
        size = limit if limit is not None else _EXPERIMENT_PAGE_DEFAULT
        window = rows[offset : offset + size]
        more = offset + size < len(rows)
        return Page(items=window, next_cursor=str(offset + size) if more else None)

    def delete_experiment(
        self,
        experiment_id: str,
        *,
        project_id: str | None = None,
        dry_run: bool = False,
        reason: str | None = None,
    ) -> dict | None:
        """Move an experiment, its runs, groups, files, notes and page to the
        server's TRASH. Frees the slug.

        ``DELETE /v1/projects/{P}/experiments/{E}``. Probe support can restore it
        for 21 days (the returned receipt says until when); after that it is
        deleted for good. ``dry_run=True`` changes nothing and answers what would
        go and whose it is. 409 if a published experiment version outside this
        experiment pins something under it, or a live W&B mirror is bound to it."""
        project, experiment = self._experiment_ids(experiment_id, project_id)
        params: dict[str, str] = {}
        if dry_run:
            self._require_dry_run_delete()
            params["dry_run"] = "true"
        if reason:
            params["reason"] = reason
        if not params:
            return self.transport.delete(f"/v1/projects/{project}/experiments/{experiment}")
        resp = self.transport.request(
            "DELETE",
            f"/v1/projects/{project}/experiments/{experiment}",
            params=params,
            idempotent=True,
        )
        return resp.json() if resp.content else None

    def experiment_edges(
        self, experiment_id: str, *, limit: int | None = None, project_id: str | None = None
    ) -> list[dict]:
        """Every lineage edge under an experiment (the run-level view is
        :meth:`run_edges`); at most ``limit`` (1-1000) when given, stored edges
        first. The experiment's OWN links are :meth:`experiment_lineage`.

        ``GET /v1/projects/{P}/experiments/{E}/edges``; ``project_id`` saves the
        lookup of where the experiment is filed."""
        params = {"limit": limit} if limit is not None else None
        return self._on_experiment(
            lambda p, e: self.transport.get(
                f"/v1/projects/{p}/experiments/{e}/edges", params=params
            ),
            experiment_id,
            project_id,
        )

    # -- run groups (sweeps / ensembles) ------------------------------------
    @staticmethod
    def _warn_if_notes_dropped(sent: str | None, row: dict, what: str) -> None:
        """Surface the silent drop when the backend predates research-os 0096.

        Neither RunPatch nor RunCreate forbids extra fields, so an
        older backend ACCEPTS `notes`, ignores it, and answers 2xx -- the caveat
        vanishes and the caller is told it succeeded. This is the 0094 hazard, and
        the check is free: create and PATCH both return the row, so nothing extra
        is fetched.

        WARN rather than raise, unlike `set_project_notes`. That call's only effect
        is the notes write, so failing it loses nothing. These calls have already
        created or mutated the entity by the time the response is in hand -- raising
        would leave a run created on the server and an exception in the caller's
        lap, which is worse than a dropped note.
        """
        if sent is None or "notes" in row:
            return
        warnings.warn(
            f"this research-os backend predates `notes` on {what} (0096): it "
            "accepted the field, ignored it, and answered 2xx, so the note was "
            "NOT stored. Upgrade the backend to >= 0.107.0.0.",
            stacklevel=3,
        )

    def create_group(
        self,
        experiment_id: str,
        name: str,
        *,
        kind: str = "group",
        spec: dict | None = None,
        notes: str | None = None,
        project_id: str | None = None,
    ) -> dict:
        """Create a run group under an experiment — coordination metadata for a
        sweep or ensemble; ``spec`` holds e.g. the search space.

        Pass the returned ``id`` to :meth:`create_run` as ``group_id`` to file a run
        under it. 409 if the name is taken within the experiment.

        ``notes`` is accepted and ignored with a DeprecationWarning: sweep groups
        no longer carry notes, so what a sweep tested goes in the experiment's
        notes. Never put it in ``name`` either: the name is part of the group's
        uniqueness key within the experiment, so a description appended to it
        mints a second group instead of colliding with the one it describes."""
        from ....reads.notes_cap import GROUP_NOTES_REMOVED, warn_notes_ignored

        warn_notes_ignored(notes, GROUP_NOTES_REMOVED)
        model = RunGroupCreate(name=name, kind=kind, spec=spec or {})
        body = {
            key: value
            for key, value in model.model_dump(mode="json", exclude_none=True).items()
            if key != "notes"
        }
        return self._on_experiment(
            lambda p, e: self.transport.post(f"/v1/projects/{p}/experiments/{e}/groups", body),
            experiment_id,
            project_id,
        )

    def list_groups(self, experiment_id: str, *, project_id: str | None = None) -> list[dict]:
        """The experiment's run groups, newest first
        (``GET /v1/projects/{P}/experiments/{E}/groups``)."""
        return self._on_experiment(
            lambda p, e: self.transport.get(f"/v1/projects/{p}/experiments/{e}/groups"),
            experiment_id,
            project_id,
        )

    def get_group(self, group_id: str) -> dict:
        return self.transport.get(f"/v1/groups/{group_id}")

    def update_group(
        self,
        group_id: str,
        *,
        name: str | None = None,
        spec: dict | None = None,
        notes: str | None = None,
    ) -> dict:
        """Field-replace PATCH: only the fields you pass change.

        ``notes`` is accepted and ignored with a DeprecationWarning, never sent:
        sweep groups no longer carry notes (the server refuses a notes write
        here), so what a sweep tested goes in the experiment's notes. A call
        with ``notes`` alone writes nothing and returns the group as it is."""
        from ....reads.notes_cap import GROUP_NOTES_REMOVED, warn_notes_ignored

        warn_notes_ignored(notes, GROUP_NOTES_REMOVED)
        # THE GUARD READS THE CALLER'S ARGUMENTS, not the dumped model. The
        # generated model tracks the backend's, and a default it adds (`force`
        # was one) survives `exclude_none`, so the body is never empty and an
        # argumentless `update_group()` would PATCH a group with nothing in it.
        if name is None and spec is None:
            if notes is not None:
                return self.get_group(group_id)
            raise ValueError("update_group needs at least one of name/spec")
        # Only the two fields this call can send: a default the generated model
        # carries for the old notes write (`force`) would make the server refuse
        # the whole PATCH as a notes write.
        dumped = RunGroupPatch(name=name, spec=spec).model_dump(mode="json", exclude_none=True)
        body = {key: value for key, value in dumped.items() if key in ("name", "spec")}
        return self.transport.patch(f"/v1/groups/{group_id}", body)
from probe.sdk.client.authorship import _put_authorship  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.resources.projects.experiment_locator import _offset_cursor  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.resources.projects.experiments import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _EXPERIMENT_DESCRIPTION_RETIRED,
    _from_experiment_api,
    _refuse_read_only_experiment_fields,
)
from probe.sdk.client.resources.projects.projects import _same_name  # noqa: E402 -- pieces need each other; the front door loads this one first
