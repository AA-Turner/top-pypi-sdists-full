import pytest
from pathlib import Path
from sage.core.request_classifier import EvidenceTracker
from sage.cli_core import SAGEAgent, _reset_evidence_tracker, _get_evidence_tracker
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


class DummyRenderer:
    def __init__(self):
        self.warnings = []
        self.infos = []
    def warning(self, msg):
        self.warnings.append(msg)
    def info(self, msg):
        self.infos.append(msg)
    def get_output_mode(self):
        return "clean"
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

class DummyEngine:
    def clear(self):
        pass
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

class DummyClassification:
    def __init__(self):
        self.read_only = True
        self.is_informational = False
        self.request_type = "ANALYSIS"
        self.quantity_required = False
        self.target_entities = []
    def __getattr__(self, name):
        return None

def test_agent_execution_ledger_initialization(monkeypatch):
    """Verify that SAGEAgent.execution_ledger is correctly initialized and reset."""
    import sage.main as sage_main
    
    dummy_renderer = DummyRenderer()
    dummy_engine = DummyEngine()
    dummy_router = None

    agent = SAGEAgent(
        cwd=Path("."),
        renderer=dummy_renderer,
        engine=dummy_engine,
        router=dummy_router,
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
    
    # Patch dependencies
    monkeypatch.setattr(sage_main, "_classify_and_store_request", lambda prompt: DummyClassification())
    monkeypatch.setattr(sage_main, "_check_context_relevance", lambda p1, p2: True)
    
    def raise_on_send(prompt, *args, **kwargs):
        raise RuntimeError("Stop execution path")
        
    monkeypatch.setattr(agent, "send_to_model", raise_on_send)
    
    try:
        agent.execute_task_prompt("test task")
    except RuntimeError:
        pass
        
    assert isinstance(agent.execution_ledger, ExecutionLedger)
    assert len(agent.execution_ledger.files_read) == 0  # Should be reset/re-initialized


def test_repetition_loop_prevention(monkeypatch):
    """Verify that process_response stops execution when all commands have already failed."""
    import sage.main as sage_main
    
    dummy_renderer = DummyRenderer()
    dummy_engine = DummyEngine()
    dummy_router = None

    agent = SAGEAgent(
        cwd=Path(".").resolve(),
        renderer=dummy_renderer,
        engine=dummy_engine,
        router=dummy_router,
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

    # Response containing duplicate failed tool calls
    duplicate_failed_response = (
        "Let me try reading the file again.\n"
        "READ: non_existent.py\n"
        "SEARCH: missing_pattern\n"
    )

    # Call process_response and ensure it returns early with the loop warning
    monkeypatch.setattr(sage_main, "_get_current_classification", lambda: DummyClassification())
    
    written, final_response = agent.process_response(
        duplicate_failed_response,
        tool_depth=0,
        phase_name="analysis",
    )

    # Assertions
    assert written == []
    assert final_response.strip() == duplicate_failed_response.strip()
    assert any("Repetition loop detected" in w for w in dummy_renderer.warnings)
