"""THE condense decision (``context_trim.decide_condense``): when a conversation's older turns
become one summary. Arman, 2026-10-24: the major condense fires where the next send would cross the
conversation's cap (200,000 today: the lower of the model's window and the input cap resolved for
the person and organization), never at a fixed earlier number — "that makes it such that we start
losing conversations far too early" (about the 120,000 trigger). Earlier condensing is a separate,
named level behind its own switch, off by default. Boundaries pinned."""

from __future__ import annotations

import pytest

from matrx_ai.config.context_trim import (
    CONDENSE_KNOB_KEYS,
    CONDENSE_LEVELS,
    CachePrices,
    CondensePolicy,
    condense_policy_from_knobs,
    decide_condense,
    payback_pays,
)

POLICY = CondensePolicy(
    next_turn_reserve_tokens=20_000,
    keep_recent_tokens=30_000,
    summary_target_tokens=4_000,
    min_saved_tokens=5_000,
)
CAP = 200_000
WINDOW_1M = 1_000_000


def test_the_fixed_120k_trigger_is_retired_a_person_chat_keeps_its_turns_to_the_cap() -> None:
    """Red before: a 1M-window chat with the 200,000 cap was condensed at 120,000."""
    d = decide_condense(
        estimated_prompt_tokens=120_000, policy=POLICY, model_window_tokens=WINDOW_1M, window_ceiling_tokens=CAP
    )
    assert (d.condense, d.rule) == (False, "below_cap"), d.to_snapshot()
    assert "condense_trigger_tokens" not in CONDENSE_KNOB_KEYS
    assert not hasattr(CondensePolicy(), "trigger_tokens")


def test_at_turn_end_it_fires_when_the_next_send_would_cross_the_cap() -> None:
    held = decide_condense(
        estimated_prompt_tokens=179_999, policy=POLICY, model_window_tokens=WINDOW_1M, window_ceiling_tokens=CAP
    )
    taken = decide_condense(
        estimated_prompt_tokens=180_000, policy=POLICY, model_window_tokens=WINDOW_1M, window_ceiling_tokens=CAP
    )
    assert (held.condense, held.trigger_tokens, held.cap_tokens) == (False, 180_000, CAP)
    assert (taken.condense, taken.rule, taken.level) == (True, "at_cap", "at_cap")
    assert taken.est_freed_tokens == 180_000 - 30_000 - 4_000


def test_at_the_send_it_fires_only_over_the_cap() -> None:
    """The last line: a send that would exceed the cap is condensed first (no reserve)."""
    under = decide_condense(
        estimated_prompt_tokens=199_000, policy=POLICY, window_ceiling_tokens=CAP, at_send=True
    )
    over = decide_condense(
        estimated_prompt_tokens=200_001, policy=POLICY, window_ceiling_tokens=CAP, at_send=True
    )
    assert (under.condense, under.trigger_tokens, under.reserve_tokens) == (False, CAP, 0)
    assert (over.condense, over.rule) == (True, "over_cap")


def test_a_higher_cap_for_a_person_or_organization_moves_the_condense() -> None:
    d = decide_condense(
        estimated_prompt_tokens=300_000, policy=POLICY, model_window_tokens=WINDOW_1M, window_ceiling_tokens=500_000
    )
    assert (d.condense, d.trigger_tokens) == (False, 480_000)


def test_a_small_window_model_is_capped_by_its_own_window() -> None:
    held = decide_condense(
        estimated_prompt_tokens=107_999, policy=POLICY, model_window_tokens=128_000, window_ceiling_tokens=CAP
    )
    taken = decide_condense(
        estimated_prompt_tokens=108_000, policy=POLICY, model_window_tokens=128_000, window_ceiling_tokens=CAP
    )
    assert (held.condense, held.cap_tokens, held.trigger_tokens) == (False, 128_000, 108_000)
    assert (taken.condense, taken.rule) == (True, "at_cap")


def test_a_reserve_larger_than_the_window_never_condenses_every_turn() -> None:
    d = decide_condense(estimated_prompt_tokens=3_000, policy=POLICY, model_window_tokens=16_000)
    assert d.trigger_tokens == 8_000 and d.condense is False


def test_no_cap_known_and_level_one_off_holds() -> None:
    d = decide_condense(estimated_prompt_tokens=900_000, policy=POLICY)
    assert (d.condense, d.rule, d.cap_tokens) == (False, "no_cap", None)


def test_a_condense_that_frees_too_little_never_breaks_the_cache() -> None:
    small_cap = 60_000  # trigger 40,000
    taken = decide_condense(estimated_prompt_tokens=40_000, policy=POLICY, window_ceiling_tokens=small_cap)
    assert taken.condense is True  # frees 6,000 >= 5,000
    refused = decide_condense(
        estimated_prompt_tokens=40_000, policy=POLICY, window_ceiling_tokens=small_cap, condensable_tokens=8_999
    )
    assert (refused.condense, refused.rule) == (False, "too_little_to_free")  # frees 4,999


