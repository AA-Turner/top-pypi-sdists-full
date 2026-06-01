"""Tests for v0.1.143 / #348 — per-batch gap-agent processing.

Three units under test:
  - `plan_batches`: chunks indicators, filters evidence per batch
  - `compute_unmapped_findings`: deterministic UnmappedFinding builder
  - `fill_missing_classifications`: safety net for LLM omissions

Plus integration tests via `GapAgent.run()` with a sequenced stub
that returns different per-batch responses, verifying batches run
sequentially and results merge correctly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import pytest

from efterlev.agents import GapAgent, GapAgentInput
from efterlev.agents.gap import (
    GapReport,
    KsiClassification,
    compute_unmapped_findings,
    fill_missing_classifications,
    plan_batches,
)
from efterlev.llm.base import LLMMessage, LLMResponse
from efterlev.models import Evidence, Indicator, SourceRef
from efterlev.provenance import ProvenanceStore, active_store


def _ind(ksi_id: str) -> Indicator:
    return Indicator(
        id=ksi_id,
        theme=ksi_id.split("-")[1],
        name=f"name-{ksi_id}",
        statement="...",
        controls=["sc-28"],
    )


def _ev(
    *,
    detector_id: str = "aws.encryption",
    ksis_evidenced: list[str] | None = None,
    controls: list[str] | None = None,
    resource_name: str = "r",
) -> Evidence:
    return Evidence.create(
        detector_id=detector_id,
        source_ref=SourceRef(file=Path("main.tf"), line_start=1, line_end=2),
        ksis_evidenced=ksis_evidenced if ksis_evidenced is not None else ["KSI-SVC-VRI"],
        controls_evidenced=controls if controls is not None else ["SC-28"],
        content={"resource_name": resource_name},
        timestamp=datetime(2026, 5, 16, tzinfo=UTC),
    )


# --- plan_batches --------------------------------------------------------


def test_plan_batches_empty_indicators_returns_empty_plan() -> None:
    assert plan_batches([], []) == []


def test_plan_batches_chunks_indicators_by_default_size() -> None:
    indicators = [_ind(f"KSI-X-{i:03d}") for i in range(13)]
    batches = plan_batches(indicators, [])
    # Default batch size is 5: 13 indicators -> 3 batches (5, 5, 3).
    assert [len(b.indicators) for b in batches] == [5, 5, 3]
    assert all(b.total == 3 for b in batches)
    assert [b.index for b in batches] == [1, 2, 3]


def test_plan_batches_respects_custom_batch_size() -> None:
    indicators = [_ind(f"KSI-X-{i:03d}") for i in range(10)]
    batches = plan_batches(indicators, [], batch_size_ksis=3)
    # 10 / 3 = 4 batches (3, 3, 3, 1).
    assert [len(b.indicators) for b in batches] == [3, 3, 3, 1]


def test_plan_batches_zero_or_negative_size_falls_back_to_default() -> None:
    indicators = [_ind(f"KSI-X-{i:03d}") for i in range(6)]
    batches_zero = plan_batches(indicators, [], batch_size_ksis=0)
    batches_neg = plan_batches(indicators, [], batch_size_ksis=-1)
    # Defaults to 5 -> 2 batches of (5, 1).
    assert [len(b.indicators) for b in batches_zero] == [5, 1]
    assert [len(b.indicators) for b in batches_neg] == [5, 1]


def test_plan_batches_filters_evidence_by_ksi_overlap() -> None:
    """Evidence whose `ksis_evidenced` doesn't include any KSI in the batch
    must be excluded — that's the core context-saving move."""
    a, b, c = _ind("KSI-A"), _ind("KSI-B"), _ind("KSI-C")
    ev_a = _ev(ksis_evidenced=["KSI-A"], resource_name="evA")
    ev_b = _ev(ksis_evidenced=["KSI-B"], resource_name="evB")
    ev_c = _ev(ksis_evidenced=["KSI-C"], resource_name="evC")
    batches = plan_batches([a, b, c], [ev_a, ev_b, ev_c], batch_size_ksis=2)
    # 2 batches: [A, B] and [C].
    assert len(batches) == 2
    batch1_resources = {ev.content["resource_name"] for ev in batches[0].evidence}
    batch2_resources = {ev.content["resource_name"] for ev in batches[1].evidence}
    assert batch1_resources == {"evA", "evB"}
    assert batch2_resources == {"evC"}


