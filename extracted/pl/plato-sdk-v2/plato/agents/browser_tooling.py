"""Shared instruction block + shell setup for ``agent-browser`` tooling.

Agent packages (claude-code, gemini-cli, codex) opt in by setting
``AgentConfig.browser_tooling = True``; the base ``BaseAgent`` reads the flag
and splices the block into the effective system prompt plus prepends the bun
bin to ``PATH`` so the ``agent-browser`` CLI resolves in the agent subshell.
"""

from __future__ import annotations

AGENT_BROWSER_PATH_EXPORT = 'export PATH="$HOME/.bun/bin:$PATH"'
"""Shell fragment that adds the bun bin dir (where ``agent-browser`` lives) to
``PATH``. Nvm-sourced node is already on PATH via the agent's existing
``nvm_source`` prefix, so this only needs to contribute bun."""


def build_agent_browser_sessions_block(env_aliases: list[str]) -> str:
    """Render a per-env ``--session`` map block for the task instruction.

    When the runner pre-logs-in via ``agent-browser``, each env's cookies land in
    its own named session jar (keyed by ``env.alias``). The agent then has to
    pass the right ``--session <name>`` so later ``agent-browser`` calls reuse
    those authenticated cookies. This block tells the model which names exist
    for the current session — returns empty string when there are no envs.
    """
    if not env_aliases:
        return ""
    session_lines = "\n".join(f"- `{alias}`" for alias in env_aliases)
    return (
        "\n\n## Authenticated Sessions\n\n"
        "Each env below has a pre-authenticated `agent-browser` session; pass its name via\n"
        "`--session <name>` (or set `AGENT_BROWSER_SESSION=<name>`) to inherit the saved\n"
        "cookies rather than starting a fresh, logged-out browser:\n\n"
        f"{session_lines}\n"
    )


AGENT_BROWSER_INSTRUCTIONS = """## Browser Commands

Use the `agent-browser` CLI for all browser interaction:

- `agent-browser open <url>` — navigate to a URL
- `agent-browser snapshot -i` — list interactive elements with refs (`@e1`, `@e2`, ...)
- `agent-browser click <ref>` — click an element (e.g. `@e5`)
- `agent-browser fill <ref> <text>` — fill an input field
- `agent-browser select <ref> <value>` — select a dropdown option
- `agent-browser press <key>` — press a key (e.g. `Enter`, `Escape`)
- `agent-browser screenshot` — take a screenshot
- `agent-browser get text <selector>` — get text content
- `agent-browser wait <selector>` — wait for an element
- `agent-browser wait --text "text"` — wait for text to appear
"""
"""``agent-browser`` CLI command reference.

The block is agent-package agnostic: no per-env session names, no task
framing. Callers (typically ``BaseAgent._append_browser_tooling_prompt``)
concatenate it to the agent's effective system prompt. Worlds that need
per-env session hints render those in their own task instruction — mixing
world-specific env context into the shared block belongs in the world, not
here.
"""
