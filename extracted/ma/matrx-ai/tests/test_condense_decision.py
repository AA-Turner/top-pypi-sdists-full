"""THE condense decision (``context_trim.decide_condense``): when a conversation's older turns
become one summary. Boundaries pinned; the same numbers as the trim gate's near-limit rule."""

from __future__ import annotations

import pytest

from matrx_ai.config.context_trim import (
    CONDENSE_KNOB_KEYS,
    CachePrices,
    CondensePolicy,
    condense_policy_from_knobs,
    decide_condense,
    payback_pays,
)

POLICY = CondensePolicy(
    trigger_tokens=120_000,
    keep_recent_tokens=30_000,
    summary_target_tokens=4_000,
    min_saved_tokens=5_000,
    force_window_percent=85,
)


def test_one_token_under_the_trigger_holds() -> None:
    d = decide_condense(estimated_prompt_tokens=119_999, policy=POLICY, model_window_tokens=1_000_000)
    assert (d.condense, d.rule, d.trigger_tokens) == (False, "below_trigger", 120_000)


def test_at_the_trigger_condenses_even_on_a_1m_model() -> None:
    # The 9b224bf5 case: a 1M declared window must not let a chat grow past the product limit.
    d = decide_condense(estimated_prompt_tokens=120_000, policy=POLICY, model_window_tokens=1_000_000)
    assert (d.condense, d.rule) == (True, "at_trigger")
    assert d.est_freed_tokens == 120_000 - 30_000 - 4_000


def test_a_small_window_model_condenses_before_its_own_limit() -> None:
    # 100K window x 85% = 85,000 < the 120,000 knob: the window decides, and it is "near the limit".
    held = decide_condense(estimated_prompt_tokens=84_999, policy=POLICY, model_window_tokens=100_000)
    taken = decide_condense(estimated_prompt_tokens=85_000, policy=POLICY, model_window_tokens=100_000)
    assert (held.condense, held.trigger_tokens) == (False, 85_000)
    assert (taken.condense, taken.rule) == (True, "forced_near_limit")


def test_a_platform_window_ceiling_caps_the_declared_window() -> None:
    d = decide_condense(
        estimated_prompt_tokens=110_000,
        policy=CondensePolicy(trigger_tokens=500_000, keep_recent_tokens=30_000, summary_target_tokens=4_000),
        model_window_tokens=1_000_000,
        window_ceiling_tokens=128_000,
    )
    assert d.effective_window_tokens == 128_000
    assert d.trigger_tokens == int(128_000 * 0.85)
    assert (d.condense, d.rule) == (True, "forced_near_limit")


def test_an_unknown_window_uses_the_knob_trigger_alone() -> None:
    d = decide_condense(estimated_prompt_tokens=120_000, policy=POLICY, model_window_tokens=None)
    assert (d.condense, d.effective_window_tokens, d.trigger_tokens) == (True, None, 120_000)


def test_a_condense_that_frees_too_little_never_breaks_the_cache() -> None:
    policy = CondensePolicy(
        trigger_tokens=40_000, keep_recent_tokens=30_000, summary_target_tokens=4_000, min_saved_tokens=5_000
    )
    held = decide_condense(estimated_prompt_tokens=39_999, policy=policy)
    assert held.condense is False and held.rule == "below_trigger"
    small = decide_condense(estimated_prompt_tokens=40_000, policy=policy)  # frees 6,000 >= 5,000
    assert small.condense is True
    tight = CondensePolicy(
        trigger_tokens=36_000, keep_recent_tokens=30_000, summary_target_tokens=4_000, min_saved_tokens=5_000
    )
    refused = decide_condense(estimated_prompt_tokens=38_999, policy=tight)  # frees 4,999
    assert (refused.condense, refused.rule) == (False, "too_little_to_free")


def test_the_knob_reader_refuses_a_missing_key() -> None:
    values = {k: 1 for k in CONDENSE_KNOB_KEYS}
    with pytest.raises(KeyError):
        condense_policy_from_knobs(values)  # the two shared trim keys are missing
    values.update(cache_gate_min_saved_tokens=5_000, payback_force_window_percent=85)
    with pytest.raises(KeyError):
        condense_policy_from_knobs(values)  # the payback horizon is shared with the trim gate too
    values.update(payback_expected_remaining_calls=20)
    policy = condense_policy_from_knobs(values)
    assert policy.source == "org_knobs" and policy.expected_remaining_calls == 20


