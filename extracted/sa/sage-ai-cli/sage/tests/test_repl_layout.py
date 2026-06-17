import pytest
from pathlib import Path
from sage.core.repl import SageREPL
from sage.main import _build_prompt_reader
from sage.core.validation import is_garbage_content
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.keys import Keys

def test_repl_layout_initialization():
    class DummyAgent:
        pass
    def dummy_execute(text):
        pass
    repl = SageREPL(DummyAgent(), dummy_execute)
    
    # Check that status container was inserted at index 0
    children = repl.session.layout.container.children
    assert len(children) > 0
    assert isinstance(children[0], ConditionalContainer)

def test_repl_bracketed_paste_handling():
    class DummyAgent:
        pass
    def dummy_execute(text):
        pass
    repl = SageREPL(DummyAgent(), dummy_execute)
    
    # Check that Keys.BracketedPaste is in the key bindings list
    has_bracketed_paste = any(Keys.BracketedPaste in b.keys for b in repl.kb.bindings)
    assert has_bracketed_paste

def test_build_prompt_reader_bracketed_paste(monkeypatch, tmp_path):
    # Force isatty to return True so we take the prompt_toolkit path
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    
    # Store the instantiated key bindings here
    captured_kb = []
    
    class DummyPromptSession:
        def __init__(self, **kwargs):
            kb = kwargs.get('key_bindings')
            captured_kb.append(kb)
            class DummyLayout:
                class DummyContainer:
                    def __init__(self):
                        self.children = []
                def __init__(self):
                    self.container = DummyLayout.DummyContainer()
            self.layout = DummyLayout()
            
    import prompt_toolkit
    monkeypatch.setattr(prompt_toolkit, "PromptSession", DummyPromptSession)
    
    _build_prompt_reader(tmp_path)
    
    assert len(captured_kb) == 1
    kb = captured_kb[0]
    assert kb is not None
    
    # Verify Keys.BracketedPaste binding is registered
    paste_binding = next((b for b in kb.bindings if Keys.BracketedPaste in b.keys), None)
    assert paste_binding is not None
    
    class DummyBuffer:
        def __init__(self):
            self.inserted = []
        def insert_text(self, text):
            self.inserted.append(text)
            
    class DummyEvent:
        def __init__(self, data, buf):
            self.data = data
            self.current_buffer = buf
            
    # 1. Test pasting large data
    buf = DummyBuffer()
    ev = DummyEvent("line1\nline2\nline3\nline4\nline5\nline6\nline7\nline8\nline9\nline10", buf)
    
    paste_binding.handler(ev)
    
    assert buf.inserted == ["[Pasted 10 lines]"]
    pastes_dir = tmp_path / ".sage" / "pastes"
    assert pastes_dir.exists()
    files = list(pastes_dir.glob("paste_*.txt"))
    assert len(files) == 1
    assert files[0].read_text(encoding="utf-8") == ev.data
    
    # 2. Test pasting small data
    buf_small = DummyBuffer()
    ev_small = DummyEvent("short single line", buf_small)
    
    paste_binding.handler(ev_small)
    assert buf_small.inserted == ["short single line"]

def test_is_garbage_content_placeholders():
    # JavaScript/TypeScript comments
    is_garbage, reason = is_garbage_content("index.js", "const x = 1;\n// TODO: implement this function\nconst y = 2;")
    assert is_garbage
    assert "TODO" in reason or "placeholder" in reason

    # Block comment placeholders
    is_garbage, reason = is_garbage_content("style.css", "/* TODO: add style rules */\nbody { background: black; }")
    assert is_garbage
    assert "TODO" in reason or "placeholder" in reason

    # HTML comment placeholders
    is_garbage, reason = is_garbage_content("index.html", "<!-- TODO: add main navigation -->\n<div>Content</div>")
    assert is_garbage
    assert "TODO" in reason or "placeholder" in reason

    # Clean code without placeholders
    is_garbage, reason = is_garbage_content("app.js", "const x = 1;\nconst y = 2;")
    assert not is_garbage

def test_greenfield_prompts_are_generic():
    from sage.main import _build_multistep_phase_prompts
    
    task_prompt = "Build a brand new chess game from scratch"
    prompts = _build_multistep_phase_prompts(task_prompt, cwd=None)
    
    # Verify that planning and implementation prompts do not contain hardcoded advertisement platform references
    for phase, content in prompts:
        assert "advertisement" not in content.lower()
        assert "campaign" not in content.lower()
        assert "expo/react native" not in content.lower()

def test_auto_validate_garbage_rejection(tmp_path):
    from sage.main import _auto_validate
    
    # Create a temporary directory structure
    file_path = tmp_path / "incomplete.js"
    file_path.write_text("const x = 1;\n// TODO: write more code", encoding="utf-8")
    
    # Validate
    res = _auto_validate(["incomplete.js"], tmp_path)
    assert res is not None
    cmd, output = res
    assert cmd == "code completeness check"
    assert "incomplete" in output.lower()

    # Clean file should pass
    clean_path = tmp_path / "complete.js"
    clean_path.write_text("const x = 1;\nconst y = 2;", encoding="utf-8")
    res_clean = _auto_validate(["complete.js"], tmp_path)
    assert res_clean is None

def test_repl_status_html_escaping():
    from sage.core.renderer import set_repl_status, clear_repl_status
    from prompt_toolkit.formatted_text import to_formatted_text
    
    class DummyAgent:
        _is_running = True
    def dummy_execute(text):
        pass
    
    repl = SageREPL(DummyAgent(), dummy_execute)
    
    # Set status message containing characters that are invalid in raw XML/HTML
    set_repl_status("Running: echo \"hello\" && python <app.py>")
    
    children = repl.session.layout.container.children
    status_window = children[0].content
    status_control = status_window.content
    
    # Evaluate the callable using prompt_toolkit's helper
    formatted = to_formatted_text(status_control.text)
    
    # Check that HTML parsing succeeded and holds resolved values
    # formatted is a list of tuples like (style_str, text_str)
    combined_text = "".join(text for _, text in formatted)
    assert "echo" in combined_text
    assert "&&" in combined_text
    assert "<app.py>" in combined_text
    
    clear_repl_status()
