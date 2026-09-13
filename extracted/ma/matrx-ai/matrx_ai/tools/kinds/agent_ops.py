"""Kinds for the aidream-hosted agent-ops tool results: ``self_prompt`` ·
``rulebook`` · ``research_run`` · ``office`` (KIND_TOOL_LEDGER, ``lead-w2f``).
Implementations live in aidream (`services/agent_self_prompt/tools.py`,
`services/distillation/tools.py`, `tools/research_tool.py`,
`services/office_generation/tools.py`); the models live HERE because
``TOOL_RESULT_KINDS`` may never import aidream.

WHY ``office`` DOES NOT BIND ``office_file_result`` / ``office_extraction_result``:
those ACTIVE workflow_io kinds are the office NODES' payloads, and the tool's
two branches would need BOTH — the executor's one-declared-kind-per-tool law
forbids that, the generate branch adds an ``action`` key neither declares, and
the tool's extract branch is a SUMMARY (``portions`` is a count, no file_id) —
so the tool's receipt union is a genuinely different shape and gets its own
slug, with the overlap recorded here rather than silently twinned.

WHY ``research_run`` IS NOT THE RESEARCH-CONTENT FAMILY: the tool returns the
refresh/run STATE machine (bounds, schedule, status receipts) — the research
REPORT content is the `research_report` family and stays untouched.

All placeholder tier; union rule as everywhere.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind
from pydantic import JsonValue


@kind(
    "self_prompt_result",
    label="Self-Prompt Result",
    family="agent_self_prompt",
    example={"action": "read", "agent_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "key": "voice", "found": True, "content": "Keep it plain.", "available_keys": ["voice"]},
    # PLACEHOLDER — read_full / read / replace / patch over the agent's own
    # self-managed prompt sections.
    maturity="placeholder",
)
class SelfPromptResult(KindModel):
    action: str = ""
    agent_id: str = ""
    #: ``read_full``.
    system_prompt: str | None = None
    keys: list[str] | None = None
    #: ``read`` one section.
    key: str | None = None
    found: bool | None = None
    content: str | None = None
    available_keys: list[str] | None = None
    #: ``replace`` / ``patch`` receipt.
    created: bool | None = None
    section: str | None = None
    note: str | None = None


@kind(
    "rulebook_tool_result",
    label="Rulebook Tool Result",
    family="distillation",
    example={
        "action": "read_rule",
        "rule": {"id": "r-1", "name": "one-copy", "section": "docs", "statement": "One copy of everything.", "severity": "must", "draft": False},
    },
    # PLACEHOLDER — the Scout's read/read_rule/add_rules/update_rule/
    # retire_rule/update_meta/settle_tension union.
    maturity="placeholder",
)
class RulebookToolResult(KindModel):
    action: str = ""
    #: ``read`` — the rulebook header + capped rule views.
    rulebook_id: str | None = None
    name: str | None = None
    description: str | None = None
    status: str | None = None
    version: int | None = None
    #: Measured live: a dict on real rows (provenance object), not a string.
    source: JsonValue | None = None
    sections: JsonValue | None = None
    intake: JsonValue | None = None
    rule_count: int | None = None
    draft_count: int | None = None
    rejected_count: int | None = None
    feedback_count: int | None = None
    rules: list[dict] | None = None
    open_feedback: JsonValue | None = None
    open_tensions: JsonValue | None = None
    description_truncated: bool | None = None
    rules_truncated: bool | None = None
    rules_shown: int | None = None
    #: ``read`` keeps the rule vocabulary complete while paging rule bodies.
    rule_ids: list[str] | None = None
    approved_rule_ids: list[str] | None = None
    rule_index: list[dict] | None = None
    #: Every read page declares whether its vocabulary fragment is complete;
    #: when false, call the opaque ``next_cursor`` exactly as returned.
    vocabulary_complete: bool | None = None
    vocabulary_page_offset: int | None = None
    vocabulary_total_rules: int | None = None
    next_cursor: str | None = None
    rules_bodies_paged: bool | None = None
    rules_paging_note: str | None = None
    intake_truncated: bool | None = None
    #: ``read_rule``.
    rule: dict | None = None
    #: write receipts.
    rule_id: str | None = None
    rulebook_version: int | None = None
    added: list[dict] | None = None
    duplicates_skipped: list[str] | None = None
    rejected: list[str] | None = None
    updated: list[str] | None = None
    #: ``retire_rules`` bulk receipt.
    retired: list[str] | None = None
    refused: list[str] | None = None
    not_found: list[str] | None = None
    refused_note: str | None = None
    not_found_note: str | None = None
    relates_to: JsonValue | None = None
    relations_dropped: int | None = None
    relations_note: str | None = None
    #: ``update_rule`` receipt for a POLICY rule (W58) — the judgment shape that
    #: landed: {kind, precondition, next_action, action_kind, cost, risk}.
    #: Nested deliberately: ``kind`` is the reserved content-IR marker name, so
    #: a top-level receipt field of that name would collide with ``__kind``.
    policy: JsonValue | None = None
    #: ``settle_tension``.
    tension_id: str | None = None
    outcome: str | None = None
    note: str | None = None
    #: A Rulebook receipt is structurally trimmed before it reaches the
    #: universal result gate.  The agent is told exactly what to re-read.
    result_truncated: bool | None = None
    result_truncation_note: str | None = None


@kind(
    "research_run_state",
    label="Research Run State",
    family="research",
    example={"topic_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "Competitor pricing", "status": "idle", "is_running": False, "cost_bounds": {"total_llm_calls": 40}},
    # PLACEHOLDER — bounds/start/status/schedule receipts of the refresh state
    # machine (ResearchRefreshState + per-action receipt fields). NOT the
    # research-report content family.
    maturity="placeholder",
)
class ResearchRunState(KindModel):
    topic_id: str = ""
    name: str = ""
    #: state fields (status/schedule reads).
    status: str | None = None
    is_running: bool | None = None
    updated_at: str | None = None
    refresh_interval_hours: int | None = None
    next_refresh_at: str | None = None
    last_refresh_at: str | None = None
    last_refresh_outcome: str | None = None
    last_refresh_error: str | None = None
    last_refresh_trigger: str | None = None
    consecutive_refresh_failures: int | None = None
    is_claimed: bool | None = None
    keywords_total: int | None = None
    keywords_never_searched: int | None = None
    latest_document_version: int | None = None
    latest_document_at: str | None = None
    cost_bounds: dict | None = None
    execution: dict | None = None
    #: ``bounds``.
    summary: str | None = None
    can_run_unattended: bool | None = None
    #: ``start``.
    started: bool | None = None
    mode: str | None = None
    reason: str | None = None
    hint: str | None = None
    #: ``status``.
    is_complete: bool | None = None
    #: ``schedule``.
    scheduled: bool | None = None


@kind(
    "office_tool_result",
    label="Office Tool Result",
    family="office",
    example={"action": "generate", "file_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "office_kind": "docx", "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "byte_size": 20480},
    # PLACEHOLDER — the generate (FileRef receipt) + extract (markdown summary)
    # union; see the module docstring for the office_file_result reuse verdict.
    maturity="placeholder",
)
class OfficeToolResult(KindModel):
    action: str = ""
    #: ``generate`` — the stored-file receipt (OfficeGenerationResponse).
    file_id: str | None = None
    office_kind: str | None = None
    mime_type: str | None = None
    file_name: str | None = None
    byte_size: int | None = None
    url: str | None = None
    download_url: str | None = None
    cdn_url: str | None = None
    visibility: str | None = None
    #: ``extract`` — the markdown summary (`portions` is a COUNT here).
    markdown: str | None = None
    portions: int | None = None
    warnings: list[str] | None = None


__all__ = ["SelfPromptResult", "RulebookToolResult", "ResearchRunState", "OfficeToolResult"]


@kind(
    "google_workspace_result",
    label="Google Workspace Result",
    family="google_workspace",
    example={"created": True, "file_id": "1AbC", "name": "Notes", "kind": "google_document", "open_in_google": "https://docs.google.com/…"},
    # PLACEHOLDER — list_resources/create/read/append (Docs), read/write
    # (Sheets) and prepare_email (which NEVER sends) receipts.
    maturity="placeholder",
)
class GoogleWorkspaceResult(KindModel):
    #: `list_resources`.
    resources: list[dict] | None = None
    count: int | None = None
    note: str | None = None
    #: create receipts.
    created: bool | None = None
    file_id: str | None = None
    name: str | None = None
    kind: str | None = None
    open_in_google: str | None = None
    #: document read/append window.
    title: str | None = None
    text: str | None = None
    total_chars: int | None = None
    showing_chars: str | None = None
    has_more: bool | None = None
    next_start_char: int | None = None
    appended: bool | None = None
    #: sheet read/write window.
    tab: str | None = None
    range: str | None = None
    rows: list[list[JsonValue]] | None = None
    row_count: int | None = None
    sheet_size: str | None = None
    next_range_a1: str | None = None
    written: bool | None = None
    #: `prepare_email` — a draft for the HUMAN send step; never sent here.
    sent: bool | None = None
    draft: dict | None = None
    from_email: str | None = None
    next_step: str | None = None


@kind(
    "tool_result_page",
    label="Tool Result Page",
    family="tooling",
    example={"call_id": "call-1", "tool_name": "fs_read", "total_chars": 120000, "retained_chars": 100000, "offset": 0, "returned_chars": 8000, "next_offset": 8000, "has_more": True, "content": "…"},
    # PLACEHOLDER — one paged slice of a prior truncated tool result
    # (fetch_tool_result). NOT the runtime wrapper kind `tool_result`.
    maturity="placeholder",
)
class ToolResultPage(KindModel):
    call_id: str = ""
    tool_name: str | None = None
    total_chars: int = 0
    retained_chars: int = 0
    offset: int = 0
    returned_chars: int = 0
    next_offset: int | None = None
    has_more: bool = False
    content: str = ""
    #: DB-fallback branch only: where the slice came from + the honest cap.
    source: str | None = None
    db_copy_truncated: bool | None = None


@kind(
    "file_extraction_result",
    label="File Extraction Result",
    family="files",
    example={"file_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "file_name": "report.pdf", "has_extraction": True, "mode": "clean", "content": "…", "char_count": 1200, "truncated": False},
    # PLACEHOLDER — `file_read`'s window over a file's EXTRACTED text. NOT the
    # active `file_text_content` kind ({text, bytes_read, local_path} — a raw
    # local read): this shape is the docproc extraction with paging.
    maturity="placeholder",
)
class FileExtractionResult(KindModel):
    file_id: str = ""
    file_name: str | None = None
    mime_type: str | None = None
    processed_document_id: str | None = None
    #: False (with empty content) is a normal answer — never processed.
    has_extraction: bool = False
    mode: str | None = None
    total_pages: int | None = None
    content: str | None = None
    char_count: int | None = None
    truncated: bool | None = None
    #: page-wise reads only.
    pages: list[dict] | None = None
    pages_returned: int | None = None


@kind(
    "content_plan_tool_result",
    label="Content Plan Tool Result",
    family="content_plan",
    example={"node": {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "title": "Pricing"}},
    # PLACEHOLDER — the content_plan dispatcher's union (tree/profile/entity
    # reads, node writes, archetype + CMS bridge branches — the latter wrapped
    # under named keys so foreign service dumps can join this closed shape).
    maturity="placeholder",
)
class ContentPlanToolResult(KindModel):
    #: `get_tree`.
    site_id: str | None = None
    count: int | None = None
    total: int | None = None
    nodes: list[dict] | None = None
    truncation_notice: str | None = None
    #: profile / entity reads.
    profiles: list[dict] | None = None
    entities: list[dict] | None = None
    entity: dict | None = None
    #: node writes.
    node: dict | None = None
    warnings: JsonValue | None = None
    node_id: str | None = None
    deleted: bool | None = None
    #: listings.
    sites: JsonValue | None = None
    archetypes: list[JsonValue] | None = None
    concepts: list[JsonValue] | None = None
    #: wrapped service-dump branches (reshaped 2026-08-26 — see tools.py).
    tagging: JsonValue | None = None
    attachment: JsonValue | None = None
    apply_result: JsonValue | None = None
    instantiation: JsonValue | None = None
    checklist: dict | None = None
    deepening: JsonValue | None = None
    reconciliation: dict | None = None
    alignment: dict | None = None


__all__ += [
    "GoogleWorkspaceResult",
    "ToolResultPage",
    "FileExtractionResult",
    "ContentPlanToolResult",
]


@kind(
    "sealed_case_tool_result",
    label="Sealed Case Tool Result",
    family="masterwork",
    example={
        "action": "ask",
        "case_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "run_scope": "workflow_run:8c1f…",
        "seq": 3,
        "question": "What were her vital signs on arrival?",
        "answer": "Heart rate 34 bpm, blood pressure 104/62, afebrile.",
        "found": True,
        "cost": "low",
        "risk": "low",
        "asked_kind": "ask",
        "disclosures_so_far": 3,
    },
    # PLACEHOLDER — the sealed source's ask / commit / ledger union. The
    # `commit` branch deliberately carries NO correctness field of any kind:
    # the oracle never grades (services/masterworks/sealed_case.py).
    maturity="placeholder",
)
class SealedCaseToolResult(KindModel):
    action: str = ""
    case_id: str = ""
    run_scope: str = ""
    #: ``ask`` — one disclosure.
    seq: int | None = None
    question: str | None = None
    answer: str | None = None
    found: bool | None = None
    cost: str | None = None
    risk: str | None = None
    asked_kind: str | None = None
    #: ``ask`` / ``commit`` receipt. NEVER a verdict.
    disclosures_so_far: int | None = None
    recorded: bool | None = None
    #: ``ledger``.
    disclosures: list[dict] | None = None
    score: dict | None = None


__all__ += ["SealedCaseToolResult"]
