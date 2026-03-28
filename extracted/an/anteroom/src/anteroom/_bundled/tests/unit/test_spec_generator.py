"""Unit tests for spec_generator — LLM-assisted spec generation (#1165)."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.spec_generator import (
    generate_spec_from_issue,
    generate_spec_from_prompt,
)


def _make_ai_service(response: str | None) -> AsyncMock:
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value=response)
    return svc


VALID_LLM_JSON = json.dumps(
    {
        "requirements": "Must support widgets.",
        "design": "Use the widget parser pattern.",
        "tasks": [
            {"id": "t1", "summary": "Implement parser"},
            {"id": "t2", "summary": "Add tests", "depends_on": ["t1"]},
        ],
    }
)

VALID_LLM_JSON_FENCED = f"```json\n{VALID_LLM_JSON}\n```"


# ---------------------------------------------------------------------------
# generate_spec_from_prompt — valid JSON
# ---------------------------------------------------------------------------


class TestGenerateFromPromptValid:
    @pytest.mark.asyncio
    async def test_valid_json_returns_yaml(self) -> None:
        svc = _make_ai_service(VALID_LLM_JSON)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "requirements" in result
        assert "design" in result
        assert "tasks" in result
        assert "WARNING" not in result

    @pytest.mark.asyncio
    async def test_valid_json_parseable_as_spec(self) -> None:
        from anteroom.services.spec_schema import parse_spec_content

        svc = _make_ai_service(VALID_LLM_JSON)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        spec = parse_spec_content(result)
        assert spec.requirements.strip() == "Must support widgets."
        assert spec.design.strip() == "Use the widget parser pattern."
        assert len(spec.tasks) == 2

    @pytest.mark.asyncio
    async def test_valid_json_preserves_depends_on(self) -> None:
        from anteroom.services.spec_schema import parse_spec_content

        svc = _make_ai_service(VALID_LLM_JSON)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        spec = parse_spec_content(result)
        assert spec.tasks[1].depends_on == ["t1"]

    @pytest.mark.asyncio
    async def test_valid_json_with_fences(self) -> None:
        svc = _make_ai_service(VALID_LLM_JSON_FENCED)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" not in result
        assert "requirements" in result

    @pytest.mark.asyncio
    async def test_requirements_field_present(self) -> None:
        from anteroom.services.spec_schema import parse_spec_content

        svc = _make_ai_service(VALID_LLM_JSON)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        spec = parse_spec_content(result)
        assert "widgets" in spec.requirements.lower()

    @pytest.mark.asyncio
    async def test_design_field_present(self) -> None:
        from anteroom.services.spec_schema import parse_spec_content

        svc = _make_ai_service(VALID_LLM_JSON)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        spec = parse_spec_content(result)
        assert "widget parser" in spec.design.lower()

    @pytest.mark.asyncio
    async def test_tasks_field_present(self) -> None:
        from anteroom.services.spec_schema import parse_spec_content

        svc = _make_ai_service(VALID_LLM_JSON)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        spec = parse_spec_content(result)
        assert spec.tasks[0].id == "t1"
        assert spec.tasks[1].id == "t2"

    @pytest.mark.asyncio
    async def test_calls_ai_service_complete(self) -> None:
        svc = _make_ai_service(VALID_LLM_JSON)
        await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        svc.complete.assert_awaited_once()
        messages = svc.complete.call_args[0][0]
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Build widgets"


# ---------------------------------------------------------------------------
# generate_spec_from_prompt — malformed/partial
# ---------------------------------------------------------------------------


class TestGenerateFromPromptFallback:
    @pytest.mark.asyncio
    async def test_malformed_json_returns_warning(self) -> None:
        svc = _make_ai_service("this is not json at all")
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" in result
        assert "this is not json at all" in result

    @pytest.mark.asyncio
    async def test_partial_json_missing_requirements(self) -> None:
        partial = json.dumps({"design": "d", "tasks": [{"id": "t1", "summary": "s"}]})
        svc = _make_ai_service(partial)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" in result

    @pytest.mark.asyncio
    async def test_partial_json_missing_design(self) -> None:
        partial = json.dumps({"requirements": "r", "tasks": [{"id": "t1", "summary": "s"}]})
        svc = _make_ai_service(partial)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" in result

    @pytest.mark.asyncio
    async def test_partial_json_missing_tasks(self) -> None:
        partial = json.dumps({"requirements": "r", "design": "d"})
        svc = _make_ai_service(partial)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" in result

    @pytest.mark.asyncio
    async def test_empty_response_returns_warning(self) -> None:
        svc = _make_ai_service(None)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" in result

    @pytest.mark.asyncio
    async def test_empty_string_response(self) -> None:
        svc = _make_ai_service("")
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" in result

    @pytest.mark.asyncio
    async def test_empty_prompt_still_calls_ai(self) -> None:
        svc = _make_ai_service(VALID_LLM_JSON)
        result = await generate_spec_from_prompt("", ai_service=svc, namespace="ns", name="feat")
        svc.complete.assert_awaited_once()
        assert "WARNING" not in result

    @pytest.mark.asyncio
    async def test_tasks_not_a_list(self) -> None:
        bad = json.dumps({"requirements": "r", "design": "d", "tasks": "not a list"})
        svc = _make_ai_service(bad)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" in result

    @pytest.mark.asyncio
    async def test_empty_tasks_list(self) -> None:
        bad = json.dumps({"requirements": "r", "design": "d", "tasks": []})
        svc = _make_ai_service(bad)
        result = await generate_spec_from_prompt("Build widgets", ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" in result


# ---------------------------------------------------------------------------
# generate_spec_from_issue
# ---------------------------------------------------------------------------


class TestGenerateFromIssue:
    @pytest.mark.asyncio
    async def test_success(self) -> None:
        issue_json = json.dumps({"title": "Add widgets", "body": "We need widgets.", "labels": [{"name": "feat"}]})
        mock_result = MagicMock(returncode=0, stdout=issue_json, stderr="")
        svc = _make_ai_service(VALID_LLM_JSON)
        with patch("anteroom.services.spec_generator.subprocess.run", return_value=mock_result):
            result = await generate_spec_from_issue(42, ai_service=svc, namespace="ns", name="feat")
        assert "WARNING" not in result
        assert "requirements" in result

    @pytest.mark.asyncio
    async def test_prompt_includes_title_and_body(self) -> None:
        issue_json = json.dumps({"title": "Add widgets", "body": "Detailed body.", "labels": []})
        mock_result = MagicMock(returncode=0, stdout=issue_json, stderr="")
        svc = _make_ai_service(VALID_LLM_JSON)
        with patch("anteroom.services.spec_generator.subprocess.run", return_value=mock_result):
            await generate_spec_from_issue(42, ai_service=svc, namespace="ns", name="feat")
        prompt = svc.complete.call_args[0][0][1]["content"]
        assert "Add widgets" in prompt
        assert "Detailed body." in prompt

    @pytest.mark.asyncio
    async def test_not_found_raises_value_error(self) -> None:
        mock_result = MagicMock(returncode=1, stdout="", stderr="issue not found")
        svc = _make_ai_service(VALID_LLM_JSON)
        with patch("anteroom.services.spec_generator.subprocess.run", return_value=mock_result):
            with pytest.raises(ValueError, match="Failed to fetch issue"):
                await generate_spec_from_issue(999, ai_service=svc, namespace="ns", name="feat")

    @pytest.mark.asyncio
    async def test_timeout_raises_value_error(self) -> None:
        svc = _make_ai_service(VALID_LLM_JSON)
        with patch(
            "anteroom.services.spec_generator.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="gh", timeout=15),
        ):
            with pytest.raises(ValueError, match="Timed out"):
                await generate_spec_from_issue(42, ai_service=svc, namespace="ns", name="feat")

    @pytest.mark.asyncio
    async def test_gh_not_found_raises_value_error(self) -> None:
        svc = _make_ai_service(VALID_LLM_JSON)
        with patch(
            "anteroom.services.spec_generator.subprocess.run",
            side_effect=FileNotFoundError(),
        ):
            with pytest.raises(ValueError, match="gh.*not found"):
                await generate_spec_from_issue(42, ai_service=svc, namespace="ns", name="feat")

    @pytest.mark.asyncio
    async def test_unparseable_gh_output(self) -> None:
        mock_result = MagicMock(returncode=0, stdout="not json", stderr="")
        svc = _make_ai_service(VALID_LLM_JSON)
        with patch("anteroom.services.spec_generator.subprocess.run", return_value=mock_result):
            with pytest.raises(ValueError, match="Could not parse"):
                await generate_spec_from_issue(42, ai_service=svc, namespace="ns", name="feat")

    @pytest.mark.asyncio
    async def test_labels_included_in_prompt(self) -> None:
        issue_json = json.dumps({"title": "Bug", "body": "It breaks.", "labels": [{"name": "bug"}, {"name": "urgent"}]})
        mock_result = MagicMock(returncode=0, stdout=issue_json, stderr="")
        svc = _make_ai_service(VALID_LLM_JSON)
        with patch("anteroom.services.spec_generator.subprocess.run", return_value=mock_result):
            await generate_spec_from_issue(42, ai_service=svc, namespace="ns", name="feat")
        prompt = svc.complete.call_args[0][0][1]["content"]
        assert "bug" in prompt
        assert "urgent" in prompt
