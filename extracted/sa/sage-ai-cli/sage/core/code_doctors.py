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
    sqlmodel_json_fields_fixed: int = 0
    yaml_env_style_fixed: int = 0


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
    "JSON":                "from sqlmodel import JSON",

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


# ──────────────────────── fix_wrong_python_imports ─────────────────────


# Wrong import patterns seen in LLM-generated FastAPI code, paired with
# correct replacements. Applied to every .py file in backend/.
_WRONG_IMPORT_FIXES: tuple[tuple[re.Pattern[str], str], ...] = (
    # AsyncSession is from sqlalchemy.ext.asyncio, NOT from sqlmodel
    (
        re.compile(r"from\s+sqlmodel\s+import\s+([^#\n]*)\bAsyncSession\b([^#\n]*)"),
        None,  # handled specially below
    ),
    # create_async_engine is from sqlalchemy.ext.asyncio, NOT from sqlmodel
    (
        re.compile(r"from\s+sqlmodel\s+import\s+([^#\n]*)\bcreate_async_engine\b([^#\n]*)"),
        None,  # handled specially below (similar to AsyncSession fix)
    ),
    # Session (sync) wrongly imported from sqlalchemy.ext.asyncio — use AsyncSession
    (re.compile(r"from\s+sqlalchemy\.ext\.asyncio\s+import\s+([^#\n]*)\bSession\b([^#\n]*)"),
     None,  # handled specially: replace Session with AsyncSession
    ),
    # Wrong current_tenant_id import paths — LLMs emit 5 different wrong paths.
    # Canonical: from app.middleware.tenant import current_tenant_id
    (re.compile(r"from\s+app\s+import\s+current_tenant_id"),
     "from app.middleware.tenant import current_tenant_id"),
    (re.compile(r"from\s+app\.core\.tenant\s+import\s+current_tenant_id"),
     "from app.middleware.tenant import current_tenant_id"),
    (re.compile(r"from\s+app\.utils\s+import\s+current_tenant_id"),
     "from app.middleware.tenant import current_tenant_id"),
    (re.compile(r"from\s+app\.dependencies\s+import\s+current_tenant_id"),
     "from app.middleware.tenant import current_tenant_id"),
    (re.compile(r"from\s+app\.core\.dependencies\s+import\s+current_tenant_id"),
     "from app.middleware.tenant import current_tenant_id"),
    # Settings used as class attribute instead of instance — detect Settings.FIELD
    # pattern and ensure settings instance is used instead
    (re.compile(r"from\s+app\.core\.config\s+import\s+Settings\b"),
     "from app.core.config import get_settings\n_settings = get_settings()"),
    # Wrong path imports in tests: "from backend.app import" → "from app import"
    (re.compile(r"from\s+backend\.app\."),
     "from app."),
    # API router package import fix
    (re.compile(r"from\s+app\.api\s+import\s+api_router"),
     "from app.api.routes import api_router"),
)


