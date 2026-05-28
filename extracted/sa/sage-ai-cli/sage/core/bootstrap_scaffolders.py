"""Run real CLI scaffolders to bootstrap a project layout.

Production frameworks ship official scaffolders that produce correct
config (Expo's app.json with bundle IDs, splash, permissions; alembic's
versioned migrations directory). Sage uses them when available, falls
back to manual generation when the CLI isn't installed or the network
is offline.

The named `bootstrap_scaffolders` (not `bootstrap`) to avoid colliding
with the unrelated `sage.core.bootstrap` module that already exists for
session-init concerns.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class ScaffoldResult:
    name: str
    ran: bool
    ok: bool
    log: str
    files_touched: int = 0


def _run(cmd: list[str], cwd: Path, *, timeout: int = 600) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, check=False, timeout=timeout,
        )
        return proc.returncode == 0, (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)


def _has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


# ──────────────────────── Expo scaffold ────────────────────────────────


def scaffold_expo(out_dir: Path, *, log: Callable[[str], None]) -> ScaffoldResult:
    """Run `npx create-expo-app` so the frontend has the official Expo layout.

    Sage's hand-rolled package.json + tsconfig + babel.config is fine but
    misses pieces the real template includes: app.json with proper
    bundle identifiers + splash + icon + permissions, scripts/reset-project,
    .easignore. Running `create-expo-app` gives us that for free.

    If npx isn't available OR the network is offline, returns ran=False and
    the manual generation path takes over.
    """
    import os
    if os.environ.get("SAGE_TESTING") == "1":
        log("[bootstrap] SAGE_TESTING active — skipping Expo scaffold under test")
        return ScaffoldResult(name="create-expo-app", ran=False, ok=False, log="testing bypass")

    if not _has("npx") or not _has("node"):
        log("[bootstrap] npx not found — skipping Expo scaffold, manual gen will run")
        return ScaffoldResult(name="create-expo-app", ran=False, ok=False, log="npx missing")

    frontend = out_dir / "frontend"
    # If the user has already wiped + we're starting fresh, frontend doesn't
    # exist. We let create-expo-app create it.
    if frontend.exists() and any(frontend.iterdir()):
        log(f"[bootstrap] {frontend} already populated — skipping Expo scaffold")
        return ScaffoldResult(name="create-expo-app", ran=False, ok=False,
                              log="dir not empty")

    log("[bootstrap] running `npx create-expo-app frontend --template default --no-install`")
    ok, output = _run(
        ["npx", "--yes", "create-expo-app@latest", "frontend",
         "--template", "default", "--no-install"],
        cwd=out_dir,
        timeout=300,
    )
    if not ok:
        log("[bootstrap] create-expo-app failed; manual gen will run")
        return ScaffoldResult(name="create-expo-app", ran=True, ok=False, log=output[-2000:])

    touched = sum(1 for _ in frontend.rglob("*") if _.is_file())
    log(f"[bootstrap] Expo scaffold created {touched} files")
    return ScaffoldResult(
        name="create-expo-app", ran=True, ok=True, log=output[-1000:],
        files_touched=touched,
    )


# ──────────────────────── Alembic scaffold ─────────────────────────────


def scaffold_alembic(backend_dir: Path, *, log: Callable[[str], None]) -> ScaffoldResult:
    """Run `alembic init` so versioned migrations work out of the box.

    Falls back gracefully when alembic isn't installed in the host env.
    """
    import os
    if os.environ.get("SAGE_TESTING") == "1":
        log("[bootstrap] SAGE_TESTING active — skipping Alembic scaffold under test")
        return ScaffoldResult(name="alembic-init", ran=False, ok=False, log="testing bypass")

    if not _has("alembic"):
        # Try `python -m alembic` instead
        import sys
        ok, output = _run([sys.executable, "-m", "alembic", "--version"], backend_dir)
        if not ok:
            log("[bootstrap] alembic not available — manual gen will run")
            return ScaffoldResult(name="alembic-init", ran=False, ok=False, log="missing")

    if (backend_dir / "alembic" / "env.py").exists():
        log("[bootstrap] alembic/ already populated — skipping")
        return ScaffoldResult(name="alembic-init", ran=False, ok=False, log="exists")

    log("[bootstrap] running `alembic init -t async alembic`")
    cmd = ["alembic", "init", "-t", "async", "alembic"]
    if not _has("alembic"):
        import sys
        cmd = [sys.executable, "-m", "alembic", "init", "-t", "async", "alembic"]
    ok, output = _run(cmd, cwd=backend_dir, timeout=120)
    if not ok:
        log(f"[bootstrap] alembic init failed: {output[-500:]}")
        return ScaffoldResult(name="alembic-init", ran=True, ok=False, log=output[-1500:])
    return ScaffoldResult(name="alembic-init", ran=True, ok=True, log=output[-500:])


# ──────────────────────── public entry ─────────────────────────────────


def run_bootstrap(
    out_dir: Path,
    *,
    frontend: str | None,
    backend: str | None,
    log: Callable[[str], None],
) -> list[ScaffoldResult]:
    """Run every applicable scaffolder. Order matters (Expo before alembic).

    Sage's manual file emission later overwrites only files it owns
    (package.json from dep_resolver, alembic.ini from architecture_modules)
    so the scaffolder + manual approach compose without conflict.
    """
    results: list[ScaffoldResult] = []
    if frontend == "react-native-web":
        results.append(scaffold_expo(out_dir, log=log))
    if backend in {"fastapi", "django", "flask"}:
        backend_dir = out_dir / "backend"
        backend_dir.mkdir(parents=True, exist_ok=True)
        # Only run alembic init if a Python project file already exists
        # (so alembic doesn't reject the empty dir)
        if (backend_dir / "pyproject.toml").exists() or (backend_dir / "requirements.txt").exists():
            results.append(scaffold_alembic(backend_dir, log=log))
    return results


__all__ = ["ScaffoldResult", "run_bootstrap", "scaffold_alembic", "scaffold_expo"]
