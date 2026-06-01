"""JSONL append-only receipt log for the provenance store.

One line per `write_record` call. The log is an independent sidechannel to the
SQLite store: a `verify_receipts` walk cross-checks the two to surface any
tampering that content-addressing alone can't catch (consistent rewrites of
both the SQLite DB and the blob store would pass hash verification but leave
the receipt log visibly out of sync).

Atomicity: each append opens the file in `O_APPEND` mode, takes an exclusive
`fcntl.flock`, writes a single JSON line + newline, and fsyncs. POSIX-only
(macOS + Linux); Windows support is on the v1.5+ roadmap.

Per-line schema (stable):

    {
      "ts":            ISO-8601 string,
      "record_id":     "sha256:...",
      "record_type":   one of evidence|claim|finding|mapping|remediation,
      "derived_from":  ["sha256:...", ...],
      "primitive":     "name@version" | null,
      "agent":         "name" | null,
      "model":         "model-id" | null,
      "prompt_hash":   "sha256:..." | null
    }

Per DECISIONS 2026-04-20 (design call #5): full `derived_from` list is stored
inline rather than hashed so a reader can reconstruct chain topology from the
log alone if the SQLite store is lost or suspect.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from efterlev.errors import ProvenanceError
from efterlev.models import ProvenanceRecord

# Cross-platform exclusive file lock around append. fcntl.flock is POSIX-
# only; on Windows the stdlib equivalent is msvcrt.locking. v0.1.22's
# release-smoke matrix repair surfaced that this module's prior
# unconditional `import fcntl` made the wheel un-importable on Windows
# (`ModuleNotFoundError: No module named 'fcntl'`), which silently broke
# every Windows install since fcntl was added to receipts.py — masked
# until v0.1.22 fixed the matrix's assertion script and Windows cells
# could finally surface the import error.
if sys.platform == "win32":
    import msvcrt

    def _flock_exclusive(fd: int) -> None:
        # msvcrt.locking is BYTE-RANGE based: lock + unlock target the
        # current file position to position+nbytes. The lock acquired here
        # must be released at the same byte range, but with O_APPEND the
        # file position advances after each write — so by the time
        # _flock_release runs, the position is at NEW_EOF and the unlock
        # tries to release a different byte range than was locked. Result:
        # PermissionError [Errno 13] from msvcrt.locking on unlock.
        #
        # Fix: explicitly lseek to byte 0 before both lock and unlock so
        # they target the same byte range [0, 1). With O_APPEND set on the
        # fd, actual writes still go to EOF regardless of file position
        # (kernel-level behavior on POSIX, equivalent C-runtime behavior
        # on Windows). The byte-0 lock is purely advisory — it doesn't
        # block reads, and no real data ever gets written at byte 0.
        #
        # v0.1.25's release-smoke matrix Windows-2022 cell hit this bug
        # ("PermissionError: [Errno 13]" at receipts.py:116). v0.1.26
        # closes it.
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_LOCK, 1)

    def _flock_release(fd: int) -> None:
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
else:
    import fcntl

    def _flock_exclusive(fd: int) -> None:
        fcntl.flock(fd, fcntl.LOCK_EX)

    def _flock_release(fd: int) -> None:
        fcntl.flock(fd, fcntl.LOCK_UN)


class ReceiptLog:
    """Append-only JSONL record of every write to the provenance store."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Create the file if missing so flock has something to acquire.
        self.path.touch(exist_ok=True)

    def append(self, record: ProvenanceRecord) -> None:
        # v0.1.9: token usage telemetry. Agents that invoked an LLM stash
        # `input_tokens` and `output_tokens` on the record's metadata dict
        # (pulled from the SDK response's usage block). Surfacing on the
        # receipt line lets operators sum a run's spend without parsing
        # blob payloads — e.g.:
        #   jq -r 'select(.input_tokens) | [.input_tokens, .output_tokens] | @tsv' \
        #     .efterlev/receipts.log | awk '{i+=$1; o+=$2} END {print "in:", i, "out:", o}'
        # Records without an LLM call (deterministic primitive
        # invocations, manifest evidence, etc.) omit both fields entirely.
        record_dict: dict[str, Any] = {
            "ts": record.timestamp.isoformat(),
            "record_id": record.record_id,
            "record_type": record.record_type,
            "derived_from": list(record.derived_from),
            "primitive": record.primitive,
            "agent": record.agent,
            "model": record.model,
            "prompt_hash": record.prompt_hash,
        }
        meta = record.metadata or {}
        if "input_tokens" in meta:
            record_dict["input_tokens"] = meta["input_tokens"]
        if "output_tokens" in meta:
            record_dict["output_tokens"] = meta["output_tokens"]
        line = json.dumps(record_dict, separators=(",", ":"))
        data = (line + "\n").encode("utf-8")

        fd = os.open(self.path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            _flock_exclusive(fd)
            try:
                os.write(fd, data)
                os.fsync(fd)
            finally:
                _flock_release(fd)
        finally:
            os.close(fd)

    def read_all(self) -> list[dict[str, Any]]:
        """Parse every line; raise ProvenanceError on a malformed line."""
        if not self.path.exists():
            return []
        entries: list[dict[str, Any]] = []
        for lineno, raw in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                entries.append(json.loads(raw))
            except json.JSONDecodeError as e:
                raise ProvenanceError(f"receipts.log line {lineno} is not valid JSON: {e}") from e
        return entries
