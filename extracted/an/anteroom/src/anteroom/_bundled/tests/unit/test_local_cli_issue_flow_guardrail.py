"""Unit tests for the real-behavior validation guardrail (#1200).

Covers:

- ``sensitive_paths_touched`` fnmatch filter
- ``extract_plan_file_paths`` parse of "Files to Modify" / "Files to Create"
- ``extract_validation_note`` parse of ``Real validation:`` line
- ``build_pr_body_with_validation`` idempotent upsert
- Prompt contract: builders include the sensitive-scope block + new JSON
  keys when ``sensitive_paths`` is non-empty, and omit them otherwise
- Author prompts: ``build_claude_implement_prompt`` and
  ``build_claude_pr_fix_prompt`` include the author-side block when the
  scope is sensitive
- ``apply_validation_gate`` server-side override behavior
- ``cmd_review_plan`` / ``cmd_review_existing_work`` / ``cmd_review_pr``
  override when the scope is sensitive and the review lacks a real
  validation note
- ``cmd_review_pr`` PR-body assertion (defense-in-depth when the review
  claims validation present but the body section is missing)
- ``cmd_open_pr`` injects the Real-behavior validation section when the
  scope is sensitive, and fails closed when the note is missing
- Non-sensitive scopes pass through unchanged (backward compat)
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


def _import_helper():
    script = Path(__file__).resolve().parents[2] / "scripts" / "workflows" / "local_cli_issue_flow.py"
    spec = importlib.util.spec_from_file_location("local_cli_issue_flow", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


helper = _import_helper()


# ---------------------------------------------------------------------------
# sensitive_paths_touched
# ---------------------------------------------------------------------------


class TestSensitivePathsTouched:
    def test_matches_workflow_script(self) -> None:
        hits = helper.sensitive_paths_touched(["scripts/workflows/local_cli_issue_flow.py", "docs/readme.md"])
        assert hits == ["scripts/workflows/local_cli_issue_flow.py"]

    def test_matches_workflow_service(self) -> None:
        hits = helper.sensitive_paths_touched(
            [
                "src/anteroom/services/workflow_runners.py",
                "src/anteroom/services/workflow_engine.py",
                "src/anteroom/cli/repl.py",
            ]
        )
        assert hits == [
            "src/anteroom/services/workflow_runners.py",
            "src/anteroom/services/workflow_engine.py",
        ]

    def test_matches_example_workflow_yaml(self) -> None:
        hits = helper.sensitive_paths_touched(["examples/workflows/foo.yaml"])
        assert hits == ["examples/workflows/foo.yaml"]

    def test_matches_workflow_cli(self) -> None:
        hits = helper.sensitive_paths_touched(["src/anteroom/cli/workflow_cli.py"])
        assert hits == ["src/anteroom/cli/workflow_cli.py"]

    def test_ignores_unrelated_paths(self) -> None:
        hits = helper.sensitive_paths_touched(
            [
                "src/anteroom/cli/repl.py",
                "src/anteroom/services/storage.py",
                "docs/index.md",
                "README.md",
                "tests/unit/test_foo.py",
            ]
        )
        assert hits == []

    def test_deduplicates_preserving_order(self) -> None:
        hits = helper.sensitive_paths_touched(
            [
                "scripts/workflows/a.py",
                "src/anteroom/services/workflow_runners.py",
                "scripts/workflows/a.py",
            ]
        )
        assert hits == ["scripts/workflows/a.py", "src/anteroom/services/workflow_runners.py"]


# ---------------------------------------------------------------------------
# pr_changed_file_paths / git_diff_names — fail-closed contract (#1200)
# ---------------------------------------------------------------------------


class TestFailClosedPathLookups:
    """The sensitive-path guardrail MUST fail closed: when `gh` or `git`
    fails to return the path list, the helpers return ``None`` (not ``[]``)
    so the callers can treat the scope as sensitive instead of silently
    bypassing the guardrail. These tests are the regression sentinels for
    the fail-open hole caught in senior review on PR #1349.
    """

    def test_pr_changed_file_paths_returns_none_on_gh_failure(self) -> None:
        def fake_run_stdout(cmd, *, cwd=None):
            raise SystemExit(1)

        with patch.object(helper, "run_stdout", side_effect=fake_run_stdout):
            result = helper.pr_changed_file_paths(42)
        assert result is None, (
            "pr_changed_file_paths must return None on gh failure, not []. "
            "An empty list [] silently disables the guardrail (fail-open)."
        )

    def test_pr_changed_file_paths_returns_list_on_success(self) -> None:
        with patch.object(
            helper,
            "run_stdout",
            return_value="scripts/workflows/foo.py\nsrc/anteroom/cli/repl.py\n",
        ):
            result = helper.pr_changed_file_paths(42)
        assert result == ["scripts/workflows/foo.py", "src/anteroom/cli/repl.py"]

    def test_pr_changed_file_paths_returns_empty_list_on_no_files(self) -> None:
        with patch.object(helper, "run_stdout", return_value=""):
            result = helper.pr_changed_file_paths(42)
        assert result == []

    def test_git_diff_names_returns_none_on_git_failure(self) -> None:
        def fake_run_stdout(cmd, *, cwd=None):
            raise SystemExit(128)

        with patch.object(helper, "run_stdout", side_effect=fake_run_stdout):
            result = helper.git_diff_names(Path("/tmp/worktree"), "origin/main")
        assert result is None, (
            "git_diff_names must return None on git failure, not []. "
            "An empty list [] silently disables the guardrail (fail-open)."
        )

    def test_git_diff_names_returns_list_on_success(self) -> None:
        with patch.object(
            helper,
            "run_stdout",
            return_value="scripts/workflows/foo.py\nREADME.md\n",
        ):
            result = helper.git_diff_names(Path("/tmp/worktree"), "origin/main")
        assert result == ["scripts/workflows/foo.py", "README.md"]


class TestCmdCallersFailClosed:
    """Verify that cmd_review_pr and cmd_open_pr treat a None return from
    their path-lookup helpers as 'assume sensitive' (fail-closed), not
    'assume clean' (fail-open)."""

    def test_cmd_review_pr_assumes_sensitive_when_gh_fails(self) -> None:
        args = SimpleNamespace(issue=1200)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "ensure_pr_number", return_value=42),
            # gh failure — returns None, not [].
            patch.object(helper, "pr_changed_file_paths", return_value=None),
            patch.object(
                helper,
                "codex_once",
                return_value=helper.CodexRunResult(
                    text=(
                        '{"decision":"approve","summary":"OK","comment_markdown":"LGTM",'
                        '"real_validation_required":true,"real_validation_present":false}'
                    ),
                    exit_code=0,
                ),
            ),
            patch.object(helper, "post_pr_review") as mock_post,
            patch.object(helper, "edit_pr_labels"),
            patch.object(helper, "update_state"),
        ):
            rc = helper.cmd_review_pr(args)

        # Must NOT approve — the guardrail should fire because the scope
        # is assumed sensitive when the path lookup fails.
        assert rc == 1
        posted_decision = mock_post.call_args.args[1]
        assert posted_decision == "changes_requested"
        posted_comment = mock_post.call_args.args[2]
        assert "Blocked" in posted_comment

    def test_cmd_open_pr_assumes_sensitive_when_git_diff_fails(self) -> None:
        args = SimpleNamespace(issue=1200)
        summary_with_note = "Made the change.\n\nReal validation: ran temp-repo probe; exit 0."

        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "branch": "issue-1200-thing",
                    "issue_title": "Do workflow thing",
                    "implementation_summary": summary_with_note,
                    "real_validation_note": "ran temp-repo probe; exit 0.",
                },
            ),
            patch.object(helper, "current_pr_number", return_value=None),
            patch.object(helper, "latest_main_ref", return_value="origin/main"),
            # git failure — returns None, not [].
            patch.object(helper, "git_diff_names", return_value=None),
        ):
            # Should NOT crash and should still proceed (the scope is
            # assumed sensitive, and the note IS present, so open-pr should
            # attempt to create the PR with the validation section). The
            # key assertion is that it doesn't silently skip the guardrail.
            # We let it fail on the gh pr create call (not mocked) — that's
            # fine; the point is that sensitive_paths is not empty.
            # For this test, we assert the guardrail detected sensitivity
            # by checking that build_pr_body_with_validation would be called
            # with a non-empty sensitive_paths list. We mock run_stdout to
            # capture the body-file content.
            captured_body: dict[str, str] = {}

            def fake_run_stdout(cmd, *, cwd=None):
                if cmd[:3] == ["gh", "pr", "create"]:
                    idx = cmd.index("--body-file")
                    captured_body["content"] = Path(cmd[idx + 1]).read_text()
                    return "https://example.com/pr/99"
                raise AssertionError(f"Unexpected: {cmd}")

            with (
                patch.object(helper, "run_stdout", side_effect=fake_run_stdout),
                patch.object(helper, "current_pr_number", side_effect=[None, 99]),
                patch.object(helper, "update_state"),
            ):
                rc = helper.cmd_open_pr(args)

        assert rc == 0
        body = captured_body["content"]
        # The guardrail treated the scope as sensitive (git_diff_names
        # returned None) and injected the validation section.
        assert "## Real-behavior validation" in body
        assert "ran temp-repo probe" in body


# ---------------------------------------------------------------------------
# extract_plan_file_paths
# ---------------------------------------------------------------------------


class TestExtractPlanFilePaths:
    def test_extracts_from_files_to_modify_section(self) -> None:
        plan = """
