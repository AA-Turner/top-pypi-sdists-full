"""Tests for the improved action tracking system.

Covers:
- log_action with campaign_id
- get_actions_taken / get_actions_skipped time-windowed queries
- get_outreach_changes real-table queries
- get_verification_summary
- _log_skip helper in the planner
- run_scheduler_activity report formatting
"""

from __future__ import annotations

import time

import pytest

from heylead.db.async_bridge import run_db
from heylead.db.queries import (
    create_campaign,
    create_outreach,
    get_actions_taken,
    get_actions_skipped,
    get_actions_skipped_detailed,
    get_outreach_changes,
    get_verification_summary,
    log_action,
    save_contact,
    save_engagement,
    update_outreach,
)
from heylead.db.schema import get_db


# ── Helpers ──


def _make_campaign_outreach(
    status: str = "pending",
    invited_at: int | None = None,
    accepted_at: int | None = None,
) -> tuple[str, str, str]:
    """Create campaign + contact + outreach. Returns (camp_id, contact_id, outreach_id)."""
    camp_id = create_campaign(name="Track Test", status="active")
    contact_id = save_contact(
        campaign_id=camp_id,
        name="Alice Test",
        title="CTO",
        company="TestCo",
        linkedin_id=f"alice-{time.time_ns()}",
    )
    outreach_id = create_outreach(campaign_id=camp_id, contact_id=contact_id, status=status)

    if invited_at or accepted_at:
        db = get_db()
        parts, vals = [], []
        if invited_at:
            parts.append("invited_at = ?")
            vals.append(invited_at)
        if accepted_at:
            parts.append("accepted_at = ?")
            vals.append(accepted_at)
        vals.append(outreach_id)
        db.execute(f"UPDATE outreaches SET {', '.join(parts)} WHERE id = ?", tuple(vals))
        db.commit()
        db.close()

    return camp_id, contact_id, outreach_id


# ── Tests: log_action with campaign_id ──


class TestLogActionCampaignId:
    def test_log_action_stores_campaign_id(self):
        camp_id = create_campaign(name="Log Test", status="active")
        action_id = log_action(
            "invitation_sent",
            result="success",
            campaign_id=camp_id,
            details={"test": True},
        )
        db = get_db()
        row = db.execute("SELECT * FROM actions_log WHERE id = ?", (action_id,)).fetchone()
        db.close()

        assert row is not None
        assert row["campaign_id"] == camp_id
        assert row["action_type"] == "invitation_sent"
        assert row["result"] == "success"

    def test_log_action_without_campaign_id(self):
        action_id = log_action("test_action", result="success")
        db = get_db()
        row = db.execute("SELECT * FROM actions_log WHERE id = ?", (action_id,)).fetchone()
        db.close()

        assert row is not None
        assert row["campaign_id"] is None


# ── Tests: get_actions_taken ──


class TestGetActionsTaken:
    def test_returns_grouped_results(self):
        camp_id = create_campaign(name="AT Test", status="active")
        log_action("invitation_sent", result="success", campaign_id=camp_id)
        log_action("invitation_sent", result="success", campaign_id=camp_id)
        log_action("invitation_sent", result="error", campaign_id=camp_id)
        log_action("followup_sent", result="success", campaign_id=camp_id)

        actions = get_actions_taken(hours=1, campaign_id=camp_id)

        assert "invitation_sent" in actions
        assert actions["invitation_sent"]["total"] == 3
        assert actions["invitation_sent"]["success"] == 2
        assert actions["invitation_sent"]["error"] == 1

        assert "followup_sent" in actions
        assert actions["followup_sent"]["total"] == 1

    def test_excludes_skip_entries(self):
        camp_id = create_campaign(name="AT Skip", status="active")
        log_action("invitation_sent", result="success", campaign_id=camp_id)
        log_action("skip_invite", result="skipped", campaign_id=camp_id,
                   details={"reason": "daily_limit"})

        actions = get_actions_taken(hours=1, campaign_id=camp_id)

        assert "invitation_sent" in actions
        assert "skip_invite" not in actions

    def test_empty_window(self):
        actions = get_actions_taken(hours=0)
        assert actions == {}


