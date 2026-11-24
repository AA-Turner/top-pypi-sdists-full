"""``kind_*`` — agent tools for authoring Content-IR KINDS from user data.

The first half of the creator-agent loop (``kindcomp_*`` in
``kind_component.py`` is the second): take the user's actual data, shape it
into a named, versioned kind in ``content_ir.kind_definition``, attach a
validated canonical example, and then teach the platform's agents to emit it
(a ``render_block`` skill in ``skill.definition`` + a prompt content block in
``public.content_blocks``).

Kind lifecycle rules enforced here:
- Slugs are normalized exactly like the contract publisher
  (lowercase, ``[^a-z0-9]+`` → ``_``), unique per organization.
- New kinds are ``is_active=true`` — every kind is born active; switching one
  off is a deliberate act (Arman, 2026-10-13). ``authoring_owner='python'``
  (``data`` stays NULL — the emitted JSON Schema is the contract, and since
  2026-08-29 that is true everywhere: the frontend registry DERIVES a kind's
  field model from ``emitted_json_schema`` and reads ``data`` for nothing.
  See ``fields_from_json_schema`` for what its absence used to cost),
  ``created_by`` = the requesting user, org = the request's active org
  (personal-org backstopped by the DB trigger).
- A canonical example is REQUIRED and validated against the schema BEFORE
  insert; the DB derived-on-write trigger
  (``content_ir.kind_example_recompute_validation``) re-derives
  ``validation_status`` on every write, so status can never drift from data.
- ``kind_update_schema`` re-checks every live example afterward and reports
  stranded ones (the version-bump/example-stranding trap): the
  ``_revalidate_examples`` DB trigger re-runs validation, and this tool reads
  the results back and screams instead of leaving silent red rows.

Authorization (see ``kind_shared``): any user may create kinds in their own
org; every read is gated at ``viewer`` and every schema/example/skill/block
write at ``editor`` through the live ``iam.has_access_for`` SECURITY DEFINER
function (owner fast-path in code) — org membership alone never unlocks a
kind locked to one person. New kinds are therefore created as org platform
data (not published to the web, no ``only_me`` list filter), never locked to
their creator: such a kind was editable only by the one account that created
it, which stranded every other member — including org admins and super
admins — at viewer.

Platform mints: ``kind_create(platform_kind=true)`` is the ONE sanctioned way
a PLATFORM kind is born — admin-gated (``AppContext.is_admin``, refused
loudly otherwise), it stamps the definition and its new children system-org +
``public``; every other row of the composed create inherits the definition's
org, so no manual SQL promotion exists anymore (B6, 2026-08-23). Never
auto-detect platform intent — the flag is always explicit.
"""

from __future__ import annotations

import json
import logging
import re
import traceback
from typing import Any

from matrx_graph.content_ir.sdk import disposition_refusal
from matrx_utils.row_access import is_published, publish_columns
from matrx_utils.text_case import humanize_identifier

from matrx_ai.db._registry import get_model as get_db_model
from matrx_ai.tools.implementations.kind_completeness import kind_completeness
from matrx_ai.tools.implementations.kind_create_plan import KindPlan, KindPlanner, PlannedKind
from matrx_ai.tools.implementations.kind_shared import (
    GENERIC_INPUT_COMPONENT_KEY,
    SHAPE_AUTHORING_POINTER,
    WriteRefused,
    asset_organization_id,
    child_kind_fields_of_schema,
    component_summary,
    ctx_is_admin,
    ctx_org_id,
    ctx_user_id,
    ensure_can_edit_kind,
    ensure_can_view_kind,
    ensure_root_marker,
    enum_str,
    err,
    example_summary,
    fields_from_json_schema,
    infer_schema_from_sample,
    inject_kind_markers_into_schema,
    kind_summary,
    refused,
    resolve_kind,
    schema_fingerprint,
    system_organization_id,
    update_as_the_person,
    validate_against_schema,
    writing_as_the_person,
)
from matrx_ai.tools.implementations.kind_skill_generation import (
    RefreshDecision,
    decide_refresh,
    generated_metadata,
    reach_changes,
    reach_of,
    render_skill_body,
    skill_description,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)


def _wire_output(output: Any) -> Any:
    """A nested tool receipt in JSON wire form (marker included)."""
    from pydantic import BaseModel

    return output.model_dump(mode="json") if isinstance(output, BaseModel) else output


def _exec_error(e: Exception) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="execution", message=str(e), traceback=traceback.format_exc()),
    )


async def _duplicate_shape_refusal(
    fingerprint: str, *, exclude_id: str | None = None
) -> ToolResult | None:
    """Refuse a schema that is byte-identical to an ACTIVE hand-authored kind.

    Two names for one shape is duplication the platform forbids: the frontend's
    fingerprint index (`buildKindFingerprintIndex`) is first-writer-wins, so the
    loser silently displays as the winner, and no agent, tool, or human gets
    told. `keyword_set` and `keyword_variant_set` were minted 32ms apart,
    byte-identical, and nothing objected — found three weeks later by an
    unrelated re-emit tool (FOUND_DEFECTS D164).

    SCOPE THIS EXACTLY AS WRITTEN. Fingerprint collisions are endemic and
    LEGITIMATE among the ~665 machine-minted `is_contract_artifact` snapshots
    (`action_io_*` / `tool_io_*` / `agent_io_*`) — every tool that shares an
    input shape with another collides by construction, and refusing those would
    break the contract publisher. Only `family == "user_authored"` kinds that
    are ACTIVE are catalog items a human picks, and only those may collide.
    An inactive kind is already out of the bindable index, so it cannot shadow
    anything and must not block a mint.

    Since the 2026-08-20 contract-artifact eviction those snapshots no longer
    live in `kind_definition` at all (they moved to `content_ir.io_contract`
    and were soft-deleted here), so the `is_contract_artifact` leg below and
    the `deleted_at` leg above now skip the same rows. Both stay: the flag is
    the stated intent, and a restored or re-minted contract row must never be
    able to block a human's mint.
    """
    if not fingerprint:
        return None
    KindDefinition = get_db_model("KindDefinition")
    for row in await KindDefinition.filter(emitted_fingerprint=fingerprint).all():
        if row.deleted_at is not None or not row.is_active:
            continue
        if getattr(row, "is_contract_artifact", False):
            continue
        if (row.metadata or {}).get("family") != "user_authored":
            continue
        if exclude_id and str(row.id) == exclude_id:
            continue
        return err(
            "validation",
            f"This schema is byte-identical to the active kind '{row.kind}' "
            f"(id {row.id}, fingerprint {fingerprint[:16]}…). Two names for one "
            "shape is banned — the render registry is first-writer-wins, so one "
            "of them would silently display as the other.",
            f"Use kind_get('{row.kind}') and bind to it instead. If this really is "
            "a DIFFERENT concept, the schema has to differ too — a distinct shape "
            "needs distinct fields, not just a distinct name.",
        )
    return None


def _component_authoring_bundle() -> dict[str, Any]:
    """Where the component author's rules are. The rules live ONLY in the
    ``shape-authoring`` skill, attached to every run holding this tool."""
    return {
        "rules": SHAPE_AUTHORING_POINTER,
        "compile_gate": (
            "kindcomp_create_component / update / patch run an esbuild TSX "
            "syntax gate and the import allowlist at write time — a refusal "
            "names the exact error; fix and resubmit."
        ),
    }


_KIND_CREATE_ECHO_BUDGET_CHARS = 20_000


def _bounded_create_echo(
    canonical_example: dict[str, Any], json_schema: dict[str, Any]
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str | None]:
    """Keep a create receipt bounded without cutting structured JSON.

    The caller already supplied both bodies and the durable kind row remains the
    source of truth.  When their combined JSON is large, omit both atomically and
    point the agent at ``kind_get`` so it can deliberately retrieve the persisted
    bodies.  Cutting either dict as text would corrupt its structure.
    """
    import json

    echo_chars = len(json.dumps(canonical_example, default=str)) + len(
        json.dumps(json_schema, default=str)
    )
    if echo_chars <= _KIND_CREATE_ECHO_BUDGET_CHARS:
        return canonical_example, json_schema, None
    return (
        None,
        None,
        "The canonical example and JSON Schema were persisted but omitted from "
        "this bounded receipt. Call kind_get with this kind_definition_id "
        "(include_schema=true) to retrieve them.",
    )


