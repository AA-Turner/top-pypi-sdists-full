"""Tests for scripts/workflows/local_cli_issue_flow.py invocation helpers."""

from __future__ import annotations

import io
import json
import subprocess
import threading
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest


# The helper script is not a package — import it via importlib so tests work
# regardless of sys.path configuration.
def _import_helper():
    import importlib.util

    script = Path(__file__).resolve().parents[2] / "scripts" / "workflows" / "local_cli_issue_flow.py"
    spec = importlib.util.spec_from_file_location("local_cli_issue_flow", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


helper = _import_helper()


class FakePopen:
    def __init__(self, *, stdout: str = "", stderr: str = "", returncode: int = 0) -> None:
        self.stdout = io.StringIO(stdout)
        self.stderr = io.StringIO(stderr)
        self.returncode = returncode
        self.pid = 12345

    def wait(self) -> int:
        return self.returncode

    def poll(self) -> int | None:
        return self.returncode

    def terminate(self) -> None:
        self.returncode = self.returncode or -15

    def kill(self) -> None:
        self.returncode = self.returncode or -9


class TestClaudeOnce:
    def test_invocation_uses_stream_json_and_permission_bypass(self, tmp_path: Path) -> None:
        fake = FakePopen(
            stdout='{"type":"result","result":"plan output"}\n',
        )
        with patch.object(subprocess, "Popen", return_value=fake) as mock_popen:
            result = helper.claude_once("Draft a plan", cwd=tmp_path)

        mock_popen.assert_called_once()
        args = mock_popen.call_args
        cmd = args[0][0]
        assert cmd == [
            "claude",
            "-p",
            "--verbose",
            "--output-format",
            "stream-json",
            "--include-partial-messages",
            "--permission-mode",
            "bypassPermissions",
            "--",
            "Draft a plan",
        ]
        assert args[1]["cwd"] == str(tmp_path)
        assert result == "plan output"

    def test_no_minus_c_flag(self, tmp_path: Path) -> None:
        fake = FakePopen(stdout='{"type":"result","result":"ok"}\n')
        with patch.object(subprocess, "Popen", return_value=fake) as mock_popen:
            helper.claude_once("prompt", cwd=tmp_path)

        cmd = mock_popen.call_args[0][0]
        assert "-C" not in cmd

    def test_prompt_with_dashes_not_parsed_as_flag(self, tmp_path: Path) -> None:
        prompt = "--this looks like a flag"
        fake = FakePopen(stdout='{"type":"result","result":"ok"}\n')
        with patch.object(subprocess, "Popen", return_value=fake) as mock_popen:
            helper.claude_once(prompt, cwd=tmp_path)

        cmd = mock_popen.call_args[0][0]
        assert cmd[-1] == prompt
        assert "--" in cmd  # separator before prompt

    def test_partial_text_flushes_before_newline(self, tmp_path: Path) -> None:
        long_text = "A" * 80
        fake = FakePopen(
            stdout=(
                '{"type":"stream_event","event":{"type":"content_block_delta","delta":{"text":"' + long_text + '"}}}\n'
                '{"type":"result","result":"done"}\n'
            )
        )
        with patch.object(subprocess, "Popen", return_value=fake), patch("builtins.print") as mock_print:
            helper.claude_once("prompt", cwd=tmp_path)

        printed = [call.args[0] for call in mock_print.call_args_list if call.args]
        assert any(len(line) >= helper.STREAM_SOFT_LIMIT for line in printed)

    def test_uses_structured_stdout_error_when_claude_exits_nonzero(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        fake = FakePopen(
            stdout=(
                '{"type":"assistant","message":{"content":[{"type":"text","text":"Credit balance is too low"}]}}\n'
                '{"type":"result","result":"Credit balance is too low"}\n'
            ),
            returncode=1,
        )
        with patch.object(subprocess, "Popen", return_value=fake), pytest.raises(SystemExit) as exc_info:
            helper.claude_once("prompt", cwd=tmp_path)

        assert exc_info.value.code == 1
        assert "Claude CLI failed: Credit balance is too low" in capsys.readouterr().err


class TestCodexOnce:
    def test_invocation_uses_json_exec_and_cwd(self, tmp_path: Path) -> None:
        event = {
            "type": "item.completed",
            "item": {"type": "agent_message", "text": '{"decision": "approve"}'},
        }
        fake = FakePopen(stdout=json.dumps(event) + "\n")
        with patch.object(subprocess, "Popen", return_value=fake) as mock_popen:
            result = helper.codex_once("Review the plan", cwd=tmp_path)

        cmd = mock_popen.call_args[0][0]
        assert cmd == [
            "codex",
            "exec",
            "--json",
            "--color",
            "never",
            "--dangerously-bypass-approvals-and-sandbox",
            "--",
            "Review the plan",
        ]
        assert mock_popen.call_args[1]["cwd"] == str(tmp_path)
        assert result.text == '{"decision": "approve"}'
        assert result.timed_out is False

    def test_extra_flags_inserted_before_prompt(self, tmp_path: Path) -> None:
        event = {
            "type": "item.completed",
            "item": {"type": "agent_message", "text": "ok"},
        }
        fake = FakePopen(stdout=json.dumps(event) + "\n")
        with patch.object(subprocess, "Popen", return_value=fake) as mock_popen:
            helper.codex_once("prompt", cwd=tmp_path, extra_flags=["--disable", "plugins"])

        cmd = mock_popen.call_args[0][0]
        assert cmd == [
            "codex",
            "exec",
            "--json",
            "--color",
            "never",
            "--dangerously-bypass-approvals-and-sandbox",
            "--disable",
            "plugins",
            "--",
            "prompt",
        ]

    def test_no_minus_c_flag(self, tmp_path: Path) -> None:
        fake = FakePopen(stdout='{"type":"item.completed","item":{"type":"agent_message","text":"ok"}}\n')
        with patch.object(subprocess, "Popen", return_value=fake) as mock_popen:
            helper.codex_once("prompt", cwd=tmp_path)

        cmd = mock_popen.call_args[0][0]
        assert "-C" not in cmd

    def test_returns_last_agent_message_and_streams_command_events(self, tmp_path: Path) -> None:
        events = [
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": "Inspecting issue now."},
            },
            {
                "type": "item.started",
                "item": {
                    "type": "command_execution",
                    "command": '/bin/zsh -lc "gh issue view 1117"',
                },
            },
            {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "aggregated_output": "Issue body line 1\nIssue body line 2\n",
                },
            },
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": '{"decision": "approve"}'},
            },
        ]
        fake = FakePopen(stdout="\n".join(json.dumps(event) for event in events) + "\n")
        with patch.object(subprocess, "Popen", return_value=fake), patch("builtins.print") as mock_print:
            result = helper.codex_once("prompt", cwd=tmp_path)

        printed = [call.args[0] for call in mock_print.call_args_list if call.args]
        assert '[command] /bin/zsh -lc "gh issue view 1117"' in printed
        assert "Issue body line 1" in printed
        assert result.text == '{"decision": "approve"}'

    def test_returns_timeout_result_and_kills_process_group(self, tmp_path: Path) -> None:
        release_read = threading.Event()

        class BlockingStdout:
            closed = False

            def readline(self) -> str:
                release_read.wait(1)
                return ""

        fake = FakePopen(stdout="", stderr="Command timed out after 120s\n")
        fake.stdout = BlockingStdout()
        monotonic_values = iter([0.0, 0.05, 0.11])

        def terminate(proc: FakePopen) -> None:
            proc.returncode = -9
            release_read.set()

        with (
            patch.object(subprocess, "Popen", return_value=fake),
            patch.object(helper.time, "monotonic", side_effect=lambda: next(monotonic_values)),
            patch.object(helper, "_terminate_process_group", side_effect=terminate) as mock_kill,
        ):
            result = helper.codex_once("prompt", cwd=tmp_path, timeout_seconds=0.1)

        assert result.timed_out is True
        assert result.exit_code == 124
        mock_kill.assert_called_once_with(fake)

    def test_timeout_does_not_wait_for_blocked_stdout_read(self, tmp_path: Path) -> None:
        release_read = threading.Event()

        class BlockingStdout:
            closed = False

            def readline(self) -> str:
                release_read.wait(1)
                return ""

        fake = FakePopen(stderr="timed out\n")
        fake.stdout = BlockingStdout()
        monotonic_values = iter([0.0, 0.05, 0.11])

        def terminate(proc: FakePopen) -> None:
            proc.returncode = -9
            release_read.set()

        with (
            patch.object(subprocess, "Popen", return_value=fake),
            patch.object(helper.time, "monotonic", side_effect=lambda: next(monotonic_values)),
            patch.object(helper, "_terminate_process_group", side_effect=terminate) as mock_kill,
        ):
            result = helper.codex_once("prompt", cwd=tmp_path, timeout_seconds=0.1)

        assert result.timed_out is True
        assert result.exit_code == 124
        mock_kill.assert_called_once_with(fake)

    def test_timeout_spawn_uses_dedicated_process_group(self, tmp_path: Path) -> None:
        fake = FakePopen(stdout='{"type":"item.completed","item":{"type":"agent_message","text":"ok"}}\n')
        with patch.object(subprocess, "Popen", return_value=fake) as mock_popen:
            helper.codex_once("prompt", cwd=tmp_path)

        kwargs = mock_popen.call_args.kwargs
        if helper.os.name == "nt":
            assert kwargs["creationflags"] == subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            assert kwargs["start_new_session"] is True


