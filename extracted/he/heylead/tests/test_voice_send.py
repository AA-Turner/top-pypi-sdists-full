"""Tests for Sprint 3: voice message sending via Unipile + send_voice_memo tool."""

from __future__ import annotations

import base64
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from heylead.ai.voice_memo_generator import cleanup_voice_memo

# ── Fixtures ──

SAMPLE_AUDIO = b"\xff\xfb\x90\x00" * 100  # Fake MP3 bytes


def _make_audio_file() -> str:
    """Write temp MP3 file, return path."""
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.write(fd, SAMPLE_AUDIO)
    os.close(fd)
    return path


# ── Unipile Client: send_voice_message / send_new_voice_message ──


class TestUnipileSendVoiceMessage:
    @pytest.mark.asyncio
    async def test_send_voice_existing_chat(self):
        """Voice message in an existing chat via multipart."""
        from heylead.linkedin.unipile import UnipileClient

        audio_path = _make_audio_file()
        try:
            def handler(request):
                ct = request.headers.get("content-type", "")
                assert "multipart/form-data" in ct
                return httpx.Response(200, json={"message_id": "m1"})

            transport = httpx.MockTransport(handler)
            client = UnipileClient.__new__(UnipileClient)
            client.base_url = "https://fake.unipile.com"
            client.api_key = "test-key"
            client._client = httpx.AsyncClient(transport=transport)

            result = await client.send_voice_message(
                account_id="acc1", chat_id="chat1", audio_path=audio_path,
            )
            assert result["success"] is True
            assert result["error"] == ""
            await client.close()
        finally:
            if os.path.exists(audio_path):
                os.unlink(audio_path)

    @pytest.mark.asyncio
    async def test_send_voice_new_chat(self):
        """Voice message starting a new chat."""
        from heylead.linkedin.unipile import UnipileClient

        audio_path = _make_audio_file()
        try:
            def handler(request):
                return httpx.Response(201, json={"chat_id": "new-chat-1"})

            transport = httpx.MockTransport(handler)
            client = UnipileClient.__new__(UnipileClient)
            client.base_url = "https://fake.unipile.com"
            client.api_key = "test-key"
            client._client = httpx.AsyncClient(transport=transport)

            result = await client.send_new_voice_message(
                account_id="acc1", provider_id="prov1", audio_path=audio_path,
            )
            assert result["success"] is True
            assert result["chat_id"] == "new-chat-1"
            await client.close()
        finally:
            if os.path.exists(audio_path):
                os.unlink(audio_path)

    @pytest.mark.asyncio
    async def test_send_voice_file_not_found(self):
        """Missing audio file returns error without crashing."""
        from heylead.linkedin.unipile import UnipileClient

        client = UnipileClient.__new__(UnipileClient)
        client.base_url = "https://fake.unipile.com"
        client.api_key = "test-key"
        client._client = httpx.AsyncClient()

        result = await client.send_voice_message(
            account_id="acc1", chat_id="chat1", audio_path="/nonexistent/voice.mp3",
        )
        assert result["success"] is False
        assert "not found" in result["error"]
        await client.close()

    @pytest.mark.asyncio
    async def test_send_voice_rate_limited(self):
        """429 from Unipile handled gracefully."""
        from heylead.linkedin.unipile import UnipileClient

        audio_path = _make_audio_file()
        try:
            transport = httpx.MockTransport(lambda req: httpx.Response(429))
            client = UnipileClient.__new__(UnipileClient)
            client.base_url = "https://fake.unipile.com"
            client.api_key = "test-key"
            client._client = httpx.AsyncClient(transport=transport)

            result = await client.send_voice_message(
                account_id="acc1", chat_id="chat1", audio_path=audio_path,
            )
            assert result["success"] is False
            assert "Rate limited" in result["error"]
            await client.close()
        finally:
            if os.path.exists(audio_path):
                os.unlink(audio_path)

    @pytest.mark.asyncio
    async def test_send_voice_with_text(self):
        """Voice message with accompanying text."""
        from heylead.linkedin.unipile import UnipileClient

        audio_path = _make_audio_file()
        try:
            def handler(request):
                return httpx.Response(200, json={})

            transport = httpx.MockTransport(handler)
            client = UnipileClient.__new__(UnipileClient)
            client.base_url = "https://fake.unipile.com"
            client.api_key = "test-key"
            client._client = httpx.AsyncClient(transport=transport)

            result = await client.send_voice_message(
                account_id="acc1", chat_id="chat1",
                audio_path=audio_path, text="Check this out!",
            )
            assert result["success"] is True
            await client.close()
        finally:
            if os.path.exists(audio_path):
                os.unlink(audio_path)


