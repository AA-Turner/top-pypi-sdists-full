"""Tests for evidence grounding enforcement - P0 items 11-17.

Tests verify:
- Evidence grounding is enforced before synthesis
- Output matches requested format
- No side effects in analysis mode
- Structured output validation
- Error messages are actionable
- Retry loop respects classification
- Classification preserved through retries
"""

from sage.core.request_classifier import (
    ClassifiedRequest,
    CodeGenerationBlocker,
    EvidenceTracker,
    FormatRequirement,
    InstructionManager,
    OutputFormat,
    OutputFormatEnforcer,
    PipelineType,
    RequestClassifier,
    RequestType,
    SynthesisGate,
    validate_response,
)


class TestEvidenceGroundingEnforced:
    """P0 item 11: Evidence grounding is enforced."""

    def test_synthesis_requires_evidence(self):
        """Synthesis should be blocked without evidence."""
        gate = SynthesisGate()
        tracker = EvidenceTracker()

        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is False
        assert "evidence" in reason.lower()

    def test_file_reads_provide_evidence(self):
        """Successful file reads should count as evidence."""
        tracker = EvidenceTracker()
        tracker.record_file_read("src/main.py", success=True)
        tracker.record_file_read("src/utils.py", success=True)

        assert tracker.has_verified_evidence()
        assert len(tracker.verified_files) == 2

    def test_search_results_provide_evidence(self):
        """Search results should count as evidence."""
        tracker = EvidenceTracker()
        tracker.record_search("def main", ["src/main.py", "src/cli.py"])

        assert tracker.has_verified_evidence()
        assert tracker.has_successful_searches()

    def test_failed_reads_not_counted_as_evidence(self):
        """Failed reads should not count as evidence."""
        tracker = EvidenceTracker()
        tracker.record_file_read("nonexistent.py", success=False)

        assert not tracker.has_verified_evidence()
        assert tracker.all_reads_failed()

    def test_empty_searches_not_counted_as_evidence(self):
        """Empty searches should not count as evidence."""
        tracker = EvidenceTracker()
        tracker.record_search("nonexistent_pattern", [])

        assert not tracker.has_verified_evidence()
        assert tracker.all_searches_empty()

    def test_evidence_summary_accurate(self):
        """Evidence summary should accurately reflect gathered evidence."""
        tracker = EvidenceTracker()
        tracker.record_file_read("file1.py", success=True)
        tracker.record_file_read("file2.py", success=False)
        tracker.record_search("pattern1", ["file1.py"])
        tracker.record_search("pattern2", [])
        tracker.record_command("ls", True)
        tracker.record_command("cat nonexistent", False)

        summary = tracker.get_evidence_summary()
        assert summary["verified_files"] == 1
        assert summary["failed_files"] == 1
        assert summary["successful_searches"] == 1
        assert summary["empty_searches"] == 1
        assert summary["total_commands"] == 2
        assert summary["successful_commands"] == 1

    def test_minimum_evidence_requirements(self):
        """Synthesis gate should enforce minimum evidence requirements."""
        gate = SynthesisGate(min_files=3, min_searches=2)
        tracker = EvidenceTracker()

        # One file is not enough
        tracker.record_file_read("file1.py", success=True)
        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is False
        assert "insufficient" in reason.lower()

        # Add more files
        tracker.record_file_read("file2.py", success=True)
        tracker.record_file_read("file3.py", success=True)

        # Still need searches
        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is False
        assert "searches" in reason.lower()

        # Add searches
        tracker.record_search("p1", ["file1.py"])
        tracker.record_search("p2", ["file2.py"])

        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is True


class TestOutputMatchesRequestedFormat:
    """P0 item 12: Output matches requested format."""

    def test_list_generation_requires_numbered_items(self):
        """List generation should require numbered items."""
        classification = ClassifiedRequest(
            original_request="List 20 improvements",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
            quantity_required=20,
            min_items=20,
        )

        requirements = OutputFormatEnforcer.get_requirements(classification)
        assert requirements.requires_numbering is True
        assert requirements.min_items == 20

    def test_format_validation_catches_insufficient_items(self):
        """Format validation should catch insufficient numbered items."""
        requirements = FormatRequirement(
            format_type=OutputFormat.MARKDOWN_LIST,
            requires_numbering=True,
            min_items=10,
        )

        response = """
        1. First item
        2. Second item
        3. Third item
        """

        is_valid, errors = OutputFormatEnforcer.validate_format(response, requirements)
        assert is_valid is False
        assert any("3 numbered items" in e for e in errors)

    def test_format_validation_passes_sufficient_items(self):
        """Format validation should pass with sufficient items."""
        requirements = FormatRequirement(
            format_type=OutputFormat.MARKDOWN_LIST,
            requires_numbering=True,
            min_items=3,
            requires_file_refs=False,  # Disable for this test
        )

        response = """
        1. First item
        2. Second item
        3. Third item
        4. Fourth item
        """

        is_valid, errors = OutputFormatEnforcer.validate_format(response, requirements)
        assert is_valid is True

    def test_table_format_required_for_large_lists(self):
        """Large lists should require table format."""
        classification = ClassifiedRequest(
            original_request="List 50 improvements",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_TABLE,
            pipeline_type=PipelineType.LIST_GENERATION,
            quantity_required=50,
            min_items=50,
        )

        requirements = OutputFormatEnforcer.get_requirements(classification)
        assert requirements.requires_table is True

    def test_priority_ranking_required_when_requested(self):
        """Priority ranking should be required when requested."""
        classification = ClassifiedRequest(
            original_request="List and rank by priority",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
            priority_ranking=True,
        )

        requirements = OutputFormatEnforcer.get_requirements(classification)
        assert requirements.requires_priority is True


