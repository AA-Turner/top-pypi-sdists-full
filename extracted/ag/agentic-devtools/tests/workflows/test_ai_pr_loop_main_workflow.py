"""Tests for ai-pr-loop.yml workflow structure."""

import json
from pathlib import Path
from unittest.mock import patch

import yaml

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import DispatchRepairAction
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_PR_LOOP = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop.yml"
AI_PR_LOOP_TRUSTED_EVENTS = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop-trusted-events.yml"


class TestAiPrLoopMainWorkflow:
    """Validates ai-pr-loop.yml workflow structure and requirements."""

    def test_workflow_file_exists(self) -> None:
        assert AI_PR_LOOP.exists()

    def test_valid_yaml(self) -> None:
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        assert parsed is not None
        assert "jobs" in parsed
        assert "ai-pr-loop" in parsed["jobs"]

    def test_trusted_pull_request_events_run_default_branch_preflight(self) -> None:
        """Trusted PR activity runs live reconciliation from the default branch."""
        parsed = yaml.safe_load(AI_PR_LOOP_TRUSTED_EVENTS.read_text(encoding="utf-8"))
        workflow_on = parsed.get("on", parsed.get(True))
        assert workflow_on["pull_request_target"]["types"] == [
            "opened",
            "synchronize",
            "reopened",
            "ready_for_review",
        ]
        job = parsed["jobs"]["trusted-event-reconciliation"]
        checkout = next(step for step in job["steps"] if step.get("uses") == "actions/checkout@v4")
        assert checkout["with"]["ref"] == "${{ github.event.repository.default_branch }}"
        preflight = next(step for step in job["steps"] if step.get("name") == "Run live reconciliation preflight")
        assert preflight["run"].startswith("agdt-ci-reconcile ")

    def test_has_cooldown_gate_step(self) -> None:
        """An early provider-cooldown gate runs before PR-token provider calls."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        gate_idx = next(i for i, step in enumerate(steps) if step.get("id") == "cooldown-gate")
        dispatch_idx = next(i for i, step in enumerate(steps) if step.get("id") == "dispatch-pr")
        assert gate_idx < dispatch_idx, "cooldown-gate must run before PR-token provider work"

    def test_cooldown_gate_bootstrap_uses_full_history_and_precedes_import(self) -> None:
        """The gate package is installed and import-checked before cooldown evaluation."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        checkout = next(step for step in steps if step.get("name") == "Checkout workflow sources")
        setup_idx = next(i for i, step in enumerate(steps) if step.get("name") == "Set up Python for cooldown gate")
        bootstrap_idx = next(i for i, step in enumerate(steps) if step.get("id") == "cooldown-bootstrap")
        smoke_idx = next(i for i, step in enumerate(steps) if step.get("id") == "cooldown-import-smoke")
        gate_idx = next(i for i, step in enumerate(steps) if step.get("id") == "cooldown-gate")

        assert checkout["with"]["fetch-depth"] == 0
        assert checkout["with"]["ref"] == "${{ github.event.repository.default_branch }}"
        assert setup_idx < bootstrap_idx < smoke_idx < gate_idx
        assert "python -m pip install --disable-pip-version-check -q ." in steps[bootstrap_idx]["run"]
        assert "import agentic_devtools" in steps[smoke_idx]["run"]
        assert "agentic_devtools.__version__" in steps[smoke_idx]["run"]
        assert (
            "from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command"
            in steps[smoke_idx]["run"]
        )

    def test_cooldown_gate_uses_writer_token(self) -> None:
        """Gate reads cooldown variable with the writer PAT, not the PR token."""
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "REPO_VARIABLE_WRITER_PAT" in content
        assert "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT" in content
        assert "--mode" in content
        assert "cooldown-gate" in content

    def test_cooldown_gate_checks_all_loop_credentials(self) -> None:
        """Any active loop-credential cooldown must block provider work."""
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "AI_PR_LOOP_CREDENTIAL_IDENTITY: DEFAULT_CLASSIC_REPO_WORKFLOW_PAT" in content

    def test_cooldown_gate_uses_python_command(self) -> None:
        """The workflow delegates cooldown parsing to the Python watchdog command."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        gate_step = next(step for step in steps if step.get("id") == "cooldown-gate")
        gate_command = gate_step["run"]
        assert "from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command" in gate_command
        assert "--mode" in gate_command
        assert "cooldown-gate" in gate_command

    def test_repair_dispatch_model_is_configurable_with_luna_default(self) -> None:
        """Agent Tasks repairs use the optional model variable and preserve API opt-in."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        run_loop = next(step for step in parsed["jobs"]["ai-pr-loop"]["steps"] if step.get("id") == "run-loop")

        assert run_loop["env"]["COPILOT_AGENT_MODEL"] == "${{ vars.AI_PR_LOOP_REPAIR_MODEL || 'gpt-6-luna' }}"
        assert run_loop["env"]["AGDT_USE_AGENT_TASKS_API"] == "1"

    def test_run_loop_separates_bookkeeping_and_dispatch_credentials(self) -> None:
        """Review bookkeeping uses the Actions bot token while dispatch keeps its PAT."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        run_loop = next(step for step in parsed["jobs"]["ai-pr-loop"]["steps"] if step.get("id") == "run-loop")

        assert run_loop["env"]["AI_PR_LOOP_BOOKKEEPING_TOKEN"] == "${{ github.token }}"
        assert run_loop["env"]["GH_TOKEN"] == "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}"
        assert parsed["permissions"]["pull-requests"] == "write"

    def test_scheduled_reconciliation_has_bookkeeping_token(self) -> None:
        """Scheduled reconciliation can verify the Actions bookkeeping identity."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["scheduled-reconciliation"]["steps"]
        reconcile = next(step for step in steps if "agdt-ci-reconcile" in step.get("run", ""))

        assert reconcile["env"]["AI_PR_LOOP_BOOKKEEPING_TOKEN"] == "${{ github.token }}"
        assert reconcile["env"]["GH_TOKEN"] == "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}"

    def test_provider_steps_gated_on_cooldown(self) -> None:
        """Resolve PR metadata and loop execution are skipped while a cooldown is active."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        gate_condition = "steps.cooldown-gate.outputs.cooldown_active != 'true'"
        gated_ids = {s.get("id") or s.get("name", "") for s in steps if gate_condition in (s.get("if") or "")}
        assert "dispatch-pr" in gated_ids, "Resolve PR head ref step must be gated on cooldown-gate"
        assert "run-loop" in gated_ids, "Run AI PR loop orchestrator step must be gated on cooldown-gate"

    def test_redispatch_step_gated_on_actions_executed(self) -> None:
        """Redispatch is gated on actions_executed == 'true' to prevent no-op redispatch loops."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        dispatch_step = next(
            (s for s in steps if "Dispatch AI PR Loop Redispatch" in s.get("name", "")),
            None,
        )
        assert dispatch_step is not None
        expected_if = "always() && steps.run-loop.outputs.actions_executed == 'true'"
        assert (dispatch_step.get("if") or "").strip() == expected_if

    def test_redispatch_uses_default_workflow_pat(self) -> None:
        """Redispatch uses the default workflow PAT without cross-role fallback."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        dispatch_step = next(step for step in steps if step.get("name") == "Dispatch AI PR Loop Redispatch")
        assert dispatch_step["env"] == {
            "GH_TOKEN": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
            "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
            "AGDT_GITHUB_SECRETS_JSON": "${{ steps.dispatch-pr.outputs.read_token_secrets }}",
            "REPO_VARIABLE_WRITER_PAT": "${{ secrets.REPO_VARIABLE_WRITER_PAT }}",
            "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        }
        assert "--mode redispatch-dispatch-redispatch" in dispatch_step["run"]
        assert "REPO_VARIABLE_WRITER_PAT" not in dispatch_step["run"]
        assert "SPECKIT_PR_TOKEN" not in dispatch_step["run"]
        assert "FALLBACK_GH_TOKEN" not in dispatch_step["run"]

    def test_promoted_finding_is_visible_to_repair_dispatch(self) -> None:
        """A promoted native thread enters the ordinary same-run repair payload."""
        review_body = (
            "<details><summary>Previously missed (1)</summary>\n"
            "### [P1] Add validation\n"
            "**File:** `src/example.py`\n"
            "**Line:** 2\n"
            "Validate the input.\n"
            "</details>"
        )
        review = ReviewInfo(7, "Copilot", "COMMENTED", body=review_body, commit_sha="head")
        clean_review = ReviewInfo(8, "Copilot", "COMMENTED", commit_sha="head")
        native_comment = ReviewCommentInfo(
            id=901,
            path="src/example.py",
            body="Recovered CCR finding [P1] Add validation",
            html_url="https://github.com/owner/repo/pull/42#discussion_r901",
            source_review_id=7,
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        marker_comments: dict[int, str] = {}

        def post_marker_comment(_pr_number: int, body: str) -> int:
            comment_id = len(marker_comments) + 1
            marker_comments[comment_id] = body
            return comment_id

        def review_endpoint_response(url: str, *_args: object, **_kwargs: object) -> str:
            if url.endswith("/pulls/42/reviews/7/comments"):
                return "[]"
            if url.endswith("/pulls/42/reviews/7"):
                return json.dumps({"body": review_body})
            raise AssertionError(f"Unexpected GitHub endpoint: {url}")

        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head",
            review_state="COMMENTED",
            copilot_review_id=8,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=8,
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[review, clean_review],
        )
        with (
            patch.object(
                provider,
                "get_commit_range_diff",
                return_value=(
                    "diff --git a/src/example.py b/src/example.py\n"
                    "--- a/src/example.py\n"
                    "+++ b/src/example.py\n"
                    "@@ -1 +1,2 @@\n"
                    "+new\n"
                ),
            ),
            patch.object(provider, "list_all_review_comments", return_value=[]),
            patch.object(
                provider,
                "list_review_comments",
                side_effect=lambda _pr_number, review_id: [native_comment] if review_id == 7 else [],
            ),
            patch.object(provider, "list_review_threads_by_thread_id", return_value={901: (False, (901,))}),
            patch.object(provider, "create_review_thread", return_value=native_comment),
            patch.object(provider, "list_issue_comments", return_value=[]),
            patch.object(
                provider,
                "find_comment",
                side_effect=lambda _pr, marker: next(
                    ((key, body) for key, body in marker_comments.items() if marker in body),
                    None,
                ),
            ),
            patch.object(provider, "post_comment", side_effect=post_marker_comment),
            patch.object(provider, "list_review_thread_states", return_value={901: (False, False)}),
            patch.object(provider, "dispatch_repair", return_value=77) as dispatch_repair,
            patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=review_endpoint_response),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger"),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            promoted = provider.promote_ccr_findings(
                pr_number=42,
                commit_sha="head",
                base_sha="base",
                reviews=[review, clean_review],
            )
            assert promoted[0].id == 901
            action = DispatchRepairAction()
            derived = DerivedState(snapshot)
            evaluation = action.evaluate(snapshot, derived)
            result = action.execute(provider, snapshot, derived)

        assert evaluation.decision == ActionDecision.EXECUTE
        assert evaluation.preconditions["stuck_prior_threads"] is True
        assert result.decision == ActionDecision.EXECUTE
        dispatched = dispatch_repair.call_args.kwargs["review_comments"]
        assert [comment.id for comment in dispatched] == [901]
        assert dispatched[0].source_review_id == 7

    def test_loop_concurrency_is_scoped_to_the_selected_pr(self) -> None:
        """A loop run for one PR must not replace a pending run for another PR."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        assert parsed["concurrency"]["group"] == "ai-pr-loop-${{ inputs.pr_number }}"
        assert parsed["concurrency"]["cancel-in-progress"] is False

    def test_loop_does_not_install_or_checkout_pr_head_code(self) -> None:
        """The trusted orchestrator must not import or execute code from the PR head."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        assert not any(
            step.get("uses") == "actions/checkout@v4"
            and step.get("with", {}).get("ref") == "${{ steps.dispatch-pr.outputs.head_ref }}"
            for step in steps
        )
        assert not any("-e ." in step.get("run", "") for step in steps)

    def test_closed_or_merged_prs_are_skipped_before_loop_execution(self) -> None:
        """Closed or merged PRs must set pr_open=false and skip loop execution."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        dispatch_step = next(s for s in steps if s.get("id") == "dispatch-pr")
        run_loop = next(s for s in steps if s.get("id") == "run-loop")
        assert "pr_state" in dispatch_step["run"]
        assert "pr_open=false" in dispatch_step["run"]
        assert "steps.dispatch-pr.outputs.pr_open == 'true'" in run_loop["if"]
