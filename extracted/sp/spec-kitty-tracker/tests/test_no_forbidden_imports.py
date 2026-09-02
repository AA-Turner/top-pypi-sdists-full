"""N21: spec_kitty_tracker imports no core/SaaS/events/framework module.

TRK-M1-01 draft N21: "AST scan of src/spec_kitty_tracker forbids
specify_cli, apps, django, spec_kitty_events". This is the dependency-
direction half of TRK-M1-02's REQ-03 ("Provider-neutral protocol/registry;
no specify_cli/apps/spec_kitty_events imports"): Tracker owns its
contracts and must not import consumer implementation modules (Core/SaaS,
TRACKER_ARCH_ROLE.md:64-71) or a product-domain event package
(spec_kitty_events, A15 — the event/time seam means Tracker takes no
dependency on it).

Complements tests/test_no_rollout_in_tracker.py (which bans env-var
access patterns) with an import-direction guard.
"""

from __future__ import annotations

import ast
from pathlib import Path

TRACKER_SRC = Path(__file__).parent.parent / "src" / "spec_kitty_tracker"

FORBIDDEN_TOP_LEVEL_MODULES: frozenset[str] = frozenset(
    {
        "specify_cli",
        "apps",
        "django",
        "spec_kitty_events",
    }
)


def _top_level_module_names(tree: ast.Module) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        # Relative imports (node.level > 0) are intra-package and cannot
        # reach a forbidden top-level module.
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module is not None:
            names.add(node.module.split(".")[0])
    return names


def test_tracker_source_imports_no_forbidden_module() -> None:
    assert TRACKER_SRC.is_dir(), f"Expected tracker source at {TRACKER_SRC}"

    py_files = sorted(TRACKER_SRC.rglob("*.py"))
    assert py_files, f"No .py files found under {TRACKER_SRC} — package layout is broken"

    violations: list[str] = []
    for py_file in py_files:
        tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        hit = _top_level_module_names(tree) & FORBIDDEN_TOP_LEVEL_MODULES
        if hit:
            rel = py_file.relative_to(TRACKER_SRC.parent.parent)
            violations.append(f"  {rel}: imports forbidden module(s) {sorted(hit)}")

    assert not violations, (
        "spec_kitty_tracker must not import core/SaaS/events/framework modules "
        "(TRK-M1-01 draft N21; TRACKER_ARCH_ROLE.md:64-71 — Tracker must not "
        "import core or SaaS implementation modules; A15 — no spec_kitty_events "
        "dependency):\n" + "\n".join(violations)
    )
