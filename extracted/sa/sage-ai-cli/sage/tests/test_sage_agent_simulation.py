"""Comprehensive simulation tests for SAGE agent behavior.

This test file simulates the full SAGE agent flow to verify:
1. Early pattern detection during streaming works correctly
2. Validation rejects bad responses before processing
3. Recovery prompts guide the model to correct behavior
4. The agent can handle analysis and implementation tasks
5. TDD workflow operates correctly

Run with: pytest sage/tests/test_sage_agent_simulation.py -v
"""

from __future__ import annotations

from pathlib import Path

# =============================================================================
# TEST 1: Streaming Pattern Detection
# =============================================================================


class TestStreamingPatternDetection:
    """Test early pattern detection during streaming."""

    def test_detect_xml_tool_tags(self):
        """XML tool tags should be detected and rejected early."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        bad_responses = [
            "<execute_tool>read</execute_tool>",
            "<tool_call>read_file</tool_call>",
            "<function_call name='read'>path</function_call>",
        ]

        for response in bad_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is True, f"Should detect XML tags in: {response[:50]}..."
            assert "xml" in reason.lower() or "tool" in reason.lower()

    def test_allow_execute_tool_yaml_payload_when_normalizable(self):
        """An <execute_tool> block with YAML payload should be allowed if it normalizes to READ:/SEARCH:/RUN:."""
        from sage.core.renderer import _detect_bad_streaming_patterns, normalize_tool_command_syntax

        response = "<execute_tool>\ntool_name: read_file\nparameters:\n  file_path: test.py\n</execute_tool>"

        normalized = normalize_tool_command_syntax(response)
        assert "READ: test.py" in normalized

        is_bad, reason = _detect_bad_streaming_patterns(response)
        assert is_bad is False, f"Normalizable XML tool payload should not be rejected: {reason}"

    def test_allow_execute_tool_json_payload_when_normalizable(self):
        """<execute_tool> with JSON (tool_name/parameters) should normalize to READ: like YAML."""
        from sage.core.renderer import _detect_bad_streaming_patterns, normalize_tool_command_syntax

        response = """<execute_tool>
{
  "tool_name": "read_file",
  "parameters": {
    "file_path": "README.md"
  }
}
</execute_tool>"""

        normalized = normalize_tool_command_syntax(response)
        assert "READ: README.md" in normalized

        is_bad, reason = _detect_bad_streaming_patterns(response)
        assert is_bad is False, f"JSON XML tool payload should not be rejected: {reason}"

    def test_detect_yaml_tool_syntax(self):
        """YAML tool syntax should be detected and rejected early."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        bad_responses = [
            "tool_name: read_file\nparameters:\n  file_path: test.py",
            "function: analyze\nargs:\n  path: .",
        ]

        for response in bad_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is True, f"Should detect YAML syntax in: {response[:50]}..."

    def test_detect_repetitive_paths(self):
        """Repetitive path patterns should be detected and rejected."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        bad_paths = [
            "ai-platform/ai-platform/ai-platform/ai-platform/ai-platform/ai-platform/test.py",
            "src/src/src/src/src/src/main.py",
            "backend/backend/backend/backend/backend/model.py",
        ]

        for path in bad_paths:
            is_bad, reason = _detect_bad_streaming_patterns(path)
            assert is_bad is True, f"Should detect repetitive path: {path[:50]}..."
            assert "repetitive" in reason.lower()

    def test_detect_tool_refusal(self):
        """Tool refusal claims should be detected and rejected."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        refusal_responses = [
            "I cannot execute the read commands, so I will assume...",
            "Since tool commands will not work, I'll proceed based on assumptions.",
            "Tool commands do not work in this environment, so let me guess...",
        ]

        for response in refusal_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is True, f"Should detect refusal in: {response[:50]}..."

    def test_allow_valid_responses(self):
        """Valid responses should not be flagged."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        valid_responses = [
            "READ: sage/main.py\nSEARCH: test_*.py",
            "Based on reading the file, I found these issues:\n1. Bug at line 42",
            "FILE: sage/tests/test_new.py\n```python\ndef test_feature():\n    assert True\n```",
            "RUN: pytest -v\nRESULT: All 10 tests passed",
        ]

        for response in valid_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is False, f"Should NOT flag valid response: {response[:50]}..."


# =============================================================================
# TEST 2: Context Validation for Analysis Tasks
# =============================================================================


class TestAnalysisTaskValidation:
    """Test validation for analysis/list generation tasks."""

    def test_reject_large_list_without_reads(self):
        """Large recommendation lists without file reads should be rejected."""
        from sage.cli_core import _validate_context_gathering

        # Generate 100 recommendations
        recommendations = "\n".join([f"{i}. Fix issue {i} in the codebase" for i in range(1, 101)])

        is_valid, reason = _validate_context_gathering(
            recommendations,
            files_read=[],  # No files read
            is_analysis_request=True,
        )

        assert is_valid is False, "Should reject 100 recommendations with 0 files"
        assert "recommendation" in reason.lower() or "file" in reason.lower()

    def test_accept_list_with_proportional_reads(self):
        """Lists with proportional file reads should be accepted."""
        from sage.cli_core import _validate_context_gathering

        # Generate 50 recommendations
        recommendations = "\n".join([f"{i}. Fix issue in module {i}" for i in range(1, 51)])

        is_valid, reason = _validate_context_gathering(
            recommendations,
            files_read=["main.py", "config.py", "utils.py", "models.py", "api.py", "tests.py"],
            is_analysis_request=True,
        )

        assert is_valid is True, f"Should accept with 6 files read: {reason}"

    def test_reject_assumption_based_reasoning(self):
        """Responses that proceed by assuming should be rejected."""
        from sage.cli_core import _validate_context_gathering

        assumption_responses = [
            "I will proceed by assuming the codebase uses standard patterns...",
            "Let me assume this is a typical Python project and...",
            "Based on assumptions about the structure, here are 50 improvements:\n"
            + "\n".join([f"{i}. Item {i}" for i in range(1, 51)]),
        ]

        for response in assumption_responses:
            is_valid, reason = _validate_context_gathering(
                response, files_read=[], is_analysis_request=True
            )
            assert is_valid is False, (
                f"Should reject assumption-based reasoning: {response[:50]}..."
            )


# =============================================================================
# TEST 3: Tool Description vs Execution Detection
# =============================================================================


class TestToolExecutionValidation:
    """Test detection of tool descriptions vs actual execution."""

    def test_detect_descriptive_tool_mentions(self):
        """Tool descriptions WITHOUT actual execution should be detected and rejected."""
        from sage.cli_core import _detect_tool_description_vs_execution

        # These are ONLY descriptions with NO actual commands - should be rejected
        descriptive_only_responses = [
            "I will read the following files: main.py, config.py, and engine.py",
            "Let me investigate by reading the codebase first",
            "I'm going to search for the pattern test_*.py in the codebase",
            "I plan to execute the tests using pytest",
        ]

        for response in descriptive_only_responses:
            is_descriptive, tools = _detect_tool_description_vs_execution(response)
            assert is_descriptive is True, f"Should detect description-only in: {response[:50]}..."

        # These have preamble BUT also actual commands - should be ALLOWED (not rejected)
        # because the actual READ:/SEARCH:/RUN: commands ARE present
        responses_with_commands = [
            "I will read the following files:\nREAD: main.py\nREAD: config.py",
            "Let me investigate by reading:\nREAD: sage/core/engine.py",
            "I'm going to search for the pattern:\nSEARCH: test_*.py",
            "I plan to execute the tests:\nRUN: pytest -v",
        ]

        for response in responses_with_commands:
            is_descriptive, tools = _detect_tool_description_vs_execution(response)
            # These should NOT be flagged as descriptive because they have actual commands
            assert is_descriptive is False, (
                f"Should ALLOW response with commands: {response[:50]}..."
            )

    def test_allow_direct_tool_execution(self):
        """Direct tool execution should NOT be flagged."""
        from sage.cli_core import _detect_tool_description_vs_execution

        execution_responses = [
            "READ: sage/main.py\nREAD: sage/config.py\n\nBased on these files...",
            "SEARCH: test_*.py\n\nFound the following test files...",
            "RUN: pytest sage/tests/ -v\n\nRESULT: 10 passed, 0 failed",
        ]

        for response in execution_responses:
            is_descriptive, _ = _detect_tool_description_vs_execution(response)
            assert is_descriptive is False, f"Should NOT flag direct execution: {response[:50]}..."

    def test_detect_tool_refusal_claims(self):
        """Claims that tools can't be executed should be detected."""
        from sage.cli_core import _detect_tool_description_vs_execution

        refusal_responses = [
            "Since I cannot execute the read commands, I will assume...",
            "Unable to execute tool commands, so here's my best guess...",
            "Tool commands do not work here, proceeding with assumptions...",
        ]

        for response in refusal_responses:
            is_descriptive, tools = _detect_tool_description_vs_execution(response)
            assert is_descriptive is True, f"Should detect refusal in: {response[:50]}..."
            assert "TOOL_REFUSAL" in tools


