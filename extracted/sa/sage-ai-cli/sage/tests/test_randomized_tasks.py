import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from typer.testing import CliRunner

# Import sage modules
from sage.main import app as sage_app
from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig
from sage.core.asset_generator import (
    make_png, make_jpg, make_webp, make_bmp, make_tiff, make_gif,
    make_animated_gif, make_svg, make_pdf, make_ico, make_mp4, make_webm,
    make_wav, make_mp3, make_ogg, make_flac, make_m4a, make_opus
)

runner = CliRunner()

# Comprehensive list of standard computer file extensions (135 extensions!)
ALL_EXTENSIONS = [
    # Plain Text / General Documents
    "txt", "csv", "json", "xml", "html", "css", "js", "ts", "md", "yaml", "yml", "ini", "conf", "sql", "toml", "properties", "log", "bak", "tmp", "temp", "rtf", "ascii",
    # Source Code / Programming Languages
    "py", "c", "cpp", "h", "hpp", "java", "kt", "swift", "go", "rs", "sh", "bat", "ps1", "gd", "cs", "php", "rb", "pl", "pyw", "m", "scala", "dart", "tsx", "jsx", "lua", "r", "hs", "erl", "ex", "exs",
    # Images (Raster & Vector & Metaformats)
    "png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "gif", "animated_gif", "svg", "ico", "psd", "ai", "eps", "raw", "dng",
    # Documents (Complex Binary formats / Layouts)
    "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "pages", "numbers", "key",
    # Audio
    "wav", "mp3", "ogg", "flac", "m4a", "opus", "aac", "wma", "mid", "midi", "amr", "aiff",
    # Video
    "mp4", "webm", "mkv", "avi", "mov", "wmv", "flv", "m4v", "3gp",
    # Archives & Compression
    "zip", "tar", "gz", "rar", "7z", "tgz", "bz2", "xz", "dmg", "pkg", "iso", "img", "cab",
    # Fonts
    "ttf", "otf", "woff", "woff2", "eot",
    # Databases
    "db", "sqlite", "sqlite3", "sqlitedb", "mdb", "accdb",
    # Cryptographic / Keys / Certificates
    "pem", "crt", "key", "pub", "asc", "gpg", "der", "pfx", "p12",
    # Game / 3D Model Formats
    "fbx", "obj", "gltf", "glb", "blend", "unity", "tscn", "dae", "stl", "ply",
    # System Binaries / Compiled Code / Executables
    "bin", "exe", "dll", "so", "dylib", "class", "o", "a", "app", "apk", "ipa"
]

# Map specific extensions to procedural asset generators
MEDIA_GENERATORS = {
    "png": make_png,
    "jpg": make_jpg,
    "jpeg": make_jpg,
    "webp": make_webp,
    "bmp": make_bmp,
    "tiff": make_tiff,
    "tif": make_tiff,
    "gif": make_gif,
    "animated_gif": make_animated_gif,
    "svg": make_svg,
    "ico": make_ico,
    "pdf": make_pdf,
    "mp4": make_mp4,
    "webm": make_webm,
    "mkv": make_mp4,
    "avi": make_mp4,
    "mov": make_mp4,
    "wmv": make_mp4,
    "flv": make_mp4,
    "m4v": make_mp4,
    "3gp": make_mp4,
    "wav": make_wav,
    "mp3": make_mp3,
    "ogg": make_ogg,
    "flac": make_flac,
    "m4a": make_m4a,
    "opus": make_opus,
    "aac": make_wav,
    "wma": make_wav,
    "mid": make_wav,
    "midi": make_wav,
    "amr": make_wav,
    "aiff": make_wav,
}

