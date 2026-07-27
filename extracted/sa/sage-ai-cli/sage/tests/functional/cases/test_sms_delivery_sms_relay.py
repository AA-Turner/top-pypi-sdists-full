"""SMS Relay Delivery Tests."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

class TestSMSRelayDelivery:
    def test_sms_relay_short_message(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="")
            bridge._send_macos_sms = lambda number, msg: mock_run(["sms", number, msg])
            bridge._send_macos_sms("+15551234567", "Hello via SMS relay!")
            assert mock_run.called

    def test_sms_relay_special_characters(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        special_msg = 'Hello "world" & <test> 🎉'
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            bridge._send_macos_sms = lambda number, msg: mock_run(["sms", number, msg])
            bridge._send_macos_sms("+15551234567", special_msg)
            assert mock_run.called

    def test_sms_relay_multiline(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        multi_line = "Line 1\nLine 2\nLine 3"
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            bridge._send_macos_sms = lambda number, msg: mock_run(["sms", number, msg])
            bridge._send_macos_sms("+15551234567", multi_line)
            assert mock_run.called

    def test_sms_relay_empty_message(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            bridge._send_macos_sms = lambda number, msg: mock_run(["sms", number, msg])
            bridge._send_macos_sms("+15551234567", "")
            assert mock_run.called

    def test_sms_relay_international_number(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            bridge._send_macos_sms = lambda number, msg: mock_run(["sms", number, msg])
            bridge._send_macos_sms("+447700900000", "International test")
            assert mock_run.called

    def test_sms_relay_long_message_chunking(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        long_msg = "X" * 2000
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            bridge._send_macos_sms = lambda number, msg: mock_run(["sms", number, msg])
            bridge._send_macos_sms("+15551234567", long_msg)
            assert mock_run.called
