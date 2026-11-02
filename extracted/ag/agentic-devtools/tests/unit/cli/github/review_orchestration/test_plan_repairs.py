import pytest

from agentic_devtools.cli.github.review_orchestration import RunState, plan_repairs


def plan(data, **kwargs):
    return plan_repairs(
        RunState.model_validate(data), observed_head="a" * 40, observed_fingerprint="b" * 64, now=1000, **kwargs
    )


def test_ready_is_not_merge_readiness(state_data):
    result = plan(state_data)
    assert result.status == "ready"
    assert len(result.batches) == 1
    assert result.next_due_at == 1300
    assert not result.invalidate_evidence


@pytest.mark.parametrize("field,value", [("observed_head", "c" * 40), ("observed_fingerprint", "d" * 64)])
def test_changed_head_or_fingerprint_invalidates_cached_evidence(state_data, field, value):
    kwargs = {"observed_head": "a" * 40, "observed_fingerprint": "b" * 64, "now": 1000, field: value}
    result = plan_repairs(RunState.model_validate(state_data), **kwargs)
    assert result.status == "waiting"
    assert result.invalidate_evidence
    assert not result.batches


@pytest.mark.parametrize(
    "field,value",
    [
        ("observed_head", None),
        ("observed_fingerprint", None),
        ("observed_head", "short"),
        ("observed_fingerprint", "short"),
        ("now", True),
        ("now", -1),
    ],
)
def test_invalid_observation_fails_explicitly(state_data, field, value):
    kwargs = {"observed_head": "a" * 40, "observed_fingerprint": "b" * 64, "now": 1000, field: value}
    with pytest.raises(ValueError):
        plan_repairs(RunState.model_validate(state_data), **kwargs)


@pytest.mark.parametrize("surface", ["reviews", "threads", "checks", "tasks"])
@pytest.mark.parametrize("completeness", ["unknown", "incomplete"])
def test_incomplete_is_not_zero(state_data, surface, completeness):
    state_data["findings"] = []
    state_data["evidence"][surface] = completeness
    result = plan(state_data)
    assert result.status == "waiting"
    assert "incomplete" in result.reason
    assert not result.batches


@pytest.mark.parametrize(
    "updates,reason",
    [
        ({"reviewer_id": 99}, "CCR"),
        ({"review_id": None}, "CCR"),
        ({"reviewed_head_sha": None}, "CCR"),
        ({"reviewed_head_sha": "c" * 40}, "CCR"),
    ],
)
def test_requires_exact_ccr_review_correlation(state_data, updates, reason):
    state_data["evidence"].update(updates)
    assert reason in plan(state_data).reason
    assert not plan(state_data).batches


def test_rejects_finding_from_another_review(state_data):
    state_data["findings"][0]["review_id"] = 18
    assert plan(state_data).status == "blocked"
    state_data["findings"][0].update(review_id=17, reviewer_id=99)
    assert plan(state_data).status == "blocked"


@pytest.mark.parametrize("status", ["blocked", "budget_exhausted", "closed", "merged"])
def test_terminal_outcomes_do_not_dispatch(state_data, status):
    state_data["status"] = status
    assert plan(state_data).status == status
    assert not plan(state_data).batches


def test_budget_due_and_authorization_guards(state_data):
    state_data["cycles"] = 12
    assert plan(state_data).status == "ready"
    state_data["cycles"] = 13
    assert plan(state_data).status == "budget_exhausted"
    state_data["cycles"] = 0
    result = plan_repairs(
        RunState.model_validate(state_data), observed_head="a" * 40, observed_fingerprint="b" * 64, now=4600
    )
    assert result.status == "budget_exhausted"
    state_data["next_due_at"] = 1300
    assert plan(state_data).next_due_at == 1300
    assert not plan(state_data).batches
    state_data["next_due_at"] = 1000
    state_data["authorized_actions"] = []
    assert plan(state_data).status == "blocked"


