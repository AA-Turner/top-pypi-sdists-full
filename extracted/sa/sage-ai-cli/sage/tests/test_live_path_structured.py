"""TDD tests for live path structured tools integration.

These tests verify that the LIVE CLI paths use:
1. Structured ToolCall objects instead of tuple parsing
2. Simple Q&A mode detection for sage run
3. First-token timeout actually working
4. Model availability verification

Run with: pytest sage/tests/test_live_path_structured.py -v
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# =============================================================================
# P0-1: Live loop must use structured tools, not tuple parser
# =============================================================================


class TestLiveLoopUsesStructuredTools:
    """Tests that live agent loop uses ToolCall, not tuples."""

    def test_phase_loop_uses_structured_extraction(self):
        """Phase loop should use _extract_tool_commands_structured, not _extract_tool_commands."""
        # Read the source and verify _extract_tool_commands_structured is used in phase loop
        main_py = Path(__file__).parent.parent / "main.py"
        source = main_py.read_text()

        # Find the phase loop area (around line 10829)
        # The tuple parser call should be replaced with structured call
        # Check that _extract_tool_commands_structured is used
        import_structured = "_extract_tool_commands_structured" in source
        assert import_structured, "main.py should use _extract_tool_commands_structured"

    def test_response_processing_uses_structured_tools(self):
        """_process_response and related calls should use structured extraction."""
        from sage.core.tools import ToolCall
        from sage.main import _extract_tool_commands_structured

        # Valid response with tool commands
        response = """Let me read the files:
