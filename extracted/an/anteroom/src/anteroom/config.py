"""Configuration loader: YAML file with environment variable fallbacks."""

from __future__ import annotations

import copy
import json
import logging
import os
import re
import stat
from dataclasses import dataclass, field
from dataclasses import field as _dc_field
from pathlib import Path
from typing import Any

import yaml

from .services.context_thresholds import (
    DEFAULT_CONTEXT_AUTO_COMPACT_BUFFER_TOKENS,
    DEFAULT_CONTEXT_AUTO_COMPACT_TOKENS,
    DEFAULT_CONTEXT_WARN_BUFFER_TOKENS,
    DEFAULT_CONTEXT_WARN_TOKENS,
    DEFAULT_MAX_OUTPUT_TOKENS,
    DEFAULT_MODEL_CONTEXT_WINDOW,
    DEFAULT_SUMMARY_TRIGGER_BUFFER_TOKENS,
    DEFAULT_SUMMARY_TRIGGER_TOKEN_COUNT,
    ContextThresholdConfig,
    derive_context_thresholds,
)
from .services.project_links import ProjectConfig, build_project_config

logger = logging.getLogger(__name__)

_UNSET = object()  # sentinel distinguishing "not set" from None/False/0

_BUILTIN_TOOL_DESCRIPTIONS: dict[str, str] = {
    "read_file": "Read file contents with line numbers. Use this instead of bash cat/head/tail.",
    "write_file": "Create or overwrite a file. Only use for new files or full rewrites; prefer edit_file for changes.",
    "edit_file": "Exact string replacement in files. Preferred for targeted code changes.",
    "bash": "Run shell commands (git, build tools, tests, installs). Do NOT use for file reading or searching.",
    "glob_files": "Find files and directories by name/path pattern (e.g. '**/*.py'). Use instead of bash find or ls.",
    "grep": "Regex search across file contents. Use instead of bash grep or rg.",
    "create_canvas": "Create a rich content panel (code, docs, diagrams) alongside chat.",
    "update_canvas": "Replace canvas content entirely with new content.",
    "patch_canvas": "Apply incremental search/replace edits to an existing canvas.",
    "run_agent": "Spawn a sub-agent for parallel or isolated tasks. Each gets its own context.",
    "ask_user": "Ask the user a question and wait for their response. Use instead of asking in text output.",
}


def build_runtime_context(
    *,
    model: str,
    builtin_tools: list[str] | None = None,
    mcp_servers: dict[str, dict[str, Any]] | None = None,
    interface: str = "web",
    working_dir: str | None = None,
    tls_enabled: bool = False,
    background_suggest_seconds: int = 0,
    detach_suggest_seconds: int = 0,
) -> str:
    """Build an XML-tagged runtime context block for the system prompt."""
    from anteroom import __version__ as version

    iface_label = "Web UI" if interface == "web" else "CLI REPL"

    lines = [
        "<anteroom_context>",
        f"You are Anteroom v{version}, running via the {iface_label}.",
        f"Current model: {model}",
    ]

    # Tools
    tool_lines: list[str] = []
    if builtin_tools:
        for name in builtin_tools:
            desc = _BUILTIN_TOOL_DESCRIPTIONS.get(name, "")
            tool_lines.append(f"  - {name}: {desc}" if desc else f"  - {name}")
    if mcp_servers:
        for srv_name, srv_info in mcp_servers.items():
            status = srv_info.get("status", "unknown")
            if status == "connected":
                tools = srv_info.get("tools", [])
                if isinstance(tools, list):
                    for t in tools:
                        t_name = t.get("name", t) if isinstance(t, dict) else t
                        tool_lines.append(f'  - {t_name} (via MCP server "{srv_name}")')
    if tool_lines:
        lines.append("")
        lines.append("Available tools:")
        lines.extend(tool_lines)

    # MCP servers
    if mcp_servers:
        lines.append("")
        lines.append("MCP servers:")
        for srv_name, srv_info in mcp_servers.items():
            status = srv_info.get("status", "unknown")
            tool_count = srv_info.get("tool_count", 0)
            lines.append(f"  - {srv_name}: {status} ({tool_count} tools)")

    # Capabilities
    lines.append("")
    lines.append("Anteroom capabilities:")
    if interface == "web":
        lines.append(
            "  - Web UI: 4 themes (Midnight/Dawn/Aurora/Ember), conversation folders & tags, "
            "projects with custom instructions, file attachments, command palette (Cmd/Ctrl+K), "
            "model switching, prompt queuing, shared databases"
        )
    else:
        lines.append(
            "  - CLI: built-in file/shell tools, MCP integration, skills system, "
            "@file references, /commands, ANTEROOM.md project instructions"
        )
    lines.append(
        "  - Shared: SQLite with FTS search, conversation forking & rewinding, "
        "SSE streaming, OpenAI-compatible API backend"
    )

    # Config details
    if interface == "cli" and working_dir:
        lines.append(f"\nWorking directory: {working_dir}")
    if interface == "web":
        lines.append(f"\nTLS: {'enabled' if tls_enabled else 'disabled'}")

    # Execution surface routing advisory (#1317)
    if background_suggest_seconds > 0 or detach_suggest_seconds > 0:
        lines.append("")
        lines.append("Execution surface routing:")
        if background_suggest_seconds > 0:
            lines.append(
                f"  - For shell commands expected to take over {background_suggest_seconds}s, "
                "use background: true to keep the conversation responsive."
            )
        if detach_suggest_seconds > 0:
            lines.append(
                f"  - For AI work expected to take over {detach_suggest_seconds}s with no required "
                "inline return, use detach: true on run_agent."
            )
        lines.append("  - For multi-step pipelines with checkpoints, prefer a workflow definition.")
        lines.append("  - When you choose an execution surface, briefly tell the user why.")

    lines.append("</anteroom_context>")
    return "\n".join(lines)


_DEFAULT_SYSTEM_PROMPT = """\
You are Anteroom, a capable AI coding assistant with direct access to tools for interacting with \
the user's local system and external services. You operate as a hands-on partner — not a suggestion \
engine. You help developers write, debug, refactor, and understand code.

<agentic_behavior>
- Complete tasks fully and autonomously. When a task requires multiple steps or tool calls, execute \
all steps without pausing to ask the user for confirmation between them. Keep going until the work \
is done.
- Default to action over suggestion. If the user asks you to do something and you have the tools to \
do it, do it — don't describe what you would do instead.
- If a multi-step operation involves batches, pagination, or iteration, continue through all \
iterations automatically. Never stop partway to ask "should I continue?" unless you hit an error or \
genuine ambiguity.
- Only ask the user a question when you need information you truly cannot infer from context, \
available tools, or prior conversation. When you do ask, ask one focused question, not a list.
- IMPORTANT: When you need to ask the user a question, you MUST use the ask_user tool. Do NOT \
ask questions in your text output — the user cannot respond to text mid-turn. The ask_user tool \
pauses execution and waits for a response before continuing.
</agentic_behavior>

<tool_use>
DO NOT use bash to do what dedicated tools can do:
- To read files, use read_file — not cat, head, tail, or sed.
- To edit files, use edit_file — not sed, awk, or echo redirection.
- To create files, use write_file — not cat with heredoc or echo.
- To search for files or directories by name, use glob_files — not find or ls.
- To search file contents, use grep — not bash grep or rg.
Reserve bash for system commands that require shell execution: git, build tools, package managers, \
running tests, starting servers.

Tool selection:
- Prefer edit_file over write_file for modifying existing files. edit_file makes targeted changes; \
write_file replaces the entire file.
- Prefer grep over bash for searching code. Prefer glob_files over bash for finding files or directories.
- Read files before modifying them. Never assume you know a file's current contents.

Parallel execution:
- When multiple tool calls are independent of each other, make them all in parallel in the same \
response. For example, reading 3 files should be 3 parallel read_file calls, not sequential.
- If one tool call depends on the result of another, run them sequentially — never guess at \
dependent values.

Error handling:
- If a tool call fails, analyze the error and try a different approach. Do not repeat the exact \
same call.
- After two failures on the same operation, explain the issue to the user.
- Treat tool outputs as real data. Never fabricate or hallucinate tool results.
</tool_use>

<code_modification>
- Always read a file before modifying it. Do not propose changes to code you have not read.
- Prefer editing existing files over creating new ones. Build on existing work.
- Understand existing code before suggesting modifications. Look at surrounding patterns, naming \
conventions, and architecture before writing new code.
- Produce working code with necessary imports, error handling, and type hints. Never output \
pseudocode or partial snippets when the user needs a real implementation.
- Match the conventions of the surrounding codebase: indentation, naming, patterns, structure.

Avoid over-engineering:
- Only make changes that are directly requested or clearly necessary.
- Don't add features, refactor code, or make "improvements" beyond what was asked.
- Don't add docstrings, comments, or type annotations to code you didn't change.
- Don't create helpers, utilities, or abstractions for one-time operations. Three similar lines \
of code is better than a premature abstraction.
- Don't add error handling or validation for scenarios that cannot happen. Trust internal code and \
framework guarantees; only validate at system boundaries.
</code_modification>

<git_operations>
When performing git operations:
- Never run destructive git commands (push --force, reset --hard, checkout ., clean -f, branch -D) \
unless the user explicitly requests them.
- Never amend published commits or skip hooks (--no-verify) unless explicitly asked.
- When staging files, prefer adding specific files by name rather than "git add -A" or "git add .", \
which can accidentally include secrets or binaries.
- Never force-push to main/master. Warn the user if they request it.
- Prefer creating new commits over amending existing ones.
- When a pre-commit hook fails, the commit did not happen — do not use --amend (which would modify \
the previous commit). Fix the issue, re-stage, and create a new commit.
</git_operations>

<investigation>
- Never speculate about code you have not read. If the user references a file, read it first.
- If the user asks about system state, configuration, or behavior, verify with tools rather than \
guessing from memory.
- When debugging, gather evidence before hypothesizing. Read error messages, check logs, inspect \
the actual state — don't assume.
- If you are uncertain about something, say what you know and what you don't, rather than \
presenting guesses as facts.
</investigation>

<communication>
- Be direct and concise. Lead with the answer or action, not preamble.
- Never open with flattery ("Great question!") or filler ("I'd be happy to help!"). Just respond.
- Don't apologize for unexpected results — investigate and fix them.
- Use markdown formatting naturally: code blocks with language tags, headers for structure in longer \
responses, tables when comparing data. Keep formatting minimal for short answers.
- When explaining what you did, focus on outcomes and key decisions, not a narration of every step.
- If the user is wrong about something, say so directly and explain why.
</communication>

<safety>
Carefully consider the reversibility and impact of actions. You can freely take local, reversible \
actions like editing files or running tests. But for actions that are hard to reverse, affect shared \
systems, or could be destructive, confirm with the user first.

Actions that always require confirmation:
- Deleting files, branches, database tables, or processes (rm -rf, git branch -D, DROP TABLE)
- Force-pushing, resetting hard, discarding uncommitted changes (git push --force, git reset --hard)
- Pushing code, creating PRs, commenting on issues, sending messages to external services
- Modifying shared infrastructure, permissions, or CI/CD configuration

Security:
- Never output, log, or commit secrets, credentials, API keys, or tokens.
- Do not introduce security vulnerabilities: no SQL injection, command injection, XSS, path \
traversal, or other OWASP top 10 issues. If you notice insecure code, fix it immediately.
- Use parameterized queries for database operations. Never concatenate user input into SQL.
- Never use eval(), exec(), or subprocess with shell=True on user-controlled input.
- Prefer reversible approaches: git reverts over file deletion, edits over full overwrites.
</safety>"""


@dataclass
class AIConfig:
    base_url: str
    api_key: str
    model: str = "gpt-4"
    system_prompt: str = _DEFAULT_SYSTEM_PROMPT
    user_system_prompt: str = ""
    verify_ssl: bool = True
    api_key_command: str = ""
    request_timeout: int = 120  # seconds; overall stream timeout
    connect_timeout: int = 5  # seconds; TCP connect timeout
    write_timeout: int = 30  # seconds; time to send request body
    pool_timeout: int = 10  # seconds; wait for free connection from pool
    first_token_timeout: int = 30  # seconds; max wait for first token after connect
    chunk_stall_timeout: int = 30  # seconds; max silence between chunks mid-stream
    retry_max_attempts: int = 3  # retries on transient errors (0 = disabled)
    retry_backoff_base: float = 1.0  # seconds; base for exponential backoff
    narration_cadence: int = 8  # progress updates every N tool calls; 0 = disabled
    max_tools: int = 128  # hard cap on tools per request; 0 = unlimited
    temperature: float | None = None  # None = provider default; 0.0-2.0
    top_p: float | None = None  # None = provider default; 0.0-1.0
    seed: int | None = None  # None = provider default; any int for deterministic output
    allowed_domains: list[str] = field(default_factory=list)  # empty = no restriction
    allowed_models: list[str] = field(default_factory=list)  # empty = show all
    block_localhost_api: bool = False  # when True, reject loopback/localhost base_url
    provider: str = "openai"  # "openai", "anthropic", or "litellm"
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    """Required by Anthropic; used as max_tokens for Anthropic provider."""
    litellm_bedrock_tools_confirmed: bool = False  # opt-in for Bedrock tool calling via LiteLLM
    model_family_aliases: dict[str, str] = field(default_factory=dict)  # map family names to model IDs


@dataclass
class McpServerConfig:
    name: str
    transport: str  # "stdio" or "sse"
    command: str | None = None
    args: list[str] = field(default_factory=list)
    url: str | None = None
    env: dict[str, str] = field(default_factory=dict)
    timeout: float = 30.0  # seconds; connection timeout per server
    tools_include: list[str] = field(default_factory=list)  # allowlist; fnmatch patterns
    tools_exclude: list[str] = field(default_factory=list)  # blocklist; fnmatch patterns
    trust_level: str = "untrusted"  # "trusted" or "untrusted"; controls defensive prompt envelopes on tool results

    def __post_init__(self) -> None:
        if self.trust_level not in ("trusted", "untrusted"):
            raise ValueError(f"trust_level must be 'trusted' or 'untrusted', got {self.trust_level!r}")


@dataclass
class SharedDatabaseConfig:
    name: str
    path: str
    passphrase_hash: str = ""


@dataclass
class AppSettings:
    host: str = "127.0.0.1"
    port: int = 8080
    data_dir: Path = field(default_factory=lambda: Path.home() / ".anteroom")
    tls: bool = False


@dataclass
class PlanningConfig:
    enabled: bool = True
    auto_threshold_tools: int = 15
    auto_mode: str = "off"  # "off", "suggest", or "auto"


@dataclass
class BudgetConfig:
    """Token budget enforcement for denial-of-wallet prevention."""

    enabled: bool = False
    max_tokens_per_request: int = 0  # 0 = unlimited
    max_tokens_per_conversation: int = 0  # 0 = unlimited
    max_tokens_per_day: int = 0  # 0 = unlimited
    warn_threshold_percent: int = 80  # emit warning at this % of limit
    action_on_exceed: str = "block"  # "block" or "warn"


@dataclass
class UsageConfig:
    """Token usage tracking and cost estimation settings."""

    week_days: int = 7  # number of days in a "week" period
    month_days: int = 30  # number of days in a "month" period
    model_costs: dict[str, dict[str, float]] = field(
        default_factory=lambda: {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-4.1": {"input": 2.00, "output": 8.00},
            "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
            "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
            "o3": {"input": 2.00, "output": 8.00},
            "o3-mini": {"input": 1.10, "output": 4.40},
            "o4-mini": {"input": 1.10, "output": 4.40},
            "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
            "claude-opus-4-20250514": {"input": 15.00, "output": 75.00},
            "claude-haiku-4-20250514": {"input": 0.80, "output": 4.00},
        }
    )  # per 1M tokens
    budgets: BudgetConfig = field(default_factory=BudgetConfig)


@dataclass
class SkillsConfig:
    auto_invoke: bool = True  # let the AI auto-invoke skills from natural language


@dataclass
class CompactionConfig:
    """Shared configuration for conversation history compaction (#1412, #1413).

    Owned by the compaction service (``services/compaction.py``).  Both the
    shared agent loop's auto-compact path and the CLI ``/compact`` command
    read from this config.
    """

    preserve_tail: int = 6
    """Recent messages preserved intact during compaction.

    When > 0, only the older portion of the conversation is summarised and
    the trailing N messages are kept verbatim, with walk-back rules to
    guarantee provider-safe ordering (see ``_find_tail_boundary``).  When 0,
    compaction reverts to the legacy full-summary behaviour.

    Clamped to ``[0, 200]`` at load time to guard against misconfiguration
    silently defeating compaction.
    """

    compact_rehydrate: bool = True
    """Append a bounded ``<session_state>`` block to compaction summaries (#1414).

    When True, the shared compaction service scans the messages being
    summarised and appends a deterministic block listing recently touched
    files, the last working directory, and unresolved tool errors.  When
    False, the summary prose is the only source of post-compact state.
    """

    compact_rehydrate_max_files: int = 20
    """Max file paths preserved per category (read/written/edited) in the
    ``<session_state>`` block.  Most recent entries are kept, deduplicated.
    Clamped to ``[0, 200]`` at load time."""

    compact_rehydrate_max_errors: int = 5
    """Max unresolved tool errors preserved in the ``<session_state>`` block.
    Most recent entries are kept.  Clamped to ``[0, 50]`` at load time."""

    microcompact_enabled: bool = True
    """Enable the proactive microcompact stage (#1266).

    When True, the agent loop runs a cheap, deterministic, in-memory
    history sweep before each LLM call. It includes oversized-tool-output
    trimming and token-pressure historical tool-result collapse. The former reads
    ``cli.tool_output_max_chars`` (the single trim-threshold authority,
    shared with reactive Strategy 1). Microcompact runs in-memory only;
    it never writes to SQLite."""

    historical_tool_collapse_enabled: bool = True
    """Enable proactive collapse of older tool-result content under token pressure.

    When True, the agent loop may compact historical tool results before
    LLM-backed summary compaction is needed. The strategy is turn-group aware,
    preserves recent groups, and never writes collapsed results to SQLite."""

    historical_tool_collapse_trigger_token_count: int = 80_000
    """Estimated-token threshold for proactive historical tool-result collapse.

    Clamped to ``[5_000, 500_000]`` at load time. This default is below the
    summary compaction threshold so deterministic collapse can reduce pressure
    before an LLM-backed summary is required."""

    historical_tool_collapse_keep_recent_groups: int = 6
    """Recent turn groups left untouched by proactive historical collapse.

    Clamped to ``[0, 200]`` at load time. Turn groups keep assistant tool calls
    together with their matching tool results."""

    historical_tool_collapse_compact_chars: int = 1_000
    """Character budget for each collapsed historical tool result.

    Clamped to ``[50, 50_000]`` at load time. Structured fields such as status,
    path, exit code, and error remain visible when they fit within the budget."""

    summary_trigger_msg_count: int = 80
    """Message-count threshold that triggers proactive summary compaction.

    When ``len(messages)`` reaches this value, the agent loop fires the
    LLM-backed summary compaction path. Clamped to ``[10, 1000]`` at
    load time. Legacy module constant
    ``services.compaction.PROACTIVE_COMPACTION_MSG_THRESHOLD`` reads
    from this field for backward compatibility."""

    summary_trigger_token_count: int = DEFAULT_SUMMARY_TRIGGER_TOKEN_COUNT
    """Estimated-token threshold that triggers proactive summary compaction.

    When the estimated prompt token count reaches this value, the agent
    loop fires the LLM-backed summary compaction path. Clamped to
    ``[5_000, 500_000]`` at load time. Legacy module constant
    ``services.compaction.PROACTIVE_COMPACTION_TOKEN_THRESHOLD`` reads
    from this field for backward compatibility."""

    summary_trigger_buffer_tokens: int = DEFAULT_SUMMARY_TRIGGER_BUFFER_TOKENS
    """Tokens to keep free before proactive summary compaction when deriving
    ``summary_trigger_token_count`` from the active model context window."""

    reactive_max_attempts: int = 4
    """Max bounded retries after a ``context_length_exceeded`` error.

    The reactive overflow ladder (#1415) at ``services/agent_loop.py``
    cycles through its four strategies at most this many times before
    giving up. Clamped to ``[0, 10]`` at load time. ``0`` disables
    reactive recovery entirely (not recommended — the loop will
    surface the original provider error)."""

    summary_max_completion_tokens: int = 1000
    """Maximum output budget for LLM compaction summaries.

    The service scales the requested summary budget with conversation size,
    capped by this value. Clamped to ``[256, 16000]`` at load time."""

    summary_retry_max_attempts: int = 3
    """Total summary attempts for prompt-too-long compaction failures.

    Retries only occur for structured ``context_length_exceeded`` failures.
    Clamped to ``[1, 10]`` at load time."""

    summary_retry_drop_groups: int = 2
    """Oldest safe turn groups to drop before each summary retry.

    Turn-group boundaries keep assistant tool calls attached to tool results.
    Clamped to ``[1, 50]`` at load time."""


@dataclass
class CliHierarchyConfig:
    """Visual-hierarchy knobs for CLI rendering (#1370).

    All three fields default to preserving existing observable behaviour:
    timestamps are off, ``turn_separator_char`` is only emitted when the
    explicit helper is called, and the additive ``code_block_language_label``
    is a low-risk visual hint that themes can style.
    """

    show_timestamps: bool = False
    turn_separator_char: str = "\u2500"
    code_block_language_label: bool = True


@dataclass
class CliStreamingConfig:
    """Live markdown streaming knobs for CLI rendering (#1365).

    Drives the ``rich.live.Live``-backed incremental renderer that shows
    markdown formatting (bold/italic/code-fence/headers) as tokens arrive,
    instead of buffering silently and rendering once at the end of the turn.

    Auto-disabled at runtime in non-TTY, ``NO_COLOR``, and exec-mode contexts
    regardless of ``enabled`` — see ``cli/streaming.py`` for the guard.
    """

    enabled: bool = False
    refresh_hz: float = 20.0
    live_in_exec_mode: bool = False
    code_fence_container: bool = True


@dataclass
class CliLiveToolsConfig:
    """Live tool-call lifecycle rendering knobs (#1364).

    Controls the compact two-phase tool-call surface in the CLI REPL: a
    running phase carried by the unified thinking/footer ticker, and a
    completion phase rendered as a single concise line via
    ``render_tool_call_completion()``.

    All three fields default to the values that produce the richest
    completion line; users can opt out of the args footline or the
    metric suffix per preference.
    """

    show_args_in_verbose: bool = True
    show_metric_suffix: bool = True
    metric_max_chars: int = 40


