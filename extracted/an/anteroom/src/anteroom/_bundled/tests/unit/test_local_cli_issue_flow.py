"""Tests for scripts/workflows/local_cli_issue_flow.py invocation helpers."""

from __future__ import annotations

import io
import json
import subprocess
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

    def wait(self) -> int:
        return self.returncode


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
        assert result == '{"decision": "approve"}'

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
        assert result == '{"decision": "approve"}'


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


class TestConsumeTextChunks:
    def test_prefers_newline_boundaries(self) -> None:
        emitted, pending = helper._consume_text_chunks("", "first line\nsecond line")
        assert emitted == ["first line"]
        assert pending == "second line"

    def test_soft_wraps_long_partial_output(self) -> None:
        emitted, pending = helper._consume_text_chunks("", "x" * 75, soft_limit=60)
        assert emitted == ["x" * 60]
        assert pending == "x" * 15


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
