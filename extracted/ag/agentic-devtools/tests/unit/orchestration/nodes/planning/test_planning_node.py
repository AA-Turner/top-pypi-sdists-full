"""Tests for planning_node."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

from agentic_devtools.orchestration.nodes.planning import (
    planning_node,
)


def _mock_result(returncode=0, stdout="", stderr=""):
    return type("Result", (), {"returncode": returncode, "stdout": stdout, "stderr": stderr})()


class TestPlanningNode:
    def test_blocked_when_issue_data_insufficient(self):
        result = planning_node(
            {
                "issue_key": "T-1",
                "issue_data": {"summary": "", "description": ""},
            }
        )
        assert result["status"] == "blocked"
        assert result["blocked_reason"] is not None

    def test_generates_plan_on_valid_issue(self):
        mock_response = MagicMock()
        mock_response.text = "## Plan\n\n1. Do thing A\n2. Do thing B"
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "TEST-1",
                    "issue_data": {
                        "summary": "Implement authentication",
                        "description": (
                            "Add JWT-based authentication to the REST API with proper error handling and tests"
                        ),
                    },
                }
            )
            assert result["plan"] is not None
            assert "Plan" in result["plan"]
            assert result["plan_posted"] is True
            assert result["token_usage_prompt"] == 100
            # Success path must clear stale terminal signals from resumed checkpoints
            assert result["status"] == "active"
            assert result["error"] is None
            assert result["blocked_reason"] is None

    def test_success_clears_stale_blocked_state_from_checkpoint(self):
        """A resumed checkpoint carrying error/status=blocked must be cleared on success."""
        mock_response = MagicMock()
        mock_response.text = "## Plan\n\n1. Step"
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "TEST-1",
                    "status": "blocked",
                    "error": "previous blocked reason",
                    "blocked_reason": "previous blocked reason",
                    "issue_data": {
                        "summary": "Implement authentication",
                        "description": (
                            "Add JWT-based authentication to the REST API with proper error handling and tests"
                        ),
                    },
                }
            )
            assert result["status"] == "active"
            assert result["error"] is None
            assert result["blocked_reason"] is None
            assert result["plan_posted"] is True

    def test_handles_llm_exception(self):
        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.side_effect = RuntimeError("no config")
            result = planning_node(
                {
                    "issue_key": "TEST-1",
                    "issue_data": {
                        "summary": "Valid summary here",
                        "description": "Valid description that is long enough to pass blocked check",
                    },
                }
            )
            assert result["error"] is not None
            assert "no config" in result["error"]

    def test_emits_blocked_event(self):
        result = planning_node(
            {
                "issue_key": "T-1",
                "issue_data": {"summary": "", "description": "x"},
            }
        )
        assert result["events"][0]["event"] == "planning_blocked"

    def test_emits_completed_event(self):
        mock_response = MagicMock()
        mock_response.text = "plan"
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 1
        mock_response.usage.output_tokens = 1

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that is long enough",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
            assert result["events"][0]["event"] == "planning_completed"

    def test_accumulates_token_usage(self):
        mock_response = MagicMock()
        mock_response.text = "plan"
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 200
        mock_response.usage.output_tokens = 100

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that is long enough",
                        "description": "A valid description with enough detail to proceed",
                    },
                    "token_usage_prompt": 50,
                    "token_usage_completion": 25,
                }
            )
            assert result["token_usage_prompt"] == 250
            assert result["token_usage_completion"] == 125

    def test_missing_issue_data_defaults_to_empty(self):
        result = planning_node({"issue_key": "T-1"})
        assert result["status"] == "blocked"

    def test_coerces_non_dict_issue_data_to_empty_dict_before_plan_generation(self):
        with (
            patch("agentic_devtools.orchestration.nodes.planning._check_blocked", return_value=None),
            patch(
                "agentic_devtools.orchestration.nodes.planning._generate_plan",
                return_value={"plan": "ok", "is_blocked": False, "blocked_reason": "", "token_usage": {}},
            ) as mock_generate,
        ):
            planning_node({"issue_key": "T-1", "issue_data": "corrupted"})
            assert mock_generate.call_args[0][1] == {}

    def test_llm_detected_blocked_returns_blocked_status(self):
        """Cover lines 69-71: LLM returns is_blocked=true in its response."""
        mock_response = MagicMock()
        mock_response.text = json.dumps({"is_blocked": True, "blocked_reason": "Ambiguous requirements", "plan": ""})
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 5

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
            assert result["status"] == "blocked"
            assert result["blocked_reason"] == "Ambiguous requirements"
            assert result["events"][0]["event"] == "planning_blocked"

    def test_non_json_llm_response_treated_as_plan_text(self):
        """Cover line 175: response.text is not valid JSON, fallback to plain text."""
        mock_response = MagicMock()
        mock_response.text = "Here is my plan:\n1. Do thing A\n2. Do thing B"
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 50
        mock_response.usage.output_tokens = 30

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
            assert result["plan"] == "Here is my plan:\n1. Do thing A\n2. Do thing B"
            assert result["plan_posted"] is True

    def test_json_list_response_falls_back_to_plain_text(self):
        """JSON-valid but non-dict response (e.g. a list) must fall back to raw text."""
        mock_response = MagicMock()
        mock_response.text = '["step1", "step2"]'
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 5

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
            assert result["plan"] == '["step1", "step2"]'
            assert result["plan_posted"] is True

    def test_json_string_response_falls_back_to_plain_text(self):
        """JSON-valid string (not dict) must fall back to raw text, not raise AttributeError."""
        mock_response = MagicMock()
        mock_response.text = '"just a string"'
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 5
        mock_response.usage.output_tokens = 3

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
            assert result["plan"] == '"just a string"'
            assert result["plan_posted"] is True

    def test_no_usage_on_response_returns_empty_token_usage(self):
        """Cover branch 166->173: response.usage is None, token_usage stays empty."""
        mock_response = MagicMock()
        mock_response.text = "## Plan\n\n1. Do A"
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                    "token_usage_prompt": 10,
                    "token_usage_completion": 5,
                }
            )
            # Token usage should not increase when usage is None
            assert result["token_usage_prompt"] == 10
            assert result["token_usage_completion"] == 5

    def test_corrupted_none_token_state_does_not_raise(self):
        """Corrupted None state values for token_usage must not raise TypeError."""
        mock_response = MagicMock()
        mock_response.text = "plan"
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 50
        mock_response.usage.output_tokens = 25

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                    "token_usage_prompt": None,
                    "token_usage_completion": None,
                }
            )
            assert result["token_usage_prompt"] == 50
            assert result["token_usage_completion"] == 25

    def test_corrupted_bool_token_state_does_not_raise(self):
        """Boolean state values for token_usage must not be treated as 1/0."""
        mock_response = MagicMock()
        mock_response.text = "plan"
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 5

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with (
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment", return_value=True),
            patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory,
        ):
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                    "token_usage_prompt": True,
                    "token_usage_completion": False,
                }
            )
            assert result["token_usage_prompt"] == 10
            assert result["token_usage_completion"] == 5

    def test_description_as_dict_does_not_crash(self):
        """ADF dict in issue_data['description'] must be treated as empty, not raise AttributeError."""
        adf_description = {"type": "doc", "version": 1, "content": []}
        result = planning_node(
            {
                "issue_key": "T-1",
                "issue_data": {"summary": "Valid summary", "description": adf_description},
            }
        )
        # Non-string description is coerced to "" → too short → blocked
        assert result["status"] == "blocked"
        assert "description" in result["blocked_reason"].lower()

    def test_description_as_none_does_not_crash(self):
        """None in issue_data['description'] must be treated as empty, not raise AttributeError."""
        result = planning_node(
            {
                "issue_key": "T-1",
                "issue_data": {"summary": "Valid summary", "description": None},
            }
        )
        assert result["status"] == "blocked"
        assert "description" in result["blocked_reason"].lower()

    def test_summary_as_none_does_not_crash(self):
        """None in issue_data['summary'] must be treated as empty, not raise AttributeError."""
        result = planning_node(
            {
                "issue_key": "T-1",
                "issue_data": {"summary": None, "description": "A valid description"},
            }
        )
        assert result["status"] == "blocked"
        assert "summary" in result["blocked_reason"].lower()

    def test_missing_issue_key_fails_fast(self):
        """Absent issue_key must return an error without calling the LLM."""
        result = planning_node({"issue_data": {"summary": "Valid summary", "description": "Valid description"}})
        assert "error" in result
        assert "issue_key" in result["error"]
        assert result["events"][0]["event"] == "planning_failed"

    def test_blank_issue_key_fails_fast(self):
        """Blank string issue_key must return an error without calling the LLM."""
        result = planning_node(
            {
                "issue_key": "   ",
                "issue_data": {"summary": "Valid summary", "description": "Valid description"},
            }
        )
        assert "error" in result
        assert "issue_key" in result["error"]
        assert result["events"][0]["event"] == "planning_failed"

    def test_non_string_issue_key_fails_fast(self):
        """Non-string issue_key (e.g. from corrupted checkpoint) must return an error."""
        result = planning_node(
            {
                "issue_key": 42,
                "issue_data": {"summary": "Valid summary", "description": "Valid description"},
            }
        )
        assert "error" in result
        assert "issue_key" in result["error"]
        assert result["events"][0]["event"] == "planning_failed"

    def test_llm_blocked_with_non_string_blocked_reason_uses_fallback(self):
        """LLM returning a non-string blocked_reason (e.g. list/dict) must be coerced to fallback message."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning._post_planning_comment",
                return_value=True,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.planning._generate_plan",
                return_value={
                    "is_blocked": True,
                    "blocked_reason": ["ambiguous", "missing details"],
                    "token_usage": {},
                },
            ),
        ):
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
        assert result["status"] == "blocked"
        assert isinstance(result["blocked_reason"], str)
        assert result["blocked_reason"] == "Issue is too ambiguous for autonomous implementation"

    def test_llm_blocked_with_empty_string_blocked_reason_uses_fallback(self):
        """LLM returning is_blocked=true with empty blocked_reason must use the fallback message."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning._post_planning_comment",
                return_value=True,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.planning._generate_plan",
                return_value={"is_blocked": True, "blocked_reason": "", "token_usage": {}},
            ),
        ):
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
        assert result["status"] == "blocked"
        assert result["blocked_reason"] == "Issue is too ambiguous for autonomous implementation"

    def test_non_boolean_is_blocked_flag_does_not_block(self):
        """A non-boolean is_blocked value must not route the workflow to the blocked path."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning._post_planning_comment",
                return_value=True,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.planning._generate_plan",
                return_value={
                    "is_blocked": "false",
                    "blocked_reason": "should be ignored",
                    "plan": "my plan",
                    "token_usage": {},
                },
            ),
        ):
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
        assert "status" not in result or result["status"] != "blocked"
        assert result["plan"] == "my plan"
        assert result["plan_posted"] is True

    def test_non_string_plan_is_treated_as_empty(self):
        """A non-string plan value must be treated as empty instead of a fake stringified plan."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning._post_planning_comment",
                return_value=True,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.planning._generate_plan",
                return_value={"is_blocked": False, "blocked_reason": "", "plan": ["step1", "step2"], "token_usage": {}},
            ),
        ):
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
        assert result["plan_posted"] is True
        assert isinstance(result["plan"], str)
        assert result["plan"] == ""

    def test_non_dict_token_usage_falls_back_to_empty(self):
        """Non-dict token_usage (e.g. list from corrupted state) must not raise AttributeError."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning._post_planning_comment",
                return_value=True,
            ),
            patch(
                "agentic_devtools.orchestration.nodes.planning._generate_plan",
                return_value={"is_blocked": False, "blocked_reason": "", "plan": "my plan", "token_usage": [1, 2, 3]},
            ),
        ):
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                    "token_usage_prompt": 10,
                    "token_usage_completion": 5,
                }
            )
        # token_usage was a list (non-dict), so prompt/completion tokens from it are 0
        assert result["token_usage_prompt"] == 10
        assert result["token_usage_completion"] == 5
        assert result["plan_posted"] is True


