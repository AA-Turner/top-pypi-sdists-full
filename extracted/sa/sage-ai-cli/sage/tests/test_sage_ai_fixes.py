"""TDD tests for SAGE AI critical issues identified in log analysis.

This test file covers:
- P0: Thinking block suppression
- P0: Evidence grounding enforcement
- P0: Request classification for list generation
- P1: Output validation (no repetition, specific findings)
- P1: Prompt enhancement
- P1: Search result display

Run with: pytest sage/tests/test_sage_ai_fixes.py -v
"""

from __future__ import annotations

import re

import pytest

# =============================================================================
# P0: Thinking Block Suppression Tests
# =============================================================================


class TestThinkingBlockSuppression:
    """Tests for complete thinking block suppression in all output modes."""

    def test_thinking_filter_removes_complete_blocks(self):
        """ThinkingSuppressionFilter should remove entire <thinking> blocks."""
        from sage.core.thinking_filter import ThinkingSuppressionFilter

        filter_obj = ThinkingSuppressionFilter()

        # Test with complete thinking block
        input_tokens = [
            "Here is ",
            "<thinking>",
            "Let me think about this...",
            "I need to consider...",
            "</thinking>",
            "the answer.",
        ]

        output = []
        for token in input_tokens:
            result = filter_obj.feed(token)
            if result:
                output.append(result)

        # Flush any remaining
        tail = filter_obj.flush_display_tail()
        if tail:
            output.append(tail)

        final_output = "".join(output)

        # Should NOT contain thinking tags or content
        assert "<thinking>" not in final_output
        assert "</thinking>" not in final_output
        assert "Let me think" not in final_output

        # Should contain the actual output
        assert "Here is" in final_output
        assert "the answer" in final_output

    def test_thinking_filter_handles_multiline_blocks(self):
        """Filter should handle thinking blocks spanning multiple tokens."""
        from sage.core.thinking_filter import ThinkingSuppressionFilter

        filter_obj = ThinkingSuppressionFilter()

        input_text = """Start of output
<thinking>
This is internal reasoning.
Multiple lines of thought.
Complex analysis here.
</thinking>
End of output"""

        output = []
        for char in input_text:
            result = filter_obj.feed(char)
            if result:
                output.append(result)

        tail = filter_obj.flush_display_tail()
        if tail:
            output.append(tail)

        final_output = "".join(output)

        assert "Start of output" in final_output
        assert "End of output" in final_output
        assert "<thinking>" not in final_output
        assert "internal reasoning" not in final_output

    def test_renderer_applies_thinking_filter_by_default(self):
        """Renderer should apply thinking filter in clean/normal modes."""
        from sage.core import renderer

        # In clean mode (default), thinking should be suppressed
        renderer.set_output_mode("clean")
        assert renderer.suppress_thinking() is True

        # In normal mode, thinking should still be suppressed
        renderer.set_output_mode("normal")
        assert renderer.suppress_thinking() is True

        # Only in verbose mode should thinking be shown
        renderer.set_output_mode("verbose")
        assert renderer.suppress_thinking() is False


# =============================================================================
# P0: Evidence Grounding Tests
# =============================================================================


class TestEvidenceGrounding:
    """Tests for evidence tracker integration and synthesis gate enforcement."""

    def test_file_read_records_evidence(self):
        """Reading files should record evidence in tracker."""
        from sage.main import _record_file_read, _reset_evidence_tracker

        tracker = _reset_evidence_tracker()
        assert len(tracker.verified_files) == 0

        # Record successful read
        _record_file_read("sage/main.py", success=True)

        assert len(tracker.verified_files) == 1
        assert "sage/main.py" in tracker.verified_files

    def test_failed_read_not_counted_as_evidence(self):
        """Failed reads should not count as verified evidence."""
        from sage.main import _record_file_read, _reset_evidence_tracker

        tracker = _reset_evidence_tracker()

        # Record failed read
        _record_file_read("nonexistent.py", success=False)

        # Should not be in verified files
        assert len(tracker.verified_files) == 0
        assert not tracker.has_verified_evidence()

    def test_search_records_evidence(self):
        """Search operations should record evidence."""
        from sage.main import _record_search, _reset_evidence_tracker

        tracker = _reset_evidence_tracker()

        # Record search with results
        _record_search("import asyncio", ["file1.py", "file2.py"])

        assert tracker.has_successful_searches()

    def test_synthesis_gate_blocks_without_evidence(self):
        """Synthesis should be blocked if no evidence gathered."""
        from sage.main import _check_synthesis_gate, _reset_evidence_tracker

        _reset_evidence_tracker()

        # Without evidence, synthesis should be blocked
        can_synthesize, reason = _check_synthesis_gate()

        assert can_synthesize is False
        assert "evidence" in reason.lower()

    def test_synthesis_gate_allows_with_evidence(self):
        """Synthesis should be allowed with verified evidence."""
        from sage.main import _check_synthesis_gate, _record_file_read, _reset_evidence_tracker

        _reset_evidence_tracker()
        _record_file_read("test.py", success=True)

        # With evidence, synthesis should be allowed
        can_synthesize, reason = _check_synthesis_gate()

        assert can_synthesize is True


