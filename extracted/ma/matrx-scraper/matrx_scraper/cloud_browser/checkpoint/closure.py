"""Proving a profile is CLOSED before archiving (S3 §4).

A live-directory snapshot fails WORSE than "invalid" — it comes back looking healthy
and signed out (PLAN.md §Encryption design, proof P3). A boolean "we called close()"
is not proof. Five checks must pass; the engine refuses to archive otherwise and
records what it saw in ``closure_proof``.

Process / fd inspection is injectable (``ProcessInspector``) so this is fully
testable with no real Chromium: the default inspector reads ``/proc`` on Linux.
"""

from __future__ import annotations

import glob
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from matrx_orm import check_local_sqlite_integrity, read_local_sqlite_rows

from .constants import COOKIE_SCHEME_BASIC, COOKIE_SCHEME_KEYRING
from .errors import ClosureError
from .manifest import ClosureProof
from datetime import UTC


class ProcessInspector(Protocol):
    """Reports process / file-descriptor evidence about a profile directory."""

    def pids_using_dir(self, profile_dir: Path) -> list[int]:
        """PIDs whose cmdline names this user_data_dir."""
        ...

    def open_fd_paths(self, profile_dir: Path) -> list[str]:
        """Open fd symlink targets that point under the profile tree."""
        ...


class ProcProcessInspector:
    """Default Linux inspector over ``/proc`` (S3 §4 checks 2 and 3)."""

    def pids_using_dir(self, profile_dir: Path) -> list[int]:
        needle = str(profile_dir.resolve())
        found: list[int] = []
        for cmdline in glob.glob("/proc/*/cmdline"):
            try:
                with open(cmdline, "rb") as fh:
                    args = fh.read().replace(b"\x00", b" ").decode(errors="ignore")
            except OSError:
                continue
            if needle in args:
                try:
                    found.append(int(cmdline.split("/")[2]))
                except (IndexError, ValueError):
                    pass
        return found

    def open_fd_paths(self, profile_dir: Path) -> list[str]:
        needle = str(profile_dir.resolve())
        hits: list[str] = []
        for fd_link in glob.glob("/proc/*/fd/*"):
            try:
                target = os.readlink(fd_link)
            except OSError:
                continue
            if target.startswith(needle):
                hits.append(target)
        return hits


_SINGLETON_FILES = ("SingletonLock", "SingletonCookie", "SingletonSocket")
_SQLITE_TARGETS = (
    "Default/Cookies",
    "Default/Login Data",
    "Default/Network/Network Persistent State",
)


@dataclass
class _WallClock:
    def now_iso(self) -> str:
        from datetime import datetime

        return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _singleton_held(profile_dir: Path) -> list[str]:
    """Present-and-live singleton files. A dangling symlink (stale) does not count."""
    held: list[str] = []
    for name in _SINGLETON_FILES:
        p = profile_dir / name
        if not p.is_symlink() and not p.exists():
            continue
        if p.is_symlink():
            # dangling symlink == stale == released
            try:
                os.stat(p)  # follows link
            except OSError:
                continue
        held.append(name)
    return held


def _sqlite_settled(profile_dir: Path) -> tuple[list[str], str, int]:
    """Run PRAGMA quick_check read-only on each present SQLite DB; check WAL is flushed.

    Returns (checked_files, result, wal_bytes_remaining). Raises ``sqlite_unsettled``
    on any non-``ok`` quick_check or a non-empty WAL.
    """
    checked: list[str] = []
    wal_remaining = 0
    for rel in _SQLITE_TARGETS:
        db = profile_dir / rel
        if not db.exists():
            continue
        for sidecar_suffix in ("-wal", "-journal"):
            sidecar = Path(str(db) + sidecar_suffix)
            if sidecar.exists() and sidecar.stat().st_size > 0:
                wal_remaining += sidecar.stat().st_size
        try:
            result = check_local_sqlite_integrity(db)
        except sqlite3.Error as exc:
            raise ClosureError(
                f"sqlite quick_check could not run on {rel}: {exc}",
                code="sqlite_unsettled",
            ) from exc
        checked.append(rel)
        if result != "ok":
            raise ClosureError(
                f"sqlite quick_check failed on {rel}: {result}", code="sqlite_unsettled"
            )
    if wal_remaining > 0:
        raise ClosureError(
            f"non-empty WAL/journal sidecar(s) remain: {wal_remaining} bytes unflushed",
            code="sqlite_unsettled",
        )
    return checked, "ok", wal_remaining


