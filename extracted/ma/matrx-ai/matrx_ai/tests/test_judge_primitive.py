"""Forcing functions for the Judge primitive — contract, D-15, Selector, kappa.

Every test here pins a rule that, if it broke, would break silently: a judge
would keep returning verdicts, they would just stop meaning anything. No DB and
no LLM — the paid path is proven by `scripts/_verify_judge_primitive.py`.
"""

from __future__ import annotations

import pytest

from matrx_ai.evaluators import (
    COMPARATIVE_VERDICTS,
    EntityRef,
    Judge,
    JudgeContract,
    JudgeContractError,
    JudgeOutcome,
    JudgeSubject,
    Selector,
)
from matrx_ai.evaluators.calibration import LabeledCase, calibrate, cohens_kappa
from matrx_ai.evaluators.judge import _assert_rubric_isolation
from matrx_ai.evaluators.ledger import verdict_payload

RUBRIC = (
    "Rank the subject against the reference on correctness and completeness. "
    "Never reward verbosity; formatting-only differences are 'same'."
)


def _comparative(**overrides) -> JudgeContract:
    base = {
        "key": "test.judge",
        "question": "Is the subject better than the reference?",
        "mode": "comparative",
        "subject_kind": "test_answer",
        "rubric_name": "test.v1",
        "rubric": RUBRIC,
        "rubric_provenance": "H",
        "rubric_author": "arman@armansadeghi.com",
    }
    return JudgeContract(**{**base, **overrides})


# ── The contract ────────────────────────────────────────────────────────────


def test_rubric_mode_without_a_named_rubric_is_refused_at_construction() -> None:
    """D-14: absolute scoring is only ever allowed against a NAMED rubric."""
    with pytest.raises(JudgeContractError, match="rubric mode requires"):
        JudgeContract(key="k", question="q", mode="rubric", subject_kind="s")
    with pytest.raises(JudgeContractError):
        JudgeContract(
            key="k", question="q", mode="rubric", subject_kind="s", rubric_name="named"
        )  # named but empty


def test_rubric_mode_with_a_named_rubric_is_accepted() -> None:
    contract = JudgeContract(
        key="k",
        question="q",
        mode="rubric",
        subject_kind="s",
        rubric_name="named",
        rubric=RUBRIC,
        verdict_values=("pass", "fail"),
    )
    assert contract.mode == "rubric"


def test_empty_verdict_vocabulary_is_refused() -> None:
    with pytest.raises(JudgeContractError, match="verdict_values"):
        _comparative(verdict_values=())


def test_contract_is_frozen_so_a_version_cannot_drift_under_its_ledger_rows() -> None:
    contract = _comparative()
    with pytest.raises(Exception):  # pydantic frozen
        contract.version = 2  # type: ignore[misc]


def test_rubric_fingerprint_changes_with_the_rubric_and_is_none_without_one() -> None:
    a = _comparative()
    b = _comparative(rubric=RUBRIC + " Also: cite evidence.")
    assert a.rubric_fingerprint != b.rubric_fingerprint
    assert JudgeContract(
        key="k", question="q", mode="comparative", subject_kind="s"
    ).rubric_fingerprint is None


# ── D-15 ────────────────────────────────────────────────────────────────────


def test_d15_subject_that_authored_the_rubric_is_refused() -> None:
    contract = _comparative(rubric_author_ref=EntityRef(ref_type="agent", ref_id="A"))
    with pytest.raises(JudgeContractError, match="never author or see"):
        contract.assert_not_self_authored(EntityRef(ref_type="agent", ref_id="A"))


def test_d15_a_different_subject_is_allowed() -> None:
    contract = _comparative(rubric_author_ref=EntityRef(ref_type="agent", ref_id="A"))
    contract.assert_not_self_authored(EntityRef(ref_type="agent", ref_id="B"))


def test_d15_rubric_text_inside_the_subject_is_refused() -> None:
    """The realistic way this rule dies: a caller pastes the grading criteria
    into the agent's own prompt, handing the judged unit its answer key."""
    contract = _comparative()
    with pytest.raises(JudgeContractError, match="never see the rubric"):
        _assert_rubric_isolation(
            contract, JudgeSubject(label="subject", content="My instructions: " + RUBRIC)
        )


def test_d15_also_checks_the_reference_not_only_the_subject() -> None:
    contract = _comparative()
    with pytest.raises(JudgeContractError):
        _assert_rubric_isolation(
            contract,
            JudgeSubject(label="subject", content="clean"),
            JudgeSubject(label="reference", content="leaked: " + RUBRIC),
        )


def test_d15_isolation_does_not_false_positive_on_unrelated_content() -> None:
    _assert_rubric_isolation(
        _comparative(), JudgeSubject(label="subject", content="An index speeds up reads.")
    )


# ── Mode enforcement ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_score_is_refused_on_a_comparative_contract() -> None:
    judge = Judge(_comparative())
    with pytest.raises(JudgeContractError, match="requires mode='rubric'"):
        await judge.score(JudgeSubject(label="s", content="x"), ledger=False)


@pytest.mark.asyncio
async def test_compare_is_refused_on_a_rubric_contract() -> None:
    judge = Judge(
        JudgeContract(
            key="k",
            question="q",
            mode="rubric",
            subject_kind="s",
            rubric_name="n",
            rubric=RUBRIC,
            verdict_values=("pass", "fail"),
        )
    )
    with pytest.raises(JudgeContractError, match="requires mode='comparative'"):
        await judge.compare(
            JudgeSubject(label="s", content="x"),
            JudgeSubject(label="r", content="y"),
            ledger=False,
        )


# ── Selector ────────────────────────────────────────────────────────────────


