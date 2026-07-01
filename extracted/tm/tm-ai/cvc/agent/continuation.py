"""
cvc.agent.continuation — Autopilot continuation engine.

Detects premature LLM stops and injects continuation prompts to keep the
agentic loop running until the task is genuinely complete.

Inspired by:
- Claude Code's Ralph Wiggum stop-hook (self-referential loop with completion signals)
- GitHub Copilot's Autopilot mode (continuous iteration until task complete)
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field

logger = logging.getLogger("cvc.agent.continuation")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Default max iterations when autopilot is active.
# Resolved lazily from CvcAgentConfig so `cvc setup` / `cvc agent-config set` work without
# restarting Python. Env vars still win via the agent_config precedence chain.
def _agent_cfg():
    try:
        from cvc.core.agent_config import get_agent_config
        return get_agent_config()
    except Exception:
        return None


def _autopilot_max_iterations() -> int:
    cfg = _agent_cfg()
    if cfg is not None:
        return int(cfg.autopilot_max_iterations)
    return int(os.environ.get("CVC_AUTOPILOT_MAX_ITERS", "100"))


def _autopilot_hard_cap() -> int:
    cfg = _agent_cfg()
    if cfg is not None:
        return int(cfg.autopilot_hard_cap)
    return 200


def _autopilot_cost_pause() -> float:
    cfg = _agent_cfg()
    if cfg is not None:
        return float(cfg.autopilot_cost_pause)
    return float(os.environ.get("CVC_AUTOPILOT_COST_PAUSE", "5.0"))


# Module-level snapshots for back-compat (re-resolved on each access).
AUTOPILOT_MAX_ITERATIONS = _autopilot_max_iterations()
AUTOPILOT_HARD_CAP = _autopilot_hard_cap()

# Cost warning still env-only (no tunable yet).
AUTOPILOT_COST_WARN = float(os.environ.get("CVC_AUTOPILOT_COST_WARN", "1.0"))
AUTOPILOT_COST_PAUSE = _autopilot_cost_pause()

# Completion signal the LLM is instructed to emit when done
COMPLETION_SIGNAL = "<task_complete/>"

# Phrases that indicate the LLM stopped prematurely instead of continuing
_HEDGING_PATTERNS = [
    r"\blet me know\b",
    r"\bwould you like\b",
    r"\bshall I\b",
    r"\bdo you want\b",
    r"\bnext steps?\s+(?:would|could|might)\s+be\b",
    r"\bI (?:would|could|can)(?: also)?\b.*\bif you(?:'d)?\s+like\b",
    r"\bfeel free to\b",
    r"\bI can also\b",
    r"\bhere(?:'s| is) (?:a |the )?summary\b",
    r"\bthat(?:'s| is) (?:everything|all|it)\b",
]
_HEDGING_RE = re.compile("|".join(_HEDGING_PATTERNS), re.IGNORECASE)


# ---------------------------------------------------------------------------
# Plan Tracker
# ---------------------------------------------------------------------------

@dataclass
class PlanStep:
    """A single step extracted from the agent's plan."""
    index: int
    description: str
    completed: bool = False