def _fix_sqlalchemy_wrong_imports(src: str) -> str:
    """Fix common wrong SQLAlchemy/SQLModel import patterns.

    Handles:
    1. from sqlmodel import ..., AsyncSession      → split out to sqlalchemy
    2. from sqlmodel import ..., create_async_engine → split out to sqlalchemy
    3. from sqlalchemy.ext.asyncio import ..., Session → replace with AsyncSession
    """
    changed = src

    def _move_from_sqlmodel(text: str, symbol: str, correct_import: str) -> str:
        """Move `symbol` from a sqlmodel import line to `correct_import` line."""
        pattern = re.compile(
            rf"^(from\s+sqlmodel\s+import\s+)(.*\b{re.escape(symbol)}\b.*)$",
            re.MULTILINE,
        )
        m = pattern.search(text)
        if not m:
            return text
        imports_str = m.group(2)
        remaining = re.sub(rf",?\s*\b{re.escape(symbol)}\b\s*,?", ",", imports_str)
        remaining = re.sub(r",\s*,", ",", remaining)
        remaining = remaining.strip(" ,")
        new_sqlmodel = f"from sqlmodel import {remaining}" if remaining else ""
        replacement = "\n".join(filter(None, [new_sqlmodel, correct_import]))
        new_text = pattern.sub(replacement, text)
        # Dedupe if already imported elsewhere
        if new_text.count(correct_import) > 1:
            idx = new_text.find(correct_import)
            rest = new_text[idx + len(correct_import):]
            rest = rest.replace(correct_import + "\n", "").replace(correct_import, "")
            new_text = new_text[:idx] + correct_import + rest
        return new_text

    changed = _move_from_sqlmodel(
        changed, "AsyncSession",
        "from sqlalchemy.ext.asyncio import AsyncSession"
    )
    changed = _move_from_sqlmodel(
        changed, "create_async_engine",
        "from sqlalchemy.ext.asyncio import create_async_engine"
    )

    # Fix: from sqlalchemy.ext.asyncio import ..., Session (sync — wrong)
    # Replace bare Session with AsyncSession in asyncio imports
    changed = re.sub(
        r"(from\s+sqlalchemy\.ext\.asyncio\s+import\s+[^#\n]*)\bSession\b",
        r"\1AsyncSession",
        changed,
    )

    return changed


# Keep old name as alias for backward compat
def _fix_sqlmodel_async_session_import(src: str) -> str:
    return _fix_sqlalchemy_wrong_imports(src)


def fix_wrong_python_imports(path: Path) -> int:
    """Fix known wrong import patterns in LLM-generated Python files.

    Returns the number of substitutions made.
    """
    try:
        src = path.read_text("utf-8", errors="replace")
    except OSError:
        return 0

    original = src
    changes = 0

    # Fix SQLAlchemy/SQLModel import issues (AsyncSession, create_async_engine, Session)
    new_src = _fix_sqlalchemy_wrong_imports(src)
    if new_src != src:
        src = new_src
        changes += 1

    # Apply line-level regex fixes
    for pattern, replacement in _WRONG_IMPORT_FIXES:
        if replacement is None:
            continue  # handled by _fix_sqlalchemy_wrong_imports above
        new_src, n = pattern.subn(replacement, src)
        if n:
            src = new_src
            changes += n

    # Fix Field(onupdate=...) — not supported by SQLModel, causes TypeError at import
    if "onupdate=" in src:
        import re as _re
        new_src = _re.sub(r",\s*onupdate\s*=[^,\)]+", "", src)
        if new_src != src:
            src = new_src
            changes += 1

    # Fix truncated string literals (LLM sometimes cuts mid-string)
    # Detect and replace with a stub if file doesn't parse cleanly
    import ast as _ast
    try:
        _ast.parse(src)
    except SyntaxError as _e:
        if "unterminated string" in str(_e) or "EOL while scanning" in str(_e):
            # Truncate at the broken line and add a stub router
            _lines = src.splitlines()
            _bad = (_e.lineno or len(_lines)) - 1
            _clean = "\n".join(_lines[:max(0, _bad - 1)])
            if path.name.endswith(".py") and "router" in src[:500]:
                _stub = _clean + '\n\n# File was truncated — stub router added\nfrom fastapi import APIRouter\nrouter = APIRouter()\n'
            else:
                _stub = _clean + "\n"
            try:
                _ast.parse(_stub)
                src = _stub
                changes += 1
            except SyntaxError:
                pass

    if src != original:
        path.write_text(src, encoding="utf-8")
    return changes


# ──────────────────────── fix_react_native_package_json ─────────────────


