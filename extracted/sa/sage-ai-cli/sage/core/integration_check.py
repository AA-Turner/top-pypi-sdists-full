"""Cross-file integration check.

Runs AFTER all files are generated but BEFORE stage 8 install/verify.
Catches a class of bugs the per-file validator can't see — like one
file importing `from app.main import settings` when `app/main.py`
doesn't export `settings`.

The existing `integrity_pass` does this for `from app.X.Y import Z`
patterns where X.Y is a nested module. This module catches imports
from ALL project-internal paths (including `app.main`, `app.config`,
top-level modules), then asks the LLM to fix the importing OR exporting
file so the symbol is actually available.

This is the specific bug that caused tests_ok=False in the last build:

  # conftest.py
  from app.main import settings  # ← `settings` not defined in main.py
"""

from __future__ import annotations

import ast
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from sage.core.pre_write_validator import validated_generate
from sage.core.principal_engineer import (
    _collect_module_symbols,
    strip_code_fences,
)


GenerateFn = Callable[[str], str]
ProgressFn = Callable[[str], None]


@dataclass
class IntegrationReport:
    dangling_imports: list[dict] = field(default_factory=list)
    fixed_files: int = 0
    skipped_no_module: int = 0
    case_fixes: int = 0


# ──────────────────────── discovery ────────────────────────────────────


_PROJECT_PKG_PATTERNS = (
    re.compile(r"^app\."),    # app.x.y
    re.compile(r"^app$"),     # bare app
    re.compile(r"^tests\."),
)


def _is_project_module(module: str) -> bool:
    return any(p.match(module) for p in _PROJECT_PKG_PATTERNS)


def _collect_py_files(root: Path) -> dict[str, str]:
    """Read every .py file under root, keyed by 'app/x/y.py' relative path."""
    files: dict[str, str] = {}
    if not root.is_dir():
        return files
    for p in root.rglob("*.py"):
        if any(part in {"venv", ".venv", "__pycache__", "node_modules"}
               for part in p.parts):
            continue
        try:
            files[str(p.relative_to(root))] = p.read_text("utf-8", errors="replace")
        except OSError:
            continue
    return files


def _module_to_relpath(module: str) -> str:
    """`app.main` → `app/main.py`. `app` → `app/__init__.py`."""
    parts = module.split(".")
    return "/".join(parts) + ".py"


# ──────────────────────── analysis ─────────────────────────────────────


def find_cross_file_dangling(
    py_files: dict[str, str],
) -> list[tuple[str, str, str]]:
    """Find every (importer, module, name) where module is a project file
    and name is NOT defined in that module.

    Catches `from app.main import settings` when main.py has no `settings`.
    """
    # Build a symbol table per module path
    module_symbols: dict[str, set[str]] = {}
    for path, content in py_files.items():
        # path 'app/main.py' → module 'app.main'
        if path.endswith("/__init__.py"):
            module = path[: -len("/__init__.py")].replace("/", ".")
        else:
            module = path[: -3].replace("/", ".")
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue
        module_symbols[module] = _collect_module_symbols(content)

    # Walk every file, look for project-internal from-imports
    issues: list[tuple[str, str, str]] = []
    for path, content in py_files.items():
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if not node.module or not _is_project_module(node.module):
                continue
            target_syms = module_symbols.get(node.module)
            if target_syms is None:
                # Module doesn't exist — covered by integrity_pass already
                continue
            for alias in node.names:
                if alias.name == "*":
                    continue
                if alias.name not in target_syms:
                    issues.append((path, node.module, alias.name))
    return issues


def _build_fix_prompt(
    importer: str,
    importer_source: str,
    target_module: str,
    target_path: str,
    target_source: str,
    missing_names: list[str],
) -> str:
    return (
        f"Two files in the same project are out of sync. The importing file "
        f"asks for symbols the target module doesn't define.\n\n"
        f"## Importing file: `{importer}`\n```python\n{importer_source[:3000]}\n```\n\n"
        f"## Target module: `{target_path}` (module `{target_module}`)\n"
        f"```python\n{target_source[:3000]}\n```\n\n"
        f"## Missing symbols from `{target_module}`\n"
        + "\n".join(f"  - `{n}`" for n in missing_names)
        + "\n\nPick the BEST fix per missing symbol:\n"
        f"  a) If `{target_module}` SHOULD export the symbol, add it there. Output:\n"
        f'     {{"path": "{target_path}", "content": "<full new content>"}}\n'
        f"  b) If the importer should use a different name OR not import it at\n"
        f"     all, fix the importer. Output:\n"
        f'     {{"path": "{importer}", "content": "<full new content>"}}\n\n'
        "Choose ONE file to fix. Output a single JSON object with `path` and "
        "`content`. NO prose, NO markdown fences."
    )


