"""Shape LAYERS for the ``kindcomp_*`` tools: "my view" / "my organization's view".

``target`` on a kindcomp tool picks the table it works in:

- ``shared`` (default) — ``content_ir.kind_component``, today's behaviour and gates, untouched.
- ``mine`` — ``content_ir.kind_component_layer`` with ``audience_user_id`` = the caller.
- ``organization`` — the same table with ``audience_organization_id`` = the ``organization_id``
  argument; the DATABASE decides whether the caller is an owner/admin of it.

Three rules hold for every layer path (shape-layers PLAN v2, ATTACK finding B1):

1. **Everything runs AS THE PERSON** (``as_the_person``): the table's write-gate trigger lets writes
   with no signed-in user straight through, so a privileged-connection write would bypass the
   author-only / org-admin-only gate. No privileged fallback exists here.
2. **Reads declare their own audience.** RLS also shows a user's layer row to coworkers and every
   row to a platform admin, so each lookup states ``audience_user_id = me`` (or the explicit org)
   and every id lookup re-checks it. Another person's component id is "not found".
3. **Keyed by kind SLUG.** No ``kind_definition`` is required; an unregistered or unreadable kind
   works. A readable definition is only a schema HINT; a ``sample`` can stand in for one.

``kind_component`` is never read or written here, and there is no ``is_default`` logic.
"""

from __future__ import annotations

import traceback
from typing import Any

