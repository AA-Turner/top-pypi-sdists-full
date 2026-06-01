"""Provenance store, receipt log, walker, and verify tests.

Uses `tmp_path` for filesystem isolation — every test gets a fresh
`.efterlev/` under a pytest-managed temp dir. The store and receipts log
are both on disk, so these are integration-ish tests, not pure units.
"""

from __future__ import annotations

import json
from pathlib import Path
from threading import Thread

import pytest

from efterlev.errors import ProvenanceError
from efterlev.provenance import (
    ProvenanceStore,
    render_chain_text,
    verify_receipts,
    walk_chain,
)

# --- ProvenanceStore: writes and reads ----------------------------------------


def test_store_write_then_get_record(tmp_path: Path) -> None:
    with ProvenanceStore(tmp_path) as store:
        record = store.write_record(
            payload={"detector_id": "aws.test", "content": {"x": 1}},
            record_type="evidence",
            primitive="scan_terraform@0.1.0",
        )
        assert record.record_id.startswith("sha256:")
        assert record.content_ref.endswith(".json")

        roundtrip = store.get_record(record.record_id)
        assert roundtrip is not None
        assert roundtrip.record_id == record.record_id
        assert roundtrip.record_type == "evidence"
        assert roundtrip.primitive == "scan_terraform@0.1.0"


def test_store_read_payload_round_trips_original_dict(tmp_path: Path) -> None:
    payload = {"detector_id": "aws.test", "content": {"resource": "bucket-1", "ok": True}}
    with ProvenanceStore(tmp_path) as store:
        record = store.write_record(payload=payload, record_type="evidence")
        assert store.read_payload(record) == payload


def test_store_same_payload_twice_shares_blob_but_produces_distinct_records(
    tmp_path: Path,
) -> None:
    payload = {"detector_id": "aws.test", "content": {"x": 1}}
    with ProvenanceStore(tmp_path) as store:
        first = store.write_record(payload=payload, record_type="evidence")
        second = store.write_record(payload=payload, record_type="evidence")
        # Different records because timestamps differ...
        assert first.record_id != second.record_id
        # ...but the same blob on disk.
        assert first.content_ref == second.content_ref


def test_write_record_dedupes_detector_evidence_by_evidence_id_v0_1_155(tmp_path: Path) -> None:
    """v0.1.155 / #360: write-time evidence dedupe. The second write of a
    payload with the same `evidence_id` returns the EXISTING record (skip
    blob + SQLite insert) so the store stops growing on re-scans of
    unchanged source.
    """
    from datetime import UTC, datetime

    payload = {
        "evidence_id": "sha256:" + "a" * 64,
        "detector_id": "aws.test",
        "source_ref": {"file": "main.tf"},
        "timestamp": datetime(2026, 1, 1, tzinfo=UTC).isoformat(),
        "content": {"k": "v"},
    }
    with ProvenanceStore(tmp_path) as store:
        first = store.write_record(payload=payload, record_type="evidence")
        before = store._conn.execute(
            "SELECT COUNT(*) FROM provenance_records WHERE record_type='evidence'"
        ).fetchone()[0]
        # Second write — same evidence_id, different timestamp.
        payload_2 = {**payload, "timestamp": datetime(2026, 5, 17, tzinfo=UTC).isoformat()}
        second = store.write_record(payload=payload_2, record_type="evidence")
        after = store._conn.execute(
            "SELECT COUNT(*) FROM provenance_records WHERE record_type='evidence'"
        ).fetchone()[0]
        # SQLite row count did NOT grow — the dedupe skipped the insert.
        assert before == after == 1, f"expected 1 row, before={before} after={after}"
        # And the second call returned the FIRST record (same record_id).
        assert first.record_id == second.record_id


def test_write_record_does_not_dedupe_primitive_wrapper_records_v0_1_155(tmp_path: Path) -> None:
    """v0.1.155 / #360: primitive-wrapper records ({"input":..., "output":...}
    have no top-level `evidence_id` — they capture per-run primitive-
    invocation history and SHOULD continue to write distinct rows. Only
    detector-emitted Evidence dedupes.
    """
    payload = {"input": {"target_dir": "/x"}, "output": {"resources": 5}}
    with ProvenanceStore(tmp_path) as store:
        first = store.write_record(
            payload=payload, record_type="evidence", primitive="scan_terraform@0.1.0"
        )
        second = store.write_record(
            payload=payload, record_type="evidence", primitive="scan_terraform@0.1.0"
        )
        # Distinct records — no dedupe on payload-without-evidence_id.
        assert first.record_id != second.record_id