@dataclass
class PlanTracker:
    """
    Tracks multi-step plan execution.

    Extracts numbered plans from LLM output and matches tool results
    to plan steps to determine which steps are done.
    """
    steps: list[PlanStep] = field(default_factory=list)

    def extract_plan(self, text: str) -> list[PlanStep]:
        """Parse a numbered plan from LLM response text."""
        plan_match = re.search(
            r'(?:^|\n)\s*(?:Plan|Steps|Approach|Strategy):\s*\n'
            r'((?:\s*\d+[\.\)]\s*.+\n?)+)',
            text,
            re.IGNORECASE | re.MULTILINE,
        )
        if not plan_match:
            return self.steps

        lines = plan_match.group(1).strip().split("\n")
        self.steps = []
        for i, line in enumerate(lines, 1):
            step_match = re.match(r'\s*\d+[\.\)]\s*(.+)', line)
            if step_match:
                self.steps.append(PlanStep(index=i, description=step_match.group(1).strip()))
        return self.steps

    def mark_step_complete(self, step_index: int) -> None:
        """Mark a specific step as completed (1-based index)."""
        for step in self.steps:
            if step.index == step_index:
                step.completed = True
                break

    def match_and_complete(self, tool_name: str, tool_result: str) -> None:
        """Heuristically match a tool result to the next incomplete step."""
        for step in self.steps:
            if step.completed:
                continue
            desc_lower = step.description.lower()
            # Simple heuristic: if tool name or key words appear in step description
            if (tool_name.lower() in desc_lower
                    or any(w in desc_lower for w in _tool_keywords(tool_name))
                    or ("error" not in tool_result.lower()[:100])):
                step.completed = True
                return

    def get_remaining(self) -> list[PlanStep]:
        return [s for s in self.steps if not s.completed]

    def is_complete(self) -> bool:
        return len(self.steps) > 0 and all(s.completed for s in self.steps)

    @property
    def progress_str(self) -> str:
        done = sum(1 for s in self.steps if s.completed)
        total = len(self.steps)
        return f"{done}/{total}" if total > 0 else ""


def _tool_keywords(tool_name: str) -> list[str]:
    """Map tool names to keywords that might appear in plan step descriptions."""
    mapping = {
        "read_file": ["read", "examine", "look at", "check", "inspect"],
        "write_file": ["create", "write", "generate", "add"],
        "edit_file": ["edit", "modify", "update", "fix", "change"],
        "patch_file": ["patch", "modify", "update"],
        "bash": ["run", "execute", "install", "test", "build", "command"],
        "glob": ["find", "search", "locate", "list"],
        "grep": ["search", "find", "look for"],
        "web_search": ["search", "research", "look up"],
        "cvc_commit": ["commit", "save", "checkpoint"],
        "cvc_branch": ["branch", "create branch"],
    }
    return mapping.get(tool_name, [tool_name.replace("_", " ")])


# ---------------------------------------------------------------------------
# Continuation Engine
# ---------------------------------------------------------------------------

@dataclass
class ContinuationState:
    """Tracks continuation state across iterations."""
    enabled: bool = False
    mode: str = "persistent"  # "persistent" | "full_auto"
    continuation_count: int = 0
    plan_tracker: PlanTracker = field(default_factory=PlanTracker)
    cost_warned: bool = False
    cost_paused: bool = False
    # Stall detection
    _recent_tool_calls: list[str] = field(default_factory=list)

    @property
    def max_iterations(self) -> int:
        return AUTOPILOT_MAX_ITERATIONS if self.enabled else 25


