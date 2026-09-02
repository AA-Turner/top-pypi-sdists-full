"""Tests for implementation_node."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agentic_devtools.models.git_results import SetupResult
from agentic_devtools.orchestration.nodes.implementation import (
    _build_context,
    _generate_implementation,
    _generate_test,
    _get_repo_root,
    _implement_checklist_item,
    _resolve_output_path,
    implementation_node,
)


class TestImplementationNode:
    def test_dry_run_marks_items_complete_without_running_tdd(self):
        items = [{"description": "task 1", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
        ) as mock_implement:
            result = implementation_node({"checklist_items": items, "issue_key": "T-1", "dry_run": True})

        mock_implement.assert_not_called()
        assert result["checklist_complete"] is True
        assert result["checklist_items"][0]["is_complete"] is True
        assert result["dry_run_skipped"] is True
        assert result["implementation_log"][0]["status"] == "dry_run"

    def test_dry_run_with_no_valid_items_returns_error(self):
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
        ) as mock_implement:
            result = implementation_node({"checklist_items": ["corrupted"], "issue_key": "T-1", "dry_run": True})

        mock_implement.assert_not_called()
        assert result["checklist_complete"] is False
        assert result["error"] == "No valid checklist items to implement; cannot mark implementation complete."
        assert result["dry_run_skipped"] is True

    def test_empty_checklist_does_not_complete(self):
        """An empty checklist has no valid items and must NOT be marked complete."""
        result = implementation_node({"checklist_items": []})
        assert result["checklist_complete"] is False
        assert result["error"] is not None
        assert result["step"] == "implementation"

    def test_invalid_checklist_type_does_not_complete(self):
        """A non-list checklist (corrupted checkpoint) resets to [] and must NOT complete."""
        result = implementation_node({"checklist_items": "not a list"})
        assert result["checklist_complete"] is False
        assert result["error"] is not None

    def test_skips_complete_items(self):
        items = [
            {"description": "done", "is_complete": True},
            {"description": "also done", "is_complete": True},
        ]
        result = implementation_node({"checklist_items": items})
        assert result["checklist_complete"] is True
        assert result["error"] is None

    def test_handles_non_dict_items(self):
        """A checklist of only non-dict entries has no valid items and must NOT complete."""
        items = ["not a dict", 42, None]
        result = implementation_node({"checklist_items": items})
        assert result["checklist_complete"] is False
        assert result["error"] is not None

    def test_completes_when_valid_items_present_alongside_non_dict_entries(self):
        """Non-dict entries are ignored; a completed valid item still marks the checklist done."""
        items = [{"description": "done", "is_complete": True}, "corrupted", None]
        result = implementation_node({"checklist_items": items})
        assert result["checklist_complete"] is True
        assert result["error"] is None

    def test_records_error_on_item_failure(self):
        items = [{"description": "do something", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
            side_effect=RuntimeError("crash"),
        ):
            result = implementation_node({"checklist_items": items, "issue_key": "T-1"})
            assert result["error"] is not None
            assert "crash" in result["error"]
            assert result["checklist_complete"] is False

    def test_records_error_from_result(self):
        items = [{"description": "do something", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
            return_value={"error": "test failed"},
        ):
            result = implementation_node({"checklist_items": items, "issue_key": "T-1"})
            assert result["error"] is not None
            assert "test failed" in result["error"]

    def test_marks_item_complete_on_success(self):
        items = [{"description": "task 1", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
            return_value={"affected_paths": ["src/new.py"]},
        ):
            result = implementation_node({"checklist_items": items, "issue_key": "T-1"})
            assert result["checklist_items"][0]["is_complete"] is True
            assert "src/new.py" in result["affected_paths"]

    def test_emits_completed_event_when_all_done(self):
        items = [{"description": "task 1", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
            return_value={"affected_paths": []},
        ):
            result = implementation_node({"checklist_items": items, "issue_key": "T-1"})
            assert result["events"][0]["event"] == "implementation_completed"

    def test_emits_partial_event_on_failure(self):
        items = [{"description": "task 1", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
            return_value={"error": "oops"},
        ):
            result = implementation_node({"checklist_items": items, "issue_key": "T-1"})
            assert result["events"][0]["event"] == "implementation_partial"

    def test_preserves_existing_implementation_log(self):
        existing_log = [{"item_index": 0, "status": "completed", "timestamp": "t1"}]
        items = [
            {"description": "done", "is_complete": True},
            {"description": "todo", "is_complete": False},
        ]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
            return_value={"affected_paths": ["x.py"]},
        ):
            result = implementation_node(
                {
                    "checklist_items": items,
                    "implementation_log": existing_log,
                    "issue_key": "T-1",
                }
            )
            assert len(result["implementation_log"]) == 2
            assert result["implementation_log"][0]["status"] == "completed"

    def test_corrupted_implementation_log_in_state_treated_as_empty(self):
        """Non-list implementation_log (e.g. dict from corrupted checkpoint) resets to []."""
        items = [{"description": "done", "is_complete": True}]
        result = implementation_node(
            {
                "checklist_items": items,
                "implementation_log": {"bad": "value"},
            }
        )
        # Should not raise; log starts fresh
        assert isinstance(result["implementation_log"], list)

    def test_corrupted_affected_paths_string_not_iterated_as_chars(self):
        """String affected_paths from corrupted checkpoint must not iterate character-by-character."""
        items = [{"description": "task", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
            return_value={"affected_paths": ["src/x.py"]},
        ):
            result = implementation_node(
                {
                    "checklist_items": items,
                    "affected_paths": "not-a-list",
                    "issue_key": "T-1",
                }
            )
        # Corrupted input is discarded; only paths from this run are present
        assert result["affected_paths"] == ["src/x.py"]

    def test_accumulates_token_usage_across_items(self):
        """Token usage from all checklist items must be summed and added to state totals."""
        items = [
            {"description": "task 1", "is_complete": False},
            {"description": "task 2", "is_complete": False},
        ]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
            return_value={"affected_paths": [], "token_usage_prompt": 100, "token_usage_completion": 50},
        ):
            result = implementation_node(
                {
                    "checklist_items": items,
                    "issue_key": "T-1",
                    "token_usage_prompt": 10,
                    "token_usage_completion": 5,
                }
            )
        # Two items × 100 prompt + 50 completion, plus state totals of 10/5
        assert result["token_usage_prompt"] == 210
        assert result["token_usage_completion"] == 105

    def test_token_usage_includes_failed_item_tokens(self):
        """Token usage from a failing item must still be included in the returned total."""
        items = [{"description": "task", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._implement_checklist_item",
            return_value={"error": "RED phase failed", "token_usage_prompt": 80, "token_usage_completion": 30},
        ):
            result = implementation_node({"checklist_items": items, "issue_key": "T-1"})
        assert result["token_usage_prompt"] == 80
        assert result["token_usage_completion"] == 30


def _mock_result(returncode=0, stdout="", stderr=""):
    return type("Result", (), {"returncode": returncode, "stdout": stdout, "stderr": stderr})()


class TestGetRepoRoot:
    def test_prefers_setup_result_worktree_path(self, tmp_path):
        state = {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
        with patch(
            "agentic_devtools.orchestration.nodes.implementation.resolve_repo_root",
            return_value=tmp_path.resolve(),
        ) as mock_resolve_repo_root:
            result = _get_repo_root(state)
        assert result == tmp_path.resolve()
        mock_resolve_repo_root.assert_called_once_with(state)

    def test_returns_path_on_success(self):
        with patch(
            "agentic_devtools.orchestration.nodes.implementation.resolve_repo_root",
            return_value=Path("/home/user/repo"),
        ):
            result = _get_repo_root()
            assert result == Path("/home/user/repo")

    def test_returns_none_on_failure(self):
        with patch(
            "agentic_devtools.orchestration.nodes.implementation.resolve_repo_root",
            return_value=None,
        ):
            result = _get_repo_root()
            assert result is None


class TestBuildContext:
    def test_returns_structure_and_conventions(self, tmp_path):
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("pass")
        result = _build_context(tmp_path)
        assert "structure" in result
        assert "conventions" in result
        assert isinstance(result["structure"], list)
        assert len(result["structure"]) <= 100


class TestImplementChecklistItem:
    def test_returns_error_when_no_repo_root(self):
        with patch(
            "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
            return_value=None,
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert result["error"] == "Cannot determine repository root"

    def test_returns_error_on_red_phase_failure(self, tmp_path):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"error": "LLM unavailable"},
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert "RED phase failed" in result["error"]

    def test_returns_error_on_green_phase_failure(self, tmp_path):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"path": "tests/test_new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_implementation",
                return_value={"error": "cannot generate"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation.run_command",
                # Only one run_command call here (RED verify); GREEN fails before VERIFY runs
                return_value=_mock_result(1, stdout="FAILED"),  # RED verify: test fails as expected (TDD RED)
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert "GREEN phase failed" in result["error"]

    def test_returns_error_on_verify_failure(self, tmp_path):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"path": "tests/test_new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_implementation",
                return_value={"path": "src/new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation.run_command",
                # RED verify returns 1 (test fails, as expected); VERIFY also returns 1 (tests still fail)
                side_effect=[
                    _mock_result(1, stdout="FAILED"),
                    _mock_result(1, stdout="FAILED", stderr="assertion error"),
                ],
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert "VERIFY phase failed" in result["error"]

    def test_returns_error_when_red_phase_test_already_passes(self, tmp_path):
        """RED verify: test passing before implementation means item may already be implemented."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"path": "tests/test_new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation.run_command",
                return_value=_mock_result(0),  # test already passes — RED check fails
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert "RED phase failed" in result["error"]
            assert "already passes" in result["error"]

    def test_returns_error_when_red_phase_test_has_syntax_error(self, tmp_path):
        """Pytest exit code 2 (syntax/collection error) must be rejected in the RED phase."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"path": "tests/test_new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation.run_command",
                return_value=_mock_result(2, stderr="SyntaxError"),  # pytest collection/syntax error
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert "RED phase failed" in result["error"]
            assert "invalid" in result["error"]
            assert "2" in result["error"]

    def test_returns_error_when_red_phase_no_tests_collected(self, tmp_path):
        """Pytest exit code 5 (no tests collected) must be rejected in the RED phase."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"path": "tests/test_new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation.run_command",
                return_value=_mock_result(5, stderr="no tests ran"),  # no tests collected
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert "RED phase failed" in result["error"]
            assert "invalid" in result["error"]
            assert "5" in result["error"]

    def test_accumulates_token_usage_from_generate_calls(self, tmp_path):
        """Token usage from _generate_test and _generate_implementation must be returned."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={
                    "path": "tests/test_new.py",
                    "token_usage": {"prompt_tokens": 100, "completion_tokens": 50},
                },
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_implementation",
                return_value={"path": "src/new.py", "token_usage": {"prompt_tokens": 200, "completion_tokens": 80}},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation.run_command",
                side_effect=[_mock_result(1, stdout="FAILED"), _mock_result(0)],
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert result["token_usage_prompt"] == 300
            assert result["token_usage_completion"] == 130

    def test_success_returns_affected_paths(self, tmp_path):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"path": "tests/test_new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_implementation",
                return_value={"path": "src/new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation.run_command",
                # RED verify returns 1 (test fails, as expected); VERIFY returns 0 (tests pass)
                side_effect=[_mock_result(1, stdout="FAILED"), _mock_result(0)],
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert result["affected_paths"] == ["tests/test_new.py", "src/new.py"]

    def test_runs_red_and_green_verification_in_worktree_cwd(self, tmp_path):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"path": "tests/test_new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_implementation",
                return_value={"path": "src/new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation.run_command",
                side_effect=[_mock_result(1, stdout="FAILED"), _mock_result(0)],
            ) as mock_run_command,
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})

        assert result["affected_paths"] == ["tests/test_new.py", "src/new.py"]
        assert mock_run_command.call_args_list[0].kwargs["cwd"] == str(tmp_path)
        assert mock_run_command.call_args_list[1].kwargs["cwd"] == str(tmp_path)

    def test_success_with_empty_test_path(self, tmp_path):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"path": ""},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_implementation",
                return_value={"path": "src/new.py"},
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert result["affected_paths"] == ["src/new.py"]

    def test_success_with_empty_impl_path(self, tmp_path):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation._get_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_test",
                return_value={"path": "tests/test_new.py"},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation._generate_implementation",
                return_value={"path": ""},
            ),
            patch(
                "agentic_devtools.orchestration.nodes.implementation.run_command",
                # RED verify returns 1 (test fails, as expected); VERIFY returns 0 (tests pass)
                side_effect=[_mock_result(1, stdout="FAILED"), _mock_result(0)],
            ),
        ):
            result = _implement_checklist_item({"description": "do stuff"}, 0, {"issue_key": "T-1", "plan": "plan"})
            assert result["affected_paths"] == ["tests/test_new.py"]


class TestGenerateTest:
    def test_success_writes_file_and_returns_path(self, tmp_path):
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "tests/test_new.py", "content": "def test_x(): pass"})
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_test("do stuff", "plan", {}, "T-1", tmp_path)
            assert result["path"] == "tests/test_new.py"
            assert (tmp_path / "tests" / "test_new.py").read_text() == "def test_x(): pass"

    def test_returns_token_usage_on_success(self, tmp_path):
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "tests/test_new.py", "content": "def test_x(): pass"})
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_test("do stuff", "plan", {}, "T-1", tmp_path)
            assert result["token_usage"] == {"prompt_tokens": 10, "completion_tokens": 5}

    def test_returns_token_usage_on_invalid_output(self, tmp_path):
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "", "content": ""})
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_test("do stuff", "plan", {}, "T-1", tmp_path)
            assert result["error"] == "LLM did not produce valid test file output"
            assert result["token_usage"] == {"prompt_tokens": 10, "completion_tokens": 5}

    def test_returns_error_on_invalid_output(self, tmp_path):
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "", "content": ""})
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_test("do stuff", "plan", {}, "T-1", tmp_path)
            assert result["error"] == "LLM did not produce valid test file output"

    def test_returns_error_with_token_usage_when_json_response_is_not_object(self, tmp_path):
        mock_response = MagicMock()
        mock_response.text = json.dumps(["not", "an", "object"])
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_test("do stuff", "plan", {}, "T-1", tmp_path)
            assert result["error"] == "LLM did not produce valid test file output"
            assert result["token_usage"] == {"prompt_tokens": 10, "completion_tokens": 5}

    def test_returns_error_on_exception(self, tmp_path):
        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(side_effect=RuntimeError("connection timeout"))

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_test("do stuff", "plan", {}, "T-1", tmp_path)
            assert "connection timeout" in result["error"]
            assert result["token_usage"] == {}

    def test_returns_token_usage_on_post_response_exception(self, tmp_path):
        """When exception occurs after LLM response (e.g. JSON parse error), token_usage is preserved."""
        mock_response = MagicMock()
        mock_response.text = "not-valid-json{"
        mock_response.usage = MagicMock(input_tokens=7, output_tokens=3)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_test("do stuff", "plan", {}, "T-1", tmp_path)
            assert "error" in result
            assert result["token_usage"] == {"prompt_tokens": 7, "completion_tokens": 3}

    def test_returns_empty_token_usage_when_no_usage_info(self, tmp_path):
        """When response.usage is None, token_usage dict must be empty."""
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "tests/test_new.py", "content": "def test_x(): pass"})
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_test("do stuff", "plan", {}, "T-1", tmp_path)
            assert result["token_usage"] == {}

    def test_rejects_path_traversal_output_path(self, tmp_path):
        blocked_path = (tmp_path / "../../outside.py").resolve()
        assert not blocked_path.is_relative_to(tmp_path.resolve())
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "../../outside.py", "content": "def test_x(): pass"})
        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_test("do stuff", "plan", {}, "T-1", tmp_path)
            assert "Path traversal is not allowed" in result["error"]
            assert not blocked_path.exists()


class TestGenerateImplementation:
    def test_success_writes_file_and_returns_path(self, tmp_path):
        # Create a test file for context
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_new.py").write_text("def test_x(): assert True")

        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "src/new.py", "content": "def x(): return True"})
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "tests/test_new.py", "T-1", tmp_path)
            assert result["path"] == "src/new.py"
            assert (tmp_path / "src" / "new.py").read_text() == "def x(): return True"

    def test_returns_token_usage_on_success(self, tmp_path):
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "src/new.py", "content": "def x(): return True"})
        mock_response.usage = MagicMock(input_tokens=20, output_tokens=8)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "", "T-1", tmp_path)
            assert result["token_usage"] == {"prompt_tokens": 20, "completion_tokens": 8}

    def test_returns_error_on_invalid_output(self, tmp_path):
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "", "content": ""})
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "", "T-1", tmp_path)
            assert result["error"] == "LLM did not produce valid implementation output"

    def test_returns_error_with_token_usage_when_json_response_is_not_object(self, tmp_path):
        mock_response = MagicMock()
        mock_response.text = json.dumps(["not", "an", "object"])
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "", "T-1", tmp_path)
            assert result["error"] == "LLM did not produce valid implementation output"
            assert result["token_usage"] == {"prompt_tokens": 10, "completion_tokens": 5}

    def test_returns_error_on_exception(self, tmp_path):
        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(side_effect=RuntimeError("bad"))

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "", "T-1", tmp_path)
            assert "bad" in result["error"]
            assert result["token_usage"] == {}

    def test_returns_token_usage_on_post_response_exception(self, tmp_path):
        """When exception occurs after LLM response (e.g. JSON parse error), token_usage is preserved."""
        mock_response = MagicMock()
        mock_response.text = "not-valid-json{"
        mock_response.usage = MagicMock(input_tokens=15, output_tokens=6)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "", "T-1", tmp_path)
            assert "error" in result
            assert result["token_usage"] == {"prompt_tokens": 15, "completion_tokens": 6}

    def test_reads_test_file_for_context(self, tmp_path):
        """Verify the test file content is read when test_path points to an existing file."""
        (tmp_path / "tests").mkdir()
        test_file = tmp_path / "tests" / "test_x.py"
        test_file.write_text("def test_x(): assert True")

        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "src/x.py", "content": "pass"})
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "tests/test_x.py", "T-1", tmp_path)
            assert result["path"] == "src/x.py"

    def test_handles_missing_test_file(self, tmp_path):
        """When test_path doesn't exist, test_content should be empty."""
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "src/x.py", "content": "pass"})
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "tests/nonexistent.py", "T-1", tmp_path)
            assert result["path"] == "src/x.py"

    def test_rejects_absolute_output_path(self, tmp_path):
        absolute_bad_path = (tmp_path.parent / "evil.py").resolve()
        assert absolute_bad_path.is_absolute()
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": str(absolute_bad_path), "content": "pass"})
        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "", "T-1", tmp_path)
            assert "Absolute paths are not allowed" in result["error"]
            assert not absolute_bad_path.exists()

    def test_returns_empty_token_usage_when_no_usage_info(self, tmp_path):
        """When response.usage is None, token_usage dict must be empty."""
        mock_response = MagicMock()
        mock_response.text = json.dumps({"file_path": "src/new.py", "content": "def x(): return True"})
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_implementation("do stuff", "plan", {}, "", "T-1", tmp_path)
            assert result["token_usage"] == {}


class TestResolveOutputPath:
    def test_allows_repo_relative_path(self, tmp_path):
        resolved = _resolve_output_path(tmp_path, "src/module.py")
        assert resolved == (tmp_path / "src/module.py").resolve()

    def test_rejects_absolute_path(self, tmp_path):
        with pytest.raises(ValueError, match="Absolute paths are not allowed"):
            _resolve_output_path(tmp_path, "/tmp/evil.py")

    def test_rejects_path_traversal(self, tmp_path):
        with pytest.raises(ValueError, match="Path traversal is not allowed"):
            _resolve_output_path(tmp_path, "../outside.py")
