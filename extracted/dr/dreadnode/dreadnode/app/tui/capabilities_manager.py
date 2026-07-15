"""Runtime capability snapshot for the TUI.

Mirrors the server-side :class:`dreadnode.app.server.capability_manager.CapabilityRegistry`
from the TUI's perspective: owns the last ``RuntimeInfo`` snapshot the
runtime server sent us, plus the derived queries the rest of the TUI uses
(default capability/agent resolution, visible agent list, MCP server
list, component health, capability updates). All of this used to live
directly on :class:`DreadnodeTextualApp` as ~12 scattered helper methods
hanging off a bare ``runtime_info`` attribute.

The :class:`CapabilitiesContextPort` protocol is the narrow surface the
manager uses to push state back into the app (mention overlay agents,
runtime_health groups, working_dir reactive, conversation re-sync). The
app implements it via an ``_AppCapabilitiesContext`` adapter in
``app.py``; nothing in the manager imports ``DreadnodeTextualApp``
directly.

Part A of the capabilities/tools/skills refactor. Parts B and C extend
this module with a typed ``tool_catalog`` dict and a registration API
for :mod:`dreadnode.app.tui.tool_format`.
"""

import typing as t
from dataclasses import dataclass, field

from loguru import logger
from textual.message import Message

from dreadnode.app.client.models import RuntimeInfo, SessionInfo, ToolInfo
from dreadnode.app.tui import tool_format

if t.TYPE_CHECKING:
    from dreadnode.app.client.managed_client import ManagedRuntimeClient


# Mirrors ``packages/sdk/dreadnode/app/server/app.py:_BUNDLED_DEFAULT_CAPABILITY``.
# Hardcoded here rather than imported because the TUI shouldn't take a hard
# dependency on the server module's import graph for a single string constant.
# Kept narrow so a wandering rename is easy to spot in review.
_BUNDLED_CAPABILITY_NAME = "dreadnode"


@dataclass(frozen=True, slots=True)
class CapabilitiesSummary:
    """Snapshot of *user-installed* capabilities for the welcome widget.

    Excludes the bundled ``dreadnode`` capability — that ships in the
    SDK wheel and is always loaded, so counting it would inflate the
    "you have N capabilities" signal in a way the user can't act on.

    ``enabled_slugs`` is the alphabetised list of currently-enabled
    capability names. Disabled capabilities aren't named individually
    (the count is enough to flag "you have things turned off"); the
    user can drill into the capabilities screen to manage them.
    """

    enabled_count: int = 0
    disabled_count: int = 0
    enabled_slugs: tuple[str, ...] = field(default_factory=tuple)


class ComponentStateChanged(Message):
    """Posted to the app after the runtime bus reports a component state change.

    Carries the raw payload so screens can decide what to re-render. The
    ``runtime_info`` snapshot has already been patched in place by the
    subscriber loop before this message is posted, so handlers should
    re-read from :class:`CapabilitiesManager` rather than the payload.
    """

    def __init__(self, payload: dict[str, t.Any]) -> None:
        super().__init__()
        self.payload = payload


# =============================================================================
# Port
# =============================================================================


class CapabilitiesContextPort(t.Protocol):
    """Narrow surface the :class:`CapabilitiesManager` uses to mutate app state."""

    def managed_client(self) -> "ManagedRuntimeClient":
        """Return the currently active runtime server client."""

    def set_working_dir(self, working_dir: str) -> None:
        """Set the ``working_dir`` reactive after a runtime refresh."""

    def set_mention_agents(self, agents: list[dict[str, str]]) -> None:
        """Push the visible agent list into the ``@``-mention overlay."""

    def set_runtime_health(self, groups: tuple[tuple[str, str, str, str], ...]) -> None:
        """Set the ``runtime_health`` reactive for the page-status zone."""

    def sync_sessions(self) -> None:
        """Request a session listing re-sync."""

    def update_context(self) -> None:
        """Request a context-bar re-sync (agent name, session label, ...)."""

    async def refresh_skill_names(self) -> None:
        """Re-fetch skill names for the slash overlay."""

    def open_capabilities_screen(self) -> None:
        """Push the capabilities screen onto the screen stack."""

    def set_welcome_capabilities(self, summary: "CapabilitiesSummary | None") -> None:
        """Push a fresh capability snapshot into the welcome widget.

        Called from :meth:`CapabilitiesManager.apply_runtime_info`. Passing
        ``None`` represents pre-hydration; the widget renders that as
        "block suppressed" so we don't flash a wrong empty state.
        """


# =============================================================================
# Manager
# =============================================================================


