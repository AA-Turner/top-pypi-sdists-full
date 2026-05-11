"""Item #16 — Type-check-aware code generation."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

__all__ = ["TypeCheckResult", "run_type_check"]


@dataclass
class TypeCheckResult:
    checked: bool
    skipped: bool
    errors: list[str]
    detail: str = ""


def run_type_check(project_root: Path, *, language: str = "python") -> TypeCheckResult:
    if language == "python":
        if shutil.which("pyright"):
            try:
                r = subprocess.run(
                    ["pyright", str(project_root)],
                    capture_output=True, text=True, timeout=60,
                )
                errors = [l for l in r.stdout.splitlines() if "error" in l.lower()]
                return TypeCheckResult(
                    checked=True, skipped=False,
                    errors=errors,
                    detail=r.stdout[-500:],
                )
            except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
                return TypeCheckResult(
                    checked=False, skipped=True,
                    errors=[], detail=f"pyright failed: {exc}",
                )
        if shutil.which("mypy"):
            try:
                r = subprocess.run(
                    ["mypy", str(project_root)],
                    capture_output=True, text=True, timeout=60,
                )
                errors = [l for l in r.stdout.splitlines() if "error:" in l]
                return TypeCheckResult(
                    checked=True, skipped=False,
                    errors=errors,
                    detail=r.stdout[-500:],
                )
            except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
                return TypeCheckResult(
                    checked=False, skipped=True,
                    errors=[], detail=f"mypy failed: {exc}",
                )
        return TypeCheckResult(
            checked=False, skipped=True,
            errors=[], detail="no type checker installed (pyright or mypy)",
        )
    if language in {"typescript", "ts", "javascript"}:
        if shutil.which("tsc"):
            try:
                r = subprocess.run(
                    ["tsc", "--noEmit"],
                    cwd=str(project_root),
                    capture_output=True, text=True, timeout=60,
                )
                errors = [l for l in r.stdout.splitlines() if "error TS" in l]
                return TypeCheckResult(
                    checked=True, skipped=False,
                    errors=errors,
                    detail=r.stdout[-500:],
                )
            except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
                return TypeCheckResult(
                    checked=False, skipped=True,
                    errors=[], detail=f"tsc failed: {exc}",
                )
        return TypeCheckResult(
            checked=False, skipped=True,
            errors=[], detail="tsc not installed",
        )
    return TypeCheckResult(
        checked=False, skipped=True,
        errors=[], detail=f"unknown language: {language}",
    )
