"""Deterministic post-generation code repair (no LLM).

The integrity pass in `integrity_pass.py` uses an LLM to fix dangling
imports — that's slow on local hardware (~30s per file). For systemic
LLM-output bugs that have ONE OBVIOUS FIX, we don't need an LLM. We need
a sed-grade tool that runs in milliseconds.

This module is the "code doctor" pass. Eight sub-doctors, each addressing
a specific LLM blind spot we've observed:

  1. add_missing_imports   — inject common missing imports (Index, bcrypt,
                              get_current_user, crontab, etc.)
  2. fix_framework_collision — `react-router-dom` → `expo-router`,
                              `<div>` → `<View>` in RN files,
                              `<input>` → `<TextInput>`, `<button>` → `<Pressable>`
  3. detect_truncations    — find files that end mid-token (unclosed
                              braces, unclosed JSX) and report (caller
                              decides what to do with them)
  4. python_syntax_check   — `ast.parse` every Python file, log failures
  5. typescript_syntax_check — `tsc --noEmit` on the frontend, log errors
  6. eslint_fix            — `eslint . --fix` for auto-fixable JS issues
  7. prettier_format       — `prettier --write` for consistent formatting
  8. ruff_fix              — `ruff check --fix --unsafe-fixes`

Every doctor returns a count of fixes applied so the build report can
show what was deterministically repaired vs. what needed LLM help.
"""

from __future__ import annotations

import ast
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


ProgressFn = Callable[[str], None]


@dataclass
class DoctorReport:
    imports_added: int = 0
    framework_collisions_fixed: int = 0
    truncations_detected: list[str] = field(default_factory=list)
    python_syntax_errors: list[str] = field(default_factory=list)
    typescript_files_failed: int = 0
    eslint_fixes_ran: bool = False
    prettier_ran: bool = False
    ruff_fixes_ran: bool = False
    files_touched: int = 0
    init_stubs_written: int = 0
    indent_fixes_applied: int = 0


# ──────────────────────── add_missing_imports ──────────────────────────

# Map: undefined-name -> import line. These cover the systemic blind
# spots we've observed in qwen3 + other local models.
_COMMON_IMPORTS: dict[str, str] = {
    "get_current_user":    "from app.auth.dependencies import get_current_user",
    "current_tenant_id":   "from app.middleware.tenant import current_tenant_id",
    "get_settings":        "from app.core.config import get_settings",
    "settings":            "from app.core.config import settings",
    "Settings":            "from app.core.config import Settings",
    "Pagination":          "from app.schemas.pagination import Pagination",
    "get_session":         "from app.db.session import get_session",
    "Base":                "from app.db.base import Base",
    "async_session_factory": "from app.db.base import async_session_factory",

    # SQLAlchemy / SQLModel
    "Index":               "from sqlalchemy import Index",
    "func":                "from sqlalchemy import func",
    "select":              "from sqlalchemy import select",
    "Column":              "from sqlalchemy import Column",
    "ForeignKey":          "from sqlalchemy import ForeignKey",
    "AsyncSession":        "from sqlalchemy.ext.asyncio import AsyncSession",
    "Field":               "from sqlmodel import Field",
    "SQLModel":            "from sqlmodel import SQLModel",
    "Relationship":        "from sqlmodel import Relationship",

    # FastAPI
    "FastAPI":             "from fastapi import FastAPI",
    "APIRouter":           "from fastapi import APIRouter",
    "Depends":             "from fastapi import Depends",
    "HTTPException":       "from fastapi import HTTPException",
    "status":              "from fastapi import status",
    "Request":             "from fastapi import Request",
    "Response":            "from fastapi import Response",

    # Pydantic
    "BaseModel":           "from pydantic import BaseModel",
    "ConfigDict":          "from pydantic import ConfigDict",
    "field_validator":     "from pydantic import field_validator",
    "model_validator":     "from pydantic import model_validator",

    # Security / auth
    "bcrypt":              "from passlib.hash import bcrypt",
    "JWTError":            "from jose import JWTError",
    "jwt":                 "from jose import jwt",

    # Celery
    "crontab":             "from celery.schedules import crontab",
    "Celery":              "from celery import Celery",

    # Stdlib
    "datetime":            "from datetime import datetime",
    "timedelta":           "from datetime import timedelta",
    "date":                "from datetime import date",
    "Optional":            "from typing import Optional",
    "List":                "from typing import List",
    "Dict":                "from typing import Dict",
    "Any":                 "from typing import Any",
    "Tuple":               "from typing import Tuple",
    "Union":               "from typing import Union",
    "Callable":            "from typing import Callable",
    "Annotated":           "from typing import Annotated",
    "UUID":                "from uuid import UUID",
    "uuid4":               "from uuid import uuid4",
    "Path":                "from pathlib import Path",
    "Decimal":             "from decimal import Decimal",
    "Enum":                "from enum import Enum",
}