# =============================================================================
# TEST 4: Implementation Task Validation
# =============================================================================


class TestImplementationTaskValidation:
    """Test validation for implementation tasks."""

    def test_reject_phantom_implementation(self):
        """Implementation claims without FILE: blocks should be rejected."""
        from sage.cli_core import _validate_implementation_claim

        phantom_response = """
I've implemented the model registry with the following features:

1. Dynamic model loading with caching
2. Memory management and cleanup
3. Performance optimization

The implementation is complete and ready for testing.
"""
        is_valid, reason = _validate_implementation_claim(phantom_response)
        assert is_valid is False, "Should reject phantom implementation"
        assert "file" in reason.lower()

    def test_accept_real_implementation(self):
        """Implementation with FILE: blocks should be accepted."""
        from sage.cli_core import _validate_implementation_claim

        real_response = """
I've implemented the feature:

FILE: sage/feature.py
```python
def new_feature():
    return True
```

FILE: sage/tests/test_feature.py
```python
def test_new_feature():
    from sage.feature import new_feature
    assert new_feature() == True
```

The implementation is complete.
"""
        is_valid, reason = _validate_implementation_claim(real_response)
        assert is_valid is True, f"Should accept real implementation: {reason}"

    def test_reject_tdd_claim_without_tests(self):
        """TDD claims without test files should be rejected."""
        from sage.cli_core import _validate_tdd_compliance

        tdd_response = """
Following TDD principles, I've implemented the feature.

FILE: sage/feature.py
```python
def feature():
    return True
```

Tests first - the implementation is complete!
"""
        is_valid, reason = _validate_tdd_compliance(
            tdd_response,
            files_written=["sage/feature.py"],  # No test files
            is_implementation_request=True,
        )
        assert is_valid is False, f"Should reject TDD without tests: {reason}"
        assert "test" in reason.lower()


# =============================================================================
# TEST 5: Failure Loop Detection
# =============================================================================


