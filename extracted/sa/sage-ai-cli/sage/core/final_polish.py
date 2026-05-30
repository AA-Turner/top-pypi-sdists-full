"""Final polish pass — runs AFTER stage 8 verify settles.

Two responsibilities:

1. **Auto-add missing `@types/*` packages.** When `tsc --noEmit` complains
   "Cannot find type definition file for 'jest'", the fix is usually to
   add `@types/jest` to devDependencies. This scans `tsconfig.json` types
   array + the actual code for jest globals + zustand etc. and ensures
   each is in package.json. Then `npm install` re-runs.

2. **Final `ruff --fix --unsafe-fixes` + `eslint --fix`.** The earlier
   doctor pass (stage 7.4) ran these once, but stages 7.5 (integrity)
   and 8 (repair) regenerated files AFTER that, potentially introducing
   new style issues. One more pass at the end catches them.

3. **One more verify run** (capped). After polish, re-run install +
   tests. If still failing, return the report — the user gets honest
   information about what didn't auto-fix.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from sage.core.install_verify import verify_all


ProgressFn = Callable[[str], None]


@dataclass
class PolishReport:
    types_added: list[str] = field(default_factory=list)
    ruff_fixes_ran: bool = False
    eslint_fixes_ran: bool = False
    final_install_ok: bool | None = None
    final_build_ok: bool | None = None
    final_runs_ok: bool | None = None
    final_tests_ok: bool | None = None


# ────────────────── @types/* auto-resolver ──────────────────────


# packages that commonly need their @types counterpart
_NEEDS_TYPES = {
    "jest": "@types/jest",
    "react": "@types/react",  # though usually already there
    "react-dom": "@types/react-dom",
    "node": "@types/node",
    "supertest": "@types/supertest",
    "express": "@types/express",
    "cors": "@types/cors",
    "lodash": "@types/lodash",
}


def _scan_tsconfig_types(frontend: Path) -> set[str]:
    """Return the set of names in `compilerOptions.types` if any."""
    p = frontend / "tsconfig.json"
    if not p.exists():
        return set()
    try:
        data = json.loads(p.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    types = data.get("compilerOptions", {}).get("types", [])
    return {str(t) for t in types if isinstance(t, str)}


def _scan_code_for_globals(frontend: Path) -> set[str]:
    """Look for usage of jest globals + other common needs-types-pkgs."""
    globals_found: set[str] = set()
    patterns = {
        "jest": re.compile(r"\b(?:jest|describe|it|test|expect)\s*[\(\.]"),
        "node": re.compile(r"\bprocess\.env\b|\b__dirname\b|\brequire\b"),
    }
    for ext in ("ts", "tsx", "js", "jsx"):
        for p in frontend.rglob(f"*.{ext}"):
            if any(part in {"node_modules", "dist", "build", ".expo"}
                   for part in p.parts):
                continue
            try:
                content = p.read_text("utf-8", errors="replace")
            except OSError:
                continue
            for name, pat in patterns.items():
                if pat.search(content):
                    globals_found.add(name)
    return globals_found


def _scan_imports(frontend: Path) -> set[str]:
    """Return top-level package names imported across the frontend."""
    imports: set[str] = set()
    pat = re.compile(r"""(?:from|import)\s+['"]([@\w\-/]+)['"]""")
    for ext in ("ts", "tsx", "js", "jsx"):
        for p in frontend.rglob(f"*.{ext}"):
            if any(part in {"node_modules", "dist", "build", ".expo"}
                   for part in p.parts):
                continue
            try:
                content = p.read_text("utf-8", errors="replace")
            except OSError:
                continue
            for match in pat.finditer(content):
                spec = match.group(1)
                # Skip relative imports
                if spec.startswith(".") or spec.startswith("/"):
                    continue
                # @scope/name vs plain name
                if spec.startswith("@"):
                    parts = spec.split("/")
                    if len(parts) >= 2:
                        imports.add("/".join(parts[:2]))
                else:
                    imports.add(spec.split("/")[0])
    return imports


