import pytest
from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig

class DummyBackend:
    def __init__(self, *args, **kwargs):
        pass
    def get_linked_providers(self):
        return [
            {"provider_id": "google.com", "email": "linked@gmail.com"},
            {"provider_id": "apple.com", "phone_number": "+15555551234"}
        ]

def test_recipient_verification(monkeypatch):
    monkeypatch.setattr("sage.core.sms_bridge.SAGEBackend", DummyBackend)
    
    cfg = SMSConfig(computer_name="TestPC")
    bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
    
    # Simulate ready handshake values
    bridge._user_email = "primary@example.com"
    bridge._user_phone = "+14085073140"
    
    # Verify primary contact methods
    assert bridge._is_recipient_verified("primary@example.com") is True
    assert bridge._is_recipient_verified("PRIMARY@EXAMPLE.COM") is True
    assert bridge._is_recipient_verified("+14085073140") is True
    assert bridge._is_recipient_verified("4085073140") is True
    assert bridge._is_recipient_verified("408-507-3140") is True
    
    # Verify linked provider contact methods
    assert bridge._is_recipient_verified("linked@gmail.com") is True
    assert bridge._is_recipient_verified("+15555551234") is True
    assert bridge._is_recipient_verified("5555551234") is True
    
    # Verify carrier gateways mapping to verified phone numbers
    assert bridge._is_recipient_verified("4085073140@vtext.com") is True
    assert bridge._is_recipient_verified("5555551234@tmomail.net") is True
    
    # Unverified / other people's addresses must be rejected
    assert bridge._is_recipient_verified("other@example.com") is False
    assert bridge._is_recipient_verified("+19999999999") is False
    assert bridge._is_recipient_verified("9999999999@vtext.com") is False
