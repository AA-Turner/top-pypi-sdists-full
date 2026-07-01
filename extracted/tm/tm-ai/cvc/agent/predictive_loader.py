"""
cvc.agent.predictive_loader — Predictive Context Preloader (PCP).

Uses commit history + user model + time-of-day patterns to PREDICT what
context the agent will need before the user asks. Pre-loads relevant
memories, skills, and file contexts into working memory.

Key innovation: No agent system does proactive context assembly.
They all wait for the user to ask. CVC predicts and pre-caches,
reducing latency and improving quality of first responses.

Prediction signals:
  - Recent commit topics (what was the user working on?)
  - User model preferences (what tools/languages/patterns?)
  - Time-of-day patterns (morning = planning, afternoon = coding?)
  - Day-of-week patterns (Monday = reviews, Friday = deployments?)
  - Branch context (what is the current branch about?)
  - Season/recency (what files were recently modified?)
"""

from __future__ import annotations

import json
import logging
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.predictive_loader")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class PredictedContext:
    """Predicted context that should be pre-loaded."""

    prediction_id: str = ""
    timestamp: float = field(default_factory=time.time)
    confidence: float = 0.0  # 0.0–1.0

    # Predicted needs
    likely_topics: list[str] = field(default_factory=list)
    relevant_skills: list[str] = field(default_factory=list)
    relevant_files: list[str] = field(default_factory=list)
    relevant_memories: list[str] = field(default_factory=list)  # Memory entry summaries
    suggested_branch: str | None = None

    # Pre-loaded context text for prompt injection
    preloaded_context: str = ""

    # Prediction rationale (for debugging)
    rationale: str = ""


@dataclass
class ActivityPattern:
    """Tracked pattern of time-based user activity."""

    hour_topics: dict[int, list[str]] = field(default_factory=dict)  # hour → [topics]
    weekday_topics: dict[int, list[str]] = field(default_factory=dict)  # 0=Mon → [topics]
    recent_files: list[str] = field(default_factory=list)
    recent_branches: list[str] = field(default_factory=list)
    topic_frequency: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Predictive Context Preloader
# ---------------------------------------------------------------------------


