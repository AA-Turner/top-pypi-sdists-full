"""Local, append-only, content-addressed provenance store.

Two on-disk components under `.efterlev/`:

  store.db       SQLite — one row per `ProvenanceRecord`
  store/xx/yy/…  content-addressed blob store — raw payloads (Evidence / Claim
                 content dicts serialized as JSON) at paths derived from their
                 own SHA-256

The blob store is write-idempotent: same payload → same path → second write
is a no-op. Records referencing identical payloads share a blob; the records
themselves differ because a `ProvenanceRecord` carries its own timestamp and
origin metadata, so two writes of the same payload at different times produce
two distinct records pointing at the same blob. This is the right semantic for
"new evidence for the same thing at a later date" without overwriting history.
"""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import threading
from pathlib import Path
from typing import Any

from efterlev.errors import ProvenanceError
from efterlev.models import ProvenanceRecord, RecordType
from efterlev.provenance.receipts import ReceiptLog

log = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS provenance_records (
    record_id    TEXT PRIMARY KEY,
    record_type  TEXT NOT NULL,
    content_ref  TEXT NOT NULL,
    derived_from TEXT NOT NULL,
    primitive    TEXT,
    agent        TEXT,
    model        TEXT,
    prompt_hash  TEXT,
    timestamp    TEXT NOT NULL,
    metadata     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_record_type ON provenance_records(record_type);
CREATE INDEX IF NOT EXISTS idx_timestamp   ON provenance_records(timestamp);
"""


def _canonical_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _payload_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _shard_path(payload_hash: str) -> Path:
    # e.g. "abcd1234..." -> Path("ab/cd/abcd1234...")
    return Path(payload_hash[:2]) / payload_hash[2:4] / payload_hash


class ProvenanceStore:
    """SQLite-backed record index plus content-addressed blob store.

    All paths under `root / ".efterlev"`; the constructor creates the directory
    tree and schema on first use, so it is safe to point at either an existing
    store or a fresh directory.
    """

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.efterlev_dir = self.root / ".efterlev"
        self.db_path = self.efterlev_dir / "store.db"
        self.blob_dir = self.efterlev_dir / "store"
        self.receipts = ReceiptLog(self.efterlev_dir / "receipts.log")

        self.efterlev_dir.mkdir(parents=True, exist_ok=True)
        self.blob_dir.mkdir(parents=True, exist_ok=True)
        # `check_same_thread=False` lets the same ProvenanceStore instance be
        # used from multiple threads (e.g., a parallel scan). SQLite's file-
        # level locking handles concurrency at the DB layer; `_write_lock`
        # serializes our Python-side use of the connection object itself.
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()
        self._write_lock = threading.Lock()
        # v0.1.155 / #360: write-time evidence dedupe — paired with v0.1.153's
        # read-time `iter_evidence` dedupe. The store accumulated rows + blobs
        # on every re-scan because `record_id` includes the scan-time timestamp.
        # This in-memory `evidence_id → record_id` cache lets `write_record`
        # skip writes when the same detector evidence is already in the store.
        # Lazy-loaded on first evidence write; maintained incrementally.
        self._evidence_id_to_record_id: dict[str, str] | None = None

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> ProvenanceStore:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # --- writes ---------------------------------------------------------------

    def write_record(
        self,
        *,
        payload: dict[str, Any],
        record_type: RecordType,
        derived_from: list[str] | None = None,
        primitive: str | None = None,
        agent: str | None = None,
        model: str | None = None,
        prompt_hash: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ProvenanceRecord:
        """Persist `payload` to the blob store and insert a ProvenanceRecord row.

        Atomically appends a receipt log line. Returns the finalized record (with
        its content-addressed `record_id` computed).

        Defense-in-depth (2026-04-23, DECISIONS "Store-level validate_claim_provenance"):
        for `record_type="claim"` records with non-empty `derived_from`, each
        cited id is verified to resolve to an existing record in the store
        BEFORE insertion. A cited id that doesn't resolve raises
        `ProvenanceError` and the record is NOT written. Per-agent fence
        validators remain the primary enforcement against the model-
        hallucinated-an-id failure mode; this check is the secondary
        enforcement against buggy-agent-code or direct-store-write paths
        where the agent-level check doesn't run.
        """
        # Dry-run short-circuit (v0.1.20): when an agent CLI command is
        # invoked with `--dry-run`, the active dry-run session is set
        # in the context var; in that mode we want zero side effects on
        # the workspace's `.efterlev/` (no SQLite row, no blob, no
        # receipts.log line). Return a structurally-valid stub
        # ProvenanceRecord so callers (which use `record.record_id` for
        # downstream Claim attribution) don't crash. Defense-in-depth
        # claim-provenance validation is also skipped — there's no
        # real chain to validate against. See DECISIONS 2026-05-06
        # "Tier 1 #2b design".
        from efterlev.agents.dry_run import get_active_dry_run_session

        if get_active_dry_run_session() is not None:
            return ProvenanceRecord.create(
                record_type=record_type,
                content_ref="sha256:" + "0" * 64,  # sentinel; never written to disk
                derived_from=derived_from,
                primitive=primitive,
                agent=agent,
                model=model,
                prompt_hash=prompt_hash,
                metadata=metadata,
            )

        if record_type == "claim" and derived_from:
            self._validate_claim_derived_from(derived_from)

        # v0.1.155 / #360: write-time dedupe for detector-emitted Evidence.
        # Two record families land at record_type="evidence":
        # 1. Detector-emitted Evidence (Evidence.model_dump payload — has
        #    `evidence_id` at the top level). v0.1.152 made evidence_id
        #    stable across re-scans by excluding `timestamp` from the
        #    hash basis, so this is the right dedupe key.
        # 2. Primitive-wrapper records ({"input":..., "output":...} from
        #    the @primitive decorator). These embed Evidence with fresh
        #    `timestamp` fields inside `output.evidence[]`, so content_ref
        #    is genuinely different per scan even with unchanged source.
        #    They're kept (audit history of which primitives ran when),
        #    but they're small per scan (~4-5 wrappers) vs the per-detector
        #    Evidence emissions (~90 records on the customer's workspace).
        # Net: this dedupe stops ~95% of per-scan SQLite growth on a
        # workspace whose source files haven't changed.
        if record_type == "evidence" and isinstance(payload, dict):
            ev_id = payload.get("evidence_id")
            if isinstance(ev_id, str) and ev_id:
                existing_rid = self._lookup_record_id_by_evidence_id(ev_id)
                if existing_rid is not None:
                    existing = self.get_record(existing_rid)
                    if existing is not None:
                        return existing

        content_ref = self._put_blob(payload)
        record = ProvenanceRecord.create(
            record_type=record_type,
            content_ref=content_ref,
            derived_from=derived_from,
            primitive=primitive,
            agent=agent,
            model=model,
            prompt_hash=prompt_hash,
            metadata=metadata,
        )

        with self._write_lock:
            try:
                self._conn.execute(
                    "INSERT OR IGNORE INTO provenance_records "
                    "(record_id, record_type, content_ref, derived_from, "
                    " primitive, agent, model, prompt_hash, timestamp, metadata) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        record.record_id,
                        record.record_type,
                        record.content_ref,
                        json.dumps(record.derived_from),
                        record.primitive,
                        record.agent,
                        record.model,
                        record.prompt_hash,
                        record.timestamp.isoformat(),
                        json.dumps(record.metadata),
                    ),
                )
                self._conn.commit()
            except sqlite3.Error as e:
                raise ProvenanceError(f"failed to insert record {record.record_id}: {e}") from e

        self.receipts.append(record)
        # v0.1.155 / #360: maintain the evidence_id → record_id cache so
        # subsequent writes in the same process hit the dedupe path.
        if (
            record_type == "evidence"
            and isinstance(payload, dict)
            and self._evidence_id_to_record_id is not None
        ):
            new_ev_id = payload.get("evidence_id")
            if isinstance(new_ev_id, str) and new_ev_id:
                self._evidence_id_to_record_id.setdefault(new_ev_id, record.record_id)
        return record

    def _lookup_record_id_by_evidence_id(self, evidence_id: str) -> str | None:
        """Return the record_id of an existing evidence record whose payload's
        `evidence_id` matches, or None. Used by `write_record` (v0.1.155 /
        #360) to skip duplicate detector emissions.

        Lazy-loads `self._evidence_id_to_record_id` on first call by scanning
        existing evidence blobs once. Subsequent lookups are O(1). The cache
        is maintained incrementally on each successful evidence write.
        """
        if self._evidence_id_to_record_id is None:
            self._evidence_id_to_record_id = {}
            rows = self._conn.execute(
                "SELECT record_id, content_ref FROM provenance_records "
                "WHERE record_type = 'evidence' ORDER BY timestamp ASC"
            ).fetchall()
            for record_id, content_ref in rows:
                blob_path = self.blob_dir / content_ref
                if not blob_path.exists():
                    continue
                try:
                    payload = json.loads(blob_path.read_bytes())
                except (OSError, json.JSONDecodeError):
                    continue
                if not isinstance(payload, dict):
                    continue
                ev_id = payload.get("evidence_id")
                if isinstance(ev_id, str) and ev_id:
                    # First occurrence wins (matches iter_evidence's oldest-
                    # wins semantics) — pre-v0.1.155 stores already contain
                    # duplicate evidence_ids; collapse onto the oldest row.
                    self._evidence_id_to_record_id.setdefault(ev_id, record_id)
        return self._evidence_id_to_record_id.get(evidence_id)

    def _put_blob(self, payload: dict[str, Any]) -> str:
        """Write payload to blob store (idempotent); return relative content_ref."""
        data = _canonical_bytes(payload)
        digest = hashlib.sha256(data).hexdigest()
        rel = _shard_path(digest)
        full = self.blob_dir / rel.with_suffix(".json")
        if not full.exists():
            full.parent.mkdir(parents=True, exist_ok=True)
            # Write with a tmp+rename so partial writes never leave a half-file
            # that a later read would treat as valid.
            tmp = full.with_suffix(".json.tmp")
            tmp.write_bytes(data)
            tmp.rename(full)
        return str(rel.with_suffix(".json"))

    def _validate_claim_derived_from(self, derived_from: list[str]) -> None:
        """Verify every cited id resolves to something in the store. Raises on miss.

        Called from `write_record` for Claim records with non-empty
        `derived_from`. An id "resolves" if it matches EITHER:

        1. a `ProvenanceRecord.record_id` directly, OR
        2. an `Evidence.evidence_id` stored inside an evidence-typed
           record's payload.

        The dual-keyed check exists because `Evidence.evidence_id` is a
        hash of Evidence content while `ProvenanceRecord.record_id` is a
        hash of the envelope (content_ref + metadata + timestamp). When
        the scan path stores Evidence, the two ids diverge — but the
        agents that cite evidence work in the `Evidence.evidence_id`
        namespace (that's the fence id the model sees). The validation
        must accept both so legitimate chains don't false-fail.

        A missing id is a serious integrity failure: it means the agent
        or a direct store-write path produced a claim citing an id that
        doesn't resolve, which the per-agent fence validators should
        have caught first. Raising `ProvenanceError` here prevents the
        bad record from ever being persisted.
        """
        if not derived_from:
            return  # Defensive — caller should have checked; still cheap here.

        # Step 1: try record_id match — cheap index lookup.
        placeholders = ",".join("?" * len(derived_from))
        # Placeholders are a constructed-count string of `?` — no
        # user-controlled SQL fragments. IDs pass through parameterized
        # binding. Safe despite the f-string.
        query_by_record = (
            f"SELECT record_id FROM provenance_records WHERE record_id IN ({placeholders})"
        )
        rows = self._conn.execute(query_by_record, derived_from).fetchall()
        found: set[str] = {row[0] for row in rows}

        still_missing = [rid for rid in derived_from if rid not in found]
        if not still_missing:
            return

        # Step 2: for the remaining ids, scan evidence payloads for a
        # matching Evidence.evidence_id. Evidence records are kept small
        # and bounded by detector count * resources, so a full scan is
        # acceptable for this defense-in-depth check. O(evidence * cites)
        # in the worst case; in practice bounded by ~100 * 5.
        evidence_rows = self._conn.execute(
            "SELECT content_ref FROM provenance_records WHERE record_type = 'evidence'"
        ).fetchall()
        still_missing_set = set(still_missing)
        for (content_ref,) in evidence_rows:
            if not still_missing_set:
                break
            blob_path = self.blob_dir / content_ref
            if not blob_path.exists():
                continue
            try:
                payload = json.loads(blob_path.read_bytes())
            except (OSError, json.JSONDecodeError):
                continue
            ev_id = payload.get("evidence_id") if isinstance(payload, dict) else None
            if isinstance(ev_id, str) and ev_id in still_missing_set:
                still_missing_set.discard(ev_id)

        if still_missing_set:
            first_miss = sorted(still_missing_set)[0]
            raise ProvenanceError(
                f"claim cites {len(still_missing_set)} evidence id(s) that do not "
                f"resolve in the provenance store; first miss: {first_miss!r}. "
                f"Checked both `ProvenanceRecord.record_id` and "
                f"`Evidence.evidence_id` in stored evidence payloads. "
                f"This typically means either the agent's fence validator is "
                f"broken or a direct store-write bypassed the agent pipeline. "
                f"No claim record was persisted."
            )

    # --- reads ----------------------------------------------------------------

    def get_record(self, record_id: str) -> ProvenanceRecord | None:
        row = self._conn.execute(
            "SELECT record_type, content_ref, derived_from, primitive, agent, "
            "model, prompt_hash, timestamp, metadata "
            "FROM provenance_records WHERE record_id = ?",
            (record_id,),
        ).fetchone()
        if row is None:
            return None
        (
            record_type,
            content_ref,
            derived_from,
            primitive,
            agent,
            model,
            prompt_hash,
            timestamp,
            metadata,
        ) = row
        return ProvenanceRecord(
            record_id=record_id,
            record_type=record_type,
            content_ref=content_ref,
            derived_from=json.loads(derived_from),
            primitive=primitive,
            agent=agent,
            model=model,
            prompt_hash=prompt_hash,
            timestamp=timestamp,  # pydantic coerces ISO str to datetime
            metadata=json.loads(metadata),
        )

    def read_payload(self, record: ProvenanceRecord) -> dict[str, Any]:
        full = self.blob_dir / record.content_ref
        if not full.exists():
            raise ProvenanceError(
                f"blob missing for record {record.record_id}: {record.content_ref}"
            )
        try:
            data: dict[str, Any] = json.loads(full.read_bytes())
        except json.JSONDecodeError as e:
            raise ProvenanceError(f"blob at {record.content_ref} is not valid JSON: {e}") from e
        return data

    def latest_record_with_primitive_prefix(
        self, prefix: str
    ) -> tuple[ProvenanceRecord, dict[str, Any]] | None:
        """Return the most recent (record, payload) where `primitive LIKE prefix%`.

        Used by `efterlev.primitives.scan.latest_scan_summary` to find the most
        recent scan-primitive invocation (`scan_terraform@*` or
        `scan_terraform_plan@*`) without hardcoding versions. Returns None when
        no record matches — typical when the user runs an agent command before
        running `efterlev scan`. The payload is the raw `{"input", "output"}`
        dict the @primitive decorator persisted; callers extract the fields
        they need rather than this method coupling to any specific
        primitive's output schema.
        """
        like_pattern = f"{prefix}%"
        row = self._conn.execute(
            "SELECT record_id FROM provenance_records "
            "WHERE primitive LIKE ? ORDER BY timestamp DESC, record_id DESC LIMIT 1",
            (like_pattern,),
        ).fetchone()
        if row is None:
            return None
        record = self.get_record(row[0])
        if record is None:
            return None
        try:
            payload = self.read_payload(record)
        except ProvenanceError:
            return None
        return record, payload

    def iter_records(self) -> list[str]:
        """Return every record_id in insertion order (by timestamp)."""
        rows = self._conn.execute(
            "SELECT record_id FROM provenance_records ORDER BY timestamp, record_id"
        ).fetchall()
        return [r[0] for r in rows]

    def resolve_record_id_prefix(self, ref: str) -> str | None:
        """Resolve a record_id OR evidence_id reference (full or prefix) to a record_id.

        Rationales, attestations, and POA&Ms print 8-char prefixes for
        readability (`_short_id`), so users naturally paste the prefix into
        `efterlev provenance show <id>`. Earlier `get_record` only matched
        the full 64-hex form, leaving the prefix path a dead end.

        Dual-keyed semantics — mirrors `resolve_to_record` but with prefix
        support. The cited prefix may be EITHER a `ProvenanceRecord.record_id`
        prefix (envelope hash) OR an `Evidence.evidence_id` prefix (Evidence
        content hash inside an evidence payload). The two are structurally
        distinct: agents cite Evidence by its `evidence_id` (the fence id
        the model sees), but the SQLite index is on `record_id`. Without
        Step 2 the most common user-pasted prefix — straight from the POA&M
        — would never resolve. v0.1.5 shipped only Step 1; the v0.1.5
        terraform-aws-vpc shakedown surfaced the gap.

        `ref` accepts: full `sha256:<64hex>`, `sha256:<prefix>`, or bare hex
        prefix without the `sha256:` scheme. Returns the unique full
        `ProvenanceRecord.record_id`, or None when nothing matches. Raises
        `ProvenanceError` on prefix collision (≥2 matches across both
        steps) — surfacing the collision is more useful than silently
        picking one.

        The minimum prefix length is 4 hex chars. Below that, even the
        ~100-record default workspace can collide too easily for the
        error to be actionable.
        """
        normalized = ref if ref.startswith("sha256:") else f"sha256:{ref}"
        bare = normalized[len("sha256:") :]
        if len(bare) < 4 or not all(c in "0123456789abcdef" for c in bare.lower()):
            return None

        # Step 1: record_id prefix match — cheap indexed lookup.
        if len(bare) == 64:
            row = self._conn.execute(
                "SELECT record_id FROM provenance_records WHERE record_id = ?",
                (normalized,),
            ).fetchone()
            step1 = [row[0]] if row else []
        else:
            step1 = [
                r[0]
                for r in self._conn.execute(
                    "SELECT record_id FROM provenance_records WHERE record_id LIKE ?",
                    (f"{normalized}%",),
                ).fetchall()
            ]

        # Step 2: evidence_id prefix match — scan evidence payloads. Bounded
        # by detector_count * scanned_resources; sequential read is fine.
        # Same v0.2 perf followups as `resolve_to_record` (maintain an
        # evidence_id → record_id index, cache within a walk).
        evidence_rows = self._conn.execute(
            "SELECT record_id, content_ref FROM provenance_records WHERE record_type = 'evidence'"
        ).fetchall()
        step2: list[str] = []
        for record_id, content_ref in evidence_rows:
            blob_path = self.blob_dir / content_ref
            if not blob_path.exists():
                continue
            try:
                payload = json.loads(blob_path.read_bytes())
            except (OSError, json.JSONDecodeError):
                continue
            ev_id = payload.get("evidence_id") if isinstance(payload, dict) else None
            if isinstance(ev_id, str) and ev_id.startswith(normalized):
                step2.append(record_id)

        # Combine + dedupe. Same record can match both steps (e.g. a record
        # whose record_id and evidence_id share a prefix); count it once.
        candidates = list({*step1, *step2})
        if not candidates:
            return None
        if len(candidates) > 1:
            raise ProvenanceError(
                f"prefix {ref!r} matches multiple records — disambiguate with "
                f"a longer prefix. Use `efterlev provenance verify` to list "
                f"all record_ids."
            )
        return candidates[0]

    def resolve_to_record(self, citation_id: str) -> ProvenanceRecord | None:
        """Look up `citation_id` as either a record_id OR an evidence payload's evidence_id.

        Why dual-key: `Evidence.evidence_id` (Evidence-content hash) is
        structurally distinct from `ProvenanceRecord.record_id` (envelope hash
        including timestamps + metadata). Agents cite evidence by
        `Evidence.evidence_id` because that's the fence id the model sees in
        the prompt, but the store indexes by `record_id`. A cited id may
        therefore resolve via either path.

        Mirrors the dual-key lookup `_validate_claim_derived_from` does at the
        write boundary (the round-2 3PAO review of 2026-04-25 found that the
        validator accepted citations the walker subsequently couldn't resolve
        — a real traceability bug; this helper is the fix).

        Returns the resolved `ProvenanceRecord` on hit, `None` on miss. The
        walker uses this; the batch validator uses its own optimized path
        because it scores many ids at once and benefits from set-arithmetic.
        """
        # Step 1: direct record_id hit (cheap indexed lookup).
        record = self.get_record(citation_id)
        if record is not None:
            return record

        # Step 2: scan evidence payloads for an Evidence.evidence_id match.
        # Evidence record count is bounded by detector count * scanned
        # resources; a sequential scan is acceptable. Two improvements
        # tracked as v0.2 work in DECISIONS: (a) maintain an evidence_id →
        # record_id index alongside writes for O(1) lookup, (b) cache
        # within a single walk_chain invocation so a tree with many leaves
        # doesn't re-scan per leaf.
        evidence_rows = self._conn.execute(
            "SELECT record_id, content_ref FROM provenance_records WHERE record_type = 'evidence'"
        ).fetchall()
        for record_id, content_ref in evidence_rows:
            blob_path = self.blob_dir / content_ref
            if not blob_path.exists():
                continue
            try:
                payload = json.loads(blob_path.read_bytes())
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(payload, dict) and payload.get("evidence_id") == citation_id:
                return self.get_record(record_id)
        return None

    def iter_record_refs(self) -> list[tuple[str, str]]:
        """Return `(record_id, content_ref)` for every record, all types.

        Used by `efterlev provenance verify` to walk the full content-
        addressed chain and re-verify each blob's SHA-256 against the
        path it's stored at. Returning `content_ref` saves the verifier
        from re-querying per record.
        """
        rows = self._conn.execute(
            "SELECT record_id, content_ref FROM provenance_records ORDER BY timestamp, record_id"
        ).fetchall()
        return [(r[0], r[1]) for r in rows]

    def iter_evidence(self) -> list[tuple[str, dict[str, Any]]]:
        """Return `(record_id, evidence_payload)` for every detector-emitted record.

        Filters on `record_type="evidence"` + payload that parses as an
        Evidence model dump (checked structurally via required keys). Primitive
        invocation records share record_type="evidence" when the primitive is
        deterministic but have payload shape `{"input": ..., "output": ...}`,
        so the structural filter cleanly separates them.

        Silently drops records whose blob is missing, unreadable, or has an
        unexpected shape — `log.warning` flags each drop so an operator
        investigating a missing evidence record has a breadcrumb. A corrupt
        store is a real failure mode (blob store + SQLite could drift under
        disk-full or killed-mid-write conditions); surfacing the drop count
        in logs is better than silently swallowing.

        Returns a list because iteration order matters for deterministic
        display and test assertions; the list size is bounded by the number
        of detector hits, which at v0 is small.
        """
        rows = self._conn.execute(
            "SELECT record_id, content_ref FROM provenance_records "
            "WHERE record_type = 'evidence' ORDER BY timestamp, record_id"
        ).fetchall()
        results: list[tuple[str, dict[str, Any]]] = []
        # v0.1.153 / #358: dedupe by `evidence_id`. Re-scanning the same source
        # writes new SQLite rows (record_id includes timestamp) pointing at new
        # blob files (blob filename hashes the payload which also includes
        # timestamp), even though the Evidence content (and `evidence_id`) is
        # stable since v0.1.152. Without dedupe here, `iter_evidence` returns
        # N records after 1 scan, 2N after 2 scans, and the gap-agent prompt
        # grows linearly with scan count — the v0.1.151 prompt cache never
        # hits. "Keep first occurrence" (ORDER BY timestamp ASC above) means
        # the oldest record wins, which is fine — only the content matters.
        seen_evidence_ids: set[str] = set()
        for record_id, content_ref in rows:
            full = self.blob_dir / content_ref
            if not full.exists():
                log.warning(
                    "iter_evidence: blob missing for record %s (ref %s); skipping",
                    record_id,
                    content_ref,
                )
                continue
            try:
                payload = json.loads(full.read_bytes())
            except json.JSONDecodeError as e:
                log.warning(
                    "iter_evidence: blob at %s is not valid JSON (%s); skipping record %s",
                    content_ref,
                    e,
                    record_id,
                )
                continue
            if not isinstance(payload, dict):
                log.warning(
                    "iter_evidence: blob at %s is not a JSON object; skipping record %s",
                    content_ref,
                    record_id,
                )
                continue
            # Detector-emitted Evidence has these required fields; primitive
            # invocation records have {"input","output"} instead — those are
            # an expected structural mismatch, not a corruption, so no log.
            if {"detector_id", "source_ref", "timestamp"} <= payload.keys():
                ev_id = payload.get("evidence_id")
                if isinstance(ev_id, str) and ev_id:
                    if ev_id in seen_evidence_ids:
                        continue
                    seen_evidence_ids.add(ev_id)
                results.append((record_id, payload))
        return results

    def iter_claims_by_metadata_kind(
        self, kind: str
    ) -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
        """Return `(record_id, metadata, payload)` for every claim tagged `kind`.

        The Gap Agent tags each KSI classification Claim with
        `metadata={"kind": "ksi_classification", ...}`. Downstream agents
        (Documentation, Remediation) find the classifications by filtering on
        the kind tag rather than re-classifying from raw evidence.

        The filter is `record_type="claim"` + `metadata.kind=<kind>`; payloads
        are returned alongside so callers can reconstruct the Claim content
        without a second blob read.
        """
        rows = self._conn.execute(
            "SELECT record_id, metadata, content_ref FROM provenance_records "
            "WHERE record_type = 'claim' ORDER BY timestamp, record_id"
        ).fetchall()
        results: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
        for record_id, metadata_json, content_ref in rows:
            try:
                metadata = json.loads(metadata_json)
            except json.JSONDecodeError:
                continue
            if not isinstance(metadata, dict) or metadata.get("kind") != kind:
                continue
            full = self.blob_dir / content_ref
            if not full.exists():
                continue
            try:
                payload = json.loads(full.read_bytes())
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                results.append((record_id, metadata, payload))
        return results
