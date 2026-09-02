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
- New kinds are ``is_active=false`` (the dual-gate: activation is a frontend
  decision once a component exists), ``authoring_owner='python'``
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
``visibility='personal'`` kind. New kinds are therefore created ``internal``
(org platform data), NOT ``personal``: a personal kind is editable only by the
one account that created it, which strands every other member — including org
admins and super admins — at viewer.

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
import traceback
from typing import Any

from matrx_ai.db._registry import get_model as get_db_model
from matrx_ai.tools.implementations.kind_shared import (
    COMPONENT_ALLOWED_IMPORTS,
    COMPONENT_DESIGN_DOCTRINE,
    GENERIC_INPUT_COMPONENT_KEY,
    PLATFORM_COMPONENT_CONTRACTS,
    PROPS_CONTRACT,
    RESERVED_KIND_SLUGS,
    collect_child_kind_fields,
    component_summary,
    ctx_is_admin,
    ctx_org_id,
    ctx_user_id,
    ensure_can_edit_kind,
    ensure_can_view_kind,
    ensure_root_marker,
    err,
    example_summary,
    fields_from_json_schema,
    infer_schema_from_sample,
    inject_kind_markers_into_schema,
    kind_summary,
    normalize_kind_slug,
    resolve_kind,
    schema_fingerprint,
    system_organization_id,
    validate_against_schema,
    validate_kind_slug_format,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)


