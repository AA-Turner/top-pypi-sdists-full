#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Check that all compat modules have a COMPAT_REMOVAL_DATE comment.

Any .py file under src/omnibase_compat/ that defines a class and was committed
more than 30 days ago must carry:

    # COMPAT_MIGRATION_TARGET: <canonical.module.path>
    # COMPAT_REMOVAL_DATE: YYYY-MM-DD

Exits 1 if stale modules are found (missing removal date, or removal date passed).

Pre-expiry warning window (OMN-13879)
-------------------------------------
A hardcoded ``COMPAT_REMOVAL_DATE`` silently converts to a CI-wedging hard
failure the moment it passes, with no advance notice — a ``looks-fine-until-it-
isn't`` time bomb that blocked the whole compat merge queue on 2026-07-01. To
give the owner lead time, any module whose removal date falls within the next
``COMPAT_RETENTION_WARN_DAYS`` days (default 14) is reported as a **non-fatal
WARNING** — printed but NOT counted as a violation, so the gate stays green
while the date is still in the future. The hard-fail on a *passed* date is
unchanged.

Run: python scripts/check_compat_retention.py
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from collections.abc import Callable
from datetime import date, datetime
from pathlib import Path

SRC = Path("src/omnibase_compat")
SKIP_FILES = {"__init__.py"}
SKIP_MARKER = "compat-skip-retention:"
REMOVAL_DATE_RE = re.compile(r"#\s*COMPAT_REMOVAL_DATE:\s*(\d{4}-\d{2}-\d{2})")
STALE_THRESHOLD_DAYS = 30

# OMN-13879: warn this many days before a removal date expires. Override with
# the COMPAT_RETENTION_WARN_DAYS env var (non-negative int; invalid/blank falls
# back to the default).
DEFAULT_WARN_WINDOW_DAYS = 14
WARN_WINDOW_ENV = "COMPAT_RETENTION_WARN_DAYS"


def resolve_warn_window_days(environ: dict[str, str] | None = None) -> int:
    """Resolve the pre-expiry warning window in days.

    Honours ``COMPAT_RETENTION_WARN_DAYS`` when it is a non-negative integer;
    otherwise returns :data:`DEFAULT_WARN_WINDOW_DAYS`. A malformed or negative
    value falls back to the default rather than raising — the gate must never
    fail *because of* its own warning knob.
    """
    raw = (environ if environ is not None else os.environ).get(WARN_WINDOW_ENV, "").strip()
    if not raw:
        return DEFAULT_WARN_WINDOW_DAYS
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_WARN_WINDOW_DAYS
    return value if value >= 0 else DEFAULT_WARN_WINDOW_DAYS


def get_file_commit_date(path: Path) -> date | None:
    """Return the earliest commit date for a file, or None if untracked."""
    result = subprocess.run(
        ["git", "log", "--follow", "--format=%aI", "--", str(path)],
        capture_output=True,
        text=True,
    )
    lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    # Last line = oldest commit
    oldest = lines[-1]
    return datetime.fromisoformat(oldest).date()


def has_skip_marker(text: str) -> bool:
    return any(SKIP_MARKER in line for line in text.splitlines()[:10])


def has_class_definition(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return False
    return any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))


def classify_module(
    *,
    text: str,
    commit_date: date,
    today: date,
    warn_window_days: int,
) -> tuple[str, str | None]:
    """Classify one compat module against the retention policy.

    Pure function — no I/O — so the date logic is exhaustively unit-testable.

    Returns ``(status, message)`` where ``status`` is one of:

    * ``"ok"``        — compliant, no action needed (message is ``None``).
    * ``"warn"``      — removal date is in the future but within the warning
                        window; report but do NOT fail the gate.
    * ``"violation"`` — missing removal date on an aged file, or a date that has
                        already passed; fail the gate.
    """
    days_old = (today - commit_date).days
    match = REMOVAL_DATE_RE.search(text)

    if match is None:
        if days_old > STALE_THRESHOLD_DAYS:
            return (
                "violation",
                f"no COMPAT_REMOVAL_DATE comment"
                f" (committed {days_old} days ago, threshold {STALE_THRESHOLD_DAYS})",
            )
        return "ok", None

    removal_date = date.fromisoformat(match.group(1))
    if removal_date < today:
        return (
            "violation",
            f"COMPAT_REMOVAL_DATE {removal_date} has passed"
            f" (today is {today}) — migrate or extend the date",
        )

    days_until = (removal_date - today).days
    if days_until <= warn_window_days:
        return (
            "warn",
            f"COMPAT_REMOVAL_DATE {removal_date} expires in {days_until} day(s)"
            f" (today is {today}) — decide before it hard-fails CI:"
            f" migrate the shim or consciously extend the date",
        )

    return "ok", None


def scan_tree(
    src: Path,
    *,
    today: date,
    warn_window_days: int,
    commit_date_fn: Callable[[Path], date | None] = get_file_commit_date,
) -> tuple[list[str], list[str]]:
    """Walk ``src`` and partition modules into (violations, warnings).

    ``commit_date_fn`` is injectable so tests can supply deterministic dates
    without a git checkout.
    """
    violations: list[str] = []
    warnings: list[str] = []

    for py_file in sorted(src.rglob("*.py")):
        if py_file.name in SKIP_FILES:
            continue

        text = py_file.read_text(encoding="utf-8")

        if has_skip_marker(text):
            continue

        if not has_class_definition(py_file):
            continue

        commit_date = commit_date_fn(py_file)
        if commit_date is None:
            # Untracked file — skip (not yet committed)
            continue

        status, message = classify_module(
            text=text,
            commit_date=commit_date,
            today=today,
            warn_window_days=warn_window_days,
        )
        if status == "violation":
            violations.append(f"{py_file}: {message}")
        elif status == "warn":
            warnings.append(f"{py_file}: {message}")

    return violations, warnings


def main(argv: list[str] | None = None) -> int:
    """Run the retention check. Returns process exit code (0 ok, 1 violations)."""
    warn_window_days = resolve_warn_window_days()
    today = date.today()

    violations, warnings = scan_tree(SRC, today=today, warn_window_days=warn_window_days)

    # Pre-expiry warnings are advisory: printed, never fatal.
    if warnings:
        print(
            f"WARNING — {len(warnings)} compat module(s) approach "
            f"COMPAT_REMOVAL_DATE within {warn_window_days} days:"
        )
        for w in warnings:
            print(f"  {w}")
        print(
            "\nAct before expiry: an expired COMPAT_REMOVAL_DATE HARD-FAILS the "
            "`validate` job and wedges the compat merge queue for every PR. "
            "Either remove the migrated shim or consciously extend the date."
        )
        print()

    if violations:
        print("FAIL — stale compat modules found:")
        for v in violations:
            print(f"  {v}")
        print()
        print(
            "Each compat module with class definitions must carry:\n"
            "  # COMPAT_MIGRATION_TARGET: <canonical.module.path>\n"
            "  # COMPAT_REMOVAL_DATE: YYYY-MM-DD\n"
            "Or add '# compat-skip-retention: <reason>' in the first 10 lines to exempt."
        )
        return 1

    count = sum(1 for _ in SRC.rglob("*.py"))
    suffix = f" ({len(warnings)} pre-expiry warning(s))" if warnings else ""
    print(f"OK — scanned {count} files, no stale compat modules.{suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
