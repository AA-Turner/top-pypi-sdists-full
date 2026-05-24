import sys
import unittest
from unittest.mock import MagicMock, patch
import pytest

from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig

@pytest.fixture
def mock_bridge():
    cfg = SMSConfig(computer_name="TestPC")
    with patch("sage.core.sms_bridge.SAGEBackend"):
        # We don't need a real WebSocket for these routing tests
        bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
        return bridge

@pytest.mark.parametrize("platform, device_type, expected_method", [
    ("darwin", "apple", "imessage"),
    ("darwin", "android", "kdeconnect"),
    ("linux", "apple", "kdeconnect"),
    ("win32", "apple", "kdeconnect"),
    ("linux", "android", "kdeconnect"),
])
def test_handle_native_message_routing(mock_bridge, platform, device_type, expected_method):
    """Verify _handle_native_message routes to the correct OS-level sender."""
    msg = {
        "phone": "4085073140",
        "text": "Hello",
        "device_type": device_type
    }
    
    with patch("sys.platform", platform), \
         patch("sage.core.sms_bridge._send_imessage") as mock_imsg, \
         patch("sage.core.sms_bridge._send_via_kdeconnect") as mock_kde:
        
        mock_imsg.return_value = True
        mock_kde.return_value = True
        
        mock_bridge._handle_native_message(msg)
        
        if expected_method == "imessage":
            mock_imsg.assert_called_once()
            mock_kde.assert_not_called()
        else:
            mock_kde.assert_called_once()

@pytest.mark.parametrize("platform, apple_email, expected_kde", [
    ("darwin", "user@icloud.com", False),
    ("linux", "4085073140", True),
    ("linux", "user@icloud.com", False), # Email-only, KDE can't handle
])
def test_handle_imessage_to_apple_id_fallback(mock_bridge, platform, apple_email, expected_kde):
    """Verify imessage_to_apple_id falls back to KDE Connect on Linux/Windows for phone numbers."""
    msg = {
        "apple_email": apple_email,
        "text": "Hello"
    }
    
    with patch("sys.platform", platform), \
         patch("sage.core.sms_bridge._send_imessage") as mock_imsg, \
         patch("sage.core.sms_bridge._send_via_kdeconnect") as mock_kde:
        
        mock_imsg.return_value = True
        mock_kde.return_value = True
        
        mock_bridge._handle_imessage_to_apple_id(msg)
        
        if platform == "darwin":
            mock_imsg.assert_called_once()
        elif expected_kde:
            mock_kde.assert_called_once()
        else:
            mock_kde.assert_not_called()

@pytest.mark.parametrize("platform, device_type, expected_method", [
    ("darwin", "apple", "imessage"),
    ("linux", "apple", "kdeconnect"),
    ("linux", "", "kdeconnect"), # untagged fallback
])
def test_deliver_native_routing(mock_bridge, platform, device_type, expected_method):
    """Verify outbound task reply routing."""
    with patch("sys.platform", platform), \
         patch("sage.core.sms_bridge._send_imessage") as mock_imsg, \
         patch("sage.core.sms_bridge._send_via_kdeconnect") as mock_kde:
        
        mock_imsg.return_value = True
        mock_kde.return_value = True
        
        mock_bridge._deliver_native("4085073140@vtext.com", "reply", device_type)
        
        if expected_method == "imessage":
            mock_imsg.assert_called_once()
        else:
            mock_kde.assert_called_once()