class CapabilitiesManager:
    """Caches runtime capability metadata and answers derived queries."""

    def __init__(self, *, context: CapabilitiesContextPort) -> None:
        self._context = context
        self.runtime_info: RuntimeInfo | None = None
        # Flat tool catalog populated from ``/api/tools`` alongside each
        # runtime refresh. Keyed by tool name. Used by
        # :mod:`dreadnode.app.tui.tool_format` (Part C) to drive label
        # formatting and summarization without hardcoding built-in names.
        self.tool_catalog: dict[str, ToolInfo] = {}
        # Flag the capabilities screen sets before dismiss to request a
        # runtime reload on the next open. Read and cleared by the screen
        # router via :meth:`consume_pending_capability_reload`.
        self.pending_capability_reload: bool = False
        # Diagnostic message the capabilities "fix" flow queues for the
        # agent after the screen dismisses. Consumed by the app's
        # capabilities-dismiss callback.
        self.pending_fix_message: str | None = None

    # ------------------------------------------------------------------
    # Default capability / agent resolution
    # ------------------------------------------------------------------

    def default_capability_name(self) -> str | None:
        """Resolve the active runtime's default capability for display and routing."""
        if self.runtime_info is None:
            return None
        default_capability = getattr(self.runtime_info, "default_capability", None)
        if default_capability:
            for capability in self.runtime_info.capabilities:
                if capability.name == default_capability:
                    return capability.name
        for capability in self.runtime_info.capabilities:
            if capability.agents:
                return capability.name
        return None

    def default_agent_name(self) -> str | None:
        """Resolve the runtime's default entry agent name, if any."""
        default_capability = self.default_capability_name()
        if self.runtime_info is None:
            return None
        if default_capability is not None:
            for capability in self.runtime_info.capabilities:
                if capability.name == default_capability and capability.agents:
                    return capability.agents[0].name
        for capability in self.runtime_info.capabilities:
            if capability.agents:
                return capability.agents[0].name
        return None

    def capability_for_agent(self, agent_name: str) -> str | None:
        """Return the loaded capability name for a unique agent match."""
        if self.runtime_info is None:
            return None
        matches = [
            capability.name
            for capability in self.runtime_info.capabilities
            for agent in capability.agents
            if agent.name == agent_name
        ]
        if len(matches) == 1:
            return matches[0]
        return None

    def session_display_agent(self, session_info: SessionInfo) -> str:
        """Return the best available display name for a session's active agent."""
        return (
            session_info.agent or session_info.capability or self.default_agent_name() or "default"
        )

    # ------------------------------------------------------------------
    # Agent / MCP / component enumeration
    # ------------------------------------------------------------------

    @staticmethod
    def _fallback_default_agent_entry() -> dict[str, str]:
        """Synthetic fallback agent shown only when no real agent is available."""
        return {
            "name": "default",
            "description": "Fallback default runtime",
            "model": "inherit",
            "capability": "built-in",
        }

    def collect_agents(self) -> list[dict[str, str]]:
        """Build the visible agent list from loaded capabilities.

        Shows the synthetic ``default`` entry only when no real agents
        are available.
        """
        agents: list[dict[str, str]] = []
        seen: set[str] = set()
        if self.runtime_info:
            for cap in self.runtime_info.capabilities:
                for agent in cap.agents:
                    if agent.name in seen:
                        continue
                    agents.append(
                        {
                            "name": agent.name,
                            "description": agent.description or "",
                            "model": agent.model or "inherit",
                            "capability": cap.name,
                            "capability_version": getattr(cap, "version", None) or "",
                        }
                    )
                    seen.add(agent.name)
        if agents:
            return agents
        return [self._fallback_default_agent_entry()]

    def collect_mcp_servers(self) -> list[dict[str, t.Any]]:
        """Extract MCP server info from runtime info components."""
        if not self.runtime_info:
            return []
        servers: list[dict[str, t.Any]] = []
        for cap in self.runtime_info.capabilities:
            for comp in cap.components or []:
                kind = comp.get("kind") if isinstance(comp, dict) else getattr(comp, "kind", None)
                if kind == "mcp_server":
                    _get = (
                        comp.get
                        if isinstance(comp, dict)
                        else lambda k, d=None, _comp=comp: getattr(_comp, k, d)
                    )
                    servers.append(
                        {
                            "name": _get("name", "?"),
                            "status": _get("status", "?"),
                            "error": _get("error"),
                            "detail": _get("detail"),
                            "qualified_name": _get("qualified_name"),
                            "capability": _get("capability") or cap.name,
                            "transport": _get("transport"),
                            "tool_count": _get("tool_count", 0),
                        }
                    )
        return servers

    def collect_workers(self) -> list[dict[str, t.Any]]:
        """Extract worker info from runtime info components."""
        if not self.runtime_info:
            return []
        workers: list[dict[str, t.Any]] = []
        for cap in self.runtime_info.capabilities:
            for comp in cap.components or []:
                kind = comp.get("kind") if isinstance(comp, dict) else getattr(comp, "kind", None)
                if kind == "worker":
                    _get = (
                        comp.get
                        if isinstance(comp, dict)
                        else lambda k, d=None, _comp=comp: getattr(_comp, k, d)
                    )
                    workers.append(
                        {
                            "name": _get("name", "?"),
                            "status": _get("status", "?"),
                            "error": _get("error"),
                            "detail": _get("detail"),
                            "capability": _get("capability") or cap.name,
                        }
                    )
        return workers

    def collect_component_issues(self) -> list[dict[str, str | None]]:
        """Extract all component health issues from runtime info."""
        if not self.runtime_info:
            return []
        issues: list[dict[str, str | None]] = []
        for cap in self.runtime_info.capabilities:
            for comp in cap.components or []:
                _get = (
                    comp.get
                    if isinstance(comp, dict)
                    else lambda k, d=None, _comp=comp: getattr(_comp, k, d)
                )
                status = _get("status", "ok")
                # ``needs_auth`` is a warning-level issue — surfaced in the
                # ambient status bar so the user notices, but visually
                # distinct from a hard error/degraded state (ENG-6989).
                if status in ("error", "degraded", "needs_auth"):
                    issues.append(
                        {
                            "name": _get("name", "?"),
                            "kind": _get("kind", "?"),
                            "status": status,
                            "error": _get("error"),
                            "detail": _get("detail"),
                        }
                    )
        return issues

    # ------------------------------------------------------------------
    # Runtime health / update summaries
    # ------------------------------------------------------------------

    def runtime_health_groups(
        self,
    ) -> tuple[tuple[str, str, str, str], ...]:
        """Compute the issue-and-updates groups for the PageStatus zone."""
        issues = self.collect_component_issues()

        def _summarize(items: list[dict[str, str | None]], max_names: int = 2) -> str:
            names = ", ".join(str(i.get("name", "?")) for i in items[:max_names])
            if len(items) > max_names:
                names += f" +{len(items) - max_names}"
            return names

        mcp_errors = [
            i for i in issues if i.get("kind") == "mcp_server" and i.get("status") != "needs_auth"
        ]
        mcp_needs_auth = [
            i for i in issues if i.get("kind") == "mcp_server" and i.get("status") == "needs_auth"
        ]
        other_issues = [i for i in issues if i.get("kind") != "mcp_server"]

        groups: list[tuple[str, str, str, str]] = []
        if mcp_errors:
            groups.append(("MCP", _summarize(mcp_errors), "/mcp", "error"))
        # ``needs_auth`` is its own bucket so a future PageStatus severity
        # split can render it distinctly from hard errors. Today both
        # render with WARNING styling (ENG-6989).
        if mcp_needs_auth:
            groups.append(("auth", _summarize(mcp_needs_auth), "/mcp", "warning"))
        if other_issues:
            groups.append(("components", _summarize(other_issues), "/capabilities", "error"))

        if self.runtime_info:
            updates = [cap for cap in self.runtime_info.capabilities if cap.update_available]
            if updates:
                names = ", ".join(cap.name for cap in updates[:2])
                if len(updates) > 2:
                    names += f" +{len(updates) - 2}"
                groups.append(("updates", names, "/capabilities", "update"))

        return tuple(groups)

    def update_runtime_health(self) -> None:
        """Push fresh ``runtime_health`` groups into the app."""
        self._context.set_runtime_health(self.runtime_health_groups())

    def welcome_capabilities_summary(self) -> CapabilitiesSummary | None:
        """Compute the user-installed capability snapshot for the welcome widget.

        Returns ``None`` until ``runtime_info`` arrives (pre-hydration).
        Once hydrated, the bundled ``dreadnode`` capability is filtered out
        and the remaining capabilities are split by ``cap.enabled``.
        Slugs are sorted alphabetically so renders are deterministic and
        we don't accidentally suggest a curated order.
        """
        if self.runtime_info is None:
            return None

        enabled: list[str] = []
        disabled = 0
        for cap in self.runtime_info.capabilities:
            if cap.name == _BUNDLED_CAPABILITY_NAME:
                continue
            if cap.enabled:
                enabled.append(cap.name)
            else:
                disabled += 1
        enabled.sort()

        return CapabilitiesSummary(
            enabled_count=len(enabled),
            disabled_count=disabled,
            enabled_slugs=tuple(enabled),
        )

    def apply_component_state_change(self, payload: dict[str, t.Any]) -> bool:
        """Patch the cached ``runtime_info`` from a ``component.state_changed`` payload.

        Returns ``True`` if the matching component was found and updated;
        ``False`` if the snapshot doesn't know about it (capability not
        loaded yet — typically a startup race that the next full refresh
        will resolve). Callers update reactive state and notify open
        screens themselves so this method stays a pure patch.
        """
        if self.runtime_info is None:
            return False
        capability = payload.get("capability")
        name = payload.get("name")
        kind = payload.get("kind")
        if not capability or not name or kind not in ("worker", "mcp_server"):
            return False
        for cap in self.runtime_info.capabilities:
            if cap.name != capability:
                continue
            for comp in cap.components or []:
                if comp.get("kind") == kind and comp.get("name") == name:
                    if "status" in payload:
                        comp["status"] = payload["status"]
                    comp["error"] = payload.get("error")
                    if payload.get("detail") is not None:
                        comp["detail"] = payload["detail"]
                    if "tool_count" in payload and payload["tool_count"] is not None:
                        comp["tool_count"] = payload["tool_count"]
                    return True
            return False
        return False

    # ------------------------------------------------------------------
    # State mutation
    # ------------------------------------------------------------------

    async def apply_runtime_info(
        self,
        runtime_info: RuntimeInfo,
        *,
        refresh_skills: bool = False,
    ) -> None:
        """Apply fresh runtime metadata to the app's visible state."""
        self.runtime_info = runtime_info
        logger.debug(
            "Runtime refresh | capabilities={}",
            len(runtime_info.capabilities),
        )
        self.update_runtime_health()
        self._context.set_mention_agents(self.collect_agents())
        self._context.set_working_dir(runtime_info.working_dir or "")
        self._context.set_welcome_capabilities(self.welcome_capabilities_summary())
        self._context.sync_sessions()
        self._context.update_context()
        if refresh_skills:
            await self._context.refresh_skill_names()

    async def refresh(self) -> None:
        """Fetch fresh runtime info + tool catalog from the server and apply."""
        client = self._context.managed_client()
        runtime_info = await client.fetch_runtime_info()
        await self.apply_runtime_info(runtime_info)
        # Tool catalog lives alongside runtime_info — a catalog refresh
        # failure should be non-fatal since the runtime metadata is the
        # load-bearing piece.
        try:
            tools = await client.fetch_tools()
        except Exception:
            logger.opt(exception=True).warning("Failed to refresh tool catalog")
            return
        self.set_tool_catalog(tools)

    def set_tool_catalog(self, tools: list[ToolInfo]) -> None:
        """Replace the tool catalog with a fresh list, keyed by name.

        Re-seeds :mod:`dreadnode.app.tui.tool_format` with the built-in
        defaults and then registers key-arg hints for every catalog
        entry that carries a JSON Schema — capability-provided tools
        get the same compact labelling as built-ins instead of falling
        back to the generic first-string-arg heuristic.
        """
        self.tool_catalog = {tool.name: tool for tool in tools if tool.name}
        tool_format.clear_tool_registry()
        for tool in self.tool_catalog.values():
            keys = tool_format.derive_key_args_from_schema(tool.parameters_schema)
            if keys:
                tool_format.register_tool_key_args(tool.name, keys)

    def find_tool(self, name: str) -> ToolInfo | None:
        """Return the catalog entry for ``name`` or ``None``."""
        return self.tool_catalog.get(name)

    def tool_capability(self, name: str) -> str | None:
        """Return the capability group for a tool (``built-in``, cap name, ...)."""
        tool = self.tool_catalog.get(name)
        return tool.capability if tool else None

    async def reload_and_open(self) -> None:
        """Ask the server to reload capabilities and then open the screen."""
        await self._context.managed_client().reload_capabilities()
        self._context.open_capabilities_screen()

    # ------------------------------------------------------------------
    # Pending-state signals used by the capabilities screen flow
    # ------------------------------------------------------------------

    def consume_pending_capability_reload(self) -> bool:
        """Pop the pending-reload flag. Returns its prior value."""
        pending = self.pending_capability_reload
        if pending:
            self.pending_capability_reload = False
        return pending

    def take_pending_fix_message(self) -> str | None:
        """Pop the pending fix message, marking a reload as pending if present."""
        message = self.pending_fix_message
        if message is None:
            return None
        self.pending_fix_message = None
        self.pending_capability_reload = True
        return message
