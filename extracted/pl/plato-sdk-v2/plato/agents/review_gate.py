"""SDK-level review gate for agent continuation loops.

Wraps the common pattern: agent executes → review runs → merge if passed →
continue with feedback if failed. Creates standardized OTel spans with
``plato.review.*`` attributes so the Chronos parallel agent view can
render review results and merge status.

Usage::

    from plato.agents.review_gate import ReviewGateResult, attach_review_gate

    async def my_review(hostname: str) -> ReviewGateResult:
        result = await run_my_review_pipeline(hostname)
        return ReviewGateResult(
            passed=result.passed,
            feedback=result.feedback,
            result_data=result.model_dump(mode="json"),
        )

    runner = world.agent(config, display_name="builder-1", mounts=[mount])
    attach_review_gate(
        runner,
        review_fn=my_review,
        branch_name="pr/feature-1",
        merge_fn=lambda: integrate_and_refresh(transport, ref, branch_name),
    )
    await runner.run(instruction)
"""

from __future__ import annotations

import json
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from plato.agents.task import AgentTask

logger = logging.getLogger(__name__)


@dataclass
class ReviewGateResult:
    """Result from a review function.

    Attributes:
        passed: Whether the review passed (agent work is acceptable).
        feedback: Human-readable feedback for the agent on failure.
        result_data: Arbitrary JSON-serializable dict with full review details.
            Attached to the OTel span as ``plato.review.result_json``.
        score: Optional numeric score (0.0-1.0).
        verdict: Optional verdict string (e.g. "pass", "fail").
    """

    passed: bool
    feedback: str = ""
    result_data: dict[str, Any] = field(default_factory=dict)
    score: float | None = None
    verdict: str | None = None


def attach_review_gate(
    runner: AgentTask,
    *,
    review_fn: Callable[[str], Awaitable[ReviewGateResult]],
    branch_name: str,
    merge_fn: Callable[[], Awaitable[bool]] | None = None,
    max_continuations: int = 2,
    checkpoint_fn: Callable[[str], Awaitable[None]] | None = None,
    result_dir: Path | None = None,
) -> AgentTask:
    """Wire up a review gate with standardized OTel span attributes.

    After each agent execution:
    1. Calls ``review_fn(agent_hostname)`` inside a ``pr_review.{branch_name}`` span.
    2. Attaches review results as ``plato.review.*`` span attributes.
    3. If passed and ``merge_fn`` is provided, merges and checkpoints.
    4. If failed, continues the agent with feedback.

    Args:
        runner: The AgentTask to attach the gate to.
        review_fn: Async function that takes the agent hostname and returns a ReviewGateResult.
        branch_name: Git branch name for span naming and result persistence.
        merge_fn: Optional async function that merges the branch. Returns True on success.
        max_continuations: Max retry attempts after the initial run.
        checkpoint_fn: Optional async function called after successful merge.
        result_dir: Optional directory to persist review results as JSON.
    """
    _last_result: dict[str, Any] = {}
    _review_history: list[dict[str, Any]] = []

    if result_dir is not None:
        _results_path = result_dir / ".pr-review-results" / f"{branch_name}.json"
    else:
        _results_path = None

    async def _review_and_merge_passed() -> bool:
        from opentelemetry import trace

        tracer = trace.get_tracer("plato.agents.review_gate")
        hostname = runner.runtime_info.hostname if runner.runtime_info else ""

        with tracer.start_as_current_span(
            f"pr_review.{branch_name}",
            attributes={"plato.review.branch": branch_name},
        ) as review_span:
            gate_result = await review_fn(hostname)

            result_dict = gate_result.result_data
            _last_result.clear()
            _last_result.update(result_dict)
            _last_result["passed"] = gate_result.passed
            _last_result["feedback"] = gate_result.feedback
            _review_history.append(dict(_last_result))

            # Attach standard review attributes to span
            review_span.set_attribute("plato.review.passed", gate_result.passed)
            review_json = json.dumps(result_dict, default=str)
            review_span.set_attribute("plato.review.result_json", review_json[:32000])
            if gate_result.score is not None:
                review_span.set_attribute("plato.review.score", gate_result.score)
            if gate_result.verdict is not None:
                review_span.set_attribute("plato.review.verdict", gate_result.verdict)

            # Persist to disk if configured
            if _results_path is not None:
                _results_path.parent.mkdir(parents=True, exist_ok=True)
                _results_path.write_text(json.dumps(result_dict, default=str, indent=2))

            logger.info(
                "Review gate [%s]: passed=%s score=%s verdict=%s",
                branch_name,
                gate_result.passed,
                gate_result.score,
                gate_result.verdict,
            )

            if not gate_result.passed:
                return False

            # Review passed — merge if merge_fn provided
            if merge_fn is not None:
                try:
                    merged = await merge_fn()
                    if not merged:
                        _last_result["feedback"] = (
                            "Review passed but merge to main failed (conflicts). "
                            "Pull the latest main, resolve conflicts, and commit."
                        )
                        _last_result["passed"] = False
                        review_span.set_attribute("plato.review.merge_status", "conflict")
                        logger.warning("Merge failed for branch %s after review passed", branch_name)
                        return False
                    review_span.set_attribute("plato.review.merge_status", "merged")
                    logger.info("Merged branch %s to main", branch_name)
                    if checkpoint_fn:
                        await checkpoint_fn(f"merged.{branch_name.replace('/', '.')}")
                    return True
                except Exception as exc:
                    _last_result["feedback"] = (
                        f"Review passed but merge to main failed: {exc}\n"
                        "Pull the latest main, resolve conflicts, and commit."
                    )
                    _last_result["passed"] = False
                    review_span.set_attribute("plato.review.merge_status", f"error: {exc}")
                    logger.error("Merge error for branch %s: %s", branch_name, exc)
                    return False

            # No merge_fn — just return passed
            return True

    def _build_continuation_instruction() -> str:
        if not _last_result:
            return (
                "Your code did not pass review. "
                "Run validate.sh to check for errors, fix any issues, "
                "and commit your changes."
            )
        if _last_result.get("passed"):
            return "Your code passed review. Say AGENT_FINISH."

        feedback = _last_result.get("feedback", "")

        parts = [f"Your code did not pass the automated review (attempt {len(_review_history)})."]
        if feedback:
            parts.append(f"Here is the review feedback:\n\n{feedback[:3000]}")
        else:
            parts.append("No detailed feedback available — re-run validate.sh to check for errors.")

        # Include prior review history so the agent knows what was already tried
        if len(_review_history) > 1:
            history_lines = []
            for i, prev in enumerate(_review_history[:-1], 1):
                prev_score = prev.get("score", "?")
                prev_verdict = prev.get("verdict", "?")
                prev_feedback = prev.get("feedback", "")[:500]
                history_lines.append(
                    f"  Review #{i}: verdict={prev_verdict} score={prev_score}\n    Feedback: {prev_feedback}"
                )
            parts.append("Previous review attempts for this branch:\n" + "\n".join(history_lines))

        parts.append("\nFix the issues described above and commit your changes.")
        return "\n\n".join(parts)

    runner.with_continuation(
        exit_condition=_review_and_merge_passed,
        max_continuations=max_continuations,
        continuation_instruction=_build_continuation_instruction,
    )
    return runner
