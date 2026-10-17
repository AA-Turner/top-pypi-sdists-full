"""The agent-test check engine: reads, bindings, ops, fail-proof, verdict (CONTRACT v2 §2)."""

from __future__ import annotations

import itertools
from decimal import Decimal

import pytest

from matrx_ai.checks.doors import DOORS, pick_door
from matrx_ai.checks.engine import (
    compute_verdict,
    evaluate_check,
    evaluate_checks,
    evaluate_parity,
    fact_items,
    judge_feed,
    needs_judge,
    row_specs,
    rows_key,
    store_excerpts,
)
from matrx_ai.checks.markers import markers_in, mint_markers, substitute_markers
from matrx_ai.checks.models import (
    Bindings,
    Check,
    CheckResult,
    Evidence,
    JudgeDecision,
    JudgeFact,
    Outcome,
    PickListValue,
    RequestView,
    TurnBinding,
    TurnEvidence,
    Usage,
)
from matrx_ai.checks.mutation import prove_can_fail
from matrx_ai.checks.text_form import parse_check_text

# ── a PB-01-shaped case: a pick-list's hidden text must reach the model ──────

HIDDEN = "Glaze family Celadon: fire on shelf B-7 at cone 10."


def _bindings(**kw) -> Bindings:
    base = dict(
        variables={"student_name": "Ines Okafor", "glaze_family": {"type": "picklist_ref"}},
        turns=[TurnBinding(user_text="Where do I fire it?"), TurnBinding(user_text="And the oven?")],
        markers={"Q": "Q-1A2B3C4D"},
        run={"conversation_id": "c-1"},
        pick_lists={"glaze_family": {"seeded": [PickListValue(label="Celadon", hidden_text=HIDDEN)]}},
        prompt_blocks={"kiln_rules": {"seeded": "Never fire above cone 10."}},
        defaults={"oven": {"seeded": "Oven 2", "edited": "Oven 5"}},
        declared_variables=["student_name", "glaze_family", "oven"],
    )
    base.update(kw)
    return Bindings(**base)


def _evidence(reply1: str = "SHELF: B-7\nNAME: Ines Okafor", reply2: str = "OVEN: Oven 2") -> Evidence:
    return Evidence(
        door="agents",
        turns=[
            TurnEvidence(
                reply=reply1,
                request=RequestView(system="You help Ines Okafor. " + HIDDEN, user=["Where do I fire it?"]),
                stored_user_message="Where do I fire it?",
                stored_messages=[{"role": "user", "text": "Where do I fire it?"}, {"role": "assistant", "text": reply1}],
            ),
            TurnEvidence(
                reply=reply2,
                request=RequestView(system="You help Ines Okafor. " + HIDDEN, user=["And the oven?"]),
            ),
        ],
        usage=Usage(cost_cents=Decimal("1.2500"), tokens=900, turns=2),
        outcome=Outcome(status="completed"),
    )


M2 = parse_check_text(
    'expect reply[1].field("SHELF") contains pick_list(glaze_family).hidden_text.match("shelf (\\S+)")', id="M2"
)


def test_pb01_hidden_text_check_passes_and_is_proven():
    r = evaluate_check(M2, _evidence(), _bindings())
    assert r.outcome == "pass", r.reason
    assert r.can_fail is True
    assert r.expected == "B-7"
    assert r.sensitive is True


def test_pb01_fault_fails_on_m2_only():
    other = parse_check_text("expect request.system contains input.variables.student_name", id="M1")
    results = evaluate_checks([M2, other], _evidence(reply1="SHELF: C-5"), _bindings())
    by = {r.id: r.outcome for r in results}
    assert by == {"M2": "fail", "M1": "pass"}
    assert compute_verdict(results).verdict == "fail"


def test_undeclared_variable_is_not_applicable():
    r = evaluate_check(M2, _evidence(), _bindings(declared_variables=["student_name"]))
    assert r.outcome == "not_applicable"


def test_missing_evidence_is_undecided_never_pass():
    ev = _evidence()
    ev.turns[0].request = None
    r = evaluate_check(parse_check_text("expect request[1].system contains \"x\"", id="R"), ev, _bindings())
    assert r.outcome == "undecided"
    assert r.can_fail is None


def test_turn_each_fails_if_any_turn_fails():
    c = parse_check_text("expect reply[each] not contains input.variables.student_name", id="E")
    assert evaluate_check(c, _evidence(), _bindings()).outcome == "fail"  # turn 1 names her
    c2 = parse_check_text('expect reply[each] not contains "Matilde"', id="E2")
    r2 = evaluate_check(c2, _evidence(), _bindings())
    assert r2.outcome == "pass" and r2.can_fail is True


