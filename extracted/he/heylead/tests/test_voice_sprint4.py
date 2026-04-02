"""Tests for Sprint 4: Voice memo polish — A/B testing, analytics, scheduler, user controls."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ── Voice mode constants ──


class TestVoiceModeConstants:
    def test_valid_voice_modes(self):
        from heylead.constants import (
            VALID_VOICE_MODES,
            VOICE_MODE_AB_TEST,
            VOICE_MODE_MIXED,
            VOICE_MODE_TEXT_ONLY,
            VOICE_MODE_VOICE_ONLY,
        )

        assert VOICE_MODE_TEXT_ONLY == "text_only"
        assert VOICE_MODE_VOICE_ONLY == "voice_only"
        assert VOICE_MODE_MIXED == "mixed"
        assert VOICE_MODE_AB_TEST == "ab_test"
        assert len(VALID_VOICE_MODES) == 4
        assert "text_only" in VALID_VOICE_MODES
        assert "voice_only" in VALID_VOICE_MODES
        assert "mixed" in VALID_VOICE_MODES
        assert "ab_test" in VALID_VOICE_MODES


# ── edit_campaign voice_mode ──


class TestEditCampaignVoiceMode:
    @pytest.mark.asyncio
    async def test_invalid_voice_mode(self):
        """Rejects invalid voice_mode values."""
        from heylead.tools.edit_campaign import run_edit_campaign

        with patch("heylead.db.aio.get_setting", return_value=True):
            result = await run_edit_campaign(voice_mode="invalid")
        assert "Invalid voice_mode" in result
        assert "text_only" in result

    @pytest.mark.asyncio
    async def test_nothing_to_change(self):
        """Returns nothing-to-change when no params provided."""
        from heylead.tools.edit_campaign import run_edit_campaign

        with patch("heylead.db.aio.get_setting", return_value=True):
            result = await run_edit_campaign()
        assert "Nothing to change" in result

    @pytest.mark.asyncio
    async def test_voice_mode_update(self):
        """Updates campaign voice_mode in config_json."""
        from heylead.tools.edit_campaign import run_edit_campaign

        campaign = {
            "id": "camp-1",
            "name": "Test Campaign",
            "mode": "autopilot",
            "config_json": "{}",
            "context_json": "{}",
        }

        with patch("heylead.db.aio.get_setting", return_value=True), \
             patch("heylead.db.aio.find_active_campaign", return_value=(campaign, None)), \
             patch("heylead.db.aio.update_campaign") as mock_update, \
             patch("heylead.db.aio.get_campaign_context", return_value={}):
            result = await run_edit_campaign(voice_mode="mixed")

        assert "Voice mode" in result
        assert "mixed" in result

        # Verify config_json was updated
        call_kwargs = mock_update.call_args[1]
        updated_config = json.loads(call_kwargs["config_json"])
        assert updated_config["voice_mode"] == "mixed"

    @pytest.mark.asyncio
    async def test_voice_mode_no_change(self):
        """No update when voice_mode matches current."""
        from heylead.tools.edit_campaign import run_edit_campaign

        campaign = {
            "id": "camp-1",
            "name": "Test Campaign",
            "mode": "autopilot",
            "config_json": json.dumps({"voice_mode": "mixed"}),
            "context_json": "{}",
        }

        with patch("heylead.db.aio.get_setting", return_value=True), \
             patch("heylead.db.aio.find_active_campaign", return_value=(campaign, None)), \
             patch("heylead.db.aio.get_campaign_context", return_value={}):
            result = await run_edit_campaign(voice_mode="mixed")

        assert "No changes needed" in result


# ── Voice memo stats DB queries ──


class TestVoiceMemoStats:
    def _setup_db(self, tmp_path, monkeypatch):
        from heylead.db import schema as schema_mod
        from heylead import config

        # Reset singleton so each test gets a fresh connection to its own tmp DB
        monkeypatch.setattr(schema_mod, "_conn", None)

        db_path = tmp_path / "test.db"
        monkeypatch.setattr(config, "db_path", lambda: db_path)
        monkeypatch.setattr(config, "ensure_dirs", lambda: None)

        db = schema_mod.get_db()
        # Insert parent rows
        db.execute("INSERT INTO campaigns (id, name, status) VALUES ('c1', 'test', 'active')")
        db.execute("INSERT INTO contacts (id, name, campaign_id) VALUES ('ct1', 'Alice', 'c1')")
        db.execute("INSERT INTO contacts (id, name, campaign_id) VALUES ('ct2', 'Bob', 'c1')")
        db.execute(
            "INSERT INTO outreaches (id, campaign_id, contact_id, status) "
            "VALUES ('out-1', 'c1', 'ct1', 'connected')"
        )
        db.execute(
            "INSERT INTO outreaches (id, campaign_id, contact_id, status) "
            "VALUES ('out-2', 'c1', 'ct2', 'connected')"
        )
        # Insert voice message
        db.execute(
            "INSERT INTO messages (id, outreach_id, role, text, format) "
            "VALUES ('m1', 'out-1', 'sdr', 'Hello voice', 'voice')"
        )
        # Insert text messages
        db.execute(
            "INSERT INTO messages (id, outreach_id, role, text, format) "
            "VALUES ('m2', 'out-2', 'sdr', 'Hello text', 'text')"
        )
        db.execute(
            "INSERT INTO messages (id, outreach_id, role, text, format) "
            "VALUES ('m3', 'out-2', 'sdr', 'Follow up text', 'text')"
        )
        db.commit()
        db.close()

    def test_voice_memo_stats(self, tmp_path, monkeypatch):
        """get_voice_memo_stats returns correct counts."""
        from heylead.db.queries import get_voice_memo_stats

        self._setup_db(tmp_path, monkeypatch)

        stats = get_voice_memo_stats("c1")
        assert stats["voice_sent"] == 1
        assert stats["text_sent"] == 2

    def test_voice_memo_stats_empty(self, tmp_path, monkeypatch):
        """get_voice_memo_stats returns zeros when no messages."""
        from heylead.db import schema as schema_mod
        from heylead import config
        from heylead.db.queries import get_voice_memo_stats

        # Reset singleton so each test gets a fresh connection to its own tmp DB
        monkeypatch.setattr(schema_mod, "_conn", None)

        db_path = tmp_path / "test.db"
        monkeypatch.setattr(config, "db_path", lambda: db_path)
        monkeypatch.setattr(config, "ensure_dirs", lambda: None)

        db = schema_mod.get_db()
        db.close()

        stats = get_voice_memo_stats("c1")
        assert stats["voice_sent"] == 0
        assert stats["text_sent"] == 0

    def test_daily_voice_memo_count(self, tmp_path, monkeypatch):
        """get_daily_voice_memo_count returns today's voice count."""
        from heylead.db.queries import get_daily_voice_memo_count

        self._setup_db(tmp_path, monkeypatch)

        count = get_daily_voice_memo_count()
        assert count == 1  # One voice message inserted

    def test_voice_memo_stats_all_campaigns(self, tmp_path, monkeypatch):
        """get_voice_memo_stats with no campaign_id covers all campaigns."""
        from heylead.db.queries import get_voice_memo_stats

        self._setup_db(tmp_path, monkeypatch)

        stats = get_voice_memo_stats("")
        assert stats["voice_sent"] == 1
        assert stats["text_sent"] == 2


