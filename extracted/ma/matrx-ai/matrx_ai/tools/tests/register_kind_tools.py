"""
One-shot registration script for the kind_* + kindcomp_* creator-agent
toolsets (kind-registry authoring — see implementations/kind_authoring.py and
implementations/kind_component.py).

Parameters are derived DIRECTLY from the declared Pydantic arg models
(standard JSON Schema — one of the two shapes the tool-drift gate
canonicalises), so the DB row cannot drift from the code contract at
registration time.

Run once:  python -m matrx_ai.tools.tests.register_kind_tools
"""

from __future__ import annotations

import asyncio

from matrx_ai.tools._generated_declarations import (
    InstanceCreateArgs,
    InstanceDeleteArgs,
    InstanceGetArgs,
    InstanceListArgs,
    InstanceUpdateArgs,
    KindAddExampleArgs,
    KindcompCreateComponentArgs,
    KindcompGetCodeArgs,
    KindcompGetContextArgs,
    KindcompPatchCodeArgs,
    KindcompResolveIncidentArgs,
    KindcompUpdateCodeArgs,
    KindcompUpdateSettingsArgs,
    KindCreateArgs,
    KindCreateContentBlockArgs,
    KindCreateSkillArgs,
    KindGetArgs,
    KindUpdateSchemaArgs,
)

