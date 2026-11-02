from __future__ import annotations

import json
import logging
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from matrx_orm import Q

from matrx_utils.row_access import SHOWN_TO_VALUES, RowAccess, ShownToLiteral

from matrx_graph.db._registry import get_model
from matrx_graph.errors import DefinitionError, OutputContractError
from matrx_graph.types.definition import Definition

#: A workflow's row-access words (access ladder T-13): ``published_to_web`` is the
#: only anonymous lane and a workflow is born NOT published; ``shown_to`` is the
#: list filter (``None`` follows the type's knob — org-shown by default, because a
#: workflow nobody else can see is the exception); ``"only_me"`` is the explicit
#: "keep it to myself" choice the caller makes.

#: THE ARCHIVED-ITEMS LAW (Arman, 2026-09-09 —
#: ``common-docs/policies/archived-items.md``): every list over an entity that
#: can be archived carries a tri-state archive filter, and the default hides
#: archived rows. Same three words as the canonical ``wfx_list_scoped`` /
#: ``agx_list_scoped`` RPC parameter ``p_archived`` and the clients' shared
#: ``ArchiveFilter`` control, so one vocabulary crosses SQL, Python and TS.
#:
#: A boolean cannot express "archived only", which is exactly why the law names
#: three states rather than two.
ARCHIVED_FILTER_VALUES: frozenset[str] = frozenset({"active", "archived", "all"})
DEFAULT_ARCHIVED_FILTER = "active"

#: workflow.definition.workflow_type (mirrors agent.definition.agent_type): who made
#: the row. ``generated`` rows (a feature's own workflow for a parent record) are
#: hidden from list lanes unless the caller asks for them.
WORKFLOW_TYPE_VALUES: tuple[str, ...] = ("user", "builtin", "generated")


def _archived_predicate(archived: str) -> dict[str, Any]:
    """Translate the tri-state into the ORM filter fragment.

    Raises on anything else rather than silently falling back: an unrecognised
    value means a caller believes it is filtering when it is not, and a list
    that quietly shows archived rows is the defect this law exists to kill.
    """
    value = (archived or "").strip().lower() or DEFAULT_ARCHIVED_FILTER
    if value not in ARCHIVED_FILTER_VALUES:
        raise DefinitionError(
            f"archived must be one of {sorted(ARCHIVED_FILTER_VALUES)}, got {archived!r}"
        )
    if value == "all":
        return {}
    return {"is_archived": value == "archived"}


def _normalized_for_save(definition: Definition) -> Definition:
    """Config-declared handle lists as the node's config model computes them.

    Every writer (Studio, Conductor, MCP, an agent) goes through ``create`` /
    ``save_draft``, so the persisted draft never carries a stale or missing
    derived handle list (``matrx_graph.validation.normalize_config_output_handles``).
    """
    from matrx_graph.validation import normalize_config_output_handles

    return normalize_config_output_handles(definition)


class _Unset:
    """"Field not supplied" — distinct from ``None``, which CLEARS a nullable
    column. Used by ``save_draft`` for the IO-declaration columns."""


_UNSET = _Unset()


