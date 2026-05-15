"""Cross-file integrity pass for the dynamic builder.

The legacy `principal_engineer.build_project` already had a cross-file
integrity pass that detects dangling imports (importing a name a sibling
module doesn't define) + undefined names at module scope, and asks the
LLM to rewrite the offending file with the real sibling context.

The new `principal_builder.build_project_principal` skipped this pass.
This module wires it in. Runs between stage 7 (file generation) and
stage 8 (install + verify). Catches the systemic missing-imports problem
the overnight build hit (~30% of files used names like `get_current_user`,
`Index`, `bcrypt`, `crontab` without importing them).

Two passes:

1. **Cross-module dangling-import pass** — walks all generated Python
   files, finds `from app.X import Y` where module X doesn't actually
   export Y, regenerates the importing file with X's real contents in
   the prompt.

2. **Single-file undefined-name pass** — for each Python file, run AST
   bound/used analysis, detect names used at any scope that aren't
   bound. Regenerates the file with the undefined-name list fed back.

Caps total regen rounds (per pass and per file) so a misbehaving model
can't loop forever. Returns counts of files touched for the build
report.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from sage.core.pre_write_validator import validated_generate
from sage.core.principal_engineer import (
    _collect_module_symbols,
    _find_dangling_imports,
    _module_to_path,
    build_integrity_fix_prompt,
    build_lint_fix_prompt,
    detect_python_undefined_names,
    lint_python_file,
    strip_code_fences,
)


GenerateFn = Callable[[str], str]
ProgressFn = Callable[[str], None]


@dataclass
class IntegrityReport:
    """Counts of repairs performed across both passes."""
    dangling_fixes: int = 0
    lint_fixes: int = 0
    files_scanned: int = 0
    skipped_unparseable: int = 0


# ──────────────────────── package discovery ────────────────────────────


def _python_files_under(root: Path, package_dir: str = "app") -> dict[str, str]:
    """Read all .py files under `root/package_dir`, keyed by 'package/path/file.py'.

    Strips the `root` prefix so paths align with the module-path helper
    expectations: `app/api/v1/health.py` -> module `app.api.v1.health`.

    Filters out venvs, caches, and __pycache__ dirs.
    """
    pkg = root / package_dir
    if not pkg.is_dir():
        return {}

    files: dict[str, str] = {}
    for p in pkg.rglob("*.py"):
        if any(part in {"venv", ".venv", "__pycache__", "node_modules"}
               for part in p.parts):
            continue
        rel = p.relative_to(root)
        try:
            files[str(rel)] = p.read_text("utf-8", errors="replace")
        except OSError:
            continue
    return files


# ──────────────────────── dangling-import pass ─────────────────────────


def _run_dangling_pass(
    root: Path,
    *,
    generate: GenerateFn,
    log: ProgressFn,
    max_files: int = 50,
) -> int:
    """Find dangling imports across the project, regenerate offending files."""
    py_files = _python_files_under(root)
    if not py_files:
        return 0

    issues = _find_dangling_imports(py_files, project_root_pkg="app")
    if not issues:
        return 0

    # Group by importing file so we fix each at most once
    by_file: dict[str, list[tuple[str, str]]] = {}
    for importer, module, name in issues:
        by_file.setdefault(importer, []).append((module, name))

    log(f"  [integrity] found dangling imports in {len(by_file)} files")
    fixes = 0
    for importer, missing in list(by_file.items())[:max_files]:
        sibling_paths = sorted({_module_to_path(m) for m, _ in missing})
        siblings = {
            p: py_files[p] for p in sibling_paths if p in py_files
        }
        prompt = build_integrity_fix_prompt(
            importer, py_files[importer], siblings, missing
        )
        # KEY: route through pre-write validator with retry. Previously the
        # raw LLM output was written directly — that's how the <div> regen
        # regression and indent errors landed in stage-7-clean files.
        try:
            fixed, vresult = validated_generate(
                initial_prompt=prompt,
                path=importer,
                generate=generate,
                sanitize=strip_code_fences,
                max_attempts=3,
                log=log,
            )
        except Exception as exc:  # noqa: BLE001 — integrity must never crash
            log(f"  [integrity] {importer}: generate failed ({exc})")
            continue
        if len(fixed) < 20:
            continue
        # If validation didn't fully pass, still write best-effort. Doctor
        # pass + stage 8 will pick up remaining issues.
        target = root / importer
        target.write_text(fixed, encoding="utf-8")
        py_files[importer] = fixed
        fixes += 1
        status = "↻" if vresult.ok else "⚠"
        log(f"  [integrity] {status} {importer} ({len(missing)} dangling refs)")
    return fixes


# ──────────────────────── single-file lint/undefined pass ──────────────


def _run_lint_pass(
    root: Path,
    *,
    generate: GenerateFn,
    log: ProgressFn,
    max_rounds: int = 2,
) -> int:
    """For each Python file, detect lint diagnostics + undefined names,
    regenerate if needed. Capped at `max_rounds` per file."""
    py_files = _python_files_under(root)
    fixes = 0
    for rel_path in py_files:
        full = root / rel_path
        for round_idx in range(max_rounds):
            current = full.read_text("utf-8", errors="replace")
            try:
                diagnostics = lint_python_file(full)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                diagnostics = []
            undefined = detect_python_undefined_names(current)
            if not diagnostics and not undefined:
                break
            prompt = build_lint_fix_prompt(
                rel_path, current, diagnostics, undefined
            )
            try:
                fixed, _ = validated_generate(
                    initial_prompt=prompt,
                    path=rel_path,
                    generate=generate,
                    sanitize=strip_code_fences,
                    max_attempts=3,
                    log=log,
                )
            except Exception as exc:  # noqa: BLE001
                log(f"  [integrity-lint] {rel_path}: generate failed ({exc})")
                break
            if len(fixed) < 20:
                break
            full.write_text(fixed, encoding="utf-8")
            fixes += 1
            log(
                f"  [integrity-lint] ⚒ {rel_path} round {round_idx+1} "
                f"({len(diagnostics)} diag, {len(undefined)} undef)"
            )
    return fixes


# ──────────────────────── auto-format pre-pass ─────────────────────────


def _run_ruff_fix(root: Path, *, log: ProgressFn) -> None:
    """Run `ruff check --fix --unsafe-fixes` to kill auto-fixable issues
    BEFORE the LLM-driven passes. Knocks out 80%+ of style + unused-import
    problems without consuming any LLM tokens.
    """
    import shutil
    if not shutil.which("ruff"):
        log("  [integrity] ruff not installed — skipping auto-fix")
        return
    try:
        result = subprocess.run(
            ["ruff", "check", "--fix", "--unsafe-fixes", "."],
            cwd=root, capture_output=True, text=True, timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        log(f"  [integrity] ruff auto-fix skipped: {exc}")
        return
    # ruff exits non-zero when files were modified — that's expected
    tail = (result.stdout + result.stderr).splitlines()[-3:]
    for line in tail:
        if line.strip():
            log(f"  [integrity] ruff: {line.strip()}")


# ──────────────────────── public entry ─────────────────────────────────


def run_integrity_pass(
    out_dir: Path,
    *,
    generate: GenerateFn,
    log: ProgressFn,
    enable_ruff_fix: bool = True,
    enable_lint_pass: bool = True,
) -> IntegrityReport:
    """Top-level integrity pass for a generated project tree.

    Runs (in order):
      1. `ruff check --fix --unsafe-fixes` — deterministic auto-fix
      2. Cross-module dangling-import pass — LLM regen on importers
      3. Per-file lint + undefined-name pass — LLM regen capped per file

    Returns counts for the build report. Never crashes — exception
    handling around every generate call.
    """
    backend = out_dir / "backend"
    if not backend.is_dir():
        log("  [integrity] no backend/ — skipping")
        return IntegrityReport()

    log("[integrity] starting cross-file integrity pass...")

    if enable_ruff_fix:
        log("  [integrity] running ruff --fix --unsafe-fixes")
        _run_ruff_fix(backend, log=log)

    dangling_fixes = _run_dangling_pass(backend, generate=generate, log=log)

    lint_fixes = 0
    if enable_lint_pass:
        lint_fixes = _run_lint_pass(backend, generate=generate, log=log)

    py_files = _python_files_under(backend)
    log(
        f"[integrity] done. dangling_fixes={dangling_fixes} "
        f"lint_fixes={lint_fixes} files_scanned={len(py_files)}"
    )

    return IntegrityReport(
        dangling_fixes=dangling_fixes,
        lint_fixes=lint_fixes,
        files_scanned=len(py_files),
    )


__all__ = ["IntegrityReport", "run_integrity_pass"]
