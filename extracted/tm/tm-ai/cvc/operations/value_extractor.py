"""
cvc.operations.value_extractor — Heuristic value detector.

The soul layer records "values" — declarative principles the user
states or repeats. The full LLM-driven path (cvc.core.user_model.
apply_soul_reasoning_response) only fires on session stop, which
dashboard chats never reach. So values were perpetually 0.

This module adds a cheap, deterministic pass that scans user
messages for value-shaped sentences:

  - "I believe X"
  - "I care about X"
  - "X is important to me"
  - "I value X"
  - "I always X" / "I never X"
  - "X matters more than Y"
  - "the most important thing is X"
  - "I want to build X for Y"
  - "my principle is X"
  - "I think X" / "I feel X" (softer, lower confidence)

Outputs: list[ExtractedValue] ready to merge into UserIdentitySnapshot
via UserModelManager.

hotfix/soul-values-and-cleanup-2026-06-30 — first-time heuristic
extractor. Companion to entity_extractor. Triggers without an LLM
call so the What You Believe section populates immediately on
every chat turn, not just at session-stop.
"""
from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Iterable

logger = logging.getLogger("cvc.value_extractor")


# ── Pattern catalogue ───────────────────────────────────────────────
# Each tuple: (compiled regex, base confidence, category hint).
# The regex MUST contain a named group ``statement`` capturing the
# value statement to record. Categories are intentionally broad —
# the AI cleanup pass tightens them later.

# Strong / declarative patterns (high confidence)
STRONG_PATTERNS: list[tuple[re.Pattern, float, str]] = [
    (re.compile(r"\bi\s+believe\s+(?:that\s+)?(?P<statement>[^.!?\n]+)", re.I), 0.85, "philosophy"),
    (re.compile(r"\bi\s+strongly\s+believe\s+(?:that\s+)?(?P<statement>[^.!?\n]+)", re.I), 0.9, "philosophy"),
    (re.compile(r"\bi\s+(?:really\s+)?care\s+about\s+(?P<statement>[^.!?\n]+)", re.I), 0.8, "life"),
    (re.compile(r"\bi\s+value\s+(?P<statement>[^.!?\n]+)", re.I), 0.8, "philosophy"),
    (re.compile(r"\bi\s+value\s+(?:the\s+)?(?P<statement>[^.!?\n]+)", re.I), 0.8, "philosophy"),
    (re.compile(r"\b(?:the\s+)?most\s+important\s+thing\s+(?:is|to\s+me\s+is)\s+(?P<statement>[^.!?\n]+)", re.I), 0.85, "philosophy"),
    (re.compile(r"\bwhat\s+matters\s+(?:most\s+)?to\s+me\s+is\s+(?P<statement>[^.!?\n]+)", re.I), 0.85, "philosophy"),
    (re.compile(r"\bmy\s+(?:core\s+)?principle(?:s)?\s+(?:is|are)\s+(?P<statement>[^.!?\n]+)", re.I), 0.85, "philosophy"),
    (re.compile(r"\bmy\s+(?:guiding\s+)?(?:belief|philosophy)\s+is\s+(?P<statement>[^.!?\n]+)", re.I), 0.8, "philosophy"),
    (re.compile(r"\bi\s+(?:always|never)\s+(?P<statement>[^.!?\n]+)", re.I), 0.7, "work"),
    (re.compile(r"\bi\s+prioritise\s+(?P<statement>[^.!?\n]+)", re.I), 0.7, "work"),
    (re.compile(r"\bi\s+prioritize\s+(?P<statement>[^.!?\n]+)", re.I), 0.7, "work"),
    (re.compile(r"\bi\s+(?:refuse|won't)\s+to\s+(?P<statement>[^.!?\n]+)", re.I), 0.75, "philosophy"),
    (re.compile(r"\bi\s+won'?t\s+(?P<statement>[^.!?\n]+)", re.I), 0.65, "philosophy"),
    (re.compile(r"\bnever\s+(?P<statement>[^.!?\n]+?)\s+at\s+the\s+cost\s+of\s+(?P<cost>[^.!?\n]+)", re.I), 0.85, "life"),
    (re.compile(r"\bX\s+matters\s+more\s+than\s+Y", re.I), 0.7, "philosophy"),  # capturable below
    (re.compile(r"\b(?:family|health|users?|truth|integrity|simplicity|speed|quality|impact)\b\s+(?:comes\s+first|matters\s+most|is\s+non-?negotiable)", re.I), 0.8, "philosophy"),
]

