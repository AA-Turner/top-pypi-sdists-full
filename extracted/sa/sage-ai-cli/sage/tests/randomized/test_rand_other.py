import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from typer.testing import CliRunner

from sage.main import app as sage_app
from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig
from sage.tests.randomized.shared_generators import MEDIA_GENERATORS, make_dummy_file

runner = CliRunner()

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)

CATEGORY_EXTENSIONS = ["ttf", "otf", "woff", "woff2", "eot", "db", "sqlite", "sqlite3", "sqlitedb", "mdb", "accdb", "pem", "crt", "key", "pub", "asc", "gpg", "der", "pfx", "p12", "fbx", "obj", "gltf", "glb", "blend", "unity", "tscn", "dae", "stl", "ply", "bin", "exe", "dll", "so", "dylib", "class", "o", "a", "app", "apk", "ipa"]

@pytest.mark.parametrize("ext", CATEGORY_EXTENSIONS)
def test_file_generators_other(temp_dir, ext):
    out_path = temp_dir / f"test_file.{ext if ext != 'animated_gif' else 'gif'}"
    if ext in MEDIA_GENERATORS:
        generator_fn = MEDIA_GENERATORS[ext]
        ffmpeg_installed = bool(shutil.which("ffmpeg"))
        ffmpeg_formats = (
            "mp4", "webm", "mkv", "avi", "mov", "wmv", "flv", "m4v", "3gp",
            "mp3", "ogg", "flac", "m4a", "opus", "aac", "wma", "mid", "midi", "amr", "aiff"
        )
        if not ffmpeg_installed and ext in ffmpeg_formats:
            with patch("shutil.which", return_value="/fake/ffmpeg"), \
                 patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                out_path.write_bytes(b"dummy audio/video content")
                result = generator_fn(out_path)
                assert result == out_path
        else:
            result = generator_fn(out_path)
            assert result.exists()
            assert result.stat().st_size > 0
    else:
        result = make_dummy_file(out_path, ext)
        assert result.exists()
        assert result.stat().st_size > 0

@pytest.mark.parametrize("ext", CATEGORY_EXTENSIONS)
@patch("sage.main._prepare_model_for_use")
@patch("sage.main._build_router")
def test_cli_ask_file_generation_other(mock_router, mock_prep, ext):
    mock_prep.return_value = (MagicMock(), "cloud:gemini-2.0-flash")
    mock_router_inst = MagicMock()
    mock_router_inst.stream.return_value = [f"Generated test_file.{ext}"]
    mock_router.return_value = mock_router_inst
    result = runner.invoke(sage_app, ["ask", f"Create a test file with .{ext} extension", "--raw"])
    assert result.exit_code == 0
    assert f"test_file.{ext}" in result.output

@pytest.mark.parametrize("ext", CATEGORY_EXTENSIONS)
@patch("subprocess.run")
def test_sms_bridge_file_generation_other(mock_run, temp_dir, ext):
    cfg = SMSConfig(computer_name="TestPC", working_dir=str(temp_dir))
    with patch("sage.core.sms_bridge.SAGEBackend"):
        bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
        mock_result = MagicMock(returncode=0, stdout=f"Successfully generated file.{ext}", stderr="")
        mock_run.return_value = mock_result
        output = bridge._run_sage_task(f"Create a file with extension {ext}", mode="agent")
        assert f"file.{ext}" in output

@pytest.mark.parametrize("ext", CATEGORY_EXTENSIONS)
@pytest.mark.asyncio
async def test_backend_chat_file_generation_other(ext):
    try:
        from fastapi.testclient import TestClient
        from backend.app import app as backend_app
    except ImportError:
        pytest.skip("FastAPI test dependencies not available")
    client = TestClient(backend_app)
    mock_runtime = MagicMock()
    mock_runtime.chat.return_value = f"Created file.{ext}"
    mock_app_state = MagicMock()
    mock_app_state.runtime_manager.runtime = mock_runtime
    mock_app_state.rate_limiter.get_client_id.return_value = "test_client"
    mock_limiter = MagicMock()
    mock_limiter.check_and_consume.return_value = MagicMock(allowed=True)
    with patch("backend.app.check_rate_limit"), \
         patch("backend.app._verify_firebase_token", return_value={"uid": "test_user", "email": "test@example.com"}), \
         patch("backend.app.ensure_user_record"), \
         patch("backend.app.check_access", return_value=(True, None)), \
         patch("backend.app.get_user_record", return_value={"tier": "free"}), \
         patch("backend.tier_rate_limiter.get_tier_limiter", return_value=mock_limiter), \
         patch("backend.app.get_app_state", return_value=mock_app_state):
        payload = {
            "messages": [{"role": "user", "content": f"Create a responsive app file with extension {ext}"}],
            "model_id": "cloud:gemini-2.0-flash",
            "conversation_id": "test_conv",
            "temperature": 0.7,
            "stream": False
        }
        response = client.post("/chat", json=payload, headers={"Authorization": "Bearer test_token"})
        assert response.status_code == 200
        json_data = response.json()
        assert json_data.get("ok") is True
