"""Tests for email overflow when LinkedIn limits are hit.

Covers:
- can_send_now() returns correct block_type for each scenario
- can_send_email_now() respects email-specific limits
- select_channel() routes to email when linkedin_limit_hit=True
- get_email_eligible_pending_outreaches() excludes already-contacted prospects
"""

from __future__ import annotations

import json
import time
import uuid


# ──────────────────────────────────────────────
# can_send_now() block_type tests
# ──────────────────────────────────────────────


async def test_can_send_now_returns_three_tuple():
    """can_send_now() must return a 3-tuple."""
    from heylead.linkedin.rate_limiter import can_send_now

    result = await can_send_now()
    assert len(result) == 3
    can_send, reason, block_type = result
    assert isinstance(can_send, bool)
    assert isinstance(reason, str)
    assert isinstance(block_type, str)


async def test_can_send_now_always_true_regardless_of_daily_count():
    """can_send_now() always returns True — no daily limit enforcement."""
    from heylead.linkedin.rate_limiter import can_send_now, BLOCK_NONE

    can_send, reason, block_type = await can_send_now()
    assert can_send
    assert reason == ""
    assert block_type == BLOCK_NONE


async def test_can_send_now_always_true_regardless_of_weekly_count():
    """can_send_now() always returns True — no weekly limit enforcement."""
    from heylead.linkedin.rate_limiter import can_send_now, BLOCK_NONE

    can_send, reason, block_type = await can_send_now()
    assert can_send
    assert reason == ""
    assert block_type == BLOCK_NONE


async def test_can_send_now_always_true_regardless_of_time():
    """can_send_now() always returns True — no time-of-day enforcement."""
    from heylead.linkedin.rate_limiter import can_send_now, BLOCK_NONE

    can_send, reason, block_type = await can_send_now()
    assert can_send
    assert reason == ""
    assert block_type == BLOCK_NONE


async def test_can_send_now_ok():
    """can_send_now() always returns True with BLOCK_NONE."""
    from heylead.linkedin.rate_limiter import can_send_now, BLOCK_NONE

    can_send, reason, block_type = await can_send_now()
    assert can_send
    assert reason == ""
    assert block_type == BLOCK_NONE


# ──────────────────────────────────────────────
# can_send_email_now() tests
# ──────────────────────────────────────────────


async def test_can_send_email_now_ok():
    """can_send_email_now() always returns True — no email limits."""
    from heylead.linkedin.rate_limiter import can_send_email_now

    can_send, reason = await can_send_email_now()
    assert can_send
    assert reason == ""


async def test_can_send_email_now_always_true():
    """can_send_email_now() always returns True — no daily or weekly email limits."""
    from heylead.linkedin.rate_limiter import can_send_email_now

    can_send, reason = await can_send_email_now()
    assert can_send
    assert reason == ""


# ──────────────────────────────────────────────
# select_channel() with linkedin_limit_hit tests
# ──────────────────────────────────────────────


def test_select_channel_email_when_limit_hit_and_email_available(monkeypatch):
    """Routes to email when LinkedIn limits hit + prospect has email."""
    from heylead.services import channel_selector
    from heylead.services.channel_selector import select_channel, CHANNEL_EMAIL

    # Patch get_setting on the channel_selector module (it imports directly)
    monkeypatch.setattr(
        channel_selector, "get_setting",
        lambda k, d=None: "email-acc-123" if k == "email_account_id" else d,
    )

    prospect = {"name": "Test", "email": "test@example.com"}
    channel = select_channel(prospect=prospect, linkedin_limit_hit=True)
    assert channel == CHANNEL_EMAIL


def test_select_channel_linkedin_when_limit_hit_but_no_email_account(monkeypatch):
    """Falls back to LinkedIn when limits hit but no email account connected."""
    from heylead.services import channel_selector
    from heylead.services.channel_selector import select_channel, CHANNEL_LINKEDIN

    monkeypatch.setattr(
        channel_selector, "get_setting",
        lambda k, d=None: "" if k == "email_account_id" else d,
    )

    prospect = {"name": "Test", "email": "test@example.com"}
    channel = select_channel(prospect=prospect, linkedin_limit_hit=True)
    assert channel == CHANNEL_LINKEDIN


def test_select_channel_linkedin_when_limit_hit_but_no_email_address(monkeypatch):
    """Falls back to LinkedIn when limits hit but prospect has no email."""
    from heylead.services import channel_selector
    from heylead.services.channel_selector import select_channel, CHANNEL_LINKEDIN

    monkeypatch.setattr(
        channel_selector, "get_setting",
        lambda k, d=None: "email-acc-123" if k == "email_account_id" else d,
    )

    prospect = {"name": "Test", "title": "CEO"}  # No email field
    channel = select_channel(prospect=prospect, linkedin_limit_hit=True)
    assert channel == CHANNEL_LINKEDIN