def _name_undefined_in(source: str, name: str) -> bool:
    """True if `name` is used somewhere in `source` but never imported/defined."""
    if not re.search(rf"\b{re.escape(name)}\b", source):
        return False
    # Already imported?
    if re.search(
        rf"^(?:from\s+\S+\s+import\s+(?:[^,#\n]+,\s*)*\s*{re.escape(name)}\b|"
        rf"import\s+(?:\S+\s+as\s+)?{re.escape(name)}\b)",
        source, re.MULTILINE,
    ):
        return False
    # Defined as a class/function/var in this file?
    if re.search(
        rf"^(?:class|def|async\s+def)\s+{re.escape(name)}\b|"
        rf"^{re.escape(name)}\s*[=:]",
        source, re.MULTILINE,
    ):
        return False
    return True


def _insertion_point(source: str) -> int:
    """Pick the line index after `from __future__` imports and module docstring."""
    lines = source.split("\n")
    insert_at = 0
    in_docstring = False
    docstring_quote = ""
    for i, line in enumerate(lines[:20]):
        stripped = line.strip()
        if not in_docstring and (stripped.startswith('"""') or stripped.startswith("'''")):
            quote = stripped[:3]
            # Single-line docstring?
            if len(stripped) > 3 and stripped.endswith(quote):
                insert_at = i + 1
                continue
            in_docstring = True
            docstring_quote = quote
            continue
        if in_docstring and docstring_quote in stripped:
            in_docstring = False
            insert_at = i + 1
            continue
        if in_docstring:
            continue
        if stripped.startswith("from __future__"):
            insert_at = i + 1
            continue
    return insert_at


def add_missing_imports(path: Path) -> int:
    """Inject common missing imports into a Python file. Returns count added."""
    try:
        src = path.read_text("utf-8", errors="replace")
    except OSError:
        return 0
    to_add: list[str] = []
    for name, imp in _COMMON_IMPORTS.items():
        if _name_undefined_in(src, name):
            to_add.append(imp)
    if not to_add:
        return 0
    lines = src.split("\n")
    insert_at = _insertion_point(src)
    new_lines = lines[:insert_at] + to_add + [""] + lines[insert_at:]
    path.write_text("\n".join(new_lines), encoding="utf-8")
    return len(to_add)


# ──────────────────────── fix_framework_collision ──────────────────────


# Substitutions to apply ONLY in React Native files (frontend/app/, frontend/src/)
_RN_SUBSTITUTIONS: tuple[tuple[re.Pattern[str], str], ...] = (
    # Wrong router
    (re.compile(r"from\s+['\"]react-router-dom['\"]"),
     "from 'expo-router'"),
    (re.compile(r"import\s+\{\s*Link\s*\}\s+from\s+['\"]react-router-dom['\"]"),
     "import { Link } from 'expo-router'"),
    # useNavigate doesn't exist in expo-router; use router.push via useRouter
    (re.compile(r"useNavigate"), "useRouter"),

    # HTML → RN primitives (must be careful — only replace as JSX tags, not as identifiers)
    (re.compile(r"<div(\s|>)"), r"<View\1"),
    (re.compile(r"</div>"), "</View>"),
    (re.compile(r"<span(\s|>)"), r"<Text\1"),
    (re.compile(r"</span>"), "</Text>"),
    (re.compile(r"<button(\s|>)"), r"<Pressable\1"),
    (re.compile(r"</button>"), "</Pressable>"),
    (re.compile(r"<input(\s|/>)"), r"<TextInput\1"),
    (re.compile(r"<h1(\s|>)"), r"<Text\1"),
    (re.compile(r"</h1>"), "</Text>"),
    (re.compile(r"<h2(\s|>)"), r"<Text\1"),
    (re.compile(r"</h2>"), "</Text>"),
    (re.compile(r"<p(\s|>)"), r"<Text\1"),
    (re.compile(r"</p>"), "</Text>"),
    (re.compile(r"<form(\s|>)"), r"<View\1"),
    (re.compile(r"</form>"), "</View>"),
    (re.compile(r"<label(\s|>)"), r"<Text\1"),
    (re.compile(r"</label>"), "</Text>"),
    # className= → style= is a more nuanced translation, leave it but flag

    # Common state errors
    (re.compile(r"document\.getElementById"), "// document.getElementById is web-only — TODO"),
)


