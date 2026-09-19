"""Read-only, caller-scoped access to the runtime's existing diagnostics."""

import typing as t
from dataclasses import dataclass
from pathlib import Path

from dreadnode.app.diagnostics import redact_sensitive_text

if t.TYPE_CHECKING:
    from dreadnode.agents import Agent
    from dreadnode.app.server.capability_manager import CapabilityRegistry


@dataclass
class RuntimeInspection:
    registry: t.Callable[[], "CapabilityRegistry | None"]
    agent: t.Callable[[], "Agent"]
    capability: tuple[str, str] | None

    @staticmethod
    def to_prompt() -> str:
        """Render host guidance shared by every runtime agent delivery path."""
        return (
            "## Runtime capability health\n\n"
            "Use `runtime_info` when asked what this runtime can do, before work that "
            "depends on uncertain capability health, or after a component fails. It reads "
            "current recorded diagnostics; loaded components are not necessarily usable "
            "or exposed as tools to you. Report affected functionality and diagnostic "
            "reasons when blocked or degraded. Missing or unknown health is not success. "
            "Do not infer overall health from a successful inspection."
        )

    def runtime_info(self) -> dict[str, t.Any]:
        """Inspect current capability inventory, component health, and your exposed tools.

        Read-only. Reports recorded state, not a live probe or a guarantee that a tool
        will succeed. Null diagnostics and unrecorded health mean unknown information.
        """
        agent = self.agent()
        result: dict[str, t.Any] = {
            "agent": agent.name,
            "active_capability": (
                {"name": self.capability[0], "version": self.capability[1] or None}
                if self.capability
                else None
            ),
            "exposed_tools": sorted({tool.wire_name for tool in agent.all_tools}),
            "registry_status": "unavailable",
            "capabilities": [],
        }
        registry = self.registry()
        if registry is None:
            result["reason"] = "Runtime capability registry is unavailable; health is unknown."
            return result

        snapshot = registry.to_runtime_info(working_dir=Path.cwd())
        result["registry_status"] = "available"
        for capability in snapshot.capabilities:
            loaded = registry.capabilities.get(capability.name)
            # Failed local loads may share a name with a healthy bundled capability.
            is_loaded = (
                loaded is not None
                and (str(loaded.path) if loaded.path is not None else None) == capability.local_path
            )
            result["capabilities"].append(
                {
                    "name": capability.name,
                    "display_name": capability.display_name,
                    "version": capability.version,
                    "loaded": is_loaded,
                    "enabled": capability.enabled,
                    "health_recording": "recorded" if capability.components else "unknown",
                    "components": [
                        {
                            "kind": component.kind,
                            "name": component.name,
                            "status": component.status,
                            "error": self._diagnostic(component.error),
                            "detail": self._diagnostic(component.detail),
                        }
                        for component in capability.components
                    ],
                }
            )
        return result

    @staticmethod
    def _diagnostic(value: str | None) -> str | None:
        return redact_sensitive_text(value)[:2000] if value else None