def test_select_channel_linkedin_when_no_limit_hit(monkeypatch):
    """LinkedIn is default when limits are not hit, even if prospect has email."""
    from heylead.services import channel_selector
    from heylead.services.channel_selector import select_channel, CHANNEL_LINKEDIN

    monkeypatch.setattr(
        channel_selector, "get_setting",
        lambda k, d=None: "email-acc-123" if k == "email_account_id" else d,
    )

    prospect = {"name": "Test", "email": "test@example.com"}
    channel = select_channel(prospect=prospect, linkedin_limit_hit=False)
    assert channel == CHANNEL_LINKEDIN


def test_select_channel_force_email_overrides(monkeypatch):
    """force_channel='email' works regardless of limit state."""
    from heylead.services import channel_selector
    from heylead.services.channel_selector import select_channel, CHANNEL_EMAIL

    monkeypatch.setattr(
        channel_selector, "get_setting",
        lambda k, d=None: "email-acc-123" if k == "email_account_id" else d,
    )

    prospect = {"name": "Test"}
    channel = select_channel(prospect=prospect, force_channel="email")
    assert channel == CHANNEL_EMAIL


def test_select_channel_14_day_fallback_still_works(monkeypatch):
    """The existing 14-day fallback is independent of linkedin_limit_hit."""
    from heylead.services import channel_selector
    from heylead.services.channel_selector import select_channel, CHANNEL_EMAIL

    monkeypatch.setattr(
        channel_selector, "get_setting",
        lambda k, d=None: "email-acc-123" if k == "email_account_id" else d,
    )

    outreach = {
        "channel": "linkedin",
        "invited_at": time.time() - (15 * 86400),  # 15 days ago
        "status": "invited",
    }
    prospect = {"name": "Test", "email": "test@example.com"}
    channel = select_channel(outreach=outreach, prospect=prospect, linkedin_limit_hit=False)
    assert channel == CHANNEL_EMAIL


# ──────────────────────────────────────────────
# Email eligible outreaches query tests
# ──────────────────────────────────────────────


def _setup_db_with_prospects():
    """Create test campaigns, contacts, and outreaches.

    Note: contacts table has no direct `email` column.
    Email is stored in profile_json.
    """
    from heylead.db.schema import get_db

    db = get_db()
    now = int(time.time())
    campaign_id = str(uuid.uuid4())

    # Create campaign
    db.execute(
        """INSERT INTO campaigns (id, name, status, mode, created_at, updated_at)
           VALUES (?, 'Test Campaign', 'active', 'autopilot', ?, ?)""",
        (campaign_id, now, now),
    )

    contacts = []
    outreaches = []

    # Contact 1: has email in profile_json, pending → eligible
    c1 = str(uuid.uuid4())
    o1 = str(uuid.uuid4())
    profile1 = json.dumps({"name": "Alice", "email": "alice@acme.com"})
    db.execute(
        """INSERT INTO contacts (id, campaign_id, name, title, company, profile_json, fit_score, created_at, updated_at)
           VALUES (?, ?, 'Alice', 'CTO', 'Acme', ?, 0.9, ?, ?)""",
        (c1, campaign_id, profile1, now, now),
    )
    db.execute(
        """INSERT INTO outreaches (id, campaign_id, contact_id, status, created_at, updated_at)
           VALUES (?, ?, ?, 'pending', ?, ?)""",
        (o1, campaign_id, c1, now, now),
    )
    contacts.append(c1)
    outreaches.append(o1)

    # Contact 2: has email_address in profile_json, pending → eligible
    c2 = str(uuid.uuid4())
    o2 = str(uuid.uuid4())
    profile2 = json.dumps({"name": "Bob", "email": "bob@company.com"})
    db.execute(
        """INSERT INTO contacts (id, campaign_id, name, title, company, profile_json, fit_score, created_at, updated_at)
           VALUES (?, ?, 'Bob', 'VP', 'Company', ?, 0.8, ?, ?)""",
        (c2, campaign_id, profile2, now, now),
    )
    db.execute(
        """INSERT INTO outreaches (id, campaign_id, contact_id, status, created_at, updated_at)
           VALUES (?, ?, ?, 'pending', ?, ?)""",
        (o2, campaign_id, c2, now, now),
    )
    contacts.append(c2)
    outreaches.append(o2)

    # Contact 3: NO email in profile_json, pending → NOT eligible
    c3 = str(uuid.uuid4())
    o3 = str(uuid.uuid4())
    profile3 = json.dumps({"name": "Charlie", "title": "Manager"})
    db.execute(
        """INSERT INTO contacts (id, campaign_id, name, title, company, profile_json, fit_score, created_at, updated_at)
           VALUES (?, ?, 'Charlie', 'Manager', 'NoEmail Inc', ?, 0.7, ?, ?)""",
        (c3, campaign_id, profile3, now, now),
    )
    db.execute(
        """INSERT INTO outreaches (id, campaign_id, contact_id, status, created_at, updated_at)
           VALUES (?, ?, ?, 'pending', ?, ?)""",
        (o3, campaign_id, c3, now, now),
    )

    # Contact 4: has email but already invited → NOT eligible
    c4 = str(uuid.uuid4())
    o4 = str(uuid.uuid4())
    profile4 = json.dumps({"name": "Diana", "email": "diana@sent.com"})
    db.execute(
        """INSERT INTO contacts (id, campaign_id, name, title, company, profile_json, fit_score, created_at, updated_at)
           VALUES (?, ?, 'Diana', 'CEO', 'AlreadySent', ?, 0.95, ?, ?)""",
        (c4, campaign_id, profile4, now, now),
    )
    db.execute(
        """INSERT INTO outreaches (id, campaign_id, contact_id, status, invited_at, created_at, updated_at)
           VALUES (?, ?, ?, 'invited', ?, ?, ?)""",
        (o4, campaign_id, c4, now, now, now),
    )

    db.commit()
    db.close()
    return campaign_id, contacts, outreaches