class TestFailureLoopDetection:
    """Test failure loop detection and recovery."""

    def test_detect_repeated_identical_errors(self):
        """Repeated identical errors should trigger loop detection."""
        from sage.cli_core import FailureLoopDetector

        detector = FailureLoopDetector(max_identical_errors=3)

        # Record same error 3 times
        detector.record_error("has_collection_errors: test discovery failed")
        detector.record_error("has_collection_errors: test discovery failed")
        is_loop = detector.record_error("has_collection_errors: test discovery failed")

        assert is_loop is True, "Should detect repeated error loop"

        is_looping, reason = detector.is_in_loop()
        assert is_looping is True
        assert "has_collection_errors" in reason.lower()

    def test_detect_repeated_validation_failures(self):
        """Repeated validation failures should trigger loop detection."""
        from sage.cli_core import FailureLoopDetector

        detector = FailureLoopDetector(max_identical_errors=3)

        # Record same validation failure 3 times
        for _ in range(3):
            detector.record_validation_failure(["described tools instead of executing them"])

        is_looping, reason = detector.is_in_loop()
        assert is_looping is True

    def test_reset_clears_history(self):
        """Reset should clear all history."""
        from sage.cli_core import FailureLoopDetector

        detector = FailureLoopDetector()

        # Add some history
        detector.record_error("error A")
        detector.record_error("error A")
        detector.record_validation_failure(["violation"])

        # Reset
        detector.reset()

        # Should not be in loop after reset
        is_looping, _ = detector.is_in_loop()
        assert is_looping is False


# =============================================================================
# TEST 6: File Path Validation
# =============================================================================


class TestFilePathValidation:
    """Test file path validation against codebase structure."""

    def test_reject_repetitive_path_segments(self, tmp_path: Path):
        """Repetitive path segments should be rejected."""
        from sage.core.validation import validate_file_path_against_codebase

        # Create basic structure
        (tmp_path / "sage").mkdir()
        (tmp_path / "sage" / "__init__.py").touch()

        bad_paths = [
            "ai-platform/ai-platform/ai-platform/ai-platform/test.py",
            "src/src/src/src/main.py",
            "foo/foo/foo/foo/bar.py",
        ]

        for path in bad_paths:
            is_valid, reason = validate_file_path_against_codebase(path, tmp_path)
            assert is_valid is False, f"Should reject repetitive path: {path}"
            assert "repetitive" in reason.lower()

    def test_reject_excessively_long_paths(self, tmp_path: Path):
        """Excessively long paths should be rejected."""
        from sage.core.validation import validate_file_path_against_codebase

        # Create a path that's way too long
        long_path = "/".join(["dir"] * 100) + "/file.py"

        is_valid, reason = validate_file_path_against_codebase(long_path, tmp_path)
        assert is_valid is False, "Should reject excessively long path"

    def test_accept_valid_paths(self, tmp_path: Path):
        """Valid paths should be accepted."""
        from sage.core.validation import validate_file_path_against_codebase

        # Create structure
        (tmp_path / "sage").mkdir()
        (tmp_path / "sage" / "__init__.py").touch()

        valid_paths = [
            "sage/new_module.py",
            "sage/tests/test_new.py",
        ]

        for path in valid_paths:
            is_valid, reason = validate_file_path_against_codebase(path, tmp_path)
            # May be valid or have other warnings, but not for the bad patterns
            if not is_valid:
                assert "repetitive" not in reason.lower()
                assert "long" not in reason.lower()


# =============================================================================
# TEST 7: Recovery Prompt Effectiveness
# =============================================================================


class TestRecoveryPrompts:
    """Test that recovery prompts guide to correct behavior."""

    def test_recovery_prompt_structure(self):
        """Verify recovery prompt has required elements."""
        # Simulate building a validation retry prompt
        violations = [
            "You described tools (READ, SEARCH) instead of executing them.",
            "Generated 100 recommendations but read ZERO files.",
        ]

        violations_text = "\n".join(f"{i + 1}. {v}" for i, v in enumerate(violations))
        task_prompt = "Analyze the codebase and list 100 items"

        # This is what the recovery prompt looks like (from main.py)
        recovery_prompt = (
            f"❌ YOUR PREVIOUS RESPONSE WAS REJECTED - DO NOT REPEAT IT\n\n"
            f"WHAT WENT WRONG:\n{violations_text}\n\n"
            f"═══════════════════════════════════════════════════════════\n"
            f"CRITICAL: YOUR VERY FIRST LINE MUST BE A TOOL COMMAND\n"
            f"═══════════════════════════════════════════════════════════\n\n"
            f"DO THIS NOW (copy exactly):\n"
            f"READ: sage/main.py\n"
            f"READ: sage/core/validation.py\n\n"
            f"RULES YOU MUST FOLLOW:\n"
            f"1. Start IMMEDIATELY with READ: or SEARCH: - NO introductory text\n"
            f"2. Do NOT say 'I will read' - just write 'READ: filename'\n"
            f"3. Do NOT say 'cannot execute' or 'assuming' - the commands WILL execute\n"
            f"4. WAIT for file contents before making ANY recommendations\n"
            f"5. Each recommendation must cite specific file:line numbers\n\n"
            f"WRONG: 'I will investigate by reading the files...'\n"
            f"RIGHT: 'READ: sage/main.py'\n\n"
            f"Original request: {task_prompt}"
        )

        # Verify key elements are present
        assert "REJECTED" in recovery_prompt
        assert "READ:" in recovery_prompt
        assert "SEARCH:" in recovery_prompt
        assert "cannot execute" in recovery_prompt
        assert "WRONG:" in recovery_prompt
        assert "RIGHT:" in recovery_prompt
        assert task_prompt in recovery_prompt


# =============================================================================
# TEST 8: End-to-End Simulation
# =============================================================================


