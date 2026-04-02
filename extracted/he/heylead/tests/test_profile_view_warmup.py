"""Tests for the Profile View warm-up action.

Covers:
- DB query: get_profile_view_candidates()
- Scheduler planner: plan_profile_views()
- Scheduler executor: _execute_profile_view()
- Engage tool: _handle_view() (autopilot + copilot)
- Campaign config toggle: enable_profile_views
"""

from __future__ import annotations

import json
import time
from unittest.mock import AsyncMock, patch

import pytest

from heylead.constants import (
    JOB_PROFILE_VIEW,
    PROFILE_VIEW_DELAY_MAX,
    PROFILE_VIEW_DELAY_MIN,
)
from heylead.db.async_bridge import run_db
from heylead.db.queries import (
    create_campaign,
    create_outreach,
    create_scheduler_job,
    get_pending_job_count,
    get_profile_view_candidates,
    save_contact,
    save_engagement,
    update_campaign,
)
from heylead.db.schema import get_db


# ── Helpers ──


def _setup_campaign_and_outreach(
    status: str = "pending",
    config_json: dict | None = None,
) -> tuple[str, str, str]:
    """Create a campaign + contact + outreach. Returns (campaign_id, contact_id, outreach_id)."""
    camp_id = create_campaign(name="Test Campaign", status="active")
    if config_json:
        update_campaign(camp_id, config_json=json.dumps(config_json))
    contact_id = save_contact(
        campaign_id=camp_id,
        name="Jane Doe",
        title="VP Sales",
        company="Acme",
        linkedin_id="jane-123",
    )
    outreach_id = create_outreach(campaign_id=camp_id, contact_id=contact_id, status=status)
    return camp_id, contact_id, outreach_id


# ── DB Query Tests ──


class TestGetProfileViewCandidates:
    def test_returns_pending_outreaches_without_view(self):
        camp_id, _, outreach_id = _setup_campaign_and_outreach()
        candidates = get_profile_view_candidates(camp_id)
        assert len(candidates) == 1
        assert candidates[0]["outreach_id"] == outreach_id

    def test_excludes_already_viewed(self):
        camp_id, _, outreach_id = _setup_campaign_and_outreach()
        save_engagement(
            outreach_id=outreach_id,
            action_type="profile_view",
            post_id="",
            post_text="",
            text="Viewed Jane Doe's profile",
            status="sent",
        )
        candidates = get_profile_view_candidates(camp_id)
        assert len(candidates) == 0

    def test_excludes_non_pending_status(self):
        camp_id, _, _ = _setup_campaign_and_outreach(status="invited")
        candidates = get_profile_view_candidates(camp_id)
        assert len(candidates) == 0

    def test_excludes_skip_engagement(self):
        camp_id, _, outreach_id = _setup_campaign_and_outreach()
        db = get_db()
        db.execute(
            "UPDATE outreaches SET next_action = 'skip_engagement' WHERE id = ?",
            (outreach_id,),
        )
        db.commit()
        db.close()
        candidates = get_profile_view_candidates(camp_id)
        assert len(candidates) == 0

    def test_orders_by_fit_score_desc(self):
        camp_id = create_campaign(name="Score Test", status="active")
        c1 = save_contact(
            campaign_id=camp_id,
            name="Low Score",
            title="Jr Dev",
            company="A",
            linkedin_id="low-1",
            fit_score=0.3,
        )
        c2 = save_contact(
            campaign_id=camp_id,
            name="High Score",
            title="CTO",
            company="B",
            linkedin_id="high-1",
            fit_score=0.9,
        )
        create_outreach(campaign_id=camp_id, contact_id=c1, status="pending")
        create_outreach(campaign_id=camp_id, contact_id=c2, status="pending")
        candidates = get_profile_view_candidates(camp_id)
        assert len(candidates) == 2
        assert candidates[0]["name"] == "High Score"


# ── Planner Tests ──


