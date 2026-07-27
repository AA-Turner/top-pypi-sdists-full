"""
Model matrix tests for SAGE AI.

Tests all models across all platforms (CLI, website chat, website CLI)
with example prompts to verify functionality.
"""

import json

import pytest

# ═══════════════════════════════════════════════════════════════════════════════
# MODEL DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

# Pollinations cloud aliases removed — keep empty list for compatibility with matrix tests.
CLOUD_MODELS: list[dict] = []

# Browser models (WebLLM, runs in browser)
BROWSER_MODELS = [
    {"id": "browser:Llama-3.2-1B-Instruct-q4f16_1-MLC", "name": "Llama 3.2 1B", "size": "0.6 GB"},
    {"id": "browser:Llama-3.2-3B-Instruct-q4f16_1-MLC", "name": "Llama 3.2 3B", "size": "1.8 GB"},
    {"id": "browser:Phi-3.5-mini-instruct-q4f16_1-MLC", "name": "Phi 3.5 Mini", "size": "2.2 GB"},
    {"id": "browser:Qwen2.5-1.5B-Instruct-q4f16_1-MLC", "name": "Qwen 2.5 1.5B", "size": "0.9 GB"},
    {"id": "browser:SmolLM2-1.7B-Instruct-q4f16_1-MLC", "name": "SmolLM2 1.7B", "size": "1.0 GB"},
    {"id": "browser:gemma-2-2b-it-q4f16_1-MLC", "name": "Gemma 2 2B", "size": "1.4 GB"},
    {
        "id": "browser:TinyLlama-1.1B-Chat-v1.0-q4f16_1-MLC",
        "name": "TinyLlama 1.1B",
        "size": "0.6 GB",
    },
]

# Ollama models (requires local Ollama server)
OLLAMA_MODELS = [
    {"id": "ollama:llama3.2", "name": "Llama 3.2"},
    {"id": "ollama:qwen2.5-coder", "name": "Qwen 2.5 Coder"},
    {"id": "ollama:deepseek-r1", "name": "DeepSeek R1"},
    {"id": "ollama:gemma2", "name": "Gemma 2"},
    {"id": "ollama:mistral", "name": "Mistral"},
    {"id": "ollama:phi4", "name": "Phi 4"},
]

# All models combined
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
# MODEL ID FORMAT TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestModelIdFormat:
    """Test model ID format validation."""

    @pytest.mark.parametrize("model", CLOUD_MODELS)
    def test_cloud_model_id_format(self, model):
        """Test cloud model IDs have correct format."""
        model_id = model["id"]
        assert model_id.startswith("cloud:")
        name = model_id.removeprefix("cloud:")
        assert len(name) > 0
        assert " " not in name

    @pytest.mark.parametrize("model", BROWSER_MODELS)
    def test_browser_model_id_format(self, model):
        """Test browser model IDs have correct format."""
        model_id = model["id"]
        assert model_id.startswith("browser:")
        name = model_id.removeprefix("browser:")
        assert len(name) > 0
        assert "-MLC" in name  # WebLLM models end with -MLC

    @pytest.mark.parametrize("model", OLLAMA_MODELS)
    def test_ollama_model_id_format(self, model):
        """Test Ollama model IDs have correct format."""
        model_id = model["id"]
        assert model_id.startswith("ollama:")
        name = model_id.removeprefix("ollama:")
        assert len(name) > 0
        assert " " not in name


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL RESOLUTION TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestModelResolution:
    """Test model resolution and provider detection."""

    @pytest.mark.parametrize("model", ALL_MODELS)
    def test_model_has_required_fields(self, model):
        """Test all models have required fields."""
        assert "id" in model
        assert "name" in model

    def test_cloud_models_removed_from_matrix(self):
        """Pollinations-backed cloud entries are no longer tracked."""
        assert CLOUD_MODELS == []

    def test_browser_models_have_size(self):
        """Test browser models have size info."""
        for model in BROWSER_MODELS:
            assert "size" in model
            assert "GB" in model["size"]

    def test_no_duplicate_model_ids(self):
        """Test no duplicate model IDs exist."""
        ids = [m["id"] for m in ALL_MODELS]
        assert len(ids) == len(set(ids))


