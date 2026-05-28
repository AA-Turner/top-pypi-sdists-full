import os
import sys
import pytest

from sage.core.renderer import _build_console, set_no_color
from sage.main import app as sage_app

def test_no_color_env_variable(monkeypatch):
    """Test that NO_COLOR environment variable disables colors dynamically in console."""
    monkeypatch.setenv("NO_COLOR", "1")
    console = _build_console()
    assert console.no_color is True
    assert console._highlight is False

def test_term_dumb_env_variable(monkeypatch):
    """Test that TERM=dumb environment variable disables colors dynamically in console."""
    monkeypatch.setenv("TERM", "dumb")
    console = _build_console()
    assert console.no_color is True
    assert console._highlight is False

def test_set_no_color_rebuilds_consoles():
    """Test that set_no_color actually toggles color suppression and rebuilds consoles."""
    from sage.core import renderer
    
    set_no_color(True)
    assert renderer.console.no_color is True
    assert renderer.console._highlight is False
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

def test_empty_term_env_variable(monkeypatch):
    """Test that empty TERM environment variable disables colors dynamically in console."""
    monkeypatch.setenv("TERM", "")
    console = _build_console()
    assert console.no_color is True
    assert console._highlight is False

def test_unset_term_env_variable(monkeypatch):
    """Test that missing/unset TERM environment variable disables colors dynamically in console."""
    monkeypatch.delenv("TERM", raising=False)
    console = _build_console()
    assert console.no_color is True
    assert console._highlight is False

def test_legacy_encoding_disables_color(monkeypatch):
    """Test that legacy stdout encoding disables colors dynamically in console."""
    class DummyStream:
        encoding = "US-ASCII"
        def isatty(self):
            return True
        def write(self, data):
            pass
        def flush(self):
            pass

    monkeypatch.setattr(sys, "stdout", DummyStream())
    console = _build_console()
    assert console.no_color is True
    assert console._highlight is False


def test_clean_ansi_principal_builder():
    """Test that principal builder's _clean_ansi strips escapes from nested structures."""
    from sage.core.principal_builder import _clean_ansi
    nested = {
        "text": "\x1b[1mBold Text\x1b[0m",
        "list": ["\x1b[31mRed\x1b[0m", "Green"],
        "dict": {"nested_text": "\x1b[2mDim\x1b[0m"}
    }
    cleaned = _clean_ansi(nested)
    assert cleaned["text"] == "Bold Text"
    assert cleaned["list"] == ["Red", "Green"]
    assert cleaned["dict"]["nested_text"] == "Dim"


def test_clean_ansi_dynamic_builder():
    """Test that dynamic builder's _clean_ansi strips escapes from nested structures."""
    from sage.core.dynamic_builder import _clean_ansi
    nested = {
        "text": "\x1b[1mBold Text\x1b[0m",
        "list": ["\x1b[31mRed\x1b[0m", "Green"],
        "dict": {"nested_text": "\x1b[2mDim\x1b[0m"}
    }
    cleaned = _clean_ansi(nested)
    assert cleaned["text"] == "Bold Text"
    assert cleaned["list"] == ["Red", "Green"]
    assert cleaned["dict"]["nested_text"] == "Dim"


def test_telemetry_logger_strips_ansi(tmp_path):
    """Test that TelemetryLogger strips ANSI escape codes from output and prompt before logging."""
    from sage.core.telemetry import TelemetryLogger
    logger = TelemetryLogger(session_id="test_session", root=tmp_path)
    logger.log_turn(
        prompt="\x1b[1mUser Prompt\x1b[0m",
        model="dummy-model",
        output="\x1b[32mAssistant output\x1b[0m",
        validator_signal=None,
        success=True
    )
    records = logger.read()
    assert len(records) == 1
    assert records[0]["prompt"] == "User Prompt"
    assert records[0]["output"] == "Assistant output"


def test_distill_logger_strips_ansi(tmp_path):
    """Test that DistillLogger strips ANSI escape codes from final response and user prompt before logging."""
    from sage.core.distill import DistillLogger, DistillEvent
    logger = DistillLogger(session_id="test_session", root=tmp_path)
    event = DistillEvent(
        user_prompt="\x1b[1mPrompt\x1b[0m",
        final_response="\x1b[2mResponse\x1b[0m"
    )
    logger.log(event)
    events = logger.events()
    assert len(events) == 1
    assert events[0].user_prompt == "Prompt"
    assert events[0].final_response == "Response"


def test_sms_bridge_log_strips_ansi(tmp_path, monkeypatch):
    """Test that SAGEMessageBridge._log strips ANSI escape codes before writing to log."""
    from sage.core.sms_bridge import SAGEMessageBridge
    
    class DummyConfig:
        computer_name = "test-comp"
        
    class DummyBridge(SAGEMessageBridge):
        def __init__(self):
            self.cfg = DummyConfig()
            # We override the log file path
            self._log_fp = (tmp_path / "sms.log").open("a", buffering=1, encoding="utf-8")
            
    bridge = DummyBridge()
    bridge._log("\x1b[1mHello\x1b[0m \x1b[32mWorld\x1b[0m")
    bridge._log_fp.close()
    
    log_content = (tmp_path / "sms.log").read_text("utf-8")
    assert "Hello World" in log_content
    assert "\x1b" not in log_content