@pytest.mark.parametrize(
    "retry_class,count,status",
    [
        ("throttling", 3, "budget_exhausted"),
        ("transport", 3, "budget_exhausted"),
        ("repair", 2, "budget_exhausted"),
        ("credential", 1, "blocked"),
        ("oauth", 1, "blocked"),
    ],
)
def test_independent_failure_budgets(state_data, retry_class, count, status):
    state_data["failures"][retry_class] = count
    assert plan(state_data).status == status


@pytest.mark.parametrize(
    "retry_class,count,status",
    [
        ("throttling", 3, "budget_exhausted"),
        ("transport", 3, "budget_exhausted"),
        ("repair", 2, "budget_exhausted"),
        ("credential", 1, "blocked"),
        ("oauth", 1, "blocked"),
    ],
)
@pytest.mark.parametrize("waiting_guard", ["future_tick", "incomplete_evidence"])
def test_terminal_failures_precede_waiting_guards(state_data, retry_class, count, status, waiting_guard):
    state_data["failures"][retry_class] = count
    if waiting_guard == "future_tick":
        state_data["next_due_at"] = 1300
    else:
        state_data["evidence"]["reviews"] = "incomplete"
    assert plan(state_data).status == status


def test_does_not_redispatch_resolved_delivered_or_unknown_acceptance(reserve, state_data):
    state_data["findings"][0]["status"] = "resolved"
    assert not plan(state_data).batches
    state_data = reserve("delivered")
    assert not plan(state_data).batches
    state_data = reserve("acceptance_unknown")
    assert plan(state_data).status == "blocked"
    assert "acceptance" in plan(state_data).reason
    assert not plan(state_data).batches


def test_same_file_supporting_test_and_branch_writes_serialize(state_data):
    first = state_data["findings"][0]
    state_data["findings"].append({**first, "comment_id": 24, "path": "other.py"})
    assert list(map(len, plan(state_data).batches)) == [1, 1]
    for finding in state_data["findings"]:
        finding["side_effects"] = []
    assert list(map(len, plan(state_data).batches)) == [1, 1]
    state_data["findings"][1].update(path=r"SRC\Example.py", supporting_files=[])
    assert list(map(len, plan(state_data).batches)) == [1, 1]


def test_disjoint_batches_are_deterministic_and_bounded(state_data):
    first = state_data["findings"][0]
    state_data["findings"] = [
        {**first, "comment_id": n, "path": f"src/{n}.py", "supporting_files": [], "side_effects": []}
        for n in range(1, 6)
    ]
    original = plan(state_data).batches
    assert list(map(len, original)) == [2, 2, 1]
    state_data["findings"].reverse()
    assert plan(state_data).batches == original


def test_active_reservations_block_only_conflicting_candidates(reserve):
    state_data = reserve()
    first = state_data["findings"][0]
    other = {**first, "status": "pending", "comment_id": 24, "attempt_id": None, "task_id": None, "session_id": None}
    state_data["findings"].append(other)
    assert not plan(state_data).batches
    other.update(path="other.py", supporting_files=[], side_effects=[])
    assert len(plan(state_data).batches[0]) == 1
    state_data["max_parallel"] = 1
    result = plan(state_data)
    assert result.status == "waiting"
    assert not result.batches
    assert "slots" in result.reason


def test_stale_reservation_head_is_not_released(reserve):
    state_data = reserve()
    state_data["reservations"][0]["head_sha"] = "c" * 40
    assert plan(state_data).status == "blocked"
    assert "reservation" in plan(state_data).reason


def test_complete_empty_findings_wait_for_separate_readiness_gate(state_data):
    state_data["findings"] = []
    result = plan(state_data)
    assert result.status == "waiting"
    assert result.reason == "no pending repairs; use the separate review-readiness gate"


def test_active_reservations_without_pending_repairs_keep_waiting(reserve):
    result = plan(reserve())
    assert result.status == "waiting"
    assert "active reservations" in result.reason


def test_blocked_findings_without_pending_repairs_do_not_reach_readiness_gate(reserve):
    result = plan(reserve("blocked"))
    assert result.status == "blocked"
    assert "blocked" in result.reason


def test_review_request_in_flight_prevents_repair_race(state_data):
    state_data["review_requested_head"] = "a" * 40
    assert plan(state_data).status == "waiting"
    assert not plan(state_data).batches