def test_write_record_does_not_dedupe_claims_v0_1_155(tmp_path: Path) -> None:
    """Claims (e.g., gap-agent KSI classifications) MUST keep writing
    distinct rows on every agent run — re-running gap with the same
    evidence still produces a fresh historical record. Dedupe is
    record_type='evidence' only.
    """
    payload = {
        "claim_type": "classification",
        "content": {"ksi_id": "KSI-X-Y", "status": "implemented", "rationale": "..."},
        "confidence": "medium",
    }
    with ProvenanceStore(tmp_path) as store:
        first = store.write_record(payload=payload, record_type="claim")
        second = store.write_record(payload=payload, record_type="claim")
        assert first.record_id != second.record_id


def test_iter_evidence_dedupes_pre_v0_1_155_duplicate_evidence_id_rows(
    tmp_path: Path,
) -> None:
    """v0.1.153 / #358 + v0.1.155 / #360: pre-v0.1.155 stores accumulated
    duplicate `evidence_id` rows on every re-scan (write-time dedupe
    didn't exist yet). `iter_evidence` MUST still collapse them by
    `evidence_id` on read so existing stores benefit without a migration.

    Simulates a pre-v0.1.155 store by inserting two duplicate evidence
    rows directly via the SQLite + blob layer, bypassing `write_record`'s
    v0.1.155 dedupe. Asserts `iter_evidence` returns exactly one record
    (the older).
    """
    import sqlite3
    from datetime import UTC, datetime

    ev_id = "sha256:" + "a" * 64
    early = datetime(2026, 1, 1, tzinfo=UTC).isoformat()
    later = datetime(2026, 5, 17, tzinfo=UTC).isoformat()
    base = {
        "evidence_id": ev_id,
        "detector_id": "aws.s3_encryption",
        "source_ref": {"file": "main.tf"},
        "content": {"resource": "audit"},
    }
    with ProvenanceStore(tmp_path) as store:
        # Write two duplicate evidence blobs + SQLite rows DIRECTLY,
        # bypassing v0.1.155 write_record dedupe. This is how a pre-
        # v0.1.155 store would look after two scans of unchanged source.
        for ts, rid_suffix in ((early, "1"), (later, "2")):
            payload = {**base, "timestamp": ts}
            content_ref = store._put_blob(payload)
            try:
                store._conn.execute(
                    "INSERT INTO provenance_records "
                    "(record_id, record_type, content_ref, derived_from, "
                    " primitive, agent, model, prompt_hash, timestamp, metadata) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        "sha256:" + rid_suffix * 64,
                        "evidence",
                        content_ref,
                        "[]",
                        "test@0.1.0",
                        None,
                        None,
                        None,
                        ts,
                        "{}",
                    ),
                )
                store._conn.commit()
            except sqlite3.Error:
                raise

        # `iter_evidence` should collapse to exactly one record (the older).
        rows = store.iter_evidence()
        assert len(rows) == 1, (
            f"iter_evidence should dedupe by evidence_id; got {len(rows)} records"
        )
        assert rows[0][1]["timestamp"] == early


def test_store_missing_record_returns_none(tmp_path: Path) -> None:
    with ProvenanceStore(tmp_path) as store:
        assert store.get_record("sha256:" + "0" * 64) is None


def test_store_read_payload_raises_when_blob_missing(tmp_path: Path) -> None:
    with ProvenanceStore(tmp_path) as store:
        record = store.write_record(payload={"detector_id": "a"}, record_type="evidence")
        # Simulate a corrupted store by deleting the blob.
        (store.blob_dir / record.content_ref).unlink()
        with pytest.raises(ProvenanceError, match="blob missing"):
            store.read_payload(record)


# --- resolve_record_id_prefix --------------------------------------------------


def test_resolve_record_id_prefix_full_id_round_trips(tmp_path: Path) -> None:
    with ProvenanceStore(tmp_path) as store:
        record = store.write_record(payload={"x": 1}, record_type="evidence")
        assert store.resolve_record_id_prefix(record.record_id) == record.record_id


