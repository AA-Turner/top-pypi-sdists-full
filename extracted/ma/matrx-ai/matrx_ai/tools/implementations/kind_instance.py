"""``instance_*`` — agent tools for SAVED KIND INSTANCES (user data shaped by
a Content-IR kind).

``content_ir.kind_instance`` (kc_002) is the persistence half of the creator
loop: once a kind exists, "save this" turns a payload into a durable, owned,
shareable row. Contract facts these tools encode:

- ``kind_version`` is PINNED at write (like ``kind_example``): an instance
  records which schema version it was written against.
- ``validation_status`` is DERIVED — the DB BEFORE trigger
  (``content_ir.kind_instance_recompute_validation``) recomputes the verdict
  against the pinned version's schema on every relevant write. Writer-supplied
  status is never trusted; these tools read the verdict back after every write
  and surface anything non-passed loudly.
- Access = standard ownership of the INSTANCE (entity RLS on the
  ``content_ir_kind_instance`` token): a user owns instances of ANY kind they
  can view (including platform kinds); the kind's org/creator never governs
  the instance. Creating an instance additionally requires VIEWER on the kind.
- The version-bump/stranding trap: after ``kind_update_schema`` bumps a kind,
  older instances stay pinned to their original version. ``instance_update``
  offers ``repin_to_current`` to move an instance onto the current schema, and
  ``content_ir.revalidate_kind_instances`` (DB RPC) bulk-recomputes verdicts.
- Title derivation (2026-07-18): explicit title -> the kind's
  ``metadata.title_key`` field (per-kind override, non-empty scalar) -> the
  shared ``_TITLE_KEYS`` list -> None. Mirrored verbatim by matrx-frontend
  ``instance-title.ts``.
- ACCEPTED TRADE-OFF (2026-07-18 review F1): the definition-side trigger
  (``kind_definition_revalidate_instances``, AFTER UPDATE OF
  emitted_json_schema) revalidates ALL live instances of the kind
  synchronously inside the schema-change transaction — unbounded and
  unbatched. Correct-by-construction and fine at current volume; if a kind
  ever accumulates thousands of live instances, ``kind_update_schema`` will
  stall for the full recompute. The fix at that scale is batching the
  trigger into the RPC (deliberately NOT built now — no over-engineering).

Authorization mirrors ``kind_shared``: reads viewer-gated, writes editor-gated
through the live ``iam.has_access_for`` SECURITY DEFINER function (owner
fast-path in code), fail-closed, content-free denials on reads.
"""

from __future__ import annotations

import logging
import math
import traceback
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

from matrx_ai.db._registry import get_model as get_db_model
from matrx_ai.tools.implementations.kind_shared import (
    ctx_org_id,
    ctx_user_id,
    ensure_can_view_kind,
    ensure_root_marker,
    err,
    is_uuid,
    kind_title_key,
    resolve_kind,
    validate_against_schema,
)
from matrx_ai.tools.kinds.kind_instances import (
    KindInstanceDetail,
    KindInstancePage,
    KindInstanceRecord,
    KindInstanceSummary,
    KindInstanceWriteResult,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)

INSTANCE_ENTITY_TOKEN = "content_ir_kind_instance"

# Keys probed (in order) to derive the denormalized display title from data.
# CROSS-REPO MIRROR: matrx-frontend features/content-ir/studio/instance-title.ts
# (`INSTANCE_TITLE_KEYS` + `deriveInstanceTitle`) implements the SAME derivation
# order — explicit title -> the kind's `metadata.title_key` field (non-empty
# scalar) -> this shared list -> None. Change BOTH sides together.
_TITLE_KEYS = ("title", "name", "label", "heading", "subject", "customer")

_MAX_LIST_LIMIT = 200


