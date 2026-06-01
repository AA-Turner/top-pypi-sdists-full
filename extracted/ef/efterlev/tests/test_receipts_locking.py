"""Tests for cross-platform file locking in `efterlev.provenance.receipts`.

v0.1.22's fix to the release-smoke matrix-assertion script surfaced a
real product bug: `src/efterlev/provenance/receipts.py` had `import
fcntl` unconditionally, but `fcntl` is POSIX-only — the wheel was
un-importable on Windows (`ModuleNotFoundError: No module named
'fcntl'`), and the silent-matrix gap kept the bug invisible across
every release since `fcntl` was added.

v0.1.23 wraps the lock primitives behind `_flock_exclusive` /
`_flock_release` helpers that pick `fcntl` on POSIX and `msvcrt` on
Windows. These tests:

- Lock against the regression by importing the module on the current
  platform (so import-time errors fail the test suite).
- Verify the helpers are bound (sanity check that the platform-detection
  branch picked one of the two implementations).
- Exercise an end-to-end append path on the platform-correct lock
  primitives, proving they let multiple sequential appends succeed.

Cross-platform `msvcrt.locking` semantics aren't fully exercised here
(would need a Windows runner for the actual lock-window test), but the
matrix in `release-smoke` validates the Windows + macOS + Linux paths
in CI; this file pins the contract that the helpers are at least
importable + functional on the platform the test suite runs on.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

from efterlev.models import ProvenanceRecord
from efterlev.provenance import receipts as receipts_module
from efterlev.provenance.receipts import ReceiptLog, _flock_exclusive, _flock_release


def test_module_imports_on_current_platform() -> None:
    """The receipts module must be importable on every platform efterlev
    targets. v0.1.20-v0.1.22 silently failed Windows because the
    unconditional `import fcntl` raised at import time."""
    assert receipts_module is not None


def test_lock_helpers_are_bound() -> None:
    """Sanity: the platform-detection branch selected one of the two
    implementations and bound both names."""
    assert callable(_flock_exclusive)
    assert callable(_flock_release)


def test_platform_specific_lock_backend_picked() -> None:
    """Lock helpers wire to the correct stdlib module per platform."""
    if sys.platform == "win32":
        # On Windows, _flock_exclusive should call msvcrt.locking.
        # Best we can do without monkey-patching: confirm msvcrt was
        # imported into the receipts module's namespace.
        assert hasattr(receipts_module, "msvcrt")
    else:
        assert hasattr(receipts_module, "fcntl")


def test_append_and_read_round_trip(tmp_path: Path) -> None:
    """End-to-end: a receipt append + read on the current platform's
    lock primitives produces the expected JSONL line."""
    log_path = tmp_path / "receipts.log"
    log = ReceiptLog(log_path)
    record = ProvenanceRecord(
        record_id="rec-1",
        record_type="evidence",
        content_ref="sha256:" + "a" * 64,
        derived_from=[],
        primitive=None,
        agent=None,
        model=None,
        prompt_hash=None,
        timestamp=datetime(2026, 5, 7, tzinfo=UTC),
        metadata={},
    )
    log.append(record)
    log.append(record)  # second append acquires lock again — proves release worked
    lines = log.read_all()
    assert len(lines) == 2
    assert lines[0]["record_id"] == "rec-1"
    assert lines[1]["record_id"] == "rec-1"


def test_no_unconditional_fcntl_import_in_receipts() -> None:
    """Hard-lock the regression: a careless edit reverting back to
    `import fcntl` at the top would silently break Windows again. Pin
    against that by reading the source file."""
    src = Path(receipts_module.__file__).read_text(encoding="utf-8")
    # An unconditional `import fcntl` line at module top would be the
    # regression. The current pattern uses `import fcntl` only inside
    # `else:` after `if sys.platform == "win32":`. Pin both shapes.
    assert "if sys.platform" in src
    assert "import msvcrt" in src
    # The bare top-level import (no leading whitespace) is what we're
    # protecting against.
    for line in src.splitlines():
        if line.startswith("import fcntl") or line.startswith("from fcntl"):
            raise AssertionError(
                f"receipts.py has top-level fcntl import: {line!r}. "
                "Use the platform-gated _flock_exclusive / _flock_release "
                "helpers instead."
            )


def test_windows_lock_helpers_lseek_to_byte_zero_before_lock_and_unlock() -> None:
    """Source-level pin against v0.1.26's msvcrt.locking byte-range bug.

    msvcrt.locking is byte-range based — lock + unlock must target the
    same byte range. With O_APPEND, file position advances after each
    write, so without explicit lseek(0) before both lock and unlock,
    the unlock targets a different byte range than the lock and fails
    with PermissionError [Errno 13]. v0.1.25 release-smoke matrix
    Windows-2022 cell hit this; v0.1.26 fixes it by lseek-ing to byte 0
    before each msvcrt.locking call.

    This test is platform-independent: it reads receipts.py source and
    asserts the lseek-to-zero pattern is present in BOTH the lock and
    unlock helpers within the Windows branch. A regression that drops
    the lseek would re-break Windows; this test catches it on macOS /
    Linux dev laptops, no Windows runner needed.
    """
    src = Path(receipts_module.__file__).read_text(encoding="utf-8")
    # Find the Windows branch (`if sys.platform == "win32":`) and assert
    # the body contains the lseek-then-lock-and-lseek-then-unlock pattern
    # for both helpers. We grep for the full function bodies inside the
    # win32 branch — easier than parsing AST and just as load-bearing.
    win_branch_start = src.find('if sys.platform == "win32":')
    assert win_branch_start >= 0, "Windows branch not found in receipts.py"
    # The else: branch starts the POSIX implementation; everything
    # between the if and else is Windows code.
    else_branch_start = src.find("else:", win_branch_start)
    assert else_branch_start > win_branch_start
    win_branch = src[win_branch_start:else_branch_start]
    # Both helpers must lseek before their msvcrt.locking call.
    assert "os.lseek(fd, 0, os.SEEK_SET)" in win_branch, (
        "Windows branch must lseek(fd, 0) before msvcrt.locking — without "
        "it, lock + unlock target different byte ranges (after O_APPEND "
        "write) and msvcrt.locking raises PermissionError on unlock."
    )
    # At least 2 occurrences (one before LK_LOCK, one before LK_UNLCK).
    assert win_branch.count("os.lseek(fd, 0, os.SEEK_SET)") >= 2, (
        "Windows branch must lseek(fd, 0) before BOTH msvcrt.locking calls "
        "(one before LK_LOCK, one before LK_UNLCK). Found "
        f"{win_branch.count('os.lseek(fd, 0, os.SEEK_SET)')} occurrences; "
        "expected at least 2."
    )
    # Both LK_LOCK and LK_UNLCK should appear in the win branch.
    assert "LK_LOCK" in win_branch
    assert "LK_UNLCK" in win_branch
