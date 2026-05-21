"""Install + verify orchestrator.

Discovers every project under a root directory and runs the appropriate
toolchain (install → test → lint → typecheck → format) against each one.
Captures stdout+stderr per step in structured `StepResult` records the
verify loop in `build_project` can feed back to the LLM for fixes.

This module is the answer to the user's complaint that "neither the
frontend nor backend was installed by sage in order to test and run the
code" and "How can sage test its code if it never installed its code."
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


ProjectKind = Literal["python", "node", "go", "rust", "java", "kotlin", "ruby"]


@dataclass
class DiscoveredProject:
    kind: ProjectKind
    root: Path
    extras: dict[str, str] = field(default_factory=dict)


@dataclass
class StepResult:
    name: str
    ok: bool
    log: str
    duration_s: float
    returncode: int = 0


@dataclass
class VerifyReport:
    project: DiscoveredProject
    steps: list[StepResult]

    @property
    def install_ok(self) -> bool | None:
        for s in self.steps:
            if "install" in s.name.lower():
                return s.ok
        return None

    @property
    def tests_ok(self) -> bool | None:
        for s in self.steps:
            if s.name.lower() in {"pytest", "npm test", "go test", "cargo test"}:
                return s.ok
        return None

    @property
    def all_ok(self) -> bool:
        return all(s.ok for s in self.steps)


# Directories we always skip when discovering projects — they contain
# *installed* packages, not source projects.
_SKIP_DIRS: frozenset[str] = frozenset(
    {
        "node_modules", "venv", ".venv", "env", ".env", "build", "dist",
        ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache",
        "__pycache__", ".next", ".expo", "target", "out", "bin",
    }
)


# ──────────────────────── discovery ────────────────────────────────────


def discover_projects(root: Path) -> list[DiscoveredProject]:
    """Walk `root` and return one DiscoveredProject per detected sub-project.

    Detection markers (in priority order, first hit wins per directory):
      - package.json        → node
      - pyproject.toml      → python
      - requirements.txt    → python
      - go.mod              → go
      - Cargo.toml          → rust
      - pom.xml / build.gradle* → java/kotlin

    Skips any directory inside `_SKIP_DIRS` (notably node_modules, venv).
    Multiple markers in the same directory produce ONE project — we pick
    the most specific.
    """
    root = root.resolve()
    found: list[DiscoveredProject] = []
    seen_roots: set[Path] = set()

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skipped dirs in-place so os.walk doesn't recurse into them
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS and not d.startswith(".")]

        here = Path(dirpath)
        if here in seen_roots:
            continue

        kind: ProjectKind | None = None
        if "package.json" in filenames:
            kind = "node"
        elif "pyproject.toml" in filenames or "requirements.txt" in filenames:
            kind = "python"
        elif "go.mod" in filenames:
            kind = "go"
        elif "Cargo.toml" in filenames:
            kind = "rust"
        elif "pom.xml" in filenames or any(
            f.startswith("build.gradle") for f in filenames
        ):
            kind = "java"
        if kind:
            found.append(DiscoveredProject(kind=kind, root=here))
            seen_roots.add(here)

    return found


# ──────────────────────── step runner ──────────────────────────────────


def run_step(
    name: str,
    cmd: list[str],
    *,
    cwd: Path,
    timeout: int = 600,
    env: dict[str, str] | None = None,
) -> StepResult:
    """Run a shell command and capture the result. Never raises."""
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=full_env,
            check=False,
        )
        log = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        return StepResult(
            name=name,
            ok=proc.returncode == 0,
            log=log,
            duration_s=time.monotonic() - start,
            returncode=proc.returncode,
        )
    except FileNotFoundError as exc:
        return StepResult(
            name=name,
            ok=False,
            log=f"command not found: {exc}",
            duration_s=time.monotonic() - start,
            returncode=127,
        )
    except subprocess.TimeoutExpired:
        return StepResult(
            name=name,
            ok=False,
            log=f"timeout after {timeout}s",
            duration_s=time.monotonic() - start,
            returncode=124,
        )
    except Exception as exc:  # noqa: BLE001 — verification must NEVER crash
        return StepResult(
            name=name,
            ok=False,
            log=f"unexpected error: {exc}",
            duration_s=time.monotonic() - start,
            returncode=1,
        )


# ──────────────────────── per-language verify ──────────────────────────


def _has_script(package_json: Path, script: str) -> bool:
    try:
        data = json.loads(package_json.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return script in (data.get("scripts") or {})


def _verify_python(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root

    has_req = (root / "requirements.txt").exists()
    has_pyproject = (root / "pyproject.toml").exists()

    # 1. Install runtime deps (prefer requirements.txt for fast/exact install,
    # fall back to pyproject if absent)
    pip = [sys.executable, "-m", "pip"]
    if has_req:
        steps.append(
            run_step(
                "pip install",
                pip + ["install", "-r", "requirements.txt", "--quiet"],
                cwd=root,
                timeout=900,
            )
        )
    if has_pyproject:
        # Also install the package itself so tests can import `app.*`
        steps.append(
            run_step(
                "pip install -e .[dev]",
                pip + ["install", "-e", ".[dev]", "--quiet"],
                cwd=root,
                timeout=900,
            )
        )

    # 2. Run tests
    steps.append(
        run_step(
            "pytest",
            [sys.executable, "-m", "pytest", "-q"],
            cwd=root,
        )
    )

    # 3. Lint (only if ruff installed in this env)
    if shutil.which("ruff") or (root / ".venv" / "bin" / "ruff").exists():
        steps.append(run_step("ruff check", ["ruff", "check", "."], cwd=root))
    return steps


def _verify_node(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    pkg = root / "package.json"

    # 1. Install
    steps.append(
        run_step(
            "npm install",
            ["npm", "install", "--no-audit", "--no-fund"],
            cwd=root,
            timeout=1200,
        )
    )

    # 2. Test (only if defined)
    if _has_script(pkg, "test"):
        # Vitest rejects --watchAll (a Jest-only flag). Detect by checking
        # devDependencies for "vitest" and omit the flag for those projects.
        _is_vitest = False
        try:
            _pkg_data = json.loads(pkg.read_text("utf-8", errors="replace"))
            _deps = {
                **_pkg_data.get("devDependencies", {}),
                **_pkg_data.get("dependencies", {}),
            }
            _is_vitest = "vitest" in _deps
        except Exception:
            pass
        _test_cmd = (
            ["npm", "test", "--silent"]
            if _is_vitest
            else ["npm", "test", "--silent", "--", "--watchAll=false"]
        )
        steps.append(run_step("npm test", _test_cmd, cwd=root))

    # 3. Typecheck
    if _has_script(pkg, "typecheck"):
        steps.append(run_step("npm typecheck", ["npm", "run", "typecheck"], cwd=root))

    # 4. Lint
    if _has_script(pkg, "lint"):
        steps.append(run_step("npm lint", ["npm", "run", "lint"], cwd=root))

    return steps


def _verify_go(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    steps.append(run_step("go mod tidy", ["go", "mod", "tidy"], cwd=root))
    steps.append(run_step("go build", ["go", "build", "./..."], cwd=root))
    steps.append(run_step("go test", ["go", "test", "./..."], cwd=root))
    return steps


def _verify_rust(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    steps.append(run_step("cargo build", ["cargo", "build", "--quiet"], cwd=root))
    steps.append(run_step("cargo test", ["cargo", "test", "--quiet"], cwd=root))
    return steps


_VERIFIERS = {
    "python": _verify_python,
    "node": _verify_node,
    "go": _verify_go,
    "rust": _verify_rust,
}


def verify_project(project: DiscoveredProject) -> list[StepResult]:
    """Run install + test + lint for ONE project. Steps gated on tool/script availability."""
    fn = _VERIFIERS.get(project.kind)
    if not fn:
        return [
            StepResult(
                name=f"{project.kind} verifier",
                ok=False,
                log=f"no verifier registered for {project.kind}",
                duration_s=0.0,
                returncode=1,
            )
        ]
    return fn(project)


def verify_all(root: Path) -> list[VerifyReport]:
    """Discover every project under `root` and verify each."""
    reports: list[VerifyReport] = []
    for project in discover_projects(root):
        steps = verify_project(project)
        reports.append(VerifyReport(project=project, steps=steps))
    return reports


__all__ = [
    "DiscoveredProject",
    "ProjectKind",
    "StepResult",
    "VerifyReport",
    "discover_projects",
    "run_step",
    "verify_all",
    "verify_project",
]
