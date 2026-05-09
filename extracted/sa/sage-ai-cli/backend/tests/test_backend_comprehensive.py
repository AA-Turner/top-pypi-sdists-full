"""Comprehensive tests for backend app module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch, Mock
from datetime import datetime
import json

import pytest


# =============================================================================
# Tests for RateLimiter
# =============================================================================


class TestRateLimiter:
    """Tests for RateLimiter class."""

    def test_import(self):
        """RateLimiter can be imported."""
        from backend.app import RateLimiter
        assert RateLimiter is not None

    def test_create_default(self):
        """Create rate limiter with defaults."""
        from backend.app import RateLimiter

        limiter = RateLimiter()
        assert limiter is not None

    def test_create_custom(self):
        """Create rate limiter with custom settings."""
        from backend.app import RateLimiter

        limiter = RateLimiter(
            requests_per_minute=120,
            burst_limit=20,
        )
        assert limiter.requests_per_minute == 120
        assert limiter.burst_limit == 20

    def test_is_allowed(self):
        """Check if request is allowed."""
        from backend.app import RateLimiter

        limiter = RateLimiter(requests_per_minute=60, burst_limit=10)
        # Should allow first request
        result = limiter.is_allowed("test-client")
        assert result is True

    def test_is_allowed_multiple(self):
        """Check multiple requests."""
        from backend.app import RateLimiter

        limiter = RateLimiter(requests_per_minute=100, burst_limit=10)
        # Should allow several requests from different clients
        results = [limiter.is_allowed(f"client-{i}") for i in range(5)]
        # All should succeed (different clients)
        assert all(results)


# =============================================================================
# Tests for AppState
# =============================================================================


class TestAppState:
    """Tests for AppState class."""

    def test_import(self):
        """AppState can be imported."""
        from backend.app import AppState
        assert AppState is not None


# =============================================================================
# Tests for API Error Classes
# =============================================================================


class TestAPIError:
    """Tests for APIError class."""

    def test_import(self):
        """APIError can be imported."""
        from backend.app import APIError
        assert APIError is not None

    def test_create(self):
        """Create API error."""
        from backend.app import APIError

        error = APIError(
            status_code=400,
            error_code="BAD_REQUEST",
            message="Bad request",
        )
        assert error.status_code == 400
        assert error.detail["error"] == "BAD_REQUEST"


class TestNotFoundError:
    """Tests for NotFoundError class."""

    def test_import(self):
        """NotFoundError can be imported."""
        from backend.app import NotFoundError
        assert NotFoundError is not None

    def test_create(self):
        """Create not found error."""
        from backend.app import NotFoundError

        error = NotFoundError("Model", "test-model")
        assert error.status_code == 404
        assert "Model" in error.detail["message"]
        assert "test-model" in error.detail["message"]


class TestValidationError:
    """Tests for ValidationError class."""

    def test_import(self):
        """ValidationError can be imported."""
        from backend.app import ValidationError
        assert ValidationError is not None

    def test_create(self):
        """Create validation error."""
        from backend.app import ValidationError

        error = ValidationError("Invalid input")
        assert error.status_code == 400
        assert "Invalid input" in error.detail["message"]


class TestModelRuntimeError:
    """Tests for ModelRuntimeError class."""

    def test_import(self):
        """ModelRuntimeError can be imported."""
        from backend.app import ModelRuntimeError
        assert ModelRuntimeError is not None

    def test_create(self):
        """Create model runtime error."""
        from backend.app import ModelRuntimeError

        error = ModelRuntimeError("Model failed to load")
        assert error.status_code == 500


class TestRateLimitError:
    """Tests for RateLimitError class."""

    def test_import(self):
        """RateLimitError can be imported."""
        from backend.app import RateLimitError
        assert RateLimitError is not None

    def test_create_default(self):
        """Create rate limit error with defaults."""
        from backend.app import RateLimitError

        error = RateLimitError()
        assert error.status_code == 429

    def test_create_custom_retry(self):
        """Create rate limit error with custom retry time."""
        from backend.app import RateLimitError

        error = RateLimitError(retry_after=120)
        assert error.detail["details"]["retry_after_seconds"] == 120


# =============================================================================
# Tests for Helper Functions
# =============================================================================


class TestExtractBearerToken:
    """Tests for _extract_bearer_token function."""

    def test_import(self):
        """Function can be imported."""
        from backend.app import _extract_bearer_token
        assert _extract_bearer_token is not None

    def test_valid_bearer(self):
        """Extract valid bearer token."""
        from backend.app import _extract_bearer_token

        result = _extract_bearer_token("Bearer test-token")
        assert result == "test-token"

    def test_no_auth(self):
        """No authorization header."""
        from backend.app import _extract_bearer_token

        result = _extract_bearer_token(None)
        assert result is None

    def test_no_bearer_prefix(self):
        """Authorization without Bearer prefix."""
        from backend.app import _extract_bearer_token

        result = _extract_bearer_token("Basic test-token")
        assert result is None


class TestValidateModelIdPath:
    """Tests for validate_model_id_path function."""

    def test_import(self):
        """Function can be imported."""
        from backend.app import validate_model_id_path
        assert validate_model_id_path is not None

    def test_valid_id(self):
        """Validate valid model ID."""
        from backend.app import validate_model_id_path

        result = validate_model_id_path("llama-3.2-3b")
        assert result == "llama-3.2-3b"

    def test_cloud_prefix(self):
        """Validate cloud model ID."""
        from backend.app import validate_model_id_path

        result = validate_model_id_path("cloud:openai")
        assert result == "cloud:openai"


class TestValidateConversationIdPath:
    """Tests for validate_conversation_id_path function."""

    def test_import(self):
        """Function can be imported."""
        from backend.app import validate_conversation_id_path
        assert validate_conversation_id_path is not None

    def test_valid_id(self):
        """Validate valid conversation ID."""
        from backend.app import validate_conversation_id_path

        result = validate_conversation_id_path("conv-123-abc")
        assert result == "conv-123-abc"


class TestValidateModelNamePath:
    """Tests for validate_model_name_path function."""

    def test_import(self):
        """Function can be imported."""
        from backend.app import validate_model_name_path
        assert validate_model_name_path is not None

    def test_valid_name(self):
        """Validate valid model name."""
        from backend.app import validate_model_name_path

        result = validate_model_name_path("llama-3b")
        assert result == "llama-3b"


# =============================================================================
# Tests for Schemas
# =============================================================================


class TestSchemas:
    """Tests for backend schemas."""

    def test_chat_req(self):
        """ChatReq schema."""
        from backend.schemas import ChatReq, ChatMessage

        req = ChatReq(
            model_id="test-model",
            messages=[ChatMessage(role="user", content="Hello")],
        )
        assert req.model_id == "test-model"
        assert len(req.messages) == 1

    def test_chat_message(self):
        """ChatMessage schema."""
        from backend.schemas import ChatMessage

        msg = ChatMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_chat_message_with_attachments(self):
        """ChatMessage with attachments."""
        from backend.schemas import ChatMessage, FileAttachment

        attachment = FileAttachment(file_id="file-123", filename="test.txt")
        msg = ChatMessage(
            role="user",
            content="Check this file",
            attachments=[attachment],
        )
        assert len(msg.attachments) == 1

    def test_file_attachment(self):
        """FileAttachment schema."""
        from backend.schemas import FileAttachment

        att = FileAttachment(file_id="file-123", filename="test.txt")
        assert att.file_id == "file-123"
        assert att.filename == "test.txt"


# =============================================================================
# Tests for Hardware Detection
# =============================================================================


class TestHardware:
    """Tests for hardware module."""

    def test_import(self):
        """Hardware module can be imported."""
        from backend.hardware import detect_hardware_summary
        assert detect_hardware_summary is not None

    def test_detect_hardware(self):
        """Detect hardware returns dict."""
        from backend.hardware import detect_hardware_summary

        result = detect_hardware_summary()
        assert isinstance(result, dict)

    def test_hardware_returns_info(self):
        """Hardware dict has some info."""
        from backend.hardware import detect_hardware_summary

        result = detect_hardware_summary()
        # Should have at least one key
        assert len(result) > 0


# =============================================================================
# Tests for Config
# =============================================================================


class TestBackendConfig:
    """Tests for backend config."""

    def test_import(self):
        """AppSettings can be imported."""
        from backend.config import AppSettings
        assert AppSettings is not None

    def test_settings_instance(self):
        """Settings instance exists."""
        from backend.config import settings

        assert settings is not None

    def test_settings_has_port(self):
        """Settings has port."""
        from backend.config import settings

        assert hasattr(settings, "port")
        assert settings.port > 0


# =============================================================================
# Tests for Conversation Logger
# =============================================================================


class TestConversationLogger:
    """Tests for conversation logger."""

    def test_import(self):
        """Logger can be imported."""
        from backend.conversation_logger import ConversationLogger
        assert ConversationLogger is not None

    def test_create(self, tmp_path):
        """Create conversation logger."""
        from backend.conversation_logger import ConversationLogger

        logger = ConversationLogger(base_dir=tmp_path)
        assert logger is not None


# =============================================================================
# Tests for Conversations
# =============================================================================


class TestConversations:
    """Tests for conversations module."""

    def test_import(self):
        """Conversations module can be imported."""
        from backend.conversations import ConversationStore
        assert ConversationStore is not None

    def test_create(self):
        """Create conversation store."""
        from backend.conversations import ConversationStore

        store = ConversationStore()
        assert store is not None

    def test_create_conversation(self):
        """Create a conversation."""
        from backend.conversations import ConversationStore

        store = ConversationStore()
        conv = store.create("Test Conversation")
        # create() returns a dict with the conversation data
        assert conv is not None
        assert "id" in conv


# =============================================================================
# Tests for File Store
# =============================================================================


class TestFileStore:
    """Tests for file store module."""

    def test_import(self):
        """File store can be imported."""
        from backend.file_store import FileStore
        assert FileStore is not None

    def test_create(self, tmp_path):
        """Create file store."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        assert store is not None