## Summary
Some summary.

### Files to Modify

| File | Change |
|---|---|
| `src/anteroom/services/workflow_runners.py` | update X |
| `tests/unit/test_workflow_runners.py` | add regression |

### Other heading
`unrelated.py` — not in a files section, must not be picked up.
""".strip()
        assert helper.extract_plan_file_paths(plan) == [
            "src/anteroom/services/workflow_runners.py",
            "tests/unit/test_workflow_runners.py",
        ]

    def test_extracts_from_files_to_create_section(self) -> None:
        plan = """
### Files to Create
- `src/anteroom/services/message_router.py` — new pure helper
- `tests/unit/test_message_router.py` — unit tests
""".strip()
        assert helper.extract_plan_file_paths(plan) == [
            "src/anteroom/services/message_router.py",
            "tests/unit/test_message_router.py",
        ]

    def test_extracts_from_both_sections(self) -> None:
        plan = """
### Files to Create
- `src/anteroom/services/new_thing.py` — the new module

### Files to Modify
- `src/anteroom/services/old_thing.py` — tweak
""".strip()
        assert helper.extract_plan_file_paths(plan) == [
            "src/anteroom/services/new_thing.py",
            "src/anteroom/services/old_thing.py",
        ]

    def test_ignores_paths_outside_file_sections(self) -> None:
        plan = """
