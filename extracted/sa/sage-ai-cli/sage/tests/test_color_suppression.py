import os
import pytest

from sage.core.renderer import _build_console, set_no_color
from sage.main import app as sage_app

def test_no_color_env_variable(monkeypatch):
    """Test that NO_COLOR environment variable disables colors dynamically in console."""
    monkeypatch.setenv("NO_COLOR", "1")
    console = _build_console()
    assert console.no_color is True

def test_term_dumb_env_variable(monkeypatch):
    """Test that TERM=dumb environment variable disables colors dynamically in console."""
    monkeypatch.setenv("TERM", "dumb")
    console = _build_console()
    assert console.no_color is True

def test_set_no_color_rebuilds_consoles():
    """Test that set_no_color actually toggles color suppression and rebuilds consoles."""
    from sage.core import renderer
    
    set_no_color(True)
    assert renderer.console.no_color is True
    assert renderer.err_console.no_color is True

    # Restore default
    set_no_color(False)

class DummyConsole:
    def __init__(self):
        self.printed = []
    def print(self, *args, **kwargs):
        self.printed.append(args[0] if args else "")

class DummyLive:
    def __init__(self, *args, **kwargs):
        raise AssertionError("Live spinner should not be instantiated when color/spinners are disabled")
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def test_no_tty_disables_color_and_spinners(monkeypatch):
    """Test that if stdout is not a TTY, color is disabled and spinners are not started."""
    import sys
    import sage.core.renderer as renderer
    from sage.core.renderer import _build_console, status_spinner
    
    # Setup dummy console and disable Live
    dummy_console = DummyConsole()
    monkeypatch.setattr(renderer, "console", dummy_console)
    monkeypatch.setattr(renderer, "Live", DummyLive)
    
    # Make isatty return False
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)
    
    # Rebuild console to test it picks up no_color
    console = _build_console(stderr=False)
    assert console.no_color is True
    
    with status_spinner("Testing status"):
        pass
        
    # Check that the dummy console captured the status print
    assert len(dummy_console.printed) == 1
    assert "Testing status" in dummy_console.printed[0]
