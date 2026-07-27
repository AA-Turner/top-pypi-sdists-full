import sys
import os
import pytest
import json
import time
from pathlib import Path
from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig

class DummySubprocessResult:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

@pytest.fixture
def sms_bridge_setup(tmp_path, monkeypatch):
    # Mock config
    cfg = SMSConfig(computer_name="test-mac")
    cfg.working_dir = str(tmp_path)
    cfg.task_timeout = 60
    monkeypatch.setattr(SMSConfig, "load", lambda *a, **k: cfg)
    
    # Mock tokens & auth
    monkeypatch.setattr("sage.core.sms_bridge._load_sage_token", lambda: ("token-123", "http://fake-api"))
    monkeypatch.setattr("sage.core.cli_auth.get_uid_from_token", lambda tok: "uid-123")
    
    bridge = SAGEMessageBridge(cfg=cfg, token="token-123", api_base="http://fake-api")
    bridge._phone_contacts_cache["+14085073140"] = {"email": "user@example.com", "device_type": "android"}
    bridge._phone_contacts_cache["+16696498725"] = {"email": "user@example.com", "device_type": "apple"}
    
    # Mock recipient verification to allow these senders
    monkeypatch.setattr(bridge, "_is_recipient_verified", lambda recipient: True)
    
    # Track sent messages
    sent_messages = []
    def mock_send_imessage(target, body, attachments=None):
        sent_messages.append({
            "target": target,
            "body": body,
            "attachments": attachments or [],
            "service": "iMessage"
        })
        return True
        
    def mock_send_via_kdeconnect(target, body):
        sent_messages.append({
            "target": target,
            "body": body,
            "attachments": [],
            "service": "KDE Connect"
        })
        return True

    def mock_share_via_kdeconnect(path):
        if sent_messages:
            sent_messages[-1]["attachments"].append(str(path))
        return True

    monkeypatch.setattr("sage.core.sms_bridge._send_imessage", mock_send_imessage)
    monkeypatch.setattr("sage.core.sms_bridge._send_via_kdeconnect", mock_send_via_kdeconnect)
    monkeypatch.setattr("sage.core.sms_bridge._share_via_kdeconnect", mock_share_via_kdeconnect)

    return bridge, tmp_path, sent_messages


def _run_test_case(bridge, workspace, sent_messages, sender, task, file_to_create, file_content="", expect_attached: bool = True):
    """Helper to mock execution and run the bridge handler."""
    import subprocess
    
    def mock_subprocess_run(cmd, *args, **kwargs):
        # Simulate SAGE executing and writing the asset file
        target_file = Path(workspace) / file_to_create
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(file_content, encoding="utf-8")
        
        # Verify the file was written
        assert target_file.exists()
        assert target_file.stat().st_size > 0
        
        return DummySubprocessResult(
            returncode=0,
            stdout=f"Done. Successfully generated: {file_to_create}"
        )
        
    import builtins
    # We monkeypatch subprocess.run in the module
    import subprocess as _sub
    original_run = _sub.run
    _sub.run = mock_subprocess_run
    
    try:
        synthetic_msg = {
            "task": task,
            "from": sender,
        }
        device_type = "apple" if sender == "+16696498725" else "android"
        bridge._handle_local_imessage_task(synthetic_msg, "iMessage", device_type)
    finally:
        _sub.run = original_run

    # Assertions
    assert len(sent_messages) == 1
    reply = sent_messages[0]
    assert reply["target"] == sender
    assert f"generated: {file_to_create}" in reply["body"]
    
    # Verify that the generated file was correctly attached
    expected_attachment = str(Path(workspace) / file_to_create)
    if expect_attached:
        assert expected_attachment in reply["attachments"]
    else:
        assert expected_attachment not in reply["attachments"]


def test_sms_bridge_image(sms_bridge_setup):
    """Test image asset creation (.png)."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+16696498725",
        task="Create a portrait image of a cat as a PNG",
        file_to_create="cat_portrait.png",
        file_content="mock_png_binary_data"
    )


def test_sms_bridge_video(sms_bridge_setup):
    """Test video asset creation (.mp4)."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+16696498725",
        task="Create a 10s video of ocean waves as a MP4",
        file_to_create="ocean_waves.mp4",
        file_content="mock_mp4_binary_data"
    )


def test_sms_bridge_music_video(sms_bridge_setup):
    """Test music video asset creation (.mp4)."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+14085073140",
        task="Make a music video for Lily that says I love you Lily you’re so pretty",
        file_to_create="lily_love_song.mp4",
        file_content="mock_music_video_mp4_data"
    )


def test_sms_bridge_music_audio(sms_bridge_setup):
    """Test music/audio file creation (.mp3)."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+16696498725",
        task="Generate a soft lofi beat audio file as an MP3",
        file_to_create="lofi_beat.mp3",
        file_content="mock_mp3_binary_data"
    )


def test_sms_bridge_website(sms_bridge_setup):
    """Test website project scaffolding."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+14085073140",
        task="Build a clean landing page website using HTML and CSS",
        file_to_create="index.html",
        file_content="<!DOCTYPE html><html><body><h1>Welcome</h1></body></html>",
        expect_attached=False
    )


def test_sms_bridge_backend_system(sms_bridge_setup):
    """Test backend system implementation."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+16696498725",
        task="Create a python backend server app with FastAPI",
        file_to_create="server.py",
        file_content="from fastapi import FastAPI\napp = FastAPI()",
        expect_attached=False
    )


def test_sms_bridge_mobile_app(sms_bridge_setup):
    """Test mobile app component creation."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+14085073140",
        task="Build a React Native mobile app task component",
        file_to_create="TaskComponent.tsx",
        file_content="export default function TaskComponent() {}",
        expect_attached=False
    )


def test_sms_bridge_video_game(sms_bridge_setup):
    """Test video game file creation."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+16696498725",
        task="Write a simple snake game in python using pygame",
        file_to_create="snake_game.py",
        file_content="import pygame\n# Game loop here",
        expect_attached=False
    )


def test_sms_bridge_python_specifically_requested(sms_bridge_setup):
    """Test python file creation when specifically requested via SMS."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+16696498725",
        task="Create a python backend server app with FastAPI and send the python code to my phone",
        file_to_create="server.py",
        file_content="from fastapi import FastAPI\napp = FastAPI()",
        expect_attached=False
    )


def test_sms_bridge_gif(sms_bridge_setup):
    """Test GIF asset generation."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+14085073140",
        task="Generate an animated loading spinner as a GIF",
        file_to_create="spinner.gif",
        file_content="mock_gif_data"
    )


def test_sms_bridge_sprite(sms_bridge_setup):
    """Test sprite creation."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+16696498725",
        task="Create a 2D player walk cycle sprite sheet as a PNG",
        file_to_create="player_walk_sprites.png",
        file_content="mock_sprites_png_data"
    )


def test_sms_bridge_animation(sms_bridge_setup):
    """Test animation asset creation."""
    bridge, workspace, sent_messages = sms_bridge_setup
    _run_test_case(
        bridge, workspace, sent_messages,
        sender="+14085073140",
        task="Make a bouncing ball animation file",
        file_to_create="bouncing_ball.mp4",
        file_content="mock_anim_video_data"
    )