class TestReviewCommands:
    def test_build_existing_work_review_prompt_focuses_on_changed_branch_state(self) -> None:
        prompt = helper.build_codex_existing_work_review_prompt(
            1179,
            issue_context="## Description\nUnify runtime version metadata.",
            plan_markdown="## Summary\nReview current branch state.",
            assessment={
                "branch": "issue-1179-unify-runtime-version",
                "base_ref": "origin/main",
                "ahead_of_main": 2,
                "changed_files": ["src/anteroom/__init__.py", "tests/unit/test_cli_init.py"],
                "commit_subjects": ["feat: unify version metadata", "test: cover version metadata"],
            },
        )

        assert "This is NOT a fresh-plan review" in prompt
        assert "Do NOT read or inspect files that are not in the changed-files list" in prompt
        assert "src/anteroom/__init__.py" in prompt
        assert "feat: unify version metadata" in prompt

    def test_build_plan_review_prompt_focuses_on_extracted_plan(self) -> None:
        prompt = helper.build_codex_plan_review_prompt(
            1229,
            issue_context="## Description\nTight startup bug.",
            plan_markdown="## Summary\nFix startup.\n## Files to Modify\n- src/anteroom/services/ai_service.py",
        )

        assert "<issue_context>" in prompt
        assert "Tight startup bug." in prompt
        assert "<implementation_plan>" in prompt
        assert "Fix startup." in prompt
        assert "Do not wander through unrelated code." in prompt

    def test_review_plan_missing_plan_fails_fast(self) -> None:
        args = SimpleNamespace(issue=1201)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(helper, "ensure_worktree", return_value={"worktree_path": "/tmp/worktree"}),
            patch.object(helper, "issue_data", return_value={"body": "## Description\nNo plan yet."}),
            patch.object(helper, "edit_issue_labels") as mock_labels,
            patch.object(helper, "update_state") as mock_state,
            patch.object(helper, "codex_once") as mock_codex,
        ):
            assert helper.cmd_review_plan(args) == 2

        mock_labels.assert_called_once_with(1201, add=["needs-senior-review"], remove=["senior-approved"])
        assert mock_state.call_args.kwargs["last_plan_review_failure"] == "missing_plan"
        mock_codex.assert_not_called()

    def test_review_existing_work_approve_sets_senior_approved(self) -> None:
        args = SimpleNamespace(issue=1179)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "existing_work_assessment": {
                        "implementation_present": True,
                        "branch": "issue-1179",
                        "base_ref": "origin/main",
                        "ahead_of_main": 2,
                        "changed_files": ["src/anteroom/__init__.py"],
                        "commit_subjects": ["feat: unify version metadata"],
                    },
                },
            ),
            patch.object(
                helper,
                "issue_data",
                return_value={
                    "body": (
                        "## Description\nScoped bug.\n\n"
                        f"{helper.PLAN_START}\n## Summary\nReview branch state.\n{helper.PLAN_END}"
                    )
                },
            ),
            patch.object(
                helper,
                "codex_once",
                return_value=helper.CodexRunResult(
                    text='{"decision":"approve","summary":"Looks good","comment_markdown":"Approved"}',
                    exit_code=0,
                ),
            ),
            patch.object(helper, "post_issue_comment") as mock_comment,
            patch.object(helper, "edit_issue_labels") as mock_labels,
            patch.object(helper, "update_state") as mock_state,
        ):
            assert helper.cmd_review_existing_work(args) == 0

        mock_comment.assert_called_once()
        mock_labels.assert_called_once_with(1179, add=["senior-approved"], remove=["needs-senior-review"])
        assert mock_state.call_args.kwargs["last_plan_review_decision"] == "approve"

    def test_existing_work_prompt_excludes_senior_reviewer_phrasing(self) -> None:
        prompt = helper.build_codex_existing_work_review_prompt(
            1301,
            issue_context="## Description\nNarrow review scope.",
            plan_markdown="## Summary\nScope the review.",
            assessment={
                "branch": "issue-1301",
                "base_ref": "origin/main",
                "ahead_of_main": 1,
                "changed_files": ["scripts/workflows/local_cli_issue_flow.py"],
                "commit_subjects": ["fix: narrow review"],
            },
        )
        assert "existing-work validator" in prompt
        assert "Do NOT run the test suite" in prompt
        assert "Do NOT execute pytest" in prompt
        assert "Do NOT perform a senior review or act as a senior reviewer" in prompt
        assert "senior reviewer for" not in prompt

    def test_existing_work_review_passes_disable_plugins_flag(self) -> None:
        args = SimpleNamespace(issue=1301)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "existing_work_assessment": {
                        "implementation_present": True,
                        "branch": "issue-1301",
                        "base_ref": "origin/main",
                        "ahead_of_main": 1,
                        "changed_files": ["scripts/workflows/local_cli_issue_flow.py"],
                        "commit_subjects": ["fix: narrow review"],
                    },
                },
            ),
            patch.object(
                helper,
                "issue_data",
                return_value={
                    "body": (
                        "## Description\nNarrow review.\n\n"
                        f"{helper.PLAN_START}\n## Summary\nScope the review.\n{helper.PLAN_END}"
                    )
                },
            ),
            patch.object(
                helper,
                "codex_once",
                return_value=helper.CodexRunResult(
                    text='{"decision":"approve","summary":"OK","comment_markdown":"Approved"}',
                    exit_code=0,
                ),
            ) as mock_codex,
            patch.object(helper, "post_issue_comment"),
            patch.object(helper, "edit_issue_labels"),
            patch.object(helper, "update_state"),
        ):
            assert helper.cmd_review_existing_work(args) == 0

        assert mock_codex.call_args.kwargs["extra_flags"] == ["--disable", "plugins"]

    def test_existing_work_timeout_reports_timeout_as_primary_cause(self) -> None:
        args = SimpleNamespace(issue=1301)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "existing_work_assessment": {
                        "implementation_present": True,
                        "branch": "issue-1301",
                        "base_ref": "origin/main",
                        "ahead_of_main": 1,
                        "changed_files": ["scripts/workflows/local_cli_issue_flow.py"],
                        "commit_subjects": ["fix: narrow review"],
                    },
                },
            ),
            patch.object(
                helper,
                "issue_data",
                return_value={
                    "body": (
                        "## Description\nNarrow review.\n\n"
                        f"{helper.PLAN_START}\n## Summary\nScope it.\n{helper.PLAN_END}"
                    )
                },
            ),
            patch.object(
                helper,
                "codex_once",
                return_value=helper.CodexRunResult(
                    text="",
                    timed_out=True,
                    stderr="Reading additional input from stdin...\nSome real error",
                    exit_code=124,
                ),
            ),
            patch.object(helper, "edit_issue_labels"),
            patch.object(helper, "update_state") as mock_state,
        ):
            assert helper.cmd_review_existing_work(args) == 2

        error = mock_state.call_args.kwargs["last_plan_review_error"]
        assert error.startswith("Timed out after ")
        assert "Reading additional input from stdin" not in error
        assert "Some real error" in error

    def test_existing_work_timeout_with_only_noise_stderr(self) -> None:
        args = SimpleNamespace(issue=1301)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "existing_work_assessment": {
                        "implementation_present": True,
                        "branch": "issue-1301",
                        "base_ref": "origin/main",
                        "ahead_of_main": 1,
                        "changed_files": ["scripts/workflows/local_cli_issue_flow.py"],
                        "commit_subjects": ["fix: narrow review"],
                    },
                },
            ),
            patch.object(
                helper,
                "issue_data",
                return_value={
                    "body": (
                        "## Description\nNarrow review.\n\n"
                        f"{helper.PLAN_START}\n## Summary\nScope it.\n{helper.PLAN_END}"
                    )
                },
            ),
            patch.object(
                helper,
                "codex_once",
                return_value=helper.CodexRunResult(
                    text="",
                    timed_out=True,
                    stderr="Reading additional input from stdin...",
                    exit_code=124,
                ),
            ),
            patch.dict(helper.os.environ, {"ANTEROOM_LOCAL_PLAN_REVIEW_TIMEOUT_SECONDS": "300"}, clear=False),
            patch.object(helper, "edit_issue_labels"),
            patch.object(helper, "update_state") as mock_state,
        ):
            assert helper.cmd_review_existing_work(args) == 2

        error = mock_state.call_args.kwargs["last_plan_review_error"]
        assert error == "Timed out after 300s"
        assert "stdin" not in error


