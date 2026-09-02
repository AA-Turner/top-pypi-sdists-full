"""``kindcomp_*`` — agent tools for authoring Content-IR kind COMPONENTS.

The kind-registry sibling of ``tool_component.py`` (the toolcomp_* suite):
where toolcomp_* authors ``tool.ui`` renderers for tool results, kindcomp_*
authors ``content_ir.kind_component`` renderers for ``__kind``-shaped
structured content. A user works with the creator agent, the agent shapes the
user's data into a kind (see ``kind_authoring.py``), then authors a fully
custom component here — the component the user actually sees in chat, docs,
and workflow output.

UNIFICATION ENDGAME: tool results are ``__kind``-bound (the tool_io contract
family published by ``scripts/sync_content_ir_contracts.py``), so kind
components are designed to eventually SUBSUME tool.ui renderers. This toolset
is the successor; ``tool_component.py`` is the ancestor. New rendering
capability lands here first.

Storage model (``content_ir.kind_component``):
- ``source='db'`` + ``component_source`` (the code, TSX) — DB-authored
  components, which is everything this toolset writes. ``source='bundled'``
  rows point at code shipped in the frontend bundle and are NOT editable here.
- ``props_transform`` — optional JS/TS expression module mapping the raw kind
  payload to the component's props.
- ``platform`` × ``role`` × ``component_key`` identify a component within its
  kind; ``is_default`` picks the winner per (platform, role).
- ``semver`` (text) is the human-facing version label — bump it via
  ``bump_version``. The integer ``version`` column is DB-trigger-managed
  (``platform._touch_row``) and must NEVER be app-written; full row history
  snapshots land in ``history.row_versions`` (``_version_capture``) and read
  back through the ``content_ir.kind_component_version`` view.
- Crash reports from live renders land in
  ``content_ir.kind_component_incident`` and surface through
  ``kindcomp_get_context`` until resolved with ``kindcomp_resolve_incident``.

Authorization: see ``kind_shared`` module docstring — every read is gated at
``viewer`` and every write at ``editor`` through the live
``iam.has_access_for`` SECURITY DEFINER function (owner fast-path in code; no
hand-rolled visibility/org semantics). Incident payloads are stricter:
editor-only, because ``data_snapshot`` carries the exact crashing ``__kind``
payload (potentially another user's business data).
"""

from __future__ import annotations

import traceback
from datetime import UTC, datetime
from typing import Any

from matrx_ai.db._registry import get_model as get_db_model
from matrx_ai.tools.implementations.kind_shared import (
    CODE_SECTIONS,
    COMPONENT_DESIGN_DOCTRINE,
    COMPONENT_PLATFORMS,
    COMPONENT_ROLES,
    PLATFORM_COMPONENT_CONTRACTS,
    PROPS_CONTRACT,
    can_access_kind,
    component_import_lint,
    component_source_lint,
    component_summary,
    ctx_user_id,
    ensure_can_edit_kind,
    ensure_can_view_kind,
    err,
    example_summary,
    kind_summary,
    kind_title_key,
    resolve_kind,
    tsx_compile_check,
)
from matrx_ai.tools.implementations.tool_component import (
    _apply_patch,
    _bump_semver_patch,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

KIND_COMPONENT_CREATE_FAILED_KIND = "kind_component_create_failed"


def _optional_ctx_value(ctx: ToolContext, name: str) -> Any | None:
    try:
        return getattr(ctx, name) or None
    except Exception:
        return None


async def _capture_component_create_failure(
    exc: BaseException, *, ctx: ToolContext, kind: str, platform: str, role: str
) -> None:
    """Capture an unexpected create failure without retaining authored source."""
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        exc,
        kind=KIND_COMPONENT_CREATE_FAILED_KIND,
        request_id=_optional_ctx_value(ctx, "request_id"),
        user_id=_optional_ctx_value(ctx, "user_id"),
        conversation_id=_optional_ctx_value(ctx, "conversation_id"),
        route="kindcomp_create_component",
        error_type=type(exc).__name__,
        context={"kind": kind, "platform": platform, "role": role},
    )