# ── DB: save_message with format ──


class TestSaveMessageFormat:
    def _setup_db(self, tmp_path, monkeypatch):
        """Create a fresh DB with parent rows for FK satisfaction."""
        from heylead.db import schema as schema_mod
        from heylead import config

        db_path = tmp_path / "test.db"
        monkeypatch.setattr(config, "db_path", lambda: db_path)
        monkeypatch.setattr(config, "ensure_dirs", lambda: None)

        db = schema_mod.get_db()
        # Insert parent rows so FK constraints are satisfied
        db.execute("INSERT INTO campaigns (id, name, status) VALUES ('c1', 'test', 'active')")
        db.execute("INSERT INTO contacts (id, name) VALUES ('ct1', 'Test')")
        db.execute(
            "INSERT INTO outreaches (id, campaign_id, contact_id, status) "
            "VALUES ('out-1', 'c1', 'ct1', 'pending')"
        )
        db.commit()
        db.close()

    def test_save_message_default_format(self, tmp_path, monkeypatch):
        """save_message defaults to format='text'."""
        from heylead.db import queries

        self._setup_db(tmp_path, monkeypatch)

        msg_id = queries.save_message("out-1", "sdr", "Hello")
        db = queries.get_db()
        row = db.execute("SELECT format FROM messages WHERE id = ?", (msg_id,)).fetchone()
        db.close()
        assert row["format"] == "text"

    def test_save_message_voice_format(self, tmp_path, monkeypatch):
        """save_message with format='voice' stored correctly."""
        from heylead.db import queries

        self._setup_db(tmp_path, monkeypatch)

        msg_id = queries.save_message("out-1", "sdr", "Hello", format="voice")
        db = queries.get_db()
        row = db.execute("SELECT format FROM messages WHERE id = ?", (msg_id,)).fetchone()
        db.close()
        assert row["format"] == "voice"


# ── send_voice_memo tool (mocked) ──


class TestSendVoiceMemoTool:
    @pytest.mark.asyncio
    async def test_not_enabled(self):
        """Returns error when voice memos not enabled."""
        from heylead.tools.send_voice_memo import run_send_voice_memo

        with patch("heylead.tools.send_voice_memo.is_voice_memo_enabled", return_value=False):
            result = await run_send_voice_memo()
        assert "not enabled" in result

    @pytest.mark.asyncio
    async def test_no_campaign(self):
        """Returns error when no active campaign."""
        from heylead.tools.send_voice_memo import run_send_voice_memo

        with patch("heylead.tools.send_voice_memo.is_voice_memo_enabled", return_value=True), \
             patch("heylead.tools.send_voice_memo.find_active_campaign", return_value=(None, "No active campaigns.\n\nCreate one with create_campaign('description').")):
            result = await run_send_voice_memo()
        assert "No active campaign" in result

    @pytest.mark.asyncio
    async def test_no_candidates(self):
        """Returns all-caught-up when no followup candidates."""
        from heylead.tools.send_voice_memo import run_send_voice_memo

        campaign = {"id": "c1", "name": "Test"}
        with patch("heylead.tools.send_voice_memo.is_voice_memo_enabled", return_value=True), \
             patch("heylead.tools.send_voice_memo.find_active_campaign", return_value=(campaign, "")), \
             patch("heylead.tools.send_voice_memo.get_followup_candidates", return_value=[]):
            result = await run_send_voice_memo()
        assert "All caught up" in result
