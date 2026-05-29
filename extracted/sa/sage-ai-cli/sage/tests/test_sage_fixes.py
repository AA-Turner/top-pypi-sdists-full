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

def test_repl_status_ui_hides_when_message_cleared(monkeypatch):
    """Test that get_status_text in repl.py returns HTML('') when status message is cleared."""
    from sage.core.repl import SageREPL
    from sage.core.renderer import clear_repl_status, set_repl_status
    
    class DummyAgent:
        def __init__(self):
            self._is_running = True
            
    dummy_agent = DummyAgent()
    repl = SageREPL(agent=dummy_agent, execute_fn=lambda x: None)
    
    # Get the get_status_text function from FormattedTextControl
    get_status_text = repl.session.layout.container.children[0].content.content.text
    
    # 1. Setup active message
    set_repl_status("Loading...", "thinking")
    text = get_status_text()
    # The formatted HTML contains styling tags but should render 'Loading...'
    assert "Loading..." in text.value
    
    # 2. Clear status message
    clear_repl_status()
    text_cleared = get_status_text()
    assert text_cleared.value == ""

def test_strip_markdown_fences():
    """Verify that strip_markdown_fences correctly strips code block fences from content."""
    from sage.core.tools import strip_markdown_fences
    
    content = "```python\nimport sys\nprint('hello')\n```"
    assert strip_markdown_fences(content) == "import sys\nprint('hello')"
    
    content_no_fence = "import sys\nprint('hello')"
    assert strip_markdown_fences(content_no_fence) == "import sys\nprint('hello')"
    
    content_with_whitespace = "\n\n```javascript\nconst x = 1;\n```\n\n"
    assert strip_markdown_fences(content_with_whitespace) == "const x = 1;"

def test_classification_with_pasted_logs():
    """Verify that request classifier strips previous terminal output/logs and markdown blocks to determine correct intent."""
    classifier = RequestClassifierV2()
    
    pasted_prompt = """
📊 Request type: ANALYSIS (read-only analysis)
· Analysis  📊 Request type: ANALYSIS (read-only analysis)

```
Some markdown blocks showing code
```

Make the actual platform not just a prompt
    """
    
    res = classifier.classify(pasted_prompt)
    assert res.read_only is False
    assert res.request_type in (RequestTypeV2.IMPLEMENTATION, RequestTypeV2.FIX_ALL, RequestTypeV2.MULTI_STEP)

def test_no_color_with_sage_env(monkeypatch):
    """Verify that SAGE_NO_COLOR and SAGE_ASCII turn off terminal color escape codes."""
    from sage.core import renderer
    
    # 1. Test SAGE_NO_COLOR
    monkeypatch.setenv("SAGE_NO_COLOR", "1")
    # Simulate re-evaluation of _no_color_enabled
    monkeypatch.setattr(renderer, "_no_color_enabled", True)
    renderer._rebuild_consoles()
    assert renderer.console.no_color is True
    
    # 2. Test SAGE_ASCII
    monkeypatch.delenv("SAGE_NO_COLOR", raising=False)
    monkeypatch.setenv("SAGE_ASCII", "1")
    monkeypatch.setattr(renderer, "_no_color_enabled", True)
    renderer._rebuild_consoles()
    assert renderer.console.no_color is True


def test_build_routing_to_principal_pipeline(monkeypatch):
    """Verify that build requests route to principal pipeline inside execute_task_prompt."""
    from sage.main import SAGEAgent
    from pathlib import Path
    
    class DummyRenderer:
        def __init__(self):
            self.infos = []
        def info(self, msg, *args, **kwargs):
            self.infos.append(msg)
        def get_output_mode(self):
            return "normal"
            
    class DummyEngine:
        def __init__(self):
            self.system_prompt = "system prompt"
            self._messages = []
        def clear(self):
            pass
            
    dummy_agent = SAGEAgent(
        cwd=Path("/tmp"),
        renderer=DummyRenderer(),
        engine=DummyEngine(),
        router=None,
        model_id="test-model",
        temp=0.1,
        tokens=4096,
        model_locked=False,
        is_local=False,
    )
    
    route_called = []
    def mock_route(user_input, base_out_dir, router, model_id, temp, tokens, model_locked, system_prompt, **kwargs):
        route_called.append({
            "user_input": user_input,
            "base_out_dir": base_out_dir,
            "model_id": model_id,
        })
        return {
            "install_ok": True,
            "tests_ok": True,
            "out_dir": "/tmp",
        }
        
    monkeypatch.setattr("sage.main._route_to_principal_pipeline", mock_route)
    
    # Use a prompt that matches looks_like_build_request but contains negation text
    build_prompt = "Build a FastAPI backend with PostgreSQL and Redis caching. Do not modify any placeholder names."
    
    written, task_ok = dummy_agent.execute_task_prompt(build_prompt, save_history=False, enhanced_mode=True)
    
    assert len(route_called) == 1
    assert route_called[0]["user_input"] == build_prompt
    assert task_ok is True


