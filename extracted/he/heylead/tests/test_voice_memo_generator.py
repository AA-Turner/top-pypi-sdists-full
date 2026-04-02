"""Tests for ai/voice_memo_generator.py — voice memo generation orchestrator."""

from __future__ import annotations

import os
import tempfile
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from heylead.ai.voice_memo_generator import (
    cleanup_old_voice_memos,
    cleanup_voice_memo,
    generate_voice_memo,
)


SAMPLE_AUDIO = b"\xff\xfb\x90\x00" * 100  # Fake MP3 bytes

SAMPLE_VOICE_CONFIG = {
    "acting_instructions": "Direct, professional",
    "speed": 1.0,
    "output_format": "mp3",
    "sample_rate": 48000,
    "sliders": {"assertiveness": 50},
}


# ── generate_voice_memo ──


class TestGenerateVoiceMemo:
    @pytest.mark.asyncio
    @patch("heylead.ai.voice_memo_generator.get_hume_api_key", return_value="test-key")
    @patch("heylead.ai.voice_memo_generator.get_setting", return_value=SAMPLE_VOICE_CONFIG)
    async def test_success_local(self, mock_setting, mock_key):
        with patch("heylead.ai.voice_memo_generator._generate_local", new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = {
                "audio": SAMPLE_AUDIO,
                "duration_seconds": 3.5,
                "generation_id": "gen-123",
            }
            with tempfile.TemporaryDirectory() as tmpdir:
                output = os.path.join(tmpdir, "test.mp3")
                result = await generate_voice_memo(
                    "Hello world",
                    voice_config=SAMPLE_VOICE_CONFIG,
                    output_path=output,
                )

                assert result["success"] is True
                assert result["audio_path"] == output
                assert result["duration_seconds"] == 3.5
                assert result["file_size_bytes"] == len(SAMPLE_AUDIO)
                assert os.path.exists(output)

    @pytest.mark.asyncio
    async def test_empty_text(self):
        result = await generate_voice_memo("", voice_config=SAMPLE_VOICE_CONFIG)
        assert result["success"] is False
        assert "Empty text" in result["error"]

    @pytest.mark.asyncio
    @patch("heylead.ai.voice_memo_generator.get_setting", return_value={})
    async def test_no_voice_config(self, mock_setting):
        result = await generate_voice_memo("Hello", voice_config=None)
        assert result["success"] is False
        assert "No Hume voice config" in result["error"]

    @pytest.mark.asyncio
    @patch("heylead.ai.voice_memo_generator.get_hume_api_key", return_value="test-key")
    @patch("heylead.ai.voice_memo_generator.get_setting", return_value=SAMPLE_VOICE_CONFIG)
    async def test_generation_error(self, mock_setting, mock_key):
        with patch("heylead.ai.voice_memo_generator._generate_local", new_callable=AsyncMock) as mock_gen:
            mock_gen.side_effect = RuntimeError("Hume API failed")
            result = await generate_voice_memo(
                "Hello",
                voice_config=SAMPLE_VOICE_CONFIG,
            )
            assert result["success"] is False
            assert "Hume API failed" in result["error"]

    @pytest.mark.asyncio
    @patch("heylead.ai.voice_memo_generator.get_hume_api_key", return_value="test-key")
    async def test_text_truncation(self, mock_key):
        with patch("heylead.ai.voice_memo_generator._generate_local", new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = {
                "audio": SAMPLE_AUDIO,
                "duration_seconds": 1.0,
                "generation_id": "gen-456",
            }
            long_text = "A" * 600
            with tempfile.TemporaryDirectory() as tmpdir:
                output = os.path.join(tmpdir, "test.mp3")
                result = await generate_voice_memo(
                    long_text,
                    voice_config=SAMPLE_VOICE_CONFIG,
                    output_path=output,
                )
                assert result["success"] is True
                assert len(result["text"]) == 500


# ── cleanup ──


class TestCleanup:
    def test_cleanup_voice_memo(self):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(SAMPLE_AUDIO)
            path = f.name
        assert os.path.exists(path)
        cleanup_voice_memo(path)
        assert not os.path.exists(path)

    def test_cleanup_nonexistent(self):
        # Should not raise
        cleanup_voice_memo("/tmp/nonexistent_voice_memo.mp3")

    def test_cleanup_old_voice_memos(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create an "old" file
            old_file = Path(tmpdir) / "old.mp3"
            old_file.write_bytes(SAMPLE_AUDIO)
            # Set mtime to 48 hours ago
            old_time = time.time() - (48 * 3600)
            os.utime(old_file, (old_time, old_time))

            # Create a "new" file
            new_file = Path(tmpdir) / "new.mp3"
            new_file.write_bytes(SAMPLE_AUDIO)

            with patch("heylead.ai.voice_memo_generator.voice_memo_dir", return_value=Path(tmpdir)):
                deleted = cleanup_old_voice_memos(max_age_hours=24)

            assert deleted == 1
            assert not old_file.exists()
            assert new_file.exists()