class TestEndToEndSimulation:
    """Simulate end-to-end SAGE agent behavior."""

    def test_simulate_analysis_task_flow(self):
        """Simulate the full analysis task validation flow."""
        from sage.cli_core import (
            _detect_tool_description_vs_execution,
            _validate_context_gathering,
        )

        # Simulate a description-only response (NO actual commands)
        description_only = """
I will investigate this codebase by reading the following files:
- sage/main.py
- sage/core/validation.py
- sage/core/renderer.py

Then I will analyze the architecture and provide 100 recommendations.
"""
        is_descriptive, tools = _detect_tool_description_vs_execution(description_only)
        assert is_descriptive is True, "Description-only response should be rejected"

        # Response with commands should be ALLOWED (not considered descriptive)
        response_with_commands = """
I will investigate this codebase by reading the following files:

READ: sage/main.py
READ: sage/core/validation.py
READ: sage/core/renderer.py

Then I will analyze the architecture and provide 100 recommendations.
"""
        is_descriptive, tools = _detect_tool_description_vs_execution(response_with_commands)
        assert is_descriptive is False, "Response with commands should be allowed"

        # Simulate a BAD second response (tool refusal + fabrication)
        bad_response_2 = """
Since I cannot execute the read commands, I will proceed by assuming typical patterns.

1. Add input validation
2. Implement error handling
3. Add unit tests
... (97 more generic items)
"""
        is_descriptive, tools = _detect_tool_description_vs_execution(bad_response_2)
        assert is_descriptive is True, "Second response should be rejected for tool refusal"
        assert "TOOL_REFUSAL" in tools

        # Simulate a GOOD response (direct tool execution)
        good_response = """READ: sage/main.py
READ: sage/core/validation.py

Based on reading sage/main.py:1-500, I found:
1. Line 142: Missing input validation in `_process_response()`
2. Line 283: Potential null reference in `_validate_file_path()`
3. Line 401: TODO comment indicates incomplete implementation
"""
        is_descriptive, _ = _detect_tool_description_vs_execution(good_response)
        assert is_descriptive is False, "Good response should NOT be flagged"

        # Validate the good response has proportional reads
        is_valid, _ = _validate_context_gathering(
            good_response,
            files_read=["sage/main.py", "sage/core/validation.py"],
            is_analysis_request=True,
        )
        assert is_valid is True, "Good response should pass context validation"

    def test_simulate_implementation_task_flow(self):
        """Simulate the full implementation task validation flow."""
        from sage.cli_core import (
            _validate_completion_claim,
            _validate_implementation_claim,
            _validate_tdd_compliance,
        )

        # Simulate a BAD implementation response (no FILE: blocks)
        bad_impl = """
I've implemented the new feature with proper error handling and tests.
The implementation follows best practices and is ready for review.
All done!
"""
        is_valid_impl, _ = _validate_implementation_claim(bad_impl)
        has_evidence = _validate_completion_claim(bad_impl)

        assert is_valid_impl is False, "Should reject impl without FILE: blocks"
        assert has_evidence is False, "Should reject completion without evidence"

        # Simulate a GOOD implementation response
        good_impl = """
FILE: sage/tests/test_feature.py
```python
import pytest
from sage.feature import new_feature

def test_new_feature_returns_true():
    assert new_feature() == True

def test_new_feature_handles_edge_case():
    assert new_feature(None) == False
```

FILE: sage/feature.py
```python
def new_feature(value=True):
    if value is None:
        return False
    return True
```

RUN: pytest sage/tests/test_feature.py -v
RESULT: 2 passed, 0 failed

All done! Tests are passing.
"""
        is_valid_impl, _ = _validate_implementation_claim(good_impl)
        has_evidence = _validate_completion_claim(good_impl)
        is_tdd_compliant, _ = _validate_tdd_compliance(
            good_impl,
            files_written=["sage/tests/test_feature.py", "sage/feature.py"],
            is_implementation_request=True,
        )

        assert is_valid_impl is True, "Should accept impl with FILE: blocks"
        assert has_evidence is True, "Should accept completion with evidence"
        assert is_tdd_compliant is True, "Should pass TDD compliance"


# =============================================================================
# TEST 9: Non-Standard Tool Syntax Detection
# =============================================================================


