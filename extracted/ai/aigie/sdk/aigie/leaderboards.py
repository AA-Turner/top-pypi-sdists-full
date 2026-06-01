"""
Leaderboards for model and prompt comparison.

Provides tools to rank and compare models, prompts, and configurations
based on various metrics like quality, cost, and latency.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any
from uuid import uuid4


class RankingMetric(Enum):
    """Metrics used for ranking."""

    QUALITY_SCORE = "quality_score"
    ACCURACY = "accuracy"
    LATENCY_AVG = "latency_avg"
    LATENCY_P50 = "latency_p50"
    LATENCY_P90 = "latency_p90"
    LATENCY_P99 = "latency_p99"
    COST_PER_REQUEST = "cost_per_request"
    COST_TOTAL = "cost_total"
    TOKENS_PER_REQUEST = "tokens_per_request"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    SUCCESS_RATE = "success_rate"
    HUMAN_PREFERENCE = "human_preference"
    WIN_RATE = "win_rate"
    ELO_RATING = "elo_rating"
    CUSTOM = "custom"


class AggregationType(Enum):
    """How to aggregate metrics."""

    AVERAGE = "average"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    MEDIAN = "median"
    P90 = "p90"
    P99 = "p99"
    COUNT = "count"
    LATEST = "latest"


@dataclass
class LeaderboardEntry:
    """An entry in a leaderboard."""

    id: str
    rank: int
    name: str
    category: str  # e.g., "model", "prompt", "configuration"

    # Identifiers
    model: str | None = None
    provider: str | None = None
    prompt_id: str | None = None
    configuration: dict[str, Any] | None = None

    # Metrics
    primary_score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)

    # Statistics
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0

    # Comparison
    rank_change: int = 0  # Positive = improved, negative = dropped
    previous_rank: int | None = None

    # Metadata
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "rank": self.rank,
            "name": self.name,
            "category": self.category,
            "model": self.model,
            "provider": self.provider,
            "prompt_id": self.prompt_id,
            "configuration": self.configuration,
            "primary_score": self.primary_score,
            "metrics": self.metrics,
            "total_runs": self.total_runs,
            "successful_runs": self.successful_runs,
            "failed_runs": self.failed_runs,
            "success_rate": self.successful_runs / self.total_runs if self.total_runs > 0 else 0,
            "rank_change": self.rank_change,
            "previous_rank": self.previous_rank,
            "tags": self.tags,
            "metadata": self.metadata,
            "last_updated": self.last_updated.isoformat(),
        }


@dataclass
class ComparisonPair:
    """A head-to-head comparison between two entries."""

    id: str
    entry_a_id: str
    entry_b_id: str

    # Results
    winner_id: str | None = None  # None for tie
    score_a: float | None = None
    score_b: float | None = None

    # Context
    prompt_used: str | None = None
    input_data: dict[str, Any] | None = None

    # Judgment
    judged_by: str = "auto"  # "auto", "human", "llm"
    judge_model: str | None = None
    judge_reasoning: str | None = None
    human_annotator: str | None = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "entry_a_id": self.entry_a_id,
            "entry_b_id": self.entry_b_id,
            "winner_id": self.winner_id,
            "score_a": self.score_a,
            "score_b": self.score_b,
            "prompt_used": self.prompt_used,
            "input_data": self.input_data,
            "judged_by": self.judged_by,
            "judge_model": self.judge_model,
            "judge_reasoning": self.judge_reasoning,
            "human_annotator": self.human_annotator,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class EloRating:
    """ELO rating for an entry."""

    entry_id: str
    rating: float = 1500.0
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    ties: int = 0
    history: list[tuple[datetime, float]] = field(default_factory=list)

    def win_rate(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.wins / self.games_played

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "rating": self.rating,
            "games_played": self.games_played,
            "wins": self.wins,
            "losses": self.losses,
            "ties": self.ties,
            "win_rate": self.win_rate(),
            "history": [(dt.isoformat(), r) for dt, r in self.history[-100:]],
        }


@dataclass
class Leaderboard:
    """A leaderboard for comparing entries."""

    id: str
    name: str
    description: str | None

    # Configuration
    category: str  # "models", "prompts", "configurations"
    primary_metric: RankingMetric
    aggregation: AggregationType = AggregationType.AVERAGE
    higher_is_better: bool = True

    # Entries
    entries: dict[str, LeaderboardEntry] = field(default_factory=dict)

    # ELO ratings (for head-to-head comparisons)
    elo_ratings: dict[str, EloRating] = field(default_factory=dict)
    comparisons: list[ComparisonPair] = field(default_factory=list)

    # Settings
    min_runs_for_ranking: int = 10
    recalculate_interval_hours: int = 1
    include_confidence_intervals: bool = True

    # Metadata
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_calculated: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "primary_metric": self.primary_metric.value,
            "aggregation": self.aggregation.value,
            "higher_is_better": self.higher_is_better,
            "entries_count": len(self.entries),
            "comparisons_count": len(self.comparisons),
            "min_runs_for_ranking": self.min_runs_for_ranking,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_calculated": self.last_calculated.isoformat() if self.last_calculated else None,
        }


class LeaderboardManager:
    """
    Manages leaderboards for model and prompt comparison.

    Usage:
        manager = LeaderboardManager(client)

        # Create a model leaderboard
        leaderboard = manager.create_leaderboard(
            name="GPT vs Claude",
            category="models",
            primary_metric=RankingMetric.QUALITY_SCORE,
        )

        # Add entries
        manager.add_entry(
            leaderboard_id=leaderboard.id,
            name="GPT-4",
            model="gpt-4",
            provider="openai",
        )
        manager.add_entry(
            leaderboard_id=leaderboard.id,
            name="Claude 3 Opus",
            model="claude-3-opus",
            provider="anthropic",
        )

        # Record metrics
        manager.record_metric(
            leaderboard_id=leaderboard.id,
            entry_name="GPT-4",
            metrics={"quality_score": 0.95, "latency_avg": 1200},
        )

        # Get rankings
        rankings = manager.get_rankings(leaderboard.id)

        # Run head-to-head comparison
        comparison = await manager.compare_entries(
            leaderboard_id=leaderboard.id,
            entry_a="GPT-4",
            entry_b="Claude 3 Opus",
            prompt="Explain quantum computing",
        )
    """

    def __init__(self, client: Any | None = None):
        self._client = client
        self._leaderboards: dict[str, Leaderboard] = {}
        self._metric_history: dict[str, list[dict[str, Any]]] = {}  # entry_id -> metrics over time

    # =========================================================================
    # Leaderboard Management
    # =========================================================================

    def create_leaderboard(
        self,
        name: str,
        category: str = "models",
        primary_metric: RankingMetric = RankingMetric.QUALITY_SCORE,
        aggregation: AggregationType = AggregationType.AVERAGE,
        higher_is_better: bool = True,
        description: str | None = None,
        min_runs_for_ranking: int = 10,
        tags: list[str] | None = None,
    ) -> Leaderboard:
        """Create a new leaderboard."""
        leaderboard = Leaderboard(
            id=str(uuid4()),
            name=name,
            description=description,
            category=category,
            primary_metric=primary_metric,
            aggregation=aggregation,
            higher_is_better=higher_is_better,
            min_runs_for_ranking=min_runs_for_ranking,
            tags=tags or [],
        )
        self._leaderboards[leaderboard.id] = leaderboard
        return leaderboard

    def get_leaderboard(self, leaderboard_id: str) -> Leaderboard | None:
        """Get a leaderboard by ID."""
        return self._leaderboards.get(leaderboard_id)

    def get_leaderboard_by_name(self, name: str) -> Leaderboard | None:
        """Get a leaderboard by name."""
        for lb in self._leaderboards.values():
            if lb.name == name:
                return lb
        return None

    def list_leaderboards(
        self,
        category: str | None = None,
        tags: list[str] | None = None,
    ) -> list[Leaderboard]:
        """List leaderboards with optional filtering."""
        leaderboards = list(self._leaderboards.values())

        if category:
            leaderboards = [lb for lb in leaderboards if lb.category == category]

        if tags:
            leaderboards = [lb for lb in leaderboards if any(t in lb.tags for t in tags)]

        return leaderboards

    def delete_leaderboard(self, leaderboard_id: str) -> bool:
        """Delete a leaderboard."""
        if leaderboard_id in self._leaderboards:
            del self._leaderboards[leaderboard_id]
            return True
        return False

    # =========================================================================
    # Entry Management
    # =========================================================================

    def add_entry(
        self,
        leaderboard_id: str,
        name: str,
        model: str | None = None,
        provider: str | None = None,
        prompt_id: str | None = None,
        configuration: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LeaderboardEntry | None:
        """Add an entry to a leaderboard."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return None

        entry = LeaderboardEntry(
            id=str(uuid4()),
            rank=len(leaderboard.entries) + 1,
            name=name,
            category=leaderboard.category,
            model=model,
            provider=provider,
            prompt_id=prompt_id,
            configuration=configuration or {},
            tags=tags or [],
            metadata=metadata or {},
        )

        leaderboard.entries[entry.id] = entry

        # Initialize ELO rating
        leaderboard.elo_ratings[entry.id] = EloRating(entry_id=entry.id)

        leaderboard.updated_at = datetime.utcnow()
        return entry

    def get_entry(
        self,
        leaderboard_id: str,
        entry_id: str | None = None,
        entry_name: str | None = None,
    ) -> LeaderboardEntry | None:
        """Get an entry by ID or name."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return None

        if entry_id:
            return leaderboard.entries.get(entry_id)

        if entry_name:
            for entry in leaderboard.entries.values():
                if entry.name == entry_name:
                    return entry

        return None

    def remove_entry(self, leaderboard_id: str, entry_id: str) -> bool:
        """Remove an entry from a leaderboard."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return False

        if entry_id in leaderboard.entries:
            del leaderboard.entries[entry_id]
            if entry_id in leaderboard.elo_ratings:
                del leaderboard.elo_ratings[entry_id]
            leaderboard.updated_at = datetime.utcnow()
            return True

        return False

    # =========================================================================
    # Metric Recording
    # =========================================================================

    def record_metric(
        self,
        leaderboard_id: str,
        entry_name: str,
        metrics: dict[str, float],
        success: bool = True,
        timestamp: datetime | None = None,
    ) -> bool:
        """Record metrics for an entry."""
        entry = self.get_entry(leaderboard_id, entry_name=entry_name)
        if not entry:
            return False

        timestamp = timestamp or datetime.utcnow()

        # Update entry metrics
        for key, value in metrics.items():
            if key in entry.metrics:
                # Rolling average
                entry.metrics[key] = (entry.metrics[key] * entry.total_runs + value) / (
                    entry.total_runs + 1
                )
            else:
                entry.metrics[key] = value

        entry.total_runs += 1
        if success:
            entry.successful_runs += 1
        else:
            entry.failed_runs += 1

        entry.last_updated = timestamp

        # Store in history
        history_key = f"{leaderboard_id}:{entry.id}"
        if history_key not in self._metric_history:
            self._metric_history[history_key] = []
        self._metric_history[history_key].append(
            {
                "timestamp": timestamp,
                "metrics": metrics,
                "success": success,
            }
        )

        # Keep history manageable
        if len(self._metric_history[history_key]) > 10000:
            self._metric_history[history_key] = self._metric_history[history_key][-5000:]

        return True

    def record_comparison(
        self,
        leaderboard_id: str,
        entry_a_name: str,
        entry_b_name: str,
        winner_name: str | None = None,  # None for tie
        score_a: float | None = None,
        score_b: float | None = None,
        prompt_used: str | None = None,
        judged_by: str = "auto",
        judge_model: str | None = None,
        judge_reasoning: str | None = None,
        human_annotator: str | None = None,
    ) -> ComparisonPair | None:
        """Record a head-to-head comparison."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return None

        entry_a = self.get_entry(leaderboard_id, entry_name=entry_a_name)
        entry_b = self.get_entry(leaderboard_id, entry_name=entry_b_name)

        if not entry_a or not entry_b:
            return None

        winner_id = None
        if winner_name:
            winner = self.get_entry(leaderboard_id, entry_name=winner_name)
            if winner:
                winner_id = winner.id

        comparison = ComparisonPair(
            id=str(uuid4()),
            entry_a_id=entry_a.id,
            entry_b_id=entry_b.id,
            winner_id=winner_id,
            score_a=score_a,
            score_b=score_b,
            prompt_used=prompt_used,
            judged_by=judged_by,
            judge_model=judge_model,
            judge_reasoning=judge_reasoning,
            human_annotator=human_annotator,
        )

        leaderboard.comparisons.append(comparison)

        # Update ELO ratings
        self._update_elo(leaderboard, entry_a.id, entry_b.id, winner_id)

        leaderboard.updated_at = datetime.utcnow()
        return comparison

    def _update_elo(
        self,
        leaderboard: Leaderboard,
        entry_a_id: str,
        entry_b_id: str,
        winner_id: str | None,
        k_factor: float = 32.0,
    ):
        """Update ELO ratings based on a comparison result."""
        elo_a = leaderboard.elo_ratings.get(entry_a_id)
        elo_b = leaderboard.elo_ratings.get(entry_b_id)

        if not elo_a or not elo_b:
            return

        # Calculate expected scores
        expected_a = 1 / (1 + 10 ** ((elo_b.rating - elo_a.rating) / 400))
        expected_b = 1 - expected_a

        # Actual scores
        if winner_id == entry_a_id:
            actual_a, actual_b = 1.0, 0.0
            elo_a.wins += 1
            elo_b.losses += 1
        elif winner_id == entry_b_id:
            actual_a, actual_b = 0.0, 1.0
            elo_a.losses += 1
            elo_b.wins += 1
        else:  # Tie
            actual_a, actual_b = 0.5, 0.5
            elo_a.ties += 1
            elo_b.ties += 1

        # Update ratings
        now = datetime.utcnow()
        elo_a.rating += k_factor * (actual_a - expected_a)
        elo_a.games_played += 1
        elo_a.history.append((now, elo_a.rating))

        elo_b.rating += k_factor * (actual_b - expected_b)
        elo_b.games_played += 1
        elo_b.history.append((now, elo_b.rating))

    # =========================================================================
    # Rankings
    # =========================================================================

    def calculate_rankings(self, leaderboard_id: str) -> list[LeaderboardEntry]:
        """Calculate and update rankings for a leaderboard."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return []

        entries = list(leaderboard.entries.values())

        # Filter entries with enough runs
        qualified = [e for e in entries if e.total_runs >= leaderboard.min_runs_for_ranking]
        unqualified = [e for e in entries if e.total_runs < leaderboard.min_runs_for_ranking]

        # Calculate primary score for each entry
        for entry in qualified:
            metric_key = leaderboard.primary_metric.value
            if metric_key in entry.metrics:
                entry.primary_score = entry.metrics[metric_key]
            elif leaderboard.primary_metric == RankingMetric.ELO_RATING:
                elo = leaderboard.elo_ratings.get(entry.id)
                entry.primary_score = elo.rating if elo else 1500.0
            elif leaderboard.primary_metric == RankingMetric.WIN_RATE:
                elo = leaderboard.elo_ratings.get(entry.id)
                entry.primary_score = elo.win_rate() if elo else 0.0

        # Sort by primary score
        qualified.sort(
            key=lambda e: e.primary_score,
            reverse=leaderboard.higher_is_better,
        )

        # Assign ranks
        for i, entry in enumerate(qualified):
            entry.previous_rank = entry.rank
            entry.rank = i + 1
            entry.rank_change = entry.previous_rank - entry.rank if entry.previous_rank else 0

        # Unqualified entries get rank = None effectively (high rank number)
        for entry in unqualified:
            entry.previous_rank = entry.rank
            entry.rank = len(qualified) + 1
            entry.rank_change = 0

        leaderboard.last_calculated = datetime.utcnow()
        leaderboard.updated_at = datetime.utcnow()

        return qualified

    def get_rankings(
        self,
        leaderboard_id: str,
        limit: int | None = None,
        include_unqualified: bool = False,
    ) -> list[LeaderboardEntry]:
        """Get current rankings for a leaderboard."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return []

        # Recalculate if needed
        if (
            leaderboard.last_calculated is None
            or datetime.utcnow() - leaderboard.last_calculated
            > timedelta(hours=leaderboard.recalculate_interval_hours)
        ):
            self.calculate_rankings(leaderboard_id)

        entries = sorted(leaderboard.entries.values(), key=lambda e: e.rank)

        if not include_unqualified:
            entries = [e for e in entries if e.total_runs >= leaderboard.min_runs_for_ranking]

        if limit:
            entries = entries[:limit]

        return entries

    def get_entry_rank(
        self,
        leaderboard_id: str,
        entry_name: str,
    ) -> int | None:
        """Get the rank of a specific entry."""
        rankings = self.get_rankings(leaderboard_id)
        for entry in rankings:
            if entry.name == entry_name:
                return entry.rank
        return None

    # =========================================================================
    # Analysis
    # =========================================================================

    def get_head_to_head(
        self,
        leaderboard_id: str,
        entry_a_name: str,
        entry_b_name: str,
    ) -> dict[str, Any]:
        """Get head-to-head statistics between two entries."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return {}

        entry_a = self.get_entry(leaderboard_id, entry_name=entry_a_name)
        entry_b = self.get_entry(leaderboard_id, entry_name=entry_b_name)

        if not entry_a or not entry_b:
            return {}

        # Filter comparisons between these entries
        comparisons = [
            c
            for c in leaderboard.comparisons
            if (c.entry_a_id == entry_a.id and c.entry_b_id == entry_b.id)
            or (c.entry_a_id == entry_b.id and c.entry_b_id == entry_a.id)
        ]

        a_wins = sum(1 for c in comparisons if c.winner_id == entry_a.id)
        b_wins = sum(1 for c in comparisons if c.winner_id == entry_b.id)
        ties = len(comparisons) - a_wins - b_wins

        elo_a = leaderboard.elo_ratings.get(entry_a.id)
        elo_b = leaderboard.elo_ratings.get(entry_b.id)

        return {
            "entry_a": entry_a_name,
            "entry_b": entry_b_name,
            "total_comparisons": len(comparisons),
            "a_wins": a_wins,
            "b_wins": b_wins,
            "ties": ties,
            "a_win_rate": a_wins / len(comparisons) if comparisons else 0,
            "b_win_rate": b_wins / len(comparisons) if comparisons else 0,
            "elo_a": elo_a.rating if elo_a else 1500,
            "elo_b": elo_b.rating if elo_b else 1500,
            "elo_diff": (elo_a.rating if elo_a else 1500) - (elo_b.rating if elo_b else 1500),
        }

    def get_metric_trends(
        self,
        leaderboard_id: str,
        entry_name: str,
        metric: str,
        days: int = 7,
    ) -> list[dict[str, Any]]:
        """Get metric trends over time for an entry."""
        entry = self.get_entry(leaderboard_id, entry_name=entry_name)
        if not entry:
            return []

        history_key = f"{leaderboard_id}:{entry.id}"
        history = self._metric_history.get(history_key, [])

        cutoff = datetime.utcnow() - timedelta(days=days)
        filtered = [h for h in history if h["timestamp"] >= cutoff]

        return [
            {
                "timestamp": h["timestamp"].isoformat(),
                "value": h["metrics"].get(metric),
            }
            for h in filtered
            if metric in h["metrics"]
        ]

    def get_leaderboard_summary(self, leaderboard_id: str) -> dict[str, Any]:
        """Get a summary of the leaderboard."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return {}

        rankings = self.get_rankings(leaderboard_id, limit=10)

        return {
            "id": leaderboard.id,
            "name": leaderboard.name,
            "category": leaderboard.category,
            "primary_metric": leaderboard.primary_metric.value,
            "total_entries": len(leaderboard.entries),
            "total_comparisons": len(leaderboard.comparisons),
            "top_10": [
                {
                    "rank": e.rank,
                    "name": e.name,
                    "score": e.primary_score,
                    "runs": e.total_runs,
                }
                for e in rankings
            ],
            "last_updated": leaderboard.updated_at.isoformat(),
        }

    # =========================================================================
    # Export
    # =========================================================================

    def export_leaderboard(
        self,
        leaderboard_id: str,
        format: str = "json",
    ) -> str:
        """Export a leaderboard to a format."""
        leaderboard = self._leaderboards.get(leaderboard_id)
        if not leaderboard:
            return ""

        rankings = self.get_rankings(leaderboard_id, include_unqualified=True)

        data = {
            "leaderboard": leaderboard.to_dict(),
            "rankings": [e.to_dict() for e in rankings],
            "elo_ratings": {eid: elo.to_dict() for eid, elo in leaderboard.elo_ratings.items()},
            "comparisons": [c.to_dict() for c in leaderboard.comparisons[-1000:]],
        }

        if format == "json":
            return json.dumps(data, indent=2)
        if format == "jsonl":
            return "\n".join(json.dumps({"entry": e.to_dict()}) for e in rankings)
        raise ValueError(f"Unsupported format: {format}")


# Convenience functions
def create_leaderboard_manager(client: Any | None = None) -> LeaderboardManager:
    """Create a new leaderboard manager."""
    return LeaderboardManager(client)


def create_model_leaderboard(
    manager: LeaderboardManager,
    name: str = "Model Comparison",
    metric: RankingMetric = RankingMetric.QUALITY_SCORE,
) -> Leaderboard:
    """Create a leaderboard for comparing models."""
    return manager.create_leaderboard(
        name=name,
        category="models",
        primary_metric=metric,
        description="Compare LLM models on quality, latency, and cost",
    )


def create_prompt_leaderboard(
    manager: LeaderboardManager,
    name: str = "Prompt Comparison",
    metric: RankingMetric = RankingMetric.QUALITY_SCORE,
) -> Leaderboard:
    """Create a leaderboard for comparing prompts."""
    return manager.create_leaderboard(
        name=name,
        category="prompts",
        primary_metric=metric,
        description="Compare prompt templates on effectiveness",
    )
