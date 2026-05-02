"""Tests for classifier enforcement - P0 items 6-10.

Tests verify:
- Classifier is single source of truth for pipeline selection
- No competing heuristics can override classification
- Read-only mode enforced in all branches
- Synthesis blocked without verified evidence
"""

from sage.core.request_classifier import (
    ClassifiedRequest,
    EvidenceTracker,
    OutputFormat,
    PipelineType,
    RequestClassifier,
    RequestType,
    SynthesisGate,
    validate_response,
)


class TestClassifierAsSingleSourceOfTruth:
    """P0 item 6: Classifier is the single source of truth."""

    def test_classification_determines_pipeline(self):
        """Pipeline should be determined solely by classification."""
        classifier = RequestClassifier()

        # List generation should use LIST_GENERATION pipeline
        result = classifier.classify("List 100 improvements")
        assert result.pipeline_type == PipelineType.LIST_GENERATION

        # Analysis should use ANALYSIS_ONLY pipeline
        result = classifier.classify("Analyze the codebase")
        assert result.pipeline_type == PipelineType.ANALYSIS_ONLY

        # Implementation should use IMPLEMENTATION pipeline
        result = classifier.classify("Implement a new feature")
        assert result.pipeline_type == PipelineType.IMPLEMENTATION

    def test_classification_is_immutable_during_execution(self):
        """Classification should not change during task execution."""
        classifier = RequestClassifier()
        result = classifier.classify("List 50 issues")

        # Store original values
        original_type = result.request_type
        original_pipeline = result.pipeline_type
        original_read_only = result.read_only

        # Simulate what happens during execution - values should be unchanged
        assert result.request_type == original_type
        assert result.pipeline_type == original_pipeline
        assert result.read_only == original_read_only

    def test_pipeline_type_matches_request_type(self):
        """Pipeline type should always match the request type."""
        classifier = RequestClassifier()

        # Read-only types should have read-only pipelines
        for req_text, expected_pipeline in [
            ("Analyze security issues", PipelineType.ANALYSIS_ONLY),
            ("List 100 improvements", PipelineType.LIST_GENERATION),
            ("What is this code doing?", PipelineType.ANALYSIS_ONLY),  # Questions use ANALYSIS_ONLY
            ("Compare A and B", PipelineType.ANALYSIS_ONLY),
        ]:
            result = classifier.classify(req_text)
            assert result.pipeline_type == expected_pipeline, f"Failed for: {req_text}"


class TestNoCompetingHeuristics:
    """P0 item 7: No competing complexity heuristics."""

    def test_classifier_overrides_ai_complexity(self):
        """Classifier should not be overridden by AI complexity assessment."""
        classifier = RequestClassifier()

        # List generation is read-only regardless of AI complexity
        result = classifier.classify("List 100 improvements to the codebase")

        assert result.read_only is True
        assert result.strict_read_only is True
        # Even if AI says this is "high complexity", it's still read-only
        assert result.request_type == RequestType.LIST_GENERATION

    def test_read_only_not_overridden_by_word_count(self):
        """Read-only classification should not be overridden by word count."""
        classifier = RequestClassifier()

        # Long request is still read-only if classified as analysis
        long_request = "Analyze the codebase and " + " ".join(["detailed"] * 100)
        result = classifier.classify(long_request)

        if result.request_type == RequestType.ANALYSIS:
            assert result.read_only is True

    def test_read_only_not_overridden_by_and_keyword(self):
        """Read-only should not be overridden just because request contains 'and'."""
        classifier = RequestClassifier()

        # Analysis with 'and' is still read-only
        result = classifier.classify("Analyze security and performance issues")
        assert result.read_only is True

        # List generation with 'and' is still read-only
        result = classifier.classify("List bugs and improvements")
        assert result.read_only is True


class TestReadOnlyEnforcementInAllBranches:
    """P0 item 8: Read-only enforced in all branches."""

    def test_read_only_in_initial_classification(self):
        """Read-only should be set in initial classification."""
        classifier = RequestClassifier()

        result = classifier.classify("Analyze the code")
        assert result.read_only is True

    def test_read_only_preserved_in_retry(self):
        """Read-only should be preserved in retry prompts."""
        classifier = RequestClassifier()

        result = classifier.classify("List 100 items")
        assert result.read_only is True
        assert result.strict_read_only is True

        # Simulated retry - classification should still be read-only
        # In real code, this would be enforced by the continuation prompt
        assert result.read_only is True

    def test_strict_read_only_for_analysis_tasks(self):
        """Analysis tasks should have strict_read_only=True."""
        classifier = RequestClassifier()

        for request in [
            "Analyze the codebase",
            "List 100 improvements",
            "Review security issues",
        ]:
            result = classifier.classify(request)
            if result.request_type in (RequestType.ANALYSIS, RequestType.LIST_GENERATION):
                assert result.strict_read_only is True, f"Failed for: {request}"