def _attempt_integration_fix(
    importer: str,
    target_module: str,
    target_path: str,
    missing: list[str],
    py_files: dict[str, str],
    *,
    generate: GenerateFn,
    log: ProgressFn,
) -> tuple[str, str] | None:
    """Ask LLM for a fix; return (path_to_write, new_content) or None."""
    if importer not in py_files or target_path not in py_files:
        return None
    prompt = _build_fix_prompt(
        importer, py_files[importer],
        target_module, target_path, py_files[target_path],
        missing,
    )
    try:
        # Use validated_generate so the proposed fix is checked before
        # we return it. If validation fails after retries, fall through.
        # Note: the response is JSON, but validated_generate validates
        # the OUTER content as Python — that's wrong, so we sanitize
        # and parse manually.
        raw = generate(prompt)
    except Exception as exc:  # noqa: BLE001
        log(f"  [integration] {importer}: generate failed ({exc})")
        return None
    try:
        cleaned = strip_code_fences(raw)
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1:
            return None
        import json
        payload = json.loads(cleaned[start : end + 1])
    except Exception:  # noqa: BLE001
        return None
    path = payload.get("path")
    content = payload.get("content")
    if not isinstance(path, str) or not isinstance(content, str):
        return None
    if len(content) < 20:
        return None
    # Final per-file validation
    from sage.core.pre_write_validator import validate_generated_file
    vresult = validate_generated_file(content, path)
    if not vresult.ok:
        log(f"  [integration] proposed fix for {path} failed validation; skipping")
        return None
    return path, content


def _attempt_case_fix(
    importer_path: Path,
    missing_names: list[str],
    target_module_symbols: set[str],
) -> int:
    """Deterministic rename for case-mismatched imports.

    The LLM often emits `AIAdvertisement` in one file and `AiAdvertisement`
    in another. When the importer's missing name has a case-insensitive
    match in the target module, rewrite the importer's import to use the
    real name — no LLM round-trip needed. Returns count of names renamed.
    """
    if not target_module_symbols or not importer_path.exists():
        return 0
    by_lower = {s.lower(): s for s in target_module_symbols}
    renames: dict[str, str] = {}
    for name in missing_names:
        actual = by_lower.get(name.lower())
        if actual and actual != name:
            renames[name] = actual
    if not renames:
        return 0
    try:
        src = importer_path.read_text("utf-8", errors="replace")
    except OSError:
        return 0
    new_src = src
    for old, new in renames.items():
        # Word-boundary replace — don't touch substrings.
        new_src = re.sub(rf"\b{re.escape(old)}\b", new, new_src)
    if new_src == src:
        return 0
    importer_path.write_text(new_src, encoding="utf-8")
    return len(renames)


# ──────────────────────── public entry ─────────────────────────────────


def run_integration_check(
    out_dir: Path,
    *,
    generate: GenerateFn,
    log: ProgressFn,
    max_fixes: int = 30,
) -> IntegrationReport:
    """Detect cross-file dangling imports across the backend; fix via LLM.

    Runs AFTER feature generation but BEFORE stage 8. Closes the
    integration gap the per-file validator can't see.
    """
    backend = out_dir / "backend"
    if not backend.is_dir():
        log("[integration] no backend/ — skipping")
        return IntegrationReport()

    log("[integration] checking cross-file dangling imports...")
    py_files = _collect_py_files(backend)
    if not py_files:
        return IntegrationReport()

    issues = find_cross_file_dangling(py_files)
    if not issues:
        log("[integration] clean — no cross-file dangling imports")
        return IntegrationReport()

    # Group: (importer, target_module) → list[missing_name]
    grouped: dict[tuple[str, str], list[str]] = {}
    for importer, module, name in issues:
        grouped.setdefault((importer, module), []).append(name)

    log(f"[integration] found {len(grouped)} importer/module pairs with dangling refs")
    report = IntegrationReport(
        dangling_imports=[
            {"importer": imp, "module": mod, "missing": names}
            for (imp, mod), names in grouped.items()
        ]
    )

    # Build a per-module symbol set once so case-fix can consult it quickly.
    import ast as _ast
    module_symbols: dict[str, set[str]] = {}
    for path, content in py_files.items():
        if path.endswith("/__init__.py"):
            mod = path[: -len("/__init__.py")].replace("/", ".")
        else:
            mod = path[: -3].replace("/", ".")
        try:
            _ast.parse(content)
        except SyntaxError:
            continue
        module_symbols[mod] = _collect_module_symbols(content)

    for (importer, target_module), missing in list(grouped.items())[:max_fixes]:
        target_path = _module_to_relpath(target_module)
        if target_path not in py_files:
            report.skipped_no_module += 1
            continue

        # First try the deterministic case-fold fix — fast, zero LLM cost.
        # Most dangling-import failures we've seen are PascalCase vs
        # mixedCase divergence (AIAdvertisement vs AiAdvertisement), not
        # genuinely missing symbols.
        case_renames = _attempt_case_fix(
            backend / importer, missing, module_symbols.get(target_module, set()),
        )
        if case_renames:
            report.case_fixes += case_renames
            py_files[importer] = (backend / importer).read_text("utf-8", errors="replace")
            log(f"  [integration] case-fix {importer} ({case_renames} renamed)")
            # Re-check whether ALL names were resolved by case-fix.
            remaining = [n for n in missing
                         if n.lower() not in {s.lower() for s in module_symbols.get(target_module, set())}]
            if not remaining:
                continue
            missing = remaining

        fix = _attempt_integration_fix(
            importer, target_module, target_path, missing,
            py_files, generate=generate, log=log,
        )
        if not fix:
            continue
        rel_path, new_content = fix
        target = backend / rel_path
        if target.name == "__init__.py":
            new_content = ""
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_content, encoding="utf-8")
        py_files[rel_path] = new_content
        report.fixed_files += 1
        log(f"  [integration] ↻ {rel_path} ← fix for `{target_module}` missing {missing}")

    log(
        f"[integration] done. fixed={report.fixed_files} "
        f"skipped={report.skipped_no_module} "
        f"dangling_pairs={len(grouped)}"
    )
    return report


__all__ = [
    "IntegrationReport",
    "find_cross_file_dangling",
    "run_integration_check",
]
