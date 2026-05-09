"""TDD tests for SAGE behavioral bugs identified from sage run analysis.

This test file covers critical behavioral issues where SAGE:
1. Describes tools instead of executing them (outputs "I will READ:" as text)
2. Generates filler/repetitive content without actual analysis
3. Claims it lacks context but doesn't use READ: to get it
4. Violates read-only mode by generating implementation suggestions
5. Doesn't detect responses with repeated boilerplate items

Run with: pytest sage/tests/test_sage_behavioral_fixes.py -v
"""

from __future__ import annotations

import pytest

# =============================================================================
# BUG-1: Model describes tools instead of executing them
# =============================================================================


class TestToolExecutionDetection:
    """Tests that SAGE detects when model describes tools vs executes them."""

    def test_detect_descriptive_tool_mentions(self):
        """Should detect when model ONLY describes tools without executing them."""
        from sage.main import _detect_tool_description_vs_execution

        # Model ONLY describing what it WILL do - no actual tool commands (bug)
        # This is the problematic case: talking ABOUT tools without using them
        descriptive_response = """
I will investigate this by reading the following files:

- ai-platform/backend/app.py
- ai-platform/backend/config.py
- ai-platform/sage/main.py

Then I will analyze the architecture and run the tests.
"""

        is_descriptive, mentioned_tools = _detect_tool_description_vs_execution(
            descriptive_response
        )

        # Pure description without actual tool commands should be flagged
        assert is_descriptive is True, "Pure description without tool commands should be flagged"

    def test_detect_actual_tool_execution(self):
        """Should recognize when model actually executes tools."""
        from sage.main import _detect_tool_description_vs_execution

        # Model actually executing (correct)
        execution_response = """
READ: ai-platform/backend/app.py
READ: ai-platform/backend/config.py

Based on the files above, I can see...
"""

        is_descriptive, mentioned_tools = _detect_tool_description_vs_execution(execution_response)

        # Should NOT be flagged as descriptive because tools are at start
        assert is_descriptive is False

    def test_detect_mixed_description_and_execution(self):
        """Should allow preamble when actual tool commands are present."""
        from sage.main import _detect_tool_description_vs_execution

        # Preamble followed by actual tool commands is ACCEPTABLE
        # The tool commands will actually execute
        mixed_response = """
I need to read these files first:

READ: ai-platform/backend/app.py
READ: ai-platform/backend/config.py

And then execute:

RUN: pytest tests/
"""

        is_descriptive, mentioned_tools = _detect_tool_description_vs_execution(mixed_response)

        # Preamble + actual commands is allowed - commands will execute
        assert is_descriptive is False, "Preamble with actual commands should not be flagged"
        assert "READ" in mentioned_tools
        assert "RUN" in mentioned_tools


# =============================================================================
# BUG-2: Model generates filler/repetitive content
# =============================================================================


class TestFillerContentDetection:
    """Tests that SAGE detects repetitive filler content."""

    def test_detect_repetitive_list_items(self):
        """Should detect when model generates repetitive boilerplate items."""
        from sage.main import _detect_repetitive_filler

        # Example from the log: items 13-50 are all "Implement basic logging for X"
        filler_response = """
13. Implement basic logging for debugging information.
14. Implement basic logging for informational messages.
15. Implement basic logging for tracing requests.
16. Implement basic logging for performance metrics.
17. Implement basic logging for security events.
18. Implement basic logging for audit trails.
19. Implement basic logging for user actions.
20. Implement basic logging for system changes.
"""

        is_filler, repetition_score = _detect_repetitive_filler(filler_response)

        assert is_filler is True
        assert repetition_score > 0.7  # High repetition score

    def test_allow_legitimate_varied_content(self):
        """Should allow legitimate varied recommendations."""
        from sage.main import _detect_repetitive_filler

        varied_response = """
1. Fix authentication bypass in terminal WebSocket
2. Implement rate limiting for API endpoints
3. Add input validation for file paths
4. Refactor the context management module
5. Optimize database query performance
"""

        is_filler, repetition_score = _detect_repetitive_filler(varied_response)

        assert is_filler is False
        assert repetition_score < 0.5  # Low repetition score

    def test_detect_template_repetition(self):
        """Should detect template-based repetition patterns."""
        from sage.main import _detect_repetitive_filler

        template_response = """
1. Implement X for Y.
2. Implement X for Z.
3. Implement X for A.
4. Implement X for B.
5. Implement X for C.
6. Implement X for D.
"""

        is_filler, repetition_score = _detect_repetitive_filler(template_response)

        assert is_filler is True


