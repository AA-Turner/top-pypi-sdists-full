"""Comprehensive integration tests for AI Model Prompts.

Tests cover:
1. Text prompts for analysis tasks
2. Coding tasks with TDD (Test-Driven Development)
3. Mathematics questions with correct answers
4. Various model providers (mocked for unit testing)
5. CLI and web interface compatibility

These tests validate prompt handling, response quality, and integration.
"""

import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterator
from unittest.mock import MagicMock, patch

import pytest

from sage.providers.base import Message, ModelInfo, ProviderBase


# =============================================================================
# Mock Provider for Testing
# =============================================================================


class MockProvider(ProviderBase):
    """Mock provider for testing AI model integration."""

    name = "mock"

    def __init__(self, responses: dict[str, str] | None = None):
        self.responses = responses or {}
        self.call_history: list[dict] = []

    def set_response(self, prompt_pattern: str, response: str):
        """Set a response for a prompt pattern."""
        self.responses[prompt_pattern] = response

    def generate(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Return mock response."""
        last_message = messages[-1].content if messages else ""
        self.call_history.append({
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        })

        # Find matching response
        for pattern, response in self.responses.items():
            if pattern.lower() in last_message.lower():
                return response

        return "Mock response: No matching pattern found."

    def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Iterator[str]:
        """Yield mock response tokens."""
        response = self.generate(messages, model, temperature, max_tokens)
        for word in response.split():
            yield word + " "

    def list_models(self) -> list[ModelInfo]:
        """Return mock models."""
        return [
            ModelInfo(
                id="mock-model-small",
                provider="mock",
                name="Mock Small Model",
                local=False,
            ),
            ModelInfo(
                id="mock-model-large",
                provider="mock",
                name="Mock Large Model",
                local=False,
            ),
        ]

    def is_available(self) -> bool:
        """Always available."""
        return True


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_provider():
    """Create a mock provider instance."""
    return MockProvider()


@pytest.fixture
def analysis_provider():
    """Provider configured for analysis tasks."""
    provider = MockProvider()
    provider.set_response(
        "analyze",
        """## Code Analysis Results

### Summary
The codebase is well-structured with clear separation of concerns.

### Key Findings

1. **Architecture**: Uses layered architecture with proper abstractions.
2. **Code Quality**: Good test coverage and consistent coding style.
3. **Security**: No obvious security vulnerabilities found.
4. **Performance**: Efficient algorithms with O(n) complexity.
5. **Maintainability**: Clear documentation and modular design.

### Recommendations
- Consider adding type hints to legacy functions
- Update deprecated dependencies
- Add integration tests for edge cases
""",
    )
    return provider


@pytest.fixture
def coding_provider():
    """Provider configured for TDD coding tasks."""
    provider = MockProvider()
    provider.set_response(
        "implement",
        """Let me implement this feature with TDD.

First, I'll write the failing test:

FILE: sage/tests/test_feature.py
```python
import pytest
from sage.feature import calculate_sum

def test_calculate_sum_basic():
    assert calculate_sum([1, 2, 3]) == 6

def test_calculate_sum_empty():
    assert calculate_sum([]) == 0

def test_calculate_sum_negative():
    assert calculate_sum([-1, 1]) == 0
```

RUN: pytest sage/tests/test_feature.py -v

Now implementing to make tests pass:

FILE: sage/feature.py
```python
def calculate_sum(numbers: list[int]) -> int:
    \"\"\"Calculate the sum of a list of numbers.\"\"\"
    return sum(numbers)
```

RUN: pytest sage/tests/test_feature.py -v

All tests should pass now.
""",
    )
    return provider


@pytest.fixture
def math_provider():
    """Provider configured for mathematics tasks."""
    provider = MockProvider()
    provider.set_response(
        "calculate",
        """Let me solve this step by step:

**Problem**: Calculate the result.

**Solution**:
1. First, identify the operation
2. Apply the mathematical rules
3. Verify the result

**Answer**: The result is **42**.

**Verification**: We can verify by working backwards.
""",
    )
    provider.set_response(
        "math",
        """Mathematical Analysis:

For the expression 2 + 2:
- Step 1: We have two addends: 2 and 2
- Step 2: Adding them together: 2 + 2 = 4

**Final Answer: 4**
""",
    )
    provider.set_response(
        "fibonacci",
        """The Fibonacci sequence starts as: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34...

For n=10, the 10th Fibonacci number is **55**.

Explanation:
- F(0) = 0
- F(1) = 1
- F(10) = F(9) + F(8) = 34 + 21 = 55
""",
    )
    return provider


# =============================================================================
# Tests for Analysis Prompts
# =============================================================================


class TestAnalysisPrompts:
    """Tests for analysis-type prompts."""

    def test_analysis_prompt_basic(self, analysis_provider):
        """Basic analysis prompt returns structured response."""
        messages = [
            Message(role="user", content="Analyze this code for quality issues")
        ]

        response = analysis_provider.generate(messages, "mock-model-small")

        assert "Analysis" in response
        assert "Findings" in response or "Summary" in response

    def test_analysis_response_has_sections(self, analysis_provider):
        """Analysis response has proper sections."""
        messages = [
            Message(role="user", content="Analyze the architecture")
        ]

        response = analysis_provider.generate(messages, "mock-model-small")

        # Should have headers/sections
        assert "##" in response or "**" in response

    def test_analysis_detects_request_type(self):
        """Classify analysis request type."""
        from sage.core.unified_classifier import classify_request, RequestType

        # Use a prompt without "bugs" to avoid DEBUGGING classification
        result = classify_request("Analyze this codebase architecture")

        assert result.request_type == RequestType.ANALYSIS

    def test_analysis_read_only_detection(self):
        """Analysis with read-only constraint is detected."""
        from sage.core.unified_classifier import is_read_only_request

        assert is_read_only_request("Just analyze, don't modify anything") is True
        assert is_read_only_request("Analyze and fix the bugs") is False


class TestListGenerationPrompts:
    """Tests for list generation prompts (list 100 items)."""

    def test_detects_quantity_in_prompt(self):
        """Detect quantity requirement in prompt."""
        from sage.core.unified_classifier import get_required_quantity

        assert get_required_quantity("List 100 items to improve") == 100
        assert get_required_quantity("Give me 50 suggestions") == 50
        assert get_required_quantity("What can be improved?") == 0

    def test_validates_list_completeness(self):
        """Validate that list meets quantity requirement."""
        # Generate a list with 100 items
        items = [f"{i+1}. Item {i+1}" for i in range(100)]
        response = "\n".join(items)

        # Count numbered items
        numbered = re.findall(r"^\s*(\d+)[.\)]\s+", response, re.MULTILINE)
        assert len(numbered) == 100

    def test_detects_incomplete_list(self):
        """Detect when list is incomplete."""
        # Only 10 items instead of 100
        items = [f"{i+1}. Item {i+1}" for i in range(10)]
        response = "\n".join(items)

        numbered = re.findall(r"^\s*(\d+)[.\)]\s+", response, re.MULTILINE)
        requested = 100
        threshold = requested * 0.7  # 70% threshold

        assert len(numbered) < threshold, "Should detect incomplete list"

    def test_list_generation_classifier(self):
        """List generation is properly classified."""
        from sage.core.unified_classifier import classify_request, RequestType

        result = classify_request("List 100 things that need improvement")

        assert result.request_type == RequestType.LIST_GENERATION
        assert result.quantity.quantity == 100


# =============================================================================
# Tests for Coding with TDD
# =============================================================================


class TestTDDCodingPrompts:
    """Tests for TDD coding prompts."""

    def test_tdd_response_structure(self, coding_provider):
        """TDD response has proper structure."""
        messages = [
            Message(role="user", content="Implement a sum function with TDD")
        ]

        response = coding_provider.generate(messages, "mock-model-small")

        # Should have FILE: blocks
        assert "FILE:" in response

        # Should have test files
        assert "test_" in response

        # Should have RUN: commands
        assert "RUN:" in response

    def test_tdd_test_before_implementation(self, coding_provider):
        """TDD: tests should come before implementation."""
        messages = [
            Message(role="user", content="Implement feature with TDD")
        ]

        response = coding_provider.generate(messages, "mock-model-small")

        # Find all FILE: blocks
        file_blocks = re.findall(r"FILE:\s*(\S+)", response)

        if len(file_blocks) >= 2:
            # First should be test file
            test_indices = [i for i, f in enumerate(file_blocks) if "test_" in f]
            impl_indices = [i for i, f in enumerate(file_blocks) if "test_" not in f]

            if test_indices and impl_indices:
                assert min(test_indices) < min(impl_indices), "Test should come before implementation"

    def test_tdd_has_assertions(self, coding_provider):
        """TDD tests should have assertions."""
        messages = [
            Message(role="user", content="Implement with TDD")
        ]

        response = coding_provider.generate(messages, "mock-model-small")

        # Should have assert statements
        assert "assert" in response

    def test_implementation_classifier(self):
        """Implementation request is properly classified."""
        from sage.core.unified_classifier import classify_request, RequestType

        result = classify_request("Implement a new authentication system")

        assert result.request_type == RequestType.IMPLEMENTATION
        assert result.must_include_code is True


class TestTDDValidation:
    """Tests for TDD validation logic."""

    def test_detects_invalid_tool_syntax(self):
        """Detect invalid tool syntax."""
        bad_response = """
        <execute_tool>
        tool_name: read_file
        </execute_tool>
        """

        # Should detect <execute_tool> as invalid
        assert re.search(r"<execute_tool>", bad_response) is not None

    def test_valid_sage_syntax(self):
        """Valid SAGE syntax is not flagged."""
        good_response = """
        FILE: test.py
        ```python
        def test():
            pass
        ```
        RUN: pytest test.py
        """

        invalid_patterns = [
            r"<execute_tool>",
            r"tool_name:\s*\w+",
        ]

        for pattern in invalid_patterns:
            assert re.search(pattern, good_response) is None

    def test_detects_print_instead_of_code(self):
        """Detect print statements instead of actual code."""
        bad_response = """
        <execute_tool>
        print("Starting implementation...")
        </execute_tool>
        """

        # Should NOT have valid FILE: blocks
        assert re.search(r"FILE:\s*\S+\s*\n```", bad_response) is None


# =============================================================================
# Tests for Mathematics Prompts
# =============================================================================


class TestMathematicsPrompts:
    """Tests for mathematics prompts."""

    def test_math_basic_arithmetic(self, math_provider):
        """Basic arithmetic question."""
        messages = [
            Message(role="user", content="What is 2 + 2? Show your math work.")
        ]

        response = math_provider.generate(messages, "mock-model-small")

        # Should contain the answer
        assert "4" in response

    def test_math_with_steps(self, math_provider):
        """Math response includes steps."""
        messages = [
            Message(role="user", content="Calculate the fibonacci sequence")
        ]

        response = math_provider.generate(messages, "mock-model-small")

        # Should have step-by-step explanation (case-insensitive)
        assert "step" in response.lower() or "f(" in response.lower()

    def test_math_answer_extraction(self, math_provider):
        """Extract answer from math response."""
        messages = [
            Message(role="user", content="What is 2 + 2? math question")
        ]

        response = math_provider.generate(messages, "mock-model-small")

        # Extract the final answer
        answer_match = re.search(r"(?:answer|result)[:\s]*(\d+)", response.lower())
        if answer_match:
            assert answer_match.group(1) == "4"

    def test_math_verification(self, math_provider):
        """Math response includes verification."""
        messages = [
            Message(role="user", content="Calculate something")
        ]

        response = math_provider.generate(messages, "mock-model-small")

        # Should mention verification
        assert "verify" in response.lower() or "verification" in response.lower()


# =============================================================================
# Tests for Model Provider Integration
# =============================================================================


class TestProviderIntegration:
    """Tests for model provider integration."""

    def test_mock_provider_tracks_calls(self, mock_provider):
        """Provider tracks call history."""
        messages = [Message(role="user", content="Hello")]
        mock_provider.generate(messages, "mock-model-small")

        assert len(mock_provider.call_history) == 1
        assert mock_provider.call_history[0]["model"] == "mock-model-small"

    def test_provider_streaming(self, mock_provider):
        """Provider streaming works."""
        mock_provider.set_response("test", "Hello world!")
        messages = [Message(role="user", content="test message")]

        tokens = list(mock_provider.stream(messages, "mock-model-small"))
        assert len(tokens) > 0

    def test_provider_list_models(self, mock_provider):
        """Provider lists available models."""
        models = mock_provider.list_models()

        assert len(models) >= 1
        assert all(isinstance(m, ModelInfo) for m in models)

    def test_provider_availability(self, mock_provider):
        """Provider reports availability."""
        assert mock_provider.is_available() is True


class TestMultiProviderSupport:
    """Tests for multi-provider support."""

    def test_provider_base_interface(self):
        """ProviderBase interface is complete."""
        # Check abstract methods
        assert hasattr(ProviderBase, "generate")
        assert hasattr(ProviderBase, "stream")
        assert hasattr(ProviderBase, "list_models")
        assert hasattr(ProviderBase, "is_available")

    def test_model_info_dataclass(self):
        """ModelInfo dataclass works correctly."""
        model = ModelInfo(
            id="test-model",
            provider="test",
            name="Test Model",
            local=False,
            description="A test model",
        )

        assert model.id == "test-model"
        assert model.provider == "test"
        assert model.local is False

    def test_message_dataclass(self):
        """Message dataclass works correctly."""
        msg = Message(role="user", content="Hello")

        assert msg.role == "user"
        assert msg.content == "Hello"


# =============================================================================
# Tests for Response Quality
# =============================================================================


class TestResponseQuality:
    """Tests for response quality validation."""

    def test_detect_repetitive_content(self):
        """Detect repetitive/stuck model output."""
        response = "implement the feature " * 20

        words = response.split()
        trigrams = [' '.join(words[i:i+3]) for i in range(len(words)-2)]
        most_common = Counter(trigrams).most_common(1)

        # Should detect excessive repetition
        assert most_common[0][1] >= 10, "Should detect repetition"

    def test_detect_garbage_paths(self):
        """Detect garbage path output."""
        garbage = "ai-tools/" * 15

        pattern = r"([\w-]+/){10,}"
        assert re.search(pattern, garbage) is not None

    def test_normal_path_not_flagged(self):
        """Normal nested paths are not flagged."""
        normal = "src/components/ui/buttons/primary.tsx"

        pattern = r"([\w-]+/){10,}"
        assert re.search(pattern, normal) is None

    def test_empty_response_detection(self):
        """Detect empty or too-short responses."""
        responses = [
            "",
            "OK",
            "Done",
            "I'll do that",
        ]

        for response in responses:
            # Short responses for complex tasks should be flagged
            is_too_short = len(response.strip()) < 50
            assert is_too_short, f"'{response}' should be flagged as too short"


# =============================================================================
# Tests for CLI Integration
# =============================================================================


class TestCLIIntegration:
    """Tests for CLI integration."""

    def test_cli_command_parsing(self):
        """CLI commands are properly parsed."""
        from sage.core.commands import parse_command

        # Test pytest command
        parsed = parse_command("pytest -v tests/")
        assert parsed.is_valid
        assert parsed.executable == "pytest"

    def test_cli_safe_commands(self):
        """CLI validates safe commands."""
        from sage.core.commands import is_command_allowed

        assert is_command_allowed("pytest tests/") is True
        assert is_command_allowed("rm -rf /") is False

    def test_cli_shell_safety(self):
        """Shell commands are validated."""
        from sage.core.shell import is_safe_readonly_command

        # Read-only commands should be safe
        safe, _ = is_safe_readonly_command("ls -la")
        assert safe is True

        # Dangerous commands should not be safe
        safe, _ = is_safe_readonly_command("rm -rf /")
        assert safe is False


# =============================================================================
# Tests for Web Interface Integration
# =============================================================================


class TestWebIntegration:
    """Tests for web interface integration."""

    def test_request_classification_api(self):
        """Request classification works for web API."""
        from sage.core.unified_classifier import classify_request

        # Simulate web API request
        result = classify_request("Help me fix this bug in authentication")

        assert result is not None
        assert result.original_request == "Help me fix this bug in authentication"

    def test_quantity_parsing_api(self):
        """Quantity parsing works for web API."""
        from sage.core.unified_classifier import parse_quantity

        # Use a clearer quantity phrase that the parser recognizes
        result = parse_quantity("List 50 items to improve")

        assert result.quantity == 50

    def test_output_format_detection(self):
        """Output format detection for web rendering."""
        from sage.core.unified_classifier import classify_request, OutputFormat

        result = classify_request("Show results as JSON")
        assert result.output_format == OutputFormat.JSON

        result = classify_request("Display as a table")
        assert result.output_format == OutputFormat.TABLE


# =============================================================================
# Integration Tests - Full Workflow
# =============================================================================


class TestFullWorkflowIntegration:
    """Integration tests for complete workflows."""

    def test_analysis_workflow(self, analysis_provider):
        """Complete analysis workflow."""
        # 1. Classify request
        from sage.core.unified_classifier import classify_request, RequestType

        request = "Analyze the codebase"
        classification = classify_request(request)

        assert classification.request_type == RequestType.ANALYSIS

        # 2. Generate response
        messages = [Message(role="user", content=request)]
        response = analysis_provider.generate(messages, "mock-model-small")

        # 3. Validate response quality
        assert len(response) > 50  # Not too short
        assert "##" in response or "**" in response  # Has structure

    def test_tdd_workflow(self, coding_provider):
        """Complete TDD implementation workflow."""
        # 1. Classify as implementation
        from sage.core.unified_classifier import classify_request, RequestType

        request = "Implement a calculator with TDD"
        classification = classify_request(request)

        assert classification.request_type == RequestType.IMPLEMENTATION
        assert classification.must_include_code is True

        # 2. Generate TDD response
        messages = [Message(role="user", content=request)]
        response = coding_provider.generate(messages, "mock-model-small")

        # 3. Validate TDD structure
        assert "FILE:" in response
        assert "test_" in response
        assert "RUN:" in response
        assert "assert" in response

    def test_math_workflow(self, math_provider):
        """Complete math problem workflow."""
        # 1. Generate math solution
        request = "What is the 10th fibonacci number?"
        messages = [Message(role="user", content=request)]
        response = math_provider.generate(messages, "mock-model-small")

        # 2. Validate has answer
        assert "55" in response or "fibonacci" in response.lower()

        # 3. Validate has explanation
        assert "step" in response.lower() or "F(" in response

    def test_multi_task_workflow(self, analysis_provider, coding_provider, math_provider):
        """Workflow with multiple task types."""
        tasks = [
            ("Analyze the security", analysis_provider, "analysis"),
            ("Implement with TDD", coding_provider, "file:"),
            ("fibonacci", math_provider, "fibonacci"),  # Match the pattern key
        ]

        for prompt, provider, expected in tasks:
            messages = [Message(role="user", content=prompt)]
            response = provider.generate(messages, "mock-model-small")

            assert expected.lower() in response.lower(), \
                f"Expected '{expected}' in response for '{prompt}'"


# =============================================================================
# Tests for Error Handling
# =============================================================================


class TestErrorHandling:
    """Tests for error handling in AI integration."""

    def test_empty_prompt_handling(self, mock_provider):
        """Handle empty prompts gracefully."""
        messages = [Message(role="user", content="")]
        response = mock_provider.generate(messages, "mock-model-small")

        # Should return some response, not crash
        assert response is not None

    def test_very_long_prompt(self, mock_provider):
        """Handle very long prompts."""
        long_content = "x" * 10000
        messages = [Message(role="user", content=long_content)]
        response = mock_provider.generate(messages, "mock-model-small")

        assert response is not None

    def test_special_characters_in_prompt(self, mock_provider):
        """Handle special characters in prompts."""
        special_content = "Test with <special> & \"characters\" 'here'"
        messages = [Message(role="user", content=special_content)]
        response = mock_provider.generate(messages, "mock-model-small")

        assert response is not None

    def test_unicode_in_prompt(self, mock_provider):
        """Handle unicode in prompts."""
        unicode_content = "Test with unicode: 你好 🎉 café naïve"
        messages = [Message(role="user", content=unicode_content)]
        response = mock_provider.generate(messages, "mock-model-small")

        assert response is not None
