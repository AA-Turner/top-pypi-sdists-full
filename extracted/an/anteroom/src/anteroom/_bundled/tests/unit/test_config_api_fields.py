"""Tests for config_api.py scoped config editing endpoints."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from anteroom.routers.config_api import (
    ConfigFieldResetBody,
    ConfigFieldSetBody,
    _get_active_space,
    _get_working_dir,
    _persist_config,
    explain_config_field,
    get_config_field,
    get_config_sources,
    list_config_fields,
    reset_config_field,
    set_config_field,
)


def _make_request(
    enforced_fields: list[str] | None = None,
    active_space: dict[str, Any] | None = None,
) -> MagicMock:
    request = MagicMock()
    request.app.state.enforced_fields = enforced_fields or []
    request.app.state.active_space = active_space
    request.app.state.config = MagicMock()
    return request


# ---------------------------------------------------------------------------
# _get_active_space
# ---------------------------------------------------------------------------


class TestGetActiveSpace:
    def test_returns_space_if_set(self) -> None:
        request = _make_request(active_space={"id": "s1", "name": "test"})
        assert _get_active_space(request) == {"id": "s1", "name": "test"}

    def test_returns_none_if_missing(self) -> None:
        request = MagicMock()
        request.app.state = MagicMock(spec=[])
        assert _get_active_space(request) is None


# ---------------------------------------------------------------------------
# _get_working_dir
# ---------------------------------------------------------------------------


class TestGetWorkingDir:
    def test_returns_space_dir_if_available(self) -> None:
        space = {"source_file": "/home/user/.anteroom/space.yaml"}
        request = _make_request(active_space=space)
        assert _get_working_dir(request) == "/home/user/.anteroom"

    def test_falls_back_to_cwd(self) -> None:
        request = _make_request()
        request.app.state.active_space = None
        with patch("anteroom.routers.config_api.os.getcwd", return_value="/tmp"):
            assert _get_working_dir(request) == "/tmp"


# ---------------------------------------------------------------------------
# get_config_field
# ---------------------------------------------------------------------------


class TestGetConfigField:
    @pytest.mark.asyncio
    async def test_sensitive_field_returns_403(self) -> None:
        request = _make_request()
        with pytest.raises(HTTPException) as exc_info:
            await get_config_field("ai.api_key", request)
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_malformed_dot_path_returns_400(self) -> None:
        request = _make_request()

        with (
            patch("anteroom.routers.config_api._build_api_context", return_value=({}, [])),
            patch(
                "anteroom.routers.config_api.get_config_field.__wrapped__",
                side_effect=HTTPException(status_code=400),
            )
            if False
            else pytest.raises(HTTPException) as exc_info,
        ):
            # get_field raises ValueError on malformed paths
            with patch("anteroom.services.config_editor.get_field", side_effect=ValueError("bad path")):
                with patch("anteroom.routers.config_api._build_api_context", return_value=({}, [])):
                    await get_config_field("", request)
        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_existing_field_returns_200(self) -> None:
        request = _make_request()
        mock_result = MagicMock()
        mock_result.dot_path = "ai.model"
        mock_result.effective_value = "gpt-4"
        mock_result.source_layer = "personal"
        mock_result.is_enforced = False
        mock_result.field_info = None

        with (
            patch("anteroom.routers.config_api._build_api_context", return_value=({}, [])),
            patch("anteroom.services.config_editor.get_field", return_value=mock_result),
        ):
            result = await get_config_field("ai.model", request)
        assert result["dot_path"] == "ai.model"
        assert result["effective_value"] == "gpt-4"

    @pytest.mark.asyncio
    async def test_nonexistent_field_returns_null_value(self) -> None:
        request = _make_request()
        mock_result = MagicMock()
        mock_result.dot_path = "ai.nonexistent"
        mock_result.effective_value = None
        mock_result.source_layer = None
        mock_result.is_enforced = False
        mock_result.field_info = None

        with (
            patch("anteroom.routers.config_api._build_api_context", return_value=({}, [])),
            patch("anteroom.services.config_editor.get_field", return_value=mock_result),
        ):
            result = await get_config_field("ai.nonexistent", request)
        assert result["effective_value"] is None


# ---------------------------------------------------------------------------
# set_config_field
# ---------------------------------------------------------------------------


class TestSetConfigField:
    @pytest.mark.asyncio
    async def test_sensitive_field_returns_403(self) -> None:
        request = _make_request()
        body = ConfigFieldSetBody(dot_path="ai.api_key", value="secret", scope="personal")
        with pytest.raises(HTTPException) as exc_info:
            await set_config_field(body, request)
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_invalid_scope_returns_400(self) -> None:
        request = _make_request()
        body = ConfigFieldSetBody(dot_path="ai.model", value="gpt-4", scope="invalid")

        with (
            patch("anteroom.services.config_editor.check_write_allowed", return_value=(True, None)),
            patch("anteroom.services.config_editor.validate_field_value", return_value=("gpt-4", [])),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await set_config_field(body, request)
            assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_enforced_field_returns_403(self) -> None:
        request = _make_request(enforced_fields=["ai.model"])
        body = ConfigFieldSetBody(dot_path="ai.model", value="gpt-4", scope="personal")

        with patch(
            "anteroom.services.config_editor.check_write_allowed",
            return_value=(False, "Enforced by team config"),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await set_config_field(body, request)
            assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_validation_error_returns_422(self) -> None:
        request = _make_request()
        body = ConfigFieldSetBody(dot_path="ai.temperature", value="not-a-number", scope="personal")

        with (
            patch("anteroom.services.config_editor.check_write_allowed", return_value=(True, None)),
            patch(
                "anteroom.services.config_editor.validate_field_value",
                return_value=(None, ["must be a number"]),
            ),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await set_config_field(body, request)
            assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_valid_personal_set_succeeds(self) -> None:
        request = _make_request()
        body = ConfigFieldSetBody(dot_path="ai.model", value="gpt-4o", scope="personal")

        with (
            patch("anteroom.services.config_editor.check_write_allowed", return_value=(True, None)),
            patch("anteroom.services.config_editor.validate_field_value", return_value=("gpt-4o", [])),
            patch("anteroom.services.config_editor.write_personal_field", return_value=Path("/cfg.yaml")),
            patch("anteroom.services.config_editor.apply_field_to_config"),
        ):
            result = await set_config_field(body, request)
            assert result["dot_path"] == "ai.model"
            assert result["value"] == "gpt-4o"
            assert result["scope"] == "personal"


# ---------------------------------------------------------------------------
# reset_config_field
# ---------------------------------------------------------------------------


class TestResetConfigField:
    @pytest.mark.asyncio
    async def test_sensitive_field_returns_403(self) -> None:
        request = _make_request()
        body = ConfigFieldResetBody(dot_path="ai.api_key", scope="personal")
        with pytest.raises(HTTPException) as exc_info:
            await reset_config_field(body, request)
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_invalid_scope_returns_400(self) -> None:
        request = _make_request()
        body = ConfigFieldResetBody(dot_path="ai.model", scope="galaxy")
        with pytest.raises(HTTPException) as exc_info:
            await reset_config_field(body, request)
        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_personal_reset_succeeds(self) -> None:
        request = _make_request()
        body = ConfigFieldResetBody(dot_path="ai.model", scope="personal")

        with patch("anteroom.services.config_editor.reset_personal_field", return_value=True):
            result = await reset_config_field(body, request)
            assert result["deleted"] is True
            assert result["scope"] == "personal"


# ---------------------------------------------------------------------------
# list_config_fields
# ---------------------------------------------------------------------------


class TestListConfigFields:
    @pytest.mark.asyncio
    async def test_returns_field_list(self) -> None:
        request = _make_request()
        result = await list_config_fields(request)
        paths = [item["dot_path"] for item in result]
        assert "ai.model" in paths

    @pytest.mark.asyncio
    async def test_query_filters_registry_results(self) -> None:
        request = _make_request()
        result = await list_config_fields(request, query="approval")
        paths = [item["dot_path"] for item in result]
        assert "safety.approval_mode" in paths

    @pytest.mark.asyncio
    async def test_include_current_redacts_sensitive_values(self) -> None:
        request = _make_request()
        request.app.state.config = {"ai": {"api_key": "secret"}}

        with patch("anteroom.routers.config_api._build_api_context", return_value=({}, [])):
            result = await list_config_fields(request, query="ai.api_key", include_current=True, include_sensitive=True)

        assert result[0]["sensitive"] is True
        assert result[0]["current"]["effective_value"] == "***"


# ---------------------------------------------------------------------------
# config explanation endpoints
# ---------------------------------------------------------------------------


class TestConfigExplanationEndpoints:
    @pytest.mark.asyncio
    async def test_explain_config_field_returns_redacted_payload(self) -> None:
        request = _make_request()
        mock_explanation = MagicMock()
        mock_explanation.to_dict.return_value = {
            "dot_path": "ai.api_key",
            "effective_value": "***",
            "is_sensitive": True,
        }

        with (
            patch("anteroom.services.config_explanation.build_explanation_context", return_value=MagicMock()),
            patch("anteroom.services.config_explanation.explain_setting", return_value=mock_explanation),
        ):
            result = await explain_config_field("ai.api_key", request)

        assert result["effective_value"] == "***"
        assert result["is_sensitive"] is True

    @pytest.mark.asyncio
    async def test_explain_config_field_invalid_path_returns_400(self) -> None:
        request = _make_request()

        with (
            patch("anteroom.services.config_explanation.build_explanation_context", return_value=MagicMock()),
            patch("anteroom.services.config_explanation.explain_setting", side_effect=ValueError("bad path")),
            pytest.raises(HTTPException) as exc_info,
        ):
            await explain_config_field("", request)

        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_get_config_sources_returns_structured_sources(self) -> None:
        request = _make_request(enforced_fields=["ai.model"])
        payload = {"layers": [], "enforced_fields": ["ai.model"], "pack_contributions": []}

        with (
            patch("anteroom.services.config_explanation.build_explanation_context", return_value=MagicMock()),
            patch("anteroom.services.config_explanation.list_sources", return_value=payload),
        ):
            result = await get_config_sources(request)

        assert result["enforced_fields"] == ["ai.model"]


# ---------------------------------------------------------------------------
# _persist_config
# ---------------------------------------------------------------------------


class TestPersistConfig:
    def test_nonexistent_path_is_noop(self) -> None:
        config = MagicMock()
        with patch("anteroom.config._get_config_path", return_value=Path("/nonexistent/config.yaml")):
            _persist_config(config)

    def test_yaml_round_trip(self, tmp_path: Path) -> None:
        config_path = tmp_path / "config.yaml"
        config_path.write_text("ai:\n  model: gpt-3.5\n")

        config = MagicMock()
        config.ai.model = "gpt-4"
        config.ai.user_system_prompt = "Be helpful"

        with patch("anteroom.config._get_config_path", return_value=config_path):
            _persist_config(config)

        import yaml

        with open(config_path) as f:
            data = yaml.safe_load(f)
        assert data["ai"]["model"] == "gpt-4"
        assert data["ai"]["system_prompt"] == "Be helpful"

    def test_removes_system_prompt_when_empty(self, tmp_path: Path) -> None:
        config_path = tmp_path / "config.yaml"
        config_path.write_text("ai:\n  model: gpt-4\n  system_prompt: old\n")

        config = MagicMock()
        config.ai.model = "gpt-4"
        config.ai.user_system_prompt = ""

        with patch("anteroom.config._get_config_path", return_value=config_path):
            _persist_config(config)

        import yaml

        with open(config_path) as f:
            data = yaml.safe_load(f)
        assert "system_prompt" not in data["ai"]