# =============================================================================
# BUG-3: Model claims it lacks context but doesn't use READ:
# =============================================================================


class TestContextGatheringValidation:
    """Tests that SAGE enforces context gathering when model claims it lacks info."""

    def test_detect_claims_without_reads(self):
        """Should detect when model claims no context but doesn't read files."""
        from sage.main import _validate_context_gathering

        no_context_claim = """
I cannot provide specific recommendations without reading the actual code.

Here are general suggestions:
1. Implement input validation
2. Add error handling
...
"""

        files_read = []  # No files were read

        is_valid, reason = _validate_context_gathering(
            no_context_claim, files_read, is_analysis_request=True
        )

        assert is_valid is False
        assert "claimed lack of context" in reason.lower()
        assert "no files read" in reason.lower()

    def test_allow_claims_with_actual_reads(self):
        """Should allow context claims when model actually read files."""
        from sage.main import _validate_context_gathering

        claim_with_reads = """
Based on the files I've read, here are specific recommendations...
"""

        files_read = ["backend/app.py", "sage/main.py"]

        is_valid, _ = _validate_context_gathering(
            claim_with_reads, files_read, is_analysis_request=True
        )

        assert is_valid is True

    def test_detect_no_file_references_claim(self):
        """Should detect 'no file references available' without reads."""
        from sage.main import _validate_context_gathering

        # From the log
        response = """
| 96. | Implement feature X | No file references available without prior context. |
| 97. | Implement feature Y | No file references available without prior context. |
"""

        files_read = []

        is_valid, reason = _validate_context_gathering(
            response, files_read, is_analysis_request=True
        )

        assert is_valid is False
        assert "no file references" in reason.lower()

    def test_fail_closed_uncertainty_then_specifics(self):
        """P1-B: Model that admits uncertainty then gives specifics should fail closed."""
        from sage.main import _validate_context_gathering

        # Model admits it doesn't know, then gives specific recommendations anyway
        response = """
I don't have access to the actual codebase, but here are my recommendations:

1. Fix the authentication bug in backend/auth.py line 45
2. Add rate limiting to api/routes.py
3. Update the database schema in models/user.py
"""

        files_read = []  # No files were actually read

        is_valid, reason = _validate_context_gathering(
            response, files_read, is_analysis_request=True
        )

        # Should FAIL because model claimed no access but gave specific file references
        assert is_valid is False
        assert "no files read" in reason.lower() or "lack" in reason.lower()

    def test_fail_closed_speculative_audit(self):
        """P1-B: Speculative audit without evidence should fail closed."""
        from sage.main import _validate_context_gathering

        # Model produces "audit" without reading anything
        response = """
After analyzing the codebase, I found these critical issues:

1. SQL injection vulnerability in database.py
2. Missing input validation in forms.py
3. Hardcoded credentials in config.py
"""

        files_read = []  # No files were actually read

        is_valid, reason = _validate_context_gathering(
            response, files_read, is_analysis_request=True
        )

        # Should FAIL because no evidence backs the claims
        assert is_valid is False


# =============================================================================
# BUG-4: Model violates read-only mode
# =============================================================================


