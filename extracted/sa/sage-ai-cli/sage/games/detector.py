"""Prompt → GameRequest classifier.

Regex-first (no LLM cost on the common path). LLM fallback only when
regex confidence is low — e.g. "build me something fun" is ambiguous.

Wired into spec_decomposer so existing `sage ask "<prompt>"` and
`sage run` automatically route game prompts to the games pipeline. No
new top-level commands.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Callable, Optional

from .engines.base import GameRequest


GenerateFn = Callable[[str], str]


# Engine names — first match wins. We list aliases each engine uses
# colloquially so "UE5", "Unreal Engine 5", "Unreal" all map together.
_ENGINE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\b(godot\s*4?|godot\s*engine)\b", re.I), "godot"),
    (re.compile(r"\b(unreal(\s+engine)?\s*(5|4)?|ue\s*5|ue\s*4|uat)\b", re.I), "unreal"),
    (re.compile(r"\bunity(\s+3d|\s+2d)?\b", re.I), "unity"),
    (re.compile(r"\bbevy(\s+engine)?\b", re.I), "bevy"),
    (re.compile(r"\b(phaser(\s*3)?|phaserjs)\b", re.I), "phaser"),
    (re.compile(r"\b(love\s*2?d|love2d|löve)\b", re.I), "love2d"),
    (re.compile(r"\bpygame\b", re.I), "pygame"),
    (re.compile(r"\b(gamemaker(\s+studio)?|gms\s*2)\b", re.I), "gamemaker"),
    (re.compile(r"\bconstruct\s*3\b", re.I), "construct"),
    (re.compile(r"\brpg\s*maker(\s*mv|\s*mz)?\b", re.I), "rpgmaker"),
)


# Genre vocabulary — strong signal that the prompt is asking for a game
# even if no engine is named. Order matters: more specific genres first.
_GENRE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\b(metroidvania|soulslike|roguelite|roguelike)\b", re.I), "roguelike"),
    (re.compile(r"\b(platformer|jump\s+and\s+run)\b", re.I), "platformer"),
    (re.compile(r"\b(rpg|jrpg|crpg|role[\s-]?playing)\b", re.I), "rpg"),
    (re.compile(r"\b(fps|first[\s-]?person\s+shooter)\b", re.I), "fps"),
    (re.compile(r"\b(tower\s*defense|td\s+game)\b", re.I), "tower-defense"),
    (re.compile(r"\b(racing|kart\s*racer)\b", re.I), "racing"),
    (re.compile(r"\b(puzzle|match[\s-]?3|tetris[\s-]?like)\b", re.I), "puzzle"),
    (re.compile(r"\b(rts|real[\s-]?time\s+strategy)\b", re.I), "rts"),
    (re.compile(r"\b(turn[\s-]?based|tbs)\b", re.I), "turn-based"),
    (re.compile(r"\b(walking\s*sim(?:ulator)?|exploration\s+game)\b", re.I), "walking-sim"),
    (re.compile(r"\b(shmup|bullet\s*hell|shoot[\s-]?em[\s-]?up)\b", re.I), "shmup"),
    (re.compile(r"\b(survival|sandbox\s+survival)\b", re.I), "survival"),
    (re.compile(r"\b(fighting\s+game|brawler)\b", re.I), "fighting"),
)


# Generic "I want a game" phrases — used as a fallback signal so the
# detector triggers even when the user hasn't named a genre or engine.
_GAME_NOUN = re.compile(
    r"\b(game|playable|gameplay|player(?:\s+character)?|enemies?|"
    r"\b(?:2|3)d\s+game)\b",
    re.I,
)

_PERSPECTIVE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bfirst[\s-]?person\b", re.I), "first-person"),
    (re.compile(r"\bthird[\s-]?person\b", re.I), "third-person"),
    (re.compile(r"\bisometric\b", re.I), "isometric"),
    (re.compile(r"\btop[\s-]?down\b", re.I), "top-down"),
    (re.compile(r"\bside[\s-]?(scroller|view)\b", re.I), "side-scroller"),
    (re.compile(r"\b3d\b", re.I), "3d"),
    (re.compile(r"\b2d\b", re.I), "2d"),
)

_ART_STYLE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bpixel(\s*art)?\b", re.I), "pixel"),
    (re.compile(r"\bcartoon\b", re.I), "cartoon"),
    (re.compile(r"\bvoxel(\s*art)?\b", re.I), "voxel"),
    (re.compile(r"\blow[\s-]?poly\b", re.I), "low-poly"),
    (re.compile(r"\brealistic\b", re.I), "realistic"),
    (re.compile(r"\b(watercolor|hand[\s-]?drawn|sketch)\b", re.I), "hand-drawn"),
    (re.compile(r"\b(noir|monochrome|black\s*and\s*white)\b", re.I), "noir"),
)


@dataclass
class _RegexHit:
    """Internal: tracks what the regex pass found + a rough confidence score."""

    engine: Optional[str] = None
    genre: Optional[str] = None
    perspective: Optional[str] = None
    art_style: Optional[str] = None
    has_game_noun: bool = False

    def confidence(self) -> float:
        """0.0–1.0 confidence that this prompt is a game request.

        Engine match alone → near-certain (0.9). Genre alone is also a
        strong signal — almost nobody types "platformer" or "metroidvania"
        in a non-game context, so we credit 0.75 instead of 0.4. The other
        signals are corroborative.
        """
        score = 0.0
        if self.engine:
            score += 0.9
        if self.genre:
            score += 0.75
        if self.perspective in {"first-person", "third-person", "isometric",
                                 "top-down", "side-scroller"}:
            score += 0.3
        if self.perspective in {"2d", "3d"}:
            score += 0.15        # "2d" alone is weak (could be a print app)
        if self.has_game_noun:
            score += 0.25
        if self.art_style in {"pixel", "voxel", "low-poly"}:
            score += 0.2         # these strongly imply games over web design
        return min(score, 1.0)


def _scan(prompt: str) -> _RegexHit:
    hit = _RegexHit(has_game_noun=bool(_GAME_NOUN.search(prompt)))
    for pat, label in _ENGINE_PATTERNS:
        if pat.search(prompt):
            hit.engine = label
            break
    for pat, label in _GENRE_PATTERNS:
        if pat.search(prompt):
            hit.genre = label
            break
    for pat, label in _PERSPECTIVE_PATTERNS:
        if pat.search(prompt):
            hit.perspective = label
            break
    for pat, label in _ART_STYLE_PATTERNS:
        if pat.search(prompt):
            hit.art_style = label
            break
    return hit


_LLM_CLASSIFIER_PROMPT = """Classify this user prompt. Answer ONLY in JSON.

