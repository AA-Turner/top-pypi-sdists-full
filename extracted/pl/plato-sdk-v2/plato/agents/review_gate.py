"""SDK-level review gate for agent continuation loops.

Wraps the common pattern: agent executes → review runs → merge if passed →
continue with feedback if failed. Creates standardized OTel spans with
``plato.review.*`` attributes so the Chronos parallel agent view can
render review results and merge status.

Usage::

    from plato.agents.review_gate import ReviewGateResult, attach_review_gate

    async def my_review(hostname: str, *, attempt_number: int = 1) -> ReviewGateResult:
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
from typing import Any, Literal

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
        failure_kind: Optional machine-readable failure class.
        exhaustion_policy_override: Optional per-result override for what to do
            when review continuations are exhausted.
        continuation_cap_cost: Cost charged against the continuation budget
            for this review outcome. Use ``0.0`` for failures that should
            keep looping without consuming the PR-review cap.
    """

    passed: bool
    feedback: str = ""
    result_data: dict[str, Any] = field(default_factory=dict)
    score: float | None = None
    verdict: str | None = None
    failure_kind: str = ""
    exhaustion_policy_override: Literal["fail", "merge", "raise"] | None = None
    continuation_cap_cost: float = 1.0


@dataclass(frozen=True)
class ReviewGateMergeResult:
    """Outcome of the post-review merge attempt."""

    merged: bool
    conflict_files: list[str] = field(default_factory=list)
    error: str = ""


