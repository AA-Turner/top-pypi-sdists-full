import pytest
import os
from sage.core.sms_bridge import (
    SAGEMessageBridge,
    SMSConfig,
    _is_recipient_verified_globally,
    _send_imessage,
    _send_macos_sms,
    _send_via_kdeconnect
)

class DummyBackend:
    def __init__(self, *args, **kwargs):
        pass
    def get_linked_providers(self):
        return [
            {"provider_id": "google.com", "email": "linked@gmail.com"},
            {"provider_id": "apple.com", "phone_number": "+15555551234"}
        ]
    def list_contacts(self):
        return [
            {"email": "phone:4085073140", "device_type": "android", "label": "My Pixel"},
            {"email": "phone:6696498725", "device_type": "apple", "label": "My iPhone"}
        ]
    def _get(self, path):
        if path == "/billing/me":
            return {"email": "primary@example.com"}
        return {}

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


def test_global_recipient_verification(monkeypatch):
    # Set the force test env var so that the check is actually run instead of bypassed in tests
    monkeypatch.setenv("SAGE_SMS_FORCE_VERIFICATION_TEST", "1")
    monkeypatch.setattr("sage.core.sms_bridge.SAGEBackend", DummyBackend)
    
    # Mock load_auth to return the primary email
    monkeypatch.setattr("sage.core.cli_auth.load_auth", lambda: {"email": "primary@example.com"})
    monkeypatch.setattr("sage.core.sms_bridge._load_sage_token", lambda: ("fake_token", "http://fake"))
    
    # Verify verified contacts
    assert _is_recipient_verified_globally("primary@example.com") is True
    assert _is_recipient_verified_globally("linked@gmail.com") is True
    assert _is_recipient_verified_globally("+15555551234") is True
    assert _is_recipient_verified_globally("5555551234") is True
    assert _is_recipient_verified_globally("5555551234@tmomail.net") is True
    
    # Verify unverified contacts are blocked
    assert _is_recipient_verified_globally("other@example.com") is False
    assert _is_recipient_verified_globally("lily@example.com") is False
    assert _is_recipient_verified_globally("+19999999999") is False


def test_send_functions_permit_unverified(monkeypatch):
    # Outbound sending should now be permitted for any recipient
    # We mock _run_send_script to always succeed for this test
    monkeypatch.setattr("sage.core.sms_bridge.SAGEBackend", DummyBackend)
    monkeypatch.setattr("sage.core.cli_auth.load_auth", lambda: {"email": "primary@example.com"})
    monkeypatch.setattr("sage.core.sms_bridge._load_sage_token", lambda: ("fake_token", "http://fake"))
    
    # Mock chat.db check to return True
    monkeypatch.setattr("sage.core.sms_bridge._imessage_row_matches", lambda baseline, text, recipient=None: True)
    # Mock osascript run to return success
    class MockResult:
        returncode = 0
        stdout = "ok"
        stderr = ""
    import subprocess
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: MockResult())
    monkeypatch.setattr("sage.core.sms_bridge._find_kdeconnect_cli", lambda: "/usr/local/bin/kdeconnect-cli")

    assert _send_imessage("lily@example.com", "hello") is True
    assert _send_macos_sms("+19999999999", "hello") is True
    # KDE Connect should now also pass as it returns True on successful subprocess launch
    assert _send_via_kdeconnect("+19999999999", "hello") is True
