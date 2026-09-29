"""THE SURFACE-WRITE RECEIPT — before → after for every tool that changes a surface.

Arman, 2026-09-26: *"Anytime an agent uses a tool that writes to a surface, we
are showing only the new text but I want any tool that overwrites to show a
shared diff view."*

A tool that changes content a person owns — a note, a working document, a
context item, a file, a CMS page, a component's code, an agent's prompt —
attaches ONE receipt to its ``ToolResult``:

    return attach_surface_write(
        ToolResult(success=True, output=receipt, ...),
        before=old_content, after=new_content,
        target_type="note", target_id=note_id, target_label=label,
        mode="patch", content_format="markdown",
    )

The receipt is OUT OF BAND: ``ToolResult.surface_write`` is excluded from every
dump, so the model never pays for the prior content. The executor turns it into
ONE ``tool_step`` event (``step == SURFACE_WRITE_STEP``) just before
``tool_completed``; that event streams live AND lands in
``chat.tool_call.execution_events``, so the client's one tool-card layer renders
the same shared diff live and on reload with no per-tool code
(matrx-frontend ``features/tool-call-visualization/surface-write/``).

Size: each side is capped by the knob ``agents.tool_dispatch``
``surface_write_max_chars``. A capped side is cut at the cap and the receipt says
so (``truncated``) — the card announces it; it never pretends the diff is whole.

Guard: ``tests/test_surface_write_receipts.py`` — every tool in
:data:`SURFACE_WRITE_TOOLS` must attach a receipt, and every registered tool
whose name says it writes must be declared here or in
:data:`NOT_SURFACE_WRITES` with its reason.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, Field

from matrx_ai.tools.knobs import tool_dispatch_knob

if TYPE_CHECKING:
    from matrx_ai.tools.models import ToolResult

#: The ``tool_step`` step name the client keys on. One string, both repos.
SURFACE_WRITE_STEP = "surface_write"

SURFACE_WRITE_MAX_CHARS_KEY = "surface_write_max_chars"
#: KNOB MIRROR of platform.feature_knob "agents.tool_dispatch" "surface_write_max_chars"
SURFACE_WRITE_MAX_CHARS_MIRROR = 200_000

SurfaceWriteMode = Literal["overwrite", "patch", "append", "prepend", "insert", "create", "structured"]
SurfaceWriteFormat = Literal["markdown", "text", "code", "html", "css", "json"]


class SurfaceWriteReceipt(BaseModel):
    """What changed on which surface — the whole payload the diff card reads."""

    target_type: str = Field(description="note | working_document | context | file | cms_page | …")
    target_id: str | None = None
    target_label: str = ""
    mode: SurfaceWriteMode
    content_format: SurfaceWriteFormat = "text"
    language: str | None = Field(default=None, description="Code language when content_format is code.")
    before: str
    after: str
    before_chars: int
    after_chars: int
    truncated: bool = False
    edits: int | None = Field(default=None, description="How many patch hunks landed, for a patch.")


def _cap() -> int:
    raw = tool_dispatch_knob(SURFACE_WRITE_MAX_CHARS_KEY, SURFACE_WRITE_MAX_CHARS_MIRROR)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return SURFACE_WRITE_MAX_CHARS_MIRROR
    return value if value > 0 else SURFACE_WRITE_MAX_CHARS_MIRROR


def build_surface_write(
    *,
    before: str | None,
    after: str | None,
    target_type: str,
    mode: SurfaceWriteMode,
    target_id: str | None = None,
    target_label: str = "",
    content_format: SurfaceWriteFormat = "text",
    language: str | None = None,
    edits: int | None = None,
) -> SurfaceWriteReceipt:
    before_s = before or ""
    after_s = after or ""
    cap = _cap()
    truncated = len(before_s) > cap or len(after_s) > cap
    return SurfaceWriteReceipt(
        target_type=target_type,
        target_id=target_id,
        target_label=target_label,
        mode=mode,
        content_format=content_format,
        language=language,
        before=before_s[:cap],
        after=after_s[:cap],
        before_chars=len(before_s),
        after_chars=len(after_s),
        truncated=truncated,
        edits=edits,
    )


def attach_surface_write(result: ToolResult, **receipt: object) -> ToolResult:
    """Attach a receipt to a SUCCESSFUL result and return it (a failed write changed nothing)."""
    if result.success:
        result.surface_write = build_surface_write(**receipt)  # type: ignore[arg-type]
    return result


def render_structured(value: object) -> str:
    """Stable, human-diffable text for a structured value (fields, rows, maps):
    sorted-key JSON, two-space indent, so a one-field change is a one-line diff."""
    import json

    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str)


def attach_structured_write(
    result: ToolResult,
    *,
    before: object,
    after: object,
    target_type: str,
    target_id: str | None = None,
    target_label: str = "",
    edits: int | None = None,
) -> ToolResult:
    """The receipt for a STRUCTURED write (row fields, settings, a map, a plan):
    before and after rendered as stable JSON, mode ``structured``. No patch mode —
    the values are replaced as a whole, and the diff shows exactly which moved."""
    return attach_surface_write(
        result,
        before=render_structured(before),
        after=render_structured(after),
        target_type=target_type,
        target_id=target_id,
        target_label=target_label,
        mode="structured",
        content_format="json",
        edits=edits,
    )


def attach_sections_surface_write(
    result: ToolResult,
    *,
    before: dict[str, str | None],
    after: dict[str, str | None],
    header: str = "// ── {name} ──",
    **receipt: object,
) -> ToolResult:
    """One receipt for a write that changed several named sections (code fields,
    page html/css/js). Only sections whose text actually changed are shown; a
    single changed section is shown bare, several are joined under ``header``."""
    changed = [k for k in after if (before.get(k) or "") != (after.get(k) or "")]
    if not changed:
        return result
    if len(changed) == 1:
        k = changed[0]
        b, a = before.get(k) or "", after.get(k) or ""
    else:
        b = "\n\n".join(f"{header.format(name=k)}\n{before.get(k) or ''}" for k in changed)
        a = "\n\n".join(f"{header.format(name=k)}\n{after.get(k) or ''}" for k in changed)
    return attach_surface_write(result, before=b, after=a, **receipt)


#: Every tool (or ``tool:action``) that changes surface content, mapped to the
#: function that performs the write. The guard proves each one attaches a
#: receipt on success — directly, or by forwarding to ``context_patch``.
SURFACE_WRITE_TOOLS: dict[str, tuple[str, str]] = {
    "context_patch:str_replace": ("matrx_ai.tools.implementations.ctx_write", "context_patch"),
    "context_patch:insert": ("matrx_ai.tools.implementations.ctx_write", "context_patch"),
    "context_patch:append": ("matrx_ai.tools.implementations.ctx_write", "context_patch"),
    "context_patch:prepend": ("matrx_ai.tools.implementations.ctx_write", "context_patch"),
    "context_patch:overwrite": ("matrx_ai.tools.implementations.ctx_write", "context_patch"),
    "context_patch:json_patch": ("matrx_ai.tools.implementations.ctx_write", "context_patch"),
    "context_patch:json_merge": ("matrx_ai.tools.implementations.ctx_write", "context_patch"),
    "note:update": ("matrx_ai.tools.implementations.notes", "note_update"),
    "note:patch": ("matrx_ai.tools.implementations.notes", "note_patch"),
    "widget_text_replace": ("matrx_ai.tools.implementations.widgets", "widget_text_replace"),
    "widget_text_patch": ("matrx_ai.tools.implementations.widgets", "widget_text_patch"),
    "widget_text_append": ("matrx_ai.tools.implementations.widgets", "widget_text_append"),
    "widget_text_prepend": ("matrx_ai.tools.implementations.widgets", "widget_text_prepend"),
    "widget_text_insert_before": ("matrx_ai.tools.implementations.widgets", "widget_text_insert_before"),
    "widget_text_insert_after": ("matrx_ai.tools.implementations.widgets", "widget_text_insert_after"),
    "widget_update_field": ("matrx_ai.tools.implementations.widgets", "widget_update_field"),
    "widget_update_record": ("matrx_ai.tools.implementations.widgets", "widget_update_record"),
    # The generic `data` tool is how the default chat agent edits a person's
    # notes, tasks and projects (found live 2026-09-26: General Chat rewrote a
    # note through data:update, not the note tool).
    "data:update": ("aidream.tools.data_tool", "_data_impl"),
    "data:patch": ("aidream.tools.data_tool", "_data_impl"),
    "toolcomp_update_code": ("matrx_ai.tools.implementations.tool_component", "toolcomp_update_code"),
    "toolcomp_patch_code": ("matrx_ai.tools.implementations.tool_component", "toolcomp_patch_code"),
    "kindcomp_update_code": ("matrx_ai.tools.implementations.kind_component", "kindcomp_update_code"),
    "kindcomp_patch_code": ("matrx_ai.tools.implementations.kind_component", "kindcomp_patch_code"),
    "document:edit": ("aidream.services.udt_content.tools", "document"),
    "self_prompt:replace": ("aidream.services.agent_self_prompt.tools", "self_prompt"),
    "self_prompt:patch": ("aidream.services.agent_self_prompt.tools", "self_prompt"),
    "google_workspace:append_document": ("aidream.services.google_workspace.tools", "_append_document"),
    "google_workspace:write_sheet": ("aidream.services.google_workspace.tools", "_write_sheet"),
    "html_page:update": ("aidream.tools.cms_html_page_tool", "_update"),
    "html_page:patch": ("aidream.tools.cms_html_page_tool", "_patch"),
    "cms_page:patch": ("aidream.tools.cms_page_tool", "_patch"),
    "cms_page:save_draft": ("aidream.tools.cms_page_tool", "_save_draft"),
    "cms_page:rollback": ("aidream.tools.cms_page_tool", "_lifecycle"),
    # Throws the unpublished draft away: the editor goes back to the published
    # text, so the card shows the draft that was discarded.
    "cms_page:discard_draft": ("aidream.tools.cms_page_tool", "_lifecycle"),
    # store UPSERTS by key — an existing memory's text is replaced.
    "memory:store": ("matrx_ai.tools.implementations.memory", "memory_store"),
    "cms_component:update": ("aidream.tools.cms_component_tool", "_update"),
    "cms_component:patch": ("aidream.tools.cms_component_tool", "_patch"),
    # Short text a person owns, replaced whole (no patch mode: a memory or a
    # task title is a sentence, and the diff shows the change word by word).
    "memory:update": ("matrx_ai.tools.implementations.memory", "memory_update"),
    "task:update": ("matrx_ai.tools.implementations.tasks", "task_update"),
    "fs_write": ("matrx_ai.tools.implementations.filesystem", "fs_write"),
    "fs_edit": ("matrx_ai.tools.implementations.filesystem", "fs_edit"),
    "fs_patch": ("matrx_ai.tools.implementations.filesystem", "fs_patch"),
}

#: STRUCTURED writes — they replace stored values (fields, rows, settings,
#: maps, plans) rather than prose, so they carry a receipt (via
#: ``attach_structured_write``) but no patch mode. Same guard as above.
STRUCTURED_WRITE_TOOLS: dict[str, tuple[str, str]] = {
    "content_plan:deepen_node": ("aidream.services.content_plan.tools", "_deepen_node"),
    "cms_collection:restore": ("aidream.tools.cms_collection_tool", "_restore"),
    "workflow_author:patch": ("aidream.tools.workflow_tool", "_workflow_author"),
    "content_plan:update_brief": ("aidream.services.content_plan.tools", "_update_brief"),
    "workbook:edit": ("aidream.services.udt_content.tools", "_workbook"),
    "kind_update_schema": ("matrx_ai.tools.implementations.kind_authoring", "kind_update_schema"),
    "instance_update": ("matrx_ai.tools.implementations.kind_instance", "instance_update"),
    "content_plan:update_node": ("aidream.services.content_plan.tools", "_update_node"),
    "content_plan:move_node": ("aidream.services.content_plan.tools", "_move_node"),
    "content_plan:set_status": ("aidream.services.content_plan.tools", "_set_status"),
    "content_plan:set_keyword": ("aidream.services.content_plan.tools", "_set_keyword"),
    "content_plan:update_entity": ("aidream.services.content_plan.tools", "_update_entity"),
    "content_plan:apply_tree": ("aidream.services.content_plan.tools", "_apply_tree"),
    "topical_map:upsert": ("aidream.tools.topical_map_tool", "_upsert"),
    "topical_map:replace_section": ("aidream.tools.topical_map_tool", "_replace_section"),
    "topical_map:patch": ("aidream.tools.topical_map_tool", "_patch"),
    "topical_map:move": ("aidream.tools.topical_map_tool", "_move"),
    "topical_map:merge": ("aidream.tools.topical_map_tool", "_merge"),
    "topical_map:split": ("aidream.tools.topical_map_tool", "_split"),
    "topical_map:set_facet": ("aidream.tools.topical_map_tool", "_set_facet"),
    "topical_map:reject_topics": ("aidream.tools.topical_map_tool", "_reject_topics"),
    "topical_map:add_facet_values": ("aidream.tools.topical_map_tool", "_add_facet_values"),
    "topical_map:set_page_intents": ("aidream.tools.topical_map_tool", "_set_page_intents"),
    "topical_map:update_map": ("aidream.tools.topical_map_tool", "_update_map"),
    "cms_asset:update": ("aidream.tools.cms_asset_tool", "_update"),
    "cms_collection:update": ("aidream.tools.cms_collection_tool", "_update"),
    "cms_site:update": ("aidream.tools.cms_site_tool", "_update"),
    "cms_data:update": ("aidream.tools.cms_data_tool", "_update"),
    "cms_data:set_flags": ("aidream.tools.cms_data_tool", "_set_flags"),
    "cms_page:update": ("aidream.tools.cms_page_tool", "_update"),
    "dictionary:set_settings": ("matrx_ai.tools.implementations.dictionary", "dictionary"),
    "dictionary:upsert_entries": ("matrx_ai.tools.implementations.dictionary", "dictionary"),
    "picklist:update_item": ("matrx_ai.tools.implementations.picklists_tools", "_picklist_impl"),
    "picklist:batch_update": ("matrx_ai.tools.implementations.picklists_tools", "_picklist_impl"),
    "dataset:update_row": ("matrx_ai.tools.implementations.datasets_tools", "dataset"),
    "records:entity_write": ("matrx_records.agent.tool", "records"),
    "records:record_write": ("matrx_records.agent.tool", "records"),
    "records:record_restore_version": ("matrx_records.agent.tool", "records"),
    "rulebook:update_rule": ("aidream.services.distillation.tools", "_rulebook"),
    "rulebook:update_meta": ("aidream.services.distillation.tools", "_rulebook"),
    "rulebook:settle_tension": ("aidream.services.distillation.tools", "_rulebook"),
    "workflow_node:update_node": ("aidream.services.workflow_node_agent.tools", "_workflow_node"),
    "workflow_node:patch": ("aidream.services.workflow_node_agent.tools", "_workflow_node"),
    "workflow_node:update_agent": ("aidream.services.workflow_node_agent.tools", "_workflow_node"),
    "workflow_author:update": ("aidream.tools.workflow_tool", "_workflow_author"),
    "workflow_plan:update": ("aidream.services.workflow_plans.tools", "_workflow_plan"),
    "workflow_plan:set_shape": ("aidream.services.workflow_plans.tools", "_workflow_plan"),
    "workflow_plan:set_sample": ("aidream.services.workflow_plans.tools", "_workflow_plan"),
    "workflow_plan:split": ("aidream.services.workflow_plans.tools", "_workflow_plan"),
    "workflow_plan:merge": ("aidream.services.workflow_plans.tools", "_workflow_plan"),
    "workflow_plan:decompose": ("aidream.services.workflow_plans.tools", "_workflow_plan"),
    "workflow_plan:promote": ("aidream.services.workflow_plans.tools", "_workflow_plan"),
    "workflow_plan:resolve": ("aidream.services.workflow_plans.tools", "_workflow_plan"),
    "workflow_plan:dissolve": ("aidream.services.workflow_plans.tools", "_workflow_plan"),
    "db_user:update": ("aidream.services.db_grants.tools", "_dispatch"),
    "db_admin:update": ("aidream.services.db_grants.tools", "_dispatch"),
    "sql:update": ("matrx_ai.tools.implementations.database", "db_update"),
    "sql:upsert": ("matrx_ai.tools.implementations.database", "_sql_upsert"),
    "kindcomp_update_settings": ("matrx_ai.tools.implementations.kind_component", "kindcomp_update_settings"),
    "toolcomp_update_settings": ("matrx_ai.tools.implementations.tool_component", "toolcomp_update_settings"),
    "record_timezone": ("aidream.services.personal_staff.timezone_tool", "record_timezone"),
}

#: Surface writers that do NOT attach a receipt yet — must stay EMPTY
#: (``test_nothing_is_pending``). A new writer that cannot attach one is a
#: defect to fix, not a row.
PENDING_SURFACE_WRITES: dict[str, str] = {
}

#: Tools that offer a PATCH, with the failure codes their model-facing
#: description must name so the model can act on a refused patch.
#: scripts/check_tool_write_census.py --live reads each tool's description from
#: the database and fails when a code (or the patch-first instruction) is
#: missing — so a description cannot silently drift back to "fuzzy match".
_ONE_PLACE = ("patch_no_match", "patch_ambiguous")
PATCHING_TOOLS: dict[str, tuple[str, ...]] = {
    "context_patch": (*_ONE_PLACE, "patch_protected_block"),
    "note": (*_ONE_PLACE, "patch_protected_block"),
    "data": _ONE_PLACE,
    "document": _ONE_PLACE,
    "self_prompt": _ONE_PLACE,
    "widget_text_patch": (*_ONE_PLACE, "patch_protected_block"),
    "fs_edit": _ONE_PLACE,
    "fs_patch": _ONE_PLACE,
    "html_page": _ONE_PLACE,
    "cms_page": _ONE_PLACE,
    "cms_component": _ONE_PLACE,
    "kindcomp_patch_code": _ONE_PLACE,
    "toolcomp_patch_code": _ONE_PLACE,
}

#: The actions classified below are DERIVED (``matrx_ai.tools.dispatch_census``):
#: Literal dispatch fields from the argument models, str-typed dispatchers from
#: the constants their implementation dispatches on, registry dispatchers from
#: the registry. Nothing here is a hand-kept action list, and a bare tool name
#: classifies only a tool that HAS no actions — never a wildcard.


def _not(reason: str, *keys: str) -> dict[str, str]:
    return dict.fromkeys(keys, reason)


_READS = "reads or searches; changes nothing"
_CREATES = "creates a NEW item; nothing already stored is replaced (the card shows what was made)"
_REMOVES = "removes or archives an item (recoverable where the table soft-deletes); nothing is overwritten"
_LIFECYCLE = "moves an item through its lifecycle (publish / activate / retire / discard); content is unchanged"
_EXTERNAL = "acts outside a person's stored content (a browser, a message, a job, a login, an external API)"
_PROPOSES = "proposes a change a person approves in its own approval card, which shows the change"
_SESSION = "changes only this conversation's working state (loaded tools, active context, a cache)"
_OPERATIONAL = "operational bookkeeping on platform rows (incidents, errors, traces), not a person's content"
_SECRET = "writes a secret; secrets are never displayed, so there is nothing to diff"
_CHECKLIST = "the agent's own working checklist for this conversation, drawn live by its own card"
_COMPOSITE = "runs a named multi-step operation that creates new items; it replaces nothing"
_UNARCHIVES = (
    "brings archived items back (the inverse of an archiving delete); content is unchanged except a "
    "name or route taken meanwhile, which comes back suffixed and is reported in the result's notices"
)

#: Every other action of every registered tool, classified with its reason.
#: The guard (aidream/tools/tests/test_every_tool_action_is_classified.py)
#: derives the full action list from the argument models and fails on any
#: action in none of SURFACE_WRITE_TOOLS / STRUCTURED_WRITE_TOOLS / this map. A
#: key ``tool`` classifies every action of that tool.
NOT_SURFACE_WRITES: dict[str, str] = {
    **_not("creates a new page on an external host; there is no prior content", "code_store_html"),
    **_not("attaches a media reference through context_patch json_patch, which carries its own receipt",
           "widget_attach_media"),
    **_not(_CREATES, "widget_create_artifact", "note:create", "task:create", "context:create",
           "cms_asset:upload", "cms_collection:create", "cms_component:create", "cms_data:create", "cms_page:create",
           "cms_page:create_many", "cms_site:create", "cms_site:starter_kit", "cms_site:redirect_record",
           "content_plan:create_entity", "content_plan:create_node", "content_plan:instantiate_archetype",
           "content_plan:attach_entity", "content_plan:tag_topic", "dataset:create", "dataset:add_rows",
           "picklist:create", "html_page:create", "html_page:promote", "google_workspace:create_document",
           "google_workspace:create_sheet", "google_workspace:import_contact", "google_workspace:import_sheet_as_table",
           "google_workspace:import_tasks", "rulebook:add_rules", "topical_map:create_map",
           "topical_map:create_planned_page", "workflow_node:create_agent", "workflow_node:fork_agent",
           "workflow_author:create", "document:create", "workbook:create", "data:create", "db_admin:create",
           "db_user:create", "sql:insert", "instance_create", "kind_add_example", "kind_create",
           "kind_create_content_block", "kind_create_skill", "kindcomp_create_component", "toolcomp_create_component",
           "fs_mkdir", "office:generate", "storage_source_import", "travel_create_summary", "credential_login:capture",
           "workflow_plan:build_agent", "workflow_plan:recommend", "workflow_plan:emit"),
    **_not(_UNARCHIVES, "cms_site:restore", "cms_site:redirect_restore", "cms_page:restore",
           "cms_component:restore", "cms_asset:restore", "html_page:restore", "dictionary:restore_entries"),
    # The media, writing and crisis desk (BRIEFS-MEDIA-WRITING-CRISIS, 2026-09-27): a clip and a voice
    # fingerprint are NEW records (nothing replaced); the checks and the moment feed only read.
    **_not(_CREATES, "cloud_browser:render_clip", "brand_voice_measure:extract"),
    **_not(_READS, "brand_voice_measure:check", "pitch_advisories", "crm_one_per_outlet", "pr_moments"),
    # Not the media desk's, classified so the guard stays green: both only read (knowledge_open opens a
    # knowledge_search result; records:guide returns one verb's worked example).
    **_not(_READS, "knowledge_open", "records:guide"),
    **_not(_COMPOSITE, "data_action:create_note_in_project", "data_action:create_task_in_project",
           "data_action:transcript_to_note"),
    **_not(_READS, "data_action:catalog", "data_action:read_file_extraction", "data_action:resolve_contact"),
    **_not(_REMOVES, "workflow_plan:retire", "note:delete", "task:delete", "memory:forget", "cloud_file:delete", "cloud_file:batch_delete",
           "cms_asset:delete", "cms_collection:delete", "cms_collection:archive", "cms_component:delete",
           "cms_data:delete", "cms_page:delete", "cms_site:delete", "cms_site:redirect_delete",
           "content_plan:delete_node", "dataset:delete_row", "dictionary:delete_entries", "html_page:delete",
           "records:record_delete", "data:delete", "db_admin:delete", "db_user:delete", "sql:delete",
           "instance_delete"),
    **_not(_LIFECYCLE, "workflow_plan:settle", "cms_page:publish", "cms_page:publish_many",
           "kind_activate", "rulebook:retire_rule", "rulebook:retire_rules",
           "topical_map:retire"),
    **_not(_EXTERNAL, *(f"cloud_browser:{a}" for a in (
        "click", "close", "dismiss_handoff", "get_element", "list_local_devices", "list_profiles", "navigate",
        "screenshot", "scroll", "select_option", "start_local", "type_text", "wait_for")),
           "notify_me:send", "send_text", "send_secure_link", "ask_person",
           "agent_call", "mandate_call", "staff_escalate", "credential_login:attempt", "credential_login:auto",
           "credential_login:authenticator", "credential_login:report", "google_workspace:prepare_email",
           "github_repositories:refresh", "seo:collect_rank", "research_run:start", "research_run:schedule",
           "agent_plan:run", "agent_plan:cancel", "workflow_run:run", "workflow_run:cancel", "shell_execute",
           "shell_python", "code_execute_python", "cms_verify:capture", "cms_verify:capture_site",
           "cms_verify:render_check", "cms_page:submit_exception", "sealed_case:commit", "sealed_case:ask",
           "cms_collection:rotate_site_key", "content_plan:cms_align", "content_plan:cms_reconcile"),
    **_not(_PROPOSES, "records:booking_propose", "records:capture_propose", "records:checklist_propose",
           "records:dashboard_propose", "records:document_propose", "records:enrich_propose",
           "records:field_propose", "records:form_propose", "records:import_propose", "records:pipeline_propose",
           "records:portal_propose", "records:signature_request", "records:subscription_propose",
           "records:table_propose", "keyword_meaning_suggest:propose_guideline_edit",
           "keyword_meaning_suggest:propose_matcher", "keyword_meaning_suggest:propose_stamp",
           "keyword_meaning_suggest:propose_worth", "credential_login:propose_recipe"),
    **_not(_SESSION, "load_chrome_tools", "load_desktop_tools", "scope_system:apply", "topical_map:use_map"),
    **_not(_OPERATIONAL, "errors:resolve", "kindcomp_resolve_incident", "toolcomp_resolve_incident",
           "report_trace_incident"),
    **_not(_SECRET, "user_secret_set"),
    **_not(_CHECKLIST, *(f"tasks:{a}" for a in (
        "add", "clear_all", "clear_completed", "remove", "reorder", "set_status", "update"))),
    **_not(_READS, "tasks:list", "value_store:describe", "value_store:get", "value_store:list",
           "self_prompt:read", "self_prompt:read_full"),
    **_not("the conversation value store (tool-result cache), not a person's surface",
           "value_store:put", "value_store:groom"),
    **_not(
        _READS,
    "agent_plan:status", "cardsight_identify", "cisco_serial_lookup", "cloud_file:batch_get",
    "cloud_file:get", "cloud_file:list", "cms_asset:get", "cms_asset:list",
    "cms_asset:usage", "cms_asset:versions", "cms_collection:get", "cms_collection:list",
    "cms_collection:versions", "cms_component:get", "cms_component:list", "cms_component:versions",
    "cms_data:export", "cms_data:get", "cms_data:list", "cms_data:query",
    "cms_data:stats", "cms_find_page", "cms_inspect:component_catalog", "cms_inspect:css_cascade",
    "cms_inspect:rules", "cms_inspect:site_overview", "cms_page:get", "cms_page:list",
    "cms_page:versions", "cms_site:get", "cms_site:list", "cms_site:redirects",
    "cms_site:versions", "code_fetch_code", "code_fetch_tree", "content_plan:foundation_checklist",
    "content_plan:get_profile", "content_plan:get_tree", "content_plan:list_archetypes", "content_plan:list_concepts",
    "content_plan:list_entities", "content_plan:list_sites", "context:batch", "context:get",
    "conversations:get_messages", "conversations:get_summary", "conversations:list", "conversations:search",
    "credential_login:discover", "credential_login:list", "data:catalog", "data:count",
    "data:get", "data:query", "dataset:get", "dataset:list",
    "dataset:search", "db_admin:get", "db_admin:query", "db_admin:schema",
    "db_user:get", "db_user:query", "db_user:schema", "debug_traces_by_call",
    "debug_traces_by_conv", "debug_traces_failures_since", "debug_traces_get_file", "debug_traces_list_files",
    "debug_traces_recent", "desktop_capabilities", "dictionary:fetch_user_content", "dictionary:get_settings",
    "dictionary:list_entries", "dictionary:list_owners", "dictionary:resolve", "document:read",
    "document_content:assets", "document_content:images", "document_content:page_index", "document_content:read",
    "document_search", "errors:get", "errors:list", "errors:metrics",
    "errors:surfaces", "factcheck_search", "fetch_tool_result", "file_read",
    "fs_list", "fs_read", "fs_search", "get_open_trace_incidents",
    "git_ingest", "github_repositories:list", "github_repositories:status", "google_marketing:read_google_analytics",
    "google_marketing:read_search_console", "google_marketing:read_tag_manager", "google_marketing:read_youtube_analytics", "google_marketing:read_youtube_channel",
    "google_marketing:tracking_health", "google_workspace:list_resources", "google_workspace:read_calendar", "google_workspace:read_contacts",
    "google_workspace:read_document", "google_workspace:read_presentation", "google_workspace:read_sheet", "google_workspace:read_tasks",
    "html_page:get", "html_page:list", "html_page:versions", "icecat_lookup",
    "image_metadata", "instance_get", "instance_list", "kind_get",
    "kindcomp_get_code", "kindcomp_get_context", "knowledge_browse:chunk", "knowledge_browse:entity",
    "knowledge_browse:sources", "knowledge_browse:store", "knowledge_browse:stores", "knowledge_compare",
    "knowledge_search", "llms_txt_fetch", "math_calculate", "memory:recall",
    "memory:search", "news_get_headlines", "note:get", "note:list",
    "notify_me:readiness", "notify_me:status", "office:extract", "package_info",
    "picklist:get", "picklist:list", "random_wheel", "records:entity_read",
    "records:metadata_search", "records:record_aggregate", "records:record_history", "records:record_read",
    "records:table_list", "research_run:bounds", "research_run:status", "research_web",
    "reverse_image_search", "rulebook:read", "rulebook:read_rule", "rulebook_read:get",
    "rulebook_read:list", "rulebook_read:sections", "scope_system:expand_context_item", "scope_system:expand_scope",
    "scope_system:expand_scope_type", "scope_system:overview", "sealed_case:ledger", "seo:check_batch",
    "seo:check_descriptions", "seo:check_titles", "seo:keyword_data", "skill:get",
    "skill:list", "skill:search", "sql:query", "sql:schema",
    "staff_roster", "storage_source_browse", "storage_source_connections", "task:get",
    "task:list", "text_analyze", "text_regex_extract", "toolcomp_get_code",
    "toolcomp_get_context", "toolcomp_get_incident_detail", "toolcomp_get_sample_detail", "toolcomp_list_tools",
    "topical_map:associations", "topical_map:diagnostics", "topical_map:facet_values", "topical_map:get",
    "topical_map:graph", "topical_map:map_history", "topical_map:map_pages", "topical_map:maps",
    "topical_map:outline", "topical_map:page_intents", "topical_map:search", "topical_map:topic_gaps",
    "topical_map:tree", "travel_get_activities", "travel_get_events", "travel_get_location",
    "travel_get_restaurants", "travel_get_weather", "upc_lookup", "verify:answer",
    "verify:document", "vsc_get_state", "weather_history", "web:batch_read",
    "web:read", "web:search", "workbook:read", "workflow_author:validate",
    "workflow_catalog:definition_shape", "workflow_catalog:get_node_type", "workflow_catalog:get_workflow", "workflow_catalog:list_models",
    "workflow_catalog:list_node_types", "workflow_catalog:list_workflows", "workflow_node:get_agent", "workflow_node:get_context",
    "workflow_plan:check", "workflow_plan:list", "workflow_plan:read", "workflow_run:status",
    "ximilar_identify",
    ),
}
