# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""How one `--read-timeout` is split between a comparison's two reads and its report."""

from __future__ import annotations

import pytest

from airbyte_ops_mcp.regression_tests import read_budget
from airbyte_ops_mcp.regression_tests.read_budget import ReadBudget, report_reserve_s

pytestmark = pytest.mark.unit


class _FakeClock:
    """A monotonic clock that moves only when the test moves it."""

    def __init__(self) -> None:
        self.now = 1_000.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> _FakeClock:
    fake = _FakeClock()
    monkeypatch.setattr(read_budget, "monotonic", fake)
    return fake


@pytest.mark.parametrize(
    ("budget_s", "reserve_s"),
    [
        pytest.param(14_400, 600, id="runner-default"),
        pytest.param(10_200, 600, id="workflow-170-minutes"),
        pytest.param(6_000, 600, id="a-tenth-is-exactly-ten-minutes"),
        pytest.param(3_000, 300, id="small-budget-keeps-a-tenth"),
        pytest.param(9, 0, id="tiny-budget-keeps-nothing"),
        pytest.param(0, 0, id="never-below-zero"),
    ],
)
def test_the_reserve_is_ten_minutes_or_a_tenth_of_a_smaller_budget(
    budget_s: int, reserve_s: int
) -> None:
    assert report_reserve_s(budget_s) == reserve_s


def test_the_workflow_budget_gives_the_control_96_minutes_and_the_target_64(
    clock: _FakeClock,
) -> None:
    budget = ReadBudget.start(170 * 60)

    assert budget.control_share_s() == 96 * 60
    clock.advance(96 * 60)  # the control reads to the end of its share
    assert budget.target_share_s() == 64 * 60


def test_a_control_that_finishes_early_leaves_the_target_the_rest(
    clock: _FakeClock,
) -> None:
    budget = ReadBudget.start(170 * 60)

    clock.advance(10 * 60)

    assert budget.target_share_s() == 150 * 60


def test_setup_before_the_control_is_charged_to_the_budget(clock: _FakeClock) -> None:
    budget = ReadBudget.start(170 * 60)

    clock.advance(20 * 60)  # building and pulling images, fetching the config

    assert budget.control_share_s() == 84 * 60  # 60% of the 140 minutes left


def test_a_small_budget_is_split_the_same_way(clock: _FakeClock) -> None:
    budget = ReadBudget.start(300)

    assert budget.reserve_s == 30
    assert budget.control_share_s() == 162
    clock.advance(162)
    assert budget.target_share_s() == 108


@pytest.mark.parametrize("budget_s", [1, 59, 300, 600, 10_200, 14_400])
def test_both_shares_and_the_reserve_fit_inside_the_budget(
    clock: _FakeClock, budget_s: int
) -> None:
    budget = ReadBudget.start(budget_s)

    control_s = budget.control_share_s()
    clock.advance(control_s)
    target_s = budget.target_share_s()

    assert control_s >= 0
    assert target_s >= 0
    assert control_s + target_s + budget.reserve_s <= budget_s


def test_a_target_with_no_time_left_gets_zero_never_a_negative_share(
    clock: _FakeClock,
) -> None:
    budget = ReadBudget.start(600)

    clock.advance(budget.control_share_s())
    clock.advance(300)  # parsing the control's output ran into the reserve

    assert budget.target_share_s() == 0
    clock.advance(10_000)
    assert budget.target_share_s() == 0
    assert budget.control_share_s() == 0