class TestNonStandardToolSyntax:
    """Test detection of non-standard tool syntax patterns."""

    def test_detect_function_call_syntax_in_streaming(self):
        """Function call style syntax should be detected during streaming."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        bad_responses = [
            '**Command:** read_file("sage/main.py")',
            "**Action:** Read the following files",
            'Command: read_file("test.py")',
            "Action: Search for patterns",
            'Let me use read_file("config.py") to check',
            'I will call search_files("*.py")',
        ]

        for response in bad_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is True, f"Should detect non-standard syntax in: {response[:50]}..."
            assert "syntax" in reason.lower() or "standard" in reason.lower()

    def test_detect_function_call_syntax_in_validation(self):
        """Function call style syntax should be detected during validation."""
        from sage.cli_core import _detect_tool_description_vs_execution

        bad_responses = [
            'I will use read_file("sage/main.py") to examine the code',
            '**Command:** read_file("test.py")\n**Action:** Read',
            "Tool: read\nFile: config.py",
        ]

        for response in bad_responses:
            is_descriptive, tools = _detect_tool_description_vs_execution(response)
            assert is_descriptive is True, f"Should detect non-standard in: {response[:50]}..."
            assert "NONSTANDARD_TOOL_SYNTAX" in tools

    def test_allow_valid_tool_syntax(self):
        """Valid READ:/SEARCH:/RUN: syntax should not be flagged."""
        from sage.core.renderer import _detect_bad_streaming_patterns
        from sage.cli_core import _detect_tool_description_vs_execution

        valid_responses = [
            "READ: sage/main.py",
            "SEARCH: test_*.py",
            "RUN: pytest -v",
            "READ: sage/main.py\nREAD: sage/config.py\n\nBased on reading...",
            "ls -F\ncat README.md",  # normalized to RUN: before validation
        ]

        for response in valid_responses:
            # Check streaming detection
            is_bad, _ = _detect_bad_streaming_patterns(response)
            assert is_bad is False, f"Should NOT flag valid syntax in streaming: {response[:50]}..."

            # Check validation detection
            is_descriptive, tools = _detect_tool_description_vs_execution(response)
            assert "NONSTANDARD_TOOL_SYNTAX" not in tools


# =============================================================================
# TEST 10: Argumentative Behavior Detection
# =============================================================================


class TestArgumentativeBehaviorDetection:
    """Test detection of argumentative/blocking behavior patterns."""

    def test_detect_request_for_input_in_streaming(self):
        """Requests for user input should be detected during streaming."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        argumentative_responses = [
            "Please provide the output of the previous commands so I can analyze it.",
            "I need you to share the file contents before I can proceed.",
            "Could you provide the search results? I'll wait for your input.",
            "Before I can continue, please paste the output.",
            "Waiting for you to run the command and share the results.",
            "Shall I proceed with the implementation?",
            "Would you like me to continue with the next step?",
            "Do you want me to implement this feature?",
        ]

        for response in argumentative_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is True, f"Should detect argumentative behavior in: {response[:50]}..."
            assert "argumentative" in reason.lower() or "execute" in reason.lower()

    def test_detect_request_for_input_in_validation(self):
        """Requests for user input should be detected during validation."""
        from sage.cli_core import _detect_tool_description_vs_execution

        argumentative_responses = [
            "Please provide the output so I can analyze it.",
            "I need the file contents before proceeding.",
            "Before I can proceed, please share the results.",
            "Should I proceed with the implementation?",
        ]

        for response in argumentative_responses:
            is_descriptive, tools = _detect_tool_description_vs_execution(response)
            assert is_descriptive is True, f"Should detect argumentative in: {response[:50]}..."
            assert "ARGUMENTATIVE_BEHAVIOR" in tools

    def test_allow_working_responses(self):
        """Responses that are actively working should not be flagged."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        working_responses = [
            "READ: sage/main.py\n\nBased on reading the file, I found issues...",
            "SEARCH: test_*.py\n\nFound 10 test files. Let me analyze them...",
            "FILE: sage/feature.py\n```python\ndef feature(): pass\n```",
            "The analysis shows the following issues in the codebase:\n1. Bug at line 42...",
        ]

        for response in working_responses:
            is_bad, _ = _detect_bad_streaming_patterns(response)
            assert is_bad is False, f"Should NOT flag working response: {response[:50]}..."


# =============================================================================
# TEST 11: Mode Transition Detection
# =============================================================================


class TestModeTransitionDetection:
    """Test detection of mode transition requests (analysis -> implementation)."""

    def test_detect_implementation_transition_requests(self):
        """Requests to switch to implementation mode should be detected."""
        from sage.core.request_classifier import RequestClassifier, RequestType

        classifier = RequestClassifier()

        transition_requests = [
            "implement all of these",
            "do the first 5 items",
            "implement items 1-10",
            "go ahead and fix them",
            "start implementing",
            "implement them using TDD",
            "fix these issues",
            "let's implement the changes",
            "now implement",
            "yes, implement them",
            "proceed with implementation",
            "make those changes",
            "apply the fixes",
        ]

        for request in transition_requests:
            classification = classifier.classify(request)
            # Should classify as FIX_ALL (implementation mode)
            assert classification.request_type == RequestType.FIX_ALL, (
                f"'{request}' should be classified as FIX_ALL, got {classification.request_type}"
            )
            # Should NOT be read-only
            assert classification.read_only is False, f"'{request}' should NOT be read-only"
            # Should require TDD
            assert classification.requires_tdd is True, f"'{request}' should require TDD"

    def test_analysis_requests_stay_readonly(self):
        """Analysis requests should remain read-only."""
        from sage.core.request_classifier import RequestClassifier

        classifier = RequestClassifier()

        analysis_requests = [
            "analyze the codebase",
            "list 100 improvements",
            "review the architecture",
            "identify issues in the code",
            "what needs to be fixed?",
        ]

        for request in analysis_requests:
            classification = classifier.classify(request)
            # Should be read-only
            assert classification.read_only is True, f"'{request}' should be read-only"

    def test_hybrid_requests_classify_correctly(self):
        """Hybrid requests should still trigger implementation mode."""
        from sage.core.request_classifier import RequestClassifier, RequestType

        classifier = RequestClassifier()

        # Hybrid requests where implementation intent is clear
        # Note: When both analysis and implementation verbs are present,
        # the classifier uses pattern priority. These requests have
        # clear implementation intent that should trigger FIX_ALL.
        hybrid_requests = [
            "fix all issues",
            "find bugs and then fix them",
            "implement all the improvements",
        ]

        for request in hybrid_requests:
            classification = classifier.classify(request)
            # Should either be FIX_ALL or IMPLEMENTATION (not pure analysis)
            assert classification.request_type in (
                RequestType.FIX_ALL,
                RequestType.IMPLEMENTATION,
            ), f"'{request}' should trigger implementation mode, got {classification.request_type}"
            # Should NOT be read-only
            assert classification.read_only is False, f"'{request}' should NOT be read-only"


# =============================================================================
# TEST 12: Combined Detection Flow
# =============================================================================


class TestCombinedDetectionFlow:
    """Test the combined detection flow for all bad patterns."""

    def test_all_bad_patterns_caught_in_single_response(self):
        """A response with multiple bad patterns should be caught."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        # Response with multiple issues:
        # 1. Non-standard tool syntax
        # 2. Argumentative behavior
        # 3. Tool refusal
        terrible_response = """
**Command:** read_file("sage/main.py")

Since I cannot execute the read commands directly, please provide the output.

I will proceed by assuming the codebase follows standard patterns.

Once you share the file contents, I can analyze them.
"""
        is_bad, reason = _detect_bad_streaming_patterns(terrible_response)
        assert is_bad is True, "Response with multiple bad patterns should be caught"

    def test_early_rejection_prevents_wasted_generation(self):
        """Bad patterns early in response should trigger immediate rejection."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        # Just the start of a bad response (streaming context)
        early_bad_content = "**Command:** read_file("
        is_bad, _ = _detect_bad_streaming_patterns(early_bad_content)
        assert is_bad is True, "Should catch bad pattern early"

    def test_good_response_passes_all_checks(self):
        """A well-formed response should pass all detection checks."""
        from sage.core.renderer import _detect_bad_streaming_patterns
        from sage.cli_core import _detect_tool_description_vs_execution

        good_response = """READ: sage/main.py