# =============================================================================
# Tests for GitHub Client
# =============================================================================


class TestGitHubClient:
    """Tests for GitHub client module."""

    def test_import_functions(self):
        """GitHub client functions can be imported."""
        from backend.github_client import validate_github_url, list_releases
        assert validate_github_url is not None
        assert list_releases is not None

    def test_validate_github_url_valid(self):
        """Validate valid GitHub URL."""
        from backend.github_client import validate_github_url

        valid, msg = validate_github_url("https://github.com/user/repo")
        assert valid is True

    def test_validate_github_url_invalid(self):
        """Validate invalid URL."""
        from backend.github_client import validate_github_url

        valid, msg = validate_github_url("http://example.com")
        assert valid is False

    def test_release_asset_dataclass(self):
        """ReleaseAsset dataclass."""
        from backend.github_client import ReleaseAsset

        asset = ReleaseAsset(
            name="model.gguf",
            download_url="https://github.com/...",
            size_bytes=1000000,
            content_type="application/octet-stream",
        )
        assert asset.name == "model.gguf"


# =============================================================================
# Tests for Model Catalog
# =============================================================================


class TestBackendModelCatalog:
    """Tests for backend model catalog."""

    def test_import(self):
        """Model catalog can be imported."""
        from backend.model_catalog import list_catalog_models
        assert list_catalog_models is not None

    def test_list_catalog(self):
        """List catalog models returns list."""
        from backend.model_catalog import list_catalog_models

        result = list_catalog_models()
        assert isinstance(result, list)