def test_resolve_record_id_prefix_unique_short_prefix(tmp_path: Path) -> None:
    """Rationales print 8-char prefixes; resolver maps them back to full IDs."""
    with ProvenanceStore(tmp_path) as store:
        record = store.write_record(payload={"x": 1}, record_type="evidence")
        bare_prefix = record.record_id[len("sha256:") : len("sha256:") + 8]
        # Both `sha256:abc12345` and bare `abc12345` should resolve.
        assert store.resolve_record_id_prefix(f"sha256:{bare_prefix}") == record.record_id
        assert store.resolve_record_id_prefix(bare_prefix) == record.record_id


def test_resolve_record_id_prefix_no_match_returns_none(tmp_path: Path) -> None:
    with ProvenanceStore(tmp_path) as store:
        store.write_record(payload={"x": 1}, record_type="evidence")
        assert store.resolve_record_id_prefix("sha256:deadbeef") is None
        assert store.resolve_record_id_prefix("deadbeef") is None


def test_resolve_record_id_prefix_too_short_returns_none(tmp_path: Path) -> None:
    """Below 4 hex chars, even small workspaces can collide; refuse early."""
    with ProvenanceStore(tmp_path) as store:
        store.write_record(payload={"x": 1}, record_type="evidence")
        assert store.resolve_record_id_prefix("ab") is None
        assert store.resolve_record_id_prefix("sha256:ab") is None


def test_resolve_record_id_prefix_collision_raises(tmp_path: Path) -> None:
    """When a prefix matches ≥2 records, the resolver must raise instead of
    silently disambiguating by insertion order. Naturally producing a ≥4-char
    sha256 collision is hard, so we drive the LIKE branch by writing enough
    records that any 1-char prefix matches several, then asking the resolver
    for a 4-char prefix that overlaps two natural record_ids."""
    with ProvenanceStore(tmp_path) as store:
        # 1000 records → ~16 expected collisions on 4-char prefixes (birthday).
        for i in range(1000):
            store.write_record(payload={"i": i}, record_type="evidence")
        buckets: dict[str, list[str]] = {}
        for rid in store.iter_records():
            buckets.setdefault(rid[len("sha256:") : len("sha256:") + 4], []).append(rid)
        collisions = [pfx for pfx, members in buckets.items() if len(members) >= 2]
        assert collisions, "expected at least one 4-char collision after 1000 writes"
        with pytest.raises(ProvenanceError, match="multiple records"):
            store.resolve_record_id_prefix(collisions[0])


def test_resolve_record_id_prefix_resolves_evidence_id_prefix(tmp_path: Path) -> None:
    """v0.1.6 fix: POAM rationales print 8-char prefixes of `Evidence.evidence_id`,
    not `ProvenanceRecord.record_id`. The two are different SHAs (envelope vs
    content hash). v0.1.5's prefix-resolver only matched record_ids; pasting
    the POAM-shown prefix into `provenance show` returned 'no record matches'
    even though the full evidence_id walked correctly via dual-key lookup."""
    from datetime import UTC, datetime

    from efterlev.models import Evidence, SourceRef

    with ProvenanceStore(tmp_path) as store:
        ev = Evidence.create(
            detector_id="aws.test",
            source_ref=SourceRef(file=Path("main.tf"), line_start=1, line_end=10),
            ksis_evidenced=["KSI-X"],
            controls_evidenced=["AC-1"],
            content={"x": 1},
            timestamp=datetime(2026, 5, 4, tzinfo=UTC),
        )
        record = store.write_record(payload=ev.model_dump(mode="json"), record_type="evidence")
        # Precondition: record_id and evidence_id are distinct SHAs.
        assert record.record_id != ev.evidence_id

        # 8-char prefix of evidence_id resolves to the wrapping record_id.
        ev_prefix = ev.evidence_id[len("sha256:") : len("sha256:") + 8]
        assert store.resolve_record_id_prefix(ev_prefix) == record.record_id
        assert store.resolve_record_id_prefix(f"sha256:{ev_prefix}") == record.record_id

        # Full evidence_id also resolves (dual-key path).
        assert store.resolve_record_id_prefix(ev.evidence_id) == record.record_id


# --- ReceiptLog: atomicity under concurrency ----------------------------------