TOOLS = [
    {
        "name": "kind_create",
        "args": KindCreateArgs,
        "description": (
            "Create a new Content-IR kind (a named, versioned JSON Schema in the platform "
            "shape registry) from the user's data. Provide name + label and EITHER an explicit "
            "json_schema OR sample_data (the schema is inferred deterministically from it; "
            "send your sample WITH its __kind markers — they identify the shape and its "
            "nested children, and the stored example keeps them). A canonical example is "
            "stored beside the kind and MUST "
            "validate against the schema — creation is refused otherwise. SET title_key (a "
            "single data key, stored as metadata.title_key) whenever the sample has an obvious "
            "title-ish field NOT in the shared derivation list (title/name/label/heading/"
            "subject/customer) — e.g. wine_name — so saved instances don't list as 'Untitled'; "
            "it must name a schema property. Automatically seeds "
            "the 'generic_structured' input-role component (the ONLY routable input key — "
            "never create custom input components) so the /shapes Test form works, and for "
            "flat schemas a per-field form definition (nested shapes keep the JSON editor). "
            "New kinds are inactive and private in your organization; platform builds by an "
            "ADMIN pass platform_kind=true to mint straight into the Matrx System org with "
            "visibility='public' (refused for non-admins — never pass it for a user's "
            "personal kind). Next steps: "
            "kindcomp_create_component (build the renderer), kind_create_skill + "
            "kind_create_content_block (teach agents to emit it)."
        ),
        "icon": "Shapes",
        "annotations": [{"type": "destructiveHint", "value": False}],
    },
    {
        "name": "kind_get",
        "args": KindGetArgs,
        "description": (
            "Fetch a kind's full definition: JSON schema, fingerprint, examples with "
            "validation status, components, and detection surfaces. Pass kind as slug or "
            "kind_definition_id; include_schema=false skips the schema body."
        ),
        "icon": "Shapes",
        "annotations": [{"type": "readOnlyHint", "value": True}],
    },
    {
        "name": "kind_update_schema",
        "args": KindUpdateSchemaArgs,
        "description": (
            "Replace a kind's JSON Schema. The kind version bumps automatically and every "
            "example is re-validated by the DB trigger; the result reports STRANDED examples "
            "(now-failing or pinned to an older kind version) so schema evolution never "
            "silently breaks the example set. Fix stranded examples before activating the kind."
        ),
        "icon": "Shapes",
        "annotations": [{"type": "destructiveHint", "value": True}],
    },
    {
        "name": "kind_add_example",
        "args": KindAddExampleArgs,
        "description": (
            "Add an example payload to a kind. Validated against the current schema BEFORE "
            "insert (refused on failure). is_canonical=true makes it the reference example "
            "and demotes the previous canonical one."
        ),
        "icon": "Shapes",
        "annotations": [{"type": "destructiveHint", "value": False}],
    },
    {
        "name": "kind_create_skill",
        "args": KindCreateSkillArgs,
        "description": (
            "Create the render_block agent skill (skill_id kind_<slug>) that teaches platform "
            "agents to emit this kind as __kind JSON, following the shipped kind_* skill house "
            "format (shape, real example, field table, JSON syntax rules). body overrides the "
            "generated body; extra_guidance appends domain rules. Requires a canonical example."
        ),
        "icon": "GraduationCap",
        "annotations": [{"type": "destructiveHint", "value": False}],
    },
    {
        "name": "kind_create_content_block",
        "args": KindCreateContentBlockArgs,
        "description": (
            "Create the reusable prompt content block (block_id kind-<slug>) users drop into "
            "agent prompts to make an agent emit this kind. template overrides the generated "
            "one. Requires a canonical example unless template is provided."
        ),
        "icon": "Blocks",
        "annotations": [{"type": "destructiveHint", "value": False}],
    },
    {
        "name": "instance_create",
        "args": InstanceCreateArgs,
        "description": (
            "Save a payload as a durable instance of a Content-IR kind ('save this'). Provide "
            "kind (slug or kind_definition_id) and data (the payload object). The stored "
            "instance CARRIES its root __kind marker — it is part of the data, stamped (or "
            "corrected) for you, so a saved row can never forget what it is. "
            "The payload is validated against the kind's current schema "
            "BEFORE insert (refused on failure), the kind_version is pinned at write, and the "
            "DB derived-on-write trigger's verdict is read back as the truth. title sets the "
            "display label (derived when omitted: the kind's metadata.title_key field first, "
            "then title/name-ish keys). The instance is "
            "private, owned by you, in your organization — you own instances of any kind you "
            "can view, including platform kinds. Requires viewer access on the kind. Saved "
            "instances appear in the shape's Instances tab at /shapes/<slug>."
        ),
        "icon": "Save",
        "annotations": [{"type": "destructiveHint", "value": False}],
    },
    {
        "name": "instance_list",
        "args": InstanceListArgs,
        "description": (
            "List YOUR saved kind instances (rows you created), newest-updated first. kind "
            "narrows to one kind; status (pending/passed/failed) narrows by validation "
            "verdict. Paginated (limit default 50, max 200; offset). Light projection: id, "
            "kind, title, validation_status, kind_version, updated_at — use instance_get for "
            "the payload."
        ),
        "icon": "List",
        "annotations": [{"type": "readOnlyHint", "value": True}],
    },
    {
        "name": "instance_get",
        "args": InstanceGetArgs,
        "description": (
            "Fetch one kind instance: full payload, title, pinned kind_version, derived "
            "validation_status, and the kind's current version (pinned_behind_current flags "
            "an instance stranded behind a schema bump). Access: viewer on the instance."
        ),
        "icon": "FileJson",
        "annotations": [{"type": "readOnlyHint", "value": True}],
    },
    {
        "name": "instance_update",
        "args": InstanceUpdateArgs,
        "description": (
            "Update an instance's data and/or title (editor access). Data for a "
            "current-version instance is validated before write (refused on failure); for an "
            "instance pinned to an older kind version the DB verdict is read back and "
            "surfaced loudly — pass repin_to_current=true to move it onto the current schema "
            "in the same write (the fix for the version-bump stranding trap)."
        ),
        "icon": "Save",
        "annotations": [
            {"type": "destructiveHint", "value": True},
            {"type": "idempotentHint", "value": True},
        ],
    },
    {
        "name": "instance_delete",
        "args": InstanceDeleteArgs,
        "description": (
            "Soft-delete a kind instance (recoverable tombstone: deleted_at set, row "
            "retained). Editor access required."
        ),
        "icon": "Trash2",
        "annotations": [{"type": "destructiveHint", "value": True}],
    },
    {
        "name": "kindcomp_get_context",
        "args": KindcompGetContextArgs,
        "description": (
            "Primary context bundle for working on a kind's UI component: the kind definition "
            "(schema + fingerprint + version + summary.title_key, the per-kind instance-title "
            "field), the canonical example payload (the exact data "
            "shape the component receives), summaries of every component, open render "
            "incidents deduplicated by error signature, and props_contract — the authoritative "
            "component mounting contract (the frontend renders DB components as <Component "
            "data={value} kind={kind} config={config} />: read everything from props.data, "
            "never flat props; props_transform output also lands under props.data). Use this "
            "FIRST when creating or fixing any kind component. Pass kind (slug or "
            "kind_definition_id) or component_id."
        ),
        "icon": "Wrench",
        "annotations": [{"type": "readOnlyHint", "value": True}],
    },
    {
        "name": "kindcomp_create_component",
        "args": KindcompCreateComponentArgs,
        "description": (
            "Create a DB-authored render component for a kind (source='db'). PROPS CONTRACT: "
            "the frontend mounts your component as <Component data={value} kind={kind} "
            "config={config} /> — the kind instance arrives as props.data (destructure "
            "{ data }); flat props are NEVER provided and reading them renders empty with no "
            "error. props_transform reshapes the value but its output STILL arrives as "
            "props.data. Sources that never reference `data` are refused. Required: kind, "
            "component_key (short stable id), component_source (COMPLETE TSX source). Never "
            "create input-role components — the seeded 'generic_structured' row is the only "
            "routable input path. Components are unique per (kind, platform, role, "
            "component_key); duplicates fail with a pointer to kindcomp_update_code."
        ),
        "icon": "PlusCircle",
        "annotations": [{"type": "destructiveHint", "value": False}],
    },
    {
        "name": "kindcomp_get_code",
        "args": KindcompGetCodeArgs,
        "description": (
            "Read the full source of a kind component. sections picks component_source and/or "
            "props_transform (default both). Output: one metadata object with a sections map; "
            "reference those section names in kindcomp_patch_code."
        ),
        "icon": "Code",
        "annotations": [{"type": "readOnlyHint", "value": True}],
    },
    {
        "name": "kindcomp_update_code",
        "args": KindcompUpdateCodeArgs,
        "description": (
            "Replace code sections on a kind component. updates maps section name "
            "(component_source / props_transform) to the COMPLETE replacement code — never "
            "partial. PROPS CONTRACT: the component reads the kind instance from props.data "
            "(flat props are never provided; props_transform output also lands under "
            "props.data) — a component_source with no `data` reference is refused. "
            "bump_version advances the human-facing semver; the integer revision "
            "auto-increments in the DB and prior rows snapshot to history automatically."
        ),
        "icon": "Code",
        "annotations": [
            {"type": "destructiveHint", "value": True},
            {"type": "idempotentHint", "value": True},
        ],
    },
    {
        "name": "kindcomp_patch_code",
        "args": KindcompPatchCodeArgs,
        "description": (
            "Apply targeted old_string->new_string replacements to one code section of a kind "
            "component without rewriting it. Patches apply in order with three matching rounds "
            "of decreasing strictness (exact, whitespace-normalized, quote+whitespace-"
            "normalized). If any patch fails all rounds — or the patched component_source "
            "would no longer reference props.data (the silent-empty-render class) — the whole "
            "operation aborts and nothing is written. Each patch also accepts find/replace "
            "as aliases for old_string/new_string."
        ),
        "icon": "Scissors",
        "annotations": [
            {"type": "destructiveHint", "value": True},
            {"type": "idempotentHint", "value": False},
        ],
    },
    {
        "name": "kindcomp_update_settings",
        "args": KindcompUpdateSettingsArgs,
        "description": (
            "Update non-code settings on a kind component: is_active, is_default, sort_order, "
            "config, pinned_kind_version, component_key, or notes. Code fields go through "
            "kindcomp_update_code."
        ),
        "icon": "Settings",
        "annotations": [{"type": "idempotentHint", "value": True}],
    },
    {
        "name": "kindcomp_resolve_incident",
        "args": KindcompResolveIncidentArgs,
        "description": (
            "Mark a kind-component render incident as resolved after fixing the component, so "
            "it stops appearing in kindcomp_get_context's open incident list. Optionally add "
            "resolution notes."
        ),
        "icon": "CheckCircle",
        "annotations": [{"type": "idempotentHint", "value": True}],
    },
]