def test_selector_refuses_a_rubric_mode_contract_by_construction() -> None:
    """There is no absolute-score path into the Selector. That IS the
    specialization (VISION §3.6)."""
    contract = JudgeContract(
        key="k",
        question="q",
        mode="rubric",
        subject_kind="s",
        rubric_name="n",
        rubric=RUBRIC,
        verdict_values=("pass", "fail"),
    )
    with pytest.raises(JudgeContractError, match="picks by COMPARISON"):
        Selector(contract)


@pytest.mark.asyncio
async def test_selector_refuses_an_empty_candidate_list() -> None:
    with pytest.raises(JudgeContractError, match="candidate list is empty"):
        await Selector(_comparative()).select([])


@pytest.mark.asyncio
async def test_selector_keeps_the_incumbent_on_same_and_unseats_on_better(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A tie must NOT churn the champion — otherwise candidate ORDER decides
    the winner more than quality does."""
    contract = _comparative()
    selector = Selector(contract)
    scripted = iter(["same", "better", "worse"])

    async def fake_compare(subject, reference, **kwargs):  # noqa: ANN001, ANN003
        return JudgeOutcome(
            verdict=next(scripted),
            confidence=0.9,
            reasoning="scripted",
            judge_key=contract.key,
            judge_version=contract.version,
            mode="comparative",
        )

    async def no_ledger(*args, **kwargs):  # noqa: ANN002, ANN003
        return None

    monkeypatch.setattr(selector._judge, "compare", fake_compare)  # noqa: SLF001
    monkeypatch.setattr(selector, "_record", no_ledger)

    candidates = [JudgeSubject(label=name, content=name) for name in ("a", "b", "c", "d")]
    result = await selector.select(candidates)

    # b ties a -> a holds; c beats a -> c champion; d loses to c -> c holds.
    assert result.winner_label == "c"
    assert [c.verdict for c in result.comparisons] == ["same", "better", "worse"]


# ── The ledger payload ──────────────────────────────────────────────────────


def test_verdict_payload_carries_the_judge_identity_and_rubric_provenance() -> None:
    """The deferred-write shape used by a mirror-contained replay. If a field
    silently vanishes here, the accuracy record loses the very thing that makes
    it attributable."""
    contract = _comparative()
    payload = verdict_payload(
        contract=contract,
        subject=JudgeSubject(label="s", content="x", ref=EntityRef(ref_type="t", ref_id="1")),
        reference=JudgeSubject(label="r", content="y", ref=EntityRef(ref_type="t", ref_id="2")),
        outcome=JudgeOutcome(
            verdict="worse",
            confidence=0.7,
            reasoning="because",
            judge_key=contract.key,
            judge_version=contract.version,
            mode="comparative",
        ),
        invocation={"runner": "slot", "model": "m"},
        organization_id="org",
        user_id="user",
    )
    assert payload["judge_key"] == contract.key
    assert payload["judge_version"] == contract.version
    assert payload["subject_ref_id"] == "1"
    assert payload["reference_ref_id"] == "2"
    assert payload["rubric_fingerprint"] == contract.rubric_fingerprint
    assert payload["rubric_provenance"] == "H"
    assert payload["rubric_author"] == "arman@armansadeghi.com"
    assert payload["organization_id"] == "org"
    assert payload["verdict"] == "worse"


# ── Calibration ─────────────────────────────────────────────────────────────


def test_cohens_kappa_matches_the_textbook_worked_example() -> None:
    cases = (
        [LabeledCase(judge_verdict="a", authority_verdict="a")] * 20
        + [LabeledCase(judge_verdict="b", authority_verdict="b")] * 15
        + [LabeledCase(judge_verdict="a", authority_verdict="b")] * 5
        + [LabeledCase(judge_verdict="b", authority_verdict="a")] * 10
    )
    po, kappa = cohens_kappa(cases)
    assert po == pytest.approx(0.7)
    assert kappa == pytest.approx(0.4)


def test_kappa_is_none_not_one_when_both_raters_used_a_single_identical_label() -> None:
    """Perfect agreement with no variance carries no information. Reporting
    1.0 here would be the single most misleading thing this can do."""
    cases = [LabeledCase(judge_verdict="better", authority_verdict="better")] * 80
    po, kappa = cohens_kappa(cases)
    assert po == 1.0
    assert kappa is None
    assert calibrate(cases, judge_key="k").band == "insufficient_data"


def test_bands_only_apply_above_the_minimum_case_count() -> None:
    strong = [LabeledCase(judge_verdict="a", authority_verdict="a")] * 20 + [
        LabeledCase(judge_verdict="b", authority_verdict="b")
    ] * 20
    assert calibrate(strong, judge_key="k").band == "insufficient_data"

    big = strong * 2 + [LabeledCase(judge_verdict="a", authority_verdict="b")]
    assert calibrate(big, judge_key="k").band == "production"


def test_confusion_matrix_names_the_direction_of_error() -> None:
    cases = [LabeledCase(judge_verdict="better", authority_verdict="worse")] * 3
    result = calibrate(cases, judge_key="k")
    assert result.confusion == {"better": {"worse": 3}}


def test_no_cases_reports_nothing_rather_than_zero() -> None:
    result = calibrate([], judge_key="k")
    assert result.cases == 0
    assert result.raw_agreement is None
    assert result.cohens_kappa is None
    assert result.band == "insufficient_data"


def test_default_comparative_vocabulary_is_an_enumeration_not_a_scale() -> None:
    assert COMPARATIVE_VERDICTS == ("better", "same", "worse", "regressed")
    assert all(isinstance(v, str) for v in COMPARATIVE_VERDICTS)