class ContinuationEngine:
    """
    Detects premature LLM stops and builds continuation prompts.

    The core logic:
    1. LLM outputs text (no tool calls) → would normally break the loop
    2. We check: is this REALLY done? (completion signal, plan progress, hedging)
    3. If not done → inject a continuation prompt as a user message → loop continues
    4. If done → allow the break
    """

    def __init__(self, state: ContinuationState | None = None):
        self.state = state or ContinuationState()

    @property
    def enabled(self) -> bool:
        return self.state.enabled

    def enable(self, mode: str = "persistent") -> None:
        self.state.enabled = True
        self.state.mode = mode

    def disable(self) -> None:
        self.state.enabled = False
        self.state.continuation_count = 0

    def should_continue(
        self,
        response_text: str,
        tool_calls_this_turn: int,
        session_cost: float = 0.0,
    ) -> bool:
        """
        Determine if the agent should continue working instead of stopping.

        Returns True if we should inject a continuation prompt.
        """
        if not self.state.enabled:
            return False

        # Hard cap reached
        if self.state.continuation_count >= AUTOPILOT_HARD_CAP:
            logger.info("Autopilot hard cap (%d) reached", AUTOPILOT_HARD_CAP)
            return False

        # Cost guardrail: pause at threshold
        if session_cost >= AUTOPILOT_COST_PAUSE and not self.state.cost_paused:
            logger.info("Autopilot cost pause at $%.2f", session_cost)
            return False

        # If the LLM explicitly signaled completion, respect it
        if COMPLETION_SIGNAL in response_text:
            logger.debug("Completion signal detected — task done")
            return False

        # If no text at all, don't continue (empty response)
        if not response_text.strip():
            return False

        # Stall detection: 3+ identical continuation cycles
        if self._detect_stall():
            logger.info("Stall detected — stopping autopilot")
            return False

        # Check for hedging language (strong signal of premature stop)
        has_hedging = bool(_HEDGING_RE.search(response_text))

        # Check plan progress
        has_remaining_steps = len(self.state.plan_tracker.get_remaining()) > 0

        # If LLM made tool calls this turn and then gave text = likely a progress
        # update, not a real stop. Always continue.
        if tool_calls_this_turn > 0:
            return True

        # If there are remaining plan steps, continue
        if has_remaining_steps:
            return True

        # If hedging language detected, continue
        if has_hedging:
            return True

        # No strong signals — check if response feels like a mid-task update
        # (short responses that don't seem like a complete summary)
        if len(response_text.strip()) < 200 and not _looks_like_final_summary(response_text):
            return True

        return False

    def build_continuation_prompt(self, response_text: str) -> str:
        """Build a continuation prompt to inject as a user message."""
        self.state.continuation_count += 1

        remaining = self.state.plan_tracker.get_remaining()
        if remaining:
            steps_text = "\n".join(
                f"  {s.index}. {s.description}" for s in remaining
            )
            return (
                f"Continue executing. You have {len(remaining)} remaining steps:\n"
                f"{steps_text}\n\n"
                f"Proceed with step {remaining[0].index} now. "
                f"Do not explain — just execute. "
                f"Include <task_complete/> only when ALL steps are done."
            )

        # No plan extracted — generic continuation
        return (
            "You stopped before the task was fully complete. "
            "Continue working on the remaining parts. "
            "Do not explain what you plan to do — just do it. "
            "Include <task_complete/> when everything is done and verified."
        )

    def record_tool_calls(self, tool_names: list[str]) -> None:
        """Record tool calls for stall detection."""
        sig = "|".join(sorted(tool_names))
        self._recent_signatures = getattr(self, "_recent_signatures", [])
        self._recent_signatures.append(sig)
        # Keep last 5
        if len(self._recent_signatures) > 5:
            self._recent_signatures = self._recent_signatures[-5:]

    def _detect_stall(self) -> bool:
        """Detect if the last 3 continuation cycles had identical tool calls."""
        sigs = getattr(self, "_recent_signatures", [])
        if len(sigs) >= 3:
            return sigs[-1] == sigs[-2] == sigs[-3] and sigs[-1] != ""
        return False

    def check_cost_warning(self, session_cost: float) -> str | None:
        """Return a warning message if cost threshold reached."""
        if session_cost >= AUTOPILOT_COST_PAUSE and not self.state.cost_paused:
            self.state.cost_paused = True
            return (
                f"Autopilot paused — session cost ${session_cost:.2f} "
                f"exceeds ${AUTOPILOT_COST_PAUSE:.2f} threshold. "
                f"Use /autopilot on to resume."
            )
        if session_cost >= AUTOPILOT_COST_WARN and not self.state.cost_warned:
            self.state.cost_warned = True
            return (
                f"Autopilot cost warning — session at ${session_cost:.2f} "
                f"(pause at ${AUTOPILOT_COST_PAUSE:.2f})"
            )
        return None


def _looks_like_final_summary(text: str) -> bool:
    """Heuristic: does the text look like a complete task summary?"""
    indicators = [
        r"\ball (?:changes|files|steps|tasks)\b.*\b(?:complete|done|finished)\b",
        r"\bsuccessfully\b.*\b(?:created|implemented|fixed|updated)\b",
        r"\beverything\b.*\b(?:is|has been)\b.*\b(?:set up|configured|ready)\b",
        r"\bhere(?:'s| is) (?:a |the )?(?:summary|overview|recap)\b",
        COMPLETION_SIGNAL.replace("/", r"\/").replace("<", r"\<").replace(">", r"\>"),
    ]
    combined = re.compile("|".join(indicators), re.IGNORECASE)
    return bool(combined.search(text))
