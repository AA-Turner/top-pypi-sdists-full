"""Auto-verification loop after every code change.

When sage writes a file, run the project's tests/typecheck/lint and feed
failures back to the model. Three iterations of this routinely beats one
shot from a much bigger model.

Detects test/lint commands from `package.json`, `pyproject.toml`, common
filenames (`pytest.ini`, `Makefile`). Falls back to no-op (returns ok=True)
when no command can be inferred — refuses to fail-closed when there's
nothing to run.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

__all__ = ["VerifyOutcome", "ProjectVerifier", "infer_test_command"]


@dataclass
class VerifyOutcome:
    ok: bool
    command: str
    stdout_tail: str
    stderr_tail: str
    duration_s: float
    skipped_reason: str = ""


def _read_json_safe(p: Path) -> dict:
    try:
        return json.loads(p.read_text("utf-8"))
    except Exception:
        return {}


def infer_test_command(cwd: Path) -> list[str] | None:
    """Best-effort guess at the project's test command."""
    cwd = cwd.resolve()
    # Python
    if (cwd / "pyproject.toml").exists() or (cwd / "pytest.ini").exists():
        if shutil.which("pytest"):
            return ["pytest", "-x", "-q"]
    if (cwd / "tox.ini").exists() and shutil.which("tox"):
        return ["tox", "-q"]
    # JS/TS
    pkg = cwd / "package.json"
    if pkg.exists():
        data = _read_json_safe(pkg)
        scripts = data.get("scripts") or {}
        if "test" in scripts:
            # Prefer the package manager declared by lockfile
            if (cwd / "pnpm-lock.yaml").exists() and shutil.which("pnpm"):
                return ["pnpm", "test", "--", "--run"] if "vitest" in scripts.get("test", "") else ["pnpm", "test"]
            if (cwd / "yarn.lock").exists() and shutil.which("yarn"):
                return ["yarn", "test"]
            if shutil.which("npm"):
                return ["npm", "test", "--silent"]
    # Rust
    if (cwd / "Cargo.toml").exists() and shutil.which("cargo"):
        return ["cargo", "test", "--quiet"]
    # Go
    if (cwd / "go.mod").exists() and shutil.which("go"):
        return ["go", "test", "./..."]
    # Make
    if (cwd / "Makefile").exists() and shutil.which("make"):
        return ["make", "test"]
    return None


def _tail(s: str, n: int = 60) -> str:
    lines = s.splitlines()
    return "\n".join(lines[-n:])


class ProjectVerifier:
    """Runs the inferred test/lint command and returns a structured result."""

    def __init__(self, cwd: Path, *, timeout_s: float = 90.0):
        self.cwd = cwd
        self.timeout_s = timeout_s

    def run(self) -> VerifyOutcome:
        import time
        cmd = infer_test_command(self.cwd)
        if cmd is None:
            return VerifyOutcome(
                ok=True, command="", stdout_tail="", stderr_tail="",
                duration_s=0.0, skipped_reason="no test command inferred",
            )
        t0 = time.time()
        try:
            r = subprocess.run(
                cmd, cwd=str(self.cwd),
                capture_output=True, text=True, timeout=self.timeout_s,
                stdin=subprocess.DEVNULL,
            )
            return VerifyOutcome(
                ok=(r.returncode == 0), command=" ".join(cmd),
                stdout_tail=_tail(r.stdout), stderr_tail=_tail(r.stderr),
                duration_s=time.time() - t0,
            )
        except subprocess.TimeoutExpired:
            return VerifyOutcome(
                ok=False, command=" ".join(cmd), stdout_tail="",
                stderr_tail=f"TIMEOUT after {self.timeout_s}s",
                duration_s=time.time() - t0,
            )
        except FileNotFoundError as exc:
            return VerifyOutcome(
                ok=False, command=" ".join(cmd), stdout_tail="",
                stderr_tail=str(exc), duration_s=time.time() - t0,
            )

    def loop(
        self,
        *,
        regenerate_fn,
        max_iterations: int = 3,
    ) -> tuple[VerifyOutcome, list[VerifyOutcome]]:
        """Run, and if failing, call regenerate_fn(stderr_tail) up to max_iterations.

        regenerate_fn is expected to apply a code fix; we just measure.
        Returns (final_outcome, history).
        """
        history: list[VerifyOutcome] = []
        outcome = self.run()
        history.append(outcome)
        i = 0
        while not outcome.ok and outcome.command and i < max_iterations:
            try:
                regenerate_fn(outcome.stderr_tail or outcome.stdout_tail)
            except Exception:
                break
            outcome = self.run()
            history.append(outcome)
            i += 1
        return outcome, history