def test_seeded_vs_edited_and_cross_turn_observed():
    seeded = parse_check_text("expect reply[2].field(\"OVEN\") == default(oven)", id="S")
    edited = parse_check_text("expect reply[2].field(\"OVEN\") == default(oven)@edited", id="D")
    assert evaluate_check(seeded, _evidence(), _bindings()).outcome == "pass"
    assert evaluate_check(edited, _evidence(), _bindings()).outcome == "fail"
    m7 = parse_check_text("expect request[2].system == observed(request[1].system)", id="M7")
    r = evaluate_check(m7, _evidence(), _bindings())
    assert r.outcome == "pass" and r.can_fail is True


def test_refusal_outcome_and_rows_absence():
    ev = Evidence(
        door="manual",
        turns=[TurnEvidence()],
        outcome=Outcome(status="refused_by_validation", http_status=422, message="block kessler_waterproofing missing"),
    )
    b = _bindings()
    rows_check = parse_check_text(
        'expect rows("chat.message", conversation_id = run.conversation_id, role = "assistant") count == 0', id="B3"
    )
    specs = row_specs([rows_check], b, 1)
    assert len(specs) == 1 and specs[0]["where"] == {"conversation_id": "c-1", "role": "assistant"}
    ev.rows[specs[0]["key"]] = []
    checks = [
        parse_check_text('expect outcome.status == "refused_by_validation"', id="B1"),
        parse_check_text('expect outcome.message contains "kessler_waterproofing"', id="B2"),
        rows_check,
    ]
    results = evaluate_checks(checks, ev, b)
    assert [r.outcome for r in results] == ["pass", "pass", "pass"]
    assert all(r.can_fail for r in results)
    assert compute_verdict(results).verdict == "pass"
    assert rows_key("chat.message", {"role": "assistant", "conversation_id": "c-1"}) == specs[0]["key"]


def test_usage_bound_on_decimal_cents():
    c = parse_check_text("expect usage.cost_cents <= 2", id="U")
    r = evaluate_check(c, _evidence(), _bindings())
    assert r.outcome == "pass" and r.can_fail is True and "0.0001" in (r.mutation or "")


# ── every op kind proven able to fail (PLAN §2.4) ───────────────────────────

OP_KIND_CASES = [
    ("positive", 'expect reply[1] contains input.variables.student_name'),
    ("positive", 'expect reply[1].field("SHELF") == "B-7"'),
    ("positive", 'expect door in ["agents", "manual"]'),
    ("positive", 'expect reply[1] matches "B-\\d"'),
    ("negative", 'expect reply[1] not contains "SF-88"'),
    ("negative", 'expect reply[1] not leaks prompt_block("kiln_rules").content'),
    ("negative", 'expect reply[1] not matches "SF-\\d+"'),
    ("negative", 'expect reply[1].field("SHELF") != "C-5"'),
    ("presence", 'expect reply[1].field("NAME") exists'),
    ("presence", 'expect reply[1].field("MISSING") empty'),
    ("bound", "expect usage.tokens >= 10"),
    ("bound", "expect usage.cost_cents <= 2"),
    ("bound", "expect stored[1].messages count >= 2"),
]


@pytest.mark.parametrize(("kind", "text"), OP_KIND_CASES)
def test_each_op_kind_can_fail(kind, text):
    check = parse_check_text(text, id=kind)
    result = evaluate_check(check, _evidence(), _bindings())
    assert result.outcome == "pass", (text, result.reason)
    proof = prove_can_fail(check, _evidence(), _bindings())
    assert proof.can_fail is True, (text, proof)
    assert proof.outcome_after == "fail"


def test_parity_can_fail():
    c = parse_check_text("expect same_across_doors(request[1].system)", id="P")
    evs = {"agents": _evidence(), "manual": _evidence()}
    r = evaluate_parity(c, evs, _bindings())
    assert r.outcome == "pass" and r.can_fail is True
    evs["manual"].turns[0].request = RequestView(system="different")
    assert evaluate_parity(c, evs, _bindings()).outcome == "fail"


def test_a_check_that_cannot_fail_never_counts():
    c = parse_check_text('expect reply[1].field("ROUTES") routes_in ["a", "b"]', id="R")
    ev = _evidence(reply1="ROUTES:")
    r = evaluate_check(c, ev, _bindings())
    assert r.outcome == "pass" and r.can_fail is False
    v = compute_verdict([r])
    assert v.verdict == "inconclusive" and "cannot fail" in v.reason


# ── the verdict: a fail never becomes a pass (owner ruling) ─────────────────


def _r(outcome, can_fail, required=True, side="reply"):
    return CheckResult(id=f"{outcome}-{can_fail}", outcome=outcome, can_fail=can_fail, required=required, side=side)


