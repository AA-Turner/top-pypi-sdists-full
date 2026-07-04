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
    from sage.cli_core import SAGEAgent
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
            "build_ok": True,
            "runs_ok": True,
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
    from sage.cli_core import _route_to_principal_pipeline
    from sage.core import renderer
    from sage.core.principal_builder import PrincipalBuildReport
    
    # 1. Setup mocks
    monkeypatch.setattr("sage.core.validation_helpers._pick_build_model", lambda m: (m, "Mock swap reason"))
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


def test_concurrent_token_refresh(monkeypatch):
    """Test that concurrent calls to get_valid_token() refresh the token exactly once under thread-safety lock."""
    import threading
    import time
    from sage.core import cli_auth

    # Ensure SAGE_TESTING is NOT set to "1" for this test, otherwise get_valid_token just returns "fake-test-token"
    monkeypatch.delenv("SAGE_TESTING", raising=False)

    # Mock token data
    expired_auth = {
        "id_token": "expired-token",
        "refresh_token": "refresh-token",
        "expires_at": time.time() - 3600  # expired
    }
    
    refreshed_auth = {
        "id_token": "fresh-token",
        "refresh_token": "refresh-token",
        "expires_at": time.time() + 3600  # valid
    }

    # Track how many times load_auth, save_auth, and _refresh_token are called
    state = {"auth": expired_auth, "refresh_calls": 0}

    def mock_load_auth():
        return state["auth"]

    def mock_save_auth(data):
        state["auth"] = data

    def mock_refresh_token(auth):
        state["refresh_calls"] += 1
        # Simulate some network delay to increase chances of race conditions if lock wasn't working
        time.sleep(0.1)
        res = refreshed_auth.copy()
        mock_save_auth(res)
        return res

    monkeypatch.setattr(cli_auth, "load_auth", mock_load_auth)
    monkeypatch.setattr(cli_auth, "save_auth", mock_save_auth)
    monkeypatch.setattr(cli_auth, "_refresh_token", mock_refresh_token)

    # Spawn multiple threads calling get_valid_token()
    results = []
    def run_get_token():
        try:
            token = cli_auth.get_valid_token()
            results.append(token)
        except Exception as e:
            results.append(e)

    threads = [threading.Thread(target=run_get_token) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # All threads should have received "fresh-token"
    assert all(r == "fresh-token" for r in results), f"Expected all results to be 'fresh-token', got {results}"
    # _refresh_token should only be called once because the subsequent threads saw the refreshed token
    assert state["refresh_calls"] == 1, f"Expected exactly 1 refresh call, got {state['refresh_calls']}"


def test_parse_fixes_from_llm_json_strict_false():
    """Verify that json parsing with strict=False allows literal control characters (newlines/tabs)."""
    from sage.core.dynamic_builder import _parse_fixes_from_llm
    from pathlib import Path

    # JSON with a literal newline inside a string property
    raw = """
    {
      "app/main.py": "from fastapi import FastAPI
app = FastAPI()"
    }
    """
    fixes = _parse_fixes_from_llm(raw, [Path("app/main.py")], [], Path("/tmp"))
    assert fixes is not None
    assert fixes["app/main.py"] == "from fastapi import FastAPI\napp = FastAPI()"


def test_parse_fixes_from_llm_markdown_fallback():
    """Verify that Markdown code block extraction maps comments to target files."""
    from sage.core.dynamic_builder import _parse_fixes_from_llm
    from pathlib import Path

    raw = """
    We need to update two files.
    
    Here is the first file:
    ```python
    # filepath: app/core/security.py
    ALGORITHM = "HS256"
    ```
    
    And here is the second file:
    ```python
    # app/webhooks/handlers.py
    import jwt
    ```
    """
    relevant = [Path("/tmp/app/core/security.py"), Path("/tmp/app/webhooks/handlers.py")]
    fixes = _parse_fixes_from_llm(raw, relevant, [], Path("/tmp"))
    assert fixes is not None
    assert "app/core/security.py" in fixes
    assert "app/webhooks/handlers.py" in fixes
    assert 'ALGORITHM = "HS256"' in fixes["app/core/security.py"]
    assert "import jwt" in fixes["app/webhooks/handlers.py"]


def test_parse_fixes_from_llm_single_file_fallback():
    """Verify that single target file fallback maps raw code output to that target."""
    from sage.core.dynamic_builder import _parse_fixes_from_llm
    from pathlib import Path

    raw = """
    ```python
    def health_check():
        return {"status": "ok"}
    ```
    """
    fixes = _parse_fixes_from_llm(raw, [Path("/tmp/app/api/health.py")], [], Path("/tmp"))
    assert fixes is not None
    assert "app/api/health.py" in fixes
    assert "def health_check():" in fixes["app/api/health.py"]


def test_parse_fixes_from_llm_json_cleaning():
    """Verify that _parse_fixes_from_llm can parse and clean up malformed JSON."""
    from sage.core.dynamic_builder import _parse_fixes_from_llm
    from pathlib import Path

    # JSON with single quotes, trailing commas, and line comments
    raw = """
    Here is the JSON fix:
    {
      'app/main.py': 'from fastapi import FastAPI\napp = FastAPI()', // this is a comment
      'app/utils.py': 'def foo():\n    return 42',
    }
    """
    relevant = [Path("app/main.py"), Path("app/utils.py")]
    fixes = _parse_fixes_from_llm(raw, relevant, [], Path("/tmp"))
    assert fixes is not None
    assert "app/main.py" in fixes
    assert "app/utils.py" in fixes
    assert "FastAPI" in fixes["app/main.py"]
    assert "def foo():" in fixes["app/utils.py"]


def test_parse_fixes_from_llm_preceding_text_filename():
    """Verify that _parse_fixes_from_llm can associate a code block with preceding text filename."""
    from sage.core.dynamic_builder import _parse_fixes_from_llm
    from pathlib import Path

    raw = """
    We need to update two files.
    
    Here is the first update for app/core/security.py:
    ```python
    ALGORITHM = "HS256"
    ```
    
    Now, let's fix backend/app/webhooks/handlers.py with this change:
    ```python
    import jwt
    ```
    """
    relevant = [Path("/tmp/app/core/security.py"), Path("/tmp/app/webhooks/handlers.py")]
    fixes = _parse_fixes_from_llm(raw, relevant, [], Path("/tmp"))
    assert fixes is not None
    assert "app/core/security.py" in fixes
    assert "app/webhooks/handlers.py" in fixes
    assert 'ALGORITHM = "HS256"' in fixes["app/core/security.py"]
    assert "import jwt" in fixes["app/webhooks/handlers.py"]


def test_attempt_repair_validation_retry_loop(tmp_path, monkeypatch):
    """Verify that _attempt_repair retries validation failures and writes valid code."""
    from sage.core.dynamic_builder import _attempt_repair
    from sage.core.install_verify import StepResult
    from sage.core import principal_builder
    
    # Setup mock project
    class DummyProject:
        def __init__(self, root):
            self.kind = "python"
            self.root = root
            
    project = DummyProject(tmp_path)
    step = StepResult(name="pytest", ok=False, returncode=1, log="undefined name: ALGORITHM", duration_s=1.0)
    
    # We will simulate the LLM outputting:
    # 1. Broken code (NameError/undefined name)
    # 2. Corrected code (defining ALGORITHM)
    attempts = []
    def mock_generate(prompt):
        attempts.append(prompt)
        if len(attempts) == 1:
            # First attempt: uses ALGORITHM without defining it
            return '{"app/core/security.py": "print(ALGORITHM)"}'
        else:
            # Second attempt: defines ALGORITHM
            return '{"app/core/security.py": "ALGORITHM = \\"HS256\\"\\nprint(ALGORITHM)"}'
            
    # Mock _likely_files_for_step
    monkeypatch.setattr("sage.core.dynamic_builder._likely_files_for_step", lambda p, s: [tmp_path / "app/core/security.py"])
    
    # Pre-create the file so read_text() inside _attempt_repair succeeds
    target_file = tmp_path / "app/core/security.py"
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text("print(ALGORITHM)", encoding="utf-8")
    
    # Run repair
    mock_log = []
    _attempt_repair(project, step, generate=mock_generate, log=mock_log.append)
    
    # Verify that it retried once and succeeded on the second attempt
    assert len(attempts) == 2
    # Verify validation warning was logged
    assert any("failed validation" in m for m in mock_log)
    # Verify file was written
    target = tmp_path / "app/core/security.py"
    assert target.exists()
    assert 'ALGORITHM = "HS256"' in target.read_text()


def test_verify_report_all_four_checks():
    """Verify that VerifyReport correctly parses all four verification checks (install_ok, build_ok, runs_ok, tests_ok) from steps."""
    from sage.core.install_verify import VerifyReport, StepResult, DiscoveredProject
    
    project = DiscoveredProject(kind="python", root=Path("/tmp"))
    
    # Test all None if steps are empty or mismatching names
    report_empty = VerifyReport(project=project, steps=[])
    assert report_empty.install_ok is None
    assert report_empty.build_ok is None
    assert report_empty.runs_ok is None
    assert report_empty.tests_ok is None
    
    # Test install_ok matches install, tidy, restore
    report_install_fail = VerifyReport(project=project, steps=[
        StepResult(name="npm install", ok=False, returncode=1, log="", duration_s=1.0)
    ])
    assert report_install_fail.install_ok is False
    assert report_install_fail.build_ok is None
    
    report_tidy_ok = VerifyReport(project=project, steps=[
        StepResult(name="go mod tidy", ok=True, returncode=0, log="", duration_s=1.0)
    ])
    assert report_tidy_ok.install_ok is True
    
    # Test build_ok matches compile or build
    report_build_fail = VerifyReport(project=project, steps=[
        StepResult(name="npm run build", ok=False, returncode=1, log="", duration_s=1.0)
    ])
    assert report_build_fail.build_ok is False
    assert report_build_fail.runs_ok is None

    report_compile_ok = VerifyReport(project=project, steps=[
        StepResult(name="go compile", ok=True, returncode=0, log="", duration_s=1.0)
    ])
    assert report_compile_ok.build_ok is True
    assert report_compile_ok.runs_ok is None

    # Test runs_ok matches run check, start check, import check
    report_run_fail = VerifyReport(project=project, steps=[
        StepResult(name="start check", ok=False, returncode=1, log="", duration_s=1.0)
    ])
    assert report_run_fail.build_ok is None
    assert report_run_fail.runs_ok is False

    report_import_ok = VerifyReport(project=project, steps=[
        StepResult(name="python import check", ok=True, returncode=0, log="", duration_s=1.0)
    ])
    assert report_import_ok.build_ok is None
    assert report_import_ok.runs_ok is True

    # Test tests_ok matches test, pytest, rspec, ctest
    report_test_fail = VerifyReport(project=project, steps=[
        StepResult(name="pytest", ok=False, returncode=1, log="", duration_s=1.0)
    ])
    assert report_test_fail.tests_ok is False
    
    report_test_ok = VerifyReport(project=project, steps=[
        StepResult(name="npm test", ok=True, returncode=0, log="", duration_s=1.0)
    ])
    assert report_test_ok.tests_ok is True


def test_repl_agent_task_ok_requires_build_and_run(monkeypatch):
    """Verify that REPLAgent.execute_task_prompt requires install_ok, build_ok, runs_ok, and tests_ok to all be True/not-False."""
    from sage.cli_core import SAGEAgent
    from pathlib import Path

    class DummyRenderer:
        def __init__(self):
            self.infos = []
        def info(self, msg, *args, **kwargs):
            self.infos.append(msg)
        def get_output_mode(self):
            return "normal"
        def print_assistant_response(self, *args, **kwargs):
            pass

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

    # Make sure we route to principal pipeline by forcing looks_like_build_request to True
    monkeypatch.setattr("sage.core.principal_engineer.looks_like_build_request", lambda prompt: True)

    # 1. Test case when install_ok is False
    monkeypatch.setattr("sage.main._route_to_principal_pipeline", lambda *args, **kwargs: {
        "install_ok": False,
        "build_ok": True,
        "runs_ok": True,
        "tests_ok": True,
        "out_dir": "/tmp",
    })
    _, task_ok = dummy_agent.execute_task_prompt("Build an app", save_history=False, enhanced_mode=True)
    assert task_ok is False

    # 2. Test case when build_ok is False
    monkeypatch.setattr("sage.main._route_to_principal_pipeline", lambda *args, **kwargs: {
        "install_ok": True,
        "build_ok": False,
        "runs_ok": True,
        "tests_ok": True,
        "out_dir": "/tmp",
    })
    _, task_ok = dummy_agent.execute_task_prompt("Build an app", save_history=False, enhanced_mode=True)
    assert task_ok is False

    # 3. Test case when runs_ok is False
    monkeypatch.setattr("sage.main._route_to_principal_pipeline", lambda *args, **kwargs: {
        "install_ok": True,
        "build_ok": True,
        "runs_ok": False,
        "tests_ok": True,
        "out_dir": "/tmp",
    })
    _, task_ok = dummy_agent.execute_task_prompt("Build an app", save_history=False, enhanced_mode=True)
    assert task_ok is False

    # 4. Test case when tests_ok is False
    monkeypatch.setattr("sage.main._route_to_principal_pipeline", lambda *args, **kwargs: {
        "install_ok": True,
        "build_ok": True,
        "runs_ok": True,
        "tests_ok": False,
        "out_dir": "/tmp",
    })
    _, task_ok = dummy_agent.execute_task_prompt("Build an app", save_history=False, enhanced_mode=True)
    assert task_ok is False

    # 5. Test case when all 4 are True
    monkeypatch.setattr("sage.main._route_to_principal_pipeline", lambda *args, **kwargs: {
        "install_ok": True,
        "build_ok": True,
        "runs_ok": True,
        "tests_ok": True,
        "out_dir": "/tmp",
    })
    _, task_ok = dummy_agent.execute_task_prompt("Build an app", save_history=False, enhanced_mode=True)
    assert task_ok is True


def test_pre_validate_content_rejects_incomplete():
    """Verify that pre_validate_content flags placeholder stubs, TODOs, and syntax errors."""
    from sage.core.validation import pre_validate_content
    
    # 1. Placeholder stubs in functions
    incomplete_fn = "def do_something(x):\n    pass"
    ok, error = pre_validate_content("main.py", incomplete_fn)
    assert ok is False
    assert "empty function" in error or "stub" in error
    
    # 2. raise NotImplementedError
    nie_code = "def process():\n    raise NotImplementedError('TODO')"
    ok, error = pre_validate_content("main.py", nie_code)
    assert ok is False
    assert "placeholder" in error or "NotImplementedError" in error or "stub" in error

    # 3. Truncated file ending in ...
    truncated_code = "def helper():\n    return 42\n..."
    ok, error = pre_validate_content("main.py", truncated_code)
    assert ok is False
    assert "truncated" in error

    # 4. Correct complete code
    valid_code = "def helper():\n    return 42\n\ndef run():\n    res = helper()\n    print(res)"
    ok, error = pre_validate_content("main.py", valid_code)
    assert ok is True


def test_extract_and_write_files_captures_failed_writes(tmp_path):
    """Verify that _extract_and_write_files records validation errors in failed_writes."""
    from sage.core.validation_helpers import _extract_and_write_files
    
    # JSON content containing syntax error + placeholder
    failed_writes = {}
    bad_code_response = """
FILE: failed_test.py
```python
def broken_syntax(x)  # Missing colon
    pass
```
    """
    written = _extract_and_write_files(
        bad_code_response,
        tmp_path,
        failed_writes=failed_writes
    )
    assert len(written) == 0
    assert "failed_test.py" in failed_writes
    assert "Syntax error" in failed_writes["failed_test.py"] or "syntax" in failed_writes["failed_test.py"].lower()


def test_repl_agent_retries_on_failed_file_writes(monkeypatch, tmp_path):
    """Verify that SAGEAgent.process_response triggers the retry flow on failed writes."""
    from sage.cli_core import SAGEAgent
    from pathlib import Path

    class DummyRenderer:
        def __init__(self):
            self.infos = []
        def info(self, msg, *args, **kwargs):
            self.infos.append(msg)
        def warning(self, msg, *args, **kwargs):
            pass
        def error(self, msg, *args, **kwargs):
            pass
        def set_bottom_dock_status(self, *args, **kwargs):
            pass
        def print_files_written(self, *args, **kwargs):
            pass
        def get_output_mode(self):
            return "normal"

    class DummyEngine:
        def __init__(self):
            self.system_prompt = "system prompt"
            self._messages = []

    dummy_agent = SAGEAgent(
        cwd=tmp_path,
        renderer=DummyRenderer(),
        engine=DummyEngine(),
        router=None,
        model_id="test-model",
        temp=0.1,
        tokens=4096,
        model_locked=False,
        is_local=False,
    )

    # We will simulate:
    # 1. First response: writes a broken python file (missing colon)
    # 2. Model retry: returns a corrected version
    model_responses = [
        # Correct response on retry
        """
FILE: corrected.py
```python
def build_me():
    return "done"
```
        """
    ]

    def mock_send(prompt):
        # Check that prompt mentions the validation defect
        assert "defect" in prompt.lower() or "rejected" in prompt.lower()
        assert "corrected.py" in prompt
        return model_responses.pop(0)

    # Monkeypatch looks_like_build_request and _get_current_task_prompt
    monkeypatch.setattr("sage.core.principal_engineer.looks_like_build_request", lambda prompt: False)
    monkeypatch.setattr("sage.main._get_current_task_prompt", lambda: "Build a helper function")

    # Initial response containing a syntax error
    initial_response = """
FILE: corrected.py
```python
def build_me()
    pass
```
    """

    written, final_response = dummy_agent.process_response(
        initial_response,
        send_fn=mock_send
    )

    assert "corrected.py" in written
    assert len(model_responses) == 0  # mock_send was called to retrieve the corrected version
    assert (tmp_path / "corrected.py").exists()
    assert 'return "done"' in (tmp_path / "corrected.py").read_text()


def test_scaffold_continuation_empty_round_handling(monkeypatch, tmp_path):
    """Verify that scaffold continuation breaks after empty rounds when model returns premature SCAFFOLD_COMPLETE."""
    from sage.cli_core import SAGEAgent
    from pathlib import Path
    
    warnings = []
    class DummyRenderer:
        def __init__(self):
            self.infos = []
        def info(self, msg, *args, **kwargs):
            self.infos.append(msg)
        def success(self, msg, *args, **kwargs):
            pass
        def warning(self, msg, *args, **kwargs):
            warnings.append(msg)
        def phase(self, *args, **kwargs):
            pass
        def get_output_mode(self):
            return "normal"
        def activate_bottom_dock(self, *args, **kwargs):
            return True
        def set_bottom_dock_todos(self, *args, **kwargs):
            pass
        def set_bottom_dock_status(self, *args, **kwargs):
            pass
        def print_validation_start(self, *args, **kwargs):
            pass
        def print_validation_success(self, *args, **kwargs):
            pass
        def print_validation_failure(self, *args, **kwargs):
            pass
        def print_files_written(self, *args, **kwargs):
            pass
        def clear_bottom_dock_todos(self, *args, **kwargs):
            pass
        def deactivate_bottom_dock(self, *args, **kwargs):
            pass
            
    class DummyEngine:
        def __init__(self):
            self.system_prompt = "system prompt"
            self._messages = []
        def clear(self):
            pass
            
    dummy_agent = SAGEAgent(
        cwd=tmp_path,
        renderer=DummyRenderer(),
        engine=DummyEngine(),
        router=None,
        model_id="test-model",
        temp=0.1,
        tokens=4096,
        model_locked=False,
        is_local=False,
    )
    
    # Enable greenfield manifest with missing file
    dummy_agent._greenfield_manifest = ["app/main.py"]
    
    # Mock helpers
    monkeypatch.setattr("sage.core.principal_engineer.looks_like_build_request", lambda prompt: False)
    monkeypatch.setattr("sage.main._get_current_task_prompt", lambda: "Build a brand new platform")
    monkeypatch.setattr("sage.main._auto_validate", lambda *args, **kwargs: None)
    monkeypatch.setattr("sage.core.validation.pre_validate_content", lambda *args, **kwargs: (True, ""))
    monkeypatch.setattr("sage.core.validation_helpers._pre_validate_content", lambda *args, **kwargs: (True, ""))
    
    # First response (multistep plan/planning response)
    responses = [
        "FILE_MANIFEST:\napp/main.py\n\nI will do this.\n\nFILE: app/utils.py\n```python\n# Utils\n```",
        # Batch continuation responses
        "SCAFFOLD_COMPLETE\nNo new files.",
        "SCAFFOLD_COMPLETE\nNo new files.",
    ]
    
    # Set SAGE_BATCH_LIMIT to 5
    monkeypatch.setenv("SAGE_BATCH_LIMIT", "5")
    
    send_calls = []
    def mock_send(prompt):
        send_calls.append(prompt)
        if responses:
            return responses.pop(0)
        return "SCAFFOLD_COMPLETE"
        
    # Mock _execute_multistep to simulate writing the first file
    def mock_execute_multistep(prompt, send_fn, classification=None):
        # Write first file
        (tmp_path / "app/utils.py").parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / "app/utils.py").write_text("# Utils", encoding="utf-8")
        dummy_agent._greenfield_manifest = ["app/main.py"]
        return ["app/utils.py"], "FILE_MANIFEST:\napp/main.py\n\nFILE: app/utils.py\n```python\n# Utils\n```"
        
    monkeypatch.setattr(dummy_agent, "_execute_multistep", mock_execute_multistep)
    
    # Run task prompt
    written, task_ok = dummy_agent.execute_task_prompt(
        "Build a brand new platform",
        save_history=False,
        enhanced_mode=True,
        sender=mock_send
    )
    
    # Verify the warning is present in the prompt for batch 3 (send_calls[2]) after model declared done in batch 2
    assert len(send_calls) >= 3
    assert "⚠️ WARNING: In the previous batch, you output SCAFFOLD_COMPLETE" in send_calls[2]
    
    # Check that it warns "Model declared done but 1 manifest files still missing"
    assert any("still missing — continuing" in w for w in warnings)


