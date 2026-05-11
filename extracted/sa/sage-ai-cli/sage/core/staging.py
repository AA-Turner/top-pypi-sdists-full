"""T5 — Tmpdir staging for all writes.

Every batch of writes goes through an isolated tmpdir that mirrors the
real cwd. Validators run there, tests run there. Only on full success
does the change apply to the real repo. Fixes the Novellia class of bug
where partial garbage corrupts the user's actual project.

Usage:
    with StagingArea(cwd) as stage:
        ok = stage.stage_write("src/server.js", content, validate=True)
        if not ok:
            # Validator rejected — nothing applied to real repo
            pass
        result = stage.run(["pytest"])
        if result.returncode == 0:
            stage.commit()   # apply to real repo
        # else: context exit drops the tmpdir; real repo untouched
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from sage.core.content_validator import validate_content

__all__ = ["StagingArea", "StagedRunResult"]


# Directories we never copy into staging — they're heavy, vendored, or
# generated, and the staged tests don't need them.
_EXCLUDE_DIRS = frozenset({
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "dist", "build", "target", ".next", ".nuxt", ".cache",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "vendor", "third_party", "coverage",
})


@dataclass
class StagedRunResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


class StagingArea:
    """Isolated tmpdir copy of the cwd. Writes there; commit on success."""

    def __init__(self, cwd: Path, *, root: Path | None = None):
        self.cwd = cwd.resolve()
        self._root_override = root
        self._tmp: tempfile.TemporaryDirectory | None = None
        self._root: Path | None = None
        self._writes: dict[str, str | None] = {}  # rel_path → content (None = delete)
        self._committed = False

    @property
    def root(self) -> Path:
        if self._root is None:
            raise RuntimeError("StagingArea not entered — use `with StagingArea(cwd):`")
        return self._root

    def __enter__(self) -> "StagingArea":
        if self._root_override is not None:
            self._root_override.mkdir(parents=True, exist_ok=True)
            self._root = self._root_override
        else:
            self._tmp = tempfile.TemporaryDirectory(prefix="sage-stage-")
            self._root = Path(self._tmp.name)
        # Mirror existing files into the staging area (skip excluded dirs)
        if self.cwd.is_dir():
            shutil.copytree(
                self.cwd, self._root, dirs_exist_ok=True,
                ignore=lambda src, names: [n for n in names if n in _EXCLUDE_DIRS],
            )
        return self

    def __exit__(self, *exc_info) -> bool:
        if self._tmp is not None:
            self._tmp.cleanup()
        self._root = None
        return False

    # ── Stage operations ───────────────────────────────────────────

    def stage_write(self, relpath: str, content: str, *,
                    validate: bool = True) -> bool:
        """Write to the staging area only. Returns False if validator rejected."""
        if validate:
            result = validate_content(relpath, content)
            if not result.ok:
                # Don't write the staged file at all — caller can inspect via
                # stage_was_rejected if needed
                return False
        target = self.root / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        self._writes[relpath] = content
        return True

    def stage_delete(self, relpath: str) -> None:
        target = self.root / relpath
        if target.exists():
            target.unlink()
        self._writes[relpath] = None

    def run(self, cmd: list[str], *, timeout: float = 60.0,
            env: dict | None = None) -> StagedRunResult:
        """Run a command inside the staging area."""
        try:
            r = subprocess.run(
                cmd, cwd=str(self.root),
                capture_output=True, text=True, timeout=timeout,
                env=env if env is not None else os.environ.copy(),
            )
            return StagedRunResult(
                returncode=r.returncode, stdout=r.stdout, stderr=r.stderr,
            )
        except subprocess.TimeoutExpired as exc:
            return StagedRunResult(
                returncode=-9, stdout=exc.stdout or "", stderr=exc.stderr or "",
                timed_out=True,
            )

    # ── Commit ─────────────────────────────────────────────────────

    def commit(self) -> list[str]:
        """Apply all staged writes to the real cwd. Returns the list of files
        actually written/deleted."""
        applied: list[str] = []
        for relpath, content in self._writes.items():
            target = self.cwd / relpath
            if content is None:
                if target.exists():
                    target.unlink()
                    applied.append(relpath)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                applied.append(relpath)
        self._committed = True
        return applied