from matrx_ai.db._registry import get_model as get_db_model
from matrx_ai.tools.implementations.kind_shared import (
    COMPONENT_PLATFORMS,
    COMPONENT_ROLES,
    SHAPE_AUTHORING_POINTER,
    WriteRefused,
    bound_kind_bodies,
    can_access_kind,
    ctx_org_id,
    ctx_user_id,
    err,
    infer_schema_from_sample,
    is_uuid,
    normalize_kind_slug,
    refused,
    resolve_kind,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.person_session import as_the_person

LAYER_TARGETS = ("mine", "organization")
LAYER_SETTINGS_KEYS = frozenset(
    {"is_active", "sort_order", "config", "pinned_kind_version", "component_key", "notes"}
)
_RLS_REFUSAL_MARKERS = ("row-level security", "permission denied", "42501")


def is_layer_target(args: dict[str, Any]) -> bool:
    return (args.get("target") or "shared") in LAYER_TARGETS


def target_refusal(args: dict[str, Any]) -> ToolResult | None:
    target = args.get("target") or "shared"
    if target not in ("shared", *LAYER_TARGETS):
        return err(
            "validation",
            f"Invalid target '{target}'. Valid: shared, mine, organization.",
            "shared = the view everyone gets; mine = only me; organization = my whole organization "
            "(needs organization_id and an owner/admin role in it).",
        )
    if target == "organization" and not (args.get("organization_id") or "").strip():
        return err(
            "validation",
            "target 'organization' requires organization_id.",
            "Pass the organization this view is for; the database decides whether you may write it.",
        )
    return None


class Audience:
    """Who a layer row is for, plus the org stamped on the row."""

    def __init__(self, target: str, user_id: str, organization_id: str | None):
        self.target = target
        self.user_id = user_id
        self.organization_id = organization_id  # org stamped on the row

    @property
    def label(self) -> str:
        return "your own view" if self.target == "mine" else "your organization's view"

    def fields(self) -> dict[str, Any]:
        if self.target == "mine":
            return {"audience_user_id": self.user_id}
        return {"audience_organization_id": self.organization_id}

    def matches(self, row: Any) -> bool:
        """The explicit audience predicate, applied to a loaded row."""
        if row.deleted_at is not None:
            return False
        if self.target == "mine":
            return str(row.audience_user_id or "") == self.user_id
        return row.audience_user_id is None and str(row.audience_organization_id or "") == str(
            self.organization_id
        )


def audience_for(
    args: dict[str, Any], ctx: ToolContext
) -> tuple[Audience | None, ToolResult | None]:
    bad = target_refusal(args)
    if bad:
        return None, bad
    user_id = ctx_user_id(ctx)
    if not user_id:
        return None, err("forbidden", "A view belongs to a signed-in person; none is signed in.")
    target = args["target"]
    if target == "organization":
        org = str(args["organization_id"]).strip()
        if not is_uuid(org):
            return None, err("validation", "organization_id must be an organization id (uuid).")
        return Audience(target, user_id, org), None
    org = ctx_org_id(ctx)
    if not org:
        return None, err(
            "validation",
            "No active organization on this request, so a view cannot be stamped with one.",
            "Run from a client that carries the active organization.",
        )
    return Audience(target, user_id, org), None


def layer_summary(row: Any) -> dict[str, Any]:
    """``KindComponentSummary`` projection of a layer row (no definition id, never a default)."""
    return {
        "id": str(row.id),
        "kind_definition_id": "",
        "platform": row.platform,
        "role": row.role,
        "component_key": row.component_key,
        "source": row.source,
        "semver": row.semver,
        "version": row.version,
        "is_default": False,
        "is_active": row.is_active,
        "sort_order": row.sort_order,
        "pinned_kind_version": row.pinned_kind_version,
        "has_component_source": bool(row.component_source),
        "has_props_transform": bool(row.props_transform),
        "component_source_length": len(row.component_source or ""),
        "props_transform_length": len(row.props_transform or ""),
        "notes": row.notes,
        "deleted": row.deleted_at is not None,
    }


async def list_layer_rows(slug: str, audience: Audience) -> list[Any]:
    """The caller's OWN rows for a slug: explicit audience predicate, in the person's session."""
    Layer = get_db_model("KindComponentLayer")
    async with as_the_person():
        rows = await Layer.filter(kind=slug, **audience.fields()).all()
    return [r for r in rows if audience.matches(r)]


async def load_layer(component_id: str, audience: Audience) -> tuple[Any | None, ToolResult | None]:
    """One layer row by id, only if it is this audience's. Anything else: the same
    content-free not-found, whether the id is missing or someone else's."""
    Layer = get_db_model("KindComponentLayer")
    if not is_uuid(component_id):
        return None, err("not_found", f"View '{component_id}' not found.")
    async with as_the_person():
        row = await Layer.get_or_none(use_cache=False, id=component_id)
    if row is None or not audience.matches(row):
        return None, err("not_found", f"View '{component_id}' not found.")
    return row, None


async def _write(audience_row_id: str, ctx: ToolContext, **values: Any) -> ToolResult | None:
    """Update a layer row AS THE PERSON. Returns an error result, or None on success."""
    Layer = get_db_model("KindComponentLayer")
    values["updated_by"] = ctx_user_id(ctx)
    try:
        async with as_the_person():
            result = await Layer.update_where({"id": str(audience_row_id)}, **values)
            if not int(getattr(result, "rows_affected", 0) or 0):
                raise WriteRefused(f"no view {audience_row_id} was changed for this person")
    except WriteRefused as exc:
        return refused("view", audience_row_id, exc)
    except Exception as exc:
        if any(m in str(exc) for m in _RLS_REFUSAL_MARKERS):
            return refused("view", audience_row_id, exc)
        raise
    return None


async def _definition_hints(slug: str, ctx: ToolContext) -> tuple[Any | None, Any | None]:
    """Schema + canonical example of the REGISTERED kind, when the person can read it.
    Never required: unregistered, unreadable or ambiguous all quietly yield no hints."""
    try:
        kd, failure = await resolve_kind(slug, ctx)
        if failure or kd is None or not await can_access_kind(kd, ctx, "viewer"):
            return None, None
        KindExample = get_db_model("KindExample")
        examples = [
            e
            for e in await KindExample.filter(kind_definition_id=str(kd.id)).all()
            if e.deleted_at is None and e.is_canonical
        ]
        return kd, (examples[0].data if examples else None)
    except Exception:  # noqa: BLE001 -- hints are best-effort by design
        return None, None


def _fail(exc: BaseException) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="execution", message=str(exc), traceback=traceback.format_exc()),
    )