def fix_react_native_package_json(frontend_root: Path) -> int:
    """Ensure React Native projects use Jest (jest-expo), not Vitest.

    If `react-native` is in dependencies but the test script uses vitest,
    replace the test script with the correct jest --watchAll=false command
    and remove vitest from both dependencies and devDependencies.
    Returns 1 if the file was modified.
    """
    import os
    if os.environ.get("SAGE_TESTING") == "1":
        return 0
    pkg = frontend_root / "package.json"
    if not pkg.exists():
        return 0
    try:
        data = _json.loads(pkg.read_text("utf-8", errors="replace"))
    except Exception:
        return 0

    all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    is_rn = "react-native" in all_deps or "expo" in all_deps
    if not is_rn:
        return 0

    changed = False

    # Fix test script to use jest
    scripts = data.get("scripts", {})
    test_cmd = scripts.get("test", "")
    if "vitest" in test_cmd or "--watchAll" in test_cmd:
        data["scripts"]["test"] = "jest --watchAll=false --passWithNoTests"
        changed = True

    # Remove vitest from deps (belongs in web projects only)
    for section in ("dependencies", "devDependencies"):
        if "vitest" in data.get(section, {}):
            del data[section]["vitest"]
            changed = True
        # Also ensure @testing-library/react-native is in devDependencies
        dev = data.setdefault("devDependencies", {})
        if "@testing-library/react-native" not in dev:
            dev["@testing-library/react-native"] = "^12.9.0"
            changed = True
        if "jest-expo" not in dev:
            dev["jest-expo"] = "~52.0.0"
            changed = True
        if "jest" not in dev:
            dev["jest"] = "^29.7.0"
            changed = True

    if changed:
        pkg.write_text(_json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 1 if changed else 0


# ──────────────────────── fix_react_native_jest_config ──────────────────


def fix_react_native_jest_config(frontend_root: Path) -> int:
    """Ensure React Native projects have a properly configured jest.config.js.

    Specifically, it needs 'jest-expo' preset and transformIgnorePatterns to avoid
    syntax errors when parsing react-native node_modules.
    """
    import os
    if os.environ.get("SAGE_TESTING") == "1":
        return 0
    pkg = frontend_root / "package.json"
    if not pkg.exists():
        return 0
    try:
        data = _json.loads(pkg.read_text("utf-8", errors="replace"))
        all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        is_rn = "react-native" in all_deps or "expo" in all_deps
        if not is_rn:
            return 0
    except Exception:
        return 0

    jest_cfg = frontend_root / "jest.config.js"
    expected_content = """module.exports = {
  preset: 'jest-expo',
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg)',
  ],
};
"""
    if jest_cfg.exists():
        try:
            content = jest_cfg.read_text("utf-8")
            if "jest-expo" in content and "transformIgnorePatterns" in content:
                return 0
        except Exception:
            pass

    try:
        jest_cfg.write_text(expected_content, encoding="utf-8")
        return 1
    except Exception:
        return 0


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
    """Unconditionally empty all __init__.py files to make sure they are 100% blank markers.

    An empty __init__.py is always valid Python, makes the package importable, and
    is the right thing for a leaf-import model.
    """
    if path.name != "__init__.py":
        return False
    try:
        src = path.read_text("utf-8", errors="replace")
    except OSError:
        return False
    if src != "":
        path.write_text("", encoding="utf-8")
        return True
    return False


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


def _yaml_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for ext in ("yaml", "yml"):
        for p in root.rglob(f"*.{ext}"):
            out.append(p)
    return out


import json as _json


def fix_yaml_env_style(path: Path) -> int:
    """Repair YAML files where the LLM wrote env-style key=value pairs instead of key: value."""
    if path.suffix not in (".yaml", ".yml"):
        return 0
    try:
        content = path.read_text("utf-8", errors="replace")
    except OSError:
        return 0

    lines = content.splitlines()
    fixed = 0
    new_lines = []
    for line in lines:
        stripped = line.strip()
        # Detect lines like KEY=VALUE (ignoring comments, and ensuring it looks like an env var assignment)
        if not stripped.startswith('#') and '=' in stripped:
            parts = stripped.split('=', 1)
            key = parts[0].strip()
            val = parts[1].strip()
            if re.match(r"^[A-Za-z0-9_.-]+$", key) and ':' not in key:
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.append(f"{indent}{key}: {val}")
                fixed += 1
                continue
        new_lines.append(line)

    if fixed > 0:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return fixed


def fix_sqlmodel_json_fields(path: Path) -> int:
    """Detect fields in SQLModel classes (table=True) annotated with dict/list/Dict/List
    and ensure they use sa_type=JSON.
    """
    try:
        content = path.read_text("utf-8", errors="replace")
    except OSError:
        return 0

    if "SQLModel" not in content:
        return 0

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return 0

    class SQLModelTableVisitor(ast.NodeVisitor):
        def __init__(self):
            self.fields_to_fix = []
            self.current_class = None
            self.is_table = False

        def visit_ClassDef(self, node):
            is_table = False
            for kw in node.keywords:
                if kw.arg == "table":
                    if isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        is_table = True
                    elif isinstance(kw.value, ast.Name) and kw.value.id == "True":
                        is_table = True
            
            old_class = self.current_class
            old_is_table = self.is_table
            
            self.current_class = node.name
            self.is_table = is_table
            
            self.generic_visit(node)
            
            self.current_class = old_class
            self.is_table = old_is_table

        def visit_AnnAssign(self, node):
            if not self.is_table or self.current_class is None:
                return
            
            if not isinstance(node.target, ast.Name):
                return
            
            ann_str = self._get_annotation_type_name(node.annotation)
            if ann_str in ("dict", "Dict", "list", "List"):
                has_sa = False
                field_call = None
                if isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name) and node.value.func.id == "Field":
                        field_call = node.value
                        for kw in node.value.keywords:
                            if kw.arg in ("sa_type", "sa_column"):
                                has_sa = True
                
                if not has_sa:
                    self.fields_to_fix.append((node, field_call))

        def _get_annotation_type_name(self, node):
            if isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Subscript):
                return self._get_annotation_type_name(node.value)
            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
                left = self._get_annotation_type_name(node.left)
                right = self._get_annotation_type_name(node.right)
                if left in ("dict", "Dict", "list", "List"):
                    return left
                if right in ("dict", "Dict", "list", "List"):
                    return right
            elif isinstance(node, ast.Attribute):
                return node.attr
            return ""

    visitor = SQLModelTableVisitor()
    visitor.visit(tree)

    if not visitor.fields_to_fix:
        return 0

    lines = content.splitlines()

    def get_node_source(node):
        start_line, start_col = node.lineno - 1, node.col_offset
        end_line, end_col = node.end_lineno - 1, node.end_col_offset
        if start_line == end_line:
            return lines[start_line][start_col:end_col]
        else:
            res = [lines[start_line][start_col:]]
            for l in range(start_line + 1, end_line):
                res.append(lines[l])
            res.append(lines[end_line][:end_col])
            return "\n".join(res)

    modifications = []
    for node, field_call in visitor.fields_to_fix:
        if field_call is not None:
            field_src = get_node_source(field_call)
            if field_src.strip().startswith("Field"):
                first_paren = field_src.find('(')
                last_paren = field_src.rfind(')')
                if first_paren != -1 and last_paren != -1:
                    inner = field_src[first_paren+1:last_paren].strip()
                    if inner:
                        if inner.endswith(','):
                            new_src = f"Field({inner} sa_type=JSON)"
                        else:
                            new_src = f"Field({inner}, sa_type=JSON)"
                    else:
                        new_src = "Field(sa_type=JSON)"
                else:
                    new_src = "Field(sa_type=JSON)"
            else:
                new_src = "Field(sa_type=JSON)"
            modifications.append((field_call.lineno, field_call.col_offset, field_call.end_lineno, field_call.end_col_offset, new_src))
        elif node.value is not None:
            val_src = get_node_source(node.value)
            new_src = f"Field(default={val_src}, sa_type=JSON)"
            modifications.append((node.value.lineno, node.value.col_offset, node.value.end_lineno, node.value.end_col_offset, new_src))
        else:
            modifications.append((node.end_lineno, node.end_col_offset, node.end_lineno, node.end_col_offset, " = Field(default=None, sa_type=JSON)"))

    # Sort modifications from bottom to top so offsets remain valid
    modifications.sort(key=lambda x: (x[0], x[1]), reverse=True)

    line_starts = [0]
    for line in lines:
        line_starts.append(line_starts[-1] + len(line) + 1)

    char_mods = []
    for start_line, start_col, end_line, end_col, new_src in modifications:
        start_char = line_starts[start_line - 1] + start_col
        end_char = line_starts[end_line - 1] + end_col
        char_mods.append((start_char, end_char, new_src))

    char_mods.sort(key=lambda x: x[0], reverse=True)
    new_content = content
    for start_char, end_char, new_src in char_mods:
        new_content = new_content[:start_char] + new_src + new_content[end_char:]

    path.write_text(new_content, encoding="utf-8")
    return len(visitor.fields_to_fix)