# ── Tests: get_actions_skipped ──


class TestGetActionsSkipped:
    def test_returns_skip_reasons(self):
        camp_id = create_campaign(name="Skip Test", status="active")
        log_action("skip_follow", result="skipped", campaign_id=camp_id,
                   details={"reason": "daily_limit", "count": 50, "limit": 50})
        log_action("skip_follow", result="skipped", campaign_id=camp_id,
                   details={"reason": "daily_limit"})
        log_action("skip_engage", result="skipped", campaign_id=camp_id,
                   details={"reason": "no_candidates"})

        skips = get_actions_skipped(hours=1, campaign_id=camp_id)

        assert skips["daily_limit"] == 2
        assert skips["no_candidates"] == 1

    def test_detailed_skip_groups_by_action(self):
        camp_id = create_campaign(name="Skip Detail", status="active")
        log_action("skip_follow", result="skipped", campaign_id=camp_id,
                   details={"reason": "daily_limit"})
        log_action("skip_engage", result="skipped", campaign_id=camp_id,
                   details={"reason": "daily_limit"})
        log_action("skip_invite", result="skipped", campaign_id=camp_id,
                   details={"reason": "rate_limited"})

        skips = get_actions_skipped_detailed(hours=1, campaign_id=camp_id)

        assert "daily_limit" in skips
        assert skips["daily_limit"]["follow"] == 1
        assert skips["daily_limit"]["engage"] == 1
        assert "rate_limited" in skips
        assert skips["rate_limited"]["invite"] == 1


# ── Tests: get_outreach_changes ──


class TestGetOutreachChanges:
    def test_counts_invited(self):
        now = int(time.time())
        camp_id, _, outreach_id = _make_campaign_outreach(status="invited", invited_at=now)

        # Mark as verified so it shows in verified-only count
        db = get_db()
        db.execute(
            "UPDATE outreaches SET verified_status = 'confirmed' WHERE id = ?",
            (outreach_id,),
        )
        db.commit()
        db.close()

        changes = get_outreach_changes(hours=1, campaign_id=camp_id)
        assert changes["invited"] == 1
        assert changes["accepted"] == 0

    def test_counts_invited_pending(self):
        """Unverified invitations appear in invited_pending."""
        now = int(time.time())
        camp_id, _, _ = _make_campaign_outreach(status="invited", invited_at=now)

        changes = get_outreach_changes(hours=1, campaign_id=camp_id)
        assert changes["invited"] == 0  # not yet verified
        assert changes["invited_pending"] == 1

    def test_counts_accepted(self):
        now = int(time.time())
        camp_id, _, _ = _make_campaign_outreach(
            status="connected", invited_at=now - 3600, accepted_at=now,
        )

        changes = get_outreach_changes(hours=1, campaign_id=camp_id)
        assert changes["accepted"] == 1

    def test_counts_engagements(self):
        now = int(time.time())
        camp_id, _, outreach_id = _make_campaign_outreach(status="pending")

        save_engagement(
            outreach_id=outreach_id,
            action_type="comment",
            post_id="post-1",
            text="Great post!",
            status="sent",
        )
        save_engagement(
            outreach_id=outreach_id,
            action_type="react",
            post_id="post-2",
            status="sent",
        )

        # Mark engagements as verified
        db = get_db()
        db.execute(
            "UPDATE engagements SET verified_status = 'verified' WHERE outreach_id = ? AND action_type = 'comment'",
            (outreach_id,),
        )
        db.execute(
            "UPDATE engagements SET verified_status = 'trust_api' WHERE outreach_id = ? AND action_type = 'react'",
            (outreach_id,),
        )
        db.commit()
        db.close()

        changes = get_outreach_changes(hours=1, campaign_id=camp_id)
        assert changes["engagements"].get("comment") == 1
        assert changes["engagements"].get("react") == 1

    def test_counts_engagements_pending(self):
        """Unverified engagements appear in engagements_pending."""
        now = int(time.time())
        camp_id, _, outreach_id = _make_campaign_outreach(status="pending")

        save_engagement(
            outreach_id=outreach_id,
            action_type="comment",
            post_id="post-1",
            text="Nice!",
            status="sent",
        )

        changes = get_outreach_changes(hours=1, campaign_id=camp_id)
        assert changes["engagements"].get("comment") is None  # not verified
        assert changes["engagements_pending"].get("comment") == 1

    def test_old_data_excluded(self):
        old_time = int(time.time()) - 7200  # 2h ago
        camp_id, _, _ = _make_campaign_outreach(status="invited", invited_at=old_time)

        changes = get_outreach_changes(hours=1, campaign_id=camp_id)
        assert changes["invited"] == 0


