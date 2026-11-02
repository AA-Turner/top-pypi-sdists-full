"""ProducerRegistry: each producer's sequence high-water, delivered tally, capture gaps and clean seal."""

from __future__ import annotations

import json
import os
from pathlib import Path

from probe.foundation.durable.durable import SYNC_FULL, file_lock, now_iso, write_text_atomic

#: How many capture-gap records a producer file keeps; `gap_count` keeps the total. The list
#: grew by one per dropped write and the file is rewritten on every drop: 6,000 drops made a
#: refused `log()` 16 ms -> 107 ms.
_GAPS_KEPT = 32


class ProducersMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    # -- producer registry (parity F4) --------------------------------------
    def _producer_file(self, producer_id: str) -> Path:
        return self.producers_dir / f"{_safe_component(producer_id)}.json"

    def _ensure_producers_dir(self) -> None:
        self.producers_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            os.chmod(self.producers_dir, 0o700)
        except OSError:
            pass

    def _read_producer_locked(self, producer_id: str) -> dict:
        try:
            return json.loads(self._producer_file(producer_id).read_text())
        except (OSError, json.JSONDecodeError, ValueError):
            return {}

    def _update_producer_locked(
        self,
        producer_id: str,
        record: dict,
        *,
        role: str | None = None,
        last_sequence: int | None = None,
        delivered: int | None = None,
        gap: dict | None = None,
        state: str | None = None,
        sync: str = SYNC_FULL,
    ) -> None:
        record.setdefault("schema", SCHEMA)
        record.setdefault("producer_id", producer_id)
        record.setdefault("role", role)
        record.setdefault("registered_at", now_iso())
        record.setdefault("last_sequence", 0)
        record.setdefault("delivered", 0)
        record.setdefault("gaps", [])
        record.setdefault("gap_count", len(record["gaps"]))
        record.setdefault("closed_at", None)
        if last_sequence is not None:
            record["last_sequence"] = max(int(record["last_sequence"]), last_sequence)
        if delivered is not None:
            # Additive, and re-read from disk under the lock by every caller: the drainer and a
            # live writer touch the same record from different processes, so an in-memory counter
            # would clobber.
            record["delivered"] = int(record.get("delivered") or 0) + int(delivered)
        if gap is not None:
            # A count plus the most recent few: the full list grew by one per dropped write and
            # is rewritten with every drop.
            record["gap_count"] = int(record.get("gap_count") or 0) + 1
            record["gaps"] = [*record["gaps"], gap][-_GAPS_KEPT:]
        if state is not None:
            record["state"] = state
            record["closed_at"] = now_iso() if state == "closed" else None
        else:
            record.setdefault("state", "open")
        write_text_atomic(
            self._producer_file(producer_id),
            json.dumps(record, indent=2) + "\n",
            mode=0o600,
            sync=sync,
        )

    def register_producer(self, producer_id: str, *, role: str = "sdk") -> None:
        """Join this journal's producer registry. Sequences make silent capture loss VISIBLE:
        every later append stamps ``producer_id`` + a per-producer sequence and the registry
        records the high-water mark. A registry saying N with no op (queued, dead-lettered or
        delivered) ever stamped N is a write lost between caller and journal; ``note_capture_gap``
        records those the caller catches itself. Re-registering an existing id resumes its
        sequence (restarts, and ids shared across short-lived processes, continue the same line).
        """
        self._ensure()
        self._ensure_producers_dir()
        self._producer_id = producer_id
        self._producer_role = role
        with file_lock(self.append_lock):
            record = self._read_producer_locked(producer_id)
            self._update_producer_locked(
                producer_id, record, role=role, state="open"
            )

    def note_capture_gap(self, reason: str) -> None:
        """Burn a sequence for a write that never reached the journal, so the loss is a visible
        hole, not silence (Miles' capture_gaps)."""
        if self._producer_id is None:
            return
        with file_lock(self.append_lock):
            record = self._read_producer_locked(self._producer_id)
            sequence = int(record.get("last_sequence") or 0) + 1
            self._update_producer_locked(
                self._producer_id,
                record,
                role=self._producer_role,
                last_sequence=sequence,
                # scanning disabled: gap={"sequence": sequence, "reason": scrub_text(reason), "at": now_iso()},
                gap={"sequence": sequence, "reason": reason, "at": now_iso()},
            )

    def note_delivered(self, producer_id: str, count: int = 1) -> None:
        """Add ``count`` landed ops to one producer's tally, per delivered op (a pass may die mid-way). A
        floor: written after the op file is gone, so a crash under-counts by at most one."""
        if not producer_id or count <= 0:
            return
        self._ensure_producers_dir()
        with file_lock(self.append_lock):
            record = self._read_producer_locked(producer_id)
            self._update_producer_locked(producer_id, record, delivered=count)

    def seal_producer(self) -> None:
        """Mark this producer cleanly closed. A producer left "open" whose process is gone is a
        crashed writer: the report shows exactly that."""
        if self._producer_id is None or not self.producers_dir.exists():
            return
        with file_lock(self.append_lock):
            record = self._read_producer_locked(self._producer_id)
            self._update_producer_locked(
                self._producer_id, record, role=self._producer_role, state="closed"
            )

    def producer_report(self) -> list[dict]:
        """Every producer this journal knows: sequence high-water, ``delivered`` tally, capture
        gaps, open/closed state. Unparseable records are skipped, not raised: diagnostics, never a
        blocker."""
        if not self.producers_dir.exists():
            return []
        out: list[dict] = []
        for path in sorted(self.producers_dir.iterdir()):
            if not path.name.endswith(".json"):
                continue
            try:
                out.append(json.loads(path.read_text()))
            except (OSError, json.JSONDecodeError, ValueError):
                continue
        return out
from probe.sdk.delivery.ops.ops import SCHEMA  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _safe_component  # noqa: E402 -- pieces need each other; the front door loads this one first