def test_plan_batches_duplicates_multi_ksi_evidence_across_batches() -> None:
    """A single evidence record attributed to KSIs in multiple batches must
    appear in every batch — correctness over de-dup."""
    a = _ind("KSI-A")
    c = _ind("KSI-C")
    ev_ac = _ev(ksis_evidenced=["KSI-A", "KSI-C"], resource_name="ev_ac")
    batches = plan_batches([a, c], [ev_ac], batch_size_ksis=1)
    assert len(batches) == 2
    assert all(len(b.evidence) == 1 for b in batches)
    assert all(b.evidence[0].content["resource_name"] == "ev_ac" for b in batches)


def test_plan_batches_excludes_unmapped_evidence_from_all_batches() -> None:
    """Evidence with `ksis_evidenced=[]` is never sent to the LLM — handled
    deterministically by `compute_unmapped_findings`."""
    a = _ind("KSI-A")
    ev_mapped = _ev(ksis_evidenced=["KSI-A"], resource_name="mapped")
    ev_unmapped = _ev(ksis_evidenced=[], resource_name="unmapped")
    batches = plan_batches([a], [ev_mapped, ev_unmapped])
    assert len(batches) == 1
    assert [ev.content["resource_name"] for ev in batches[0].evidence] == ["mapped"]


# --- compute_unmapped_findings -------------------------------------------


def test_compute_unmapped_findings_skips_mapped_evidence() -> None:
    mapped = _ev(ksis_evidenced=["KSI-A"], resource_name="mapped")
    findings = compute_unmapped_findings([mapped])
    assert findings == []


def test_compute_unmapped_findings_emits_one_finding_per_unmapped_record() -> None:
    u1 = _ev(ksis_evidenced=[], controls=["SC-7"], resource_name="u1")
    u2 = _ev(ksis_evidenced=[], controls=["AU-2", "AU-3"], resource_name="u2")
    mapped = _ev(ksis_evidenced=["KSI-A"], resource_name="mapped")
    findings = compute_unmapped_findings([u1, mapped, u2])
    assert len(findings) == 2
    evidence_ids = {f.evidence_id for f in findings}
    assert u1.evidence_id in evidence_ids
    assert u2.evidence_id in evidence_ids
    assert mapped.evidence_id not in evidence_ids


def test_compute_unmapped_findings_note_mentions_detector_and_controls() -> None:
    unmapped = _ev(
        detector_id="github.branch_protection",
        ksis_evidenced=[],
        controls=["AC-3"],
    )
    findings = compute_unmapped_findings([unmapped])
    assert len(findings) == 1
    note = findings[0].note
    assert "github.branch_protection" in note
    assert "AC-3" in note
    assert "not mapped to any KSI" in note


def test_compute_unmapped_findings_handles_evidence_with_no_controls() -> None:
    """Evidence with empty controls_evidenced (rare but possible) still
    gets a note — the template handles the (none) case explicitly."""
    unmapped = _ev(ksis_evidenced=[], controls=[])
    findings = compute_unmapped_findings([unmapped])
    assert len(findings) == 1
    assert "(none)" in findings[0].note


# --- fill_missing_classifications ----------------------------------------


def test_fill_missing_classifications_no_op_when_all_present() -> None:
    a, b = _ind("KSI-A"), _ind("KSI-B")
    report = GapReport(
        ksi_classifications=[
            KsiClassification(ksi_id="KSI-A", status="not_implemented", rationale="x"),
            KsiClassification(ksi_id="KSI-B", status="not_implemented", rationale="y"),
        ],
        unmapped_findings=[],
    )
    patched, notes = fill_missing_classifications(report, [a, b])
    assert notes == []
    assert patched is report  # short-circuit returns the input unchanged


def test_fill_missing_classifications_adds_placeholder_for_omitted_ksi() -> None:
    a, b = _ind("KSI-A"), _ind("KSI-B")
    report = GapReport(
        ksi_classifications=[
            KsiClassification(
                ksi_id="KSI-A", status="implemented", rationale="x", evidence_ids=["sha256:foo"]
            ),
        ],
        unmapped_findings=[],
    )
    patched, notes = fill_missing_classifications(report, [a, b])
    assert len(patched.ksi_classifications) == 2
    by_id = {clf.ksi_id: clf for clf in patched.ksi_classifications}
    assert by_id["KSI-B"].status == "not_implemented"
    assert "[auto-repair:" in by_id["KSI-B"].rationale
    assert by_id["KSI-B"].evidence_ids == []
    assert any("KSI-B" in n for n in notes)


