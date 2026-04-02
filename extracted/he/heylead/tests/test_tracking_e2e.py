"""End-to-end tests for tracking fixes on the MCP client side.

Verifies campaign stats, engagement campaign_id linking, monthly usage sync,
acceptance rate calculations, and reaction (like) engagement flow.
"""

from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

from heylead.db.async_bridge import run_db
from heylead.db.queries import (
    create_campaign,
    create_outreach,
    get_campaign_stats,
    get_engagement_stats,
    get_monthly_usage,
    increment_usage,
    save_contact,
    save_engagement,
    set_monthly_usage,
    update_outreach,
)
from heylead.db.schema import get_db


# ── Helpers ──


def _setup_campaign_and_outreach(
    status: str = "pending",
    invite_attempts: int = 0,
    invited_at: int | None = None,
) -> tuple[str, str, str]:
    """Create a campaign + contact + outreach. Returns (campaign_id, contact_id, outreach_id)."""
    camp_id = create_campaign(name="Test Campaign", status="active")
    contact_id = save_contact(
        campaign_id=camp_id,
        name="Jane Doe",
        title="VP Sales",
        company="Acme",
        linkedin_id="jane-123",
    )
    outreach_id = create_outreach(campaign_id=camp_id, contact_id=contact_id, status=status)

    # Apply extra fields via raw SQL (update_outreach may not accept all)
    if invite_attempts or invited_at:
        db = get_db()
        updates = []
        vals: list = []
        if invite_attempts:
            updates.append("invite_attempts = ?")
            vals.append(invite_attempts)
        if invited_at:
            updates.append("invited_at = ?")
            vals.append(invited_at)
        vals.append(outreach_id)
        db.execute(f"UPDATE outreaches SET {', '.join(updates)} WHERE id = ?", tuple(vals))
        db.commit()
        db.close()

    return camp_id, contact_id, outreach_id


# ── Test Class 1: Campaign Stats ──


class TestCampaignStats:
    """Tests for get_campaign_stats() — acceptance rate, invite_failed, mature rate."""

    def test_invite_failed_counts_pending_with_attempts(self):
        camp_id, _, out_id = _setup_campaign_and_outreach(
            status="pending", invite_attempts=2,
        )
        stats = get_campaign_stats(camp_id)
        assert stats["invite_failed"] == 1

    def test_invite_failed_excludes_invited(self):
        camp_id, _, out_id = _setup_campaign_and_outreach(status="invited")
        # invited status = successful, should not be counted as failed
        stats = get_campaign_stats(camp_id)
        assert stats["invite_failed"] == 0

    def test_mature_acceptance_rate(self):
        camp_id = create_campaign(name="Mature Test", status="active")
        eight_days_ago = int(time.time()) - (8 * 86400)

        # Old invite (>7d ago) — accepted
        c1 = save_contact(campaign_id=camp_id, name="Old Lead", linkedin_id="old-1")
        o1 = create_outreach(campaign_id=camp_id, contact_id=c1, status="connected")
        db = get_db()
        db.execute("UPDATE outreaches SET invited_at = ? WHERE id = ?", (eight_days_ago, o1))
        db.commit()
        db.close()

        # Recent invite (<7d ago) — still pending
        c2 = save_contact(campaign_id=camp_id, name="New Lead", linkedin_id="new-1")
        o2 = create_outreach(campaign_id=camp_id, contact_id=c2, status="invited")
        db = get_db()
        db.execute("UPDATE outreaches SET invited_at = ? WHERE id = ?", (int(time.time()), o2))
        db.commit()
        db.close()

        stats = get_campaign_stats(camp_id)
        # Primary acceptance rate uses only mature (>7d) invitations
        # Old invite is mature + connected → 100% acceptance of mature pool
        assert abs(stats["acceptance_rate"] - 1.0) < 0.01  # 1/1 = 100%
        # Raw rate includes both invites → 1/2 = 50%
        assert abs(stats["raw_acceptance_rate"] - 0.5) < 0.01

    def test_opted_out_counted_as_connected(self):
        camp_id = create_campaign(name="OptOut Test", status="active")
        eight_days_ago = int(time.time()) - (8 * 86400)

        # Lead that opted out (still replied, so counts as connected)
        c1 = save_contact(campaign_id=camp_id, name="Opted Out", linkedin_id="opt-1")
        o1 = create_outreach(campaign_id=camp_id, contact_id=c1, status="opted_out")
        db = get_db()
        db.execute("UPDATE outreaches SET invited_at = ? WHERE id = ?", (eight_days_ago, o1))
        db.commit()
        db.close()

        # Lead that accepted
        c2 = save_contact(campaign_id=camp_id, name="Accepted", linkedin_id="acc-1")
        o2 = create_outreach(campaign_id=camp_id, contact_id=c2, status="connected")
        db = get_db()
        db.execute("UPDATE outreaches SET invited_at = ? WHERE id = ?", (eight_days_ago, o2))
        db.commit()
        db.close()

        stats = get_campaign_stats(camp_id)
        # Both count as connected, both in denominator → 2/2 = 100%
        assert abs(stats["acceptance_rate"] - 1.0) < 0.01
        # opted_out counts as replied
        assert stats["replied"] == 1