# ── tool bodies ────────────────────────────────────────────────────────────────


async def layer_get_context(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools.kinds.kind_authoring import (
        KindComponentSummary,
        KindDefinitionSummary,
    )
    from matrx_ai.tools.kinds.kind_components import (
        KindComponentContext,
        KindComponentContextSummary,
    )

    audience, bad = audience_for(args, ctx)
    if bad:
        return bad
    assert audience is not None
    slug = normalize_kind_slug((args.get("kind") or "").strip()) if args.get("kind") else ""
    component_id = (args.get("component_id") or "").strip()
    if not slug and not component_id:
        return err("validation", "Provide kind (slug) or component_id.")
    try:
        if component_id and not slug:
            row, failure = await load_layer(component_id, audience)
            if failure:
                return failure
            slug = row.kind
        rows = await list_layer_rows(slug, audience)
        kd, canonical = await _definition_hints(slug, ctx)
        schema = kd.emitted_json_schema if kd is not None else None
        notes: list[str] = [
            f"Target {audience.target}: only {audience.label} for '{slug}' is listed here; the shared "
            "view and other people's views are not shown."
        ]
        sample = args.get("sample")
        if kd is None:
            notes.append(
                f"Kind '{slug}' has no definition you can read — that does not block a view. "
                "Design against the on-screen instance."
            )
        if sample is not None and schema is None:
            schema = infer_schema_from_sample(sample)
            canonical = sample
            notes.append(
                "json_schema was inferred from the sample you passed: a hint for this view only, "
                "never the contract."
            )
        elif sample is not None and canonical is None:
            canonical = sample
        schema_out, example_out, bodies_note = bound_kind_bodies(
            schema, canonical, ctx=ctx, tool_name="kindcomp_get_context"
        )
        if bodies_note:
            notes.append(bodies_note)
        return ToolResult(
            success=True,
            output=KindComponentContext(
                kind=KindDefinitionSummary(
                    id=str(kd.id) if kd is not None else "",
                    kind=slug,
                    label=getattr(kd, "label", None),
                    is_active=bool(getattr(kd, "is_active", False)),
                    has_schema=schema is not None,
                ),
                json_schema=schema_out,
                canonical_example=example_out,
                canonical_example_status=None,
                examples=[],
                alternate_examples=[],
                components=[KindComponentSummary(**layer_summary(r)) for r in rows],
                component_ids=[str(r.id) for r in rows],
                open_incidents=[],
                incidents_visible=False,
                rules=SHAPE_AUTHORING_POINTER,
                summary=KindComponentContextSummary(
                    kind=slug,
                    kind_definition_id=str(kd.id) if kd is not None else "",
                    kind_version=getattr(kd, "version", None),
                    is_active=bool(getattr(kd, "is_active", False)),
                    has_canonical_example=example_out is not None,
                    component_count=len(rows),
                    open_incident_types=None,
                ),
                note=" ".join(notes),
            ),
            output_self_capped=True,
        )
    except Exception as e:
        return _fail(e)


async def layer_create(
    args: dict[str, Any], ctx: ToolContext, *, compile_checked: bool
) -> ToolResult:
    from matrx_ai.tools.kinds.kind_components import KindComponentCreateResult

    audience, bad = audience_for(args, ctx)
    if bad:
        return bad
    assert audience is not None
    slug = normalize_kind_slug((args.get("kind") or "").strip())
    component_key = (args.get("component_key") or "").strip()
    platform = (args.get("platform") or "web").strip()
    role = (args.get("role") or "output").strip()
    if platform not in COMPONENT_PLATFORMS or role not in COMPONENT_ROLES:
        return err("validation", f"Invalid platform/role '{platform}'/'{role}'.")
    try:
        # One live view per (kind, platform, role, audience): a second is an update, not a create.
        live = [
            r
            for r in await list_layer_rows(slug, audience)
            if r.platform == platform and r.role == role
        ]
        if live:
            return err(
                "validation",
                f"{audience.label.capitalize()} for '{slug}' ({platform}/{role}) already exists — id {live[0].id}.",
                "Use kindcomp_update_code or kindcomp_patch_code with target and that component_id.",
            )
        payload: dict[str, Any] = {
            "kind": slug,
            "platform": platform,
            "role": role,
            **audience.fields(),
            "component_key": component_key,
            "source": "db",
            "component_source": (args.get("component_source") or "").strip(),
            "props_transform": (args.get("props_transform") or "").strip() or None,
            "config": args.get("config") or {},
            "is_active": True,
            "organization_id": str(audience.organization_id),
            "created_by": audience.user_id,  # the DB trigger re-stamps it from the session
        }
        if args.get("pinned_kind_version") is not None:
            payload["pinned_kind_version"] = int(args["pinned_kind_version"])
        if (args.get("notes") or "").strip():
            payload["notes"] = args["notes"].strip()
        Layer = get_db_model("KindComponentLayer")
        try:
            async with as_the_person():
                created = await Layer.create_item(**payload)
        except Exception as exc:
            if any(m in str(exc) for m in _RLS_REFUSAL_MARKERS):
                return err(
                    "no_access",
                    f"You cannot make {audience.label} here; nothing was written.",
                    f"The database refused it for this person ({exc}).",
                )
            raise
        return ToolResult(
            success=True,
            output=KindComponentCreateResult(
                component_id=str(created.id),
                kind=slug,
                kind_definition_id="",
                platform=platform,
                role=role,
                component_key=component_key,
                semver=created.semver,
                compile_checked=compile_checked,
                compile_note=(
                    None
                    if compile_checked
                    else "esbuild is not installed on this host — the TSX syntax gate "
                    "was SKIPPED; the code was accepted unverified."
                ),
                message=(
                    f"{audience.label.capitalize()} for '{slug}' created (target {audience.target}). "
                    "It is not the shared view and is never a default. Iterate with "
                    "kindcomp_update_code / kindcomp_patch_code using the same target."
                ),
            ),
        )
    except Exception as e:
        return _fail(e)


async def layer_get_code(args: dict[str, Any], ctx: ToolContext, sections: list[str]) -> ToolResult:
    from matrx_ai.tools.kinds.kind_components import KindComponentCode

    audience, bad = audience_for(args, ctx)
    if bad:
        return bad
    assert audience is not None
    try:
        row, failure = await load_layer(args["component_id"], audience)
        if failure:
            return failure
        return ToolResult(
            success=True,
            output=KindComponentCode(
                component_id=str(row.id),
                kind_definition_id="",
                platform=row.platform,
                role=row.role,
                component_key=row.component_key,
                source=row.source,
                semver=row.semver,
                version=row.version,
                is_default=False,
                is_active=row.is_active,
                config=row.config,
                pinned_kind_version=row.pinned_kind_version,
                sections_returned=sections,
                section_lengths={s: len(getattr(row, s) or "") for s in sections},
                sections={s: getattr(row, s) or "" for s in sections},
            ),
        )
    except Exception as e:
        return _fail(e)


async def load_editable_layer(
    args: dict[str, Any], ctx: ToolContext
) -> tuple[Any | None, ToolResult | None]:
    audience, bad = audience_for(args, ctx)
    if bad:
        return None, bad
    assert audience is not None
    return await load_layer((args.get("component_id") or "").strip(), audience)


async def write_layer(row_id: str, ctx: ToolContext, **values: Any) -> ToolResult | None:
    return await _write(row_id, ctx, **values)


async def reload_layer(row_id: str) -> Any | None:
    Layer = get_db_model("KindComponentLayer")
    async with as_the_person():
        return await Layer.get_or_none(use_cache=False, id=row_id)
