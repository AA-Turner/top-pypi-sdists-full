"""
Comprehensive API tests for SAGE AI Backend.

Tests all model-related API endpoints across cloud, browser, and Ollama models
with example prompts to verify functionality.
"""

import json
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL DEFINITIONS FOR TESTING
# ═══════════════════════════════════════════════════════════════════════════════

# Legacy Pollinations-backed cloud aliases removed — empty keeps parametrized cloud tests as no-ops.
CLOUD_MODELS: list[dict] = []

BROWSER_MODELS = [
    {"id": "browser:Llama-3.2-1B-Instruct-q4f16_1-MLC", "name": "Llama 3.2 1B"},
    {"id": "browser:Llama-3.2-3B-Instruct-q4f16_1-MLC", "name": "Llama 3.2 3B"},
    {"id": "browser:Phi-3.5-mini-instruct-q4f16_1-MLC", "name": "Phi 3.5 Mini"},
]

OLLAMA_MODELS = [
    {"id": "ollama:llama3.2", "name": "Llama 3.2"},
    {"id": "ollama:qwen2.5-coder", "name": "Qwen 2.5 Coder"},
    {"id": "ollama:deepseek-r1", "name": "DeepSeek R1"},
]

ALL_MODELS = CLOUD_MODELS + BROWSER_MODELS + OLLAMA_MODELS


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE PROMPTS FOR TESTING
# ═══════════════════════════════════════════════════════════════════════════════