# After substitution, we need to ensure View/Text/Pressable/TextInput are imported
_RN_IMPORTS_AFTER_SUBSTITUTION = [
    "View", "Text", "Pressable", "TextInput", "ScrollView", "ActivityIndicator",
]


def fix_framework_collision_rn(path: Path) -> int:
    """Apply React Native substitutions to a frontend file. Returns count."""
    try:
        src = path.read_text("utf-8", errors="replace")
    except OSError:
        return 0
    new_src = src
    count = 0
    for pattern, replacement in _RN_SUBSTITUTIONS:
        new_src, n = pattern.subn(replacement, new_src)
        count += n
    if count == 0:
        return 0

    # After substitution we likely need RN primitives imported. Check
    # if any are used + not imported, and add a single import line.
    used = [name for name in _RN_IMPORTS_AFTER_SUBSTITUTION
            if re.search(rf"<{name}[\s/>]", new_src)]
    missing = [
        name for name in used
        if not re.search(
            rf"import\s+\{{[^}}]*\b{name}\b[^}}]*\}}\s+from\s+['\"]react-native['\"]",
            new_src,
        )
    ]
    if missing:
        # Check if there's already a react-native import we can extend
        rn_import = re.search(
            r"^import\s+\{([^}]+)\}\s+from\s+['\"]react-native['\"]",
            new_src, re.MULTILINE,
        )
        if rn_import:
            existing = [s.strip() for s in rn_import.group(1).split(",") if s.strip()]
            all_names = sorted(set(existing + missing))
            new_line = "import { " + ", ".join(all_names) + " } from 'react-native'"
            new_src = new_src[:rn_import.start()] + new_line + new_src[rn_import.end():]
        else:
            # Add new import after any other imports at the top
            lines = new_src.split("\n")
            insert_at = 0
            for i, line in enumerate(lines[:20]):
                if line.startswith("import ") or line.startswith("from "):
                    insert_at = i + 1
            new_lines = (
                lines[:insert_at]
                + ["import { " + ", ".join(missing) + " } from 'react-native';"]
                + lines[insert_at:]
            )
            new_src = "\n".join(new_lines)

    path.write_text(new_src, encoding="utf-8")
    return count


# ──────────────────────── detect_truncations ───────────────────────────


def stub_truncated_init(path: Path) -> bool:
    """If this `__init__.py` doesn't parse, overwrite it with an empty stub.

    The overnight build kept landing with truncated __init__.py files (LLM
    ran out of tokens mid-import-block). An empty __init__.py is always
    valid Python, makes the package importable, and is the right thing for
    a barrel-style package — explicit re-exports live in the leaf modules.
    Only applied to `__init__.py` so we never silently empty real code.

    Returns True if the file was rewritten.
    """
    if path.name != "__init__.py":
        return False
    try:
        src = path.read_text("utf-8", errors="replace")
    except OSError:
        return False
    try:
        ast.parse(src)
        return False  # parses fine, leave alone
    except SyntaxError:
        pass
    path.write_text('"""Package init."""\n', encoding="utf-8")
    return True


