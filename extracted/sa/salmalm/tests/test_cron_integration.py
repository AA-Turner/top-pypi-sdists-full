"""Integration tests for LLM Cron Manager."""
import asyncio
import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

KST = timezone(timedelta(hours=9))

import pytest

from salmalm.core.llm_cron import LLMCronManager


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def cron(tmp_path):
    """Fresh LLMCronManager with isolated jobs file."""
    mgr = LLMCronManager()
    mgr._JOBS_FILE = tmp_path / ".cron_jobs.json"
    return mgr


def _make_job(cron, kind="every", seconds=60, prompt="테스트"):
    if kind == "every":
        return cron.add_job("test-job", {"kind": "every", "seconds": seconds}, prompt)
    elif kind == "cron":
        return cron.add_job("test-job", {"kind": "cron", "expr": "* * * * *"}, prompt)
    elif kind == "at":
        past = datetime.now(KST).replace(microsecond=0).isoformat()
        return cron.add_job("test-job", {"kind": "at", "time": past}, prompt)


# ── _should_run ───────────────────────────────────────────────────────────────

class TestShouldRun:
    def test_every_first_run(self, cron):
        job = _make_job(cron, kind="every", seconds=60)
        assert cron._should_run(job) is True

    def test_every_not_elapsed(self, cron):
        job = _make_job(cron, kind="every", seconds=3600)
        job["last_run"] = datetime.now(KST).isoformat()
        assert cron._should_run(job) is False

    def test_every_elapsed(self, cron):
        job = _make_job(cron, kind="every", seconds=1)
        job["last_run"] = "2000-01-01T00:00:00+09:00"
        assert cron._should_run(job) is True

    def test_disabled_never_runs(self, cron):
        job = _make_job(cron, kind="every", seconds=1)
        job["enabled"] = False
        job["last_run"] = None
        assert cron._should_run(job) is False

    def test_at_runs_once(self, cron):
        job = _make_job(cron, kind="at")
        assert cron._should_run(job) is True
        job["last_run"] = datetime.now().isoformat()
        assert cron._should_run(job) is False

    def test_legacy_every_format(self, cron):
        """{'every': 60} without 'kind' key should normalize correctly."""
        job = cron.add_job("legacy", {"every": 60}, "test")
        job["last_run"] = None
        assert cron._should_run(job) is True

    def test_cron_expr_wildcard(self, cron):
        job = _make_job(cron, kind="cron")
        assert cron._should_run(job) is True

    def test_cron_already_ran_this_minute(self, cron):
        job = _make_job(cron, kind="cron")
        job["last_run"] = datetime.now(KST).isoformat()
        assert cron._should_run(job) is False


# ── save / load ───────────────────────────────────────────────────────────────

class TestPersistence:
    def test_save_and_load(self, cron):
        cron.add_job("job1", {"kind": "every", "seconds": 300}, "hello")
        cron2 = LLMCronManager()
        cron2._JOBS_FILE = cron._JOBS_FILE
        cron2.load_jobs()
        assert len(cron2.jobs) == 1
        assert cron2.jobs[0]["name"] == "job1"

    def test_remove_job(self, cron):
        job = cron.add_job("job1", {"kind": "every", "seconds": 60}, "x")
        assert cron.remove_job(job["id"]) is True
        assert len(cron.jobs) == 0
        # File should reflect removal
        data = json.loads(cron._JOBS_FILE.read_text())
        assert data == []

    def test_load_missing_file(self, cron, tmp_path):
        cron._JOBS_FILE = tmp_path / "nonexistent.json"
        cron.load_jobs()
        assert cron.jobs == []


# ── tick() ────────────────────────────────────────────────────────────────────