def attach_review_gate(
    runner: AgentTask,
    *,
    review_fn: Callable[..., Awaitable[ReviewGateResult]],
    branch_name: str,
    merge_fn: Callable[[], Awaitable[bool | ReviewGateMergeResult]] | None = None,
    reviewed_commit_fn: Callable[[], str | None] | None = None,
    max_continuations: int = 2,
    max_zero_cost_continuations: int | None = None,
    compaction_instruction: str | Callable[[], str] | None = None,
    checkpoint_fn: Callable[[str], Awaitable[None]] | None = None,
    result_dir: Path | None = None,
    exhaustion_policy: Literal["fail", "merge", "raise"] = "fail",
) -> AgentTask:
    """Wire up a review gate with standardized OTel span attributes.

    After each agent execution:
    1. Calls ``review_fn(agent_hostname)`` inside a ``pr_review.{branch_name}`` span.
    2. Attaches review results as ``plato.review.*`` span attributes.
    3. If passed and ``merge_fn`` is provided, merges and checkpoints.
    4. If failed, continues the agent with feedback.

    Args:
        runner: The AgentTask to attach the gate to.
        review_fn: Async function that takes the agent hostname and an ``attempt_number``
            keyword argument (1-indexed) and returns a ReviewGateResult.
        branch_name: Git branch name for span naming and result persistence.
        merge_fn: Optional async function that merges the branch. Returns True on success.
        reviewed_commit_fn: Optional function that returns the commit SHA currently
            under review. Attached to the span as ``plato.review.commit_sha`` when available.
        max_continuations: Max retry attempts after the initial run. Charged
            against review failures (cap_cost > 0).
        max_zero_cost_continuations: Max retry attempts charged against zero-cost
            failures (build/merge, cap_cost == 0). These don't deplete the review
            budget, but are bounded here so a never-converging merge-conflict loop
            can't retry indefinitely. Defaults to ``max_continuations``.
        compaction_instruction: Optional ``/compact <instructions>`` message run on
            the live session after each execution and before review (see
            AgentTask._run_session_compaction), to shrink the continued session
            while its cache is warm.
        checkpoint_fn: Optional async function called after successful merge.
        result_dir: Optional directory to persist review results as JSON.
        exhaustion_policy: Behavior when review continuations are exhausted without
            a passing review. ``"fail"`` leaves the task unmerged, ``"merge"``
            force-merges the latest branch state, and ``"raise"`` raises a
            runtime error instead of returning normally.
    """
    _last_result: dict[str, Any] = {}
    _review_history: list[dict[str, Any]] = []
    _last_failure_kind = ""
    _last_exhaustion_policy_override: Literal["fail", "merge", "raise"] | None = None
    _last_continuation_cap_cost = 1.0
    _last_reviewed_commit: str | None = None
    # Count of review-repair failures that consumed the (cap_cost > 0) review
    # budget. Once this reaches ``max_continuations`` under a "merge" policy, the
    # gate stops running review and flips into merge-only mode (below).
    _review_failures_charged = 0
    # When True, review_fn no longer runs — the builder's sole remaining job is
    # to make the branch merge cleanly. The merge-resolution loop is bounded by
    # ``max_zero_cost_continuations``; if it never merges the route is
    # quarantined (returned unmerged) instead of crashing the session.
    _merge_only_mode = False
    # Conflict-resolution feedback shown to the builder while in merge-only mode.
    # Kept separate from the review feedback in ``_last_result`` so the final
    # persisted review record is never clobbered.
    _merge_only_feedback = ""

    if result_dir is not None:
        _results_path = result_dir / ".pr-review-results" / f"{branch_name}.json"
    else:
        _results_path = None

    async def _attempt_force_merge_only() -> bool:
        """Force-merge the branch in merge-only mode (review repair is done).

        Returns True if the branch merged (route is complete). On a conflict or
        merge error, returns False with a zero-cost continuation so the builder
        loops again on conflict resolution — bounded by max_zero_cost_continuations.
        Never raises and never overwrites the persisted review record.
        """
        nonlocal _last_continuation_cap_cost, _merge_only_feedback
        if merge_fn is None:  # defensive — flip is only entered with merge_fn set
            return False
        merge_result = await merge_fn()
        if isinstance(merge_result, ReviewGateMergeResult):
            merged = merge_result.merged
            conflict_files = list(merge_result.conflict_files)
            merge_error = merge_result.error
        else:
            merged = bool(merge_result)
            conflict_files = []
            merge_error = ""

        if merged:
            runner.merged = True
            runner.review_exhaustion_force_merged = True
            _last_result["passed"] = True
            _last_result["merge_status"] = "merged_after_review_exhaustion"
            logger.info(
                "Force-merged branch %s after review exhaustion (merge-only mode)",
                branch_name,
            )
            if checkpoint_fn:
                await checkpoint_fn(f"merged.{branch_name.replace('/', '.')}")
            return True

        # Conflict/error: keep looping as a zero-cost merge-resolution continuation.
        _last_continuation_cap_cost = 0.0
        _last_result["merge_status"] = "conflict"
        if conflict_files:
            _last_result["merge_conflict_files"] = conflict_files
        if merge_error:
            _last_result["merge_error"] = merge_error
        conflict_list = (
            "\n".join(f"- {path}" for path in conflict_files) if conflict_files else "(run `git status` to list them)"
        )
        _merge_only_feedback = (
            "Automated review repair is complete and will NOT run again. "
            "Your ONLY remaining task is to make this branch merge cleanly into `main`.\n\n"
            "Run `git fetch origin main && git merge origin/main`, resolve all conflict "
            "markers, and commit. Do not change unrelated code.\n\n"
            f"Conflicting files:\n{conflict_list}"
        )
        logger.warning(
            "Force-merge in merge-only mode hit conflicts for branch %s: %s",
            branch_name,
            conflict_files or merge_error,
        )
        return False

    async def _review_and_merge_passed() -> bool:
        nonlocal _last_failure_kind, _last_exhaustion_policy_override, _last_continuation_cap_cost
        nonlocal _last_reviewed_commit, _review_failures_charged, _merge_only_mode
        from opentelemetry import trace

        # Already past the review-repair budget: skip review entirely and only
        # try to land the merge. Leaves the persisted review record untouched.
        if _merge_only_mode:
            return await _attempt_force_merge_only()

        tracer = trace.get_tracer("plato.agents.review_gate")
        hostname = runner.runtime_info.hostname if runner.runtime_info else ""

        attempt_number = len(_review_history) + 1

        with tracer.start_as_current_span(
            f"pr_review.{branch_name}",
            attributes={
                "plato.review.branch": branch_name,
                "plato.review.attempt_number": attempt_number,
            },
        ) as review_span:
            reviewed_commit = reviewed_commit_fn() if reviewed_commit_fn is not None else None
            _last_reviewed_commit = reviewed_commit
            gate_result = await review_fn(hostname, attempt_number=attempt_number)

            result_dict = gate_result.result_data
            overall_passed = gate_result.passed

            # If review passed, attempt merge as part of the same review cycle
            merge_status = None
            merge_conflict_files: list[str] = []
            merge_error = ""
            if overall_passed and merge_fn is not None:
                try:
                    merge_result = await merge_fn()
                    if isinstance(merge_result, ReviewGateMergeResult):
                        merged = merge_result.merged
                        merge_conflict_files = list(merge_result.conflict_files)
                        merge_error = merge_result.error
                    else:
                        merged = merge_result
                    if merged:
                        merge_status = "merged"
                        logger.info("Merged branch %s to main", branch_name)
                        if checkpoint_fn:
                            await checkpoint_fn(f"merged.{branch_name.replace('/', '.')}")
                    else:
                        overall_passed = False
                        gate_result.failure_kind = gate_result.failure_kind or "merge"
                        gate_result.continuation_cap_cost = 0.0
                        if merge_conflict_files:
                            merge_status = "conflict"
                            feedback = [
                                "Your code passed review but has merge conflicts with main.",
                            ]
                            feedback.append(
                                "Conflicting files:\n" + "\n".join(f"- {path}" for path in merge_conflict_files)
                            )
                            feedback.append("Pull the latest main into your branch, resolve conflicts, and commit.")
                            gate_result.feedback = "\n\n".join(feedback)
                            logger.warning("Merge conflict for branch %s", branch_name)
                        else:
                            merge_status = "error"
                            merge_error = merge_error or "merge returned merged=False without conflict files"
                            gate_result.feedback = (
                                "Your code passed review but could not be merged automatically.\n\n"
                                f"Merge error: {merge_error}\n\n"
                                "Re-run the task or inspect the git state before making code changes."
                            )
                            logger.warning("Merge error for branch %s: %s", branch_name, merge_error)
                except Exception as exc:
                    merge_status = "error"
                    overall_passed = False
                    merge_error = str(exc)
                    gate_result.failure_kind = gate_result.failure_kind or "merge"
                    gate_result.continuation_cap_cost = 0.0
                    gate_result.feedback = (
                        f"Your code passed review but could not be merged: {exc}\n"
                        "Re-run the task or inspect the git state before making code changes."
                    )
                    logger.error("Merge error for branch %s: %s", branch_name, exc)
            elif overall_passed and checkpoint_fn is not None:
                await checkpoint_fn(f"reviewed.{branch_name.replace('/', '.')}")

            _last_result.clear()
            _last_result.update(result_dict)
            _last_result["passed"] = overall_passed
            _last_result["feedback"] = gate_result.feedback
            _last_result["score"] = gate_result.score
            _last_result["verdict"] = gate_result.verdict
            _last_failure_kind = gate_result.failure_kind
            _last_exhaustion_policy_override = gate_result.exhaustion_policy_override
            _last_continuation_cap_cost = float(gate_result.continuation_cap_cost)
            if gate_result.failure_kind:
                _last_result["failure_kind"] = gate_result.failure_kind
            if gate_result.exhaustion_policy_override is not None:
                _last_result["exhaustion_policy_override"] = gate_result.exhaustion_policy_override
            _last_result["continuation_cap_cost"] = _last_continuation_cap_cost
            if reviewed_commit:
                _last_result["reviewed_commit_sha"] = reviewed_commit
            if merge_conflict_files:
                _last_result["merge_conflict_files"] = merge_conflict_files
            if merge_error:
                _last_result["merge_error"] = merge_error
            if merge_status is not None:
                _last_result["merge_status"] = merge_status
            _review_history.append(dict(_last_result))

            # Attach final attributes to the span (includes merge outcome)
            review_span.set_attribute("plato.review.passed", overall_passed)
            if reviewed_commit:
                result_dict["reviewed_commit_sha"] = reviewed_commit
                review_span.set_attribute("plato.review.commit_sha", reviewed_commit)
            if merge_conflict_files:
                result_dict["merge_conflict_files"] = merge_conflict_files
                review_span.set_attribute("plato.merge.conflict_files", json.dumps(merge_conflict_files))
            if merge_error:
                result_dict["merge_error"] = merge_error
                review_span.set_attribute("plato.merge.error", merge_error[:4000])
            if merge_status is not None:
                result_dict["merge_status"] = merge_status
            review_json = json.dumps(result_dict, default=str)
            review_span.set_attribute("plato.review.result_json", review_json[:32000])
            if gate_result.score is not None:
                review_span.set_attribute("plato.review.score", gate_result.score)
            if gate_result.verdict is not None:
                review_span.set_attribute("plato.review.verdict", gate_result.verdict)
            if merge_status is not None:
                review_span.set_attribute("plato.merge.status", merge_status)

            # Persist to disk if configured
            if _results_path is not None:
                _results_path.parent.mkdir(parents=True, exist_ok=True)
                _results_path.write_text(json.dumps(result_dict, default=str, indent=2))

            logger.info(
                "Review gate [%s]: passed=%s score=%s verdict=%s merge=%s",
                branch_name,
                overall_passed,
                gate_result.score,
                gate_result.verdict,
                merge_status,
            )

        # ``overall_passed`` may have been flipped to False by a merge conflict
        # on an otherwise-passing review; that stays the existing zero-cost
        # resolution path. The review-exhaustion flip only applies to genuine
        # review *failures* that consume the review-repair budget.
        review_failed = not gate_result.passed
        if review_failed:
            selected_policy = gate_result.exhaustion_policy_override or exhaustion_policy
            review_repair_failure = _last_continuation_cap_cost > 0
            if (
                review_repair_failure
                and selected_policy == "merge"
                and merge_fn is not None
                and _review_failures_charged >= max_continuations
            ):
                # Review-repair budget is used up. Stop reviewing and switch to
                # merge-only mode; the just-persisted review record is the
                # preserved final feedback and is left intact.
                _merge_only_mode = True
                logger.warning(
                    "Review-repair budget exhausted for branch %s (%d failures); "
                    "switching to merge-only mode (no more review repair)",
                    branch_name,
                    _review_failures_charged,
                )
                return await _attempt_force_merge_only()
            if review_repair_failure:
                _review_failures_charged += 1

        return overall_passed

    def _build_continuation_instruction() -> str:
        # In merge-only mode the builder's sole job is conflict resolution; show
        # the merge-only feedback instead of the (preserved) review-repair text.
        if _merge_only_mode and _merge_only_feedback:
            return _merge_only_feedback
        if not _last_result:
            return (
                "Your code did not pass review. "
                "Run validate.sh to check for errors, fix any issues, "
                "and commit your changes."
            )
        if _last_result.get("passed"):
            return "Your code passed review. Say AGENT_FINISH."

        feedback = _last_result.get("feedback", "")
        merge_status = _last_result.get("merge_status")
        merge_error = str(_last_result.get("merge_error", ""))

        if merge_status == "conflict":
            parts = [
                f"Your code passed the automated review (attempt {len(_review_history)}), "
                "but could not be merged into main due to conflicts."
            ]
        elif merge_status and merge_status != "merged":
            parts = [
                f"Your code passed the automated review (attempt {len(_review_history)}), but the merge step failed."
            ]
        else:
            parts = [f"Your code did not pass the automated review (attempt {len(_review_history)})."]
        # Ground the (possibly just-compacted) session in the exact commit it
        # produced last cycle, so it can re-orient even after its detailed
        # working memory was summarized away.
        if _last_reviewed_commit:
            parts.append(
                f"This feedback is for the commit you just made on this branch: "
                f"`{_last_reviewed_commit}`. Run `git show {_last_reviewed_commit} --stat` "
                "(or `git diff`) to see exactly what you changed last cycle before "
                "applying the fixes below."
            )
        if feedback:
            parts.append(f"Here is the review feedback:\n\n{feedback}")
        elif merge_error:
            parts.append(f"Merge error: {merge_error}")
        else:
            parts.append("No detailed feedback available — re-run validate.sh to check for errors.")

        parts.append("\nFix the issues described above and commit your changes.")
        return "\n\n".join(parts)

    async def _handle_review_exhaustion() -> None:
        # Merge-only mode used up its merge-resolution budget and the branch
        # still won't merge: quarantine the route (leave it unmerged) and return
        # normally so other routes in the gather survive. Never raise here.
        if _merge_only_mode:
            runner.review_exhaustion_quarantined = True
            _last_result["merge_status"] = "quarantined_unmerged"
            _last_result["passed"] = False
            logger.warning(
                "Branch %s could not be merged after exhausting the post-review "
                "merge-resolution budget; quarantining the route (unmerged) instead "
                "of crashing the session.",
                branch_name,
            )
            return

        selected_exhaustion_policy = _last_exhaustion_policy_override or exhaustion_policy
        if selected_exhaustion_policy == "fail":
            return

        if selected_exhaustion_policy == "raise":
            feedback = str(_last_result.get("feedback", "")).strip()
            message = f"Review cycles exhausted for branch {branch_name} after {1 + max_continuations} attempt(s)."
            if _last_failure_kind:
                message += f" Failure kind: {_last_failure_kind}."
            if feedback:
                message += f" Last review feedback:\n\n{feedback}"
            raise RuntimeError(message)

        if selected_exhaustion_policy == "merge":
            if merge_fn is None:
                raise RuntimeError(f"Review cycles exhausted for branch {branch_name}, but no merge_fn is configured.")
            merge_result = await merge_fn()
            if isinstance(merge_result, ReviewGateMergeResult):
                if not merge_result.merged:
                    if merge_result.conflict_files:
                        raise RuntimeError(
                            "Review cycles exhausted and forced merge hit conflicts: "
                            + ", ".join(merge_result.conflict_files)
                        )
                    raise RuntimeError(
                        "Review cycles exhausted and forced merge failed: "
                        + (merge_result.error or "unknown merge error")
                    )
            elif merge_result is not True:
                raise RuntimeError(f"Review cycles exhausted and forced merge failed for branch {branch_name}.")
            runner.merged = True
            runner.review_exhaustion_force_merged = True
            _last_result["passed"] = True
            _last_result["merge_status"] = "forced_merge_after_review_exhaustion"
            if _last_failure_kind:
                _last_result["failure_kind"] = _last_failure_kind
            _last_result["feedback"] = (
                _last_result.get("feedback", "") or "Review cycles exhausted; branch was force-merged by policy."
            )
            return

        raise RuntimeError(f"Unknown review exhaustion policy: {selected_exhaustion_policy}")

    runner.with_continuation(
        exit_condition=_review_and_merge_passed,
        max_continuations=max_continuations,
        continuation_instruction=_build_continuation_instruction,
        on_exhausted=_handle_review_exhaustion,
        continuation_cap_cost=lambda: _last_continuation_cap_cost,
        max_zero_cost_continuations=max_zero_cost_continuations,
        compaction_instruction=compaction_instruction,
    )
    return runner