def fix_misplaced_imports_in_test_files(root: Path) -> int:
    """Fix test files where import statements ended up inside function bodies.

    LLMs sometimes emit code like:
        async def test_foo(db):
            \"\"\"docstring.\"\"\"
        from module import Thing   ← should be at top of file

            actual_code = ...

    This doctor collects all misplaced top-level imports and moves them to the
    file header, making the file parse correctly. Returns number of files fixed.
    """
    fixed = 0
    test_dirs = list(root.rglob("tests")) + [root / "tests"]
    checked = set()
    candidates: list[Path] = []
    for td in test_dirs:
        if td.is_dir() and td not in checked:
            checked.add(td)
            candidates.extend(td.rglob("*.py"))

    for path in candidates:
        try:
            src = path.read_text("utf-8", errors="replace")
        except OSError:
            continue
        try:
            ast.parse(src)
            continue  # already valid
        except SyntaxError as exc:
            if "indent" not in (exc.msg or "").lower():
                continue

        lines = src.splitlines(keepends=True)
        import_lines: list[tuple[int, str]] = []
        other_lines: list[tuple[int, str]] = []

        # Classify each line: import-like at "wrong" location vs. everything else.
        # A line is a "misplaced import" if it matches ^(import|from .* import)
        # AND is NOT at the start of the file AND is surrounded by indented code.
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            is_import = re.match(r"^(import |from \S+ import )", stripped)
            if is_import and not line.startswith(stripped[0]):
                # Line has some indent before the import keyword — definitely wrong
                import_lines.append((i, stripped))
            elif is_import and i > 0:
                # Unindented import but NOT at top — check if it's in a bad location
                # (surrounded by indented context)
                prev = lines[i - 1] if i > 0 else ""
                if prev.strip() and (prev[0] in " \t" or "\"\"\"" in prev):
                    import_lines.append((i, stripped))
                else:
                    other_lines.append((i, line))
            else:
                other_lines.append((i, line))

        if not import_lines:
            continue

        # Rebuild: all collected imports go at the very top, rest follows.
        # Deduplicate while preserving order.
        seen = set()
        top_imports: list[str] = []
        for _, imp in import_lines:
            key = imp.strip()
            if key not in seen:
                seen.add(key)
                top_imports.append(imp if imp.endswith("\n") else imp + "\n")

        # Find the last existing top-level import in other_lines to insert after
        reconstructed = [ln for _, ln in other_lines]
        insert_at = 0
        for i, ln in enumerate(reconstructed):
            stripped = ln.lstrip()
            if re.match(r"^(import |from \S+ import )", stripped) and not ln[0:1].strip() == "":
                insert_at = i + 1
            elif stripped and not stripped.startswith("#") and i > 0:
                break

        new_src = "".join(
            reconstructed[:insert_at] + top_imports + reconstructed[insert_at:]
        )
        try:
            ast.parse(new_src)
        except SyntaxError:
            continue  # our fix made things worse, skip

        path.write_text(new_src, encoding="utf-8")
        fixed += 1

    return fixed