# Native platform tools live in the system org, publicly visible (same as the
# toolcomp_* rows).
SYSTEM_ORGANIZATION_ID = "39c38960-d30c-4840-b0c1-c9960de95582"

OUTPUT_SCHEMA = {
    "type": "object",
    "description": "Tool-specific result object; on failure a structured error with suggested_action.",
}


async def register_all() -> None:
    from matrx_ai._ext import get_ext

    get_async_supabase_client = get_ext("get_async_supabase_client")
    client = get_async_supabase_client()

    for tool in TOOLS:
        existing = (
            await client.schema("tool")
            .table("definition")
            .select("id, name")
            .eq("name", tool["name"])
            .execute()
        )
        if existing.data:
            print(f"  [SKIP]   {tool['name']} — already registered (id={existing.data[0]['id']})")
            continue

        payload = {
            "name": tool["name"],
            "description": tool["description"],
            # Standard JSON Schema straight from the declared args model —
            # zero drift against the code contract by construction.
            "parameters": tool["args"].model_json_schema(),
            "output_schema": OUTPUT_SCHEMA,
            "source_kind": "native",
            "category": "internal",
            "tags": ["kind-registry", "internal", "creator-agent"],
            "icon": tool["icon"],
            "is_active": True,
            "organization_id": SYSTEM_ORGANIZATION_ID,
            "visibility": "public",
            "annotations": tool.get("annotations", []),
        }
        res = await client.schema("tool").table("definition").insert(payload).execute()
        if res.data:
            print(f"  [OK]     {tool['name']} — registered (id={res.data[0]['id']})")
        else:
            print(f"  [ERROR]  {tool['name']} — insert returned no data")


async def sync_descriptions() -> None:
    """Push THIS file's descriptions onto existing tool.definition rows.

    Descriptions are the agent-facing UX and are NOT covered by the drift
    gate — run this after editing any description above so the DB (the
    source the agent actually reads) matches the code."""
    from matrx_ai._ext import get_ext

    client = get_ext("get_async_supabase_client")()
    for tool in TOOLS:
        res = (
            await client.schema("tool")
            .table("definition")
            .update({"description": tool["description"]})
            .eq("name", tool["name"])
            .execute()
        )
        state = "OK" if res.data else "MISSING"
        print(f"  [{state}] {tool['name']} description synced")


if __name__ == "__main__":
    import sys

    if "--sync-descriptions" in sys.argv:
        asyncio.run(sync_descriptions())
    else:
        asyncio.run(register_all())
