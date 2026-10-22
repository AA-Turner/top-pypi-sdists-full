"""A provider's plan cap ("usage_limit_reached", "do not retry automatically") is never asked again, even when its words
also say "try again later". Live 2026-10-21: one capped Notion query was sent three times."""

from __future__ import annotations

from matrx_ai.tools import mcp_resilience as r

CAPPED = ('{"code":"usage_limit_reached","message":"You have reached the query limit for this workspace. '
          'Try again later. Do not retry automatically."}')


def test_a_plan_cap_reply_is_not_a_stumble():
    assert r.classify_reply(CAPPED) is None


def test_a_plan_cap_raised_is_not_a_stumble():
    assert r.classify(RuntimeError(CAPPED)) is None


def test_a_real_try_again_later_is_still_a_stumble():
    assert r.classify_reply("Service temporarily unavailable, try again later") == r.NO_ANSWER