class TestReadOnlyModeEnforcement:
    """Tests that SAGE enforces read-only mode constraints."""

    def test_detect_implementation_in_analysis_request(self):
        """Should detect when model suggests implementation in analysis mode."""
        from sage.main import _validate_readonly_mode

        # User asked for analysis, model suggests implementation
        user_request = "Analyze the codebase and list 100 items that should be improved"

        response = """
1. Implement authentication flow using OAuth 2.0 standards.
2. Design the core data model schema for user profiles.
3. Develop basic CRUD operations for core entities.
"""

        is_compliant, reason = _validate_readonly_mode(
            response, user_request, is_analysis_request=True
        )

        assert is_compliant is False
        assert "implementation" in reason.lower() or "read-only" in reason.lower()

    def test_allow_analysis_in_analysis_request(self):
        """Should allow proper analysis without implementation."""
        from sage.main import _validate_readonly_mode

        user_request = "Analyze the codebase and list 100 items that should be improved"

        response = """
After analyzing the codebase, here are the improvement areas:

1. Authentication module lacks rate limiting
2. Database queries are not optimized
3. Error handling is inconsistent across modules
"""

        is_compliant, _ = _validate_readonly_mode(response, user_request, is_analysis_request=True)

        assert is_compliant is True

    def test_detect_imperative_verbs_in_analysis(self):
        """Should detect imperative implementation verbs in analysis mode."""
        from sage.main import _validate_readonly_mode

        user_request = "What needs to be fixed in the auth system?"

        response = """
1. Implement OAuth 2.0 authentication
2. Add JWT token validation
3. Create refresh token rotation
"""

        is_compliant, reason = _validate_readonly_mode(
            response, user_request, is_analysis_request=True
        )

        assert is_compliant is False
        # Should detect imperative verbs: "Implement", "Add", "Create"


# =============================================================================
# BUG-5: Model generates responses without proper tool usage
# =============================================================================


class TestToolUsageValidation:
    """Tests that SAGE validates tool usage in responses."""

    def test_reject_analysis_without_file_reads(self):
        """Should reject analysis responses that don't read any files."""
        from sage.main import _validate_tool_usage_for_analysis

        response = """
Here are 100 improvements for the codebase:

1. Improve authentication
2. Add logging
3. Optimize queries
... (97 more items)
"""

        files_read = []
        search_executed = False

        is_valid, reason = _validate_tool_usage_for_analysis(
            response,
            files_read=files_read,
            search_executed=search_executed,
            num_recommendations=100,
        )

        assert is_valid is False
        assert "no files read" in reason.lower() or "no analysis performed" in reason.lower()

    def test_allow_analysis_with_file_reads(self):
        """Should allow analysis that actually read files."""
        from sage.main import _validate_tool_usage_for_analysis

        response = """
Based on analyzing the codebase (10 files read), here are improvements:

1. In backend/app.py: Add rate limiting to API endpoints
2. In sage/main.py: Refactor tool execution loop for clarity
3. In backend/auth.py: Fix authentication bypass vulnerability
"""

        files_read = ["backend/app.py", "sage/main.py", "backend/auth.py"]

        is_valid, _ = _validate_tool_usage_for_analysis(
            response, files_read=files_read, search_executed=False, num_recommendations=3
        )

        assert is_valid is True

    def test_require_proportional_analysis_effort(self):
        """Should require analysis effort proportional to request size."""
        from sage.main import _validate_tool_usage_for_analysis

        # User asked for 100 items but only 2 files read
        response = "Here are 100 improvements..."

        files_read = ["file1.py", "file2.py"]

        is_valid, reason = _validate_tool_usage_for_analysis(
            response, files_read=files_read, search_executed=False, num_recommendations=100
        )

        assert is_valid is False
        # Should detect insufficient analysis (only 2 files for 100 items)


# =============================================================================
# Integration Tests
# =============================================================================


class TestSageBehavioralIntegrity:
    """Integration tests for SAGE behavioral fixes."""

    def test_full_analysis_request_validation(self):
        """Should validate entire analysis request flow."""
        from sage.main import _validate_analysis_response

        user_request = "Analyze the codebase and list 100 items that should be improved"

        # Bad response: describes tools, generates filler, no reads
        bad_response = """
I will read these files:
READ: file1.py
READ: file2.py

1. Implement basic logging for X
2. Implement basic logging for Y
3. Implement basic logging for Z
... (97 more similar items)
"""

        files_read = []

        is_valid, violations = _validate_analysis_response(
            bad_response, user_request, files_read=files_read
        )

        assert is_valid is False
        assert len(violations) >= 2  # Multiple violations detected
        # Violations should include filler detection and lack of file reads
        assert any("filler" in v.lower() or "placeholder" in v.lower() for v in violations)
        assert any("no files" in v.lower() or "no analysis" in v.lower() for v in violations)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
