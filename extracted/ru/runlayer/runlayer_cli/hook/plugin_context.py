"""Deterministic Runlayer Plugin routing context for session hooks.

Org installs ship a ``runlayer`` SKILL.md that asks the model to route tool
and skill discovery through the Runlayer Plugin. The model can skip a skill;
it cannot skip ``additionalContext`` emitted by a ``SessionStart`` or
``UserPromptSubmit`` hook. This module builds that context when the built-in
Runlayer Plugin is configured for the current session and stays silent
otherwise, so sessions without the plugin are untouched.

Runs inside ``aiwatch hook`` on every prompt: config lookups only, no network.
"""

from __future__ import annotations

from dataclasses import dataclass

from runlayer_cli.config import load_config
from runlayer_cli.hook import hook_io
from runlayer_cli.hook.clients import Client
from runlayer_cli.hook.mcp_lookup import (
    codex_mcp_server_key,
    lookup_codex_mcp_server,
    lookup_mcp_server,
)
from runlayer_cli.hook.mcp_types import MCPServer
from runlayer_cli.mdm_config import read_managed_config

# Stable ID of the built-in Runlayer Plugin (backend ``app/core/mcp_constants``).
RUNLAYER_PLUGIN_ID = "a9d3ab20-4f5f-4d7b-a7b2-7b2b6f1d0d44"
_PLUGIN_URL_MARKER = f"/api/v1/proxy/plugins/{RUNLAYER_PLUGIN_ID}/mcp"
# The webapp hands out ``<host>/mcp`` for the built-in plugin (backend
# ``RUNLAYER_PLUGIN_MCP_ALIAS_PATH``). Any host serves something at ``/mcp``, so
# the alias only counts on the configured Runlayer host.
_PLUGIN_ALIAS_PATH = "/mcp"

# ``RUNLAYER_PLUGIN_CONTEXT=0`` in the client's environment disables injection.
# Read through ``hook_io`` and allowlisted in ``daemon_protocol`` so the value
# reaches daemon-served hooks, which never see the client's own environment.
DISABLE_ENV = "RUNLAYER_PLUGIN_CONTEXT"
_DISABLED_VALUES = frozenset({"0", "false", "off"})


@dataclass(frozen=True)
class PluginInstall:
    """How the built-in plugin reaches the model in one client.

    ``server`` is the MCP server name exactly as the client prefixes tool names
    with it (``mcp__<server>__<tool>``). ``plugin`` is the client-side plugin
    package that carries the server, or None for a direct MCP entry.
    """

    server: str
    plugin: str | None = None


# Candidate installs per client, in the order the client exposes them in tool
# names. The proxy URL, not the name, is the identity; names only decide what
# to call the server in the injected text.
#
# Claude Code: the Anthropic org plugin zip (plugin ``runlayer`` exposing
# server ``runlayer-plugin``) is namespaced ``plugin_<plugin>_<server>`` and is
# checked before the plain names because ``lookup_mcp_server`` also finds a
# plugin-provided server under its plain name. Auto Sync and new installs use
# ``runlayer-plugin``; legacy org installs use ``onelayer``.
_CLAUDE_CODE_CANDIDATES: tuple[PluginInstall, ...] = (
    PluginInstall("plugin_runlayer_runlayer-plugin", plugin="runlayer"),
    PluginInstall("plugin_runlayer_onelayer", plugin="runlayer"),
    PluginInstall("runlayer-plugin"),
    PluginInstall("onelayer"),
)
# Codex: direct entries in ``~/.codex/config.toml`` or the managed TOML.
_CODEX_CANDIDATES: tuple[PluginInstall, ...] = (
    PluginInstall("runlayer-plugin"),
    PluginInstall("onelayer"),
)

_CLIENT_LABELS = {Client.CLAUDE_CODE: "Claude Code", Client.CODEX: "Codex"}

