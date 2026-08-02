# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for the compat retention gate's pre-expiry warning window (OMN-13879).

A hardcoded ``COMPAT_REMOVAL_DATE`` silently converts to a CI-wedging hard
failure the moment it passes (this is what wedged compat dev on 2026-07-01).
The warning window prints a non-fatal WARNING for the N days before a date
expires so the owner has lead time, while preserving the hard-fail on a passed
date. These tests pin both the pure ``classify_module`` date logic and the
``scan_tree`` partition (with an injected commit-date probe so no git checkout
is needed).
"""

from __future__ import annotations

import importlib.util
from datetime import date
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_compat_retention.py"

_TODAY = date(2026, 7, 3)
# Committed well beyond the 30-day stale threshold so date logic is exercised.
_OLD_COMMIT = date(2026, 1, 1)


def _load_module():
    spec = importlib.util.spec_from_file_location("check_compat_retention", _SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def mod():
    return _load_module()


def _module_text(removal_date: str | None) -> str:
    header = "class Foo:\n    pass\n"
    if removal_date is None:
        return header
    return (
        "# COMPAT_MIGRATION_TARGET: omnibase_core.models.foo\n"
        f"# COMPAT_REMOVAL_DATE: {removal_date}\n" + header
    )


# ---------------------------------------------------------------------------
# classify_module — pure date logic
# ---------------------------------------------------------------------------


def test_expired_date_is_violation(mod) -> None:
    status, message = mod.classify_module(
        text=_module_text("2026-07-01"),
        commit_date=_OLD_COMMIT,
        today=_TODAY,
        warn_window_days=14,
    )
    assert status == "violation"
    assert "has passed" in message


def test_date_within_window_is_warn(mod) -> None:
    # 10 days out, window 14 → warn (non-fatal).
    status, message = mod.classify_module(
        text=_module_text("2026-07-13"),
        commit_date=_OLD_COMMIT,
        today=_TODAY,
        warn_window_days=14,
    )
    assert status == "warn"
    assert "expires in 10 day(s)" in message


def test_date_beyond_window_is_ok(mod) -> None:
    # 60 days out, window 14 → clean.
    status, message = mod.classify_module(
        text=_module_text("2026-09-01"),
        commit_date=_OLD_COMMIT,
        today=_TODAY,
        warn_window_days=14,
    )
    assert status == "ok"
    assert message is None


def test_date_equal_today_is_warn_not_violation(mod) -> None:
    # The removal date's own day is still valid (not < today) — warn, don't fail.
    status, message = mod.classify_module(
        text=_module_text("2026-07-03"),
        commit_date=_OLD_COMMIT,
        today=_TODAY,
        warn_window_days=14,
    )
    assert status == "warn"
    assert "expires in 0 day(s)" in message


def test_window_boundary_is_inclusive(mod) -> None:
    # Exactly warn_window_days away → still warn (<=).
    status, _ = mod.classify_module(
        text=_module_text("2026-07-17"),  # 14 days out
        commit_date=_OLD_COMMIT,
        today=_TODAY,
        warn_window_days=14,
    )
    assert status == "warn"


def test_missing_date_old_file_is_violation(mod) -> None:
    status, message = mod.classify_module(
        text=_module_text(None),
        commit_date=_OLD_COMMIT,
        today=_TODAY,
        warn_window_days=14,
    )
    assert status == "violation"
    assert "no COMPAT_REMOVAL_DATE" in message


def test_missing_date_new_file_is_ok(mod) -> None:
    # Committed 5 days ago — under the 30-day stale threshold.
    status, message = mod.classify_module(
        text=_module_text(None),
        commit_date=date(2026, 6, 28),
        today=_TODAY,
        warn_window_days=14,
    )
    assert status == "ok"
    assert message is None


# ---------------------------------------------------------------------------
# resolve_warn_window_days — env override
# ---------------------------------------------------------------------------


def test_warn_window_default(mod) -> None:
    assert mod.resolve_warn_window_days({}) == mod.DEFAULT_WARN_WINDOW_DAYS


def test_warn_window_custom(mod) -> None:
    assert mod.resolve_warn_window_days({"COMPAT_RETENTION_WARN_DAYS": "30"}) == 30


def test_warn_window_zero_disables(mod) -> None:
    # 0 is valid — only same-day/past dates warn/fail; nothing pre-warns.
    assert mod.resolve_warn_window_days({"COMPAT_RETENTION_WARN_DAYS": "0"}) == 0


@pytest.mark.parametrize("bad", ["", "  ", "abc", "-5", "3.5"])
def test_warn_window_invalid_falls_back(mod, bad: str) -> None:
    assert (
        mod.resolve_warn_window_days({"COMPAT_RETENTION_WARN_DAYS": bad})
        == mod.DEFAULT_WARN_WINDOW_DAYS
    )


# ---------------------------------------------------------------------------
# scan_tree — partition with an injected commit-date probe
# ---------------------------------------------------------------------------


def test_scan_tree_partitions_violation_warn_ok(mod, tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "expired.py").write_text(_module_text("2026-07-01"))
    (src / "soon.py").write_text(_module_text("2026-07-10"))  # 7 days → warn
    (src / "far.py").write_text(_module_text("2027-06-01"))  # ok
    (src / "__init__.py").write_text("")  # skipped

    violations, warnings = mod.scan_tree(
        src,
        today=_TODAY,
        warn_window_days=14,
        commit_date_fn=lambda _p: _OLD_COMMIT,
    )

    assert len(violations) == 1
    assert "expired.py" in violations[0]
    assert len(warnings) == 1
    assert "soon.py" in warnings[0]


def test_scan_tree_skip_marker_and_untracked(mod, tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "exempt.py").write_text(
        "# compat-skip-retention: intentional\n" + _module_text("2026-07-01")
    )
    (src / "untracked.py").write_text(_module_text("2026-07-01"))

    def commit_date_fn(p: Path) -> date | None:
        return None if p.name == "untracked.py" else _OLD_COMMIT

    violations, warnings = mod.scan_tree(
        src,
        today=_TODAY,
        warn_window_days=14,
        commit_date_fn=commit_date_fn,
    )

    # exempt.py skipped by marker, untracked.py skipped by None commit date.
    assert violations == []
    assert warnings == []
