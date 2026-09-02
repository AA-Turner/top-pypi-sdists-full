"""THE EQUIVALENCE LAW — a setting converts to the target's nearest equivalent;
it is dropped ONLY when the target genuinely has no equivalent.

> Arman, 2026-08-17: *"I should be able to call any model, from any provider,
> with configurations from any other model and any other provider in any random
> way I want, and every single configuration should properly convert and get
> properly applied without anything being dropped or lost — unless it's an
> additive configuration offering something that the given new model does not
> support."*

That is the product's number-one selling point, and until this module existed
the engine did the opposite by DEFAULT: ``ControlRule.on_unmapped`` defaulted to
``"drop"``, and 135 of the 135 live rules carrying a ``value_map`` took that
default. Measured on the live catalog, 1,132 (value × model) combinations were
discarded rather than converted — ask for ``21:9`` on a model whose map lists
only ``16:9``/``1:1`` and you did not get 16:9, you got the model's *default*,
announced by one yellow line in a server log.

WHY A REGISTRY AND NOT ONE "NEAREST". The old ``nearest`` resolved by position
in ``ai.setting.canonical_values``. That is right for an ordered SCALE
(``low < medium < high``) and wrong — sometimes destructively — for everything
else: ``21:9`` is nearest ``16:9`` by geometry, not by list position, and
``alloy`` has no nearest to ``kore`` at all, because a voice is an identity, not
a degree. Converting incorrectly is its own violation of the law, so each
setting declares HOW equivalence is measured, and a setting with no declared
metric returns ``None`` — which the caller reports as a loud drop rather than
inventing an answer.

ADDING A SETTING: give it a metric here. A setting that reaches production with
no metric and a ``value_map`` will drop values; `scripts/check_catalog_vocabulary.py`
is what makes that visible.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

# ── ordered scales ───────────────────────────────────────────────────────────
# Settings whose ai.setting.canonical_values IS a monotonic scale, so position
# in that list is a true distance. Membership is a CLAIM about the vocabulary —
# never add a setting here to make a conversion happen; add it because the
# values really do run from less to more.
ORDERED_SCALES: frozenset[str] = frozenset(
    {
        "reasoning_effort",
        "reasoning_summary",
        "resolution",
        "quality",
        "verbosity",
    }
)

# The house postures (ai_041): "auto" = leave unset, "none" = send nothing.
# They are never the equivalent of a DEGREE the caller asked for — snapping
# "minimal" onto "none" turns "think a little" into "do not think".
_HOUSE_VALUES = frozenset({"auto", "none"})

# ── format tokens: base + optional sample-rate/bitrate params ────────────────
# Canonical format values are either a bare name ("mp3", "wav") or a
# parameterised one ("mp3_44100_128" = 44.1kHz/128kbps, "wav_24000" = 24kHz
# PCM-in-WAV). The first numeric group is always the SAMPLE RATE; a second one
# (mp3/opus bitrate) is parsed but never used for equivalence — sample rate is
# what changes whether two candidates sound the same, bitrate is a quality
# knob within that.
#
# A generic "letters-then-digits" regex CANNOT extract the base, because
# "mp3" — a base name, not a parameter — itself ends in a digit. Base names
# are matched explicitly instead (longest-first, so "alaw" never
# short-circuits inside a hypothetical longer name).
_KNOWN_FORMAT_BASES: tuple[str, ...] = tuple(
    sorted(
        {"png", "webp", "jpeg", "jpg", "mp3", "aac", "opus", "ogg", "wav", "flac", "pcm", "mulaw", "ulaw", "alaw"},
        key=len,
        reverse=True,
    )
)

# Some canonical tokens spell the exact same codec two different ways
# (mu-law telephony is "mulaw" bare or "ulaw_8000" parameterised; A-law is
# "alaw" bare or "alaw_8000"). Normalising the base here means family
# membership and rate-matching only ever have to know ONE name per codec.
_BASE_SYNONYMS: dict[str, str] = {"ulaw": "mulaw"}


def _parse_format_token(token: str) -> tuple[str, int | None]:
    """(normalized_base, sample_rate_or_None). A token that doesn't start with
    one of ``_KNOWN_FORMAT_BASES`` returns itself as its own base with no
    rate — it simply can't match any known family, which IS the correct "no
    honest equivalence" outcome rather than a crash."""
    lowered = token.strip().lower()
    for base in _KNOWN_FORMAT_BASES:
        if lowered == base:
            return _BASE_SYNONYMS.get(base, base), None
        if lowered.startswith(base + "_"):
            rest = lowered[len(base) + 1 :]
            first_part = rest.split("_", 1)[0]
            rate = int(first_part) if first_part.isdigit() else None
            return _BASE_SYNONYMS.get(base, base), rate
    return lowered, None


