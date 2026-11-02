"""Tests for _generate_plan."""

from unittest.mock import AsyncMock, MagicMock, patch

from agentic_devtools.orchestration.nodes.planning import _generate_plan


class TestGeneratePlan:
    def test_non_string_issue_fields_are_omitted_from_prompt(self):
        mock_response = MagicMock()
        mock_response.text = "plan"
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider

            _generate_plan(
                "T-1",
                {
                    "summary": {"type": "doc", "content": []},
                    "description": ["step 1", "step 2"],
                },
            )

        messages = mock_provider.complete.await_args.args[0]
        assert messages[1].content == "Issue Key: T-1\nSummary: \n\nDescription:\n"

    def test_structured_json_response_preserves_tasks_and_risks(self):
        mock_response = MagicMock()
        mock_response.text = (
            '{"is_blocked": false, "plan": "Do work", '
            '"tasks": [{"description": "Add node", "affected_files": ["a.py", "b.py"]}], '
            '"risks": [{"description": "Regression", "mitigation": "Add tests"}]}'
        )
        mock_response.usage = None

        mock_provider = MagicMock()
        mock_provider.complete = AsyncMock(return_value=mock_response)

        with patch("agentic_devtools.orchestration.llm.factory.ProviderFactory") as mock_factory:
            mock_factory.return_value.get_provider.return_value = mock_provider

            result = _generate_plan("T-1", {"summary": "Summary", "description": "Detailed description"})

        assert result["plan"] == "Do work"
        assert result["tasks"] == [{"description": "Add node", "affected_files": ["a.py", "b.py"]}]
        assert result["risks"] == [{"description": "Regression", "mitigation": "Add tests"}]