class TestStderrNoiseFiltering:
    def test_filter_removes_stdin_noise(self) -> None:
        raw = "Reading additional input from stdin...\nActual error\nreading from stdin"
        assert helper._filter_stderr_noise(raw) == "Actual error"

    def test_filter_preserves_real_errors(self) -> None:
        raw = "Connection refused\nTimeout exceeded"
        assert helper._filter_stderr_noise(raw) == "Connection refused\nTimeout exceeded"

    def test_filter_empty_after_noise_removal(self) -> None:
        raw = "Reading additional input from stdin..."
        assert helper._filter_stderr_noise(raw) == ""

    def test_timeout_error_message_leads_with_timeout(self) -> None:
        msg = helper._timeout_error_message(300, "Reading additional input from stdin...\nReal error")
        assert msg.startswith("Timed out after 300s")
        assert "Real error" in msg
        assert "stdin" not in msg

    def test_timeout_error_message_without_stderr(self) -> None:
        msg = helper._timeout_error_message(300, "")
        assert msg == "Timed out after 300s"


class TestExistingWorkFastPath:
    def test_assess_existing_work_detects_committed_branch_changes(self, tmp_path: Path) -> None:
        root = tmp_path / "repo"
        worktree = tmp_path / "worktree"
        root.mkdir()
        worktree.mkdir()
        state = {"worktree_path": str(worktree), "branch": "issue-1179"}

        def fake_run_stdout(command: list[str], *, cwd: Path | None = None) -> str:
            if command[:3] == ["git", "rev-list", "--count"] and command[3] in {"origin/main..HEAD", "main..HEAD"}:
                return "2"
            if command[:3] == ["git", "diff", "--name-only"]:
                return "src/anteroom/__init__.py\ntests/unit/test_cli_init.py\n"
            if command[:3] == ["git", "log", "--format=%s"]:
                return "feat: unify version metadata\ntest: cover version metadata\n"
            if command[:3] == ["git", "status", "--porcelain"]:
                return ""
            raise AssertionError(command)

        with (
            patch.object(helper, "run"),
            patch.object(helper, "run_stdout", side_effect=fake_run_stdout),
        ):
            result = helper.assess_existing_work(root, state)

        assert result["implementation_present"] is True
        assert result["ahead_of_main"] == 2
        assert result["worktree_clean"] is True
        assert result["changed_files"] == ["src/anteroom/__init__.py", "tests/unit/test_cli_init.py"]
        assert result["commit_subjects"] == ["feat: unify version metadata", "test: cover version metadata"]

    def test_cmd_assess_existing_work_prints_existing_work_token(self, capsys: pytest.CaptureFixture[str]) -> None:
        args = SimpleNamespace(issue=1179)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(helper, "ensure_worktree", return_value={"worktree_path": "/tmp/worktree"}),
            patch.object(
                helper,
                "assess_existing_work",
                return_value={"implementation_present": True, "changed_files": ["src/anteroom/__init__.py"]},
            ),
            patch.object(helper, "update_state") as mock_state,
        ):
            assert helper.cmd_assess_existing_work(args) == 0

        assert capsys.readouterr().out.strip() == "existing_work_present"
        assert mock_state.call_args.kwargs["existing_work_assessment"]["implementation_present"] is True

    def test_cmd_plan_existing_work_updates_issue_plan_without_claude(self) -> None:
        args = SimpleNamespace(issue=1179)
        assessment = {
            "implementation_present": True,
            "branch": "issue-1179",
            "base_ref": "origin/main",
            "ahead_of_main": 2,
            "changed_files": ["src/anteroom/__init__.py"],
            "commit_subjects": ["feat: unify version metadata"],
            "changed_test_files": ["tests/unit/test_cli_init.py"],
        }
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree", "existing_work_assessment": assessment},
            ),
            patch.object(helper, "update_issue_plan") as mock_plan,
            patch.object(helper, "edit_issue_labels") as mock_labels,
            patch.object(helper, "update_state") as mock_state,
            patch.object(helper, "claude_once") as mock_claude,
        ):
            assert helper.cmd_plan_existing_work(args) == 0

        mock_claude.assert_not_called()
        mock_plan.assert_called_once()
        mock_labels.assert_called_once_with(1179, add=["needs-senior-review"], remove=["senior-approved"])
        assert mock_state.call_args.kwargs["last_plan_review_decision"] == "pending"

    def test_review_plan_timeout_leaves_needs_review_and_returns_failure(self) -> None:
        args = SimpleNamespace(issue=1201)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(helper, "ensure_worktree", return_value={"worktree_path": "/tmp/worktree"}),
            patch.object(
                helper,
                "issue_data",
                return_value={
                    "body": (
                        "## Description\nScoped bug.\n\n"
                        f"{helper.PLAN_START}\n## Summary\nTight plan.\n{helper.PLAN_END}"
                    )
                },
            ),
            patch.object(
                helper,
                "codex_once",
                return_value=helper.CodexRunResult(
                    text="",
                    timed_out=True,
                    stderr="Command timed out after 120s",
                    exit_code=124,
                ),
            ),
            patch.object(helper, "edit_issue_labels") as mock_labels,
            patch.object(helper, "update_state") as mock_state,
        ):
            assert helper.cmd_review_plan(args) == 2

        mock_labels.assert_called_once_with(1201, add=["needs-senior-review"], remove=["senior-approved"])
        assert mock_state.call_args.kwargs["last_plan_review_decision"] == "review_failed"
        assert mock_state.call_args.kwargs["last_plan_review_failure"] == "timed_out"

    def test_review_plan_uses_configured_timeout(self) -> None:
        args = SimpleNamespace(issue=1201)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(helper, "ensure_worktree", return_value={"worktree_path": "/tmp/worktree"}),
            patch.object(
                helper,
                "issue_data",
                return_value={
                    "body": (
                        "## Description\nScoped bug.\n\n"
                        f"{helper.PLAN_START}\n## Summary\nTight plan.\n{helper.PLAN_END}"
                    )
                },
            ),
            patch.dict(helper.os.environ, {"ANTEROOM_LOCAL_PLAN_REVIEW_TIMEOUT_SECONDS": "420"}, clear=False),
            patch.object(
                helper,
                "codex_once",
                return_value=helper.CodexRunResult(text='{"decision":"approve"}', exit_code=0),
            ) as mock_codex,
            patch.object(helper, "post_issue_comment"),
            patch.object(helper, "edit_issue_labels"),
            patch.object(helper, "update_state"),
        ):
            helper.cmd_review_plan(args)

        assert mock_codex.call_args.kwargs["timeout_seconds"] == 420

    def test_review_pr_invalid_output_leaves_needs_review_and_returns_failure(self) -> None:
        args = SimpleNamespace(issue=1201)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(helper, "ensure_worktree", return_value={"worktree_path": "/tmp/worktree"}),
            patch.object(helper, "ensure_pr_number", return_value=55),
            patch.object(helper, "codex_once", return_value=helper.CodexRunResult(text="not json", exit_code=0)),
            patch.object(helper, "edit_pr_labels") as mock_labels,
            patch.object(helper, "update_state") as mock_state,
        ):
            assert helper.cmd_review_pr(args) == 2

        mock_labels.assert_called_once_with(55, add=["needs-senior-review"], remove=["senior-approved"])
        assert mock_state.call_args.kwargs["last_pr_review_decision"] == "review_failed"
        assert mock_state.call_args.kwargs["last_pr_review_failure"] == "invalid_output"


class TestEnsureTool:
    def test_passes_when_tool_exists(self) -> None:
        with patch("shutil.which", return_value="/usr/bin/git"):
            helper.ensure_tool("git")  # should not raise

    def test_fails_when_tool_missing(self) -> None:
        with patch("shutil.which", return_value=None):
            with pytest.raises(SystemExit) as exc_info:
                helper.ensure_tool("nonexistent-tool")
            assert exc_info.value.code == 1


class TestRunStdout:
    def test_returns_stripped_stdout(self) -> None:
        fake = MagicMock(returncode=0, stdout="  hello world  \n", stderr="")
        with patch.object(subprocess, "run", return_value=fake):
            assert helper.run_stdout(["echo", "hello"]) == "hello world"

    def test_raises_on_nonzero_exit(self) -> None:
        fake = MagicMock(returncode=1, stdout="", stderr="bad command")
        with patch.object(subprocess, "run", return_value=fake):
            with pytest.raises(SystemExit):
                helper.run_stdout(["false"])


