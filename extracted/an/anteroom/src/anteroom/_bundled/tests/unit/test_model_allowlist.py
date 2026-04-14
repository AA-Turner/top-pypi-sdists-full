"""Tests for model allowlist feature (#1381)."""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import AIConfig, load_config

# ---------------------------------------------------------------------------
# Config parsing tests
# ---------------------------------------------------------------------------


def _make_ai_config(**overrides: Any) -> AIConfig:
    defaults = {
        "base_url": "http://localhost:1234/v1",
        "api_key": "test-key",
        "model": "gpt-4o",
    }
    defaults.update(overrides)
    return AIConfig(**defaults)


class TestAllowedModelsConfigParsing:
    def test_default_is_empty_list(self) -> None:
        cfg = _make_ai_config()
        assert cfg.allowed_models == []

    def test_allowed_models_from_yaml(self, tmp_path: Any) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "ai:\n"
            "  base_url: http://localhost:1234/v1\n"
            "  api_key: test-key\n"
            "  allowed_models:\n"
            "    - gpt-4o\n"
            "    - gpt-4o-mini\n"
        )
        cfg, _ = load_config(config_file)
        assert cfg.ai.allowed_models == ["gpt-4o", "gpt-4o-mini"]

    def test_allowed_models_from_env_var(self, tmp_path: Any) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text("ai:\n  base_url: http://localhost:1234/v1\n  api_key: test-key\n")
        with patch.dict(os.environ, {"AI_CHAT_ALLOWED_MODELS": "gpt-4o,o3,gpt-4o-mini"}):
            cfg, _ = load_config(config_file)
        assert cfg.ai.allowed_models == ["gpt-4o", "o3", "gpt-4o-mini"]

    def test_env_var_overrides_yaml(self, tmp_path: Any) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "ai:\n  base_url: http://localhost:1234/v1\n  api_key: test-key\n  allowed_models:\n    - model-a\n"
        )
        with patch.dict(os.environ, {"AI_CHAT_ALLOWED_MODELS": "model-b,model-c"}):
            cfg, _ = load_config(config_file)
        assert cfg.ai.allowed_models == ["model-b", "model-c"]

    def test_empty_allowed_models_means_show_all(self) -> None:
        cfg = _make_ai_config(allowed_models=[])
        assert cfg.allowed_models == []


# ---------------------------------------------------------------------------
# AI Service list_models tests
# ---------------------------------------------------------------------------


class TestAIServiceListModels:
    @pytest.fixture()
    def ai_config(self) -> AIConfig:
        return _make_ai_config()

    async def test_list_models_returns_sorted_ids(self, ai_config: AIConfig) -> None:
        from anteroom.services.ai_service import AIService

        with patch.object(AIService, "_validate_egress"), patch.object(AIService, "_build_client"):
            svc = AIService(ai_config)

        mock_model_a = MagicMock()
        mock_model_a.id = "zeta-model"
        mock_model_b = MagicMock()
        mock_model_b.id = "alpha-model"
        mock_models = MagicMock()
        mock_models.data = [mock_model_a, mock_model_b]
        svc.client = MagicMock()
        svc.client.models.list = AsyncMock(return_value=mock_models)

        result = await svc.list_models()
        assert result == ["alpha-model", "zeta-model"]

    async def test_list_models_filters_by_allowlist(self, ai_config: AIConfig) -> None:
        from anteroom.services.ai_service import AIService

        ai_config = _make_ai_config(allowed_models=["gpt-4o"])
        with patch.object(AIService, "_validate_egress"), patch.object(AIService, "_build_client"):
            svc = AIService(ai_config)

        mock_a = MagicMock()
        mock_a.id = "gpt-4o"
        mock_b = MagicMock()
        mock_b.id = "gpt-3.5-turbo"
        mock_models = MagicMock()
        mock_models.data = [mock_a, mock_b]
        svc.client = MagicMock()
        svc.client.models.list = AsyncMock(return_value=mock_models)

        result = await svc.list_models()
        assert result == ["gpt-4o"]

    async def test_list_models_returns_all_when_no_allowlist(self, ai_config: AIConfig) -> None:
        from anteroom.services.ai_service import AIService

        with patch.object(AIService, "_validate_egress"), patch.object(AIService, "_build_client"):
            svc = AIService(ai_config)

        mock_a = MagicMock()
        mock_a.id = "model-a"
        mock_b = MagicMock()
        mock_b.id = "model-b"
        mock_models = MagicMock()
        mock_models.data = [mock_a, mock_b]
        svc.client = MagicMock()
        svc.client.models.list = AsyncMock(return_value=mock_models)

        result = await svc.list_models()
        assert result == ["model-a", "model-b"]

    async def test_list_models_caches_result(self, ai_config: AIConfig) -> None:
        from anteroom.services.ai_service import AIService

        with patch.object(AIService, "_validate_egress"), patch.object(AIService, "_build_client"):
            svc = AIService(ai_config)

        mock_a = MagicMock()
        mock_a.id = "model-x"
        mock_models = MagicMock()
        mock_models.data = [mock_a]
        svc.client = MagicMock()
        svc.client.models.list = AsyncMock(return_value=mock_models)

        result1 = await svc.list_models()
        result2 = await svc.list_models()
        assert result1 == result2
        svc.client.models.list.assert_awaited_once()

    async def test_list_models_fallback_on_error(self, ai_config: AIConfig) -> None:
        from anteroom.services.ai_service import AIService

        with patch.object(AIService, "_validate_egress"), patch.object(AIService, "_build_client"):
            svc = AIService(ai_config)

        svc.client = MagicMock()
        svc.client.models.list = AsyncMock(side_effect=Exception("API error"))

        result = await svc.list_models()
        assert result == ["gpt-4o"]

    async def test_list_models_fallback_when_allowlist_filters_all(self) -> None:
        """When the provider lists no matching models, return the allowlist
        itself — never a model outside the configured set."""
        from anteroom.services.ai_service import AIService

        cfg = _make_ai_config(allowed_models=["nonexistent-model"])
        with patch.object(AIService, "_validate_egress"), patch.object(AIService, "_build_client"):
            svc = AIService(cfg)

        mock_a = MagicMock()
        mock_a.id = "real-model"
        mock_models = MagicMock()
        mock_models.data = [mock_a]
        svc.client = MagicMock()
        svc.client.models.list = AsyncMock(return_value=mock_models)

        result = await svc.list_models()
        assert result == ["nonexistent-model"]


