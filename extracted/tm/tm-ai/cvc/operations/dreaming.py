"""
cvc.operations.dreaming — DAG Dreaming (Cognitive Consolidation).

Implements a two-phase "sleep" cycle inspired by OpenClaw's REM dreaming,
but operating on the ENTIRE Merkle DAG commit history rather than just
today's sessions. This is CVC's "total recall" equivalent.

Phase 1 — Light Sleep:
  - Traverse recent N commits
  - Extract snippets with recency decay (14-day half-life)
  - Score by: frequency × relevance × diversity × recency
  - Promote candidates above threshold

Phase 2 — REM Sleep:
  - Deep LLM reflection on promoted candidates
  - Extract concept tags via vocabulary clustering
  - Detect contradictions across commits
  - Generate narrative dream summaries
  - Write "dream commits" on the ``dreams`` branch

Key innovation: OpenClaw dreams within a day. CVC dreams across weeks/months
of cognitive history. The Merkle DAG gives it total recall — every dream
commit links cryptographically to the source commits it was derived from.
"""

from __future__ import annotations

import json
import logging
import math
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.dreaming")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RECENCY_HALF_LIFE_DAYS = 14.0
MIN_PROMOTION_SCORE = 0.60
MAX_DREAM_CANDIDATES = 50
CONCEPT_TAG_LIMIT = 20


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class DreamCandidate:
    """A snippet promoted from light sleep for REM processing."""

    candidate_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    source_commit: str = ""
    content: str = ""
    topic_keywords: list[str] = field(default_factory=list)
    recency_score: float = 0.0
    frequency_score: float = 0.0
    relevance_score: float = 0.0
    diversity_score: float = 0.0
    composite_score: float = 0.0
    timestamp: float = 0.0


@dataclass
class DreamEntry:
    """A consolidated dream — the output of REM sleep."""

    dream_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    timestamp: float = field(default_factory=time.time)
    source_commits: list[str] = field(default_factory=list)
    concept_tags: list[str] = field(default_factory=list)
    narrative: str = ""
    contradictions: list[str] = field(default_factory=list)
    insights: list[str] = field(default_factory=list)
    candidate_count: int = 0


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

LIGHT_SLEEP_PROMPT = """\
You are performing cognitive light sleep — extracting the most important snippets \
from recent agent activity for deeper processing.

## Recent Commit Summaries (newest first)
{commit_summaries}

## Instructions
Extract the top {max_candidates} most important ideas, patterns, or insights from \
these commits. For each, provide:

1. A concise content summary (1-2 sentences)
2. Topic keywords (3-5 words)
3. A relevance score (0.0-1.0) — how useful for future tasks?

Respond with ONLY valid JSON:
{{
  "candidates": [
    {{
      "content": "...",
      "topic_keywords": ["word1", "word2"],
      "relevance_score": 0.0,
      "source_commit_index": 0
    }}
  ]
}}
"""

REM_SLEEP_PROMPT = """\
You are performing cognitive REM sleep — deep reflection and consolidation of \
knowledge from multiple agent sessions.

## Promoted Dream Candidates
{candidates_json}

## Instructions
Perform deep consolidation:

1. **Concept tags**: Extract the top {tag_limit} abstract concepts that span \
   multiple candidates (not just keywords — conceptual themes).
2. **Contradictions**: Identify any candidates that contradict each other.
3. **Insights**: Synthesize cross-cutting insights that combine knowledge from \
   multiple candidates in novel ways.
4. **Narrative**: Write a 2-3 paragraph "dream diary" entry summarizing the \
   consolidated knowledge. This should read as a natural reflection, not a list.

Respond with ONLY valid JSON:
{{
  "concept_tags": ["tag1", "tag2"],
  "contradictions": ["Candidate X says A but candidate Y says B"],
  "insights": ["By combining X and Y, we can conclude Z"],
  "narrative": "The agent has been working on..."
}}
"""


# ---------------------------------------------------------------------------
# Dreaming Engine
# ---------------------------------------------------------------------------