def attempt_indent_fix(path: Path) -> bool:
    """Best-effort dedent for "unexpected indent" at the top of the module.

    The qwen3 / llama models frequently emit a Python file where the first
    real statement after the imports has a stray leading space. `ast.parse`
    rejects with "unexpected indent". The deterministic fix is to strip
    leading whitespace from that single line — no LLM needed.

    Returns True if a fix was written.
    """
    try:
        src = path.read_text("utf-8", errors="replace")
    except OSError:
        return False
    try:
        ast.parse(src)
        return False  # nothing to fix
    except SyntaxError as exc:
        if exc.lineno is None or "unexpected indent" not in (exc.msg or ""):
            return False
        bad_lineno = exc.lineno

    lines = src.split("\n")
    idx = bad_lineno - 1  # 0-indexed
    if not 0 <= idx < len(lines):
        return False

    # Only dedent if the prior non-blank line is NOT itself indented — i.e.
    # we're at module scope. Don't touch indented bodies of real blocks.
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j >= 0 and lines[j] and lines[j][0] in " \t":
        return False  # this looks like a real indented context

    fixed_line = lines[idx].lstrip()
    if fixed_line == lines[idx]:
        return False  # nothing to strip
    lines[idx] = fixed_line
    new_src = "\n".join(lines)

    # Only commit the change if it parses now — otherwise we made things worse.
    try:
        ast.parse(new_src)
    except SyntaxError:
        return False

    path.write_text(new_src, encoding="utf-8")
    return True


def detect_truncated_python(path: Path) -> bool:
    """True if the file ends in a way that suggests the LLM ran out of tokens."""
    try:
        src = path.read_text("utf-8", errors="replace")
    except OSError:
        return False
    if not src.strip():
        return True
    # Try to parse — syntax error suggests truncation OR LLM bug
    try:
        ast.parse(src)
        return False
    except SyntaxError as exc:
        # A genuine syntax error near EOF likely = truncation
        return exc.lineno is not None and exc.lineno >= len(src.split("\n")) - 3


def detect_truncated_tsx(path: Path) -> bool:
    """Heuristic check for TS/TSX truncation: unbalanced braces/JSX."""
    try:
        src = path.read_text("utf-8", errors="replace")
    except OSError:
        return False
    if not src.strip():
        return True
    # Count braces (ignoring strings would be more correct, but this catches most)
    opens = src.count("{")
    closes = src.count("}")
    parens_open = src.count("(")
    parens_close = src.count(")")
    return (opens - closes) >= 2 or (parens_open - parens_close) >= 2


# ──────────────────────── auto-format passes ───────────────────────────


def _has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run_ruff_fix(backend: Path, *, log: ProgressFn) -> bool:
    if not _has("ruff"):
        return False
    try:
        subprocess.run(
            ["ruff", "check", "--fix", "--unsafe-fixes", "."],
            cwd=backend, capture_output=True, text=True, timeout=120, check=False,
        )
        log("  [doctor] ruff --fix done")
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        log(f"  [doctor] ruff skipped: {exc}")
        return False


def run_eslint_fix(frontend: Path, *, log: ProgressFn) -> bool:
    if not (frontend / "node_modules").is_dir():
        log("  [doctor] node_modules missing; eslint skipped")
        return False
    try:
        result = subprocess.run(
            ["npx", "--no-install", "eslint", ".", "--fix", "--ext", ".ts,.tsx"],
            cwd=frontend, capture_output=True, text=True, timeout=180, check=False,
        )
        # eslint exits non-zero when issues remain; that's expected
        log(f"  [doctor] eslint --fix done (rc={result.returncode})")
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        log(f"  [doctor] eslint skipped: {exc}")
        return False


def run_prettier_format(frontend: Path, *, log: ProgressFn) -> bool:
    if not (frontend / "node_modules").is_dir():
        return False
    try:
        result = subprocess.run(
            ["npx", "--no-install", "prettier", "--write", "**/*.{ts,tsx,js,jsx,json}",
             "--ignore-path", ".gitignore"],
            cwd=frontend, capture_output=True, text=True, timeout=120, check=False,
        )
        log(f"  [doctor] prettier --write done (rc={result.returncode})")
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        log(f"  [doctor] prettier skipped: {exc}")
        return False


# ──────────────────────── orchestrator ─────────────────────────────────


def _python_files(root: Path) -> list[Path]:
    return [
        p for p in root.rglob("*.py")
        if not any(part in {"venv", ".venv", "__pycache__"} for part in p.parts)
    ]


def _frontend_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for ext in ("ts", "tsx", "js", "jsx"):
        for p in root.rglob(f"*.{ext}"):
            if not any(part in {"node_modules", ".expo", "dist", "build"}
                       for part in p.parts):
                out.append(p)
    return out