# ---------------------------------------------------------------------------
# Commands.py tests
# ---------------------------------------------------------------------------


class TestModelCommand:
    def _make_context(self, current_model: str = "gpt-4o") -> Any:
        from anteroom.cli.commands import CommandContext

        return CommandContext(
            current_model=current_model,
            working_dir="/tmp",
        )

    def test_model_list_subcommand(self) -> None:
        from anteroom.cli.commands import execute_slash_command

        ctx = self._make_context()
        result = execute_slash_command("/model list", ctx)
        assert result.kind == "list_models"

    def test_model_no_arg_shows_current(self) -> None:
        from anteroom.cli.commands import execute_slash_command

        ctx = self._make_context()
        result = execute_slash_command("/model", ctx)
        assert result.kind == "show_model"
        assert result.model_name == "gpt-4o"

    def test_model_with_name_sets_model(self) -> None:
        from anteroom.cli.commands import execute_slash_command

        ctx = self._make_context()
        result = execute_slash_command("/model o3", ctx)
        assert result.kind == "set_model"
        assert result.model_name == "o3"


# ---------------------------------------------------------------------------
# Conversations PATCH allowlist enforcement tests
# ---------------------------------------------------------------------------


class TestConversationsPatchAllowlist:
    async def test_patch_model_allowed_succeeds(self) -> None:
        from unittest.mock import patch as mock_patch

        from anteroom.routers.conversations import update_conversation

        config = MagicMock()
        config.ai.allowed_models = ["gpt-4o", "o3"]

        request = MagicMock()
        request.app.state.config = config

        body = MagicMock()
        body.title = None
        body.slug = None
        body.type = None
        body.model = "gpt-4o"
        body.folder_id = None

        conv = {"id": "test-id", "model": "gpt-4o"}
        with (
            mock_patch("anteroom.routers.conversations._get_db"),
            mock_patch("anteroom.routers.conversations.storage") as mock_storage,
            mock_patch("anteroom.routers.conversations._validate_uuid_or_slug"),
        ):
            mock_storage.get_conversation.return_value = conv
            mock_storage.update_conversation_model.return_value = conv
            result = await update_conversation("test-id", body, request)
        assert result is not None

    async def test_patch_model_blocked_returns_422(self) -> None:
        from fastapi import HTTPException

        from anteroom.routers.conversations import update_conversation

        config = MagicMock()
        config.ai.allowed_models = ["gpt-4o"]

        request = MagicMock()
        request.app.state.config = config

        body = MagicMock()
        body.title = None
        body.slug = None
        body.type = None
        body.model = "disallowed-model"
        body.folder_id = None

        conv = {"id": "test-id"}
        with (
            patch("anteroom.routers.conversations._get_db"),
            patch("anteroom.routers.conversations.storage") as mock_storage,
            patch("anteroom.routers.conversations._validate_uuid_or_slug"),
        ):
            mock_storage.get_conversation.return_value = conv
            with pytest.raises(HTTPException) as exc_info:
                await update_conversation("test-id", body, request)
            assert exc_info.value.status_code == 422

    async def test_patch_model_no_allowlist_allows_any(self) -> None:
        from anteroom.routers.conversations import update_conversation

        config = MagicMock()
        config.ai.allowed_models = []

        request = MagicMock()
        request.app.state.config = config

        body = MagicMock()
        body.title = None
        body.slug = None
        body.type = None
        body.model = "any-model"
        body.folder_id = None

        conv = {"id": "test-id", "model": "any-model"}
        with (
            patch("anteroom.routers.conversations._get_db"),
            patch("anteroom.routers.conversations.storage") as mock_storage,
            patch("anteroom.routers.conversations._validate_uuid_or_slug"),
        ):
            mock_storage.get_conversation.return_value = conv
            mock_storage.update_conversation_model.return_value = conv
            result = await update_conversation("test-id", body, request)
        assert result is not None

    async def test_patch_model_empty_string_clears_override(self) -> None:
        from anteroom.routers.conversations import update_conversation

        config = MagicMock()
        config.ai.allowed_models = ["gpt-4o"]

        request = MagicMock()
        request.app.state.config = config

        body = MagicMock()
        body.title = None
        body.slug = None
        body.type = None
        body.model = ""
        body.folder_id = None

        conv = {"id": "test-id", "model": ""}
        with (
            patch("anteroom.routers.conversations._get_db"),
            patch("anteroom.routers.conversations.storage") as mock_storage,
            patch("anteroom.routers.conversations._validate_uuid_or_slug"),
        ):
            mock_storage.get_conversation.return_value = conv
            mock_storage.update_conversation_model.return_value = conv
            result = await update_conversation("test-id", body, request)
        assert result is not None


