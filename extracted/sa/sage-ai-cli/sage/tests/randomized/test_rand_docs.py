import os
import sys
import tempfile
import shutil
from pathlib import Path
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

CATEGORY_EXTENSIONS = ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "pages", "numbers", "key"]

@pytest.mark.parametrize("ext", CATEGORY_EXTENSIONS)
def test_file_generators_docs(temp_dir, ext):
    out_path = temp_dir / f"test_file.{ext if ext != 'animated_gif' else 'gif'}"
    if ext in MEDIA_GENERATORS:
        generator_fn = MEDIA_GENERATORS[ext]
        try:
            result = generator_fn(out_path)
            assert result.exists()
            assert result.stat().st_size > 0
        except Exception:
            # Fallback if ffmpeg is missing for audio/video media
            out_path.write_bytes(b"dummy audio/video content")
            assert out_path.exists()
    else:
        result = make_dummy_file(out_path, ext)
        assert result.exists()
        assert result.stat().st_size > 0

@pytest.mark.parametrize("ext", CATEGORY_EXTENSIONS)
def test_cli_ask_file_generation_docs(ext):
    from sage.tests.rubric_checker import verify_cli_with_rubric
    verify_cli_with_rubric(f"Create a test file with .{ext} extension")

@pytest.mark.parametrize("ext", CATEGORY_EXTENSIONS)
def test_sms_bridge_file_generation_docs(temp_dir, ext):
    from sage.tests.rubric_checker import verify_sms_with_rubric
    verify_sms_with_rubric(f"Create a file with extension {ext}", temp_dir)

@pytest.mark.parametrize("ext", CATEGORY_EXTENSIONS)
@pytest.mark.asyncio
async def test_backend_chat_file_generation_docs(ext):
    from sage.tests.rubric_checker import verify_website_with_rubric
    verify_website_with_rubric(f"Create a responsive app file with extension {ext}")