# Medium patterns (still declarative, lower confidence)
MEDIUM_PATTERNS: list[tuple[re.Pattern, float, str]] = [
    (re.compile(r"\bi\s+(?:want|need)\s+to\s+build\s+(?P<statement>[^.!?\n]+?)\s+for\s+(?P<why>[^.!?\n]+?)(?:[.!?\n]|$)", re.I), 0.6, "work"),
    (re.compile(r"\bi\s+(?:want|need)\s+to\s+build\s+(?P<statement>[^.!?\n]+?)(?:[.!?\n]|$)", re.I), 0.55, "work"),
    (re.compile(r"\bi\s+(?:want|need)\s+to\s+(?:ship|deliver|launch)\s+(?P<statement>[^.!?\n]+?)(?:[.!?\n]|$)", re.I), 0.6, "work"),
    (re.compile(r"\bi'?m\s+(?:building|working\s+on)\s+(?P<statement>[^.!?\n]+?)\s+because\s+(?P<why>[^.!?\n]+?)(?:[.!?\n]|$)", re.I), 0.6, "work"),
    (re.compile(r"\bi'?m\s+(?:building|working\s+on)\s+(?P<statement>[^.!?\n]+?)(?:[.!?\n]|$)", re.I), 0.55, "work"),
    (re.compile(r"\bthe\s+whole\s+point\s+(?:of\s+\w+\s+)?is\s+(?P<statement>[^.!?\n]+)", re.I), 0.6, "philosophy"),
    (re.compile(r"\bwhy\s+i\s+(?:do|build|ship)\s+(?:this|that)\s*[:\-]?\s*(?P<statement>[^.!?\n]+)", re.I), 0.6, "philosophy"),
    (re.compile(r"\bmy\s+(?:north\s+star|mission)\s+is\s+(?P<statement>[^.!?\n]+)", re.I), 0.75, "philosophy"),
]

# Soft patterns (heuristic, lower confidence — let the AI cleanup
# decide whether to keep)
SOFT_PATTERNS: list[tuple[re.Pattern, float, str]] = [
    (re.compile(r"\bi\s+think\s+(?:that\s+)?(?P<statement>[^.!?\n]+)", re.I), 0.4, "philosophy"),
    (re.compile(r"\bi\s+feel\s+(?:that\s+)?(?P<statement>[^.!?\n]+)", re.I), 0.45, "life"),
    (re.compile(r"\bfor\s+me,?\s+(?P<statement>[^.!?\n]+?)\s+(?:is\s+)?(?:important|key|critical|essential|non-?negotiable)", re.I), 0.65, "philosophy"),
]


# ── Reject patterns ────────────────────────────────────────────────
# Things that look like value statements but aren't. Keep this list
# small — false negatives (missing a real value) are preferable to
# false positives (recording junk).
JUNK_PATTERNS: list[re.Pattern] = [
    re.compile(r"^\s*(i\s+)?(do\s+not|don'?t)\s+know\s*$", re.I),
    re.compile(r"^\s*(i\s+)?(do\s+not|don'?t)\s+have\s+(?:a\s+)?(?:an?\s+)?(?:opinion|idea|clue)\s*$", re.I),
    re.compile(r"^\s*(?:just\s+)?(?:checking|saying|noting)\s*$", re.I),
    re.compile(r"^\s*(?:yes|no|maybe|sure|ok|okay|fine|good|nice|cool)\s*$", re.I),
    re.compile(r"^\s*i\s+'?m\s+(?:just\s+)?(?:checking|saying|noting)\s*$", re.I),
    re.compile(r"^\s*i\s+'?m\s+(?:happy|sad|tired|busy|here|back|ready)\s*$", re.I),
    re.compile(r"^\s*this\s+(?:is|seems|looks)\s+(?:good|fine|nice|cool|broken|wrong)\s*$", re.I),
    re.compile(r"^\s*(?:hello|hi|hey|good\s+morning|good\s+evening)\s*$", re.I),
]


# ── Length and shape filters ───────────────────────────────────────
MIN_STATEMENT_LEN = 12  # shorter = almost certainly noise
MAX_STATEMENT_LEN = 280  # longer = model the AI cleanup can trim


@dataclass
class ExtractedValue:
    """A candidate value statement pulled out of a user message."""

    statement: str
    category: str = "work"
    confidence: float = 0.5
    source_message_idx: int = -1
    context_snippet: str = ""
    extracted_at: float = field(default_factory=time.time)


def _clean(stmt: str) -> str:
    """Trim a captured statement to a clean single sentence."""
    if not stmt:
        return ""
    s = stmt.strip()
    # Strip trailing clauses introduced by 'because', 'so that', 'so'
    # so we record the value itself, not the justification.
    s = re.sub(r"\s+(?:because|so\s+that|so)\s+.*$", "", s, flags=re.I)
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    # Strip leading punctuation
    s = re.sub(r"^[\s,;:.\-]+", "", s)
    return s