def _pick_by_base(
    base: str, value_rate: int | None, by_base: dict[str, list[tuple[str, int | None]]]
) -> str | None:
    """Among the candidates sharing ``base``, prefer one carrying the SAME
    sample rate as the value (wav_24000 -> pcm_24000 over pcm_8000); fall back
    to the alphabetically-first member when neither side has a rate to match
    on, or none of the candidate rates agree."""
    members = by_base.get(base)
    if not members:
        return None
    if value_rate is not None:
        same_rate = sorted(token for token, rate in members if rate == value_rate)
        if same_rate:
            return same_rate[0]
    return sorted(token for token, _rate in members)[0]


# Format families: members of one family are interchangeable renderings of the
# same thing, so any member converts to any other member before it converts to
# an outsider. Within a family the ORDER below is the preference order. Every
# entry is a normalized BASE (post-synonym, no rate/param suffix) — a
# parameterised canonical value (mp3_44100_128, alaw_8000, wav_24000) is
# matched via ``_parse_format_token`` before it's compared here.
_IMAGE_FORMAT_FAMILY: tuple[str, ...] = ("png", "webp", "jpeg", "jpg")
_AUDIO_FORMAT_FAMILIES: dict[str, tuple[str, ...]] = {
    "lossy": ("mp3", "aac", "opus", "ogg"),
    "lossless": ("wav", "flac", "pcm"),
    "telephony": ("mulaw", "alaw"),
}
_FORMAT_FAMILIES: tuple[tuple[str, ...], ...] = (
    _IMAGE_FORMAT_FAMILY,
    *_AUDIO_FORMAT_FAMILIES.values(),
)

# Reverse index: normalized base -> which audio family it belongs to. Every
# canonical audio_format value (2026-08-17 vocabulary) falls into exactly one
# of these three families, so this covers the full vocabulary by construction.
_AUDIO_FAMILY_OF_BASE: dict[str, str] = {
    base: name for name, bases in _AUDIO_FORMAT_FAMILIES.items() for base in bases
}

# LAST-RESORT cross-family order for audio_format ONLY (see ``_audio_format``):
# tried strictly AFTER the value's own family has been searched and failed.
# lossless first (re-encoding a lossy/telephony source into PCM/WAV/FLAC loses
# nothing further and is always a safe destination), then lossy (still a
# normal-fidelity, widely-playable format), and telephony LAST (narrowband
# 8kHz mu-law/A-law — a real quality cut, accepted only because it is still
# audible speech, which is strictly better than the setting silently vanishing).
_AUDIO_FAMILY_FALLBACK_ORDER: tuple[str, ...] = ("lossless", "lossy", "telephony")


def _house_filtered(candidates: Iterable[str]) -> set[str]:
    return {c for c in candidates if c not in _HOUSE_VALUES}


# ── metrics ──────────────────────────────────────────────────────────────────
def _ordinal(value: str, candidates: set[str], order: tuple[str, ...]) -> str | None:
    """Position in the canonical scale; ties break toward the LATER (more
    intense) position — never silently weaken what the caller asked for."""
    if value not in order:
        return None
    index = order.index(value)
    best: str | None = None
    best_rank: tuple[int, int] | None = None
    for position, candidate in enumerate(order):
        if candidate not in candidates:
            continue
        rank = (abs(position - index), -position)
        if best_rank is None or rank < best_rank:
            best, best_rank = candidate, rank
    return best