## Summary
Uses `src/anteroom/services/storage.py` as a reference but does not touch it.

### Files to Modify
- `src/anteroom/routers/chat.py` — only this
""".strip()
        assert helper.extract_plan_file_paths(plan) == ["src/anteroom/routers/chat.py"]

    def test_rejects_absolute_and_dotdot_paths(self) -> None:
        plan = """
### Files to Modify
- `/etc/passwd` — no
- `../outside.py` — no
- `src/anteroom/services/good.py` — yes
""".strip()
        assert helper.extract_plan_file_paths(plan) == ["src/anteroom/services/good.py"]

    def test_empty_plan_returns_empty(self) -> None:
        assert helper.extract_plan_file_paths("") == []

    def test_plan_without_file_sections_returns_empty(self) -> None:
        plan = """
## Summary
No file sections at all — backtick mentions: `src/anteroom/foo.py`.
""".strip()
        assert helper.extract_plan_file_paths(plan) == []

    def test_deduplicates_preserving_order(self) -> None:
        plan = """
### Files to Modify
- `src/anteroom/a.py` — once
- `src/anteroom/b.py` — first
- `src/anteroom/a.py` — again (duplicate)
""".strip()
        assert helper.extract_plan_file_paths(plan) == [
            "src/anteroom/a.py",
            "src/anteroom/b.py",
        ]


# ---------------------------------------------------------------------------
# extract_validation_note
# ---------------------------------------------------------------------------


class TestExtractValidationNote:
    def test_parses_single_line_note(self) -> None:
        summary = "Made a change.\n\nReal validation: ran temp-repo probe; got exit 0.\n"
        assert helper.extract_validation_note(summary) == "ran temp-repo probe; got exit 0."

    def test_parses_multiline_note(self) -> None:
        summary = """
