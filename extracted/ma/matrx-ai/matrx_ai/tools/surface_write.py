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
    # `self_prompt` is a router (tool_runner -> the case's Action); the receipt is
    # built in each case's Action, so the declaration names the Action (25bb3e441).
    "self_prompt:replace": ("aidream.services.agent_self_prompt.tools", "self_prompt_replace"),
    "self_prompt:patch": ("aidream.services.agent_self_prompt.tools", "self_prompt_patch"),
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
    "workbook:edit": ("aidream.services.udt_content.tools", "_edit"),
    # write_formula runs the same edit (``_workbook`` action=edit, which attaches the receipt), then recalculates.
    "workbook:write_formula": ("aidream.services.udt_content.tools", "_edit"),
    "deck:edit": ("aidream.services.udt_content.deck_tool", "_run"),
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
    "pick_list:update_item": ("matrx_ai.tools.implementations.pick_list_tools", "_pick_list_impl"),
    "pick_list:batch_update": ("matrx_ai.tools.implementations.pick_list_tools", "_pick_list_impl"),
    "records:entity_write": ("matrx_records.agent.tool", "records"),
    "records:record_write": ("matrx_records.agent.tool", "records"),
    "records:record_restore_version": ("matrx_records.agent.tool", "records"),
    "understanding:save": ("aidream.services.agent_understanding.tools", "understanding"),
    "rulebook:update_rule": ("aidream.services.distillation.tools", "_rulebook"),
    "rulebook:update_meta": ("aidream.services.distillation.tools", "_rulebook"),
    "rulebook:settle_tension": ("aidream.services.distillation.tools", "_rulebook"),
    "workflow_node:update_node": ("aidream.services.workflow_node_agent.tools", "_case_update_node"),
    "workflow_node:patch": ("aidream.services.workflow_node_agent.tools", "_case_patch"),
    "workflow_node:update_agent": ("aidream.services.workflow_node_agent.tools", "_case_update_agent"),
    "workflow_author:update": ("aidream.tools.workflow_tool", "_workflow_author"),
    "workflow_plan:update": ("aidream.services.workflow_plans.tools", "_with_receipt"),
    "workflow_plan:set_shape": ("aidream.services.workflow_plans.tools", "_with_receipt"),
    "workflow_plan:set_sample": ("aidream.services.workflow_plans.tools", "_with_receipt"),
    "workflow_plan:split": ("aidream.services.workflow_plans.tools", "_with_receipt"),
    "workflow_plan:merge": ("aidream.services.workflow_plans.tools", "_with_receipt"),
    "workflow_plan:decompose": ("aidream.services.workflow_plans.tools", "_with_receipt"),
    "workflow_plan:promote": ("aidream.services.workflow_plans.tools", "_with_receipt"),
    "workflow_plan:resolve": ("aidream.services.workflow_plans.tools", "_with_receipt"),
    "workflow_plan:dissolve": ("aidream.services.workflow_plans.tools", "_with_receipt"),
    "db_user:update": ("aidream.services.db_grants.tools", "_dispatch"),
    "db_admin:update": ("aidream.services.db_grants.tools", "_dispatch"),
    "sql:update": ("matrx_ai.tools.implementations.database", "db_update"),
    "sql:upsert": ("matrx_ai.tools.implementations.database", "_sql_upsert"),
    "sql:patch": ("matrx_ai.tools.implementations.database", "_sql_patch"),
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
    "advanced_read": "a paid read of web pages; writes nothing the person sees on a surface",
    **_not("attaches a media reference through context_patch json_patch, which carries its own receipt",
           "widget_attach_media"),
    **_not(_CREATES, "applet:build", "applet:write"),
    **_not("rewrites an Applet's files through the builder; every save is a version in app.definition_version the person can restore, "
           "so the prior content is never lost", "applet:change"),
    **_not("places an Applet under a section of the company address; the Applet's own content is untouched", "applet:place"),
    **_not(_CREATES, "widget_create_artifact", "note:create", "task:create", "context:create",
           "cms_asset:upload", "cms_collection:create", "cms_component:create", "cms_data:create", "cms_page:create",
           "cms_page:create_many", "cms_site:create", "cms_site:starter_kit", "cms_site:redirect_record",
           "content_plan:create_entity", "content_plan:create_node", "content_plan:instantiate_archetype",
           "content_plan:attach_entity", "content_plan:tag_topic", "pick_list:create", "html_page:create", "html_page:promote", "google_workspace:create_document",
           "google_workspace:create_sheet", "google_workspace:import_contact", "google_workspace:import_sheet_as_table",
           "google_workspace:import_tasks", "rulebook:add_rules", "topical_map:create_map",
           "topical_map:create_planned_page", "workflow_node:create_agent", "workflow_node:fork_agent",
           "workflow_author:create", "document:create", "workbook:create", "data:create", "db_admin:create",
           "db_user:create", "sql:insert", "instance_create", "kind_add_example", "kind_create",
           "kind_create_content_block", "kind_create_skill", "kindcomp_create_component", "toolcomp_create_component",
           "fs_mkdir", "office:generate", "storage_source_import", "credential_login:capture",
           "workflow_plan:build_agent", "workflow_plan:recommend", "workflow_plan:emit"),
    **_not(_UNARCHIVES, "cms_site:restore", "cms_site:redirect_restore", "cms_page:restore",
           "cms_component:restore", "cms_asset:restore", "html_page:restore", "dictionary:restore_entries"),
    # The media, writing and crisis desk (BRIEFS-MEDIA-WRITING-CRISIS, 2026-09-27): a clip and a voice
    # fingerprint are NEW records (nothing replaced); the checks and the moment feed only read.
    **_not(_CREATES, "cloud_browser:render_clip"),
    **_not(_READS, "pitch_advisories", "crm_one_per_outlet", "pr_moments"),
    # Not the media desk's, classified so the guard stays green: both only read (knowledge_open opens a
    # knowledge_search result; records:guide returns one verb's worked example).
    **_not(_READS, "knowledge_open", "records:guide"),
    **_not(_COMPOSITE, "data_action:create_note_in_project", "data_action:create_task_in_project",
           "data_action:transcript_to_note"),
    **_not(_READS, "data_action:catalog", "data_action:read_file_extraction", "data_action:resolve_contact"),
    **_not(_REMOVES, "workflow_plan:retire", "note:delete", "task:delete", "memory:forget", "cloud_file:delete", "cloud_file:batch_delete",
           "cms_asset:delete", "cms_collection:delete", "cms_collection:archive", "cms_component:delete",
           "cms_data:delete", "cms_page:delete", "cms_site:delete", "cms_site:redirect_delete",
           "content_plan:delete_node", "dictionary:delete_entries", "html_page:delete",
           "records:record_delete", "data:delete", "db_admin:delete", "db_user:delete", "sql:delete",
           "instance_delete"),
    **_not(_LIFECYCLE, "workflow_plan:settle", "cms_page:publish", "cms_page:publish_many",
           "kind_activate", "rulebook:retire_rule", "rulebook:retire_rules",
           "topical_map:retire"),
    **_not(_EXTERNAL, *(f"cloud_browser:{a}" for a in (
        "click", "close", "create_profile", "dismiss_handoff", "get_element", "list_local_devices", "list_profiles", "navigate",
        "screenshot", "scroll", "select_option", "start_local", "type_text", "wait_for")),
           "notify_me:send", "send_text", "send_secure_link", "ask_person",
           "agent", "send_message", "mandate_call", "staff_escalate", "credential_login:attempt", "credential_login:auto",
           "credential_login:authenticator", "credential_login:report", "google_workspace:prepare_email",
           "github_repositories:refresh", "seo:collect_rank", "research_run:start", "research_run:schedule",
           "agent_plan:run", "agent_plan:cancel", "workflow_run:run", "workflow_run:cancel", "shell_execute",
           "shell_python", "code_execute_python", "cms_verify:capture", "cms_verify:capture_site",
           "cms_verify:render_check", "page_check:open", "cms_page:submit_exception", "sealed_case:commit", "sealed_case:ask",
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
    "agent_plan:status", "applet:get", "applet:list", "cardsight_identify", "cisco_serial_lookup", "cloud_file:batch_get",
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
    "data:get", "data:query", "db_admin:get", "db_admin:query", "db_admin:schema",
    "db_user:get", "db_user:query", "db_user:schema", "debug_traces_by_call",
    "debug_traces_by_conv", "debug_traces_failures_since", "debug_traces_get_file", "debug_traces_list_files",
    "debug_traces_recent", "desktop_capabilities", "dictionary:fetch_user_content", "dictionary:get_settings",
    "dictionary:list_entries", "dictionary:list_owners", "dictionary:resolve", "document:read",
    "document_content:assets", "document_content:images", "document_content:page_index", "document_content:read",
    "drill:ask", "drill:describe", "drill:rows", "drill:sources",
    "document_search", "errors:get", "errors:list", "errors:metrics",
    "errors:surfaces", "fetch_tool_result", "file_read",
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
    "pick_list:get", "pick_list:list", "random_wheel", "records:entity_read",
    "records:metadata_search", "records:record_aggregate", "records:record_history", "records:record_read",
    "records:schema", "records:table_list", "research_run:bounds", "research_run:status", "research_web",
    "reverse_image_search", "rulebook:read", "rulebook:read_rule", "rulebook_read:get",
    "rulebook_read:list", "rulebook_read:sections", "scope_system:expand_context_item", "scope_system:expand_scope",
    "scope_system:expand_scope_type", "scope_system:list_organizations", "scope_system:overview", "sealed_case:ledger", "seo:check_batch",
    "seo:check_descriptions", "seo:check_titles", "seo:keyword_data", "skill:get",
    "skill:list", "skill:search", "sql:query", "sql:schema",
    "staff_roster", "storage_source_browse", "storage_source_connections", "task:get",
    "task:list", "text_analyze", "text_regex_extract", "toolcomp_get_code",
    "toolcomp_get_context", "toolcomp_get_incident_detail", "toolcomp_get_sample_detail", "toolcomp_list_tools",
    "topical_map:associations", "topical_map:diagnostics", "topical_map:facet_values", "topical_map:get",
    "topical_map:graph", "topical_map:map_history", "topical_map:map_pages", "topical_map:maps",
    "topical_map:outline", "topical_map:page_intents", "topical_map:search", "topical_map:topic_gaps",
    "topical_map:tree", "upc_lookup", "verify:answer",
    "verify:document", "vsc_get_state", "web:batch_read",
    "web:read", "web:search", "workbook:read", "workflow_author:validate",
    "workflow_catalog:definition_shape", "workflow_catalog:get_node_type", "workflow_catalog:get_workflow", "workflow_catalog:list_models",
    "workflow_catalog:list_node_types", "workflow_catalog:list_workflows", "workflow_node:get_agent", "workflow_node:get_context",
    "workflow_plan:check", "workflow_plan:list", "workflow_plan:read", "workflow_run:status",
    "ximilar_identify",
    ),
    # ---- 2026-11-02 (lane CONVERGE-SURFACES): the actions registered since the last census ----
    **_not(_READS,
           "agent_messages:read", "agent_messages:rooms", "agent_messages:who", "agent_messages:whoami",
           "applet:versions", "attention:list", "computers:list", "conversations:get_item",
           "db_read:bundle", "db_read:find", "db_read:query", "db_read:schema",
           "desktop_apps:list", "desktop_audio:devices", "desktop_browser:read", "desktop_browser:screenshot",
           "desktop_browser:sessions", "desktop_browser:tabs", "desktop_calendar:events", "desktop_calendar:reminders",
           "desktop_clipboard:read", "desktop_contacts:get", "desktop_contacts:search", "desktop_documents:ocr",
           "desktop_documents:pdf_text", "desktop_entities:names", "desktop_entities:private_data",
           "desktop_git:diff", "desktop_git:log", "desktop_git:status", "desktop_location", "desktop_mail:accounts",
           "desktop_mail:list", "desktop_messages:chats", "desktop_messages:list", "desktop_net:bluetooth",
           "desktop_net:devices", "desktop_net:info", "desktop_net:mdns", "desktop_net:scan", "desktop_net:wifi",
           "desktop_notes:folders", "desktop_notes:list", "desktop_notes:read", "desktop_notes:search",
           "desktop_outlook:list", "desktop_outlook:read", "desktop_outlook:status", "desktop_photos:get",
           "desktop_photos:search", "desktop_power:status", "desktop_process:list", "desktop_process:ports",
           "desktop_resources:snapshot", "desktop_schedule:list", "desktop_stack:list", "desktop_stack:logs", "desktop_screen:capture", "desktop_screen:list",
           "desktop_system:info", "desktop_window:list", "desktop_windows_admin:event_log",
           "desktop_windows_admin:features", "desktop_windows_admin:registry_read", "desktop_windows_admin:services",
           "find_tools", "fs_watch:events", "google_marketing:inspect_urls", "google_marketing:read_ga4_report",
           "google_marketing:run_dig_rule", "google_marketing:search_opportunities", "google_marketing:sitemaps_list",
           "google_marketing:sites_list", "kindcomp_preview", "news_brand_context",
           "news_earliest_reports", "outlook:calendar", "outlook:list", "outlook:read", "pdf_compare",
           "pdf_form_fields", "pdf_redact_find", "schedule_wakeup:list",
           "seo_ai_visibility:brand_mentions", "seo_ai_visibility:share_of_voice", "seo_ai_visibility:try_prompt",
           "seo_domain:keyword_gap", "seo_domain:overview", "seo_domain:ranked_keywords",
           "seo_domain:serp_competitors", "seo_keywords:cluster", "seo_keywords:list_saved", "seo_keywords:metrics",
           "seo_keywords:research", "seo_keywords:serp_check", "seo_local:categories", "seo_local:find_business",
           "seo_local:maps_results", "seo_local:posts", "seo_local:profile", "seo_local:questions",
           "seo_local:rank_grid", "seo_local:reviews", "seo_rank:estimate", "seo_rank:scenario", "seo_rank:targets",
           "seo_report:get", "seo_report:list", "seo_report:templates", "seo_site:backlink_profile",
           "seo_site:competitors", "seo_site:context", "seo_site:crawl_status", "seo_site:findings",
           "shell_job:list", "shell_job:output", "site_data", "social_own_account_insights", "social_own_accounts",
           "social_own_comments", "social_own_posts", "spaces:list", "spaces:read", "spend_desk:alarms",
           "spend_desk:approvals", "spend_desk:decisions", "spend_desk:holds", "spend_desk:numbers",
           "spend_desk:settings", "studio_workspace:get", "tables_ai_column:estimate", "tables_ai_column:preview",
           "tables_automation:list", "tables_automation:runs", "tables_dashboard:interface", "tables_dashboard:list",
           "tables_dashboard:run", "tables_discuss:comments", "tables_discuss:followers", "tables_share:find_person",
           "tables_share:who", "tables_snapshot:job", "tables_snapshot:snapshots", "tables_template:installed",
           "tables_template:list", "video_clone:analyze", "video_clone:links", "video_clone:plan", "video_clone:read",
           "video_clone:status", "workbook:find", "workflow_author:dry_run", "workflow_run:step_results"),
    **_not(_CREATES,
           "agent_author", "applet:wire", "attention:file_to_agents", "attention:report", "cloud_browser:save_page",
           "compare", "create_dated_change", "crm_outreach_list_add", "desktop_calendar:create_event",
           "desktop_calendar:create_reminder", "desktop_documents:image_resize", "desktop_documents:office_generate",
           "desktop_schedule:create", "news_monitor_save", "pdf_bates", "pdf_compress", "pdf_convert",
           "pdf_delete_pages", "pdf_extract_pages", "pdf_fill_form", "pdf_find_replace", "pdf_merge", "pdf_ocr",
           "pdf_page_numbers", "pdf_protect", "pdf_redact_apply", "pdf_reorder_pages", "pdf_rotate_pages",
           "pdf_set_bookmarks", "pdf_set_properties", "pdf_split", "pdf_unprotect", "pdf_watermark",
           "schedule_wakeup:schedule", "seo_keywords:save", "seo_keywords:tag", "seo_rank:add_targets",
           "seo_report:save", "seo_site:propose_competitor", "spaces:create", "spend_desk:file_request",
           "studio_workspace:add", "tables_automation:create", "tables_dashboard:add_kind",
           "tables_discuss:comment", "tables_export:csv", "tables_shape:create_base", "tables_snapshot:snapshot",
           "tables_snapshot:snapshot_base", "tables_template:install", "video_clone:create", "video_clone:variants",
           "video_clone:generate", "video_clone:render", "workflow_author:clone_template",
           "workflow_author:save_as_template", "workflow_author:trigger_create"),
    **_not(_REMOVES,
           "attention:resolve", "seo_keywords:remove_saved",
           "seo_rank:remove_targets", "seo_site:dismiss_competitor", "spaces:archive", "studio_workspace:remove",
           "tables_automation:archive", "tables_shape:archive_column", "tables_shape:archive_table",
           "tables_template:clear_samples", "tables_template:uninstall", "workflow_author:archive",
           "workflow_author:trigger_delete", "desktop_schedule:cancel", "schedule_wakeup:cancel"),
    **_not(_UNARCHIVES,
           "tables_automation:restore", "tables_shape:restore_table", "tables_template:restore",
           "workflow_author:unarchive"),
    **_not(_LIFECYCLE,
           "attention:escalate", "attention:reclassify", "spend_desk:decide_approval", "spend_desk:decide_hold",
           "spend_desk:pause_automation", "spend_desk:resume_automation", "spend_desk:resolve_alarm",
           "spend_desk:snooze_alarm", "tables_automation:disable", "tables_automation:enable",
           "tables_discuss:resolve", "workflow_author:publish", "workflow_author:trigger_off",
           "workflow_author:trigger_on"),
    **_not(_PROPOSES,
           "records:field_convert", "records:template_propose", "records:view_propose"),
    **_not(_EXTERNAL,
           "agent_messages:reply", "agent_messages:send", "computers:start_coding", "conversations:background_work",
           "desktop_apps:open", "desktop_audio:play", "desktop_audio:record", "desktop_automation",
           "desktop_browser:call", "desktop_browser:click", "desktop_browser:close", "desktop_browser:navigate",
           "desktop_browser:type", "desktop_clipboard:write", "desktop_git:add", "desktop_git:branch",
           "desktop_git:clone", "desktop_git:commit", "desktop_git:pull", "desktop_git:push", "desktop_git:stash",
           "desktop_input:hotkey", "desktop_input:mouse_click", "desktop_input:mouse_move", "desktop_input:type_text",
           "desktop_mail:send", "desktop_messages:send", "desktop_net:download", "desktop_notes:write",
           "desktop_outlook:draft", "desktop_power:prevent_sleep", "desktop_process:kill", "desktop_stack:start", "desktop_stack:stop", "desktop_system:notify",
           "desktop_system:open_path", "desktop_system:open_url", "desktop_transcribe", "desktop_web:browser_fetch",
           "desktop_web:fetch", "desktop_web:research", "desktop_web:scrape", "desktop_web:search",
           "desktop_window:focus", "desktop_window:minimize", "desktop_window:move",
           "desktop_windows_admin:registry_write", "desktop_windows_admin:service_control", "fs_watch:start",
           "fs_watch:stop", "google_marketing:sitemaps_delete", "google_marketing:sitemaps_submit",
           "news_monitor_run", "outlook:draft", "seo_rank:check_now", "seo_site:start_crawl",
           "session_offer", "session_start", "session_withdraw", "shell_job:start", "shell_job:stop",
           "social_own_account_refresh", "tables_automation:run", "workbook:google_push",
           "workflow_author:manual_result", "workflow_author:rerun_from", "workflow_author:retry_step",
           "workflow_author:skip_step", "workflow_author:step_run", "workflow_author:test_step",
           "workflow_author:trigger_fire"),
    **_not(_SESSION, "load_tools", "use_tool"),
    **_not("controls a running conversation or job (stop, cancel, resume); no stored content changes",
           "conversations:cancel", "conversations:pause", "conversations:resume", "conversations:stop"),
    **_not(_READS, "crm_outreach_history"),
    **_not("changes who can open an item (a share); the item's content is unchanged",
           "data_action:share_with_everyone", "tables_share:grant", "tables_share:remove"),
    **_not("follows or unfollows a record's discussion for notices; no content changes",
           "tables_discuss:follow", "tables_discuss:unfollow"),
    **_not("changes an admin spend-control setting (operations), not a person's content", "spend_desk:set_setting"),
    **_not("changes an Applet through the builder; every save is a version in app.definition_version the person can "
           "restore, so the prior content is never lost", "applet:edit", "applet:restore"),
    **_not("saves a Space page through the Spaces store; every save is a page snapshot the person can restore from "
           "the page's history", "spaces:save", "records:page_write"),
    **_not("the Studio assistant's working fields for THIS conversation, merged key by key and drawn live by the "
           "Studio card; a field the person edited is theirs and the tool refuses to overwrite it",
           "studio_workspace:set", "studio_workspace:update"),
    **_not("changes a video project through its one versioned patch path (base_version); each change is a new "
           "version of the project", "video_clone:edit", "video_clone:patch"),
    **_not("changes a table's structure (a column's or a table's name, where a base sits); no row values or text are "
           "overwritten", "tables_shape:rename_column", "tables_shape:rename_table", "tables_shape:move_base"),
    **_not("changes an automation's rule (the Tables screen's own Edit); no row values or text are overwritten",
           "tables_automation:update"),
    **_not("moves an installed template to its newer version through custom.template_upgrade, which rolls back "
           "whole on failure; rows the person entered are kept", "tables_template:upgrade"),
    **_not("puts a table back to a snapshot the person names (the Tables screen's own Restore)",
           "tables_snapshot:restore", "tables_snapshot:restore_base"),
    **_not("runs an AI column over rows (the Tables screen's Fill); estimate and preview show what it will write "
           "first", "tables_ai_column:fill"),
    **_not(_READS, "deck:read", "workbook:describe_sheet"),
    **_not("changes how a table's rows are drawn (the kind bound to each row); no row value or text changes, and "
           "the binding is reversible", "tables_shape:show_rows_as"),
    **_not(_CREATES, "deck:create"),
    **_not("changes a table's access level (Confidential or Organization) with a recorded reason; no row values "
           "or text change", "tables_share:set_confidential", "tables_share:set_organization"),
    **_not("changes a column in place (its type, or who can see its values); apply=false previews what converts "
           "and a value that does not convert is kept with its row, so nothing is overwritten",
           "tables_shape:retype_column", "tables_shape:set_sensitivity", "tables_shape:set_required"),
    **_not("patches an artifact by writing a NEW version of it (history is never rewritten); the prior version stays",
           "edit_artifact"),
    **_not("copies rows from a connected source (Notion, a data source); dry_run shows the field-level diff first "
           "and a row changed on both sides keeps the person's version", "records:data_sync", "records:notion_sync"),
    # ── classified 2026-11-10 (C117): these tools shipped without a row, so the guard had been red ──────────────
    **_not(_EXTERNAL, "coding_sessions_drive:account_continue", "coding_sessions_drive:agent_set", "coding_sessions_drive:folders_create", "coding_sessions_drive:options_set", "coding_sessions_drive:prefs_set", "coding_sessions_drive:queue_change", "coding_sessions_drive:reconcile", "coding_sessions_drive:send", "coding_sessions_drive:start", "coding_sessions_drive:stop", "coding_sessions_drive:stop_elsewhere", "coding_sessions_drive:takeover"),
    **_not(_READS, "coding_sessions_read:activity", "coding_sessions_read:agents_access", "coding_sessions_read:assets_get", "coding_sessions_read:assets_list", "coding_sessions_read:discover", "coding_sessions_read:folders_check", "coding_sessions_read:folders_recent", "coding_sessions_read:history", "coding_sessions_read:item_full", "coding_sessions_read:prefs", "coding_sessions_read:providers", "coding_sessions_read:runs", "coding_sessions_read:search", "coding_sessions_read:sessions", "coding_sessions_read:titles_status", "coding_sessions_read:transcript"),
    **_not(_CREATES, "credential_login:create_generated", "understanding:start"),
    **_not(_SESSION, "understanding:open", "records:conversation_bind", "records:conversation_unbind"),
    **_not("applies a table maker's waiting changes to this organization's copy of the table (a dropped column is "
           "retired, never deleted; a retype keeps a value that does not convert with its row); no row values or text "
           "are overwritten", "understanding:update_tables"),
    **_not("sets this conversation's agent mode (one key of its settings, the same one the person's mode menu sets); "
           "no content changes", "set_mode"),
    **_not(_READS, "desktop_action_needed:get", "desktop_action_needed:list", "desktop_action_needed:wait",
           "desktop_process:sample", "desktop_resources:processes", "desktop_semantic_find:search",
           "desktop_semantic_find:status", "understanding:entries", "understanding:status"),
    **_not(_EXTERNAL, "desktop_action_needed:cancel", "desktop_action_needed:raise", "desktop_process:signal",
           "desktop_stack:restart", "page_check:press"),
    # ── classified 2026-11-10 (C117 round 2): Action tool doors the guard sees once configure_packages has loaded them ──
    **_not(_CREATES, "api_connector_create", "api_endpoint_create"),
    **_not("edits an API connector's or endpoint's declared settings (name, URL, auth kind, fields); the person reads "
           "them on the connector page and a secret is never displayed, so there is nothing to diff",
           "api_connector_update", "api_endpoint_update"),
    **_not(_REMOVES, "api_connector_delete", "api_endpoint_delete"),
    **_not(_READS, "api_connector_list"),
    **_not(_EXTERNAL, "api_connector_test"),
    **_not("mints a one-minute private preview link for a port on a Cloud Computer the person may use; nothing stored changes",
           "cloud_computer_preview_link"),
    # ── classified 2026-11-10 (C117 round 3): tool doors of Actions, seen only once the whole suite has loaded them ──
    **_not(_READS, "list_agents", "org_section_list", "org_section_resolve"),
    **_not("creates a custom section of the company address or changes a section's settings (path, label, audience, "
           "order, brand); settings, not text, and an agent putting pages live for anyone on the web asks the person first",
           "org_section_save"),
    **_not(_LIFECYCLE, "org_section_hide"),
    **_not("places an item under a section of the company address; the item's own content is untouched",
           "org_section_place"),
    **_not(_REMOVES, "org_section_unplace"),
    **_not("stops a helper agent this conversation started; what it already did is kept", "task_stop"),
    # ── classified 2026-11-13: Action tool doors that join the census once a run has opened them ──
    **_not(_READS, "appointment_list", "appointment_offer", "factcheck_search", "hub_page_source_list",
           "hub_page_source_read", "hub_page_source_versions", "org_member_list", "weather_history",
           "web_google_place_reviews", "brand_voice_measure:check", "brand_voice_measure:extract"),
    **_not("moves one appointment through its status or time (book, approve, cancel, move, check in, complete, no-show); "
           "the client is told and the calendar page shows the result; no text a person owns is overwritten",
           "appointment_book", "appointment_approve", "appointment_cancel", "appointment_move", "appointment_check_in",
           "appointment_complete", "appointment_no_show", "appointment_after_book"),
    **_not("changes a business's booking settings (services, providers, rooms, hours, days off, booking pages) as fields "
           "on the booking screens; settings, not text", "appointment_hours_set", "appointment_page_set",
           "appointment_resource_set", "appointment_service_set", "appointment_time_off_set", "appointments_enable",
           "appointments_import_booking_form"),
    **_not(_EXTERNAL, "appointment_busy_refresh", "appointment_calendar_link"),
    **_not("changes a membership plan a business sells (name, price, benefits) or takes it off sale; settings, not text",
           "membership_plan_set"),
    **_not("saves a company page file to its DRAFT only; the site changes on publish, and every publish is a version in "
           "the page's History the person can restore", "hub_page_source_edit", "hub_page_source_write"),
    **_not(_LIFECYCLE, "hub_page_source_publish", "hub_page_source_restore", "hub_page_discard_draft"),
    **_not("starts a draft of a page file copied from the platform file the address draws; nothing on the site changes",
           "hub_page_start"),
    **_not("changes who is in the organization or their role (invite, remove, set role); the Members page shows it, and "
           "the database decides who may in its own sentence", "org_member_invite", "org_member_remove",
           "org_member_set_role"),
    # ── classified 2026-11-13: the Vault's chat tool and the Applet job door ──
    **_not(_READS, "vault:find"),
    **_not("asks the person to type the values on a private capture page and parks until they answer; the agent writes "
           "no value and sees field names only", "vault:add"),
    **_not("renames, re-tags or re-describes one vault item (settings, not text a person owns, and never a secret "
           "value); the answer names what changed", "vault:organize"),
    **_not(_PROPOSES, "vault:setup_code", "vault:share"),
    **_not("attaches an AI job (an agent or workflow the organization already owns, or a new one the builder makes) to "
           "an Applet's page wiring; the Applet's files are untouched", "applet:job"),
    # ── classified 2026-11-13: every Action tool door the server opens at startup (the full census, loaded the same way alone or in a suite) ──
    **_not(_READS,
           "cerbo_get_patient", "cerbo_list_appointments", "cerbo_list_changes", "cerbo_list_encounters",
           "cerbo_search_patients", "custom_automation_revisions", "custom_dashboards", "custom_doc_templates",
           "custom_enrich_due", "custom_field_history", "custom_field_update_rehoming_choices",
           "custom_form_look_options", "custom_form_results", "custom_forms", "custom_formula_parse",
           "custom_formula_preview", "custom_interface_read", "custom_portals", "custom_query_record_as_of",
           "custom_read_records_matching", "custom_record_aggregate_as_of", "custom_record_history",
           "custom_record_restore_preview", "custom_record_values_versioned", "custom_subscription_preview",
           "custom_table_homes_named", "custom_table_webhooks", "custom_views", "google_email_search",
           "hub_contact_read", "hub_menu_read", "hub_my_things_read", "hub_page_preview", "hub_page_resolve",
           "hub_page_source_options", "hub_section_items", "hub_shared_list", "hub_site_pages", "hub_site_wizard_read",
           "hub_tree_read", "hub_unsorted_list", "mail_analytics_campaign_metrics",
           "mail_analytics_report_exports_list", "mail_audience_analytics", "mail_audience_contact_activity",
           "mail_audience_contact_get", "mail_audience_contacts_counts", "mail_audience_top_locations", "mail_audience_contacts_list",
           "mail_audience_exports_list", "mail_audience_groups_list", "mail_audience_preferences_page_get",
           "mail_audience_screens_get", "mail_audience_settings_get", "mail_audience_tags_list",
           "mail_bring_over_history", "mail_campaign_recipients", "mail_campaign_rss_feed_preview", "mail_flow_check",
           "mail_flow_contacts", "mail_flow_report", "mail_flow_templates", "mail_manager_list", "mail_read_thread",
           "mail_search", "mail_segment_evaluate", "mail_segment_list", "mail_send_setup", "news_freshness_check",
           "news_search", "news_story_size", "org_slug_check", "org_team_hr_department_options", "org_team_list",
           "org_team_members", "social_outliers", "space_page_read", "table_aggregate", "table_ai_column_estimate",
           "table_airtable_bases", "table_airtable_preview", "table_automation_app_trigger_terms",
           "table_automation_list", "table_automation_runs", "table_base_job", "table_columns",
           "table_dashboard_interface", "table_dashboard_list", "table_dashboard_run", "table_discuss_followers",
           "table_export_csv", "table_list", "table_schema", "table_row_back_links", "table_row_comments", "table_row_get",
           "table_row_list", "table_row_template_list", "table_share_find_person", "table_share_who",
           "table_snapshot_job", "table_snapshot_snapshots", "table_synced_google_sheets", "table_synced_preview",
           "table_synced_refresh_choices", "table_synced_status", "table_synced_test", "table_template_installed",
           "table_template_list", "workbook_agent_changes", "workflow_graph_lay_out"),
    **_not(_CREATES,
           "custom_anon_token_issue", "custom_base_copy_finish", "custom_copy_table_extras", "custom_doc_render_body",
           "custom_doc_render_document", "custom_field_duplicate", "custom_table_duplicate",
           "custom_table_template_declare", "hub_page_create", "mail_audience_contact_note_add",
           "mail_audience_create", "mail_audience_tags_create", "mail_campaign_replicate", "mail_flow_create",
           "mail_save_draft", "org_team_create", "table_automation_create", "table_comments_import", "table_create",
           "table_row_comment", "table_row_create", "table_shape_create_base", "table_synced_connect",
           "table_synced_connect_app", "table_synced_connect_google_sheet", "table_synced_import_once",
           "table_synced_insert_row", "table_template_install", "workbook_from_table", "workbook_to_table"),
    **_not("makes a NEW file or export (a CSV, a ZIP, a filled PDF) or saves PDF content as new rows; nothing already stored is replaced, and a PDF save first answers with its mapping",
           "custom_io_export", "mail_analytics_report_export", "mail_audience_export", "pdf_fill_form_from_record",
           "pdf_form_to_record", "pdf_tables_to_records"),
    **_not("copies a table or base into a NEW one (snapshot, restore as new, or a move done as a server job); nothing is overwritten",
           "table_base_move", "table_base_restore_job", "table_base_snapshot_job", "table_snapshot_restore",
           "table_snapshot_restore_base", "table_snapshot_snapshot", "table_snapshot_snapshot_base"),
    **_not(_EXTERNAL,
           "custom_doc_sign", "custom_portal_invite", "custom_portal_invite_many",
           "mail_audience_contact_event_add",  # records the event, then can start a flow that mails the contact
           "mail_audience_contacts_email_profile_link", "mail_audience_contacts_resend_confirmation",
           "mail_analytics_snapshot_email",  # mails a saved comparative snapshot to the typed addresses
           "mail_campaign_ab_pick_winner", "mail_campaign_resend",
           "mail_campaign_rss_start", "mail_campaign_schedule", "mail_flow_add_contacts",
           "mail_manager_touchpoint_schedule", "mail_reply", "mail_send", "mail_webhook_post", "social_ads_search",
           "social_analyze_post", "social_fetch_post", "social_fetch_profile", "social_search",
           "table_automation_app_trigger_check", "table_automation_app_trigger_sync", "table_automation_run",
           "table_automation_run_script", "workflow_graph_start_run"),
    **_not("runs an AI column over rows (the Tables screen's Fill); the preview shows what it will write first",
           "table_ai_column_run"),
    **_not("copies rows from a connected source (Airtable, Notion, a sheet or another table); a row changed on both sides keeps the person's version",
           "table_airtable_sync", "table_notion_move", "table_synced_refresh"),
    **_not(_LIFECYCLE,
           "custom_anon_publish", "custom_anon_token_revoke", "custom_form_archive", "custom_portal_archive",
           "custom_portal_revoke", "custom_table_webhook_archive", "hub_page_archive", "hub_page_go_live",
           "mail_audience_contacts_archive", "mail_campaign_pause", "mail_flow_pause_step", "mail_flow_set_state",
           "org_team_archive", "table_archive", "table_archive_job", "table_automation_archive", "table_automation_disable",
           "table_automation_enable", "table_base_snapshot_schedule", "table_column_archive", "table_row_archive",
           "table_synced_auto_refresh", "table_view_archive", "workflow_graph_publish"),
    **_not(_UNARCHIVES,
           "custom_dashboard_restore", "custom_doc_render_restore", "custom_doc_template_restore",
           "custom_form_restore", "custom_portal_restore", "mail_audience_contacts_unarchive",
           "table_automation_restore", "table_restore_job", "table_row_restore", "table_shape_restore_table", "table_template_restore",
           "table_view_restore"),
    **_not(_REMOVES,
           "custom_dashboard_delete", "custom_doc_render_delete", "custom_doc_template_delete", "custom_inbox_clear",
           "custom_io_import_forget", "hub_page_unfile", "hub_page_unplace", "mail_audience_contact_note_delete",
           "mail_audience_contacts_delete", "mail_audience_fields_delete", "mail_audience_tags_delete",
           "mail_campaign_delete", "mail_campaign_folder_delete", "mail_flow_delete", "mail_flow_remove_contacts",
           "mail_manager_delete", "mail_manager_touchpoint_delete", "mail_segment_delete",
           "mail_template_folder_delete", "org_team_member_remove", "table_share_remove", "table_synced_delete_row",
           "table_template_clear_samples", "table_template_uninstall"),
    **_not("changes stored record values through the records store; every earlier value stays in the record's history and restores from it, and a stale write is refused",
           "custom_automation_revision_restore", "custom_autonumber_backfill", "custom_checklist_start",
           "custom_checklist_step_complete", "custom_enrich_pin", "custom_field_restore", "custom_pipeline_move",
           "custom_record_reparent", "custom_record_restore_version", "custom_record_update",
           "custom_table_row_defaults_apply", "custom_value_restore", "table_row_update", "table_row_upsert",
           "table_synced_write_cell", "workbook_undo_agent_change"),
    **_not("settles an item a person was asked about (approve or reject a held change, a form review) or parks an inbox item; the inbox shows the result",
           "custom_form_review_decide", "custom_inbox_snooze", "custom_work_approval_decide", "custom_work_decide_many"),
    **_not(_SECRET,
           "custom_form_set_password"),
    **_not("changes who may open a table, or where it lives (Confidential, Organization, one person, one workspace), with the Share dialog showing and undoing it; no row value or text changes",
           "custom_table_move", "custom_table_share_outside_grant", "table_set_confidential", "table_set_organization",
           "table_share_grant", "table_typed_make_confidential"),
    **_not("changes a column in place (its type, who can see it, whether it is required, or a split, merge or extraction); a preview shows what converts, values that do not convert are kept, and the migration can be undone",
           "custom_migrate_extract_parent", "custom_migrate_merge", "custom_migrate_retype", "custom_migrate_split",
           "custom_migrate_undo", "table_column_required", "table_column_retype", "table_column_sensitivity"),
    **_not("runs one step of a table import, which makes new rows or a new table; nothing already stored is replaced",
           "custom_io_import_begin", "custom_io_import_declare_columns", "custom_io_import_finish",
           "custom_io_import_plan", "custom_io_import_rows"),
    **_not("puts a person on a team or changes their role; the team page shows it, and the database decides who may in its own sentence",
           "org_team_member_add", "org_team_member_invite"),
    **_not("changes a contact's fields, tags, groups or consent through the audience's own doors (the one consent door refuses with words); the contact page shows the result",
           "mail_audience_contact_add", "mail_audience_contact_change_email", "mail_audience_contact_update", "mail_audience_contact_vip",
           "mail_audience_combine", "mail_audience_contacts_set_subscription", "mail_audience_fields_save", "mail_audience_groups_save",
           "mail_audience_subscribe", "mail_audience_tag", "mail_audience_tags_apply", "mail_audience_unsubscribe",
           "mail_audience_unsubscribe_emails"),
    **_not("edits a mailing record (a draft campaign, flow, form, segment, touchpoint, folder, label or audience setting) the Mail screens show; a sent campaign is never changed",
           "mail_audience_archive", "mail_audience_preferences_page_set", "mail_audience_reorder",
           "mail_audience_restore", "mail_audience_screens_save",
           "mail_audience_settings_save", "mail_campaign_folder_save", "mail_campaign_move", "mail_campaign_save",
           "mail_flow_save", "mail_form_save", "mail_label", "mail_manager_optimize_dates", "mail_manager_save",
           "mail_manager_touchpoint_save", "mail_move", "mail_segment_save", "mail_segment_save_from_report",
           "mail_template_folder_save", "mail_template_move"),
    **_not("writes a company page file as a DRAFT only; the site changes on publish, and every earlier version stays in the page's History to restore",
           "hub_site_wizard_apply", "hub_template_reset"),
    **_not("opens one new deal in the organization's CRM (and finds or adds the one contact it is with); new rows, nothing replaced",
           "crm_deal_create"),
    **_not("writes rows of the organization's Import reports (what an import carried over); new rows, nothing replaced",
           "table_import_run_record"),
    **_not("reads an import's standing report; the rows it adds first are the importer's own notes, new rows, nothing replaced",
           "table_import_report"),
    **_not("runs one statement on the person's own custom tables, as them, through the records store (the Tables screen's SQL box); a read answers rows, a write is the person's own",
           "table_sql"),
    **_not("edits a workflow's DRAFT graph through checked operations; publishing is a separate act and every published version stays to restore",
           "workflow_graph_apply_ops", "workflow_graph_create"),
    **_not("changes the declared settings of a table, a screen or the company site (columns, views, forms, dashboards, portals, webhooks, automations, addresses, menus, organization and team details) as fields the screen itself shows; settings, not text a person owns",
           "crm_deal_pipeline_save", "custom_action_declare", "custom_booking_declare", "custom_dashboard_declare",
           "custom_doc_template_save", "custom_enrich_declare", "custom_field_notify_on_assign", "custom_field_update",
           "custom_form_declare", "custom_form_knobs", "custom_grid_layout", "custom_history_retention_floor_raise",
           "custom_history_retention_set", "custom_inbound_declare", "custom_inbound_set", "custom_pipeline_declare",
           "custom_portal_card", "custom_portal_declare", "custom_record_row_controls_set",
           "custom_set_table_locked_rows_show_submitted", "custom_subscription_mute", "custom_table_copy_sync",
           "custom_table_decorate", "custom_table_row_defaults_set", "custom_table_row_label_set",
           "custom_table_webhook_declare", "custom_view_declare", "custom_view_designate", "custom_view_look_set",
           "custom_view_record_order_set", "hub_addresses_ensure", "hub_contact_set", "hub_page_address",
           "hub_page_change_source", "hub_page_file", "hub_page_menu", "hub_page_nest", "hub_page_place",
           "hub_page_reorder", "hub_site_ensure", "hub_starters_ensure", "hub_template_set", "org_identity_set",
           "org_slug_change", "org_team_address_set", "org_team_hr_department_set", "org_team_rename",
           "table_automation_update", "table_column_add", "table_column_rename", "table_column_settings",
           "table_dashboard_add_kind", "table_discuss_follow", "table_discuss_resolve", "table_discuss_unfollow",
           "table_favorite", "table_relation_add", "table_row_template_save", "table_shape_move_base",
           "table_shape_show_rows_as", "table_synced_repoint_app", "table_template_upgrade", "table_view_save",
           "workbook_refresh_from_table"),
    **_not(_READS,
           "actions_find",
           "calendar_events_read",
           "calendar_free_busy",
           "calendar_list",
           "coding_sessions_read:recent_seen",
           "coding_sessions_read:session_watch",
           "db_read:definition",
           "mail_account_standing",
           "mail_audience_webhooks_list",
           "mail_campaign_preview",
           "mail_campaign_recipient_count",
           "mail_campaign_send_checklist",
           "notices_read:alarm",
           "notices_read:alarms",
           "notices_read:child_runs",
           "notices_read:spend",
           "notices_read:texts",
           "platform_request_follow_up:status",
           "project:get",
           "project:list",
           "cerbo_describe_change:create_appointment",
           "cerbo_describe_change:create_appointment_type",
           "cerbo_describe_change:create_email_appointment_reminder",
           "cerbo_describe_change:create_encounter",
           "cerbo_describe_change:create_inventory",
           "cerbo_describe_change:create_patient",
           "cerbo_describe_change:create_patient_blood_pressure_vital",
           "cerbo_describe_change:create_patient_custom_vital",
           "cerbo_describe_change:create_patient_document",
           "cerbo_describe_change:create_patient_facility",
           "cerbo_describe_change:create_patient_health_maintenance",
           "cerbo_describe_change:create_patient_height_vital",
           "cerbo_describe_change:create_patient_image",
           "cerbo_describe_change:create_patient_questionnaire",
           "cerbo_describe_change:create_patient_specialist",
           "cerbo_describe_change:create_patient_weight_vital",
           "cerbo_describe_change:create_secure_message",
           "cerbo_describe_change:create_sms_appointment_reminder",
           "cerbo_describe_change:create_supplement",
           "cerbo_describe_change:create_tag",
           "cerbo_describe_change:create_task",
           "cerbo_describe_change:delete_appointment",
           "cerbo_describe_change:delete_encounter",
           "cerbo_describe_change:delete_patient",
           "cerbo_describe_change:delete_patient_facility",
           "cerbo_describe_change:delete_patient_specialist",
           "cerbo_describe_change:delete_patient_tag",
           "cerbo_describe_change:delete_portal_request",
           "cerbo_describe_change:delete_tag",
           "cerbo_describe_change:discontinue_patient_prescription",
           "cerbo_describe_change:discontinue_patient_supplement",
           "cerbo_describe_change:invite_to_portal",
           "cerbo_describe_change:queue_patient_prescription",
           "cerbo_describe_change:queue_patient_supplement",
           "cerbo_describe_change:refill_patient_prescription",
           "cerbo_describe_change:send_patient_email",
           "cerbo_describe_change:update_appointment",
           "cerbo_describe_change:update_inventory",
           "cerbo_describe_change:update_patient",
           "cerbo_describe_change:update_patient_note",
           "cerbo_describe_change:update_patient_tags",
           "cerbo_describe_change:update_supplement",
           "cerbo_describe_change:update_tag",
           "cerbo_describe_change:update_task",
           "cerbo_describe_change:validate_portal_credentials",
           "cerbo_describe_change:validate_user_credentials",
           "cerbo_export_patient_tags",
           "cerbo_get_record",
           "cerbo_list_records",
           "cerbo_patient_records"),
    **_not(_CREATES,
           "calendar_event_create",
           "orchestra_create",
           "org_chart_create_position",
           "project:create",
           "study_cards",
           "study_explain_card",
           "study_grade_spoken",
           "study_make_deck",
           "study_make_quiz",
           "study_plan",
           "board_add_tile",
           "map_add_box",
           "orchestra_add_member",
           "orchestra_add_seat"),
    **_not(_REMOVES,
           "calendar_event_delete",
           "mail_campaign_archive",
           "mail_template_archive",
           "mail_audience_webhooks_archive",
           "orchestra_archive",
           "orchestra_remove_member",
           "orchestra_remove_seat",
           "org_chart_remove_position",
           "board_remove_tile",
           "map_delete"),
    **_not(_UNARCHIVES,
           "calendar_event_restore",
           "orchestra_restore",
           "org_chart_restore_position"),
    **_not(_EXTERNAL,
           "actions_run",
           "api_connector_authorize_start",
           "notify_webhook",
           "platform_submit_request",
           "platform_request_follow_up:add",
           "mail_audience_webhooks_test",
           "table_button_press",
           "table_import_file_job",
           "table_synced_connect_job",
           "table_synced_job",
           "table_synced_refresh_job",
           "table_synced_stop_job",
           "staff_ask",
           "cerbo_change:create_appointment",
           "cerbo_change:create_appointment_type",
           "cerbo_change:create_email_appointment_reminder",
           "cerbo_change:create_encounter",
           "cerbo_change:create_inventory",
           "cerbo_change:create_patient",
           "cerbo_change:create_patient_blood_pressure_vital",
           "cerbo_change:create_patient_custom_vital",
           "cerbo_change:create_patient_document",
           "cerbo_change:create_patient_facility",
           "cerbo_change:create_patient_health_maintenance",
           "cerbo_change:create_patient_height_vital",
           "cerbo_change:create_patient_image",
           "cerbo_change:create_patient_questionnaire",
           "cerbo_change:create_patient_specialist",
           "cerbo_change:create_patient_weight_vital",
           "cerbo_change:create_secure_message",
           "cerbo_change:create_sms_appointment_reminder",
           "cerbo_change:create_supplement",
           "cerbo_change:create_tag",
           "cerbo_change:create_task",
           "cerbo_change:delete_appointment",
           "cerbo_change:delete_encounter",
           "cerbo_change:delete_patient",
           "cerbo_change:delete_patient_facility",
           "cerbo_change:delete_patient_specialist",
           "cerbo_change:delete_patient_tag",
           "cerbo_change:delete_portal_request",
           "cerbo_change:delete_tag",
           "cerbo_change:discontinue_patient_prescription",
           "cerbo_change:discontinue_patient_supplement",
           "cerbo_change:invite_to_portal",
           "cerbo_change:queue_patient_prescription",
           "cerbo_change:queue_patient_supplement",
           "cerbo_change:refill_patient_prescription",
           "cerbo_change:send_patient_email",
           "cerbo_change:update_appointment",
           "cerbo_change:update_inventory",
           "cerbo_change:update_patient",
           "cerbo_change:update_patient_note",
           "cerbo_change:update_patient_tags",
           "cerbo_change:update_supplement",
           "cerbo_change:update_tag",
           "cerbo_change:update_task",
           "cerbo_change:validate_portal_credentials",
           "cerbo_change:validate_user_credentials"),
    **_not("changes the declared settings or layout of an item a screen shows as fields (a calendar event's time or answer, a board or map layout, an org chart or orchestra seat, a table's name or template, a webhook, an appointment setting); settings, not text a person owns, and the screen shows the result",
           "appointment_client_rename",
           "appointment_providers_link_hr",
           "appointment_zone_set",
           "board_connect",
           "board_move_tile",
           "board_update_tile",
           "calendar_event_move",
           "calendar_event_respond",
           "calendar_event_update",
           "mail_audience_webhooks_save",
           "map_connect",
           "map_group",
           "map_move",
           "map_update_box",
           "orchestra_move",
           "orchestra_reorder",
           "orchestra_set_config",
           "orchestra_set_member",
           "orchestra_set_member_context",
           "org_chart_link",
           "org_chart_place_under",
           "org_chart_unlink",
           "org_chart_update_position",
           "project:update",
           "table_rename",
           "table_synced_release_edit",
           "table_template_publish_version",
           "tables_template:publish_version",
           "topical_map:layout"),
}
