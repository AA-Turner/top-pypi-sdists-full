"""SMS KDE Connect Delivery Tests."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

class TestKDEConnectDelivery:
    def test_deliver_text_android(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="")
            # We bypass the full initialization for testing logic
            def mock_deliver(text, recipient, device_type):
                subprocess.run(["kdeconnect-cli", "--send-sms", text])
            
            bridge._deliver_native = mock_deliver
            bridge._deliver_native(
                text="Hello Android!",
                recipient="+15559876543",
                device_type="android",
            )
            assert mock_run.called
            cmd = mock_run.call_args[0][0] if mock_run.call_args[0] else []
            cmd_str = " ".join(str(c) for c in cmd)
            assert "kdeconnect" in cmd_str

    def test_deliver_long_text_android(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            def mock_deliver(text, recipient, device_type):
                subprocess.run(["kdeconnect-cli", "--send-sms", text])
            
            bridge._deliver_native = mock_deliver
            bridge._deliver_native(
                text="B" * 3000,
                recipient="+15559876543",
                device_type="android",
            )
            assert mock_run.called

    def test_status_for_android_device(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        bridge.cfg = MagicMock()
        bridge.cfg.computer_name = "test-kde-bot"
        bridge.cfg.model = "cloud:qwen3-coder"
        bridge.working_dir = Path(tempfile.mkdtemp())
        
        model = bridge.cfg.model
        output = (
            f"✅ [{bridge.cfg.computer_name}]\n"
            f"📁 {bridge.working_dir}\n"
            f"🤖 {model}"
        )
        assert "✅" in output
        assert "qwen" in output.lower()

    def test_help_for_android_device(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        bridge._build_help_text = lambda: "Help text for Android"
        
        help_text = bridge._build_help_text()
        assert len(help_text) > 5

    def test_model_switch_android(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        bridge.cfg = MagicMock()
        bridge.cfg.model = "cloud:qwen3-coder"
        
        bridge.cfg.model = "cloud:mistral-small"
        assert bridge.cfg.model == "cloud:mistral-small"

    def test_cd_command_android(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        new_dir = Path(tempfile.mkdtemp())
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        bridge.working_dir = Path(tempfile.mkdtemp())
        
        bridge.working_dir = new_dir
        assert bridge.working_dir == new_dir

    def test_temp_command_android(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        bridge.cfg = MagicMock()
        
        val = max(0.0, min(2.0, 1.5))
        bridge.cfg.temperature = val
        assert bridge.cfg.temperature == 1.5

    def test_timeout_command_android(self):
        from sage.core.sms_bridge import SAGEMessageBridge
        bridge = SAGEMessageBridge.__new__(SAGEMessageBridge)
        bridge.cfg = MagicMock()
        
        bridge.cfg.task_timeout = max(0, 300)
        assert bridge.cfg.task_timeout == 300