# ---------------------------------------------------------------------------
# THE RECORD-STORE ARM (lane FINAL-SWITCH-KINDS, 2026-09-27)
# ---------------------------------------------------------------------------
#
# `content_ir.kind_instance` is declared superseded by `custom.record` (W1-REG). An
# organization that has adopted the record store for that source keeps its kind records
# THERE, and a tool that wrote the old table for it would be writing where nobody reads.
# The per-organization answer lives in the host (aidream `services/kind_records/routed.py`,
# the ONE door every server kind-record path asks). This package may never import the
# host, so the door is handed in: `matrx_ai.configure(kind_record_arm=...)`.
#
# Every verb asks `_store_arm(ctx)` once. `None` means today's table, and the legacy body
# below runs exactly as it always has.

#: The ``_ext`` key the host's kind-record arm is registered under.
KIND_RECORD_ARM_EXT_KEY = "kind_record_arm"

#: The actor a store-arm write declares — the same system word the legacy create declares.
_STORE_SYSTEM = {
    "create": "tool:instance_create",
    "update": "tool:instance_update",
    "delete": "tool:instance_delete",
}

_kind_arm_announced: set[str] = set()


def _kind_record_arm() -> Any | None:
    """The host's kind-record arm, or ``None`` on a host with no record store.

    Unwired is ANNOUNCED once, by name: without it every organization's kind records are
    read and written on today's table, including an organization that has moved them.
    """
    from matrx_ai._ext import get_ext, has_ext

    if has_ext(KIND_RECORD_ARM_EXT_KEY):
        return get_ext(KIND_RECORD_ARM_EXT_KEY)
    if "unwired" not in _kind_arm_announced:
        _kind_arm_announced.add("unwired")
        logger.warning(
            "matrx-ai has no '%s' configured, so the kind_instance tool reads and writes ONLY "
            "content_ir.kind_instance — an organization that keeps its kind records in the "
            "record store would not see what this tool saves. REMEDY: "
            "aidream/package_integration.py, matrx_ai.configure(kind_record_arm=KindRecordToolArm()).",
            KIND_RECORD_ARM_EXT_KEY,
        )
    return None


async def _store_arm(ctx: ToolContext) -> Any | None:
    """The arm, when THIS organization keeps its kind records in the record store; else None."""
    arm = _kind_record_arm()
    if arm is None:
        return None
    user_id = ctx_user_id(ctx)
    org_id = ctx_org_id(ctx)
    if not user_id or not org_id:
        # Nobody to act as: the host's door answers legacy for this too (AGT-N-4).
        return None
    if await arm.through_the_store(user_id=user_id, organization_id=org_id):
        return arm
    return None


def _store_row(row: dict[str, Any], arm: Any) -> Any:
    """A store record as the attribute row every body below already reads.

    The document carries the legacy relation's own columns key for key; the header carries
    the timestamps. `visibility` is not a column of a record — a record is seen through its
    Table's ladder — so the row says that instead of printing a legacy word it never had.
    """
    base: dict[str, Any] = {
        "id": row.get("id"),
        "kind_definition_id": row.get("kind_definition_id"),
        "kind_version": row.get("kind_version"),
        "title": row.get("title"),
        "data": row.get("data"),
        "validation_status": row.get("validation_status") or "pending",
        "validated_at": row.get("validated_at"),
        "created_by": row.get("created_by"),
        "organization_id": row.get("organization_id"),
        "metadata": row.get("metadata") or {},
        "visibility": row.get("visibility") or "table",
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "deleted_at": row.get("deleted_at"),
    }
    row_ns = SimpleNamespace(**base)
    row_ns._store_arm = arm  # noqa: SLF001 — marks which arm this row came from
    return row_ns


def _from_store(row: Any) -> Any | None:
    """The arm a resolved row came from, or ``None`` for a legacy row."""
    return getattr(row, "_store_arm", None)


def _exec_error(e: Exception) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc()),
    )


def _scalar_title(value: Any) -> str | None:
    """A non-empty scalar rendered as a title string; None for anything else.
    Mirrors the frontend `scalarTitle` exactly (booleans -> 'true'/'false')."""
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value) if math.isfinite(value) else None
    return None