# ── Test Class 2: Engagement Campaign ID ──


class TestSaveEngagementCampaignId:
    """Tests for save_engagement() with campaign_id and get_engagement_stats()."""

    def test_campaign_id_stored(self):
        camp_id, _, out_id = _setup_campaign_and_outreach(status="invited")
        eng_id = save_engagement(
            outreach_id=out_id,
            action_type="comment",
            post_id="p-1",
            text="Great post!",
            campaign_id=camp_id,
        )
        # Verify it's in the DB
        db = get_db()
        row = db.execute(
            "SELECT campaign_id FROM engagements WHERE id = ?", (eng_id,)
        ).fetchone()
        db.close()
        assert row is not None
        assert row["campaign_id"] == camp_id

    def test_engagement_stats_via_outreach_join(self):
        camp_id, _, out_id = _setup_campaign_and_outreach(status="invited")
        save_engagement(
            outreach_id=out_id,
            action_type="comment",
            post_id="p-1",
            text="Nice!",
            # No campaign_id — should still be found via outreach JOIN
        )
        stats = get_engagement_stats(camp_id)
        assert stats["comments"] >= 1
        assert stats["total"] >= 1

    def test_engagement_stats_via_direct_campaign_id(self):
        # Campaign A has the outreach
        camp_a, _, out_a = _setup_campaign_and_outreach(status="invited")
        # Campaign B is the one we want the engagement counted for
        camp_b = create_campaign(name="Target Campaign", status="active")

        # Engagement belongs to outreach in campaign A, but direct campaign_id
        # points to campaign B — should appear in campaign B's stats
        save_engagement(
            outreach_id=out_a,
            action_type="react",
            post_id="p-2",
            campaign_id=camp_b,
        )
        stats = get_engagement_stats(camp_b)
        assert stats["reactions"] >= 1


# ── Test Class 3: Monthly Usage ──


class TestSetMonthlyUsage:
    """Tests for set_monthly_usage() — backend sync overwrites local counters."""

    def test_overwrites_counters(self):
        set_monthly_usage({
            "invitations_sent": 5,
            "messages_sent": 3,
            "engagements_sent": 2,
        })
        usage = get_monthly_usage()
        assert usage["invitations_sent"] == 5
        assert usage["messages_sent"] == 3
        assert usage["engagements_sent"] == 2

    def test_partial_update_preserves_other_fields(self):
        # First set invitations
        increment_usage("invitations_sent")
        assert get_monthly_usage()["invitations_sent"] == 1

        # Now sync only messages from backend — invitations should survive
        set_monthly_usage({"messages_sent": 10})
        usage = get_monthly_usage()
        assert usage["invitations_sent"] == 1  # NOT zeroed
        assert usage["messages_sent"] == 10


# ── Test Class 4: Update Outreach Event Timestamps ──


class TestOutreachTimestamps:
    """Tests for update_outreach() auto-setting invited_at/accepted_at/first_reply_at."""

    def test_invited_at_set_on_first_invite(self):
        camp_id, _, out_id = _setup_campaign_and_outreach(status="pending")
        before = int(time.time())
        update_outreach(out_id, status="invited")
        db = get_db()
        row = db.execute(
            "SELECT invited_at FROM outreaches WHERE id = ?", (out_id,)
        ).fetchone()
        db.close()
        assert row["invited_at"] is not None
        assert row["invited_at"] >= before

    def test_accepted_at_set_on_connected(self):
        camp_id, _, out_id = _setup_campaign_and_outreach(status="invited")
        update_outreach(out_id, status="connected")
        db = get_db()
        row = db.execute(
            "SELECT accepted_at FROM outreaches WHERE id = ?", (out_id,)
        ).fetchone()
        db.close()
        assert row["accepted_at"] is not None

    def test_first_reply_at_set_on_replied(self):
        camp_id, _, out_id = _setup_campaign_and_outreach(status="connected")
        update_outreach(out_id, status="replied")
        db = get_db()
        row = db.execute(
            "SELECT first_reply_at FROM outreaches WHERE id = ?", (out_id,)
        ).fetchone()
        db.close()
        assert row["first_reply_at"] is not None

    def test_full_lifecycle_timestamps(self):
        camp_id, _, out_id = _setup_campaign_and_outreach(status="pending")
        update_outreach(out_id, status="invited")
        update_outreach(out_id, status="connected")
        update_outreach(out_id, status="replied")
        db = get_db()
        row = db.execute(
            "SELECT invited_at, accepted_at, first_reply_at FROM outreaches WHERE id = ?",
            (out_id,),
        ).fetchone()
        db.close()
        assert row["invited_at"] is not None
        assert row["accepted_at"] is not None
        assert row["first_reply_at"] is not None
        assert row["invited_at"] <= row["accepted_at"]
        assert row["accepted_at"] <= row["first_reply_at"]


# ── Test Class 5: React Engagement E2E ──