def add_missing_types_packages(frontend: Path, *, log: ProgressFn) -> list[str]:
    """Ensure every needs-types-pkg used in the project has its @types in package.json.

    Returns list of @types packages added.
    """
    pkg_path = frontend / "package.json"
    if not pkg_path.exists():
        return []
    try:
        pkg = json.loads(pkg_path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    dev = pkg.get("devDependencies", {})
    deps = pkg.get("dependencies", {})
    already_have = set(dev.keys()) | set(deps.keys())

    needed: set[str] = set()
    # From tsconfig types array
    for t in _scan_tsconfig_types(frontend):
        types_pkg = _NEEDS_TYPES.get(t)
        if types_pkg and types_pkg not in already_have:
            needed.add(types_pkg)
    # From code globals (jest/node/etc.)
    for global_name in _scan_code_for_globals(frontend):
        types_pkg = _NEEDS_TYPES.get(global_name)
        if types_pkg and types_pkg not in already_have:
            needed.add(types_pkg)
    # From imports — if `import x from 'jest'` etc.
    for imp in _scan_imports(frontend):
        types_pkg = _NEEDS_TYPES.get(imp)
        if types_pkg and types_pkg not in already_have:
            needed.add(types_pkg)

    if not needed:
        return []

    # Default versions for the most common ones
    versions = {
        "@types/jest": "^29.5.14",
        "@types/react": "~18.3.12",
        "@types/react-dom": "~18.3.5",
        "@types/node": "^20.0.0",
        "@types/supertest": "^6.0.2",
        "@types/express": "^5.0.0",
        "@types/cors": "^2.8.17",
        "@types/lodash": "^4.17.13",
    }
    pkg.setdefault("devDependencies", {})
    added: list[str] = []
    for t in sorted(needed):
        pkg["devDependencies"][t] = versions.get(t, "latest")
        added.append(t)

    # Re-sort devDependencies alphabetically (consistent with how npm writes it)
    pkg["devDependencies"] = dict(sorted(pkg["devDependencies"].items()))

    pkg_path.write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")
    log(f"  [polish] added missing @types packages: {', '.join(added)}")
    return added


# ────────────────── auto-fix pass ─────────────────────────────


def _has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run_ruff_final(backend: Path, *, log: ProgressFn) -> bool:
    if not _has("ruff") or not backend.is_dir():
        return False
    try:
        subprocess.run(
            ["ruff", "check", "--fix", "--unsafe-fixes", "."],
            cwd=backend, capture_output=True, text=True, timeout=120, check=False,
        )
        log("  [polish] ruff --fix --unsafe-fixes done")
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        log(f"  [polish] ruff skipped: {exc}")
        return False


def run_eslint_final(frontend: Path, *, log: ProgressFn) -> bool:
    if not (frontend / "node_modules").is_dir():
        log("  [polish] node_modules not present — skipping eslint")
        return False
    try:
        result = subprocess.run(
            ["npx", "--no-install", "eslint", ".", "--fix",
             "--ext", ".ts,.tsx", "--no-error-on-unmatched-pattern"],
            cwd=frontend, capture_output=True, text=True, timeout=180, check=False,
        )
        log(f"  [polish] eslint --fix done (rc={result.returncode})")
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        log(f"  [polish] eslint skipped: {exc}")
        return False


# ────────────────── re-install + re-verify ────────────────────


def reinstall_frontend(frontend: Path, *, log: ProgressFn) -> bool:
    """After modifying package.json, re-run npm install to pull new deps."""
    if not frontend.is_dir() or not (frontend / "package.json").exists():
        return False
    try:
        result = subprocess.run(
            ["npm", "install", "--no-audit", "--no-fund"],
            cwd=frontend, capture_output=True, text=True, timeout=600, check=False,
        )
        if result.returncode == 0:
            log("  [polish] re-installed frontend deps after @types additions")
            return True
        log(f"  [polish] npm install failed rc={result.returncode}")
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        log(f"  [polish] npm install skipped: {exc}")
        return False


# ────────────────── public entry ──────────────────────────────


def run_final_polish(
    out_dir: Path,
    *,
    log: ProgressFn,
) -> PolishReport:
    """One last sweep after stage 8 settles."""
    report = PolishReport()
    backend = out_dir / "backend"
    frontend = out_dir / "frontend"

    log("[polish] starting final cleanup pass...")

    # 1. Add missing @types/* deps
    if frontend.is_dir():
        added = add_missing_types_packages(frontend, log=log)
        report.types_added = added
        if added:
            reinstall_frontend(frontend, log=log)

    # 2. Run ruff --fix + eslint --fix one more time
    if backend.is_dir():
        report.ruff_fixes_ran = run_ruff_final(backend, log=log)
    if frontend.is_dir():
        report.eslint_fixes_ran = run_eslint_final(frontend, log=log)

    # 3. One final verify run, capture results
    try:
        verify_reports = verify_all(out_dir)
        report.final_install_ok = all(
            r.install_ok in (True, None) for r in verify_reports
        )
        report.final_build_ok = all(
            r.build_ok in (True, None) for r in verify_reports
        )
        report.final_runs_ok = all(
            r.runs_ok in (True, None) for r in verify_reports
        )
        report.final_tests_ok = all(
            r.tests_ok in (True, None) for r in verify_reports
        )
    except Exception as exc:  # noqa: BLE001
        log(f"  [polish] final verify failed to run: {exc}")

    log(
        f"[polish] done. types_added={len(report.types_added)} "
        f"ruff={report.ruff_fixes_ran} eslint={report.eslint_fixes_ran} "
        f"final_install_ok={report.final_install_ok} "
        f"final_build_ok={report.final_build_ok} "
        f"final_runs_ok={report.final_runs_ok} "
        f"final_tests_ok={report.final_tests_ok}"
    )
    return report


__all__ = ["PolishReport", "add_missing_types_packages", "run_final_polish"]