Prompt: {prompt!r}

Determine:
- task_type: one of "webapp", "game", "library", "cli"
- engine:    one of "godot", "unity", "unreal", "bevy", "phaser",
             "love2d", "pygame", "gamemaker", "construct", "rpgmaker", or null
- genre:     a short genre tag (platformer, rpg, fps, ...) or null
- perspective: "2d", "3d", "first-person", "third-person", "isometric",
               "top-down", "side-scroller", or null
- art_style: "pixel", "cartoon", "low-poly", "realistic", "voxel",
             "hand-drawn", or null

Output ONLY the JSON object. No prose, no markdown fences.
"""


def _llm_classify(prompt: str, generate: GenerateFn) -> dict:
    """Single-call LLM fallback for ambiguous prompts. Returns dict or {}."""
    try:
        raw = generate(_LLM_CLASSIFIER_PROMPT.format(prompt=prompt))
    except Exception:  # noqa: BLE001 — classifier MUST NOT crash callers
        return {}
    try:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1:
            return {}
        parsed = json.loads(raw[start : end + 1])
        return parsed if isinstance(parsed, dict) else {}
    except (json.JSONDecodeError, ValueError):
        return {}


def classify_prompt(
    prompt: str,
    *,
    generate: Optional[GenerateFn] = None,
    confidence_threshold: float = 0.7,
) -> tuple[str, Optional[GameRequest]]:
    """Return (task_type, GameRequest|None).

    Common path: pure regex. LLM fallback only when regex confidence
    is below threshold AND `generate` is supplied.
    """
    hit = _scan(prompt)
    conf = hit.confidence()

    if conf >= confidence_threshold:
        return "game", GameRequest(
            task_type="game",
            engine=hit.engine,
            genre=hit.genre,
            perspective=hit.perspective,
            art_style=hit.art_style,
            raw_prompt=prompt,
        )

    # Regex didn't find enough. If the prompt mentions a game noun but no
    # engine/genre, still treat as a game request — the pipeline will pick
    # a default engine.
    if hit.has_game_noun and conf >= 0.2:
        return "game", GameRequest(
            task_type="game",
            engine=hit.engine,
            genre=hit.genre,
            perspective=hit.perspective,
            art_style=hit.art_style,
            raw_prompt=prompt,
        )

    # Ambiguous and we have a model — ask it. Return whatever it says.
    if generate is not None and conf > 0:
        result = _llm_classify(prompt, generate)
        if result.get("task_type") == "game":
            return "game", GameRequest(
                task_type="game",
                engine=result.get("engine"),
                genre=result.get("genre"),
                perspective=result.get("perspective"),
                art_style=result.get("art_style"),
                raw_prompt=prompt,
            )

    return "webapp", None