class DreamingEngine:
    """
    Implements the two-phase cognitive consolidation cycle.

    Designed to be called on a schedule (e.g., cron, or after every N commits)
    or manually via ``cvc dream``.
    """

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = cvc_root
        self.dreams_dir = cvc_root / "dreams"
        self.dreams_dir.mkdir(parents=True, exist_ok=True)

    # -- Phase 1: Light Sleep -----------------------------------------------

    def compute_recency_score(self, commit_timestamp: float, now: float | None = None) -> float:
        """Exponential decay with configurable half-life."""
        now = now or time.time()
        age_days = (now - commit_timestamp) / 86400.0
        return math.exp(-0.693 * age_days / RECENCY_HALF_LIFE_DAYS)

    def compute_frequency_score(
        self,
        topic_keywords: list[str],
        all_keywords: dict[str, int],
    ) -> float:
        """How often these keywords appear across all commits."""
        if not topic_keywords or not all_keywords:
            return 0.0
        max_freq = max(all_keywords.values()) if all_keywords else 1
        avg_freq = sum(all_keywords.get(k, 0) for k in topic_keywords) / len(topic_keywords)
        return min(1.0, avg_freq / max(max_freq, 1))

    def compute_diversity_score(
        self,
        topic_keywords: list[str],
        already_promoted: list[DreamCandidate],
    ) -> float:
        """Reward candidates that cover topics not already promoted."""
        if not already_promoted:
            return 1.0  # First candidate is always maximally diverse
        existing_keywords: set[str] = set()
        for c in already_promoted:
            existing_keywords.update(c.topic_keywords)
        if not topic_keywords:
            return 0.0
        novel = sum(1 for k in topic_keywords if k not in existing_keywords)
        return novel / len(topic_keywords)

    def score_candidate(
        self,
        candidate: DreamCandidate,
        all_keywords: dict[str, int],
        already_promoted: list[DreamCandidate],
    ) -> float:
        """Compute composite score for a dream candidate."""
        frequency = self.compute_frequency_score(candidate.topic_keywords, all_keywords)
        diversity = self.compute_diversity_score(candidate.topic_keywords, already_promoted)

        candidate.frequency_score = frequency
        candidate.diversity_score = diversity

        # Weighted composite (matches OpenClaw's scoring weights)
        composite = (
            frequency * 0.24
            + candidate.relevance_score * 0.30
            + diversity * 0.15
            + candidate.recency_score * 0.15
            + 0.10  # consolidation baseline
            + 0.06  # conceptual baseline
        )
        candidate.composite_score = composite
        return composite

    def build_light_sleep_prompt(
        self,
        commits: list[Any],  # list[CognitiveCommit]
        max_candidates: int = MAX_DREAM_CANDIDATES,
    ) -> str:
        """Build the LLM prompt for light sleep extraction."""
        summaries = []
        for i, commit in enumerate(commits[:50]):  # Cap at 50 commits
            msg_count = len(commit.content_blob.messages)
            summary = commit.message[:100] or f"Commit with {msg_count} messages"
            files = list(commit.content_blob.files_written.keys())[:5]
            files_str = ", ".join(files) if files else "none"

            summaries.append(
                f"[{i}] {commit.commit_hash[:8]} "
                f"({time.strftime('%Y-%m-%d', time.localtime(commit.metadata.timestamp))}) "
                f"— {summary} | files: {files_str}"
            )

        return LIGHT_SLEEP_PROMPT.format(
            commit_summaries="\n".join(summaries),
            max_candidates=min(max_candidates, len(commits)),
        )

    def parse_light_sleep_response(
        self,
        response_text: str,
        commits: list[Any],
    ) -> list[DreamCandidate]:
        """Parse light sleep LLM response into candidates."""
        text = response_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:])
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse light sleep response")
            return []

        candidates = []
        now = time.time()
        for item in data.get("candidates", []):
            idx = item.get("source_commit_index", 0)
            if 0 <= idx < len(commits):
                commit = commits[idx]
                candidate = DreamCandidate(
                    source_commit=commit.commit_hash,
                    content=item.get("content", ""),
                    topic_keywords=item.get("topic_keywords", []),
                    relevance_score=float(item.get("relevance_score", 0.5)),
                    recency_score=self.compute_recency_score(commit.metadata.timestamp, now),
                    timestamp=commit.metadata.timestamp,
                )
                candidates.append(candidate)

        return candidates

    # -- Phase 2: REM Sleep -------------------------------------------------

    def build_rem_sleep_prompt(
        self,
        promoted: list[DreamCandidate],
        tag_limit: int = CONCEPT_TAG_LIMIT,
    ) -> str:
        """Build the LLM prompt for REM deep consolidation."""
        candidates_data = [
            {
                "id": c.candidate_id,
                "content": c.content,
                "topic_keywords": c.topic_keywords,
                "score": round(c.composite_score, 3),
                "source_commit": c.source_commit[:8],
            }
            for c in promoted
        ]

        return REM_SLEEP_PROMPT.format(
            candidates_json=json.dumps(candidates_data, indent=2),
            tag_limit=tag_limit,
        )

    def parse_rem_response(
        self,
        response_text: str,
        promoted: list[DreamCandidate],
    ) -> DreamEntry:
        """Parse REM sleep response into a DreamEntry."""
        text = response_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:])
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse REM sleep response")
            return DreamEntry(narrative="REM sleep parsing failed")

        return DreamEntry(
            source_commits=[c.source_commit for c in promoted],
            concept_tags=data.get("concept_tags", [])[:CONCEPT_TAG_LIMIT],
            narrative=data.get("narrative", ""),
            contradictions=data.get("contradictions", []),
            insights=data.get("insights", []),
            candidate_count=len(promoted),
        )

    # -- Persistence --------------------------------------------------------

    def persist_dream(self, dream: DreamEntry) -> Path:
        """Save a dream entry to disk."""
        filename = f"dream_{dream.dream_id}.json"
        path = self.dreams_dir / filename
        path.write_text(
            json.dumps(
                {
                    "dream_id": dream.dream_id,
                    "timestamp": dream.timestamp,
                    "source_commits": dream.source_commits[:20],
                    "concept_tags": dream.concept_tags,
                    "narrative": dream.narrative,
                    "contradictions": dream.contradictions,
                    "insights": dream.insights,
                    "candidate_count": dream.candidate_count,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        logger.info(
            "Persisted dream %s: %d concepts, %d insights, %d contradictions",
            dream.dream_id,
            len(dream.concept_tags),
            len(dream.insights),
            len(dream.contradictions),
        )

        # Also append to DREAMS.md for human-readable audit trail
        self._append_to_dreams_md(dream)

        return path

    def _append_to_dreams_md(self, dream: DreamEntry) -> None:
        """Append a dream to the human-readable DREAMS.md file."""
        dreams_md = self.cvc_root / "DREAMS.md"
        existing = ""
        if dreams_md.exists():
            existing = dreams_md.read_text(encoding="utf-8")
        else:
            existing = "# CVC Dream Diary\n\nCognitive consolidation from DAG dreaming.\n"

        date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(dream.timestamp))
        entry = (
            f"\n---\n"
            f"## Dream: {date_str}\n"
            f"**Concepts**: {', '.join(dream.concept_tags[:10])}\n"
            f"**Sources**: {len(dream.source_commits)} commits\n\n"
            f"{dream.narrative}\n"
        )
        if dream.insights:
            entry += "\n**Insights:**\n"
            for insight in dream.insights:
                entry += f"- {insight}\n"
        if dream.contradictions:
            entry += "\n**Contradictions detected:**\n"
            for contradiction in dream.contradictions:
                entry += f"- ⚠️ {contradiction}\n"

        dreams_md.write_text(existing + entry, encoding="utf-8")

    def load_recent_dreams(self, limit: int = 10) -> list[DreamEntry]:
        """Load the most recent dream entries."""
        dreams = []
        files = sorted(self.dreams_dir.glob("dream_*.json"), reverse=True)
        for f in files[:limit]:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                dreams.append(DreamEntry(**data))
            except Exception as e:
                logger.warning("Failed to load dream %s: %s", f.name, e)
        return dreams

    def get_last_dream_timestamp(self) -> float:
        """Get the timestamp of the most recent dream."""
        dreams = self.load_recent_dreams(limit=1)
        return dreams[0].timestamp if dreams else 0.0

    # ------------------------------------------------------------------
    # Orchestrator — the full dream cycle
    # ------------------------------------------------------------------

    async def run_dream_cycle(
        self,
        commits: list[Any],
        adapter: Any | None = None,
        model: str = "",
    ) -> "DreamEntry | None":
        """Run a complete two-phase dreaming cycle.

        Phase 1 (Light Sleep): Extract candidates from recent commits
        using the LLM. Score and promote the best ones.

        Phase 2 (REM Sleep): Deep consolidation of promoted candidates.
        Extract cross-cutting concepts, contradictions, and insights.
        Write a narrative dream diary entry.

        Persists the dream to ``.cvc/dreams/`` and ``DREAMS.md``.

        Args:
            commits: Recent CognitiveCommit objects to dream about.
            adapter: LLM adapter for making completion calls. If None,
                     returns None (can't dream without a brain).
            model: Model name to use for the LLM calls.

        Returns:
            DreamEntry if the dream completed successfully, None if
            there weren't enough commits or the LLM wasn't available.
        """
        if not commits or len(commits) < 3:
            logger.info("dreaming: not enough commits to dream (need ≥3, got %d)", len(commits))
            return None

        if adapter is None:
            logger.info("dreaming: no LLM adapter — skipping dream cycle")
            return None

        logger.info("dreaming: starting cycle with %d commits", len(commits))

        # ── Phase 1: Light Sleep ────────────────────────────────────
        light_prompt = self.build_light_sleep_prompt(commits)
        try:
            from cvc.core.models import ChatCompletionRequest, ChatMessage
            light_response = await adapter.complete(
                ChatCompletionRequest(
                    model=model,
                    messages=[ChatMessage(role="user", content=light_prompt)],
                    max_tokens=1500,
                )
            )
        except Exception as exc:
            logger.warning("dreaming: light sleep LLM call failed: %s", exc)
            return None

        if not light_response.choices:
            logger.warning("dreaming: light sleep returned no choices")
            return None

        candidates = self.parse_light_sleep_response(
            light_response.choices[0].message.content,
            commits,
        )

        if not candidates:
            logger.info("dreaming: light sleep produced no candidates")
            return None

        # Build keyword frequency map for scoring
        all_keywords: dict[str, int] = {}
        for c in candidates:
            for kw in c.topic_keywords:
                all_keywords[kw.lower()] = all_keywords.get(kw.lower(), 0) + 1

        # Score and promote candidates above threshold
        promoted: list[DreamCandidate] = []
        for candidate in candidates:
            score = self.score_candidate(candidate, all_keywords, promoted)
            if score >= MIN_PROMOTION_SCORE:
                promoted.append(candidate)

        # If nothing cleared the threshold, take the top 5 by composite score
        if not promoted:
            candidates.sort(key=lambda c: c.composite_score, reverse=True)
            promoted = candidates[:5]
            logger.info(
                "dreaming: no candidates above threshold (%.2f); taking top %d",
                MIN_PROMOTION_SCORE,
                len(promoted),
            )

        logger.info(
            "dreaming: promoted %d/%d candidates for REM sleep",
            len(promoted),
            len(candidates),
        )

        # ── Phase 2: REM Sleep ──────────────────────────────────────
        rem_prompt = self.build_rem_sleep_prompt(promoted)
        try:
            rem_response = await adapter.complete(
                ChatCompletionRequest(
                    model=model,
                    messages=[ChatMessage(role="user", content=rem_prompt)],
                    max_tokens=1200,
                )
            )
        except Exception as exc:
            logger.warning("dreaming: REM sleep LLM call failed: %s", exc)
            return None

        if not rem_response.choices:
            logger.warning("dreaming: REM sleep returned no choices")
            return None

        dream = self.parse_rem_response(
            rem_response.choices[0].message.content,
            promoted,
        )

        # Persist the dream
        dream_path = self.persist_dream(dream)
        logger.info(
            "dreaming: cycle complete — dream %s persisted to %s",
            dream.dream_id,
            dream_path,
        )

        return dream