def derive_title(data: Any, explicit: str | None, title_key: str | None = None) -> str | None:
    """Explicit title wins; else the kind's ``metadata.title_key`` field when it
    holds a non-empty scalar; else the first non-empty string under a shared
    title/name-ish key of the payload object.

    The derivation ORDER is a cross-repo contract — mirrored verbatim by
    matrx-frontend ``instance-title.ts#deriveInstanceTitle``."""
    if explicit:
        return explicit
    if isinstance(data, dict):
        if title_key:
            override = _scalar_title(data.get(title_key))
            if override:
                return override
        for key in _TITLE_KEYS:
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def instance_summary(row: Any, kind_slug: str | None = None) -> dict[str, Any]:
    out = {
        "id": str(row.id),
        "kind_definition_id": str(row.kind_definition_id),
        "title": row.title,
        "kind_version": row.kind_version,
        "validation_status": row.validation_status,
        "updated_at": str(row.updated_at) if row.updated_at else None,
        "deleted": row.deleted_at is not None,
    }
    if kind_slug is not None:
        out["kind"] = kind_slug
    return out


async def _can_access_instance(row: Any, ctx: ToolContext, level: str) -> bool:
    """RLS's answer, in the CALLER's session, for this instance at ``level``.

    ``viewer`` — ``content_ir.kind_instance`` returns the row to them.
    ``editor`` — ``SELECT ... FOR UPDATE`` returns it (the UPDATE policy answers).
    No owner fast path and no ``iam.has_access_for`` call: the database decides.
    """
    from matrx_ai.tools.person_session import as_the_person, person_may_change

    if not ctx_user_id(ctx):
        return False
    KindInstance = get_db_model("KindInstance")
    if level == "viewer":
        async with as_the_person():
            seen = await KindInstance.get_or_none(use_cache=False, id=str(row.id))
        return seen is not None
    return await person_may_change(KindInstance, {"id": str(row.id)})


async def _resolve_instance(
    instance_id: str, ctx: ToolContext, level: str
) -> tuple[Any | None, ToolResult | None]:
    """Fetch a live instance and gate it at ``level``. Missing, deleted, and
    unauthorized all return the same content-free not-found (an unauthorized
    probe learns nothing about another tenant's rows)."""
    instance_id = (instance_id or "").strip()
    if not instance_id or not is_uuid(instance_id):
        return None, err("validation", "instance_id must be a kind_instance UUID.")
    arm = await _store_arm(ctx)
    if arm is not None:
        # THE STORE ARM. The read door is the viewer gate and the write door is the editor
        # gate, so there is no second access check here to drift from them.
        found = await arm.get(
            user_id=ctx_user_id(ctx), organization_id=ctx_org_id(ctx), record_id=instance_id
        )
        if found is None or found.get("deleted_at") is not None:
            return None, err(
                "not_found",
                f"Instance {instance_id} was not found, or you do not have access to it.",
                "Check the id, or ask the owner to share the instance with you.",
            )
        return _store_row(found, arm), None
    from matrx_ai.tools.person_session import as_the_person

    KindInstance = get_db_model("KindInstance")
    async with as_the_person():  # the read itself is RLS's: a hidden row never loads
        row = await KindInstance.get_or_none(use_cache=False, id=instance_id)
    if row is None or row.deleted_at is not None or (
        level != "viewer" and not await _can_access_instance(row, ctx, level)
    ):
        return None, err(
            "not_found",
            f"Instance {instance_id} was not found, or you do not have access to it.",
            "Check the id, or ask the owner to share the instance with you.",
        )
    return row, None