def test_payload_truncation_logic():
    """Verify that SageHostedProvider correctly truncates intermediate messages,
    while keeping the system prompt and the latest user prompt in full.
    """
    from sage.providers.sage_hosted import SageHostedProvider
    from sage.providers.base import Message

    provider = SageHostedProvider()
    
    # 1. Test no truncation for small payload (e.g. 30KB total)
    messages = [
        Message(role="system", content="System prompt instructions"),
        Message(role="user", content="User message intermediate 1"),
        Message(role="assistant", content="Assistant reply intermediate 1"),
        Message(role="user", content="a" * 30000),  # 30KB
    ]
    payload = provider._build_request_payload(messages, "qwen3-coder", 0.7, 2048, stream=False)
    # Check that it wasn't truncated
    assert len(payload["messages"]) == 4
    assert payload["messages"][0]["content"] == "System prompt instructions"
    assert payload["messages"][-1]["content"] == "a" * 30000

    # 2. Test truncation for very large payload (> 150KB)
    system_content = "System instructions: be a helpful coding assistant."
    user_latest_content = "User latest: generate a clean code class." + "x" * 20000
    
    large_messages = [
        Message(role="system", content=system_content),
        Message(role="user", content="y" * 100000),  # 100KB intermediate
        Message(role="assistant", content="z" * 100000),  # 100KB intermediate
        Message(role="user", content=user_latest_content),
    ]
    
    payload_large = provider._build_request_payload(large_messages, "qwen3-coder", 0.7, 2048, stream=False)
    
    # The total payload length should be close to 150,000 characters
    total_len = sum(len(m["content"]) for m in payload_large["messages"])
    assert total_len <= 150000
    
    # The system message and the last user message must be preserved
    assert payload_large["messages"][0]["role"] == "system"
    assert payload_large["messages"][0]["content"] == system_content
    
    assert payload_large["messages"][-1]["role"] == "user"
    assert payload_large["messages"][-1]["content"] == user_latest_content
    
    # Check that intermediates were truncated/dropped to fit within budget
    # The first intermediate (y*100000) was processed second and should be truncated
    # The second intermediate (z*100000) was processed first and fits in budget, so it is kept in full
    assert len(payload_large["messages"][1]["content"]) < 100000
    assert len(payload_large["messages"][2]["content"]) == 100000


def test_route_to_principal_pipeline_progress_logs(monkeypatch, tmp_path):
    """Verify that build progress logs in _route_to_principal_pipeline print to the console when output mode is normal/verbose, and are silent in clean mode."""
    from sage.main import _route_to_principal_pipeline
    from sage.core import renderer
    from sage.core.principal_builder import PrincipalBuildReport
    
    # 1. Setup mocks
    monkeypatch.setattr("sage.main._pick_build_model", lambda m: (m, "Mock swap reason"))
    monkeypatch.setattr("sage.core.principal_engineer.decompose_multi_build_request", lambda prompt: [("mock-proj", prompt)])
    
    dummy_report = PrincipalBuildReport(
        title="Mock Project",
        stack={"frontend": "React", "backend": "FastAPI"},
        out_dir=str(tmp_path),
        file_count=5,
        feature_count=2,
        install_ok=True,
        tests_ok=True,
        stuck_features=[]
    )
    
    # Capture calls to build_project_principal
    build_called = []
    def mock_build(task, out_dir, generate, progress=None, **kwargs):
        build_called.append(progress)
        if progress:
            # Simulate a progress update call from the builder
            progress("Scaffolding files")
        return dummy_report
        
    monkeypatch.setattr("sage.core.principal_builder.build_project_principal", mock_build)
    
    # Mock router
    class DummyRouter:
        def generate(self, *args, **kwargs):
            return "dummy output"
    router = DummyRouter()
    
    # Mock console to capture prints
    printed_lines = []
    class DummyConsole:
        def print(self, msg, *args, **kwargs):
            printed_lines.append(msg)
    monkeypatch.setattr(renderer, "console", DummyConsole())
    
    # 2. Test in normal mode (should print logs)
    monkeypatch.setattr(renderer, "_output_mode", "normal")
    printed_lines.clear()
    
    report = _route_to_principal_pipeline(
        user_input="Build a FastAPI app with React frontend",
        base_out_dir=tmp_path,
        router=router,
        model_id="test-model",
        temp=0.1,
        tokens=2048,
        model_locked=False,
        system_prompt="system prompt"
    )
    
    assert report is not None
    # We should have captured progress output and routing logs
    assert len(printed_lines) > 0
    # Check that progress callback is called and console.print prints the progress wrapped in [dim]
    assert any("Mock swap reason" in line for line in printed_lines)
    assert any("[dim]Scaffolding files[/dim]" in line for line in printed_lines)
    assert any("Project at: [cyan]" in line for line in printed_lines)
    
    # 3. Test in clean mode (should NOT print logs)
    monkeypatch.setattr(renderer, "_output_mode", "clean")
    printed_lines.clear()
    
    report_clean = _route_to_principal_pipeline(
        user_input="Build a FastAPI app with React frontend",
        base_out_dir=tmp_path,
        router=router,
        model_id="test-model",
        temp=0.1,
        tokens=2048,
        model_locked=False,
        system_prompt="system prompt"
    )
    
    assert report_clean is not None
    # In clean mode, progress/routing prints should be suppressed
    assert len(printed_lines) == 0