# ── Tests: get_verification_summary ──


class TestGetVerificationSummary:
    def test_counts_verified(self):
        now = int(time.time())
        camp_id, _, outreach_id = _make_campaign_outreach(
            status="invited", invited_at=now,
        )

        db = get_db()
        db.execute(
            "UPDATE outreaches SET verified_at = ?, verified_status = 'confirmed' WHERE id = ?",
            (now, outreach_id),
        )
        db.commit()
        db.close()

        summary = get_verification_summary(hours=1)
        assert summary.get("confirmed", 0) >= 1

    def test_counts_pending(self):
        now = int(time.time())
        _make_campaign_outreach(status="invited", invited_at=now)

        summary = get_verification_summary(hours=1)
        assert summary.get("pending", 0) >= 1


# ── Tests: _log_skip helper ──


class TestLogSkipHelper:
    @pytest.mark.asyncio
    async def test_log_skip_creates_entry(self):
        from heylead.db.async_bridge import run_db
        from heylead.scheduler.planner import _log_skip

        camp_id = await run_db(create_campaign, name="Skip Helper", status="active")
        await _log_skip(camp_id, "follow", "daily_limit", {"count": 50, "limit": 50})

        def _check(cid):
            _db = get_db()
            row = _db.execute(
                "SELECT * FROM actions_log WHERE action_type = 'skip_follow' AND campaign_id = ?",
                (cid,),
            ).fetchone()
            _db.close()
            return row

        row = await run_db(_check, camp_id)

        assert row is not None
        assert row["result"] == "skipped"
        import json
        details = json.loads(row["details_json"])
        assert details["reason"] == "daily_limit"
        assert details["count"] == 50

    @pytest.mark.asyncio
    async def test_log_skip_never_raises(self):
        from heylead.scheduler.planner import _log_skip

        # Should not raise even with bad data
        await _log_skip(None, "test", "test_reason")


# ── Tests: run_scheduler_activity ──


class TestRunSchedulerActivity:
    @pytest.mark.asyncio
    async def test_activity_report_format(self):
        from heylead.tools.scheduler_status import run_scheduler_activity

        # Seed some data
        def _seed():
            now = int(time.time())
            camp_id, _, outreach_id = _make_campaign_outreach(
                status="invited", invited_at=now,
            )
            log_action("invitation_sent", result="success", campaign_id=camp_id)
            log_action("skip_follow", result="skipped", campaign_id=camp_id,
                       details={"reason": "daily_limit"})
            return camp_id

        camp_id = await run_db(_seed)

        result = await run_scheduler_activity(hours=1, campaign_id=camp_id)

        assert "# Activity Report" in result
        assert "Verified LinkedIn Results" in result
        assert "Invitations sent:" in result
        assert "Actions Taken" in result
        assert "Actions NOT Taken" in result
        assert "daily_limit" in result