# The kind loading-component library slugs — MIRROR of the frontend source of
# truth (apps/shared/rich-content/src/kinds/react/loading/kind-loading-slugs.ts).
# An unknown slug silently falls back to the generic skeleton at runtime, and
# the frontend shape doctor REDs it (`unknown-loading-component`) — so this
# tool refuses unknown slugs loudly instead of storing a lie. Growing the
# library = new slug there FIRST, then here.
KIND_LOADING_SLUGS: tuple[str, ...] = (
    "card",
    "list",
    "table",
    "timeline",
    "chart",
    "deck",
    "flashcards",
    "quiz",
    "notes",
    "form",
    "media",
    "stat-grid",
    "document",
    "diagram",
    "chat",
    "gallery",
    "kanban",
    "tree",
    "code",
    "map",
    "progress",
    "minimal",
    "generic",
)


async def _create_single_kind(
    *,
    slug: str,
    label: str,
    wire_schema: dict[str, Any],
    block_schema: dict[str, Any],
    canonical_marked: dict[str, Any],
    user_id: str,
    org_id: str | None,
    description: str | None = None,
    title_key: str | None = None,
    loading_component: str | None = None,
    platform: bool = False,
    disposition: str | None = None,
    variant_of: str | None = None,
    new_kind_reason: str | None = None,
) -> tuple[Any | None, Any | None, Any | None, ToolResult | None]:
    """Persist ONE kind row + its marked canonical example + the seeded input
    component. Returns ``(kind_row, example_row, input_component_row, error)``.
    Shared by the root create and recursive child creation so both store the
    same one-shape form.

    ``platform=True`` (admin-gated in ``kind_create`` — never set it from any
    other path) mints a PLATFORM kind: published to the web instead of
    unpublished org data. The caller passes the system org as ``org_id``; every
    downstream row (example, component, edge, skill, content block) inherits
    ``kd.organization_id``, so the whole composed create lands in the system
    org with no manual promotion step.
    """
    fingerprint = schema_fingerprint(wire_schema)
    dup = await _duplicate_shape_refusal(fingerprint)
    if dup:
        return None, None, None, dup

    metadata: dict[str, Any] = {
        "family": "user_authored",
        "generated": False,
        "created_via": "kind_create",
        # KINDS-GLUE wave 1b: what this kind's output IS, stated by the caller. Checked by
        # the ONE validator on the exact metadata written, right before the insert.
        "disposition": disposition,
    }
    if description:
        metadata["description"] = description
    if variant_of and new_kind_reason:
        # A deliberate variant of a live kind carries why it exists, so a later
        # sweep can tell it from an accidental near-duplicate (KindPlanner).
        metadata["variant_of"] = variant_of
        metadata["new_kind_reason"] = new_kind_reason
    if title_key:
        metadata["title_key"] = title_key
    if loading_component:
        # THE ONE LOADING SEQUENCE (2026-08-24): this slug is what renders the
        # instant the kind is identified in a stream, before the component
        # resolves. Validated against KIND_LOADING_SLUGS by kind_create.
        metadata["loading_component"] = loading_component

    form_fields = fields_from_json_schema(wire_schema)

    KindDefinition = get_db_model("KindDefinition")
    payload: dict[str, Any] = {
        "kind": slug,
        "label": label,
        "authoring_owner": "python",
        "data": form_fields,
        "sample_data": canonical_marked,
        # 🚨 BOTH COLUMNS DECLARE `__kind` (Arman, 2026-08-23). There is no
        # marker-free "wire shape" any more: `emitted_json_schema` is what every
        # Python validator reads AND what `response_format_for_kind` binds an
        # agent to, so a marker-free export made a bound producer structurally
        # unable to say what it was emitting. KINDS_EVERYWHERE_PLAN §4.2.
        "emitted_json_schema": block_schema,
        "emitted_block_schema": block_schema,
        "emitted_fingerprint": fingerprint,
        "is_active": True,
        # Org platform data, never one person's private row: locking every
        # agent-created kind to its creator left org admins and super admins
        # at viewer, refused every edit (2026-07-25 incident). Admin platform
        # mints (platform_kind=true) are published to the web in the system
        # org instead — the state the manual SQL promotions used to produce
        # by hand (B6, 2026-08-23). Always written explicitly (T-13).
        **publish_columns(platform, user_id),
        "created_by": user_id,
        "metadata": metadata,
    }
    if not org_id:
        # THE REQUEST CONTEXT IS CARRIED, NEVER REBUILT: a kind definition is
        # org platform data, so it is born in the organization this tool call
        # acts in — read off the carried context by the caller, never omitted.
        # Until 2026-09-17 the key was simply left out of the payload and the
        # database's personal-org backstop stamped the AGENT's owner, so an
        # org's own kinds appeared in one person's private workspace and every
        # admin of that org was refused the edit.
        raise ValueError(
            f"kind_create({slug!r}): this call carries no organization, so the kind "
            "definition has no tenant. A tool call inherits the organization the "
            "boundary admitted; a platform mint names the system organization "
            "explicitly. Fix the caller — nothing here picks a tenant."
        )
    payload["organization_id"] = org_id
    refusal = disposition_refusal(slug, metadata.get("disposition"))
    if refusal:
        return None, None, None, err(
            "validation",
            refusal,
            "Pass disposition (and child_dispositions for each new nested kind) and retry.",
        )
    # content_ir.kind_definition is certified: written AS THE PERSON (RLS +
    # governance decide). The example / input component / edges below are
    # KIND_TABLES_PENDING_CANONICAL_RLS and stay on the privileged connection.
    try:
        async with writing_as_the_person(None):
            kd = await KindDefinition.create_item(**payload)
    except WriteRefused as exc:
        return None, None, None, refused("a new kind in organization", str(org_id), exc)
    try:
        example_fresh, input_component, failure = await _seed_kind_assets(
            kd, slug=slug, canonical_marked=canonical_marked, user_id=user_id
        )
    except Exception:
        # The row is in; a failure after it must not leave a live kind holding the slug.
        await _undo_created([str(kd.id)], user_id)
        raise
    if failure:
        await _undo_created([str(kd.id)], user_id)
        return None, None, None, failure
    return kd, example_fresh, input_component, None


async def _seed_kind_assets(
    kd: Any, *, slug: str, canonical_marked: dict[str, Any], user_id: str
) -> tuple[Any | None, Any | None, ToolResult | None]:
    """The canonical example and the seeded input component of a just-inserted kind."""
    KindExample = get_db_model("KindExample")
    example = await KindExample.create_item(
        kind_definition_id=str(kd.id),
        kind_version=kd.version,
        data=canonical_marked,
        label="Canonical example",
        source="authored",
        is_canonical=True,
        organization_id=str(kd.organization_id),
        created_by=user_id,
    )
    example_fresh = await KindExample.get_or_none(use_cache=False, id=str(example.id))
    example_status = example_fresh.validation_status if example_fresh else "unknown"
    if example_status != "passed":
        # The derived-on-write DB trigger is the authority; disagreement
        # with our pre-check is a platform defect — scream, don't hide it.
        return (
            None,
            None,
            err(
                "execution",
                f"Kind '{slug}' could not be saved (id {kd.id}, now removed): the DB "
                f"validation trigger marked its canonical example '{example_status}' while "
                "the in-process check passed. This is a validator-drift defect — report it.",
            ),
        )

    # Seed the input path: the /shapes Test form routes exclusively
    # through the platform's generic input component.
    KindComponent = get_db_model("KindComponent")
    input_component = await KindComponent.create_item(
        kind_definition_id=str(kd.id),
        platform="web",
        role="input",
        component_key=GENERIC_INPUT_COMPONENT_KEY,
        source="bundled",
        is_default=True,
        is_active=True,
        organization_id=str(kd.organization_id),
        created_by=user_id,
    )
    return example_fresh, input_component, None