# ── Voice format selection (experiment_service) ──


class TestVoiceFormatSelection:
    def test_text_only_mode(self):
        """text_only voice_mode returns 'text'."""
        from heylead.services.experiment_service import get_voice_format_for_outreach

        campaign = {
            "id": "c1",
            "config_json": json.dumps({"voice_mode": "text_only"}),
        }

        with patch("heylead.db.queries.get_campaign", return_value=campaign):
            result = get_voice_format_for_outreach("c1", "out-1")
        assert result == "text"

    def test_voice_only_mode(self):
        """voice_only voice_mode returns 'voice'."""
        from heylead.services.experiment_service import get_voice_format_for_outreach

        campaign = {
            "id": "c1",
            "config_json": json.dumps({"voice_mode": "voice_only"}),
        }

        with patch("heylead.db.queries.get_campaign", return_value=campaign):
            result = get_voice_format_for_outreach("c1", "out-1")
        assert result == "voice"

    def test_mixed_mode_even_followup(self):
        """mixed mode with even followup_count returns 'text'."""
        from heylead.services.experiment_service import get_voice_format_for_outreach

        campaign = {
            "id": "c1",
            "config_json": json.dumps({"voice_mode": "mixed"}),
        }
        outreach = {"followup_count": 0}

        with patch("heylead.db.queries.get_campaign", return_value=campaign), \
             patch("heylead.db.queries.get_outreach", return_value=outreach):
            result = get_voice_format_for_outreach("c1", "out-1")
        assert result == "text"

    def test_mixed_mode_odd_followup(self):
        """mixed mode with odd followup_count returns 'voice'."""
        from heylead.services.experiment_service import get_voice_format_for_outreach

        campaign = {
            "id": "c1",
            "config_json": json.dumps({"voice_mode": "mixed"}),
        }
        outreach = {"followup_count": 1}

        with patch("heylead.db.queries.get_campaign", return_value=campaign), \
             patch("heylead.db.queries.get_outreach", return_value=outreach):
            result = get_voice_format_for_outreach("c1", "out-1")
        assert result == "voice"

    def test_ab_test_variant_a(self):
        """ab_test mode with variant A returns 'text'."""
        from heylead.services.experiment_service import get_voice_format_for_outreach

        campaign = {
            "id": "c1",
            "config_json": json.dumps({"voice_mode": "ab_test"}),
        }
        outreach = {"variant": "A"}

        with patch("heylead.db.queries.get_campaign", return_value=campaign), \
             patch("heylead.db.queries.get_outreach", return_value=outreach):
            result = get_voice_format_for_outreach("c1", "out-1")
        assert result == "text"

    def test_ab_test_variant_b(self):
        """ab_test mode with variant B returns 'voice'."""
        from heylead.services.experiment_service import get_voice_format_for_outreach

        campaign = {
            "id": "c1",
            "config_json": json.dumps({"voice_mode": "ab_test"}),
        }
        outreach = {"variant": "B"}

        with patch("heylead.db.queries.get_campaign", return_value=campaign), \
             patch("heylead.db.queries.get_outreach", return_value=outreach):
            result = get_voice_format_for_outreach("c1", "out-1")
        assert result == "voice"

    def test_no_campaign(self):
        """Returns 'text' when campaign not found."""
        from heylead.services.experiment_service import get_voice_format_for_outreach

        with patch("heylead.db.queries.get_campaign", return_value=None):
            result = get_voice_format_for_outreach("nonexistent", "out-1")
        assert result == "text"

    def test_default_mode(self):
        """Returns 'text' when no voice_mode in config."""
        from heylead.services.experiment_service import get_voice_format_for_outreach

        campaign = {
            "id": "c1",
            "config_json": "{}",
        }

        with patch("heylead.db.queries.get_campaign", return_value=campaign):
            result = get_voice_format_for_outreach("c1", "out-1")
        assert result == "text"


