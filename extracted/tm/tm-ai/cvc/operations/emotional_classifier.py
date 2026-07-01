"""
cvc.operations.emotional_classifier — Auto-encode mood from message text.

Foundation Horizon 2: "Emotional context encoding: when the user is
frustrated ('ugh, this again'), capture that. When they're excited
('it works!'), capture that. Future time-travel should let them feel
the emotional arc, not just the technical one."

Two-tier design:
  1. Heuristic classifier (this module, deterministic, no LLM cost):
     lexicon-based with negation handling, exclamation density,
     message length penalty (terse = likely frustrated).
  2. LLM fallback (caller passes an adapter): the heuristic is a
     fast first-pass; when its confidence is low or the text is
     long, defer to a real model.

Output: (mood, intensity, confidence) — confidence < 0.4 means
"let the LLM decide". Caller decides what to do.

Mood taxonomy mirrors EmotionalContext.mood in user_model:
    frustrated | excited | focused | tired | curious | proud
    | anxious | grateful | playful | neutral

The classifier is intentionally SIMPLE — it's a heuristic, not
sentiment analysis. The goal is "did the user feel something
noteworthy enough to tag the commit", not "what is their precise
emotional state".
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Iterable

logger = logging.getLogger("cvc.emotional_classifier")

# ── Lexicons ──────────────────────────────────────────────────────────────
# Each word has a base weight; final mood = argmax weighted sum.
# Weights are small integers so the heuristic never produces
# extreme intensity on its own — caller decides ceiling.

FRUSTRATED_LEXICON = {
    "ugh": 2, "damn": 2, "shit": 2, "fuck": 3, "wtf": 3, "broken": 2,
    "bug": 1, "wrong": 1, "error": 1, "fail": 2, "failed": 2, "fails": 2,
    "doesn't work": 2, "not working": 2, "still": 1, "again": 1,
    "why": 1, "ughh": 2, "frustrated": 3, "annoyed": 3, "annoying": 3,
    "stupid": 2, "wasted": 2, "useless": 3, "hate": 2, "broken again": 3,
    "regression": 2, "regressed": 2, "reverted": 1, "stopped working": 2,
    "broken": 2, "fml": 3, "ughhh": 2,
}

EXCITED_LEXICON = {
    "yes": 1, "yess": 2, "yesss": 3, "works": 2, "it works": 3,
    "shipped": 3, "ship": 2, "launched": 3, "live": 1, "deployed": 2,
    "amazing": 3, "awesome": 3, "incredible": 3, "fantastic": 3,
    "love": 1, "beautiful": 2, "perfect": 2, "finally": 2, "yay": 3,
    "woohoo": 3, "boom": 2, "nailed": 2, "killed it": 3, "nice": 1,
    "great": 1, "wow": 2, "solved": 2, "fixed": 2, "hooked up": 2,
}

FOCUSED_LEXICON = {
    "implementing": 1, "building": 1, "writing": 1, "designing": 1,
    "spec": 1, "specs": 1, "architecture": 1, "refactor": 1, "schema": 1,
    "foundation": 1, "structure": 1, "pattern": 1, "approach": 1,
    "decide": 1, "deciding": 1, "reviewing": 1, "thinking": 1,
    "considered": 1, "options": 1, "compare": 1, "tradeoff": 1,
    "trade-offs": 1, "principle": 1,
}

TIRED_LEXICON = {
    "tired": 3, "exhausted": 3, "long day": 2, "no energy": 2,
    "burnt out": 3, "drained": 2, "sleepy": 2, "ugh i need coffee": 2,
    "low energy": 2, "fed up": 2,
}

CURIOUS_LEXICON = {
    "what if": 2, "wonder": 1, "wondering": 1, "could we": 2,
    "is there": 1, "how does": 1, "why does": 1, "research": 1,
    "investigate": 1, "explore": 1, "exploring": 1, "let me think": 1,
    "hmm": 1, "interesting": 1, "i wonder": 2, "would it": 2,
}

PROUD_LEXICON = {
    "shipped it": 3, "proud": 3, "love how this": 2, "i built": 2,
    "released": 2, "milestone": 2, "completed": 1, "done": 1,
    "achievement": 2, "this is mine": 2, "my work": 1,
}

ANXIOUS_LEXICON = {
    "worried": 3, "concerned": 2, "nervous": 2, "anxious": 3,
    "scared": 2, "what if it": 2, "deadline": 1, "running out": 2,
    "afraid": 2, "stress": 2, "stressed": 2, "panic": 3, "pressure": 1,
}

GRATEFUL_LEXICON = {
    "thanks": 1, "thank you": 2, "thx": 1, "appreciate": 2,
    "grateful": 3, "lifesaver": 3, "saved me": 2, "you're the best": 2,
    "awesome job": 2, "well done": 2, "good catch": 2,
}

PLAYFUL_LEXICON = {
    "lol": 2, "haha": 2, "hehe": 2, "😂": 3, "😄": 2, "🤣": 3,
    "funny": 1, "lolz": 2, "kidding": 1, "jk": 1, "btw": 0, "btw ": 0,
    "btw,": 0,  # these last three should NOT trigger playful
}

# Negation flips the mood within a window
NEGATIONS = {"not", "no", "never", "n't", "without", "barely", "hardly"}

# Mood priority when multiple moods score equally — emotional arc
# cares about the *peak*, so excited/proud beat neutral
MOOD_PRIORITY = {
    "frustrated": 8,
    "anxious": 7,
    "excited": 6,
    "proud": 5,
    "grateful": 4,
    "playful": 3,
    "focused": 2,
    "curious": 1,
    "tired": 0,
    "neutral": -1,
}


@dataclass
class Classification:
    mood: str
    intensity: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0 — how sure we are
    trigger: str = ""  # what phrase tipped the classification


def _normalise(text: str) -> str:
    """Lowercase + collapse whitespace + strip punctuation noise."""
    t = text.lower()
    t = re.sub(r"[\u2018\u2019\u201c\u201d]", "'", t)  # smart quotes
    t = re.sub(r"[!?]{2,}", "!", t)  # collapse !!!, !!, ?!
    return re.sub(r"\s+", " ", t).strip()


def _count_signals(text: str, lexicon: dict[str, int]) -> tuple[int, list[str]]:
    """Count weighted hits in text; return (total_weight, matched_phrases)."""
    total = 0
    matched: list[str] = []
    # Longer phrases first so "doesn't work" matches before "work"
    sorted_keys = sorted(lexicon.keys(), key=lambda k: -len(k))
    used_spans: list[tuple[int, int]] = []

    def overlaps(span: tuple[int, int]) -> bool:
        for s, e in used_spans:
            if not (span[1] <= s or span[0] >= e):
                return True
        return False

    for phrase in sorted_keys:
        start = 0
        while True:
            idx = text.find(phrase, start)
            if idx < 0:
                break
            span = (idx, idx + len(phrase))
            if not overlaps(span):
                # Negation check: look back 3 tokens for negation
                prefix = text[max(0, idx - 20):idx].strip().split()
                if any(t in NEGATIONS for t in prefix[-3:]):
                    # Negated — flip to negative weight (the opposite of the mood)
                    # E.g. "not working" → mild POSITIVE (relief?) — for simplicity
                    # we just zero it out (caller can LLM-fallback)
                    pass
                else:
                    total += lexicon[phrase]
                    matched.append(phrase)
                    used_spans.append(span)
            start = idx + len(phrase)
    return total, matched


def classify_text(text: str) -> Classification:
    """Heuristically classify a piece of user text into (mood, intensity, confidence).

    Args:
        text: raw user message(s), any length

    Returns:
        Classification with mood from the 10-mood taxonomy, intensity 0-1,
        and confidence 0-1. Confidence < 0.4 means "defer to LLM".
    """
    if not text or not text.strip():
        return Classification(mood="neutral", intensity=0.0, confidence=0.0)

    norm = _normalise(text)

    # Score each mood
    scores: dict[str, tuple[int, list[str]]] = {}
    for mood, lex in [
        ("frustrated", FRUSTRATED_LEXICON),
        ("excited", EXCITED_LEXICON),
        ("focused", FOCUSED_LEXICON),
        ("tired", TIRED_LEXICON),
        ("curious", CURIOUS_LEXICON),
        ("proud", PROUD_LEXICON),
        ("anxious", ANXIOUS_LEXICON),
        ("grateful", GRATEFUL_LEXICON),
        ("playful", PLAYFUL_LEXICON),
    ]:
        scores[mood] = _count_signals(norm, lex)

    # Pick the mood with the highest score (ties broken by priority)
    best_mood = "neutral"
    best_score = 0
    best_matched: list[str] = []
    for mood, (score, matched) in scores.items():
        if score > best_score or (
            score == best_score and score > 0
            and MOOD_PRIORITY[mood] > MOOD_PRIORITY[best_mood]
        ):
            best_mood = mood
            best_score = score
            best_matched = matched

    if best_score == 0:
        # No lexicon hit → neutral with low intensity
        return Classification(
            mood="neutral",
            intensity=0.1,
            confidence=0.2,  # low — caller should LLM-fallback on long texts
            trigger="",
        )

    # Intensity: scale by score, capped. Long messages dilute.
    raw_intensity = min(1.0, best_score / 4.0)
    # Long neutral text reduces intensity (mixed signals across sentences)
    if len(norm) > 500:
        raw_intensity *= 0.6
    elif len(norm) > 200:
        raw_intensity *= 0.8

    # Confidence: how clearly did the winning mood dominate?
    total = sum(s for s, _ in scores.values())
    dominance = best_score / total if total > 0 else 0.0
    confidence = min(1.0, dominance * 1.5)  # scaled so 67% dominance = 1.0

    trigger = best_matched[0] if best_matched else ""

    return Classification(
        mood=best_mood,
        intensity=round(raw_intensity, 3),
        confidence=round(confidence, 3),
        trigger=trigger,
    )


def classify_session(messages: Iterable[dict]) -> Classification:
    """Classify a session's emotional arc by combining all user messages.

    Args:
        messages: list of {"role": ..., "content": ...} dicts

    Returns:
        The dominant Classification across the session. User messages only.
    """
    user_text = " ".join(
        (m.get("content") or "") for m in messages if m.get("role") in ("user", "human")
    )
    return classify_text(user_text)