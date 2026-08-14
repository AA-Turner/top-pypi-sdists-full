"""k90 — oracle contracts: schema round-trips + the invariants that make the
contracts trustworthy (an ineligible view must explain itself, a passing
scorecard cannot carry a repair code, confidence stays in [0, 1]).

Run:
  cd /srv/share/projects/hugpy/dev/abstract_hugpy_dev
  ./venv/bin/python -m pytest tests/test_oracle_contracts.py -q
"""
from __future__ import annotations

import os
import sys

import pytest

_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from abstract_hugpy_dev.oracle.contracts import (  # noqa: E402
    ArtifactKind,
    ArtifactRef,
    BudgetHints,
    CapabilityView,
    Check,
    CheckKind,
    Eligibility,
    ExecutionReceipt,
    FailureClass,
    GoalSpec,
    InputKind,
    InputRef,
    JudgeResult,
    QualityProfile,
    RepairCode,
    ResourceHints,
    Scorecard,
    SourceRegistry,
)


# ---------------------------------------------------------------------------
# Round-trips: to_dict -> from_dict is lossless for every contract.
# ---------------------------------------------------------------------------


def test_goalspec_roundtrip():
    spec = GoalSpec(
        objective="transcribe the supplied clip and summarize it",
        raw_prompt="yo can you write down what they say in this and give me the gist",
        inputs=(InputRef(kind=InputKind.VIDEO, ref="/uploads/clip.mp4",
                         label="the clip"),),
        capability="audio.transcribe",
        quality=QualityProfile.BEST,
        budget=BudgetHints(max_seconds=120.0, max_vram_gb=8.0),
        acceptance=("every spoken line present", "no hallucinated words"),
    )
    again = GoalSpec.from_dict(spec.to_dict())
    assert again == spec
    # the raw prompt survives normalization verbatim
    assert again.raw_prompt == spec.raw_prompt


def test_goalspec_minimal_defaults():
    spec = GoalSpec(objective="summarize", raw_prompt="tl;dr this")
    assert spec.capability is None            # auto-capability
    assert spec.quality is QualityProfile.BALANCED
    assert GoalSpec.from_dict(spec.to_dict()) == spec


def test_capabilityview_roundtrip():
    view = CapabilityView(
        name="audio.transcribe",
        source=SourceRegistry.TASKS,
        accepts=(ArtifactKind.AUDIO, ArtifactKind.VIDEO),
        produces=(ArtifactKind.TEXT, ArtifactKind.JSON),
        model_ids=("whisper-large-v3-turbo",),
        eligibility=Eligibility(eligible=False,
                                reasons=("no online worker registered",)),
        resources=ResourceHints(min_vram_gb=4.0, frameworks=("transformers",),
                                notes="planning estimate"),
    )
    assert CapabilityView.from_dict(view.to_dict()) == view


def test_execution_receipt_roundtrip_and_request_normalization():
    req = {"prompt": "hello", "max_tokens": 64, "options": {"b": 2, "a": 1}}
    receipt = ExecutionReceipt(
        request=ExecutionReceipt.normalize_request(req),
        capability="text.chat",
        model_id="Qwen2.5-3B-Instruct-GGUF",
        worker="worker-a1",
        started_at="2026-08-05T12:00:00Z",
        ended_at="2026-08-05T12:00:03Z",
        duration_s=3.0,
        retries=1,
        failure=FailureClass.TIMEOUT,
        artifacts=(ArtifactRef(kind=ArtifactKind.TEXT, uri="/artifacts/out.txt",
                               sha256="ab" * 32),),
        warnings=("retried once",),
        log_excerpt=("worker timeout at 2.5s", "retry on worker-a1"),
    )
    again = ExecutionReceipt.from_dict(receipt.to_dict())
    assert again == receipt
    assert again.request_dict() == req
    # normalization is order-independent -> identical frozen value
    assert (ExecutionReceipt.normalize_request({"b": 1, "a": {"y": 2, "x": 1}})
            == ExecutionReceipt.normalize_request({"a": {"x": 1, "y": 2}, "b": 1}))


