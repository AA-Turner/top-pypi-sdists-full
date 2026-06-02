import sys
import pytest
from pathlib import Path

from sage.core.sms_bridge import (
    _send_imessage,
    _send_via_kdeconnect,
    _send_macos_sms,
    _imessage_max_rowid,
)

class DummySubprocessResult:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

class CapturedSubprocess:
    def __init__(self):
        self.calls = []
        self.results = []
    def __call__(self, args, *a, **k):
        self.calls.append(args)
        if self.results:
            return self.results.pop(0)
        return DummySubprocessResult()

def test_imessage_max_rowid_failure(monkeypatch):
    """Test that _imessage_max_rowid handles missing Full Disk Access by returning -1."""
    monkeypatch.setattr("sys.platform", "darwin")
    monkeypatch.setattr("os.path.exists", lambda path: True)
    
    def raise_connect(*args, **kwargs):
        raise Exception("Operation not permitted")
        
    import sqlite3
    monkeypatch.setattr(sqlite3, "connect", raise_connect)
    assert _imessage_max_rowid() == -1


def test_send_imessage_success(monkeypatch):
    """Test that _send_imessage returns True if osascript works and chat.db is unreadable."""
    monkeypatch.setattr("sys.platform", "darwin")
    monkeypatch.setattr("sage.core.sms_bridge._imessage_max_rowid", lambda: -1)
    
    sub = CapturedSubprocess()
    sub.results.append(DummySubprocessResult(returncode=0, stdout="ok\n"))
    import subprocess
    monkeypatch.setattr(subprocess, "run", sub)
    
    # Since FDA is missing (_imessage_max_rowid returns -1), SAGE should trust AppleScript success and return True
    assert _send_imessage("test@example.com", "Hello iMessage") is True
    
    assert len(sub.calls) > 0
    args = sub.calls[0]
    assert args[0] == "osascript"
    assert "participant" in args[2] or "buddy" in args[2]


def test_send_imessage_osascript_failure(monkeypatch):
    """Test that _send_imessage returns False if osascript fails entirely."""
    monkeypatch.setattr("sys.platform", "darwin")
    monkeypatch.setattr("sage.core.sms_bridge._imessage_max_rowid", lambda: -1)
    
    sub = CapturedSubprocess()
    sub.results.append(DummySubprocessResult(returncode=1, stdout="", stderr="error"))
    import subprocess
    monkeypatch.setattr(subprocess, "run", sub)

    assert _send_imessage("test@example.com", "Fail") is False


def test_send_via_kdeconnect(monkeypatch):
    """Test KDE Connect real SMS send."""
    monkeypatch.setattr("sage.core.sms_bridge._find_kdeconnect_cli", lambda: "/fake/kdeconnect-cli")
    
    sub = CapturedSubprocess()
    sub.results.append(DummySubprocessResult(returncode=0, stdout="device-12345\n"))
    sub.results.append(DummySubprocessResult(returncode=0, stdout=""))
    import subprocess
    monkeypatch.setattr(subprocess, "run", sub)

    assert _send_via_kdeconnect("+14085073140", "Hello KDE") is True

    assert len(sub.calls) == 2
    send_args = sub.calls[1]
    assert "/fake/kdeconnect-cli" in send_args
    assert "--send-sms" in send_args
    assert "Hello KDE" in send_args
    assert "-d" in send_args
    assert "device-12345" in send_args


def test_send_macos_sms(monkeypatch):
    """Test macOS Messages.app SMS relay."""
    monkeypatch.setattr("sys.platform", "darwin")
    monkeypatch.setattr("sage.core.sms_bridge._imessage_max_rowid", lambda: -1)
    
    sub = CapturedSubprocess()
    sub.results.append(DummySubprocessResult(returncode=0, stdout="ok\n"))
    import subprocess
    monkeypatch.setattr(subprocess, "run", sub)

    # Since FDA is missing, SAGE should trust AppleScript success and return True
    assert _send_macos_sms("+14085073140", "Hello SMS") is True
    
    assert len(sub.calls) > 0
    args = sub.calls[0]
    assert args[0] == "osascript"
    assert "SMS" in args[2]


def test_international_phone_normalization():
    from sage.core.sms_bridge import _normalize_e164_globally
    # US/Canada numbers
    assert _normalize_e164_globally("4085073140") == "+14085073140"
    assert _normalize_e164_globally("+14085073140") == "+14085073140"
    assert _normalize_e164_globally("14085073140") == "+14085073140"
    
    # International numbers
    assert _normalize_e164_globally("+447123456789") == "+447123456789"
    assert _normalize_e164_globally("447123456789") == "+447123456789"
    assert _normalize_e164_globally("+491701234567") == "+491701234567"
    assert _normalize_e164_globally("491701234567") == "+491701234567"
    
    # Non-phone/empty
    assert _normalize_e164_globally("abc") == ""
    assert _normalize_e164_globally("") == ""