class TestReactEngagementE2E:
    """E2E tests for the reaction (LIKE) engagement path."""

    @pytest.mark.asyncio
    async def test_react_saves_engagement_to_db(self):
        """Successful reaction saves engagement record with correct fields."""
        from heylead.tools.engage_prospect import _handle_reaction

        camp_id, _, out_id = await run_db(_setup_campaign_and_outreach, status="pending")

        mock_client = AsyncMock()
        mock_client.send_post_reaction.return_value = {"success": True}

        candidate = {"name": "Jane Doe", "outreach_id": out_id}
        target_post = {"id": "post-123", "text": "Short post about AI in sales"}

        result = await _handle_reaction(
            mock_client, "acct-1", out_id, candidate, target_post,
            mode="autopilot", campaign_id=camp_id,
        )

        assert "Liked" in result
        mock_client.send_post_reaction.assert_called_once_with(
            "acct-1", "post-123", "LIKE",
            outreach_id=out_id,
            post_text="Short post about AI in sales",
        )

        # Verify DB record
        def _check(oid, cid):
            db = get_db()
            row = db.execute(
                "SELECT * FROM engagements WHERE outreach_id = ? AND action_type = 'react'",
                (oid,),
            ).fetchone()
            db.close()
            return row

        row = await run_db(_check, out_id, camp_id)
        assert row is not None
        assert row["reaction_type"] == "LIKE"
        assert row["post_id"] == "post-123"
        assert row["status"] == "sent"
        assert row["campaign_id"] == camp_id

    @pytest.mark.asyncio
    async def test_react_failure_does_not_save(self):
        """Failed reaction does NOT save engagement record."""
        from heylead.tools.engage_prospect import _handle_reaction

        camp_id, _, out_id = await run_db(_setup_campaign_and_outreach, status="pending")

        mock_client = AsyncMock()
        mock_client.send_post_reaction.return_value = {"success": False, "error": "Rate limited"}

        candidate = {"name": "Jane Doe", "outreach_id": out_id}
        target_post = {"id": "post-456", "text": "Some post"}

        result = await _handle_reaction(
            mock_client, "acct-1", out_id, candidate, target_post,
            mode="autopilot", campaign_id=camp_id,
        )

        assert "failed" in result.lower()

        def _check(oid):
            db = get_db()
            row = db.execute(
                "SELECT * FROM engagements WHERE outreach_id = ? AND action_type = 'react'",
                (oid,),
            ).fetchone()
            db.close()
            return row

        row = await run_db(_check, out_id)
        assert row is None

    @pytest.mark.asyncio
    async def test_react_copilot_sends_in_autopilot(self):
        """Copilot mode removed — reaction is always sent (autopilot)."""
        from heylead.tools.engage_prospect import _handle_reaction

        camp_id, _, out_id = await run_db(_setup_campaign_and_outreach, status="pending")

        mock_client = AsyncMock()
        mock_client.send_post_reaction.return_value = {"success": True}

        candidate = {"name": "Jane Doe", "outreach_id": out_id}
        target_post = {"id": "post-789", "text": "A thought-provoking post"}

        result = await _handle_reaction(
            mock_client, "acct-1", out_id, candidate, target_post,
            mode="copilot", campaign_id=camp_id,
        )

        assert "liked" in result.lower()
        mock_client.send_post_reaction.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_react_auto_react_only(self):
        """engagement_mode='react_only' always returns True."""
        from heylead.tools.engage_prospect import _should_react_auto

        # Even with long text and zero prior engagements → True
        assert await _should_react_auto("out-x", "A" * 100, "react_only") is True

    @pytest.mark.asyncio
    async def test_should_react_auto_comment_only(self):
        """engagement_mode='comment_only' always returns False."""
        from heylead.tools.engage_prospect import _should_react_auto

        # Even with short text → False
        assert await _should_react_auto("out-x", "Hi", "comment_only") is False

    @pytest.mark.asyncio
    async def test_should_react_auto_short_text(self):
        """Auto mode: short text (<50 chars) returns True."""
        from heylead.tools.engage_prospect import _should_react_auto

        assert await _should_react_auto("out-x", "Short", "auto") is True

    @pytest.mark.asyncio
    async def test_should_react_auto_first_engagement_uses_probability(self):
        """Auto mode: first engagement uses 50/50 probability (no longer forced comment)."""
        from heylead.tools.engage_prospect import _should_react_auto

        camp_id, _, out_id = await run_db(_setup_campaign_and_outreach, status="pending")
        # With 50% probability, run multiple times and expect a mix
        results = [await _should_react_auto(out_id, "A" * 100, "auto") for _ in range(50)]
        assert any(results), "Expected at least one react in 50 trials"
        assert not all(results), "Expected at least one comment in 50 trials"

    def test_react_shows_in_engagement_stats(self):
        """Reaction engagement shows up in get_engagement_stats()."""
        camp_id, _, out_id = _setup_campaign_and_outreach(status="pending")

        save_engagement(
            outreach_id=out_id,
            action_type="react",
            post_id="p-react-1",
            reaction_type="LIKE",
            status="sent",
            campaign_id=camp_id,
        )

        stats = get_engagement_stats(camp_id)
        assert stats["reactions"] >= 1
        assert stats["total"] >= 1