_PLUGIN_INSTALL_LINE = (
    'Runlayer Plugin is installed as the {client} plugin "{plugin}". '
    "Its tools are prefixed mcp__{server}__."
)
_SERVER_INSTALL_LINE = (
    'Runlayer Plugin is connected as MCP server "{server}". '
    "Its tools are prefixed mcp__{server}__."
)

_ROUTING_RULES = """\
{install} Follow these rules:
1. Before answering a request that may need organization-specific guidance \
(workflows, runbooks, policies, setup, QA or verification steps), call \
search_skills (or list_skills to browse), then get_skill_file with the skill id \
and file id it returned (get_skill lists a skill's files when you need more). \
Skip this for arithmetic, tiny copyedits, or requests that clearly need no \
specialized guidance.
2. For external services, use a separately connected Runlayer connector when \
one exposes the tool. Otherwise call the matching tool the plugin advertises, by \
the exact name shown in the tool list. If the plugin exposes search_tools and \
execute_tool instead, call search_tools first, then execute_tool with the exact \
returned name. In either case, if what you find is a DISABLED_, AUTH_REQUIRED_ \
or INPUTS_REQUIRED_ placeholder, call it directly (never through execute_tool) \
and relay its instructions to the user. Never guess tool names.
3. Do not use built-in integrations (Slack, GitHub, Linear, Notion, Google, ...) \
for a service available through Runlayer. They bypass organization policy and \
audit logs.
4. To delegate work, when the plugin exposes them, call list_agents, inspect \
with get_agent, then run_agent with confirm=true and poll get_agent_run_trace \
for the result. Never route skills or agents through execute_tool."""


def _configured_runlayer_host() -> str | None:
    """Runlayer host from the CLI config or MDM, without touching the keychain."""
    try:
        host = load_config().default_host or read_managed_config().get("host")
    except Exception:
        return None
    return host.rstrip("/") if host else None


def _is_plugin_url(url: str, runlayer_host: str | None) -> bool:
    if _PLUGIN_URL_MARKER in url:
        return True
    if not runlayer_host:
        return False
    return url.rstrip("/") == f"{runlayer_host}{_PLUGIN_ALIAS_PATH}"


def _lookup(client: Client, server: str, cwd: str) -> MCPServer | None:
    if client is Client.CODEX:
        return lookup_codex_mcp_server(server)
    return lookup_mcp_server(server, cwd)


def find_runlayer_plugin(client: Client, cwd: str) -> PluginInstall | None:
    """How the built-in Runlayer Plugin is installed for *client*, or None."""
    if client is Client.CLAUDE_CODE:
        candidates = _CLAUDE_CODE_CANDIDATES
    elif client is Client.CODEX:
        candidates = _CODEX_CANDIDATES
    else:
        return None
    runlayer_host = _configured_runlayer_host()
    for candidate in candidates:
        found = _lookup(client, candidate.server, cwd)
        if found is None or not _is_plugin_url(found.get("url", ""), runlayer_host):
            continue
        server = candidate.server
        if client is Client.CODEX:
            # Codex builds tool names from the configured key, which may differ
            # from the candidate spelling (``runlayer_plugin`` for
            # ``runlayer-plugin``).
            server = codex_mcp_server_key(candidate.server) or candidate.server
        return PluginInstall(server, candidate.plugin)
    return None


def _install_line(client: Client, install: PluginInstall) -> str:
    if install.plugin is not None:
        return _PLUGIN_INSTALL_LINE.format(
            client=_CLIENT_LABELS[client], plugin=install.plugin, server=install.server
        )
    return _SERVER_INSTALL_LINE.format(server=install.server)


def build_plugin_context(client: Client, cwd: str) -> str | None:
    """Routing rules to inject, or None when the plugin is absent or disabled."""
    if (hook_io.getenv(DISABLE_ENV) or "").strip().lower() in _DISABLED_VALUES:
        return None
    install = find_runlayer_plugin(client, cwd)
    if install is None:
        return None
    return _ROUTING_RULES.format(install=_install_line(client, install))