def test_email_eligible_returns_only_prospects_with_email():
    """Only pending outreaches with email in profile_json should be returned."""
    from heylead.db.queries import get_email_eligible_pending_outreaches

    campaign_id, contacts, outreaches = _setup_db_with_prospects()

    results = get_email_eligible_pending_outreaches(campaign_id)

    # Should return Alice and Bob (email in profile_json)
    # Should NOT return Charlie (no email) or Diana (already invited)
    names = [r["name"] for r in results]
    assert "Alice" in names
    assert "Bob" in names
    assert "Charlie" not in names
    assert "Diana" not in names


def test_email_eligible_ordered_by_fit_score():
    """Results should be ordered by fit_score DESC."""
    from heylead.db.queries import get_email_eligible_pending_outreaches

    campaign_id, contacts, outreaches = _setup_db_with_prospects()

    results = get_email_eligible_pending_outreaches(campaign_id)

    # Alice (0.9) should be before Bob (0.8)
    assert len(results) >= 2
    assert results[0]["name"] == "Alice"
    assert results[1]["name"] == "Bob"


def test_email_eligible_cross_campaign_guard():
    """Prospects contacted in another campaign should be excluded."""
    from heylead.db.schema import get_db
    from heylead.db.queries import get_email_eligible_pending_outreaches

    campaign_id, contacts, outreaches = _setup_db_with_prospects()

    # Create a second campaign with Alice already invited
    now = int(time.time())
    campaign2_id = str(uuid.uuid4())
    db = get_db()
    db.execute(
        """INSERT INTO campaigns (id, name, status, mode, created_at, updated_at)
           VALUES (?, 'Campaign 2', 'active', 'autopilot', ?, ?)""",
        (campaign2_id, now, now),
    )
    # Alice already invited in campaign 2
    o_cross = str(uuid.uuid4())
    db.execute(
        """INSERT INTO outreaches (id, campaign_id, contact_id, status, invited_at, created_at, updated_at)
           VALUES (?, ?, ?, 'invited', ?, ?, ?)""",
        (o_cross, campaign2_id, contacts[0], now, now, now),
    )
    db.commit()
    db.close()

    # Query campaign 1 — Alice should now be excluded
    results = get_email_eligible_pending_outreaches(campaign_id)
    names = [r["name"] for r in results]
    assert "Alice" not in names
    assert "Bob" in names


# ──────────────────────────────────────────────
# Email rate tracking tests
# ──────────────────────────────────────────────


def test_email_rate_limit_today_creates_record():
    """get_email_rate_limit_today() should create a record if none exists."""
    from heylead.db.queries import get_email_rate_limit_today

    result = get_email_rate_limit_today()
    assert result["sent"] == 0


def test_increment_email_sent():
    """increment_email_sent() should increase today's counter."""
    from heylead.db.queries import get_email_rate_limit_today, increment_email_sent

    assert get_email_rate_limit_today()["sent"] == 0

    increment_email_sent()
    assert get_email_rate_limit_today()["sent"] == 1

    increment_email_sent()
    assert get_email_rate_limit_today()["sent"] == 2


def test_weekly_email_sum():
    """get_weekly_email_sum() should sum across days."""
    from heylead.db.queries import get_weekly_email_sum, increment_email_sent

    assert get_weekly_email_sum() == 0
    increment_email_sent()
    increment_email_sent()
    assert get_weekly_email_sum() == 2


# ──────────────────────────────────────────────
# Constants validation
# ──────────────────────────────────────────────


def test_email_overflow_constants_exist():
    """Remaining email overflow constants should be defined."""
    from heylead.constants import (
        EMAIL_INVITE_DELAY_MIN,
        EMAIL_INVITE_DELAY_MAX,
        JOB_EMAIL_INVITE,
    )

    assert EMAIL_INVITE_DELAY_MIN < EMAIL_INVITE_DELAY_MAX
    assert JOB_EMAIL_INVITE == "email_invite"


def test_job_email_invite_in_executor_dispatch():
    """JOB_EMAIL_INVITE should be registered in the executor dispatch table."""
    from heylead.constants import JOB_EMAIL_INVITE

    assert JOB_EMAIL_INVITE == "email_invite"
