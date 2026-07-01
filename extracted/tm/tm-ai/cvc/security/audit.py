"""
cvc.security.audit — append-only, hash-chained audit log.

Every read/write of the soul is recorded here. The chain makes tampering
detectable: flip one byte and every subsequent hash check fails.

Storage: append-only JSONL at <vault>/audit.log with the rolling hash in
each line's `chain_hash` field. Verification replays the chain forward.

What this proves to the owner:
  "Nobody — not malware, not a thief, not me on a bad day — has touched
   my soul without leaving a trace I can verify."
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.security.audit")


class AuditAction(str, Enum):
    """The verbs the soul can do. Every soul I/O maps to one of these."""

    VAULT_INITIALIZE = "vault.initialize"
    VAULT_UNLOCK = "vault.unlock"
    VAULT_LOCK = "vault.lock"
    VAULT_BLOB_WRITE = "vault.blob.write"
    VAULT_BLOB_READ = "vault.blob.read"
    SOUL_READ = "soul.read"
    SOUL_WRITE = "soul.write"
    SOUL_RESTORE = "soul.restore"
    SOUL_MERGE = "soul.merge"
    SOUL_DREAM = "soul.dream"
    WILL_CREATE = "will.create"
    WILL_UPDATE = "will.update"
    WILL_RELEASE = "will.release"
    WILL_EXECUTOR_ADD = "will.executor.add"
    WILL_EXECUTOR_REMOVE = "will.executor.remove"
    NETWORK_BRAIN_CALL = "network.brain.call"
    NETWORK_BLOCKED = "network.blocked"
    SHELL_EXEC = "shell.exec"


@dataclass
class AuditEntry:
    """One line in the audit log."""

    timestamp: float
    action: str
    actor: str = "owner"          # who initiated — usually "owner", can be "agent"
    target: str = ""              # what was touched (file, commit, blob name)
    detail: dict[str, Any] = field(default_factory=dict)
    prev_hash: str = ""           # hash of previous entry (empty for genesis)
    chain_hash: str = ""          # sha256 of (this entry without chain_hash + prev_hash)


class AuditLog:
    """Append-only, hash-chained audit log."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    # ── append ─────────────────────────────────────────────────────────

    def append(
        self,
        action: AuditAction | str,
        *,
        actor: str = "owner",
        target: str = "",
        detail: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Append a new entry. Computes the chain hash automatically."""
        a = action.value if isinstance(action, AuditAction) else str(action)
        prev_hash = self._last_chain_hash()
        entry = AuditEntry(
            timestamp=time.time(),
            action=a,
            actor=actor,
            target=target,
            detail=detail or {},
            prev_hash=prev_hash,
        )
        entry.chain_hash = self._hash_entry(entry)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry)) + "\n")
        return entry

    # ── verification ──────────────────────────────────────────────────

    def verify(self) -> tuple[bool, str]:
        """
        Replay the chain. Returns (ok, message).

        If ok is False, message explains where the chain broke.
        """
        if not self.log_path.exists():
            return True, "no audit log yet"

        prev_hash = ""
        count = 0
        with self.log_path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                count += 1
                try:
                    data = json.loads(line)
                except json.JSONDecodeError as exc:
                    return False, f"line {line_no}: invalid JSON — {exc}"
                entry = AuditEntry(**{k: v for k, v in data.items() if k in AuditEntry.__dataclass_fields__})
                if entry.prev_hash != prev_hash:
                    return False, f"line {line_no}: prev_hash mismatch"
                recomputed = self._hash_entry(entry)
                if recomputed != entry.chain_hash:
                    return False, f"line {line_no}: hash mismatch (tampering detected)"
                prev_hash = entry.chain_hash

        return True, f"chain verified across {count} entries"

    def tail(self, n: int = 50) -> list[dict[str, Any]]:
        """Return the most recent N entries (newest last)."""
        if not self.log_path.exists():
            return []
        with self.log_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        out = []
        for line in lines[-n:]:
            line = line.strip()
            if line:
                out.append(json.loads(line))
        return out

    def count(self) -> int:
        if not self.log_path.exists():
            return 0
        with self.log_path.open("r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())

    # ── internals ──────────────────────────────────────────────────────

    def _last_chain_hash(self) -> str:
        if not self.log_path.exists():
            return ""
        try:
            with self.log_path.open("rb") as f:
                f.seek(0, 2)
                size = f.tell()
                if size == 0:
                    return ""
                # read last non-empty line
                f.seek(max(0, size - 4096))
                chunk = f.read().decode("utf-8", errors="ignore")
            for line in reversed(chunk.splitlines()):
                line = line.strip()
                if line:
                    return json.loads(line).get("chain_hash", "")
        except Exception as exc:  # noqa: BLE001
            logger.warning("could not read last chain hash: %s", exc)
        return ""

    @staticmethod
    def _hash_entry(entry: AuditEntry) -> str:
        # Hash excludes chain_hash itself (that would be circular)
        body = json.dumps(
            {
                "timestamp": entry.timestamp,
                "action": entry.action,
                "actor": entry.actor,
                "target": entry.target,
                "detail": entry.detail,
                "prev_hash": entry.prev_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(body.encode("utf-8")).hexdigest()