def test_parse_fixes_from_llm_accepts_valid_unlisted_files(tmp_path):
    """Verify that _parse_fixes_from_llm accepts unlisted code files under project root and normalizes absolute/relative keys."""
    from sage.core.dynamic_builder import _parse_fixes_from_llm
    
    # Setup test directories
    project_root = tmp_path / "project"
    project_root.mkdir(parents=True, exist_ok=True)
    
    # 1. Test case: JSON contains an unlisted file that exists on disk
    existing_file = project_root / "src/components/Button.tsx"
    existing_file.parent.mkdir(parents=True, exist_ok=True)
    existing_file.write_text("// Existing button code", encoding="utf-8")
    
    # Target files list only has package.json (heuristic mismatch)
    targets = [project_root / "package.json"]
    
    raw_json = '{"src/components/Button.tsx": "export const Button = () => <button>Click</button>"}'
    fixes = _parse_fixes_from_llm(raw_json, targets, [], project_root)
    assert fixes is not None
    assert "src/components/Button.tsx" in fixes
    assert "export const Button" in fixes["src/components/Button.tsx"]
    
    # 2. Test case: JSON contains an unlisted file that does not exist yet, but has a valid code extension under project root
    raw_json_new = '{"backend/app/api/new_endpoint.py": "def new_api(): return 42"}'
    fixes_new = _parse_fixes_from_llm(raw_json_new, targets, [], project_root)
    assert fixes_new is not None
    assert "backend/app/api/new_endpoint.py" in fixes_new
    assert "def new_api():" in fixes_new["backend/app/api/new_endpoint.py"]

    # 3. Test case: JSON contains absolute paths, which should be normalized to project-relative keys
    absolute_key = str((project_root / "backend/main.py").resolve())
    raw_json_absolute = f'{{"{absolute_key}": "print(\\"hello\\")"}}'
    fixes_absolute = _parse_fixes_from_llm(raw_json_absolute, targets, [], project_root)
    assert fixes_absolute is not None
    assert "backend/main.py" in fixes_absolute
    assert fixes_absolute["backend/main.py"] == 'print("hello")'


