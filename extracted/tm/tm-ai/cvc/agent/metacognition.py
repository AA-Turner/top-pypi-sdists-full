"""
cvc.agent.metacognition — Metacognitive Monitor (F10).

Injects periodic self-assessment checkpoints into the agent's
reasoning loop. Every N tool calls, the monitor pauses the agent
to ask: "Am I on track? What have I accomplished? What's blocking me?"

Each checkpoint is versioned as a CVC commit, creating a trail of
self-assessments that can be analyzed to detect recurring failure modes
and improve future performance.

Key concepts:
  - assessment_interval: Default every 15 tool calls
  - MetacognitiveSnapshot: A structured self-assessment
  - drift_detection: Compares current progress to initial goal
  - intervention strategies: pause, refocus, escalate, abort
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.metacognition")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_ASSESSMENT_INTERVAL = 15  # Every N tool calls
DRIFT_THRESHOLD = 0.4  # Goal similarity below this → intervention
MAX_HISTORY = 100  # Keep at most N snapshots per session


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class MetacognitiveSnapshot:
    """A structured self-assessment at a given point."""

    timestamp: float = 0.0
    tool_call_count: int = 0
    original_goal: str = ""
    current_activity: str = ""
    progress_assessment: str = ""
    confidence: float = 0.5  # 0-1 subjective confidence
    drift_detected: bool = False
    intervention: str = ""  # none | refocus | escalate | abort
    reasoning: str = ""
    tools_since_last: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "tool_call_count": self.tool_call_count,
            "original_goal": self.original_goal,
            "current_activity": self.current_activity,
            "progress_assessment": self.progress_assessment,
            "confidence": self.confidence,
            "drift_detected": self.drift_detected,
            "intervention": self.intervention,
            "reasoning": self.reasoning,
            "tools_since_last": self.tools_since_last,
        }


# ---------------------------------------------------------------------------
# Monitor
# ---------------------------------------------------------------------------


class MetacognitiveMonitor:
    """
    Tracks tool calls and injects self-assessment checkpoints.

    Usage:
        monitor = MetacognitiveMonitor(original_goal="Fix the auth module")
        ...
        # On each tool call:
        monitor.record_tool_call("grep_search")
        if monitor.should_assess():
            prompt = monitor.build_assessment_prompt(recent_context)
            # Send to LLM, parse response
            monitor.record_snapshot(snapshot)
    """

    def __init__(
        self,
        original_goal: str = "",
        assessment_interval: int = DEFAULT_ASSESSMENT_INTERVAL,
        cvc_root: Path | None = None,
    ) -> None:
        self.original_goal = original_goal
        self.assessment_interval = assessment_interval
        self.cvc_root = cvc_root
        self.tool_call_count = 0
        self.tools_since_last: list[str] = []
        self.snapshots: list[MetacognitiveSnapshot] = []
        self._last_assessment_at = 0

    def record_tool_call(self, tool_name: str) -> None:
        """Record a tool call. Called in the POST_TOOL_USE hook."""
        self.tool_call_count += 1
        self.tools_since_last.append(tool_name)

    def should_assess(self) -> bool:
        """Check if it's time for a metacognitive assessment."""
        calls_since = self.tool_call_count - self._last_assessment_at
        return calls_since >= self.assessment_interval

    def build_assessment_prompt(self, recent_context: str = "") -> str:
        """
        Build the metacognitive assessment prompt.

        Sent to the LLM to get a self-assessment, which we parse into
        a MetacognitiveSnapshot.
        """
        tools_str = ", ".join(self.tools_since_last[-20:])
        prev_snapshot_str = ""
        if self.snapshots:
            last = self.snapshots[-1]
            prev_snapshot_str = (
                f"\n\nPrevious assessment ({last.tool_call_count} tool calls ago):\n"
                f"- Progress: {last.progress_assessment}\n"
                f"- Confidence: {last.confidence:.0%}\n"
                f"- Intervention: {last.intervention}"
            )

        return f"""You are performing a metacognitive self-assessment. Pause and evaluate.

## Original Goal
{self.original_goal}

## Current State
- Tool calls so far: {self.tool_call_count}
- Recent tools used: {tools_str}
{prev_snapshot_str}

## Recent Context
{recent_context[:2000]}

## Instructions
Respond with ONLY a JSON object:
{{
  "current_activity": "What am I doing right now? (1 sentence)",
  "progress_assessment": "How close am I to the goal? (1-2 sentences)",
  "confidence": 0.0 to 1.0,
  "drift_detected": true/false,
  "intervention": "none" | "refocus" | "escalate" | "abort",
  "reasoning": "Why this assessment? (1-2 sentences)"
}}

- "refocus" = I've drifted from the goal and should return to it
- "escalate" = I'm stuck and need to try a different approach
- "abort" = The task seems impossible or I'm in a loop
- "none" = I'm on track, keep going"""

    def parse_assessment_response(self, llm_response: str) -> MetacognitiveSnapshot:
        """Parse the LLM's self-assessment into a snapshot."""
        snapshot = MetacognitiveSnapshot(
            timestamp=time.time(),
            tool_call_count=self.tool_call_count,
            original_goal=self.original_goal,
            tools_since_last=list(self.tools_since_last),
        )

        try:
            # Strip markdown code fences if present
            text = llm_response.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            data = json.loads(text)
            snapshot.current_activity = data.get("current_activity", "")
            snapshot.progress_assessment = data.get("progress_assessment", "")
            snapshot.confidence = float(data.get("confidence", 0.5))
            snapshot.drift_detected = bool(data.get("drift_detected", False))
            snapshot.intervention = data.get("intervention", "none")
            snapshot.reasoning = data.get("reasoning", "")
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.warning("Failed to parse metacognitive response: %s", e)
            snapshot.current_activity = "Assessment parse failed"
            snapshot.confidence = 0.5
            snapshot.intervention = "none"

        return snapshot

    def record_snapshot(self, snapshot: MetacognitiveSnapshot) -> None:
        """Record a snapshot and reset the tool counter."""
        self.snapshots.append(snapshot)
        if len(self.snapshots) > MAX_HISTORY:
            self.snapshots = self.snapshots[-MAX_HISTORY:]
        self.tools_since_last = []
        self._last_assessment_at = self.tool_call_count

    def get_intervention_message(self, snapshot: MetacognitiveSnapshot) -> str | None:
        """
        Get a user-visible intervention message if the snapshot warrants it.

        Returns None if no intervention needed (intervention == "none").
        """
        if snapshot.intervention == "none":
            return None

        messages = {
            "refocus": (
                f"**Metacognitive Check**: I may have drifted from the goal. "
                f'Original: "{self.original_goal}". '
                f'Current: "{snapshot.current_activity}". '
                f"Refocusing now."
            ),
            "escalate": (
                f"**Metacognitive Check**: I'm having difficulty making progress. "
                f"Assessment: {snapshot.progress_assessment}. "
                f"Trying a different approach."
            ),
            "abort": (
                f"**Metacognitive Check**: This task may need human guidance. "
                f"Assessment: {snapshot.progress_assessment}. "
                f"Confidence: {snapshot.confidence:.0%}."
            ),
        }
        return messages.get(snapshot.intervention)

    def get_session_summary(self) -> dict[str, Any]:
        """Summarize the metacognitive activity for this session."""
        if not self.snapshots:
            return {
                "total_assessments": 0,
                "total_tool_calls": self.tool_call_count,
            }

        confidences = [s.confidence for s in self.snapshots]
        interventions = [s.intervention for s in self.snapshots if s.intervention != "none"]
        drift_count = sum(1 for s in self.snapshots if s.drift_detected)

        return {
            "total_assessments": len(self.snapshots),
            "total_tool_calls": self.tool_call_count,
            "avg_confidence": sum(confidences) / len(confidences),
            "min_confidence": min(confidences),
            "drift_detections": drift_count,
            "interventions": interventions,
            "final_assessment": self.snapshots[-1].progress_assessment,
        }

    def persist_snapshots(self) -> None:
        """Save snapshots to a JSON file in .cvc/metacognition/."""
        if not self.cvc_root or not self.snapshots:
            return

        meta_dir = self.cvc_root / "metacognition"
        meta_dir.mkdir(parents=True, exist_ok=True)

        session_id = f"{int(self.snapshots[0].timestamp)}"
        path = meta_dir / f"session_{session_id}.json"

        data = {
            "original_goal": self.original_goal,
            "total_tool_calls": self.tool_call_count,
            "snapshots": [s.to_dict() for s in self.snapshots],
            "summary": self.get_session_summary(),
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.info("Persisted %d metacognitive snapshots to %s", len(self.snapshots), path)