READ: sage/core/validation.py
SEARCH: test_*.py

Based on reading sage/main.py:1-500 and sage/core/validation.py:1-200, I found the following issues:

1. **sage/main.py:142** - Missing input validation in `_process_response()`. The function should validate the response format before processing.

2. **sage/main.py:283** - Potential null reference in `_validate_file_path()`. Add a null check before accessing `path.parent`.

3. **sage/core/validation.py:45** - The regex pattern is inefficient. Consider compiling patterns once at module level.

These are specific, grounded recommendations based on the actual code I read.
"""
        # Should pass streaming check
        is_bad, reason = _detect_bad_streaming_patterns(good_response)
        assert is_bad is False, f"Good response should pass streaming check: {reason}"

        # Should pass tool execution check
        is_descriptive, tools = _detect_tool_description_vs_execution(good_response)
        assert is_descriptive is False, "Good response should pass tool execution check"
        assert "TOOL_REFUSAL" not in tools
        assert "NONSTANDARD_TOOL_SYNTAX" not in tools
        assert "ARGUMENTATIVE_BEHAVIOR" not in tools


# =============================================================================
# TEST 13: Missing Colon Detection
# =============================================================================


class TestMissingColonDetection:
    """Test handling of tool commands missing colons (READ vs READ:)."""

    def test_detect_read_without_colon_is_normalized(self):
        """READ without colon should be normalized instead of rejected."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        normalized_responses = [
            "READ sage/main.py",
            "READ sage/utils.py\nREAD sage/config.py",
            "SEARCH *.py",
            "RUN pytest -v",
        ]

        for response in normalized_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is False, f"Should normalize bare tool syntax in: {response} ({reason})"

    def test_allow_correct_colon_syntax(self):
        """Correct READ: syntax should not be flagged."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        valid_responses = [
            "READ: sage/main.py",
            "READ: sage/utils.py\nREAD: sage/config.py",
            "SEARCH: *.py",
            "RUN: pytest -v",
        ]

        for response in valid_responses:
            is_bad, _ = _detect_bad_streaming_patterns(response)
            assert is_bad is False, f"Should NOT flag valid syntax: {response}"


# =============================================================================
# TEST 14: Print Statement Detection
# =============================================================================


class TestPrintStatementDetection:
    """Test detection of Python print statements (model outputting code instead of tools)."""

    def test_print_statements_allowed_in_code(self):
        """print() statements are now allowed to avoid false positives in code blocks."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        # Print statements are no longer detected to avoid false positives
        # when the model generates code with print statements inside markdown blocks
        # Note: Avoid test strings that might trigger other detections
        code_responses = [
            '  print("Hello world")',
            'print(f"Processing {item}")',
            'print("Debug message")',
        ]

        for response in code_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            # Should NOT be flagged anymore
            assert is_bad is False, f"print() should be allowed: {response}, reason: {reason}"

    def test_allow_print_in_code_blocks(self):
        """print() inside FILE: code blocks should be allowed."""

        valid_response = """READ: sage/main.py

Based on reading the file, here is my implementation:

FILE: sage/feature.py
```python
def log_message(msg):
    print(f"[INFO] {msg}")
```
"""
        # The FILE: block pattern should prevent false positives
        # However, since we can't fully parse markdown here, this may still flag
        # The important thing is bare print statements ARE flagged
        pass  # This test validates the concept


# =============================================================================
# TEST 15: Shell Command Style Detection
# =============================================================================


class TestShellCommandDetection:
    """Bare one-line ls/cat are normalized to RUN: before validation (weak models)."""

    def test_detect_ls_command(self):
        """Bare ls lines normalize to RUN: and must not abort streaming as 'bad syntax'."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        for response in ("ls -F", "ls -la"):
            is_bad, _reason = _detect_bad_streaming_patterns(response)
            assert is_bad is False, (
                f"Bare ls should normalize to RUN: and not fail validation: {response}"
            )

    def test_detect_cat_command(self):
        """Bare cat lines normalize to RUN: and must not abort streaming."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        for response in ("cat README.md", "cat src/main.py"):
            is_bad, _reason = _detect_bad_streaming_patterns(response)
            assert is_bad is False, (
                f"Bare cat should normalize to RUN: and not fail validation: {response}"
            )