def test_attempt_repair_with_unlisted_files(tmp_path):
    """Verify that _attempt_repair successfully applies fixes for files not heuristically identified by _likely_files_for_step, preventing regression of the healing loop parsing bug, without mocking validation or file matching."""
    from sage.core.dynamic_builder import _attempt_repair
    from sage.core.install_verify import StepResult
    from sage.core.install_verify import DiscoveredProject
    
    project = DiscoveredProject(kind="node", root=tmp_path)
    # The step log has no relative paths, only absolute or general descriptions
    step = StepResult(name="npm typecheck", ok=False, returncode=1, log="Type error: Property 'user' does not exist on type 'Session' at /usr/local/node/lib/index.js", duration_s=1.0)
    
    # Pre-create candidate files so real _likely_files_for_step discovers them naturally
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    (tmp_path / "tsconfig.json").write_text("{}", encoding="utf-8")
    
    broken_file_path = tmp_path / "src/app/session.ts"
    broken_file_path.parent.mkdir(parents=True, exist_ok=True)
    broken_file_path.write_text("export type Session = { id: string };", encoding="utf-8")
    
    # Simple Python generator (no mock library) returning the corrected JSON contents
    def mock_generate(prompt):
        return '{"src/app/session.ts": "export type Session = { id: string; user?: string };"}'
        
    mock_log = []
    # Call _attempt_repair with the real pre-write validator and the real heuristic resolver running end-to-end
    _attempt_repair(project, step, generate=mock_generate, log=mock_log.append)
    
    # Verify that the unlisted file was correctly written and the bug was bypassed successfully
    assert broken_file_path.exists()
    assert 'user?: string' in broken_file_path.read_text()
    assert any("wrote src/app/session.ts" in m for m in mock_log)
    assert not any("could not parse fix" in m for m in mock_log)


