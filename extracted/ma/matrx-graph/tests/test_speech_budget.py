"""Speech pace → word target: the resolver and the ``speech.budget`` node.

A stated duration becomes a word target from ONE pace answer (the
``speech/pace_wpm`` setting, injected by the host), never from a number a
writer or a prompt guesses. "Two minutes" at 150 wpm is 300 words, band
240–360 — the figure the podcast script writers receive.
"""

from __future__ import annotations

import pytest

from matrx_graph import speech_pace as sp
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.nodes.speech.budget import (
    SpeechBudgetConfig,
    SpeechBudgetExecutor,
    SpeechBudgetInput,
)
from matrx_graph.types.result import Failure, Success


@pytest.fixture(autouse=True)
def _no_host_resolver():
    previous = sp.get_speech_pace_resolver()
    sp.set_speech_pace_resolver(None)
    yield
    sp.set_speech_pace_resolver(previous)


def test_words_for_seconds_is_pace_times_minutes() -> None:
    assert sp.words_for_seconds(120, 150) == 300
    assert sp.words_for_seconds(60, 150) == 150
    assert sp.words_for_seconds(90, 140) == 210


def test_budget_carries_a_twenty_percent_band() -> None:
    budget = sp.budget_for_seconds(120, sp.SpeechPace(wpm=150, source="test"))
    assert budget.target_word_count == 300
    assert budget.target_duration_seconds == 120
    assert (budget.band_min, budget.band_max) == (240, 360)
    assert budget.wpm == 150
    assert budget.pace_source == "test"


def test_budget_refuses_a_non_positive_duration() -> None:
    with pytest.raises(ValueError):
        sp.budget_for_seconds(0, sp.SpeechPace(wpm=150, source="test"))


def test_chars_for_seconds_matches_the_old_tts_window() -> None:
    # The Google 3.1-flash TTS cap was a hand-derived 750 chars ("~150 wpm /
    # ~5.5 chars per word"); 55 s at 150 wpm lands on the same window.
    assert 740 <= sp.chars_for_seconds(55, 150) <= 760


async def test_standalone_pace_is_announced_not_silent() -> None:
    pace = await sp.speech_pace(organization_id=None)
    assert pace.wpm == sp.STANDALONE_SPEECH_PACE_WPM == 150
    assert pace.source == "standalone"


async def test_host_resolver_is_the_pace() -> None:
    seen: list[str | None] = []

    async def resolver(organization_id: str | None) -> int:
        seen.append(organization_id)
        return 120

    sp.set_speech_pace_resolver(resolver)
    pace = await sp.speech_pace(organization_id="org-1")
    assert pace.wpm == 120
    assert pace.source == "setting speech/pace_wpm"
    assert seen == ["org-1"]


async def test_host_resolver_out_of_range_is_refused() -> None:
    async def resolver(organization_id: str | None) -> int:
        return 0

    sp.set_speech_pace_resolver(resolver)
    with pytest.raises(ValueError):
        await sp.speech_pace(organization_id="org-1")


class _App:
    organization_id = "org-9"


class _Ctx:
    app = _App()
    organization_id = "org-9"


async def test_node_turns_two_minutes_into_three_hundred_words() -> None:
    result = await SpeechBudgetExecutor().execute(
        _Ctx(),  # type: ignore[arg-type]
        SpeechBudgetInput(target_seconds=120, language="english"),
        SpeechBudgetConfig(),
    )
    assert isinstance(result, Success)
    out = result.result
    assert out.target_word_count == 300
    assert out.target_duration_seconds == 120
    assert (out.band_min, out.band_max) == (240, 360)
    assert out.language == "english"


async def test_node_accepts_the_form_string_value() -> None:
    result = await SpeechBudgetExecutor().execute(
        _Ctx(),  # type: ignore[arg-type]
        SpeechBudgetInput(target_seconds="180"),
        SpeechBudgetConfig(),
    )
    assert isinstance(result, Success)
    assert result.result.target_word_count == 450


async def test_node_fails_loudly_on_a_bad_duration() -> None:
    result = await SpeechBudgetExecutor().execute(
        _Ctx(),  # type: ignore[arg-type]
        SpeechBudgetInput(target_seconds="soon"),
        SpeechBudgetConfig(),
    )
    assert isinstance(result, Failure)


async def test_node_reads_the_organizations_pace() -> None:
    async def resolver(organization_id: str | None) -> int:
        assert organization_id == "org-9"
        return 200

    sp.set_speech_pace_resolver(resolver)
    result = await SpeechBudgetExecutor().execute(
        _Ctx(),  # type: ignore[arg-type]
        SpeechBudgetInput(target_seconds=60),
        SpeechBudgetConfig(),
    )
    assert isinstance(result, Success)
    assert result.result.target_word_count == 200
    assert result.result.pace_source == "setting speech/pace_wpm"


def test_node_is_registered_as_a_builtin() -> None:
    registry = register_builtin_nodes(overwrite=True)
    assert registry.get("speech.budget") is not None