class TestStateDir:
    def test_uses_real_git_dir_not_dot_git_path(self, tmp_path: Path) -> None:
        root = tmp_path / "repo"
        root.mkdir()
        gitdir = tmp_path / "git-meta" / "worktree-a"

        with patch.object(helper, "run_stdout", return_value=str(gitdir)):
            result = helper.state_dir(root, 1092)

        assert result == gitdir / helper.STATE_DIRNAME / "issue-1092"


class TestRequiredToolsForAction:
    def test_prepare_only_needs_git_and_gh(self) -> None:
        assert helper._required_tools_for_action("prepare") == ("gh", "git")

    def test_plan_needs_claude(self) -> None:
        assert helper._required_tools_for_action("plan") == ("gh", "git", "claude")

    def test_review_pr_needs_codex(self) -> None:
        assert helper._required_tools_for_action("review-pr") == ("gh", "git", "codex")


class TestWorktreeHelpers:
    def test_list_worktrees_parses_porcelain_output(self) -> None:
        output = (
            "worktree /tmp/repo\n"
            "HEAD abc123\n"
            "branch refs/heads/main\n"
            "\n"
            "worktree /tmp/repo-issue\n"
            "HEAD def456\n"
            "branch refs/heads/issue-1199\n"
        )

        with patch.object(helper, "run_stdout", return_value=output):
            assert helper.list_worktrees(Path("/tmp/repo")) == [
                {"worktree": "/tmp/repo", "HEAD": "abc123", "branch": "refs/heads/main"},
                {"worktree": "/tmp/repo-issue", "HEAD": "def456", "branch": "refs/heads/issue-1199"},
            ]

    def test_worktree_for_branch_returns_attached_path(self, tmp_path: Path) -> None:
        repo = tmp_path / "repo"
        repo.mkdir()
        attached = tmp_path / "repo-issue"
        attached.mkdir()
        entries = [
            {"worktree": str(repo), "branch": "refs/heads/main"},
            {"worktree": str(attached), "branch": "refs/heads/issue-1199"},
        ]

        with patch.object(helper, "list_worktrees", return_value=entries):
            assert helper.worktree_for_branch(repo, "issue-1199") == attached.resolve()

    def test_worktree_entry_for_branch_returns_missing_attached_entry(self, tmp_path: Path) -> None:
        repo = tmp_path / "repo"
        repo.mkdir()
        missing = tmp_path / "missing-worktree"
        entries = [
            {"worktree": str(missing), "branch": "refs/heads/issue-1199"},
        ]

        with patch.object(helper, "list_worktrees", return_value=entries):
            assert helper.worktree_entry_for_branch(repo, "issue-1199") == entries[0]
            assert helper.worktree_for_branch(repo, "issue-1199") is None

    def test_worktree_for_branch_ignores_prunable_or_missing_entries(self, tmp_path: Path) -> None:
        repo = tmp_path / "repo"
        repo.mkdir()
        missing = tmp_path / "missing-worktree"
        entries = [
            {
                "worktree": str(missing),
                "branch": "refs/heads/issue-1199",
                "prunable": "gitdir file points to non-existent location",
            },
        ]

        with patch.object(helper, "list_worktrees", return_value=entries):
            assert helper.worktree_entry_for_branch(repo, "issue-1199") == entries[0]
            assert helper.worktree_for_branch(repo, "issue-1199") is None

    def test_ensure_worktree_reuses_existing_attached_worktree(self, tmp_path: Path) -> None:
        root = tmp_path / "repo"
        root.mkdir()
        attached = tmp_path / "existing-worktree"
        attached.mkdir()
        branch = "issue-1199-example"
        issue = {"state": "open", "title": "Example", "url": "https://example.com/issues/1199"}

        run_results = [MagicMock(returncode=0), MagicMock(returncode=0)]

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "issue_branch", return_value=branch),
            patch.object(helper, "issue_worktree", return_value=tmp_path / "preferred-worktree"),
            patch.object(helper, "worktree_for_branch", return_value=attached),
            patch.object(
                helper,
                "sanitize_reused_worktree",
                return_value={"removed_junk": [], "tracked_dirty": [], "unexpected_untracked": []},
            ),
            patch.object(helper, "run", side_effect=run_results) as mock_run,
            patch.object(helper, "update_state", return_value={"worktree_path": str(attached)}) as mock_update_state,
        ):
            state = helper.ensure_worktree(root, 1199)

        assert state == {"worktree_path": str(attached)}
        assert mock_run.call_args_list == [
            ((["git", "fetch", "origin", "main"],), {"cwd": root, "check": False}),
            ((["git", "show-ref", "--verify", f"refs/heads/{branch}"],), {"cwd": root, "check": False}),
        ]
        mock_update_state.assert_called_once_with(
            root,
            1199,
            issue_number=1199,
            issue_title="Example",
            issue_url="https://example.com/issues/1199",
            branch=branch,
            worktree_path=str(attached),
            repo_name="owner/repo",
            worktree_python="",
            worktree_venv="",
            worktree_bin="",
            prepare_worktree_status="reused_clean",
            prepare_removed_junk=[],
            prepare_tracked_dirty_paths=[],
            prepare_unexpected_untracked_paths=[],
        )

    def test_ensure_worktree_prunes_and_recreates_missing_attached_worktree(self, tmp_path: Path) -> None:
        root = tmp_path / "repo"
        root.mkdir()
        preferred = tmp_path / "preferred-worktree"
        branch = "issue-1199-example"
        issue = {"state": "open", "title": "Example", "url": "https://example.com/issues/1199"}

        run_results = [
            MagicMock(returncode=0),
            MagicMock(returncode=0),
            MagicMock(returncode=0),
            MagicMock(returncode=0),
        ]

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "issue_branch", return_value=branch),
            patch.object(helper, "issue_worktree", return_value=preferred),
            patch.object(helper, "worktree_for_branch", side_effect=[None, None]),
            patch.object(
                helper,
                "worktree_entry_for_branch",
                return_value={"worktree": str(preferred), "branch": f"refs/heads/{branch}"},
            ),
            patch.object(helper, "run", side_effect=run_results) as mock_run,
            patch.object(helper, "update_state", return_value={"worktree_path": str(preferred)}) as mock_update_state,
        ):
            state = helper.ensure_worktree(root, 1199)

        assert state == {"worktree_path": str(preferred)}
        assert mock_run.call_args_list == [
            ((["git", "fetch", "origin", "main"],), {"cwd": root, "check": False}),
            ((["git", "show-ref", "--verify", f"refs/heads/{branch}"],), {"cwd": root, "check": False}),
            ((["git", "worktree", "prune"],), {"cwd": root}),
            ((["git", "worktree", "add", str(preferred), branch],), {"cwd": root}),
        ]
        mock_update_state.assert_called_once_with(
            root,
            1199,
            issue_number=1199,
            issue_title="Example",
            issue_url="https://example.com/issues/1199",
            branch=branch,
            worktree_path=str(preferred),
            repo_name="owner/repo",
            worktree_python="",
            worktree_venv="",
            worktree_bin="",
            prepare_worktree_status="created_clean",
            prepare_removed_junk=[],
            prepare_tracked_dirty_paths=[],
            prepare_unexpected_untracked_paths=[],
        )


class TestConsumeTextChunks:
    def test_prefers_newline_boundaries(self) -> None:
        emitted, pending = helper._consume_text_chunks("", "first line\nsecond line")
        assert emitted == ["first line"]
        assert pending == "second line"

    def test_soft_wraps_long_partial_output(self) -> None:
        emitted, pending = helper._consume_text_chunks("", "x" * 75, soft_limit=60)
        assert emitted == ["x" * 60]
        assert pending == "x" * 15


class TestWorktreePythonEnv:
    def test_detects_worktree_virtualenv(self, tmp_path: Path) -> None:
        python = tmp_path / ".venv" / "bin" / "python"
        python.parent.mkdir(parents=True)
        python.write_text("")

        result = helper.worktree_python_env(tmp_path)

        assert result["worktree_python"] == str(python.resolve())
        assert result["worktree_venv"] == str((tmp_path / ".venv").resolve())
        assert result["worktree_bin"] == str((tmp_path / ".venv" / "bin").resolve())

    def test_resolve_worktree_python_prefers_explicit_env(self) -> None:
        assert (
            helper.resolve_worktree_python(
                {helper.WORKTREE_PYTHON_ENV: "/tmp/explicit/python"},
                {"worktree_python": "/tmp/state/python"},
            )
            == "/tmp/explicit/python"
        )

    def test_resolve_worktree_python_falls_back_to_saved_state(self) -> None:
        assert helper.resolve_worktree_python({}, {"worktree_python": "/tmp/state/python"}) == "/tmp/state/python"