def test_init_py_interceptor(tmp_path, monkeypatch):
    """Verify that writing to __init__.py is intercepted and results in a 0-byte file on disk."""
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    init_path = tmp_path / "__init__.py"
    
    # Write using builtins.open
    with open(init_path, "w") as f:
        f.write("import os\n")
        
    assert init_path.exists()
    assert init_path.stat().st_size == 0
    
    # Write using pathlib.Path
    init_path.write_text("some content")
    assert init_path.stat().st_size == 0


def test_verify_iterate_until_green_returns_list_at_max_rounds(tmp_path, monkeypatch):
    """Verify that _verify_iterate_until_green returns a list of VerifyReports even when loop max rounds are reached."""
    from sage.core.dynamic_builder import _verify_iterate_until_green
    from sage.core.install_verify import VerifyReport, StepResult, DiscoveredProject
    
    # 1. Setup mock functions
    project = DiscoveredProject(kind="python", root=tmp_path)
    reports = [VerifyReport(project=project, steps=[
        StepResult(name="pytest", ok=False, returncode=1, log="some error", duration_s=1.0)
    ])]
    
    # Mock verify_all to always return failing reports
    monkeypatch.setattr("sage.core.dynamic_builder.verify_all", lambda path: reports)
    
    # Mock _attempt_repair to do nothing
    monkeypatch.setattr("sage.core.dynamic_builder._attempt_repair", lambda *args, **kwargs: None)
    
    # Run _verify_iterate_until_green
    logs = []
    res = _verify_iterate_until_green(
        tmp_path,
        generate=lambda p: "",
        log=logs.append,
        stuck_threshold=10,  # avoid triggering stuck detection before round 8
    )
    
    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0].project.kind == "python"
    assert any("round 8/8" in m for m in logs)


