"""ProjectAdminMixin, Client's methods: list, update, move and delete projects, checking the server
applied each filter and write (twin: app/projects)."""

from __future__ import annotations

from .... import errors
from ....values.tags import canonical_tags
from ....delivery.transport.transport import Page


class _UNSET:  # noqa: N801 — a sentinel type, used as the value itself
    """Distinguishes "argument omitted" from an explicit ``None`` (0148).

    ``update_project``'s ``parent_project_id`` is the one field where those
    differ on the wire: an explicit null DETACHES, an omitted key leaves the
    parent untouched. A default of ``None`` could not express that.
    """


class ProjectAdminMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    @staticmethod
    def _verify_tags_filter(requested: list[str], items: list, route: str) -> None:
        """A pre-0066 backend IGNORES the ``tags=`` filter and returns the
        unfiltered list — a confident wrong answer presented as filtered (the
        same failure shape as the 0054 ``project_id`` guard in list_runs).
        Every returned row must carry ALL requested tags; both sides compare in
        canonical form so a legacy un-normalized row can never false-positive.
        Refuse rather than mislabel. (An empty page proves nothing and passes.)"""
        want = set(canonical_tags(requested))
        for item in items:
            if want - set(canonical_tags(item.get("tags") or [])):
                raise errors.NotFoundError(
                    f"this research-os backend predates {route}?tags= (0066): it "
                    "ignored the filter and returned unfiltered rows. Upgrade "
                    "the backend to filter by tags."
                )

    @staticmethod
    def _verify_tags_written(sent: list[str], row: dict | None, route: str) -> None:
        """A pre-0066 backend silently DROPS ``tags`` from write bodies (unknown
        Pydantic fields are ignored) and answers 200 with the row unchanged — a
        confident no-op. The response must echo the canonical sent list; refuse
        rather than pretend (the write-side twin of ``_verify_tags_filter``).
        ``row=None`` (a spooled fail-open write) is unverifiable and passes."""
        if row is None:
            return
        # scanning disabled: from .redaction import default_scrub

        if "tags" not in row or canonical_tags(row.get("tags") or []) != canonical_tags(
            # scanning disabled: default_scrub(sent)
            sent
        ):
            raise errors.NotFoundError(
                f"this research-os backend predates tags on {route} (0066): it "
                "ignored the tags write and returned the row unchanged. Upgrade "
                "the backend."
            )

    @staticmethod
    def _verify_parent_filter(requested: str, items: list, route: str) -> None:
        """A pre-0148 backend IGNORES ``parent_id=`` and returns EVERY project in
        the tenant -- which a caller asking for one project's children would then
        present as those children. The same failure shape as the tags and
        ``project_id`` guards: a confident wrong answer wearing the shape of a
        filtered one. Refuse rather than mislabel. (An empty page proves nothing
        and passes.)"""
        for item in items:
            if str(item.get("parent_project_id") or "") != str(requested):
                raise errors.NotFoundError(
                    f"this research-os backend predates {route}?parent_id= (0148): "
                    "it ignored the filter and returned unfiltered rows. Upgrade "
                    "the backend."
                )

    @staticmethod
    def _verify_part_of_filter(requested: str, items: list, route: str) -> None:
        """The same trap for ``part_of=`` (0401): an older backend ignores it and
        returns every project, which would read as the parts of ``requested``.
        Every row a 0401 backend returns carries ``part_of``, naming
        ``requested``. (An empty page proves nothing and passes.)"""
        for item in items:
            if str(requested) not in {str(target) for target in item.get("part_of") or ()}:
                raise errors.NotFoundError(
                    f"this research-os backend predates {route}?part_of= (0401): "
                    "it ignored the filter and returned unfiltered rows. Upgrade "
                    "the backend."
                )

    def list_projects(
        self,
        *,
        workspace_id: str | None = None,
        tags: list[str] | None = None,
        part_of: str | None = None,
        parent_id: str | None = None,
        **params,
    ) -> Page:
        """``tags`` filters to projects carrying ALL of them (AND, 0066).

        ``part_of`` lists the projects linked as a part of that one (0401), in
        any workspace. ``parent_id`` is the older filter, kept for existing
        callers.
        """
        query = dict(params)
        if workspace_id is not None:
            query["workspace_id"] = workspace_id
        if part_of is not None:
            query["part_of"] = part_of
        if parent_id is not None:
            query["parent_id"] = parent_id
        # Send the canonical form (the server normalizes anyway): the guard
        # below then compares like against like.
        tags = canonical_tags(tags) if tags else None
        if tags:
            query["tags"] = tags
        page = self.transport.get_page("/v1/projects", params=query or None)
        if tags and page.items:
            self._verify_tags_filter(tags, page.items, "GET /v1/projects")
        if part_of is not None and page.items:
            self._verify_part_of_filter(part_of, page.items, "GET /v1/projects")
        if parent_id is not None and page.items:
            self._verify_parent_filter(parent_id, page.items, "GET /v1/projects")
        return page

    def update_project(
        self,
        project_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        document: str | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        kind: str | None = None,
        parent_project_id: str | None | type[_UNSET] = _UNSET,
        authored_by: str | None = None,
    ) -> dict:
        """PATCH /v1/projects/{id} for display fields and visible Markdown.

        ``document`` is authored Markdown that lives INSIDE the
        project's Overview page, as a block the page's AI writer may not
        rewrite. It is replaced wholesale and is last-write-wins: read the
        current project immediately before editing and preserve its existing
        sections. ``""`` clears it. It is separate from the project's private
        Notes, but NOT from the Overview page -- it is part of it.

        DO NOT expect a read-back to be byte-identical: a detail GET answers
        from the page, which renders the document. A fenced block loses its
        language and an ``http://`` link loses its href, because a page may
        carry neither. Verify that what you meant is THERE, not that the bytes
        match.

        ``tags`` REPLACES the whole list ([] clears); the server normalizes to
        lowercase-kebab (CONTRACT.md "tags").

        ``kind`` re-declares what the project is for (0149); ``None`` leaves it
        untouched (kind cannot be cleared).

        ``parent_project_id`` is kept for existing callers and is the ONE
        explicit-null field: a project id moves the one ``part_of`` link that
        stands for this project's old filing to that project, ``None`` drops
        it, and omitting the argument leaves it untouched; the project's other
        ``part_of`` links stay. New code links projects with
        :meth:`add_project_reference` (``relation="part_of"``).

        A project's README embed is part of ``document``, not a separate
        field: write ``[README](https://github.com/owner/repo)`` on its own line
        and the repository's README renders at that point in the document. The
        server derives ``project.repo`` from it, so there is nothing else to set.

        Re-filing into another workspace is :meth:`move_project`, not a keyword here.
        Same route, but splitting the verbs keeps a reindex fan-out (see move_project)
        from being something you can trigger by mistyping an update.
        """
        body = {
            key: value
            for key, value in {
                "name": name,
                "description": description,
                "document": document,
                "tags": tags,
                "metadata": metadata,
                "kind": kind,
            }.items()
            if value is not None
        }
        if parent_project_id is not _UNSET:
            # Explicit null on the wire = detach; a uuid = attach/move.
            body["parent_project_id"] = parent_project_id
        if not body:
            raise ValueError("update_project needs at least one field to set")
        # AFTER the emptiness check, deliberately. `authored_by` declares who
        # wrote the OTHER fields; on its own it declares authorship of nothing,
        # and letting it satisfy "at least one field to set" would turn a
        # no-op call into a PATCH.
        _put_authorship(body, authored_by)
        row = self.transport.patch(f"/v1/projects/{project_id}", body)
        if document is not None:
            self._verify_entity_markdown_written(
                "project",
                document,
                row,
                "PATCH /v1/projects/{id}",
            )
        if tags is not None:
            self._verify_tags_written(tags, row, "PATCH /v1/projects/{id}")
        return row

    @staticmethod
    def _verify_entity_markdown_written(
        kind: str,
        sent: str,
        row: dict,
        route: str,
    ) -> None:
        """Refuse a successful-looking ``document`` no-op.

        Older Pydantic schemas ignore an unknown field and still answer 2xx. A
        visible document that silently vanished is worse than a capability
        error, so every entity write compares the value the write's OWN
        response carries before returning success.

        ``row`` MUST be that response, never a fresh detail read. Since 0219 a
        project's or experiment's detail GET answers ``document`` from
        the Overview page, which renders the document rather than storing it
        verbatim -- so a read-back comparison fails for text that landed
        exactly as sent, and reports it as a backend too old to trust.
        """
        # scanning disabled: from .redaction import default_scrub

        # The transport intentionally stores the safe form. Compare against
        # that same form while retaining the guard against silently lost writes.
        # scanning disabled: expected = default_scrub(sent) if sent.strip() else ""
        expected = sent if sent.strip() else ""
        if row.get("document") != expected:
            raise errors.RosError(
                f"the research-os backend accepted the {kind} Markdown write on "
                f"{route} but did not store it; upgrade the backend before relying "
                "on document/--summary"
            )

    @staticmethod
    def _verify_entity_markdown_present(
        kind: str,
        sent: str,
        row: dict,
        route: str,
    ) -> None:
        """The weaker half of the guard, for a read that cannot be byte-exact.

        A project's or experiment's detail GET answers from the Overview page,
        which renders the document; comparing bytes there fails for text that
        landed perfectly. What the guard actually defends against is a schema
        that took the field and stored nothing, and a document that comes back
        at all disproves that. Weaker on purpose, and said out loud rather than
        dressed up as the stronger check.
        """
        if sent.strip() and not str(row.get("document") or "").strip():
            raise errors.RosError(
                f"the research-os backend accepted the {kind} Markdown write on "
                f"{route} but stored nothing; upgrade the backend before relying "
                "on document/--summary"
            )

    def move_project(self, project_id: str, workspace_id: str) -> dict:
        """Re-file a project into another workspace.

        PATCH is the only backend door, but this is a much heavier operation than the
        verb suggests: when the workspace actually changes, the server reindexes every
        live descendant experiment and terminal run in the same transaction, because
        those documents denormalize ``workspace_id``. A no-op move (same workspace)
        skips the fan-out entirely.

        An unknown workspace is a 422, not a 404 — it is a rejected *value*, not a
        missing resource. Projects linked to this one stay where they are.
        """
        return self.transport.patch(f"/v1/projects/{project_id}", {"workspace_id": workspace_id})

    def delete_project(
        self, project_id: str, *, recursive: bool = False, dry_run: bool = False
    ) -> dict | None:
        """Move a project, and everything under it, to the server's TRASH.

        Experiments, runs, telemetry and files go with it, and the slug is freed.
        Probe support can restore it for 21 days (the returned receipt says
        until when); after that it is deleted for good. A server without the
        `trash` feature (:meth:`supports_feature`) deletes PERMANENTLY and
        returns None. 409 if a published experiment version pins something in
        it. Deleting a project never deletes the projects linked to it
        (``part_of`` or ``references``); ``recursive`` is kept for existing
        callers. ``dry_run=True`` changes nothing and answers what would go,
        whose it is and when it last changed."""
        # transport.request, not .delete: the parity guard resolves paths from
        # the AST, and a path mutated by += would read as unreachable. The
        # query rides `params`, keeping the literal template intact.
        if dry_run:
            self._require_dry_run_delete()
        params = {
            key: "true" for key, wanted in (("recursive", recursive), ("dry_run", dry_run)) if wanted
        }
        resp = self.transport.request(
            "DELETE",
            f"/v1/projects/{project_id}",
            params=params or None,
            idempotent=True,
        )
        return resp.json() if resp.content else None
from probe.sdk.client.authorship import _put_authorship  # noqa: E402 -- pieces need each other; the front door loads this one first