class TestCleanupWorktreeJunk:
    def test_removes_magicmock_artifacts(self, tmp_path: Path) -> None:
        bad = tmp_path / "<MagicMock name='mock.app.data_dir.__truediv__()' id='123'>"
        bad.write_text("junk")
        keep = tmp_path / "normal.txt"
        keep.write_text("keep")

        removed = helper.cleanup_worktree_junk(tmp_path)

        assert removed == [bad.name]
        assert not bad.exists()
        assert keep.exists()

    def test_removes_tmp_issue_body_files(self, tmp_path: Path) -> None:
        tmp_file = tmp_path / ".tmp_issue_1227_body.md"
        tmp_file.write_text("temp body")
        keep = tmp_path / "unknown_file.txt"
        keep.write_text("keep")

        removed = helper.cleanup_worktree_junk(tmp_path)

        assert tmp_file.name in removed
        assert not tmp_file.exists()
        assert keep.exists()

    def test_does_not_remove_unknown_files(self, tmp_path: Path) -> None:
        unknown = tmp_path / "unknown_file.txt"
        unknown.write_text("keep me")

        removed = helper.cleanup_worktree_junk(tmp_path)

        assert removed == []
        assert unknown.exists()

    def test_removes_multiple_tmp_issue_files(self, tmp_path: Path) -> None:
        files = []
        for n in (1, 42, 1227):
            f = tmp_path / f".tmp_issue_{n}_body.md"
            f.write_text(f"body {n}")
            files.append(f)

        removed = helper.cleanup_worktree_junk(tmp_path)

        assert sorted(removed) == sorted(f.name for f in files)
        for f in files:
            assert not f.exists()


class TestPrepareWorktreeSanitation:
    def test_classify_worktree_status_separates_tracked_and_untracked(self, tmp_path: Path) -> None:
        with patch.object(
            helper,
            "run_stdout",
            return_value=" M README.md\nA  staged.py\nR  old.py -> new.py\n?? notes.txt\n",
        ):
            result = helper.classify_worktree_status(tmp_path)

        assert result == {
            "tracked_dirty": ["README.md", "new.py", "staged.py"],
            "untracked": ["notes.txt"],
        }

    def test_sanitize_reused_worktree_allows_only_known_junk(self, tmp_path: Path) -> None:
        with (
            patch.object(helper, "cleanup_worktree_junk", return_value=["<MagicMock junk>"]) as mock_cleanup,
            patch.object(
                helper,
                "classify_worktree_status",
                return_value={"tracked_dirty": [], "untracked": ["<MagicMock junk>"]},
            ),
        ):
            result = helper.sanitize_reused_worktree(tmp_path)

        mock_cleanup.assert_called_once_with(tmp_path)
        assert result == {
            "removed_junk": ["<MagicMock junk>"],
            "tracked_dirty": [],
            "unexpected_untracked": [],
        }

    def test_sanitize_reused_worktree_fails_for_tracked_changes(self, tmp_path: Path) -> None:
        with (
            patch.object(helper, "cleanup_worktree_junk", return_value=[]),
            patch.object(
                helper,
                "classify_worktree_status",
                return_value={"tracked_dirty": ["src/app.py"], "untracked": []},
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            helper.sanitize_reused_worktree(tmp_path)

        assert exc_info.value.code == 1

    def test_sanitize_reused_worktree_fails_for_unexpected_untracked(self, tmp_path: Path) -> None:
        with (
            patch.object(helper, "cleanup_worktree_junk", return_value=[]),
            patch.object(
                helper,
                "classify_worktree_status",
                return_value={"tracked_dirty": [], "untracked": ["notes.txt"]},
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            helper.sanitize_reused_worktree(tmp_path)

        assert exc_info.value.code == 1

    def test_ensure_worktree_records_prepare_status_for_reused_clean_worktree(self, tmp_path: Path) -> None:
        root = tmp_path / "repo"
        root.mkdir()
        attached = tmp_path / "attached-worktree"
        attached.mkdir()
        branch = "issue-1223-example"
        issue = {"state": "open", "title": "Example", "url": "https://example.com/issues/1223"}

        run_results = [MagicMock(returncode=0), MagicMock(returncode=0)]

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "issue_branch", return_value=branch),
            patch.object(helper, "issue_worktree", return_value=tmp_path / "preferred-worktree"),
            patch.object(helper, "worktree_for_branch", return_value=attached),
            patch.object(
                helper,
                "sanitize_reused_worktree",
                return_value={"removed_junk": [], "tracked_dirty": [], "unexpected_untracked": []},
            ) as mock_sanitize,
            patch.object(helper, "run", side_effect=run_results),
            patch.object(helper, "update_state", return_value={"worktree_path": str(attached)}) as mock_update_state,
        ):
            helper.ensure_worktree(root, 1223)

        mock_sanitize.assert_called_once_with(attached)
        assert mock_update_state.call_args.kwargs["prepare_worktree_status"] == "reused_clean"
        assert mock_update_state.call_args.kwargs["prepare_removed_junk"] == []
        assert mock_update_state.call_args.kwargs["prepare_tracked_dirty_paths"] == []
        assert mock_update_state.call_args.kwargs["prepare_unexpected_untracked_paths"] == []

    def test_cmd_prepare_prints_path_and_prepare_summary(self) -> None:
        args = SimpleNamespace(issue=1223)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(helper, "ensure_labels"),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "prepare_worktree_status": "reused_junk_cleaned",
                    "prepare_removed_junk": ["<MagicMock junk>"],
                },
            ),
            patch("builtins.print") as mock_print,
        ):
            assert helper.cmd_prepare(args) == 0

        assert mock_print.call_args_list == [
            (("/tmp/worktree",), {}),
            (("prepare_worktree: reused_junk_cleaned (removed_junk: <MagicMock junk>)",), {"file": helper.sys.stderr}),
        ]