async def instance_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Save a payload as a durable instance of a kind ("save this").

    Provide ``kind`` (slug or kind_definition_id) and ``data`` (the payload
    object). The stored instance CARRIES its root ``__kind`` marker — it is
    part of the data (KINDS_EVERYWHERE_PLAN §4.2), stamped (or corrected) here
    so a row can never forget what it is.
    The payload is validated against the kind's current schema BEFORE insert
    (refused on failure — a knowingly-broken instance is never written); the
    DB derived-on-write trigger then recomputes ``validation_status`` against
    the pinned kind_version, and that verdict is read back as the truth.

    ``title`` sets the display label; when omitted it is derived from
    title/name-ish keys in the data. The instance is created private, owned by
    you, in your active organization — you own instances of any kind you can
    view, including platform kinds. Requires viewer access on the kind.
    """
    from matrx_ai.tools._generated_declarations import InstanceCreateArgs

    InstanceCreateArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    data = args.get("data")
    title = (args.get("title") or "").strip() or None
    if not kind_ref:
        return err("validation", "kind (slug or kind_definition_id) is required.")
    if not isinstance(data, dict):
        return err("validation", "data must be a JSON object (the instance payload).")
    try:
        kd, failure = await resolve_kind(kind_ref, ctx)
        if failure:
            return failure
        denied = await ensure_can_view_kind(kd, ctx)
        if denied:
            return denied
        user_id = ctx_user_id(ctx)
        if not user_id:
            return err(
                "validation", "No authenticated user in context — cannot attribute the instance."
            )

        # THE MARKER IS THE DATA. Validation tolerates it (the checker does the
        # schema-aware reduction itself), so nothing is stripped on the way in.
        data = ensure_root_marker(data, kd.kind)
        if isinstance(kd.emitted_json_schema, dict):
            errors = validate_against_schema(data, kd.emitted_json_schema)
            if errors:
                return err(
                    "validation",
                    f"Payload does not validate against '{kd.kind}' v{kd.version}: {errors[:10]}",
                    "Fix the payload to match the kind's schema, then retry.",
                )

        KindInstance = get_db_model("KindInstance")
        payload: dict[str, Any] = {
            "kind_definition_id": str(kd.id),
            "kind_version": kd.version,
            "data": data,
            "title": derive_title(data, title, kind_title_key(kd)),
            "created_by": user_id,
        }
        # The INSTANCE lives in the CALLER's org (never the kind's — the kind's
        # org must not govern user data), READ off the carried context and
        # REFUSED by name when it is absent. Until 2026-09-17 the key was left
        # out and the DB `_stamp_org_default` backstop derived a tenant from
        # `created_by`, so the row landed in the agent owner's personal
        # workspace instead of the organization the person was working in.
        org_id = ctx_org_id(ctx)
        if not org_id:
            raise ValueError(
                f"instance_create({kd.kind!r}): this call carries no organization, so "
                "the instance has no tenant. A tool call inherits the organization the "
                "boundary admitted — fix the caller; the database never guesses one."
            )
        payload["organization_id"] = org_id
        arm = await _store_arm(ctx)
        if arm is not None:
            return await _store_create(arm, kd, payload, ctx)
        # A tool invocation is an agent-authored persistence door.  The host
        # emits this ContextVar declaration as transaction-local GUCs when the
        # injected ORM opens the create transaction; without it an admitted
        # row is correctly born unconfirmed, but the door is defective.
        from matrx_orm import declared_actor

        async with declared_actor("ai", "tool:instance_create"):
            created = await KindInstance.create_item(**payload)

        fresh = await KindInstance.get_or_none(use_cache=False, id=str(created.id))
        verdict = fresh.validation_status if fresh else "unknown"
        if verdict != "passed":
            # The derived-on-write DB trigger is the authority; disagreement
            # with our pre-check is a platform defect — scream, don't hide it.
            return err(
                "execution",
                f"Instance {created.id} of kind '{kd.kind}' was written but the DB validation "
                f"trigger marked it '{verdict}' while the in-process check passed. This is a "
                "validator-drift defect — report it.",
            )
        return ToolResult(
            success=True,
            output=KindInstanceWriteResult(
                instance_id=str(created.id),
                kind=kd.kind,
                kind_definition_id=str(kd.id),
                kind_version=kd.version,
                title=fresh.title if fresh else payload["title"],
                validation_status=verdict,
                message=(
                    f"Instance saved as '{fresh.title}'"
                    if fresh and fresh.title
                    else "Instance saved"
                )
                + f" (kind '{kd.kind}' v{kd.version}, verdict: {verdict}).",
            ),
        )
    except Exception as e:
        return _exec_error(e)


async def _store_create(
    arm: Any, kd: Any, payload: dict[str, Any], ctx: ToolContext
) -> ToolResult:
    """``instance_create`` on the record-store arm: the same payload, the same receipt.

    The store has no derived-on-write validation trigger, so the verdict is the one this
    call just established: ``passed`` when the kind carries a schema and the payload was
    checked against it above (a failing payload never gets here), ``pending`` when the kind
    has no schema to check against — said, never promoted to ``passed``.
    """
    verdict = "passed" if isinstance(kd.emitted_json_schema, dict) else "pending"
    values = {**payload, "validation_status": verdict}
    record_id = await arm.create(
        user_id=ctx_user_id(ctx),
        organization_id=ctx_org_id(ctx),
        values=values,
        system=_STORE_SYSTEM["create"],
    )
    title = payload.get("title")
    return ToolResult(
        success=True,
        output=KindInstanceWriteResult(
            instance_id=str(record_id),
            kind=kd.kind,
            kind_definition_id=str(kd.id),
            kind_version=kd.version,
            title=title,
            validation_status=verdict,
            message=(f"Instance saved as '{title}'" if title else "Instance saved")
            + f" (kind '{kd.kind}' v{kd.version}, verdict: {verdict}) in this organization's "
            "record store.",
        ),
    )


async def instance_list(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """List YOUR saved instances (rows you created), newest-updated first.

    ``kind`` (slug or kind_definition_id) narrows to one kind;
    ``status`` (pending/passed/failed) narrows by validation verdict.
    Pagination via ``limit`` (default 50, max 200) and ``offset``. The
    projection is intentionally light: id, kind, title, validation_status,
    kind_version, updated_at — use instance_get for the payload.
    """
    from matrx_ai.tools._generated_declarations import InstanceListArgs

    InstanceListArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    status = (args.get("status") or "").strip() or None
    limit = max(1, min(int(args.get("limit") or 50), _MAX_LIST_LIMIT))
    offset = max(0, int(args.get("offset") or 0))
    try:
        user_id = ctx_user_id(ctx)
        if not user_id:
            return err("validation", "No authenticated user in context.")

        kind_by_id: dict[str, str] = {}
        filters: dict[str, Any] = {"created_by": user_id}
        if kind_ref:
            kd, failure = await resolve_kind(kind_ref, ctx)
            if failure:
                return failure
            denied = await ensure_can_view_kind(kd, ctx)
            if denied:
                return denied
            filters["kind_definition_id"] = str(kd.id)
            kind_by_id[str(kd.id)] = kd.kind
        if status:
            if status not in ("pending", "passed", "failed"):
                return err("validation", "status must be one of: pending, passed, failed.")
            filters["validation_status"] = status

        arm = await _store_arm(ctx)
        if arm is not None:
            rows = [
                _store_row(found, arm)
                for found in await arm.list(
                    user_id=user_id, organization_id=ctx_org_id(ctx), match=filters
                )
                if found.get("deleted_at") is None
            ]
        else:
            KindInstance = get_db_model("KindInstance")
            rows = [r for r in await KindInstance.filter(**filters).all() if r.deleted_at is None]
        rows.sort(key=lambda r: str(r.updated_at or ""), reverse=True)
        total = len(rows)
        page = rows[offset : offset + limit]

        # Resolve kind slugs for the page (single fetch per distinct kind).
        KindDefinition = get_db_model("KindDefinition")
        for r in page:
            kd_id = str(r.kind_definition_id)
            if kd_id not in kind_by_id:
                kd_row = await KindDefinition.get_or_none(use_cache=False, id=kd_id)
                kind_by_id[kd_id] = kd_row.kind if kd_row else "unknown"

        return ToolResult(
            success=True,
            output=KindInstancePage(
                total=total,
                limit=limit,
                offset=offset,
                instances=[
                    KindInstanceSummary(
                        **instance_summary(r, kind_by_id.get(str(r.kind_definition_id)))
                    )
                    for r in page
                ],
            ),
        )
    except Exception as e:
        return _exec_error(e)


async def instance_get(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Fetch one instance: full payload, title, pinned kind_version, derived
    validation_status, and the kind's slug/current version (so a pin behind
    the current schema is visible). Access: viewer on the instance (owner /
    shared / visibility) — missing and unauthorized return the same
    content-free not-found.
    """
    from matrx_ai.tools._generated_declarations import InstanceGetArgs

    InstanceGetArgs.model_validate(args)  # enforce the declared arg contract
    try:
        row, failure = await _resolve_instance(args.get("instance_id") or "", ctx, "viewer")
        if failure:
            return failure
        KindDefinition = get_db_model("KindDefinition")
        kd = await KindDefinition.get_or_none(use_cache=False, id=str(row.kind_definition_id))
        return ToolResult(
            success=True,
            output=KindInstanceDetail(
                instance=KindInstanceRecord(
                    **instance_summary(row, kd.kind if kd else None),
                    data=row.data,
                    validated_at=str(row.validated_at) if row.validated_at else None,
                    visibility=str(getattr(row.visibility, "value", row.visibility)),
                    created_at=str(row.created_at) if row.created_at else None,
                    metadata=row.metadata or {},
                ),
                kind_current_version=kd.version if kd else None,
                pinned_behind_current=bool(kd and row.kind_version != kd.version),
            ),
        )
    except Exception as e:
        return _exec_error(e)


