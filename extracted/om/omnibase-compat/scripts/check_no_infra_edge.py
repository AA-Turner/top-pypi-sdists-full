#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Assert omnibase_compat has no omnibase_infra edge in its dependency closure.

Durability-plan Task 3.1 (OMN-12599): the compat compatibility gate must run
without importing, installing, or resolving ``omnibase_infra``. The pre-existing
``validate_no_upstream_deps.py`` only scans ``import`` statements in ``src/``; it
does not catch an ``omnibase_infra`` package that is *declared* in
``pyproject.toml`` or *resolved* into ``uv.lock`` without an explicit import.
Such a declared-but-unimported edge still forces the gate to install/resolve
infra, which is exactly the invariant this guard exists to prevent.

This guard scans the full dependency closure:

* every ``[project.dependencies]`` entry,
* every ``[project.optional-dependencies]`` group entry,
* every ``[dependency-groups]`` entry,
* every locked package ``name`` in ``uv.lock``.

It fails fast (exit 1) if any forbidden upstream package name appears in any of
those surfaces. The package's own name (``omnibase-compat``) is never a
violation.

Run: ``python scripts/check_no_infra_edge.py``

The closure-scan logic is importable (``scan_dependency_closure``) so the guard
can be exercised against synthetic fixtures from tests.
"""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

# Forbidden upstream package distribution names (PEP 503 normalized comparison
# treats '-' and '_' as equivalent). omnibase_infra is the primary target of the
# no-infra-edge invariant; the sibling upstream packages are included because the
# compat package's zero-upstream-dependency contract forbids all of them.
FORBIDDEN_PACKAGES: tuple[str, ...] = (
    "omnibase-infra",
    "omnibase-core",
    "omnibase-spi",
)

# The package itself is always allowed in its own lock/metadata.
SELF_PACKAGE = "omnibase-compat"


def _normalize(name: str) -> str:
    """PEP 503 style normalization for distribution name comparison."""
    return name.strip().lower().replace("_", "-")


def _requirement_name(requirement: str) -> str:
    """Extract the bare distribution name from a PEP 508 requirement string."""
    # Strip extras, version specifiers, markers, and URLs. The distribution name
    # is the leading run before any of: [ ( < > = ! ~ ; @ space.
    name = requirement.strip()
    for sep in ("[", "(", "<", ">", "=", "!", "~", ";", "@", " "):
        idx = name.find(sep)
        if idx != -1:
            name = name[:idx]
    return _normalize(name)


def _collect_pyproject_requirement_names(pyproject_path: Path) -> set[str]:
    """Return normalized distribution names declared anywhere in pyproject."""
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    names: set[str] = set()

    project = data.get("project", {})
    for req in project.get("dependencies", []):
        names.add(_requirement_name(req))
    for group in project.get("optional-dependencies", {}).values():
        for req in group:
            names.add(_requirement_name(req))

    for group in data.get("dependency-groups", {}).values():
        for req in group:
            # dependency-groups entries may be strings or {include-group: ...}
            # mapping tables; only string requirements name a distribution.
            if isinstance(req, str):
                names.add(_requirement_name(req))

    return names


def _collect_lock_package_names(lock_path: Path) -> set[str]:
    """Return normalized package names locked in uv.lock."""
    if not lock_path.exists():
        return set()
    data = tomllib.loads(lock_path.read_text(encoding="utf-8"))
    return {_normalize(pkg["name"]) for pkg in data.get("package", []) if "name" in pkg}


def scan_dependency_closure(repo_root: Path) -> list[str]:
    """Scan pyproject + uv.lock for forbidden upstream edges.

    Returns a list of human-readable violation strings (empty when clean).
    """
    forbidden = {_normalize(p) for p in FORBIDDEN_PACKAGES}
    self_name = _normalize(SELF_PACKAGE)
    violations: list[str] = []

    pyproject_path = repo_root / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {pyproject_path}")

    declared = _collect_pyproject_requirement_names(pyproject_path)
    for name in sorted(declared & forbidden):
        violations.append(f"pyproject.toml declares forbidden dependency: {name}")

    locked = _collect_lock_package_names(repo_root / "uv.lock")
    for name in sorted((locked & forbidden) - {self_name}):
        violations.append(f"uv.lock resolves forbidden package into closure: {name}")

    return violations


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    violations = scan_dependency_closure(repo_root)
    if violations:
        print("FAIL — omnibase_infra (or sibling upstream) edge found in closure:")
        for v in violations:
            print(f"  {v}")
        print()
        print("The compat compatibility gate must validate without resolving or")
        print("installing omnibase_infra. Remove the upstream edge from")
        print("pyproject.toml and re-lock (uv lock) to restore the invariant.")
        return 1

    print("OK — no omnibase_infra/core/spi edge in pyproject dependencies or uv.lock closure.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