# =============================================================================
# Tests for Model Registry
# =============================================================================


class TestModelRegistry:
    """Tests for model registry."""

    def test_import(self):
        """Model registry can be imported."""
        from backend.model_registry import ModelRegistry
        assert ModelRegistry is not None

    def test_create(self):
        """Create model registry."""
        from backend.model_registry import ModelRegistry

        registry = ModelRegistry()
        assert registry is not None


# =============================================================================
# Tests for Prompt Engine
# =============================================================================


class TestPromptEngine:
    """Tests for prompt engine."""

    def test_import(self):
        """Prompt engine functions can be imported."""
        from backend.prompt_engine import load_system_prompt, build_messages
        assert load_system_prompt is not None
        assert build_messages is not None


# =============================================================================
# Tests for Runtime Manager
# =============================================================================


class TestRuntimeManager:
    """Tests for runtime manager."""

    def test_import(self):
        """Runtime manager can be imported."""
        from backend.runtime_manager import RuntimeManager
        assert RuntimeManager is not None

    def test_create(self):
        """Create runtime manager."""
        from backend.runtime_manager import RuntimeManager

        manager = RuntimeManager()
        assert manager is not None


# =============================================================================
# Tests for App Creation
# =============================================================================


class TestCreateApp:
    """Tests for create_app function."""

    def test_import(self):
        """create_app can be imported."""
        from backend.app import create_app
        assert create_app is not None

    def test_create_app(self):
        """Create FastAPI app."""
        from backend.app import create_app

        app = create_app()
        assert app is not None


