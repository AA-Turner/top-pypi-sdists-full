"""
cvc.operations.tournament — Quantum Branch Tournament (QBT).

Extends the existing QuantumExecutor into a competitive tournament.
Spawn N parallel branches, evaluate results with an LLM judge,
promote the winner's reasoning as a skill, and archive losers as
negative examples in ChromaDB.

Key innovation: No other system does competitive parallel reasoning
with negative learning. Failed branches become "what NOT to do"
embeddings, improving future decisions through avoidance learning.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.tournament")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class TournamentEntry:
    """A single branch's performance in the tournament."""

    branch_name: str = ""
    strategy: str = ""
    success: bool = False
    quality_score: float = 0.0  # 0.0–1.0 from LLM judge
    reasoning_summary: str = ""
    error_description: str = ""
    commit_hash: str = ""
    execution_time_s: float = 0.0
    token_cost: float = 0.0


@dataclass
class TournamentResult:
    """Complete results of a quantum tournament."""

    tournament_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    task_name: str = ""
    timestamp: float = field(default_factory=time.time)
    entries: list[TournamentEntry] = field(default_factory=list)
    winner: TournamentEntry | None = None
    skill_extracted: bool = False
    negative_lessons_stored: int = 0

    @property
    def success_rate(self) -> float:
        if not self.entries:
            return 0.0
        return sum(1 for e in self.entries if e.success) / len(self.entries)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

JUDGE_PROMPT = """\
You are a tournament judge evaluating {n_entries} competing solutions to a task.

## Task
{task_description}

## Solutions
{solutions_json}

## Instructions
Evaluate each solution on:
1. **Correctness** (0-1): Does it solve the task?
2. **Efficiency** (0-1): Token cost, execution time, brevity
3. **Quality** (0-1): Code quality, reasoning depth, robustness

Respond with ONLY valid JSON:
{{
  "evaluations": [
    {{
      "branch_name": "...",
      "correctness": 0.0,
      "efficiency": 0.0,
      "quality": 0.0,
      "composite_score": 0.0,
      "reasoning": "Why this score",
      "negative_lesson": "What to avoid from this approach (empty if good)"
    }}
  ],
  "winner": "branch_name_of_best",
  "winner_reasoning": "Why this one is best"
}}
"""

NEGATIVE_LESSON_PROMPT = """\
Summarize the key failure pattern from this approach as a concise rule \
the agent should remember to avoid in the future.

## Failed Approach
Strategy: {strategy}
Error: {error_description}
Reasoning: {reasoning_summary}

Respond with a single sentence starting with "AVOID:" that captures the \
anti-pattern. Example: "AVOID: Using regex to parse HTML when a DOM parser is available."
"""


# ---------------------------------------------------------------------------
# Tournament Engine
# ---------------------------------------------------------------------------