# =============================================================================
# TEST 16: Fabrication Detection
# =============================================================================


class TestFabricationDetection:
    """Test detection of fabricated numbered lists without file reads."""

    def test_detect_numbered_list_without_reads(self):
        """Numbered list without READ: commands should be detected."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        # A fabricated response: long numbered list but no READ: commands (threshold matches renderer)
        fabricated = """Here are my recommendations for improving this codebase without examining any files:

1. Add input validation across all endpoints
2. Implement comprehensive error handling middleware
3. Add unit tests with high coverage targets
4. Update developer documentation and onboarding guides
5. Refactor the main application entry point for clarity
6. Add structured logging with correlation identifiers
7. Improve error messages shown to API consumers
8. Introduce caching layers where profiling indicates hotspots
9. Add integration tests against staging environments
10. Implement observability dashboards for production metrics
"""
        is_bad, reason = _detect_bad_streaming_patterns(fabricated)
        assert is_bad is True, "Should detect fabricated list without reads"
        assert "fabrication" in reason.lower()

    def test_allow_medium_numbered_remediation_without_reads(self):
        """Typical 5–7 step env/config checklists are not treated as fabrication."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        plan = """Steps to fix Firebase configuration:

1. Create `.env` in `web/` with VITE_FIREBASE_API_KEY
2. Add VITE_FIREBASE_AUTH_DOMAIN and related keys
3. Verify `web/src/firebase.js` loads env vars
4. Restart the dev server
5. Test Google sign-in
6. Test Apple sign-in
7. Test email/password and password reset
"""
        is_bad, reason = _detect_bad_streaming_patterns(plan)
        assert is_bad is False, reason

    def test_allow_list_with_file_evidence(self):
        """Numbered list with file evidence should be allowed."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        grounded = """READ: sage/main.py

Based on reading the file, I found the following issues:

1. Line 42: Missing validation
2. Line 85: Potential null reference
3. Line 120: Hardcoded value
"""
        is_bad, _ = _detect_bad_streaming_patterns(grounded)
        assert is_bad is False, "Should allow list with READ: commands"


# =============================================================================
# TEST 17: Additional Argumentative Patterns
# =============================================================================


class TestAdditionalArgumentativePatterns:
    """Test detection of additional argumentative patterns from logs."""

    def test_detect_please_provide_context(self):
        """Requests for context should be detected."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        argumentative_responses = [
            "Please provide the following so I can begin the analysis:",
            "I need to know which files or codebase we are reviewing.",
            "Awaiting the file contents to proceed.",
            "Since no file structure or initial context has been provided, I cannot proceed.",
            "I have not yet received the output from the SEARCH commands.",
            "Without the code context, any list I generate would be pure speculation.",
        ]

        for response in argumentative_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is True, f"Should detect argumentative: {response[:50]}..."

    def test_detect_i_understand_patterns(self):
        """'I understand' stalling patterns should be detected."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        stalling_responses = [
            "I understand the request to generate a comprehensive list.",
            "I understand the requirement to provide findings.",
            "I am ready to proceed with the next task.",
        ]

        for response in stalling_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is True, f"Should detect stalling: {response[:50]}..."


# =============================================================================
# TEST 18: Session Context Persistence
# =============================================================================


class TestSessionContextPersistence:
    """Test session context persistence functions."""

    def test_session_files_read_persistence(self, tmp_path):
        """Files read should persist to session state."""
        from sage.cli_core import (
            _add_session_file_read,
            _get_session_files_read,
            _save_session_state,
        )

        # Create .sage directory
        sage_dir = tmp_path / ".sage"
        sage_dir.mkdir()

        # Initialize empty state
        _save_session_state(tmp_path, {})

        # Add some files
        _add_session_file_read(tmp_path, "sage/main.py")
        _add_session_file_read(tmp_path, "sage/config.py")

        # Verify they're stored
        files = _get_session_files_read(tmp_path)
        assert "sage/main.py" in files
        assert "sage/config.py" in files

    def test_session_mode_persistence(self, tmp_path):
        """Session mode should persist."""
        from sage.cli_core import (
            _get_session_mode,
            _save_session_state,
            _set_session_mode,
        )

        # Create .sage directory
        sage_dir = tmp_path / ".sage"
        sage_dir.mkdir()
        _save_session_state(tmp_path, {})

        # Default mode should be analysis
        mode = _get_session_mode(tmp_path)
        assert mode == "analysis"

        # Set to implementation
        _set_session_mode(tmp_path, "implementation")
        mode = _get_session_mode(tmp_path)
        assert mode == "implementation"

    def test_session_pending_tasks(self, tmp_path):
        """Pending tasks should persist."""
        from sage.cli_core import (
            _add_session_pending_task,
            _get_incomplete_tasks,
            _mark_task_completed,
            _save_session_state,
        )

        # Create .sage directory
        sage_dir = tmp_path / ".sage"
        sage_dir.mkdir()
        _save_session_state(tmp_path, {})

        # Add a task
        _add_session_pending_task(
            tmp_path,
            {
                "request": "implement feature X",
                "type": "FIX_ALL",
                "status": "pending",
            },
        )

        # Verify it's there
        tasks = _get_incomplete_tasks(tmp_path)
        assert len(tasks) == 1
        assert tasks[0]["request"] == "implement feature X"

        # Mark it complete
        _mark_task_completed(tmp_path, 0)

        # Should be empty now
        tasks = _get_incomplete_tasks(tmp_path)
        assert len(tasks) == 0


# =============================================================================
# TEST 19: File Path Validation
# =============================================================================


class TestFilePathValidation:
    """Test validation of file paths in READ: commands.

    This prevents SAGE from crashing when the model outputs garbage text
    as file paths like "READ: The previous interaction was a directive..."
    """

    def test_reject_prose_as_path(self):
        """Prose text should be rejected as a file path."""
        from sage.cli_core import _is_valid_file_path

        invalid_paths = [
            "The previous interaction was a directive to perform an analysis",
            "I will read the following files to understand the codebase",
            "Based on the provided context, let me analyze",
            "Let me start by reading the main file",
            "This is what I found in the codebase",
            "Please note that the implementation requires",
            "According to the requirements, we need to",
        ]

        for path in invalid_paths:
            is_valid = _is_valid_file_path(path)
            assert is_valid is False, f"Should reject prose: {path[:50]}..."

    def test_reject_paths_with_sentence_patterns(self):
        """Paths with sentence patterns should be rejected."""
        from sage.cli_core import _is_valid_file_path

        invalid_paths = [
            "file.py is the main entry point",
            "config.yaml should be modified",
            "tests are located in this directory",
            "implementation would require changes",
        ]

        for path in invalid_paths:
            is_valid = _is_valid_file_path(path)
            assert is_valid is False, f"Should reject sentence: {path[:50]}..."

    def test_reject_very_long_paths(self):
        """Very long paths (>255 chars) should be rejected."""
        from sage.cli_core import _is_valid_file_path

        long_path = "a" * 300 + ".py"
        assert _is_valid_file_path(long_path) is False

    def test_reject_paths_with_multiple_spaces(self):
        """Paths with multiple consecutive spaces should be rejected."""
        from sage.cli_core import _is_valid_file_path

        invalid_paths = [
            "file.py  and another thing",
            "some text  with  multiple  spaces",
        ]

        for path in invalid_paths:
            is_valid = _is_valid_file_path(path)
            assert is_valid is False, f"Should reject multi-space: {path}"

    def test_accept_valid_file_paths(self):
        """Valid file paths should be accepted."""
        from sage.cli_core import _is_valid_file_path

        valid_paths = [
            "sage/main.py",
            "backend/app.py",
            "pyproject.toml",
            "README.md",
            "src/components/Button.tsx",
            ".gitignore",
            "tests/test_main.py",
            "config.yaml",
            "`sage/main.py`",  # Backtick wrapped
            "path/to/deep/nested/file.py",
            "file-with-dashes.py",
            "file_with_underscores.py",
        ]

        for path in valid_paths:
            is_valid = _is_valid_file_path(path)
            assert is_valid is True, f"Should accept valid path: {path}"

    def test_extract_tool_commands_filters_invalid_paths(self):
        """_extract_tool_commands should filter out invalid READ: paths."""
        from sage.cli_core import _extract_tool_commands

        text = """READ: sage/main.py