def test_fill_missing_classifications_drops_unknown_ksi_ids() -> None:
    """v0.1.146 / #351: model sometimes emits a malformed KSI id (e.g.
    `KSI-SUS` instead of `KSI-IAM-SUS`). Without filtering, both the
    bad id AND the placeholder for the real omitted id end up in the
    report. v0.1.146 drops unknown ids; placeholder still fires for
    the missing real id."""
    real_ksi = _ind("KSI-IAM-SUS")
    report = GapReport(
        ksi_classifications=[
            # Bad: model dropped the IAM family prefix.
            KsiClassification(
                ksi_id="KSI-SUS",
                status="evidence_layer_inapplicable",
                rationale="bad id",
                evidence_ids=[],
            ),
        ],
        unmapped_findings=[],
    )
    patched, notes = fill_missing_classifications(report, [real_ksi])
    # Bad id dropped; real id filled with placeholder.
    by_id = {clf.ksi_id: clf for clf in patched.ksi_classifications}
    assert "KSI-SUS" not in by_id
    assert "KSI-IAM-SUS" in by_id
    assert by_id["KSI-IAM-SUS"].status == "not_implemented"
    assert any("KSI-SUS" in n and "dropped" in n for n in notes)
    assert any("KSI-IAM-SUS" in n and "omitted" in n for n in notes)


def test_fill_missing_classifications_preserves_existing_classifications() -> None:
    """The patched report must keep the original classifications byte-identical
    — we only ADD placeholders, never modify what the model returned."""
    a, b = _ind("KSI-A"), _ind("KSI-B")
    original_a = KsiClassification(
        ksi_id="KSI-A", status="partial", rationale="real", evidence_ids=["sha256:r"]
    )
    report = GapReport(ksi_classifications=[original_a], unmapped_findings=[])
    patched, _ = fill_missing_classifications(report, [a, b])
    by_id = {clf.ksi_id: clf for clf in patched.ksi_classifications}
    assert by_id["KSI-A"] == original_a


# --- GapAgent.run() integration ------------------------------------------


@dataclass
class _PerBatchStubClient:
    """Returns a different response on each call — enough for batched flow."""

    responses: list[str]
    model: str = "stub-haiku"
    call_count: int = 0
    last_prompt_hash: str = ""
    last_system: str = ""
    last_messages: list[LLMMessage] = field(default_factory=list)

    def complete(
        self,
        *,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int = 4096,
        on_chunk=None,
    ) -> LLMResponse:
        import hashlib

        idx = min(self.call_count, len(self.responses) - 1)
        text = self.responses[idx]
        self.last_system = system
        self.last_messages = list(messages)
        self.call_count += 1
        prompt_hash = hashlib.sha256(
            (system + "\n".join(m.content for m in messages)).encode("utf-8")
        ).hexdigest()
        self.last_prompt_hash = prompt_hash
        return LLMResponse(text=text, model=self.model, prompt_hash=prompt_hash)


def _batch_response(ksi_ids: list[str]) -> str:
    """A clean response with one not_implemented classification per KSI."""
    return json.dumps(
        {
            "ksi_classifications": [
                {
                    "ksi_id": kid,
                    "status": "not_implemented",
                    "rationale": "no evidence",
                    "evidence_ids": [],
                }
                for kid in ksi_ids
            ],
            "unmapped_findings": [],
        }
    )


def test_gap_agent_run_makes_one_llm_call_per_batch(tmp_path: Path) -> None:
    """13 indicators with default batch size 5 -> 3 batches -> 3 LLM calls.
    The merged report covers all 13 indicators."""
    indicators = [_ind(f"KSI-X-{i:03d}") for i in range(13)]
    batch_a = [f"KSI-X-{i:03d}" for i in range(5)]
    batch_b = [f"KSI-X-{i:03d}" for i in range(5, 10)]
    batch_c = [f"KSI-X-{i:03d}" for i in range(10, 13)]
    stub = _PerBatchStubClient(
        responses=[_batch_response(batch_a), _batch_response(batch_b), _batch_response(batch_c)]
    )
    with ProvenanceStore(tmp_path) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        report = agent.run(GapAgentInput(indicators=indicators, evidence=[]))
    assert stub.call_count == 3
    assert len(report.ksi_classifications) == 13
    assert {clf.ksi_id for clf in report.ksi_classifications} == {i.id for i in indicators}