def test_receipt_log_written_per_record(tmp_path: Path) -> None:
    with ProvenanceStore(tmp_path) as store:
        store.write_record(payload={"a": 1}, record_type="evidence")
        store.write_record(payload={"a": 2}, record_type="evidence")
        entries = store.receipts.read_all()
        assert len(entries) == 2
        assert all(e["record_id"].startswith("sha256:") for e in entries)


def test_receipt_log_carries_token_usage_when_metadata_supplies_it(tmp_path: Path) -> None:
    """v0.1.9: when an agent persists `input_tokens` / `output_tokens` in
    record metadata, receipts.log surfaces them as top-level fields so
    operators can sum spend with `jq` without parsing blob payloads."""
    with ProvenanceStore(tmp_path) as store:
        # Claim record with token metadata (simulates an agent write path).
        store.write_record(
            payload={"a": 1},
            record_type="evidence",
            metadata={"kind": "x", "input_tokens": 8421, "output_tokens": 2103},
        )
        # Record without token metadata (deterministic primitive invocation).
        store.write_record(payload={"a": 2}, record_type="evidence")

        entries = store.receipts.read_all()
        with_tokens = [e for e in entries if "input_tokens" in e]
        without_tokens = [e for e in entries if "input_tokens" not in e]
        assert len(with_tokens) == 1
        assert with_tokens[0]["input_tokens"] == 8421
        assert with_tokens[0]["output_tokens"] == 2103
        # Records that didn't carry usage in metadata stay clean — no
        # zero-sentinel that would skew aggregates.
        assert len(without_tokens) == 1


