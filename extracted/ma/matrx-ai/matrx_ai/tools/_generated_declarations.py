"""Tool argument contracts — HAND-OWNED (bootstrapped once from the DB).

This module is the code source of truth for tool ARGUMENT SHAPES. Importing
it registers every locally-owned tool into matrx_ai.tools.declared via @tool;
the executor validates incoming args against these models at dispatch, and the
tool-drift gate (aidream/startup/tools_check.py) diffs them against the live
tool_def DB rows and BLOWS UP on any mismatch. The DATABASE is the source of
truth: when code and DB disagree, fix the model here to match the DB.
Edit by hand. `generate_tool_models.py` only re-bootstraps with --force
(it refuses to overwrite otherwise), so this file never silently re-syncs
to the DB behind your back.
"""

from __future__ import annotations

import importlib
from typing import Any, Literal

from pydantic import AliasChoices, Field

from matrx_ai.tools.arg_models import (
    CloudFileArgs,
    ContextArgs,
    ContextPatchArgs,
    DatasetArgs,
    DictionaryArgs,
    FsEditArgs,
    FsListArgs,
    FsMkdirArgs,
    FsReadArgs,
    FsSearchArgs,
    FsWriteArgs,
    MemoryArgs,
    NoteArgs,
    PicklistArgs,
    RagSearchArgs,
    SeoArgs,
    ShellExecuteArgs,
    ShellPythonArgs,
    SkillArgs,
    SqlArgs,
    TaskArgs,
    TextAnalyzeArgs,
    WebArgs,
)
from matrx_ai.tools.declared import NoArgs, ToolArgs, tool


class AgentCallArgs(ToolArgs):
    agent_id: str = Field(description="UUID of the saved agent to run.")
    variables: dict[str, Any] | None = Field(default=None)
    user_input: str | None = Field(default=None)
    settings: dict[str, Any] | None = Field(default=None)
    result_mode: Literal["inline", "reference", "inline_once"] = Field(default="inline")
    result_key: str | None = Field(default=None)
    result_description: str | None = Field(default=None)
    history_mode: Literal["none", "snapshot", "fork"] = Field(default="none")
    history_conversation_id: str | None = Field(default=None)
    history_up_to_position: int | None = Field(default=None)
    remember: bool = Field(default=False)
    remember_visible_to_user: bool = Field(default=False)


class CodeExecutePythonArgs(ToolArgs):
    code_input: str = Field(
        validation_alias=AliasChoices("code_input", "code"),
        description="Python source to execute. The conventional `code` alias is accepted.",
    )
    timeout_seconds: int = Field(default=30)


class CodeFetchCodeArgs(ToolArgs):
    output_mode: Literal["clean", "original", "signatures"] = Field(default="clean")
    project_root: str
    subdirectory: str = Field(default="")


class CodeFetchTreeArgs(ToolArgs):
    project_root: str
    subdirectory: str = Field(default="")
    show_all_directories: bool = Field(default=False)


class CodeStoreHtmlArgs(ToolArgs):
    html_input: str


# context (get|batch|create) + context_patch wire models are the discriminated
# unions ContextArgs / ContextPatchArgs in arg_models.dispatcher_args — the per
# action contract the drift gate diffs against tool_def."$variants". The old flat
# CtxGetArgs / CtxBatchArgs / CtxCreateArgs classes were retired with the legacy
# ctx_* tool rows (migration 0100).


class DebugTracesByCallArgs(ToolArgs):
    call_id: str


class DebugTracesByConvArgs(ToolArgs):
    limit: int = Field(default=500)
    conversation_id: str
    verbose: bool = Field(default=False)


class DebugTracesFailuresSinceArgs(ToolArgs):
    iso_ts: str
    limit: int = Field(default=300)
    verbose: bool = Field(default=False)


class DebugTracesGetFileArgs(ToolArgs):
    filename: str
    offset: int = Field(default=0)
    max_chars: int = Field(default=0)


class DebugTracesRecentArgs(ToolArgs):
    event: Literal["FAIL", "LOOP_BLOCK", "NO_EXECUTOR", "OK", "SURFACE_REJECT"] | None = Field(
        default=None
    )
    limit: int = Field(default=200)
    since: str | None = Field(default=None)
    tool_name: str | None = Field(default=None)
    verbose: bool = Field(default=False)


class FsPatchArgs(ToolArgs):
    path: str
    edits: list
    create_if_missing: bool = Field(default=False)


class GetOpenTraceIncidentsArgs(ToolArgs):
    limit: int = Field(default=20)
    severity: Literal["critical", "high", "low", "medium"] | None = Field(default=None)
    tool_name: str | None = Field(default=None)