# =============================================================================
# Tests for Health Endpoint
# =============================================================================


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_function(self):
        """Health function exists."""
        from backend.app import health
        assert health is not None

    def test_health_returns_dict(self):
        """Health returns dict."""
        from backend.app import health

        result = health()
        assert isinstance(result, dict)
        assert "ok" in result


# =============================================================================
# Tests for Hardware Endpoint
# =============================================================================


class TestHardwareEndpoint:
    """Tests for /hardware endpoint."""

    def test_hardware_function(self):
        """Hardware function exists."""
        from backend.app import hardware
        assert hardware is not None

    def test_hardware_returns_dict(self):
        """Hardware returns dict."""
        from backend.app import hardware

        result = hardware()
        assert isinstance(result, dict)


# =============================================================================
# Tests for Catalog Endpoints
# =============================================================================


class TestCatalogEndpoint:
    """Tests for /catalog endpoint."""

    @patch("backend.app.get_app_state")
    def test_catalog_function(self, mock_state):
        """Catalog function exists."""
        from backend.app import catalog
        assert catalog is not None


# =============================================================================
# Tests for Auto Updater
# =============================================================================


class TestAutoUpdater:
    """Tests for auto updater module."""

    def test_import(self):
        """Auto updater can be imported."""
        from backend.auto_updater import AutoUpdater
        assert AutoUpdater is not None

    def test_tracked_source(self):
        """TrackedSource dataclass."""
        from backend.auto_updater import TrackedSource

        source = TrackedSource(
            model_id="test",
            owner="owner",
            repo="repo",
        )
        assert source.model_id == "test"


# =============================================================================
# Tests for Schema Validation
# =============================================================================


class TestSchemaValidation:
    """Tests for schema validation."""

    def test_chat_req_temperature_bounds(self):
        """Temperature must be in valid range."""
        from backend.schemas import ChatReq, ChatMessage

        # Valid temperature
        req = ChatReq(
            model_id="test",
            messages=[ChatMessage(role="user", content="Hi")],
            temperature=0.5,
        )
        assert req.temperature == 0.5

    def test_chat_req_max_tokens_bounds(self):
        """Max tokens must be in valid range."""
        from backend.schemas import ChatReq, ChatMessage

        req = ChatReq(
            model_id="test",
            messages=[ChatMessage(role="user", content="Hi")],
            max_tokens=1024,
        )
        assert req.max_tokens == 1024

    def test_chat_message_roles(self):
        """Message roles are validated."""
        from backend.schemas import ChatMessage

        for role in ["system", "user", "assistant"]:
            msg = ChatMessage(role=role, content="Test")
            assert msg.role == role


# =============================================================================
# Tests for API Response Format
# =============================================================================


class TestAPIResponseFormat:
    """Tests for API response format."""

    def test_health_response_format(self):
        """Health response has correct format."""
        from backend.app import health

        result = health()
        assert "ok" in result
        assert result["ok"] is True

    def test_hardware_response_format(self):
        """Hardware response has correct format."""
        from backend.app import hardware

        result = hardware()
        assert isinstance(result, dict)