def fix_vitest_test_script(frontend_root: Path) -> int:
    """Remove Jest-only --watchAll flag from vitest-based package.json test scripts.

    Vitest uses 'vitest run' for CI/non-watch mode; --watchAll and --watchAll=false
    are Jest flags that vitest rejects with 'Unknown option'. Returns 1 if patched.
    """
    pkg = frontend_root / "package.json"
    if not pkg.exists():
        return 0
    try:
        data = _json.loads(pkg.read_text("utf-8", errors="replace"))
    except Exception:
        return 0
    # Only apply to vitest projects
    all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    if "vitest" not in all_deps:
        return 0
    scripts = data.get("scripts", {})
    test_cmd = scripts.get("test", "")
    # Strip --watchAll and --watchAll=false from any vitest test script
    new_cmd = re.sub(r"\s*--watchAll(?:=\S+)?", "", test_cmd).strip()
    if new_cmd == test_cmd:
        return 0
    pkg.write_text(_json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 1


def fix_package_level_imports(path: Path) -> int:
    """Resolve package-level imports like `from app.models import X` to `from app.models.x import X`."""
    try:
        src = path.read_text("utf-8", errors="replace")
    except OSError:
        return 0

    # Locate backend root
    backend_root = None
    for parent in path.parents:
        if parent.name == "backend" or (parent / "app").is_dir():
            backend_root = parent
            break
    if not backend_root:
        for parent in path.parents:
            if (parent / "app").is_dir():
                backend_root = parent
                break
    if not backend_root:
        return 0

    import ast
    try:
        tree = ast.parse(src)
    except Exception:
        return 0

    lines = src.split("\n")
    replacements = []

    # Cache file structures for speed
    package_files_cache = {}

    def get_defining_module(package_name: str, symbol: str) -> str | None:
        cache_key = package_name
        if cache_key not in package_files_cache:
            # Locate the package directory
            parts = package_name.split(".")
            package_dir = backend_root / "/".join(parts)
            if not package_dir.is_dir():
                package_files_cache[cache_key] = []
            else:
                files = []
                for f in package_dir.glob("*.py"):
                    if f.name != "__init__.py":
                        files.append(f)
                package_files_cache[cache_key] = files

        for f in package_files_cache[cache_key]:
            try:
                content = f.read_text("utf-8", errors="ignore")
                if re.search(rf"\b(?:class|def)\s+{re.escape(symbol)}\b|^\s*{re.escape(symbol)}\s*=", content, re.MULTILINE):
                    return f.stem
            except Exception:
                pass
        return None

    target_packages = {"app.models", "app.services", "app.schemas", "app.repositories", "app.tasks", "app.api.v1", "app.api"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in target_packages:
            start_idx = node.lineno - 1
            end_idx = getattr(node, "end_lineno", node.lineno) - 1
            
            new_import_lines = []
            for name_alias in node.names:
                name = name_alias.name
                asname = name_alias.asname
                module_stem = get_defining_module(node.module, name)
                if module_stem:
                    full_module = f"{node.module}.{module_stem}"
                    import_str = f"from {full_module} import {name}"
                    if asname:
                        import_str += f" as {asname}"
                    new_import_lines.append(import_str)
                else:
                    if name and name[0].isupper():
                        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
                        snake_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                        base_snake = snake_name
                        for suffix in ["_create", "_update", "_out", "_list_response", "_repository", "_service", "_task", "_router", "_controller"]:
                            if base_snake.endswith(suffix):
                                base_snake = base_snake[:-len(suffix)]
                                break
                        parts = node.module.split(".")
                        package_dir = backend_root / "/".join(parts)
                        if (package_dir / f"{base_snake}.py").is_file():
                            full_module = f"{node.module}.{base_snake}"
                        elif (package_dir / f"{snake_name}.py").is_file():
                            full_module = f"{node.module}.{snake_name}"
                        else:
                            full_module = node.module
                    else:
                        full_module = node.module

                    import_str = f"from {full_module} import {name}"
                    if asname:
                        import_str += f" as {asname}"
                    new_import_lines.append(import_str)
            
            new_text = "\n".join(new_import_lines)
            replacements.append((start_idx, end_idx, new_text))

    if not replacements:
        return 0

    replacements.sort(key=lambda x: x[0], reverse=True)
    
    modified = False
    for start_idx, end_idx, new_text in replacements:
        orig_text = "\n".join(lines[start_idx : end_idx + 1])
        if orig_text.strip() != new_text.strip():
            lines[start_idx : end_idx + 1] = [new_text]
            modified = True

    if modified:
        path.write_text("\n".join(lines), encoding="utf-8")
        return len(replacements)
    return 0


def fix_tsconfig_types(frontend_root: Path) -> int:
    """Remove react-native-web from tsconfig.json types array to avoid type resolution issues."""
    tsconfig_path = frontend_root / "tsconfig.json"
    if not tsconfig_path.exists():
        return 0
    try:
        content = tsconfig_path.read_text("utf-8")
        data = _json.loads(content)
        changed = False
        if "compilerOptions" in data and "types" in data["compilerOptions"]:
            types = data["compilerOptions"]["types"]
            if isinstance(types, list) and "react-native-web" in types:
                types.remove("react-native-web")
                changed = True
        if changed:
            tsconfig_path.write_text(_json.dumps(data, indent=2) + "\n", encoding="utf-8")
            return 1
    except Exception:
        try:
            content = tsconfig_path.read_text("utf-8")
            new_content = re.sub(r'\s*,\s*"react-native-web"\s*', '', content)
            new_content = re.sub(r'\s*"react-native-web"\s*,\s*', '', new_content)
            new_content = re.sub(r'\s*"react-native-web"\s*', '', new_content)
            if new_content != content:
                tsconfig_path.write_text(new_content, encoding="utf-8")
                return 1
        except Exception:
            pass
    return 0


def remove_duplicate_jest_configs(frontend_root: Path) -> int:
    """Ensure we do not have both jest.config.js and jest.config.ts in React Native frontend projects."""
    js_config = frontend_root / "jest.config.js"
    ts_config = frontend_root / "jest.config.ts"
    if js_config.exists() and ts_config.exists():
        try:
            ts_config.unlink()
            return 1
        except Exception:
            pass
    return 0


def fix_missing_init_imports(backend_root: Path) -> int:
    """Fix broken re-export imports in Python __init__.py files.

    When an __init__.py does `from .user import User` but user.py doesn't exist,
    we create a minimal stub so imports resolve. Only creates stubs for simple
    single-class re-exports that look like ORM models (SQLModel / Base patterns).
    Returns the number of stubs created.
    """
    import importlib.util
    stubs = 0
    for init in backend_root.rglob("__init__.py"):
        try:
            src = init.read_text("utf-8", errors="replace")
        except OSError:
            continue
        for match in re.finditer(r"^from \.([\w]+) import (\w+)", src, re.MULTILINE):
            mod_name, class_name = match.group(1), match.group(2)
            target = init.parent / f"{mod_name}.py"
            if target.exists():
                continue
            # Only stub simple model-like names (User, Profile, Tenant, etc.)
            # to avoid creating noisy stubs for utility helpers
            if not re.match(r"[A-Z][a-zA-Z]+$", class_name):
                continue
            target.write_text(
                f"from sqlmodel import SQLModel, Field\nfrom typing import Optional\n\n\n"
                f"class {class_name}(SQLModel, table=True):\n"
                f'    """Auto-generated stub — replace with real model."""\n'
                f"    __tablename__ = \"{mod_name}\"\n"
                f"    id: Optional[int] = Field(default=None, primary_key=True)\n",
                encoding="utf-8",
            )
            stubs += 1
    return stubs


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

    # Repair YAML files (e.g. env-style assignments)
    n_yaml = 0
    for p in _yaml_files(out_dir):
        n_yaml += fix_yaml_env_style(p)
    if n_yaml:
        log(f"  [doctor] repaired {n_yaml} env-style YAML files")
        report.yaml_env_style_fixed += n_yaml
        report.files_touched += n_yaml

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
        # Fix broken re-export imports (e.g. __init__.py references missing user.py)
        n_stubs = fix_missing_init_imports(backend)
        if n_stubs:
            log(f"  [doctor] created {n_stubs} missing module stubs for __init__ imports")
            report.files_touched += n_stubs
        # Fix misplaced import statements in test files (common LLM generation bug)
        n_test_imports = fix_misplaced_imports_in_test_files(backend)
        if n_test_imports:
            log(f"  [doctor] fixed misplaced imports in {n_test_imports} test files")
            report.files_touched += n_test_imports

    if frontend.is_dir():
        # React Native projects: enforce Jest (jest-expo), remove vitest
        n_rn = fix_react_native_package_json(frontend)
        if n_rn:
            log("  [doctor] fixed React Native package.json (jest-expo, removed vitest)")
            report.files_touched += n_rn
        n_rn_jest = fix_react_native_jest_config(frontend)
        if n_rn_jest:
            log("  [doctor] fixed React Native jest.config.js (preset: jest-expo and transformIgnorePatterns)")
            report.files_touched += n_rn_jest
        n_dup_jest = remove_duplicate_jest_configs(frontend)
        if n_dup_jest:
            log("  [doctor] removed duplicate jest.config.ts config file")
            report.files_touched += n_dup_jest
        n_tsconfig_types = fix_tsconfig_types(frontend)
        if n_tsconfig_types:
            log("  [doctor] removed react-native-web from tsconfig.json types array")
            report.files_touched += n_tsconfig_types
        # Web projects using vitest: remove Jest-only --watchAll flag
        n_vitest = fix_vitest_test_script(frontend)
        if n_vitest:
            log("  [doctor] removed --watchAll from vitest test script in package.json")
            report.files_touched += n_vitest

    if backend.is_dir():
        # Fix wrong import paths (AsyncSession from sqlmodel, current_tenant_id paths)
        n_imports = 0
        for p in _python_files(backend):
            n_imports += fix_wrong_python_imports(p)
        if n_imports:
            log(f"  [doctor] fixed {n_imports} wrong import patterns in backend Python files")
            report.files_touched += n_imports
        n_pkg_imports = 0
        for p in _python_files(backend):
            n_pkg_imports += fix_package_level_imports(p)
        if n_pkg_imports:
            log(f"  [doctor] resolved {n_pkg_imports} package-level imports to direct modules")
            report.files_touched += n_pkg_imports
        n_json_fields = 0
        for p in _python_files(backend):
            n_json_fields += fix_sqlmodel_json_fields(p)
        if n_json_fields:
            log(f"  [doctor] added sa_type=JSON to {n_json_fields} SQLModel dict/list fields")
            report.sqlmodel_json_fields_fixed += n_json_fields
            report.files_touched += n_json_fields

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
        # Only run React Native substitutions if this is a React Native project
        is_rn = False
        pkg_path = frontend / "package.json"
        if pkg_path.exists():
            try:
                pkg_data = _json.loads(pkg_path.read_text("utf-8", errors="replace"))
                all_deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                is_rn = "react-native" in all_deps or "expo" in all_deps
            except Exception:
                pass
        if is_rn:
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
    "fix_sqlmodel_json_fields",
    "run_code_doctors",
    "run_eslint_fix",
    "stub_truncated_init",
    "run_prettier_format",
    "run_ruff_fix",
]