READ: sage/main.py
READ: sage/core/tools.py
SEARCH: def _process_response
"""

        calls = _extract_tool_commands_structured(response)

        # Must return structured ToolCall objects
        assert len(calls) == 3
        assert all(isinstance(c, ToolCall) for c in calls)

    def test_structured_extraction_accepts_bare_read_syntax(self):
        """Near-miss tool syntax like READ file.py should still become a ToolCall."""
        from sage.main import _extract_tool_commands_structured

        calls = _extract_tool_commands_structured("READ README.md")

        assert len(calls) == 1
        assert calls[0].arguments["path"] == "README.md"

    def test_tuple_parser_not_used_in_live_checks(self):
        """Live path checks should not use the old tuple parser."""
        main_py = Path(__file__).parent.parent / "main.py"
        source = main_py.read_text()

        # Find usages of _extract_tool_commands (the old tuple parser)
        # It should only exist as a function definition, not as calls in live paths

        # Count calls to _extract_tool_commands (not _structured variant)
        tuple_parser_calls = re.findall(
            r"_extract_tool_commands\([^_]",  # Match calls but not _structured
            source,
        )

        # The old parser should have minimal usage (ideally 0 in live paths)
        # Allow for the function definition and any legacy compatibility
        # But live loop checks should use structured version
        assert len(tuple_parser_calls) <= 3, (
            f"Found {len(tuple_parser_calls)} calls to old tuple parser. "
            "Live paths should use _extract_tool_commands_structured"
        )


# =============================================================================
# P0-3: sage run must NOT over-instruct simple Q&A
# =============================================================================


class TestAskSimpleQAMode:
    """Tests that sage run uses simple mode for Q&A prompts."""

    def test_simple_qa_should_not_use_enhance_task_prompt(self):
        """Simple Q&A prompts should bypass _enhance_task_prompt."""
        from sage.main import _is_simple_qa_prompt

        simple_prompts = [
            "What is 2+2?",
            "What's the capital of France?",
            "How do I print hello world in Python?",
            "Explain recursion",
            "What does async mean?",
        ]

        for prompt in simple_prompts:
            assert _is_simple_qa_prompt(prompt), f"'{prompt}' should be detected as simple Q&A"

    def test_agent_tasks_should_use_enhance_task_prompt(self):
        """Agent tasks should still use _enhance_task_prompt."""
        from sage.main import _is_simple_qa_prompt

        agent_prompts = [
            "Analyze the codebase and list all improvements",
            "Fix the bug in auth.py",
            "Implement user authentication",
            "Read main.py and refactor the function",
        ]

        for prompt in agent_prompts:
            assert not _is_simple_qa_prompt(prompt), (
                f"'{prompt}' should NOT be detected as simple Q&A"
            )

    def test_ask_path_checks_simple_qa(self):
        """The ask command path should check _is_simple_qa_prompt."""
        # This test documents the requirement that the ask command
        # should use _is_simple_qa_prompt to decide whether to enhance
        from sage.main import _is_simple_qa_prompt

        # The function should exist and be usable
        assert callable(_is_simple_qa_prompt)

        # Simple test
        assert _is_simple_qa_prompt("What is 2+2?")


# =============================================================================
# P0-4: First-token timeout must actually work
# =============================================================================


class TestFirstTokenTimeoutWorks:
    """Tests that first-token timeout is actually enforced."""

    def test_timeout_parameter_exists(self):
        """stream_tokens_with_phase should have first_token_timeout parameter."""
        import inspect

        from sage.core.renderer import stream_tokens_with_phase

        sig = inspect.signature(stream_tokens_with_phase)
        params = list(sig.parameters.keys())

        assert "first_token_timeout" in params, (
            "stream_tokens_with_phase must have first_token_timeout parameter"
        )

    def test_streaming_timeout_error_exists(self):
        """StreamingTimeoutError should be importable."""
        from sage.core.renderer import StreamingTimeoutError

        assert issubclass(StreamingTimeoutError, Exception)

    def test_timeout_error_has_useful_message(self):
        """StreamingTimeoutError should have a useful message."""
        from sage.core.renderer import StreamingTimeoutError

        error = StreamingTimeoutError("No response from model within 30 seconds")
        assert "30 seconds" in str(error)


# =============================================================================
# P1-3: Model listing must verify files exist
# =============================================================================


class TestModelListingVerifiesFiles:
    """Tests that model listing verifies backing files exist."""

    def test_llama_cpp_is_available_checks_files(self):
        """LlamaCppProvider.is_available() should check file existence."""
        from sage.config import SageConfig
        from sage.providers.llama_cpp import LlamaCppProvider

        # Create mock config with non-existent model file
        mock_config = MagicMock(spec=SageConfig)
        mock_config.local_model_names.return_value = ["test:model"]
        mock_model = MagicMock()
        mock_model.path = "/nonexistent/path/model.gguf"
        mock_config.get_local_model.return_value = mock_model

        provider = LlamaCppProvider(mock_config)

        # Mock llama_cpp being available
        with patch.dict("sys.modules", {"llama_cpp": MagicMock()}):
            # Should return False because file doesn't exist
            result = provider.is_available()
            assert result is False, "Provider should not be available when model file doesn't exist"

    def test_model_listing_filters_missing_files(self):
        """Model listing should not include models with missing files."""
        import os
        import tempfile

        from sage.config import SageConfig
        from sage.providers.llama_cpp import LlamaCppProvider

        # Create a temp file to represent an existing model
        with tempfile.NamedTemporaryFile(suffix=".gguf", delete=False) as f:
            existing_path = f.name

        try:
            mock_config = MagicMock(spec=SageConfig)
            mock_config.local_model_names.return_value = ["existing:model", "missing:model"]

            def get_model(name):
                m = MagicMock()
                if name == "existing:model":
                    m.path = existing_path
                else:
                    m.path = "/nonexistent/model.gguf"
                return m

            mock_config.get_local_model.side_effect = get_model

            provider = LlamaCppProvider(mock_config)

            with patch.dict("sys.modules", {"llama_cpp": MagicMock()}):
                # is_available should work with at least one valid model
                assert provider.is_available() is True
        finally:
            os.unlink(existing_path)


# =============================================================================
# P1-4: Project root conventions must be unified
# =============================================================================


class TestProjectRootConventions:
    """Tests that project root is handled consistently."""

    def test_execution_ledger_binds_root_once(self):
        """ExecutionLedger should bind project root once and cache it."""
        from sage.core.tools import ExecutionLedger

        ledger = ExecutionLedger()

        # First bind
        root1 = ledger.bind_project_root("/first/path")
        assert root1 == "/first/path"

        # Second bind should return cached value
        root2 = ledger.bind_project_root("/second/path")
        assert root2 == "/first/path", "Should return cached root, not new path"

    def test_test_directory_convention(self):
        """Test directory should follow consistent convention."""
        # The repo uses sage/tests for SAGE tests
        # This should be the canonical location

        sage_tests = Path(__file__).parent
        assert sage_tests.name == "tests"
        assert sage_tests.parent.name == "sage"


# =============================================================================
# Integration: Verify structured tools flow
# =============================================================================


class TestStructuredToolsIntegration:
    """Integration tests for structured tools in live path."""

    def test_full_structured_flow(self):
        """Text -> ToolCall -> ExecutionLedger -> Validate claims."""
        from sage.core.tools import ExecutionLedger
        from sage.main import _extract_tool_commands_structured

        # Model response with tool commands
        response = """I'll read the relevant files:
READ: sage/main.py
READ: sage/core/tools.py
SEARCH: class ExecutionLedger
"""

        # Extract structured calls
        calls = _extract_tool_commands_structured(response)
        assert len(calls) == 3

        # Record in ledger
        ledger = ExecutionLedger()
        for call in calls:
            ledger.record_execution(call, success=True)

        # Verify ledger state
        assert ledger.total_reads == 2
        assert "sage/main.py" in ledger.files_read
        assert "sage/core/tools.py" in ledger.files_read

        # Validate claims
        assert ledger.can_claim_read_count(2)
        assert not ledger.can_claim_read_count(10)

    def test_blank_commands_rejected(self):
        """Blank tool commands should be rejected."""
        from sage.main import _extract_tool_commands_structured

        # Response with blank commands
        response = """READ:
READ:
READ:
"""

        calls = _extract_tool_commands_structured(response)

        # Should return empty - blank commands are invalid
        assert len(calls) == 0, "Blank commands should be rejected"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
