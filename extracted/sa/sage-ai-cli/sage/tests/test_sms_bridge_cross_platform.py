import sys
import pytest

from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig

@pytest.fixture(autouse=True)
def mock_recipient_verification(monkeypatch):
    monkeypatch.setattr("sage.core.sms_bridge.SAGEMessageBridge._is_recipient_verified", lambda *args, **kwargs: True)

class DummyBackend:
    def __init__(self, *args, **kwargs):
        pass

@pytest.mark.parametrize("platform, device_type, expected_method", [
    ("darwin", "apple", "imessage"),
    ("darwin", "android", "kdeconnect"),
    ("linux", "apple", "kdeconnect"),
    ("win32", "apple", "kdeconnect"),
    ("linux", "android", "kdeconnect"),
])
def test_handle_native_message_routing(monkeypatch, platform, device_type, expected_method):
    """Verify _handle_native_message routes to the correct OS-level sender."""
    calls = []
    monkeypatch.setattr("sage.core.sms_bridge.SAGEBackend", DummyBackend)
    monkeypatch.setattr("sys.platform", platform)
    monkeypatch.setattr("sage.core.sms_bridge._send_imessage", lambda *a, **k: calls.append("imessage") or True)
    monkeypatch.setattr("sage.core.sms_bridge._send_via_kdeconnect", lambda *a, **k: calls.append("kdeconnect") or True)
    
    cfg = SMSConfig(computer_name="TestPC")
    bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
    
    msg = {
        "phone": "4085073140",
        "text": "Hello",
        "device_type": device_type
    }
    
    bridge._handle_native_message(msg)
    
    assert len(calls) == 1
    assert calls[0] == expected_method


@pytest.mark.parametrize("platform, apple_email, expected_kde", [
    ("darwin", "user@icloud.com", False),
    ("linux", "4085073140", True),
    ("linux", "user@icloud.com", False), # Email-only, KDE can't handle
])
def test_handle_imessage_to_apple_id_fallback(monkeypatch, platform, apple_email, expected_kde):
    """Verify imessage_to_apple_id falls back to KDE Connect on Linux/Windows for phone numbers."""
    calls = []
    monkeypatch.setattr("sage.core.sms_bridge.SAGEBackend", DummyBackend)
    monkeypatch.setattr("sys.platform", platform)
    monkeypatch.setattr("sage.core.sms_bridge._send_imessage", lambda *a, **k: calls.append("imessage") or True)
    monkeypatch.setattr("sage.core.sms_bridge._send_via_kdeconnect", lambda *a, **k: calls.append("kdeconnect") or True)
    
    cfg = SMSConfig(computer_name="TestPC")
    bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
    
    msg = {
        "apple_email": apple_email,
        "text": "Hello"
    }
    
    bridge._handle_imessage_to_apple_id(None, msg)
    
    if platform == "darwin":
        assert "imessage" in calls
    elif expected_kde:
        assert "kdeconnect" in calls
    else:
        assert len(calls) == 0


@pytest.mark.parametrize("platform, device_type, expected_method", [
    ("darwin", "apple", "imessage"),
    ("linux", "apple", "kdeconnect"),
    ("linux", "", "kdeconnect"), # untagged fallback
])
def test_deliver_native_routing(monkeypatch, platform, device_type, expected_method):
    """Verify outbound task reply routing."""
    calls = []
    monkeypatch.setattr("sage.core.sms_bridge.SAGEBackend", DummyBackend)
    monkeypatch.setattr("sys.platform", platform)
    monkeypatch.setattr("sage.core.sms_bridge._send_imessage", lambda *a, **k: calls.append("imessage") or True)
    monkeypatch.setattr("sage.core.sms_bridge._send_via_kdeconnect", lambda *a, **k: calls.append("kdeconnect") or True)
    
    cfg = SMSConfig(computer_name="TestPC")
    bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
    
    bridge._deliver_native("4085073140@vtext.com", "reply", device_type)
    
    assert len(calls) == 1
    assert calls[0] == expected_method