class TestTick:
    def test_tick_calls_process_message(self, cron):
        """tick() should call process_message for due jobs."""
        cron.add_job("job1", {"kind": "every", "seconds": 1}, "현재 시각 알려줘")

        mock_response = "현재 시각은 오후 6시입니다."

        with patch("salmalm.core.llm_cron._get_heartbeat") as mock_hb, \
             patch("salmalm.core.engine_pipeline.process_message", new_callable=AsyncMock) as mock_pm, \
             patch("salmalm.core.llm_cron._get_usage", return_value={"total_cost": 0.0}), \
             patch("salmalm.core.llm_cron._write_daily_log"), \
             patch.object(cron, "_notify_completion"):

            mock_hb.return_value.should_beat.return_value = False
            mock_pm.return_value = mock_response

            asyncio.run(cron.tick())

        assert mock_pm.called
        assert cron.jobs[0]["run_count"] == 1
        assert cron.jobs[0]["last_run"] is not None

    def test_tick_skips_disabled_job(self, cron):
        job = cron.add_job("job1", {"kind": "every", "seconds": 1}, "test")
        job["enabled"] = False

        with patch("salmalm.core.llm_cron._get_heartbeat") as mock_hb, \
             patch("salmalm.core.engine_pipeline.process_message", new_callable=AsyncMock) as mock_pm, \
             patch("salmalm.core.llm_cron._get_usage", return_value={"total_cost": 0.0}):

            mock_hb.return_value.should_beat.return_value = False
            asyncio.run(cron.tick())

        assert not mock_pm.called

    def test_tick_uses_fresh_session_id(self, cron):
        """Each tick must use a unique session ID (no history contamination)."""
        cron.add_job("job1", {"kind": "every", "seconds": 1}, "test")
        session_ids = []

        async def capture_session(session_id, *a, **kw):
            session_ids.append(session_id)
            return "ok"

        with patch("salmalm.core.llm_cron._get_heartbeat") as mock_hb, \
             patch("salmalm.core.engine_pipeline.process_message", side_effect=capture_session), \
             patch("salmalm.core.llm_cron._get_usage", return_value={"total_cost": 0.0}), \
             patch("salmalm.core.llm_cron._write_daily_log"), \
             patch.object(cron, "_notify_completion"):

            mock_hb.return_value.should_beat.return_value = False
            # Run tick twice
            cron.jobs[0]["last_run"] = None
            asyncio.run(cron.tick())
            cron.jobs[0]["last_run"] = None  # reset for second tick
            asyncio.run(cron.tick())

        assert len(session_ids) == 2
        assert session_ids[0] != session_ids[1], "Session IDs must be unique per tick"

    def test_tick_system_suffix_no_tts(self, cron):
        """tick() must pass system_suffix blocking TTS tools."""
        cron.add_job("job1", {"kind": "every", "seconds": 1}, "말해줘")
        captured_kwargs = {}

        async def capture(*a, **kw):
            captured_kwargs.update(kw)
            return "ok"

        with patch("salmalm.core.llm_cron._get_heartbeat") as mock_hb, \
             patch("salmalm.core.engine_pipeline.process_message", side_effect=capture), \
             patch("salmalm.core.llm_cron._get_usage", return_value={"total_cost": 0.0}), \
             patch("salmalm.core.llm_cron._write_daily_log"), \
             patch.object(cron, "_notify_completion"):

            mock_hb.return_value.should_beat.return_value = False
            asyncio.run(cron.tick())

        assert "system_suffix" in captured_kwargs
        assert "TTS" in captured_kwargs["system_suffix"] or "tts" in captured_kwargs["system_suffix"].lower()

    def test_tick_error_increments_error_count(self, cron):
        """Errors in tick() should increment error_count without crashing."""
        cron.add_job("job1", {"kind": "every", "seconds": 1}, "test")

        with patch("salmalm.core.llm_cron._get_heartbeat") as mock_hb, \
             patch("salmalm.core.engine_pipeline.process_message", new_callable=AsyncMock) as mock_pm, \
             patch("salmalm.core.llm_cron._get_usage", return_value={"total_cost": 0.0}), \
             patch.object(cron, "_handle_cron_failure"):

            mock_hb.return_value.should_beat.return_value = False
            mock_pm.side_effect = RuntimeError("API down")
            asyncio.run(cron.tick())

        assert cron.jobs[0]["error_count"] == 1
        assert cron.jobs[0]["last_run"] is not None

    def test_at_job_disabled_after_run(self, cron):
        """One-shot 'at' job must be disabled after execution."""
        job = _make_job(cron, kind="at")

        with patch("salmalm.core.llm_cron._get_heartbeat") as mock_hb, \
             patch("salmalm.core.engine_pipeline.process_message", new_callable=AsyncMock) as mock_pm, \
             patch("salmalm.core.llm_cron._get_usage", return_value={"total_cost": 0.0}), \
             patch("salmalm.core.llm_cron._write_daily_log"), \
             patch.object(cron, "_notify_completion"):

            mock_hb.return_value.should_beat.return_value = False
            mock_pm.return_value = "완료"
            asyncio.run(cron.tick())

        assert cron.jobs[0]["enabled"] is False
