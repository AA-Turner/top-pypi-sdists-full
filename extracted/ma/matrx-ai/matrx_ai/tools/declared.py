"""Code-as-source-of-truth tool declaration + in-process registry.

This module is the spine of the tool-drift validation system. A tool's four
orthogonal facts — *identity* (name), *location* (function_path), *ownership*
(source_kind / executor) and *argument schema* (a Pydantic model) — are declared
in code via the :func:`tool` decorator. The validator
(:mod:`matrx_ai.tools.validation`) diffs this code registry against the
``tool_def`` / ``tool_binding`` database rows and reports any divergence.

Why code is the source of truth: tools change fast. When the name, location, or
arguments of a tool drift away from what the database says, agents call into the
void. By forcing every server-executed tool to declare itself here, the drift is
mechanically detectable at release time instead of in production.

Package independence: importing this module pulls in only ``pydantic``. The host
application (aidream, matrx-local, any third party) declares its own tools with
the *same* decorator, contributing into the *same* registry — so a single
validation pass covers every server-side tool regardless of which package owns
it. External / client-executed tools (matrx-extend browser tools, matrx-local,
MCP servers) have no server function and are intentionally not declared here;
the validator reports them as ``external`` rather than as drift.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict


class ToolDeclarationError(Exception):
    """Raised when two different functions try to claim the same tool name."""


class ToolArgs(BaseModel):
    """Base class for every tool's argument model.

    ``extra="forbid"`` is load-bearing in two places:

    * **Validation** — the generated JSON Schema carries
      ``additionalProperties: false``, keeping the code model and the DB schema
      honest about exactly which arguments exist.
    * **Runtime** — when the executor validates an incoming tool call against
      this model, an unexpected key raises a ``ValidationError`` that the
      executor classifies as a ``model_error`` ("the model passed an argument
      this tool does not accept") and *not* a ``tool_defect`` ("the tool body
      threw"). That single distinction is the whole point of the failure
      classification work.
    """

    model_config = ConfigDict(extra="forbid")


class NoArgs(ToolArgs):
    """Explicit empty-argument model for tools that take no parameters."""


@dataclass(frozen=True)
class DeclaredTool:
    """A tool as declared in code — the authoritative record for drift checks."""

    name: str
    source_kind: str
    args_model: type[BaseModel]
    func: Callable[..., Any]
    module: str
    qualname: str
    executor: str | None
    validate: bool
    deprecated: bool

    @property
    def function_path(self) -> str:
        # The DB stores ``<module>.<function>``. ``__qualname__`` equals the
        # bare function name for module-level functions (which every tool is),
        # so this is exactly the location the database should mirror.
        return f"{self.module}.{self.qualname}"


_REGISTRY: dict[str, DeclaredTool] = {}


def tool(
    *,
    name: str,
    source_kind: str,
    args: type[BaseModel] = NoArgs,
    executor: str | None = None,
    validate: bool = True,
    deprecated: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Declare ``fn`` as the server-side implementation of tool ``name``.

    The decorator never alters the wrapped function's call signature — the
    executor still invokes it as ``fn(args, ctx)``. It only records the tool in
    the in-process registry and stamps ``fn.__matrx_tool__`` for introspection.

    Args:
        name: Canonical tool name. Must match ``tool_def.name`` exactly.
        source_kind: One of ``"native" | "mcp_discovered" | "admin_authored"
            | "agent_authored"``. Must match ``tool_def.source_kind`` exactly.
        args: A :class:`ToolArgs` subclass describing the arguments. Its JSON
            Schema is diffed against ``tool_def.parameters``.
        executor: Optional executor name (e.g. ``"matrx-ai-core"``,
            ``"aidream"``). When set, it is checked against the tool's
            ``tool_binding`` rows — the row's ``executor_name`` must include
            this value or the validator flags a binding mismatch.
        validate: Set ``False`` to keep the tool registered for runtime arg
            validation but exempt it from drift checks (the code-side ignore
            switch). Mirrors ``tool_def.validation_exempt`` on the DB side.
        deprecated: Marks a tool that is being retired; the validator treats it
            as exempt and expects it to be ``is_active=false`` in the DB.
    """

    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        declared = DeclaredTool(
            name=name,
            source_kind=source_kind,
            args_model=args,
            func=fn,
            module=fn.__module__,
            qualname=fn.__qualname__,
            executor=executor,
            validate=validate,
            deprecated=deprecated,
        )
        existing = _REGISTRY.get(name)
        if existing is not None and existing.function_path != declared.function_path:
            raise ToolDeclarationError(
                f"Tool name {name!r} is declared by two different functions: "
                f"{existing.function_path} and {declared.function_path}. "
                "Tool names must be globally unique."
            )
        _REGISTRY[name] = declared
        fn.__matrx_tool__ = declared  # type: ignore[attr-defined]
        return fn

    return deco


def declared_tools() -> dict[str, DeclaredTool]:
    """Return a copy of the full code registry keyed by tool name."""
    return dict(_REGISTRY)


def get_declared_tool(name: str) -> DeclaredTool | None:
    return _REGISTRY.get(name)


# ── Generic tool families ──────────────────────────────────────────────────
# A *family* is the platform answer to "a row in the DB must not require a
# hand-written code declaration to work." Some tools share ONE implementation
# and are dispatched purely by name: the canonical case is the bundle listers
# (``bundle:list_<name>``) — one ``list_bundle_tools`` handler backs N
# data-driven ``tool_def`` rows. Declaring N identical ``@tool`` lines (one per
# member) is duplication that breaks the instant a member is added to the DB the
# natural, data-driven way. A family is declared ONCE via :func:`tool_family`;
# every member is then pure data. Both the runtime registry (callable
# resolution) and the drift validator resolve a member through the family, so a
# family member and a singly-declared tool are indistinguishable downstream.


@dataclass(frozen=True)
class DeclaredFamily:
    """A generic family of tools sharing one implementation, matched by name prefix."""

    name_prefix: str
    source_kind: str
    args_model: type[BaseModel]
    func: Callable[..., Any]
    module: str
    qualname: str
    executor: str | None
    validate: bool
    deprecated: bool

    @property
    def function_path(self) -> str:
        return f"{self.module}.{self.qualname}"

    def matches(self, name: str) -> bool:
        return name.startswith(self.name_prefix)

    def as_declared(self, name: str) -> DeclaredTool:
        """Materialise the family as a concrete :class:`DeclaredTool` for ``name``
        so callers can treat a family member exactly like a singly-declared tool."""
        return DeclaredTool(
            name=name,
            source_kind=self.source_kind,
            args_model=self.args_model,
            func=self.func,
            module=self.module,
            qualname=self.qualname,
            executor=self.executor,
            validate=self.validate,
            deprecated=self.deprecated,
        )


_FAMILY_REGISTRY: list[DeclaredFamily] = []


def tool_family(
    *,
    name_prefix: str,
    source_kind: str,
    args: type[BaseModel] = NoArgs,
    executor: str | None = None,
    validate: bool = True,
    deprecated: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Declare ``fn`` as the shared implementation of every tool whose name starts
    with ``name_prefix``. Unlike :func:`tool`, NO per-member declaration is needed:
    members are created as pure ``tool_def`` rows and resolve to this one handler.

    Args mirror :func:`tool`; ``name_prefix`` replaces the exact ``name``. A second
    family claiming the same prefix with a different function is a hard error — a
    prefix maps to exactly one implementation.
    """

    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        fam = DeclaredFamily(
            name_prefix=name_prefix,
            source_kind=source_kind,
            args_model=args,
            func=fn,
            module=fn.__module__,
            qualname=fn.__qualname__,
            executor=executor,
            validate=validate,
            deprecated=deprecated,
        )
        for existing in _FAMILY_REGISTRY:
            if existing.name_prefix == name_prefix and existing.function_path != fam.function_path:
                raise ToolDeclarationError(
                    f"Tool family prefix {name_prefix!r} is declared by two different "
                    f"functions: {existing.function_path} and {fam.function_path}. "
                    "A family prefix must map to exactly one implementation."
                )
        # Idempotent on re-import: drop any prior same-prefix entry, then append.
        _FAMILY_REGISTRY[:] = [f for f in _FAMILY_REGISTRY if f.name_prefix != name_prefix]
        _FAMILY_REGISTRY.append(fam)
        fn.__matrx_tool_family__ = fam  # type: ignore[attr-defined]
        return fn

    return deco


def declared_families() -> list[DeclaredFamily]:
    """Return a copy of the registered tool families."""
    return list(_FAMILY_REGISTRY)


def match_family(name: str) -> DeclaredFamily | None:
    """Return the family whose prefix matches ``name`` (longest prefix wins for
    determinism), or ``None`` when no family applies."""
    best: DeclaredFamily | None = None
    for fam in _FAMILY_REGISTRY:
        if fam.matches(name) and (best is None or len(fam.name_prefix) > len(best.name_prefix)):
            best = fam
    return best


def get_effective_declared(name: str) -> DeclaredTool | None:
    """The single funnel for "what code backs this tool name?" — an exact ``@tool``
    declaration if present, else a matching ``@tool_family`` materialised for this
    name, else ``None``."""
    dt = _REGISTRY.get(name)
    if dt is not None:
        return dt
    fam = match_family(name)
    return fam.as_declared(name) if fam is not None else None


def clear_registry() -> None:
    """Test helper — wipe the registry between isolated runs."""
    _REGISTRY.clear()
    _FAMILY_REGISTRY.clear()