def prove_closed(
    profile_dir: Path,
    *,
    context_closed_at: str,
    process_exit_confirmed_at: str,
    close_wait_ms: int,
    escalation: str = "none",
    inspector: ProcessInspector | None = None,
) -> ClosureProof:
    """Run the five closure checks (S3 §4). Raises ``ClosureError`` on the first fail.

    ``context_closed_at`` / ``process_exit_confirmed_at`` / ``close_wait_ms`` /
    ``escalation`` are the worker's record of the shutdown it performed (check 1); the
    remaining checks (2-5) are verified here against the on-disk state.
    """
    profile_dir = profile_dir.resolve()
    if not profile_dir.is_dir():
        raise ClosureError(f"profile dir not found: {profile_dir}", code="close_not_completed")
    inspector = inspector or ProcProcessInspector()

    # Check 2 — no live Chromium process on this profile.
    pids = inspector.pids_using_dir(profile_dir)
    if pids:
        raise ClosureError(
            f"chromium still running on profile (pids={pids})",
            code="chromium_still_running",
        )

    # Check 3 — no open fds into the profile tree.
    open_fds = inspector.open_fd_paths(profile_dir)
    if open_fds:
        raise ClosureError(
            f"open file descriptors into profile: {open_fds}",
            code="open_file_descriptors",
        )

    # Check 4 — singleton locks released.
    held = _singleton_held(profile_dir)
    if held:
        raise ClosureError(f"singleton lock(s) held: {held}", code="singleton_lock_held")

    # Check 5 — SQLite settled.
    checked, sqlite_result, wal_remaining = _sqlite_settled(profile_dir)

    if escalation not in ("none", "sigterm", "sigkill"):
        raise ClosureError(f"invalid escalation {escalation!r}", code="close_not_completed")

    return ClosureProof(
        context_closed_at=context_closed_at,
        process_exit_confirmed_at=process_exit_confirmed_at,
        close_wait_ms=close_wait_ms,
        escalation=escalation,  # type: ignore[arg-type]
        open_fd_count=0,
        singleton_files_present=[],
        sqlite_checked=checked,
        sqlite_result=sqlite_result,
        wal_bytes_remaining=wal_remaining,
    )


def detect_cookie_scheme(profile_dir: Path) -> str:
    """Observe the Chromium cookie encryption scheme from ``Default/Cookies`` (D-5).

    Reads the ``encrypted_value`` prefix of the cookies table: ``v10`` = basic store
    (portable), ``v11`` = keyring key living outside the profile dir (NOT portable).
    Defaults to the basic scheme when there are no encrypted rows to observe — the
    worker image is asserted keyring-free at build time, so v10 is the expected state.
    """
    db = profile_dir / "Default" / "Cookies"
    if not db.exists():
        return COOKIE_SCHEME_BASIC
    try:
        rows = read_local_sqlite_rows(
            db,
            table="cookies",
            columns=("encrypted_value",),
            where_not_null=("encrypted_value",),
            min_lengths={"encrypted_value": 3},
            limit=50,
        )
    except sqlite3.Error:
        return COOKIE_SCHEME_BASIC
    for (blob,) in rows:
        if not blob:
            continue
        prefix = bytes(blob[:3])
        if prefix == b"v11":
            return COOKIE_SCHEME_KEYRING
        if prefix == b"v10":
            return COOKIE_SCHEME_BASIC
    return COOKIE_SCHEME_BASIC
