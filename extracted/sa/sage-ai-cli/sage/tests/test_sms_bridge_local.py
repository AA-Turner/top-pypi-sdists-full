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
    
    # Since FDA is missing (_imessage_max_rowid returns -1), SAGE should now return False to trigger fallback
    assert _send_imessage("test@example.com", "Hello iMessage") is False
    
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

    # Since FDA is missing, it should fail
    assert _send_macos_sms("+14085073140", "Hello SMS") is False
    
    assert len(sub.calls) > 0
    args = sub.calls[0]
    assert args[0] == "osascript"
    assert "SMS" in args[2]