# ── Scheduler executor voice format ──


class TestSchedulerExecutorVoice:
    @pytest.mark.asyncio
    async def test_followup_executor_uses_voice_format(self):
        """Follow-up executor passes voice format from get_voice_format_for_outreach."""
        from heylead.scheduler.executors import _execute_followup

        job = {
            "id": "j1",
            "campaign_id": "c1",
            "outreach_id": "out-1",
            "job_type": "followup",
        }

        with patch("heylead.tools.send_followup.run_send_followup", new_callable=AsyncMock) as mock_send, \
             patch("heylead.services.experiment_service.get_voice_format_for_outreach", return_value="voice"), \
             patch("heylead.scheduler.executors._check_outreach_still_valid", return_value=None), \
             patch("heylead.scheduler.executors._check_recent_messages", return_value=None):
            mock_send.return_value = "Follow-up sent"
            result = await _execute_followup(job)

        assert result == "Follow-up sent"
        call_kwargs = mock_send.call_args[1]
        assert call_kwargs["format"] == "voice"

    @pytest.mark.asyncio
    async def test_followup_executor_defaults_text(self):
        """Follow-up executor defaults to text when voice format lookup fails."""
        from heylead.scheduler.executors import _execute_followup

        job = {
            "id": "j1",
            "campaign_id": "c1",
            "outreach_id": "out-1",
            "job_type": "followup",
        }

        with patch("heylead.tools.send_followup.run_send_followup", new_callable=AsyncMock) as mock_send, \
             patch("heylead.services.experiment_service.get_voice_format_for_outreach", side_effect=Exception("fail")), \
             patch("heylead.scheduler.executors._check_outreach_still_valid", return_value=None), \
             patch("heylead.scheduler.executors._check_recent_messages", return_value=None):
            mock_send.return_value = "Follow-up sent"
            result = await _execute_followup(job)

        assert result == "Follow-up sent"
        call_kwargs = mock_send.call_args[1]
        assert call_kwargs["format"] == "text"

    @pytest.mark.asyncio
    async def test_followup_executor_no_outreach_id(self):
        """Follow-up executor uses text format when no outreach_id."""
        from heylead.scheduler.executors import _execute_followup

        job = {
            "id": "j1",
            "campaign_id": "c1",
            "job_type": "followup",
        }

        with patch("heylead.tools.send_followup.run_send_followup", new_callable=AsyncMock) as mock_send, \
             patch("heylead.scheduler.executors._check_outreach_still_valid", return_value=None), \
             patch("heylead.scheduler.executors._check_recent_messages", return_value=None):
            mock_send.return_value = "Follow-up sent"
            result = await _execute_followup(job)

        call_kwargs = mock_send.call_args[1]
        assert call_kwargs["format"] == "text"