def _is_junk(stmt: str) -> bool:
    if not stmt:
        return True
    s = stmt.strip()
    if len(s) < MIN_STATEMENT_LEN or len(s) > MAX_STATEMENT_LEN:
        return True
    for pat in JUNK_PATTERNS:
        if pat.match(s):
            return True
    return False


def extract_from_message(text: str, message_idx: int = 0) -> list[ExtractedValue]:
    """Extract value statements from one user message.

    Algorithm:
      1. Scan STRONG_PATTERNS first (high confidence, philosophy/life).
      2. Then MEDIUM_PATTERNS (work-anchored declarations).
      3. Then SOFT_PATTERNS (heuristic, lower confidence).
      4. Dedupe by lowercased statement; keep highest confidence.
      5. Filter out junk + length issues.
    """
    if not text or not text.strip():
        return []
    candidates: dict[str, ExtractedValue] = {}

    tiers: list[tuple[list[tuple[re.Pattern, float, str]], str]] = [
        (STRONG_PATTERNS, "philosophy"),
        (MEDIUM_PATTERNS, "work"),
        (SOFT_PATTERNS, "philosophy"),
    ]

    for patterns, _tier_default_cat in tiers:
        for pat, conf, cat_hint in patterns:
            has_why = "why" in pat.groupindex
            for m in pat.finditer(text):
                if "statement" in pat.groupindex:
                    stmt = m.group("statement") or ""
                else:
                    stmt = m.group(0) or ""
                # hotfix/soul-values-and-cleanup-2026-06-30 — if the
                # pattern also captured a "why" clause, fold it back
                # into the statement so the recorded value carries
                # the reasoning. E.g. "build CVC for Jai" becomes
                # "build CVC for Jai" — full context preserved.
                if has_why:
                    why = m.group("why")
                    if why and why.strip():
                        stmt = f"{stmt.strip()} for {why.strip()}"
                stmt = _clean(stmt)
                if _is_junk(stmt):
                    continue
                key = stmt.lower()
                if key in candidates:
                    # Keep the higher-confidence extraction
                    if conf > candidates[key].confidence:
                        candidates[key].confidence = conf
                        candidates[key].category = cat_hint or candidates[key].category
                    continue
                candidates[key] = ExtractedValue(
                    statement=stmt,
                    category=cat_hint,
                    confidence=conf,
                    source_message_idx=message_idx,
                    context_snippet=text[max(0, m.start() - 40): m.end() + 40][:240],
                )

    return list(candidates.values())


def extract_from_session(messages: Iterable[dict]) -> list[ExtractedValue]:
    """Extract values from a full session (user messages only)."""
    out: list[ExtractedValue] = []
    seen: dict[str, ExtractedValue] = {}

    for i, m in enumerate(messages):
        if m.get("role") not in ("user", "human"):
            continue
        text = m.get("content") or ""
        for val in extract_from_message(text, message_idx=i):
            key = val.statement.lower()
            if key not in seen:
                seen[key] = val
            else:
                # Keep highest-confidence version, bump timestamp.
                if val.confidence > seen[key].confidence:
                    seen[key].confidence = val.confidence
                seen[key].last_reinforced_at = time.time()  # type: ignore[attr-defined]
    return list(seen.values())


def merge_into_snapshot(extracted: list[ExtractedValue], snapshot) -> int:
    """Merge extracted values into a UserIdentitySnapshot, dedup by lowercased statement.

    Returns count of NEW values added (existing ones get last_reinforced bumped).

    hotfix/soul-values-and-cleanup-2026-06-30 — also deduplicates WITHIN
    the extracted list so callers that pass a fresh extract_from_message
    result don't accidentally double-add when multiple patterns matched
    the same sentence.
    """
    added = 0
    from cvc.core.user_model import ValueStatement

    existing = {v.statement.lower(): v for v in (snapshot.values or [])}
    seen_in_batch: dict[str, ExtractedValue] = {}

    # First pass: dedup within the extracted batch, keep highest conf.
    for ext in extracted:
        key = ext.statement.lower()
        if key in seen_in_batch:
            if ext.confidence > seen_in_batch[key].confidence:
                seen_in_batch[key].confidence = ext.confidence
            continue
        seen_in_batch[key] = ext

    # Second pass: merge into snapshot.
    for key, ext in seen_in_batch.items():
        if key in existing:
            v = existing[key]
            v.last_reinforced = ext.extracted_at
            v.confidence = max(v.confidence, ext.confidence)
            continue
        snapshot.values.append(
            ValueStatement(
                statement=ext.statement,
                category=ext.category,
                confidence=ext.confidence,
            )
        )
        added += 1
    return added