@dataclass
class CliDensityConfig:
    """Tool-result density knobs for CLI rendering (#1367).

    Controls how tool-call *results* are rendered in the CLI: how much of the
    output body is shown, whether diff context lines are collapsed, whether
    identical-shape results are deduplicated, etc.

    ``mode`` defaults to ``"normal"`` — which is byte-identical to the
    pre-#1367 rendering path. Users opt into smart summaries by setting
    ``"compact"`` or ``"minimal"`` (or the ``/density`` slash command at
    runtime). ``"detailed"`` expands the existing ``Verbosity.DETAILED``
    body-rendering. ``"auto"`` maps from the current ``Verbosity`` state.
    """

    mode: str = "normal"
    collapse_repeats: bool = True
    diff_context_lines: int = 3
    head_lines: int = 3
    tail_lines: int = 2


@dataclass
class CliInputConfig:
    """CLI input-surface controls for prompt-toolkit polish (#1369)."""

    editing_mode: str = "emacs"  # "emacs" or "vi"
    show_hints: bool = True
    hint_max_displays: int = 1  # per hint context, per session
    large_paste_lines: int = 5
    show_mode_badge: bool = False


@dataclass
class CliConfig:
    theme: str = "midnight"
    builtin_tools: bool = True
    max_tool_iterations: int = 50
    max_consecutive_text_only: int = 3  # stop after N text-only responses with no tool calls (0 = disabled)
    max_line_repeats: int = 5  # stop if a single response repeats the same line N+ times (0 = disabled)
    context_warn_tokens: int = DEFAULT_CONTEXT_WARN_TOKENS
    context_auto_compact_tokens: int = DEFAULT_CONTEXT_AUTO_COMPACT_TOKENS
    context_reserved_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    context_warn_buffer_tokens: int = DEFAULT_CONTEXT_WARN_BUFFER_TOKENS
    context_auto_compact_buffer_tokens: int = DEFAULT_CONTEXT_AUTO_COMPACT_BUFFER_TOKENS
    tool_dedup: bool = True  # collapse consecutive similar tool calls; False = show all
    retry_delay: float = 5.0  # seconds between CLI auto-retry countdown ticks
    max_retries: int = 3  # max CLI auto-retry attempts for retryable errors
    esc_hint_delay: float = 8.0  # seconds before showing "esc to cancel" hint
    stall_display_threshold: float = 5.0  # seconds of chunk silence before showing "stalled"
    stall_warning_threshold: float = 15.0  # seconds before showing full stall warning
    stall_throughput_threshold: float = 30.0  # chars/sec below which "slow" indicator shows
    tool_output_max_chars: int = 10_000  # max chars per tool result before truncation
    tool_replay_max_chars: int = 10_000  # max chars per tool result on conversation resume
    file_reference_max_chars: int = 100_000  # max chars from @file references
    model_context_window: int = DEFAULT_MODEL_CONTEXT_WINDOW  # model context window size for usage bar
    background_suggest_seconds: int = 30  # advisory threshold for background shell tasks (0 = disabled)
    detach_suggest_seconds: int = 120  # advisory threshold for detached subagents (0 = disabled)
    update_check: bool = True  # check PyPI for newer versions on startup
    update_check_command: str = ""  # custom command returning latest version (replaces pip index)
    # Startup update notification template; empty string suppresses notification.
    update_check_message: str = "Update available: {current} -> {latest} -- pip install --upgrade anteroom"
    show_attribution_footer: bool = True  # compact per-turn attribution line in CLI (#923)
    planning: PlanningConfig = field(default_factory=PlanningConfig)
    usage: UsageConfig = field(default_factory=UsageConfig)
    skills: SkillsConfig = field(default_factory=SkillsConfig)
    hierarchy: CliHierarchyConfig = field(default_factory=CliHierarchyConfig)
    streaming: CliStreamingConfig = field(default_factory=CliStreamingConfig)
    live_tools: CliLiveToolsConfig = field(default_factory=CliLiveToolsConfig)
    density: CliDensityConfig = field(default_factory=CliDensityConfig)
    input: CliInputConfig = field(default_factory=CliInputConfig)


@dataclass
class UserIdentity:
    user_id: str
    display_name: str
    public_key: str  # PEM
    private_key: str  # PEM


@dataclass
class EmbeddingsConfig:
    enabled: bool | None = None  # None = auto-detect at startup, True = force-enable, False = force-disable
    provider: str = "local"  # "local" (fastembed) or "api" (OpenAI-compatible)
    model: str = "text-embedding-3-small"
    dimensions: int = 0  # 0 = auto-detect from provider/model
    local_model: str = "BAAI/bge-small-en-v1.5"
    base_url: str = ""
    api_key: str = ""
    api_key_command: str = ""
    cache_dir: str = ""  # custom fastembed cache directory for offline/vendored models


@dataclass
class SafetyToolConfig:
    enabled: bool = True


