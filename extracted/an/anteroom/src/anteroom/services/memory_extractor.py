"""Selective auto-propose memory extraction (#1454).

Pure post-turn extractor: given a final assistant response and the set of
memories already recalled this turn, ask the LLM to surface durable facts
worth remembering as candidate memories. The function does not write to
the database, emit events, or call propose_candidate — that is the
runner's job. This keeps the extractor pluggable and easy to test
independently.

Returns ``(items, reason)`` mirroring the
:func:`anteroom.services.memory_recall.retrieve_memories` shape so callers
can branch on a small set of named outcomes:

* ``"ok"`` — extraction yielded one or more candidates after filtering
* ``"disabled"`` — auto-propose config is off
* ``"empty_input"`` — assistant text is too short / empty to extract from
* ``"no_results"`` — LLM returned an empty list or nothing survived filters
* ``"failed"`` — model call failed, JSON parse failed, or unexpected error
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from ..config import MemoryAutoProposeConfig

if TYPE_CHECKING:
    from .ai_service import AIService
    from .memory_recall import RecalledMemory

logger = logging.getLogger(__name__)

# Maximum length of assistant text fed to the extractor — keeps LLM cost
# bounded for very long final turns and prevents prompt-bloat.
_MAX_INPUT_CHARS = 8000

# Minimum useful assistant text length. Short responses (acknowledgements,
# tool-result echoes) are skipped to save LLM round-trips.
_MIN_INPUT_CHARS = 80


@dataclass(frozen=True)
class ExtractedCandidate:
    """A candidate memory surfaced by the extractor.

    The runner is the sole writer that persists candidates via
    ``memory_promotion.propose_candidate(...)``.
    """

    content: str
    category: str  # one of MEMORY_CATEGORIES — validated by extractor
    confidence: float  # 0.0-1.0
    scope: str  # "user" | "project" | "local" — defaulted by runner if absent


_EXTRACTION_PROMPT = """You are a memory extraction assistant for an AI \
gateway. Scan the assistant response below and surface DURABLE FACTS the \
user would benefit from the assistant remembering across future turns.

Output requirements (strict):
- Reply with valid JSON ONLY. No prose, no markdown fences.
- Shape: {{"candidates": [{{"category": "...", "content": "...", \
"confidence": 0.0-1.0}}]}}
- Allowed categories: {categories}
- Maximum {max_candidates} candidates total. Quality over quantity.
- ``content`` must be a complete, self-contained statement (1-2 sentences) \
that would still make sense if read months later with no surrounding \
context.
- ``confidence`` must reflect how confident you are this is a durable \
fact (not a one-off remark). Use 0.0 if you would not personally save it.

DO NOT extract:
- Conversational filler, acknowledgements, or transient task state
- Tool output verbatim
- Information already present in the recalled memories list below
- Speculation or hypotheticals
- Things the user did not assert as true

Recalled memories already known to the assistant this turn (for dedupe):
{recalled_block}

Assistant response to scan:
\"\"\"
{assistant_text}
\"\"\"