def test_scorecard_roundtrip():
    card = Scorecard(
        hard_pass=False,
        checks=(
            Check(name="decodes", kind=CheckKind.TECHNICAL, value=True,
                  threshold=None, passed=True),
            Check(name="duration_s", kind=CheckKind.TECHNICAL, value=1.2,
                  threshold=4.0, passed=False, detail="shot too short"),
        ),
        judge_results=(
            JudgeResult(judge="qwen-vl", verdict="fail", score=0.35,
                        rationale="requested action not visible"),
        ),
        confidence=0.7,
        disagreements=("technical pass vs judge fail on motion",),
        diagnosis="clip is 1.2s against a 4s minimum",
        repair_code=RepairCode.SHOT_TOO_SHORT,
        recommended_repair="regenerate the clip with min_frames raised",
    )
    assert Scorecard.from_dict(card.to_dict()) == card


# ---------------------------------------------------------------------------
# Invariants — structurally-invalid contracts are refused at construction.
# ---------------------------------------------------------------------------


def test_goalspec_requires_objective_and_raw_prompt():
    with pytest.raises(ValueError):
        GoalSpec(objective="", raw_prompt="x")
    with pytest.raises(ValueError):
        GoalSpec(objective="x", raw_prompt="   ")


def test_goalspec_capability_must_be_namespaced():
    with pytest.raises(ValueError):
        GoalSpec(objective="x", raw_prompt="x", capability="transcribe")


def test_budget_hints_must_be_positive():
    with pytest.raises(ValueError):
        BudgetHints(max_seconds=0)
    with pytest.raises(ValueError):
        BudgetHints(max_vram_gb=-1)


def test_ineligible_without_reasons_is_refused():
    with pytest.raises(ValueError):
        Eligibility(eligible=False, reasons=())
    # eligible with advisory reasons is fine
    Eligibility(eligible=True, reasons=("no online worker; central serves it",))


def test_capabilityview_name_must_be_namespaced_and_produce_something():
    ok = dict(source=SourceRegistry.TASKS, accepts=(ArtifactKind.TEXT,),
              produces=(ArtifactKind.TEXT,), model_ids=(),
              eligibility=Eligibility(eligible=True))
    with pytest.raises(ValueError):
        CapabilityView(name="chat", **ok)
    with pytest.raises(ValueError):
        CapabilityView(name="text.chat", **{**ok, "produces": ()})


def test_receipt_rejects_negative_duration_and_retries():
    base = dict(request=(), capability="text.chat", model_id="m", worker=None,
                started_at="t0", ended_at="t1")
    with pytest.raises(ValueError):
        ExecutionReceipt(duration_s=-0.1, **base)
    with pytest.raises(ValueError):
        ExecutionReceipt(duration_s=0.0, retries=-1, **base)


def test_scorecard_confidence_bounds():
    with pytest.raises(ValueError):
        Scorecard(hard_pass=True, confidence=1.5)
    with pytest.raises(ValueError):
        Scorecard(hard_pass=True, confidence=-0.01)


def test_scorecard_pass_cannot_carry_repair_code():
    with pytest.raises(ValueError):
        Scorecard(hard_pass=True, repair_code=RepairCode.IDENTITY_DRIFT)


def test_repair_code_vocabulary_is_complete():
    expected = {
        "identity_drift", "action_missing", "voice_similarity_low",
        "line_omitted", "shot_too_short", "lip_sync_out_of_range",
        "temporal_artifact", "intent_mismatch", "source_authority_missing",
        "decode_failed", "empty_output", "format_mismatch", "timeout",
        "worker_unavailable", "capability_gap",
    }
    assert {c.value for c in RepairCode} == expected


def test_contracts_serialize_to_plain_json():
    import json
    card = Scorecard(hard_pass=True, checks=(
        Check(name="decodes", kind=CheckKind.TECHNICAL, value=True,
              threshold=None, passed=True),))
    # every to_dict must be json.dumps-able with no custom encoder
    json.dumps(card.to_dict())
    json.dumps(GoalSpec(objective="x", raw_prompt="x").to_dict())
    json.dumps(CapabilityView(
        name="text.chat", source=SourceRegistry.TASKS,
        accepts=(ArtifactKind.TEXT,), produces=(ArtifactKind.TEXT,),
        model_ids=("m",), eligibility=Eligibility(eligible=True)).to_dict())