class TestAssertPrApproved:
    def test_passes_when_label_present(self) -> None:
        args = SimpleNamespace(issue=1140, wait_seconds=0, poll_interval=5)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(helper, "ensure_pr_number", return_value=1143),
            patch.object(helper, "pr_review_state", return_value={"label_names": ["senior-approved"]}),
        ):
            assert helper.cmd_assert_pr_approved(args) == 0

    def test_waits_and_retries_until_label_present(self) -> None:
        args = SimpleNamespace(issue=1140, wait_seconds=10, poll_interval=5)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(helper, "ensure_pr_number", return_value=1143),
            patch.object(
                helper,
                "pr_review_state",
                side_effect=[
                    {"label_names": [], "reviewDecision": "REVIEW_REQUIRED", "isDraft": True, "state": "OPEN"},
                    {
                        "label_names": ["senior-approved"],
                        "reviewDecision": "APPROVED",
                        "isDraft": False,
                        "state": "OPEN",
                    },
                ],
            ),
            patch.object(helper.time, "monotonic", side_effect=[0, 0, 5]),
            patch.object(helper.time, "sleep") as mock_sleep,
        ):
            assert helper.cmd_assert_pr_approved(args) == 0
        mock_sleep.assert_called_once_with(5)

    def test_failure_reports_pr_state(self) -> None:
        args = SimpleNamespace(issue=1140, wait_seconds=0, poll_interval=5)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(helper, "ensure_pr_number", return_value=1143),
            patch.object(
                helper,
                "pr_review_state",
                return_value={
                    "label_names": ["needs-senior-review"],
                    "reviewDecision": "REVIEW_REQUIRED",
                    "isDraft": True,
                    "state": "OPEN",
                },
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            helper.cmd_assert_pr_approved(args)

        assert exc_info.value.code == 1


class TestPrInspection:
    def test_summarize_status_checks_counts_pending_and_failures(self) -> None:
        summary = helper.summarize_status_checks(
            [
                {"conclusion": "SUCCESS", "status": "COMPLETED"},
                {"conclusion": "FAILURE", "status": "COMPLETED"},
                {"conclusion": None, "status": "IN_PROGRESS"},
            ]
        )

        assert summary == {
            "overall": "failing",
            "counts": {"pending": 1, "failing": 1, "passing": 1, "skipped": 0, "cancelled": 0},
            "has_required_pending": True,
            "has_required_failures": True,
        }

    def test_summarize_status_checks_handles_status_context_entries(self) -> None:
        summary = helper.summarize_status_checks(
            [
                {"__typename": "StatusContext", "state": "SUCCESS"},
                {"__typename": "StatusContext", "state": "PENDING"},
                {"__typename": "StatusContext", "state": "FAILURE"},
            ]
        )

        assert summary == {
            "overall": "failing",
            "counts": {"pending": 1, "failing": 1, "passing": 1, "skipped": 0, "cancelled": 0},
            "has_required_pending": True,
            "has_required_failures": True,
        }

    @pytest.mark.parametrize(
        ("payload", "expected"),
        [
            ({"exists": False}, "no_pr"),
            (
                {
                    "exists": True,
                    "branch_status": {"needs_refresh": True},
                    "check_summary": {},
                    "is_draft": False,
                    "mergeable": "mergeable",
                },
                "refresh_needed",
            ),
            (
                {
                    "exists": True,
                    "branch_status": {"needs_refresh": False},
                    "check_summary": {"has_required_failures": False, "has_required_pending": False},
                    "is_draft": True,
                    "mergeable": "mergeable",
                },
                "review_repair",
            ),
            (
                {
                    "exists": True,
                    "branch_status": {"needs_refresh": False},
                    "check_summary": {"has_required_failures": True, "has_required_pending": False},
                    "is_draft": False,
                    "mergeable": "mergeable",
                },
                "review_repair",
            ),
            (
                {
                    "exists": True,
                    "branch_status": {"needs_refresh": False},
                    "check_summary": {"has_required_failures": False, "has_required_pending": False},
                    "is_draft": False,
                    "mergeable": "mergeable",
                },
                "review_only",
            ),
        ],
    )
    def test_classify_pr_lifecycle(self, payload: dict[str, object], expected: str) -> None:
        assert helper.classify_pr_lifecycle(payload) == expected

    def test_inspect_pr_reports_no_pr_bucket(self) -> None:
        with (
            patch.object(helper, "ensure_worktree", return_value={"branch": "issue-1206-example"}),
            patch.object(helper, "current_pr_number", return_value=None),
            patch.object(helper, "run_stdout", return_value="abc123"),
        ):
            result = helper.inspect_pr_state(Path("/tmp/repo"), 1206)

        assert result["exists"] is False
        assert result["lifecycle"] == "no_pr"
        assert result["ready_for_senior_review"] is False

    def test_inspect_pr_reports_review_only_payload(self) -> None:
        with (
            patch.object(helper, "ensure_worktree", return_value={"branch": "issue-1206-example"}),
            patch.object(helper, "current_pr_number", return_value=77),
            patch.object(
                helper,
                "run_json",
                return_value={
                    "number": 77,
                    "url": "https://example.com/pr/77",
                    "state": "OPEN",
                    "isDraft": False,
                    "reviewDecision": "APPROVED",
                    "labels": [{"name": "needs-senior-review"}],
                    "mergeable": "MERGEABLE",
                    "headRefName": "issue-1206-example",
                    "baseRefName": "main",
                    "headRefOid": "headsha",
                    "baseRefOid": "basesha",
                    "statusCheckRollup": [{"conclusion": "SUCCESS", "status": "COMPLETED"}],
                },
            ),
            patch.object(
                helper,
                "branch_status",
                return_value={
                    "head_ref": "issue-1206-example",
                    "base_ref": "main",
                    "base_sha": "basesha",
                    "head_sha": "headsha",
                    "behind_base": 0,
                    "ahead_of_base": 2,
                    "diverged": False,
                    "needs_refresh": False,
                },
            ),
        ):
            result = helper.inspect_pr_state(Path("/tmp/repo"), 1206)

        assert result["pr_number"] == 77
        assert result["labels"] == ["needs-senior-review"]
        assert result["mergeable"] == "mergeable"
        assert result["check_summary"]["overall"] == "passing"
        assert result["lifecycle"] == "review_only"
        assert result["ready_for_senior_review"] is True

    def test_inspect_pr_treats_success_status_context_as_passing(self) -> None:
        with (
            patch.object(helper, "ensure_worktree", return_value={"branch": "issue-1206-example"}),
            patch.object(helper, "current_pr_number", return_value=77),
            patch.object(
                helper,
                "run_json",
                return_value={
                    "number": 77,
                    "url": "https://example.com/pr/77",
                    "state": "OPEN",
                    "isDraft": False,
                    "reviewDecision": "APPROVED",
                    "labels": [{"name": "needs-senior-review"}],
                    "mergeable": "MERGEABLE",
                    "headRefName": "issue-1206-example",
                    "baseRefName": "main",
                    "headRefOid": "headsha",
                    "baseRefOid": "basesha",
                    "statusCheckRollup": [{"__typename": "StatusContext", "state": "SUCCESS"}],
                },
            ),
            patch.object(
                helper,
                "branch_status",
                return_value={
                    "head_ref": "issue-1206-example",
                    "base_ref": "main",
                    "base_sha": "basesha",
                    "head_sha": "headsha",
                    "behind_base": 0,
                    "ahead_of_base": 2,
                    "diverged": False,
                    "needs_refresh": False,
                },
            ),
        ):
            result = helper.inspect_pr_state(Path("/tmp/repo"), 1206)

        assert result["check_summary"]["overall"] == "passing"
        assert result["check_summary"]["counts"]["passing"] == 1
        assert result["check_summary"]["counts"]["pending"] == 0
        assert result["lifecycle"] == "review_only"
        assert result["ready_for_senior_review"] is True

    def test_open_pr_keeps_existing_draft_unchanged(self) -> None:
        args = SimpleNamespace(issue=1206)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"branch": "issue-1206-example", "issue_title": "Example"},
            ),
            patch.object(helper, "current_pr_number", return_value=88),
            patch.object(helper, "update_state") as mock_update_state,
            patch.object(helper, "run") as mock_run,
            patch("builtins.print") as mock_print,
        ):
            assert helper.cmd_open_pr(args) == 0

        mock_update_state.assert_called_once_with(Path("/tmp/repo"), 1206, pr_number=88)
        mock_run.assert_not_called()
        mock_print.assert_called_once_with(88)

    def test_assert_pr_fresh_fails_when_refresh_needed(self) -> None:
        args = SimpleNamespace(issue=1206)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "inspect_pr_state",
                return_value={
                    "exists": True,
                    "pr_number": 88,
                    "branch_status": {"needs_refresh": True, "behind_base": 3, "ahead_of_base": 1, "diverged": True},
                },
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            helper.cmd_assert_pr_fresh(args)

        assert exc_info.value.code == 1

    def test_assert_pr_mergeable_fails_when_conflicting(self) -> None:
        args = SimpleNamespace(issue=1206)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "inspect_pr_state",
                return_value={"exists": True, "pr_number": 88, "mergeable": "conflicting"},
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            helper.cmd_assert_pr_mergeable(args)

        assert exc_info.value.code == 1


class TestCmdChecks:
    def test_saves_output_to_state_on_success(self) -> None:
        args = SimpleNamespace(issue=1229, mode="initial")
        mock_proc = SimpleNamespace(returncode=0, stdout="all passed\n", stderr="")
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "cleanup_worktree_junk", return_value=[]),
            patch.object(helper, "checks_command", return_value="true"),
            patch("subprocess.run", return_value=mock_proc),
            patch.object(helper, "update_state") as mock_state,
        ):
            result = helper.cmd_checks(args)

        assert result == 0
        mock_state.assert_called_once()
        assert "all passed" in mock_state.call_args.kwargs["last_checks_output"]

    def test_saves_output_to_state_on_failure(self) -> None:
        args = SimpleNamespace(issue=1229, mode="initial")
        mock_proc = SimpleNamespace(
            returncode=1,
            stdout="FAILED test_foo.py::test_bar\n",
            stderr="AssertionError\n",
        )
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "cleanup_worktree_junk", return_value=[]),
            patch.object(helper, "checks_command", return_value="false"),
            patch("subprocess.run", return_value=mock_proc),
            patch.object(helper, "update_state") as mock_state,
            pytest.raises(SystemExit) as exc_info,
        ):
            helper.cmd_checks(args)

        assert exc_info.value.code == 1
        mock_state.assert_called_once()
        saved_output = mock_state.call_args.kwargs["last_checks_output"]
        assert "FAILED test_foo.py" in saved_output
        assert "AssertionError" in saved_output

    def test_allow_baseline_succeeds_when_only_baseline_failures_remain(self) -> None:
        args = SimpleNamespace(issue=1229, mode="initial", allow_baseline=True)
        stage_result = {
            "returncode": 1,
            "output": "baseline_only",
            "results": [{"name": "pytest", "returncode": 1, "fingerprints": ["pytest:test_a"], "parse_failed": False}],
            "command": "ruff check src/ tests/ && python -m pytest tests/unit/ -x -q --tb=short",
            "env_signature": "sig-1",
            "runtime": {},
        }
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "checks_baseline": {
                        "base_sha": "abc",
                        "checks_command": stage_result["command"],
                        "checks_env_signature": "sig-1",
                        "results": [{"name": "pytest", "fingerprints": ["pytest:test_a"], "parse_failed": False}],
                    },
                },
            ),
            patch.object(helper, "run_check_stages", return_value=stage_result),
            patch.object(helper, "compare_against_baseline", return_value=(True, "baseline_only")),
            patch.object(helper, "update_state") as mock_state,
        ):
            assert helper.cmd_checks(args) == 0

        assert "baseline_only" in mock_state.call_args.kwargs["last_checks_output"]

    def test_allow_baseline_fails_without_capture(self) -> None:
        args = SimpleNamespace(issue=1229, mode="initial", allow_baseline=True)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(
                helper,
                "run_check_stages",
                return_value={
                    "returncode": 1,
                    "output": "failed",
                    "results": [],
                    "command": "true",
                    "env_signature": "sig-1",
                    "runtime": {},
                },
            ),
            patch.object(helper, "update_state"),
            pytest.raises(SystemExit) as exc_info,
        ):
            helper.cmd_checks(args)

        assert exc_info.value.code == 1