class GitIngestArgs(ToolArgs):
    mode: Literal["digest", "summary", "tree"] = Field(default="digest")
    token: str | None = Field(default=None)
    branch: str | None = Field(default=None)
    source: str
    exclude: list | None = Field(default=None)
    include: list | None = Field(default=None)
    max_chars: int = Field(default=50000)
    max_file_size: int = Field(default=1048576)
    include_submodules: bool = Field(default=False)


class LlmsTxtFetchArgs(ToolArgs):
    url: str
    full: bool = Field(default=False)
    max_chars: int = Field(default=50000)


class LoadChromeToolsArgs(ToolArgs):
    # Categories are the matrx-extend tool taxonomy (source of truth:
    # matrx-extend/src/lib/tools/categories.ts ToolCategory). Kept in lockstep
    # with the tool_def `load_chrome_tools` row's parameters.category.enum AND
    # the live `category` column of every chrome-extension-bound tool_def row
    # (what the handler validates against via get_category_names()).
    category: Literal[
        "core",
        "reading",
        "interaction",
        "tabs",
        "capture",
        "chrome",
        "human",
        "memory",
        "ai",
        "demos",
        "guidance",
        "devtools",
        "webmcp",
        "desktop",
    ]


class LoadDesktopToolsArgs(ToolArgs):
    # Categories are the desktop mega-tool taxonomy (source of truth: the
    # `category` column of the 19 matrx-local-bound tool.definition rows;
    # matrx-local/app/tools/actions.py ACTION_GROUPS carries the same values).
    # Kept in lockstep with the tool_def `load_desktop_tools` row's
    # parameters.category.enum.
    category: Literal[
        "desktop",
        "desktop-web",
    ]


class MathCalculateArgs(ToolArgs):
    expression: str


class RandomWheelArgs(ToolArgs):
    mode: Literal["list", "web", "image"] = Field(default="list")
    items: list[dict[str, Any]] = Field(default_factory=list)
    pool: str | None = Field(default=None)
    queries: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    display_count: int = Field(default=18, ge=2, le=28)
    freshness: str | None = Field(default=None)
    title: str = Field(default="")
    avoid: list[str] = Field(default_factory=list)
    dramatize: bool = Field(default=True)


class NewsGetHeadlinesArgs(ToolArgs):
    query: str | None = Field(default=None)
    country: (
        Literal[
            "ar",
            "at",
            "au",
            "be",
            "br",
            "ca",
            "ch",
            "de",
            "eg",
            "es",
            "fr",
            "gb",
            "hk",
            "ie",
            "in",
            "it",
            "jp",
            "kr",
            "mx",
            "nl",
            "no",
            "nz",
            "pl",
            "pt",
            "ru",
            "se",
            "sg",
            "tw",
            "us",
            "za",
        ]
        | None
    ) = Field(default=None)
    sources: str | None = Field(default=None)
    category: (
        Literal["business", "entertainment", "general", "health", "science", "sports", "technology"]
        | None
    ) = Field(default=None)
    language: Literal[
        "ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "zh"
    ] = Field(default="en")


class PackageInfoArgs(ToolArgs):
    name: str
    ecosystem: Literal["npm", "pypi"] = Field(default="pypi")
    max_chars: int = Field(default=20000)
    include_readme: bool = Field(default=True)


class ReportTraceIncidentArgs(ToolArgs):
    category: Literal["A_extension", "B_agent", "C_server", "D_embedded_envelope"] = Field(
        default="C_server"
    )
    err_type: str = Field(default="unknown")
    evidence: list | None = Field(default=None)
    fix_path: str | None = Field(default=None)
    severity: Literal["critical", "high", "low", "medium"] = Field(default="medium")
    tool_name: str
    args_sample: dict | None = Field(default=None)
    last_seen_ts: str | None = Field(default=None)
    ai_complexity: Literal["large", "medium", "small", "trivial", "unknown"] | None = Field(
        default=None
    )
    extra_context: str | None = Field(default=None)
    first_seen_ts: str | None = Field(default=None)
    sample_call_ids: list | None = Field(default=None)
    suspected_cause: str | None = Field(default=None)
    occurrence_count: int = Field(default=1)
    ai_estimated_files: list | None = Field(default=None)
    err_msg_normalised: str
    source_environment: str = Field(default="production")


class ResearchWebArgs(ToolArgs):
    country: str = Field(default="us")
    queries: list
    freshness: Literal["pd", "pm", "pw", "py"] | None = Field(default=None)
    instructions: str
    research_depth: Literal["deep", "medium", "shallow", "very_deep"] = Field(default="medium")


class TextRegexExtractArgs(ToolArgs):
    text: str
    group: int = Field(default=0)
    pattern: str
    find_all: bool = Field(default=True)