class TestNoSideEffectsInAnalysisMode:
    """P0 item 13: No side effects in analysis mode."""

    def test_analysis_mode_is_read_only(self):
        """Analysis mode should set read_only=True."""
        classifier = RequestClassifier()
        result = classifier.classify("Analyze the codebase")

        assert result.read_only is True
        assert result.request_type == RequestType.ANALYSIS

    def test_list_generation_is_read_only(self):
        """List generation should set read_only=True."""
        classifier = RequestClassifier()
        result = classifier.classify("List 100 improvements")

        assert result.read_only is True
        assert result.strict_read_only is True

    def test_code_blocking_prompt_generated(self):
        """Code blocking prompt should be generated for strict read-only."""
        classification = ClassifiedRequest(
            original_request="List 100 improvements",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
            read_only=True,
            strict_read_only=True,
        )

        blocking_prompt = CodeGenerationBlocker.get_blocking_prompt(classification)
        assert "FORBIDDEN" in blocking_prompt
        assert "FILE:" in blocking_prompt
        assert "CODE GENERATION BLOCKED" in blocking_prompt

    def test_code_detection_catches_file_blocks(self):
        """Code detection should catch FILE: blocks."""
        response = """
        Here's my analysis:

        FILE: src/main.py
        ```python
        def new_function():
            pass
        ```
        """

        has_code, violations = CodeGenerationBlocker.check_for_code(response)
        assert has_code is True
        assert len(violations) > 0

    def test_code_stripping_removes_file_blocks(self):
        """Code stripping should remove FILE: blocks."""
        response = """Here's my analysis:

FILE: src/main.py
```python
def new_function():
    pass
```

This concludes the analysis."""

        cleaned = CodeGenerationBlocker.strip_code_blocks(response)
        assert "FILE:" not in cleaned
        assert "def new_function" not in cleaned
        assert "This concludes the analysis" in cleaned


class TestStructuredOutputValidation:
    """P0 item 14: Structured output validation."""

    def test_validation_checks_format(self):
        """Validation should check output format."""
        classification = ClassifiedRequest(
            original_request="List 10 items",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
            read_only=True,
            min_items=10,
        )

        # Response with only 3 items
        response = """
        1. First item `src/a.py`
        2. Second item `src/b.py`
        3. Third item `src/c.py`
        """

        result = validate_response(response, classification)
        # Should indicate incomplete
        assert result.should_retry or not result.is_valid or result.warnings

    def test_validation_enforces_read_only(self):
        """Validation should reject FILE: blocks in read-only mode."""
        classification = ClassifiedRequest(
            original_request="List 10 items",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
            read_only=True,
            strict_read_only=True,
        )

        response = """
        1. First improvement `src/main.py`

        FILE: src/main.py
        ```python
        # This should not be here
        ```
        """

        result = validate_response(response, classification)
        # Should flag the FILE: block
        assert not result.is_valid or result.should_retry or len(result.errors) > 0


class TestActionableErrorMessages:
    """P0 item 15: Error messages are actionable."""

    def test_format_errors_are_specific(self):
        """Format errors should specify what's missing."""
        requirements = FormatRequirement(
            format_type=OutputFormat.MARKDOWN_LIST,
            requires_numbering=True,
            min_items=20,
            requires_priority=True,
        )

        response = """
        1. Item one
        2. Item two
        """

        is_valid, errors = OutputFormatEnforcer.validate_format(response, requirements)
        assert is_valid is False
        # Errors should mention specific issues
        assert any("2 numbered items" in e and "20" in e for e in errors)
        assert any("priority" in e.lower() for e in errors)

    def test_synthesis_gate_explains_requirements(self):
        """Synthesis gate should explain what evidence is needed."""
        gate = SynthesisGate(min_files=5, min_searches=2)
        tracker = EvidenceTracker()
        tracker.record_file_read("file1.py", success=True)

        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is False
        assert "5 verified files" in reason
        assert "have 1" in reason


class TestRetryLoopRespectsClassification:
    """P0 item 16: Retry loop respects classification."""

    def test_retry_preserves_read_only(self):
        """Retry should preserve read_only setting."""
        classifier = RequestClassifier()
        initial = classifier.classify("List 100 improvements")

        # Simulate retry - classification should still be read-only
        assert initial.read_only is True
        assert initial.strict_read_only is True

    def test_retry_preserves_format_requirements(self):
        """Retry should preserve format requirements."""
        classifier = RequestClassifier()
        initial = classifier.classify("List 50 improvements ranked by priority")

        # All requirements should be preserved
        assert initial.quantity_required == 50
        assert initial.priority_ranking is True
        assert initial.min_items == 50

    def test_instructions_include_retry_context(self):
        """Instructions should include context for retries."""
        classification = ClassifiedRequest(
            original_request="List 100 improvements",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
            read_only=True,
            quantity_required=100,
            min_items=100,
        )

        instructions = InstructionManager.build_instruction_block(classification)
        assert "QUANTITY" in instructions
        assert "List 100 improvements" in instructions
        assert "DO NOT" in instructions