async def kind_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Create a new kind (a named, versioned JSON Schema) from the user's data
    — INCLUDING its nested child kinds and their composition edges, in this
    one call.

    Provide ``name`` (becomes the slug, normalized), ``label``, and EITHER:
    - ``json_schema`` — an explicit JSON Schema object, OR
    - ``sample_data`` — a representative payload object; the schema is
      inferred deterministically (fields optional by default — pass
      ``required_fields`` to name the root fields the shape cannot exist
      without; first array element types the array).

    NESTING (the composition doctrine — lists of structured items get their
    own item kind; most shapes are two levels): mark nested kind instances in
    ``sample_data`` with their own ``__kind`` slugs. Every root-level field
    holding a marked object (or a homogeneous list of marked objects) is
    linked as a ``kind_edge``.

    NAMING — ONE CALL, NEVER A PROBE (Arman, 2026-10-31): the caller never
    checks first. Every kind position, innermost first, is resolved by
    ``KindPlanner`` (kind_create_plan.py): an existing kind with the same shape
    (or the requested name, when the example fits it) is REUSED; a name taken
    by a different shape is REFUSED with the field difference — match that
    kind or evolve it with ``kind_update_schema`` (Arman, 2026-11-02: no
    ``<name>_2`` / ``<container>_<name>`` twin is minted beside a named kind).
    ``new_kind_reasons`` ``{name: why it is not that kind}`` is the one door to
    a deliberate variant (container-qualified, then ``_2``…); the reason is
    stored on the new row. Otherwise the kind is created. The receipt leads with
    ``kind`` (the name to use) and ``names`` (every position's final name and
    status). Junk names ("", "unknown", "none", "data_2", …) are refused.
    Every problem is collected before the first write and returned in one
    refusal; ``dry_run`` returns the plan without saving anything.

    ``canonical_example`` is the reference payload stored beside the kind
    (defaults to ``sample_data`` when inferring). It is stored in BLOCK shape
    — ``__kind`` markers at the root and at every nested kind position (the
    one-shape doctrine) — so the stored example IS the render block. It MUST
    validate against the schema — this tool refuses to create a kind whose
    own example fails.

    ``title_key`` (optional) names the ONE data field that holds an
    instance's natural display title, stored as
    ``kind_definition.metadata.title_key``. SET IT whenever the sample has an
    obvious title-ish field that is NOT already in the shared derivation list
    (title/name/label/heading/subject/customer) — e.g. ``wine_name`` for a
    wine-tasting kind — otherwise saved instances of the kind list as
    "Untitled". Must name a schema property; leave unset when a shared key
    already covers it.

    ``loading_component`` (SET IT on every build) names the loading-library
    slug that renders the instant this kind is identified in a live stream,
    before its component resolves — stored as
    ``kind_definition.metadata.loading_component``. Pick the slug whose
    silhouette best matches the finished component (card, list, table,
    timeline, chart, deck, flashcards, quiz, notes, form, media, stat-grid,
    document, diagram, chat, gallery, kanban, tree, code, map, progress,
    minimal, generic). Unknown slugs are refused: an unknown slug would fall
    back to the generic skeleton silently, and the shape doctor flags exactly
    that as a defect. Left unset, the kind renders the generic skeleton and
    the doctor reports the gap.

    Also seeded automatically:
    - The input-role component row (platform='web', role='input',
      component_key='generic_structured') that powers the /shapes Test form.
      'generic_structured' is the ONLY routable input key today — never create
      custom input-role components; the frontend refuses other input keys.
    - When the schema is flat (string/number/boolean/enum/string-array
      fields), a per-field form definition (``kind_definition.data``) so the
      Test tab renders a friendly fielded form instead of a raw JSON textarea.
      Nested shapes keep the JSON fallback; the emitted JSON Schema stays the
      validation source of truth either way (``fielded_form`` in the result
      says which you got).

    The kind is created private in your organization. Next steps
    in the loop: kindcomp_create_component (build the renderer), then
    kind_create_skill + kind_create_content_block (teach agents to emit it).

    ``platform_kind`` (ADMIN-ONLY, default false): mint a PLATFORM kind —
    the definition, its NEW child kinds, and every row the composed create
    writes (examples, edges, seeded input component, and later the
    skill/content block/components, which all inherit the definition's org)
    land in the Matrx System organization published to the web,
    instead of caller-org/unpublished. This replaces the manual SQL promotion
    step every platform build needed. Refused loudly for non-admin callers —
    a personal kind never needs it and never gets it.
    """
    from matrx_ai.tools._generated_declarations import KindCreateArgs

    KindCreateArgs.model_validate(args)  # enforce the declared arg contract
    name = (args.get("name") or "").strip()
    label = (args.get("label") or "").strip()
    json_schema = args.get("json_schema")
    sample_data = args.get("sample_data")
    canonical_example = args.get("canonical_example")
    description = (args.get("description") or "").strip() or None
    title_key = (args.get("title_key") or "").strip() or None
    loading_component = (args.get("loading_component") or "").strip() or None
    required_fields = args.get("required_fields") or None
    platform_kind = bool(args.get("platform_kind", False))
    disposition = args.get("disposition")
    child_dispositions = dict(args.get("child_dispositions") or {})
    dry_run = bool(args.get("dry_run", False))
    field_rules = args.get("field_rules") or None
    new_kind_reasons = args.get("new_kind_reasons") or None

    if loading_component and loading_component not in KIND_LOADING_SLUGS:
        return err(
            "invalid_args",
            f"loading_component '{loading_component}' is not a loading-library "
            f"slug. Valid slugs: {', '.join(KIND_LOADING_SLUGS)}. An unknown "
            "slug would silently render the generic skeleton — pick the "
            "closest real one.",
        )

    if platform_kind and not ctx_is_admin(ctx):
        # Explicit, loud, fail-closed — never silently fall back to a
        # personal mint the admin would then have to hunt down and promote,
        # and never auto-detect platform intent for anyone.
        return err(
            "forbidden",
            "platform_kind=true is an admin action: it mints the kind (and every row "
            "the composed create writes) into the Matrx System organization, published "
            "to the web, so it works only for a platform admin from the "
            "admin app or the admin MCP, never from a normal chat.",
            "Retry without platform_kind to create a normal kind in your own "
            "organization.",
        )

    if not label and not dry_run:
        return err("validation", "label is required.")
    if json_schema is None and sample_data is None and canonical_example is None:
        # Any one of the three is enough: an example alone IS the shape (one-shape doctrine),
        # so the schema is inferred from whichever example was sent.
        return err(
            "validation",
            "Provide json_schema (explicit), or sample_data / canonical_example (the schema is "
            "inferred from it).",
        )
    if json_schema is not None and not isinstance(json_schema, dict):
        return err("validation", "json_schema must be a JSON Schema object.")
    if required_fields is not None and not (
        isinstance(required_fields, list) and all(isinstance(f, str) for f in required_fields)
    ):
        return err("validation", "required_fields must be a list of root field names.")

    try:
        # The marked canonical is the ONE stored shape (block form). It drives
        # child-kind discovery, block-schema derivation, and the stored example.
        if canonical_example is None:
            canonical_example = sample_data
        if canonical_example is None:
            from matrx_graph.contract_kinds import example_from_schema

            canonical_example = example_from_schema(json_schema)
        if not isinstance(canonical_example, dict):
            return err("validation", "canonical_example must be a JSON object.")

        if title_key:
            # Per-kind instance-title override (metadata.title_key — see
            # kind_instance.derive_title + the matrx-frontend mirror): must
            # name a real schema property — a typo here would silently
            # produce "Untitled" instances forever.
            try:
                root_schema = json_schema if json_schema is not None else (
                    infer_schema_from_sample(canonical_example)
                )
            except ValueError:
                root_schema = {}
            properties = root_schema.get("properties")
            if isinstance(properties, dict) and title_key not in properties:
                return err(
                    "validation",
                    f"title_key '{title_key}' is not a property of the schema "
                    f"(known: {sorted(properties)[:20]}).",
                    "Pass the exact data key that holds an instance's display title.",
                )

        # ONE CALL, NEVER A PROBE (Arman, 2026-10-31): every kind in the shape —
        # innermost first — is resolved to the name the caller must use (reused,
        # renamed, or new) and every problem is collected BEFORE the first write.
        # Slugs are global (`kind_definition_global_slug_unique`); a name taken by a
        # different shape is refused with the doors (match / evolve), and forked only
        # on a stated new_kind_reasons entry, which the receipt and the row both carry.
        planner = KindPlanner(
            ctx,
            child_dispositions=child_dispositions,
            platform=platform_kind,
            field_rules=field_rules,
            new_kind_reasons=new_kind_reasons,
        )
        plan = await planner.plan(
            name=name,
            sample=canonical_example,
            json_schema=json_schema,
            required_fields=required_fields,
            disposition=disposition,
        )
        root = plan.root
        if plan.problems or root is None:
            return err(
                "validation",
                "Nothing was saved. Fix "
                + ("this" if len(plan.problems) == 1 else f"these {len(plan.problems)} problems")
                + " and send it once more:\n- "
                + "\n- ".join(plan.problems),
            )
        user_id = ctx_user_id(ctx)
        if not user_id:
            return err("validation", "No authenticated user in context — cannot attribute the kind.")
        # A platform mint targets the system org; created_by stays the real
        # admin caller (honest attribution + the owner fast-path for edits).
        org_id = system_organization_id() if platform_kind else ctx_org_id(ctx)
        names = _name_receipts(plan)
        if dry_run:
            return _plan_receipt(root, names, dry_run=True)
        if not root.writes:
            reused = _plan_receipt(root, names, dry_run=False)
            return await _with_completeness(reused, root.row) if root.row is not None else reused

        written, failure = await _write_plan(
            plan,
            user_id=user_id,
            org_id=org_id,
            platform=platform_kind,
            label=label,
            description=description,
            title_key=title_key,
            loading_component=loading_component,
        )
        if failure:
            return failure
        kd, example, input_component = written[id(root)]
        for receipt in names:
            node_written = written.get(receipt.pop("_node"))
            if node_written:
                receipt["kind_definition_id"] = str(node_written[0].id)

        edges_out: list[dict[str, Any]] = [
            {
                "edge_id": edge_id,
                "field": field,
                "child_kind": child.final,
                "child_kind_id": child_id,
                "is_list": is_list,
                "child_created": child.writes,
            }
            for field, child, is_list, edge_id, child_id in written["_root_edges"]
        ]
        json_schema = root.wire_schema or {}
        canonical_marked = root.marked

        form_fields = fields_from_json_schema(json_schema)
        from matrx_ai.tools.kinds.kind_authoring import (
            ComponentAuthoringBundle,
            KindChildEdge,
            KindCreateResult,
            KindNameResolution,
        )
        from matrx_ai.tools.output_caps import cap_list

        children, children_cap = cap_list(edges_out)
        receipt_example, receipt_schema, retrieval_instruction = _bounded_create_echo(
            canonical_marked, json_schema
        )
        renamed = [n for n in names if n["status"] != "created"]
        # A kind made for a table's rows is three parts — say which are still missing, from the DB.
        completeness = await kind_completeness(kd)
        return ToolResult(
            success=True,
            output=KindCreateResult(
                kind=root.final,
                status=root.status,
                requested_kind=root.requested,
                names=[KindNameResolution(**n) for n in names],
                kind_definition_id=str(kd.id),
                label=label,
                version=kd.version,
                organization_id=str(kd.organization_id),
                published_to_web=bool(getattr(kd, "published_to_web", False)),
                shown_to=enum_str(getattr(kd, "shown_to", None)),
                platform_kind=platform_kind,
                is_active=True,
                canonical_example_id=str(example.id) if example else None,
                canonical_example_status="passed",
                input_component_id=str(input_component.id) if input_component else None,
                input_component_key=GENERIC_INPUT_COMPONENT_KEY,
                canonical_example=receipt_example,
                canonical_example_included=receipt_example is not None,
                children=[KindChildEdge(**e) for e in children],
                fielded_form=form_fields is not None,
                form_field_count=len(form_fields) if form_fields else 0,
                json_schema=receipt_schema,
                json_schema_included=receipt_schema is not None,
                children_total=children_cap.total,
                children_shown=children_cap.shown,
                children_truncated=children_cap.truncated,
                retrieval_instruction=retrieval_instruction,
                component_authoring=ComponentAuthoringBundle(**_component_authoring_bundle()),
                message=(
                    f"Use the kind name '{root.final}'"
                    + (f" (you asked for '{root.requested}')" if root.final != root.requested else "")
                    + f". Created as a {disposition} "
                    + (
                        "(PLATFORM: system org, public)"
                        if platform_kind
                        else "(private)"
                    )
                    + (
                        f" with {len(edges_out)} composed child kind(s)"
                        if edges_out
                        else ""
                    )
                    + (
                        ". Names that differ from what you sent: "
                        + "; ".join(f"{n['path']} → '{n['kind']}' ({n['status']})" for n in renamed)
                        if renamed
                        else ""
                    )
                    + ". The stored canonical example IS the render block (markers "
                    "included). Next: kindcomp_create_component, following the "
                    "shape-authoring skill in your instructions. Then kind_activate "
                    "(it creates the skill and content block automatically).\n"
                    + completeness
                ),
            ),
            output_self_capped=True,
        )
    except Exception as e:
        return _exec_error(e)


async def _with_completeness(result: ToolResult, kd: Any) -> ToolResult:
    """Append the completeness line to a successful kind_create receipt's message."""
    if not result.success or result.output is None:
        return result
    line = await kind_completeness(kd)
    message = getattr(result.output, "message", None)
    output = result.output.model_copy(update={"message": f"{message}\n{line}" if message else line})
    return result.model_copy(update={"output": output})


def _name_receipts(plan: KindPlan) -> list[dict[str, Any]]:
    """One row per kind position, root first: what was asked, the name to use."""
    rows: list[dict[str, Any]] = []
    for node in sorted(plan.every_kind(), key=lambda n: (n.path.count("."), n.path)):
        rows.append(
            {
                "_node": id(node),
                "path": node.path,
                "requested": node.requested,
                "kind": node.final,
                "status": node.status,
                "kind_definition_id": str(node.row.id) if node.row is not None else None,
                "note": node.note,
            }
        )
    return rows


def _plan_receipt(root: PlannedKind, names: list[dict[str, Any]], *, dry_run: bool) -> ToolResult:
    """The receipt when nothing is written: a dry run, or a root that already exists."""
    from matrx_ai.tools.kinds.kind_authoring import KindCreateResult, KindNameResolution

    for receipt in names:
        receipt.pop("_node", None)
    row = root.row
    if dry_run:
        message = (
            f"Dry run — nothing was saved. Calling kind_create without dry_run would "
            f"give the kind the name '{root.final}' ({root.status})"
            + (f" with {len(names) - 1} nested kind(s) resolved as listed" if len(names) > 1 else "")
            + "."
        )
    else:
        message = (
            f"Use the kind name '{root.final}': it already exists with this shape, so "
            "nothing new was created (your label, description and other settings were "
            "not applied). Work on it with kind_get / kind_update_schema / "
            "kindcomp_create_component."
            + (f" {root.note}" if root.note else "")
        )
    return ToolResult(
        success=True,
        output=KindCreateResult(
            kind=root.final,
            status=root.status,
            requested_kind=root.requested,
            names=[KindNameResolution(**n) for n in names],
            dry_run=dry_run,
            kind_definition_id=str(row.id) if row is not None else "",
            label=getattr(row, "label", None) if row is not None else None,
            version=getattr(row, "version", None) if row is not None else None,
            organization_id=str(row.organization_id) if row is not None else None,
            published_to_web=bool(getattr(row, "published_to_web", False)) if row is not None else None,
            shown_to=enum_str(getattr(row, "shown_to", None)) if row is not None else None,
            is_active=bool(getattr(row, "is_active", False)) if row is not None else False,
            canonical_example=None,
            canonical_example_included=False,
            json_schema=None,
            json_schema_included=False,
            retrieval_instruction=(
                f"Call kind_get('{root.final}') for its schema and examples." if row is not None else None
            ),
            message=message,
        ),
        output_self_capped=True,
    )


async def _write_plan(
    plan: KindPlan,
    *,
    user_id: str,
    org_id: str | None,
    platform: bool,
    label: str,
    description: str | None,
    title_key: str | None,
    loading_component: str | None,
) -> tuple[dict[Any, Any], ToolResult | None]:
    """Write every kind the plan creates, innermost first, then its edges.

    The plan already proved every write should succeed. If one fails anyway,
    every kind this call created is soft-deleted before the failure is returned,
    so a refusal never leaves half a composed shape behind."""
    root = plan.root
    assert root is not None
    written: dict[Any, Any] = {}
    created_ids: list[str] = []
    root_edges: list[tuple[str, PlannedKind, bool, str, str]] = []
    KindEdge = get_db_model("KindEdge")
    try:
        for node in plan.every_kind():
            if not node.writes:
                continue
            is_root = node is root
            kd, example, input_component, failure = await _create_single_kind(
                slug=node.final,
                label=label if is_root else humanize_identifier(node.final),
                wire_schema=node.wire_schema or {},
                block_schema=node.block_schema or {},
                canonical_marked=node.marked,
                user_id=user_id,
                org_id=org_id,
                description=description if is_root else None,
                title_key=title_key if is_root else None,
                loading_component=loading_component if is_root else None,
                platform=platform,
                disposition=node.disposition,
                variant_of=node.variant_of,
                new_kind_reason=node.new_kind_reason,
            )
            if failure:
                await _undo_created(created_ids, user_id)
                return {}, failure
            created_ids.append(str(kd.id))
            written[id(node)] = (kd, example, input_component)
            for position, (field, child, is_list) in enumerate(node.children):
                child_id = str(written[id(child)][0].id) if child.writes else str(child.row.id)
                edge = await KindEdge.create_item(
                    parent_definition_id=str(kd.id),
                    field_name=field,
                    child_definition_id=child_id,
                    position=position,
                    organization_id=str(kd.organization_id),
                    created_by=user_id,
                )
                if is_root:
                    root_edges.append((field, child, is_list, str(edge.id), child_id))
    except Exception:
        await _undo_created(created_ids, user_id)
        raise
    written["_root_edges"] = root_edges
    return written, None


async def _undo_created(kind_ids: list[str], user_id: str) -> None:
    """Soft-delete the kinds a failed composed create already wrote."""
    from datetime import UTC, datetime

    KindDefinition = get_db_model("KindDefinition")
    for kind_id in reversed(kind_ids):
        try:
            await update_as_the_person(
                KindDefinition, kind_id, None, deleted_at=datetime.now(UTC), updated_by=user_id
            )
        except Exception as exc:
            from matrx_connect.streaming.error_capture import capture_error

            await capture_error(
                exc,
                kind="kind_create_undo_failed",
                message=f"kind_create could not soft-delete kind {kind_id} after a failed composed create",
                kind_definition_id=kind_id,
            )


async def _org_kinds_named_like(term: str, ctx: ToolContext) -> list[str]:
    """The active organization's own kinds whose name holds ``term`` — so a
    lookup by a plain word ("idea") finds the business's ``post_idea`` instead
    of concluding the business has none (PF-L4, 2026-11-02)."""
    org_id = ctx_org_id(ctx)
    words = [w for w in re.split(r"[^a-z0-9]+", (term or "").lower()) if len(w) >= 3]
    if not org_id or not words:
        return []
    try:
        KindDefinition = get_db_model("KindDefinition")
        rows = await KindDefinition.filter(organization_id=str(org_id)).all()
    except Exception as exc:
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(exc, kind="kind_get_similar_lookup_failed", organization_id=str(org_id))
        return []
    return sorted(
        str(r.kind)
        for r in rows
        if r.deleted_at is None and any(w in str(r.kind).lower() for w in words)
    )[:12]


def _kind_not_found(similar: list[str] | None = None) -> ToolResult:
    from matrx_ai.tools.kinds.kind_authoring import KindDefinitionDetail, KindDefinitionSummary

    note = (
        "No kind you can see has this name or id. To make one, call "
        "kind_create directly — it reuses an existing kind with the same "
        "shape and returns the name to use."
    )
    if similar:
        note = (
            "No kind has exactly this name. This organization's own kinds with a "
            "matching name: " + ", ".join(similar) + " — call kind_get with one of "
            "them before making anything new."
        )
    return ToolResult(
        success=True,
        output=KindDefinitionDetail(found=False, kind=KindDefinitionSummary(), note=note),
    )


async def kind_get(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Fetch a kind's full definition: schema, fingerprint, examples (with
    validation status), components, and detection surfaces. Pass ``kind`` as
    slug or kind_definition_id. Set ``include_schema=false`` to skip the
    (possibly large) schema body.

    Access: viewer on the kind (owner / public / internal+org / explicit
    grant, via the live iam.has_access_for). Missing and unauthorized return
    the same content-free not-found.
    """
    from matrx_ai.tools._generated_declarations import KindGetArgs

    KindGetArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    include_schema = bool(args.get("include_schema", True))
    if not kind_ref:
        return err("validation", "kind (slug or kind_definition_id) is required.")
    try:
        kd, failure = await resolve_kind(kind_ref, ctx)
        if not failure:
            failure = await ensure_can_view_kind(kd, ctx)
        if failure:
            if failure.error is not None and failure.error.error_type == "not_found":
                # "Does it exist?" is a question with an answer, never an error
                # (2026-10-31: Kind Creator runs opened on a FAILED kind_get 32 times
                # in 60 days). Missing and unauthorized stay the same content-free
                # answer, so an unauthorized probe still learns nothing.
                return _kind_not_found(await _org_kinds_named_like(kind_ref, ctx))
            return failure
        KindExample = get_db_model("KindExample")
        KindComponent = get_db_model("KindComponent")
        KindSurface = get_db_model("KindSurface")
        examples = [e for e in await KindExample.filter(kind_definition_id=str(kd.id)).all()
                    if e.deleted_at is None]
        components = [c for c in await KindComponent.filter(kind_definition_id=str(kd.id)).all()
                      if c.deleted_at is None]
        surfaces = [s for s in await KindSurface.filter(kind_definition_id=str(kd.id)).all()
                    if s.deleted_at is None]
        canonical = next((e for e in examples if e.is_canonical), None)
        from matrx_ai.tools.implementations.kind_shared import bound_kind_bodies

        schema_out, example_out, bodies_note = bound_kind_bodies(
            kd.emitted_json_schema if include_schema else None,
            canonical.data if canonical else None,
            ctx=ctx,
            tool_name="kind_get",
        )
        from matrx_ai.tools.kinds.kind_authoring import (
            KindComponentSummary,
            KindDefinitionDetail,
            KindDefinitionSummary,
            KindExampleSummary,
            KindSurfaceSummary,
        )

        return ToolResult(
            success=True,
            output=KindDefinitionDetail(
                kind=KindDefinitionSummary(**kind_summary(kd)),
                canonical_example=example_out,
                examples=[KindExampleSummary(**example_summary(e)) for e in examples],
                components=[KindComponentSummary(**component_summary(c)) for c in components],
                surfaces=[
                    KindSurfaceSummary(
                        id=str(s.id),
                        surface_type=s.surface_type,
                        token=s.token,
                        parser_strategy=s.parser_strategy,
                        is_active=s.is_active,
                    )
                    for s in surfaces
                ],
                json_schema=schema_out,
                note="\n".join(p for p in (await kind_completeness(kd), bodies_note) if p),
            ),
            output_self_capped=True,
        )
    except Exception as e:
        return _exec_error(e)


async def _sync_kind_edges(
    kd: Any, wire_schema: dict[str, Any], block_schema: dict[str, Any], ctx: ToolContext
) -> dict[str, list[str]]:
    """Make the kind's composition ``kind_edge`` rows say what its new schema says.

    A schema that adds (or re-points) an object / array field whose shape is another registered
    kind writes that field's edge in the SAME call — otherwise the field validates but the kind
    catalog, the output store and the renderer never see the child (``person_basics.facts``,
    2026-11-17). A field the schema DROPS retires its live edge (soft delete, the way a retired
    definition retires its edges). A field that merely stops naming a kind keeps its edge: an
    edit that sends no markers must not unwire a composition. A child slug with no live
    definition is reported, never invented — create it with kind_create first."""
    from datetime import UTC, datetime

    KindEdge = get_db_model("KindEdge")
    KindDefinition = get_db_model("KindDefinition")
    parent_id = str(kd.id)
    wanted = {
        **child_kind_fields_of_schema(wire_schema, kd.kind),
        **child_kind_fields_of_schema(block_schema, kd.kind),
    }
    live = [
        e
        for e in await KindEdge.filter(parent_definition_id=parent_id).all()
        if getattr(e, "deleted_at", None) is None
    ]
    by_field = {e.field_name: e for e in live}
    report: dict[str, list[str]] = {"added": [], "repointed": [], "retired": [], "missing_child": []}
    user_id = ctx_user_id(ctx)
    properties = block_schema.get("properties") if isinstance(block_schema, dict) else None
    kept_fields = set(properties) if isinstance(properties, dict) else set()

    async def retire(edge: Any) -> None:
        await update_as_the_person(KindEdge, str(edge.id), ctx, deleted_at=datetime.now(UTC))

    for position, (field, (slug, _is_list)) in enumerate(wanted.items()):
        child = next(
            (r for r in await KindDefinition.filter(kind=slug).all() if r.deleted_at is None), None
        )
        if child is None:
            report["missing_child"].append(f"{field}->{slug}")
            continue
        existing = by_field.get(field)
        if existing is not None and str(existing.child_definition_id) == str(child.id):
            continue
        if existing is not None:
            await retire(existing)
            report["repointed"].append(f"{field}->{slug}")
        else:
            report["added"].append(f"{field}->{slug}")
        await KindEdge.create_item(
            parent_definition_id=parent_id,
            field_name=field,
            child_definition_id=str(child.id),
            position=position,
            organization_id=str(kd.organization_id),
            created_by=user_id,
        )
    for field, edge in by_field.items():
        if field not in kept_fields:
            await retire(edge)
            report["retired"].append(field)
    return report


async def kind_update_schema(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Replace a kind's JSON Schema and surface the consequences.

    The kind's integer version bumps automatically (DB-managed) and the DB
    ``_revalidate_examples`` trigger re-validates every example against the
    new schema. This tool then reads the results back and reports STRANDED
    examples — rows that no longer validate, or that are pinned to an older
    kind_version — so schema evolution never silently breaks the example set.
    Fix stranded examples with kind_add_example (new, conforming) or by
    updating the payloads.

    NOTE: the sibling ``_revalidate_instances`` trigger also synchronously
    revalidates every LIVE saved instance of this kind inside the same
    transaction (unbounded — accepted trade-off at current volume; see the
    kind_instance module docstring). On a kind with a very large instance
    count this call will stall for the full recompute.
    """
    from matrx_ai.tools._generated_declarations import KindUpdateSchemaArgs

    KindUpdateSchemaArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    json_schema = args.get("json_schema")
    change_note = (args.get("change_note") or "").strip() or None
    if not kind_ref:
        return err("validation", "kind (slug or kind_definition_id) is required.")
    if not isinstance(json_schema, dict):
        return err("validation", "json_schema must be a JSON Schema object.")
    try:
        kd, failure = await resolve_kind(kind_ref, ctx)
        if failure:
            return failure
        denied = await ensure_can_edit_kind(kd, ctx)
        if denied:
            return denied

        # Same guard as kind_create — otherwise the refusal is bypassed by
        # minting a distinct shape and then editing it into a duplicate (D164).
        fingerprint = schema_fingerprint(json_schema)
        dup = await _duplicate_shape_refusal(fingerprint, exclude_id=str(kd.id))
        if dup:
            return dup

        KindDefinition = get_db_model("KindDefinition")
        # Re-derive the BLOCK schema alongside the wire schema. The marked
        # canonical example (when present and object-shaped) tells us which
        # nested positions carry markers; without one, only the root marker is
        # declared.
        KindExampleModel = get_db_model("KindExample")
        canonical_row = next(
            (
                e
                for e in await KindExampleModel.filter(
                    kind_definition_id=str(kd.id), is_canonical=True
                ).all()
                if e.deleted_at is None
            ),
            None,
        )
        marker_walk = (
            canonical_row.data
            if canonical_row is not None and isinstance(canonical_row.data, dict)
            else {}
        )
        block_schema = inject_kind_markers_into_schema(json_schema, marker_walk, kd.kind)
        updates: dict[str, Any] = {
            # Both columns declare the marker — see `_create_single_kind`.
            "emitted_json_schema": block_schema,
            "emitted_block_schema": block_schema,
            "emitted_fingerprint": fingerprint,
            "updated_by": ctx_user_id(ctx),
        }
        if change_note:
            updates["metadata"] = {**(kd.metadata or {}), "last_change_note": change_note}
        try:
            await update_as_the_person(KindDefinition, str(kd.id), ctx, **updates)
        except WriteRefused as exc:
            return refused("kind", str(kd.id), exc)
        fresh = await KindDefinition.get_or_none(use_cache=False, id=str(kd.id))
        edge_report = await _sync_kind_edges(kd, json_schema, block_schema, ctx)

        KindExample = get_db_model("KindExample")
        examples = [e for e in await KindExample.filter(kind_definition_id=str(kd.id)).all()
                    if e.deleted_at is None]
        stranded = [
            {
                **example_summary(e),
                "reason": (
                    "failed_validation"
                    if e.validation_status != "passed"
                    else "pinned_to_old_kind_version"
                ),
            }
            for e in examples
            if e.validation_status != "passed" or (fresh and e.kind_version != fresh.version)
        ]
        # Invalidate the in-process kind catalog cache so this process sees
        # the new schema immediately (other processes refresh within the TTL).
        try:
            from matrx_graph.kinds import invalidate_kind_catalog_cache

            from matrx_ai.processing.blocks.kind_catalog import invalidate as invalidate_blocks

            invalidate_kind_catalog_cache()
            # DD-131: the chat block pipeline keeps its OWN sync projection of the registry,
            # because a token-loop detector cannot await a lookup. Dropping only the async
            # cache would leave this process typing the kind against the shape it had BEFORE
            # this edit until the next prime compared versions.
            invalidate_blocks()
        except Exception:
            pass
        from matrx_ai.tools.kinds.kind_authoring import KindSchemaUpdateResult, StrandedExample
        from matrx_ai.tools.surface_write import attach_surface_write

        def _schema_text(schema: Any) -> str:
            return json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True, default=str)

        return attach_surface_write(ToolResult(
            success=True,
            output=KindSchemaUpdateResult(
                kind_definition_id=str(kd.id),
                kind=kd.kind,
                new_version=fresh.version if fresh else None,
                new_fingerprint=updates["emitted_fingerprint"],
                example_count=len(examples),
                stranded_examples=[StrandedExample(**s) for s in stranded],
                warning=" ".join(
                    w
                    for w in (
                        f"{len(stranded)} example(s) are stranded by this schema change — fix "
                        "them before activating the kind."
                        if stranded
                        else "",
                        "Child kind(s) not registered, so no edge was written: "
                        + ", ".join(edge_report["missing_child"])
                        + ". Create them with kind_create, then re-run kind_update_schema."
                        if edge_report["missing_child"]
                        else "",
                    )
                    if w
                )
                or None,
            ),
        ),
            before=_schema_text(kd.emitted_json_schema),
            after=_schema_text(block_schema),
            target_type="kind_definition",
            target_id=str(kd.id),
            target_label=f"{kd.kind} schema",
            mode="structured",
            content_format="json",
        )
    except Exception as e:
        return _exec_error(e)