class KindCreateArgs(ToolArgs):
    name: str
    label: str
    json_schema: dict | None = Field(default=None)
    sample_data: dict | None = Field(default=None)
    canonical_example: dict | None = Field(default=None)
    description: str | None = Field(default=None)
    title_key: str | None = Field(default=None)
    # 🚨 THE ORDER FOR ANY ADDITIVE TOOL ARG: land the code → deploy → THEN
    # declare it in `tool.definition.parameters` (and cache-bust, or time the
    # write before a restart). The reverse has NO safe window: `tool.definition`
    # is the METADATA authority — it is what the LLM is told the tool accepts —
    # while CODE is the execution authority, so declaring an arg the deployed
    # code cannot accept makes every obedient agent call fail `extra inputs are
    # not permitted` (live incident 2026-08-25, conversation c4317637; a Kind
    # Creator build lost a call to it). Live since the 2026-08-25 03:10 deploy.
    # 🚨 ONE LIST, THREE PLACES — and the model may not be able to say a wrong
    # one. The slugs are the frontend's `KIND_LOADING_SLUGS`
    # (matrx-frontend/features/content-ir/react/loading/kind-loading-slugs.ts);
    # `KIND_LOADING_SLUGS` in tools/implementations/kind_authoring.py mirrors
    # them for the runtime refusal, and matrx-frontend's
    # `pnpm check:loading-slug-twin` fails loudly when the two drift. Declaring
    # them here as a Literal makes the enum reach the LLM through
    # `tool.definition.parameters` (the DB row carries the same enum on the
    # string branch), so an invalid slug is structurally unsayable rather than
    # merely refused after the fact.
    loading_component: (
        Literal[
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
        ]
        | None
    ) = Field(
        default=None,
        description=(
            "Loading-library slug rendered the instant this kind is "
            "identified in a live stream, before its component resolves "
            "(stored as kind_definition.metadata.loading_component). SET IT "
            "on every build — pick the slug whose silhouette matches the "
            "finished component: card, list, table, timeline, chart, deck, "
            "flashcards, quiz, notes, form, media, stat-grid, document, "
            "diagram, chat, gallery, kanban, tree, code, map, progress, "
            "minimal, generic. Unknown slugs are refused."
        ),
    )
    required_fields: list[str] | None = Field(default=None)
    platform_kind: bool = Field(
        default=False,
        description=(
            "ADMIN-ONLY. True mints a PLATFORM kind: the definition, its new "
            "child kinds, and every row of the composed create land in the "
            "Matrx System organization with visibility='public' (no manual "
            "promotion). Refused for non-admin callers. Omit for normal "
            "user kinds (caller org, internal)."
        ),
    )


class KindGetArgs(ToolArgs):
    kind: str
    include_schema: bool = Field(default=True)


class KindUpdateSchemaArgs(ToolArgs):
    kind: str
    json_schema: dict
    change_note: str | None = Field(default=None)


class KindAddExampleArgs(ToolArgs):
    kind: str
    data: dict
    label: str | None = Field(default=None)
    description: str | None = Field(default=None)
    is_canonical: bool = Field(default=False)


class KindActivateArgs(ToolArgs):
    kind: str
    active: bool = Field(default=True)
    note: str | None = Field(default=None)


class KindCreateSkillArgs(ToolArgs):
    kind: str
    body: str | None = Field(default=None)
    extra_guidance: str | None = Field(default=None)


class KindCreateContentBlockArgs(ToolArgs):
    kind: str
    template: str | None = Field(default=None)
    label: str | None = Field(default=None)


class InstanceCreateArgs(ToolArgs):
    kind: str
    data: dict
    title: str | None = Field(default=None)


class InstanceListArgs(ToolArgs):
    kind: str | None = Field(default=None)
    status: Literal["pending", "passed", "failed"] | None = Field(default=None)
    limit: int = Field(default=50)
    offset: int = Field(default=0)


class InstanceGetArgs(ToolArgs):
    instance_id: str


class InstanceUpdateArgs(ToolArgs):
    instance_id: str
    data: dict | None = Field(default=None)
    title: str | None = Field(default=None)
    repin_to_current: bool = Field(default=False)


class InstanceDeleteArgs(ToolArgs):
    instance_id: str


class KindcompGetContextArgs(ToolArgs):
    kind: str | None = Field(default=None)
    component_id: str | None = Field(default=None)