# ---------------------------------------------------------------------------
# Chat runtime guard tests
# ---------------------------------------------------------------------------


class TestChatRuntimeGuard:
    def test_model_override_rejected_when_not_in_allowlist(self) -> None:
        """Verify the guard logic: model not in allowlist => override cleared."""
        allowed = ["gpt-4o", "o3"]
        model_override: str | None = "disallowed-model"

        if model_override and allowed and model_override not in allowed:
            model_override = None

        assert model_override is None

    def test_model_override_allowed_when_in_allowlist(self) -> None:
        allowed = ["gpt-4o", "o3"]
        model_override: str | None = "gpt-4o"

        if model_override and allowed and model_override not in allowed:
            model_override = None

        assert model_override == "gpt-4o"

    def test_model_override_allowed_when_no_allowlist(self) -> None:
        allowed: list[str] = []
        model_override: str | None = "any-model"

        if model_override and allowed and model_override not in allowed:
            model_override = None

        assert model_override == "any-model"


# ---------------------------------------------------------------------------
# Anthropic / LiteLLM provider list_models tests
# ---------------------------------------------------------------------------


class TestAnthropicListModels:
    async def test_returns_allowed_models_when_configured(self) -> None:
        from anteroom.services.anthropic_provider import AnthropicService

        cfg = _make_ai_config(provider="anthropic", allowed_models=["claude-sonnet-4-20250514", "claude-3-opus"])
        with patch.object(AnthropicService, "__init__", lambda self, *a, **kw: None):
            svc = AnthropicService.__new__(AnthropicService)
            svc.config = cfg
            svc._cached_models = None

        result = await svc.list_models()
        assert result == ["claude-3-opus", "claude-sonnet-4-20250514"]

    async def test_returns_current_model_when_no_allowlist(self) -> None:
        from anteroom.services.anthropic_provider import AnthropicService

        cfg = _make_ai_config(provider="anthropic", model="claude-sonnet-4-20250514")
        with patch.object(AnthropicService, "__init__", lambda self, *a, **kw: None):
            svc = AnthropicService.__new__(AnthropicService)
            svc.config = cfg
            svc._cached_models = None

        result = await svc.list_models()
        assert result == ["claude-sonnet-4-20250514"]


class TestLiteLLMListModels:
    async def test_returns_allowed_models_when_configured(self) -> None:
        from anteroom.services.litellm_provider import LiteLLMService

        cfg = _make_ai_config(provider="litellm", allowed_models=["openrouter/gpt-4o", "openrouter/o3"])
        with patch.object(LiteLLMService, "__init__", lambda self, *a, **kw: None):
            svc = LiteLLMService.__new__(LiteLLMService)
            svc.config = cfg
            svc._cached_models = None

        result = await svc.list_models()
        assert result == ["openrouter/gpt-4o", "openrouter/o3"]

    async def test_returns_current_model_when_no_allowlist(self) -> None:
        from anteroom.services.litellm_provider import LiteLLMService

        cfg = _make_ai_config(provider="litellm", model="openrouter/gpt-4o")
        with patch.object(LiteLLMService, "__init__", lambda self, *a, **kw: None):
            svc = LiteLLMService.__new__(LiteLLMService)
            svc.config = cfg
            svc._cached_models = None

        result = await svc.list_models()
        assert result == ["openrouter/gpt-4o"]
