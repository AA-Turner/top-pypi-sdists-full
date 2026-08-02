"""The single home of the "assistant" concept (Claude Code, Codex).

An :class:`Assistant` bundles everything that used to be duplicated across the parallel
``McpTarget`` / ``PermsTarget`` hierarchies and the ``claude_*`` / ``codex_*`` wrappers:

- its identity — ``name`` and ``cli_binary`` — and, defined **once** here, ``cli_present`` /
  ``is_active`` (is this assistant on the machine?);
- its three stores: :class:`~.mcp_targets.McpStore` (MCP config), :class:`~.perms_targets.PermsStore`
  (security defaults) and :class:`~.skills_deploy.SkillsTarget` (skills deployment).

:func:`active_assistants` returns the assistants present on the machine — the single selector
used everywhere a config write must fan out to every assistant the user has. Adding a third
assistant is one :class:`Assistant` instance plus its stores, no new parallel hierarchy.
"""

import shutil
from collections.abc import Callable
from dataclasses import dataclass

from ...common.mcp_targets import ClaudeMcpStore, CodexMcpStore, McpStore
from .perms_targets import ClaudePermsStore, CodexPermsStore, PermsStore
from .skills_deploy import ClaudeSkillsTarget, CodexSkillsTarget, SkillsTarget, _codex_plugin_registered


@dataclass(frozen=True)
class Assistant:
    """One AI coding assistant and its per-format configuration stores."""

    name: str
    cli_binary: str
    mcp: McpStore
    perms: PermsStore
    skills: SkillsTarget
    # True when this assistant loads MCP servers from the Pysae plugin's own
    # ``.mcp.json`` rather than from a per-server entry written into its
    # config store. For such assistants the store is never populated with MCP
    # servers — the plugin declares them, and the shim (``pysae-ai-tools mcp run
    # <server>``) resolves secrets at launch. Only legacy baked entries are
    # removed from it (migration).
    mcp_via_plugin: bool | Callable[[], bool] = False

    def uses_plugin_mcp(self) -> bool:
        if callable(self.mcp_via_plugin):
            return self.mcp_via_plugin()
        return self.mcp_via_plugin

    def cli_present(self) -> bool:
        return shutil.which(self.cli_binary) is not None

    def is_active(self) -> bool:
        """True when this assistant is on the machine: its CLI is on ``PATH``, or the MCP
        config file it owns already exists (a prior install we keep in sync)."""
        return self.cli_present() or self.mcp.config_path().exists()


CLAUDE = Assistant(
    name="claude",
    cli_binary="claude",
    mcp=ClaudeMcpStore(),
    perms=ClaudePermsStore(),
    skills=ClaudeSkillsTarget(),
    mcp_via_plugin=True,
)

CODEX = Assistant(
    name="codex",
    cli_binary="codex",
    mcp=CodexMcpStore(),
    perms=CodexPermsStore(),
    skills=CodexSkillsTarget(),
    mcp_via_plugin=lambda: _codex_plugin_registered(),
)

# Claude first: it holds the canonical source format the others convert from.
ASSISTANTS: tuple[Assistant, ...] = (CLAUDE, CODEX)


def active_assistants() -> list[Assistant]:
    """The assistants present on the machine (CLI on PATH, or an owned config file)."""
    return [assistant for assistant in ASSISTANTS if assistant.is_active()]