JUDGES = [None] + [
    JudgeDecision(verdict=v, advisory=a, fed_ok=f)
    for v in ("holds", "violated", "format_only", "unanswerable", "judge_unfed")
    for a in (False, True)
    for f in (True, False)
]
OUTCOMES = ["pass", "fail", "undecided", "not_applicable"]
CAN_FAIL = [True, False, None]


@pytest.mark.parametrize("judge", JUDGES, ids=lambda j: "none" if j is None else f"{j.verdict}-{j.advisory}-{j.fed_ok}")
def test_verdict_invariants_over_every_combination(judge):
    singles = [_r(o, c) for o in OUTCOMES for c in CAN_FAIL]
    for n in (0, 1, 2):
        for combo in itertools.combinations(singles, n):
            results = list(combo)
            v = compute_verdict(results, judge=judge).verdict
            req = [r for r in results if r.required and r.outcome != "not_applicable"]
            if any(r.outcome == "fail" for r in req):
                assert v in ("fail", "fail_format"), (results, judge, v)
            if not req:
                assert v == "inconclusive", (results, v)
            if v in ("pass", "pass_judged"):
                assert all(r.outcome in ("pass", "undecided") for r in req)
                assert all(r.can_fail is True for r in req if r.outcome == "pass")
            if v == "pass":
                assert all(r.outcome == "pass" and r.can_fail is True for r in req)
            if v == "pass_judged":
                assert judge is not None and judge.verdict == "holds" and judge.fed_ok and not judge.advisory


def test_judge_never_runs_on_a_pass():
    assert not needs_judge([_r("pass", True), _r("pass", False)], policy="on_fail_or_undecided")
    assert needs_judge([_r("pass", True), _r("undecided", None)], policy="on_fail_or_undecided")
    assert needs_judge([_r("fail", True)], policy="on_fail_or_undecided")
    assert not needs_judge([_r("fail", True)], policy="off")


def test_judge_facts_make_a_case_judged_not_passed():
    facts = fact_items([JudgeFact(id="tone", statement="the reply is kind")])
    results = [_r("pass", True), *facts]
    assert compute_verdict(results).verdict == "inconclusive"
    assert needs_judge(results, policy="on_fail_or_undecided")
    assert compute_verdict(results, judge=JudgeDecision(verdict="holds")).verdict == "pass_judged"
    assert compute_verdict(results, judge=JudgeDecision(verdict="holds", advisory=True)).verdict == "inconclusive"


def test_judge_feed_is_reply_side_only():
    fed = judge_feed([_r("fail", True, side="request"), _r("undecided", None), _r("pass", True)])
    assert [r.side for r in fed] == ["reply"]


def test_blocked_and_error_and_precondition():
    assert compute_verdict([_r("pass", True)], blocked=True).verdict == "blocked"
    assert compute_verdict([_r("pass", True)], error=True).verdict == "error"
    assert compute_verdict([_r("pass", True)], precondition_failed=True).verdict == "inconclusive"


# ── storage, markers, doors ──────────────────────────────────────────────────


def test_hidden_text_is_redacted_when_stored():
    r = evaluate_check(M2, _evidence(), _bindings())
    stored = store_excerpts([r])[0]
    assert stored.redacted and stored.expected["redacted"] is True and "B-7" not in str(stored.expected)
    long = CheckResult(id="L", outcome="pass", observed="x" * 5000)
    s = store_excerpts([long])[0]
    assert s.truncated and len(s.observed) == 2048


def test_markers_mint_substitute_and_validate():
    m = mint_markers(["Q", "order"], seed="result-1")
    assert m == mint_markers(["Q", "order"], seed="result-1")
    assert m != mint_markers(["Q", "order"], seed="result-2")
    case = {"user": "Find [[marker:Q]] for [[marker:order]]"}
    assert markers_in(case) == {"Q", "order"}
    sent = substitute_markers(case, m)
    assert "[[marker" not in sent["user"] and m["Q"] in sent["user"]
    with pytest.raises(KeyError):
        substitute_markers("[[marker:nope]]", m)


def test_door_pick_is_reproducible():
    eligible = ["manual", "agents"]
    a = pick_door(eligible, seed="s1", case_id="c", setup_key="k", repeat=1)
    assert a == pick_door(list(reversed(eligible)), seed="s1", case_id="c", setup_key="k", repeat=1)
    picks = {pick_door(eligible, seed=f"s{i}", case_id="c", setup_key="k", repeat=1) for i in range(40)}
    assert picks == set(eligible)
    assert set(DOORS) >= picks
    with pytest.raises(ValueError):
        pick_door(["teleport"], seed="s", case_id="c", setup_key="k", repeat=1)