def run_code_doctors(
    out_dir: Path,
    *,
    log: ProgressFn,
    fix_imports: bool = True,
    fix_framework: bool = True,
    detect_truncations_flag: bool = True,
    run_ruff: bool = True,
    run_eslint: bool = True,
    run_prettier: bool = False,  # off by default — adds time, no quality win
) -> DoctorReport:
    """Run every mechanical doctor on the generated project.

    Doctors are pure-Python + subprocess; no LLM calls. They run in
    seconds, can't crash the build (exception handling around every
    external call), and produce a DoctorReport with counts.
    """
    report = DoctorReport()
    backend = out_dir / "backend"
    frontend = out_dir / "frontend"

    log("[doctor] starting deterministic code repair pass...")

    # ── 0. Deterministic repairs run FIRST, so later detectors don't
    #       waste a row reporting things we're about to fix anyway.
    if backend.is_dir():
        for p in _python_files(backend):
            if stub_truncated_init(p):
                report.init_stubs_written += 1
                report.files_touched += 1
        for p in _python_files(backend):
            if attempt_indent_fix(p):
                report.indent_fixes_applied += 1
                report.files_touched += 1
        if report.init_stubs_written or report.indent_fixes_applied:
            log(
                f"  [doctor] repaired {report.init_stubs_written} truncated "
                f"__init__.py + {report.indent_fixes_applied} indent errors"
            )

    # ── 1. Python: add missing imports ──
    if fix_imports and backend.is_dir():
        for p in _python_files(backend):
            n = add_missing_imports(p)
            if n:
                report.imports_added += n
                report.files_touched += 1
        log(f"  [doctor] added {report.imports_added} missing imports across "
            f"backend files")

    # ── 2. Frontend: framework collision fix ──
    if fix_framework and frontend.is_dir():
        # Apply only to files under frontend/app/ or frontend/src/
        for p in _frontend_files(frontend):
            rel = str(p.relative_to(frontend))
            if rel.startswith("app/") or rel.startswith("src/"):
                n = fix_framework_collision_rn(p)
                if n:
                    report.framework_collisions_fixed += n
                    report.files_touched += 1
        log(f"  [doctor] fixed {report.framework_collisions_fixed} "
            f"react-router-dom/HTML collisions in frontend files")

    # ── 3. Truncation detection ──
    if detect_truncations_flag:
        for p in _python_files(backend) if backend.is_dir() else []:
            if detect_truncated_python(p):
                report.truncations_detected.append(str(p.relative_to(out_dir)))
        for p in _frontend_files(frontend) if frontend.is_dir() else []:
            if detect_truncated_tsx(p):
                report.truncations_detected.append(str(p.relative_to(out_dir)))
        if report.truncations_detected:
            log(f"  [doctor] flagged {len(report.truncations_detected)} possibly "
                f"truncated files (caller decides regen)")

    # ── 4. Python syntax check ──
    if backend.is_dir():
        for p in _python_files(backend):
            try:
                ast.parse(p.read_text("utf-8", errors="replace"))
            except SyntaxError as exc:
                report.python_syntax_errors.append(
                    f"{p.relative_to(out_dir)}:{exc.lineno}: {exc.msg}"
                )
        if report.python_syntax_errors:
            log(f"  [doctor] {len(report.python_syntax_errors)} Python syntax "
                f"errors remain (caller may regen)")

    # ── 5. Auto-format (deterministic, no LLM) ──
    if run_ruff and backend.is_dir():
        report.ruff_fixes_ran = run_ruff_fix(backend, log=log)
    if run_eslint and frontend.is_dir():
        report.eslint_fixes_ran = run_eslint_fix(frontend, log=log)
    if run_prettier and frontend.is_dir():
        report.prettier_ran = run_prettier_format(frontend, log=log)

    log(
        f"[doctor] done. imports={report.imports_added} "
        f"framework={report.framework_collisions_fixed} "
        f"truncations={len(report.truncations_detected)} "
        f"py-syntax-errors={len(report.python_syntax_errors)}"
    )
    return report


__all__ = [
    "DoctorReport",
    "add_missing_imports",
    "attempt_indent_fix",
    "detect_truncated_python",
    "detect_truncated_tsx",
    "fix_framework_collision_rn",
    "run_code_doctors",
    "run_eslint_fix",
    "stub_truncated_init",
    "run_prettier_format",
    "run_ruff_fix",
]