class TestBaselineChecksHelpers:
    def test_checks_env_signature_ignores_worktree_specific_pythonpath_noise(self) -> None:
        baseline_runtime = {
            "source": "shared_issue_venv",
            "python": "/opt/homebrew/Cellar/python@3.12/3.12.13/bin/python3.12",
            "venv": "/repo-1179/.venv",
            "path_prefix": "/repo-1179/.venv/bin",
            "pythonpath": "/tmp/anteroom-baseline-123/repo/src",
        }
        branch_runtime = {
            "source": "worktree_venv",
            "python": "/opt/homebrew/Cellar/python@3.12/3.12.13/bin/python3.12",
            "venv": "/repo-1179/.venv",
            "path_prefix": "/repo-1179/.venv/bin",
            "pythonpath": "",
        }

        baseline = helper.checks_env_signature(
            baseline_runtime, "ruff check src/ tests/ && python -m pytest tests/unit/ -x -q --tb=short"
        )
        branch = helper.checks_env_signature(
            branch_runtime, "ruff check src/ tests/ && python -m pytest tests/unit/ -x -q --tb=short"
        )

        assert baseline == branch

    def test_checks_env_signature_changes_for_different_effective_runtime(self) -> None:
        runtime_a = {
            "python": "/opt/homebrew/Cellar/python@3.12/3.12.13/bin/python3.12",
            "venv": "/repo-1179/.venv",
            "path_prefix": "/repo-1179/.venv/bin",
        }
        runtime_b = {
            "python": "/opt/homebrew/Cellar/python@3.13/3.13.0/bin/python3.13",
            "venv": "/repo-1179/.venv",
            "path_prefix": "/repo-1179/.venv/bin",
        }

        signature_a = helper.checks_env_signature(runtime_a, "pytest")
        signature_b = helper.checks_env_signature(runtime_b, "pytest")

        assert signature_a != signature_b

    def test_split_check_stages_removes_pytest_exitfirst_in_baseline_mode(self) -> None:
        stages = helper.split_check_stages(
            "ruff check src/ tests/ && python -m pytest tests/unit/ -x -q --tb=short",
            allow_baseline=True,
        )

        assert stages[0]["name"] == "ruff"
        assert stages[1]["name"] == "pytest"
        assert "-x" not in stages[1]["command"]

    def test_compare_against_baseline_rejects_new_fingerprints(self) -> None:
        current = {
            "command": "pytest",
            "env_signature": "sig",
            "results": [
                {
                    "name": "pytest",
                    "returncode": 1,
                    "fingerprints": ["pytest:test_old", "pytest:test_new"],
                    "parse_failed": False,
                }
            ],
        }
        baseline = {
            "base_sha": "base",
            "checks_command": "pytest",
            "checks_env_signature": "sig",
            "results": [{"name": "pytest", "fingerprints": ["pytest:test_old"], "parse_failed": False}],
        }

        with patch.object(helper, "latest_main_sha", return_value="base"):
            success, summary = helper.compare_against_baseline(current, baseline)

        assert success is False
        assert "pytest:test_new" in summary

    def test_compare_against_baseline_accepts_matching_empty_fingerprint_sets(self) -> None:
        current = {
            "command": "pytest",
            "env_signature": "sig",
            "results": [{"name": "pytest", "returncode": 1, "fingerprints": [], "parse_failed": False}],
        }
        baseline = {
            "base_sha": "base",
            "checks_command": "pytest",
            "checks_env_signature": "sig",
            "results": [{"name": "pytest", "fingerprints": [], "parse_failed": False}],
        }

        with patch.object(helper, "latest_main_sha", return_value="base"):
            success, summary = helper.compare_against_baseline(current, baseline)

        assert success is True
        assert summary == "baseline_only"

    def test_compare_against_baseline_rejects_empty_output_failure(self) -> None:
        """A failing stage with empty output and no fingerprints must fail closed."""
        current = {
            "command": "pytest",
            "env_signature": "sig",
            "results": [
                {
                    "name": "pytest",
                    "returncode": 1,
                    "fingerprints": [],
                    "parse_failed": True,
                }
            ],
        }
        baseline = {
            "base_sha": "base",
            "checks_command": "pytest",
            "checks_env_signature": "sig",
            "results": [{"name": "pytest", "fingerprints": [], "parse_failed": False}],
        }

        with patch.object(helper, "latest_main_sha", return_value="base"):
            success, summary = helper.compare_against_baseline(current, baseline)

        assert success is False
        assert "unable to fingerprint" in summary


class TestRunCheckStagesParseFailedFlag:
    """Verify run_check_stages sets parse_failed in the real runner path."""

    def test_fingerprintable_stage_with_no_fingerprints_sets_parse_failed(self) -> None:
        """A pytest stage that fails with empty output must have parse_failed=True."""
        fake_proc = SimpleNamespace(returncode=1, stdout="", stderr="")
        state: dict = {"checks_command": "pytest tests/", "checks_env": {}}

        with (
            patch("subprocess.run", return_value=fake_proc),
            patch.object(helper, "latest_main_sha", return_value="abc123"),
            patch.object(helper, "checks_command", return_value="pytest tests/"),
            patch.object(
                helper,
                "split_check_stages",
                return_value=[{"name": "pytest", "command": "pytest tests/"}],
            ),
            patch.object(helper, "cleanup_worktree_junk", return_value=[]),
            patch.object(helper, "runtime_env_for_worktree", return_value=({}, {})),
        ):
            result = helper.run_check_stages(
                Path("/tmp/worktree"),
                state=state,
                allow_baseline=True,
            )

        assert len(result["results"]) == 1
        assert result["results"][0]["parse_failed"] is True

    def test_fingerprintable_stage_with_fingerprints_clears_parse_failed(self) -> None:
        """A pytest stage that fails with fingerprintable output has parse_failed=False."""
        fake_proc = SimpleNamespace(
            returncode=1,
            stdout="FAILED tests/unit/test_foo.py::test_bar - AssertionError\n",
            stderr="",
        )
        state: dict = {"checks_command": "pytest tests/", "checks_env": {}}

        with (
            patch("subprocess.run", return_value=fake_proc),
            patch.object(helper, "latest_main_sha", return_value="abc123"),
            patch.object(helper, "checks_command", return_value="pytest tests/"),
            patch.object(
                helper,
                "split_check_stages",
                return_value=[{"name": "pytest", "command": "pytest tests/"}],
            ),
            patch.object(helper, "cleanup_worktree_junk", return_value=[]),
            patch.object(helper, "runtime_env_for_worktree", return_value=({}, {})),
        ):
            result = helper.run_check_stages(
                Path("/tmp/worktree"),
                state=state,
                allow_baseline=True,
            )

        assert len(result["results"]) == 1
        assert result["results"][0]["parse_failed"] is False
        assert len(result["results"][0]["fingerprints"]) > 0


class TestCmdFixChecks:
    def test_calls_claude_once_with_fix_checks_prompt(self) -> None:
        args = SimpleNamespace(issue=1229, mode="initial")
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "claude_once", return_value="fixed lint errors") as mock_claude,
            patch.object(helper, "update_state") as mock_state,
        ):
            result = helper.cmd_fix_checks(args)

        assert result == 0
        mock_claude.assert_called_once()
        prompt = mock_claude.call_args[0][0]
        assert "initial checks" in prompt.lower() or "initial" in prompt.lower()
        assert "1229" in prompt
        assert mock_claude.call_args[1]["cwd"] == Path("/tmp/worktree")
        mock_state.assert_called_once()
        assert mock_state.call_args.kwargs["last_fix_checks_summary"] == "fixed lint errors"

    def test_post_review_mode_uses_correct_prompt(self) -> None:
        args = SimpleNamespace(issue=1229, mode="post-review")
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "claude_once", return_value="fixed test") as mock_claude,
            patch.object(helper, "update_state"),
        ):
            result = helper.cmd_fix_checks(args)

        assert result == 0
        prompt = mock_claude.call_args[0][0]
        assert "post-review" in prompt.lower() or "review feedback" in prompt.lower()

    def test_refresh_mode_uses_correct_prompt(self) -> None:
        args = SimpleNamespace(issue=1229, mode="refresh")
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "claude_once", return_value="fixed") as mock_claude,
            patch.object(helper, "update_state"),
        ):
            result = helper.cmd_fix_checks(args)

        assert result == 0
        prompt = mock_claude.call_args[0][0]
        assert "refresh" in prompt.lower()

    def test_includes_failure_context_from_state(self) -> None:
        args = SimpleNamespace(issue=1229, mode="initial")
        failure_output = "FAILED tests/unit/test_foo.py::test_bar - AssertionError: 1 != 2"
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "last_checks_output": failure_output,
                },
            ),
            patch.object(helper, "claude_once", return_value="fixed assertion") as mock_claude,
            patch.object(helper, "update_state"),
        ):
            result = helper.cmd_fix_checks(args)

        assert result == 0
        prompt = mock_claude.call_args[0][0]
        assert "<failed_checks_output>" in prompt
        assert "test_bar" in prompt
        assert "AssertionError" in prompt

    def test_omits_context_block_when_no_failure_output(self) -> None:
        args = SimpleNamespace(issue=1229, mode="initial")
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "claude_once", return_value="fixed") as mock_claude,
            patch.object(helper, "update_state"),
        ):
            helper.cmd_fix_checks(args)

        prompt = mock_claude.call_args[0][0]
        assert "<failed_checks_output>" not in prompt