def _visibility_value(vis: Any, default: str = "internal") -> str:
    """The plain string value of a visibility that may be an Enum member, a
    string, or None. str(member) on a (str, Enum) mixin yields the repr
    'Visibility.INTERNAL' — never use it for serialization."""
    if vis is None:
        return default
    return str(getattr(vis, "value", vis)) or default


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
    are ACTIVE are catalogue items a human picks, and only those may collide.
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
    """Everything the component author needs, returned by kind_create itself so
    a fresh build never needs a kindcomp_get_context round-trip (that call
    remains for FIXING existing components, where live rows/incidents matter).
    """
    return {
        "props_contract": PROPS_CONTRACT,
        "platform_components": PLATFORM_COMPONENT_CONTRACTS,
        "allowed_imports": sorted(COMPONENT_ALLOWED_IMPORTS),
        "design_doctrine": COMPONENT_DESIGN_DOCTRINE,
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


_MAX_CHILD_DEPTH = 3

# The kind loading-component library slugs — MIRROR of the frontend source of
# truth (matrx-frontend features/content-ir/react/loading/kind-loading-slugs.ts).
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
) -> tuple[Any | None, Any | None, Any | None, ToolResult | None]:
    """Persist ONE kind row + its marked canonical example + the seeded input
    component. Returns ``(kind_row, example_row, input_component_row, error)``.
    Shared by the root create and recursive child creation so both store the
    same one-shape form.

    ``platform=True`` (admin-gated in ``kind_create`` — never set it from any
    other path) mints a PLATFORM kind: ``visibility='public'`` instead of
    ``'internal'``. The caller passes the system org as ``org_id``; every
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
    }
    if description:
        metadata["description"] = description
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
        "is_active": False,
        # 'internal', never 'personal': a kind definition is org platform
        # data, not one person's private row. 'personal' locked every
        # agent-created kind to its creator — org admins and super admins
        # got viewer and were refused every edit (2026-07-25 incident).
        # Admin platform mints (platform_kind=true) are 'public' in the
        # system org instead — the state the manual SQL promotions used to
        # produce by hand (B6, 2026-08-23).
        "visibility": "public" if platform else "internal",
        "created_by": user_id,
        "metadata": metadata,
    }
    if org_id:
        payload["organization_id"] = org_id
    kd = await KindDefinition.create_item(**payload)

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
            None,
            err(
                "execution",
                f"Kind '{slug}' was created (id {kd.id}) but the DB validation trigger "
                f"marked its canonical example '{example_status}' while the in-process "
                "check passed. This is a validator-drift defect — report it.",
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
    return kd, example_fresh, input_component, None


async def _resolve_or_create_child(
    *,
    slug: str,
    sample: dict[str, Any],
    user_id: str,
    org_id: str | None,
    ctx: ToolContext,
    depth: int,
    platform: bool = False,
) -> tuple[Any | None, bool, ToolResult | None]:
    """Resolve a nested child kind by slug, or create it from its marked
    sample (recursively — a child's own marked children become ITS edges).
    ``platform`` cascades verbatim from the root create, so a platform mint's
    NEW children land system-org/public too (an existing child is reused
    as-is, wherever it lives). Returns ``(kind_row, created, error)``.

    An existing child is validated against the nested sample so composition
    can never silently disagree with the child's real schema."""
    if depth > _MAX_CHILD_DEPTH:
        return None, False, err(
            "validation",
            f"Nested kind '{slug}' exceeds the composition depth cap "
            f"({_MAX_CHILD_DEPTH} levels). Flatten the shape or build the deep "
            "branch as its own kind first.",
        )

    KindDefinition = get_db_model("KindDefinition")
    existing = [
        r for r in await KindDefinition.filter(kind=slug).all() if r.deleted_at is None
    ]
    if existing:
        child = existing[0]
        denied = await ensure_can_view_kind(child, ctx)
        if denied:
            return None, False, err(
                "validation",
                f"Nested kind '{slug}' exists but is not accessible to you — "
                "composition requires at least viewer access to the child.",
                "Use a slug you own, or ask the child's owner to share it.",
            )
        if isinstance(child.emitted_json_schema, dict):
            errors = validate_against_schema(sample, child.emitted_json_schema)
            if errors:
                return None, False, err(
                    "validation",
                    f"Nested '{slug}' instance in your sample does not validate "
                    f"against the existing kind '{slug}' v{child.version}: "
                    f"{errors[:6]}",
                    "Match the existing child kind's schema exactly, or mark the "
                    "nested object with a new slug to mint a different child kind.",
                )
        return child, False, None

    marked = ensure_root_marker(sample, slug)
    grandchildren = collect_child_kind_fields(marked, slug)
    child_edges: list[tuple[str, Any, bool]] = []
    for field, info in grandchildren.items():
        gc, _created, failure = await _resolve_or_create_child(
            slug=info["slug"],
            sample=info["sample"],
            user_id=user_id,
            org_id=org_id,
            ctx=ctx,
            depth=depth + 1,
            platform=platform,
        )
        if failure:
            return None, False, failure
        child_edges.append((field, gc, info["is_list"]))

    wire_schema = infer_schema_from_sample(marked)
    block_schema = inject_kind_markers_into_schema(wire_schema, marked, slug)
    label = slug.replace("_", " ").title()
    kd, _example, _input_component, failure = await _create_single_kind(
        slug=slug,
        label=label,
        wire_schema=wire_schema,
        block_schema=block_schema,
        canonical_marked=marked,
        user_id=user_id,
        org_id=org_id,
        platform=platform,
    )
    if failure:
        return None, False, failure

    KindEdge = get_db_model("KindEdge")
    for position, (field, gc, _is_list) in enumerate(child_edges):
        await KindEdge.create_item(
            parent_definition_id=str(kd.id),
            field_name=field,
            child_definition_id=str(gc.id),
            position=position,
            organization_id=str(kd.organization_id),
            created_by=user_id,
        )
    return kd, True, None


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
    linked as a ``kind_edge``; an unknown child slug is CREATED from its
    nested sample (recursively), an existing one is validated and reused.

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

    The kind is created inactive and private in your organization. Next steps
    in the loop: kindcomp_create_component (build the renderer), then
    kind_create_skill + kind_create_content_block (teach agents to emit it).

    ``platform_kind`` (ADMIN-ONLY, default false): mint a PLATFORM kind —
    the definition, its NEW child kinds, and every row the composed create
    writes (examples, edges, seeded input component, and later the
    skill/content block/components, which all inherit the definition's org)
    land in the Matrx System organization with ``visibility='public'``,
    instead of caller-org/internal. This replaces the manual SQL promotion
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
            "platform_kind=true is admin-only: it mints the kind (and every row "
            "the composed create writes) into the Matrx System organization with "
            "visibility='public'. Your account is not a platform admin.",
            "Retry without platform_kind to create a normal kind in your own "
            "organization.",
        )

    if not name or not label:
        return err("validation", "name and label are required.")
    if json_schema is None and sample_data is None:
        return err(
            "validation",
            "Provide json_schema (explicit) or sample_data (schema is inferred from it).",
        )
    if json_schema is not None and not isinstance(json_schema, dict):
        return err("validation", "json_schema must be a JSON Schema object.")
    if required_fields is not None and not (
        isinstance(required_fields, list) and all(isinstance(f, str) for f in required_fields)
    ):
        return err("validation", "required_fields must be a list of root field names.")

    slug = normalize_kind_slug(name)
    bad_slug = validate_kind_slug_format(slug)
    if bad_slug:
        return bad_slug
    if slug in RESERVED_KIND_SLUGS:
        return err(
            "validation",
            f"'{slug}' is a reserved slug (shadowed by a /shapes route segment) — "
            "a kind with this slug would be unreachable in the studio.",
            "Pick a more specific name (e.g. add the domain: 'wine_instances').",
        )
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
        canonical_marked = ensure_root_marker(canonical_example, slug)

        if json_schema is None:
            try:
                json_schema = infer_schema_from_sample(
                    canonical_marked, required_fields=required_fields
                )
            except ValueError as ve:
                return err("validation", str(ve))

        if title_key:
            # Per-kind instance-title override (metadata.title_key — see
            # kind_instance.derive_title + the matrx-frontend mirror): must
            # name a real schema property — a typo here would silently
            # produce "Untitled" instances forever.
            properties = json_schema.get("properties")
            if isinstance(properties, dict) and title_key not in properties:
                return err(
                    "validation",
                    f"title_key '{title_key}' is not a property of the schema "
                    f"(known: {sorted(properties)[:20]}).",
                    "Pass the exact data key that holds an instance's display title.",
                )

        user_id = ctx_user_id(ctx)
        if not user_id:
            return err("validation", "No authenticated user in context — cannot attribute the kind.")
        # A platform mint targets the system org; created_by stays the real
        # admin caller (honest attribution + the owner fast-path for edits).
        org_id = system_organization_id() if platform_kind else ctx_org_id(ctx)

        KindDefinition = get_db_model("KindDefinition")
        # GLOBAL collision check — a kind slug is a global identifier (`__kind`
        # on the wire, fence languages, kind_surface tokens, the slug-keyed
        # render registry). This check used to filter to "my org or my rows",
        # so a user could mint a kind whose slug already belonged to a platform
        # kind: the DB's per-org unique index accepted it, and the frontend
        # registry then found two rows for one slug and threw, taking down kind
        # rendering for anyone who could see both. Never scope this again — the
        # DB backs it with `kind_definition_global_slug_unique`.
        existing = [
            r for r in await KindDefinition.filter(kind=slug).all() if r.deleted_at is None
        ]
        if existing:
            row = existing[0]
            mine = (org_id and str(row.organization_id) == org_id) or str(
                row.created_by or ""
            ) == user_id
            # 🚨 NEVER suggest "pick a different slug" here (2026-08-26
            # incident): that used to be this exact refusal's own
            # suggested_action, and it is a standing invitation to silently
            # FORK a sibling kind under a new name the instant a caller lacks
            # edit access on the real one — the render registry is
            # slug-keyed, so a caller's live agent that emits the ORIGINAL
            # slug then renders nothing and nobody is told why. If the user
            # named this existing kind, the correct move is always to WORK ON
            # IT (bind a component, extend its schema) or STOP and report the
            # access gap — never mint a look-alike under a made-up slug.
            if mine:
                return err(
                    "validation",
                    f"Kind '{slug}' already exists in your scope (id {row.id}). "
                    "Slugs are global — this is the same kind, not a new one.",
                    "Use kind_get to inspect it, kind_update_schema to evolve its "
                    "schema, or kindcomp_create_component / kindcomp_patch_code to "
                    "work on its component. Do not create a new kind under a "
                    "different slug for the same shape.",
                )
            return err(
                "forbidden",
                f"Kind '{slug}' already exists on the platform (id {row.id}, org "
                f"{row.organization_id}) and you do not have editor access to it. "
                f"Slugs are global — a new kind under a different slug would be a "
                f"SILENT FORK: any agent still emitting the real '{slug}' would "
                "keep rendering nothing, because the render registry is keyed by "
                "this exact slug.",
                "Do NOT create a kind under a different slug as a workaround. "
                "Stop and tell the user: this kind exists but they lack edit "
                "access — they need to be granted editor access on it (ask its "
                "owning org/admin), or, only if this is genuinely a DIFFERENT "
                "concept that happens to share a name, pick a name that "
                "actually describes the different concept (not a suffix like "
                "'_v2' or '_pro' on the same slug).",
            )

        # Nested child kinds — resolved or created BEFORE the parent so the
        # composition edges have both ids. The composition doctrine: lists of
        # structured items get their own item kind; most shapes are two levels.
        try:
            child_fields = collect_child_kind_fields(canonical_marked, slug)
        except ValueError as ve:
            return err("validation", str(ve))
        resolved_children: list[tuple[str, Any, bool, bool]] = []
        for field, info in child_fields.items():
            child, created, failure = await _resolve_or_create_child(
                slug=info["slug"],
                sample=info["sample"],  # keeps its markers; the validator reduces
                user_id=user_id,
                org_id=org_id,
                ctx=ctx,
                depth=1,
                platform=platform_kind,
            )
            if failure:
                return failure
            resolved_children.append((field, child, info["is_list"], created))

        block_schema = inject_kind_markers_into_schema(json_schema, canonical_marked, slug)

        errors = validate_against_schema(canonical_marked, block_schema)
        if errors:
            return err(
                "validation",
                "The canonical example does not validate against the schema — refusing to "
                f"create a kind whose own example fails. Errors: {errors[:10]}",
                "Fix the example or the schema so they agree, then retry.",
            )

        kd, example, input_component, failure = await _create_single_kind(
            slug=slug,
            label=label,
            wire_schema=json_schema,
            block_schema=block_schema,
            canonical_marked=canonical_marked,
            user_id=user_id,
            org_id=org_id,
            description=description,
            title_key=title_key,
            loading_component=loading_component,
            platform=platform_kind,
        )
        if failure:
            return failure

        KindEdge = get_db_model("KindEdge")
        edges_out: list[dict[str, Any]] = []
        for position, (field, child, is_list, created) in enumerate(resolved_children):
            edge = await KindEdge.create_item(
                parent_definition_id=str(kd.id),
                field_name=field,
                child_definition_id=str(child.id),
                position=position,
                organization_id=str(kd.organization_id),
                created_by=user_id,
            )
            edges_out.append(
                {
                    "edge_id": str(edge.id),
                    "field": field,
                    "child_kind": child.kind,
                    "child_kind_id": str(child.id),
                    "is_list": is_list,
                    "child_created": created,
                }
            )

        form_fields = fields_from_json_schema(json_schema)
        from matrx_ai.tools.kinds.kind_authoring import (
            ComponentAuthoringBundle,
            KindChildEdge,
            KindCreateResult,
        )
        from matrx_ai.tools.output_caps import cap_list

        children, children_cap = cap_list(edges_out)
        receipt_example, receipt_schema, retrieval_instruction = _bounded_create_echo(
            canonical_marked, json_schema
        )
        return ToolResult(
            success=True,
            output=KindCreateResult(
                kind_definition_id=str(kd.id),
                kind=slug,
                label=label,
                version=kd.version,
                organization_id=str(kd.organization_id),
                visibility=_visibility_value(kd.visibility),
                platform_kind=platform_kind,
                is_active=False,
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
                    f"Kind '{slug}' created "
                    + (
                        "(inactive, PLATFORM: system org, public)"
                        if platform_kind
                        else "(inactive, private)"
                    )
                    + (
                        f" with {len(edges_out)} composed child kind(s)"
                        if edges_out
                        else ""
                    )
                    + ". The stored canonical example IS the render block (markers "
                    "included). Next: kindcomp_create_component — the "
                    "component_authoring bundle above has the props contract, import "
                    "allowlist, and design bar. Then kind_activate (it creates the "
                    "skill and content block automatically)."
                ),
            ),
            output_self_capped=True,
        )
    except Exception as e:
        return _exec_error(e)


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
        if failure:
            return failure
        denied = await ensure_can_view_kind(kd, ctx)
        if denied:
            return denied
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
                canonical_example=canonical.data if canonical else None,
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
                json_schema=kd.emitted_json_schema if include_schema else None,
            ),
        )
    except Exception as e:
        return _exec_error(e)


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
        await KindDefinition.update_where({"id": str(kd.id)}, **updates)
        fresh = await KindDefinition.get_or_none(use_cache=False, id=str(kd.id))

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

            invalidate_kind_catalog_cache()
        except Exception:
            pass
        from matrx_ai.tools.kinds.kind_authoring import KindSchemaUpdateResult, StrandedExample

        return ToolResult(
            success=True,
            output=KindSchemaUpdateResult(
                kind_definition_id=str(kd.id),
                kind=kd.kind,
                new_version=fresh.version if fresh else None,
                new_fingerprint=updates["emitted_fingerprint"],
                example_count=len(examples),
                stranded_examples=[StrandedExample(**s) for s in stranded],
                warning=(
                    f"{len(stranded)} example(s) are stranded by this schema change — fix them "
                    "before activating the kind."
                    if stranded
                    else None
                ),
            ),
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
    """House-format render_block skill body (same shape as the shipped
    kind_* skills, e.g. kind_mermaid_diagram): what it is, the shape with a
    real example, field notes, and the JSON syntax rules."""
    example_obj = {"__kind": kd.kind}
    if isinstance(canonical_example, dict):
        example_obj.update(canonical_example)
    example_json = json.dumps(example_obj, indent=2, ensure_ascii=False)

    schema = kd.emitted_json_schema if isinstance(kd.emitted_json_schema, dict) else {}
    props = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    field_rows = "\n".join(
        f"| `{name}` | {spec.get('type', 'any') if isinstance(spec, dict) else 'any'} | "
        f"{'yes' if name in required else 'no'} |"
        for name, spec in props.items()
    )
    field_table = (
        f"| Field | Type | Required |\n|---|---|---|\n| `__kind` | string | yes |\n{field_rows}\n"
        if field_rows
        else ""
    )
    guidance = f"\n## Additional guidance\n\n{extra_guidance}\n" if extra_guidance else ""
    return (
        f"# {kd.label} (structured __kind JSON)\n\n"
        f"You can emit a **{kd.label}** as a single JSON object marked with\n"
        f'`"__kind": "{kd.kind}"`. It renders through the platform kind registry as a\n'
        f"live, custom component.\n\n"
        f"## The shape\n\n```json\n{example_json}\n```\n\n"
        f"{field_table}\n"
        f"## Syntax rules\n\n"
        f'1. `"__kind"` is always the literal `"{kd.kind}"` and must be the first key.\n'
        f"2. Valid JSON only: double-quoted keys/strings, no trailing commas, no comments.\n"
        f"3. Emit the COMPLETE object every time — when editing, return the full updated\n"
        f"   object, never a fragment or a diff.\n"
        f"4. One object per instance. Two ideas = two `{kd.kind}` objects with a sentence\n"
        f"   between them.\n"
        f"5. Match the schema exactly — include every required field; do not invent keys.\n"
        f"{guidance}"
    )


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
    `platform.categories` row referenced by `skill.render_definition`). Resolved
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
        existing = [s for s in await SklDefinition.filter(skill_id=skill_id).all()
                    if s.deleted_at is None and str(s.organization_id) == str(kd.organization_id)]
        if existing:
            return err(
                "validation",
                f"Skill '{skill_id}' already exists in this organization (id {existing[0].id}).",
                "Edit the existing skill instead of creating a duplicate.",
            )

        body = body_override or _default_skill_body(
            kd, canonical.data if canonical else None, extra_guidance
        )
        created = await SklDefinition.create_item(
            skill_id=skill_id,
            label=f"{kd.label} (structured)",
            description=(
                f"How and when to emit a {kd.kind} render block as canonical "
                f'{{"__kind": "{kd.kind}"}} JSON: the exact shape, required fields, '
                "and JSON syntax rules."
            ),
            skill_type="render_block",
            body=body,
            icon_name="Shapes",
            category_id=await _render_block_category_id(),
            is_active=True,
            is_system=False,
            organization_id=str(kd.organization_id),
            created_by=ctx_user_id(ctx),
            metadata={"kind_definition_id": str(kd.id), "created_via": "kind_create_skill"},
        )
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
    (``skill.render_definition``) that shows up in the user's content-block /
    render-block context menu and drops the emit template into a prompt.
    ``template`` overrides the generated one. Requires a canonical example
    unless template is provided.

    Writes to ``skill.render_definition`` — the table the live context menu
    (``agent.context_menu_view``) actually reads. (The retired
    ``public.content_blocks`` table is admin-only and never reaches the menu.)
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
        RenderDefinition = get_db_model("RenderDefinition")
        existing = [b for b in await RenderDefinition.filter(block_id=block_id).all()
                    if b.deleted_at is None and str(b.organization_id) == str(kd.organization_id)]
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

        # Link the block to its skill (kind_<slug>) when that skill exists in
        # the same org — formalizes the skill<->block pairing via the FK.
        SklDefinition = get_db_model("SklDefinition")
        skill_row = next(
            (s for s in await SklDefinition.filter(skill_id=f"kind_{kd.kind}").all()
             if s.deleted_at is None and str(s.organization_id) == str(kd.organization_id)),
            None,
        )

        created = await RenderDefinition.create_item(
            block_id=block_id,
            label=label or kd.label,
            description=f"Render block teaching an agent to emit the {kd.kind} kind.",
            icon_name="Shapes",
            template=template,
            is_active=True,
            category_id=await _content_block_category_id(),
            skill_id=str(skill_row.id) if skill_row else None,
            organization_id=str(kd.organization_id),
            created_by=ctx_user_id(ctx),
            # Serialize the enum by VALUE — str(member) on a (str, Enum) mixin
            # yields the repr 'Visibility.INTERNAL', which the RenderDefinition
            # EnumField rejects (this killed every wave-4 content-block write).
            visibility=_visibility_value(getattr(kd, "visibility", None)),
            metadata={"kind_definition_id": str(kd.id), "created_via": "kind_create_content_block"},
        )
        from matrx_ai.tools.kinds.kind_authoring import KindContentBlockResult

        return ToolResult(
            success=True,
            output=KindContentBlockResult(
                render_definition_id=str(created.id),
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
        from matrx_orm import call_function

        try:
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
        except Exception as gate_err:
            # The gate raises with the missing-asset reasons inlined; surface
            # them to the agent verbatim so it knows exactly what to build.
            msg = str(gate_err)
            if "failed the dual gate" in msg:
                return err(
                    "validation",
                    f'kind "{kd.kind}" cannot be activated yet — {msg}',
                    suggested=(
                        "Create the missing asset, then call kind_activate again. A missing "
                        "render leg is closed by kindcomp_create_component; a missing "
                        "structural leg by kind_add_example with is_canonical=true."
                    ),
                )
            raise
        verdict = json.loads(raw) if isinstance(raw, str) else raw

        # The catalog caches `is_active`; without this the kind stays invisible
        # to response_format_for_kind and node binding until the TTL lapses.
        try:
            from matrx_graph.kinds import invalidate_kind_catalog_cache

            invalidate_kind_catalog_cache()
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
                skill_exists = any(
                    s.deleted_at is None
                    and str(s.organization_id) == str(kd.organization_id)
                    for s in await SklDefinition.filter(skill_id=f"kind_{kd.kind}").all()
                )
                if not skill_exists:
                    skill_res = await kind_create_skill({"kind": str(kd.id)}, ctx)
                    auto_assets["skill"] = (
                        _wire_output(skill_res.output)
                        if skill_res.success
                        else {"error": skill_res.error.message if skill_res.error else "failed"}
                    )
                RenderDefinition = get_db_model("RenderDefinition")
                block_id = f"kind-{kd.kind.replace('_', '-')}"
                block_exists = any(
                    b.deleted_at is None
                    and str(b.organization_id) == str(kd.organization_id)
                    for b in await RenderDefinition.filter(block_id=block_id).all()
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