def _instance_surface_write(row: Any, fresh: Any, kind: str, result: ToolResult) -> ToolResult:
    """Before → after of the instance (title + data, pretty JSON) for the diff card."""
    import json as _json

    from matrx_ai.tools.surface_write import attach_surface_write

    def _render(r: Any) -> str:
        if r is None:
            return ""
        body = _json.dumps(getattr(r, "data", None), ensure_ascii=False, indent=2, sort_keys=True, default=str)
        return f"title: {getattr(r, 'title', None) or ''}\n{body}"

    return attach_surface_write(
        result,
        before=_render(row),
        after=_render(fresh),
        target_type="kind_instance",
        target_id=str(row.id),
        target_label=str(getattr(fresh, "title", None) or getattr(row, "title", None) or kind),
        mode="structured",
        content_format="json",
    )


async def instance_update(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Update an instance's ``data`` and/or ``title``. Editor access required.

    When the instance is pinned to the kind's CURRENT version, new data is
    validated before write (refused on failure). When it is pinned to an
    OLDER version the write proceeds and the DB trigger's verdict (computed
    against the pinned schema) is read back and surfaced loudly — pass
    ``repin_to_current=true`` to move the instance onto the current schema in
    the same write (the fix for the version-bump stranding trap).
    """
    from matrx_ai.tools._generated_declarations import InstanceUpdateArgs

    InstanceUpdateArgs.model_validate(args)  # enforce the declared arg contract
    data = args.get("data")
    title = args.get("title")
    repin = bool(args.get("repin_to_current", False))
    if data is None and title is None and not repin:
        return err("validation", "Provide data, title, and/or repin_to_current.")
    if data is not None and not isinstance(data, dict):
        return err("validation", "data must be a JSON object (the full replacement payload).")
    try:
        row, failure = await _resolve_instance(args.get("instance_id") or "", ctx, "editor")
        if failure:
            return failure
        KindDefinition = get_db_model("KindDefinition")
        kd = await KindDefinition.get_or_none(use_cache=False, id=str(row.kind_definition_id))
        if kd is None:
            return err("execution", "The instance's kind_definition no longer resolves.")

        updates: dict[str, Any] = {"updated_by": ctx_user_id(ctx)}
        target_version = kd.version if repin else row.kind_version
        if data is not None:
            data = ensure_root_marker(data, kd.kind)
            if target_version == kd.version and isinstance(kd.emitted_json_schema, dict):
                errors = validate_against_schema(data, kd.emitted_json_schema)
                if errors:
                    return err(
                        "validation",
                        f"Payload does not validate against '{kd.kind}' "
                        f"v{kd.version}: {errors[:10]}",
                        "Fix the payload to match the kind's schema, then retry.",
                    )
            updates["data"] = data
            derived = derive_title(
                data, title if isinstance(title, str) else None, kind_title_key(kd)
            )
            if derived is not None or title is not None:
                updates["title"] = derived
        elif isinstance(title, str):
            updates["title"] = title.strip() or None
        if repin:
            updates["kind_version"] = kd.version

        arm = _from_store(row)
        if arm is not None:
            # THE STORE ARM. The store stamps who wrote it on every value itself, so
            # `updated_by` is not a field of the record. With no trigger to derive the
            # verdict, a data change says what this call established: `passed` against the
            # current schema, `pending` when the instance stays pinned behind it.
            store_updates = {k: v for k, v in updates.items() if k != "updated_by"}
            if "data" in store_updates:
                checked = target_version == kd.version and isinstance(kd.emitted_json_schema, dict)
                store_updates["validation_status"] = "passed" if checked else "pending"
            await arm.update(
                user_id=ctx_user_id(ctx),
                organization_id=ctx_org_id(ctx),
                record_id=str(row.id),
                values=store_updates,
                system=_STORE_SYSTEM["update"],
            )
            found = await arm.get(
                user_id=ctx_user_id(ctx), organization_id=ctx_org_id(ctx), record_id=str(row.id)
            )
            fresh = _store_row(found, arm) if found is not None else None
        else:
            KindInstance = get_db_model("KindInstance")
            await KindInstance.update_where({"id": str(row.id)}, **updates)
            fresh = await KindInstance.get_or_none(use_cache=False, id=str(row.id))
        verdict = fresh.validation_status if fresh else "unknown"
        return _instance_surface_write(row, fresh, kd.kind, ToolResult(
            success=True,
            output=KindInstanceWriteResult(
                instance_id=str(row.id),
                kind=kd.kind,
                kind_version=fresh.kind_version if fresh else target_version,
                title=fresh.title if fresh else None,
                validation_status=verdict,
                warning=(
                    None
                    if verdict == "passed"
                    else (
                        f"The DB verdict for this instance is '{verdict}' (computed against "
                        f"pinned kind_version {fresh.kind_version if fresh else target_version}). "
                        "Fix the data, or repin_to_current after updating it to the current "
                        "schema."
                    )
                ),
            ),
        ))
    except Exception as e:
        return _exec_error(e)


async def instance_delete(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Soft-delete an instance (platform tombstone: ``deleted_at`` set, row
    retained). Editor access required. Deleting an already-deleted or unknown
    id returns the same content-free not-found."""
    from matrx_ai.tools._generated_declarations import InstanceDeleteArgs

    InstanceDeleteArgs.model_validate(args)  # enforce the declared arg contract
    try:
        row, failure = await _resolve_instance(args.get("instance_id") or "", ctx, "editor")
        if failure:
            return failure
        arm = _from_store(row)
        if arm is not None:
            answer = await arm.delete(
                user_id=ctx_user_id(ctx),
                organization_id=ctx_org_id(ctx),
                record_id=str(row.id),
                system=_STORE_SYSTEM["delete"],
            )
            if answer.get("applied") is False:
                # HELD, NOT DONE — and not an error to retry. The organization asks a person
                # before an agent removes a record from a table that predates this chat.
                return ToolResult(
                    success=True,
                    output=KindInstanceWriteResult(
                        instance_id=str(row.id),
                        deleted=False,
                        message=(
                            "HELD FOR APPROVAL — nothing was deleted yet. The delete is in this "
                            "organization's approval queue and happens when a person approves "
                            "it. Do NOT call the tool again for it; tell the person it is "
                            "waiting for their approval."
                        ),
                    ),
                )
            return ToolResult(
                success=True,
                output=KindInstanceWriteResult(
                    instance_id=str(row.id),
                    deleted=True,
                    message="Instance archived in this organization's record store (recoverable).",
                ),
            )
        KindInstance = get_db_model("KindInstance")
        await KindInstance.update_where(
            {"id": str(row.id)},
            deleted_at=datetime.now(UTC),
            updated_by=ctx_user_id(ctx),
        )
        return ToolResult(
            success=True,
            output=KindInstanceWriteResult(
                instance_id=str(row.id),
                deleted=True,
                message="Instance soft-deleted (recoverable tombstone).",
            ),
        )
    except Exception as e:
        return _exec_error(e)