def test_the_knob_reader_refuses_a_missing_key() -> None:
    values = {k: 1 for k in CONDENSE_KNOB_KEYS}
    with pytest.raises(KeyError):
        condense_policy_from_knobs(values)  # the two shared trim keys are missing
    values.update(cache_gate_min_saved_tokens=5_000)
    with pytest.raises(KeyError):
        condense_policy_from_knobs(values)  # the payback horizon is shared with the trim gate too
    values.update(payback_expected_remaining_calls=20, condense_early_payback_enabled=False)
    policy = condense_policy_from_knobs(values)
    assert policy.source == "org_knobs" and policy.expected_remaining_calls == 20
    assert policy.early_payback_enabled is False


def test_the_levels_are_named_in_order() -> None:
    assert CONDENSE_LEVELS == ("tool_output_trim", "early_payback", "at_cap")


# ── LEVEL 1, EARLY PAYBACK: its own switch, off by default; the trim gate's rule when on ──

#: Opus-class prices, USD per million tokens: cache read, cache write (5m), fresh input.
OPUS = CachePrices(read_price=0.5, write_price=6.25, input_price=5.0)
EARLY = CondensePolicy(
    next_turn_reserve_tokens=20_000,
    early_payback_enabled=True,
    keep_recent_tokens=30_000,
    summary_target_tokens=4_000,
    min_saved_tokens=5_000,
)


def test_level_one_is_off_by_default_even_when_it_would_pay_back() -> None:
    """Red before: with prices resolving, the payback rule condensed below the cap by default."""
    assert CondensePolicy().early_payback_enabled is False
    d = decide_condense(
        estimated_prompt_tokens=110_000, policy=POLICY, model_window_tokens=WINDOW_1M,
        window_ceiling_tokens=CAP, prices=OPUS,
    )
    assert (d.condense, d.rule, d.level) == (False, "below_cap", None)


def test_level_one_on_a_condense_that_pays_back_is_taken() -> None:
    # 110K, 20 more calls: frees 76K x $0.5 x 20 = $0.76 vs a 34K rewrite x $5.75 + the condenser
    # reading 110K x $5 = $0.75 -> pays.
    d = decide_condense(
        estimated_prompt_tokens=110_000, policy=EARLY, model_window_tokens=WINDOW_1M,
        window_ceiling_tokens=CAP, prices=OPUS,
    )
    assert (d.condense, d.rule, d.level) == (True, "early_payback", "early_payback"), d.to_snapshot()
    assert d.benefit_usd is not None and d.cost_usd is not None and d.benefit_usd >= d.cost_usd


def test_level_one_on_a_condense_that_does_not_pay_back_is_held() -> None:
    d = decide_condense(
        estimated_prompt_tokens=60_000, policy=EARLY, model_window_tokens=WINDOW_1M,
        window_ceiling_tokens=CAP, prices=OPUS,
    )
    assert (d.condense, d.rule) == (False, "early_payback_hold"), d.to_snapshot()


def test_level_one_unpriced_holds_and_the_cap_still_forces() -> None:
    held = decide_condense(
        estimated_prompt_tokens=110_000, policy=EARLY, model_window_tokens=WINDOW_1M, window_ceiling_tokens=CAP
    )
    assert (held.condense, held.rule) == (False, "below_cap")
    forced = decide_condense(
        estimated_prompt_tokens=185_000, policy=EARLY, model_window_tokens=WINDOW_1M,
        window_ceiling_tokens=CAP, prices=OPUS,
    )
    assert (forced.condense, forced.rule) == (True, "at_cap")


def test_the_payback_rule_is_the_trim_gates_rule() -> None:
    assert payback_pays(freed_tokens=1000, rewrite_tokens=1000, read_price=1.0, write_price=2.0, expected_remaining_calls=1)[0]
    assert not payback_pays(freed_tokens=999, rewrite_tokens=1000, read_price=1.0, write_price=2.0, expected_remaining_calls=1)[0]


def test_a_large_fixed_prefix_is_not_condensable_and_never_buys_a_condense_every_few_turns() -> None:
    """Only the history is condensable. 100k of system prompt + tools + template beside 90k of
    history at the 180k turn-end trigger: the remainder would still be at the trigger."""
    d = decide_condense(
        estimated_prompt_tokens=190_000, policy=POLICY, window_ceiling_tokens=CAP, fixed_prefix_tokens=180_000
    )
    assert d.condense is False and d.rule == "too_little_to_free" and d.est_freed_tokens == 0
    # The core's split says what a condense would replace: 20k of history frees 16k, but 174k
    # would remain — at the 180k trigger? no: below it, so it is taken; 10k frees too little.
    d = decide_condense(estimated_prompt_tokens=190_000, policy=POLICY, window_ceiling_tokens=CAP, condensable_tokens=8_000)
    assert d.condense is False and d.rule == "too_little_to_free"
    d = decide_condense(estimated_prompt_tokens=195_000, policy=POLICY, window_ceiling_tokens=CAP, condensable_tokens=12_000)
    assert d.condense is False and d.rule == "remainder_at_cap"
    # Past the cap itself, any condense that frees enough is needed to fit.
    d = decide_condense(estimated_prompt_tokens=205_000, policy=POLICY, window_ceiling_tokens=CAP, condensable_tokens=12_000)
    assert (d.condense, d.rule) == (True, "over_cap")
    # A condense that clears the trigger is taken.
    d = decide_condense(estimated_prompt_tokens=190_000, policy=POLICY, window_ceiling_tokens=CAP, condensable_tokens=60_000)
    assert d.condense is True and d.est_freed_tokens == 56_000
