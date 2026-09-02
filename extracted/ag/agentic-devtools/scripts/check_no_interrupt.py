"""Check that no interrupt() calls exist in the orchestration package.

AST-scans all *.py files under agentic_devtools/orchestration/ for runtime
interrupt() calls using these detection patterns:
  - Direct call: interrupt(...)
  - Aliased import: from langgraph.types import interrupt as <alias>
  - Attribute access: langgraph.types.interrupt(...)
  - Module alias: import langgraph.types as X; X.interrupt(...)
  - Sub-module import: from langgraph import types; types.interrupt(...)

Exit codes:
  0 — No interrupt() usage found.
  1 — One or more interrupt() calls detected.
"""

import ast
import sys
from pathlib import Path

ORCHESTRATION_DIR = Path("agentic_devtools/orchestration")


def _find_interrupt_aliases(tree: ast.Module) -> set[str]:
    """Find all names bound to the ``interrupt`` symbol from langgraph.types.

    Handles ``from langgraph.types import interrupt [as <alias>]``.
    """
    aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "langgraph.types":
            for alias in node.names:
                if alias.name == "interrupt":
                    aliases.add(alias.asname or alias.name)
    return aliases


def _find_langgraph_types_aliases(tree: ast.Module) -> set[str]:
    """Find all names that refer to the ``langgraph.types`` module itself.

    Handles::

        import langgraph.types as X          -> X
        from langgraph import types          -> types
        from langgraph import types as t     -> t
    """
    aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "langgraph.types" and alias.asname:
                    aliases.add(alias.asname)
        if isinstance(node, ast.ImportFrom) and node.module is not None and node.module == "langgraph":
            for alias in node.names:
                if alias.name == "types":
                    aliases.add(alias.asname or alias.name)
    return aliases


def _is_langgraph_types_interrupt(func_node: ast.Attribute) -> bool:
    """Return True only for the langgraph.types.interrupt(...) attribute chain."""
    return (
        func_node.attr == "interrupt"
        and isinstance(func_node.value, ast.Attribute)
        and func_node.value.attr == "types"
        and isinstance(func_node.value.value, ast.Name)
        and func_node.value.value.id == "langgraph"
    )


def _check_file(filepath: Path) -> list[str]:
    """Check a single file for interrupt() calls. Returns list of violation messages."""
    source = filepath.read_text()
    tree = ast.parse(source, filename=str(filepath))
    violations: list[str] = []

    # Find any names bound to the interrupt symbol
    aliases = _find_interrupt_aliases(tree)
    # Find any names that refer to the langgraph.types module
    module_aliases = _find_langgraph_types_aliases(tree)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        # Direct call: interrupt(...) or alias(...)
        if isinstance(node.func, ast.Name):
            if node.func.id in aliases or node.func.id == "interrupt":
                violations.append(f"{filepath}:{node.lineno}: interrupt() call via '{node.func.id}'")

        # Attribute access: langgraph.types.interrupt(...) — narrowed to avoid
        # false positives from unrelated .interrupt() methods
        if isinstance(node.func, ast.Attribute) and _is_langgraph_types_interrupt(node.func):
            violations.append(f"{filepath}:{node.lineno}: interrupt() call via langgraph.types.interrupt")

        # Attribute access via module alias: alias.interrupt(...)
        # e.g. import langgraph.types as lg_types -> lg_types.interrupt(...)
        #      from langgraph import types        -> types.interrupt(...)
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "interrupt"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in module_aliases
        ):
            violations.append(f"{filepath}:{node.lineno}: interrupt() call via '{node.func.value.id}.interrupt'")

    return violations


def main() -> int:
    """Scan all Python files in the orchestration package."""
    if not ORCHESTRATION_DIR.exists():
        print(f"ERROR: {ORCHESTRATION_DIR} not found", file=sys.stderr)
        return 1

    all_violations: list[str] = []
    py_files = sorted(ORCHESTRATION_DIR.rglob("*.py"))

    for filepath in py_files:
        violations = _check_file(filepath)
        all_violations.extend(violations)

    if all_violations:
        for v in all_violations:
            print(f"FAIL: {v}", file=sys.stderr)
        print(f"\n{len(all_violations)} interrupt() usage(s) found.", file=sys.stderr)
        return 1

    print(f"OK: No interrupt() calls found in {len(py_files)} files under {ORCHESTRATION_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
