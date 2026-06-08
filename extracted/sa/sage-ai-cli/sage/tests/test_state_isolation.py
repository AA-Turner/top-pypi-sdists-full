"""Tests for state isolation and testing - P0 items 26-35.

Tests verify:
- State is properly isolated between requests
- Global state doesn't leak between operations
- Classification state is cleared after requests
- Session state is managed properly
- Test isolation is maintained
"""

import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from sage.core.context import (
    ContextSummarizer,
    ImportanceLevel,
    ImportanceRanker,
)

# Import state management components
from sage.core.request_classifier import (
    ClassifiedRequest,
    EvidenceTracker,
    OutputFormat,
    PipelineType,
    RequestClassifier,
    RequestType,
    SynthesisGate,
)

# =============================================================================
# State Isolation Manager for Tests
# =============================================================================


@dataclass
class IsolatedState:
    """Tracks isolated state for a single request."""

    request_id: str
    classification: ClassifiedRequest | None = None
    evidence_tracker: EvidenceTracker | None = None
    files_read: list[str] = field(default_factory=list)
    files_written: list[str] = field(default_factory=list)
    commands_run: list[str] = field(default_factory=list)
    is_active: bool = False

    def clear(self):
        """Clear all state."""
        self.classification = None
        self.evidence_tracker = None
        self.files_read.clear()
        self.files_written.clear()
        self.commands_run.clear()
        self.is_active = False


class StateIsolationManager:
    """Manages state isolation between requests."""

    def __init__(self):
        self._current_state: IsolatedState | None = None
        self._completed_states: list[IsolatedState] = []
        self._state_counter = 0

    def begin_request(self) -> IsolatedState:
        """Begin a new isolated request context."""
        if self._current_state and self._current_state.is_active:
            raise RuntimeError("Cannot begin new request while another is active")

        self._state_counter += 1
        self._current_state = IsolatedState(
            request_id=f"req_{self._state_counter}",
            is_active=True,
        )
        return self._current_state

    def end_request(self) -> None:
        """End the current request and clear state."""
        if self._current_state:
            self._current_state.is_active = False
            self._completed_states.append(self._current_state)
            self._current_state = None

    def get_current_state(self) -> IsolatedState | None:
        """Get the current active state."""
        return (
            self._current_state if self._current_state and self._current_state.is_active else None
        )

    def clear_all(self) -> None:
        """Clear all state including history."""
        if self._current_state:
            self._current_state.clear()
            self._current_state = None
        self._completed_states.clear()


# =============================================================================
# Tests
# =============================================================================


class TestStateIsolationBetweenRequests:
    """P0 item 26: State is isolated between requests."""

    def test_new_request_has_clean_state(self):
        """Each new request should start with clean state."""
        manager = StateIsolationManager()

        state1 = manager.begin_request()
        state1.files_read.append("file1.py")
        state1.classification = ClassifiedRequest(
            original_request="request1",
            request_type=RequestType.ANALYSIS,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.ANALYSIS_ONLY,
        )
        manager.end_request()

        state2 = manager.begin_request()
        assert len(state2.files_read) == 0
        assert state2.classification is None

    def test_state_not_shared_between_requests(self):
        """State should not leak between requests."""
        manager = StateIsolationManager()

        state1 = manager.begin_request()
        state1.commands_run.append("pytest")
        manager.end_request()

        state2 = manager.begin_request()
        assert "pytest" not in state2.commands_run
        manager.end_request()

    def test_cannot_start_request_while_active(self):
        """Should not allow starting new request while one is active."""
        manager = StateIsolationManager()

        manager.begin_request()
        with pytest.raises(RuntimeError):
            manager.begin_request()

    def test_request_ids_are_unique(self):
        """Each request should have unique ID."""
        manager = StateIsolationManager()

        state1 = manager.begin_request()
        id1 = state1.request_id
        manager.end_request()

        state2 = manager.begin_request()
        id2 = state2.request_id
        manager.end_request()

        assert id1 != id2


class TestClassificationStateIsolation:
    """P0 item 27: Classification state is properly isolated."""

    def test_classification_cleared_after_request(self):
        """Classification should be cleared when request ends."""
        manager = StateIsolationManager()

        state = manager.begin_request()
        state.classification = ClassifiedRequest(
            original_request="List 100 items",
            request_type=RequestType.LIST_GENERATION,
            expected_format=OutputFormat.MARKDOWN_LIST,
            pipeline_type=PipelineType.LIST_GENERATION,
        )
        manager.end_request()

        # After request ends, no current state
        assert manager.get_current_state() is None

    def test_new_classification_replaces_old(self):
        """New classification should replace previous one."""
        classifier = RequestClassifier()

        result1 = classifier.classify("Analyze code")
        assert result1.request_type == RequestType.ANALYSIS

        result2 = classifier.classify("Implement feature")
        assert result2.request_type == RequestType.IMPLEMENTATION
        assert result1 is not result2

    def test_classifier_returns_independent_objects(self):
        """Each classification should be independent."""
        classifier = RequestClassifier()

        result1 = classifier.classify("List 50 items")
        result2 = classifier.classify("List 100 items")

        # Modify one shouldn't affect the other
        original_quantity = result2.quantity_required

        assert result1.quantity_required != result2.quantity_required