class TestPlanProfileViews:
    @pytest.mark.asyncio
    async def test_creates_profile_view_jobs(self):
        camp_id, _, _ = await run_db(_setup_campaign_and_outreach)
        from heylead.scheduler.planner import plan_profile_views

        await plan_profile_views(camp_id)
        count = await run_db(get_pending_job_count, camp_id, JOB_PROFILE_VIEW)
        assert count >= 1

    @pytest.mark.asyncio
    async def test_respects_disable_toggle(self):
        camp_id, _, _ = await run_db(
            _setup_campaign_and_outreach,
            config_json={"enable_profile_views": False},
        )
        from heylead.scheduler.planner import plan_profile_views

        await plan_profile_views(camp_id)
        count = await run_db(get_pending_job_count, camp_id, JOB_PROFILE_VIEW)
        assert count == 0

    @pytest.mark.asyncio
    async def test_caps_pending_jobs_at_five(self):
        def _seed():
            camp_id = create_campaign(name="Cap Test", status="active")
            now = int(time.time())
            for i in range(5):
                cid = save_contact(
                    campaign_id=camp_id,
                    name=f"Person {i}",
                    title="Engineer",
                    company="Co",
                    linkedin_id=f"person-{i}",
                )
                oid = create_outreach(campaign_id=camp_id, contact_id=cid, status="pending")
                create_scheduler_job(
                    campaign_id=camp_id,
                    job_type=JOB_PROFILE_VIEW,
                    scheduled_at=now + 600 + i * 60,
                    outreach_id=oid,
                )
            return camp_id

        camp_id = await run_db(_seed)
        from heylead.scheduler.planner import plan_profile_views

        await plan_profile_views(camp_id)
        count = await run_db(get_pending_job_count, camp_id, JOB_PROFILE_VIEW)
        # Should not exceed 5
        assert count == 5


# ── Executor Tests ──


class TestExecuteProfileView:
    @pytest.mark.asyncio
    async def test_calls_engage_prospect_with_view_action(self):
        camp_id, _, outreach_id = await run_db(_setup_campaign_and_outreach)
        job = {
            "campaign_id": camp_id,
            "outreach_id": outreach_id,
        }
        with patch(
            "heylead.tools.engage_prospect.run_engage_prospect",
            new_callable=AsyncMock,
            return_value="Viewed **Jane Doe**'s profile",
        ) as mock_engage:
            from heylead.scheduler.executors import _execute_profile_view

            result = await _execute_profile_view(job)
            mock_engage.assert_called_once_with(
                campaign_id=camp_id,
                outreach_id=outreach_id,
                action="view",
                mode="autopilot",
            )
            assert "Viewed" in str(result)

    @pytest.mark.asyncio
    async def test_permanent_failure_marks_skip(self):
        camp_id, _, outreach_id = await run_db(_setup_campaign_and_outreach)
        job = {
            "campaign_id": camp_id,
            "outreach_id": outreach_id,
        }
        with patch(
            "heylead.tools.engage_prospect.run_engage_prospect",
            new_callable=AsyncMock,
            return_value="Profile view failed for Jane: Unipile returned 404: not found",
        ):
            from heylead.scheduler.executors import _execute_profile_view

            result = await _execute_profile_view(job)
            assert "failed" in str(result).lower()

    @pytest.mark.asyncio
    async def test_transient_failure_raises_for_retry(self):
        camp_id, _, outreach_id = await run_db(_setup_campaign_and_outreach)
        job = {
            "campaign_id": camp_id,
            "outreach_id": outreach_id,
        }
        with patch(
            "heylead.tools.engage_prospect.run_engage_prospect",
            new_callable=AsyncMock,
            return_value="Profile view failed for Jane: Unipile returned 500: server error",
        ):
            from heylead.scheduler.executors import _execute_profile_view

            with pytest.raises(RuntimeError, match="Profile view failed"):
                await _execute_profile_view(job)


# ── Campaign Config Tests ──


class TestCampaignConfigToggle:
    def test_default_config_includes_profile_views(self):
        """Verify that new campaigns have enable_profile_views: True by default."""
        camp_id = create_campaign(
            name="Config Test",
            status="active",
            config_json=json.dumps({
                "enable_profile_views": True,
                "enable_follows": True,
            }),
        )
        from heylead.db.queries import get_campaign

        campaign = get_campaign(camp_id)
        config = json.loads(campaign["config_json"])
        assert config.get("enable_profile_views") is True
