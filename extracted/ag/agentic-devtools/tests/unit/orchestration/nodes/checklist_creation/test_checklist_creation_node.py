"""Tests for checklist_creation_node."""

from unittest.mock import AsyncMock, MagicMock, patch

from agentic_devtools.orchestration.nodes.checklist_creation import (
    _generate_checklist,
    checklist_creation_node,
)


class TestChecklistCreationNode:
    def test_returns_error_when_no_plan(self):
        result = checklist_creation_node({"plan": "", "issue_key": "TEST-1"})
        assert result["error"] is not None
        assert "No plan" in result["error"]
        assert result["step"] == "checklist_creation"

    def test_returns_error_on_exception(self):
        with patch(
            "agentic_devtools.orchestration.nodes.checklist_creation._generate_checklist",
            side_effect=RuntimeError("LLM unavailable"),
        ):
            result = checklist_creation_node({"plan": "Do things", "issue_key": "TEST-1"})
            assert result["error"] is not None
            assert "LLM unavailable" in result["error"]

    def test_returns_checklist_items_on_success(self):
        mock_items = [{"description": "item 1", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.checklist_creation._generate_checklist",
            return_value={"items": mock_items, "token_usage": {"prompt_tokens": 10, "completion_tokens": 5}},
        ):
            result = checklist_creation_node({"plan": "Do things", "issue_key": "T-1"})
            assert result["checklist_items"] == mock_items
            assert result["checklist_created"] is True
            assert result["token_usage_prompt"] == 10
            assert result["token_usage_completion"] == 5

    def test_success_clears_stale_error_from_checkpoint(self):
        """A resumed checkpoint carrying a stale error must be cleared on success."""
        mock_items = [{"description": "item 1", "is_complete": False}]
        with patch(
            "agentic_devtools.orchestration.nodes.checklist_creation._generate_checklist",
            return_value={"items": mock_items, "token_usage": {}},
        ):
            result = checklist_creation_node({"plan": "Do things", "issue_key": "T-1", "error": "stale error"})
            assert result["error"] is None
            assert result["checklist_created"] is True

    def test_accumulates_token_usage(self):
        with patch(
            "agentic_devtools.orchestration.nodes.checklist_creation._generate_checklist",
            return_value={"items": [], "token_usage": {"prompt_tokens": 50, "completion_tokens": 25}},
        ):
            result = checklist_creation_node(
                {
                    "plan": "Do things",
                    "issue_key": "T-1",
                    "token_usage_prompt": 100,
                    "token_usage_completion": 50,
                }
            )
            assert result["token_usage_prompt"] == 150
            assert result["token_usage_completion"] == 75

    def test_handles_empty_token_usage(self):
        with patch(
            "agentic_devtools.orchestration.nodes.checklist_creation._generate_checklist",
            return_value={"items": [], "token_usage": {}},
        ):
            result = checklist_creation_node({"plan": "Do things", "issue_key": "T-1"})
            assert result["token_usage_prompt"] == 0
            assert result["token_usage_completion"] == 0

    def test_corrupted_none_token_state_does_not_raise(self):
        """Corrupted None state values for token_usage must not raise TypeError."""
        with patch(
            "agentic_devtools.orchestration.nodes.checklist_creation._generate_checklist",
            return_value={"items": [], "token_usage": {"prompt_tokens": 30, "completion_tokens": 15}},
        ):
            result = checklist_creation_node(
                {
                    "plan": "Do things",
                    "issue_key": "T-1",
                    "token_usage_prompt": None,
                    "token_usage_completion": None,
                }
            )
            assert result["token_usage_prompt"] == 30
            assert result["token_usage_completion"] == 15

    def test_corrupted_bool_token_state_does_not_raise(self):
        """Boolean state values for token_usage must not be treated as 1/0."""
        with patch(
            "agentic_devtools.orchestration.nodes.checklist_creation._generate_checklist",
            return_value={"items": [], "token_usage": {"prompt_tokens": 20, "completion_tokens": 10}},
        ):
            result = checklist_creation_node(
                {
                    "plan": "Do things",
                    "issue_key": "T-1",
                    "token_usage_prompt": True,
                    "token_usage_completion": False,
                }
            )
            assert result["token_usage_prompt"] == 20
            assert result["token_usage_completion"] == 10

    def test_emits_completed_event(self):
        with patch(
            "agentic_devtools.orchestration.nodes.checklist_creation._generate_checklist",
            return_value={"items": [{"x": 1}], "token_usage": {}},
        ):
            result = checklist_creation_node({"plan": "Do things", "issue_key": "T-1"})
            assert result["events"][0]["event"] == "checklist_creation_completed"
            assert result["events"][0]["signals"]["item_count"] == 1

    def test_emits_failed_event_on_no_plan(self):
        result = checklist_creation_node({"plan": "", "issue_key": "T-1"})
        assert result["events"][0]["event"] == "checklist_creation_failed"

    def test_emits_failed_event_on_exception(self):
        with patch(
            "agentic_devtools.orchestration.nodes.checklist_creation._generate_checklist",
            side_effect=ValueError("bad"),
        ):
            result = checklist_creation_node({"plan": "X", "issue_key": "T-1"})
            assert result["events"][0]["event"] == "checklist_creation_failed"


class TestGenerateChecklist:
    def test_parses_valid_json_response(self):
        mock_response = MagicMock()
        mock_response.text = '{"items": [{"description": "a", "is_complete": false}]}'
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 20
        mock_response.usage.output_tokens = 10

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_checklist("T-1", "some plan")
            assert result["items"] == [{"description": "a", "is_complete": False}]
            assert result["token_usage"]["prompt_tokens"] == 20

    def test_fallback_on_invalid_json(self):
        mock_response = MagicMock()
        mock_response.text = "not valid json"
        mock_response.usage = MagicMock()
        mock_response.usage.input_tokens = 5
        mock_response.usage.output_tokens = 3

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_checklist("T-1", "plan")
            assert len(result["items"]) == 1
            assert result["items"][0]["description"] == "Implement the plan as described"

    def test_handles_none_usage(self):
        mock_response = MagicMock()
        mock_response.text = '{"items": [{"description": "a", "is_complete": false}]}'
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_checklist("T-1", "plan")
            assert result["token_usage"] == {}

    def test_empty_items_list_falls_back_to_default(self):
        """items=[] is falsy — must use fallback item so implementation_node is not tricked."""
        mock_response = MagicMock()
        mock_response.text = '{"items": []}'
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_checklist("T-1", "plan")
            assert len(result["items"]) == 1
            assert result["items"][0]["description"] == "Implement the plan as described"

    def test_missing_items_key_falls_back_to_default(self):
        """items key absent from JSON dict must use fallback."""
        mock_response = MagicMock()
        mock_response.text = '{"other_key": "value"}'
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_checklist("T-1", "plan")
            assert len(result["items"]) == 1
            assert result["items"][0]["description"] == "Implement the plan as described"

    def test_non_list_items_value_falls_back_to_default(self):
        """items value that is not a list (e.g. a string) must use fallback."""
        mock_response = MagicMock()
        mock_response.text = '{"items": "do everything"}'
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_checklist("T-1", "plan")
            assert len(result["items"]) == 1
            assert result["items"][0]["description"] == "Implement the plan as described"

    def test_json_list_response_falls_back_to_default(self):
        """JSON-valid but non-dict (e.g. a list) must use fallback, not raise AttributeError."""
        mock_response = MagicMock()
        mock_response.text = '["step1", "step2"]'
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider
            result = _generate_checklist("T-1", "plan")
            assert len(result["items"]) == 1
            assert result["items"][0]["description"] == "Implement the plan as described"
