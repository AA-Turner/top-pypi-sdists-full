"""Curated built-in tool catalog and registration for Aegis."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import Any

from .handlers_continuity import (
    run_activity_action,
    run_cron_action,
    run_memory_recall,
    run_memory_upload,
    run_procedure_inspect,
    run_procedure_manage,
    run_profile_action,
    run_todo_action,
)
from .builtins_skills import skill_tool_definitions, skill_tool_handler
from .builtins_sub_agents import sub_agents_tool_definitions, sub_agents_tool_handler
from .handlers_code_execution import run_code_execute
from .handlers_network import (
    run_browser_action,
    run_clarify,
    run_message_send,
    run_web_extract,
    run_web_read,
    run_web_search,
)
from .handlers_workspace import (
    run_file_patch,
    run_file_read,
    run_file_search,
    run_file_write,
    run_process_action,
    run_terminal_exec,
)
from .runtime import ToolAvailability, ToolDefinition, ToolRuntime, ToolSideEffectMetadata
from .schema_descriptions import enrich_builtin_tool_schema
from .surfaces import BuiltinToolDependencies

_BUILTIN_VERSION = "2.0.0"
_BUILTIN_TOOL_ORDER = (
    "terminal",
    "process",
    "file",
    "web",
    "browser",
    "clarify",
    "cron",
    "code_execution",
    "memory",
    "messaging",
    "todo",
    "skills",
    "sub_agents",
    "continuity-native",
)


def register_builtin_tools(
    runtime: ToolRuntime,
    *,
    enabled_overrides: Mapping[str, bool],
    dependencies: BuiltinToolDependencies,
) -> None:
    for definition in builtin_tool_definitions(enabled_overrides, dependencies=dependencies):
        runtime.register_tool(
            definition,
            handler=_handler_for_tool(definition, runtime=runtime, dependencies=dependencies),
        )


def builtin_tool_definitions(
    enabled_overrides: Mapping[str, bool],
    *,
    dependencies: BuiltinToolDependencies | None = None,
) -> tuple[ToolDefinition, ...]:
    browser_reason = None
    if dependencies is None or dependencies.browser_backend is None:
        browser_reason = "Browser tools require a configured browser backend."
    message_reason = None
    if dependencies is None or dependencies.message_delivery is None:
        message_reason = "Messaging tools require a configured outbound delivery target."
    cron_reason = None
    if dependencies is None or dependencies.cron_runtime is None:
        cron_reason = "Cron management is not configured on this Aegis surface."
    profile_reason = None
    if dependencies is None or dependencies.profile_management is None:
        profile_reason = "Profile management is not configured on this Aegis surface."
    activity_reason = None
    if dependencies is None or dependencies.activity_management is None:
        activity_reason = "Activity management is not configured on this Aegis surface."
    memory_reason = None
    if dependencies is None or dependencies.memory_management is None:
        memory_reason = "Memory management is not configured on this Aegis surface."
    recall_reason = None
    if dependencies is None or dependencies.recall_search is None:
        recall_reason = "Recall search is not configured on this Aegis surface."
    procedure_reason = None
    if dependencies is None or dependencies.procedure_management is None:
        procedure_reason = "Procedure management is not configured on this Aegis surface."
    skill_reason = None
    if dependencies is None or dependencies.skill_management is None:
        skill_reason = "Skill management is not configured on this Aegis surface."
    sub_agents_reason = None
    if dependencies is None or dependencies.sub_agents_surface is None:
        sub_agents_reason = "Sub-agent execution is not configured on this Aegis surface."

    definitions = (
        _builtin_tool(
            tool_id="tool.terminal.exec",
            display_name="Terminal Exec",
            family="terminal",
            backend="subprocess",
            description="Run one bounded terminal command in the current workspace.",
            schema=_object_schema(
                required=("command",),
                properties={
                    "command": {"type": "string"},
                    "cwd": {"type": "string"},
                    "timeout_seconds": {"type": "integer", "minimum": 1, "maximum": 120},
                    "background": {"type": "boolean"},
                    "env": {"type": "object"},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="high",
                approval_class="strict",
                writes_state=True,
                reads_state=True,
                categories=("terminal", "workspace"),
                notes="Runs a command or starts a background process inside the active workspace or another allowed local root.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.process.manage",
            display_name="Process Manager",
            family="process",
            backend="subprocess",
            description=(
                "Inspect or control background processes previously started through "
                "tool.terminal.exec with background=true. Do not use this for ordinary chat turns or "
                "foreground commands."
            ),
            schema=_object_schema(
                required=("action",),
                properties={
                    "action": {
                        "type": "string",
                        "enum": ["list", "ls", "poll", "inspect", "wait", "write", "kill"],
                        "description": "Use list|ls to enumerate active managed processes; use the others only with a known process_id.",
                    },
                    "process_id": {"type": "string"},
                    "input": {"type": "string"},
                    "timeout_seconds": {"type": "integer", "minimum": 1, "maximum": 120},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="high",
                approval_class="strict",
                writes_state=True,
                reads_state=True,
                categories=("process", "terminal"),
                notes="Operates on background processes created by tool.terminal.exec.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.file.read",
            display_name="File Read",
            family="file",
            backend="filesystem",
            description="Read a text workspace file with bounded line pagination.",
            schema=_object_schema(
                required=("path",),
                properties={
                    "path": {"type": "string", "description": "Workspace-relative or absolute file path to read."},
                    "offset": {"type": "integer", "minimum": 1, "description": "1-indexed first line to read."},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 2000, "description": "Maximum number of lines to read."},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="low",
                approval_class="standard",
                reads_state=True,
                categories=("file", "read"),
                notes="Reads text from a workspace file.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.file.write",
            display_name="File Write",
            family="file",
            backend="filesystem",
            description="Overwrite a text workspace file, creating parent directories as needed.",
            schema=_object_schema(
                required=("path", "content"),
                properties={
                    "path": {"type": "string", "description": "Workspace-relative or absolute file path to write."},
                    "content": {"type": "string", "description": "Complete text content to write to the file."},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="high",
                approval_class="strict",
                writes_state=True,
                reads_state=True,
                categories=("file", "write"),
                notes="Writes text to a workspace file.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.file.patch",
            display_name="File Patch",
            family="file",
            backend="filesystem",
            description="Patch text files with unique replace edits or V4A multi-file patches.",
            schema=_object_schema(
                required=("mode",),
                properties={
                    "mode": {"type": "string", "enum": ["replace", "patch"], "description": "Use replace for one file or patch for V4A patch content."},
                    "path": {"type": "string", "description": "Workspace-relative or absolute file path for replace mode."},
                    "old_string": {"type": "string", "description": "Exact text to locate; must be unique unless replace_all=true."},
                    "new_string": {"type": "string", "description": "Replacement text for the matched content."},
                    "replace_all": {"type": "boolean", "description": "Replace every match instead of requiring uniqueness."},
                    "patch": {"type": "string", "description": "V4A patch text for add, update, and delete file operations."},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="high",
                approval_class="strict",
                writes_state=True,
                reads_state=True,
                categories=("file", "patch"),
                notes="Applies bounded text replacements to a workspace file.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.file.search",
            display_name="File Search",
            family="file",
            backend="rg",
            description="Search workspace file contents or filenames with ripgrep.",
            schema=_object_schema(
                required=("query",),
                properties={
                    "query": {"type": "string", "description": "Text or regex-like pattern to search for."},
                    "target": {"type": "string", "enum": ["content", "files"], "description": "Search file contents or file paths."},
                    "path": {"type": "string", "description": "Optional file or directory path to search within."},
                    "glob": {"type": "string", "description": "Optional file glob filter such as '*.py'."},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 200, "description": "Maximum number of matches to return."},
                    "offset": {"type": "integer", "minimum": 0, "description": "Number of matches to skip for pagination."},
                    "context": {"type": "integer", "minimum": 0, "maximum": 5, "description": "Context lines around content matches."},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="low",
                approval_class="standard",
                reads_state=True,
                categories=("file", "search"),
                notes="Fast search across the active workspace or another allowed local root.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.web.search",
            display_name="Web Search",
            family="web",
            backend="duckduckgo",
            description="Search the public web and summarize the most relevant results.",
            schema=_object_schema(
                required=("query",),
                properties={
                    "query": {
                        "type": "string",
                        "description": "Search query for current public-web information.",
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 8,
                        "description": "Maximum number of search results to summarize.",
                    },
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="medium",
                approval_class="standard",
                touches_network=True,
                categories=("web", "search"),
                notes="Uses lightweight public web search with direct-result fallback.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.web.read",
            display_name="Web Read",
            family="web",
            backend="urllib",
            description="Read a specific public URL and extract a text-first summary.",
            schema=_object_schema(
                required=("url",),
                properties={
                    "url": {
                        "type": "string",
                        "description": "Public http(s) URL to fetch and summarize.",
                    }
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="medium",
                approval_class="standard",
                touches_network=True,
                categories=("web", "read"),
                notes="Fetches a public page and returns readable text.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.web.extract",
            display_name="Web Extract",
            family="web",
            backend="urllib",
            description="Fetch and summarize multiple public URLs for multi-source research.",
            schema=_object_schema(
                required=("urls",),
                properties={
                    "urls": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "One or more public http(s) URLs to fetch.",
                    },
                    "max_urls": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Optional cap on how many URLs to process from the provided list.",
                    },
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="medium",
                approval_class="standard",
                touches_network=True,
                categories=("web", "extract"),
                notes="Fetches multiple public pages and returns compact source-by-source summaries.",
            ),
        ),
        *_browser_tool_definitions(reason=browser_reason),
        _builtin_tool(
            tool_id="tool.clarify",
            display_name="Clarify",
            family="clarify",
            backend="surface-clarify",
            description="Ask the user for clarification with an open question or a bounded choice list.",
            schema=_object_schema(
                required=("question",),
                properties={
                    "question": {"type": "string"},
                    "mode": {"type": "string", "enum": ["open", "choice"]},
                    "choices": {"type": ["array", "string"]},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="low",
                approval_class="none",
                reads_state=True,
                categories=("clarify", "interaction"),
                notes="Returns a structured clarification request when the next step is ambiguous.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.cron.manage",
            display_name="Cron Manager",
            family="cron",
            backend="cron-runtime",
            description="Create, inspect, pause, resume, remove/delete, and list built-in scheduled jobs.",
            schema=_object_schema(
                required=("action",),
                properties={
                    "action": {
                        "type": "string",
                        "enum": ["list", "ls", "create", "inspect", "pause", "resume", "remove", "delete"],
                        "description": "Use list|ls without job_id; use create with schedule and job_kind; use inspect|pause|resume|remove|delete with job_id.",
                    },
                    "job_id": {"type": "string", "description": "Cron job id such as cron:9f0e36022b."},
                    "name": {"type": "string", "description": "Human-readable job name when action=create."},
                    "schedule": {"type": "string", "description": "Schedule phrase, ISO timestamp, interval, or cron expression when action=create."},
                    "job_kind": {"type": "string", "description": "Job executor kind when action=create, such as greeting, web_search, prompt, or sub_agents."},
                    "message": {"type": "string", "description": "Message payload for greeting or prompt jobs."},
                    "query": {"type": "string", "description": "Search query payload for web_search jobs."},
                    "prompt": {"type": "string", "description": "Prompt payload for prompt or sub-agent jobs."},
                    "skills": {
                        "oneOf": [{"type": "array", "items": {"type": "string"}}, {"type": "string"}],
                        "description": "Skill ids to load as operating instructions when a prompt job runs.",
                    },
                    "profile_id": {"type": "string"},
                    "clone_id": {"type": "string"},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="medium",
                approval_class="standard",
                writes_state=True,
                reads_state=True,
                categories=("cron", "automation"),
                notes="Govern recurring jobs for the active Aegis surface.",
            ),
            availability=_availability(cron_reason is None, cron_reason),
        ),
        *sub_agents_tool_definitions(reason=sub_agents_reason),
        _builtin_tool(
            tool_id="tool.code.execute",
            display_name="Code Execute",
            family="code_execution",
            backend="python-sandbox",
            description="Run a restricted Python snippet in the active workspace with bounded tool RPC access.",
            schema=_object_schema(
                required=("code",),
                properties={
                    "code": {
                        "type": "string",
                        "description": "Restricted Python snippet; may use safe stdlib imports and call tool('tool.id', {...}) for file/web/terminal tools.",
                    },
                    "timeout_seconds": {"type": "integer", "minimum": 1, "maximum": 30, "description": "Maximum runtime in seconds."},
                    "mode": {
                        "type": "string",
                        "enum": ["project", "strict"],
                        "description": "project runs in the session workspace with the active venv/conda Python; strict runs in an isolated temp directory.",
                    },
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="high",
                approval_class="strict",
                reads_state=True,
                writes_state=True,
                touches_network=True,
                categories=("code", "python", "file", "web", "terminal"),
                notes="Subprocess Python with safe stdlib imports, scrubbed ambient secrets, and separately governed nested tool RPC.",
            ),
        ),
        _builtin_tool(
            tool_id="tool.memory.recall",
            display_name="Memory Recall",
            family="memory",
            backend="evidence-runtime",
            description="Inspect durable memory state and search scoped recall without mutating canonical evidence.",
            schema=_object_schema(
                properties={
                    "action": {"type": "string", "enum": ["list", "ls", "inspect", "lineage", "search"]},
                    "memory_id": {"type": "string"},
                    "query": {"type": "string"},
                    "limit": {"type": "integer"},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="low",
                approval_class="standard",
                writes_state=False,
                reads_state=True,
                categories=("memory", "recall"),
                notes="Uses the canonical recall path for search and inspect-only memory access.",
            ),
            availability=_availability(memory_reason is None and recall_reason is None, memory_reason or recall_reason),
        ),
        _builtin_tool(
            tool_id="tool.memory.upload",
            display_name="Memory Upload",
            family="memory",
            backend="memory-runtime",
            description="Correct, pin, unpin, or delete durable memories through the canonical evidence owner.",
            schema=_object_schema(
                required=("action", "memory_id"),
                properties={
                    "action": {"type": "string", "enum": ["correct", "delete", "pin", "unpin"]},
                    "memory_id": {"type": "string"},
                    "content": {"type": "string"},
                    "reason": {"type": "string"},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="high",
                approval_class="strict",
                writes_state=True,
                reads_state=True,
                categories=("memory", "governance"),
                notes="Mutates canonical evidence with explicit correction and protection semantics.",
            ),
            availability=_availability(memory_reason is None, memory_reason),
        ),
        _builtin_tool(
            tool_id="tool.message.send",
            display_name="Message Send",
            family="messaging",
            backend="delivery",
            description="Send an outbound message to a configured delivery target.",
            schema=_object_schema(
                required=("body",),
                properties={
                    "body": {"type": "string"},
                    "target": {"type": "string"},
                    "metadata": {"type": "object"},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="high",
                approval_class="strict",
                writes_state=True,
                reads_state=True,
                touches_network=True,
                categories=("message", "delivery"),
                notes="Only available when the current surface has an outbound delivery target.",
            ),
            availability=_availability(message_reason is None, message_reason),
        ),
        _builtin_tool(
            tool_id="tool.todo.manage",
            display_name="Todo Manager",
            family="todo",
            backend="session-todo",
            description=(
                "Manage a session-scoped execution board while working an activity or task. "
                "Use activity state, not todos, for user-followed work tracking."
            ),
            schema=_object_schema(
                required=("action",),
                properties={
                    "action": {
                        "type": "string",
                        "enum": [
                            "list",
                            "ls",
                            "add",
                            "create",
                            "inspect",
                            "update",
                            "complete",
                            "reopen",
                            "remove",
                            "delete",
                            "promote",
                            "clear",
                        ],
                        "description": "Use add|create|list|clear for scratchpad setup; other actions require an item_id.",
                    },
                    "item_id": {"type": "string"},
                    "title": {"type": "string"},
                    "status": {"type": "string", "enum": ["open", "done", "promoted"]},
                    "notes": {"type": "string"},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="medium",
                approval_class="standard",
                writes_state=True,
                reads_state=True,
                categories=("todo", "scratchpad"),
                notes="Tracks short-horizon execution decomposition separately from durable goals.",
            ),
        ),
        *skill_tool_definitions(reason=skill_reason),
        _builtin_tool(
            tool_id="tool.profile.manage",
            display_name="Profile Manager",
            family="continuity-native",
            backend="operator-surface",
            description="Inspect or patch durable profile continuity: who the user is, stable preferences, boundaries, relationship, and recurring work.",
            schema=_object_schema(
                properties={
                    "action": {"type": "string", "enum": ["inspect", "show", "get", "patch", "update", "set"]},
                    "display_name": {"type": "string"},
                    "name": {"type": "string"},
                    "personality_preset": {"type": "string"},
                    "initiative": {"type": "string"},
                    "charter_text": {"type": "string"},
                    "text": {"type": "string"},
                    "content": {"type": "string"},
                    "clear_charter": {"type": "boolean"},
                    "user_text": {"type": "string"},
                    "user_content": {"type": "string"},
                    "user_fields": {"type": "object"},
                    "user_append": {"type": "boolean"},
                    "user_clear": {"type": "boolean"},
                    "relationship_text": {"type": "string"},
                    "relationship_content": {"type": "string"},
                    "relationship_append": {"type": "boolean"},
                    "relationship_clear": {"type": "boolean"},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="medium",
                approval_class="standard",
                writes_state=True,
                reads_state=True,
                categories=("profile", "continuity"),
                notes="Operates on the owner-aligned profile surface instead of split legacy state tools.",
            ),
            availability=_availability(profile_reason is None, profile_reason),
        ),
        _builtin_tool(
            tool_id="tool.activity.manage",
            display_name="Activity Manager",
            family="continuity-native",
            backend="operator-surface",
            description="Inspect or mutate actionable ongoing work threads. Do not use for biography, greetings, identity, preferences, or relationship notes.",
            schema=_object_schema(
                properties={
                    "action": {"type": "string", "enum": ["list", "ls", "show", "inspect", "create", "focus", "activate", "update", "drop", "delete"]},
                    "goal_id": {"type": "string"},
                    "parent_goal_id": {"type": "string"},
                    "title": {"type": "string"},
                    "status": {"type": "string", "enum": ["proposed", "queued", "active", "blocked", "deferred", "completed", "done", "failed", "dropped"]},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                    "owner": {"type": "string", "enum": ["user", "agent", "shared"]},
                    "dependency_refs": {"type": "array"},
                    "evidence_refs": {"type": "array"},
                    "related_memory_ids": {"type": "array"},
                    "review_checkpoint": {"type": "string"},
                    "deadline": {"type": "string"},
                    "time_sensitivity": {"type": "string", "enum": ["low", "normal", "high", "urgent"]},
                    "reason": {"type": "string"},
                    "activate": {"type": "boolean"},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="medium",
                approval_class="standard",
                writes_state=True,
                reads_state=True,
                categories=("activity", "work"),
                notes="Operates on the durable ActivityGraph through the owner-aligned activity surface.",
            ),
            availability=_availability(activity_reason is None, activity_reason),
        ),
        _builtin_tool(
            tool_id="tool.procedure.inspect",
            display_name="Procedure Inspect",
            family="continuity-native",
            backend="operator-surface",
            description="Inspect promoted procedures and procedure candidates for the active profile.",
            schema=_object_schema(
                properties={
                    "action": {"type": "string", "enum": ["list", "ls", "show", "inspect"]},
                    "procedure_id": {"type": "string"},
                    "minimum_support": {"type": "integer"},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="low",
                approval_class="standard",
                writes_state=False,
                reads_state=True,
                categories=("procedure", "inspect"),
                notes="Reads the owner-aligned procedure surface without mutating durable truth.",
            ),
            availability=_availability(procedure_reason is None, procedure_reason),
        ),
        _builtin_tool(
            tool_id="tool.procedure.manage",
            display_name="Procedure Manager",
            family="continuity-native",
            backend="operator-surface",
            description="Patch or retire promoted procedures through the owner-aligned procedure surface.",
            schema=_object_schema(
                required=("action", "procedure_id"),
                properties={
                    "action": {"type": "string", "enum": ["patch", "update", "retire"]},
                    "procedure_id": {"type": "string"},
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "content": {"type": "string"},
                    "trigger_refs": {"type": "array"},
                    "status": {"type": "string", "enum": ["active", "promoted", "verified", "retired"]},
                },
            ),
            side_effects=ToolSideEffectMetadata(
                risk_class="medium",
                approval_class="standard",
                writes_state=True,
                reads_state=True,
                categories=("procedure", "governance"),
                notes="Mutates promoted procedures without granting model-owned skill acquisition or search.",
            ),
            availability=_availability(procedure_reason is None, procedure_reason),
        ),
    )
    return tuple(
        enrich_builtin_tool_schema(replace(definition, enabled=enabled_overrides.get(definition.tool_id, definition.enabled)))
        for definition in definitions
    )


def render_builtin_tool_reference_markdown() -> str:
    grouped = _group_builtin_tools(_docs_builtin_tool_definitions())
    lines: list[str] = []
    for family in _BUILTIN_TOOL_ORDER:
        tools = grouped.get(family, ())
        if not tools:
            continue
        lines.append(f"### {family}")
        for tool in tools:
            note = ""
            if not tool.available and tool.availability.reason:
                note = f" ({tool.availability.reason})"
            lines.append(f"- `{tool.tool_id}`{note}")
        lines.append("")
    return "\n".join(lines).rstrip()


def render_builtin_tool_summary_markdown() -> str:
    grouped = _group_builtin_tools(_docs_builtin_tool_definitions())
    lines: list[str] = []
    for family in _BUILTIN_TOOL_ORDER:
        tools = grouped.get(family, ())
        if not tools:
            continue
        tool_ids = ", ".join(f"`{tool.tool_id}`" for tool in tools)
        lines.append(f"- `{family}`: {tool_ids}")
    return "\n".join(lines)


def _browser_tool_definitions(*, reason: str | None) -> tuple[ToolDefinition, ...]:
    browser_availability = _availability(reason is None, reason)
    return tuple(
        _builtin_tool(
            tool_id=tool_id,
            display_name=display_name,
            family="browser",
            backend="browser-bridge",
            description=description,
            schema=schema,
            side_effects=ToolSideEffectMetadata(
                risk_class="medium",
                approval_class="standard",
                reads_state=True,
                writes_state=tool_id not in {"tool.browser.snapshot", "tool.browser.images", "tool.browser.vision", "tool.browser.console"},
                touches_network=True,
                categories=("browser", action),
                notes="Backed by the configured browser bridge when available.",
            ),
            availability=browser_availability,
        )
        for tool_id, display_name, action, description, schema in (
            (
                "tool.browser.navigate",
                "Browser Navigate",
                "navigate",
                "Navigate the active browser session to a URL and return a compact ref-based page snapshot.",
                _object_schema(required=("url",), properties={"url": {"type": "string"}}),
            ),
            (
                "tool.browser.snapshot",
                "Browser Snapshot",
                "snapshot",
                "Capture a text snapshot of the active browser page, including interactive element refs.",
                _object_schema(properties={"full": {"type": "boolean"}}),
            ),
            (
                "tool.browser.click",
                "Browser Click",
                "click",
                "Click an element in the active browser page by snapshot ref, with selector fallback.",
                _object_schema(
                    properties={
                        "ref": {"type": "string", "description": "Snapshot element ref such as @e3."},
                        "selector": {"type": "string", "description": "CSS selector fallback when no ref exists."},
                    }
                ),
            ),
            (
                "tool.browser.type",
                "Browser Type",
                "type",
                "Type text into a browser element by snapshot ref, with selector fallback.",
                _object_schema(
                    required=("text",),
                    properties={
                        "ref": {"type": "string", "description": "Snapshot element ref such as @e3."},
                        "selector": {"type": "string", "description": "CSS selector fallback when no ref exists."},
                        "text": {"type": "string"},
                    },
                ),
            ),
            (
                "tool.browser.scroll",
                "Browser Scroll",
                "scroll",
                "Scroll the active page.",
                _object_schema(
                    properties={
                        "direction": {"type": "string", "enum": ("up", "down")},
                        "amount": {"type": "integer"},
                    }
                ),
            ),
            (
                "tool.browser.back",
                "Browser Back",
                "back",
                "Navigate backward in the active browser history.",
                _object_schema(properties={}),
            ),
            (
                "tool.browser.press",
                "Browser Press",
                "press",
                "Press a keyboard key in the active browser page.",
                _object_schema(required=("key",), properties={"key": {"type": "string"}}),
            ),
            (
                "tool.browser.images",
                "Browser Images",
                "images",
                "List image resources and metadata from the current page.",
                _object_schema(properties={}),
            ),
            (
                "tool.browser.vision",
                "Browser Vision",
                "vision",
                "Capture a browser screenshot and analyze it when a vision analyzer is configured.",
                _object_schema(
                    properties={
                        "question": {"type": "string"},
                        "prompt": {"type": "string"},
                        "annotate": {"type": "boolean"},
                    }
                ),
            ),
            (
                "tool.browser.console",
                "Browser Console",
                "console",
                "Inspect recent console output, JavaScript errors, or evaluate a JavaScript expression.",
                _object_schema(
                    properties={
                        "clear": {"type": "boolean"},
                        "expression": {"type": "string"},
                    }
                ),
            ),
        )
    )


def _docs_builtin_tool_definitions() -> tuple[ToolDefinition, ...]:
    return builtin_tool_definitions(
        {},
        dependencies=BuiltinToolDependencies(
            cwd=Path("/tmp"),
            cron_runtime=object(),  # type: ignore[arg-type]
            profile_management=object(),  # type: ignore[arg-type]
            activity_management=object(),  # type: ignore[arg-type]
            memory_management=object(),  # type: ignore[arg-type]
            recall_search=object(),  # type: ignore[arg-type]
            procedure_management=object(),  # type: ignore[arg-type]
            skill_management=object(),  # type: ignore[arg-type]
            sub_agents_surface=object(),  # type: ignore[arg-type]
            browser_backend=object(),  # type: ignore[arg-type]
        ),
    )

def _builtin_tool(
    *,
    tool_id: str,
    display_name: str,
    family: str,
    backend: str,
    description: str,
    schema: Mapping[str, Any],
    side_effects: ToolSideEffectMetadata,
    availability: ToolAvailability | None = None,
) -> ToolDefinition:
    return ToolDefinition(
        tool_id=tool_id,
        display_name=display_name,
        version=_BUILTIN_VERSION,
        description=description,
        schema=schema,
        side_effects=side_effects,
        family=family,
        audience="both",
        availability=availability or ToolAvailability(),
        backend=backend,
        metadata={"kind": "built-in"},
    )


def _availability(is_available: bool, reason: str | None) -> ToolAvailability:
    return ToolAvailability(is_available=is_available, reason=None if is_available else reason)


def _object_schema(
    *,
    properties: Mapping[str, Any],
    required: tuple[str, ...] = (),
) -> Mapping[str, Any]:
    schema: dict[str, Any] = {
        "type": "object",
        "properties": dict(properties),
    }
    if required:
        schema["required"] = list(required)
    return schema


def _group_builtin_tools(definitions: tuple[ToolDefinition, ...]) -> dict[str, tuple[ToolDefinition, ...]]:
    grouped: dict[str, list[ToolDefinition]] = {}
    for definition in definitions:
        grouped.setdefault(definition.family, []).append(definition)
    return {family: tuple(items) for family, items in grouped.items()}


def _handler_for_tool(
    definition: ToolDefinition,
    *,
    runtime: ToolRuntime,
    dependencies: BuiltinToolDependencies,
):
    tool_id = definition.tool_id
    if tool_id == "tool.terminal.exec":
        return lambda invocation: run_terminal_exec(invocation, dependencies=dependencies)
    if tool_id == "tool.process.manage":
        return lambda invocation: run_process_action(invocation, manager=dependencies.process_manager)
    if tool_id == "tool.file.read":
        return lambda invocation: run_file_read(
            invocation,
            cwd=dependencies.cwd_for_session(invocation.session_id),
            allowed_roots=dependencies.additional_workspace_roots,
        )
    if tool_id == "tool.file.write":
        return lambda invocation: run_file_write(
            invocation,
            cwd=dependencies.cwd_for_session(invocation.session_id),
            allowed_roots=dependencies.additional_workspace_roots,
        )
    if tool_id == "tool.file.patch":
        return lambda invocation: run_file_patch(
            invocation,
            cwd=dependencies.cwd_for_session(invocation.session_id),
            allowed_roots=dependencies.additional_workspace_roots,
        )
    if tool_id == "tool.file.search":
        return lambda invocation: run_file_search(
            invocation,
            cwd=dependencies.cwd_for_session(invocation.session_id),
            allowed_roots=dependencies.additional_workspace_roots,
        )
    if tool_id == "tool.web.search":
        return lambda invocation: run_web_search(invocation, user_agent=dependencies.web_user_agent)
    if tool_id == "tool.web.read":
        return lambda invocation: run_web_read(invocation, user_agent=dependencies.web_user_agent)
    if tool_id == "tool.web.extract":
        return lambda invocation: run_web_extract(invocation, user_agent=dependencies.web_user_agent)
    if tool_id.startswith("tool.browser."):
        return lambda invocation: run_browser_action(invocation, backend=dependencies.browser_backend, vision_analyzer=dependencies.browser_vision_analyzer)
    if tool_id == "tool.clarify":
        return lambda invocation: run_clarify(invocation, surface=dependencies.clarify_surface)
    if tool_id == "tool.cron.manage":
        return lambda invocation: run_cron_action(invocation, runtime=dependencies.cron_runtime)
    if tool_id == "tool.code.execute":
        return lambda invocation: run_code_execute(
            invocation,
            runtime=runtime,
            allowlist=dependencies.code_tool_allowlist,
            cwd=dependencies.cwd_for_session(invocation.session_id),
        )
    skill_handler = skill_tool_handler(tool_id, dependencies=dependencies)
    if skill_handler is not None:
        return skill_handler
    sub_agents_handler = sub_agents_tool_handler(tool_id, dependencies=dependencies)
    if sub_agents_handler is not None:
        return sub_agents_handler
    if tool_id == "tool.profile.manage":
        return lambda invocation: run_profile_action(invocation, surface=dependencies.profile_management)
    if tool_id == "tool.activity.manage":
        return lambda invocation: run_activity_action(invocation, surface=dependencies.activity_management)
    if tool_id == "tool.memory.recall":
        return lambda invocation: run_memory_recall(
            invocation,
            memory_surface=dependencies.memory_management,
            recall_surface=dependencies.recall_search,
        )
    if tool_id == "tool.memory.upload":
        return lambda invocation: run_memory_upload(invocation, surface=dependencies.memory_management)
    if tool_id == "tool.procedure.inspect":
        return lambda invocation: run_procedure_inspect(invocation, surface=dependencies.procedure_management)
    if tool_id == "tool.procedure.manage":
        return lambda invocation: run_procedure_manage(invocation, surface=dependencies.procedure_management)
    if tool_id == "tool.message.send":
        return lambda invocation: run_message_send(invocation, surface=dependencies.message_delivery)
    if tool_id == "tool.todo.manage":
        return lambda invocation: run_todo_action(
            invocation,
            store=dependencies.todo_store,
            goal_surface=dependencies.activity_management,
        )
    return None


__all__ = ["BuiltinToolDependencies", "builtin_tool_definitions", "register_builtin_tools", "render_builtin_tool_reference_markdown", "render_builtin_tool_summary_markdown"]