class TournamentEngine:
    """
    Manages quantum branch tournaments with competitive evaluation.

    Works alongside QuantumExecutor but adds:
    - LLM-judged competitive evaluation
    - Negative learning from failed branches
    - Automatic skill extraction from winning strategies
    """

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = cvc_root
        self.tournaments_dir = cvc_root / "tournaments"
        self.tournaments_dir.mkdir(parents=True, exist_ok=True)
        self.negative_lessons_path = cvc_root / "negative_lessons.json"

    def build_judge_prompt(
        self,
        task_description: str,
        entries: list[TournamentEntry],
    ) -> str:
        """Build the LLM judge prompt for tournament evaluation."""
        solutions = []
        for entry in entries:
            solutions.append(
                {
                    "branch_name": entry.branch_name,
                    "strategy": entry.strategy,
                    "success": entry.success,
                    "reasoning_summary": entry.reasoning_summary[:500],
                    "error_description": entry.error_description[:200],
                    "execution_time_s": entry.execution_time_s,
                    "token_cost": entry.token_cost,
                }
            )

        return JUDGE_PROMPT.format(
            n_entries=len(entries),
            task_description=task_description,
            solutions_json=json.dumps(solutions, indent=2),
        )

    def parse_judge_response(
        self,
        response_text: str,
        entries: list[TournamentEntry],
    ) -> TournamentResult:
        """Parse the LLM judge's evaluation."""
        text = response_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:])
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        result = TournamentResult(entries=entries)

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse tournament judge response")
            # Fallback: pick the first successful entry
            for entry in entries:
                if entry.success:
                    result.winner = entry
                    break
            return result

        # Update entry scores from evaluations
        entry_map = {e.branch_name: e for e in entries}
        for eval_data in data.get("evaluations", []):
            branch = eval_data.get("branch_name", "")
            if branch in entry_map:
                entry_map[branch].quality_score = float(eval_data.get("composite_score", 0.0))

        # Find winner
        winner_name = data.get("winner", "")
        if winner_name in entry_map:
            result.winner = entry_map[winner_name]
        else:
            # Fallback to highest scoring entry
            scored = sorted(entries, key=lambda e: e.quality_score, reverse=True)
            if scored:
                result.winner = scored[0]

        return result

    def extract_negative_lessons(
        self,
        result: TournamentResult,
    ) -> list[dict[str, Any]]:
        """
        Extract anti-patterns from losing branches.

        Stored as "negative embeddings" — patterns the agent should
        actively avoid in future similar tasks.
        """
        lessons = []
        if not result.winner:
            return lessons

        for entry in result.entries:
            if entry == result.winner:
                continue
            if entry.error_description or not entry.success:
                lesson = {
                    "lesson_id": uuid.uuid4().hex[:12],
                    "tournament_id": result.tournament_id,
                    "task_name": result.task_name,
                    "failed_strategy": entry.strategy,
                    "error_description": entry.error_description,
                    "branch_name": entry.branch_name,
                    "quality_score": entry.quality_score,
                    "timestamp": time.time(),
                    "lesson_type": "negative",
                }
                lessons.append(lesson)

        return lessons

    def persist_negative_lessons(self, lessons: list[dict[str, Any]]) -> int:
        """Persist negative lessons to disk for future reference."""
        existing: list[dict[str, Any]] = []
        if self.negative_lessons_path.exists():
            try:
                existing = json.loads(self.negative_lessons_path.read_text(encoding="utf-8"))
            except Exception:
                existing = []

        existing.extend(lessons)
        # Keep only the last 200 lessons
        existing = existing[-200:]

        self.negative_lessons_path.write_text(
            json.dumps(existing, indent=2),
            encoding="utf-8",
        )
        logger.info("Persisted %d negative lessons from tournament", len(lessons))
        return len(lessons)

    def persist_tournament(self, result: TournamentResult) -> Path:
        """Save full tournament results for auditing."""
        filename = f"tournament_{result.tournament_id}.json"
        path = self.tournaments_dir / filename
        path.write_text(
            json.dumps(
                {
                    "tournament_id": result.tournament_id,
                    "task_name": result.task_name,
                    "timestamp": result.timestamp,
                    "success_rate": result.success_rate,
                    "winner": {
                        "branch": result.winner.branch_name if result.winner else None,
                        "strategy": result.winner.strategy if result.winner else None,
                        "quality_score": result.winner.quality_score if result.winner else 0,
                    },
                    "entries": [
                        {
                            "branch": e.branch_name,
                            "strategy": e.strategy,
                            "success": e.success,
                            "quality_score": e.quality_score,
                            "error": e.error_description[:200],
                        }
                        for e in result.entries
                    ],
                    "skill_extracted": result.skill_extracted,
                    "negative_lessons_stored": result.negative_lessons_stored,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return path

    def load_negative_lessons(self, task_name: str = "") -> list[dict[str, Any]]:
        """Load negative lessons, optionally filtered by task name."""
        if not self.negative_lessons_path.exists():
            return []
        try:
            lessons = json.loads(self.negative_lessons_path.read_text(encoding="utf-8"))
            if task_name:
                return [
                    entry
                    for entry in lessons
                    if task_name.lower() in entry.get("task_name", "").lower()
                ]
            return lessons
        except Exception:
            return []
