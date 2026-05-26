import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from sage.core.repl import SageREPL
from sage.main import _build_prompt_reader
from sage.core.validation import is_garbage_content
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.keys import Keys

def test_repl_layout_initialization():
    agent = MagicMock()
    execute_fn = MagicMock()
    repl = SageREPL(agent, execute_fn)
    
    # Check that status container was inserted at index 0
    children = repl.session.layout.container.children
    assert len(children) > 0
    assert isinstance(children[0], ConditionalContainer)

def test_repl_bracketed_paste_handling():
    agent = MagicMock()
    execute_fn = MagicMock()
    repl = SageREPL(agent, execute_fn)
    
    # Check that Keys.BracketedPaste is in the key bindings list
    has_bracketed_paste = any(Keys.BracketedPaste in b.keys for b in repl.kb.bindings)
    assert has_bracketed_paste

@patch('sys.stdin.isatty', return_value=True)
@patch('sys.stdout.isatty', return_value=True)
def test_build_prompt_reader_bracketed_paste(mock_stdout, mock_stdin, tmp_path):
    # Patch Path.home to keep tests isolated from the real home directory
    with patch('pathlib.Path.home', return_value=tmp_path):
        # We can patch PromptSession so we can capture the session instance
        with patch('prompt_toolkit.PromptSession') as MockPromptSession:
            reader_fn = _build_prompt_reader(tmp_path)
            
            # Verify PromptSession was instantiated
            MockPromptSession.assert_called_once()
            
            # Get the keybindings passed to PromptSession
            call_kwargs = MockPromptSession.call_args[1]
            kb = call_kwargs.get('key_bindings')
            assert kb is not None
            
            # Verify Keys.BracketedPaste binding is registered
            paste_binding = next((b for b in kb.bindings if Keys.BracketedPaste in b.keys), None)
            assert paste_binding is not None
            
            # 1. Test pasting large data
            mock_event = MagicMock()
            large_text = "line1\nline2\nline3\nline4\nline5\nline6\nline7\nline8\nline9\nline10"
            mock_event.data = large_text
            
            # Call the handler
            paste_binding.handler(mock_event)
            
            # Verify it inserted the placeholder
            mock_event.current_buffer.insert_text.assert_called_once_with("[Pasted 10 lines]")
            
            # Verify the file was created in tmp_path/.sage/pastes/
            pastes_dir = tmp_path / ".sage" / "pastes"
            assert pastes_dir.exists()
            files = list(pastes_dir.glob("paste_*.txt"))
            assert len(files) == 1
            assert files[0].read_text(encoding="utf-8") == large_text
            
            # 2. Test pasting small data
            mock_event_small = MagicMock()
            small_text = "short single line"
            mock_event_small.data = small_text
            
            # Call the handler
            paste_binding.handler(mock_event_small)
            
            # Verify it inserted the text verbatim instead of a placeholder
            mock_event_small.current_buffer.insert_text.assert_called_once_with(small_text)

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