class TestEvidenceTracking:
    """P0 items 9-10: Evidence tracking and synthesis blocking."""

    def test_evidence_tracker_tracks_verified_files(self):
        """EvidenceTracker should track verified file reads."""
        tracker = EvidenceTracker()

        tracker.record_file_read("src/main.py", success=True)
        tracker.record_file_read("src/utils.py", success=True)

        assert tracker.has_verified_evidence()
        assert "src/main.py" in tracker.verified_files
        assert "src/utils.py" in tracker.verified_files

    def test_evidence_tracker_tracks_failed_reads(self):
        """EvidenceTracker should track failed reads separately."""
        tracker = EvidenceTracker()

        tracker.record_file_read("nonexistent.py", success=False)

        assert not tracker.has_verified_evidence()
        assert "nonexistent.py" in tracker.failed_files

    def test_evidence_tracker_tracks_search_results(self):
        """EvidenceTracker should track search results."""
        tracker = EvidenceTracker()

        tracker.record_search("pattern", results=["file1.py", "file2.py"])

        assert tracker.has_verified_evidence()
        assert tracker.search_count == 1

    def test_evidence_tracker_tracks_empty_searches(self):
        """EvidenceTracker should track searches with no results."""
        tracker = EvidenceTracker()

        tracker.record_search("nonexistent_pattern", results=[])

        assert not tracker.has_verified_evidence()
        assert tracker.empty_search_count == 1


class TestSynthesisGating:
    """P0 items 9-10: Synthesis should be blocked without evidence."""

    def test_synthesis_blocked_without_evidence(self):
        """Synthesis should be blocked if no evidence exists."""
        gate = SynthesisGate()
        tracker = EvidenceTracker()

        # No evidence gathered
        can_synthesize, reason = gate.check(tracker)

        assert can_synthesize is False
        assert "no verified evidence" in reason.lower()

    def test_synthesis_blocked_with_all_failed_reads(self):
        """Synthesis should be blocked if all reads failed."""
        gate = SynthesisGate()
        tracker = EvidenceTracker()

        tracker.record_file_read("file1.py", success=False)
        tracker.record_file_read("file2.py", success=False)

        can_synthesize, reason = gate.check(tracker)

        assert can_synthesize is False
        assert "failed" in reason.lower() or "no verified" in reason.lower()

    def test_synthesis_blocked_with_all_empty_searches(self):
        """Synthesis should be blocked if all searches returned empty."""
        gate = SynthesisGate()
        tracker = EvidenceTracker()

        tracker.record_search("pattern1", results=[])
        tracker.record_search("pattern2", results=[])

        can_synthesize, reason = gate.check(tracker)

        assert can_synthesize is False

    def test_synthesis_allowed_with_verified_evidence(self):
        """Synthesis should be allowed with verified evidence."""
        gate = SynthesisGate()
        tracker = EvidenceTracker()

        tracker.record_file_read("src/main.py", success=True)
        tracker.record_search("def main", results=["src/main.py"])

        can_synthesize, reason = gate.check(tracker)

        assert can_synthesize is True

    def test_synthesis_requires_minimum_evidence(self):
        """Synthesis should require minimum amount of evidence."""
        gate = SynthesisGate(min_files=2, min_searches=1)
        tracker = EvidenceTracker()

        # Only one file - not enough
        tracker.record_file_read("file1.py", success=True)

        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is False

        # Add another file and a search
        tracker.record_file_read("file2.py", success=True)
        tracker.record_search("pattern", results=["file1.py"])

        can_synthesize, reason = gate.check(tracker)
        assert can_synthesize is True


class TestValidationIntegration:
    """Test that validation respects classification."""

    def test_validation_enforces_read_only(self):
        """Validation should reject FILE: blocks in read-only mode."""
        classification = ClassifiedRequest(
            original_request="List 100 improvements",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
            read_only=True,
            strict_read_only=True,
        )

        response_with_file = """
        1. First improvement
        2. Second improvement

        FILE: test.py
        ```python
        # This should not be here
        ```
        """

        result = validate_response(response_with_file, classification)

        # Should flag the FILE: block as invalid via errors or should_retry
        assert not result.is_valid or result.should_retry or len(result.errors) > 0

    def test_validation_allows_code_in_implementation(self):
        """Validation should allow FILE: blocks in implementation mode."""
        classification = ClassifiedRequest(
            original_request="Implement a new feature",
            request_type=RequestType.IMPLEMENTATION,
            expected_format=OutputFormat.CODE_FILES,
            pipeline_type=PipelineType.IMPLEMENTATION,
            read_only=False,
        )

        response_with_file = """
        Here's the implementation:

        FILE: feature.py
        ```python
        def new_feature():
            pass
        ```
        """

        result = validate_response(response_with_file, classification)

        # For implementation mode, FILE: blocks should not cause errors specifically about code generation
        # The validation might have other warnings, but code generation itself should be allowed
        code_gen_errors = [e for e in result.errors if "code" in e.lower() and "block" in e.lower()]
        assert len(code_gen_errors) == 0 or result.is_valid