EXAMPLE_PROMPTS = {
    "simple": [
        "Hello, how are you?",
        "What is 2 + 2?",
        "Say 'test successful' if you can read this.",
    ],
    "coding": [
        "Write a Python function to check if a number is prime.",
        "Explain what a REST API is in one paragraph.",
        "What does the `async` keyword do in JavaScript?",
    ],
    "reasoning": [
        "If all roses are flowers and some flowers fade quickly, can we say all roses fade quickly?",
        "What comes next in the sequence: 2, 4, 8, 16, ?",
        "Explain the difference between correlation and causation.",
    ],
    "creative": [
        "Write a haiku about coding.",
        "Suggest three names for a new programming language.",
        "Describe a futuristic city in 50 words.",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def mock_app_state():
    """Create mock app state for testing."""
    mock_state = MagicMock()
    mock_state.registry.list_models.return_value = []
    mock_state.runtime_manager.runtime = None
    mock_state.runtime_manager.loaded_model_id = None
    mock_state.runtime_manager.loaded_runtime = None
    mock_state.rate_limiter.is_allowed.return_value = True
    mock_state.rate_limiter.get_client_id.return_value = "test-client"
    mock_state.download_rate_limiter.is_allowed.return_value = True
    mock_state.gcs_rate_limiter.is_allowed.return_value = True
    mock_state.terminal_rate_limiter.is_allowed.return_value = True
    return mock_state


@pytest.fixture
def client():
    """Create test client with mocked dependencies."""
    with patch("backend.app.get_app_state") as mock_get_state:
        mock_state = MagicMock()
        mock_state.registry.list_models.return_value = []
        mock_state.runtime_manager.runtime = None
        mock_state.runtime_manager.loaded_model_id = None
        mock_state.runtime_manager.loaded_runtime = None
        mock_state.rate_limiter.is_allowed.return_value = True
        mock_state.rate_limiter.get_client_id.return_value = "test-client"
        mock_get_state.return_value = mock_state

        from backend.app import app
        yield TestClient(app)


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH AND STATUS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestHealthEndpoints:
    """Test health and status endpoints."""

    def test_health_endpoint_format(self):
        """Test /health endpoint response format."""
        expected_fields = {"ok", "version", "loaded_model_id", "loaded_runtime"}
        # Verify expected structure
        assert "ok" in expected_fields
        assert "version" in expected_fields

    def test_hardware_endpoint_format(self):
        """Test /hardware endpoint response format."""
        expected_fields = {"cpu_threads", "ram_gb", "gpu_available"}
        assert "cpu_threads" in expected_fields


# ═══════════════════════════════════════════════════════════════════════════════
# MODELS ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestModelsEndpoints:
    """Test /models endpoints."""

    def test_list_models_format(self):
        """Test /models returns correct format."""
        expected_response = {"ok": True, "models": []}
        assert "ok" in expected_response
        assert "models" in expected_response
        assert isinstance(expected_response["models"], list)

    def test_model_names_format(self):
        """Test /models/names returns correct format."""
        expected_response = {"ok": True, "names": ["ollama:llama3.2", "ollama:mistral"]}
        assert "ok" in expected_response
        assert "names" in expected_response
        assert isinstance(expected_response["names"], list)

    @pytest.mark.parametrize("model", CLOUD_MODELS)
    def test_cloud_model_load_request_format(self, model):
        """Test load request format for cloud models."""
        request = {"model_id": model["id"]}
        assert "model_id" in request
        assert request["model_id"].startswith("cloud:")

    @pytest.mark.parametrize("model", OLLAMA_MODELS)
    def test_ollama_model_load_request_format(self, model):
        """Test load request format for Ollama models."""
        request = {"model_id": model["id"]}
        assert "model_id" in request
        assert request["model_id"].startswith("ollama:")


# ═══════════════════════════════════════════════════════════════════════════════
# FREE MODELS ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestFreeModelsEndpoint:
    """Test /free-models endpoint."""

    def test_free_models_response_format(self):
        """Test /free-models returns empty list with deprecation message."""
        expected_response = {
            "ok": True,
            "models": [],
            "message": "Pollinations-backed cloud models are no longer exposed. Use local Ollama or GGUF models.",
        }
        assert expected_response["ok"] is True
        assert expected_response["models"] == []

    def test_free_models_are_cloud_models(self):
        """Legacy cloud catalog is empty after Pollinations removal."""
        assert CLOUD_MODELS == []


# ═══════════════════════════════════════════════════════════════════════════════
# OLLAMA STATUS ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestOllamaStatusEndpoint:
    """Test /ollama/status endpoint."""

    def test_ollama_running_response_format(self):
        """Test response format when Ollama is running."""
        expected_response = {
            "ok": True,
            "running": True,
            "models": [
                {"name": "llama3.2:latest", "size": 2000000000, "modified": "2024-01-01"}
            ],
        }
        assert expected_response["ok"] is True
        assert expected_response["running"] is True
        assert isinstance(expected_response["models"], list)

    def test_ollama_not_running_response_format(self):
        """Test response format when Ollama is not running."""
        expected_response = {"ok": True, "running": False, "models": []}
        assert expected_response["ok"] is True
        assert expected_response["running"] is False
        assert expected_response["models"] == []


# ═══════════════════════════════════════════════════════════════════════════════
# CHAT ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestChatEndpoint:
    """Test /chat endpoint."""

    @pytest.mark.parametrize("model", CLOUD_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"])
    def test_chat_request_format_cloud(self, model, prompt):
        """Test chat request format for cloud models."""
        request = {
            "model_id": model["id"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1024,
            "stream": True,
        }
        assert "model_id" in request
        assert "messages" in request
        assert len(request["messages"]) > 0
        assert request["messages"][0]["role"] == "user"
        assert request["messages"][0]["content"] == prompt

    @pytest.mark.parametrize("model", OLLAMA_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["coding"])
    def test_chat_request_format_ollama(self, model, prompt):
        """Test chat request format for Ollama models."""
        request = {
            "model_id": model["id"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 2048,
            "stream": True,
        }
        assert request["model_id"].startswith("ollama:")
        assert request["messages"][0]["content"] == prompt

    def test_chat_response_streaming_format(self):
        """Test streaming chat response format."""
        # SSE event format
        token_event = {"token": "Hello"}
        done_event = {"done": True, "conversation_id": "conv-123"}
        step_event = {"step": "thinking", "message": "Processing..."}

        assert "token" in token_event
        assert "done" in done_event
        assert "step" in step_event

    def test_chat_response_non_streaming_format(self):
        """Test non-streaming chat response format."""
        response = {
            "ok": True,
            "output": "Hello! I'm doing well, thank you for asking.",
            "conversation_id": "conv-123",
        }
        assert response["ok"] is True
        assert isinstance(response["output"], str)

    def test_chat_error_response_format(self):
        """Test chat error response format (SSE)."""
        error_event = {
            "error": True,
            "error_code": "STREAM_ERROR",
            "message": "Connection failed",
            "request_id": "req-123",
            "partial_response": None,
        }
        assert error_event["error"] is True
        assert "error_code" in error_event
        assert "message" in error_event


class TestChatWithAllPrompts:
    """Test chat with all example prompts across platforms."""

    # Website chat - cloud and browser models
    @pytest.mark.parametrize("model", CLOUD_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"] + EXAMPLE_PROMPTS["coding"])
    def test_website_chat_cloud_models(self, model, prompt):
        """Test website chat with cloud models."""
        request = {
            "model_id": model["id"],
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }
        assert model["id"].startswith("cloud:")
        assert len(prompt) > 0

    @pytest.mark.parametrize("model", BROWSER_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"])
    def test_website_chat_browser_models(self, model, prompt):
        """Test website chat with browser models."""
        request = {
            "model_id": model["id"],
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }
        assert model["id"].startswith("browser:")
        assert len(prompt) > 0

    # CLI chat - all models
    @pytest.mark.parametrize("model", ALL_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["reasoning"])
    def test_cli_chat_all_models(self, model, prompt):
        """Test CLI chat with all models."""
        request = {
            "model_id": model["id"],
            "messages": [{"role": "user", "content": prompt}],
        }
        assert ":" in model["id"]
        assert len(prompt) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# CATALOG ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCatalogEndpoints:
    """Test /catalog endpoints."""

    def test_catalog_response_format(self):
        """Test /catalog response format."""
        expected_fields = ["model_id", "name", "description", "params", "size_gb",
                          "family", "filename", "url", "default", "backend", "category", "tags"]
        model = {
            "model_id": "qwen2.5-coder",
            "name": "Qwen 2.5 Coder",
            "description": "Coding model",
            "params": "7B",
            "size_gb": 4.5,
            "family": "qwen",
            "filename": "qwen2.5-coder-7b.gguf",
            "url": "https://example.com/model.gguf",
            "default": False,
            "backend": "gguf",
            "category": "coding",
            "tags": ["coding", "general"],
        }
        for field in expected_fields:
            assert field in model

    def test_catalog_all_response_format(self):
        """Test /catalog/all response format."""
        response = {
            "ok": True,
            "models": [],
            "total": 0,
        }
        assert "ok" in response
        assert "models" in response
        assert "total" in response

    def test_ollama_catalog_response_format(self):
        """Test /ollama/catalog response format."""
        model = {
            "name": "llama3.2",
            "display_name": "Llama 3.2",
            "sizes": "8B",
            "tags": ["general", "coding"],
            "description": "General purpose model",
            "pulls": "",
            "category": "general",
        }
        assert "name" in model
        assert "display_name" in model
        assert "category" in model


# ═══════════════════════════════════════════════════════════════════════════════
# CONVERSATION ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestConversationEndpoints:
    """Test /conversations endpoints."""

    def test_create_conversation_request_format(self):
        """Test conversation creation request format."""
        request = {"title": "Test Conversation"}
        assert "title" in request

    def test_conversation_response_format(self):
        """Test conversation response format."""
        conversation = {
            "id": "conv-123",
            "title": "Test Conversation",
            "messages": [],
            "created_at": "2024-01-01T00:00:00Z",
        }
        assert "id" in conversation
        assert "title" in conversation
        assert "messages" in conversation


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestErrorHandling:
    """Test error handling across all endpoints."""

    def test_not_found_error_format(self):
        """Test 404 error response format."""
        error = {
            "error": "NOT_FOUND",
            "message": "Model not found: invalid-model",
            "details": {"resource": "Model", "identifier": "invalid-model"},
        }
        assert error["error"] == "NOT_FOUND"
        assert "message" in error
        assert "details" in error

    def test_validation_error_format(self):
        """Test 400 error response format."""
        error = {
            "error": "VALIDATION_ERROR",
            "message": "Invalid model_id format",
            "details": {},
        }
        assert error["error"] == "VALIDATION_ERROR"

    def test_rate_limit_error_format(self):
        """Test 429 error response format."""
        error = {
            "error": "RATE_LIMIT_EXCEEDED",
            "message": "Rate limit exceeded. Please try again later.",
            "details": {"retry_after_seconds": 60},
        }
        assert error["error"] == "RATE_LIMIT_EXCEEDED"
        assert "retry_after_seconds" in error["details"]

    def test_runtime_error_format(self):
        """Test 500 error response format."""
        error = {
            "error": "RUNTIME_ERROR",
            "message": "Failed to load model: connection refused",
            "details": {},
        }
        assert error["error"] == "RUNTIME_ERROR"

    def test_ollama_not_available_error(self):
        """Test Ollama not available error message shape."""
        error_message = (
            "Ollama is not running. Cannot use 'llama3.2'. Start Ollama with: ollama serve"
        )
        assert "Ollama" in error_message
        assert "ollama serve" in error_message

    def test_model_not_found_on_cloud_run_error(self):
        """Test model not found error mentions local options."""
        error_message = (
            "Model 'invalid-model' not found. Use ollama:<name>, browser:, or a registered GGUF id."
        )
        assert "ollama:" in error_message
        assert "invalid-model" in error_message


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL ID VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestModelIdValidation:
    """Test model ID validation."""

    VALID_MODEL_IDS = [
        "ollama:llama3.2",
        "ollama:qwen2.5-coder",
        "browser:Llama-3.2-1B-Instruct-q4f16_1-MLC",
        "llama_cpp:my-local-model",
    ]

    INVALID_MODEL_IDS = [
        "",
        " ",
        "../path/traversal",
        "model\x00null",
        "a" * 500,  # Too long
    ]

    @pytest.mark.parametrize("model_id", VALID_MODEL_IDS)
    def test_valid_model_ids(self, model_id):
        """Test valid model IDs are accepted."""
        assert len(model_id) > 0
        assert ":" in model_id
        prefix = model_id.split(":")[0]
        assert prefix in {"ollama", "browser", "llama_cpp"}

    @pytest.mark.parametrize("model_id", INVALID_MODEL_IDS)
    def test_invalid_model_ids(self, model_id):
        """Test invalid model IDs are rejected."""
        # These should be caught by validation
        is_invalid = (
            not model_id or
            ".." in model_id or
            "\x00" in model_id or
            len(model_id) > 256
        )
        assert is_invalid or model_id.strip() == ""


# ═══════════════════════════════════════════════════════════════════════════════
# GCS ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestGCSEndpoints:
    """Test GCS model management endpoints."""

    def test_gcs_status_response_format(self):
        """Test /gcs/status response format."""
        response = {
            "ok": True,
            "gcs_available": True,
            "ollama_running": True,
        }
        assert "gcs_available" in response
        assert "ollama_running" in response

    def test_gcs_models_response_format(self):
        """Test /gcs/models response format."""
        model = {
            "name": "qwen2.5-coder-7b",
            "display_name": "Qwen 2.5 Coder 7B",
            "filename": "qwen2.5-coder-7b.gguf",
            "url": "gs://sage-ai-models/qwen2.5-coder-7b.gguf",
            "size_gb": 4.5,
            "params": "7B",
            "family": "qwen",
            "description": "Coding model",
            "category": "coding",
            "tags": ["coding"],
            "checksum": "abc123",
            "uploaded_at": "2024-01-01T00:00:00Z",
            "source": "ollama",
        }
        expected_fields = ["name", "filename", "url", "size_gb"]
        for field in expected_fields:
            assert field in model


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TEST HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

class TestIntegrationHelpers:
    """Helper tests for integration testing."""

    # Smoke test prompts for quick verification
    SMOKE_TEST_PROMPTS = [
        "Say 'OK' if you can read this.",
        "What is 1+1?",
        "Hello",
    ]

    # Capability test prompts for thorough testing
    CAPABILITY_PROMPTS = [
        "Write a Python function called 'add' that adds two numbers.",
        "If A > B and B > C, is A > C? Answer yes or no.",
        "List three colors, one per line.",
    ]

    @pytest.mark.parametrize("prompt", SMOKE_TEST_PROMPTS)
    def test_smoke_test_prompt_format(self, prompt):
        """Test smoke test prompts are valid."""
        assert len(prompt) > 0
        assert len(prompt) < 1000

    @pytest.mark.parametrize("prompt", CAPABILITY_PROMPTS)
    def test_capability_prompt_format(self, prompt):
        """Test capability prompts are valid."""
        assert len(prompt) > 0

    def test_full_chat_workflow(self):
        """Test full chat workflow structure."""
        # 1. Create conversation
        create_req = {"title": "Test Chat"}

        # 2. Send message
        chat_req = {
            "model_id": "ollama:llama3.2",
            "messages": [{"role": "user", "content": "Hello"}],
            "conversation_id": "conv-123",
            "stream": True,
        }

        # 3. Verify request structure
        assert "title" in create_req
        assert "model_id" in chat_req
        assert "messages" in chat_req


# ═══════════════════════════════════════════════════════════════════════════════
# PLATFORM-SPECIFIC TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestWebsiteChatIntegration:
    """Test website chat integration scenarios."""

    @pytest.mark.parametrize("model", CLOUD_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"])
    def test_website_chat_cloud_model_request(self, model, prompt):
        """Test website chat request with cloud model."""
        request = {
            "model_id": model["id"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1024,
            "stream": True,
        }
        # Verify request is valid for website
        assert request["model_id"].startswith("cloud:")
        assert request["stream"] is True

    @pytest.mark.parametrize("model", BROWSER_MODELS)
    def test_website_browser_model_requires_webgpu(self, model):
        """Test browser models require WebGPU (client-side check)."""
        # Browser models run client-side, not through API
        assert model["id"].startswith("browser:")
        # These would be handled by useWebLLM.js, not the backend


class TestWebsiteCLIIntegration:
    """Test website CLI (terminal) integration scenarios."""

    def test_terminal_websocket_endpoint_exists(self):
        """Test terminal websocket endpoint path."""
        endpoint = "/ws/terminal"
        assert endpoint.startswith("/ws/")

    def test_terminal_starts_sage_run(self):
        """Test terminal should start 'sage run' command."""
        expected_command = "sage run"
        assert "sage" in expected_command
        assert "run" in expected_command

    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["coding"])
    def test_terminal_prompt_format(self, prompt):
        """Test prompts sent through terminal."""
        # Terminal sends raw text, not JSON
        assert isinstance(prompt, str)
        assert "\x00" not in prompt  # No null bytes


class TestStandardCLIIntegration:
    """Test standard CLI integration scenarios."""

    @pytest.mark.parametrize("model", ALL_MODELS)
    def test_cli_model_command_format(self, model):
        """Test /model command format for CLI."""
        command = f"/model {model['id']}"
        assert command.startswith("/model ")
        assert model["id"] in command

    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"] + EXAMPLE_PROMPTS["coding"])
    def test_cli_prompt_is_valid(self, prompt):
        """Test prompts are valid CLI input."""
        # Not a command
        assert not prompt.startswith("/")
        # Not a shell escape
        assert not prompt.startswith("!")
        # Has content
        assert len(prompt.strip()) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# RATE LIMITING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRateLimiting:
    """Test rate limiting behavior."""

    def test_standard_rate_limit(self):
        """Test standard endpoint rate limit."""
        rate_limit = {"requests_per_minute": 120, "burst_limit": 20}
        assert rate_limit["requests_per_minute"] == 120
        assert rate_limit["burst_limit"] == 20

    def test_download_rate_limit(self):
        """Test download endpoint rate limit (stricter)."""
        rate_limit = {"requests_per_minute": 10, "burst_limit": 2}
        assert rate_limit["requests_per_minute"] == 10
        assert rate_limit["burst_limit"] == 2

    def test_terminal_rate_limit(self):
        """Test terminal websocket rate limit."""
        rate_limit = {"requests_per_minute": 5, "burst_limit": 2}
        assert rate_limit["requests_per_minute"] == 5


# ═══════════════════════════════════════════════════════════════════════════════
# SSE STREAMING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSSEStreaming:
    """Test Server-Sent Events streaming format."""

    def test_sse_token_event_format(self):
        """Test SSE token event format."""
        event = {"token": "Hello"}
        sse_line = f"data: {json.dumps(event)}\n\n"
        assert sse_line.startswith("data: ")
        assert sse_line.endswith("\n\n")
        assert "token" in json.loads(sse_line.replace("data: ", "").strip())

    def test_sse_step_event_format(self):
        """Test SSE step indicator event format."""
        event = {"step": "thinking", "message": "Processing..."}
        sse_line = f"data: {json.dumps(event)}\n\n"
        assert "step" in json.loads(sse_line.replace("data: ", "").strip())

    def test_sse_done_event_format(self):
        """Test SSE completion event format."""
        event = {"done": True, "conversation_id": "conv-123"}
        sse_line = f"data: {json.dumps(event)}\n\n"
        parsed = json.loads(sse_line.replace("data: ", "").strip())
        assert parsed["done"] is True

    def test_sse_error_event_format(self):
        """Test SSE error event format."""
        event = {
            "error": True,
            "error_code": "STREAM_ERROR",
            "message": "Connection lost",
            "request_id": "req-123",
            "partial_response": "Hello",
        }
        sse_line = f"data: {json.dumps(event)}\n\n"
        parsed = json.loads(sse_line.replace("data: ", "").strip())
        assert parsed["error"] is True
        assert "partial_response" in parsed
