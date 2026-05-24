import sys
from unittest.mock import patch, MagicMock

import pytest

from sage.core.sms_bridge import (
    _send_imessage,
    _send_via_kdeconnect,
    _send_macos_sms,
    _imessage_max_rowid,
)

@pytest.fixture
def mock_darwin(monkeypatch):
    """Force sys.platform to darwin so iMessage/macOS functions run."""
    monkeypatch.setattr(sys, "platform", "darwin")

@pytest.fixture
def mock_subprocess():
    with patch("subprocess.run") as mock_run:
        yield mock_run

def test_imessage_max_rowid_failure(mock_darwin):
    """Test that _imessage_max_rowid handles missing Full Disk Access by returning -1."""
    with patch("os.path.exists", return_value=True):
        # We simulate sqlite3 failing because of lack of permissions
        with patch("sqlite3.connect", side_effect=Exception("Operation not permitted")):
            assert _imessage_max_rowid() == -1

def test_send_imessage_success(mock_darwin, mock_subprocess):
    """Test that _send_imessage returns True if osascript works and chat.db is unreadable."""
    # Mock _imessage_max_rowid to return -1 (simulating no Full Disk Access)
    with patch("sage.core.sms_bridge._imessage_max_rowid", return_value=-1):
        # Mock osascript success
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "ok\n"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        assert _send_imessage("test@example.com", "Hello iMessage") is True
        
        # Verify subprocess was called with osascript
        mock_subprocess.assert_called()
        args = mock_subprocess.call_args[0][0]
        assert args[0] == "osascript"
        assert "participant" in args[2] or "buddy" in args[2]

def test_send_imessage_osascript_failure(mock_darwin, mock_subprocess):
    """Test that _send_imessage returns False if osascript fails entirely."""
    with patch("sage.core.sms_bridge._imessage_max_rowid", return_value=-1):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "error"
        mock_subprocess.return_value = mock_result

        assert _send_imessage("test@example.com", "Fail") is False

def test_send_via_kdeconnect(mock_subprocess):
    """Test KDE Connect real SMS send."""
    with patch("sage.core.sms_bridge._find_kdeconnect_cli", return_value="/fake/kdeconnect-cli"):
        # We need to mock two subprocess calls:
        # 1. --list-available
        # 2. --send-sms
        
        mock_list = MagicMock()
        mock_list.returncode = 0
        mock_list.stdout = "device-12345\n"
        
        mock_send = MagicMock()
        mock_send.returncode = 0
        mock_send.stdout = ""
        
        mock_subprocess.side_effect = [mock_list, mock_send]

        assert _send_via_kdeconnect("+14085073140", "Hello KDE") is True

        # Verify second call was to send SMS
        send_args = mock_subprocess.call_args_list[1][0][0]
        assert "/fake/kdeconnect-cli" in send_args
        assert "--send-sms" in send_args
        assert "Hello KDE" in send_args
        assert "-d" in send_args
        assert "device-12345" in send_args

def test_send_macos_sms(mock_darwin, mock_subprocess):
    """Test macOS Messages.app SMS relay."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "ok\n"
    mock_subprocess.return_value = mock_result

    assert _send_macos_sms("+14085073140", "Hello SMS") is True
    
    mock_subprocess.assert_called()
    args = mock_subprocess.call_args[0][0]
    assert args[0] == "osascript"
    assert "SMS" in args[2]