def _parse_ratio(value: str) -> float | None:
    if ":" not in value:
        return None
    a, _, b = value.partition(":")
    try:
        width, height = float(a), float(b)
    except ValueError:
        return None
    return width / height if height else None


def _aspect_ratio(value: str, candidates: set[str], _order: tuple[str, ...]) -> str | None:
    """Nearest by GEOMETRY, and orientation is never flipped: a portrait request
    resolves to the nearest portrait the model has, never to a landscape crop
    of it (16:10 -> 16:9, not 9:16)."""
    target = _parse_ratio(value)
    if target is None:
        return None
    want_landscape = target >= 1.0
    scored: list[tuple[float, str]] = []
    fallback: list[tuple[float, str]] = []
    for candidate in candidates:
        ratio = _parse_ratio(candidate)
        if ratio is None:
            continue
        distance = abs(ratio - target)
        if (ratio >= 1.0) == want_landscape:
            scored.append((distance, candidate))
        else:
            fallback.append((distance, candidate))
    pool = scored or fallback
    return min(pool, key=lambda item: (item[0], item[1]))[1] if pool else None


def _format_family(value: str, candidates: set[str], _order: tuple[str, ...]) -> str | None:
    """Same family first (mp3 -> aac before mp3 -> wav), preferring the family's
    declared order. A parameterised member (``mp3_44100_128``, ``alaw_8000``,
    ``wav_24000``) is matched on its normalized BASE, so a bitrate/sample-rate
    variant still finds its family — and telephony synonyms (mulaw/ulaw_8000,
    alaw/alaw_8000) unify onto one base before comparison. When both the value
    and a same-family candidate carry a sample rate, the SAME-rate candidate
    wins over an arbitrary alphabetical pick (wav_24000 -> pcm_24000, not
    pcm_8000, when both are offered). This is used directly by ``output_format``
    (still images — no cross-family fallback) and as the WITHIN-family step of
    ``_audio_format`` below."""
    value_base, value_rate = _parse_format_token(value)
    by_base: dict[str, list[tuple[str, int | None]]] = {}
    for candidate in candidates:
        cbase, crate = _parse_format_token(candidate)
        by_base.setdefault(cbase, []).append((candidate, crate))

    # Exact family member first — the same format at a different parameterisation.
    same = _pick_by_base(value_base, value_rate, by_base)
    if same is not None:
        return same

    for family in _FORMAT_FAMILIES:
        if value_base not in family:
            continue
        for preferred in family:
            got = _pick_by_base(preferred, value_rate, by_base)
            if got is not None:
                return got
    return None


def _audio_format(value: str, candidates: set[str], _order: tuple[str, ...]) -> str | None:
    """audio_format's metric. Two steps, strictly ordered:

    1. WITHIN the value's own family (lossy->lossy, lossless->lossless,
       telephony->telephony) — delegates to ``_format_family`` verbatim, so a
       same-family candidate ALWAYS wins over a cross-family one.
    2. Only when the value's own family has NO member at all on the target,
       cross into another family, in ``_AUDIO_FAMILY_FALLBACK_ORDER``
       (lossless, then lossy, then telephony last). Every canonical
       audio_format value belongs to exactly one of the three known families
       (2026-08-17 vocabulary audit); a value whose base we don't recognize
       refuses to guess and returns None rather than inventing a codec
       relationship we can't actually measure (law rule 4)."""
    within_family = _format_family(value, candidates, _order)
    if within_family is not None:
        return within_family

    value_base, value_rate = _parse_format_token(value)
    own_family = _AUDIO_FAMILY_OF_BASE.get(value_base)
    if own_family is None:
        return None

    by_base: dict[str, list[tuple[str, int | None]]] = {}
    for candidate in candidates:
        cbase, crate = _parse_format_token(candidate)
        by_base.setdefault(cbase, []).append((candidate, crate))

    for family_name in _AUDIO_FAMILY_FALLBACK_ORDER:
        if family_name == own_family:
            continue  # already tried above, via _format_family
        for base_name in _AUDIO_FORMAT_FAMILIES[family_name]:
            got = _pick_by_base(base_name, value_rate, by_base)
            if got is not None:
                return got
    return None