def test_gap_agent_run_persists_one_claim_per_classification_across_batches(
    tmp_path: Path,
) -> None:
    """Each batch's claims get written to the active store with batch metadata.
    Total claim count = total classification count."""
    indicators = [_ind(f"KSI-Y-{i:03d}") for i in range(7)]
    batch_a = [f"KSI-Y-{i:03d}" for i in range(5)]
    batch_b = [f"KSI-Y-{i:03d}" for i in range(5, 7)]
    stub = _PerBatchStubClient(responses=[_batch_response(batch_a), _batch_response(batch_b)])
    with ProvenanceStore(tmp_path) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        report = agent.run(GapAgentInput(indicators=indicators, evidence=[]))
        # 7 claim records persisted, one per KSI. Pull them back via the
        # record-ids the run() returns (claim_record_ids).
        claim_records = [store.get_record(rid) for rid in report.claim_record_ids]
        assert len(claim_records) == 7
        # Each record carries batch_index/batch_total metadata.
        batch_indices = {
            rec.metadata.get("batch_index") for rec in claim_records if rec is not None
        }
        assert batch_indices == {1, 2}
    assert len(report.claim_record_ids) == 7


def test_gap_agent_run_isolates_batch_failures(tmp_path: Path) -> None:
    """A batch that retries 3 times and gracefully repairs must not abort
    other batches. Batches 1 and 3 succeed; batch 2 retries 3 times with
    a fabricated id and graceful-repairs."""
    indicators = [_ind(f"KSI-Z-{i:03d}") for i in range(10)]
    batch_a_ksis = [f"KSI-Z-{i:03d}" for i in range(5)]
    batch_b_ksis = [f"KSI-Z-{i:03d}" for i in range(5, 10)]
    # Batch B uses a fabricated id in all 3 attempts -> graceful repair fires.
    batch_b_bad = json.dumps(
        {
            "ksi_classifications": [
                {
                    "ksi_id": kid,
                    "status": "implemented",
                    "rationale": "fab",
                    "evidence_ids": ["sha256:" + "0" * 64],
                }
                for kid in batch_b_ksis
            ],
            "unmapped_findings": [],
        }
    )
    stub = _PerBatchStubClient(
        responses=[
            _batch_response(batch_a_ksis),
            batch_b_bad,
            batch_b_bad,
            batch_b_bad,
            # No batch C in this test (only 10 indicators -> 2 batches)
        ]
    )
    with ProvenanceStore(tmp_path) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        report = agent.run(GapAgentInput(indicators=indicators, evidence=[]))
    # 1 call for batch A + 3 retries for batch B = 4 calls total.
    assert stub.call_count == 4
    # All 10 KSIs present in the report — batch B's graceful repair
    # downgraded the implemented->not_implemented but kept the entries.
    assert len(report.ksi_classifications) == 10
    by_id = {clf.ksi_id: clf for clf in report.ksi_classifications}
    for kid in batch_a_ksis:
        assert by_id[kid].status == "not_implemented"
    for kid in batch_b_ksis:
        # After graceful repair: status downgraded, evidence_ids stripped.
        assert by_id[kid].status == "not_implemented"
        assert by_id[kid].evidence_ids == []
        assert "[auto-repair:" in by_id[kid].rationale