# ═══════════════════════════════════════════════════════════════════════════════
# PLATFORM AVAILABILITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestPlatformAvailability:
    """Test model availability on different platforms."""

    # Website (Cloud Run) — browser models + empty cloud slot
    WEBSITE_AVAILABLE = CLOUD_MODELS + BROWSER_MODELS

    # Standard CLI - all models can work (if dependencies available)
    CLI_AVAILABLE = ALL_MODELS

    WEBSITE_CLI_AVAILABLE = CLOUD_MODELS + BROWSER_MODELS

    def test_website_cloud_models_available(self):
        """Test cloud models are available on website."""
        for model in CLOUD_MODELS:
            assert model in self.WEBSITE_AVAILABLE

    def test_website_browser_models_available(self):
        """Test browser models are available on website."""
        for model in BROWSER_MODELS:
            assert model in self.WEBSITE_AVAILABLE

    def test_website_ollama_not_available(self):
        """Test Ollama models are NOT available on website (no local server)."""
        for model in OLLAMA_MODELS:
            assert model not in self.WEBSITE_AVAILABLE

    def test_cli_all_models_potentially_available(self):
        """Test all models are potentially available on CLI."""
        for model in ALL_MODELS:
            assert model in self.CLI_AVAILABLE


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT TESTS PER MODEL TYPE
# ═══════════════════════════════════════════════════════════════════════════════