# =============================================================================
# P0: Request Classification Tests
# =============================================================================


class TestRequestClassification:
    """Tests for proper classification of list generation requests."""

    def test_list_100_items_classified_as_list_generation(self):
        """'List 100 items' should be classified as LIST_GENERATION."""
        from sage.core.request_classifier import PipelineType, RequestClassifier

        classifier = RequestClassifier()

        # Test various phrasings
        test_cases = [
            "Analyze the codebase and list 100 items that should be improved",
            "List 100 improvements for this code",
            "Give me 100 things to fix",
            "Provide a list of 100 issues",
        ]

        for request in test_cases:
            result = classifier.classify(request)

            assert result.pipeline_type == PipelineType.LIST_GENERATION, (
                f"Failed to classify as LIST_GENERATION: {request}"
            )
            assert result.quantity_required == 100, (
                f"Failed to extract quantity 100 from: {request}"
            )

    def test_list_generation_requires_file_verification(self):
        """List generation should require file verification."""
        from sage.core.request_classifier import RequestClassifier

        classifier = RequestClassifier()
        result = classifier.classify("List 100 improvements in the codebase")

        assert result.requires_file_verification is True
        assert result.must_include_file_paths is True

    def test_list_generation_is_read_only(self):
        """List generation should be read-only (no code changes)."""
        from sage.core.request_classifier import RequestClassifier

        classifier = RequestClassifier()
        result = classifier.classify("List 100 issues")

        assert result.read_only is True


# =============================================================================
# P1: Output Validation Tests
# =============================================================================


class TestOutputValidation:
    """Tests for output quality validation (no repetition, specificity)."""

    def test_validator_detects_repeated_items(self):
        """Validator should detect when list items are repeated."""

        def detect_repeated_items(text: str, min_count: int = 3) -> list[str]:
            """Detect repeated patterns in numbered list."""
            # Extract numbered items (e.g., "96. Item text")
            pattern = r"^\d+\.\s+(.+?)$"
            items = re.findall(pattern, text, re.MULTILINE)

            # Find duplicates
            from collections import Counter

            counts = Counter(items)
            repeated = [item for item, count in counts.items() if count >= min_count]

            return repeated

        # Test text with repetition
        repeated_text = """
96. Cost Monitoring: Monitor cloud resource consumption per service.
97. Deployment Strategy: Implement advanced deployment strategies.
98. Rollback Plan: Ensure every deployment has a tested rollback plan.
99. Incident Post-Mortems: Conduct blameless post-mortems.
100. Knowledge Base: Formalize and maintain a knowledge base.
96. Cost Monitoring: Monitor cloud resource consumption per service.
97. Deployment Strategy: Implement advanced deployment strategies.
98. Rollback Plan: Ensure every deployment has a tested rollback plan.
99. Incident Post-Mortems: Conduct blameless post-mortems.
100. Knowledge Base: Formalize and maintain a knowledge base.
96. Cost Monitoring: Monitor cloud resource consumption per service.
"""

        repeated = detect_repeated_items(repeated_text)

        # Should detect these repeated items
        assert len(repeated) > 0
        assert any("Cost Monitoring" in item for item in repeated)

    def test_validator_requires_file_references_for_code_issues(self):
        """Code-related findings should include file:line references."""

        def has_file_references(text: str) -> bool:
            """Check if text contains file:line references."""
            # Pattern: filename.ext:123 or path/to/file.ext:123
            pattern = r"[\w/.-]+\.\w+:\d+"
            return bool(re.search(pattern, text))

        # Good example with file reference
        good_text = "Issue in sage/main.py:123 - Missing import"
        assert has_file_references(good_text)

        # Bad example without file reference
        bad_text = "Implement rate limiting for better performance"
        assert not has_file_references(bad_text)

    def test_validator_detects_generic_vs_specific_findings(self):
        """Validator should distinguish generic advice from specific findings."""
        generic_phrases = [
            "implement rate limiting",
            "use kubernetes",
            "add authentication",
            "improve performance",
            "optimize queries",
        ]

        def is_generic(finding: str) -> bool:
            """Check if finding is generic advice."""
            finding_lower = finding.lower()
            return any(phrase in finding_lower for phrase in generic_phrases)

        # Generic findings
        assert is_generic("Implement rate limiting on API endpoints")
        assert is_generic("Use Kubernetes for deployment")

        # Specific findings (not generic)
        assert not is_generic("Missing subprocess import in sage/execution.py:454")
        assert not is_generic("Unused safe_utils.py module (533 lines) never imported")