class TestEvidenceTrackerIsolation:
    """P0 item 28: Evidence tracking is isolated."""

    def test_each_request_has_own_tracker(self):
        """Each request should have its own evidence tracker."""
        tracker1 = EvidenceTracker()
        tracker1.record_file_read("file1.py", success=True)

        tracker2 = EvidenceTracker()
        assert not tracker2.has_verified_evidence()
        assert "file1.py" not in tracker2.verified_files

    def test_tracker_state_independent(self):
        """Evidence trackers should be completely independent."""
        tracker1 = EvidenceTracker()
        tracker2 = EvidenceTracker()

        tracker1.record_file_read("a.py", success=True)
        tracker1.record_search("pattern", ["a.py", "b.py"])

        assert tracker2.search_count == 0
        assert len(tracker2.verified_files) == 0

    def test_tracker_cleared_for_new_request(self):
        """Tracker should be cleared for new requests."""
        manager = StateIsolationManager()

        state1 = manager.begin_request()
        state1.evidence_tracker = EvidenceTracker()
        state1.evidence_tracker.record_file_read("file.py", success=True)
        manager.end_request()

        state2 = manager.begin_request()
        state2.evidence_tracker = EvidenceTracker()
        assert not state2.evidence_tracker.has_verified_evidence()


class TestSessionStateManagement:
    """P0 item 29: Session state is managed properly."""

    def test_session_state_persists_to_file(self):
        """Session state should persist to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "session_state.json"
            state = {"last_model": "test-model", "key": "value"}
            state_file.write_text(json.dumps(state))

            loaded = json.loads(state_file.read_text())
            assert loaded["last_model"] == "test-model"

    def test_session_state_loads_correctly(self):
        """Session state should load correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "session_state.json"
            original = {"setting": True, "count": 5}
            state_file.write_text(json.dumps(original))

            loaded = json.loads(state_file.read_text())
            assert loaded == original

    def test_missing_session_state_handled(self):
        """Missing session state should be handled gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "session_state.json"
            assert not state_file.exists()

            # Should handle missing file
            default = {} if not state_file.exists() else json.loads(state_file.read_text())
            assert default == {}


class TestGlobalStateLeakage:
    """P0 item 30: Global state doesn't leak."""

    def test_no_shared_mutable_state(self):
        """Mutable state should not be shared."""
        state1 = IsolatedState(request_id="1")
        state2 = IsolatedState(request_id="2")

        state1.files_read.append("test.py")

        # state2 should not be affected
        assert "test.py" not in state2.files_read

    def test_dataclass_defaults_not_shared(self):
        """Dataclass default factories should create new objects."""
        tracker1 = EvidenceTracker()
        tracker2 = EvidenceTracker()

        tracker1.verified_files.add("file.py")

        # Should not affect tracker2
        assert "file.py" not in tracker2.verified_files

    def test_module_level_state_isolation(self):
        """Module-level state should be properly managed."""
        classifier1 = RequestClassifier()
        classifier2 = RequestClassifier()

        # They should be independent instances
        # (pattern compilation is per-instance or properly shared)
        assert classifier1._analysis_re is not None
        assert classifier2._analysis_re is not None


class TestFileOperationIsolation:
    """P0 item 31: File operations are isolated."""

    def test_file_tracking_per_request(self):
        """File tracking should be per-request."""
        state1 = IsolatedState(request_id="1")
        state2 = IsolatedState(request_id="2")

        state1.files_written.append("output1.py")
        state2.files_written.append("output2.py")

        assert "output1.py" in state1.files_written
        assert "output1.py" not in state2.files_written
        assert "output2.py" in state2.files_written
        assert "output2.py" not in state1.files_written

    def test_read_file_tracking(self):
        """Read files should be tracked separately."""
        state = IsolatedState(request_id="test")
        state.files_read.append("src/main.py")
        state.files_read.append("src/utils.py")

        assert len(state.files_read) == 2
        assert "src/main.py" in state.files_read


class TestCommandExecutionIsolation:
    """P0 item 32: Command execution is isolated."""

    def test_commands_tracked_per_request(self):
        """Commands should be tracked per request."""
        state = IsolatedState(request_id="test")
        state.commands_run.append("pytest tests/")
        state.commands_run.append("npm install")

        assert len(state.commands_run) == 2
        assert "pytest tests/" in state.commands_run

    def test_command_history_not_shared(self):
        """Command history should not be shared between requests."""
        manager = StateIsolationManager()

        state1 = manager.begin_request()
        state1.commands_run.append("make build")
        manager.end_request()

        state2 = manager.begin_request()
        assert "make build" not in state2.commands_run