Respond with the JSON object now."""


def _format_recalled_block(recalled: list[RecalledMemory]) -> str:
    """Compact list of already-recalled memories for the dedupe context."""
    if not recalled:
        return "(none)"
    lines = []
    for m in recalled[:20]:  # cap context size
        snippet = (m.content or "").strip().replace("\n", " ")
        if len(snippet) > 200:
            snippet = snippet[:197] + "..."
        lines.append(f"- [{m.category}] {snippet}")
    return "\n".join(lines)


def _normalize(text: str) -> str:
    """Lowercase + collapse whitespace + drop punctuation for fuzzy match."""
    return re.sub(r"[^\w\s]", " ", text.lower()).split().__str__()


def _is_duplicate_of_recalled(
    candidate_content: str,
    recalled: list[RecalledMemory],
    *,
    threshold: float = 0.6,
) -> bool:
    """Crude Jaccard-on-tokens check.

    The runner is responsible for any embedding-based dedupe. This pure
    fallback catches the common cases (verbatim restatement, near-paraphrase
    of an existing memory) without requiring an embedding service. Below
    threshold ``threshold`` of token overlap is treated as not a duplicate.
    """
    cand_tokens = set(re.findall(r"\w+", candidate_content.lower()))
    if not cand_tokens:
        return True  # empty candidate is always treated as duplicate
    for m in recalled:
        m_tokens = set(re.findall(r"\w+", (m.content or "").lower()))
        if not m_tokens:
            continue
        overlap = len(cand_tokens & m_tokens) / max(len(cand_tokens | m_tokens), 1)
        if overlap >= threshold:
            return True
    return False


def _parse_response(raw: str) -> list[dict[str, Any]] | None:
    """Best-effort JSON parse of the model output.

    Returns the raw candidate-list (unfiltered) on success, or ``None`` on
    any parse failure. Strips common artefacts (markdown fences, leading
    prose) before parsing.
    """
    if not raw:
        return None
    text = raw.strip()
    # Strip ```json ... ``` fences if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)
    # If the model preambled, try to find the first '{' and use that.
    brace_idx = text.find("{")
    if brace_idx > 0:
        text = text[brace_idx:]
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.debug("memory_extractor: failed to parse LLM JSON output: %r", raw[:200])
        return None
    if not isinstance(parsed, dict):
        return None
    cands = parsed.get("candidates")
    if not isinstance(cands, list):
        return None
    return cands


async def extract_candidates(
    *,
    assistant_text: str,
    ai_service: AIService,
    recalled_memories: list[RecalledMemory],
    config: MemoryAutoProposeConfig,
) -> tuple[list[ExtractedCandidate], str]:
    """Extract candidate memories from a finished assistant turn.

    Pure: no DB writes, no audit emission, no event yielding. The runner
    in ``services/auto_propose_runner.py`` calls this and then routes
    surviving candidates through ``memory_promotion.propose_candidate``.

    Returns ``(items, reason)``. ``items`` is empty whenever ``reason``
    is anything other than ``"ok"``.
    """
    if not config.enabled:
        return [], "disabled"

    text = (assistant_text or "").strip()
    if len(text) < _MIN_INPUT_CHARS:
        return [], "empty_input"

    # Cap input — very long responses get truncated to bound LLM cost.
    if len(text) > _MAX_INPUT_CHARS:
        text = text[:_MAX_INPUT_CHARS]

    prompt = _EXTRACTION_PROMPT.format(
        categories=", ".join(config.categories),
        max_candidates=config.max_candidates_per_turn,
        recalled_block=_format_recalled_block(recalled_memories),
        assistant_text=text,
    )
    messages = [{"role": "user", "content": prompt}]

    try:
        raw = await ai_service.complete(messages, max_completion_tokens=600)
    except Exception:  # extractor must NEVER break the turn
        logger.debug("memory_extractor: ai_service.complete raised", exc_info=True)
        return [], "failed"

    if not raw:
        return [], "failed"

    parsed = _parse_response(raw)
    if parsed is None:
        return [], "failed"

    allowed_categories = set(config.categories)
    surviving: list[ExtractedCandidate] = []
    for raw_cand in parsed:
        if not isinstance(raw_cand, dict):
            continue
        category = str(raw_cand.get("category", "")).strip()
        content = str(raw_cand.get("content", "")).strip()
        try:
            confidence = float(raw_cand.get("confidence", 0.0))
        except (TypeError, ValueError):
            continue
        scope_raw = raw_cand.get("scope")
        scope = str(scope_raw).strip() if scope_raw else "user"
        if scope not in ("user", "project", "local"):
            scope = "user"

        if not content or not category:
            continue
        if category not in allowed_categories:
            continue
        if confidence < config.min_confidence:
            continue
        if _is_duplicate_of_recalled(content, recalled_memories):
            continue
        surviving.append(
            ExtractedCandidate(
                content=content,
                category=category,
                confidence=confidence,
                scope=scope,
            )
        )

    # Stable order by confidence desc, then take top-N.
    surviving.sort(key=lambda c: c.confidence, reverse=True)
    surviving = surviving[: config.max_candidates_per_turn]

    if not surviving:
        return [], "no_results"
    return surviving, "ok"