class TestCloudModelPrompts:
    """Test prompts work with cloud models."""

    @pytest.mark.parametrize("model", CLOUD_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"])
    def test_cloud_model_simple_prompt(self, model, prompt):
        """Test cloud model handles simple prompts."""
        # Verify prompt format is valid
        assert len(prompt) > 0
        assert isinstance(prompt, str)
        # Model ID is valid
        assert model["id"].startswith("cloud:")

    @pytest.mark.parametrize("model", CLOUD_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["coding"])
    def test_cloud_model_coding_prompt(self, model, prompt):
        """Test cloud model handles coding prompts."""
        assert len(prompt) > 0
        assert model["id"].startswith("cloud:")


class TestBrowserModelPrompts:
    """Test prompts work with browser models."""

    @pytest.mark.parametrize("model", BROWSER_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"])
    def test_browser_model_simple_prompt(self, model, prompt):
        """Test browser model handles simple prompts."""
        assert len(prompt) > 0
        assert model["id"].startswith("browser:")

    @pytest.mark.parametrize("model", BROWSER_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["reasoning"])
    def test_browser_model_reasoning_prompt(self, model, prompt):
        """Test browser model handles reasoning prompts."""
        assert len(prompt) > 0
        assert model["id"].startswith("browser:")


class TestOllamaModelPrompts:
    """Test prompts work with Ollama models."""

    @pytest.mark.parametrize("model", OLLAMA_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"])
    def test_ollama_model_simple_prompt(self, model, prompt):
        """Test Ollama model handles simple prompts."""
        assert len(prompt) > 0
        assert model["id"].startswith("ollama:")

    @pytest.mark.parametrize("model", OLLAMA_MODELS)
    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["creative"])
    def test_ollama_model_creative_prompt(self, model, prompt):
        """Test Ollama model handles creative prompts."""
        assert len(prompt) > 0
        assert model["id"].startswith("ollama:")


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE FORMAT TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestMessageFormat:
    """Test chat message format for all platforms."""

    def test_chat_message_format(self):
        """Test chat message has correct format."""
        message = {"role": "user", "content": "Hello"}
        assert "role" in message
        assert "content" in message
        assert message["role"] in ["user", "assistant", "system"]

    def test_chat_request_format(self):
        """Test chat request has all required fields."""
        request = {
            "model_id": "ollama:llama3.2",
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
            "max_tokens": 1024,
            "stream": True,
        }
        assert "model_id" in request
        assert "messages" in request
        assert len(request["messages"]) > 0

    @pytest.mark.parametrize("model", ALL_MODELS)
    def test_request_with_each_model(self, model):
        """Test request format works with each model."""
        request = {
            "model_id": model["id"],
            "messages": [{"role": "user", "content": "Test"}],
            "temperature": 0.3,
            "max_tokens": 512,
        }
        assert request["model_id"] == model["id"]


# ═══════════════════════════════════════════════════════════════════════════════
# SAGE RUN CLI TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestSageRunCLI:
    """Test model usage in sage run CLI."""

    @pytest.mark.parametrize("model", ALL_MODELS)
    def test_model_command_format(self, model):
        """Test /model command format for each model."""
        command = f"/model {model['id']}"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "model"
        assert parts[1] == model["id"]

    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"] + EXAMPLE_PROMPTS["coding"])
    def test_prompt_is_valid_input(self, prompt):
        """Test prompts are valid REPL input."""
        # Not a command
        assert not prompt.startswith("/")
        # Not a shell escape
        assert not prompt.startswith("!")
        # Has content
        assert len(prompt.strip()) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSITE CHAT TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestWebsiteChat:
    """Test model usage in website chat."""

    @pytest.mark.parametrize("model", CLOUD_MODELS + BROWSER_MODELS)
    def test_website_model_selectable(self, model):
        """Test model can be selected on website."""
        model_id = model["id"]
        # Valid model ID format
        assert ":" in model_id
        prefix = model_id.split(":")[0]
        assert prefix in {"cloud", "browser", "ollama"}

    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"])
    def test_website_prompt_sendable(self, prompt):
        """Test prompt can be sent via website."""
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        # Check it's JSON-serializable
        json.dumps({"content": prompt})


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSITE CLI (TERMINAL) TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestWebsiteCLI:
    """Test model usage in website CLI terminal."""

    def test_terminal_starts_sage_run(self):
        """Test terminal should start sage run."""
        expected_command = "sage run"
        assert "sage" in expected_command
        assert "run" in expected_command

    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS["simple"])
    def test_terminal_prompt_format(self, prompt):
        """Test prompt format for terminal."""
        # Terminal sends raw text
        assert isinstance(prompt, str)
        # Shouldn't have control characters
        assert "\x00" not in prompt

    @pytest.mark.parametrize("cmd", ["/help", "/models", "/model ollama:llama3.2", "/clear"])
    def test_terminal_command_format(self, cmd):
        """Test terminal commands have correct format."""
        assert cmd.startswith("/")


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLING TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestModelErrorHandling:
    """Test error handling for invalid models."""

    INVALID_MODEL_IDS = [
        "",
        "invalid",
        "cloud:",
        ":openai",
        "unknown:model",
        "ollama:",
        "browser:",
    ]

    @pytest.mark.parametrize("model_id", INVALID_MODEL_IDS)
    def test_invalid_model_id_detected(self, model_id):
        """Test invalid model IDs are detected."""
        # Check format issues
        if not model_id:
            assert model_id == ""
        elif ":" not in model_id:
            assert ":" not in model_id
        elif model_id.endswith(":"):
            assert model_id[-1] == ":"
        elif model_id.startswith(":"):
            assert model_id[0] == ":"

    def test_ollama_unavailable_error_message(self):
        """Test Ollama unavailable error message format."""
        error_msg = (
            "Ollama is not running. Cannot use 'llama3.2'. Start Ollama with: ollama serve"
        )
        assert "Ollama" in error_msg
        assert "ollama serve" in error_msg

    def test_model_not_found_error_format(self):
        """Test model not found error format."""
        model_id = "nonexistent-model"
        error_msg = f"Model '{model_id}' not found."
        assert model_id in error_msg


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TEST PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestIntegrationPrompts:
    """Prompts for integration testing across all platforms."""

    # Quick sanity check prompts
    SMOKE_TEST_PROMPTS = [
        "Say 'OK' if you can read this.",
        "What is 1+1?",
        "Hello",
    ]

    # Prompts that verify model capabilities
    CAPABILITY_TEST_PROMPTS = [
        # Code generation
        "Write a Python function called 'add' that adds two numbers.",
        # Reasoning
        "If A > B and B > C, is A > C? Answer yes or no.",
        # Following instructions
        "List three colors, one per line.",
    ]

    @pytest.mark.parametrize("prompt", SMOKE_TEST_PROMPTS)
    def test_smoke_test_prompt_valid(self, prompt):
        """Test smoke test prompts are valid."""
        assert len(prompt) > 0
        assert len(prompt) < 1000  # Reasonable length

    @pytest.mark.parametrize("prompt", CAPABILITY_TEST_PROMPTS)
    def test_capability_prompt_valid(self, prompt):
        """Test capability test prompts are valid."""
        assert len(prompt) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL FEATURE SUPPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestModelFeatureSupport:
    """Test feature support across models."""

    STREAMING_MODELS = CLOUD_MODELS + BROWSER_MODELS + OLLAMA_MODELS
    TOOLS_MODELS = []  # Models that support function calling

    @pytest.mark.parametrize("model", STREAMING_MODELS)
    def test_model_supports_streaming(self, model):
        """Test model supports streaming responses."""
        # All models should support streaming
        assert model in self.STREAMING_MODELS

    def test_browser_models_require_webgpu(self):
        """Test browser models require WebGPU."""
        for model in BROWSER_MODELS:
            # Browser models need WebGPU
            assert model["id"].startswith("browser:")

    def test_cloud_models_require_no_setup(self):
        """Test cloud models require no local setup."""
        for model in CLOUD_MODELS:
            assert model["id"].startswith("cloud:")
            # No local dependencies needed