async def kind_add_example(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Add an example payload to a kind. The payload is validated against the
    current schema BEFORE insert (refused on failure — a knowingly-broken
    example is never written), and the DB trigger re-derives its
    validation_status on write. Set ``is_canonical=true`` to make it the
    reference example (the previous canonical example is demoted).
    """
    from matrx_ai.tools._generated_declarations import KindAddExampleArgs

    KindAddExampleArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    data = args.get("data")
    label = (args.get("label") or "").strip() or None
    description = (args.get("description") or "").strip() or None
    is_canonical = bool(args.get("is_canonical", False))
    if not kind_ref:
        return err("validation", "kind (slug or kind_definition_id) is required.")
    if data is None:
        return err("validation", "data (the example payload) is required.")
    try:
        kd, failure = await resolve_kind(kind_ref, ctx)
        if failure:
            return failure
        denied = await ensure_can_edit_kind(kd, ctx)
        if denied:
            return denied
        # One-shape doctrine: examples are stored in BLOCK form — the root
        # marker set to this kind, nested markers kept. The stored example IS
        # the render block a user pastes or an agent emits.
        if isinstance(data, dict):
            data = ensure_root_marker(data, kd.kind)
        check_schema_obj = (
            kd.emitted_block_schema
            if isinstance(getattr(kd, "emitted_block_schema", None), dict)
            else kd.emitted_json_schema
        )
        if isinstance(check_schema_obj, dict):
            errors = validate_against_schema(data, check_schema_obj)
            if errors:
                return err(
                    "validation",
                    f"Example does not validate against '{kd.kind}' v{kd.version}: {errors[:10]}",
                    "Fix the payload, or evolve the schema first with kind_update_schema.",
                )
        KindExample = get_db_model("KindExample")
        if is_canonical:
            existing = [e for e in await KindExample.filter(
                kind_definition_id=str(kd.id), is_canonical=True).all() if e.deleted_at is None]
            for old in existing:
                await KindExample.update_where({"id": str(old.id)}, is_canonical=False)
        created = await KindExample.create_item(
            kind_definition_id=str(kd.id),
            kind_version=kd.version,
            data=data,
            label=label or ("Canonical example" if is_canonical else "Example"),
            description=description,
            source="authored",
            is_canonical=is_canonical,
            organization_id=str(kd.organization_id),
            created_by=ctx_user_id(ctx),
        )
        fresh = await KindExample.get_or_none(use_cache=False, id=str(created.id))
        from matrx_ai.tools.kinds.kind_authoring import KindExampleResult

        return ToolResult(
            success=True,
            output=KindExampleResult(
                example_id=str(created.id),
                kind=kd.kind,
                kind_version=kd.version,
                is_canonical=is_canonical,
                validation_status=fresh.validation_status if fresh else "unknown",
            ),
        )
    except Exception as e:
        return _exec_error(e)


# ---------------------------------------------------------------------------
# Skill + content-block authoring (teach agents to EMIT the kind)
# ---------------------------------------------------------------------------


def _default_skill_body(kd: Any, canonical_example: Any, extra_guidance: str | None) -> str:
    """House-format render_block skill body — see kind_skill_generation."""
    return render_skill_body(kd, canonical_example, extra_guidance)


async def _render_block_category_id() -> str | None:
    """Resolve the render-block skill category by looking at how the shipped
    kind_* skills are categorized (never hardcode the category UUID)."""
    SklDefinition = get_db_model("SklDefinition")
    rows = await SklDefinition.filter(skill_type="render_block").limit(5).all()
    for row in rows:
        if row.category_id:
            return str(row.category_id)
    return None


async def _content_block_category_id() -> str | None:
    """Resolve the `platform.categories` id for the content-block palette the
    user's context menu shows (the "Agent Skills" content-block category).

    This is a DIFFERENT category system from `_render_block_category_id` above
    (that one is a skl category on `skill.definition`; this is a
    `platform.categories` row referenced by `agent.prompt_block`). Resolved
    by name + placement so no UUID is hardcoded; falls back to any content-block
    placement category so the block always lands somewhere the menu renders,
    never uncategorized (the invisible-block bug)."""
    # The package manifest exposes platform.categories under the namespaced
    # skill key.  Asking for the host model's concrete class name bypasses the
    # injection contract and fails in deployed hosts with DBNotConfiguredError.
    Categories = get_db_model("SklCategories")
    rows = await Categories.filter(placement_type="content-block").limit(100).all()
    live = [r for r in rows if getattr(r, "deleted_at", None) is None]
    for r in live:
        if (r.name or "").strip().lower() == "agent skills":
            return str(r.id)
    return str(live[0].id) if live else None


async def create_generated_skill(
    kd: Any,
    canonical_data: Any,
    *,
    extra_guidance: str | None,
    body_override: str | None,
    created_by: str | None,
    ctx: ToolContext | None,
    system_job: bool = False,
) -> tuple[Any, str]:
    """Write the generated ``kind_<slug>`` skill for a shape. The ONE write path for
    kind_create_skill, activation auto-create and the weekly refresh. Raises WriteRefused."""
    body = body_override or render_skill_body(kd, canonical_data, extra_guidance)
    description = skill_description(kd)
    SklDefinition = get_db_model("SklDefinition")
    asset_org = asset_organization_id(kd, ctx, system_job=system_job)
    async with writing_as_the_person(ctx, system_job=system_job):
        created = await SklDefinition.create_item(
            skill_id=f"kind_{kd.kind}",
            label=f"{kd.label} (structured)",
            description=description,
            skill_type="render_block",
            body=body,
            icon_name="Shapes",
            category_id=await _render_block_category_id(),
            is_active=True,
            organization_id=asset_org,
            created_by=created_by,
            **{k: v for k, v in reach_of(kd, system_organization_id(), asset_org).items() if v is not None},
            metadata={
                **generated_metadata(
                    kd,
                    body,
                    extra_guidance=extra_guidance,
                    body_override=bool(body_override),
                    description=description,
                ),
                # A generated shape skill is found by search; it never moves the cached
                # "You have access to N skills" preamble line (providers.counts_in_overview).
                "in_skill_overview": False,
            },
        )
    return created, body


async def refresh_generated_skill(
    existing: Any, kd: Any, canonical_data: Any, ctx: ToolContext | None, *, system_job: bool = False
) -> tuple[RefreshDecision, list[str]]:
    """Apply the regeneration rule to one existing skill. Body/description only when the rule
    allows; REACH (mirror of the shape's) and the ``kind_definition_id`` link are synced for
    every skill that is ours or curated -- neither is body content. One write per skill."""
    decision = decide_refresh(existing, kd, canonical_data)
    values: dict[str, Any] = {}
    synced: list[str] = []
    meta = dict(decision.metadata or existing.metadata or {})
    if decision.action in ("regenerate", "stamp"):
        values.update(body=decision.body, description=decision.description)
    reach = reach_changes(existing, kd, system_organization_id())
    if reach:
        values.update(reach)
        synced.append("reach")
    if not meta.get("kind_definition_id"):
        meta["kind_definition_id"] = str(kd.id)
        synced.append("link")
    if decision.metadata or "link" in synced:
        values["metadata"] = meta
    if values:
        await update_as_the_person(
            get_db_model("SklDefinition"), str(existing.id), ctx, system_job=system_job, **values
        )
    return decision, synced


async def kind_create_skill(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Create the agent skill that teaches platform agents to emit this kind.

    Writes a ``render_block`` skill (``skill.definition``) with skill_id
    ``kind_<slug>`` in the kind's organization, following the shipped kind_*
    skill house format. ``body`` overrides the generated body; ``extra_guidance``
    appends domain rules to the generated one. Requires a canonical example.
    """
    from matrx_ai.tools._generated_declarations import KindCreateSkillArgs

    KindCreateSkillArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    body_override = (args.get("body") or "").strip() or None
    extra_guidance = (args.get("extra_guidance") or "").strip() or None
    if not kind_ref:
        return err("validation", "kind (slug or kind_definition_id) is required.")
    try:
        kd, failure = await resolve_kind(kind_ref, ctx)
        if failure:
            return failure
        denied = await ensure_can_edit_kind(kd, ctx)
        if denied:
            return denied

        KindExample = get_db_model("KindExample")
        canonical = next(
            (e for e in await KindExample.filter(
                kind_definition_id=str(kd.id), is_canonical=True).all()
             if e.deleted_at is None),
            None,
        )
        if canonical is None and body_override is None:
            return err(
                "validation",
                f"Kind '{kd.kind}' has no canonical example — the generated skill body "
                "is built around it.",
                "Add one with kind_add_example(is_canonical=true) first, or pass body.",
            )

        skill_id = f"kind_{kd.kind}"
        SklDefinition = get_db_model("SklDefinition")
        homes = {str(kd.organization_id), str(asset_organization_id(kd, ctx))}
        existing = [s for s in await SklDefinition.filter(skill_id=skill_id).all()
                    if s.deleted_at is None and str(s.organization_id) in homes]
        if existing:
            return err(
                "validation",
                f"Skill '{skill_id}' already exists in this organization (id {existing[0].id}).",
                "Edit the existing skill instead of creating a duplicate.",
            )

        try:
            created, body = await create_generated_skill(
                kd,
                canonical.data if canonical else None,
                extra_guidance=extra_guidance,
                body_override=body_override,
                created_by=ctx_user_id(ctx),
                ctx=ctx,
            )
        except WriteRefused as exc:
            return refused("the skill for kind", str(kd.id), exc)
        from matrx_ai.tools.kinds.kind_authoring import KindSkillResult

        return ToolResult(
            success=True,
            output=KindSkillResult(
                skill_definition_id=str(created.id),
                skill_id=skill_id,
                kind=kd.kind,
                body_chars=len(body),
                message=f"Skill '{skill_id}' created — agents can now learn to emit this kind.",
            ),
        )
    except Exception as e:
        return _exec_error(e)


async def kind_create_content_block(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Create the render block for this kind — the reusable palette item
    (``agent.prompt_block``, block_type ``render_kind``) that shows up in the user's content-block /
    render-block context menu and drops the emit template into a prompt.
    ``template`` overrides the generated one. Requires a canonical example
    unless template is provided.

    Writes to ``agent.prompt_block`` — the table the live context menu
    (``agent.context_menu_view``) reads since aidream migration 1471.
    """
    from matrx_ai.tools._generated_declarations import KindCreateContentBlockArgs

    KindCreateContentBlockArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    template_override = (args.get("template") or "").strip() or None
    label = (args.get("label") or "").strip() or None
    if not kind_ref:
        return err("validation", "kind (slug or kind_definition_id) is required.")
    try:
        kd, failure = await resolve_kind(kind_ref, ctx)
        if failure:
            return failure
        denied = await ensure_can_edit_kind(kd, ctx)
        if denied:
            return denied

        KindExample = get_db_model("KindExample")
        canonical = next(
            (e for e in await KindExample.filter(
                kind_definition_id=str(kd.id), is_canonical=True).all()
             if e.deleted_at is None),
            None,
        )
        if canonical is None and template_override is None:
            return err(
                "validation",
                f"Kind '{kd.kind}' has no canonical example to build the template around.",
                "Add one with kind_add_example(is_canonical=true) first, or pass template.",
            )

        block_id = f"kind-{kd.kind.replace('_', '-')}"
        PromptBlock = get_db_model("PromptBlock")
        homes = {str(kd.organization_id), str(asset_organization_id(kd, ctx))}
        existing = [b for b in await PromptBlock.filter(name=block_id).all()
                    if b.deleted_at is None and str(b.organization_id) in homes]
        if existing:
            return err(
                "validation",
                f"Render block '{block_id}' already exists in this organization "
                f"(id {existing[0].id}).",
                "Edit the existing block instead of creating a duplicate.",
            )

        if template_override:
            template = template_override
        else:
            example_obj = {"__kind": kd.kind}
            if isinstance(canonical.data, dict):
                example_obj.update(canonical.data)
            template = (
                f"When the answer is a {kd.label.lower()}, emit it as a structured "
                f"render block — a single JSON object the platform renders live:\n\n"
                f"```json\n{json.dumps(example_obj, indent=2, ensure_ascii=False)}\n```\n\n"
                f"Rules:\n"
                f'- `"__kind"` is always the literal `"{kd.kind}"`, first key in the object.\n'
                f"- Match the kind's schema exactly; include every required field.\n"
                f"- Valid JSON only; emit the complete object, one per instance."
            )

        # agent.prompt_block is certified: written AS THE PERSON (RLS decides).
        # metadata is system-owned on this table (client keys are refused), so the
        # kind link lives in the name (kind-<slug>) and block_type 'render_kind'.
        try:
            async with writing_as_the_person(ctx):
                created = await PromptBlock.create_item(
                    name=block_id,
                    label=label or kd.label,
                    description=f"Render block teaching an agent to emit the {kd.kind} kind.",
                    icon_name="Shapes",
                    content=template,
                    block_type="render_kind",
                    category_id=await _content_block_category_id(),
                    organization_id=asset_organization_id(kd, ctx),
                    created_by=ctx_user_id(ctx),
                    # The block follows its kind's web lane and list filter. Enums are
                    # serialized by VALUE — str(member) on a (str, Enum) mixin yields the
                    # repr, which the EnumField rejects (this killed every wave-4 write).
                    **publish_columns(is_published(kd), ctx_user_id(ctx)),
                    **({"shown_to": enum_str(kd.shown_to)} if getattr(kd, "shown_to", None) else {}),
                )
        except WriteRefused as exc:
            return refused("the content block for kind", str(kd.id), exc)
        from matrx_ai.tools.kinds.kind_authoring import KindContentBlockResult

        return ToolResult(
            success=True,
            output=KindContentBlockResult(
                prompt_block_id=str(created.id),
                block_id=block_id,
                kind=kd.kind,
                template_chars=len(template),
                message=f"Render block '{block_id}' created — it now appears in the content-block menu.",
            ),
        )
    except Exception as e:
        return _exec_error(e)


async def kind_activate(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Run the dual gate and flip a kind's ``is_active``.

    This is the step that turns an authored kind into a LIVE one. Until it
    runs, a kind renders through the generic JSON viewer and cannot be bound
    to an agent's structured output — ``is_active`` is what
    ``isKindBindable`` (frontend) gates agent binding on.

    The gate is NOT re-implemented here. ``content_ir.evaluate_kind_activation``
    is the single authority and this tool calls it, so the browser, this tool,
    and any future surface can never disagree about what "activatable" means.
    Its two legs:

      structural — a canonical ``kind_example`` whose ``validation_status`` is
                   ``passed``. That verdict is DERIVED by a DB trigger, so a
                   fabricated pass is impossible.
      render     — an active ``role='output'`` ``kind_component`` row. Covers
                   compiled (``source='bundled'``) and agent-authored
                   (``source='db'``) components identically. Structurally n/a
                   for generated data-only contract families.

    On refusal the gate's own reasons come back verbatim — they name the
    missing asset, so the agent can go create it and retry rather than guess.

    ``active=false`` deactivates and is NEVER gated: a kind whose component has
    started failing must always be switchable off.

    Access: editor on the kind (same gate as every other kind_* write).
    """
    from matrx_ai.tools._generated_declarations import KindActivateArgs

    KindActivateArgs.model_validate(args)  # enforce the declared arg contract
    kind_ref = (args.get("kind") or "").strip()
    active = bool(args.get("active", True))
    note = (args.get("note") or "").strip() or None
    if not kind_ref:
        return err("validation", "kind (slug or kind_definition_id) is required.")
    try:
        kd, failure = await resolve_kind(kind_ref, ctx)
        if failure:
            return failure
        denied = await ensure_can_edit_kind(kd, ctx)
        if denied:
            return denied

        KindDefinition = get_db_model("KindDefinition")
        was_active = bool(kd.is_active)
        verdict: dict[str, Any] | None = None

        # `is_active` is a DB-gated column: a direct UPDATE is rejected by a
        # trigger. `content_ir.set_kind_activation` is the ONE authority — it
        # runs the dual gate (evaluate_kind_activation) and performs the gated
        # write in a single SECURITY DEFINER routine, so this tool, the browser,
        # and any future surface can never disagree about what "activate" means.
        # We pass p_actor because auth.uid() is null in server tool context;
        # a browser caller's auth.uid() always wins, so p_actor cannot spoof.
        #
        # Its authorization is the SAME `iam.has_access_for(...,'editor')` this
        # tool already checked (migration 0486). It used to be a bespoke
        # creator-only rule, which made every kind in the Matrx System org
        # unactivatable by the very agents that author them: editor everywhere
        # else, refused on the one boolean that ships the work. If activation
        # ever refuses a caller this tool just cleared, that divergence is the
        # bug — never work around it by widening the tool.
        from contextlib import nullcontext

        from matrx_orm import admin_lane, call_function

        # THE ADMIN LANE (2026-09-25): the gate's super-admin arm answers only in
        # the lane, which opens only for a run started from an admin surface.
        lane = (
            admin_lane(database=KindDefinition._database)
            if ctx_is_admin(ctx)
            else nullcontext()
        )
        # content_ir.set_kind_activation never refuses on the dual gate any more: it activates
        # and returns the gate's missing-asset reasons as `warnings` in its verdict (read below).
        # The old branch matched the words "failed the dual gate", which no live function raises.
        async with lane:
            raw = await call_function(
                KindDefinition._database,
                "content_ir",
                "set_kind_activation",
                str(kd.id),
                active,
                note,
                ctx_user_id(ctx),
                mode="scalar",
            )
        verdict = json.loads(raw) if isinstance(raw, str) else raw

        # The catalog caches `is_active`; without this the kind stays invisible
        # to response_format_for_kind and node binding until the TTL lapses.
        try:
            from matrx_graph.kinds import invalidate_kind_catalog_cache

            from matrx_ai.processing.blocks.kind_catalog import invalidate as invalidate_blocks

            invalidate_kind_catalog_cache()
            # DD-131: the chat block pipeline keeps its OWN sync projection of the registry,
            # because a token-loop detector cannot await a lookup. Dropping only the async
            # cache would leave this process typing the kind against the shape it had BEFORE
            # this edit until the next prime compared versions.
            invalidate_blocks()
        except Exception:
            logger.warning("kind catalog cache invalidation failed after activation", exc_info=True)

        # Activation auto-creates the teach-the-platform assets. They are
        # deterministic templates over the canonical example (which the
        # structural gate just proved exists and passes), so there is no
        # LLM judgment in them — no reason to spend two extra tool calls.
        # kind_create_skill / kind_create_content_block remain for overrides.
        auto_assets: dict[str, Any] = {}
        if active:
            try:
                SklDefinition = get_db_model("SklDefinition")
                homes = {str(kd.organization_id), str(asset_organization_id(kd, ctx))}
                skill_exists = any(
                    s.deleted_at is None
                    and str(s.organization_id) in homes
                    for s in await SklDefinition.filter(skill_id=f"kind_{kd.kind}").all()
                )
                if not skill_exists:
                    skill_res = await kind_create_skill({"kind": str(kd.id)}, ctx)
                    auto_assets["skill"] = (
                        _wire_output(skill_res.output)
                        if skill_res.success
                        else {"error": skill_res.error.message if skill_res.error else "failed"}
                    )
                PromptBlock = get_db_model("PromptBlock")
                block_id = f"kind-{kd.kind.replace('_', '-')}"
                block_exists = any(
                    b.deleted_at is None
                    and str(b.organization_id) in homes
                    for b in await PromptBlock.filter(name=block_id).all()
                )
                if not block_exists:
                    block_res = await kind_create_content_block({"kind": str(kd.id)}, ctx)
                    auto_assets["content_block"] = (
                        _wire_output(block_res.output)
                        if block_res.success
                        else {"error": block_res.error.message if block_res.error else "failed"}
                    )
            except Exception:
                logger.warning(
                    "auto skill/content-block creation failed after activating %s",
                    kd.kind,
                    exc_info=True,
                )
                auto_assets["error"] = (
                    "auto asset creation failed — create manually with "
                    "kind_create_skill / kind_create_content_block"
                )

        from matrx_ai.tools.kinds.kind_authoring import KindActivationResult

        return ToolResult(
            success=True,
            output=KindActivationResult(
                kind_definition_id=str(kd.id),
                kind=kd.kind,
                is_active=active,
                was_active=was_active,
                gated=active,
                verdict=verdict,
                auto_assets=auto_assets or None,
                note=(
                    None
                    if not active
                    else "Kind is live: it renders through its component and can now be bound "
                    "to an agent's structured output."
                ),
            ),
        )
    except Exception as e:
        return _exec_error(e)