class KindcompCreateComponentArgs(ToolArgs):
    kind: str
    component_key: str
    component_source: str
    props_transform: str | None = Field(default=None)
    config: dict = Field(default={})
    platform: Literal["web", "vite", "react-native", "chrome-extension", "desktop", "html-js"] = (
        Field(default="web")
    )
    # 🚨 DEPLOY-GATED WIDENING — `loading` is accepted by this code but is NOT
    # yet in `tool.definition.parameters`, so the drift gate reports arg_drift
    # on `kindcomp_create_component` until aidream prod runs this code. That is
    # the SAFE direction; see the ordering law on KindCreateArgs.loading_component.
    # After the next deploy: widen the DB enum to include "loading", then
    # cache-bust. Do NOT widen the DB first.
    role: Literal["output", "input", "loading"] = Field(default="output")
    pinned_kind_version: int | None = Field(default=None)
    is_default: bool = Field(default=True)
    notes: str | None = Field(default=None)


class KindcompGetCodeArgs(ToolArgs):
    component_id: str
    sections: list = Field(default=["component_source", "props_transform"])


class KindcompUpdateCodeArgs(ToolArgs):
    component_id: str
    updates: dict
    bump_version: bool = Field(default=False)
    notes: str | None = Field(default=None)


class KindcompPatchCodeArgs(ToolArgs):
    component_id: str
    section: Literal["component_source", "props_transform"] = Field(default="component_source")
    patches: list
    bump_version: bool = Field(default=False)
    notes: str | None = Field(default=None)


class KindcompUpdateSettingsArgs(ToolArgs):
    component_id: str
    settings: dict


class KindcompResolveIncidentArgs(ToolArgs):
    incident_id: str
    resolution_notes: str | None = Field(default=None)


class ToolcompCreateComponentArgs(ToolArgs):
    notes: str | None = Field(default=None)
    tool_id: str | None = Field(default=None)
    tool_name: str | None = Field(default=None)
    language: Literal["tsx", "jsx"] = Field(default="tsx")
    inline_code: str
    display_name: str
    overlay_code: str | None = Field(default=None)
    surface_name: str = Field(default="matrx-default/default")
    results_label: str | None = Field(default=None)
    allowed_imports: list = Field(default=["react", "lucide-react"])


class ToolcompGetCodeArgs(ToolArgs):
    sections: list = Field(default=["inline_code", "overlay_code"])
    component_id: str


class ToolcompGetContextArgs(ToolArgs):
    component_id: str | None = Field(default=None)
    surface_name: str | None = Field(default=None)
    tool_id: str | None = Field(default=None)
    tool_name: str | None = Field(default=None)


class ToolcompGetIncidentDetailArgs(ToolArgs):
    incident_id: str


class ToolcompGetSampleDetailArgs(ToolArgs):
    sample_id: str
    full_events: bool = Field(default=False)
    event_offset: int = Field(default=0, ge=0)
    event_limit: int = Field(default=10, ge=1, le=10)


class ToolcompListToolsArgs(ToolArgs):
    tag: str | None = Field(default=None)
    limit: int = Field(default=30)
    offset: int = Field(default=0)
    prefix: str | None = Field(default=None)
    category: str | None = Field(default=None)
    group_by: Literal["category", "prefix", "source_kind"] | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    source_kind: Literal["native", "mcp_discovered", "admin_authored", "agent_authored"] | None = (
        Field(default=None)
    )
    has_component: bool | None = Field(default=None)


class ToolcompPatchCodeArgs(ToolArgs):
    notes: str | None = Field(default=None)
    patches: list
    section: Literal[
        "header_extras_code", "header_subtitle_code", "inline_code", "overlay_code", "utility_code"
    ] = Field(default="inline_code")
    bump_version: bool = Field(default=False)
    component_id: str


class ToolcompResolveIncidentArgs(ToolArgs):
    incident_id: str
    resolution_notes: str | None = Field(default=None)


class ToolcompUpdateCodeArgs(ToolArgs):
    notes: str | None = Field(default=None)
    updates: dict
    bump_version: bool = Field(default=False)
    component_id: str


class ToolcompUpdateSettingsArgs(ToolArgs):
    settings: dict
    component_id: str


class TravelCreateSummaryArgs(ToolArgs):
    events: list
    location: str
    activities: list
    restaurants: list
    weather_info: dict


class TravelGetActivitiesArgs(ToolArgs):
    city: str
    weather: str


class TravelGetEventsArgs(ToolArgs):
    city: str
    weather: str


class TravelGetRestaurantsArgs(ToolArgs):
    city: str


class TravelGetWeatherArgs(ToolArgs):
    city: str


# skill (list|get|search) is the discriminated union SkillArgs in
# arg_models.dispatcher_args. The old flat SkillListArgs / SkillGetArgs /
# SkillSearchArgs classes were retired with the legacy skill_* rows (migration 0100).


class VscGetStateArgs(ToolArgs):
    fields: list


