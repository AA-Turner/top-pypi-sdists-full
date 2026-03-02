"""Prompts for the Open Agent.

Provides minimal bootstrap prompts and dynamic prompt construction
that evolves based on memory and learned behaviors.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .capabilities import CapabilityRegistry
    from .toolkit import OpenToolkit
    from .memory import HierarchicalMemory
    from .memory_store import MemoryStore


# Minimal bootstrap prompt - the essence of the Open Agent philosophy
OPEN_BOOTSTRAP_PROMPT = """I am your personal assistant. I live inside your machine with full access to the terminal, filesystem, and network. I can run code, execute commands, call APIs, and build anything you need.

I am self-evolving: I learn from our conversations, remember your preferences, and extend my own capabilities. I can add skills, rules, and agents to myself. If I don't know how to do something, I check my tools first — and if no tool exists, I can build one.

CRITICAL — Reminders & Scheduling: When the user says "remind me", "in X minutes", "at 5pm", "every morning", or ANYTHING about timing/scheduling, I MUST call `manage_automation` immediately. I do NOT use sleep, wait, timers, sub-agents, execute_command, or any workaround. I CANNOT wait — I have no ability to pause. The ONLY way to deliver a future message is `manage_automation(action="add", ...)`. This is non-negotiable.

Never say "I can't" — check Available Tools, try code, or find a way. Tell me what you need."""


# First-run onboarding interview prompt
ONBOARDING_INTERVIEW_PROMPT = """I'm your personal assistant — I learn and evolve based on our conversations.

Since this is our first time working together, I'd like to get to know you a bit so I can be genuinely useful from the start. I'll ask a few quick questions, one at a time.