def test_find_kdeconnect_cli_and_daemon_candidates(monkeypatch):
    monkeypatch.setattr("sys.platform", "darwin")
    from sage.core.sms_bridge import _find_kdeconnect_cli
    from sage.core.kdeconnect_listener import _find_kdeconnectd
    
    checked_paths = []
    def mock_exists(path):
        checked_paths.append(str(path))
        return False
        
    monkeypatch.setattr("os.path.exists", mock_exists)
    monkeypatch.setattr("shutil.which", lambda *a, **k: None)
    
    # Check CLI lookup candidates
    _find_kdeconnect_cli()
    cli_paths_str = " ".join(checked_paths)
    assert "opt/homebrew" in cli_paths_str or "homebrew" in cli_paths_str
    assert "KDE Connect" in cli_paths_str
    
    checked_paths.clear()
    # Check Daemon lookup candidates
    _find_kdeconnectd()
    daemon_paths_str = " ".join(checked_paths)
    assert "opt/homebrew" in daemon_paths_str or "homebrew" in daemon_paths_str
    assert "KDE Connect" in daemon_paths_str


def test_kdeconnectd_running_reporting(monkeypatch):
    """Test that _kdeconnectd_running returns True with warning if daemon is alive but no devices online."""
    from sage.core.sms_bridge import _kdeconnectd_running
    
    monkeypatch.setattr("sage.core.sms_bridge._find_kdeconnect_cli", lambda: "/fake/kdeconnect-cli")
    monkeypatch.setattr("sage.core.kdeconnect_listener._is_daemon_running", lambda: True)
    
    sub = CapturedSubprocess()
    sub.results.append(DummySubprocessResult(returncode=0, stdout="\n"))
    import subprocess
    monkeypatch.setattr(subprocess, "run", sub)
    
    ok, reason = _kdeconnectd_running()
    assert ok is True
    assert "no paired+reachable KDE Connect devices online" in reason


def test_kdeconnect_systemd_cooperation(monkeypatch):
    """Test that _stop_os_daemon and _start_os_daemon call systemctl user services on Linux."""
    from sage.core.kdeconnect_listener import _stop_os_daemon, _start_os_daemon
    
    monkeypatch.setattr("sys.platform", "linux")
    monkeypatch.setattr("sage.core.kdeconnect_listener._is_daemon_running", lambda: False)
    monkeypatch.setattr("sage.core.kdeconnect_listener._find_kdeconnectd", lambda: "/fake/kdeconnectd")
    
    sub = CapturedSubprocess()
    import subprocess
    monkeypatch.setattr(subprocess, "run", sub)
    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: None)
    
    # Test stop
    _stop_os_daemon()
    
    systemctl_calls = [args for args in sub.calls if args[0] == "systemctl"]
    assert len(systemctl_calls) >= 2
    assert "stop" in systemctl_calls[0]
    assert "kdeconnect" in systemctl_calls[0]
    
    # Test start
    sub.calls.clear()
    # Mock is-enabled check to return success (0)
    sub.results.append(DummySubprocessResult(returncode=0))
    sub.results.append(DummySubprocessResult(returncode=0))
    _start_os_daemon()
    
    start_calls = [args for args in sub.calls if args[0] == "systemctl"]
    assert len(start_calls) >= 2
    assert "is-enabled" in start_calls[0]
    assert "start" in start_calls[1]
    assert "kdeconnect" in start_calls[1]


def test_handshake_null_safety(monkeypatch):
    """Test that SAGEMessageBridge handshake safely handles null user_email and user_phone."""
    from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig
    import json
    
    class MockWebSocket:
        def __init__(self):
            self.sent = []
            self.closed = False
        def send(self, data):
            self.sent.append(data)
        def recv(self):
            return json.dumps({
                "type": "ready",
                "display_email": "bridge@example.com",
                "user_email": None,
                "user_phone": None
            })
        def close(self):
            self.closed = True
            
    # Mock token loading
    monkeypatch.setattr("sage.core.sms_bridge._load_sage_token", lambda: ("token-123", "http://fake-api"))
    monkeypatch.setattr("sage.core.cli_auth.get_uid_from_token", lambda tok: "uid-123")
    
    # Mock config
    cfg = SMSConfig(computer_name="test-mac")
    monkeypatch.setattr(SMSConfig, "load", lambda *a, **k: cfg)
    
    bridge = SAGEMessageBridge(cfg=cfg, token="token-123", api_base="http://fake-api")
    
    mock_ws = MockWebSocket()
    import websocket as _ws_lib
    monkeypatch.setattr(_ws_lib, "create_connection", lambda *a, **k: mock_ws)
    
    # Mock load_auth to trigger a break or stop after handshake
    call_count = 0
    def mock_load_auth():
        nonlocal call_count
        call_count += 1
        if call_count > 1:
            bridge._stop.set()
        return {"id_token": "token-123"}
        
    monkeypatch.setattr("sage.core.cli_auth.load_auth", mock_load_auth)
    
    # Run the bridge run loop
    bridge.run()
    
    # Verify that the handshake completed without raising AttributeError/TypeError
    assert bridge._user_email == ""
    assert bridge._user_phone == ""
    assert mock_ws.closed is True