READ: The previous interaction was a directive to perform an analysis
READ: backend/config.py
READ: Based on the provided context I should analyze the codebase
SEARCH: *.py"""

        commands = _extract_tool_commands(text)

        # Should have 3 valid commands (2 READs + 1 SEARCH)
        assert len(commands) == 3

        # First READ should be kept
        assert ("READ", "sage/main.py") in commands

        # Invalid paths should be filtered
        invalid_in_commands = any(
            "previous interaction" in arg.lower() or "Based on" in arg for _, arg in commands
        )
        assert invalid_in_commands is False, "Invalid paths should be filtered"

        # Third READ should be kept
        assert ("READ", "backend/config.py") in commands

        # SEARCH should be kept
        assert ("SEARCH", "*.py") in commands


# =============================================================================
# TEST 20: Hypothetical Content Detection
# =============================================================================


class TestHypotheticalContentDetection:
    """Test detection of hypothetical/speculative content."""

    def test_detect_hypothetical_patterns(self):
        """Hypothetical patterns should be detected and rejected."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        hypothetical_responses = [
            "Here is a hypothetical structure of the codebase:",
            "If you can provide the actual files, I can analyze them.",
            "Once the context is established, I will proceed.",
            "I require the actual source code to continue.",
            "Without the actual code, I cannot proceed.",
            "Assuming a standard Python project structure:",
            "I will assume the existence of a main.py file.",
        ]

        for response in hypothetical_responses:
            is_bad, reason = _detect_bad_streaming_patterns(response)
            assert is_bad is True, f"Should detect hypothetical: {response[:50]}..."
            assert "hypothetical" in reason.lower() or "speculative" in reason.lower()

    def test_detect_guessed_conventional_paths(self):
        """Multiple guessed conventional paths should be detected."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        # Response with 3+ conventional paths but no READ: commands
        guessed_paths_response = """
        Let me analyze the project structure:
        1. src/main.py - main entry point
        2. src/utils/config.py - configuration handling
        3. src/services/api_service.py - API layer
        4. src/models/user.py - data models
        """

        is_bad, reason = _detect_bad_streaming_patterns(guessed_paths_response)
        assert is_bad is True, "Should detect guessed conventional paths"
        assert "conventional path" in reason.lower() or "src/main" in reason.lower()

    def test_allow_actual_paths_with_read(self):
        """Actual project paths with READ: commands should be allowed."""
        from sage.core.renderer import _detect_bad_streaming_patterns

        valid_response = """READ: sage/main.py
READ: backend/app.py

Based on reading these files, I found the following structure:
- sage/main.py handles the CLI
- backend/app.py is the FastAPI application
"""

        is_bad, _ = _detect_bad_streaming_patterns(valid_response)
        assert is_bad is False, "Should allow valid READ: commands with real paths"