def test_receipt_log_survives_concurrent_writes(tmp_path: Path) -> None:
    # Ten threads each write three records in parallel. Expect 30 receipt
    # lines total, every line valid JSON (flock serializes writes).
    store = ProvenanceStore(tmp_path)

    def worker(i: int) -> None:
        for j in range(3):
            store.write_record(payload={"worker": i, "n": j}, record_type="evidence")

    threads = [Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    entries = store.receipts.read_all()
    assert len(entries) == 30
    # No duplicated record_ids (thread uniqueness via worker+n tuple in payload).
    assert len({e["record_id"] for e in entries}) == 30
    store.close()


# --- Walker -------------------------------------------------------------------


def test_walker_walks_three_node_chain(tmp_path: Path) -> None:
    # evidence  <--  claim1  <--  claim2
    with ProvenanceStore(tmp_path) as store:
        ev = store.write_record(
            payload={"source": "main.tf"},
            record_type="evidence",
            primitive="scan_terraform@0.1.0",
        )
        c1 = store.write_record(
            payload={"kind": "intermediate"},
            record_type="claim",
            derived_from=[ev.record_id],
            agent="gap_agent",
            model="claude-opus-4-7",
        )
        c2 = store.write_record(
            payload={"kind": "leaf"},
            record_type="claim",
            derived_from=[c1.record_id],
            agent="documentation_agent",
            model="claude-opus-4-7",
        )

        tree = walk_chain(store, c2.record_id)
        assert tree.record.record_id == c2.record_id
        assert len(tree.parents) == 1
        assert tree.parents[0].record.record_id == c1.record_id
        assert len(tree.parents[0].parents) == 1
        assert tree.parents[0].parents[0].record.record_id == ev.record_id
        assert tree.parents[0].parents[0].parents == []  # leaf


def test_walker_raises_on_missing_record(tmp_path: Path) -> None:
    with (
        ProvenanceStore(tmp_path) as store,
        pytest.raises(ProvenanceError, match="record not found"),
    ):
        walk_chain(store, "sha256:" + "0" * 64)


def test_walker_resolves_evidence_id_via_dual_key_lookup(tmp_path: Path) -> None:
    """`provenance show <evidence_id>` must work, not just `<record_id>`.

    Discovered 2026-04-25 in the round-1 3PAO review of a real attestation
    artifact: the artifact's `citations[].evidence_id` (Evidence content
    hash) was not the same as the wrapping `ProvenanceRecord.record_id`
    (envelope hash including timestamps + metadata). The store-level
    validator did dual-key lookup (`_validate_claim_derived_from`); the
    walker did not. Result: every cited evidence_id failed
    `provenance show`, blocking traceability.

    This test locks the dual-key contract on the walker. Walking by
    evidence_id must produce the same result as walking by record_id.
    """
    with ProvenanceStore(tmp_path) as store:
        # Write an evidence record carrying its own `evidence_id` field
        # in the payload — mirrors the real Evidence shape produced by
        # detectors. The Evidence's evidence_id is intentionally distinct
        # from the wrapping ProvenanceRecord's record_id.
        evidence_payload = {
            "evidence_id": "sha256:" + "a" * 64,  # the content hash
            "detector_id": "aws.test",
            "content": {"resource_name": "bucket-1"},
        }
        record = store.write_record(
            payload=evidence_payload,
            record_type="evidence",
            primitive="scan_terraform@0.1.0",
        )
        # Confirm the two ids genuinely differ (precondition for the
        # bug class — if they're ever the same, this test is moot).
        assert record.record_id != evidence_payload["evidence_id"]

        # Walk by record_id — works historically.
        by_record = walk_chain(store, record.record_id)
        assert by_record.record.record_id == record.record_id

        # Walk by evidence_id — must work post-fix.
        by_evidence = walk_chain(store, evidence_payload["evidence_id"])
        assert by_evidence.record.record_id == record.record_id


def test_resolve_to_record_returns_none_on_unresolvable_id(tmp_path: Path) -> None:
    """Helper contract: misses return None, not raise.

    `walk_chain` is responsible for raising `ProvenanceError` on miss
    (with chain context). The resolver itself returns None — keeps
    error semantics out of the lookup helper.
    """
    with ProvenanceStore(tmp_path) as store:
        store.write_record(
            payload={"evidence_id": "sha256:" + "b" * 64, "x": 1},
            record_type="evidence",
        )
        assert store.resolve_to_record("sha256:" + "0" * 64) is None


def test_walker_raises_on_cycle(tmp_path: Path) -> None:
    # Manufacture a corrupt store by writing a record whose derived_from
    # references itself via direct SQL. Walker must detect the cycle.
    with ProvenanceStore(tmp_path) as store:
        record = store.write_record(payload={"x": 1}, record_type="evidence")
        store._conn.execute(
            "UPDATE provenance_records SET derived_from = ? WHERE record_id = ?",
            (json.dumps([record.record_id]), record.record_id),
        )
        store._conn.commit()

        with pytest.raises(ProvenanceError, match="cycle in provenance graph"):
            walk_chain(store, record.record_id)


def test_render_chain_text_indents_parents(tmp_path: Path) -> None:
    with ProvenanceStore(tmp_path) as store:
        ev = store.write_record(payload={"x": 1}, record_type="evidence")
        claim = store.write_record(
            payload={"y": 2},
            record_type="claim",
            derived_from=[ev.record_id],
            agent="gap_agent",
            model="claude-opus-4-7",
        )
        tree = walk_chain(store, claim.record_id)
        output = render_chain_text(tree)
        assert claim.record_id in output
        assert ev.record_id in output
        assert "└── " in output  # child marker rendered
        # v0.1.11: leaf message disambiguated by record_type (3PAO finding).
        # Evidence leaves print the scanner-emitted variant; Claim leaves
        # print the empty-derived_from-by-design variant.
        assert "scanner-emitted leaf" in output


def test_render_chain_text_disambiguates_claim_leaf(tmp_path: Path) -> None:
    """v0.1.11 (3PAO finding): a Claim record with empty derived_from is
    legitimate when the underlying classification cited no evidence
    (`not_implemented`, `evidence_layer_inapplicable` without manifests).
    The walker should surface the by-design framing rather than the bare
    "(leaf — no derived_from)" message that read like a bug to the v0.1.10
    blinded reviewer."""
    with ProvenanceStore(tmp_path) as store:
        # Claim with no derived_from — a not_implemented classification.
        claim = store.write_record(
            payload={"status": "not_implemented"},
            record_type="claim",
            agent="gap_agent",
            model="claude-opus-4-7",
        )
        tree = walk_chain(store, claim.record_id)
        output = render_chain_text(tree)
        assert "claim with empty derived_from" in output
        assert "not a traceability break" in output


def test_render_chain_text_surfaces_source_ref_at_evidence_leaves(tmp_path: Path) -> None:
    """`efterlev provenance show` must surface source file + line range at
    evidence leaves so the user can trace a claim back to Terraform without
    opening the blob manually. Regression test for the gap caught in the
    2026-04-23 external review."""
    with ProvenanceStore(tmp_path) as store:
        ev = store.write_record(
            payload={
                "detector_id": "aws.encryption_s3_at_rest",
                "source_ref": {"file": "infra/main.tf", "line_start": 12, "line_end": 18},
                "content": {"resource_name": "reports", "encryption_state": "absent"},
            },
            record_type="evidence",
            primitive="aws.encryption_s3_at_rest@0.1.0",
        )
        claim = store.write_record(
            payload={"status": "not_implemented"},
            record_type="claim",
            derived_from=[ev.record_id],
            agent="gap_agent",
            model="claude-opus-4-7",
        )
        tree = walk_chain(store, claim.record_id)
        output = render_chain_text(tree)
        assert "source=infra/main.tf:12-18" in output


def test_render_chain_text_handles_single_line_source_ref(tmp_path: Path) -> None:
    with ProvenanceStore(tmp_path) as store:
        ev = store.write_record(
            payload={
                "source_ref": {"file": "main.tf", "line_start": 5, "line_end": 5},
            },
            record_type="evidence",
        )
        tree = walk_chain(store, ev.record_id)
        output = render_chain_text(tree)
        # Collapse file:5-5 into file:5 for single-line references.
        assert "source=main.tf:5" in output
        assert "5-5" not in output


def test_render_chain_text_omits_source_line_when_payload_lacks_source_ref(
    tmp_path: Path,
) -> None:
    """Non-Evidence records emitted under record_type=evidence by a
    primitive (e.g. init's catalog-loaded receipt) may not have a
    source_ref. The renderer must not crash and must not invent content."""
    with ProvenanceStore(tmp_path) as store:
        rec = store.write_record(
            payload={"action": "catalogs_loaded", "baseline": "fedramp-20x-moderate"},
            record_type="evidence",
            primitive="efterlev.init@0.1.0",
        )
        tree = walk_chain(store, rec.record_id)
        output = render_chain_text(tree)
        assert "source=" not in output


# --- verify_receipts ----------------------------------------------------------


def test_verify_receipts_clean_store(tmp_path: Path) -> None:
    with ProvenanceStore(tmp_path) as store:
        store.write_record(payload={"a": 1}, record_type="evidence")
        store.write_record(payload={"a": 2}, record_type="evidence")
        report = verify_receipts(store)
        assert report.clean
        assert report.store_records == 2
        assert report.receipts == 2
        assert report.missing_receipts == []
        assert report.orphan_receipts == []
        assert report.mismatched == []


def test_verify_receipts_detects_record_without_receipt(tmp_path: Path) -> None:
    # Write one record, then write a second directly to SQLite (bypassing the
    # receipt log) to simulate a tampered store.
    store = ProvenanceStore(tmp_path)
    store.write_record(payload={"a": 1}, record_type="evidence")

    store._conn.execute(
        "INSERT INTO provenance_records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "sha256:" + "f" * 64,
            "evidence",
            "ff/ff/ffff.json",
            "[]",
            None,
            None,
            None,
            None,
            "2026-04-20T00:00:00+00:00",
            "{}",
        ),
    )
    store._conn.commit()

    report = verify_receipts(store)
    assert not report.clean
    assert "sha256:" + "f" * 64 in report.missing_receipts
    store.close()


def test_verify_receipts_detects_orphan_receipt(tmp_path: Path) -> None:
    # Write a legit record, then manually append a stray receipt whose
    # record_id isn't in the store.
    store = ProvenanceStore(tmp_path)
    store.write_record(payload={"a": 1}, record_type="evidence")

    stray = {
        "ts": "2026-04-20T00:00:00+00:00",
        "record_id": "sha256:" + "1" * 64,
        "record_type": "evidence",
        "derived_from": [],
        "primitive": None,
        "agent": None,
        "model": None,
        "prompt_hash": None,
    }
    with open(store.receipts.path, "a", encoding="utf-8") as f:
        f.write(json.dumps(stray) + "\n")

    report = verify_receipts(store)
    assert not report.clean
    assert "sha256:" + "1" * 64 in report.orphan_receipts
    store.close()