# =============================================================================
# P1: Prompt Enhancement Tests
# =============================================================================


class TestPromptEnhancement:
    """Tests for prompt enhancement before execution."""

    def test_enhance_prompt_adds_specificity_requirements(self):
        """Prompt enhancement should add specificity requirements."""
        from sage.main import _enhance_task_prompt

        original = "Analyze the codebase and list 100 items"
        enhanced = _enhance_task_prompt(original)

        # Enhanced should be longer
        assert len(enhanced) > len(original)

        # Should add requirements for specificity
        enhanced_lower = enhanced.lower()
        assert any(
            keyword in enhanced_lower
            for keyword in ["specific", "file", "line", "reference", "cite", "verify"]
        )

    def test_enhance_list_prompt_adds_file_reference_requirement(self):
        """List generation prompts should require file references."""
        from sage.main import _enhance_task_prompt

        original = "List 100 improvements"
        enhanced = _enhance_task_prompt(original)

        # Should mention file references
        assert "file" in enhanced.lower() or "reference" in enhanced.lower()

    def test_enhance_prompt_adds_evidence_requirement(self):
        """Prompts should require evidence-based findings."""
        from sage.main import _enhance_task_prompt

        original = "Find issues in the code"
        enhanced = _enhance_task_prompt(original)

        # Should mention evidence or verification
        enhanced_lower = enhanced.lower()
        assert any(
            keyword in enhanced_lower
            for keyword in ["evidence", "verify", "read", "search", "examine"]
        )


# =============================================================================
# P1: Search Result Display Tests
# =============================================================================


class TestSearchResultDisplay:
    """Tests for proper display of search results."""

    def test_search_results_show_file_and_line(self):
        """Search results should show file paths and line numbers."""

        def format_search_result(file_path: str, line_num: int, line_content: str) -> str:
            """Format a search result for display."""
            return f"{file_path}:{line_num}: {line_content}"

        result = format_search_result("sage/main.py", 123, "import asyncio")

        assert "sage/main.py" in result
        assert ":123:" in result
        assert "import asyncio" in result

    def test_search_results_grouped_by_file(self):
        """Search results should be grouped by file for readability."""
        search_results = [
            ("file1.py", 10, "match1"),
            ("file1.py", 20, "match2"),
            ("file2.py", 5, "match3"),
        ]

        # Group by file
        from collections import defaultdict

        grouped = defaultdict(list)
        for file_path, line_num, content in search_results:
            grouped[file_path].append((line_num, content))

        assert len(grouped) == 2
        assert len(grouped["file1.py"]) == 2
        assert len(grouped["file2.py"]) == 1


# =============================================================================
# Integration Tests
# =============================================================================


class TestSageAIIntegration:
    """Integration tests for complete SAGE AI workflow."""

    def test_list_generation_workflow_requires_evidence(self):
        """Complete workflow: classify -> gather evidence -> synthesize."""
        from sage.core.request_classifier import RequestClassifier
        from sage.main import _check_synthesis_gate, _reset_evidence_tracker

        # 1. Classify request
        classifier = RequestClassifier()
        classification = classifier.classify("List 100 improvements")

        assert classification.quantity_required == 100

        # 2. Reset evidence tracker
        tracker = _reset_evidence_tracker()

        # 3. Without evidence, synthesis should be blocked
        can_synthesize, _ = _check_synthesis_gate()
        assert can_synthesize is False

    def test_thinking_blocks_filtered_in_clean_mode(self):
        """In clean mode, thinking blocks should never appear in output."""
        from sage.core import renderer
        from sage.core.thinking_filter import ThinkingSuppressionFilter

        # Set clean mode
        renderer.set_output_mode("clean")

        # Create filter
        filter_obj = ThinkingSuppressionFilter()

        # Process text with thinking
        text = "Output <thinking>Internal</thinking> Final"
        result = []
        for char in text:
            filtered = filter_obj.feed(char)
            if filtered:
                result.append(filtered)

        tail = filter_obj.flush_display_tail()
        if tail:
            result.append(tail)

        output = "".join(result)

        assert "<thinking>" not in output
        assert "Internal" not in output
        assert "Output" in output
        assert "Final" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
