"""The panel's pure logic, pinned to the doctrines it exists to keep.

The expensive failure here is a confident zero or a silent cut: a wave that
drops tracked questions without saying so, or a cost that ignores lanes and
repeats, reads as "we measured everything" when it did not.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from matrx_seo.ai_visibility_panel import (
    FALLBACK_COST_PER_PROMPT_ENGINE,
    KeyMessage,
    PanelPrompt,
    estimate_panel_cost,
    max_prompts_per_panel,
    message_presence,
    plan_wave,
    select_prompts,
)
from matrx_seo.providers.dataforseo.ai_answers import build_ai_answer_task


def _cell(key: str, partition: str, **extra) -> PanelPrompt:
    return PanelPrompt(
        key=key,
        text=f"question {key}",
        candidate_id=key,
        canonical_cell_id=f"cell-{key}",
        partition=partition,
        **extra,
    )


class TestLegacyPromptStaysValid:
    def test_a_hand_typed_prompt_reads_as_unclassified_human_written(self) -> None:
        legacy = PanelPrompt.model_validate(
            {"key": "p1", "text": "best crm for law firms", "intent": "comparison"}
        )
        assert not legacy.is_classified
        assert legacy.effective_transformation == "human_written"
        assert legacy.slot_id == "unclassified:p1"

    def test_enum_codes_are_checked_against_the_design_contract(self) -> None:
        with pytest.raises(ValidationError):
            _cell("x", "tracked")  # display name, not the contract code
        with pytest.raises(ValidationError):
            _cell("x", "core", lane_eligibility=["web"])
        assert _cell("x", "core", aided_status="unaided").is_classified


class TestNoWebLane:
    def test_the_no_web_task_turns_web_search_off_and_sends_no_location(self) -> None:
        task = build_ai_answer_task(
            prompt="Which CRM?",
            engine="chat_gpt",
            country_iso="US",
            city="Austin",
            web_search=False,
        )
        assert task["web_search"] is False
        assert "web_search_country_iso_code" not in task
        assert "web_search_city" not in task

    def test_the_default_stays_web_search_on_with_location(self) -> None:
        task = build_ai_answer_task(prompt="Which CRM?", engine="chat_gpt", city="Austin")
        assert task["web_search"] is True
        assert task["web_search_country_iso_code"] == "US"
        assert task["web_search_city"] == "Austin"


class TestMaxPromptsPerTier:
    def test_the_cap_comes_from_the_tier_table(self) -> None:
        assert max_prompts_per_panel("diagnostic") == 48 * 2
        assert max_prompts_per_panel("standard") == 120 * 2
        assert max_prompts_per_panel("campaign") == (40 + 40) * 2
        assert max_prompts_per_panel(None) == max_prompts_per_panel("diagnostic")
        assert max_prompts_per_panel("nonsense") == max_prompts_per_panel("diagnostic")


class TestKeyMessagePresence:
    def test_a_term_fires_on_word_boundaries_only(self) -> None:
        message = KeyMessage(key="no-code", label="We are no-code", terms=["no code", "no-code"])
        present = message_presence("It is a no-code builder for experts.", [message])
        assert present[0].present
        assert present[0].matched_terms == ["no-code"]

    def test_a_substring_inside_another_word_does_not_fire(self) -> None:
        message = KeyMessage(key="no-code", label="We are no-code", terms=["no code"])
        assert not message_presence("no coders were required", [message])[0].present

    def test_absence_reports_no_evidence_rather_than_a_guess(self) -> None:
        message = KeyMessage(key="fast", label="We are fast", terms=["fastest"])
        result = message_presence("A capable platform.", [message])[0]
        assert not result.present
        assert result.matched_terms == []


class TestPanelCost:
    def test_a_measured_price_beats_the_fallback_and_says_so(self) -> None:
        est = estimate_panel_cost(
            prompts=[PanelPrompt(key=f"p{i}", text=f"question {i}") for i in range(4)],
            engines=["chat_gpt", "claude", "perplexity"],
            measured_cost_per_call=Decimal("0.05"),
            analyst_sampling="none",
        )
        assert est.calls == 12
        assert est.estimated_cost_usd == Decimal("0.6000")
        assert est.measured
        assert "your own" in est.basis

    def test_no_history_falls_back_and_admits_it(self) -> None:
        est = estimate_panel_cost(
            prompts=[PanelPrompt(key="p", text="question p")], engines=["chat_gpt"]
        )
        assert not est.measured
        assert est.cost_per_call_usd == FALLBACK_COST_PER_PROMPT_ENGINE
        assert "no measured runs" in est.basis

    def test_an_empty_panel_costs_nothing(self) -> None:
        est = estimate_panel_cost(prompts=[], engines=["chat_gpt", "claude"])
        assert est.estimated_cost_usd == Decimal("0.0000")

    def test_lanes_and_repeats_multiply_and_eligibility_is_honoured(self) -> None:
        prompts = [
            _cell("a", "core"),  # both lanes
            _cell("b", "core", lane_eligibility=["retrieval"]),  # web only
        ]
        est = estimate_panel_cost(
            prompts=prompts,
            engines=["chat_gpt", "gemini"],
            lanes=["retrieval", "closed_model"],
            repeats=3,
            analyst_sampling="first_repeat",
        )
        # a: 2 lanes × 2 engines × 3; b: 1 lane × 2 engines × 3
        assert est.calls == 12 + 6
        assert est.calls_by_lane == {"retrieval": 12, "closed_model": 6}
        # first repeat only: (2 + 1 lanes) × 2 engines
        assert est.analyst_calls == 6
        assert est.estimated_cost_usd == (
            FALLBACK_COST_PER_PROMPT_ENGINE * 18 + FALLBACK_COST_PER_PROMPT_ENGINE * 6
        ).quantize(Decimal("0.0001"))

    def test_a_lane_with_no_api_runner_is_announced_not_priced(self) -> None:
        est = estimate_panel_cost(
            prompts=[_cell("a", "core")],
            engines=["chat_gpt"],
            lanes=["retrieval", "consumer_surface"],
            analyst_sampling="none",
        )
        assert est.calls == 1
        assert any("consumer_surface" in n for n in est.notices)


class TestSetAwareSelection:
    def test_every_wave_sets_always_run_and_only_discovery_rotates(self) -> None:
        prompts = [
            _cell("c1", "core"),
            _cell("s1", "sentinel"),
            _cell("k1", "control"),
            _cell("a1", "aided", aided_status="target_aided"),
            *[_cell(f"r{i}", "rotating") for i in range(5)],
        ]
        measured = {"c1": datetime(2026, 9, 20, tzinfo=UTC)}  # measured recently
        schedule = select_prompts(prompts, max_per_run=6, last_measured=measured)
        keys = [p.key for p in schedule.running]
        assert keys[:4] == ["c1", "s1", "k1", "a1"]
        assert len(keys) == 6
        assert not schedule.partial and schedule.shortfall == 0
        assert schedule.shortfall_detail is None
        assert [p.key for p in schedule.deferred] == ["r2", "r3", "r4"]

    def test_a_budget_below_the_fixed_sets_is_an_explicit_partial_wave(self) -> None:
        prompts = [_cell(f"c{i}", "core") for i in range(3)] + [_cell("r0", "rotating")]
        schedule = select_prompts(prompts, max_per_run=2)
        assert schedule.partial
        assert schedule.fixed_total == 3
        assert schedule.shortfall == 1
        assert "partial" in (schedule.shortfall_detail or "")
        assert [p.key for p in schedule.running] == ["c0", "c1"]
        assert [p.key for p in schedule.deferred] == ["c2", "r0"]

    def test_legacy_prompts_rotate_like_the_discovery_set(self) -> None:
        prompts = [_cell("c0", "core"), PanelPrompt(key="old", text="old question")]
        schedule = select_prompts(prompts, max_per_run=1)
        assert [p.key for p in schedule.running] == ["c0"]
        assert [p.key for p in schedule.deferred] == ["old"]
        assert not schedule.partial


class TestSeededWaveOrder:
    def _prompts(self) -> list[PanelPrompt]:
        return [_cell(f"q{i}", "core") for i in range(6)]

    def test_the_same_seed_reproduces_the_same_order(self) -> None:
        one = plan_wave(
            self._prompts(), lanes=["retrieval", "closed_model"], repeats=3, order_seed=42
        )
        two = plan_wave(
            list(reversed(self._prompts())),
            lanes=["retrieval", "closed_model"],
            repeats=3,
            order_seed=42,
        )
        assert one.cells == two.cells
        assert len(one.cells) == 6 * 2 * 3

    def test_a_different_seed_changes_the_order_but_not_the_cells(self) -> None:
        one = plan_wave(
            self._prompts(), lanes=["retrieval", "closed_model"], repeats=3, order_seed=1
        )
        two = plan_wave(
            self._prompts(), lanes=["retrieval", "closed_model"], repeats=3, order_seed=2
        )
        as_set = lambda plan: {(c.prompt_key, c.lane, c.repeat_index) for c in plan.cells}  # noqa: E731
        assert as_set(one) == as_set(two)
        assert [c.prompt_key for c in one.cells] != [c.prompt_key for c in two.cells]

    def test_lane_eligibility_limits_the_cells_and_unrunnable_is_announced(self) -> None:
        prompts = [
            _cell("w", "core", lane_eligibility=["retrieval"]),
            _cell("app", "core", lane_eligibility=["consumer_surface"]),
        ]
        plan = plan_wave(prompts, lanes=["retrieval", "closed_model"], repeats=2, order_seed=3)
        assert {(c.prompt_key, c.lane) for c in plan.cells} == {("w", "retrieval")}
        assert plan.skipped == ["app"]
        assert plan.notices


class TestPromptRotation:
    def _prompts(self, n: int) -> list[PanelPrompt]:
        return [PanelPrompt(key=f"p{i}", text=f"question {i}") for i in range(n)]

    def test_the_cap_defers_rather_than_drops(self) -> None:
        schedule = select_prompts(self._prompts(5), max_per_run=2)
        assert len(schedule.running) == 2
        assert len(schedule.deferred) == 3

    def test_never_measured_prompts_run_before_measured_ones(self) -> None:
        prompts = self._prompts(3)
        schedule = select_prompts(
            prompts,
            max_per_run=1,
            last_measured={
                "p0": datetime(2026, 8, 15, tzinfo=UTC),
                "p1": datetime(2026, 8, 14, tzinfo=UTC),
            },
        )
        assert [p.key for p in schedule.running] == ["p2"]

    def test_the_oldest_measurement_goes_first(self) -> None:
        prompts = self._prompts(2)
        schedule = select_prompts(
            prompts,
            max_per_run=1,
            last_measured={
                "p0": datetime(2026, 8, 15, tzinfo=UTC),
                "p1": datetime(2026, 8, 1, tzinfo=UTC),
            },
        )
        assert [p.key for p in schedule.running] == ["p1"]

    def test_a_big_panel_covers_itself_over_successive_passes(self) -> None:
        """The point of rotation: the tail is never permanently dark."""
        prompts = self._prompts(6)
        measured: dict[str, datetime] = {}
        covered: set[str] = set()
        for pass_no in range(3):
            schedule = select_prompts(prompts, max_per_run=2, last_measured=measured)
            for prompt in schedule.running:
                covered.add(prompt.key)
                measured[prompt.key] = datetime(2026, 8, 10 + pass_no, tzinfo=UTC)
        assert covered == {p.key for p in prompts}
