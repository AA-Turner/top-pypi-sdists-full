"""Shared instruction block + lifecycle for the computer-use MCP server.

Agent packages (claude-code, codex, ...) opt in via
``AgentConfig.computer_use_mcp_enabled``: the agent runtime writes the local
server into its MCP config (:func:`computer_use_mcp_server_entry`), boots the
server next to the agent subprocess (:class:`ComputerUseMcp`), and splices
:data:`COMPUTER_USE_MCP_INSTRUCTIONS` into the effective system prompt via
``BaseAgent._append_computer_use_mcp_prompt``.

The server always drives a REMOTE ubuntu-vm desktop
(``AgentConfig.computer_use_vm_url``) — there is deliberately no local-display
fallback; the Xvfb-backed DesktopComputer stays private to the computer-use
agent harness.
"""

from __future__ import annotations

import logging
from contextlib import suppress
from typing import TYPE_CHECKING, Any

from plato.computer_use.mcp_server import RemoteComputerToolServer
from plato.computer_use.remote_computer import RemoteDesktopComputer
from plato.sims.ubuntu_vm import AsyncClient as VMAsyncClient

if TYPE_CHECKING:
    from plato.agents.config import AgentConfig

logger = logging.getLogger(__name__)

COMPUTER_USE_MCP_SERVER_NAME = "computer"
"""Server name key in the agent's generated MCP config (tools surface as e.g.
``mcp__computer__screenshot`` in Claude Code)."""

COMPUTER_USE_MCP_PORT = 8766
"""Loopback port for the local computer-use MCP server. Fixed (not
configurable) so the agent's MCP config can be written before the server
boots; 8765 is left free for world-hosted ToolServers."""


def computer_use_mcp_url(port: int = COMPUTER_USE_MCP_PORT) -> str:
    """Local HTTP MCP endpoint URL the agent harness connects to."""
    return f"http://127.0.0.1:{port}/mcp"


COMPUTER_USE_MCP_INSTRUCTIONS = """## Remote Desktop (`computer` MCP server)

The `computer` MCP tools control a remote Ubuntu desktop VM — a separate
machine from the one your shell runs on. Its screen, apps, and files are only
reachable through these tools; in particular, use the MCP `bash` tool (not
your own shell) for commands on the desktop VM. Start with `screenshot` to
see the current screen; every action returns a fresh post-action screenshot.
Coordinates are real pixels in the most recent screenshot."""
"""Concise system-prompt block describing the computer-use MCP server. The
individual tools are self-documenting via their MCP schemas, so this only
covers what the model cannot infer from them: that the desktop is a separate
remote machine and how to orient (screenshot-first, pixel coordinates)."""


def computer_use_mcp_server_entry(config: AgentConfig) -> dict[str, Any] | None:
    """Return the MCP-config server dict for the local computer-use server.

    Returns ``None`` when ``computer_use_mcp_enabled`` is off. Raises
    ``ValueError`` when it is on without ``computer_use_vm_url`` — validated
    here (at MCP-config write time, before the agent subprocess launches)
    because there is no local fallback to degrade to.
    """
    if not config.computer_use_mcp_enabled:
        return None
    if not config.computer_use_vm_url:
        raise ValueError(
            "computer_use_mcp_enabled requires computer_use_vm_url (the remote "
            "ubuntu-vm desktop_agent URL, or an {env: alias} reference). Worlds "
            "with an ubuntu-vm env inject it at launch; set it explicitly for "
            "local runs."
        )
    if not isinstance(config.computer_use_vm_url, str):
        # An {env, port} alias no world resolved — starting the server against
        # it can only fail, so fail loudly here (mirrors write_mcp_config's
        # unresolved-EnvMcpUrl handling).
        raise ValueError(
            f"computer_use_vm_url is an unresolved env reference "
            f"{config.computer_use_vm_url!r}; this agent's world does not "
            "support env-alias computer-use attachment"
        )
    return {"url": computer_use_mcp_url()}


class ComputerUseMcp:
    """Lifecycle handle for the local computer-use MCP server.

    Boot with :meth:`start` next to the agent subprocess (inside the same
    try/finally that tears down other sidecars) and :meth:`close` on exit.
    """

    def __init__(
        self,
        vm_url: str,
        *,
        port: int = COMPUTER_USE_MCP_PORT,
        logger: logging.Logger | None = None,
    ) -> None:
        self._vm_url = vm_url
        self._port = port
        self._logger = logger or logging.getLogger(__name__)
        self._vm_client = None
        self._server = None

    @classmethod
    def from_config(cls, config: AgentConfig, *, logger: logging.Logger | None = None) -> ComputerUseMcp | None:
        """Build a handle from an agent config; None when the flag is off."""
        if computer_use_mcp_server_entry(config) is None:
            return None
        # The entry call above raised on None and on unresolved EnvMcpUrl refs.
        assert isinstance(config.computer_use_vm_url, str)
        return cls(config.computer_use_vm_url, logger=logger)

    @property
    def url(self) -> str:
        return computer_use_mcp_url(self._port)

    async def start(self) -> None:
        """Connect to the remote desktop and serve its tools over local MCP.

        Strict: any failure — including an unreachable desktop VM — cleans up
        whatever was partially created and re-raises, so the agent run ABORTS
        instead of running with a dead ``computer`` server in its MCP config
        (there is deliberately no degraded/local fallback for this feature).
        """
        self._logger.info(
            "Starting computer-use MCP server on %s (remote desktop: %s)",
            self.url,
            self._vm_url,
        )
        try:
            self._vm_client = self._make_vm_client()
            computer = RemoteDesktopComputer(vm_client=self._vm_client)
            # Probe the desktop up front (also yields the real resolution, so
            # coordinate spans normalize correctly). Deliberately NOT the
            # lenient sync_dimensions_from_remote(): a VM we cannot reach now
            # would otherwise only surface as per-tool errors mid-run.
            try:
                status = await self._vm_client.status()
            except Exception as exc:
                raise RuntimeError(f"computer-use MCP: remote desktop at {self._vm_url} is unreachable: {exc}") from exc
            computer.width = status.resolution.width
            computer.height = status.resolution.height
            self._server = RemoteComputerToolServer(computer, port=self._port)
            await self._server.start()
        except BaseException:
            # Don't leak the VM client / half-started server when startup
            # fails — callers never get the handle, so their teardown paths
            # can't close it. suppress() keeps the original error primary.
            with suppress(Exception):
                await self.close()
            raise

    def _make_vm_client(self):
        return VMAsyncClient(base_url=self._vm_url, timeout=300.0)

    async def close(self) -> None:
        if self._server is not None:
            await self._server.close()
            self._server = None
        if self._vm_client is not None:
            await self._vm_client.close()
            self._vm_client = None