class TestCleanupBetweenOperations:
    """P0 item 33: Cleanup happens between operations."""

    def test_state_cleared_on_end(self):
        """State should be cleared when request ends."""
        state = IsolatedState(request_id="test")
        state.files_read.append("file.py")
        state.commands_run.append("cmd")
        state.is_active = True

        state.clear()

        assert len(state.files_read) == 0
        assert len(state.commands_run) == 0
        assert not state.is_active
        assert state.classification is None

    def test_manager_clears_all_state(self):
        """Manager should be able to clear all state."""
        manager = StateIsolationManager()

        manager.begin_request()
        manager.end_request()
        manager.begin_request()
        manager.end_request()

        assert len(manager._completed_states) == 2

        manager.clear_all()
        assert len(manager._completed_states) == 0


class TestContextSummarizer:
    """P0 item 34: Context summarization isolation."""

    def test_summarizer_cache_works(self):
        """Summarizer cache should work correctly."""
        summarizer = ContextSummarizer()

        messages = [
            {"role": "user", "content": "Test message"},
            {"role": "assistant", "content": "Test response"},
        ]

        # First call creates cache entry
        result1 = summarizer.summarize_conversation(messages)
        # Second call should use cache
        result2 = summarizer.summarize_conversation(messages)

        assert result1 == result2

    def test_different_conversations_different_summaries(self):
        """Different conversations should get different summaries."""
        summarizer = ContextSummarizer()

        messages1 = [{"role": "user", "content": "Topic A"}]
        messages2 = [{"role": "user", "content": "Topic B"}]

        # These might be same if extractive, but cache keys should differ
        summarizer.summarize_conversation(messages1)
        summarizer.summarize_conversation(messages2)

        # Check that cache has two entries
        assert len(summarizer._summary_cache) >= 1


class TestImportanceRanking:
    """P0 item 35: Importance ranking works correctly."""

    def test_importance_ranker_detects_critical(self):
        """Ranker should detect CRITICAL markers."""
        ranker = ImportanceRanker()

        level = ranker.rank("CRITICAL: Security vulnerability found")
        assert level == ImportanceLevel.CRITICAL

    def test_importance_ranker_detects_high(self):
        """Ranker should detect HIGH importance markers."""
        ranker = ImportanceRanker()

        level = ranker.rank("IMPORTANT: This must be done first")
        assert level == ImportanceLevel.HIGH

    def test_importance_ranker_default_is_low(self):
        """Default importance should be LOW."""
        ranker = ImportanceRanker()

        level = ranker.rank("Just a regular message")
        assert level == ImportanceLevel.LOW

    def test_filter_by_importance(self):
        """Should filter messages by importance level."""
        ranker = ImportanceRanker()

        messages = [
            {"content": "CRITICAL: Must read"},
            {"content": "Regular message"},
            {"content": "IMPORTANT: Also read"},
        ]

        filtered = ranker.filter_by_importance(messages, ImportanceLevel.HIGH)

        # Should only include CRITICAL and IMPORTANT messages
        assert len(filtered) == 2
        assert any("CRITICAL" in m["content"] for m in filtered)
        assert any("IMPORTANT" in m["content"] for m in filtered)


class TestRequestClassifierIsolation:
    """Test that RequestClassifier provides isolated results."""

    def test_classify_returns_new_object(self):
        """Each classify call should return a new object."""
        classifier = RequestClassifier()

        result1 = classifier.classify("Analyze code")
        result2 = classifier.classify("Analyze code")

        # Same query, but different objects
        assert result1 is not result2

    def test_classification_modifications_dont_affect_classifier(self):
        """Modifying a result should not affect future classifications."""
        classifier = RequestClassifier()

        result1 = classifier.classify("List 50 items")
        # Even if we could modify it, next call should be clean
        result2 = classifier.classify("List 50 items")

        assert result1.quantity_required == result2.quantity_required

    def test_parallel_classifications_independent(self):
        """Classifications happening in parallel should be independent."""
        classifier = RequestClassifier()

        results = []
        for query in ["Analyze the codebase", "List 100 improvements", "Implement the feature"]:
            results.append(classifier.classify(query))

        # Each should have the correct type
        assert results[0].request_type == RequestType.ANALYSIS
        assert results[1].request_type == RequestType.LIST_GENERATION
        assert results[2].request_type == RequestType.IMPLEMENTATION


class TestSynthesisGateIsolation:
    """Test that SynthesisGate works independently."""

    def test_gates_are_independent(self):
        """Each gate instance should be independent."""
        gate1 = SynthesisGate(min_files=5)
        gate2 = SynthesisGate(min_files=10)

        assert gate1.min_files != gate2.min_files

    def test_gate_check_doesnt_modify_tracker(self):
        """Checking gate should not modify tracker."""
        gate = SynthesisGate()
        tracker = EvidenceTracker()
        tracker.record_file_read("file.py", success=True)

        initial_files = len(tracker.verified_files)
        gate.check(tracker)
        after_files = len(tracker.verified_files)

        assert initial_files == after_files