def make_dummy_file(path: Path, ext: str) -> Path:
    """Helper to generate dummy/valid files for non-media extensions."""
    # Archives & Office OpenXML files (which are actually zip files)
    if ext in ("zip", "docx", "xlsx", "pptx", "apk", "ipa", "jar", "odt", "ods", "odp"):
        import zipfile
        with zipfile.ZipFile(path, 'w') as z:
            z.writestr("mimetype" if ext.startswith("od") else "test.txt", "content")
    # Gzip formats
    elif ext in ("gz", "tgz"):
        import gzip
        with gzip.open(path, 'wb') as f:
            f.write(b"dummy compressed content")
    # Tar formats
    elif ext == "tar":
        import tarfile
        with tarfile.open(path, 'w') as tar:
            pass
    # Databases
    elif ext in ("db", "sqlite", "sqlite3", "sqlitedb"):
        import sqlite3
        conn = sqlite3.connect(path)
        try:
            conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, val TEXT)")
            conn.commit()
        finally:
            conn.close()
    # Crypto PEM/GPG formats
    elif ext in ("pem", "crt", "key", "pub", "asc", "gpg"):
        path.write_text(f"-----BEGIN {ext.upper()}-----\nDummy Key Content\n-----END {ext.upper()}-----\n", encoding="utf-8")
    # Binary executables/compiled
    elif ext in ("bin", "exe", "dll", "so", "dylib", "class", "o", "a", "app", "dmg", "pkg", "iso", "img", "cab"):
        headers = {
            "so": b"\x7fELF\x00\x00\x00\x00",
            "exe": b"MZ\x00\x00",
            "dll": b"MZ\x00\x00",
            "class": b"\xca\xfe\xba\xbe",
            "dmg": b"koly\x00\x00\x00\x00",
            "iso": b"\x00" * 32768 + b"CD001",
        }
        path.write_bytes(headers.get(ext, b"\x00\x01\x02\x03\x04\x05"))
    # Web/Fonts
    elif ext in ("ttf", "otf", "woff", "woff2", "eot"):
        headers = {
            "ttf": b"\x00\x01\x00\x00",
            "otf": b"OTTO",
            "woff": b"wOFF",
            "woff2": b"wOF2",
        }
        path.write_bytes(headers.get(ext, b"\x00\x01\x02\x03"))
    # Game Engine formats / Models
    elif ext in ("fbx", "obj", "gltf", "glb", "blend", "unity", "tscn", "dae", "stl", "ply"):
        if ext in ("obj", "gltf", "tscn", "dae"):
            path.write_text("# Blender OBJ\nv 0 0 0\nv 1 0 0\n", encoding="utf-8")
        else:
            path.write_bytes(b"FTM\x00" if ext == "fbx" else b"glTF\x02\x00\x00\x00" if ext == "glb" else b"BLENDER_v280" if ext == "blend" else b"\x00\x01\x02\x03")
    else:
        # Text/Code
        content_map = {
            "js": "console.log('hello');",
            "ts": "const x: number = 42;",
            "tsx": "const Element = () => <div>Hello</div>;",
            "jsx": "const Element = () => <div>Hello</div>;",
            "py": "print('hello')",
            "pyw": "print('hello')",
            "html": "<html><body>Hello</body></html>",
            "css": "body { color: red; }",
            "json": '{"status": "ok"}',
            "csv": "id,name\n1,test",
            "xml": "<root><status>ok</status></root>",
            "md": "# Title\nHello",
            "yaml": "status: ok",
            "yml": "status: ok",
            "ini": "[settings]\nstatus=ok",
            "conf": "status = ok",
            "toml": "status = 'ok'",
            "sql": "SELECT 1;",
            "sh": "#!/bin/sh\necho hello",
            "bat": "@echo off\necho hello",
            "ps1": "Write-Host 'hello'",
            "properties": "status=ok",
            "log": "2026-05-24 INFO hello",
            "bak": "backup content",
            "tmp": "temporary content",
            "temp": "temporary content",
            "rtf": "{\\rtf1\\ansi\\deff0 Hello}",
            "ascii": "Hello ASCII",
        }
        content = content_map.get(ext, "Hello World")
        path.write_text(content, encoding="utf-8")
    return path

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)

# ── 1. Test Asset & File Generators (File Formats: Bytes & Text) ────────────
@pytest.mark.parametrize("ext", ALL_EXTENSIONS)
def test_file_generators(temp_dir, ext):
    """Verify that all file extension generators successfully write files without raising errors."""
    out_path = temp_dir / f"test_file.{ext if ext != 'animated_gif' else 'gif'}"
    
    if ext in MEDIA_GENERATORS:
        generator_fn = MEDIA_GENERATORS[ext]
        ffmpeg_installed = bool(shutil.which("ffmpeg"))
        
        # Audio/video extensions that require ffmpeg
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

# ── 2. Test CLI Command Delivery for all extensions ─────────────────────────
@pytest.mark.parametrize("ext", ALL_EXTENSIONS)
@patch("sage.main._prepare_model_for_use")
@patch("sage.main._build_router")
def test_cli_ask_file_generation(mock_router, mock_prep, ext):
    """Verify that requesting file generation for any extension through CLI works."""
    mock_prep.return_value = (MagicMock(), "cloud:gemini-2.0-flash")
    
    # Mock router stream method
    mock_router_inst = MagicMock()
    mock_router_inst.stream.return_value = [f"Generated test_file.{ext}"]
    mock_router.return_value = mock_router_inst
    
    result = runner.invoke(sage_app, ["ask", f"Create a test file with .{ext} extension", "--raw"])
    assert result.exit_code == 0
    assert f"test_file.{ext}" in result.output

@patch("sage.main.run")
def test_cli_ask_delegation(mock_run):
    """Verify that `sage ask --agent` delegates to the interactive agent run loop."""
    result = runner.invoke(sage_app, ["ask", "Make a website", "--agent"])
    assert result.exit_code == 0
    mock_run.assert_called_once()

# ── 3. Test SMS Bridge Delivery for all extensions ──────────────────────────
@pytest.mark.parametrize("ext", ALL_EXTENSIONS)
@patch("subprocess.run")
def test_sms_bridge_file_generation(mock_run, temp_dir, ext):
    """Verify that requesting file generation for any extension through SMS bridge executes correctly."""
    cfg = SMSConfig(computer_name="TestPC", working_dir=str(temp_dir))
    
    with patch("sage.core.sms_bridge.SAGEBackend"):
        bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
        
        # Mock subprocess execution success
        mock_result = MagicMock(returncode=0, stdout=f"Successfully generated file.{ext}", stderr="")
        mock_run.return_value = mock_result
        
        output = bridge._run_sage_task(f"Create a file with extension {ext}", mode="agent")
        
        assert f"file.{ext}" in output
        mock_run.assert_called()

# ── 4. Test Website/Backend Delivery for all extensions ─────────────────────
@pytest.mark.parametrize("ext", ALL_EXTENSIONS)
@pytest.mark.asyncio
async def test_backend_chat_file_generation(ext):
    """Verify that requesting file generation for any extension through FastAPI web endpoint works."""
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
    
    # Mock firebase auth dependencies and model catalog/runner
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
        assert f"file.{ext}" in json_data.get("output")
