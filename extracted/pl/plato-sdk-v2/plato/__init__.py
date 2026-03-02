# Plato SDK
#
# v1: Legacy SDK (deprecated)
# v2: New SDK with separate sync/async modules
# agents: Harbor agent framework re-exports (ClaudeCode, OpenHands, Codex, etc.)
# sims: Simulation clients (Spree, Firefly, etc.)
# chronos: Chronos agent evaluation platform SDK
#
# Usage (v2 - recommended):
#   from plato.v2 import AsyncPlato, Plato, Env
#
# Usage (agents - Harbor):
#   from plato.agents import ClaudeCode, OpenHands, AgentFactory, AgentName
#   from plato.agents import BaseAgent, BaseInstalledAgent  # For custom agents
#
# Usage (sims):
#   from plato.sims import SpreeClient, FireflyClient
#
# Usage (chronos):
#   from plato.chronos import Client, AsyncClient
#   from plato.chronos.models import AgentCreate, WorldCreate, LaunchJobRequest
#
# Usage (sam3):
#   from plato.sam3 import Sam3, AsyncSam3

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("plato-sdk-v2")
except PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development

__all__ = ["__version__"]


def __getattr__(name: str):
    """Lazy import to avoid loading all modules at once."""
    if name == "v2":
        from plato import v2

        return v2

    if name == "Env":
        from plato.v2 import Env

        return Env

    if name in ("Plato", "SyncPlato", "PlatoTask", "v1"):
        try:
            from plato import v1

            if name == "v1":
                return v1
            return getattr(v1, name)
        except ImportError:
            raise AttributeError(f"module 'plato' has no attribute '{name}' (v1 unavailable)")

    if name == "agents":
        from plato import agents

        return agents

    if name == "sims":
        from plato import sims

        return sims

    if name == "chronos":
        import importlib

        return importlib.import_module("plato.chronos")

    if name == "sam3":
        import importlib

        return importlib.import_module("plato.sam3")

    raise AttributeError(f"module 'plato' has no attribute '{name}'")
