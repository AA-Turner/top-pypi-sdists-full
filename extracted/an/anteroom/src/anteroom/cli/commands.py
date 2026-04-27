"""Shared slash-command engine and result model.

This module is the single source of truth for all slash-command metadata:
names, aliases, descriptions, subcommand completions, and dispatch logic.

The engine parses slash commands, resolves skills, and returns typed
``CommandResult`` values -- no I/O, no DB, no rendering, no side effects.
Each interface (legacy CLI, Textual, web) interprets results via thin adapters.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass, field
from typing import Any, Literal, Sequence

from .plan import parse_plan_command
from .skills import SkillPolicy, SkillRegistry

# ---------------------------------------------------------------------------
# Command kind: exhaustive intent classification
# ---------------------------------------------------------------------------

CommandKind = Literal[
    "exit",
    # Conversation management
    "new_conversation",
    "list_conversations",
    "resume_conversation",
    "delete_conversation",
    "compact_conversation",
    "rewind_conversation",
    "search_conversations",
    "rename_conversation",
    "append_text",
    # Display / info
    "show_help",
    "show_message",
    "show_conventions",
    "show_model",
    "set_model",
    "list_models",
    "show_slug",
    "set_slug",
    "show_tools",
    "show_usage",
    "show_detail",
    "show_attribution",
    "toggle_verbose",
    "expand_last_tool",
    "set_density",
    # Skills
    "show_skills",
    # Spaces
    "show_spaces",
    "show_space",
    "show_space_sources",
    "create_space",
    "init_space",
    "load_space",
    "clone_space",
    "map_space",
    "update_space",
    "refresh_space",
    "export_space",
    "set_space",
    "delete_space",
    "link_source",
    "unlink_source",
    # Artifacts
    "show_artifacts",
    "show_artifact",
    "delete_artifact",
    "check_artifacts",
    # Packs
    "show_packs",
    "show_pack",
    "show_pack_sources",
    "refresh_pack_sources",
    "add_pack_source",
    "install_pack",
    "update_pack",
    "attach_pack",
    "detach_pack",
    "delete_pack",
    # MCP
    "show_mcp_status",
    "show_mcp_server_detail",
    "run_mcp_action",
    # Planning
    "show_plan_status",
    "set_plan_mode",
    "approve_plan",
    "edit_plan",
    "reject_plan",
    # Config
    "show_config",
    # File operations (CLI-specific intent)
    "upload_file",
    "reprocess_source",
    # Tasks
    "show_tasks",
    "show_task",
    "show_task_output",
    "cancel_task",
    # Forwarding
    "forward_prompt",
    # Feedback
    "submit_feedback",
]

CommandArgumentCompletion = Literal["conversation_slug", "path", "directory"]

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ParsedSlashCommand:
    """A parsed ``/command arg`` structure."""

    raw: str
    name: str
    arg: str = ""


@dataclass(frozen=True)
class SkillDescription:
    """Skill metadata for display."""

    display_name: str
    description: str
    source: str
    accepts_args: bool = False
    policy_summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    update_guidance: str = ""


@dataclass(frozen=True)
class SearchedDirectory:
    """Directory search result for skill loading display."""

    path: str
    source: str
    skill_count: int
    exists: bool


@dataclass
class CommandContext:
    """Input state and dependencies needed by commands."""

    current_model: str
    working_dir: str
    available_tools: Sequence[str] = field(default_factory=tuple)
    tool_registry: Any | None = None
    skill_registry: SkillRegistry | None = None
    artifact_registry: Any | None = None
    plan_mode: bool = False


@dataclass(frozen=True)
class CommandResult:
    """Typed, immutable result of command execution.

    The engine returns intent only — no I/O. Each interface adapter
    interprets the result and performs rendering / state mutation.
    """

    kind: CommandKind
    command: ParsedSlashCommand
    message: str | None = None
    # Conversation
    conversation_type: str | None = None
    conversation_title: str | None = None
    resume_target: str | None = None
    delete_target: str | None = None
    search_query: str | None = None
    search_keyword_mode: bool = False
    search_type_filter: str | None = None
    list_limit: int | None = None
    rewind_arg: str | None = None
    # Model / slug
    model_name: str | None = None
    slug_value: str | None = None
    # Space
    space_target: str | None = None
    space_edit_field: str | None = None
    space_edit_value: str | None = None
    # Artifact
    artifact_fqn: str | None = None
    artifact_type_filter: str | None = None
    artifact_source_filter: str | None = None
    # Pack
    pack_ref: str | None = None
    pack_path: str | None = None
    pack_project_scope: bool = False
    pack_attach_after_install: bool = False
    pack_priority: int | None = None
    pack_source_url: str | None = None
    # MCP
    mcp_server_name: str | None = None
    mcp_action: str | None = None
    # Plan
    plan_mode_enabled: bool | None = None
    plan_edit_arg: str | None = None
    plan_reject_reason: str | None = None
    # Tools / skills display data
    tool_names: tuple[str, ...] = ()
    skill_entries: tuple[SkillDescription, ...] = ()
    skill_warnings: tuple[str, ...] = ()
    searched_dirs: tuple[SearchedDirectory, ...] = ()
    # Forwarding
    forward_prompt: str | None = None
    # Config
    config_subcommand: str | None = None
    config_arg: str | None = None
    # Task
    task_target: str | None = None
    task_tail_lines: int | None = None
    # Upload / reprocess
    upload_path: str | None = None
    reprocess_arg: str | None = None
    # Density (#1367)
    density_mode: str | None = None
    # Display control
    echo_user: bool = True


# ---------------------------------------------------------------------------
# Centralized command metadata — single source of truth
# ---------------------------------------------------------------------------

COMMAND_DESCRIPTIONS: dict[str, str] = {
    "new": "Start a fresh conversation",
    "append": "Append text to the latest note message",
    "last": "Resume the most recent conversation",
    "list": "Browse recent conversations",
    "search": "Search conversation history",
    "resume": "Resume a conversation by slug, ID, or number",
    "delete": "Delete a conversation",
    "rename": "Rename the current conversation",
    "slug": "View or update the conversation slug",
    "rewind": "Rewind to an earlier message",
    "compact": "Compact the current conversation context",
    "conventions": "Show the active project conventions",
    "instructions": "Show the active project conventions",
    "tools": "Inspect available tools",
    "skills": "Inspect loaded skills",
    "reload-skills": "Reload skill files from disk",
    "pack": "Install, inspect, or attach packs",
    "packs": "List installed packs",
    "space": "Switch, inspect, and edit spaces",
    "spaces": "List available spaces",
    "mcp": "Inspect or reconnect MCP servers",
    "model": "Show, list, or switch models",
    "plan": "Turn planning mode on, off, or review it",
    "upload": "Upload a file into the knowledge base",
    "reprocess": "Re-extract uploaded source content",
    "usage": "Review token and cost usage",
    "verbose": "Cycle the session verbosity",
    "detail": "Replay tool calls with full output",
    "expand": "Re-render the last tool result in detail",
    "density": "Change tool-result density",
    "attribution": "Show the last turn's attribution snapshot",
    "help": "Open the command help",
    "artifact": "Inspect and manage artifacts",
    "artifacts": "List artifacts",
    "artifact-check": "Run artifact health checks",
    "task": "Inspect task status and output",
    "tasks": "List background tasks",
    "config": "Open or edit scoped config",
    "clear": "Clear the screen and start a fresh conversation",
    "copy": "Copy the last assistant response",
    "spec": "Inspect and manage specs",
    "specs": "List specs",
    "mission": "Inspect and manage missions",
    "missions": "List missions",
    "memory": "Inspect and manage memories",
    "memories": "List memories",
    "agent": "Inspect and manage detached agents",
    "agents": "List detached agents",
    "quit": "Exit the REPL",
    "exit": "Exit the REPL",
    "feedback": "Submit feedback or a bug report",
}

COMMAND_INTENT_LABELS: dict[str, str] = {
    "conversation": "Conversation",
    "workspace": "Workspace",
    "inspect": "Inspect",
    "workflow": "Workflow",
    "session": "Session",
}

COMMAND_INTENTS: dict[str, str] = {
    "new": "conversation",
    "append": "conversation",
    "last": "conversation",
    "list": "conversation",
    "search": "conversation",
    "resume": "conversation",
    "delete": "conversation",
    "rename": "conversation",
    "slug": "conversation",
    "rewind": "conversation",
    "compact": "conversation",
    "clear": "conversation",
    "upload": "workspace",
    "reprocess": "workspace",
    "space": "workspace",
    "spaces": "workspace",
    "pack": "workspace",
    "packs": "workspace",
    "artifact": "workspace",
    "artifacts": "workspace",
    "artifact-check": "workspace",
    "memory": "workspace",
    "memories": "workspace",
    "config": "workspace",
    "mission": "workflow",
    "missions": "workflow",
    "spec": "workflow",
    "specs": "workflow",
    "plan": "workflow",
    "task": "workflow",
    "tasks": "workflow",
    "agent": "workflow",
    "agents": "workflow",
    "conventions": "inspect",
    "instructions": "inspect",
    "tools": "inspect",
    "skills": "inspect",
    "reload-skills": "inspect",
    "mcp": "inspect",
    "usage": "inspect",
    "detail": "inspect",
    "expand": "inspect",
    "density": "inspect",
    "attribution": "inspect",
    "help": "inspect",
    "model": "session",
    "verbose": "session",
    "copy": "session",
    "quit": "session",
    "exit": "session",
    "feedback": "session",
}

COMMAND_ARGUMENT_HINTS: dict[str, str] = {
    "new": "<note|document|title>",
    "append": "<text>",
    "list": "[limit]",
    "search": "<query>",
    "resume": "<number|slug|id>",
    "delete": "<number|slug|id>",
    "rename": "<title>",
    "slug": "[name]",
    "space": "<subcommand>",
    "pack": "<subcommand>",
    "artifact": "<subcommand>",
    "mcp": "<subcommand>",
    "model": "[list|name]",
    "plan": "<subcommand>",
    "upload": "<path>",
    "reprocess": "[all|source_id]",
    "task": "<subcommand>",
    "memory": "<subcommand>",
    "agent": "<subcommand>",
    "spec": "<subcommand>",
    "mission": "<subcommand>",
    "config": "<subcommand>",
    "density": "<mode>",
    "feedback": "<description> [--include-history]",
}

COMMAND_SEARCH_TERMS: dict[str, tuple[str, ...]] = {
    "new": ("chat", "note", "document", "start"),
    "list": ("recent", "history"),
    "resume": ("open", "continue"),
    "clear": ("reset", "fresh"),
    "tools": ("available", "mcp"),
    "usage": ("tokens", "cost", "stats"),
    "model": ("picker", "switch"),
    "help": ("commands", "shortcuts"),
    "feedback": ("bug", "report", "issue", "diagnostic"),
}

SUBCOMMAND_COMPLETIONS: dict[str, list[str]] = {
    "artifact": ["list", "show", "delete", "import", "create"],
    "pack": [
        "list",
        "show",
        "install",
        "remove",
        "sources",
        "attach",
        "detach",
        "update",
        "add-source",
        "refresh",
    ],
    "space": [
        "list",
        "show",
        "switch",
        "select",
        "use",
        "create",
        "init",
        "load",
        "refresh",
        "clear",
        "clone",
        "map",
        "edit",
        "export",
        "sources",
        "link-source",
        "unlink-source",
    ],
    "model": ["list"],
    "config": ["list", "get", "set", "reset"],
    "mcp": ["status", "connect", "disconnect", "reconnect"],
    "plan": ["on", "off", "status", "approve", "edit", "reject"],
    "reprocess": ["all"],
    "mission": ["list", "status", "talk"],
    "memory": ["list", "show", "create", "edit", "delete"],
    "agent": ["list", "status", "cancel", "retry"],
    "task": ["list", "show", "output", "tail", "cancel"],
    "density": ["minimal", "compact", "normal", "detailed"],
}

COMMAND_ARGUMENT_COMPLETIONS: dict[str, CommandArgumentCompletion] = {
    "resume": "conversation_slug",
    "delete": "conversation_slug",
    "rename": "conversation_slug",
    "upload": "path",
}

SUBCOMMAND_ARGUMENT_COMPLETIONS: dict[str, dict[str, CommandArgumentCompletion]] = {
    "space": {
        "load": "path",
        "map": "directory",
    },
    "pack": {
        "install": "path",
        "update": "path",
    },
}

ALL_COMMAND_NAMES: list[str] = [
    "new",
    "append",
    "last",
    "list",
    "search",
    "resume",
    "delete",
    "rename",
    "slug",
    "rewind",
    "compact",
    "conventions",
    "instructions",
    "tools",
    "skills",
    "reload-skills",
    "artifact",
    "artifacts",
    "artifact-check",
    "pack",
    "packs",
    "space",
    "spaces",
    "mcp",
    "config",
    "model",
    "plan",
    "upload",
    "reprocess",
    "usage",
    "verbose",
    "detail",
    "expand",
    "density",
    "attribution",
    "help",
    "clear",
    "copy",
    "spec",
    "specs",
    "task",
    "tasks",
    "mission",
    "missions",
    "memory",
    "memories",
    "agent",
    "agents",
    "feedback",
    "quit",
    "exit",
]

# Parity tier constants for Textual/web adapters
PARITY_TIER_1_COMMANDS: tuple[str, ...] = (
    "/help",
    "/new",
    "/tools",
    "/usage",
    "/model",
    "/skills",
    "/reload-skills",
)

PARITY_TIER_2_COMMANDS: tuple[str, ...] = (
    "/list",
    "/last",
    "/resume",
    "/search",
    "/rename",
    "/slug",
    "/delete",
    "/rewind",
    "/compact",
    "/spaces",
    "/space",
    "/artifacts",
    "/artifact",
    "/packs",
    "/pack",
    "/mcp",
    "/plan",
)


def get_builtin_names() -> frozenset[str]:
    """Return the canonical set of built-in command names.

    Used by ``SkillRegistry`` to reject skill names that would shadow
    built-in commands.  Derived from ``ALL_COMMAND_NAMES`` — adding a
    command to the engine automatically prevents skill name collisions.
    """
    return frozenset(ALL_COMMAND_NAMES)


def get_subcommand_completions(command_name: str) -> tuple[str, ...]:
    """Return shared subcommand completion metadata for a slash command."""
    return tuple(SUBCOMMAND_COMPLETIONS.get(command_name, ()))


def get_argument_completion_kind(
    command_name: str,
    *,
    subcommand: str | None = None,
) -> CommandArgumentCompletion | None:
    """Return the shared argument-completion kind for a command/subcommand."""
    if subcommand:
        return SUBCOMMAND_ARGUMENT_COMPLETIONS.get(command_name, {}).get(subcommand)
    return COMMAND_ARGUMENT_COMPLETIONS.get(command_name)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_slash_command(prompt: str) -> ParsedSlashCommand | None:
    """Parse ``/command [args]`` from user input.

    Returns ``None`` for non-slash input.
    """
    stripped = prompt.strip()
    if not stripped.startswith("/"):
        return None
    parts = stripped.split(maxsplit=1)
    return ParsedSlashCommand(
        raw=prompt,
        name=parts[0].lower(),
        arg=parts[1].strip() if len(parts) > 1 else "",
    )


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------


def execute_slash_command(prompt: str, context: CommandContext) -> CommandResult | None:
    """Route a slash command to the appropriate ``CommandResult``.

    Returns ``None`` when the input is not a slash command or when the
    command should fall through to the agent loop (e.g. ``/plan <prompt>``).
    """
    parsed = parse_slash_command(prompt)
    if parsed is None:
        return None

    # -- Exit --
    if parsed.name in {"/quit", "/exit"}:
        return CommandResult(kind="exit", command=parsed, echo_user=False)

    # -- New conversation --
    if parsed.name == "/new":
        conv_type, title = _parse_new_conversation(parsed.arg)
        return CommandResult(
            kind="new_conversation",
            command=parsed,
            conversation_type=conv_type,
            conversation_title=title,
            echo_user=False,
        )

    # -- Append --
    if parsed.name == "/append":
        if not parsed.arg:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/append <text>` — appends to the last message in a note conversation.",
            )
        return CommandResult(kind="append_text", command=parsed, message=parsed.arg, echo_user=False)

    # -- Help --
    if parsed.name == "/help":
        return CommandResult(kind="show_help", command=parsed)

    # -- Compact --
    if parsed.name == "/compact":
        return CommandResult(kind="compact_conversation", command=parsed, echo_user=False)

    # -- List --
    if parsed.name == "/list":
        limit = 20
        if parsed.arg.isdigit():
            limit = max(1, int(parsed.arg))
        return CommandResult(kind="list_conversations", command=parsed, list_limit=limit)

    # -- Last --
    if parsed.name == "/last":
        return CommandResult(kind="resume_conversation", command=parsed, resume_target=None, echo_user=False)

    # -- Resume --
    if parsed.name == "/resume":
        if not parsed.arg:
            return CommandResult(kind="list_conversations", command=parsed, list_limit=20)
        return CommandResult(
            kind="resume_conversation",
            command=parsed,
            resume_target=parsed.arg,
            echo_user=False,
        )

    # -- Search --
    if parsed.name == "/search":
        if not parsed.arg:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/search <query>` | `/search --keyword <query>` | `/search --type <type> <query>`",
            )
        search_arg = parsed.arg
        search_keyword = False
        search_type: str | None = None
        if search_arg == "--keyword" or search_arg.startswith("--keyword "):
            search_keyword = True
            search_arg = search_arg[len("--keyword") :].strip()
            if not search_arg:
                return CommandResult(
                    kind="show_message",
                    command=parsed,
                    message="Usage: `/search --keyword <query>`",
                )
        elif search_arg.startswith("--type "):
            rest = search_arg[len("--type ") :].strip()
            type_parts = rest.split(maxsplit=1)
            if type_parts and type_parts[0] in ("chat", "note", "document"):
                search_type = type_parts[0]
                search_arg = type_parts[1] if len(type_parts) > 1 else ""
            else:
                return CommandResult(
                    kind="show_message",
                    command=parsed,
                    message="Invalid type. Use: chat, note, or document",
                )
            if not search_arg:
                return CommandResult(
                    kind="show_message",
                    command=parsed,
                    message="Usage: `/search --type <type> <query>`",
                )
        return CommandResult(
            kind="search_conversations",
            command=parsed,
            search_query=search_arg,
            search_keyword_mode=search_keyword,
            search_type_filter=search_type,
        )

    # -- Delete --
    if parsed.name == "/delete":
        target = parsed.arg.strip()
        if target.startswith("--confirm "):
            target = target[len("--confirm ") :].strip()
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/delete <number|slug|id>`",
            )
        return CommandResult(
            kind="delete_conversation",
            command=parsed,
            delete_target=target,
            echo_user=False,
        )

    # -- Rename --
    if parsed.name == "/rename":
        if not parsed.arg:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/rename <title>` or `/rename <number|slug|id> <title>`",
            )
        return CommandResult(
            kind="rename_conversation",
            command=parsed,
            conversation_title=parsed.arg,
        )

    # -- Slug --
    if parsed.name == "/slug":
        if not parsed.arg:
            return CommandResult(kind="show_slug", command=parsed)
        return CommandResult(kind="set_slug", command=parsed, slug_value=parsed.arg.strip().lower())

    # -- Rewind --
    if parsed.name == "/rewind":
        return CommandResult(
            kind="rewind_conversation",
            command=parsed,
            rewind_arg=parsed.arg,
            echo_user=False,
        )

    # -- Conventions / Instructions --
    if parsed.name in {"/conventions", "/instructions"}:
        return CommandResult(kind="show_conventions", command=parsed)

    # -- Tools --
    if parsed.name == "/tools":
        return CommandResult(kind="show_tools", command=parsed, tool_names=_tool_names(context))

    # -- Model --
    if parsed.name == "/model":
        if not parsed.arg:
            return CommandResult(kind="show_model", command=parsed, model_name=context.current_model)
        if parsed.arg == "list":
            return CommandResult(kind="list_models", command=parsed, model_name=context.current_model)
        return CommandResult(kind="set_model", command=parsed, model_name=parsed.arg)

    # -- Usage --
    if parsed.name == "/usage":
        return CommandResult(kind="show_usage", command=parsed)

    # -- Verbose --
    if parsed.name == "/verbose":
        return CommandResult(kind="toggle_verbose", command=parsed, echo_user=False)

    # -- Detail --
    if parsed.name == "/detail":
        return CommandResult(kind="show_detail", command=parsed, echo_user=False)

    # -- Expand (#1367) --
    if parsed.name == "/expand":
        return CommandResult(kind="expand_last_tool", command=parsed, echo_user=False)

    # -- Density (#1367) --
    if parsed.name == "/density":
        valid_modes = ("minimal", "compact", "normal", "detailed")
        arg = parsed.arg.strip().lower()
        if not arg:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message=(
                    "Usage: `/density {minimal|compact|normal|detailed}` — "
                    "controls per-tool-result verbosity for the current session."
                ),
            )
        if arg not in valid_modes:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message=(f"Unknown density '{arg}'. Valid: minimal, compact, normal, detailed."),
            )
        return CommandResult(
            kind="set_density",
            command=parsed,
            density_mode=arg,
            echo_user=False,
        )

    # -- Upload --
    if parsed.name == "/upload":
        if not parsed.arg:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/upload <file-path>`",
            )
        return CommandResult(kind="upload_file", command=parsed, upload_path=parsed.arg, echo_user=False)

    # -- Reprocess --
    if parsed.name == "/reprocess":
        return CommandResult(
            kind="reprocess_source",
            command=parsed,
            reprocess_arg=parsed.arg or None,
            echo_user=False,
        )

    # -- Skills / Reload-skills --
    if parsed.name in {"/skills", "/reload-skills"}:
        return _skills_result(parsed, context)

    # -- Spaces / Space --
    if parsed.name == "/spaces":
        return CommandResult(kind="show_spaces", command=parsed)

    if parsed.name == "/space":
        return _dispatch_space(parsed, context)

    # -- Artifacts --
    if parsed.name in {"/artifact", "/artifacts"}:
        return _dispatch_artifact(parsed, prompt)

    # -- Artifact-check --
    if parsed.name == "/artifact-check":
        return CommandResult(kind="check_artifacts", command=parsed)

    # -- Packs --
    if parsed.name in {"/pack", "/packs"}:
        return _dispatch_pack(parsed, prompt)

    # -- MCP --
    if parsed.name == "/mcp":
        return _dispatch_mcp(parsed)

    # -- Config --
    if parsed.name == "/config":
        return _dispatch_config(parsed)

    # -- Plan --
    if parsed.name == "/plan":
        return _dispatch_plan(parsed, context)

    # -- Tasks --
    if parsed.name in {"/task", "/tasks"}:
        return _dispatch_task(parsed)

    # -- Skill resolution (fallback) --
    if context.skill_registry is not None:
        is_skill, expanded = context.skill_registry.resolve_input(prompt)
        if is_skill:
            return CommandResult(
                kind="forward_prompt",
                command=parsed,
                forward_prompt=expanded,
                echo_user=False,
            )

    return None


# ---------------------------------------------------------------------------
# Subcommand dispatchers (pure — no I/O)
# ---------------------------------------------------------------------------


def _dispatch_space(parsed: ParsedSlashCommand, context: CommandContext) -> CommandResult:
    """Route ``/space <subcommand>`` to the correct result."""
    parts = parsed.arg.split(maxsplit=1)
    sub = parts[0].lower() if parts else ""
    target = parts[1].strip() if len(parts) == 2 else ""

    if sub in {"", "list"}:
        return CommandResult(kind="show_spaces", command=parsed)

    if sub in {"switch", "select", "use"}:
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/space switch <name|id>`",
            )
        return CommandResult(kind="set_space", command=parsed, space_target=target, echo_user=False)

    if sub == "show":
        return CommandResult(kind="show_space", command=parsed, space_target=target)

    if sub == "refresh":
        return CommandResult(
            kind="refresh_space",
            command=parsed,
            space_target=target or None,
            echo_user=False,
        )

    if sub == "clear":
        return CommandResult(kind="set_space", command=parsed, space_target="", echo_user=False)

    if sub in {"create", "init"}:
        if not target and sub == "create":
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/space create <name>`",
            )
        kind: CommandKind = "create_space" if sub == "create" else "init_space"
        return CommandResult(kind=kind, command=parsed, space_target=target or None, echo_user=False)

    if sub == "load":
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/space load <path-or-url>`",
            )
        return CommandResult(kind="load_space", command=parsed, space_target=target, echo_user=False)

    if sub == "clone":
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/space clone <name|id>`",
            )
        return CommandResult(kind="clone_space", command=parsed, space_target=target, echo_user=False)

    if sub == "map":
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/space map <directory>`",
            )
        return CommandResult(kind="map_space", command=parsed, space_target=target, echo_user=False)

    if sub == "edit":
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message=(
                    "Usage: `/space edit instructions <text>`\n"
                    "`/space edit model <model-name>`\n"
                    "`/space edit name <new-name>`"
                ),
            )
        edit_parts = target.split(maxsplit=1)
        edit_field = edit_parts[0].lower()
        edit_value = edit_parts[1] if len(edit_parts) == 2 else ""
        if edit_field not in {"instructions", "model", "name"}:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Unknown field. Use: `instructions`, `model`, or `name`.",
            )
        if edit_field == "name" and not edit_value.strip():
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/space edit name <new-name>`",
            )
        return CommandResult(
            kind="update_space",
            command=parsed,
            space_edit_field=edit_field,
            space_edit_value=edit_value,
            echo_user=False,
        )

    if sub == "export":
        return CommandResult(
            kind="export_space",
            command=parsed,
            space_target=target or None,
            echo_user=False,
        )

    if sub == "sources":
        return CommandResult(kind="show_space_sources", command=parsed, space_target=target or None)

    if sub == "link-source":
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/space link-source <source-id>`",
            )
        return CommandResult(kind="link_source", command=parsed, space_target=target, echo_user=False)

    if sub == "unlink-source":
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/space unlink-source <source-id>`",
            )
        return CommandResult(kind="unlink_source", command=parsed, space_target=target, echo_user=False)

    if sub == "delete":
        delete_target = target
        if delete_target.startswith("--confirm "):
            delete_target = delete_target[len("--confirm ") :].strip()
        if not delete_target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/space delete <name|id>`",
            )
        return CommandResult(kind="delete_space", command=parsed, space_target=delete_target, echo_user=False)

    # Unknown subcommand — show usage
    return CommandResult(
        kind="show_message",
        command=parsed,
        message=(
            "Usage: `/space [list|show|switch|select|use|create|init|load|refresh|"
            "clear|clone|map|edit|export|sources|link-source|unlink-source]`"
        ),
    )


def _dispatch_artifact(parsed: ParsedSlashCommand, raw_prompt: str) -> CommandResult:
    """Route ``/artifact <subcommand>`` to the correct result."""
    parts = raw_prompt.split(maxsplit=2)
    subcommand = parts[1].lower() if len(parts) >= 2 else ""

    if parsed.name == "/artifacts" and (not subcommand or subcommand.startswith("--")):
        subcommand = "list"

    if subcommand in {"", "list"}:
        # Parse --type= and --source= filters from remaining args
        rest = ""
        if parsed.name == "/artifacts":
            rest = " ".join(parts[1:]) if len(parts) >= 2 else ""
        else:
            rest = parts[2] if len(parts) >= 3 else ""
        a_type: str | None = None
        a_source: str | None = None
        for tok in rest.split():
            if tok.startswith("--type="):
                a_type = tok.split("=", 1)[1]
            elif tok.startswith("--source="):
                a_source = tok.split("=", 1)[1]
        return CommandResult(
            kind="show_artifacts",
            command=parsed,
            artifact_type_filter=a_type,
            artifact_source_filter=a_source,
        )

    if subcommand == "show":
        target = parts[2].strip() if len(parts) >= 3 else ""
        return CommandResult(kind="show_artifact", command=parsed, artifact_fqn=target)

    if subcommand == "delete":
        target = parts[2].strip() if len(parts) >= 3 else ""
        return CommandResult(kind="delete_artifact", command=parsed, artifact_fqn=target, echo_user=False)

    if subcommand == "import":
        return CommandResult(
            kind="show_message",
            command=parsed,
            message="Use the CLI: `aroom artifact import --skills|--instructions|--all`",
        )

    if subcommand == "create":
        return CommandResult(
            kind="show_message",
            command=parsed,
            message="Use the CLI: `aroom artifact create <type> <name>`",
        )

    return CommandResult(
        kind="show_message",
        command=parsed,
        message="Usage: `/artifact {list,show,delete,import,create}`",
    )


def _dispatch_pack(parsed: ParsedSlashCommand, raw_prompt: str) -> CommandResult:
    """Route ``/pack <subcommand>`` to the correct result."""
    parts = raw_prompt.split(maxsplit=2)
    subcommand = parts[1].lower() if len(parts) >= 2 else ""

    if parsed.name == "/packs" and not subcommand:
        subcommand = "list"

    if subcommand in {"", "list"}:
        return CommandResult(kind="show_packs", command=parsed)

    if subcommand == "show":
        target = parts[2].strip() if len(parts) >= 3 else ""
        return CommandResult(kind="show_pack", command=parsed, pack_ref=target)

    if subcommand in {"remove", "delete"}:
        target = parts[2].strip() if len(parts) >= 3 else ""
        return CommandResult(kind="delete_pack", command=parsed, pack_ref=target, echo_user=False)

    if subcommand == "sources":
        return CommandResult(kind="show_pack_sources", command=parsed)

    if subcommand == "refresh":
        return CommandResult(kind="refresh_pack_sources", command=parsed, echo_user=False)

    if subcommand == "add-source":
        target = parts[2].strip() if len(parts) >= 3 else ""
        return CommandResult(kind="add_pack_source", command=parsed, pack_source_url=target, echo_user=False)

    if subcommand in {"attach", "detach"}:
        rest = parts[2].strip() if len(parts) >= 3 else ""
        project_scope = "--project" in rest
        target = rest.replace("--project", "").strip()
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message=f"Usage: `/pack {subcommand} <namespace/name> [--project]`",
            )
        return CommandResult(
            kind="attach_pack" if subcommand == "attach" else "detach_pack",
            command=parsed,
            pack_ref=target,
            pack_project_scope=project_scope,
            echo_user=False,
        )

    if subcommand in {"install", "update"}:
        rest = parts[2].strip() if len(parts) >= 3 else ""
        parsed_pack_op = _parse_pack_path_flags(subcommand, rest)
        if isinstance(parsed_pack_op, str):
            return CommandResult(kind="show_message", command=parsed, message=parsed_pack_op)
        return CommandResult(
            kind="install_pack" if subcommand == "install" else "update_pack",
            command=parsed,
            pack_path=parsed_pack_op["path"],
            pack_project_scope=parsed_pack_op["project_scope"],
            pack_attach_after_install=parsed_pack_op["attach_after_install"],
            pack_priority=parsed_pack_op["priority"],
            echo_user=False,
        )

    return CommandResult(
        kind="show_message",
        command=parsed,
        message="Usage: `/pack {list,show,remove,sources,install,update,attach,detach,refresh,add-source}`",
    )


def _dispatch_mcp(parsed: ParsedSlashCommand) -> CommandResult:
    """Route ``/mcp <subcommand>`` to the correct result."""
    parts = parsed.arg.split(maxsplit=1) if parsed.arg else []
    subcommand = parts[0].lower() if parts else ""
    target = parts[1].strip() if len(parts) == 2 else ""

    if not subcommand:
        return CommandResult(kind="show_mcp_status", command=parsed)

    if subcommand == "status":
        if not target:
            return CommandResult(kind="show_mcp_status", command=parsed)
        return CommandResult(kind="show_mcp_server_detail", command=parsed, mcp_server_name=target)

    if subcommand in {"connect", "disconnect", "reconnect"}:
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message=f"Usage: `/mcp {subcommand} <name>`",
            )
        return CommandResult(
            kind="run_mcp_action",
            command=parsed,
            mcp_action=subcommand,
            mcp_server_name=target,
            echo_user=False,
        )

    return CommandResult(
        kind="show_message",
        command=parsed,
        message="Usage: `/mcp [status <name>|connect|disconnect|reconnect <name>]`",
    )


def _dispatch_config(parsed: ParsedSlashCommand) -> CommandResult:
    """Route ``/config <subcommand>`` to the correct result."""
    parts = parsed.arg.split(maxsplit=1) if parsed.arg else []
    subcommand = parts[0].lower() if parts else ""

    if subcommand in {"list", "get", "explain", "sources", "set", "reset", "help", "search"}:
        arg = parts[1].strip() if len(parts) == 2 else ""
        return CommandResult(
            kind="show_config",
            command=parsed,
            config_subcommand=subcommand,
            config_arg=arg,
            echo_user=False,
        )

    # No subcommand or unknown — the adapter decides (e.g. launch TUI in CLI)
    return CommandResult(kind="show_config", command=parsed, config_subcommand=None, echo_user=False)


def _dispatch_plan(parsed: ParsedSlashCommand, context: CommandContext) -> CommandResult | None:
    """Route ``/plan <subcommand>`` to the correct result.

    Returns ``None`` for inline plan prompts so they fall through to the
    agent loop.
    """
    subcommand, inline_prompt = parse_plan_command(parsed.raw)

    if subcommand in {"on", "start"}:
        return CommandResult(kind="set_plan_mode", command=parsed, plan_mode_enabled=True, echo_user=False)

    if subcommand == "off":
        return CommandResult(kind="set_plan_mode", command=parsed, plan_mode_enabled=False, echo_user=False)

    if subcommand == "status":
        return CommandResult(kind="show_plan_status", command=parsed, plan_mode_enabled=context.plan_mode)

    if subcommand == "approve":
        return CommandResult(kind="approve_plan", command=parsed, echo_user=False)

    if subcommand == "edit":
        return CommandResult(
            kind="edit_plan",
            command=parsed,
            plan_edit_arg=parsed.arg.split(maxsplit=1)[1] if len(parsed.arg.split(maxsplit=1)) > 1 else None,
            echo_user=False,
        )

    if subcommand == "reject":
        # Extract reason: "/plan reject <reason>"
        reject_parts = parsed.raw.split(maxsplit=2)
        reason = reject_parts[2].strip() if len(reject_parts) >= 3 else None
        return CommandResult(
            kind="reject_plan",
            command=parsed,
            plan_reject_reason=reason,
            echo_user=False,
        )

    if inline_prompt:
        return None

    return CommandResult(
        kind="show_message",
        command=parsed,
        message="Usage: `/plan on|off|status|approve|edit|reject` or `/plan <prompt>`.",
    )


def _dispatch_task(parsed: ParsedSlashCommand) -> CommandResult:
    """Route ``/task <subcommand>`` to the correct result."""
    parts = parsed.arg.split(maxsplit=2)
    sub = parts[0].lower() if parts else ""

    if parsed.name == "/tasks" or sub in {"", "list"}:
        return CommandResult(kind="show_tasks", command=parsed)

    if sub == "show":
        target = parts[1].strip() if len(parts) >= 2 else ""
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/task show <task_id>`",
            )
        return CommandResult(kind="show_task", command=parsed, task_target=target)

    if sub in {"output", "tail"}:
        target = parts[1].strip() if len(parts) >= 2 else ""
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message=f"Usage: `/task {sub} <task_id> [lines]`",
            )
        tail_lines: int | None = None
        if len(parts) >= 3 and parts[2].strip().isdigit():
            tail_lines = int(parts[2].strip())
        elif sub == "tail":
            tail_lines = 50
        return CommandResult(
            kind="show_task_output",
            command=parsed,
            task_target=target,
            task_tail_lines=tail_lines,
        )

    if sub == "cancel":
        target = parts[1].strip() if len(parts) >= 2 else ""
        if not target:
            return CommandResult(
                kind="show_message",
                command=parsed,
                message="Usage: `/task cancel <task_id>`",
            )
        return CommandResult(kind="cancel_task", command=parsed, task_target=target)

    return CommandResult(
        kind="show_message",
        command=parsed,
        message="Usage: `/task {list,show,output,tail,cancel} [args]`",
    )


# ---------------------------------------------------------------------------
# Helpers (pure — no I/O)
# ---------------------------------------------------------------------------


def _parse_new_conversation(arg: str) -> tuple[str, str]:
    """Parse ``/new [note|doc] [title]`` into (type, title)."""
    if not arg:
        return "chat", "New Conversation"
    parts = arg.split(maxsplit=1)
    first = parts[0].lower()
    if first in {"note", "doc", "document"}:
        conv_type = "document" if first in {"doc", "document"} else "note"
        title = parts[1].strip() if len(parts) > 1 and parts[1].strip() else f"New {conv_type.title()}"
        return conv_type, title
    return "chat", "New Conversation"


def _tool_names(context: CommandContext) -> tuple[str, ...]:
    """Aggregate available tool names from context."""
    names = set(context.available_tools)
    if context.tool_registry is not None:
        names.update(context.tool_registry.list_tools())
    return tuple(sorted(names))


def _parse_pack_path_flags(subcommand: str, rest: str) -> dict[str, Any] | str:
    """Parse ``/pack install|update <path> [--project] [--attach] [--priority N]``."""
    try:
        argv = shlex.split(rest)
    except ValueError as exc:
        return str(exc)

    if not argv:
        return f"Usage: `/pack {subcommand} <path>`"

    project_scope = False
    attach_after_install = False
    priority = 50
    path_tokens: list[str] = []
    idx = 0
    while idx < len(argv):
        token = argv[idx]
        if token == "--project":
            project_scope = True
            idx += 1
            continue
        if token == "--attach" and subcommand == "install":
            attach_after_install = True
            idx += 1
            continue
        if token == "--priority" and subcommand == "install":
            if idx + 1 >= len(argv):
                return "Usage: `/pack install <path> [--project] [--attach] [--priority N]`"
            try:
                priority = int(argv[idx + 1])
            except ValueError:
                return "Priority must be an integer."
            if priority < 1 or priority > 100:
                return "Priority must be between 1 and 100."
            idx += 2
            continue
        path_tokens.append(token)
        idx += 1

    if len(path_tokens) != 1:
        if subcommand == "install":
            return "Usage: `/pack install <path> [--project] [--attach] [--priority N]`"
        return "Usage: `/pack update <path> [--project]`"

    return {
        "path": path_tokens[0],
        "project_scope": project_scope,
        "attach_after_install": attach_after_install,
        "priority": priority,
    }


def _skills_result(parsed: ParsedSlashCommand, context: CommandContext) -> CommandResult:
    """Build skill listing result — pure, no reload side effects.

    The adapter is responsible for calling ``skill_registry.reload()``
    and ``load_from_artifacts()`` before rendering.
    """
    if context.skill_registry is None:
        return CommandResult(kind="show_skills", command=parsed)

    entries: list[SkillDescription] = []
    for display_name, description in context.skill_registry.get_skill_descriptions():
        skill = context.skill_registry.get(display_name)
        policy_summary = ""
        if skill and skill.policy != SkillPolicy():
            policy_summary = skill.policy.summary()
        entries.append(
            SkillDescription(
                display_name=display_name,
                description=description or "",
                source=skill.source if skill else "unknown",
                accepts_args=bool(skill and "{args}" in skill.prompt),
                policy_summary=policy_summary,
                metadata=dict(skill.metadata) if skill and skill.metadata else {},
                update_guidance=skill.update_guidance if skill else "",
            )
        )

    searched_dirs = tuple(
        SearchedDirectory(
            path=item.path,
            source=item.source,
            skill_count=item.skill_count,
            exists=item.exists,
        )
        for item in context.skill_registry.searched_dirs
    )
    return CommandResult(
        kind="show_skills",
        command=parsed,
        skill_entries=tuple(entries),
        skill_warnings=tuple(context.skill_registry.load_warnings),
        searched_dirs=searched_dirs,
    )


# ---------------------------------------------------------------------------
# Display builders (pure markdown — no I/O)
# ---------------------------------------------------------------------------


def build_help_markdown() -> str:
    """Render help text for all slash commands."""
    return (
        "## Slash Commands\n\n"
        "- `/new` start a fresh conversation\n"
        "- `/new note <title>` start a note\n"
        "- `/new doc <title>` start a document\n"
        "- `/last` resume the most recent conversation\n"
        "- `/list [N]` list recent conversations\n"
        "- `/resume <number|slug|id>` open a conversation\n"
        "- `/search <query>` search conversations\n"
        "- `/delete <number|slug|id>` delete a conversation\n"
        "- `/rewind <position> [--undo-files]` rewind the active conversation\n"
        "- `/compact` summarize the current thread to free context\n"
        "- `/conventions` show loaded project conventions\n"
        "- `/space` lists spaces, `/space create <name>` adds one, `/space edit ...` updates the active one,\n"
        "  `/space refresh` reloads it from disk, `/space export` dumps YAML,\n"
        "  and `/space switch <name>` activates one\n"
        "- `/artifact` list artifacts and `/artifact show <fqn>` inspect one\n"
        "- `/pack` lists packs; `/pack show <namespace/name>` inspects one; `/pack install <path>` or\n"
        "  `/pack update <path>` manage local packs; `/pack refresh` updates configured sources;\n"
        "  `/pack add-source <url>` adds a source\n"
        "- `/mcp` shows MCP status; `/mcp status <name>` and\n"
        "  `/mcp connect|disconnect|reconnect <name>` manage a server\n"
        "- `/plan on|off|status` controls planning mode; inline `/plan <prompt>` remains CLI/Textual-local\n"
        "- `/config` opens config help; `/config get|explain|sources|help|search|set|reset` for power users\n"
        "- `/upload <path>` uploads a local file (CLI/Textual only)\n"
        "- `/reprocess [all|<id>]` reprocesses sources (CLI/Textual only)\n"
        "- `/verbose` cycles tool detail level (CLI/Textual only)\n"
        "- `/detail` replays the last turn's tool activity (CLI/Textual only)\n"
        "- `/append <text>` appends to a note conversation\n"
        "- `/rename <title>` rename the current conversation\n"
        "- `/slug [name]` show or set the current slug\n"
        "- `/tools` list the currently available tools\n"
        "- `/skills` list available slash skills\n"
        "- `/reload-skills` reload skill files from disk\n"
        "- `/model [list|NAME]` show, list, or change the active model\n"
        "- `/usage` show token usage totals\n"
        "- `/artifact-check` run artifact health checks\n"
        "- `/quit` or `/exit` leave the app\n\n"
        "Custom skills also work here as `/skill-name ...`."
    )


def build_tools_markdown(tool_names: Sequence[str]) -> str:
    """Render tool listing as markdown."""
    if not tool_names:
        return "No tools are currently available."
    return "## Tools\n\n" + "\n".join(f"- `{name}`" for name in tool_names)


def build_skills_markdown(
    entries: Sequence[SkillDescription],
    warnings: Sequence[str],
    *,
    has_registry: bool = True,
) -> str:
    """Render skill listing as markdown."""
    if not has_registry:
        return "No skill registry is attached to this session."
    lines = ["## Skills"]
    if entries:
        for entry in entries:
            description = entry.description or "No description."
            suffix = f" ({entry.source})"
            if entry.policy_summary:
                suffix = f" [{entry.policy_summary}] ({entry.source})"
            meta_str = ""
            if entry.metadata:
                meta_parts = [f"{k}={str(v)}" for k, v in sorted(entry.metadata.items())]
                meta_str = f" [metadata: {', '.join(meta_parts)}]"
            guidance_str = f"\n    Update: {entry.update_guidance}" if entry.update_guidance else ""
            lines.append(f"- `/{entry.display_name}` — {description}{meta_str}{suffix}{guidance_str}")
    else:
        lines.append("No skills loaded. Add YAML files under `~/.anteroom/skills/` or a project `.anteroom/skills/`.")
    if warnings:
        lines.append("")
        lines.append("### Warnings")
        lines.extend(f"- {warning}" for warning in warnings)
    return "\n".join(lines)
