"""Speech pace — the ONE answer to "how many words make how many seconds".

A stated length ("a two-minute explainer") becomes a word target from one pace,
owned in one place: the setting ``speech / pace_wpm`` (words per minute,
org-overridable, seeded 150 by aidream on 2026-10-07). Nothing else may carry a
words-per-minute number — not a prompt, not a provider module, not a node.

The package never reads the database. The host installs its per-organization
reader once at boot (``set_speech_pace_resolver``); standalone, the pace is
:data:`STANDALONE_SPEECH_PACE_WPM` and every answer says so in ``source``.

Consumers:
  * ``speech.budget`` (the workflow step) — duration → word target + band.
  * the podcast code path (``/podcast/generate``) — same function, same target.
  * the Google TTS segmenter — a segment's character window from seconds.

Design: ``common-docs/systems/workflows/projects/response-checks-and-revisions/DESIGN.md`` §6.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

#: The setting's address in ``platform.feature_knob``.
SPEECH_PACE_KNOB: tuple[str, str] = ("speech", "pace_wpm")
#: The standalone (no-host) posture only — hosted, the setting is the value.
STANDALONE_SPEECH_PACE_WPM = 150
#: The setting's own bounds (its row carries the same min/max); a value outside
#: them is a broken setting, never a pace.
MIN_PACE_WPM = 80
MAX_PACE_WPM = 250
#: Average written English word incl. the following space. A property of text,
#: not an opinion — used only to turn seconds into a character window.
AVERAGE_CHARS_PER_WORD = 5.5
#: The tolerance a length target carries: ±20% absorbs abbreviations, numbers
#: read aloud and pauses (DESIGN.md §6, self-attack 4).
BUDGET_BAND = 0.2

SOURCE_SETTING = "setting speech/pace_wpm"
SOURCE_STANDALONE = "standalone"

#: ``async (organization_id) -> words per minute``.
SpeechPaceResolver = Callable[[str | None], Awaitable[int]]

_RESOLVER: SpeechPaceResolver | None = None


def set_speech_pace_resolver(resolver: SpeechPaceResolver | None) -> None:
    """Install the host's per-organization pace reader (``None`` = standalone)."""
    global _RESOLVER
    _RESOLVER = resolver


def get_speech_pace_resolver() -> SpeechPaceResolver | None:
    return _RESOLVER


@dataclass(frozen=True, slots=True)
class SpeechPace:
    wpm: int
    source: str


@dataclass(frozen=True, slots=True)
class SpeechBudget:
    target_duration_seconds: int
    target_word_count: int
    band_min: int
    band_max: int
    wpm: int
    pace_source: str


async def speech_pace(*, organization_id: str | None) -> SpeechPace:
    """The pace one organization's speech runs at. Raises on a setting out of range."""
    if _RESOLVER is None:
        return SpeechPace(wpm=STANDALONE_SPEECH_PACE_WPM, source=SOURCE_STANDALONE)
    wpm = int(await _RESOLVER(organization_id))
    if not MIN_PACE_WPM <= wpm <= MAX_PACE_WPM:
        raise ValueError(
            f"The speaking pace setting {'/'.join(SPEECH_PACE_KNOB)} is {wpm} words per "
            f"minute, outside {MIN_PACE_WPM}–{MAX_PACE_WPM}. Correct the setting."
        )
    return SpeechPace(wpm=wpm, source=SOURCE_SETTING)


def words_for_seconds(seconds: float, wpm: int) -> int:
    return round(seconds * wpm / 60)


def chars_for_seconds(seconds: float, wpm: int) -> int:
    return round(words_for_seconds(seconds, wpm) * AVERAGE_CHARS_PER_WORD)


def budget_for_seconds(seconds: int, pace: SpeechPace) -> SpeechBudget:
    """A duration → the word target a writer is given and the band a check accepts."""
    if seconds <= 0:
        raise ValueError(f"A speech duration must be positive, got {seconds} seconds.")
    words = words_for_seconds(seconds, pace.wpm)
    return SpeechBudget(
        target_duration_seconds=seconds,
        target_word_count=words,
        band_min=round(words * (1 - BUDGET_BAND)),
        band_max=round(words * (1 + BUDGET_BAND)),
        wpm=pace.wpm,
        pace_source=pace.source,
    )


async def speech_budget(seconds: int, *, organization_id: str | None) -> SpeechBudget:
    """The one call every consumer makes: resolve the pace, then the budget."""
    return budget_for_seconds(seconds, await speech_pace(organization_id=organization_id))
