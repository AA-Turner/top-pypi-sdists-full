"""GUARD: every surface-writing tool attaches the before → after receipt.

Why it exists (Arman, 2026-09-26): *"I had it built and fully used everywhere
but devs have stopped using it and now it's lost."* The diff card in the chat
renders from ONE receipt (`matrx_ai.tools.surface_write`); a writer that stops
attaching it silently reverts to "new text only". This guard fails when:

  A. a tool declared in SURFACE_WRITE_TOOLS no longer attaches a receipt
     (directly or by forwarding to `context_patch`);
  B. a registered tool whose name reads like a write — or a listed dispatcher
     write action — is declared nowhere (a new writer slipped in unseen);
  C. a PENDING entry already attaches (the gap list only shrinks: move it).
"""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import pytest

from matrx_ai.tools.surface_write import (
    PENDING_SURFACE_WRITES,
    SURFACE_WRITE_TOOLS,
)

#: Calls that mean "this function hands a receipt to the executor".
_RECEIPT_CALLS = frozenset(
    {"attach_surface_write", "_with_surface_write", "_forward_to_patch", "context_patch"}
)
_PKG = Path(__file__).resolve().parents[1]

def _module_path(module: str) -> Path:
    if module.startswith("aidream."):
        # The host's modules are read from the monorepo checkout, never imported
        # (a matrx-ai test does not import aidream).
        base = _PKG.parents[1].joinpath(*module.split("."))
        path = base.with_suffix(".py")
        if not path.exists() and (base / "__init__.py").exists():
            path = base / "__init__.py"
        if not path.exists():
            pytest.skip(f"{module} is not in this checkout")
        return path
    spec = importlib.util.find_spec(module)
    assert spec and spec.origin, f"{module} not importable"
    return Path(spec.origin)


def _module_index(module: str) -> tuple[dict[str, ast.AST], dict[str, str]]:
    tree = ast.parse(_module_path(module).read_text(encoding="utf-8"))
    defs = {
        n.name: n
        for n in ast.walk(tree)
        if isinstance(n, (ast.AsyncFunctionDef, ast.FunctionDef))
    }
    imports = {
        alias.asname or alias.name: n.module
        for n in ast.walk(tree)
        if isinstance(n, ast.ImportFrom) and n.module and n.level == 0
        for alias in n.names
    }
    return defs, imports


def _function_calls(module: str, func: str, *, depth: int = 4) -> set[str]:
    """Every call name reachable from ``func``, following helpers defined in the
    same module and helpers imported from first-party modules (a dispatcher
    wrapping its ``_impl``, a shared attach helper in a sibling module)."""
    cache: dict[str, tuple[dict[str, ast.AST], dict[str, str]]] = {}

    def index(mod: str) -> tuple[dict[str, ast.AST], dict[str, str]] | None:
        if mod not in cache:
            if mod != module:
                try:
                    cache[mod] = _module_index(mod)
                except BaseException:  # noqa: BLE001 — an unreadable helper module is just not followed
                    return None
            else:
                cache[mod] = _module_index(mod)
        return cache[mod]

    root = index(module)
    assert root and func in root[0], f"{module}.{func} not found"
    seen: set[tuple[str, str]] = set()
    names: set[str] = set()
    frontier = [(module, func)]
    for _ in range(depth + 1):
        nxt: list[tuple[str, str]] = []
        for mod, name in frontier:
            idx = index(mod)
            if (mod, name) in seen or idx is None or name not in idx[0]:
                continue
            seen.add((mod, name))
            defs, imports = idx
            for sub in ast.walk(defs[name]):
                if not isinstance(sub, ast.Call):
                    continue
                f = sub.func
                called = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
                if not called:
                    continue
                names.add(called)
                source = imports.get(called)
                if source and source.split(".")[0] in {"aidream", "matrx_ai"}:
                    nxt.append((source, called))
                else:
                    nxt.append((mod, called))
        frontier = nxt
    return names


@pytest.mark.parametrize("tool", sorted(SURFACE_WRITE_TOOLS))
def test_declared_surface_writer_attaches_a_receipt(tool: str) -> None:
    module, func = SURFACE_WRITE_TOOLS[tool]
    calls = _function_calls(module, func)
    assert calls & _RECEIPT_CALLS or any(c.endswith("surface_write") for c in calls), (
        f"{tool} ({module}.{func}) writes a surface but attaches no surface-write receipt, "
        "so its chat card falls back to showing only the new text. Remedy: return "
        "attach_surface_write(result, before=..., after=..., ...) on success."
    )


# Discovery of EVERY tool action (not just write-shaped names) lives in the host,
# which can import both declaration modules:
# aidream/tools/tests/test_every_tool_action_is_classified.py


def test_pending_list_only_shrinks() -> None:
    overlap = set(PENDING_SURFACE_WRITES) & set(SURFACE_WRITE_TOOLS)
    assert not overlap, f"{sorted(overlap)} are both wired and pending — delete the pending row."


def test_nothing_is_pending() -> None:
    """Arman, 2026-09-26: "any tool that overwrites" — the gap list ends empty.
    A new writer that cannot attach a receipt yet is a defect to fix, not a row."""
    assert not PENDING_SURFACE_WRITES, sorted(PENDING_SURFACE_WRITES)