# ── THE PAYBACK ECONOMICS (review 2026-10-22, B10): the trim gate's rule, not a fixed trigger ──

#: Opus-class prices, USD per million tokens: cache read, cache write (5m), fresh input.
OPUS = CachePrices(read_price=0.5, write_price=6.25, input_price=5.0)


def test_below_the_ceiling_a_condense_that_pays_back_is_taken() -> None:
    # 110K, 20 more calls: frees 76K x $0.5 x 20 = $0.76 vs a 34K rewrite x $5.75 + the condenser
    # reading 110K x $5 = $0.75 -> pays.
    d = decide_condense(estimated_prompt_tokens=110_000, policy=POLICY, model_window_tokens=1_000_000, prices=OPUS)
    assert (d.condense, d.rule) == (True, "payback"), d.to_snapshot()
    assert d.benefit_usd is not None and d.cost_usd is not None and d.benefit_usd >= d.cost_usd


def test_below_the_ceiling_a_condense_that_does_not_pay_back_is_held() -> None:
    d = decide_condense(estimated_prompt_tokens=60_000, policy=POLICY, model_window_tokens=1_000_000, prices=OPUS)
    assert (d.condense, d.rule) == (False, "payback_hold"), d.to_snapshot()


def test_the_payback_rule_is_the_trim_gates_rule() -> None:
    assert payback_pays(freed_tokens=1000, rewrite_tokens=1000, read_price=1.0, write_price=2.0, expected_remaining_calls=1)[0]
    assert not payback_pays(freed_tokens=999, rewrite_tokens=1000, read_price=1.0, write_price=2.0, expected_remaining_calls=1)[0]


def test_unpriced_below_the_ceiling_holds_and_the_ceiling_still_forces() -> None:
    held = decide_condense(estimated_prompt_tokens=110_000, policy=POLICY, model_window_tokens=1_000_000)
    assert (held.condense, held.rule) == (False, "below_trigger")
    forced = decide_condense(estimated_prompt_tokens=125_000, policy=POLICY, model_window_tokens=1_000_000, prices=OPUS)
    assert (forced.condense, forced.rule) == (True, "at_trigger")


def test_the_hosts_per_call_budget_caps_the_window() -> None:
    # An automated turn's host cap (200,000) is the ceiling a 1M model must stay under.
    d = decide_condense(
        estimated_prompt_tokens=171_000,
        policy=CondensePolicy(trigger_tokens=500_000, keep_recent_tokens=30_000, summary_target_tokens=4_000),
        model_window_tokens=1_000_000,
        window_ceiling_tokens=200_000,
    )
    assert (d.condense, d.rule, d.effective_window_tokens) == (True, "forced_near_limit", 200_000)


def test_a_large_fixed_prefix_is_not_condensable_and_never_buys_a_condense_every_few_turns() -> None:
    """Only the history is condensable. 100k of system prompt + tools + template beside 34k of
    history at a 120k trigger: the old estimate (everything minus keep) freed 100k and condensed
    every time the prompt crossed the trigger; the remainder is still at the trigger either way."""
    policy = CondensePolicy()
    d = decide_condense(estimated_prompt_tokens=134_000, policy=policy, fixed_prefix_tokens=100_000)
    assert d.condense is False and d.rule == "too_little_to_free" and d.est_freed_tokens == 0
    # The core's split says what a condense would replace: 20k of history frees 16k, but
    # 118k would remain at a 110k trigger — no paid condense that leaves it at the trigger.
    tight = CondensePolicy(trigger_tokens=110_000)
    d = decide_condense(estimated_prompt_tokens=134_000, policy=tight, condensable_tokens=20_000)
    assert d.condense is False and d.rule == "remainder_at_trigger"
    # Past the effective window itself, any condense that frees enough is needed to fit.
    d = decide_condense(
        estimated_prompt_tokens=134_000, policy=tight, condensable_tokens=20_000, window_ceiling_tokens=130_000
    )
    assert d.condense is True
    # A condense that clears the trigger is taken.
    d = decide_condense(estimated_prompt_tokens=134_000, policy=policy, condensable_tokens=60_000)
    assert d.condense is True and d.est_freed_tokens == 56_000