class WidgetAttachMediaArgs(ToolArgs):
    alt: str | None = Field(default=None)
    url: str
    title: str | None = Field(default=None)
    mimeType: str
    position: Literal["after", "before", "end", "inline"] | None = Field(default=None)


class WidgetCreateArtifactArgs(ToolArgs):
    data: dict
    kind: str


class WidgetTextAppendArgs(ToolArgs):
    text: str


class WidgetTextInsertAfterArgs(ToolArgs):
    text: str


class WidgetTextInsertBeforeArgs(ToolArgs):
    text: str


class WidgetTextPatchArgs(ToolArgs):
    search_text: str
    replacement_text: str


class WidgetTextPrependArgs(ToolArgs):
    text: str


class WidgetTextReplaceArgs(ToolArgs):
    text: str


class WidgetUpdateFieldArgs(ToolArgs):
    field: str
    value: Any


class WidgetUpdateRecordArgs(ToolArgs):
    patch: dict


IMPORT_FAILURES: list[str] = []


def _reg(name, source_kind, executor, args, module, func):
    try:
        fn = getattr(importlib.import_module(module), func)
    except Exception as exc:  # noqa: BLE001 - reported by the validator
        IMPORT_FAILURES.append(f"{name}: {module}.{func}: {exc!r}")
        return
    tool(name=name, source_kind=source_kind, executor=executor, args=args)(fn)


_reg(
    "agent_call",
    "native",
    "matrx-ai-core",
    AgentCallArgs,
    "matrx_ai.tools.implementations.agent_call",
    "agent_call",
)
# Bundle listers (``bundle:list_<name>``) are a GENERIC FAMILY — one handler,
# N data-driven ``tool_def`` rows. Importing the handler registers the family via
# ``@tool_family``; there is intentionally NO per-bundle ``_reg`` line here. New
# bundles (MCP-synced or system) are pure DB rows and resolve automatically.
from matrx_ai.tools.implementations import bundle_lister as _bundle_lister  # noqa: E402,F401