# Genders that mean "no constraint" — a voice with no declared gender may stand
# in for any gender, and any gender may stand in for it. Arman: "if a voice
# doesn't have a gender, then it means any gender is ok so it's easy."
_WILDCARD_GENDERS = frozenset({"", "unknown", "neutral", "any"})


def _tts_voice(
    value: str, candidates: set[str], _order: tuple[str, ...], genders: dict[str, str]
) -> str | None:
    """THE VOICE RULE (law rule 5): gender is load-bearing, identity usually is not.

    > *"The most important thing is that a male voice is mapped to a male voice,
    > and a female voice is mapped to a female voice. You don't want to mess up
    > the gender of the voice, because if you have a podcast with two speakers
    > and they have a male and a female name, you can't have the genders wrong.
    > But the actual voice MAY not matter."* — Arman, 2026-08-17

    So: same gender wins; a genderless voice is a wildcard in both directions;
    and crossing gender is NEVER allowed — with no same-gender and no wildcard
    candidate this returns None, which the caller reports as a loud drop. A
    podcast that silently swaps its male host for a female voice is worse than
    one that tells you it could not cast the part.

    Voice IDENTITY mapping (this Google voice always becomes that ElevenLabs
    voice) is deliberately NOT attempted — it is a preference, not an
    equivalence, and inventing one would be the "converting wrong" failure.
    Selection among equally-valid candidates is DETERMINISTIC (sorted), so the
    same request never casts a different voice run to run.
    """
    if not genders:
        return None

    def gender_of(token: str) -> str:
        return genders.get(token.strip().lower(), "").strip().lower()

    wanted = gender_of(value)
    wildcards = sorted(c for c in candidates if gender_of(c) in _WILDCARD_GENDERS)

    if wanted in _WILDCARD_GENDERS:
        # The request carries no gender constraint: anything is acceptable.
        return sorted(candidates)[0] if candidates else None

    same = sorted(c for c in candidates if gender_of(c) == wanted)
    if same:
        return same[0]
    # No voice of that gender — an unconstrained voice is the only honest
    # stand-in. Never fall through to the opposite gender.
    return wildcards[0] if wildcards else None


_METRICS: dict[str, Callable[..., str | None]] = {
    "aspect_ratio": _aspect_ratio,
    "output_format": _format_family,
    "audio_format": _audio_format,
}


def nearest_equivalent(
    key: str,
    value: Any,
    candidates: Iterable[Any],
    order: Iterable[Any] = (),
    *,
    genders: dict[str, str] | None = None,
) -> str | None:
    """THE ONE entry point. Returns the target's nearest equivalent of ``value``,
    or ``None`` when this setting has no way to measure equivalence — in which
    case the caller must report a loud drop, never guess.

    ``tts_voice`` resolves by GENDER (see ``_tts_voice``) — the one property
    that must never be wrong. It needs the ``genders`` lookup; without it there
    is nothing to measure and it refuses rather than casting blind.
    """
    if not isinstance(value, str):
        return None
    raw = {str(c) for c in candidates}
    # The house filter exists to stop an INTENSITY collapsing onto a posture
    # ("minimal" -> "none" = think a little -> do not think). It must not apply
    # when the caller sent a posture in the first place: "none" -> "auto" is a
    # legitimate posture-to-posture translation for an offering that expresses
    # "no reasoning" as an omitted key.
    pool = raw if value in _HOUSE_VALUES else _house_filtered(raw)
    if not pool:
        return None
    scale = tuple(str(v) for v in order)

    if key == "tts_voice":
        return _tts_voice(value, pool, scale, genders or {})

    metric = _METRICS.get(key)
    if metric is not None:
        return metric(value, pool, scale)
    if key in ORDERED_SCALES:
        return _ordinal(value, pool, scale)
    return None


__all__ = ["ORDERED_SCALES", "nearest_equivalent"]