class TestCmdFixPr:
    def test_includes_review_context_from_state(self) -> None:
        args = SimpleNamespace(issue=1229)
        review_comment = "Blocker: `cmd_fix_checks()` has no failure context injected."
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "last_pr_review_decision": "changes_requested",
                    "last_pr_review_comment": review_comment,
                    "branch": "issue-1229-test",
                },
            ),
            patch.object(helper, "ensure_pr_number", return_value=99),
            patch.object(helper, "claude_once", return_value="fixed blocker") as mock_claude,
            patch.object(helper, "update_state") as mock_state,
        ):
            result = helper.cmd_fix_pr(args)

        assert result == 0
        prompt = mock_claude.call_args[0][0]
        assert "<senior_review_feedback>" in prompt
        assert "cmd_fix_checks" in prompt
        mock_state.assert_called_once()
        assert mock_state.call_args.kwargs["last_pr_fix_summary"] == "fixed blocker"

    def test_omits_review_block_when_no_comment(self) -> None:
        args = SimpleNamespace(issue=1229)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "last_pr_review_decision": "changes_requested",
                    "branch": "issue-1229-test",
                },
            ),
            patch.object(helper, "ensure_pr_number", return_value=99),
            patch.object(helper, "claude_once", return_value="no changes") as mock_claude,
            patch.object(helper, "update_state"),
        ):
            helper.cmd_fix_pr(args)

        prompt = mock_claude.call_args[0][0]
        assert "<senior_review_feedback>" not in prompt

    def test_skips_when_no_changes_requested(self) -> None:
        args = SimpleNamespace(issue=1229)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "last_pr_review_decision": "approve",
                    "branch": "issue-1229-test",
                },
            ),
        ):
            result = helper.cmd_fix_pr(args)

        assert result == 0


class TestCmdRefreshPr:
    def test_calls_claude_once_with_refresh_prompt(self) -> None:
        args = SimpleNamespace(issue=1229)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={"worktree_path": "/tmp/worktree"},
            ),
            patch.object(helper, "claude_once", return_value="rebased and resolved conflicts") as mock_claude,
            patch.object(helper, "update_state") as mock_state,
        ):
            result = helper.cmd_refresh_pr(args)

        assert result == 0
        mock_claude.assert_called_once()
        prompt = mock_claude.call_args[0][0]
        assert "refresh" in prompt.lower()
        assert "1229" in prompt
        assert mock_claude.call_args[1]["cwd"] == Path("/tmp/worktree")
        mock_state.assert_called_once()
        assert mock_state.call_args.kwargs["last_refresh_pr_summary"] == "rebased and resolved conflicts"


class TestBuildClaudeFixChecksPrompt:
    def test_includes_failure_context_in_xml_block(self) -> None:
        prompt = helper.build_claude_fix_checks_prompt(
            42, mode="initial", failure_context="FAILED test_x.py::test_y - assert 1 == 2"
        )
        assert "<failed_checks_output>" in prompt
        assert "test_x.py::test_y" in prompt
        assert "</failed_checks_output>" in prompt

    def test_omits_block_when_context_empty(self) -> None:
        prompt = helper.build_claude_fix_checks_prompt(42, mode="initial", failure_context="")
        assert "<failed_checks_output>" not in prompt

    def test_omits_block_when_context_whitespace(self) -> None:
        prompt = helper.build_claude_fix_checks_prompt(42, mode="initial", failure_context="   \n  ")
        assert "<failed_checks_output>" not in prompt

    def test_trims_long_context_to_last_8000_chars(self) -> None:
        long_output = "x" * 10000
        prompt = helper.build_claude_fix_checks_prompt(42, mode="initial", failure_context=long_output)
        assert "<failed_checks_output>" in prompt
        block_start = prompt.index("<failed_checks_output>") + len("<failed_checks_output>")
        block_end = prompt.index("</failed_checks_output>")
        content = prompt[block_start:block_end].strip()
        assert len(content) == 8000


class TestBuildClaudePrFixPrompt:
    def test_includes_review_context_in_xml_block(self) -> None:
        prompt = helper.build_claude_pr_fix_prompt(99, review_context="Blocker: missing error handling in foo()")
        assert "<senior_review_feedback>" in prompt
        assert "missing error handling" in prompt
        assert "</senior_review_feedback>" in prompt

    def test_omits_block_when_context_empty(self) -> None:
        prompt = helper.build_claude_pr_fix_prompt(99, review_context="")
        assert "<senior_review_feedback>" not in prompt

    def test_omits_block_when_no_context_arg(self) -> None:
        prompt = helper.build_claude_pr_fix_prompt(99)
        assert "<senior_review_feedback>" not in prompt


class TestRequiredToolsNewActions:
    def test_fix_checks_needs_claude(self) -> None:
        assert helper._required_tools_for_action("fix-checks") == ("gh", "git", "claude")

    def test_refresh_pr_needs_claude(self) -> None:
        assert helper._required_tools_for_action("refresh-pr") == ("gh", "git", "claude")


class TestStdinClosedInSubprocesses:
    """Regression tests for #1298: subprocesses must not inherit stdin."""

    def test_spawn_text_subprocess_closes_stdin(self, tmp_path: Path) -> None:
        fake = FakePopen(stdout="ok\n")
        with patch.object(subprocess, "Popen", return_value=fake) as mock_popen:
            helper._spawn_text_subprocess(["echo", "hi"], cwd=tmp_path)

        kwargs = mock_popen.call_args[1]
        assert kwargs["stdin"] == subprocess.DEVNULL

    def test_run_streaming_closes_stdin(self, tmp_path: Path) -> None:
        fake = FakePopen(stdout="line\n")
        with patch.object(subprocess, "Popen", return_value=fake) as mock_popen:
            helper.run_streaming(["echo", "hi"], cwd=tmp_path)

        kwargs = mock_popen.call_args[1]
        assert kwargs["stdin"] == subprocess.DEVNULL

    def test_run_helper_closes_stdin(self, tmp_path: Path) -> None:
        fake = MagicMock(returncode=0, stdout="ok", stderr="")
        with patch.object(subprocess, "run", return_value=fake) as mock_run:
            helper.run(["echo", "hi"], cwd=tmp_path)

        kwargs = mock_run.call_args[1]
        assert kwargs["stdin"] == subprocess.DEVNULL

    def test_review_existing_work_completes_without_stdin(self) -> None:
        """cmd_review_existing_work must not block on stdin reads."""
        args = SimpleNamespace(issue=1298)
        with (
            patch.object(helper, "git_root", return_value=Path("/tmp/repo")),
            patch.object(
                helper,
                "ensure_worktree",
                return_value={
                    "worktree_path": "/tmp/worktree",
                    "existing_work_assessment": {
                        "implementation_present": True,
                        "branch": "issue-1298",
                        "base_ref": "origin/main",
                        "ahead_of_main": 1,
                        "changed_files": ["src/anteroom/services/workflow_runners.py"],
                        "commit_subjects": ["fix: close stdin in subprocesses"],
                    },
                },
            ),
            patch.object(
                helper,
                "issue_data",
                return_value={
                    "body": (
                        "## Description\nFix stdin.\n\n"
                        f"{helper.PLAN_START}\n## Summary\nClose stdin.\n{helper.PLAN_END}"
                    )
                },
            ),
            patch.object(
                helper,
                "codex_once",
                return_value=helper.CodexRunResult(
                    text='{"decision":"approve","summary":"OK","comment_markdown":"Approved"}',
                    exit_code=0,
                ),
            ),
            patch.object(helper, "post_issue_comment"),
            patch.object(helper, "edit_issue_labels"),
            patch.object(helper, "update_state"),
        ):
            assert helper.cmd_review_existing_work(args) == 0