def test_gap_agent_run_fills_omitted_ksi_with_placeholder(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """If the model returns only 3 of 5 batch indicators, the run() loop
    invokes fill_missing_classifications and adds placeholders for the
    omitted KSIs. Stderr carries a summary of every fill."""
    indicators = [_ind(f"KSI-W-{i:03d}") for i in range(5)]
    # Model only returns 3 of 5 — omits KSI-W-003 and KSI-W-004.
    incomplete_response = json.dumps(
        {
            "ksi_classifications": [
                {
                    "ksi_id": f"KSI-W-{i:03d}",
                    "status": "not_implemented",
                    "rationale": "x",
                    "evidence_ids": [],
                }
                for i in range(3)
            ],
            "unmapped_findings": [],
        }
    )
    stub = _PerBatchStubClient(responses=[incomplete_response])
    with ProvenanceStore(tmp_path) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        report = agent.run(GapAgentInput(indicators=indicators, evidence=[]))
    assert len(report.ksi_classifications) == 5
    by_id = {clf.ksi_id: clf for clf in report.ksi_classifications}
    assert "[auto-repair:" in by_id["KSI-W-003"].rationale
    assert "[auto-repair:" in by_id["KSI-W-004"].rationale
    err = capsys.readouterr().err
    assert "model omitted" in err


def test_gap_agent_run_emits_unmapped_findings_deterministically(
    tmp_path: Path,
) -> None:
    """Unmapped evidence shows up in the report via compute_unmapped_findings,
    NOT via the LLM. The LLM is never asked to enumerate unmapped findings
    in v0.1.143+."""
    a = _ind("KSI-A")
    mapped = _ev(ksis_evidenced=["KSI-A"], resource_name="mapped")
    unmapped1 = _ev(
        detector_id="aws.kms_key_rotation",
        ksis_evidenced=[],
        controls=["SC-12"],
        resource_name="u1",
    )
    unmapped2 = _ev(
        detector_id="github.action_pinning",
        ksis_evidenced=[],
        controls=["CM-2"],
        resource_name="u2",
    )
    response = json.dumps(
        {
            "ksi_classifications": [
                {
                    "ksi_id": "KSI-A",
                    "status": "partial",
                    "rationale": "ok",
                    "evidence_ids": [mapped.evidence_id],
                }
            ],
            "unmapped_findings": [],
        }
    )
    stub = _PerBatchStubClient(responses=[response])
    with ProvenanceStore(tmp_path) as store, active_store(store):
        # The mapped evidence has to exist in the store before the agent runs —
        # the citation validator checks every cited evidence_id resolves.
        for ev in [mapped, unmapped1, unmapped2]:
            store.write_record(
                payload=ev.model_dump(mode="json"),
                record_type="evidence",
                primitive=f"{ev.detector_id}@0.1.0",
            )
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        report = agent.run(GapAgentInput(indicators=[a], evidence=[mapped, unmapped1, unmapped2]))
    assert len(report.unmapped_findings) == 2
    # The deterministic note template embeds the detector_id as the second word.
    notes_combined = " ".join(f.note for f in report.unmapped_findings)
    assert "aws.kms_key_rotation" in notes_combined
    assert "github.action_pinning" in notes_combined
    # Confirm the LLM call's prompt did NOT include the unmapped section.
    assert "no KSI attribution (unmapped)" not in stub.last_messages[0].content


def test_gap_agent_run_does_not_send_unrelated_evidence_to_each_batch(
    tmp_path: Path,
) -> None:
    """The whole point of v0.1.143 — batch B's prompt must NOT carry batch A's
    evidence. Pre-v0.1.143 every call carried all evidence; post-v0.1.143
    each batch sees only its KSIs' evidence.

    Uses 6 indicators (5 in batch 1, 1 in batch 2 with the default
    batch_size_ksis=5) to force a batch boundary. Evidence A goes with
    batch 1's KSIs; evidence B goes with batch 2's KSI. Verifying batch
    2's prompt has only B's evidence is the load-bearing assertion.
    """
    # 5 KSIs that all attribute to evidence A go in batch 1; 1 KSI that
    # attributes to evidence B goes in batch 2.
    batch1_ksis = [_ind(f"KSI-A{i}") for i in range(5)]
    batch2_ksi = _ind("KSI-B")
    ev_a = _ev(
        ksis_evidenced=[f"KSI-A{i}" for i in range(5)],
        resource_name="resource_for_A",
    )
    ev_b = _ev(ksis_evidenced=["KSI-B"], resource_name="resource_for_B")
    stub = _PerBatchStubClient(
        responses=[
            _batch_response([f"KSI-A{i}" for i in range(5)]),
            _batch_response(["KSI-B"]),
        ]
    )
    with ProvenanceStore(tmp_path) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-haiku")  # type: ignore[arg-type]
        agent.run(GapAgentInput(indicators=[*batch1_ksis, batch2_ksi], evidence=[ev_a, ev_b]))
    # `last_messages` reflects the LAST (second) call — batch 2's prompt.
    second_batch_prompt = stub.last_messages[0].content
    assert "resource_for_B" in second_batch_prompt
    assert "resource_for_A" not in second_batch_prompt
