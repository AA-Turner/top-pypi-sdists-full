"""
cvc.operations.prompt_evolution — Self-Evolving System Prompt (SESP).

Inspired by upstream GEPA (Genetic-Pareto Prompt Evolution) but adapted for
CVC's Merkle DAG architecture. Every evolution step is a commit, enabling
automatic rollback if quality metrics drop.

Key differences from upstream:
  - upstream needs human PR review. CVC auto-evolves AND auto-reverts.
  - Every mutation attempt is a commit — full genetic history is traversable.
  - Quality metrics are tracked per-commit; regression triggers rollback.

Evolution loop:
  1. Analyze recent N commits for success/failure patterns
  2. Identify weak spots in the current system prompt
  3. Propose targeted mutations (not random — trace-informed)
  4. Evaluate via quality heuristics (no separate benchmark needed)
  5. Commit winning variant; auto-revert if next M sessions regress
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.prompt_evolution")


# ---------------------------------------------------------------------------
# Quality metrics for prompt evaluation
# ---------------------------------------------------------------------------


@dataclass
class PromptQualityMetrics:
    """Heuristic quality metrics derived from commit history."""

    total_commits: int = 0
    error_rate: float = 0.0  # Fraction of commits with error patterns
    correction_rate: float = 0.0  # Fraction of commits following a user correction
    tool_success_rate: float = 0.0  # Fraction of tool calls that succeeded
    avg_turn_count: float = 0.0  # Average turns to complete tasks
    avg_cost_usd: float = 0.0  # Average cost per commit
    user_satisfaction: float = 0.0  # Proxy: ratio of "thanks"/"good" vs. corrections

    @property
    def composite_score(self) -> float:
        """Single quality score (0–1). Higher is better."""
        if self.total_commits == 0:
            return 0.5  # Neutral for no data
        return (
            (1.0 - self.error_rate) * 0.30
            + (1.0 - self.correction_rate) * 0.25
            + self.tool_success_rate * 0.20
            + min(1.0, 10.0 / max(self.avg_turn_count, 1.0)) * 0.15
            + self.user_satisfaction * 0.10
        )


@dataclass
class PromptVariant:
    """A tracked system prompt variant with its performance history."""

    variant_id: str = ""
    prompt_text: str = ""
    created_at: float = field(default_factory=time.time)
    source_commit: str = ""  # Commit where this variant was introduced
    parent_variant_id: str | None = None  # The variant this was mutated from
    metrics: PromptQualityMetrics = field(default_factory=PromptQualityMetrics)
    active: bool = True
    reverted: bool = False
    revert_reason: str = ""


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

EVOLUTION_ANALYSIS_PROMPT = """\
You are a system prompt evolution engine. Analyze the agent's recent performance \
and propose targeted improvements to the system prompt.

## Current System Prompt Section Under Review
{current_section}

## Recent Performance Data
- Total commits analyzed: {total_commits}
- Error rate: {error_rate:.1%}
- Correction rate: {correction_rate:.1%} (user had to correct the agent)
- Tool success rate: {tool_success_rate:.1%}
- Average turns per task: {avg_turns:.1f}
- Composite quality score: {quality_score:.2f}/1.00

## Error Patterns Observed
{error_patterns}

## Successful Patterns
{success_patterns}

## Instructions
Propose a TARGETED mutation to the system prompt section that addresses the \
observed weaknesses. The mutation should:

1. Fix specific failure patterns (not generic improvements)
2. Preserve strengths (don't break what works)
3. Be minimal — change only what needs changing
4. Include rationale for each change

Respond with ONLY valid JSON:
{{
  "mutation_type": "add_rule|modify_rule|remove_rule|restructure",
  "rationale": "Why this change addresses the observed problems",
  "original_section": "The exact text being replaced",
  "mutated_section": "The improved text",
  "expected_impact": "What metrics should improve",
  "risk_assessment": "low|medium|high"
}}
"""


class PromptEvolutionEngine:
    """
    Manages the evolutionary lifecycle of system prompt sections.

    Each evolution is backed by the CVC Merkle DAG — you can traverse
    the full mutation history and see which variants performed best.
    """

    HISTORY_FILE = "prompt_evolution_history.json"
    QUALITY_WINDOW = 20  # Number of recent commits to evaluate quality
    REGRESSION_THRESHOLD = 0.15  # Quality drop triggering auto-revert
    MIN_COMMITS_FOR_EVOLUTION = 10  # Minimum commits before first evolution

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = cvc_root
        self._history_path = cvc_root / self.HISTORY_FILE

    def compute_quality_metrics(
        self,
        commits: list[Any],  # list[CognitiveCommit]
    ) -> PromptQualityMetrics:
        """Derive quality metrics from a window of recent commits."""
        if not commits:
            return PromptQualityMetrics()

        metrics = PromptQualityMetrics(total_commits=len(commits))

        error_count = 0
        correction_count = 0
        satisfaction_count = 0
        total_turns = 0
        total_cost = 0.0
        tool_success = 0
        tool_total = 0

        for commit in commits:
            blob = commit.content_blob
            meta = commit.metadata

            total_turns += meta.turn_count or 1
            total_cost += meta.cost_usd or 0.0

            # Detect errors in messages
            for msg in blob.messages:
                content_lower = msg.content.lower()
                if msg.role == "assistant" and any(
                    w in content_lower for w in ["error", "failed", "mistake", "sorry, i"]
                ):
                    error_count += 1

                if msg.role == "user" and any(
                    w in content_lower
                    for w in ["no,", "wrong", "that's not", "incorrect", "fix this"]
                ):
                    correction_count += 1

                if msg.role == "user" and any(
                    w in content_lower
                    for w in ["thanks", "perfect", "great", "good job", "exactly"]
                ):
                    satisfaction_count += 1

            # Tool success rate
            for key, value in blob.tool_outputs.items():
                tool_total += 1
                value_str = str(value).lower()
                if "error" not in value_str and "failed" not in value_str:
                    tool_success += 1

        n = len(commits)
        total_msgs = sum(len(c.content_blob.messages) for c in commits) or 1

        metrics.error_rate = error_count / total_msgs
        metrics.correction_rate = correction_count / total_msgs
        metrics.tool_success_rate = tool_success / max(tool_total, 1)
        metrics.avg_turn_count = total_turns / n
        metrics.avg_cost_usd = total_cost / n
        metrics.user_satisfaction = satisfaction_count / total_msgs

        return metrics

    def build_evolution_prompt(
        self,
        current_section: str,
        metrics: PromptQualityMetrics,
        error_patterns: list[str],
        success_patterns: list[str],
    ) -> str:
        """Build the LLM prompt for system prompt evolution."""
        return EVOLUTION_ANALYSIS_PROMPT.format(
            current_section=current_section[:2000],
            total_commits=metrics.total_commits,
            error_rate=metrics.error_rate,
            correction_rate=metrics.correction_rate,
            tool_success_rate=metrics.tool_success_rate,
            avg_turns=metrics.avg_turn_count,
            quality_score=metrics.composite_score,
            error_patterns="\n".join(f"- {p}" for p in error_patterns[:10]) or "None detected",
            success_patterns="\n".join(f"- {p}" for p in success_patterns[:10]) or "None detected",
        )

    def should_evolve(self, commit_count: int, last_evolution_at: float) -> bool:
        """Determine if it's time for a prompt evolution attempt."""
        if commit_count < self.MIN_COMMITS_FOR_EVOLUTION:
            return False
        # Don't evolve more than once per 50 commits
        return commit_count % 50 == 0

    def should_revert(
        self,
        pre_metrics: PromptQualityMetrics,
        post_metrics: PromptQualityMetrics,
    ) -> bool:
        """Check if a recent evolution caused quality regression."""
        if post_metrics.total_commits < 5:
            return False  # Not enough data to judge

        pre_score = pre_metrics.composite_score
        post_score = post_metrics.composite_score
        drop = pre_score - post_score

        if drop > self.REGRESSION_THRESHOLD:
            logger.warning(
                "Quality regression detected: %.2f → %.2f (drop: %.2f). Recommending revert.",
                pre_score,
                post_score,
                drop,
            )
            return True
        return False

    def load_history(self) -> list[PromptVariant]:
        """Load the evolution history."""
        if not self._history_path.exists():
            return []
        try:
            data = json.loads(self._history_path.read_text(encoding="utf-8"))
            return [PromptVariant(**v) for v in data]
        except Exception as e:
            logger.warning("Failed to load evolution history: %s", e)
            return []

    def save_variant(self, variant: PromptVariant) -> None:
        """Append a variant to the evolution history."""
        history = self.load_history()
        history.append(variant)
        self._history_path.write_text(
            json.dumps(
                [
                    {
                        "variant_id": v.variant_id,
                        "prompt_text": v.prompt_text[:5000],  # Cap storage
                        "created_at": v.created_at,
                        "source_commit": v.source_commit,
                        "parent_variant_id": v.parent_variant_id,
                        "active": v.active,
                        "reverted": v.reverted,
                        "revert_reason": v.revert_reason,
                        "metrics": {
                            "total_commits": v.metrics.total_commits,
                            "error_rate": v.metrics.error_rate,
                            "composite_score": v.metrics.composite_score,
                        },
                    }
                    for v in history
                ],
                indent=2,
            ),
            encoding="utf-8",
        )