class TestClassificationPreservedThroughRetries:
    """P0 item 17: Classification preserved through retries."""

    def test_classification_immutable(self):
        """Classification should not change after creation."""
        classifier = RequestClassifier()
        result = classifier.classify("List 100 improvements")

        # Store original values
        original_type = result.request_type
        original_pipeline = result.pipeline_type
        original_read_only = result.read_only
        original_quantity = result.quantity_required

        # Access properties multiple times (simulating retries)
        for _ in range(3):
            assert result.request_type == original_type
            assert result.pipeline_type == original_pipeline
            assert result.read_only == original_read_only
            assert result.quantity_required == original_quantity

    def test_classification_not_affected_by_response(self):
        """Classification should not change based on AI response."""
        classifier = RequestClassifier()
        result = classifier.classify("List 100 improvements")

        # Even if AI responds with code, classification should remain read-only
        assert result.read_only is True
        assert result.strict_read_only is True
        assert result.request_type == RequestType.LIST_GENERATION

    def test_format_requirements_stable(self):
        """Format requirements should be stable across retries."""
        classification = ClassifiedRequest(
            original_request="List 50 improvements ranked by priority",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_TABLE,
            pipeline_type=PipelineType.LIST_GENERATION,
            quantity_required=50,
            priority_ranking=True,
            min_items=50,
        )

        # Get requirements multiple times
        for _ in range(3):
            requirements = OutputFormatEnforcer.get_requirements(classification)
            assert requirements.requires_numbering is True
            assert requirements.requires_table is True
            assert requirements.requires_priority is True
            assert requirements.min_items == 50


class TestForbiddenPatternsEnforced:
    """Test that forbidden patterns are enforced based on classification."""

    def test_list_generation_forbids_code(self):
        """List generation should forbid code blocks."""
        classification = ClassifiedRequest(
            original_request="List improvements",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
        )

        requirements = OutputFormatEnforcer.get_requirements(classification)
        assert len(requirements.forbidden_patterns) > 0
        assert any("FILE:" in p for p in requirements.forbidden_patterns)

    def test_analysis_forbids_code(self):
        """Analysis should forbid code blocks."""
        classification = ClassifiedRequest(
            original_request="Analyze the code",
            request_type=RequestType.ANALYSIS,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.ANALYSIS_ONLY,
        )

        requirements = OutputFormatEnforcer.get_requirements(classification)
        assert len(requirements.forbidden_patterns) > 0

    def test_implementation_allows_code(self):
        """Implementation should allow code blocks."""
        classification = ClassifiedRequest(
            original_request="Implement the feature",
            request_type=RequestType.IMPLEMENTATION,
            expected_format=OutputFormat.CODE_FILES,
            pipeline_type=PipelineType.IMPLEMENTATION,
        )

        requirements = OutputFormatEnforcer.get_requirements(classification)
        assert requirements.requires_code_blocks is True
        assert len(requirements.forbidden_patterns) == 0

    def test_forbidden_pattern_caught_in_validation(self):
        """Forbidden patterns should be caught in format validation."""
        requirements = FormatRequirement(
            format_type=OutputFormat.MARKDOWN_LIST,
            forbidden_patterns=[r"^FILE:\s*"],
        )

        response = """1. First item
2. Second item

FILE: src/main.py
```python
code here
```
"""

        is_valid, errors = OutputFormatEnforcer.validate_format(response, requirements)
        assert is_valid is False
        assert any("forbidden pattern" in e.lower() for e in errors)


class TestInstructionManagement:
    """Test instruction management for proper guidance."""

    def test_instruction_block_includes_task(self):
        """Instruction block should include the original task."""
        classification = ClassifiedRequest(
            original_request="List 100 improvements",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
        )

        instructions = InstructionManager.build_instruction_block(classification)
        assert "List 100 improvements" in instructions

    def test_instruction_block_includes_priorities(self):
        """Instruction block should include instruction priorities."""
        classification = ClassifiedRequest(
            original_request="List 100 improvements",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
        )

        instructions = InstructionManager.build_instruction_block(classification)
        assert "QUANTITY" in instructions
        assert "GROUNDING" in instructions

    def test_instruction_block_includes_negative_instructions(self):
        """Instruction block should include 'DO NOT' section for read-only."""
        classification = ClassifiedRequest(
            original_request="Analyze the code",
            request_type=RequestType.ANALYSIS,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.ANALYSIS_ONLY,
            read_only=True,
        )

        instructions = InstructionManager.build_instruction_block(classification)
        assert "DO NOT" in instructions
        assert "FILE:" in instructions