class PredictiveContextPreloader:
    """
    Analyzes commit patterns to predict and pre-load context.

    Called at session startup to front-load relevant context before
    the user types anything.
    """

    PATTERNS_FILE = "activity_patterns.json"

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = cvc_root
        self._patterns_path = cvc_root / self.PATTERNS_FILE

    def analyze_commits(
        self,
        commits: list[Any],  # list[CognitiveCommit]
    ) -> ActivityPattern:
        """Extract time-based activity patterns from commit history."""
        pattern = ActivityPattern()

        for commit in commits:
            ts = commit.metadata.timestamp
            local_time = time.localtime(ts)
            hour = local_time.tm_hour
            weekday = local_time.tm_wday  # 0=Monday

            # Extract topics from commit message and file names
            topics = self._extract_topics(commit)

            # Record hour-based patterns
            if hour not in pattern.hour_topics:
                pattern.hour_topics[hour] = []
            pattern.hour_topics[hour].extend(topics)

            # Record weekday patterns
            if weekday not in pattern.weekday_topics:
                pattern.weekday_topics[weekday] = []
            pattern.weekday_topics[weekday].extend(topics)

            # Track file activity
            files = list(commit.content_blob.files_written.keys())
            pattern.recent_files.extend(files)

            # Track topic frequency
            for topic in topics:
                pattern.topic_frequency[topic] = pattern.topic_frequency.get(topic, 0) + 1

        # Deduplicate and limit recent files
        seen: set[str] = set()
        unique_files = []
        for f in reversed(pattern.recent_files):
            if f not in seen:
                seen.add(f)
                unique_files.append(f)
        pattern.recent_files = list(reversed(unique_files[:50]))

        return pattern

    def _extract_topics(self, commit: Any) -> list[str]:
        """Extract topic keywords from a commit."""
        topics: list[str] = []

        # From commit message
        words = commit.message.lower().split()
        # Filter stop words and short words
        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "was",
            "were",
            "are",
            "been",
            "be",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "shall",
            "can",
            "need",
            "to",
            "of",
            "in",
            "for",
            "on",
            "with",
            "at",
            "by",
            "from",
            "as",
            "into",
            "through",
            "during",
            "before",
            "after",
            "and",
            "but",
            "or",
            "not",
            "no",
            "nor",
            "so",
            "yet",
            "both",
            "each",
            "this",
            "that",
            "these",
            "those",
            "it",
            "its",
            "i",
            "we",
            "you",
        }
        topics.extend(w for w in words if len(w) > 3 and w not in stop_words)

        # From file paths
        for path in list(commit.content_blob.files_written.keys())[:5]:
            parts = Path(path).parts
            topics.extend(p.lower() for p in parts if len(p) > 3 and p not in stop_words)

        # From commit type
        topics.append(commit.commit_type.value)

        return topics[:20]  # Cap per commit

    def predict_context(
        self,
        pattern: ActivityPattern,
        current_branch: str,
        user_model_summary: str = "",
    ) -> PredictedContext:
        """
        Predict what context the user will need based on patterns.

        Uses time-of-day, recent activity, and user model to predict.
        """
        now = time.localtime()
        hour = now.tm_hour
        weekday = now.tm_wday

        prediction = PredictedContext()
        rationale_parts: list[str] = []

        # 1. Time-of-day prediction
        hour_topics = pattern.hour_topics.get(hour, [])
        if hour_topics:
            topic_counts = Counter(hour_topics)
            top_topics = [t for t, _ in topic_counts.most_common(5)]
            prediction.likely_topics.extend(top_topics)
            rationale_parts.append(f"Hour {hour} topics: {', '.join(top_topics[:3])}")

        # 2. Day-of-week prediction
        weekday_topics = pattern.weekday_topics.get(weekday, [])
        if weekday_topics:
            topic_counts = Counter(weekday_topics)
            top_topics = [t for t, _ in topic_counts.most_common(5)]
            for t in top_topics:
                if t not in prediction.likely_topics:
                    prediction.likely_topics.append(t)
            day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][weekday]
            rationale_parts.append(f"{day_name} topics: {', '.join(top_topics[:3])}")

        # 3. Recent file activity
        if pattern.recent_files:
            prediction.relevant_files = pattern.recent_files[:10]
            rationale_parts.append(f"Recent files: {len(pattern.recent_files)}")

        # 4. Branch context
        if current_branch != "main":
            prediction.suggested_branch = current_branch
            rationale_parts.append(f"Active branch: {current_branch}")

        # 5. Overall topic frequency
        if pattern.topic_frequency:
            top_global = sorted(
                pattern.topic_frequency.items(),
                key=lambda x: x[1],
                reverse=True,
            )[:5]
            for topic, count in top_global:
                if topic not in prediction.likely_topics:
                    prediction.likely_topics.append(topic)

        # Compute confidence based on data density
        data_points = (
            len(hour_topics)
            + len(weekday_topics)
            + len(pattern.recent_files)
            + len(pattern.topic_frequency)
        )
        prediction.confidence = min(1.0, data_points / 100.0)

        prediction.rationale = "; ".join(rationale_parts)

        # Build preloaded context text
        prediction.preloaded_context = self._build_context_text(prediction, user_model_summary)

        return prediction

    def _build_context_text(
        self,
        prediction: PredictedContext,
        user_model_summary: str,
    ) -> str:
        """Build a context injection string from the prediction."""
        parts: list[str] = []

        if prediction.likely_topics:
            parts.append(
                f"[Predicted topics for this session: {', '.join(prediction.likely_topics[:7])}]"
            )

        if prediction.relevant_files:
            parts.append(f"[Recently active files: {', '.join(prediction.relevant_files[:5])}]")

        if user_model_summary:
            parts.append(f"[User context: {user_model_summary[:200]}]")

        if prediction.suggested_branch and prediction.suggested_branch != "main":
            parts.append(f"[Active branch: {prediction.suggested_branch}]")

        return "\n".join(parts) if parts else ""

    def save_patterns(self, pattern: ActivityPattern) -> None:
        """Persist activity patterns to disk."""
        data = {
            "hour_topics": {str(k): v[-50:] for k, v in pattern.hour_topics.items()},
            "weekday_topics": {str(k): v[-50:] for k, v in pattern.weekday_topics.items()},
            "recent_files": pattern.recent_files[:50],
            "topic_frequency": dict(
                sorted(pattern.topic_frequency.items(), key=lambda x: x[1], reverse=True)[:100]
            ),
            "updated_at": time.time(),
        }
        self._patterns_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load_patterns(self) -> ActivityPattern | None:
        """Load persisted activity patterns."""
        if not self._patterns_path.exists():
            return None
        try:
            data = json.loads(self._patterns_path.read_text(encoding="utf-8"))
            pattern = ActivityPattern()
            pattern.hour_topics = {int(k): v for k, v in data.get("hour_topics", {}).items()}
            pattern.weekday_topics = {int(k): v for k, v in data.get("weekday_topics", {}).items()}
            pattern.recent_files = data.get("recent_files", [])
            pattern.topic_frequency = data.get("topic_frequency", {})
            return pattern
        except Exception as e:
            logger.warning("Failed to load activity patterns: %s", e)
            return None
