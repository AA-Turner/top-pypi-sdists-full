import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from sage.core.request_classifier import EvidenceTracker
from sage.main import SAGEAgent, _reset_evidence_tracker, _get_evidence_tracker
from sage.core.tools import ExecutionLedger

def test_evidence_tracker_failed_searches():
    """Verify that EvidenceTracker tracks failed search patterns."""
    tracker = EvidenceTracker()
    assert len(tracker.failed_searches) == 0

    # Successful search should not add to failed_searches
    tracker.record_search("test_pattern", ["file1.py"])
    assert "test_pattern" not in tracker.failed_searches
    assert len(tracker.verified_files) == 1

    # Empty search should add to failed_searches
    tracker.record_search("empty_pattern", [])
    assert "empty_pattern" in tracker.failed_searches
    assert tracker.empty_search_count == 1


def test_agent_execution_ledger_initialization():
    """Verify that SAGEAgent.execution_ledger is correctly initialized and reset."""
    mock_renderer = MagicMock()
    mock_engine = MagicMock()
    mock_router = MagicMock()

    agent = SAGEAgent(
        cwd=Path("."),
        renderer=mock_renderer,
        engine=mock_engine,
        router=mock_router,
        model_id="default",
        temp=0.1,
        tokens=1000,
        model_locked=False,
        is_local=False,
    )

    # Check initialization
    assert isinstance(agent.execution_ledger, ExecutionLedger)
    
    # Modify it to simulate execution state
    agent.execution_ledger.files_read.append("test.py")
    
    # Run execute_task_prompt start phase, it should re-initialize/reset the ledger
    with patch("sage.main._classify_and_store_request") as mock_classify, \
         patch("sage.main._check_context_relevance") as mock_relevance, \
         patch("sage.main.IntelligentExecutionEngine") as mock_engine_class:
         
        mock_classify.return_value = MagicMock(read_only=True, is_informational=False)
        mock_relevance.return_value = True
        
        # Bounded call that we can mock out early
        try:
            agent.execute_task_prompt("test task")
        except Exception:
            # We expect it to raise/fail later because of mocked components, 
            # but the ledger reset happens at the very start.
            pass
            
        assert isinstance(agent.execution_ledger, ExecutionLedger)
        assert len(agent.execution_ledger.files_read) == 0  # Should be reset/re-initialized


def test_repetition_loop_prevention():
    """Verify that process_response stops execution when all commands have already failed."""
    mock_renderer = MagicMock()
    mock_engine = MagicMock()
    mock_router = MagicMock()

    agent = SAGEAgent(
        cwd=Path(".").resolve(),
        renderer=mock_renderer,
        engine=mock_engine,
        router=mock_router,
        model_id="default",
        temp=0.1,
        tokens=1000,
        model_locked=False,
        is_local=False,
    )
    
    # Setup global tracker with some failed reads and searches
    tracker = _reset_evidence_tracker()
    tracker.record_file_read("non_existent.py", success=False)
    tracker.record_search("missing_pattern", [])

    # Mock response containing duplicate failed tool calls
    duplicate_failed_response = (
        "Let me try reading the file again.\n"
        "READ: non_existent.py\n"
        "SEARCH: missing_pattern\n"
    )

    # Call process_response and ensure it returns early with the loop warning
    with patch("sage.main._get_current_classification") as mock_class:
        # Mock class to return a read-only analysis classification
        mock_class.return_value = MagicMock(read_only=True, is_informational=False)
        
        written, final_response = agent.process_response(
            duplicate_failed_response,
            tool_depth=0,
            phase_name="analysis",
        )

        # Assertions
        assert written == []
        assert final_response.strip() == duplicate_failed_response.strip()
        mock_renderer.warning.assert_any_call(
            "⚠️ Repetition loop detected: all requested files/searches have already failed. Stopping tool execution."
        )