class DefinitionRow(BaseModel):
    """Row shape for workflow.definition + workflow.definition_version queries.

    Same shape whether loading current (is_version=False) or a snapshot
    (is_version=True) — only `version_number` / `changed_at` differ in
    meaning. This lets the router return a consistent response regardless
    of which table the row came from.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    definition_id: str  # same as id when is_version=False
    name: str
    description: str | None = None
    definition: Definition
    version: int
    version_number: int | None = None  # set when is_version=True
    is_version: bool
    is_active: bool = True
    is_archived: bool = False
    published_to_web: bool = False
    shown_to: str | None = None
    workflow_type: str = "user"
    tags: list[str] = Field(default_factory=list)
    category: str | None = None
    created_by: str | None = None
    organization_id: str | None = None
    project_id: str | None = None
    task_id: str | None = None
    change_note: str | None = None
    # SPEC-workflow-ui-contract §2.1 — THE workflow-level IO declaration.
    # AUTHOR-DECLARED, never derived: derivation (compute_deliverables) is
    # the validator's job and the serving fallback. NULL output_kind on a
    # multi-deliverable workflow is a real answer — "the run's shape IS the
    # collection" — not a gap. Copied into the version snapshot at publish.
    input_kind: str | None = None
    output_kind: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    changed_at: datetime | None = None
    is_published: bool = False
    # The definition's active-run cap (NULL = unlimited). Carried on the row so
    # a run start that already loaded the definition checks its cap without a
    # second read. Only a DEFINITION row carries it — a version row leaves it
    # None and the caller reads the definition's own value.
    max_concurrent_runs: int | None = None


class DefinitionStore:
    """CRUD + versioning over workflow.definition / workflow.definition_version.

    Mirrors the agx_ manager semantics:
        - `load(id)` — returns the current main-table row
        - `load(id, is_version=True, version_id=...)` — returns the snapshot row
        - `create(...)` — inserts main-table row AND a v1 snapshot in one txn
        - `save_draft(id, ...)` — updates main-table row in place (no version bump)
        - `publish(id, change_note=...)` — increments `version`, snapshots into
          workflow.definition_version, keeps main row as the current working copy

    Uses the host-injected matrx-orm models (``configure_db`` +
    ``db_requirements``); resolution happens at call time so import stays free
    of any configured registry.
    """

    async def create(
        self,
        *,
        name: str,
        definition: Definition,
        description: str | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
        project_id: str | None = None,
        task_id: str | None = None,
        tags: list[str] | None = None,
        category: str | None = None,
        published_to_web: bool = False,
        shown_to: ShownToLiteral | None = None,
        workflow_type: str = "user",
    ) -> DefinitionRow:
        """Create a definition + its v1 snapshot in one transaction.

        ``workflow_type`` (``user`` | ``builtin`` | ``generated``) is written
        explicitly; feature writers pass ``generated`` / ``builtin`` so the row
        stays out of the list lanes.

        ``published_to_web`` is written explicitly (never left to a column default)
        and defaults to not published. ``shown_to`` defaults to ``None`` (follow the
        type's knob); pass ``"only_me"`` for the explicit "keep it to myself" choice.
        """
        from matrx_orm import transaction
        from matrx_orm.core.transaction import get_active_connection

        if shown_to is not None and shown_to not in SHOWN_TO_VALUES:
            raise DefinitionError(
                f"Unknown shown_to '{shown_to}' — expected one of "
                f"{', '.join(SHOWN_TO_VALUES)}."
            )
        if workflow_type not in WORKFLOW_TYPE_VALUES:
            raise DefinitionError(
                f"Unknown workflow_type '{workflow_type}' — expected one of "
                f"{', '.join(WORKFLOW_TYPE_VALUES)}."
            )
        access = RowAccess(published_to_web=published_to_web, shown_to=shown_to)

        definition = _normalized_for_save(definition)
        definition_id = str(uuid4())
        async with transaction():
            instance = await get_model("WfDefinition").create(
                id=definition_id,
                name=name,
                description=description,
                nodes=[n.model_dump(mode="json") for n in definition.nodes],
                edges=[e.model_dump(mode="json") for e in definition.edges],
                viewport=definition.viewport.model_dump(mode="json"),
                channels=[c.model_dump(mode="json") for c in definition.channels],
                strict_channels=definition.strict_channels,
                entry_nodes=definition.entry_nodes,
                variables=[v.model_dump(mode="json") for v in definition.variables],
                metadata=definition.metadata,
                version=1,
                is_active=True,
                is_archived=False,
                workflow_type=workflow_type,
                **access.columns(user_id),
                tags=tags or [],
                category=category,
                created_by=_to_uuid(user_id),
                organization_id=_to_uuid(organization_id),
                project_id=_to_uuid(project_id),
                task_id=_to_uuid(task_id),
            )
            row = _instance_to_mapping(instance)
            await _insert_version_snapshot(
                row,
                change_note="initial version",
                changed_by_user_id=user_id,
                connection=get_active_connection(),
            )
        return _row_to_definition_row(row, is_version=False)

    async def load(
        self,
        definition_id: str,
        *,
        is_version: bool = False,
        version_number: int | None = None,
        version_id: str | None = None,
    ) -> DefinitionRow | None:
        def_uuid = _to_uuid(definition_id)
        if def_uuid is None:
            return None
        if not is_version:
            rows = await (
                get_model("WfDefinition").filter(id=def_uuid, deleted_at__isnull=True).values()
            )
            if not rows:
                return None
            return _row_to_definition_row(rows[0], is_version=False)

        if version_number is None and version_id is None:
            raise DefinitionError("version_number or version_id is required when is_version=True")
        filters: dict[str, Any] = {"definition_id": def_uuid}
        if version_id is not None:
            normalized_version_id = _to_uuid(version_id)
            if normalized_version_id is None:
                return None
            filters["id"] = normalized_version_id
        if version_number is not None:
            filters["version_number"] = version_number
        rows = await get_model("WfDefinitionVersion").filter(**filters).values()
        if not rows:
            return None
        return _version_row_to_definition_row(rows[0])

    async def find_by_tag(self, tag: str) -> list[DefinitionRow]:
        """Every non-archived definition carrying ``tag`` — used by seed
        scripts and the boot-time seeded-definition drift guard."""
        from matrx_orm import ArrayContains, F

        rows = await (
            get_model("WfDefinition")
            .filter(ArrayContains(F("tags"), tag), is_archived=False, deleted_at__isnull=True)
            .values()
        )
        parsed = (_row_to_definition_row_or_skip(r, is_version=False) for r in rows)
        return [r for r in parsed if r is not None]

    def _user_scope_query(
        self,
        *,
        user_id: str | None = None,
        organization_id: str | None = None,
        project_id: str | None = None,
        archived: str = DEFAULT_ARCHIVED_FILTER,
        include_ids: Sequence[str] | None = None,
        include_generated: bool = False,
    ) -> Any | None:
        """Build the shared access scope for list and count reads.

        🚨 A LIST IS DECIDED BY ACCESS, NEVER BY THE SELECTED ORGANIZATION
        (common-docs/policies/access-ladder.md; Arman,
        2026-09-25: *"I can't find my workflows because it's filtering by
        org"*). The set is the person's own rows in EVERY organization, unioned
        with ``include_ids`` — the host's discoverable ids (owner, org
        membership, grants), which already span all of the person's
        organizations.

        ``organization_id`` is an explicit, on-page FILTER on top of that set
        (the person chose "only this organization"), never the header's
        selection and never a widening. With no person and no ids, it falls
        back to the organization's shareable rows (a system caller naming a
        tenant).

        ``None`` means an explicitly supplied invalid UUID, which must match
        nothing (rather than becoming an ORM ``IS NULL`` predicate).
        """
        owner_arm: dict[str, Any] = {}
        common: dict[str, Any] = {}
        org_filter: Any = None
        if user_id:
            coerced = _to_uuid(user_id)
            if coerced is None:
                return None
            owner_arm["created_by"] = coerced
        if organization_id:
            org_filter = _to_uuid(organization_id)
            if org_filter is None:
                return None
        if project_id:
            coerced = _to_uuid(project_id)
            if coerced is None:
                return None
            common["project_id"] = coerced
        common.update(_archived_predicate(archived))
        common["deleted_at__isnull"] = True
        if not include_generated:
            common["workflow_type__in"] = ("user", "builtin")

        extra_ids = _coerce_uuid_list(include_ids)
        qb = get_model("WfDefinition")
        if not owner_arm and not extra_ids:
            if org_filter is not None:
                return qb.filter(
                    organization_id=org_filter,
                    visibility__in=("internal", "link", "public"),
                    **common,
                )
            return qb.filter(**common)
        if org_filter is not None:
            common["organization_id"] = org_filter
        if not extra_ids:
            return qb.filter(**owner_arm, **common)
        arms = [Q(**owner_arm)] if owner_arm else []
        arms.append(Q(id__in=extra_ids))
        combined = arms[0]
        for arm in arms[1:]:
            combined = combined | arm
        return qb.filter(combined, **common)

    async def list_for_user(
        self,
        *,
        user_id: str | None = None,
        organization_id: str | None = None,
        project_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
        archived: str = DEFAULT_ARCHIVED_FILTER,
        include_ids: Sequence[str] | None = None,
        include_generated: bool = False,
        typed_only: bool = False,
        search: str | None = None,
    ) -> list[DefinitionRow]:
        """Everything the person can access, across all her organizations.

        ``include_ids`` is the host's discoverable-id set (e.g. share grants
        resolved through its access kernel): those rows are ORed into the
        owner arm so shared and organization-visible items appear in lists.
        The package stays access-system-agnostic — it never resolves grants
        itself; the optional ``organization_id`` filter, project filter,
        archive filter, soft-delete filter, ordering, and limit/offset apply
        identically to every arm. ``None``/empty ``include_ids`` keeps the
        exact single-query fast path.

        ``archived`` is the platform tri-state (``active`` — the law's
        hide-by-default — / ``archived`` / ``all``), applied in SQL so counts
        and pagination describe what the caller actually renders.

        ``typed_only`` keeps workflows that declare ``input_kind`` or ``output_kind`` (the
        ones that are Actions); ``search`` matches the name or description, case-insensitive.
        """
        qb = self._user_scope_query(
            user_id=user_id,
            organization_id=organization_id,
            project_id=project_id,
            archived=archived,
            include_ids=include_ids,
            include_generated=include_generated,
        )
        qb = _narrow(qb, typed_only=typed_only, search=search)
        if qb is None:
            return []
        rows = await qb.order_by("-updated_at").limit(limit).offset(offset).values()
        parsed = (_row_to_definition_row_or_skip(r, is_version=False) for r in rows)
        return [r for r in parsed if r is not None]

    async def count_for_user(
        self,
        *,
        user_id: str | None = None,
        organization_id: str | None = None,
        project_id: str | None = None,
        archived: str = DEFAULT_ARCHIVED_FILTER,
        include_ids: Sequence[str] | None = None,
        include_generated: bool = False,
        typed_only: bool = False,
        search: str | None = None,
    ) -> int:
        """Count exactly the rows that :meth:`list_for_user` can render."""
        qb = self._user_scope_query(
            user_id=user_id,
            organization_id=organization_id,
            project_id=project_id,
            archived=archived,
            include_ids=include_ids,
            include_generated=include_generated,
        )
        qb = _narrow(qb, typed_only=typed_only, search=search)
        return 0 if qb is None else int(await qb.count())

    async def save_draft(
        self,
        definition_id: str,
        *,
        definition: Definition,
        name: str | None = None,
        description: str | None | _Unset = _UNSET,
        expected_updated_at: datetime | None = None,
        expected_version: int | None = None,
        input_kind: str | None | _Unset = _UNSET,
        output_kind: str | None | _Unset = _UNSET,
        user_id: str | None = None,
    ) -> DefinitionRow:
        """Update the draft. Optionally optimistic-concurrency guarded.

        ``user_id`` is WHO SAVED THIS, and it is written to ``updated_by``.

        🚨 Passing it is not optional bookkeeping. ``platform._stamp_actor``
        (the BEFORE INSERT OR UPDATE trigger on ~610 tables) stamps
        ``updated_by`` from ``current_setting('app.user_id')`` or
        ``auth.uid()`` — and NEITHER exists on this path: the server talks to
        Postgres directly through matrx-orm, not through PostgREST, so there
        is no verified JWT for ``auth.uid()`` to read and nothing sets the
        GUC. The trigger's ``COALESCE(uid, NEW.updated_by)`` therefore
        preserves exactly what the application wrote, and if the application
        writes nothing the column stays NULL forever. Definition aa3e6306…
        had taken 90 draft saves with ``updated_by = NULL`` throughout:
        nobody could be told who broke it. ``create()`` has always passed
        ``created_by`` explicitly for the same reason; this is its twin.

        ``description``, ``input_kind`` / ``output_kind`` use explicit-null
        semantics: omit to leave the stored value untouched; pass ``None`` to
        clear it. The Studio needs that distinction to make Delete description
        a real persisted edit rather than a visually successful no-op.

        ``input_kind`` / ``output_kind`` are THE authoring seam for the
        workflow's IO declaration (SPEC §2.1). Omit them and the stored
        declaration is untouched; pass ``None`` to CLEAR it. They are written
        unvalidated on purpose — a draft is allowed to be mid-thought; the
        publish is the gate that refuses a declaration the graph contradicts.

        ``expected_version`` is the platform's canonical compare-and-swap
        against the trigger-maintained ``version`` column: a lost race
        raises ``matrx_orm.OptimisticLockError`` (carrying the current
        version + row), which the host maps to HTTP 409 version_conflict.
        Prefer it for new callers.

        ``expected_updated_at`` (audit P1-11) is the older timestamp guard,
        kept for callers that only hold ``updated_at``: the UPDATE applies
        only if the row's ``updated_at`` still equals it; a lost race
        raises :class:`matrx_graph.errors.DraftConflictError`.
        """
        definition = _normalized_for_save(definition)
        updates: dict[str, Any] = {
            "nodes": [n.model_dump(mode="json") for n in definition.nodes],
            "edges": [e.model_dump(mode="json") for e in definition.edges],
            "viewport": definition.viewport.model_dump(mode="json"),
            "channels": [c.model_dump(mode="json") for c in definition.channels],
            "strict_channels": definition.strict_channels,
            "entry_nodes": definition.entry_nodes,
            "variables": [v.model_dump(mode="json") for v in definition.variables],
            "metadata": definition.metadata,
            "updated_at": datetime.now(UTC),
        }
        # Only a REAL author is written. `_to_uuid` answers None for a
        # non-UUID principal (admin-token auth sets user_id to the literal
        # "admin"), and writing that None would blank a known author — the
        # exact opposite of the point.
        author = _to_uuid(user_id)
        if author is not None:
            updates["updated_by"] = author
        if name is not None:
            updates["name"] = name
        if not isinstance(description, _Unset):
            updates["description"] = description
        if not isinstance(input_kind, _Unset):
            updates["input_kind"] = (input_kind or "").strip() or None
        if not isinstance(output_kind, _Unset):
            updates["output_kind"] = (output_kind or "").strip() or None
        # Explicit revision bump: hosted, platform._touch_row recomputes the
        # same OLD.version + 1 and wins; STANDALONE has no trigger, and an
        # unguarded save that leaves `version` untouched would let a
        # concurrent expected_version CAS pass despite a real intervening
        # edit (silent lost update). Every content write bumps.
        from matrx_orm import F

        updates["version"] = F("version") + 1

        filters: dict[str, Any] = {
            "id": _to_uuid(definition_id),
            "deleted_at__isnull": True,
        }
        if expected_updated_at is not None:
            filters["updated_at"] = expected_updated_at

        result = await get_model("WfDefinition").update_where(
            filters, expected_version=expected_version, **updates
        )
        if result.rows_affected == 0:
            if expected_updated_at is not None and await get_model("WfDefinition").exists(
                id=_to_uuid(definition_id), deleted_at__isnull=True
            ):
                from matrx_graph.errors import DraftConflictError

                raise DraftConflictError(
                    f"Workflow '{definition_id}' was modified since it "
                    "was loaded — reload before saving."
                )
            raise DefinitionError(f"Workflow definition '{definition_id}' not found.")
        return _row_to_definition_row(result.updated_rows[0], is_version=False)

    async def publish(
        self,
        definition_id: str,
        *,
        change_note: str | None = None,
        changed_by_user_id: str | None = None,
    ) -> DefinitionRow:
        """Promote the current draft to a new published version.

        Increments `version` on the main row and writes a snapshot into
        workflow.definition_version with the new version_number. Returns the
        updated main row.

        **The publish is the output contract's gate** (SPEC §2.3). A declared
        ``output_kind`` that is not produced by any deliverable REFUSES the
        publish, naming the mismatch — the whole transaction rolls back, so a
        lying declaration never reaches a version anyone can pin. No
        declaration plus exactly one deliverable BACKFILLS the column from it,
        in the same transaction, so the snapshot carries the resolved value.
        No declaration plus several deliverables stays NULL: that is the
        collection answer, not a hole to fill with a minted wrapper kind.
        """
        from matrx_orm import F, transaction
        from matrx_orm.core.transaction import get_active_connection

        async with transaction():
            # 🚨 A PUBLISH IS A RECORDED CHANGE (VERSION-HISTORY-FIX / HR-LOOP-CLEANUP, 2026-09-23).
            # This used to be `set version = version + 1` and nothing else — exactly the write the
            # database's no-op rule (`platform.no_change_keeps_its_version()`: equal in everything
            # but version/updated_at -> keep OLD) swallows, after which the snapshot below hit
            # UNIQUE (definition_id, version_number) and `ON CONFLICT DO NOTHING` inserted nothing:
            # a publish that "succeeded" with no new version. The same UPDATE now also writes the
            # publish itself into the row's system metadata, so it is a real change on any table
            # binding, and the row is locked first so the metadata merge cannot lose an autosave.
            model = get_model("WfDefinition")
            live = {"id": _to_uuid(definition_id), "deleted_at__isnull": True}
            locked = await model.filter(**live).select_for_update().values("version", "metadata")
            if not locked:
                raise DefinitionError(f"Workflow definition '{definition_id}' not found.")
            next_version = int(locked[0]["version"]) + 1
            result = await model.update_where(
                live,
                version=F("version") + 1,
                metadata=_with_publish_stamp(
                    locked[0].get("metadata"), next_version, changed_by_user_id
                ),
            )
            if result.rows_affected == 0:
                raise DefinitionError(f"Workflow definition '{definition_id}' not found.")
            row = result.updated_rows[0]
            if int(row["version"]) != next_version:
                raise DefinitionError(
                    f"Workflow definition '{definition_id}' publish did not advance its version "
                    f"(expected {next_version}, the database kept {row['version']}); nothing was "
                    "published. A trigger that treats the publish as a no-op is the usual cause."
                )

            backfilled = _validate_io_declaration_for_publish(row, definition_id)
            if backfilled is not None:
                await get_model("WfDefinition").update_where(
                    {"id": _to_uuid(definition_id)},
                    output_kind=backfilled,
                )
                row = dict(row)
                row["output_kind"] = backfilled

            landed = await _insert_version_snapshot(
                row,
                change_note=change_note,
                changed_by_user_id=changed_by_user_id,
                connection=get_active_connection(),
            )
            if not landed:
                # Raising rolls the increment back with it: never a version with no snapshot.
                raise DefinitionError(
                    f"Workflow definition '{definition_id}' publish refused: a snapshot for "
                    f"version {row['version']} already exists, so this publish would pin nothing new."
                )
        return _row_to_definition_row(row, is_version=False)

    async def list_versions(self, definition_id: str) -> list[DefinitionRow]:
        rows = await (
            get_model("WfDefinitionVersion")
            .filter(definition_id=_to_uuid(definition_id))
            .order_by("-version_number")
            .values()
        )
        return [_version_row_to_definition_row(r) for r in rows]

    async def list_history(self, definition_id: str) -> list[DefinitionRow]:
        """Every saved revision of a workflow, newest first.

        Published snapshots are only a subset of workflow history. The
        canonical ``history.row_versions`` ledger captures every autosave,
        rename, publish, and platform-authored update, so the Creator-facing
        history UI must read this source rather than pretending publishes are
        the whole story.
        """
        definition = await self._load_entity(definition_id)
        if definition is None:
            return []
        published = {
            row.version_number: row for row in await self.list_versions(definition_id)
        }
        history = await definition.versions(limit=max(int(definition.version) + 1, 1))
        return [
            _history_row_to_definition_row(row, published.get(int(row.version)))
            for row in history
        ]

    async def load_history_revision(
        self, definition_id: str, revision: int
    ) -> DefinitionRow | None:
        definition = await self._load_entity(definition_id)
        if definition is None:
            return None
        history = await definition.versions(limit=max(int(definition.version) + 1, 1))
        published = {
            row.version_number: row for row in await self.list_versions(definition_id)
        }
        for row in history:
            if int(row.version) == revision:
                return _history_row_to_definition_row(row, published.get(revision))
        return None

    async def _load_entity(self, definition_id: str) -> Any | None:
        definition_uuid = _to_uuid(definition_id)
        if definition_uuid is None:
            return None
        rows = await get_model("WfDefinition").filter(id=definition_uuid).limit(1).all()
        return rows[0] if rows else None

    async def archive(self, definition_id: str) -> None:
        from matrx_orm import F

        await get_model("WfDefinition").update_where(
            {"id": _to_uuid(definition_id), "deleted_at__isnull": True},
            is_archived=True,
            version=F("version") + 1,
        )

    async def set_tags(
        self, definition_id: str, tags: list[str], *, user_id: str | None = None
    ) -> DefinitionRow | None:
        """Replace the workflow's tags (the draft row's ``tags`` column) and nothing else.

        Units are found by tag (``platform:<key>``), so tags are an address, not decoration.
        ``user_id`` is WHO CHANGED THEM, written to ``updated_by`` for the same reason
        :meth:`save_draft` writes it (no ``auth.uid()`` on a direct connection). Returns the
        updated row, or ``None`` when no live workflow has that id.
        """
        from matrx_orm import F

        updates: dict[str, Any] = {"tags": list(tags), "version": F("version") + 1}
        author = _to_uuid(user_id)
        if author is not None:
            updates["updated_by"] = author
        result = await get_model("WfDefinition").update_where(
            {"id": _to_uuid(definition_id), "deleted_at__isnull": True}, **updates
        )
        if result.rows_affected == 0:
            return None
        return _row_to_definition_row(result.updated_rows[0], is_version=False)

    async def unarchive(self, definition_id: str) -> bool:
        from matrx_orm import F

        result = await get_model("WfDefinition").update_where(
            {"id": _to_uuid(definition_id), "deleted_at__isnull": True},
            is_archived=False,
            version=F("version") + 1,
        )
        return result.rows_affected > 0

    async def soft_delete(self, definition_id: str) -> bool:
        """Canonical soft delete — the row survives (restorable via the
        platform's entity_undelete / version history) but disappears from
        every store read, which all filter ``deleted_at IS NULL``. On the
        hosted platform a DB trigger (workflow._cascade_definition_soft_delete)
        deactivates + soft-deletes the definition's triggers in the same
        statement; standalone installs without that trigger should not rely
        on cascade."""
        from matrx_orm import F

        result = await get_model("WfDefinition").update_where(
            {"id": _to_uuid(definition_id), "deleted_at__isnull": True},
            deleted_at=datetime.now(UTC),
            version=F("version") + 1,
        )
        return result.rows_affected > 0


def _to_uuid(value: str | None) -> str | None:
    """Coerce a string to a normalized UUID string, or None.

    Returns None for empty/None AND for strings that are not valid UUIDs
    (e.g. admin-token auth sets `user_id` to a non-UUID literal like
    "admin"). The alternative — raising ValueError — bubbles up as a
    generic 500 at the router, which is hostile to the caller.
    """
    if not value:
        return None
    try:
        return str(UUID(str(value)))
    except (ValueError, AttributeError, TypeError):
        return None


def _coerce_uuid_list(values: Sequence[str] | None) -> list[str]:
    """Normalize an id list for an ``id__in`` filter, dropping invalid
    entries (same tolerance as _to_uuid — never let one bad id 500 a list)."""
    if not values:
        return []
    return [u for u in (_to_uuid(v) for v in values) if u is not None]


def _instance_to_mapping(instance: Any) -> dict[str, Any]:
    """Flatten a hydrated model instance into the plain column mapping the
    row-shaping helpers consume (same keys an asyncpg Record carried)."""
    return {name: getattr(instance, name) for name in type(instance)._fields}


def _validate_io_declaration_for_publish(row: Any, definition_id: str) -> str | None:
    """SPEC §2.3 — the publish gate for the workflow's IO declaration.

    Runs THE shared deliverable rule
    (:func:`matrx_graph.types.deliverables.resolve_io_declaration`) — the very
    function ``GET /workflows/{id}/result-schema`` serves from, so the endpoint
    can never advertise a contract this gate does not enforce.

    Returns the ``output_kind`` to BACKFILL onto the row, or None when the
    stored declaration already stands (or there is nothing to derive).
    Raises :class:`DefinitionError` when the declaration lies.
    """
    from matrx_graph.compile import compile as compile_graph
    from matrx_graph.types.deliverables import resolve_io_declaration

    declared_output = _declared_kind(row, "output_kind")
    declared_input = _declared_kind(row, "input_kind")
    try:
        definition = _build_definition(row)
        graph = compile_graph(definition)
    except Exception as exc:  # noqa: BLE001
        # A draft that does not compile has always been publishable (a
        # half-built workflow is saved, then finished). We cannot validate
        # what we cannot compile — but a DECLARATION that goes unchecked is
        # exactly the silent lie this gate exists to stop, so SCREAM.
        if declared_output or declared_input:
            logger.error(
                "[definition_store] PUBLISH UNVALIDATED: workflow %s declares "
                "input_kind=%r output_kind=%r but its graph does not compile (%s) — the "
                "output contract was NOT enforced for this version. Fix the graph.",
                definition_id,
                declared_input,
                declared_output,
                exc,
            )
        return None

    verdict = resolve_io_declaration(
        graph,
        definition,
        declared_output_kind=declared_output,
        declared_input_kind=declared_input,
    )
    if verdict.error:
        raise OutputContractError(
            f"Workflow definition '{definition_id}' cannot be published: {verdict.error}"
        )
    if declared_output is None and verdict.output_kind_backfilled and verdict.output_kind:
        return verdict.output_kind
    return None


def _with_publish_stamp(
    metadata: Any, version: int, changed_by_user_id: str | None
) -> dict[str, Any]:
    """The row's system metadata with this publish recorded on it (REC-59: system data lives in
    ``metadata``). ``version`` makes every stamp differ from every earlier one, so the publish is
    a change even when two land inside one clock tick."""
    merged = dict(_coerce_json_value(metadata) or {})
    merged["published"] = {
        "version": version,
        "at": datetime.now(UTC).isoformat(),
        "by": changed_by_user_id,
    }
    return merged


async def _insert_version_snapshot(
    main_row: dict[str, Any],
    *,
    change_note: str | None,
    changed_by_user_id: str | None,
    connection: Any = None,
) -> int:
    # ON CONFLICT (definition_id, version_number) DO NOTHING — returns how many rows LANDED, so
    # the caller can refuse a publish whose snapshot slot was already taken instead of passing.
    return await get_model("WfDefinitionVersion").bulk_insert_ignore(
        [
            {
                "definition_id": str(main_row["id"]),
                "version_number": main_row["version"],
                "name": main_row["name"],
                "description": main_row["description"],
                "nodes": _coerce_json_value(main_row["nodes"]),
                "edges": _coerce_json_value(main_row["edges"]),
                "viewport": _coerce_json_value(main_row["viewport"]),
                "channels": _coerce_json_value(main_row["channels"]),
                "strict_channels": main_row["strict_channels"],
                "entry_nodes": _coerce_json_value(main_row["entry_nodes"]),
                "variables": _coerce_json_value(main_row["variables"]) or [],
                "metadata": _coerce_json_value(main_row["metadata"]),
                "tags": list(main_row["tags"] or []),
                "category": main_row["category"],
                "is_active": main_row["is_active"],
                # SPEC §2.1 — the IO declaration rides into the snapshot, so a
                # pinned version answers "what does this produce" from its own
                # row instead of the mutable draft's.
                "input_kind": _declared_kind(main_row, "input_kind"),
                "output_kind": _declared_kind(main_row, "output_kind"),
                "change_note": change_note,
                "changed_by_user_id": _to_uuid(changed_by_user_id),
            }
        ],
        on_conflict=["definition_id", "version_number"],
        connection=connection,
    )


def _coerce_json_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        return json.loads(value)
    return value


logger = logging.getLogger(__name__)


def _narrow(qb: Any | None, *, typed_only: bool, search: str | None) -> Any | None:
    """The optional narrowings shared by ``list_for_user`` and ``count_for_user``."""
    if qb is None:
        return None
    from matrx_orm import Q

    if typed_only:
        qb = qb.filter(Q(input_kind__isnull=False) | Q(output_kind__isnull=False))
    term = (search or "").strip()
    if term:
        qb = qb.filter(Q(name__icontains=term) | Q(description__icontains=term))
    return qb


def _row_to_definition_row_or_skip(row: Any, *, is_version: bool) -> DefinitionRow | None:
    """List-path parse: one malformed stored row must never kill the whole
    catalog (a probe row missing ``nodes[].position`` once 500'd every
    consumer's workflow list). Reconcile: skip the row and SCREAM with the
    exact id + error so the bad data gets fixed. Single-row ``load`` keeps
    raising — asking for a specific broken row is a real error."""
    try:
        return _row_to_definition_row(row, is_version=is_version)
    except Exception:
        logger.exception(
            "[definition_store] MALFORMED workflow.definition row SKIPPED from list "
            "(id=%s, name=%r) — fix the stored row; this is a data defect, not a display issue.",
            row.get("id") if isinstance(row, dict) else "?",
            row.get("name") if isinstance(row, dict) else "?",
        )
        return None


def _row_to_definition_row(row: Any, *, is_version: bool) -> DefinitionRow:
    return DefinitionRow(
        id=str(row["id"]),
        definition_id=str(row["id"]),
        name=row["name"],
        description=row["description"],
        definition=_build_definition(row),
        version=row["version"],
        is_version=is_version,
        is_active=row["is_active"],
        is_archived=row["is_archived"],
        published_to_web=bool(row.get("published_to_web")),
        shown_to=str(row["shown_to"]) if row.get("shown_to") else None,
        workflow_type=str(row.get("workflow_type") or "user"),
        tags=list(row["tags"] or []),
        category=row["category"],
        created_by=str(row["created_by"]) if row["created_by"] else None,
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        project_id=str(row["project_id"]) if row["project_id"] else None,
        task_id=str(row["task_id"]) if row["task_id"] else None,
        input_kind=_declared_kind(row, "input_kind"),
        output_kind=_declared_kind(row, "output_kind"),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        max_concurrent_runs=_optional_int(row, "max_concurrent_runs"),
    )


def _optional_int(row: Any, key: str) -> int | None:
    try:
        value = row[key]
    except (KeyError, IndexError, TypeError):
        return None
    return int(value) if value is not None else None


def _declared_kind(row: Any, key: str) -> str | None:
    """A declared kind off a row, or None.

    Tolerant of a row that predates the columns (history ``row_data`` JSON
    snapshots are stored bytes and will not grow the key retroactively).
    Empty string is NOT a declaration — a blank text column means
    "undeclared", never a kind named ""."""
    try:
        value = row[key]
    except (KeyError, IndexError, TypeError):
        return None
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _version_row_to_definition_row(row: Any) -> DefinitionRow:
    return DefinitionRow(
        id=str(row["id"]),
        definition_id=str(row["definition_id"]),
        name=row["name"] or "",
        description=row["description"],
        definition=_build_definition(row),
        version=row["version_number"],
        version_number=row["version_number"],
        is_version=True,
        is_active=bool(row["is_active"]) if row["is_active"] is not None else True,
        tags=list(row["tags"] or []),
        category=row["category"],
        # A version is owned like its definition: callers decide "is this the
        # platform's workflow" from it (subgraph.call by name reported
        # platform=false for every published Matrx System unit until 2026-10-27).
        created_by=str(row["created_by"]) if row.get("created_by") else None,
        organization_id=str(row["organization_id"]) if row.get("organization_id") else None,
        change_note=row["change_note"],
        input_kind=_declared_kind(row, "input_kind"),
        output_kind=_declared_kind(row, "output_kind"),
        changed_at=row["changed_at"],
        is_published=True,
    )


def _history_row_to_definition_row(
    history_row: Any, published: DefinitionRow | None
) -> DefinitionRow:
    row_data = _coerce_json_value(history_row.row_data)
    row = _row_to_definition_row(row_data, is_version=True)
    return row.model_copy(
        update={
            "id": str(history_row.id),
            "definition_id": str(row_data["id"]),
            "version": int(history_row.version),
            "version_number": int(history_row.version),
            "changed_at": history_row.occurred_at,
            "change_note": published.change_note if published else None,
            "is_published": published is not None,
        }
    )


def _build_definition(row: Any) -> Definition:
    return Definition.model_validate(
        {
            "version": "1",
            "nodes": _coerce_json_value(row["nodes"]) or [],
            "edges": _coerce_json_value(row["edges"]) or [],
            "viewport": _coerce_json_value(row["viewport"]) or {"x": 0, "y": 0, "zoom": 1.0},
            "channels": _coerce_json_value(row["channels"]) or [],
            "strict_channels": bool(row["strict_channels"])
            if row["strict_channels"] is not None
            else False,
            "entry_nodes": _coerce_json_value(row["entry_nodes"]) or [],
            "variables": _coerce_json_value(row["variables"]) or [],
            "metadata": _coerce_json_value(row["metadata"]) or {},
        }
    )