@dataclass
class OsSandboxConfig:
    """OS-level sandbox controls (Win32 Job Objects on Windows, no-op elsewhere)."""

    enabled: bool | None = None  # None = auto-detect (True on Windows)
    max_memory_mb: int = 512
    max_processes: int = 10
    cpu_time_limit: int | None = None  # CPU seconds, None = no limit

    _MIN_MEMORY_MB: int = field(default=64, init=False, repr=False)
    _MIN_PROCESSES: int = field(default=1, init=False, repr=False)
    _MAX_PROCESSES: int = field(default=1000, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.max_memory_mb < self._MIN_MEMORY_MB:
            logger.warning(
                "sandbox max_memory_mb=%d below minimum (%d), clamping",
                self.max_memory_mb,
                self._MIN_MEMORY_MB,
            )
            object.__setattr__(self, "max_memory_mb", self._MIN_MEMORY_MB)
        if self.max_processes < self._MIN_PROCESSES:
            object.__setattr__(self, "max_processes", self._MIN_PROCESSES)
        if self.max_processes > self._MAX_PROCESSES:
            object.__setattr__(self, "max_processes", self._MAX_PROCESSES)
        if self.cpu_time_limit is not None and self.cpu_time_limit < 1:
            object.__setattr__(self, "cpu_time_limit", 1)

    @property
    def is_enabled(self) -> bool:
        """Resolve enabled state: None means auto-detect (True on Windows)."""
        if self.enabled is None:
            import sys

            return sys.platform == "win32"
        return self.enabled


@dataclass
class BashSandboxConfig:
    """Bash tool sandboxing controls. All fields have safe defaults."""

    enabled: bool = True
    timeout: int = 120  # per-command timeout in seconds
    max_output_chars: int = 100_000
    blocked_paths: list[str] = field(default_factory=list)
    allowed_paths: list[str] = field(default_factory=list)
    blocked_commands: list[str] = field(default_factory=list)
    allow_network: bool = True
    allow_package_install: bool = True
    log_all_commands: bool = False
    sandbox: OsSandboxConfig = field(default_factory=OsSandboxConfig)

    _MIN_TIMEOUT: int = field(default=1, init=False, repr=False)
    _MAX_TIMEOUT: int = field(default=600, init=False, repr=False)
    _MIN_OUTPUT: int = field(default=1000, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.timeout < self._MIN_TIMEOUT:
            logger.warning("bash timeout=%d below minimum (%d), clamping", self.timeout, self._MIN_TIMEOUT)
            object.__setattr__(self, "timeout", self._MIN_TIMEOUT)
        if self.timeout > self._MAX_TIMEOUT:
            logger.warning("bash timeout=%d above maximum (%d), clamping", self.timeout, self._MAX_TIMEOUT)
            object.__setattr__(self, "timeout", self._MAX_TIMEOUT)
        if self.max_output_chars < self._MIN_OUTPUT:
            logger.warning(
                "bash max_output_chars=%d below minimum (%d), clamping",
                self.max_output_chars,
                self._MIN_OUTPUT,
            )
            object.__setattr__(self, "max_output_chars", self._MIN_OUTPUT)


@dataclass
class SubagentConfig:
    max_concurrent: int = 5
    max_total: int = 10
    max_depth: int = 3
    max_iterations: int = 15
    timeout: int = 120
    max_output_chars: int = 4000
    max_prompt_chars: int = 32_000


@dataclass
class ToolRateLimitConfig:
    max_calls_per_minute: int = 0
    max_calls_per_conversation: int = 0
    max_consecutive_failures: int = 5
    action: str = "block"


@dataclass
class DlpPatternConfig:
    """A single DLP detection rule."""

    name: str = ""
    pattern: str = ""
    description: str = ""


@dataclass
class DlpConfig:
    """Data Loss Prevention scanning configuration."""

    enabled: bool = False
    scan_output: bool = True
    scan_input: bool = False  # Reserved for future use
    action: str = "redact"  # "redact", "block", "warn"
    patterns: list[DlpPatternConfig] = field(default_factory=list)  # Replaces built-in patterns
    custom_patterns: list[DlpPatternConfig] = field(default_factory=list)  # Appended to patterns
    redaction_string: str = "[REDACTED]"
    log_detections: bool = True

    def __post_init__(self) -> None:
        if self.action not in ("redact", "block", "warn"):
            logger.warning("Invalid DLP action '%s', defaulting to 'redact'", self.action)
            object.__setattr__(self, "action", "redact")


@dataclass
class PromptInjectionConfig:
    """Prompt injection detection configuration."""

    enabled: bool = False
    action: str = "warn"  # "block", "warn", "log"
    canary_length: int = 16  # bytes of randomness for canary token
    detect_encoding_attacks: bool = True
    detect_instruction_override: bool = True
    heuristic_threshold: float = 0.7  # minimum confidence to trigger action
    log_detections: bool = True

    def __post_init__(self) -> None:
        if self.action not in ("block", "warn", "log"):
            logger.warning("Invalid injection detection action '%s', defaulting to 'warn'", self.action)
            object.__setattr__(self, "action", "warn")
        if self.canary_length < 8:
            object.__setattr__(self, "canary_length", 8)
        elif self.canary_length > 64:
            object.__setattr__(self, "canary_length", 64)
        if self.heuristic_threshold < 0.0:
            object.__setattr__(self, "heuristic_threshold", 0.0)
        elif self.heuristic_threshold > 1.0:
            object.__setattr__(self, "heuristic_threshold", 1.0)


@dataclass
class OutputFilterPatternConfig:
    """A custom output filter pattern rule."""

    name: str = ""
    pattern: str = ""
    description: str = ""


@dataclass
class OutputFilterConfig:
    """Output content filter configuration (system prompt leak detection + custom patterns)."""

    enabled: bool = False
    system_prompt_leak_detection: bool = True
    leak_threshold: float = 0.4
    custom_patterns: list[OutputFilterPatternConfig] = field(default_factory=list)
    action: str = "warn"  # "warn", "block", "redact"
    redaction_string: str = "[FILTERED]"
    log_detections: bool = True

    def __post_init__(self) -> None:
        if self.action not in ("warn", "block", "redact"):
            logger.warning("Invalid output_filter action '%s', defaulting to 'warn'", self.action)
            object.__setattr__(self, "action", "warn")
        if not 0.0 < self.leak_threshold <= 1.0:
            logger.warning("Invalid leak_threshold %s, defaulting to 0.4", self.leak_threshold)
            object.__setattr__(self, "leak_threshold", 0.4)


@dataclass
class SafetyConfig:
    enabled: bool = True
    approval_mode: str = "ask_for_writes"
    approval_timeout: int = 120
    bash: BashSandboxConfig = field(default_factory=BashSandboxConfig)
    write_file: SafetyToolConfig = field(default_factory=SafetyToolConfig)
    custom_patterns: list[str] = field(default_factory=list)
    sensitive_paths: list[str] = field(default_factory=list)
    allowed_tools: list[str] = field(default_factory=list)
    denied_tools: list[str] = field(default_factory=list)
    tool_tiers: dict[str, str] = field(default_factory=dict)
    read_only: bool = False
    subagent: SubagentConfig = field(default_factory=SubagentConfig)
    tool_rate_limit: ToolRateLimitConfig = field(default_factory=ToolRateLimitConfig)
    dlp: DlpConfig = field(default_factory=DlpConfig)
    prompt_injection: PromptInjectionConfig = field(default_factory=PromptInjectionConfig)
    output_filter: OutputFilterConfig = field(default_factory=OutputFilterConfig)
    bypass_immune_paths: list[str] = field(
        default_factory=lambda: [
            ".git/hooks",
            ".anteroom/config.yaml",
            ".bashrc",
            ".bash_profile",
            ".zshrc",
            ".profile",
            ".ssh/",
            ".gnupg/",
            ".aws/credentials",
            ".config/gcloud/",
            ".netrc",
            ".kube/config",
            ".config/gh/hosts.yml",
        ]
    )


@dataclass
class RagConfig:
    """Retrieval-augmented generation settings."""

    enabled: bool = True  # auto-enabled when embeddings are available
    max_chunks: int = 10  # top-K chunks to retrieve per query
    max_tokens: int = 2000  # token budget for injected context (chars/4 estimate)
    similarity_threshold: float = 0.5  # max cosine distance; lower = stricter matching
    include_sources: bool = True  # search source chunks
    include_conversations: bool = True  # search past conversation messages
    exclude_current: bool = True  # exclude current conversation from results
    retrieval_mode: str = "dense"  # "dense", "keyword", or "hybrid"
    show_status: bool = True  # show RAG status messages in CLI


@dataclass
class RerankerConfig:
    """Cross-encoder reranker settings."""

    enabled: bool | None = None  # None = auto-detect (use if fastembed available)
    provider: str = "local"  # "local" (fastembed TextCrossEncoder); only local is supported
    model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    top_k: int = 5  # keep top-K after reranking (capped to rag.max_chunks at runtime)
    score_threshold: float = 0.0  # minimum relevance score (cross-encoder logit); 0 = no threshold
    candidate_multiplier: int = 3  # fetch top_k * multiplier candidates before reranking
    cache_dir: str = ""  # custom fastembed cache directory for offline/vendored models


@dataclass
class MemoryRecallConfig:
    """Runtime recall of typed memory artifacts (#921).

    Recall runs per-turn alongside RAG.  Scope visibility, token budget, and
    distance threshold are all independent from ``RagConfig`` so memory can
    be tuned without affecting source retrieval.
    """

    enabled: bool | None = None  # None = auto-detect (use if embeddings available)
    max_memories: int = 5  # top-K memories to inject per turn
    max_tokens: int = 800  # independent token budget (char/4 estimate)
    similarity_threshold: float = 0.5  # max cosine distance; lower = stricter
    show_status: bool = True  # show recall status line in CLI renderer


@dataclass
class CodebaseIndexConfig:
    """Tree-sitter codebase index settings."""

    enabled: bool = True  # auto-enabled; degrades gracefully without tree-sitter
    map_tokens: int = 1000  # token budget for the injected codebase map
    languages: list[str] = field(default_factory=list)  # auto-detect if empty
    exclude_dirs: list[str] = field(
        default_factory=lambda: [
            "node_modules",
            ".git",
            "__pycache__",
            "venv",
            ".venv",
            "dist",
            "build",
            ".tox",
            ".mypy_cache",
            ".pytest_cache",
            "egg-info",
        ]
    )


@dataclass
class ProxyConfig:
    enabled: bool = False  # opt-in; must be explicitly enabled
    allowed_origins: list[str] = field(default_factory=list)


@dataclass
class ReferencesConfig:
    """Paths to external instruction, rule, and skill files.

    All paths are resolved relative to the config file that declares them.
    Team and project configs can use this to share instructions, rules,
    and skills across the team or per project.
    """

    instructions: list[str] = field(default_factory=list)
    rules: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)


@dataclass
class ServerConfig:
    """HTTP server settings."""

    max_upload_mb: int = 50  # max request body size in MB; clamped [1, 1000]


@dataclass
class RateLimitConfig:
    """HTTP rate limiting settings."""

    max_requests: int = 120  # max requests per window per IP
    window_seconds: int = 60  # sliding window size
    exempt_paths: list[str] = field(default_factory=lambda: ["/api/events"])
    sse_retry_ms: int = 5000  # retry: field sent to EventSource clients (ms)


@dataclass
class SessionConfig:
    """Session management and network access control settings."""

    store: str = "memory"  # "memory" or "sqlite"
    max_concurrent_sessions: int = 0  # 0 = unlimited
    idle_timeout: int = 1800  # seconds (30 minutes)
    absolute_timeout: int = 43200  # seconds (12 hours)
    allowed_ips: list[str] = field(default_factory=list)  # CIDR or exact; empty = allow all

    _MIN_IDLE_TIMEOUT: int = field(default=60, init=False, repr=False)
    _MIN_ABSOLUTE_TIMEOUT: int = field(default=300, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.idle_timeout < self._MIN_IDLE_TIMEOUT:
            logger.warning(
                "idle_timeout=%d is below minimum (%d), clamping",
                self.idle_timeout,
                self._MIN_IDLE_TIMEOUT,
            )
            object.__setattr__(self, "idle_timeout", self._MIN_IDLE_TIMEOUT)
        if self.absolute_timeout < self._MIN_ABSOLUTE_TIMEOUT:
            logger.warning(
                "absolute_timeout=%d is below minimum (%d), clamping",
                self.absolute_timeout,
                self._MIN_ABSOLUTE_TIMEOUT,
            )
            object.__setattr__(self, "absolute_timeout", self._MIN_ABSOLUTE_TIMEOUT)


@dataclass
class StorageConfig:
    """Data retention and encryption at rest settings."""

    retention_days: int = 0  # 0 = disabled (keep forever)
    retention_check_interval: int = 3600  # seconds between retention checks
    purge_attachments: bool = True  # also delete attachment files on disk
    purge_embeddings: bool = True  # also purge orphaned embeddings
    encrypt_at_rest: bool = False  # requires sqlcipher3 optional dependency
    encryption_kdf: str = "hkdf-sha256"  # key derivation from identity key

    _MIN_RETENTION_INTERVAL: int = field(default=60, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.retention_check_interval < self._MIN_RETENTION_INTERVAL:
            logger.warning(
                "retention_check_interval=%d is below minimum (%d), clamping",
                self.retention_check_interval,
                self._MIN_RETENTION_INTERVAL,
            )
            object.__setattr__(self, "retention_check_interval", self._MIN_RETENTION_INTERVAL)


@dataclass
class AuditConfig:
    """Structured audit log settings."""

    enabled: bool = False
    log_path: str = ""  # empty = default to data_dir/audit/
    tamper_protection: str = "hmac"  # "none" or "hmac"
    rotation: str = "daily"  # "daily" or "size"
    rotate_size_bytes: int = 10_485_760  # 10 MB; only used when rotation=size
    retention_days: int = 90  # 0 = keep forever
    redact_content: bool = True  # log metadata only, strip message/tool content
    events: dict[str, bool] = field(
        default_factory=lambda: {
            "auth": True,
            "tool_calls": True,
            "dlp": True,
            "output_filter": True,
            "workflow": True,
            "memory": True,
            "subagent": True,
        }
    )


@dataclass
class MemoryPromotionConfig:
    """Governed memory promotion / review pipeline settings (#920).

    Defaults are conservative: agent proposals are allowed but land as
    ``candidate`` for explicit review; ``local_auto_approve`` is off by
    design so durable memory is never an invisible side effect of chat.
    Rate-limit and lineage caps bound the blast radius of a misbehaving
    proposer.
    """

    default_review_state: str = "candidate"  # "candidate" or "pending_review"
    local_auto_approve: bool = False  # escape hatch for solo/local mode
    agent_proposals_enabled: bool = True  # allow proposer="agent" calls
    max_lineage_entries: int = 50  # FIFO cap on decision history per memory
    max_candidates_per_conversation: int = 10  # per-conversation proposal cap
    max_reject_reason_chars: int = 500  # server-side bound on reject reason


@dataclass
class MemoryRetentionConfig:
    """Memory-artifact retention / eviction policy (#625).

    Defaults are conservative: ``enabled=False`` means the retention
    worker performs no memory eviction at all — zero-config does not
    delete memories. The pin flag (``pinned: True`` on a memory's
    metadata) is load-bearing and always honoured unless
    ``respect_pins=False``. A ``min_age_days`` grace floor prevents an
    ``idle_days`` rule from immediately evicting freshly-approved
    memories.
    """

    enabled: bool = False  # opt-in; default no eviction
    max_age_days: int | None = None  # purge memories older than N days; None = off
    idle_days: int | None = None  # purge memories not recalled in N days; None = off
    min_age_days: int = 1  # idle-rule grace floor against freshly-approved memories
    purge_statuses: list[str] = field(default_factory=lambda: ["rejected"])
    respect_pins: bool = True  # pinned memories skipped unless False


@dataclass
class MemoryAutoProposeConfig:
    """Selective auto-propose memory candidate pipeline (#1454).

    Off by default. When enabled, after each final assistant turn, an
    LLM-driven extractor scans the response for durable facts and
    proposes them through the existing governed promotion pipeline as
    ``candidate`` memories — never silently active. Bounded by per-turn
    cap, the existing per-conversation rate limit on
    ``MemoryPromotionConfig``, and a cooldown that suppresses repeats
    of the same fact in the same conversation.
    """

    enabled: bool = False  # opt-in; default no extraction
    max_candidates_per_turn: int = 1  # hard cap on proposals per assistant turn
    categories: list[str] = field(default_factory=lambda: ["preference", "project_fact", "decision", "workflow_hint"])
    min_confidence: float = 0.8  # 0.0-1.0; LLM-reported confidence floor
    notify_inline: bool = True  # render inline notice in CLI/web after extraction
    cooldown_turns: int = 5  # suppress repeats of the same content within N turns


@dataclass
class MemoryConfig:
    """Memory subsystem settings. Promotion (#920), retention (#625),
    and auto-propose (#1454) live here; recall, storage, and lifecycle
    settings can grow in place without restructuring the config tree."""

    promotion: MemoryPromotionConfig = field(default_factory=MemoryPromotionConfig)
    retention: MemoryRetentionConfig = field(default_factory=MemoryRetentionConfig)
    auto_propose: MemoryAutoProposeConfig = field(default_factory=MemoryAutoProposeConfig)


@dataclass
class ComplianceRule:
    """A single declarative compliance rule evaluated against the final config."""

    field: str  # dot-path, e.g. "safety.approval_mode"
    message: str = ""  # human-readable violation message
    must_be: Any = _UNSET
    must_not_be: Any = _UNSET
    must_match: str = ""  # regex pattern
    must_not_be_empty: bool = False
    must_contain: Any = _UNSET
    _compiled_pattern: Any = _dc_field(default=None, repr=False, compare=False)


@dataclass
class PackSourceConfig:
    """A single git-based pack source repository."""

    url: str
    branch: str = "main"
    refresh_interval: int = 30  # minutes; 0 = manual only
    auto_attach: bool = True
    priority: int = 50  # 1-100, lower wins

    _MIN_REFRESH: int = field(default=5, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.refresh_interval != 0 and self.refresh_interval < self._MIN_REFRESH:
            logger.warning(
                "refresh_interval=%d is below minimum (%d), clamping",
                self.refresh_interval,
                self._MIN_REFRESH,
            )
            self.refresh_interval = self._MIN_REFRESH
        if not 1 <= self.priority <= 100:
            logger.warning("priority=%d is out of range (1-100), clamping to 50", self.priority)
            self.priority = 50


@dataclass
class TrustedProxyConfig:
    """CIDR-based trusted proxy configuration for client IP resolution.

    When ``enabled`` is ``True`` and the socket peer is within one of
    ``trusted_cidrs``, the resolver walks the forwarded-header chain
    right-to-left and returns the first IP not in the trusted set.
    """

    enabled: bool = False
    trusted_cidrs: list[str] = field(default_factory=list)
    header: str = "X-Forwarded-For"


@dataclass
class ComplianceConfig:
    """Declarative rules engine for configuration governance."""

    rules: list[ComplianceRule] = field(default_factory=list)


@dataclass
class TranscriptConfig:
    """Controls durable transcript recording for workflow steps (#1111)."""

    enabled: bool = True
    max_assistant_chars: int = 4000
    max_tool_output_chars: int = 2000
    max_stdout_chars: int = 4000
    max_stderr_chars: int = 4000


@dataclass
class WorkflowCredentialConfig:
    """A named credential reference for workflow steps (#970).

    Each credential is either an env var lookup or a shell command.
    Raw secret values are never stored in config — only references.
    """

    name: str
    env_var: str | None = None
    command: str | None = None
    allowed_runners: list[str] | None = None  # None = all; ["shell"] = restrict


@dataclass
class WorkflowBudgetConfig:
    """Per-run budget ceilings for workflow execution (#967).

    Zero means unlimited for that dimension.
    """

    max_duration_seconds: int = 0
    max_steps: int = 0
    max_tokens: int = 0


@dataclass
class WorkflowConfig:
    """Workflow automation and orchestration settings."""

    enabled: bool = True
    approval_mode: str = "ask_for_dangerous"
    max_review_rounds: int = 2
    max_iterations: int = 30
    step_timeout: int = 300
    heartbeat_interval: int = 30
    stale_threshold: int = 60
    approval_timeout: int = 300
    registry_enabled: bool = True
    registry_heartbeat_interval: int = 30
    budget: WorkflowBudgetConfig = field(default_factory=WorkflowBudgetConfig)
    credentials: list[WorkflowCredentialConfig] = field(default_factory=list)
    executor_enabled: bool = False
    executor_poll_interval: int = 5
    max_concurrent_runs: int = 3
    scheduler_enabled: bool = True
    min_schedule_interval: int = 60
    watch_buffer_lines: int = 50
    lock_reclaim_threshold: int = 120
    transcript: TranscriptConfig = field(default_factory=TranscriptConfig)

    _MIN_STEP_TIMEOUT: int = field(default=10, init=False, repr=False)
    _MAX_STEP_TIMEOUT: int = field(default=3600, init=False, repr=False)
    _MIN_MAX_ITERATIONS: int = field(default=1, init=False, repr=False)
    _MAX_MAX_ITERATIONS: int = field(default=100, init=False, repr=False)
    _MIN_HEARTBEAT: int = field(default=5, init=False, repr=False)
    _MIN_POLL_INTERVAL: int = field(default=1, init=False, repr=False)
    _MAX_POLL_INTERVAL: int = field(default=60, init=False, repr=False)
    _MIN_CONCURRENT_RUNS: int = field(default=1, init=False, repr=False)
    _MAX_CONCURRENT_RUNS: int = field(default=20, init=False, repr=False)
    _MIN_SCHED_INTERVAL: int = field(default=60, init=False, repr=False)
    _MAX_SCHED_INTERVAL: int = field(default=86400, init=False, repr=False)
    _MIN_WATCH_BUFFER_LINES: int = field(default=1, init=False, repr=False)
    _MAX_WATCH_BUFFER_LINES: int = field(default=1000, init=False, repr=False)
    _APPROVAL_MODES: tuple[str, ...] = field(
        default=("auto", "ask_for_dangerous", "ask_for_writes", "ask"),
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        if self.approval_mode not in self._APPROVAL_MODES:
            logger.warning(
                "workflow approval_mode=%r invalid, defaulting to %r",
                self.approval_mode,
                "ask_for_dangerous",
            )
            object.__setattr__(self, "approval_mode", "ask_for_dangerous")
        if self.max_iterations < self._MIN_MAX_ITERATIONS:
            logger.warning(
                "workflow max_iterations=%d below minimum (%d), clamping",
                self.max_iterations,
                self._MIN_MAX_ITERATIONS,
            )
            object.__setattr__(self, "max_iterations", self._MIN_MAX_ITERATIONS)
        if self.max_iterations > self._MAX_MAX_ITERATIONS:
            logger.warning(
                "workflow max_iterations=%d above maximum (%d), clamping",
                self.max_iterations,
                self._MAX_MAX_ITERATIONS,
            )
            object.__setattr__(self, "max_iterations", self._MAX_MAX_ITERATIONS)
        if self.step_timeout < self._MIN_STEP_TIMEOUT:
            logger.warning(
                "workflow step_timeout=%d below minimum (%d), clamping",
                self.step_timeout,
                self._MIN_STEP_TIMEOUT,
            )
            object.__setattr__(self, "step_timeout", self._MIN_STEP_TIMEOUT)
        if self.step_timeout > self._MAX_STEP_TIMEOUT:
            logger.warning(
                "workflow step_timeout=%d above maximum (%d), clamping",
                self.step_timeout,
                self._MAX_STEP_TIMEOUT,
            )
            object.__setattr__(self, "step_timeout", self._MAX_STEP_TIMEOUT)
        if self.heartbeat_interval < self._MIN_HEARTBEAT:
            object.__setattr__(self, "heartbeat_interval", self._MIN_HEARTBEAT)
        if self.max_review_rounds < 1:
            object.__setattr__(self, "max_review_rounds", 1)
        if self.executor_poll_interval < self._MIN_POLL_INTERVAL:
            object.__setattr__(self, "executor_poll_interval", self._MIN_POLL_INTERVAL)
        if self.executor_poll_interval > self._MAX_POLL_INTERVAL:
            object.__setattr__(self, "executor_poll_interval", self._MAX_POLL_INTERVAL)
        if self.max_concurrent_runs < self._MIN_CONCURRENT_RUNS:
            object.__setattr__(self, "max_concurrent_runs", self._MIN_CONCURRENT_RUNS)
        if self.max_concurrent_runs > self._MAX_CONCURRENT_RUNS:
            object.__setattr__(self, "max_concurrent_runs", self._MAX_CONCURRENT_RUNS)
        if self.min_schedule_interval < self._MIN_SCHED_INTERVAL:
            object.__setattr__(self, "min_schedule_interval", self._MIN_SCHED_INTERVAL)
        if self.min_schedule_interval > self._MAX_SCHED_INTERVAL:
            object.__setattr__(self, "min_schedule_interval", self._MAX_SCHED_INTERVAL)
        if self.watch_buffer_lines < self._MIN_WATCH_BUFFER_LINES:
            object.__setattr__(self, "watch_buffer_lines", self._MIN_WATCH_BUFFER_LINES)
        if self.watch_buffer_lines > self._MAX_WATCH_BUFFER_LINES:
            object.__setattr__(self, "watch_buffer_lines", self._MAX_WATCH_BUFFER_LINES)
        if self.lock_reclaim_threshold < 30:
            object.__setattr__(self, "lock_reclaim_threshold", 30)


@dataclass
class HookMatcherConfig:
    """Conditions that must all match for a hook to fire.

    ``tool_name`` is an fnmatch pattern (``"*"`` matches every tool).
    ``arguments`` is an optional dict of argument key/value pairs that
    must all be present in the tool's call arguments for the hook to fire.
    An empty dict matches any arguments.
    """

    tool_name: str = "*"
    arguments: dict[str, str] = field(default_factory=dict)


@dataclass
class HookRunnerConfig:
    """How to execute a hook.

    ``type`` is ``"command"`` (shell subprocess) or ``"webhook"`` (HTTP POST).
    ``timeout`` is clamped to [1, 30] seconds.

    For ``command`` runners: ``command`` is the shell string to run.  The
    runtime (#1271) passes tool context via environment variables and reads
    a JSON decision from stdout.

    For ``webhook`` runners: ``url`` is the HTTP endpoint.  The runtime
    POSTs a JSON body with tool context and reads a JSON decision from the
    response body.
    """

    type: str = "command"
    command: str = ""
    url: str = ""
    timeout: int = 5

    _MIN_TIMEOUT: int = field(default=1, init=False, repr=False)
    _MAX_TIMEOUT: int = field(default=30, init=False, repr=False)
    _VALID_TYPES: tuple[str, ...] = field(default=("command", "webhook"), init=False, repr=False)

    def __post_init__(self) -> None:
        if self.type not in self._VALID_TYPES:
            logger.warning("hook runner type=%r invalid, defaulting to 'command'", self.type)
            object.__setattr__(self, "type", "command")
        if self.timeout < self._MIN_TIMEOUT:
            logger.warning("hook timeout=%d below minimum (%d), clamping", self.timeout, self._MIN_TIMEOUT)
            object.__setattr__(self, "timeout", self._MIN_TIMEOUT)
        if self.timeout > self._MAX_TIMEOUT:
            logger.warning("hook timeout=%d above maximum (%d), clamping", self.timeout, self._MAX_TIMEOUT)
            object.__setattr__(self, "timeout", self._MAX_TIMEOUT)


@dataclass
class HookEntryConfig:
    """A single hook definition attached to a tool lifecycle event.

    ``id`` is a stable string used for deduplication across config layers.
    When the same ``id`` appears in multiple layers, the highest-priority
    layer wins (personal > team > defaults), so teams can provide default
    hooks that operators can override locally.

    ``event`` is ``"pre_tool"`` or ``"post_tool"``.

    ``trust_source`` records which config layer declared this hook.
    Phase-1 trusted sources: ``"personal"`` and ``"team"``.  Pack-sourced
    hooks will carry ``"pack"`` and require trust verification (#1272)
    before the runtime (#1271) may execute them.

    ``message`` is an optional human-readable string included in deny/ask
    decisions surfaced to the user.
    """

    id: str = ""
    event: str = "pre_tool"
    matcher: HookMatcherConfig = field(default_factory=HookMatcherConfig)
    runner: HookRunnerConfig = field(default_factory=HookRunnerConfig)
    message: str = ""
    trust_source: str = "personal"

    _VALID_EVENTS: tuple[str, ...] = field(default=("pre_tool", "post_tool"), init=False, repr=False)
    _TRUSTED_SOURCES: tuple[str, ...] = field(default=("personal", "team"), init=False, repr=False)

    def __post_init__(self) -> None:
        if self.event not in self._VALID_EVENTS:
            logger.warning("hook event=%r invalid, defaulting to 'pre_tool'", self.event)
            object.__setattr__(self, "event", "pre_tool")

    @property
    def is_executable(self) -> bool:
        """True when this hook may be dispatched by the runtime.

        Phase-1 rule: only hooks from trusted sources (personal config and
        team config) are executable.  Pack-sourced hooks are parsed and
        deduplicated but skipped at dispatch time until #1272 adds trust
        verification.
        """
        return self.trust_source in self._TRUSTED_SOURCES


@dataclass
class FeedbackReporterConfig:
    """A single named feedback reporter (command or webhook)."""

    name: str = "default"
    type: str = "command"  # "command" | "webhook"
    command: str = ""
    url: str = ""
    timeout: int = 10  # clamped [1, 30]
    enabled: bool = True

    def __post_init__(self) -> None:
        self.timeout = max(1, min(30, self.timeout))
        if self.type not in ("command", "webhook"):
            logger.warning("feedback reporter %r has unknown type %r — defaulting to 'command'", self.name, self.type)
            object.__setattr__(self, "type", "command")


@dataclass
class FeedbackConfig:
    """Feedback and bug reporting settings.

    When no reporters are configured, the bundle is written to a local
    JSON file and the path is printed.  Configure ``reporters`` to dispatch
    to external systems such as GitHub Issues, Jira, or Slack.

    ``include_history_default`` controls whether conversation history is
    included without an explicit opt-in.  Off by default (privacy-safe).
    """

    reporters: list[FeedbackReporterConfig] = field(default_factory=list)
    include_history_default: bool = False
    max_history_messages: int = 10  # clamped [1, 50]
    retry_attempts: int = 2  # total attempts, clamped [1, 5]
    retry_backoff_seconds: float = 1.0  # clamped [0.0, 30.0]
    max_bundle_bytes: int = 1_000_000  # clamped [10_000, 5_000_000]

    def __post_init__(self) -> None:
        self.max_history_messages = max(1, min(50, self.max_history_messages))
        self.retry_attempts = max(1, min(5, self.retry_attempts))
        self.retry_backoff_seconds = max(0.0, min(30.0, self.retry_backoff_seconds))
        self.max_bundle_bytes = max(10_000, min(5_000_000, self.max_bundle_bytes))


@dataclass
class HooksConfig:
    """Runtime hook definitions for PreToolUse and PostToolUse events.

    ``pre_tool`` and ``post_tool`` are the deduplicated, ordered lists of
    hook entries that the runtime (#1271) evaluates on every tool call.

    **Phase-1 trust boundary**: only hooks from ``personal`` and ``team``
    config sources are executable.  Pack-sourced hooks (#1272) are stored
    here with ``trust_source="pack"`` but skipped by the runtime.

    **Reload semantics**: hook config is **session-scoped**.  Changes to
    the config file are detected by ConfigWatcher and logged as a notice,
    but are NOT applied to a live session.  A session restart is required
    to pick up hook config changes.  This prevents hook config from being
    used as an attack surface for stealth runtime modification.
    """

    pre_tool: list[HookEntryConfig] = field(default_factory=list)
    post_tool: list[HookEntryConfig] = field(default_factory=list)


def _parse_hook_entries(
    raw_list: object,
    event: str,
    trust_source: str,
    seen_ids: dict[str, str],
    *,
    pack_ids: set[str] | None = None,
) -> list[HookEntryConfig]:
    """Parse a list of raw hook dicts into ``HookEntryConfig`` objects.

    Deduplicates by ``id``: the first entry seen for a given id wins.
    ``seen_ids`` is updated in place so callers can track ids across
    multiple lists (e.g. pre_tool from different config layers).

    Hooks with an empty or missing ``id`` are rejected with a warning.
    Hooks from lower-priority sources whose id is already registered are
    silently dropped (higher-priority source wins).

    ``pack_ids`` is an optional set of hook ids known to originate from
    pack config.  When an id in ``raw_list`` appears in ``pack_ids``, the
    entry is tagged with ``trust_source="pack"`` regardless of the caller's
    requested ``trust_source``.  This closes a trust-boundary hole where
    pack hooks could bubble into the merged personal config (when personal
    declares no hooks) and be silently promoted to executable.
    """
    if not isinstance(raw_list, list):
        return []
    entries: list[HookEntryConfig] = []
    for raw in raw_list:
        if not isinstance(raw, dict):
            continue
        hook_id = str(raw.get("id", "")).strip()
        if not hook_id:
            logger.warning("hook entry missing 'id' field — skipped")
            continue
        if hook_id in seen_ids:
            logger.debug(
                "hook id=%r from source=%r superseded by %r — skipped",
                hook_id,
                trust_source,
                seen_ids[hook_id],
            )
            continue

        # Trust-boundary guard: if this id is known to originate from a
        # pack layer, force trust_source="pack" even if the entry reached
        # us via the merged "personal" raw dict.  deep_merge bubbles pack
        # hook lists into the personal view when personal has no
        # corresponding list, which would otherwise promote untrusted
        # pack hooks to executable status.
        effective_source = "pack" if (pack_ids is not None and hook_id in pack_ids) else trust_source
        seen_ids[hook_id] = effective_source

        raw_matcher = raw.get("matcher", {})
        if not isinstance(raw_matcher, dict):
            raw_matcher = {}
        raw_arguments = raw_matcher.get("arguments", {})
        if not isinstance(raw_arguments, dict):
            raw_arguments = {}
        matcher = HookMatcherConfig(
            tool_name=str(raw_matcher.get("tool_name", "*")),
            arguments={str(k): str(v) for k, v in raw_arguments.items()},
        )

        raw_runner = raw.get("runner", {})
        if not isinstance(raw_runner, dict):
            raw_runner = {}
        runner = HookRunnerConfig(
            type=str(raw_runner.get("type", "command")),
            command=str(raw_runner.get("command", "")),
            url=str(raw_runner.get("url", "")),
            timeout=int(raw_runner.get("timeout", 5)) if _is_int_like(raw_runner.get("timeout")) else 5,
        )

        entries.append(
            HookEntryConfig(
                id=hook_id,
                event=event,
                matcher=matcher,
                runner=runner,
                message=str(raw.get("message", "")),
                trust_source=effective_source,
            )
        )
    return entries


def _is_int_like(v: object) -> bool:
    """True when v can be safely coerced to int."""
    if isinstance(v, int):
        return True
    if isinstance(v, str):
        try:
            int(v)
            return True
        except ValueError:
            return False
    return False


def _collect_hook_ids(hooks_raw: object, event_key: str) -> set[str]:
    """Collect the set of hook ids declared under ``hooks.<event_key>``.

    Non-dict / non-list inputs and entries with empty ids are skipped.
    Used to tag pack-originated ids so they retain ``trust_source="pack"``
    even after deep_merge bubbles a pack hook list into the personal view.
    """
    if not isinstance(hooks_raw, dict):
        return set()
    entries = hooks_raw.get(event_key, [])
    if not isinstance(entries, list):
        return set()
    ids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        hook_id = str(entry.get("id", "")).strip()
        if hook_id:
            ids.add(hook_id)
    return ids


def _build_hooks_config(
    raw: dict[str, object],
    *,
    pack_raw: dict[str, object] | None = None,
    personal_raw: dict[str, object] | None = None,
    team_raw: dict[str, object] | None = None,
) -> HooksConfig:
    """Parse and merge hook config from the resolved config layers.

    ``raw`` is the fully merged config dict used as a fallback when no
    isolated per-layer views are available.

    ``personal_raw`` is the personal config snapshot taken *before*
    ``deep_merge`` introduces pack or team content.  Hooks parsed from
    this layer carry ``trust_source="personal"``.

    ``team_raw`` is the team config dict (trusted layer).  Hooks parsed
    from this layer carry ``trust_source="team"``.  Personal hooks are
    parsed first so ``seen_ids`` dedup lets personal win on id collision
    while unique-id team hooks survive.

    ``pack_raw`` is the pack config dict (untrusted in phase 1).  Entries
    are parsed and stored but marked non-executable (``trust_source="pack"``).

    Layer priority (highest first): personal > team > pack.

    When neither ``personal_raw`` nor ``team_raw`` is provided, hooks are
    parsed from ``raw`` with a pack-id guard that re-tags any id that
    originated in the pack layer so it retains ``trust_source="pack"``.
    """
    pack_hooks_raw: dict[str, object] | None = None
    pack_pre_ids: set[str] = set()
    pack_post_ids: set[str] = set()
    if pack_raw:
        candidate = pack_raw.get("hooks", {})
        if isinstance(candidate, dict):
            pack_hooks_raw = candidate
            pack_pre_ids = _collect_hook_ids(pack_hooks_raw, "pre_tool")
            pack_post_ids = _collect_hook_ids(pack_hooks_raw, "post_tool")

    seen_pre: dict[str, str] = {}
    seen_post: dict[str, str] = {}
    pre_entries: list[HookEntryConfig] = []
    post_entries: list[HookEntryConfig] = []

    if personal_raw is not None or team_raw is not None:
        # Fast path: per-layer views provided; label each correctly.
        # Personal hooks first so seen_ids dedup lets personal win on
        # id collision while unique-id team hooks pass through.
        if personal_raw is not None:
            p_hooks = personal_raw.get("hooks", {})
            if isinstance(p_hooks, dict):
                pre_entries += _parse_hook_entries(p_hooks.get("pre_tool", []), "pre_tool", "personal", seen_pre)
                post_entries += _parse_hook_entries(p_hooks.get("post_tool", []), "post_tool", "personal", seen_post)
        if team_raw is not None:
            t_hooks = team_raw.get("hooks", {})
            if isinstance(t_hooks, dict):
                pre_entries += _parse_hook_entries(t_hooks.get("pre_tool", []), "pre_tool", "team", seen_pre)
                post_entries += _parse_hook_entries(t_hooks.get("post_tool", []), "post_tool", "team", seen_post)
    else:
        # Fallback: no isolated views; parse from fully-merged ``raw``
        # and re-tag any pack-bubbled id so it retains trust_source="pack".
        hooks_raw = raw.get("hooks", {})
        if not isinstance(hooks_raw, dict):
            hooks_raw = {}
        pre_entries = _parse_hook_entries(
            hooks_raw.get("pre_tool", []),
            "pre_tool",
            "personal",
            seen_pre,
            pack_ids=pack_pre_ids,
        )
        post_entries = _parse_hook_entries(
            hooks_raw.get("post_tool", []),
            "post_tool",
            "personal",
            seen_post,
            pack_ids=pack_post_ids,
        )

    # Phase 1: parse pack-provided hooks but mark them non-executable.
    if pack_hooks_raw is not None:
        pre_entries += _parse_hook_entries(pack_hooks_raw.get("pre_tool", []), "pre_tool", "pack", seen_pre)
        post_entries += _parse_hook_entries(pack_hooks_raw.get("post_tool", []), "post_tool", "pack", seen_post)
        if pack_hooks_raw.get("pre_tool") or pack_hooks_raw.get("post_tool"):
            logger.info(
                "pack-provided hooks detected; they are NOT executable in phase 1 "
                "(trust_source='pack'). See issue #1272 for trust verification."
            )

    return HooksConfig(pre_tool=pre_entries, post_tool=post_entries)


@dataclass
class AppConfig:
    ai: AIConfig
    app: AppSettings = field(default_factory=AppSettings)
    project: ProjectConfig = field(default_factory=ProjectConfig)
    mcp_servers: list[McpServerConfig] = field(default_factory=list)
    mcp_tool_warning_threshold: int = 40  # warn when total MCP tools exceed this; 0 = disabled
    shared_databases: list[SharedDatabaseConfig] = field(default_factory=list)
    cli: CliConfig = field(default_factory=CliConfig)
    compaction: CompactionConfig = field(default_factory=CompactionConfig)
    identity: UserIdentity | None = None
    references: ReferencesConfig = field(default_factory=ReferencesConfig)
    embeddings: EmbeddingsConfig = field(default_factory=EmbeddingsConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    proxy: ProxyConfig = field(default_factory=ProxyConfig)
    rag: RagConfig = field(default_factory=RagConfig)
    reranker: RerankerConfig = field(default_factory=RerankerConfig)
    memory_recall: MemoryRecallConfig = field(default_factory=MemoryRecallConfig)
    codebase_index: CodebaseIndexConfig = field(default_factory=CodebaseIndexConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    session: SessionConfig = field(default_factory=SessionConfig)
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    audit: AuditConfig = field(default_factory=AuditConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    compliance: ComplianceConfig = field(default_factory=ComplianceConfig)
    trusted_proxy: TrustedProxyConfig = field(default_factory=TrustedProxyConfig)
    workflow: WorkflowConfig = field(default_factory=WorkflowConfig)
    pack_sources: list[PackSourceConfig] = field(default_factory=list)
    hooks: HooksConfig = field(default_factory=HooksConfig)
    feedback: FeedbackConfig = field(default_factory=FeedbackConfig)


def _resolve_data_dir() -> Path:
    """Resolve data directory: prefer ~/.anteroom, fall back to ~/.parlor for backward compat."""
    anteroom_dir = Path.home() / ".anteroom"
    parlor_dir = Path.home() / ".parlor"
    if anteroom_dir.exists():
        return anteroom_dir
    if parlor_dir.exists():
        return parlor_dir
    return anteroom_dir


def _get_config_path(data_dir: Path | None = None) -> Path:
    if data_dir:
        return data_dir / "config.yaml"
    return _resolve_data_dir() / "config.yaml"


def _resolve_reference_paths(raw: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    """Resolve relative paths in ``references`` to absolute before merge.

    Called on each config layer (personal, team, project) before
    ``deep_merge`` so that path provenance is preserved — after merge you
    can no longer tell which layer contributed which paths.
    """
    refs = raw.get("references")
    if not refs or not isinstance(refs, dict):
        return raw
    changed = False
    for key in ("instructions", "rules", "skills"):
        paths = refs.get(key)
        if not paths or not isinstance(paths, list):
            continue
        resolved: list[str] = []
        for p in paths:
            if not isinstance(p, str) or not p:
                continue
            path_obj = Path(p)
            if not path_obj.is_absolute():
                path_obj = (base_dir / path_obj).resolve()
            resolved.append(str(path_obj))
        if resolved != paths:
            changed = True
        refs[key] = resolved
    if changed:
        raw = {**raw, "references": refs}
    return raw


def load_config(
    config_path: Path | None = None,
    *,
    team_config_path: Path | None = None,
    project_config_path: Path | None = None,
    pack_config: dict[str, Any] | None = None,
    space_config: dict[str, Any] | None = None,
    working_dir: str | None = None,
    interactive: bool = False,
) -> tuple[AppConfig, list[str]]:
    """Load configuration with optional team, pack, space, and project config layers.

    Returns ``(AppConfig, enforced_fields)`` where *enforced_fields* is
    the list of dot-paths from the team config's ``enforce`` section.

    Layer precedence (highest wins)::

      env vars > project config > space config > personal config > pack config > team config > defaults

    Enforced team fields override everything — they are re-applied after
    each merge step via :func:`~anteroom.services.team_config.apply_enforcement`.

    Parameters
    ----------
    config_path:
        Path to the personal YAML config file.  If ``None``, auto-detected
        via ``_get_config_path()``.
    team_config_path:
        Explicit path to a team config file (overrides discovery).
    project_config_path:
        Explicit path to a project config file (overrides discovery).
    pack_config:
        Pre-merged pack overlay dict (output of
        :func:`~anteroom.services.config_overlays.merge_pack_overlays`).
        Applied between team and personal layers.  ``None`` or empty dict
        is a no-op.  The caller is responsible for collecting and merging
        pack overlays from the DB before calling this function.
    space_config:
        Space-scoped config dict.  Applied after personal layer.
    working_dir:
        Working directory for project config auto-discovery.
    interactive:
        If ``True``, prompt on untrusted team/project configs.

    Merge strategy
    --------------
    ``raw`` starts as the personal config (from the YAML file).  Layers
    are applied using :func:`~anteroom.services.team_config.deep_merge`
    which creates new dicts at each level — no input is mutated.

    Pack overlays are merged *before* the team layer so that the merge
    chain is: ``deep_merge(pack, personal)`` → ``deep_merge(team, result)``.
    This means team < pack < personal, which is correct.  Critically,
    pack overlay application is *unconditional* — it does not depend on
    whether a team config exists or is non-empty.  This prevents a subtle
    bug where pack overlays would be silently dropped when
    ``team_config_path`` is set but the file is empty or malformed.
    """
    raw: dict[str, Any] = {}
    path = config_path or _get_config_path()

    if path.exists():
        # Capture any external edits made while Anteroom was not running
        import contextlib

        with contextlib.suppress(Exception):
            from .services.config_history import ConfigHistoryService, get_backup_dir

            ConfigHistoryService(get_backup_dir(path.parent)).detect_and_snapshot_external_edit(path)

        with open(path, encoding="utf-8-sig") as f:
            raw = yaml.safe_load(f) or {}

    # Resolve reference paths relative to the personal config file
    raw = _resolve_reference_paths(raw, path.parent)

    # Snapshot the personal-only raw dict before any team/pack/space/project
    # layers are merged in.  Used by ``_build_hooks_config`` so that the
    # phase-1 trust boundary (personal hooks are executable, pack hooks are
    # not) does not depend on which layers happened to supply a ``hooks``
    # key.  Wholesale list replacement during deep_merge would otherwise
    # let a pack's ``pre_tool`` list bubble into the merged ``raw["hooks"]``
    # when personal declares none, silently promoting untrusted entries.
    personal_raw_snapshot: dict[str, Any] = copy.deepcopy(raw)

    # Validate raw config before parsing into dataclasses
    from .services.config_validator import validate_config

    validation = validate_config(raw)
    if not validation.is_valid:
        raise ValueError(f"Invalid configuration in {path}:\n{validation.format_errors()}")
    if validation.has_warnings:
        for w in validation.errors:
            if w.severity == "warning":
                logger.warning("Config %s: %s — %s", path, w.path, w.message)

    # --- Team config layer ---------------------------------------------------
    team_raw: dict[str, Any] = {}
    enforced_fields: list[str] = []

    from .services.team_config import apply_enforcement, deep_merge, discover_team_config, load_team_config

    team_path = discover_team_config(
        cli_path=team_config_path,
        env_path=os.environ.get("AI_CHAT_TEAM_CONFIG"),
        personal_path=raw.get("team_config_path"),
    )
    # --- Pack config layer ---------------------------------------------------
    # Pack overlays sit between team and personal in precedence:
    #   defaults < team < **packs** < personal < space < project < env vars
    #
    # We apply pack overlays here (before team merge) so that:
    #   1. deep_merge(pack, personal) makes personal win over packs  ✓
    #   2. deep_merge(team, result) makes team the base under both   ✓
    #   3. apply_enforcement() re-applies team locks after all merges ✓
    #
    # This is deliberately outside the `if team_path:` block — pack overlays
    # must apply regardless of whether team config exists.  An earlier design
    # nested this inside the team conditional, which silently dropped pack
    # overlays when team_config_path was set but the file was empty.
    if pack_config and isinstance(pack_config, dict):
        raw = deep_merge(pack_config, raw)

    if team_path:
        data_dir = path.parent if path.exists() else None
        team_raw, enforced_fields = load_team_config(team_path, data_dir, interactive=interactive)
        if team_raw:
            team_raw = _resolve_reference_paths(team_raw, Path(team_path).parent)
            raw = deep_merge(team_raw, raw)
            # Re-apply enforced fields so neither packs nor personal can override them
            raw = apply_enforcement(raw, team_raw, enforced_fields)

    # --- Space config layer --------------------------------------------------
    if space_config and isinstance(space_config, dict):
        raw = deep_merge(raw, space_config)
        if enforced_fields and team_raw:
            raw = apply_enforcement(raw, team_raw, enforced_fields)

    # --- Project config layer ------------------------------------------------
    from .services.project_config import discover_project_config, load_project_config

    # Only auto-discover project config when working_dir is explicitly set
    # (prevents accidentally loading configs from the test runner's cwd)
    proj_path = project_config_path
    if not proj_path and working_dir:
        proj_path = discover_project_config(working_dir)
    if proj_path:
        data_dir_for_trust = path.parent if path.exists() else None
        proj_raw, _required_keys = load_project_config(proj_path, data_dir_for_trust, interactive=interactive)
        if proj_raw:
            proj_raw = _resolve_reference_paths(proj_raw, Path(proj_path).parent)
            raw = deep_merge(raw, proj_raw)
            # Re-apply enforced fields so project config can't override them
            if enforced_fields and team_raw:
                raw = apply_enforcement(raw, team_raw, enforced_fields)

    ai_raw = raw.get("ai", {})
    base_url = ai_raw.get("base_url") or os.environ.get("AI_CHAT_BASE_URL", "")
    api_key = ai_raw.get("api_key") or os.environ.get("AI_CHAT_API_KEY", "")
    api_key_command = ai_raw.get("api_key_command") or os.environ.get("AI_CHAT_API_KEY_COMMAND", "")
    model = ai_raw.get("model") or os.environ.get("AI_CHAT_MODEL", "gpt-4")
    user_system_prompt = ai_raw.get("system_prompt") or os.environ.get("AI_CHAT_SYSTEM_PROMPT", "")
    if user_system_prompt:
        system_prompt = (
            _DEFAULT_SYSTEM_PROMPT + "\n\n<user_instructions>\n" + user_system_prompt + "\n</user_instructions>"
        )
    else:
        system_prompt = _DEFAULT_SYSTEM_PROMPT
        user_system_prompt = ""

    if not base_url:
        raise ValueError(
            "AI base_url is required. Set 'ai.base_url' in config.yaml "
            f"({path}) or AI_CHAT_BASE_URL environment variable."
        )
    if not api_key and not api_key_command:
        raise ValueError(
            f"AI api_key or api_key_command is required. Set 'ai.api_key' or 'ai.api_key_command' "
            f"in config.yaml ({path}) or AI_CHAT_API_KEY / AI_CHAT_API_KEY_COMMAND environment variable."
        )

    verify_ssl_raw = ai_raw.get("verify_ssl", os.environ.get("AI_CHAT_VERIFY_SSL", "true"))
    verify_ssl = str(verify_ssl_raw).lower() not in ("false", "0", "no")
    try:
        _raw_timeout = ai_raw.get("request_timeout", os.environ.get("AI_CHAT_REQUEST_TIMEOUT", 120))
        request_timeout = max(10, min(600, int(_raw_timeout)))
    except (ValueError, TypeError):
        request_timeout = 120

    try:
        _raw_connect = ai_raw.get("connect_timeout", os.environ.get("AI_CHAT_CONNECT_TIMEOUT", 5))
        connect_timeout = max(1, min(30, int(_raw_connect)))
    except (ValueError, TypeError):
        connect_timeout = 5

    try:
        _raw_write = ai_raw.get("write_timeout", os.environ.get("AI_CHAT_WRITE_TIMEOUT", 30))
        write_timeout = max(5, min(120, int(_raw_write)))
    except (ValueError, TypeError):
        write_timeout = 30

    try:
        _raw_pool = ai_raw.get("pool_timeout", os.environ.get("AI_CHAT_POOL_TIMEOUT", 10))
        pool_timeout = max(1, min(60, int(_raw_pool)))
    except (ValueError, TypeError):
        pool_timeout = 10

    try:
        _raw_first_token = ai_raw.get("first_token_timeout", os.environ.get("AI_CHAT_FIRST_TOKEN_TIMEOUT", 30))
        first_token_timeout = max(5, min(120, int(_raw_first_token)))
    except (ValueError, TypeError):
        first_token_timeout = 30

    try:
        _raw_chunk_stall = ai_raw.get("chunk_stall_timeout", os.environ.get("AI_CHAT_CHUNK_STALL_TIMEOUT", 30))
        chunk_stall_timeout = max(10, min(600, int(_raw_chunk_stall)))
    except (ValueError, TypeError):
        chunk_stall_timeout = 30

    try:
        _raw_retry_attempts = ai_raw.get("retry_max_attempts", os.environ.get("AI_CHAT_RETRY_MAX_ATTEMPTS", 3))
        retry_max_attempts = max(0, min(10, int(_raw_retry_attempts)))
    except (ValueError, TypeError):
        retry_max_attempts = 3

    try:
        _raw_retry_backoff = ai_raw.get("retry_backoff_base", os.environ.get("AI_CHAT_RETRY_BACKOFF_BASE", 1.0))
        retry_backoff_base = max(0.1, min(30.0, float(_raw_retry_backoff)))
    except (ValueError, TypeError):
        retry_backoff_base = 1.0

    try:
        narration_cadence = int(ai_raw.get("narration_cadence", os.environ.get("AI_CHAT_NARRATION_CADENCE", 8)))
        narration_cadence = max(0, narration_cadence)
    except (ValueError, TypeError):
        narration_cadence = 8

    try:
        max_tools = int(ai_raw.get("max_tools", os.environ.get("AI_CHAT_MAX_TOOLS", 128)))
        max_tools = max(0, max_tools)
    except (ValueError, TypeError):
        max_tools = 128

    _raw_temperature = ai_raw.get("temperature", os.environ.get("AI_CHAT_TEMPERATURE"))
    temperature: float | None = None
    if _raw_temperature is not None and str(_raw_temperature).strip() != "":
        try:
            temperature = max(0.0, min(2.0, float(_raw_temperature)))
        except (ValueError, TypeError):
            temperature = None

    _raw_top_p = ai_raw.get("top_p", os.environ.get("AI_CHAT_TOP_P"))
    top_p: float | None = None
    if _raw_top_p is not None and str(_raw_top_p).strip() != "":
        try:
            top_p = max(0.0, min(1.0, float(_raw_top_p)))
        except (ValueError, TypeError):
            top_p = None

    _raw_seed = ai_raw.get("seed", os.environ.get("AI_CHAT_SEED"))
    seed: int | None = None
    if _raw_seed is not None and str(_raw_seed).strip() != "":
        try:
            seed = int(_raw_seed)
        except (ValueError, TypeError):
            seed = None

    provider = str(ai_raw.get("provider", os.environ.get("AI_CHAT_PROVIDER", "openai")))
    if provider not in ("openai", "anthropic", "litellm"):
        provider = "openai"

    try:
        max_output_tokens = int(
            ai_raw.get("max_output_tokens", os.environ.get("AI_CHAT_MAX_OUTPUT_TOKENS", DEFAULT_MAX_OUTPUT_TOKENS))
        )
    except (ValueError, TypeError):
        max_output_tokens = DEFAULT_MAX_OUTPUT_TOKENS

    _raw_bedrock_confirmed = ai_raw.get(
        "litellm_bedrock_tools_confirmed",
        os.environ.get("AI_CHAT_LITELLM_BEDROCK_TOOLS_CONFIRMED", "false"),
    )
    litellm_bedrock_tools_confirmed = str(_raw_bedrock_confirmed).lower() not in ("false", "0", "no")

    _raw_allowed_domains = ai_raw.get("allowed_domains", [])
    if not isinstance(_raw_allowed_domains, list):
        _raw_allowed_domains = []
    allowed_domains: list[str] = [str(d).strip() for d in _raw_allowed_domains if d]
    _env_allowed_domains = os.environ.get("AI_CHAT_ALLOWED_DOMAINS", "")
    if _env_allowed_domains:
        allowed_domains = [d.strip() for d in _env_allowed_domains.split(",") if d.strip()]

    _raw_allowed_models = ai_raw.get("allowed_models", [])
    if not isinstance(_raw_allowed_models, list):
        _raw_allowed_models = []
    allowed_models: list[str] = [str(m).strip() for m in _raw_allowed_models if m]
    _env_allowed_models = os.environ.get("AI_CHAT_ALLOWED_MODELS", "")
    if _env_allowed_models:
        allowed_models = [m.strip() for m in _env_allowed_models.split(",") if m.strip()]

    _raw_block_localhost = ai_raw.get("block_localhost_api", os.environ.get("AI_CHAT_BLOCK_LOCALHOST_API", "false"))
    block_localhost_api = str(_raw_block_localhost).lower() not in ("false", "0", "no")

    _raw_family_aliases = ai_raw.get("model_family_aliases", {})
    if not isinstance(_raw_family_aliases, dict):
        _raw_family_aliases = {}
    model_family_aliases: dict[str, str] = {str(k).strip(): str(v).strip() for k, v in _raw_family_aliases.items() if k}
    _env_family_aliases = os.environ.get("AI_CHAT_MODEL_FAMILY_ALIASES", "")
    if _env_family_aliases:
        try:
            _parsed = json.loads(_env_family_aliases)
            if isinstance(_parsed, dict):
                model_family_aliases = {str(k).strip(): str(v).strip() for k, v in _parsed.items() if k}
        except (json.JSONDecodeError, TypeError, ValueError):
            pass  # graceful degradation — ignore malformed env var

    if narration_cadence > 0:
        system_prompt += (
            "\n\n<narration>\n"
            f"During multi-step tasks with tool calls, give a short progress update every "
            f"{narration_cadence} tool calls only when it adds user-visible value. "
            "Use one sentence when possible, focus on what changed and the next concrete step, "
            "and avoid repeating prior status.\n"
            "</narration>"
        )

    ai = AIConfig(
        base_url=base_url,
        api_key=api_key,
        api_key_command=api_key_command,
        model=model,
        system_prompt=system_prompt,
        user_system_prompt=user_system_prompt,
        verify_ssl=verify_ssl,
        request_timeout=request_timeout,
        connect_timeout=connect_timeout,
        write_timeout=write_timeout,
        pool_timeout=pool_timeout,
        first_token_timeout=first_token_timeout,
        chunk_stall_timeout=chunk_stall_timeout,
        retry_max_attempts=retry_max_attempts,
        retry_backoff_base=retry_backoff_base,
        narration_cadence=narration_cadence,
        max_tools=max_tools,
        temperature=temperature,
        top_p=top_p,
        seed=seed,
        allowed_domains=allowed_domains,
        allowed_models=allowed_models,
        block_localhost_api=block_localhost_api,
        provider=provider,
        max_output_tokens=max_output_tokens,
        litellm_bedrock_tools_confirmed=litellm_bedrock_tools_confirmed,
        model_family_aliases=model_family_aliases,
    )

    app_raw = raw.get("app", {})
    default_data_dir = str(_resolve_data_dir())
    data_dir = Path(os.path.expanduser(app_raw.get("data_dir", default_data_dir)))
    tls_raw = app_raw.get("tls", False)
    tls_enabled = str(tls_raw).lower() not in ("false", "0", "no")

    port_raw = app_raw.get("port") if "port" in app_raw else os.environ.get("AI_CHAT_PORT", 8080)
    try:
        port_val = int(port_raw)
    except (ValueError, TypeError):
        port_val = 8080
    port_val = max(1, min(65535, port_val))
    app_settings = AppSettings(
        host=app_raw.get("host", "127.0.0.1"),
        port=port_val,
        data_dir=data_dir,
        tls=tls_enabled,
    )

    mcp_servers: list[McpServerConfig] = []
    for srv in raw.get("mcp_servers", []):
        # Skip servers explicitly disabled by personal config (enabled: false).
        # This lets users opt out of team-defined servers without removing them.
        if not srv.get("enabled", True):
            logger.info("MCP server '%s' is disabled (enabled: false), skipping", srv.get("name", "?"))
            continue
        env_raw = srv.get("env", {})
        env: dict[str, str] = {}
        for k, v in env_raw.items():
            env[k] = os.path.expandvars(str(v))
        tools_include_raw = srv.get("tools_include", [])
        tools_include = [str(t) for t in tools_include_raw] if isinstance(tools_include_raw, list) else []
        tools_exclude_raw = srv.get("tools_exclude", [])
        tools_exclude = [str(t) for t in tools_exclude_raw] if isinstance(tools_exclude_raw, list) else []
        if tools_include and tools_exclude:
            logger.warning(
                "MCP server '%s': both tools_include and tools_exclude set; using include (ignoring exclude)",
                srv.get("name", "?"),
            )
            tools_exclude = []
        mcp_servers.append(
            McpServerConfig(
                name=srv["name"],
                transport=srv.get("transport", "stdio"),
                command=srv.get("command"),
                args=srv.get("args", []),
                url=srv.get("url"),
                env=env,
                timeout=float(srv.get("timeout", 30.0)),
                tools_include=tools_include,
                tools_exclude=tools_exclude,
                trust_level=srv.get("trust_level", "untrusted"),
            )
        )

    try:
        mcp_tool_warning_threshold = max(0, int(raw.get("mcp_tool_warning_threshold", 40)))
    except (ValueError, TypeError):
        mcp_tool_warning_threshold = 40

    shared_databases: list[SharedDatabaseConfig] = []
    for sdb in raw.get("shared_databases", []):
        if not sdb.get("enabled", True):
            logger.info("Shared database '%s' is disabled (enabled: false), skipping", sdb.get("name", "?"))
            continue
        shared_databases.append(
            SharedDatabaseConfig(
                name=sdb["name"],
                path=os.path.expanduser(sdb["path"]),
                passphrase_hash=sdb.get("passphrase_hash", ""),
            )
        )

    # Also support the "databases" key (newer config format)
    for db_name, db_conf in raw.get("databases", {}).items():
        if db_name == "personal":
            continue
        if isinstance(db_conf, dict):
            shared_databases.append(
                SharedDatabaseConfig(
                    name=db_name,
                    path=os.path.expanduser(db_conf.get("path", "")),
                    passphrase_hash=db_conf.get("passphrase_hash", ""),
                )
            )

    app_settings.data_dir.mkdir(parents=True, exist_ok=True)
    try:
        app_settings.data_dir.chmod(stat.S_IRWXU)  # 0700
        if path.exists():
            path.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 0600
    except OSError:
        pass  # May fail on Windows or non-owned files

    cli_raw = raw.get("cli", {})

    def _cli_raw_or_env(key: str, env_key: str) -> tuple[Any, bool]:
        if key in cli_raw:
            return cli_raw[key], True
        env_val = os.environ.get(env_key)
        if env_val is not None:
            return env_val, True
        return None, False

    def _compaction_raw_or_env(key: str, env_key: str) -> tuple[Any, bool]:
        compaction_section = raw.get("compaction", {})
        if isinstance(compaction_section, dict) and key in compaction_section:
            return compaction_section[key], True
        env_val = os.environ.get(env_key)
        if env_val is not None:
            return env_val, True
        return None, False

    def _parse_optional_int(value: Any, present: bool) -> int | None:
        if not present:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def _parse_int_setting(value: Any, *, default: int, lo: int, hi: int) -> int:
        try:
            return max(lo, min(hi, int(value)))
        except (ValueError, TypeError):
            return default

    _raw_model_context_window, _model_context_window_present = _cli_raw_or_env(
        "model_context_window", "AI_CHAT_MODEL_CONTEXT_WINDOW"
    )
    model_context_window = _parse_int_setting(
        _raw_model_context_window if _model_context_window_present else DEFAULT_MODEL_CONTEXT_WINDOW,
        default=DEFAULT_MODEL_CONTEXT_WINDOW,
        lo=1000,
        hi=2_000_000,
    )

    _raw_reserved_output, _reserved_output_present = _cli_raw_or_env(
        "context_reserved_output_tokens", "AI_CHAT_CONTEXT_RESERVED_OUTPUT_TOKENS"
    )
    context_reserved_output_tokens = _parse_int_setting(
        _raw_reserved_output if _reserved_output_present else max_output_tokens,
        default=max_output_tokens,
        lo=0,
        hi=2_000_000,
    )

    _raw_warn_buffer, _warn_buffer_present = _cli_raw_or_env(
        "context_warn_buffer_tokens", "AI_CHAT_CONTEXT_WARN_BUFFER_TOKENS"
    )
    context_warn_buffer_tokens = _parse_int_setting(
        _raw_warn_buffer if _warn_buffer_present else DEFAULT_CONTEXT_WARN_BUFFER_TOKENS,
        default=DEFAULT_CONTEXT_WARN_BUFFER_TOKENS,
        lo=0,
        hi=2_000_000,
    )

    _raw_auto_buffer, _auto_buffer_present = _cli_raw_or_env(
        "context_auto_compact_buffer_tokens", "AI_CHAT_CONTEXT_AUTO_COMPACT_BUFFER_TOKENS"
    )
    context_auto_compact_buffer_tokens = _parse_int_setting(
        _raw_auto_buffer if _auto_buffer_present else DEFAULT_CONTEXT_AUTO_COMPACT_BUFFER_TOKENS,
        default=DEFAULT_CONTEXT_AUTO_COMPACT_BUFFER_TOKENS,
        lo=0,
        hi=2_000_000,
    )

    _raw_context_warn, _context_warn_present = _cli_raw_or_env("context_warn_tokens", "AI_CHAT_CONTEXT_WARN_TOKENS")
    explicit_context_warn_tokens = _parse_optional_int(_raw_context_warn, _context_warn_present)

    _raw_context_auto, _context_auto_present = _cli_raw_or_env(
        "context_auto_compact_tokens", "AI_CHAT_CONTEXT_AUTO_COMPACT_TOKENS"
    )
    explicit_context_auto_compact_tokens = _parse_optional_int(_raw_context_auto, _context_auto_present)

    _raw_summary_buffer, _summary_buffer_present = _compaction_raw_or_env(
        "summary_trigger_buffer_tokens", "AI_CHAT_SUMMARY_TRIGGER_BUFFER_TOKENS"
    )
    summary_trigger_buffer_tokens = _parse_int_setting(
        _raw_summary_buffer if _summary_buffer_present else DEFAULT_SUMMARY_TRIGGER_BUFFER_TOKENS,
        default=DEFAULT_SUMMARY_TRIGGER_BUFFER_TOKENS,
        lo=0,
        hi=2_000_000,
    )

    _raw_summary_trigger, _summary_trigger_present = _compaction_raw_or_env(
        "summary_trigger_token_count", "AI_CHAT_SUMMARY_TRIGGER_TOKEN_COUNT"
    )
    explicit_summary_trigger_token_count = _parse_optional_int(_raw_summary_trigger, _summary_trigger_present)

    context_thresholds = derive_context_thresholds(
        ContextThresholdConfig(
            model_context_window=model_context_window,
            reserved_output_tokens=context_reserved_output_tokens,
            warn_buffer_tokens=context_warn_buffer_tokens,
            auto_compact_buffer_tokens=context_auto_compact_buffer_tokens,
            summary_trigger_buffer_tokens=summary_trigger_buffer_tokens,
            explicit_warn_tokens=explicit_context_warn_tokens,
            explicit_auto_compact_tokens=explicit_context_auto_compact_tokens,
            explicit_summary_trigger_token_count=explicit_summary_trigger_token_count,
        )
    )
    context_warn_tokens = context_thresholds.context_warn_tokens
    context_auto_compact_tokens = context_thresholds.context_auto_compact_tokens
    summary_trigger_token_count = context_thresholds.summary_trigger_token_count

    tool_dedup_env = os.environ.get("AI_CHAT_TOOL_DEDUP")
    tool_dedup_raw = tool_dedup_env if tool_dedup_env is not None else cli_raw.get("tool_dedup", True)
    tool_dedup = str(tool_dedup_raw).lower() not in ("false", "0", "no", "off")

    try:
        retry_delay = max(1.0, min(60.0, float(cli_raw.get("retry_delay", 5.0))))
    except (ValueError, TypeError):
        retry_delay = 5.0
    try:
        max_retries = max(0, min(10, int(cli_raw.get("max_retries", 3))))
    except (ValueError, TypeError):
        max_retries = 3
    try:
        esc_hint_delay = max(0.0, float(cli_raw.get("esc_hint_delay", 8.0)))
    except (ValueError, TypeError):
        esc_hint_delay = 8.0
    try:
        stall_display_threshold = max(1.0, float(cli_raw.get("stall_display_threshold", 5.0)))
    except (ValueError, TypeError):
        stall_display_threshold = 5.0
    try:
        stall_warning_threshold = max(1.0, float(cli_raw.get("stall_warning_threshold", 15.0)))
    except (ValueError, TypeError):
        stall_warning_threshold = 15.0
    try:
        stall_throughput_threshold = max(0.0, float(cli_raw.get("stall_throughput_threshold", 30.0)))
    except (ValueError, TypeError):
        stall_throughput_threshold = 30.0
    try:
        tool_output_max_chars = max(100, int(cli_raw.get("tool_output_max_chars", 10_000)))
    except (ValueError, TypeError):
        tool_output_max_chars = 10_000
    try:
        tool_replay_max_chars = max(
            100,
            int(
                cli_raw.get(
                    "tool_replay_max_chars",
                    os.environ.get("AI_CHAT_TOOL_REPLAY_MAX_CHARS", 10_000),
                )
            ),
        )
    except (ValueError, TypeError):
        tool_replay_max_chars = 10_000
    try:
        file_reference_max_chars = max(1000, min(10_000_000, int(cli_raw.get("file_reference_max_chars", 100_000))))
    except (ValueError, TypeError):
        file_reference_max_chars = 100_000
    # Execution surface routing thresholds (#1317)
    try:
        background_suggest_seconds = max(
            0,
            int(
                cli_raw.get(
                    "background_suggest_seconds",
                    os.environ.get("AI_CHAT_BACKGROUND_SUGGEST_SECONDS", 30),
                )
            ),
        )
    except (ValueError, TypeError):
        background_suggest_seconds = 30
    try:
        detach_suggest_seconds = max(
            0,
            int(
                cli_raw.get(
                    "detach_suggest_seconds",
                    os.environ.get("AI_CHAT_DETACH_SUGGEST_SECONDS", 120),
                )
            ),
        )
    except (ValueError, TypeError):
        detach_suggest_seconds = 120

    _raw_update_check = cli_raw.get("update_check", os.environ.get("AI_CHAT_UPDATE_CHECK", "true"))
    update_check = str(_raw_update_check).lower() not in ("false", "0", "no")
    update_check_command = str(cli_raw.get("update_check_command", os.environ.get("AI_CHAT_UPDATE_CHECK_COMMAND", "")))
    update_check_message = str(
        cli_raw.get(
            "update_check_message",
            os.environ.get(
                "AI_CHAT_UPDATE_CHECK_MESSAGE",
                "Update available: {current} -> {latest} -- pip install --upgrade anteroom",
            ),
        )
    )

    planning_raw = cli_raw.get("planning", {})
    if not isinstance(planning_raw, dict):
        planning_raw = {}
    planning_enabled = str(planning_raw.get("enabled", "true")).lower() not in ("false", "0", "no")
    try:
        planning_auto_threshold = max(0, int(planning_raw.get("auto_threshold_tools", 15)))
    except (ValueError, TypeError):
        planning_auto_threshold = 15
    planning_auto_mode = str(planning_raw.get("auto_mode", "off")).lower()
    if planning_auto_mode not in ("off", "suggest", "auto"):
        planning_auto_mode = "off"
    planning_config = PlanningConfig(
        enabled=planning_enabled,
        auto_threshold_tools=planning_auto_threshold,
        auto_mode=planning_auto_mode,
    )

    # Parse usage config
    usage_raw = cli_raw.get("usage", {})
    if not isinstance(usage_raw, dict):
        usage_raw = {}
    try:
        usage_week_days = max(1, int(usage_raw.get("week_days", 7)))
    except (ValueError, TypeError):
        usage_week_days = 7
    try:
        usage_month_days = max(1, int(usage_raw.get("month_days", 30)))
    except (ValueError, TypeError):
        usage_month_days = 30
    usage_model_costs = usage_raw.get("model_costs", {})
    if not isinstance(usage_model_costs, dict):
        usage_model_costs = {}
    usage_config = UsageConfig(
        week_days=usage_week_days,
        month_days=usage_month_days,
    )
    if usage_model_costs:
        # Merge user-provided costs with defaults (user overrides win)
        merged = dict(usage_config.model_costs)
        for model_name, costs in usage_model_costs.items():
            if isinstance(costs, dict):
                merged[str(model_name)] = {
                    "input": float(costs.get("input", 0)),
                    "output": float(costs.get("output", 0)),
                }
        usage_config.model_costs = merged

    # Parse budget config (under usage.budgets or top-level env vars)
    budgets_raw = usage_raw.get("budgets", {})
    if not isinstance(budgets_raw, dict):
        budgets_raw = {}
    budget_enabled_raw = budgets_raw.get("enabled", os.environ.get("AI_CHAT_BUDGET_ENABLED"))
    if budget_enabled_raw is not None:
        budget_enabled = str(budget_enabled_raw).lower() not in ("false", "0", "no")
    else:
        budget_enabled = False
    try:
        budget_max_per_request = max(
            0,
            int(
                budgets_raw.get(
                    "max_tokens_per_request",
                    os.environ.get("AI_CHAT_BUDGET_MAX_TOKENS_PER_REQUEST", 0),
                )
            ),
        )
    except (ValueError, TypeError):
        budget_max_per_request = 0
    try:
        budget_max_per_conversation = max(
            0,
            int(
                budgets_raw.get(
                    "max_tokens_per_conversation",
                    os.environ.get("AI_CHAT_BUDGET_MAX_TOKENS_PER_CONVERSATION", 0),
                )
            ),
        )
    except (ValueError, TypeError):
        budget_max_per_conversation = 0
    try:
        budget_max_per_day = max(
            0,
            int(
                budgets_raw.get(
                    "max_tokens_per_day",
                    os.environ.get("AI_CHAT_BUDGET_MAX_TOKENS_PER_DAY", 0),
                )
            ),
        )
    except (ValueError, TypeError):
        budget_max_per_day = 0
    try:
        budget_warn_pct = max(
            0,
            min(
                100,
                int(
                    budgets_raw.get(
                        "warn_threshold_percent",
                        os.environ.get("AI_CHAT_BUDGET_WARN_THRESHOLD_PERCENT", 80),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        budget_warn_pct = 80
    budget_action = str(
        budgets_raw.get(
            "action_on_exceed",
            os.environ.get("AI_CHAT_BUDGET_ACTION_ON_EXCEED", "block"),
        )
    ).lower()
    if budget_action not in ("block", "warn"):
        budget_action = "block"
    usage_config.budgets = BudgetConfig(
        enabled=budget_enabled,
        max_tokens_per_request=budget_max_per_request,
        max_tokens_per_conversation=budget_max_per_conversation,
        max_tokens_per_day=budget_max_per_day,
        warn_threshold_percent=budget_warn_pct,
        action_on_exceed=budget_action,
    )

    skills_raw = cli_raw.get("skills", {})
    if not isinstance(skills_raw, dict):
        skills_raw = {}
    skills_auto_invoke = str(skills_raw.get("auto_invoke", "true")).lower() not in ("false", "0", "no")
    skills_config = SkillsConfig(auto_invoke=skills_auto_invoke)

    # Parse cli.hierarchy (visual-hierarchy knobs, #1370)
    hierarchy_raw = cli_raw.get("hierarchy", {})
    if not isinstance(hierarchy_raw, dict):
        hierarchy_raw = {}
    hierarchy_show_timestamps_raw = os.environ.get(
        "AI_CHAT_CLI_HIERARCHY_SHOW_TIMESTAMPS",
        hierarchy_raw.get("show_timestamps", False),
    )
    hierarchy_show_timestamps = str(hierarchy_show_timestamps_raw).lower() in ("true", "1", "yes")
    hierarchy_turn_separator_char = str(
        os.environ.get(
            "AI_CHAT_CLI_HIERARCHY_TURN_SEPARATOR_CHAR",
            hierarchy_raw.get("turn_separator_char", "\u2500"),
        )
    )
    if not hierarchy_turn_separator_char:
        hierarchy_turn_separator_char = "\u2500"
    hierarchy_code_label_raw = os.environ.get(
        "AI_CHAT_CLI_HIERARCHY_CODE_BLOCK_LANGUAGE_LABEL",
        hierarchy_raw.get("code_block_language_label", True),
    )
    hierarchy_code_block_language_label = str(hierarchy_code_label_raw).lower() not in ("false", "0", "no")
    hierarchy_config = CliHierarchyConfig(
        show_timestamps=hierarchy_show_timestamps,
        turn_separator_char=hierarchy_turn_separator_char,
        code_block_language_label=hierarchy_code_block_language_label,
    )

    # Parse cli.streaming (live markdown streaming, #1365)
    streaming_raw = cli_raw.get("streaming", {})
    if not isinstance(streaming_raw, dict):
        streaming_raw = {}
    streaming_enabled_raw = os.environ.get(
        "AI_CHAT_CLI_STREAMING_ENABLED",
        streaming_raw.get("enabled", False),
    )
    streaming_enabled = str(streaming_enabled_raw).lower() not in ("false", "0", "no")
    streaming_refresh_hz_raw = os.environ.get(
        "AI_CHAT_CLI_STREAMING_REFRESH_HZ",
        streaming_raw.get("refresh_hz", 20.0),
    )
    try:
        streaming_refresh_hz = float(streaming_refresh_hz_raw)
    except (TypeError, ValueError):
        streaming_refresh_hz = 20.0
    if streaming_refresh_hz < 1.0:
        logger.warning(
            "cli.streaming.refresh_hz=%s below minimum (1.0), clamping",
            streaming_refresh_hz,
        )
        streaming_refresh_hz = 1.0
    elif streaming_refresh_hz > 60.0:
        logger.warning(
            "cli.streaming.refresh_hz=%s above maximum (60.0), clamping",
            streaming_refresh_hz,
        )
        streaming_refresh_hz = 60.0
    streaming_live_exec_raw = os.environ.get(
        "AI_CHAT_CLI_STREAMING_LIVE_IN_EXEC_MODE",
        streaming_raw.get("live_in_exec_mode", False),
    )
    streaming_live_in_exec_mode = str(streaming_live_exec_raw).lower() in ("true", "1", "yes")
    streaming_fence_raw = os.environ.get(
        "AI_CHAT_CLI_STREAMING_CODE_FENCE_CONTAINER",
        streaming_raw.get("code_fence_container", True),
    )
    streaming_code_fence_container = str(streaming_fence_raw).lower() not in ("false", "0", "no")
    streaming_config = CliStreamingConfig(
        enabled=streaming_enabled,
        refresh_hz=streaming_refresh_hz,
        live_in_exec_mode=streaming_live_in_exec_mode,
        code_fence_container=streaming_code_fence_container,
    )

    # Parse cli.live_tools (compact live tool-call lifecycle, #1364)
    live_tools_raw = cli_raw.get("live_tools", {})
    if not isinstance(live_tools_raw, dict):
        live_tools_raw = {}
    live_tools_show_args_raw = os.environ.get(
        "AI_CHAT_CLI_LIVE_TOOLS_SHOW_ARGS_IN_VERBOSE",
        live_tools_raw.get("show_args_in_verbose", True),
    )
    live_tools_show_args_in_verbose = str(live_tools_show_args_raw).lower() not in ("false", "0", "no")
    live_tools_show_metric_raw = os.environ.get(
        "AI_CHAT_CLI_LIVE_TOOLS_SHOW_METRIC_SUFFIX",
        live_tools_raw.get("show_metric_suffix", True),
    )
    live_tools_show_metric_suffix = str(live_tools_show_metric_raw).lower() not in ("false", "0", "no")
    live_tools_metric_max_raw = os.environ.get(
        "AI_CHAT_CLI_LIVE_TOOLS_METRIC_MAX_CHARS",
        live_tools_raw.get("metric_max_chars", 40),
    )
    try:
        live_tools_metric_max_chars = int(live_tools_metric_max_raw)
    except (TypeError, ValueError):
        live_tools_metric_max_chars = 40
    if live_tools_metric_max_chars < 1:
        logger.warning(
            "cli.live_tools.metric_max_chars=%s below minimum (1), clamping",
            live_tools_metric_max_chars,
        )
        live_tools_metric_max_chars = 1
    elif live_tools_metric_max_chars > 200:
        logger.warning(
            "cli.live_tools.metric_max_chars=%s above maximum (200), clamping",
            live_tools_metric_max_chars,
        )
        live_tools_metric_max_chars = 200
    live_tools_config = CliLiveToolsConfig(
        show_args_in_verbose=live_tools_show_args_in_verbose,
        show_metric_suffix=live_tools_show_metric_suffix,
        metric_max_chars=live_tools_metric_max_chars,
    )

    # Parse cli.density (tool-result density knobs, #1367)
    density_raw = cli_raw.get("density", {})
    if not isinstance(density_raw, dict):
        density_raw = {}
    density_mode = str(
        os.environ.get(
            "AI_CHAT_CLI_DENSITY_MODE",
            density_raw.get("mode", "normal"),
        )
    ).lower()
    if density_mode not in ("minimal", "compact", "normal", "detailed", "auto"):
        logger.warning(
            "cli.density.mode=%s not recognised, falling back to 'normal'",
            density_mode,
        )
        density_mode = "normal"
    density_collapse_raw = os.environ.get(
        "AI_CHAT_CLI_DENSITY_COLLAPSE_REPEATS",
        density_raw.get("collapse_repeats", True),
    )
    density_collapse_repeats = str(density_collapse_raw).lower() not in ("false", "0", "no")
    try:
        density_diff_context_lines = int(
            os.environ.get(
                "AI_CHAT_CLI_DENSITY_DIFF_CONTEXT_LINES",
                density_raw.get("diff_context_lines", 3),
            )
        )
    except (TypeError, ValueError):
        density_diff_context_lines = 3
    if density_diff_context_lines < 0:
        density_diff_context_lines = 0
    try:
        density_head_lines = int(
            os.environ.get(
                "AI_CHAT_CLI_DENSITY_HEAD_LINES",
                density_raw.get("head_lines", 3),
            )
        )
    except (TypeError, ValueError):
        density_head_lines = 3
    if density_head_lines < 0:
        density_head_lines = 0
    try:
        density_tail_lines = int(
            os.environ.get(
                "AI_CHAT_CLI_DENSITY_TAIL_LINES",
                density_raw.get("tail_lines", 2),
            )
        )
    except (TypeError, ValueError):
        density_tail_lines = 2
    if density_tail_lines < 0:
        density_tail_lines = 0
    density_config = CliDensityConfig(
        mode=density_mode,
        collapse_repeats=density_collapse_repeats,
        diff_context_lines=density_diff_context_lines,
        head_lines=density_head_lines,
        tail_lines=density_tail_lines,
    )

    input_raw = cli_raw.get("input", {})
    if not isinstance(input_raw, dict):
        input_raw = {}
    input_editing_mode = (
        str(
            input_raw.get(
                "editing_mode",
                os.environ.get("AI_CHAT_EDITING_MODE", "emacs"),
            )
        )
        .strip()
        .lower()
    )
    if input_editing_mode not in ("emacs", "vi"):
        input_editing_mode = "emacs"
    input_show_hints = str(
        os.environ.get(
            "AI_CHAT_INPUT_HINTS",
            input_raw.get("show_hints", True),
        )
    ).lower() not in ("false", "0", "no")
    try:
        input_hint_max_displays = max(
            0,
            min(
                10,
                int(
                    os.environ.get(
                        "AI_CHAT_INPUT_HINT_MAX_DISPLAYS",
                        input_raw.get("hint_max_displays", 1),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        input_hint_max_displays = 1
    try:
        input_large_paste_lines = max(
            2,
            min(
                100,
                int(
                    os.environ.get(
                        "AI_CHAT_INPUT_LARGE_PASTE_LINES",
                        input_raw.get("large_paste_lines", 5),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        input_large_paste_lines = 5
    input_show_mode_badge = str(
        os.environ.get(
            "AI_CHAT_INPUT_SHOW_MODE_BADGE",
            input_raw.get("show_mode_badge", False),
        )
    ).lower() not in ("false", "0", "no")
    input_config = CliInputConfig(
        editing_mode=input_editing_mode,
        show_hints=input_show_hints,
        hint_max_displays=input_hint_max_displays,
        large_paste_lines=input_large_paste_lines,
        show_mode_badge=input_show_mode_badge,
    )

    cli_config = CliConfig(
        builtin_tools=cli_raw.get("builtin_tools", True),
        max_tool_iterations=int(cli_raw.get("max_tool_iterations", 50)),
        context_warn_tokens=context_warn_tokens,
        context_auto_compact_tokens=context_auto_compact_tokens,
        context_reserved_output_tokens=context_thresholds.reserved_output_tokens,
        context_warn_buffer_tokens=context_warn_buffer_tokens,
        context_auto_compact_buffer_tokens=context_auto_compact_buffer_tokens,
        tool_dedup=tool_dedup,
        retry_delay=retry_delay,
        max_retries=max_retries,
        esc_hint_delay=esc_hint_delay,
        stall_display_threshold=stall_display_threshold,
        stall_warning_threshold=stall_warning_threshold,
        stall_throughput_threshold=stall_throughput_threshold,
        tool_output_max_chars=tool_output_max_chars,
        tool_replay_max_chars=tool_replay_max_chars,
        file_reference_max_chars=file_reference_max_chars,
        model_context_window=model_context_window,
        background_suggest_seconds=background_suggest_seconds,
        detach_suggest_seconds=detach_suggest_seconds,
        update_check=update_check,
        update_check_command=update_check_command,
        update_check_message=update_check_message,
        show_attribution_footer=str(
            os.environ.get(
                "AI_CHAT_SHOW_ATTRIBUTION_FOOTER",
                cli_raw.get("show_attribution_footer", True),
            )
        ).lower()
        not in ("false", "0", "no"),
        planning=planning_config,
        usage=usage_config,
        skills=skills_config,
        hierarchy=hierarchy_config,
        streaming=streaming_config,
        live_tools=live_tools_config,
        density=density_config,
        input=input_config,
    )

    identity_raw = raw.get("identity", {})
    identity_user_id = identity_raw.get("user_id") or os.environ.get("AI_CHAT_USER_ID", "")
    identity_display_name = identity_raw.get("display_name") or os.environ.get("AI_CHAT_DISPLAY_NAME", "")
    identity_public_key = identity_raw.get("public_key") or os.environ.get("AI_CHAT_PUBLIC_KEY", "")
    identity_private_key = identity_raw.get("private_key") or os.environ.get("AI_CHAT_PRIVATE_KEY", "")

    identity: UserIdentity | None = None
    if identity_user_id:
        identity = UserIdentity(
            user_id=identity_user_id,
            display_name=identity_display_name,
            public_key=identity_public_key,
            private_key=identity_private_key,
        )

    emb_raw = raw.get("embeddings", {})
    _emb_enabled_raw = emb_raw.get("enabled", os.environ.get("AI_CHAT_EMBEDDINGS_ENABLED"))
    if _emb_enabled_raw is None:
        emb_enabled: bool | None = None  # auto-detect at startup
    else:
        emb_enabled = str(_emb_enabled_raw).lower() not in ("false", "0", "no")
    emb_provider = emb_raw.get("provider") or os.environ.get("AI_CHAT_EMBEDDINGS_PROVIDER", "local")
    emb_model = emb_raw.get("model") or os.environ.get("AI_CHAT_EMBEDDINGS_MODEL", "text-embedding-3-small")
    emb_local_model = emb_raw.get("local_model") or os.environ.get(
        "AI_CHAT_EMBEDDINGS_LOCAL_MODEL", "BAAI/bge-small-en-v1.5"
    )
    emb_dimensions_raw = emb_raw.get("dimensions") or os.environ.get("AI_CHAT_EMBEDDINGS_DIMENSIONS", "")
    if emb_dimensions_raw:
        emb_dimensions = int(emb_dimensions_raw)
        emb_dimensions = max(1, min(emb_dimensions, 4096))
    else:
        # Auto-detect: 0 means "use model default"
        emb_dimensions = 0
    emb_base_url = emb_raw.get("base_url") or os.environ.get("AI_CHAT_EMBEDDINGS_BASE_URL", "")
    emb_api_key = emb_raw.get("api_key") or os.environ.get("AI_CHAT_EMBEDDINGS_API_KEY", "")
    emb_api_key_command = emb_raw.get("api_key_command") or os.environ.get("AI_CHAT_EMBEDDINGS_API_KEY_COMMAND", "")
    emb_cache_dir = emb_raw.get("cache_dir") or os.environ.get("AI_CHAT_EMBEDDINGS_CACHE_DIR", "")

    embeddings_config = EmbeddingsConfig(
        enabled=emb_enabled,
        provider=emb_provider,
        model=emb_model,
        dimensions=emb_dimensions,
        local_model=emb_local_model,
        base_url=emb_base_url,
        api_key=emb_api_key,
        api_key_command=emb_api_key_command,
        cache_dir=str(emb_cache_dir),
    )

    safety_raw = raw.get("safety", {})
    safety_enabled = str(safety_raw.get("enabled", os.environ.get("AI_CHAT_SAFETY_ENABLED", "true"))).lower() not in (
        "false",
        "0",
        "no",
    )
    safety_timeout = int(safety_raw.get("approval_timeout", 120))
    safety_timeout = max(10, min(safety_timeout, 600))
    bash_raw = safety_raw.get("bash", {})
    if not isinstance(bash_raw, dict):
        bash_raw = {}
    bash_safety_enabled = str(bash_raw.get("enabled", "true")).lower() not in ("false", "0", "no")

    def _bash_bool(key: str, env_key: str, default: bool) -> bool:
        return str(bash_raw.get(key, os.environ.get(env_key, str(default)))).lower() in ("true", "1", "yes")

    def _bash_int(key: str, env_key: str, default: int) -> int:
        try:
            return int(bash_raw.get(key, os.environ.get(env_key, default)))
        except (ValueError, TypeError):
            return default

    def _bash_list(key: str, env_key: str) -> list[str]:
        val = bash_raw.get(key)
        if val is None:
            env_val = os.environ.get(env_key, "")
            return [s.strip() for s in env_val.split(",") if s.strip()] if env_val else []
        if isinstance(val, list):
            return [str(v) for v in val]
        return []

    # Parse OS-level sandbox config (safety.bash.sandbox)
    sandbox_raw = bash_raw.get("sandbox", {})
    if not isinstance(sandbox_raw, dict):
        sandbox_raw = {}

    def _sandbox_int(key: str, env_key: str, default: int) -> int:
        try:
            return int(sandbox_raw.get(key, os.environ.get(env_key, default)))
        except (ValueError, TypeError):
            return default

    def _sandbox_optional_int(key: str, env_key: str) -> int | None:
        val = sandbox_raw.get(key)
        if val is None:
            env_val = os.environ.get(env_key)
            if env_val is None:
                return None
            val = env_val
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    sandbox_enabled_raw = sandbox_raw.get("enabled", os.environ.get("AI_CHAT_BASH_SANDBOX_ENABLED"))
    sandbox_enabled: bool | None = None
    if sandbox_enabled_raw is not None:
        sandbox_enabled = str(sandbox_enabled_raw).lower() in ("true", "1", "yes")

    os_sandbox = OsSandboxConfig(
        enabled=sandbox_enabled,
        max_memory_mb=_sandbox_int("max_memory_mb", "AI_CHAT_BASH_SANDBOX_MAX_MEMORY_MB", 512),
        max_processes=_sandbox_int("max_processes", "AI_CHAT_BASH_SANDBOX_MAX_PROCESSES", 10),
        cpu_time_limit=_sandbox_optional_int("cpu_time_limit", "AI_CHAT_BASH_SANDBOX_CPU_TIME_LIMIT"),
    )

    bash_sandbox = BashSandboxConfig(
        enabled=bash_safety_enabled,
        timeout=_bash_int("timeout", "AI_CHAT_BASH_TIMEOUT", 120),
        max_output_chars=_bash_int("max_output_chars", "AI_CHAT_BASH_MAX_OUTPUT", 100_000),
        blocked_paths=_bash_list("blocked_paths", "AI_CHAT_BASH_BLOCKED_PATHS"),
        allowed_paths=_bash_list("allowed_paths", "AI_CHAT_BASH_ALLOWED_PATHS"),
        blocked_commands=_bash_list("blocked_commands", "AI_CHAT_BASH_BLOCKED_COMMANDS"),
        allow_network=_bash_bool("allow_network", "AI_CHAT_BASH_ALLOW_NETWORK", True),
        allow_package_install=_bash_bool("allow_package_install", "AI_CHAT_BASH_ALLOW_PACKAGE_INSTALL", True),
        log_all_commands=_bash_bool("log_all_commands", "AI_CHAT_BASH_LOG_ALL_COMMANDS", False),
        sandbox=os_sandbox,
    )
    wf_raw = safety_raw.get("write_file", {})
    wf_safety_enabled = str(wf_raw.get("enabled", "true")).lower() not in ("false", "0", "no")
    safety_approval_mode = str(
        safety_raw.get("approval_mode", os.environ.get("AI_CHAT_SAFETY_APPROVAL_MODE", "ask_for_writes"))
    ).strip()
    safety_custom_patterns = safety_raw.get("custom_patterns", [])
    if not isinstance(safety_custom_patterns, list):
        safety_custom_patterns = []
    safety_sensitive_paths = safety_raw.get("sensitive_paths", [])
    if not isinstance(safety_sensitive_paths, list):
        safety_sensitive_paths = []
    safety_bypass_immune_paths_raw = safety_raw.get("bypass_immune_paths", None)
    if safety_bypass_immune_paths_raw is not None and isinstance(safety_bypass_immune_paths_raw, list):
        safety_bypass_immune_paths: list[str] | None = [str(p) for p in safety_bypass_immune_paths_raw]
    else:
        safety_bypass_immune_paths = None
    safety_allowed_tools = safety_raw.get("allowed_tools", [])
    if not isinstance(safety_allowed_tools, list):
        safety_allowed_tools = []
    safety_denied_tools = safety_raw.get("denied_tools", [])
    if not isinstance(safety_denied_tools, list):
        safety_denied_tools = []
    safety_tool_tiers = safety_raw.get("tool_tiers", {})
    if not isinstance(safety_tool_tiers, dict):
        safety_tool_tiers = {}
    safety_read_only = str(safety_raw.get("read_only", os.environ.get("AI_CHAT_READ_ONLY", "false"))).lower() in (
        "true",
        "1",
        "yes",
    )

    sa_raw = safety_raw.get("subagent", {})
    if not isinstance(sa_raw, dict):
        sa_raw = {}

    def _sa_int(key: str, default: int, lo: int, hi: int) -> int:
        try:
            val = int(sa_raw.get(key, default))
        except (ValueError, TypeError):
            val = default
        return max(lo, min(val, hi))

    subagent_config = SubagentConfig(
        max_concurrent=_sa_int("max_concurrent", 5, 1, 20),
        max_total=_sa_int("max_total", 10, 1, 50),
        max_depth=_sa_int("max_depth", 3, 1, 10),
        max_iterations=_sa_int("max_iterations", 15, 1, 100),
        timeout=_sa_int("timeout", 120, 10, 600),
        max_output_chars=_sa_int("max_output_chars", 4000, 100, 100_000),
        max_prompt_chars=_sa_int("max_prompt_chars", 32_000, 100, 100_000),
    )

    trl_raw = safety_raw.get("tool_rate_limit", {})
    if not isinstance(trl_raw, dict):
        trl_raw = {}

    def _trl_int(key: str, default: int, lo: int, hi: int) -> int:
        try:
            val = int(trl_raw.get(key, default))
        except (ValueError, TypeError):
            val = default
        return max(lo, min(val, hi))

    trl_action = str(trl_raw.get("action", "block")).lower()
    if trl_action not in ("block", "warn"):
        trl_action = "block"

    tool_rate_limit_config = ToolRateLimitConfig(
        max_calls_per_minute=_trl_int("max_calls_per_minute", 0, 0, 100_000),
        max_calls_per_conversation=_trl_int("max_calls_per_conversation", 0, 0, 100_000),
        max_consecutive_failures=_trl_int("max_consecutive_failures", 5, 0, 1000),
        action=trl_action,
    )

    # DLP config
    dlp_raw = safety_raw.get("dlp", {})
    if not isinstance(dlp_raw, dict):
        dlp_raw = {}
    dlp_enabled = str(dlp_raw.get("enabled", os.environ.get("AI_CHAT_DLP_ENABLED", "false"))).lower() in (
        "true",
        "1",
        "yes",
    )
    dlp_scan_output = str(dlp_raw.get("scan_output", "true")).lower() not in ("false", "0", "no")
    dlp_scan_input = str(dlp_raw.get("scan_input", "false")).lower() in ("true", "1", "yes")
    dlp_action = str(dlp_raw.get("action", os.environ.get("AI_CHAT_DLP_ACTION", "redact"))).lower()
    if dlp_action not in ("redact", "block", "warn"):
        dlp_action = "redact"
    dlp_redaction_string = str(dlp_raw.get("redaction_string", "[REDACTED]"))
    dlp_log_detections = str(dlp_raw.get("log_detections", "true")).lower() not in ("false", "0", "no")

    dlp_patterns: list[DlpPatternConfig] = []
    for rule_raw in dlp_raw.get("patterns", []):
        if not isinstance(rule_raw, dict) or not rule_raw.get("name") or not rule_raw.get("pattern"):
            continue
        dlp_patterns.append(
            DlpPatternConfig(
                name=str(rule_raw["name"]),
                pattern=str(rule_raw["pattern"]),
                description=str(rule_raw.get("description", "")),
            )
        )
    dlp_custom: list[DlpPatternConfig] = []
    for rule_raw in dlp_raw.get("custom_patterns", []):
        if not isinstance(rule_raw, dict) or not rule_raw.get("name") or not rule_raw.get("pattern"):
            continue
        dlp_custom.append(
            DlpPatternConfig(
                name=str(rule_raw["name"]),
                pattern=str(rule_raw["pattern"]),
                description=str(rule_raw.get("description", "")),
            )
        )

    dlp_config = DlpConfig(
        enabled=dlp_enabled,
        scan_output=dlp_scan_output,
        scan_input=dlp_scan_input,
        action=dlp_action,
        patterns=dlp_patterns,
        custom_patterns=dlp_custom,
        redaction_string=dlp_redaction_string,
        log_detections=dlp_log_detections,
    )

    # Output filter config
    of_raw = safety_raw.get("output_filter", {})
    if not isinstance(of_raw, dict):
        of_raw = {}
    of_enabled = str(of_raw.get("enabled", os.environ.get("AI_CHAT_OUTPUT_FILTER_ENABLED", "false"))).lower() in (
        "true",
        "1",
        "yes",
    )
    of_leak_detection = str(of_raw.get("system_prompt_leak_detection", "true")).lower() not in ("false", "0", "no")
    try:
        of_leak_threshold = max(0.01, min(1.0, float(of_raw.get("leak_threshold", 0.4))))
    except (ValueError, TypeError):
        of_leak_threshold = 0.4
    of_action = str(of_raw.get("action", os.environ.get("AI_CHAT_OUTPUT_FILTER_ACTION", "warn"))).lower()
    if of_action not in ("warn", "block", "redact"):
        of_action = "warn"
    of_redaction_string = str(of_raw.get("redaction_string", "[FILTERED]"))
    of_log_detections = str(of_raw.get("log_detections", "true")).lower() not in ("false", "0", "no")

    of_custom: list[OutputFilterPatternConfig] = []
    for rule_raw in of_raw.get("custom_patterns", []):
        if not isinstance(rule_raw, dict) or not rule_raw.get("name") or not rule_raw.get("pattern"):
            continue
        of_custom.append(
            OutputFilterPatternConfig(
                name=str(rule_raw["name"]),
                pattern=str(rule_raw["pattern"]),
                description=str(rule_raw.get("description", "")),
            )
        )

    output_filter_config = OutputFilterConfig(
        enabled=of_enabled,
        system_prompt_leak_detection=of_leak_detection,
        leak_threshold=of_leak_threshold,
        custom_patterns=of_custom,
        action=of_action,
        redaction_string=of_redaction_string,
        log_detections=of_log_detections,
    )

    safety_kwargs: dict[str, Any] = {
        "enabled": safety_enabled,
        "approval_mode": safety_approval_mode,
        "approval_timeout": safety_timeout,
        "bash": bash_sandbox,
        "write_file": SafetyToolConfig(enabled=wf_safety_enabled),
        "custom_patterns": [str(p) for p in safety_custom_patterns],
        "sensitive_paths": [str(p) for p in safety_sensitive_paths],
        "allowed_tools": [str(t) for t in safety_allowed_tools],
        "denied_tools": [str(t) for t in safety_denied_tools],
        "tool_tiers": {str(k): str(v) for k, v in safety_tool_tiers.items()},
        "read_only": safety_read_only,
        "subagent": subagent_config,
        "tool_rate_limit": tool_rate_limit_config,
        "dlp": dlp_config,
        "output_filter": output_filter_config,
    }
    if safety_bypass_immune_paths is not None:
        safety_kwargs["bypass_immune_paths"] = safety_bypass_immune_paths

    safety_config = SafetyConfig(
        **safety_kwargs,
    )

    # Compaction config (#1413)
    compaction_raw = raw.get("compaction", {})
    if not isinstance(compaction_raw, dict):
        compaction_raw = {}
    # Backward-compat: tolerate the old CLI-nested key until existing configs
    # are migrated.  Precedence: explicit `compaction.preserve_tail` wins,
    # then `cli.compact_preserve_tail`, then env, then default.
    _legacy_cli_preserve = cli_raw.get("compact_preserve_tail")
    try:
        # Clamped to [0, 200] to guard against misconfiguration silently
        # defeating compaction (e.g. AI_CHAT_COMPACT_PRESERVE_TAIL=999999).
        preserve_tail_raw = compaction_raw.get(
            "preserve_tail",
            _legacy_cli_preserve
            if _legacy_cli_preserve is not None
            else os.environ.get("AI_CHAT_COMPACT_PRESERVE_TAIL", 6),
        )
        preserve_tail = max(0, min(200, int(preserve_tail_raw)))
    except (ValueError, TypeError):
        preserve_tail = 6
    # Rehydration config (#1414).  Precedence: YAML wins, then env, then default.
    _rehydrate_raw = compaction_raw.get(
        "compact_rehydrate",
        os.environ.get("AI_CHAT_COMPACT_REHYDRATE", "true"),
    )
    compact_rehydrate = str(_rehydrate_raw).lower() not in ("false", "0", "no", "off")
    try:
        compact_rehydrate_max_files = max(
            0,
            min(
                200,
                int(
                    compaction_raw.get(
                        "compact_rehydrate_max_files",
                        os.environ.get("AI_CHAT_COMPACT_REHYDRATE_MAX_FILES", 20),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        compact_rehydrate_max_files = 20
    try:
        compact_rehydrate_max_errors = max(
            0,
            min(
                50,
                int(
                    compaction_raw.get(
                        "compact_rehydrate_max_errors",
                        os.environ.get("AI_CHAT_COMPACT_REHYDRATE_MAX_ERRORS", 5),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        compact_rehydrate_max_errors = 5

    # Proactive microcompact toggle (#1266).  YAML wins, then env, then default.
    _microcompact_raw = compaction_raw.get(
        "microcompact_enabled",
        os.environ.get("AI_CHAT_MICROCOMPACT_ENABLED", "true"),
    )
    microcompact_enabled = str(_microcompact_raw).lower() not in ("false", "0", "no", "off")

    _historical_tool_collapse_raw = compaction_raw.get(
        "historical_tool_collapse_enabled",
        os.environ.get("AI_CHAT_HISTORICAL_TOOL_COLLAPSE_ENABLED", "true"),
    )
    historical_tool_collapse_enabled = str(_historical_tool_collapse_raw).lower() not in (
        "false",
        "0",
        "no",
        "off",
    )
    try:
        historical_tool_collapse_trigger_token_count = max(
            5_000,
            min(
                500_000,
                int(
                    compaction_raw.get(
                        "historical_tool_collapse_trigger_token_count",
                        os.environ.get("AI_CHAT_HISTORICAL_TOOL_COLLAPSE_TRIGGER_TOKEN_COUNT", 80_000),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        historical_tool_collapse_trigger_token_count = 80_000
    try:
        historical_tool_collapse_keep_recent_groups = max(
            0,
            min(
                200,
                int(
                    compaction_raw.get(
                        "historical_tool_collapse_keep_recent_groups",
                        os.environ.get("AI_CHAT_HISTORICAL_TOOL_COLLAPSE_KEEP_RECENT_GROUPS", 6),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        historical_tool_collapse_keep_recent_groups = 6
    try:
        historical_tool_collapse_compact_chars = max(
            50,
            min(
                50_000,
                int(
                    compaction_raw.get(
                        "historical_tool_collapse_compact_chars",
                        os.environ.get("AI_CHAT_HISTORICAL_TOOL_COLLAPSE_COMPACT_CHARS", 1_000),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        historical_tool_collapse_compact_chars = 1_000

    # Summary compaction triggers (#1266 — promoted from hardcoded constants).
    try:
        summary_trigger_msg_count = max(
            10,
            min(
                1000,
                int(
                    compaction_raw.get(
                        "summary_trigger_msg_count",
                        os.environ.get("AI_CHAT_SUMMARY_TRIGGER_MSG_COUNT", 80),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        summary_trigger_msg_count = 80
    # Reactive overflow ladder retry cap (#1266 — promoted from hardcoded constant).
    try:
        reactive_max_attempts = max(
            0,
            min(
                10,
                int(
                    compaction_raw.get(
                        "reactive_max_attempts",
                        os.environ.get("AI_CHAT_REACTIVE_MAX_ATTEMPTS", 4),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        reactive_max_attempts = 4

    try:
        summary_max_completion_tokens = max(
            256,
            min(
                16_000,
                int(
                    compaction_raw.get(
                        "summary_max_completion_tokens",
                        os.environ.get("AI_CHAT_COMPACT_SUMMARY_MAX_TOKENS", 1000),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        summary_max_completion_tokens = 1000

    try:
        summary_retry_max_attempts = max(
            1,
            min(
                10,
                int(
                    compaction_raw.get(
                        "summary_retry_max_attempts",
                        os.environ.get("AI_CHAT_COMPACT_SUMMARY_RETRY_MAX_ATTEMPTS", 3),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        summary_retry_max_attempts = 3

    try:
        summary_retry_drop_groups = max(
            1,
            min(
                50,
                int(
                    compaction_raw.get(
                        "summary_retry_drop_groups",
                        os.environ.get("AI_CHAT_COMPACT_SUMMARY_RETRY_DROP_GROUPS", 2),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        summary_retry_drop_groups = 2

    compaction_config = CompactionConfig(
        preserve_tail=preserve_tail,
        compact_rehydrate=compact_rehydrate,
        compact_rehydrate_max_files=compact_rehydrate_max_files,
        compact_rehydrate_max_errors=compact_rehydrate_max_errors,
        microcompact_enabled=microcompact_enabled,
        historical_tool_collapse_enabled=historical_tool_collapse_enabled,
        historical_tool_collapse_trigger_token_count=historical_tool_collapse_trigger_token_count,
        historical_tool_collapse_keep_recent_groups=historical_tool_collapse_keep_recent_groups,
        historical_tool_collapse_compact_chars=historical_tool_collapse_compact_chars,
        summary_trigger_msg_count=summary_trigger_msg_count,
        summary_trigger_token_count=summary_trigger_token_count,
        summary_trigger_buffer_tokens=summary_trigger_buffer_tokens,
        reactive_max_attempts=reactive_max_attempts,
        summary_max_completion_tokens=summary_max_completion_tokens,
        summary_retry_max_attempts=summary_retry_max_attempts,
        summary_retry_drop_groups=summary_retry_drop_groups,
    )

    # RAG config
    rag_raw = raw.get("rag", {})
    if not isinstance(rag_raw, dict):
        rag_raw = {}
    rag_enabled = str(rag_raw.get("enabled", os.environ.get("AI_CHAT_RAG_ENABLED", "true"))).lower() not in (
        "false",
        "0",
        "no",
    )
    try:
        rag_max_chunks = max(1, min(50, int(rag_raw.get("max_chunks", os.environ.get("AI_CHAT_RAG_MAX_CHUNKS", 10)))))
    except (ValueError, TypeError):
        rag_max_chunks = 10
    try:
        _raw_rag_tokens = rag_raw.get("max_tokens", os.environ.get("AI_CHAT_RAG_MAX_TOKENS", 2000))
        rag_max_tokens = max(100, min(20_000, int(_raw_rag_tokens)))
    except (ValueError, TypeError):
        rag_max_tokens = 2000
    try:
        _raw_rag_threshold = rag_raw.get(
            "similarity_threshold", os.environ.get("AI_CHAT_RAG_SIMILARITY_THRESHOLD", 0.5)
        )
        rag_threshold = max(0.0, min(2.0, float(_raw_rag_threshold)))
    except (ValueError, TypeError):
        rag_threshold = 0.5
    rag_include_sources = str(rag_raw.get("include_sources", "true")).lower() not in ("false", "0", "no")
    rag_include_conversations = str(rag_raw.get("include_conversations", "true")).lower() not in ("false", "0", "no")
    rag_exclude_current = str(rag_raw.get("exclude_current", "true")).lower() not in ("false", "0", "no")
    _raw_retrieval_mode = str(
        rag_raw.get("retrieval_mode", os.environ.get("AI_CHAT_RAG_RETRIEVAL_MODE", "dense"))
    ).lower()
    rag_retrieval_mode = _raw_retrieval_mode if _raw_retrieval_mode in ("dense", "keyword", "hybrid") else "dense"
    rag_show_status = str(
        rag_raw.get("show_status", os.environ.get("AI_CHAT_RAG_SHOW_STATUS", "true"))
    ).lower() not in ("false", "0", "no")
    rag_config = RagConfig(
        enabled=rag_enabled,
        max_chunks=rag_max_chunks,
        max_tokens=rag_max_tokens,
        similarity_threshold=rag_threshold,
        include_sources=rag_include_sources,
        include_conversations=rag_include_conversations,
        exclude_current=rag_exclude_current,
        retrieval_mode=rag_retrieval_mode,
        show_status=rag_show_status,
    )

    # Reranker config
    reranker_raw = raw.get("reranker", {})
    if not isinstance(reranker_raw, dict):
        reranker_raw = {}
    _raw_reranker_enabled = reranker_raw.get("enabled", os.environ.get("AI_CHAT_RERANKER_ENABLED", ""))
    if _raw_reranker_enabled == "" or _raw_reranker_enabled is None:
        reranker_enabled: bool | None = None  # auto-detect
    else:
        reranker_enabled = str(_raw_reranker_enabled).lower() in ("true", "1", "yes")
    _raw_reranker_provider = str(
        reranker_raw.get("provider", os.environ.get("AI_CHAT_RERANKER_PROVIDER", "local"))
    ).lower()
    reranker_provider = _raw_reranker_provider if _raw_reranker_provider in ("local",) else "local"
    reranker_model = str(
        reranker_raw.get("model", os.environ.get("AI_CHAT_RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"))
    )
    try:
        reranker_top_k = max(1, min(50, int(reranker_raw.get("top_k", os.environ.get("AI_CHAT_RERANKER_TOP_K", 5)))))
    except (ValueError, TypeError):
        reranker_top_k = 5
    try:
        _raw_score_threshold = reranker_raw.get(
            "score_threshold", os.environ.get("AI_CHAT_RERANKER_SCORE_THRESHOLD", 0.0)
        )
        reranker_score_threshold = float(_raw_score_threshold)
    except (ValueError, TypeError):
        reranker_score_threshold = 0.0
    try:
        reranker_candidate_multiplier = max(
            1,
            min(
                10,
                int(
                    reranker_raw.get("candidate_multiplier", os.environ.get("AI_CHAT_RERANKER_CANDIDATE_MULTIPLIER", 3))
                ),
            ),
        )
    except (ValueError, TypeError):
        reranker_candidate_multiplier = 3
    reranker_cache_dir = reranker_raw.get("cache_dir") or os.environ.get("AI_CHAT_RERANKER_CACHE_DIR", "")
    reranker_config = RerankerConfig(
        enabled=reranker_enabled,
        provider=reranker_provider,
        model=reranker_model,
        top_k=reranker_top_k,
        score_threshold=reranker_score_threshold,
        candidate_multiplier=reranker_candidate_multiplier,
        cache_dir=str(reranker_cache_dir),
    )

    # Memory recall config (#921)
    mr_raw = raw.get("memory_recall", {})
    if not isinstance(mr_raw, dict):
        mr_raw = {}
    _raw_mr_enabled = mr_raw.get("enabled", os.environ.get("AI_CHAT_MEMORY_RECALL_ENABLED", ""))
    if _raw_mr_enabled == "" or _raw_mr_enabled is None:
        mr_enabled: bool | None = None  # auto-detect
    else:
        mr_enabled = str(_raw_mr_enabled).lower() in ("true", "1", "yes")
    try:
        mr_max_memories = max(
            1, min(50, int(mr_raw.get("max_memories", os.environ.get("AI_CHAT_MEMORY_RECALL_MAX_MEMORIES", 5))))
        )
    except (ValueError, TypeError):
        mr_max_memories = 5
    try:
        mr_max_tokens = max(
            50, min(10_000, int(mr_raw.get("max_tokens", os.environ.get("AI_CHAT_MEMORY_RECALL_MAX_TOKENS", 800))))
        )
    except (ValueError, TypeError):
        mr_max_tokens = 800
    try:
        mr_threshold = max(
            0.0,
            min(
                2.0,
                float(
                    mr_raw.get(
                        "similarity_threshold",
                        os.environ.get("AI_CHAT_MEMORY_RECALL_SIMILARITY_THRESHOLD", 0.5),
                    )
                ),
            ),
        )
    except (ValueError, TypeError):
        mr_threshold = 0.5
    mr_show_status = str(
        mr_raw.get("show_status", os.environ.get("AI_CHAT_MEMORY_RECALL_SHOW_STATUS", "true"))
    ).lower() not in ("false", "0", "no")
    memory_recall_config = MemoryRecallConfig(
        enabled=mr_enabled,
        max_memories=mr_max_memories,
        max_tokens=mr_max_tokens,
        similarity_threshold=mr_threshold,
        show_status=mr_show_status,
    )

    # Proxy config
    proxy_raw = raw.get("proxy", {})
    if not isinstance(proxy_raw, dict):
        proxy_raw = {}
    proxy_enabled = str(proxy_raw.get("enabled", os.environ.get("AI_CHAT_PROXY_ENABLED", "false"))).lower() in (
        "true",
        "1",
        "yes",
    )
    proxy_origins_raw = proxy_raw.get("allowed_origins", [])
    if not isinstance(proxy_origins_raw, list):
        proxy_origins_raw = []
    proxy_origins: list[str] = []
    for o in proxy_origins_raw:
        origin = str(o).rstrip("/")
        if origin == "*" or not origin.startswith(("http://", "https://")):
            logger.warning("Ignoring invalid proxy allowed_origin: %s", origin)
            continue
        proxy_origins.append(origin)
    proxy_config = ProxyConfig(
        enabled=proxy_enabled,
        allowed_origins=proxy_origins,
    )

    # References (instructions, rules, skills from team/project configs)
    refs_raw = raw.get("references", {})
    if not isinstance(refs_raw, dict):
        refs_raw = {}
    refs_config = ReferencesConfig(
        instructions=[str(p) for p in refs_raw.get("instructions", []) if isinstance(p, str) and p],
        rules=[str(p) for p in refs_raw.get("rules", []) if isinstance(p, str) and p],
        skills=[str(p) for p in refs_raw.get("skills", []) if isinstance(p, str) and p],
    )

    # Storage config (retention + encryption)
    storage_raw = raw.get("storage", {})
    if not isinstance(storage_raw, dict):
        storage_raw = {}
    try:
        storage_retention_days = max(
            0,
            int(storage_raw.get("retention_days", os.environ.get("AI_CHAT_STORAGE_RETENTION_DAYS", 0))),
        )
    except (ValueError, TypeError):
        storage_retention_days = 0
    try:
        storage_check_interval = max(
            60,
            int(storage_raw.get("retention_check_interval", os.environ.get("AI_CHAT_STORAGE_CHECK_INTERVAL", 3600))),
        )
    except (ValueError, TypeError):
        storage_check_interval = 3600
    storage_purge_attachments = str(
        storage_raw.get("purge_attachments", os.environ.get("AI_CHAT_STORAGE_PURGE_ATTACHMENTS", "true"))
    ).lower() not in ("false", "0", "no")
    storage_purge_embeddings = str(
        storage_raw.get("purge_embeddings", os.environ.get("AI_CHAT_STORAGE_PURGE_EMBEDDINGS", "true"))
    ).lower() not in ("false", "0", "no")
    storage_encrypt = str(
        storage_raw.get("encrypt_at_rest", os.environ.get("AI_CHAT_STORAGE_ENCRYPT", "false"))
    ).lower() in ("true", "1", "yes")
    storage_kdf = str(storage_raw.get("encryption_kdf", "hkdf-sha256"))
    if storage_kdf not in ("hkdf-sha256",):
        storage_kdf = "hkdf-sha256"
    storage_config = StorageConfig(
        retention_days=storage_retention_days,
        retention_check_interval=storage_check_interval,
        purge_attachments=storage_purge_attachments,
        purge_embeddings=storage_purge_embeddings,
        encrypt_at_rest=storage_encrypt,
        encryption_kdf=storage_kdf,
    )

    # Session config
    session_raw = raw.get("session", {})
    if not isinstance(session_raw, dict):
        session_raw = {}
    session_store = str(session_raw.get("store", os.environ.get("AI_CHAT_SESSION_STORE", "memory")))
    if session_store not in ("memory", "sqlite"):
        session_store = "memory"
    try:
        session_max_concurrent = max(
            0,
            int(
                session_raw.get(
                    "max_concurrent_sessions",
                    os.environ.get("AI_CHAT_SESSION_MAX_CONCURRENT", 0),
                )
            ),
        )
    except (ValueError, TypeError):
        session_max_concurrent = 0
    try:
        session_idle_timeout = max(
            0,
            int(
                session_raw.get(
                    "idle_timeout",
                    os.environ.get("AI_CHAT_SESSION_IDLE_TIMEOUT", 1800),
                )
            ),
        )
    except (ValueError, TypeError):
        session_idle_timeout = 1800
    try:
        session_absolute_timeout = max(
            0,
            int(
                session_raw.get(
                    "absolute_timeout",
                    os.environ.get("AI_CHAT_SESSION_ABSOLUTE_TIMEOUT", 43200),
                )
            ),
        )
    except (ValueError, TypeError):
        session_absolute_timeout = 43200
    session_allowed_ips_raw = session_raw.get("allowed_ips", [])
    if not isinstance(session_allowed_ips_raw, list):
        session_allowed_ips_raw = []
    session_allowed_ips = [str(ip) for ip in session_allowed_ips_raw if ip]
    env_allowed_ips = os.environ.get("AI_CHAT_SESSION_ALLOWED_IPS", "")
    if env_allowed_ips and not session_allowed_ips:
        session_allowed_ips = [ip.strip() for ip in env_allowed_ips.split(",") if ip.strip()]
    session_config = SessionConfig(
        store=session_store,
        max_concurrent_sessions=session_max_concurrent,
        idle_timeout=session_idle_timeout,
        absolute_timeout=session_absolute_timeout,
        allowed_ips=session_allowed_ips,
    )

    # Server config
    server_raw = raw.get("server", {})
    if not isinstance(server_raw, dict):
        server_raw = {}
    try:
        server_max_upload_mb = min(
            1000,
            max(
                1,
                int(server_raw.get("max_upload_mb", os.environ.get("AI_CHAT_SERVER_MAX_UPLOAD_MB", 50))),
            ),
        )
    except (ValueError, TypeError):
        server_max_upload_mb = 50
    server_config = ServerConfig(max_upload_mb=server_max_upload_mb)

    # Rate limit config
    rl_raw = raw.get("rate_limit", {})
    if not isinstance(rl_raw, dict):
        rl_raw = {}
    try:
        rl_max_requests = max(
            1,
            int(
                rl_raw.get(
                    "max_requests",
                    os.environ.get("AI_CHAT_RATE_LIMIT_MAX_REQUESTS", 120),
                )
            ),
        )
    except (ValueError, TypeError):
        rl_max_requests = 120
    try:
        rl_window_seconds = max(
            1,
            int(
                rl_raw.get(
                    "window_seconds",
                    os.environ.get("AI_CHAT_RATE_LIMIT_WINDOW_SECONDS", 60),
                )
            ),
        )
    except (ValueError, TypeError):
        rl_window_seconds = 60
    rl_exempt_paths_raw = rl_raw.get("exempt_paths", [])
    if not isinstance(rl_exempt_paths_raw, list):
        rl_exempt_paths_raw = []
    rl_exempt_paths = [str(p) for p in rl_exempt_paths_raw if p]
    env_exempt = os.environ.get("AI_CHAT_RATE_LIMIT_EXEMPT_PATHS", "")
    if env_exempt and not rl_exempt_paths:
        rl_exempt_paths = [p.strip() for p in env_exempt.split(",") if p.strip()]
    if not rl_exempt_paths:
        rl_exempt_paths = ["/api/events"]
    try:
        rl_sse_retry_ms = max(
            100,
            int(
                rl_raw.get(
                    "sse_retry_ms",
                    os.environ.get("AI_CHAT_RATE_LIMIT_SSE_RETRY_MS", 5000),
                )
            ),
        )
    except (ValueError, TypeError):
        rl_sse_retry_ms = 5000
    rate_limit_config = RateLimitConfig(
        max_requests=rl_max_requests,
        window_seconds=rl_window_seconds,
        exempt_paths=rl_exempt_paths,
        sse_retry_ms=rl_sse_retry_ms,
    )

    # Audit config
    audit_raw = raw.get("audit", {})
    if not isinstance(audit_raw, dict):
        audit_raw = {}
    audit_enabled = str(audit_raw.get("enabled", os.environ.get("AI_CHAT_AUDIT_ENABLED", "false"))).lower() in (
        "true",
        "1",
        "yes",
    )
    audit_log_path = str(audit_raw.get("log_path", os.environ.get("AI_CHAT_AUDIT_LOG_PATH", "")))
    audit_tamper = str(audit_raw.get("tamper_protection", os.environ.get("AI_CHAT_AUDIT_TAMPER_PROTECTION", "hmac")))
    if audit_tamper not in ("none", "hmac"):
        audit_tamper = "hmac"
    audit_rotation = str(audit_raw.get("rotation", "daily"))
    if audit_rotation not in ("daily", "size"):
        audit_rotation = "daily"
    try:
        audit_rotate_size = max(1_048_576, int(audit_raw.get("rotate_size_bytes", 10_485_760)))
    except (ValueError, TypeError):
        audit_rotate_size = 10_485_760
    try:
        _raw_retention = audit_raw.get("retention_days", os.environ.get("AI_CHAT_AUDIT_RETENTION_DAYS", 90))
        audit_retention = max(0, int(_raw_retention))
    except (ValueError, TypeError):
        audit_retention = 90
    audit_redact = str(
        audit_raw.get("redact_content", os.environ.get("AI_CHAT_AUDIT_REDACT_CONTENT", "true"))
    ).lower() not in ("false", "0", "no")
    audit_events_raw = audit_raw.get("events", {})
    if not isinstance(audit_events_raw, dict):
        audit_events_raw = {}
    audit_events: dict[str, bool] = {}
    for evt_key in ("auth", "tool_calls", "dlp", "output_filter", "workflow", "memory", "subagent"):
        audit_events[evt_key] = str(audit_events_raw.get(evt_key, "true")).lower() not in ("false", "0", "no")
    audit_config = AuditConfig(
        enabled=audit_enabled,
        log_path=audit_log_path,
        tamper_protection=audit_tamper,
        rotation=audit_rotation,
        rotate_size_bytes=audit_rotate_size,
        retention_days=audit_retention,
        redact_content=audit_redact,
        events=audit_events,
    )

    # Feedback config
    feedback_raw = raw.get("feedback", {})
    if not isinstance(feedback_raw, dict):
        feedback_raw = {}
    feedback_include_history = str(
        feedback_raw.get("include_history_default", os.environ.get("AI_CHAT_FEEDBACK_INCLUDE_HISTORY", "false"))
    ).lower() in ("true", "1", "yes")
    try:
        _raw_fb_hist = feedback_raw.get(
            "max_history_messages", os.environ.get("AI_CHAT_FEEDBACK_MAX_HISTORY_MESSAGES", 10)
        )
        feedback_max_history = max(1, min(50, int(_raw_fb_hist)))
    except (ValueError, TypeError):
        feedback_max_history = 10
    try:
        _raw_fb_retry = feedback_raw.get("retry_attempts", os.environ.get("AI_CHAT_FEEDBACK_RETRY_ATTEMPTS", 2))
        feedback_retry = max(1, min(5, int(_raw_fb_retry)))
    except (ValueError, TypeError):
        feedback_retry = 2
    try:
        _raw_fb_backoff = feedback_raw.get(
            "retry_backoff_seconds", os.environ.get("AI_CHAT_FEEDBACK_RETRY_BACKOFF_SECONDS", 1.0)
        )
        feedback_backoff = max(0.0, min(30.0, float(_raw_fb_backoff)))
    except (ValueError, TypeError):
        feedback_backoff = 1.0
    try:
        _raw_fb_bytes = feedback_raw.get(
            "max_bundle_bytes", os.environ.get("AI_CHAT_FEEDBACK_MAX_BUNDLE_BYTES", 1_000_000)
        )
        feedback_max_bytes = max(10_000, min(5_000_000, int(_raw_fb_bytes)))
    except (ValueError, TypeError):
        feedback_max_bytes = 1_000_000
    feedback_reporters: list[FeedbackReporterConfig] = []
    for r_raw in feedback_raw.get("reporters", []):
        if not isinstance(r_raw, dict):
            continue
        try:
            timeout_val = max(1, min(30, int(r_raw.get("timeout", 10))))
        except (ValueError, TypeError):
            timeout_val = 10
        reporter_name = str(r_raw.get("name", "default")).strip() or "default"
        reporter_type = str(r_raw.get("type", "command")).strip()
        reporter_cmd = str(r_raw.get("command", "")).strip()
        reporter_url = str(r_raw.get("url", "")).strip()
        reporter_enabled = str(r_raw.get("enabled", "true")).lower() not in ("false", "0", "no")
        if reporter_type == "command" and not reporter_cmd:
            logger.warning("feedback reporter %r has type='command' but no command — skipped", reporter_name)
            continue
        if reporter_type == "webhook" and not reporter_url:
            logger.warning("feedback reporter %r has type='webhook' but no url — skipped", reporter_name)
            continue
        feedback_reporters.append(
            FeedbackReporterConfig(
                name=reporter_name,
                type=reporter_type,
                command=reporter_cmd,
                url=reporter_url,
                timeout=timeout_val,
                enabled=reporter_enabled,
            )
        )
    feedback_config = FeedbackConfig(
        reporters=feedback_reporters,
        include_history_default=feedback_include_history,
        max_history_messages=feedback_max_history,
        retry_attempts=feedback_retry,
        retry_backoff_seconds=feedback_backoff,
        max_bundle_bytes=feedback_max_bytes,
    )

    # Memory config (#920 promotion/review pipeline)
    memory_raw = raw.get("memory", {})
    if not isinstance(memory_raw, dict):
        memory_raw = {}
    promotion_raw = memory_raw.get("promotion", {})
    if not isinstance(promotion_raw, dict):
        promotion_raw = {}

    mem_default_review_state = str(
        promotion_raw.get(
            "default_review_state",
            os.environ.get("AI_CHAT_MEMORY_PROMOTION_DEFAULT_REVIEW_STATE", "candidate"),
        )
    )
    if mem_default_review_state not in ("candidate", "pending_review"):
        mem_default_review_state = "candidate"
    mem_local_auto_approve = str(
        promotion_raw.get(
            "local_auto_approve",
            os.environ.get("AI_CHAT_MEMORY_PROMOTION_LOCAL_AUTO_APPROVE", "false"),
        )
    ).lower() in ("true", "1", "yes")
    mem_agent_proposals_enabled = str(
        promotion_raw.get(
            "agent_proposals_enabled",
            os.environ.get("AI_CHAT_MEMORY_PROMOTION_AGENT_PROPOSALS_ENABLED", "true"),
        )
    ).lower() not in ("false", "0", "no")
    try:
        mem_max_lineage_entries = max(
            1,
            int(
                promotion_raw.get(
                    "max_lineage_entries",
                    os.environ.get("AI_CHAT_MEMORY_PROMOTION_MAX_LINEAGE_ENTRIES", 50),
                )
            ),
        )
    except (ValueError, TypeError):
        mem_max_lineage_entries = 50
    try:
        mem_max_candidates_per_conversation = max(
            1,
            int(
                promotion_raw.get(
                    "max_candidates_per_conversation",
                    os.environ.get("AI_CHAT_MEMORY_PROMOTION_MAX_CANDIDATES_PER_CONVERSATION", 10),
                )
            ),
        )
    except (ValueError, TypeError):
        mem_max_candidates_per_conversation = 10
    try:
        mem_max_reject_reason_chars = max(
            1,
            int(
                promotion_raw.get(
                    "max_reject_reason_chars",
                    os.environ.get("AI_CHAT_MEMORY_PROMOTION_MAX_REJECT_REASON_CHARS", 500),
                )
            ),
        )
    except (ValueError, TypeError):
        mem_max_reject_reason_chars = 500
    # Memory retention (#625) policy
    retention_raw = memory_raw.get("retention", {})
    if not isinstance(retention_raw, dict):
        retention_raw = {}

    ret_enabled = str(
        retention_raw.get(
            "enabled",
            os.environ.get("AI_CHAT_MEMORY_RETENTION_ENABLED", "false"),
        )
    ).lower() in ("true", "1", "yes")
    ret_respect_pins = str(
        retention_raw.get(
            "respect_pins",
            os.environ.get("AI_CHAT_MEMORY_RETENTION_RESPECT_PINS", "true"),
        )
    ).lower() not in ("false", "0", "no")

    def _opt_positive_int(
        yaml_val: Any,
        env_name: str,
    ) -> int | None:
        raw_val = yaml_val if yaml_val is not None else os.environ.get(env_name)
        if raw_val is None or raw_val == "":
            return None
        try:
            parsed = int(raw_val)
        except (TypeError, ValueError):
            return None
        return parsed if parsed > 0 else None

    ret_max_age_days = _opt_positive_int(
        retention_raw.get("max_age_days"),
        "AI_CHAT_MEMORY_RETENTION_MAX_AGE_DAYS",
    )
    ret_idle_days = _opt_positive_int(
        retention_raw.get("idle_days"),
        "AI_CHAT_MEMORY_RETENTION_IDLE_DAYS",
    )

    try:
        ret_min_age_days = max(
            0,
            int(
                retention_raw.get(
                    "min_age_days",
                    os.environ.get("AI_CHAT_MEMORY_RETENTION_MIN_AGE_DAYS", 1),
                )
            ),
        )
    except (ValueError, TypeError):
        ret_min_age_days = 1

    # Accept a list from YAML or a comma-separated string from the env.
    _raw_purge_statuses = retention_raw.get(
        "purge_statuses",
        os.environ.get("AI_CHAT_MEMORY_RETENTION_PURGE_STATUSES"),
    )
    if isinstance(_raw_purge_statuses, list):
        _candidates = [str(v).strip() for v in _raw_purge_statuses if str(v).strip()]
    elif isinstance(_raw_purge_statuses, str) and _raw_purge_statuses.strip():
        _candidates = [s.strip() for s in _raw_purge_statuses.split(",") if s.strip()]
    else:
        _candidates = ["rejected"]
    _valid_statuses = {"active", "candidate", "pending_review", "rejected", "archived"}
    ret_purge_statuses = [s for s in _candidates if s in _valid_statuses] or ["rejected"]

    # Memory auto-propose (#1454) — selective extraction of candidate memories
    auto_propose_raw = memory_raw.get("auto_propose", {})
    if not isinstance(auto_propose_raw, dict):
        auto_propose_raw = {}

    ap_enabled = str(
        auto_propose_raw.get(
            "enabled",
            os.environ.get("AI_CHAT_MEMORY_AUTO_PROPOSE_ENABLED", "false"),
        )
    ).lower() in ("true", "1", "yes")
    ap_notify_inline = str(
        auto_propose_raw.get(
            "notify_inline",
            os.environ.get("AI_CHAT_MEMORY_AUTO_PROPOSE_NOTIFY_INLINE", "true"),
        )
    ).lower() not in ("false", "0", "no")
    try:
        ap_max_candidates_per_turn = max(
            1,
            int(
                auto_propose_raw.get(
                    "max_candidates_per_turn",
                    os.environ.get("AI_CHAT_MEMORY_AUTO_PROPOSE_MAX_CANDIDATES_PER_TURN", 1),
                )
            ),
        )
    except (ValueError, TypeError):
        ap_max_candidates_per_turn = 1
    try:
        ap_cooldown_turns = max(
            0,
            int(
                auto_propose_raw.get(
                    "cooldown_turns",
                    os.environ.get("AI_CHAT_MEMORY_AUTO_PROPOSE_COOLDOWN_TURNS", 5),
                )
            ),
        )
    except (ValueError, TypeError):
        ap_cooldown_turns = 5
    try:
        ap_min_confidence = float(
            auto_propose_raw.get(
                "min_confidence",
                os.environ.get("AI_CHAT_MEMORY_AUTO_PROPOSE_MIN_CONFIDENCE", 0.8),
            )
        )
    except (ValueError, TypeError):
        ap_min_confidence = 0.8
    if ap_min_confidence < 0.0:
        ap_min_confidence = 0.0
    elif ap_min_confidence > 1.0:
        ap_min_confidence = 1.0

    _raw_categories = auto_propose_raw.get(
        "categories",
        os.environ.get("AI_CHAT_MEMORY_AUTO_PROPOSE_CATEGORIES"),
    )
    _default_categories = ["preference", "project_fact", "decision", "workflow_hint"]
    if isinstance(_raw_categories, list):
        _ap_candidates = [str(v).strip() for v in _raw_categories if str(v).strip()]
    elif isinstance(_raw_categories, str) and _raw_categories.strip():
        _ap_candidates = [s.strip() for s in _raw_categories.split(",") if s.strip()]
    else:
        _ap_candidates = list(_default_categories)
    _valid_ap_categories = {"preference", "project_fact", "decision", "workflow_hint"}
    ap_categories = [c for c in _ap_candidates if c in _valid_ap_categories] or list(_default_categories)

    memory_config = MemoryConfig(
        promotion=MemoryPromotionConfig(
            default_review_state=mem_default_review_state,
            local_auto_approve=mem_local_auto_approve,
            agent_proposals_enabled=mem_agent_proposals_enabled,
            max_lineage_entries=mem_max_lineage_entries,
            max_candidates_per_conversation=mem_max_candidates_per_conversation,
            max_reject_reason_chars=mem_max_reject_reason_chars,
        ),
        retention=MemoryRetentionConfig(
            enabled=ret_enabled,
            max_age_days=ret_max_age_days,
            idle_days=ret_idle_days,
            min_age_days=ret_min_age_days,
            purge_statuses=ret_purge_statuses,
            respect_pins=ret_respect_pins,
        ),
        auto_propose=MemoryAutoProposeConfig(
            enabled=ap_enabled,
            max_candidates_per_turn=ap_max_candidates_per_turn,
            categories=ap_categories,
            min_confidence=ap_min_confidence,
            notify_inline=ap_notify_inline,
            cooldown_turns=ap_cooldown_turns,
        ),
    )

    # Codebase index config
    ci_raw = raw.get("codebase_index", {})
    if not isinstance(ci_raw, dict):
        ci_raw = {}
    ci_enabled = str(ci_raw.get("enabled", "true")).lower() not in ("false", "0", "no")
    ci_map_tokens = int(ci_raw.get("map_tokens", 1000))
    ci_languages = ci_raw.get("languages", [])
    if not isinstance(ci_languages, list):
        ci_languages = []
    ci_exclude_raw = ci_raw.get("exclude_dirs")
    ci_config = CodebaseIndexConfig(
        enabled=ci_enabled,
        map_tokens=ci_map_tokens,
        languages=[str(lang) for lang in ci_languages],
    )
    if ci_exclude_raw is not None and isinstance(ci_exclude_raw, list):
        ci_config.exclude_dirs = [str(d) for d in ci_exclude_raw]

    # Compliance rules config
    compliance_raw = raw.get("compliance", {})
    if not isinstance(compliance_raw, dict):
        compliance_raw = {}
    compliance_rules: list[ComplianceRule] = []
    for rule_raw in compliance_raw.get("rules", []):
        if not isinstance(rule_raw, dict):
            continue
        rule_field = str(rule_raw.get("field", ""))
        if not rule_field:
            continue
        must_match_str = str(rule_raw.get("must_match", ""))
        compiled = None
        if must_match_str:
            try:
                compiled = re.compile(must_match_str)
            except re.error:
                compiled = None  # invalid pattern handled at evaluation time
        compliance_rules.append(
            ComplianceRule(
                field=rule_field,
                message=str(rule_raw.get("message", "")),
                must_be=rule_raw.get("must_be", _UNSET),
                must_not_be=rule_raw.get("must_not_be", _UNSET),
                must_match=must_match_str,
                must_not_be_empty=bool(rule_raw.get("must_not_be_empty", False)),
                must_contain=rule_raw.get("must_contain", _UNSET),
                _compiled_pattern=compiled,
            )
        )
    compliance_config = ComplianceConfig(rules=compliance_rules)

    # --- Workflow config -------------------------------------------------------
    workflow_raw = raw.get("workflow", {})
    if not isinstance(workflow_raw, dict):
        workflow_raw = {}
    budget_raw = workflow_raw.get("budget", {})
    if not isinstance(budget_raw, dict):
        budget_raw = {}
    try:
        budget_max_dur = max(0, int(budget_raw.get("max_duration_seconds", 0)))
    except (ValueError, TypeError):
        budget_max_dur = 0
    try:
        budget_max_steps = max(0, int(budget_raw.get("max_steps", 0)))
    except (ValueError, TypeError):
        budget_max_steps = 0
    try:
        budget_max_tokens = max(0, int(budget_raw.get("max_tokens", 0)))
    except (ValueError, TypeError):
        budget_max_tokens = 0
    workflow_budget = WorkflowBudgetConfig(
        max_duration_seconds=budget_max_dur,
        max_steps=budget_max_steps,
        max_tokens=budget_max_tokens,
    )
    workflow_kwargs: dict[str, Any] = {"budget": workflow_budget}
    workflow_defaults = WorkflowConfig()
    for wf_key in (
        "enabled",
        "approval_mode",
        "max_review_rounds",
        "max_iterations",
        "step_timeout",
        "heartbeat_interval",
        "stale_threshold",
        "approval_timeout",
        "registry_enabled",
        "registry_heartbeat_interval",
        "executor_enabled",
        "executor_poll_interval",
        "max_concurrent_runs",
        "scheduler_enabled",
        "min_schedule_interval",
        "watch_buffer_lines",
        "lock_reclaim_threshold",
    ):
        wf_default = getattr(workflow_defaults, wf_key)
        val = workflow_raw.get(wf_key, wf_default)
        if isinstance(wf_default, bool):
            if isinstance(val, bool):
                workflow_kwargs[wf_key] = val
            else:
                workflow_kwargs[wf_key] = str(val).lower() in ("true", "1", "yes")
        elif isinstance(wf_default, str):
            workflow_kwargs[wf_key] = str(val).strip()
        elif isinstance(wf_default, int):
            try:
                workflow_kwargs[wf_key] = int(val)
            except (ValueError, TypeError):
                workflow_kwargs[wf_key] = wf_default
    # Parse workflow credentials
    creds_raw = workflow_raw.get("credentials", [])
    if not isinstance(creds_raw, list):
        creds_raw = []
    workflow_creds: list[WorkflowCredentialConfig] = []
    for cred_entry in creds_raw:
        if not isinstance(cred_entry, dict):
            continue
        cred_name = str(cred_entry.get("name", "")).strip()
        if not cred_name:
            continue
        workflow_creds.append(
            WorkflowCredentialConfig(
                name=cred_name,
                env_var=cred_entry.get("env_var"),
                command=cred_entry.get("command"),
                allowed_runners=cred_entry.get("allowed_runners"),
            )
        )
    workflow_kwargs["credentials"] = workflow_creds
    # Parse workflow.transcript.*
    transcript_raw = workflow_raw.get("transcript", {})
    if isinstance(transcript_raw, dict):
        tc_defaults = TranscriptConfig()
        tc_kwargs: dict[str, Any] = {}
        _tc_fields = ("enabled", "max_assistant_chars", "max_tool_output_chars", "max_stdout_chars", "max_stderr_chars")
        for tc_key in _tc_fields:
            if tc_key in transcript_raw:
                val = transcript_raw[tc_key]
                tc_default = getattr(tc_defaults, tc_key)
                if isinstance(tc_default, bool):
                    tc_kwargs[tc_key] = val if isinstance(val, bool) else str(val).lower() in ("true", "1", "yes")
                elif isinstance(tc_default, int):
                    try:
                        tc_kwargs[tc_key] = int(val)
                    except (ValueError, TypeError):
                        tc_kwargs[tc_key] = tc_default
        workflow_kwargs["transcript"] = TranscriptConfig(**tc_kwargs)
    workflow_config = WorkflowConfig(**workflow_kwargs)

    # Trusted proxy config
    tp_raw = raw.get("trusted_proxy", {})
    if not isinstance(tp_raw, dict):
        tp_raw = {}
    tp_enabled_raw = tp_raw.get("enabled", os.environ.get("AI_CHAT_TRUSTED_PROXY_ENABLED", "false"))
    tp_enabled = str(tp_enabled_raw).lower() in ("true", "1", "yes")
    tp_cidrs_raw = tp_raw.get("trusted_cidrs", [])
    if not isinstance(tp_cidrs_raw, list):
        tp_cidrs_raw = []
    tp_cidrs = [str(c).strip() for c in tp_cidrs_raw if c]
    env_cidrs = os.environ.get("AI_CHAT_TRUSTED_PROXY_CIDRS", "")
    if env_cidrs and not tp_cidrs:
        tp_cidrs = [c.strip() for c in env_cidrs.split(",") if c.strip()]
    tp_header = str(tp_raw.get("header", os.environ.get("AI_CHAT_TRUSTED_PROXY_HEADER", "X-Forwarded-For")))
    if not tp_header.strip():
        tp_header = "X-Forwarded-For"
    # Validate CIDRs at parse time -- fail closed on invalid entries
    import ipaddress as _ipaddress

    for cidr_entry in tp_cidrs:
        try:
            _ipaddress.ip_network(cidr_entry, strict=False)
        except ValueError:
            raise ValueError(
                f"Invalid CIDR in trusted_proxy.trusted_cidrs: {cidr_entry!r}. "
                "Each entry must be a valid IPv4 or IPv6 CIDR (e.g. '10.0.0.0/8')."
            )
    trusted_proxy_config = TrustedProxyConfig(
        enabled=tp_enabled,
        trusted_cidrs=tp_cidrs,
        header=tp_header,
    )

    # Build a "trusted" hooks view from the pre-merge personal snapshot
    # plus any team-contributed hooks.  Pack hooks are intentionally
    # excluded here — they are passed separately as ``pack_raw`` so the
    # parser can tag them with ``trust_source="pack"`` and the runtime
    # can hold them non-executable until trust verification ships (#1272).
    #
    # Team hooks merge UNDER personal (personal wins on id collision) so
    # that operators retain the final word on hook behaviour.  ``deep_merge``
    # would REPLACE the hook list wholesale (it is a plain list of dicts,
    # not a name-keyed list), silently dropping team hooks with unique ids
    # Pass per-layer views so each hook entry retains its correct
    # trust_source ("personal" vs "team") rather than being collapsed
    # into a single trusted blob.  This is required to freeze the schema
    # contract for #1271 (runtime dispatch honours trust_source).
    hooks_config = _build_hooks_config(
        raw,
        pack_raw=pack_config if isinstance(pack_config, dict) else None,
        personal_raw=personal_raw_snapshot if isinstance(personal_raw_snapshot, dict) else None,
        team_raw=team_raw if isinstance(team_raw, dict) else None,
    )

    pack_sources_raw = raw.get("pack_sources", [])
    if not isinstance(pack_sources_raw, list):
        pack_sources_raw = []
    pack_sources_list: list[PackSourceConfig] = []
    for src in pack_sources_raw:
        if not isinstance(src, dict):
            continue
        url = str(src.get("url", "")).strip()
        if not url:
            continue
        try:
            refresh = int(src.get("refresh_interval", 30))
        except (ValueError, TypeError):
            refresh = 30
        auto_attach_raw = src.get("auto_attach", True)
        if auto_attach_raw is None:
            auto_attach = True
        elif isinstance(auto_attach_raw, bool):
            auto_attach = auto_attach_raw
        else:
            auto_attach = str(auto_attach_raw).lower() in ("true", "1", "yes")
        try:
            priority = int(src.get("priority", 50))
        except (ValueError, TypeError):
            priority = 50
        pack_sources_list.append(
            PackSourceConfig(
                url=url,
                branch=str(src.get("branch", "main")),
                refresh_interval=refresh,
                auto_attach=auto_attach,
                priority=priority,
            )
        )
    project_raw = raw.get("project", {})
    if not isinstance(project_raw, dict):
        project_raw = {}
    project_config = build_project_config(project_raw)

    return (
        AppConfig(
            ai=ai,
            app=app_settings,
            project=project_config,
            mcp_servers=mcp_servers,
            mcp_tool_warning_threshold=mcp_tool_warning_threshold,
            shared_databases=shared_databases,
            cli=cli_config,
            compaction=compaction_config,
            identity=identity,
            embeddings=embeddings_config,
            safety=safety_config,
            proxy=proxy_config,
            rag=rag_config,
            reranker=reranker_config,
            memory_recall=memory_recall_config,
            references=refs_config,
            codebase_index=ci_config,
            storage=storage_config,
            session=session_config,
            rate_limit=rate_limit_config,
            server=server_config,
            audit=audit_config,
            memory=memory_config,
            compliance=compliance_config,
            trusted_proxy=trusted_proxy_config,
            workflow=workflow_config,
            pack_sources=pack_sources_list,
            hooks=hooks_config,
            feedback=feedback_config,
        ),
        enforced_fields,
    )


def ensure_identity(config_path: Path | None = None) -> UserIdentity:
    """Ensure config has an identity section; auto-generate if missing.

    Returns the UserIdentity (existing or newly created).
    """
    import getpass

    import yaml

    from .identity import generate_identity

    path = config_path or _get_config_path()
    raw: dict[str, Any] = {}
    if path.exists():
        with open(path, encoding="utf-8-sig") as f:
            raw = yaml.safe_load(f) or {}

    identity_raw = raw.get("identity", {})
    if identity_raw.get("user_id") and identity_raw.get("private_key"):
        return UserIdentity(
            user_id=identity_raw["user_id"],
            display_name=identity_raw.get("display_name", ""),
            public_key=identity_raw.get("public_key", ""),
            private_key=identity_raw.get("private_key", ""),
        )

    # Partial identity (user_id but no private_key) — repair by generating keypair
    if identity_raw.get("user_id") and not identity_raw.get("private_key"):
        from .identity import generate_identity

        fresh = generate_identity(identity_raw.get("display_name", ""))
        identity_raw["private_key"] = fresh["private_key"]
        identity_raw["public_key"] = fresh["public_key"]
        raw["identity"] = identity_raw

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(raw, f, default_flow_style=False, sort_keys=False)
        try:
            path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass

        return UserIdentity(
            user_id=identity_raw["user_id"],
            display_name=identity_raw.get("display_name", ""),
            public_key=identity_raw["public_key"],
            private_key=identity_raw["private_key"],
        )

    try:
        display_name = getpass.getuser()
    except Exception:
        display_name = "user"

    identity_data = generate_identity(display_name)
    raw["identity"] = identity_data

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(raw, f, default_flow_style=False, sort_keys=False)
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass

    return UserIdentity(
        user_id=identity_data["user_id"],
        display_name=identity_data["display_name"],
        public_key=identity_data["public_key"],
        private_key=identity_data["private_key"],
    )


_SAFE_TOOL_NAME_RE = re.compile(r"^[a-zA-Z0-9_\-]{1,128}$")


def write_allowed_tool(tool_name: str, config_path: Path | None = None) -> None:
    """Append a tool name to safety.allowed_tools in the config file.

    Preserves existing config structure. Creates the safety section if missing.
    Uses advisory file locking to prevent concurrent writes from corrupting the file.
    """
    try:
        import fcntl

        _has_fcntl = True
    except ImportError:
        _has_fcntl = False

    if not _SAFE_TOOL_NAME_RE.match(tool_name):
        raise ValueError(f"Invalid tool name format: {tool_name!r}")

    path = config_path or _get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    def _read_modify_write() -> None:
        raw: dict[str, Any] = {}
        if path.exists():
            with open(path, encoding="utf-8-sig") as f:
                raw = yaml.safe_load(f) or {}

        safety_section = raw.setdefault("safety", {})
        allowed = safety_section.setdefault("allowed_tools", [])
        if not isinstance(allowed, list):
            allowed = []
            safety_section["allowed_tools"] = allowed

        if tool_name not in allowed:
            allowed.append(tool_name)

            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(raw, f, default_flow_style=False, sort_keys=False)
            try:
                path.chmod(stat.S_IRUSR | stat.S_IWUSR)
            except OSError:
                pass

    if _has_fcntl:
        lock_path = path.with_suffix(".lock")
        with open(lock_path, "w") as lock_f:
            fcntl.flock(lock_f, fcntl.LOCK_EX)
            try:
                _read_modify_write()
            finally:
                fcntl.flock(lock_f, fcntl.LOCK_UN)
    else:
        _read_modify_write()