async def _refuse_broken_source(source: str) -> tuple[ToolResult | None, bool]:
    """The write-time component gates, in order of cheapness: the props-contract
    lint, the import allowlist, then the esbuild TSX syntax gate. Returns
    ``(refusal, compile_checked)`` — ``compile_checked=False`` means no esbuild
    on this host, which every caller surfaces loudly in its result."""
    lint_refusal = component_source_lint(source)
    if lint_refusal:
        return err("validation", lint_refusal), False
    import_refusal = component_import_lint(source)
    if import_refusal:
        return err("validation", import_refusal), False
    compile_errors, checked = await tsx_compile_check(source)
    if compile_errors:
        return (
            err(
                "validation",
                "Component TSX does not compile — nothing was written. esbuild "
                "errors:\n" + "\n".join(compile_errors),
                "Fix the syntax error(s) and resubmit the corrected source.",
            ),
            checked,
        )
    return None, checked



def _dedup_incidents(rows: list[Any]) -> list[dict[str, Any]]:
    """Collapse incidents with identical signatures (error_type + message +
    stack head) into one entry with occurrence stats — same policy as the
    toolcomp incident dedup."""
    groups: dict[tuple[str, str, str], dict[str, Any]] = {}
    for inc in rows:
        stack = (inc.error_stack or "")[:300]
        key = (inc.error_type or "", inc.error_message or "", stack)
        if key not in groups:
            groups[key] = {
                "id": str(inc.id),
                "component_id": str(inc.component_id) if inc.component_id else None,
                "component_key": inc.component_key,
                "platform": inc.platform,
                "role": inc.role,
                "error_type": inc.error_type,
                "error_message": inc.error_message,
                "error_stack_preview": stack or None,
                "component_semver": inc.component_semver,
                "has_data_snapshot": inc.data_snapshot is not None,
                "occurrences": [],
            }
        if inc.created_at:
            groups[key]["occurrences"].append(inc.created_at.isoformat())
    out = []
    for g in groups.values():
        occs = sorted(g.pop("occurrences"))
        g["first_seen"] = occs[0] if occs else None
        g["last_seen"] = occs[-1] if occs else None
        g["occurrence_count"] = len(occs)
        out.append(g)
    out.sort(key=lambda g: g.get("last_seen") or "", reverse=True)
    return out