_reg(
    "cloud_file",
    "native",
    None,
    CloudFileArgs,
    "matrx_ai.tools.implementations.cloud_files",
    "cloud_file",
)
_reg(
    "code_execute_python",
    "native",
    "matrx-ai-core",
    CodeExecutePythonArgs,
    "matrx_ai.tools.implementations.code",
    "code_execute_python",
)
_reg(
    "code_fetch_code",
    "native",
    "matrx-ai-core",
    CodeFetchCodeArgs,
    "matrx_ai.tools.implementations.code",
    "code_fetch_code",
)
_reg(
    "code_fetch_tree",
    "native",
    "matrx-ai-core",
    CodeFetchTreeArgs,
    "matrx_ai.tools.implementations.code",
    "code_fetch_tree",
)
_reg(
    "code_store_html",
    "native",
    "matrx-ai-core",
    CodeStoreHtmlArgs,
    "matrx_ai.tools.implementations.code",
    "code_store_html",
)
_reg(
    "context",
    "native",
    None,
    ContextArgs,
    "matrx_ai.tools.implementations.ctx",
    "context",
)
_reg(
    "context_patch",
    "native",
    None,
    ContextPatchArgs,
    "matrx_ai.tools.implementations.ctx_write",
    "context_patch",
)
_reg(
    "dataset",
    "native",
    None,
    DatasetArgs,
    "matrx_ai.tools.implementations.datasets_tools",
    "dataset",
)
_reg(
    "debug_traces_by_call",
    "native",
    "matrx-ai-core",
    DebugTracesByCallArgs,
    "matrx_ai.tools.implementations.debug_traces_tools",
    "debug_traces_by_call",
)
_reg(
    "debug_traces_by_conv",
    "native",
    "matrx-ai-core",
    DebugTracesByConvArgs,
    "matrx_ai.tools.implementations.debug_traces_tools",
    "debug_traces_by_conv",
)
_reg(
    "debug_traces_failures_since",
    "native",
    "matrx-ai-core",
    DebugTracesFailuresSinceArgs,
    "matrx_ai.tools.implementations.debug_traces_tools",
    "debug_traces_failures_since",
)
_reg(
    "debug_traces_get_file",
    "native",
    "matrx-ai-core",
    DebugTracesGetFileArgs,
    "matrx_ai.tools.implementations.debug_traces_tools",
    "debug_traces_get_file",
)
_reg(
    "debug_traces_list_files",
    "native",
    "matrx-ai-core",
    NoArgs,
    "matrx_ai.tools.implementations.debug_traces_tools",
    "debug_traces_list_files",
)
_reg(
    "debug_traces_recent",
    "native",
    "matrx-ai-core",
    DebugTracesRecentArgs,
    "matrx_ai.tools.implementations.debug_traces_tools",
    "debug_traces_recent",
)
_reg(
    "fs_edit",
    "native",
    "matrx-ai-core",
    FsEditArgs,
    "matrx_ai.tools.implementations.filesystem",
    "fs_edit",
)
_reg(
    "fs_list",
    "native",
    "matrx-ai-core",
    FsListArgs,
    "matrx_ai.tools.implementations.filesystem",
    "fs_list",
)
_reg(
    "fs_mkdir",
    "native",
    "matrx-ai-core",
    FsMkdirArgs,
    "matrx_ai.tools.implementations.filesystem",
    "fs_mkdir",
)
_reg(
    "fs_patch",
    "native",
    "matrx-ai-core",
    FsPatchArgs,
    "matrx_ai.tools.implementations.filesystem",
    "fs_patch",
)
_reg(
    "fs_read",
    "native",
    "matrx-ai-core",
    FsReadArgs,
    "matrx_ai.tools.implementations.filesystem",
    "fs_read",
)
_reg(
    "fs_search",
    "native",
    "matrx-ai-core",
    FsSearchArgs,
    "matrx_ai.tools.implementations.filesystem",
    "fs_search",
)
_reg(
    "fs_write",
    "native",
    "matrx-ai-core",
    FsWriteArgs,
    "matrx_ai.tools.implementations.filesystem",
    "fs_write",
)
_reg(
    "get_open_trace_incidents",
    "native",
    "matrx-ai-core",
    GetOpenTraceIncidentsArgs,
    "matrx_ai.tools.implementations.feedback_tools",
    "get_open_trace_incidents",
)
_reg(
    "git_ingest",
    "native",
    "matrx-ai-core",
    GitIngestArgs,
    "matrx_ai.tools.implementations.code_ingest",
    "git_ingest",
)
_reg(
    "llms_txt_fetch",
    "native",
    "matrx-ai-core",
    LlmsTxtFetchArgs,
    "matrx_ai.tools.implementations.code_ingest",
    "llms_txt_fetch",
)
_reg(
    "load_chrome_tools",
    "native",
    "matrx-ai-core",
    LoadChromeToolsArgs,
    "matrx_ai.tools.implementations.browser_discovery",
    "load_chrome_tools",
)
_reg(
    "load_desktop_tools",
    "native",
    "matrx-ai-core",
    LoadDesktopToolsArgs,
    "matrx_ai.tools.implementations.desktop_discovery",
    "load_desktop_tools",
)
_reg(
    "math_calculate",
    "native",
    "matrx-ai-core",
    MathCalculateArgs,
    "matrx_ai.tools.implementations.math",
    "math_calculate",
)
_reg("memory", "native", None, MemoryArgs, "matrx_ai.tools.implementations.memory", "memory")
_reg(
    "dictionary",
    "native",
    "matrx-ai-core",
    DictionaryArgs,
    "matrx_ai.tools.implementations.dictionary",
    "dictionary",
)
_reg(
    "news_get_headlines",
    "native",
    "matrx-ai-core",
    NewsGetHeadlinesArgs,
    "matrx_ai.tools.implementations.news",
    "news_get_headlines",
)
_reg("note", "native", None, NoteArgs, "matrx_ai.tools.implementations.notes", "note")
_reg(
    "package_info",
    "native",
    "matrx-ai-core",
    PackageInfoArgs,
    "matrx_ai.tools.implementations.code_ingest",
    "package_info",
)
_reg(
    "picklist",
    "native",
    None,
    PicklistArgs,
    "matrx_ai.tools.implementations.picklists_tools",
    "picklist",
)
_reg(
    "knowledge_search",
    "native",
    "matrx-ai-core",
    RagSearchArgs,
    "matrx_ai.tools.implementations.rag",
    "knowledge_search",
)
_reg(
    "report_trace_incident",
    "native",
    "matrx-ai-core",
    ReportTraceIncidentArgs,
    "matrx_ai.tools.implementations.feedback_tools",
    "report_trace_incident",
)
_reg(
    "research_web",
    "native",
    "matrx-ai-core",
    ResearchWebArgs,
    "matrx_ai.tools.implementations.web",
    "research_web",
)
_reg("seo", "native", None, SeoArgs, "matrx_ai.tools.implementations.seo", "seo")
_reg(
    "shell_execute",
    "native",
    "matrx-ai-core",
    ShellExecuteArgs,
    "matrx_ai.tools.implementations.shell",
    "shell_execute",
)
_reg(
    "shell_python",
    "native",
    "matrx-ai-core",
    ShellPythonArgs,
    "matrx_ai.tools.implementations.shell",
    "shell_python",
)
_reg(
    "skill",
    "native",
    None,
    SkillArgs,
    "matrx_ai.tools.implementations.skill",
    "skill",
)
_reg("sql", "native", None, SqlArgs, "matrx_ai.tools.implementations.database", "sql")
_reg("task", "native", None, TaskArgs, "matrx_ai.tools.implementations.tasks", "task")
_reg(
    "text_analyze",
    "native",
    "matrx-ai-core",
    TextAnalyzeArgs,
    "matrx_ai.tools.implementations.text",
    "text_analyze",
)
_reg(
    "text_regex_extract",
    "native",
    "matrx-ai-core",
    TextRegexExtractArgs,
    "matrx_ai.tools.implementations.text",
    "text_regex_extract",
)
_reg(
    "kind_create",
    "native",
    "matrx-ai-core",
    KindCreateArgs,
    "matrx_ai.tools.implementations.kind_authoring",
    "kind_create",
)
_reg(
    "kind_get",
    "native",
    "matrx-ai-core",
    KindGetArgs,
    "matrx_ai.tools.implementations.kind_authoring",
    "kind_get",
)
_reg(
    "kind_update_schema",
    "native",
    "matrx-ai-core",
    KindUpdateSchemaArgs,
    "matrx_ai.tools.implementations.kind_authoring",
    "kind_update_schema",
)
_reg(
    "kind_add_example",
    "native",
    "matrx-ai-core",
    KindAddExampleArgs,
    "matrx_ai.tools.implementations.kind_authoring",
    "kind_add_example",
)
_reg(
    "kind_activate",
    "native",
    "matrx-ai-core",
    KindActivateArgs,
    "matrx_ai.tools.implementations.kind_authoring",
    "kind_activate",
)
_reg(
    "kind_create_skill",
    "native",
    "matrx-ai-core",
    KindCreateSkillArgs,
    "matrx_ai.tools.implementations.kind_authoring",
    "kind_create_skill",
)
_reg(
    "kind_create_content_block",
    "native",
    "matrx-ai-core",
    KindCreateContentBlockArgs,
    "matrx_ai.tools.implementations.kind_authoring",
    "kind_create_content_block",
)
_reg(
    "instance_create",
    "native",
    "matrx-ai-core",
    InstanceCreateArgs,
    "matrx_ai.tools.implementations.kind_instance",
    "instance_create",
)
_reg(
    "instance_list",
    "native",
    "matrx-ai-core",
    InstanceListArgs,
    "matrx_ai.tools.implementations.kind_instance",
    "instance_list",
)
_reg(
    "instance_get",
    "native",
    "matrx-ai-core",
    InstanceGetArgs,
    "matrx_ai.tools.implementations.kind_instance",
    "instance_get",
)
_reg(
    "instance_update",
    "native",
    "matrx-ai-core",
    InstanceUpdateArgs,
    "matrx_ai.tools.implementations.kind_instance",
    "instance_update",
)
_reg(
    "instance_delete",
    "native",
    "matrx-ai-core",
    InstanceDeleteArgs,
    "matrx_ai.tools.implementations.kind_instance",
    "instance_delete",
)
_reg(
    "kindcomp_get_context",
    "native",
    "matrx-ai-core",
    KindcompGetContextArgs,
    "matrx_ai.tools.implementations.kind_component",
    "kindcomp_get_context",
)
_reg(
    "kindcomp_create_component",
    "native",
    "matrx-ai-core",
    KindcompCreateComponentArgs,
    "matrx_ai.tools.implementations.kind_component",
    "kindcomp_create_component",
)
_reg(
    "kindcomp_get_code",
    "native",
    "matrx-ai-core",
    KindcompGetCodeArgs,
    "matrx_ai.tools.implementations.kind_component",
    "kindcomp_get_code",
)
_reg(
    "kindcomp_update_code",
    "native",
    "matrx-ai-core",
    KindcompUpdateCodeArgs,
    "matrx_ai.tools.implementations.kind_component",
    "kindcomp_update_code",
)
_reg(
    "kindcomp_patch_code",
    "native",
    "matrx-ai-core",
    KindcompPatchCodeArgs,
    "matrx_ai.tools.implementations.kind_component",
    "kindcomp_patch_code",
)
_reg(
    "kindcomp_update_settings",
    "native",
    "matrx-ai-core",
    KindcompUpdateSettingsArgs,
    "matrx_ai.tools.implementations.kind_component",
    "kindcomp_update_settings",
)
_reg(
    "kindcomp_resolve_incident",
    "native",
    "matrx-ai-core",
    KindcompResolveIncidentArgs,
    "matrx_ai.tools.implementations.kind_component",
    "kindcomp_resolve_incident",
)
_reg(
    "toolcomp_create_component",
    "native",
    "matrx-ai-core",
    ToolcompCreateComponentArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_create_component",
)
_reg(
    "toolcomp_get_code",
    "native",
    "matrx-ai-core",
    ToolcompGetCodeArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_get_code",
)
_reg(
    "toolcomp_get_context",
    "native",
    "matrx-ai-core",
    ToolcompGetContextArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_get_context",
)
_reg(
    "toolcomp_get_incident_detail",
    "native",
    "matrx-ai-core",
    ToolcompGetIncidentDetailArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_get_incident_detail",
)
_reg(
    "toolcomp_get_sample_detail",
    "native",
    "matrx-ai-core",
    ToolcompGetSampleDetailArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_get_sample_detail",
)
_reg(
    "toolcomp_list_tools",
    "native",
    "matrx-ai-core",
    ToolcompListToolsArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_list_tools",
)
_reg(
    "toolcomp_patch_code",
    "native",
    "matrx-ai-core",
    ToolcompPatchCodeArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_patch_code",
)
_reg(
    "toolcomp_resolve_incident",
    "native",
    "matrx-ai-core",
    ToolcompResolveIncidentArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_resolve_incident",
)
_reg(
    "toolcomp_update_code",
    "native",
    "matrx-ai-core",
    ToolcompUpdateCodeArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_update_code",
)
_reg(
    "toolcomp_update_settings",
    "native",
    "matrx-ai-core",
    ToolcompUpdateSettingsArgs,
    "matrx_ai.tools.implementations.tool_component",
    "toolcomp_update_settings",
)
_reg(
    "travel_create_summary",
    "native",
    "matrx-ai-core",
    TravelCreateSummaryArgs,
    "matrx_ai.tools.implementations.travel",
    "travel_create_summary",
)
_reg(
    "travel_get_activities",
    "native",
    "matrx-ai-core",
    TravelGetActivitiesArgs,
    "matrx_ai.tools.implementations.travel",
    "travel_get_activities",
)
_reg(
    "travel_get_events",
    "native",
    "matrx-ai-core",
    TravelGetEventsArgs,
    "matrx_ai.tools.implementations.travel",
    "travel_get_events",
)
_reg(
    "travel_get_location",
    "native",
    "matrx-ai-core",
    NoArgs,
    "matrx_ai.tools.implementations.travel",
    "travel_get_location",
)
_reg(
    "travel_get_restaurants",
    "native",
    "matrx-ai-core",
    TravelGetRestaurantsArgs,
    "matrx_ai.tools.implementations.travel",
    "travel_get_restaurants",
)
_reg(
    "travel_get_weather",
    "native",
    "matrx-ai-core",
    TravelGetWeatherArgs,
    "matrx_ai.tools.implementations.travel",
    "travel_get_weather",
)
_reg(
    "vsc_get_state",
    "native",
    "matrx-ai-core",
    VscGetStateArgs,
    "matrx_ai.tools.implementations.vsc",
    "vsc_get_state",
)
_reg(
    "random_wheel",
    "native",
    "matrx-ai-core",
    RandomWheelArgs,
    "matrx_ai.tools.implementations.random_wheel",
    "random_wheel",
)
_reg("web", "native", None, WebArgs, "matrx_ai.tools.implementations.web", "web")
_reg(
    "widget_attach_media",
    "native",
    "matrx-ai-core",
    WidgetAttachMediaArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_attach_media",
)
_reg(
    "widget_create_artifact",
    "native",
    "matrx-ai-core",
    WidgetCreateArtifactArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_create_artifact",
)
_reg(
    "widget_text_append",
    "native",
    "matrx-ai-core",
    WidgetTextAppendArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_text_append",
)
_reg(
    "widget_text_insert_after",
    "native",
    "matrx-ai-core",
    WidgetTextInsertAfterArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_text_insert_after",
)
_reg(
    "widget_text_insert_before",
    "native",
    "matrx-ai-core",
    WidgetTextInsertBeforeArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_text_insert_before",
)
_reg(
    "widget_text_patch",
    "native",
    "matrx-ai-core",
    WidgetTextPatchArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_text_patch",
)
_reg(
    "widget_text_prepend",
    "native",
    "matrx-ai-core",
    WidgetTextPrependArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_text_prepend",
)
_reg(
    "widget_text_replace",
    "native",
    "matrx-ai-core",
    WidgetTextReplaceArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_text_replace",
)
_reg(
    "widget_update_field",
    "native",
    "matrx-ai-core",
    WidgetUpdateFieldArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_update_field",
)
_reg(
    "widget_update_record",
    "native",
    "matrx-ai-core",
    WidgetUpdateRecordArgs,
    "matrx_ai.tools.implementations.widgets",
    "widget_update_record",
)
