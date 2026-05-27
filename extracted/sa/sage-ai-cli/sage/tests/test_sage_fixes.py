import os
import sys
import pytest
from pathlib import Path
from sage.core.p0_request_classification import RequestClassifierV2, RequestTypeV2
from sage.core.renderer import set_repl_active, stream_tokens_with_phase, get_repl_status, clear_repl_status

def test_make_intent_classification():
    """Verify that requests using 'make', 'generate', 'setup', etc. are classified as write-enabled implementation."""
    classifier = RequestClassifierV2()
    
    # User's exact failing prompt
    res = classifier.classify("Make the actual platform, not just a prompt and make sure everything is fully tested without mocks")
    assert res.read_only is False
    assert res.request_type in (RequestTypeV2.IMPLEMENTATION, RequestTypeV2.FIX_ALL, RequestTypeV2.MULTI_STEP)

    # Test other verbs
    res2 = classifier.classify("generate the backend routes")
    assert res2.read_only is False

    res3 = classifier.classify("setup a NextJS client layout")
    assert res3.read_only is False

    res4 = classifier.classify("code a concurrent pool scheduler")
    assert res4.read_only is False

def test_ascii_mode_unicode_suppression(monkeypatch):
    """Test that SAGE_ASCII disables unicode symbols dynamically."""
    monkeypatch.setenv("SAGE_ASCII", "1")
    # Re-evaluate _use_unicode logic
    from sage.core import renderer
    monkeypatch.setattr(renderer, "_use_unicode", False)
    
    # Test that phase printing uses ASCII fallback
    class DummyConsole:
        def __init__(self):
            self.printed = []
        def print(self, text, *args, **kwargs):
            self.printed.append(text)
            
    dummy = DummyConsole()
    monkeypatch.setattr(renderer, "console", dummy)
    
    # Force normal mode so phase printing is not skipped
    renderer.set_output_mode("normal")
    
    renderer.phase("planning", "Detailed task layout")
    assert len(dummy.printed) == 1
    # Planning icon is ◎ for unicode, * for ASCII
    assert "*" in dummy.printed[0]
    assert "◎" not in dummy.printed[0]

def test_repl_thinking_status_cleared_on_stream(monkeypatch):
    """Test that the 'Thinking...' status spinner is cleared and stops updating once streaming starts."""
    from sage.core import renderer
    monkeypatch.setattr(renderer, "_is_main_thread", lambda: True)
    
    # Active REPL loop
    set_repl_active(True)
    clear_repl_status()
    
    # Dummy token generator
    tokens = ["hello", "world", "done"]
    
    # Run stream
    # Ensure isatty is false so Live spinner isn't started
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)
    
    res = stream_tokens_with_phase(tokens, model_id="test-model")
    
    # Verify status was cleared
    status = get_repl_status()
    assert not status.get("message")
    assert status.get("elapsed") == 0.0
    
    # Cleanup
    set_repl_active(False)
