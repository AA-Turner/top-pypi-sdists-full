"""Agent engines — pluggable, overridable owners of the agent loop.

Built-ins are resolved by name (``native``, ``claude-code``); customer engines
are resolved from a ``mod:attr`` reference (mirroring ``WorkerDef`` import refs).
Resolution precedence for the ``engine`` selector itself lives in
``create_agent`` and mirrors how ``model`` resolves.
"""

import importlib

from dreadnode.agents.engines.base import (
    AgentEngine,
    CapabilityComponent,
    EnforcementSurface,
    EngineContext,
    PermissionBridge,
    PolicyFacet,
)
from dreadnode.agents.engines.claude_code import ClaudeCodeEngine, ClaudeCodeTranslationState
from dreadnode.agents.engines.native import NativeEngine

__all__ = [
    "AgentEngine",
    "CapabilityComponent",
    "ClaudeCodeEngine",
    "ClaudeCodeTranslationState",
    "EnforcementSurface",
    "EngineContext",
    "NativeEngine",
    "PermissionBridge",
    "PolicyFacet",
    "register_engine",
    "resolve_engine",
]

_REGISTRY: dict[str, type[AgentEngine]] = {}


def register_engine(cls: type[AgentEngine]) -> type[AgentEngine]:
    """Register a built-in engine class under its ``name`` (usable as a decorator)."""
    name = getattr(cls, "name", None)
    if not name:
        raise ValueError(f"Engine {cls!r} must define a non-empty 'name'.")
    _REGISTRY[name] = cls
    return cls


register_engine(NativeEngine)
register_engine(ClaudeCodeEngine)


def _load_engine_from_ref(ref: str) -> type[AgentEngine]:
    """Import an engine class from a ``module.path:Attr`` or ``module.path.Attr`` ref."""
    module_path, _, attr = ref.partition(":")
    if not attr:
        module_path, _, attr = ref.rpartition(".")
    if not module_path or not attr:
        raise ValueError(f"Invalid engine reference {ref!r}; expected 'module.path:ClassName'.")
    try:
        module = importlib.import_module(module_path)
    except ImportError as exc:
        raise ValueError(f"Could not import engine module '{module_path}' from {ref!r}.") from exc
    obj = getattr(module, attr, None)
    if obj is None or not (isinstance(obj, type) and issubclass(obj, AgentEngine)):
        raise ValueError(f"Engine reference {ref!r} did not resolve to an AgentEngine subclass.")
    return obj


def resolve_engine(spec: "str | AgentEngine | type[AgentEngine] | None") -> AgentEngine:
    """Resolve an ``engine`` selector to a concrete :class:`AgentEngine` instance.

    Accepts ``None`` (→ native), an instance, a class, a built-in name, or a
    ``mod:attr`` reference. A fresh instance is returned for class/name/ref specs
    so stateful engines (subprocess-backed) don't leak state across turns.
    """
    if spec is None:
        return NativeEngine()
    if isinstance(spec, AgentEngine):
        return spec
    if isinstance(spec, type) and issubclass(spec, AgentEngine):
        return spec()
    if isinstance(spec, str):
        if spec in _REGISTRY:
            return _REGISTRY[spec]()
        if ":" in spec or "." in spec:
            return _load_engine_from_ref(spec)()
        known = ", ".join(sorted(_REGISTRY)) or "(none)"
        raise ValueError(f"Unknown engine '{spec}'. Known built-ins: {known}.")
    raise TypeError(f"Unsupported engine selector: {spec!r}")