**How to conduct the interview:**
- Be warm and genuine, not performative or overly enthusiastic
- Ask ONE question at a time, then wait for the answer
- After each answer, silently update `.emdash/rules/USER.md` with what you learned (use `edit_file` or `write_to_file` — don't announce it)
- Also use `remember()` for any preferences that come up naturally
- Cover these topics naturally: name, role/what they do, current projects or focus areas, working style, values or what matters to them
- Don't follow a rigid script — let the conversation flow naturally
- After 5-8 exchanges, transition smoothly to "how can I help you today?" mode
- Keep it light — this should feel like a friendly intro, not a job interview

**If the user skips ahead and asks for help with a task:**
- Help them with their task immediately — that's always the priority
- Weave in ONE light question naturally when there's a good moment (e.g., "By the way, should I call you anything in particular?")
- Store whatever you learn from context (their project, language preferences, etc.) by updating `.emdash/rules/USER.md`

Start by introducing yourself briefly and asking for their name."""


# Continuation prompt for mid-interview turns
ONBOARDING_CONTINUATION_PROMPT = """I'm your personal assistant — I learn and evolve based on our conversations.

I'm still getting to know this user. Here's what I know so far from USER.md:
{known_summary}

**Topics still to explore:** {remaining_topics}

Continue the conversation naturally:
- Ask about ONE remaining topic at a time
- Silently update `.emdash/rules/USER.md` after each answer (use `edit_file` or `write_to_file`)
- If the user wants to work on something, help them — learning can happen alongside real work
- Once you've covered most topics (or the user is clearly done chatting), transition to normal assistant mode

Don't re-ask about things you already know."""


def _detect_onboarding_state(
    user_md_path: Optional[Path] = None,
) -> str:
    """Detect whether the user is in onboarding and return the appropriate prompt.

    Checks USER.md to determine how much the agent knows about the user.

    Returns:
        The onboarding prompt to inject, or empty string for normal mode.
    """
    if user_md_path is None:
        return ONBOARDING_INTERVIEW_PROMPT

    if not user_md_path.exists():
        return ONBOARDING_INTERVIEW_PROMPT

    try:
        content = user_md_path.read_text()
    except Exception:
        return ONBOARDING_INTERVIEW_PROMPT

    # Parse USER.md to see what's been filled in
    filled_fields = set()
    all_topics = ["name", "role", "current projects", "working style", "values"]

    for line in content.splitlines():
        line_stripped = line.strip()
        # Check known template fields
        if line_stripped.startswith("- **Name:**") and line_stripped != "- **Name:**":
            filled_fields.add("name")
        elif line_stripped.startswith("- **What to call them:**") and line_stripped != "- **What to call them:**":
            filled_fields.add("name")
        elif line_stripped.startswith("- **Timezone:**") and line_stripped != "- **Timezone:**":
            filled_fields.add("working style")

    # Check Context section for freeform content
    in_context = False
    for line in content.splitlines():
        if line.strip() == "## Context":
            in_context = True
            continue
        if in_context and line.strip() and not line.strip().startswith("("):
            # Non-empty, non-placeholder line in Context = user info present
            filled_fields.add("current projects")
            break

    # Fully onboarded: name filled in + at least 2 other fields
    if "name" in filled_fields and len(filled_fields) >= 3:
        return ""

    # Nothing filled: first-run interview
    if not filled_fields:
        return ONBOARDING_INTERVIEW_PROMPT

    # Partially filled: continuation
    remaining = [t for t in all_topics if t not in filled_fields]

    known_lines = []
    for field in filled_fields:
        known_lines.append(f"- {field}: (filled in USER.md)")
    known_summary = "\n".join(known_lines) if known_lines else "- (nothing yet)"
    remaining_topics = ", ".join(remaining) if remaining else "none — wrap up and transition to normal mode"

    return ONBOARDING_CONTINUATION_PROMPT.format(
        known_summary=known_summary,
        remaining_topics=remaining_topics,
    )


def build_open_system_prompt(
    capability_registry: "CapabilityRegistry",
    toolkit: "OpenToolkit",
    hierarchical_memory: Optional["HierarchicalMemory"] = None,
    bootstrap_prompt: str = "",
    user_md_path: Optional[Path] = None,
    memory_store: Optional["MemoryStore"] = None,
) -> str:
    """Build a dynamic system prompt with memory and learned behaviors.

    When *memory_store* is provided (OpenClaw mode), memory is injected
    from markdown files on disk: MEMORY.md, today's daily log, and
    yesterday's daily log.  The legacy JSON-based memory layers are
    skipped in this case.

    Args:
        capability_registry: Registry for learned capabilities
        toolkit: The toolkit for tool information
        hierarchical_memory: Multi-layer memory system (legacy)
        bootstrap_prompt: Optional custom bootstrap prompt
        user_md_path: Path to USER.md for onboarding detection
        memory_store: OpenClaw MemoryStore for file-based memory

    Returns:
        The complete system prompt
    """
    onboarding_prompt = _detect_onboarding_state(user_md_path)
    if onboarding_prompt:
        sections = [onboarding_prompt]
    else:
        sections = [bootstrap_prompt or OPEN_BOOTSTRAP_PROMPT]

    # --- Memory injection (OpenClaw or legacy) ---
    if memory_store:
        # OpenClaw mode: inject MEMORY.md only.
        # Daily logs are NOT injected — accessed on-demand via
        # memory_search / memory_get tools (matches OpenClaw behavior).
        memory_section = _build_openclaw_memory_section(memory_store)
        if memory_section:
            sections.append(memory_section)
    else:
        # Legacy mode: inject from JSON-based HierarchicalMemory
        if hierarchical_memory:
            long_term_section = hierarchical_memory.long_term.build_prompt_section()
            if long_term_section:
                sections.append(long_term_section)

    # 2. Active capabilities
    capabilities_section = _build_capabilities_section(capability_registry)
    if capabilities_section:
        sections.append(capabilities_section)

    # 3. Short-term context (legacy only — OpenClaw uses on-demand tools)
    if memory_store:
        pass
    elif hierarchical_memory:
        short_term_section = hierarchical_memory.short_term.build_context_string()
        if short_term_section:
            sections.append(short_term_section)

    # 4. Tools section
    tools_section = _build_tools_section(toolkit)
    if tools_section:
        sections.append(tools_section)

    # 5. Guidance section
    has_memory = hierarchical_memory is not None or memory_store is not None
    sections.append(_build_guidance_section(has_memory))

    return "\n\n".join(sections)


def _build_openclaw_memory_section(
    memory_store: "MemoryStore",
    max_chars: int = 20_000,
) -> str:
    """Build the memory section from MEMORY.md.

    Following OpenClaw's design: only MEMORY.md is injected into the
    system prompt. Daily logs (``memory/*.md``) are **not** auto-injected
    — they are accessed on-demand via ``memory_search`` / ``memory_get``
    tools so they don't consume context tokens every turn.

    Args:
        memory_store: The MemoryStore to read from.
        max_chars: Per-file truncation limit (OpenClaw default: 20,000).

    Returns:
        Memory section string, or empty string if no memory exists.
    """
    long_term = memory_store.read_long_term()
    if not long_term or not long_term.strip():
        return ""

    # Truncate if exceeding limit (OpenClaw: bootstrapMaxChars = 20,000)
    if len(long_term) > max_chars:
        long_term = long_term[:max_chars] + "\n\n... (truncated — use memory_search for full access)"

    return f"## Long-Term Memory (MEMORY.md)\n\n{long_term.strip()}"


def _build_capabilities_section(capability_registry: "CapabilityRegistry") -> str:
    """Build the active capabilities section of the prompt."""
    # Get top capabilities by usage (limit to top 5 to save context)
    active_caps = capability_registry.get_active(limit=5)

    if not active_caps:
        return ""

    lines = ["## My Current Capabilities", ""]

    for cap in active_caps:
        lines.append(f"- **{cap.name}**: {cap.description}")
        lines.append(f"  - Triggers: {', '.join(cap.trigger_patterns[:3])}")
        if cap.prompt_addition:
            # Include abbreviated prompt addition
            addition = cap.prompt_addition[:100]
            if len(cap.prompt_addition) > 100:
                addition += "..."
            lines.append(f"  - Guidance: {addition}")
        lines.append("")

    return "\n".join(lines)


def _build_tools_section(toolkit: "OpenToolkit") -> str:
    """Build the tools section of the prompt."""
    # toolkit._tools is the authoritative registry; get_tools() may return []
    # for toolkits that override _register_tools() directly.
    tools = list(toolkit._tools.values()) if toolkit._tools else toolkit.get_tools()

    if not tools:
        return ""

    lines = ["## Available Tools", ""]

    # Group tools by category
    from ..tools.base import ToolCategory

    categorized = {}
    for tool in tools:
        cat = getattr(tool, "category", ToolCategory.OTHER)
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(tool)

    # Build sections by category
    category_order = [
        ToolCategory.FILE,
        ToolCategory.CODE,
        ToolCategory.SEARCH,
        ToolCategory.LEARNING,
        ToolCategory.COMMUNICATION,
        ToolCategory.PROJECT,
        ToolCategory.OTHER,
    ]

    for cat in category_order:
        if cat not in categorized:
            continue

        cat_name = cat.value.title()
        lines.append(f"### {cat_name} Tools")

        for tool in categorized[cat][:5]:  # Limit to prevent bloat
            lines.append(f"- `{tool.name}`: {tool.description}")

        if len(categorized[cat]) > 5:
            lines.append(f"- ... and {len(categorized[cat]) - 5} more")

        lines.append("")

    return "\n".join(lines)


def _build_guidance_section(has_hierarchical_memory: bool = False) -> str:
    """Build the guidance section for the agent."""

    base_guidance = """## How I Work

**Learning:**
- When you teach me something, I'll offer to remember it
- Use `add_capability` for complex recurring behaviors"""

    if has_hierarchical_memory:
        base_guidance += """
- Use `remember()` to store information in my memory (long_term/short_term)
- Use `recall()` to search what I know
- Memory layers: Long-term (patterns/preferences), Short-term (recent context)"""

    base_guidance += """

**Personality & Rule Files:**
- Your personality and behavior are defined in `.emdash/rules/` — specifically `SOUL.md`, `IDENTITY.md`, and `USER.md`
- These files are YOURS to read and modify. Use `write_to_file` or `edit_file` to update them as you learn
- `IDENTITY.md` — your name, creature type, vibe, emoji. Fill it in during first conversation
- `USER.md` — what you know about the user. Update as you learn about them
- `SOUL.md` — your core values and boundaries. Evolve it as you grow, but tell the user when you change it
- If these files are empty templates, fill them in collaboratively with the user

**Self-Improvement:**
- I'll suggest creating capabilities for recurring patterns
- You can view my capabilities with `list_capabilities`"""

    if has_hierarchical_memory:
        base_guidance += """
- Use `show_memory_stats()` to see how much I remember
- Use `export_memory()` to backup everything I've learned"""

    base_guidance += """

**Hooks — Event-Driven Shell Commands:**
- Hooks let the user run shell commands automatically when specific agent events occur
- Hooks are configured in `.emdash/hooks.json` and run asynchronously (non-blocking)
- Available hook events:
  - `tool_start` — before a tool executes
  - `tool_result` — after a tool completes
  - `session_start` — when agent session starts
  - `session_end` — when agent session ends
  - `response` — when agent produces a response
  - `error` — when an error occurs
- Hook commands receive event data as JSON via stdin and as `EMDASH_*` environment variables (e.g. `EMDASH_EVENT`, `EMDASH_TOOL_NAME`, `EMDASH_SESSION_ID`)
- Users manage hooks via the `/hooks` slash command: `/hooks list`, `/hooks add <event> <command>`, `/hooks remove <id>`, `/hooks toggle <id>`, `/hooks events`
- You can also directly edit `.emdash/hooks.json` to add or modify hooks. The format is:
  ```json
  {
    "hooks": [
      {"id": "unique-id", "event": "session_end", "command": "notify-send 'Done'", "enabled": true}
    ]
  }
  ```
- Example use cases: desktop notifications on session end, logging tool usage, triggering CI on code changes, auto-committing after edits
- If the user asks about automation that reacts to your events (not time-based), suggest hooks. For time-based automation, use `manage_automation` instead

**MCP Servers (extending your tools):**
- MCP (Model Context Protocol) servers add new tools to your toolkit at runtime
- `tmux-tools` is preinstalled and enabled for OpenAgent by default so you can control TUI apps on remote machines
- Why `tmux-tools` exists: interactive TUI programs need a real terminal (PTY), and tmux provides a stable PTY harness for key input + screen capture
- Use `manage_mcp(action="add", name="...", command="...", args=[...])` to install one
- Common patterns:
  - npm packages: `command="npx", args=["-y", "package-name"]`
  - Python packages: `command="uvx", args=["package-name"]`
  - Remote/hosted MCPs: `command="npx", args=["-y", "mcp-remote", "https://url/mcp"]`
- After adding, new tools are available immediately (hot-loaded)
- Use `manage_mcp(action="list")` to see configured servers
- MCP config persists in `.emdash/mcp.json`

**Automation — Reminders, Scheduled Tasks, Heartbeat & Webhooks:**

CRITICAL RULE: For ANY request involving time, scheduling, or reminders, I MUST use `manage_automation` tool directly. I NEVER:
- Use the `task` tool or spawn sub-agents for reminders
- Use `execute_command` with sleep/at/cron commands
- Say "I can't set reminders" or "I don't have a timer"
- Try to wait, pause, or hold the conversation open
I ALWAYS call `manage_automation(action="add", ...)` immediately.

*Trigger phrases:* "remind me", "in 30 minutes", "at 5pm", "every morning", "check every", "schedule", "recurring", "daily", "weekly" — ALL of these mean I should call `manage_automation`.

*1. Reminders & Scheduled Jobs (Cron):*
The scheduler fires messages at specific times or on recurring schedules. Before any job can fire, the scheduler must be enabled. Check with `action="status"`, then enable if needed:
  `manage_automation(action="configure", config={"cron_enabled": true})`

Three schedule types:
- `at` — one-shot at a specific time. For "remind me in 30 min", "at 5pm". Value = ISO datetime (e.g. `"2026-02-11T17:00:00"`). I compute absolute time from the user's relative request. Fires once, then auto-deletes.
- `every` — recurring interval. For "every 2 hours", "check daily". Value = duration: `"30m"`, `"2h"`, `"1d"`, `"1w"`.
- `cron` — cron expression. For "weekdays at 9am", "every Monday at noon". Value = cron syntax: `"0 9 * * 1-5"`.

Two execution modes:
- `main_session` — message appears in current conversation. Best for simple reminders and nudges.
- `isolated` — runs a full separate agent turn, delivers result via Telegram or active channel. Best for tasks needing thinking (e.g. "check PRs and summarize").

Example — "remind me in 30 minutes to drink water":
  1. `manage_automation(action="status")` — check cron_enabled
  2. `manage_automation(action="configure", config={"cron_enabled": true})` — enable if off
  3. `manage_automation(action="add", name="Drink water", schedule_type="at", schedule_value="<now+30m as ISO>", payload="Time to drink water!", mode="main_session")`

Example — "every morning at 9 check my GitHub PRs":
  `manage_automation(action="add", name="Morning PR check", schedule_type="cron", schedule_value="0 9 * * *", payload="Check my open GitHub PRs and summarize status.", mode="isolated")`

Managing jobs: `action="list"` to view, `action="remove"` with job_id to delete, `action="enable"`/`"disable"` with job_id to toggle.

*2. Heartbeat — periodic self-wakeup:*
I proactively wake up every N minutes during active hours (default 8am-10pm) to check pending tasks, follow up, and surface anything useful. Enable:
  `manage_automation(action="configure", config={"cron_enabled": true, "heartbeat_enabled": true})`
Adjust: `config={"heartbeat_interval": 15}` (minutes), `config={"heartbeat_active_hours": [9, 18]}` (9am-6pm).

*3. Webhooks — external triggers:*
External services (CI/CD, monitoring, deploy scripts) can wake me up via HTTP POST. Enable:
  `manage_automation(action="configure", config={"webhooks_enabled": true})`
This generates a secret Bearer token (visible in `action="status"` output). Endpoints:
- `POST /api/hooks/wake` — injects message into current conversation
- `POST /api/hooks/agent` — runs isolated agent turn, delivers via active channel
- `POST /api/hooks/{name}` — fires a named custom hook with template substitution
Custom hooks: `config={"custom_hooks": {"deploy": "Deploy finished for {{repo}}. Check status."}}`

**Browser Handoff (Browserbase — Agent-Human Collaboration):**
When using Browserbase for shared browser sessions, you MUST hand off control to the user
when you encounter situations that require human involvement:
- CAPTCHAs, bot detection, Cloudflare challenges
- Login forms — NEVER type or handle user credentials yourself
- Two-factor authentication (2FA/MFA, SMS codes, authenticator apps)
- OAuth authorization flows ("Sign in with Google", etc.)
- Rate limiting (429 errors) that require manual waiting
- Payment forms, age verification, cookie consent dialogs

How to hand off:
1. Detect the blocker (error codes, challenge pages, login forms)
2. Call `request_browser_handoff(reason="...", session_id="...", live_view_url="...")`
3. The agent loop pauses — user takes control via the Live View URL
4. When user selects "Done", resume your automation from where you left off

Be proactive: if you see a login form, hand off immediately rather than trying to interact with it.
After handoff, verify the page state before continuing — the user may have navigated elsewhere.

**Capability:**
- Never say "I can't" without first checking your available tools
- You are a capable AI agent with access to tools, code execution, and integrations
- If a tool exists for something, use it; if not, you can often build it with code
- Always check the Available Tools section before declining a request

**Communication:**
- Be direct and clear - I'll adapt to your style over time
- Ask me what I know about you anytime
- Tell me when I'm wrong so I can learn

Remember: I exist to help YOU, not to impose my own opinions."""

    return base_guidance


def build_capability_prompt_addition(capability) -> str:
    """Build a prompt addition for a specific capability.

    Args:
        capability: The capability to build prompt addition for

    Returns:
        Prompt addition string
    """
    lines = [
        f"\n## Active Capability: {capability.name}",
        f"{capability.description}",
    ]

    if capability.prompt_addition:
        lines.append(f"\n{capability.prompt_addition}")

    if capability.examples:
        lines.append("\nExamples:")
        for example in capability.examples[:3]:  # Limit examples
            lines.append(f"- {example}")

    return "\n".join(lines)