def test_media_asset_generation_instructions(monkeypatch):
    """Verify that build_agent_system_prompt includes the new MEDIA & ASSET GENERATION instructions."""
    from sage.core.prompts import build_agent_system_prompt
    from pathlib import Path
    
    prompt = build_agent_system_prompt(Path("."), is_local=False)
    assert "MEDIA & ASSET GENERATION" in prompt
    assert "programmatically generating any kind of media asset" in prompt
    assert "ffmpeg" in prompt
    assert "pillow" in prompt
    
    local_prompt = build_agent_system_prompt(Path("."), is_local=True)
    assert "Media & Asset Generation (CRITICAL)" in local_prompt
    assert "programmatically generate the actual file" in local_prompt


def test_remove_duplicate_jest_configs(tmp_path):
    """Verify that remove_duplicate_jest_configs deletes jest.config.ts if jest.config.js also exists."""
    from sage.core.code_doctors import remove_duplicate_jest_configs
    
    # 1. Neither exists
    assert remove_duplicate_jest_configs(tmp_path) == 0
    
    # 2. Only JS exists
    (tmp_path / "jest.config.js").write_text("module.exports = {};")
    assert remove_duplicate_jest_configs(tmp_path) == 0
    assert (tmp_path / "jest.config.js").exists()
    
    # 3. Both exist
    (tmp_path / "jest.config.ts").write_text("export default {};")
    assert remove_duplicate_jest_configs(tmp_path) == 1
    assert (tmp_path / "jest.config.js").exists()
    assert not (tmp_path / "jest.config.ts").exists()