Implemented the fix.

Real validation: ran `python3 -c "..."` against a fresh temp repo.
Output: prune+reset OK.

## Next steps
more stuff here
""".strip()
        note = helper.extract_validation_note(summary)
        assert note is not None
        assert "python3 -c" in note
        assert "prune+reset OK" in note
        # The block stops at the blank-line boundary before the next heading.
        assert "## Next steps" not in note

    def test_returns_none_when_absent(self) -> None:
        assert helper.extract_validation_note("just a summary, no real validation line") is None

    def test_returns_none_for_empty_input(self) -> None:
        assert helper.extract_validation_note("") is None

    def test_stops_at_blank_line_boundary(self) -> None:
        # The note ends at the first blank-line boundary; subsequent
        # content belongs to a separate section and is not part of the
        # validation note.
        summary = "Real validation: ran probe; got 0.\n\n## Unrelated section\nmore stuff here"
        note = helper.extract_validation_note(summary)
        assert note == "ran probe; got 0."


# ---------------------------------------------------------------------------
# build_pr_body_with_validation
# ---------------------------------------------------------------------------


class TestBuildPrBodyWithValidation:
    def test_appends_section_when_absent(self) -> None:
        base = "Implements #1200\n\nGenerated by workflow."
        out = helper.build_pr_body_with_validation(
            base,
            sensitive_paths=["scripts/workflows/foo.py"],
            note="ran temp-repo probe",
        )
        assert "## Real-behavior validation" in out
        assert "scripts/workflows/foo.py" in out
        assert "ran temp-repo probe" in out
        # Base body is preserved.
        assert "Implements #1200" in out

    def test_replaces_existing_section(self) -> None:
        base = (
            "Implements #1200\n\n"
            "Generated by workflow.\n\n"
            "## Real-behavior validation\n\n"
            "Touched sensitive paths:\n- old-path.py\n\n"
            "Validation step run by the author agent:\n\n"
            "old note\n"
        )
        out = helper.build_pr_body_with_validation(
            base,
            sensitive_paths=["new-path.py"],
            note="new note",
        )
        assert out.count("## Real-behavior validation") == 1
        assert "new-path.py" in out
        assert "new note" in out
        assert "old-path.py" not in out
        assert "old note" not in out
        # Base body before the section is preserved.
        assert "Implements #1200" in out


# ---------------------------------------------------------------------------
# Prompt contract
# ---------------------------------------------------------------------------


class TestPromptContractSensitiveScope:
    def test_plan_review_prompt_includes_guardrail_when_sensitive(self) -> None:
        prompt = helper.build_codex_plan_review_prompt(
            1200,
            issue_context="irrelevant",
            plan_markdown="irrelevant",
            sensitive_paths=["scripts/workflows/local_cli_issue_flow.py"],
        )
        assert "<sensitive_scope>" in prompt
        assert "scripts/workflows/local_cli_issue_flow.py" in prompt
        assert "real-behavior validation" in prompt
        assert '"real_validation_required"' in prompt
        assert '"real_validation_present"' in prompt
        assert '"real_validation_details"' in prompt

    def test_plan_review_prompt_omits_guardrail_when_empty(self) -> None:
        prompt = helper.build_codex_plan_review_prompt(
            1200,
            issue_context="irrelevant",
            plan_markdown="irrelevant",
            sensitive_paths=[],
        )
        assert "<sensitive_scope>" not in prompt
        assert "real-behavior validation" not in prompt

    def test_plan_review_prompt_backward_compat_without_kwarg(self) -> None:
        prompt = helper.build_codex_plan_review_prompt(1200, issue_context="a", plan_markdown="b")
        assert "<sensitive_scope>" not in prompt

    def test_existing_work_prompt_includes_guardrail_when_sensitive(self) -> None:
        prompt = helper.build_codex_existing_work_review_prompt(
            1200,
            issue_context="irrelevant",
            plan_markdown="irrelevant",
            assessment={
                "branch": "issue-1200",
                "base_ref": "origin/main",
                "ahead_of_main": 1,
                "changed_files": ["scripts/workflows/foo.py"],
                "commit_subjects": ["fix"],
            },
            sensitive_paths=["scripts/workflows/foo.py"],
        )
        assert "<sensitive_scope>" in prompt
        assert '"real_validation_present"' in prompt

    def test_pr_review_prompt_includes_guardrail_when_sensitive(self) -> None:
        prompt = helper.build_codex_pr_review_prompt(
            99,
            sensitive_paths=["src/anteroom/services/workflow_runners.py"],
        )
        assert "<sensitive_scope>" in prompt
        assert '"real_validation_present"' in prompt

    def test_pr_review_prompt_omits_guardrail_when_empty(self) -> None:
        prompt = helper.build_codex_pr_review_prompt(99, sensitive_paths=[])
        assert "<sensitive_scope>" not in prompt

    def test_implement_prompt_tells_author_to_document_real_validation(self) -> None:
        prompt = helper.build_claude_implement_prompt(1200, sensitive_paths=["scripts/workflows/foo.py"])
        assert "Real validation:" in prompt
        assert "sensitive workflow-control/Git-integration paths" in prompt

    def test_implement_prompt_omits_block_when_non_sensitive(self) -> None:
        prompt = helper.build_claude_implement_prompt(1200, sensitive_paths=[])
        assert "Real validation:" not in prompt

    def test_fix_pr_prompt_tells_author_to_document_real_validation(self) -> None:
        prompt = helper.build_claude_pr_fix_prompt(
            99,
            review_context="",
            sensitive_paths=["src/anteroom/services/workflow_engine.py"],
        )
        assert "Real validation:" in prompt


# ---------------------------------------------------------------------------
# apply_validation_gate
# ---------------------------------------------------------------------------


class TestApplyValidationGate:
    def test_passes_through_non_sensitive_scope(self) -> None:
        review = {
            "decision": "approve",
            "comment_markdown": "looks good",
            "real_validation_present": False,
        }
        decision, comment = helper.apply_validation_gate(review, sensitive_paths=[], context_label="plan review")
        assert decision == "approve"
        assert comment == "looks good"

    def test_passes_through_when_present_is_true(self) -> None:
        review = {
            "decision": "approve",
            "comment_markdown": "looks good",
            "real_validation_present": True,
        }
        decision, comment = helper.apply_validation_gate(
            review,
            sensitive_paths=["scripts/workflows/foo.py"],
            context_label="plan review",
        )
        assert decision == "approve"
        assert comment == "looks good"

    def test_forces_changes_requested_when_present_is_false(self) -> None:
        review = {
            "decision": "approve",
            "comment_markdown": "looks good",
            "real_validation_present": False,
        }
        decision, comment = helper.apply_validation_gate(
            review, sensitive_paths=["scripts/workflows/foo.py"], context_label="plan review"
        )
        assert decision == "changes_requested"
        assert "Blocked" in comment
        assert "real-behavior validation" in comment
        assert "scripts/workflows/foo.py" in comment
        assert "plan review" in comment

    def test_forces_changes_requested_when_field_missing(self) -> None:
        review = {"decision": "approve", "comment_markdown": "looks good"}
        decision, comment = helper.apply_validation_gate(
            review,
            sensitive_paths=["scripts/workflows/foo.py"],
            context_label="PR review",
        )
        assert decision == "changes_requested"
        assert "Blocked" in comment


# ---------------------------------------------------------------------------
# cmd_review_plan / cmd_review_existing_work override integration
# ---------------------------------------------------------------------------


def _codex_result(text: str, exit_code: int = 0):
    return helper.CodexRunResult(text=text, exit_code=exit_code)


class TestCmdReviewPlanGuardrail:
    def test_overrides_approve_when_sensitive_plan_missing_validation(self) -> None:
        args = SimpleNamespace(issue=1200)
        issue_body = (
            "## Description\nDo workflow things.\n\n"
            f"{helper.PLAN_START}\n"
            "### Files to Modify\n"
            "- `scripts/workflows/local_cli_issue_flow.py` — tweak\n"
            f"{helper.PLAN_END}"
        )
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "issue_data", return_value={"body": issue_body}),
            patch.object(
                helper,
                "codex_once",
                return_value=_codex_result(
                    '{"decision":"approve","summary":"OK","comment_markdown":"Approved",'
                    '"real_validation_required":true,"real_validation_present":false}'
                ),
            ),
            patch.object(helper, "post_issue_comment") as mock_post,
            patch.object(helper, "edit_issue_labels") as mock_labels,
            patch.object(helper, "update_state") as mock_state,
        ):
            rc = helper.cmd_review_plan(args)

        assert rc == 1
        # Should label as needs-senior-review (not approved).
        add_labels = [c.kwargs.get("add", []) for c in mock_labels.call_args_list]
        assert any("needs-senior-review" in labels for labels in add_labels)
        assert not any("senior-approved" in labels for labels in add_labels)
        # State records the forced failure reason.
        failure_kwargs = [c.kwargs for c in mock_state.call_args_list]
        assert any(k.get("last_plan_review_failure") == "missing_real_validation" for k in failure_kwargs)
        # The posted comment carries the block reason.
        assert mock_post.called
        posted_comment = mock_post.call_args.args[1]
        assert "Blocked" in posted_comment
        assert "real-behavior" in posted_comment

    def test_passes_through_when_sensitive_plan_has_real_validation(self) -> None:
        args = SimpleNamespace(issue=1200)
        issue_body = (
            "## Description\nDo workflow things.\n\n"
            f"{helper.PLAN_START}\n"
            "### Files to Modify\n"
            "- `scripts/workflows/local_cli_issue_flow.py` — tweak\n"
            f"{helper.PLAN_END}"
        )
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "issue_data", return_value={"body": issue_body}),
            patch.object(
                helper,
                "codex_once",
                return_value=_codex_result(
                    '{"decision":"approve","summary":"OK","comment_markdown":"LGTM",'
                    '"real_validation_required":true,"real_validation_present":true,'
                    '"real_validation_details":"ran temp-repo probe"}'
                ),
            ),
            patch.object(helper, "post_issue_comment"),
            patch.object(helper, "edit_issue_labels") as mock_labels,
            patch.object(helper, "update_state"),
        ):
            rc = helper.cmd_review_plan(args)

        assert rc == 0
        add_labels = [c.kwargs.get("add", []) for c in mock_labels.call_args_list]
        assert any("senior-approved" in labels for labels in add_labels)

    def test_non_sensitive_scope_passes_through(self) -> None:
        args = SimpleNamespace(issue=1200)
        issue_body = (
            "## Description\nDo general things.\n\n"
            f"{helper.PLAN_START}\n"
            "### Files to Modify\n"
            "- `src/anteroom/cli/repl.py` — tweak (NOT sensitive)\n"
            f"{helper.PLAN_END}"
        )
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "issue_data", return_value={"body": issue_body}),
            patch.object(
                helper,
                "codex_once",
                return_value=_codex_result(
                    # No real_validation_present field at all — override
                    # should NOT fire because scope is not sensitive.
                    '{"decision":"approve","summary":"OK","comment_markdown":"LGTM"}'
                ),
            ),
            patch.object(helper, "post_issue_comment"),
            patch.object(helper, "edit_issue_labels") as mock_labels,
            patch.object(helper, "update_state"),
        ):
            rc = helper.cmd_review_plan(args)

        assert rc == 0
        add_labels = [c.kwargs.get("add", []) for c in mock_labels.call_args_list]
        assert any("senior-approved" in labels for labels in add_labels)


class TestCmdReviewPrGuardrail:
    def test_overrides_approve_when_sensitive_pr_missing_validation(self) -> None:
        args = SimpleNamespace(issue=1200)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "ensure_pr_number", return_value=42),
            patch.object(
                helper,
                "pr_changed_file_paths",
                return_value=["scripts/workflows/local_cli_issue_flow.py"],
            ),
            patch.object(
                helper,
                "codex_once",
                return_value=_codex_result(
                    '{"decision":"approve","summary":"OK","comment_markdown":"LGTM",'
                    '"real_validation_required":true,"real_validation_present":false}'
                ),
            ),
            patch.object(helper, "post_pr_review") as mock_post,
            patch.object(helper, "edit_pr_labels") as mock_labels,
            patch.object(helper, "update_state") as mock_state,
        ):
            rc = helper.cmd_review_pr(args)

        assert rc == 1
        add_labels = [c.kwargs.get("add", []) for c in mock_labels.call_args_list]
        assert any("needs-senior-review" in labels for labels in add_labels)
        assert not any("senior-approved" in labels for labels in add_labels)
        posted_decision = mock_post.call_args.args[1]
        assert posted_decision == "changes_requested"
        posted_comment = mock_post.call_args.args[2]
        assert "Blocked" in posted_comment
        failure_kwargs = [c.kwargs for c in mock_state.call_args_list]
        assert any(k.get("last_pr_review_failure") == "missing_real_validation" for k in failure_kwargs)

    def test_overrides_when_pr_body_missing_validation_section(self) -> None:
        """Defense-in-depth: Codex claims real_validation_present=true but
        the PR body doesn't contain the ## Real-behavior validation
        section. The command must still force changes_requested."""
        args = SimpleNamespace(issue=1200)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "ensure_pr_number", return_value=42),
            patch.object(
                helper,
                "pr_changed_file_paths",
                return_value=["scripts/workflows/local_cli_issue_flow.py"],
            ),
            patch.object(
                helper,
                "codex_once",
                return_value=_codex_result(
                    '{"decision":"approve","summary":"OK","comment_markdown":"LGTM",'
                    '"real_validation_required":true,"real_validation_present":true,'
                    '"real_validation_details":"ran temp-repo probe"}'
                ),
            ),
            patch.object(
                helper,
                "run_json",
                return_value={"body": "Implements #1200\n\nGenerated by workflow."},
            ),
            patch.object(helper, "post_pr_review") as mock_post,
            patch.object(helper, "edit_pr_labels") as mock_labels,
            patch.object(helper, "update_state"),
        ):
            rc = helper.cmd_review_pr(args)

        assert rc == 1
        posted_decision = mock_post.call_args.args[1]
        assert posted_decision == "changes_requested"
        posted_comment = mock_post.call_args.args[2]
        assert "missing the" in posted_comment
        add_labels = [c.kwargs.get("add", []) for c in mock_labels.call_args_list]
        assert not any("senior-approved" in labels for labels in add_labels)

    def test_approves_when_sensitive_and_note_present_and_body_has_section(self) -> None:
        args = SimpleNamespace(issue=1200)
        body_with_section = (
            "Implements #1200\n\nGenerated by workflow.\n\n"
            "## Real-behavior validation\n\n"
            "Touched sensitive paths:\n- scripts/workflows/foo.py\n\n"
            "Validation step run by the author agent:\n\nran temp-repo probe\n"
        )
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "ensure_pr_number", return_value=42),
            patch.object(
                helper,
                "pr_changed_file_paths",
                return_value=["scripts/workflows/foo.py"],
            ),
            patch.object(
                helper,
                "codex_once",
                return_value=_codex_result(
                    '{"decision":"approve","summary":"OK","comment_markdown":"LGTM",'
                    '"real_validation_required":true,"real_validation_present":true,'
                    '"real_validation_details":"temp-repo probe"}'
                ),
            ),
            patch.object(helper, "run_json", return_value={"body": body_with_section}),
            patch.object(helper, "post_pr_review"),
            patch.object(helper, "edit_pr_labels") as mock_labels,
            patch.object(helper, "update_state"),
        ):
            rc = helper.cmd_review_pr(args)

        assert rc == 0
        add_labels = [c.kwargs.get("add", []) for c in mock_labels.call_args_list]
        assert any("senior-approved" in labels for labels in add_labels)


# ---------------------------------------------------------------------------
# cmd_open_pr PR-body persistence
# ---------------------------------------------------------------------------


class TestCmdOpenPrValidationPersistence:
    def test_injects_validation_section_when_sensitive_and_note_present(self) -> None:
        args = SimpleNamespace(issue=1200)
        summary = (
            "Applied the workflow tweak.\n\nReal validation: ran `python3 probe.py` against a temp git repo; exit 0."
        )
        captured_body: dict[str, str] = {}

        def fake_run_stdout(cmd, *, cwd=None):
            if cmd[:3] == ["gh", "pr", "create"]:
                # The temp body-file is at cmd[cmd.index("--body-file") + 1].
                idx = cmd.index("--body-file")
                captured_body["content"] = Path(cmd[idx + 1]).read_text()
                return "https://example.com/pr/55"
            if cmd[:3] == ["git", "diff", "--name-only"]:
                return "scripts/workflows/local_cli_issue_flow.py\nsrc/anteroom/services/storage.py"
            raise AssertionError(f"Unexpected stdout call: {cmd}")

        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "branch": "issue-1200-thing",
                    "issue_title": "Do workflow thing",
                    "implementation_summary": summary,
                },
            ),
            patch.object(helper, "current_pr_number", side_effect=[None, 55]),
            patch.object(helper, "latest_main_ref", return_value="origin/main"),
            patch.object(helper, "run_stdout", side_effect=fake_run_stdout),
            patch.object(helper, "update_state"),
        ):
            rc = helper.cmd_open_pr(args)

        assert rc == 0
        body = captured_body["content"]
        assert "## Real-behavior validation" in body
        assert "scripts/workflows/local_cli_issue_flow.py" in body
        assert "ran `python3 probe.py`" in body
        assert "Implements #1200" in body

    def test_fails_closed_when_sensitive_and_note_missing(self) -> None:
        args = SimpleNamespace(issue=1200)
        summary_without_note = "Made the change. No validation line here."

        def fake_run_stdout(cmd, *, cwd=None):
            if cmd[:3] == ["git", "diff", "--name-only"]:
                return "scripts/workflows/local_cli_issue_flow.py"
            raise AssertionError(f"Unexpected stdout call: {cmd}")

        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "branch": "issue-1200-thing",
                    "issue_title": "Do workflow thing",
                    "implementation_summary": summary_without_note,
                },
            ),
            patch.object(helper, "current_pr_number", return_value=None),
            patch.object(helper, "latest_main_ref", return_value="origin/main"),
            patch.object(helper, "run_stdout", side_effect=fake_run_stdout),
            patch.object(helper, "update_state") as mock_state,
        ):
            rc = helper.cmd_open_pr(args)

        assert rc == 2
        # Fail state recorded with the expected reason.
        failure_kwargs = [c.kwargs for c in mock_state.call_args_list]
        assert any(k.get("last_open_pr_failure") == "missing_real_validation" for k in failure_kwargs)

    def test_non_sensitive_scope_does_not_inject_section(self) -> None:
        args = SimpleNamespace(issue=1200)
        captured_body: dict[str, str] = {}

        def fake_run_stdout(cmd, *, cwd=None):
            if cmd[:3] == ["gh", "pr", "create"]:
                idx = cmd.index("--body-file")
                captured_body["content"] = Path(cmd[idx + 1]).read_text()
                return "https://example.com/pr/56"
            if cmd[:3] == ["git", "diff", "--name-only"]:
                return "src/anteroom/cli/repl.py\nREADME.md"
            raise AssertionError(f"Unexpected stdout call: {cmd}")

        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "branch": "issue-1200-thing",
                    "issue_title": "General thing",
                    "implementation_summary": "Just some changes.",
                },
            ),
            patch.object(helper, "current_pr_number", side_effect=[None, 56]),
            patch.object(helper, "latest_main_ref", return_value="origin/main"),
            patch.object(helper, "run_stdout", side_effect=fake_run_stdout),
            patch.object(helper, "update_state"),
        ):
            rc = helper.cmd_open_pr(args)

        assert rc == 0
        body = captured_body["content"]
        assert "## Real-behavior validation" not in body