class TestPlanningNodeDryRun:
    def test_dry_run_skips_posting(self):
        """dry_run: plan_posted is False (best-effort not delivered) and dry_run_skipped is True."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning._post_planning_comment",
                return_value=True,
            ) as mock_post,
            patch(
                "agentic_devtools.orchestration.nodes.planning._generate_plan",
                return_value={"is_blocked": False, "plan": "my plan", "token_usage": {}},
            ),
        ):
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "dry_run": True,
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
            assert result["plan_posted"] is False
            assert result["dry_run_skipped"] is True
            mock_post.assert_not_called()

    def test_truthy_non_bool_dry_run_does_not_skip(self):
        """A truthy non-bool dry_run value (e.g. string 'false') must NOT skip posting."""
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning._post_planning_comment",
                return_value=True,
            ) as mock_post,
            patch(
                "agentic_devtools.orchestration.nodes.planning._generate_plan",
                return_value={"is_blocked": False, "plan": "my plan", "token_usage": {}},
            ),
        ):
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "dry_run": "false",
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )
            assert result["dry_run_skipped"] is False
            assert result["plan_posted"] is True
            mock_post.assert_called_once()

    def test_dry_run_logs_rendered_comment_preview(self, caplog):
        caplog.set_level("INFO")
        with (
            patch(
                "agentic_devtools.orchestration.nodes.planning.format_planning_comment",
                return_value="rendered plan",
            ),
            patch(
                "agentic_devtools.orchestration.nodes.planning._generate_plan",
                return_value={
                    "is_blocked": False,
                    "plan": "my plan",
                    "tasks": [{"description": "Task A", "affected_files": ["src/a.py"]}],
                    "risks": [{"description": "Regression", "mitigation": "Add tests"}],
                    "token_usage": {},
                },
            ),
            patch("agentic_devtools.orchestration.nodes.planning._post_planning_comment") as mock_post,
        ):
            result = planning_node(
                {
                    "issue_key": "T-1",
                    "issue_provider": "github",
                    "dry_run": True,
                    "issue_data": {
                        "summary": "Valid summary that passes check",
                        "description": "A valid description with enough detail to proceed",
                    },
                }
            )

        assert result["dry_run_skipped"] is True
        assert result["plan_posted"] is False
        assert "rendered plan" in caplog.text
        mock_post.assert_not_called()