def test_fix_tsconfig_types(tmp_path):
    """Verify that fix_tsconfig_types removes react-native-web from tsconfig.json compilerOptions.types."""
    from sage.core.code_doctors import fix_tsconfig_types
    
    # 1. No tsconfig.json
    assert fix_tsconfig_types(tmp_path) == 0
    
    # 2. tsconfig without types
    tsconfig = tmp_path / "tsconfig.json"
    tsconfig.write_text('{"compilerOptions": {}}')
    assert fix_tsconfig_types(tmp_path) == 0
    
    # 3. tsconfig with react-native-web in types (JSON format)
    tsconfig.write_text('{"compilerOptions": {"types": ["react-native", "react-native-web"]}}')
    assert fix_tsconfig_types(tmp_path) == 1
    import json
    data = json.loads(tsconfig.read_text())
    assert "react-native-web" not in data["compilerOptions"]["types"]
    assert "react-native" in data["compilerOptions"]["types"]
    
    # 4. tsconfig with comments (regex fallback)
    tsconfig.write_text('{\n  // Some comment\n  "compilerOptions": {\n    "types": [\n      "react-native",\n      "react-native-web"\n    ]\n  }\n}')
    assert fix_tsconfig_types(tmp_path) == 1
    content = tsconfig.read_text()
    assert "react-native-web" not in content
    assert "react-native" in content


def test_fix_package_level_imports(tmp_path):
    """Verify that fix_package_level_imports resolves package-level imports to direct modules."""
    from sage.core.code_doctors import fix_package_level_imports
    
    backend_dir = tmp_path / "backend"
    app_models_dir = backend_dir / "app" / "models"
    app_models_dir.mkdir(parents=True, exist_ok=True)
    
    # Create background_visuals.py model file
    (app_models_dir / "background_visuals.py").write_text("""
class BackgroundVisuals:
    id: int
""")
    (app_models_dir / "user.py").write_text("""
class User:
    id: int
""")
    (app_models_dir / "__init__.py").write_text("")
    
    # Create a file that has wrong package-level imports
    test_py = backend_dir / "test_import.py"
    test_py.write_text("""
from app.models import User, BackgroundVisuals
print(User, BackgroundVisuals)
""")
    
    assert fix_package_level_imports(test_py) == 1
    
    resolved_content = test_py.read_text()
    assert "from app.models.user import User" in resolved_content
    assert "from app.models.background_visuals import BackgroundVisuals" in resolved_content
    assert "from app.models import" not in resolved_content