async def kindcomp_get_context(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Primary context bundle for working on a kind's UI component.

    Pass ``kind`` (slug or kind_definition_id) OR ``component_id``. Returns:
    the kind definition (schema + fingerprint + version; ``summary.title_key``
    carries the per-kind instance-title field from ``metadata.title_key`` —
    the natural heading for a card-style component), the canonical
    example payload (the exact data shape the component receives), summaries
    of every component on the kind, and open (unresolved) render incidents,
    deduplicated by error signature.

    Access: viewer on the kind for the bundle; the incident section is
    EDITOR-only (incidents_visible=false omits it) — crash data_snapshots can
    contain another user's business data, and only someone who can fix the
    component needs them.

    The result includes ``props_contract`` — READ IT before writing any
    component code: the frontend mounts DB components as
    ``<Component data={value} kind={kind} config={config} />``, so the kind
    instance arrives as ``props.data`` (never flat props), props_transform
    output ALSO lands under ``props.data``, and 'generic_structured' is the
    only routable input-role component key.

    Use this as the FIRST call when creating or fixing any kind component.
    """
    from matrx_ai.tools._generated_declarations import KindcompGetContextArgs

    KindcompGetContextArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    component_id = (args.get("component_id") or "").strip()
    if not kind_ref and not component_id:
        return err(
            "validation",
            "Provide kind (slug or kind_definition_id) or component_id.",
            "Slugs come from kind_create / kind_get; component ids from kindcomp_create_component.",
        )
    try:
        KindComponent = get_db_model("KindComponent")
        KindExample = get_db_model("KindExample")
        KindComponentIncident = get_db_model("KindComponentIncident")

        if component_id and not kind_ref:
            comp = await KindComponent.get_or_none(use_cache=False, id=component_id)
            if comp is None:
                return err("not_found", f"No kind component with id '{component_id}'.")
            kind_ref = str(comp.kind_definition_id)

        kd, failure = await resolve_kind(kind_ref, ctx)
        if failure:
            return failure
        denied = await ensure_can_view_kind(kd, ctx)
        if denied:
            return denied

        comp_rows = await KindComponent.filter(kind_definition_id=str(kd.id)).all()
        comp_rows = [c for c in comp_rows if c.deleted_at is None]
        example_rows = await KindExample.filter(kind_definition_id=str(kd.id)).all()
        example_rows = [e for e in example_rows if e.deleted_at is None]
        canonical = next((e for e in example_rows if e.is_canonical), None)

        # Incidents are EDITOR-gated, stricter than the rest of the bundle:
        # data_snapshot holds the exact __kind payload that crashed a render —
        # potentially another user's business data. Only someone who can fix
        # the component (editor) has any need for crash payloads; a viewer
        # sees the bundle with incidents omitted and incidents_visible=false.
        is_editor = await can_access_kind(kd, ctx, "editor")
        if is_editor:
            incident_rows = await (
                KindComponentIncident.filter(kind_definition_id=str(kd.id), resolved=False)
                .order_by("-created_at")
                .limit(50)
                .all()
            )
            incidents = _dedup_incidents(incident_rows)
        else:
            incidents = []

        from matrx_ai.tools.kinds.kind_authoring import (
            KindComponentSummary,
            KindDefinitionSummary,
            KindExampleSummary,
        )
        from matrx_ai.tools.kinds.kind_components import (
            KindComponentContext,
            KindComponentContextSummary,
            KindComponentIncidentGroup,
        )

        return ToolResult(
            success=True,
            output=KindComponentContext(
                kind=KindDefinitionSummary(**kind_summary(kd)),
                json_schema=kd.emitted_json_schema,
                canonical_example=canonical.data if canonical else None,
                canonical_example_status=canonical.validation_status if canonical else None,
                examples=[KindExampleSummary(**example_summary(e)) for e in example_rows],
                components=[KindComponentSummary(**component_summary(c)) for c in comp_rows],
                component_ids=[str(c.id) for c in comp_rows],
                open_incidents=[KindComponentIncidentGroup(**g) for g in incidents],
                incidents_visible=is_editor,
                props_contract=PROPS_CONTRACT,
                platform_components=PLATFORM_COMPONENT_CONTRACTS,
                design_doctrine=COMPONENT_DESIGN_DOCTRINE,
                summary=KindComponentContextSummary(
                    kind=kd.kind,
                    kind_definition_id=str(kd.id),
                    kind_version=kd.version,
                    is_active=kd.is_active,
                    # Per-kind instance-title override (metadata.title_key) —
                    # the data field a saved instance's title derives from;
                    # components often want the same field as their heading.
                    title_key=kind_title_key(kd),
                    has_canonical_example=canonical is not None,
                    component_count=len(comp_rows),
                    open_incident_types=len(incidents) if is_editor else None,
                ),
            ),
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=str(e),
                traceback=traceback.format_exc(),
                is_retryable=True,
            ),
        )


async def kindcomp_create_component(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Create a new DB-authored render component for a kind.

    PROPS CONTRACT (the #1 failure class — read carefully): the frontend
    mounts DB components as ``<Component data={value} kind={kind}
    config={config} />``. The kind instance arrives as ``props.data`` —
    destructure ``{ data }`` and read every field from it
    (``data.title``, ``data.items.map(...)``). Flat props (``props.title``)
    are NEVER provided; a component reading them renders EMPTY with no error
    and no incident. If you set ``props_transform``, its output ALSO arrives
    as ``props.data`` — it reshapes the value, it does not spread keys into
    props. Sources that never reference ``data`` are refused at write time.

    Required: ``kind`` (slug or kind_definition_id), ``component_key`` (short
    stable identifier, e.g. 'invoice_card'), and ``component_source`` — the
    COMPLETE TSX source. Optional: ``props_transform`` (reshapes the raw kind
    value; result still lands under ``props.data``), ``config``,
    ``pinned_kind_version``, ``platform`` (default 'web'), ``role`` (default
    'output' — never create input-role components; the seeded
    'generic_structured' input row is the only routable input path),
    ``is_default`` (default true — most user kinds have exactly one
    component), ``notes``.

    The row is written with ``source='db'``, scoped to the kind's
    organization, attributed to you. Components are unique per
    (kind, platform, role, component_key) — creating a duplicate fails with a
    pointer to kindcomp_update_code.
    """
    from matrx_ai.tools._generated_declarations import KindcompCreateComponentArgs

    KindcompCreateComponentArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    component_key = (args.get("component_key") or "").strip()
    component_source = (args.get("component_source") or "").strip()
    props_transform = (args.get("props_transform") or "").strip() or None
    config = args.get("config") or {}
    platform = (args.get("platform") or "web").strip()
    role = (args.get("role") or "output").strip()
    pinned_kind_version = args.get("pinned_kind_version")
    is_default = bool(args.get("is_default", True))
    notes = (args.get("notes") or "").strip() or None

    if not kind_ref or not component_key or not component_source:
        return err("validation", "kind, component_key, and component_source are required.")
    if platform not in COMPONENT_PLATFORMS:
        return err("validation", f"Invalid platform '{platform}'. Valid: {list(COMPONENT_PLATFORMS)}")
    if role not in COMPONENT_ROLES:
        return err("validation", f"Invalid role '{role}'. Valid: {list(COMPONENT_ROLES)}")
    refusal, compile_checked = await _refuse_broken_source(component_source)
    if refusal:
        return refusal

    try:
        kd, failure = await resolve_kind(kind_ref, ctx)
        if failure:
            return failure
        denied = await ensure_can_edit_kind(kd, ctx)
        if denied:
            return denied

        KindComponent = get_db_model("KindComponent")
        existing = await KindComponent.filter(
            kind_definition_id=str(kd.id),
            platform=platform,
            role=role,
            component_key=component_key,
        ).all()
        live = [c for c in existing if c.deleted_at is None]
        if live:
            return err(
                "validation",
                f"A component '{component_key}' already exists for kind '{kd.kind}' "
                f"({platform}/{role}) — id {live[0].id}.",
                "Use kindcomp_update_code or kindcomp_patch_code with that component_id.",
            )

        if is_default:
            # The database permits exactly one live default for each
            # kind/platform/role. Creating a new default means replacing the
            # incumbent, not colliding with it after the expensive TSX gates.
            await KindComponent.update_where(
                {
                    "kind_definition_id": str(kd.id),
                    "platform": platform,
                    "role": role,
                    "is_default": True,
                    "deleted_at": None,
                },
                is_default=False,
                updated_by=ctx_user_id(ctx),
            )

        payload: dict[str, Any] = {
            "kind_definition_id": str(kd.id),
            "platform": platform,
            "role": role,
            "component_key": component_key,
            "source": "db",
            "component_source": component_source,
            "props_transform": props_transform,
            "config": config,
            "is_default": is_default,
            "is_active": True,
            "organization_id": str(kd.organization_id),
            "created_by": ctx_user_id(ctx),
        }
        if pinned_kind_version is not None:
            payload["pinned_kind_version"] = int(pinned_kind_version)
        if notes:
            payload["notes"] = notes

        created = await KindComponent.create_item(**payload)
        from matrx_ai.tools.kinds.kind_components import KindComponentCreateResult

        return ToolResult(
            success=True,
            output=KindComponentCreateResult(
                component_id=str(created.id),
                kind=kd.kind,
                kind_definition_id=str(kd.id),
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
                    f"Component '{component_key}' created for kind '{kd.kind}'. "
                    "Iterate with kindcomp_update_code / kindcomp_patch_code."
                ),
            ),
        )
    except Exception as e:
        try:
            await _capture_component_create_failure(
                e, ctx=ctx, kind=kind_ref, platform=platform, role=role
            )
        except Exception:
            # Capture is best-effort and must never replace the tool's real
            # failure contract.
            pass
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def kindcomp_get_code(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Read the full source of a kind component.

    ``sections`` picks which code fields to return: ``component_source``
    (the TSX component) and/or ``props_transform``. Defaults to both.
    Output is one object containing metadata and a ``sections`` map. Reference
    those section names when calling kindcomp_patch_code / kindcomp_update_code.

    Access: viewer on the owning kind (mirrors the RLS SELECT policy on
    kind_component). Missing and unauthorized return the same content-free
    not-found.
    """
    from matrx_ai.tools._generated_declarations import KindcompGetCodeArgs

    KindcompGetCodeArgs.model_validate(args)  # enforce the declared arg contract
    component_id = (args.get("component_id") or "").strip()
    sections = args.get("sections") or list(CODE_SECTIONS)
    if not component_id:
        return err("validation", "component_id is required.",
                   "Get it from kindcomp_get_context.")
    invalid = [s for s in sections if s not in CODE_SECTIONS]
    if invalid:
        return err("validation", f"Invalid sections: {invalid}. Valid: {list(CODE_SECTIONS)}")
    try:
        KindComponent = get_db_model("KindComponent")
        comp = await KindComponent.get_or_none(use_cache=False, id=component_id)
        if comp is None:
            return err("not_found", f"Component '{component_id}' not found.")
        kd, failure = await resolve_kind(str(comp.kind_definition_id), ctx)
        if failure:
            return failure
        denied = await ensure_can_view_kind(kd, ctx)
        if denied:
            return denied

        metadata = {
            "component_id": str(comp.id),
            "kind_definition_id": str(comp.kind_definition_id),
            "platform": comp.platform,
            "role": comp.role,
            "component_key": comp.component_key,
            "source": comp.source,
            "semver": comp.semver,
            "version": comp.version,  # DB-managed integer revision
            "is_default": comp.is_default,
            "is_active": comp.is_active,
            "config": comp.config,
            "pinned_kind_version": comp.pinned_kind_version,
            "sections_returned": sections,
            "section_lengths": {s: len(getattr(comp, s) or "") for s in sections},
        }
        from matrx_ai.tools.kinds.kind_components import KindComponentCode

        return ToolResult(
            success=True,
            output=KindComponentCode(
                **metadata,
                sections={section: getattr(comp, section) or "" for section in sections},
            ),
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def _load_editable_component(
    component_id: str, ctx: ToolContext
) -> tuple[Any | None, Any | None, ToolResult | None]:
    """Fetch component + its kind, enforcing the edit gate and the
    db-source-only rule. Returns (component, kind, error)."""
    KindComponent = get_db_model("KindComponent")
    comp = await KindComponent.get_or_none(use_cache=False, id=component_id)
    if comp is None:
        return None, None, err("not_found", f"Component '{component_id}' not found.")
    kd, failure = await resolve_kind(str(comp.kind_definition_id), ctx)
    if failure:
        return None, None, failure
    denied = await ensure_can_edit_kind(kd, ctx)
    if denied:
        return None, None, denied
    if comp.source != "db":
        return None, None, err(
            "validation",
            f"Component '{component_id}' is source='{comp.source}' — its code ships in the "
            "frontend bundle and cannot be edited here.",
            "Create a db-sourced sibling with kindcomp_create_component instead.",
        )
    return comp, kd, None


async def kindcomp_update_code(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Replace code sections on a kind component.

    ``updates`` maps section name (``component_source`` / ``props_transform``)
    to the COMPLETE replacement code — never partial. ``bump_version``
    advances the human-facing semver; the integer revision auto-increments in
    the DB on every save regardless, and the prior row is snapshotted to
    history automatically.

    PROPS CONTRACT: the component receives the kind instance as ``props.data``
    (``<Component data={value} kind={kind} config={config} />`` — flat props
    are never provided; props_transform output also lands under
    ``props.data``). A component_source that never references ``data`` is
    refused — it would mount as a silent empty render.
    """
    from matrx_ai.tools._generated_declarations import KindcompUpdateCodeArgs

    KindcompUpdateCodeArgs.model_validate(args)  # enforce the declared arg contract
    component_id = (args.get("component_id") or "").strip()
    updates = args.get("updates") or {}
    notes = (args.get("notes") or "").strip() or None
    bump_version = bool(args.get("bump_version", False))
    if not component_id:
        return err("validation", "component_id is required.")
    invalid = [k for k in updates if k not in CODE_SECTIONS]
    if invalid:
        return err(
            "validation",
            f"Invalid update keys: {invalid}. Only code sections allowed: {list(CODE_SECTIONS)}",
            "Use kindcomp_update_settings for non-code fields.",
        )
    if not updates:
        return err("validation", "No code sections provided in updates.")
    compile_checked = True
    if "component_source" in updates:
        refusal, compile_checked = await _refuse_broken_source(
            str(updates["component_source"] or "")
        )
        if refusal:
            return refusal
    try:
        comp, _kd, failure = await _load_editable_component(component_id, ctx)
        if failure:
            return failure
        sections = list(updates.keys())
        if bump_version:
            updates["semver"] = _bump_semver_patch(comp.semver)
        if notes is not None:
            updates["notes"] = notes
        updates["updated_by"] = ctx_user_id(ctx)
        KindComponent = get_db_model("KindComponent")
        rows = await KindComponent.update_where({"id": component_id}, **updates)
        if not rows:
            return err("execution", "Update affected no rows. Check component_id.")
        fresh = await KindComponent.get_or_none(use_cache=False, id=component_id)
        from matrx_ai.tools.kinds.kind_components import KindComponentUpdateResult

        return ToolResult(
            success=True,
            output=KindComponentUpdateResult(
                component_id=component_id,
                updated_sections=sections,
                semver=fresh.semver if fresh else None,
                version=fresh.version if fresh else None,
                compile_checked=compile_checked,
                message=f"Updated {len(sections)} section(s)."
                + (
                    ""
                    if compile_checked
                    else " WARNING: esbuild missing on this host — TSX syntax NOT verified."
                ),
            ),
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def kindcomp_patch_code(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Apply targeted string replacements to one code section without
    rewriting it. Patches apply in order, each on the previous result, with
    three matching rounds of decreasing strictness (exact → whitespace-
    normalized → quote+whitespace-normalized). If any patch fails all rounds
    the WHOLE operation aborts and nothing is written.

    PROPS CONTRACT: the component receives the kind instance as ``props.data``
    (flat props are never provided; props_transform output also lands under
    ``props.data``). If patching would leave component_source with no ``data``
    reference, the whole operation is refused — the silent-empty-render class.
    """
    from matrx_ai.tools._generated_declarations import KindcompPatchCodeArgs

    KindcompPatchCodeArgs.model_validate(args)  # enforce the declared arg contract
    component_id = (args.get("component_id") or "").strip()
    section = (args.get("section") or "component_source").strip()
    patches = args.get("patches") or []
    notes = (args.get("notes") or "").strip() or None
    bump_version = bool(args.get("bump_version", False))
    if not component_id:
        return err("validation", "component_id is required.")
    if section not in CODE_SECTIONS:
        return err("validation", f"Invalid section '{section}'. Valid: {list(CODE_SECTIONS)}")
    if not patches:
        return err("validation", "patches list is empty.")
    for i, p in enumerate(patches):
        if "old_string" not in p and "find" in p:
            p["old_string"] = p["find"]
        if "new_string" not in p and "replace" in p:
            p["new_string"] = p["replace"]
        if "old_string" not in p or "new_string" not in p:
            return err("validation", f"Patch {i} is missing 'old_string' or 'new_string'.")
    try:
        comp, _kd, failure = await _load_editable_component(component_id, ctx)
        if failure:
            return failure
        code = getattr(comp, section) or ""
        if not code:
            return err(
                "validation",
                f"Section '{section}' is empty — nothing to patch.",
                "Write it first with kindcomp_update_code.",
            )
        results: list[dict[str, Any]] = []
        working = code
        for i, patch in enumerate(patches):
            desc = patch.get("description", f"patch {i + 1}")
            try:
                working, round_used = _apply_patch(working, patch["old_string"], patch["new_string"])
                results.append({"index": i, "description": desc, "status": "applied",
                                "match_round": round_used})
            except ValueError as ve:
                return ToolResult(
                    success=False,
                    error=ToolError.from_exception(
                        ve,
                        error_type="patch_no_match",
                        message=f"Patch {i} ('{desc}') failed: {ve}",
                        suggested_action=(
                            "Fetch current code with kindcomp_get_code and make old_string an "
                            "exact contiguous substring."
                        ),
                    ),
                    output={
                        "patches_applied_before_failure": len(results),
                        "failed_patch_index": i,
                        "old_string_preview": patch["old_string"][:300],
                    },
                )
        compile_checked = True
        if section == "component_source":
            refusal, compile_checked = await _refuse_broken_source(working)
            if refusal:
                message = refusal.error.message if refusal.error else "refused"
                return err(
                    "validation",
                    f"Patched result refused — {message}",
                    "Nothing was written. Adjust the patches so the result passes the "
                    "props contract, import allowlist, and TSX syntax gate.",
                )
        payload: dict[str, Any] = {section: working, "updated_by": ctx_user_id(ctx)}
        if bump_version:
            payload["semver"] = _bump_semver_patch(comp.semver)
        if notes:
            payload["notes"] = notes
        KindComponent = get_db_model("KindComponent")
        await KindComponent.update_where({"id": component_id}, **payload)
        fresh = await KindComponent.get_or_none(use_cache=False, id=component_id)
        from matrx_ai.tools.kinds.kind_components import (
            KindComponentPatchOutcome,
            KindComponentPatchResult,
        )

        return ToolResult(
            success=True,
            output=KindComponentPatchResult(
                component_id=component_id,
                section=section,
                patches_applied=len(patches),
                patch_results=[KindComponentPatchOutcome(**r) for r in results],
                semver=fresh.semver if fresh else None,
                version=fresh.version if fresh else None,
                compile_checked=compile_checked,
            ),
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def kindcomp_update_settings(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Update non-code settings on a kind component: ``is_active``,
    ``is_default``, ``sort_order``, ``config``, ``pinned_kind_version``,
    ``component_key``, or ``notes``. Code goes through kindcomp_update_code.
    """
    from matrx_ai.tools._generated_declarations import KindcompUpdateSettingsArgs

    KindcompUpdateSettingsArgs.model_validate(args)  # enforce the declared arg contract
    component_id = (args.get("component_id") or "").strip()
    settings = args.get("settings") or {}
    valid = {"is_active", "is_default", "sort_order", "config", "pinned_kind_version",
             "component_key", "notes"}
    if not component_id:
        return err("validation", "component_id is required.")
    rejected = [k for k in settings if k in CODE_SECTIONS]
    if rejected:
        return err("validation",
                   f"Code fields not allowed here: {rejected}. Use kindcomp_update_code.")
    invalid = [k for k in settings if k not in valid]
    if invalid:
        return err("validation", f"Unknown settings keys: {invalid}. Valid: {sorted(valid)}")
    if not settings:
        return err("validation", "No settings provided.")
    try:
        _comp, _kd, failure = await _load_editable_component(component_id, ctx)
        if failure:
            return failure
        settings["updated_by"] = ctx_user_id(ctx)
        KindComponent = get_db_model("KindComponent")
        rows = await KindComponent.update_where({"id": component_id}, **settings)
        if not rows:
            return err("execution", "Update affected no rows.")
        settings.pop("updated_by", None)
        from matrx_ai.tools.kinds.kind_components import KindComponentUpdateResult

        return ToolResult(
            success=True,
            output=KindComponentUpdateResult(
                component_id=component_id, updated_settings=list(settings.keys())
            ),
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def kindcomp_resolve_incident(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Mark a kind-component render incident as resolved (after fixing the
    component), so it stops appearing in kindcomp_get_context's open list.
    """
    from matrx_ai.tools._generated_declarations import KindcompResolveIncidentArgs

    KindcompResolveIncidentArgs.model_validate(args)  # enforce the declared arg contract
    incident_id = (args.get("incident_id") or "").strip()
    resolution_notes = (args.get("resolution_notes") or "").strip() or None
    if not incident_id:
        return err("validation", "incident_id is required.")
    try:
        KindComponentIncident = get_db_model("KindComponentIncident")
        inc = await KindComponentIncident.get_or_none(use_cache=False, id=incident_id)
        if inc is None:
            return err("not_found", f"Incident '{incident_id}' not found.")
        kd, failure = await resolve_kind(str(inc.kind_definition_id), ctx)
        if failure:
            return failure
        denied = await ensure_can_edit_kind(kd, ctx)
        if denied:
            return denied
        resolved_at = datetime.now(UTC)
        updates: dict[str, Any] = {
            "resolved": True,
            "resolved_at": resolved_at,
            "resolved_by": ctx_user_id(ctx),
        }
        if resolution_notes:
            updates["resolution_notes"] = resolution_notes
        await KindComponentIncident.update_where({"id": incident_id}, **updates)
        from matrx_ai.tools.kinds.kind_components import KindComponentIncidentResolution

        return ToolResult(
            success=True,
            output=KindComponentIncidentResolution(
                incident_id=incident_id,
                resolved=True,
                resolved_at=resolved_at.isoformat(),
                resolution_notes=resolution_notes,
            ),
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )
