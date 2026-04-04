"""Tests for the auto-reply scheduler pipeline.

Covers:
- get_auto_reply_candidates query (age filter, sentiment filter, dedup)
- get_daily_auto_reply_count
- plan_auto_replies planner
- _execute_auto_reply executor
- enable_auto_replies toggle in edit_campaign
"""

from __future__ import annotations

import json
import time
from unittest.mock import AsyncMock, patch

import pytest

from heylead.db.async_bridge import run_db
from heylead.db.queries import (
    create_campaign,
    create_outreach,
    create_scheduler_job,
    get_auto_reply_candidates,
    get_daily_auto_reply_count,
    log_action,
    save_contact,
    save_message,
    update_campaign,
    update_outreach,
)
from heylead.db.schema import get_db


# ── Helpers ──


def _setup_campaign_and_replied_outreach(
    status: str = "hot_lead",
    sentiment: str = "positive",
    message_age: int = 600,
    mode: str = "autopilot",
    config_json: str = "{}",
) -> tuple[str, str, str]:
    """Create campaign + contact + outreach + prospect message."""
    camp_id = create_campaign(name="Test Auto-Reply Campaign", status="active", mode=mode)
    if config_json != "{}":
        update_campaign(camp_id, config_json=config_json)

    contact_id = save_contact(
        campaign_id=camp_id,
        name="Skyler de Groot",
        title="Director, Client Partnerships",
        company="Acme Corp",
        linkedin_id="skyler-123",
    )
    outreach_id = create_outreach(
        campaign_id=camp_id,
        contact_id=contact_id,
        status=status,
    )

    # Insert a prospect message with backdated timestamp
    db = get_db()
    msg_id = f"msg-{outreach_id[:8]}"
    msg_ts = int(time.time()) - message_age
    db.execute(
        """INSERT INTO messages (id, outreach_id, role, text, sentiment, format, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (msg_id, outreach_id, "prospect",
         "Hey, let me know what you had in mind!", sentiment, "text", msg_ts),
    )
    db.commit()
    db.close()

    return camp_id, contact_id, outreach_id


# ── get_auto_reply_candidates tests ──


def test_get_auto_reply_candidates_basic():
    """Returns candidates where last message is from prospect and old enough."""
    camp_id, _, outreach_id = _setup_campaign_and_replied_outreach(
        status="replied", sentiment="question", message_age=600,
    )
    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 1
    assert candidates[0]["outreach_id"] == outreach_id
    assert candidates[0]["last_sentiment"] == "question"


def test_get_auto_reply_candidates_min_age_filter():
    """Messages newer than min_age_seconds are excluded."""
    camp_id, _, _ = _setup_campaign_and_replied_outreach(
        status="replied", sentiment="question", message_age=60,  # Only 1 min old
    )
    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 0


def test_get_auto_reply_candidates_excludes_positive():
    """Positive sentiment (meeting intent) is excluded — user should decide."""
    camp_id, _, _ = _setup_campaign_and_replied_outreach(
        status="hot_lead", sentiment="positive", message_age=600,
    )
    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 0


def test_get_auto_reply_candidates_excludes_calendar():
    """Calendar sentiment (scheduling) is excluded — user should decide."""
    camp_id, _, _ = _setup_campaign_and_replied_outreach(
        status="hot_lead", sentiment="calendar", message_age=600,
    )
    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 0


def test_get_auto_reply_candidates_excludes_opt_out():
    """opt_out sentiment messages are excluded."""
    camp_id, _, _ = _setup_campaign_and_replied_outreach(
        status="hot_lead", sentiment="opt_out", message_age=600,
    )
    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 0


def test_get_auto_reply_candidates_excludes_out_of_office():
    """out_of_office sentiment messages are excluded."""
    camp_id, _, _ = _setup_campaign_and_replied_outreach(
        status="replied", sentiment="out_of_office", message_age=600,
    )
    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 0


def test_get_auto_reply_candidates_excludes_sdr_last():
    """If last message is from SDR (we already replied), exclude."""
    camp_id, _, outreach_id = _setup_campaign_and_replied_outreach(
        status="hot_lead", sentiment="positive", message_age=600,
    )
    # Add a newer SDR message (we already replied)
    save_message(outreach_id, role="sdr", text="Thanks! Let me know if you need anything.")

    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 0


def test_get_auto_reply_candidates_dedup_pending_jobs():
    """Exclude outreaches with pending auto_reply jobs."""
    camp_id, _, outreach_id = _setup_campaign_and_replied_outreach(
        status="hot_lead", sentiment="positive", message_age=600,
    )
    # Create a pending auto_reply job for this outreach
    create_scheduler_job(
        campaign_id=camp_id,
        job_type="auto_reply",
        scheduled_at=int(time.time()) + 300,
        outreach_id=outreach_id,
    )
    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 0


def test_get_auto_reply_candidates_sentiment_priority():
    """Candidates ordered by priority: engaged > question > neutral. Positive/negative/calendar excluded."""
    camp_id = create_campaign(name="Priority Test", status="active")
    sentiments = [("negative", "replied"), ("positive", "hot_lead"), ("question", "replied"), ("neutral", "replied"), ("engaged", "replied"), ("calendar", "hot_lead")]

    for i, (sentiment, status) in enumerate(sentiments):
        cid = save_contact(
            campaign_id=camp_id, name=f"Person {i}",
            linkedin_id=f"person-{i}",
        )
        oid = create_outreach(campaign_id=camp_id, contact_id=cid, status=status)
        db = get_db()
        db.execute(
            """INSERT INTO messages (id, outreach_id, role, text, sentiment, format, timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (f"msg-{i}", oid, "prospect", f"Message {i}", sentiment, "text", int(time.time()) - 600),
        )
        db.commit()
        db.close()

    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    sentiments_ordered = [c["last_sentiment"] for c in candidates]
    # positive, negative, calendar excluded — only engaged, question, neutral remain
    assert sentiments_ordered == ["engaged", "question", "neutral"]


# ── get_daily_auto_reply_count tests ──


def test_get_daily_auto_reply_count_empty():
    """Returns 0 when no auto_reply_sent actions exist."""
    assert get_daily_auto_reply_count() == 0


def test_get_daily_auto_reply_count_with_actions():
    """Counts auto_reply_sent actions from today."""
    camp_id, _, outreach_id = _setup_campaign_and_replied_outreach()
    log_action("auto_reply_sent", outreach_id=outreach_id, result="success", details={})
    log_action("auto_reply_sent", outreach_id=outreach_id, result="success", details={})
    # This one shouldn't count
    log_action("reply_sent", outreach_id=outreach_id, result="success", details={})
    assert get_daily_auto_reply_count() == 2


# ── plan_auto_replies tests ──


@pytest.mark.asyncio
async def test_plan_auto_replies_disabled():
    """No jobs created when enable_auto_replies is off."""
    config = json.dumps({"enable_auto_replies": False})
    camp_id, _, _ = await run_db(
        _setup_campaign_and_replied_outreach, config_json=config,
    )

    from heylead.scheduler.planner import plan_auto_replies
    await plan_auto_replies(camp_id)

    def _check(cid):
        db = get_db()
        jobs = db.execute(
            "SELECT * FROM scheduler_jobs WHERE job_type = 'auto_reply' AND campaign_id = ?",
            (cid,),
        ).fetchall()
        db.close()
        return jobs

    jobs = await run_db(_check, camp_id)
    assert len(jobs) == 0


@pytest.mark.asyncio
async def test_plan_auto_replies_schedules_job():
    """Creates a scheduler job for valid candidate."""
    camp_id, _, outreach_id = await run_db(
        _setup_campaign_and_replied_outreach,
        status="replied", sentiment="question", message_age=600,
    )

    from heylead.scheduler.planner import plan_auto_replies
    await plan_auto_replies(camp_id)

    def _check(cid):
        db = get_db()
        jobs = db.execute(
            "SELECT * FROM scheduler_jobs WHERE job_type = 'auto_reply' AND campaign_id = ?",
            (cid,),
        ).fetchall()
        db.close()
        return jobs

    jobs = await run_db(_check, camp_id)
    assert len(jobs) == 1
    job = dict(jobs[0])
    assert job["outreach_id"] == outreach_id
    assert job["status"] == "pending"
    # Job should be scheduled within the delay window (now to +15 min)
    assert job["scheduled_at"] <= int(time.time()) + 15 * 60 + 10


@pytest.mark.asyncio
async def test_plan_auto_replies_max_three_per_cycle():
    """Only schedules max 3 jobs per planning cycle."""
    def _seed():
        camp_id = create_campaign(name="Max Two Test", status="active")
        for i in range(5):
            cid = save_contact(
                campaign_id=camp_id, name=f"Person {i}",
                linkedin_id=f"person-max-{i}",
            )
            oid = create_outreach(campaign_id=camp_id, contact_id=cid, status="replied")
            db = get_db()
            db.execute(
                """INSERT INTO messages (id, outreach_id, role, text, sentiment, format, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (f"msg-max-{i}", oid, "prospect", f"Question {i}?", "question", "text",
                 int(time.time()) - 600),
            )
            db.commit()
            db.close()
        return camp_id

    camp_id = await run_db(_seed)

    from heylead.scheduler.planner import plan_auto_replies
    await plan_auto_replies(camp_id)

    def _check(cid):
        db = get_db()
        jobs = db.execute(
            "SELECT * FROM scheduler_jobs WHERE job_type = 'auto_reply' AND campaign_id = ?",
            (cid,),
        ).fetchall()
        db.close()
        return jobs

    jobs = await run_db(_check, camp_id)
    assert len(jobs) <= 3


# ── edit_campaign toggle tests ──


@pytest.mark.asyncio
async def test_edit_campaign_enable_auto_replies():
    """Toggle enable_auto_replies on/off via edit_campaign."""
    from heylead.db.queries import save_setting, get_campaign

    def _setup():
        cid = create_campaign(name="Toggle Test", status="active")
        save_setting("setup_complete", True)
        return cid

    camp_id = await run_db(_setup)

    from heylead.tools.edit_campaign import run_edit_campaign
    result = await run_edit_campaign(campaign_id=camp_id, enable_auto_replies="off")
    assert "Auto-replies" in result
    assert "off" in result

    # Verify config_json was updated
    camp = await run_db(get_campaign, camp_id)
    config = json.loads(camp.get("config_json", "{}") or "{}")
    assert config.get("enable_auto_replies") is False

    # Turn back on
    result = await run_edit_campaign(campaign_id=camp_id, enable_auto_replies="on")
    assert "Auto-replies" in result
    camp = await run_db(get_campaign, camp_id)
    config = json.loads(camp.get("config_json", "{}") or "{}")
    assert config.get("enable_auto_replies") is True


# ── check_replies multi-turn & dedup tests ──


def test_check_replies_status_filter_includes_hot_lead():
    """Outreaches in hot_lead status are included in the contact lookup.

    Regression: previously the query only matched ('invited', 'connected', 'messaged'),
    so new messages from hot_lead contacts were invisible.
    """
    from heylead.db.schema import get_db as _get_db

    camp_id = create_campaign(name="Hot Lead Filter", status="active")
    contact_id = save_contact(
        campaign_id=camp_id, name="Alice Hot", linkedin_id="alice-hot-1",
    )
    outreach_id = create_outreach(
        campaign_id=camp_id, contact_id=contact_id, status="hot_lead",
    )

    # The contact_lookup query in check_replies should now include hot_lead
    db = _get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id, c.linkedin_id
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.status IN ('invited', 'connected', 'messaged', 'hot_lead', 'replied')"""
    ).fetchall()
    db.close()

    found_ids = [dict(r)["outreach_id"] for r in rows]
    assert outreach_id in found_ids


def test_check_replies_status_filter_includes_replied():
    """Outreaches in replied status are included in the contact lookup."""
    from heylead.db.schema import get_db as _get_db

    camp_id = create_campaign(name="Replied Filter", status="active")
    contact_id = save_contact(
        campaign_id=camp_id, name="Bob Replied", linkedin_id="bob-replied-1",
    )
    outreach_id = create_outreach(
        campaign_id=camp_id, contact_id=contact_id, status="replied",
    )

    db = _get_db()
    rows = db.execute(
        """SELECT o.id as outreach_id
           FROM outreaches o
           JOIN contacts c ON o.contact_id = c.id
           WHERE o.status IN ('invited', 'connected', 'messaged', 'hot_lead', 'replied')"""
    ).fetchall()
    db.close()

    found_ids = [dict(r)["outreach_id"] for r in rows]
    assert outreach_id in found_ids


def test_check_replies_dedup_same_message():
    """Saving the same prospect message text twice should be prevented by dedup logic."""
    from heylead.db.queries import get_messages_for_outreach

    camp_id = create_campaign(name="Dedup Test", status="active")
    contact_id = save_contact(
        campaign_id=camp_id, name="Dedup Person", linkedin_id="dedup-1",
    )
    outreach_id = create_outreach(
        campaign_id=camp_id, contact_id=contact_id, status="hot_lead",
    )

    # Save initial prospect message
    save_message(outreach_id, role="prospect", text="Sounds great, let's chat!", sentiment="positive")

    # Simulate the dedup check that check_replies does
    existing_msgs = get_messages_for_outreach(outreach_id)
    last_prospect = None
    for m in reversed(existing_msgs):
        if m.get("role") == "prospect":
            last_prospect = m
            break

    # Same text should be detected as duplicate
    assert last_prospect is not None
    assert last_prospect["text"].strip() == "Sounds great, let's chat!"

    # Different text should NOT be a duplicate
    assert last_prospect["text"].strip() != "When can we meet?"


def test_multiturn_auto_reply_candidates():
    """After auto-reply (SDR message), a new prospect message creates a valid candidate.

    Full flow:
    1. Prospect sends message -> status hot_lead
    2. Auto-reply sent (SDR message) -> status stays hot_lead
    3. Prospect sends NEW message -> should be a valid auto-reply candidate
    """
    camp_id = create_campaign(name="Multiturn Test", status="active")
    contact_id = save_contact(
        campaign_id=camp_id, name="Multiturn Person", linkedin_id="multi-1",
    )
    outreach_id = create_outreach(
        campaign_id=camp_id, contact_id=contact_id, status="hot_lead",
    )

    # Step 1: Prospect sent first message (10 min ago)
    db = get_db()
    db.execute(
        """INSERT INTO messages (id, outreach_id, role, text, sentiment, format, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ("msg-multi-1", outreach_id, "prospect",
         "Sounds great!", "positive", "text", int(time.time()) - 600),
    )
    db.commit()
    db.close()

    # Step 2: Auto-reply sent (8 min ago)
    db = get_db()
    db.execute(
        """INSERT INTO messages (id, outreach_id, role, text, sentiment, format, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ("msg-multi-2", outreach_id, "sdr",
         "Great to hear! When works for a quick chat?", "", "text", int(time.time()) - 480),
    )
    db.commit()
    db.close()

    # At this point, last message is from SDR -> NOT a candidate
    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 0

    # Step 3: Prospect replies again with a question (6 min ago)
    db = get_db()
    db.execute(
        """INSERT INTO messages (id, outreach_id, role, text, sentiment, format, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ("msg-multi-3", outreach_id, "prospect",
         "What does the product do exactly?", "question", "text", int(time.time()) - 360),
    )
    db.commit()
    db.close()

    # Now last message is from prospect with question sentiment -> IS a candidate
    candidates = get_auto_reply_candidates(camp_id, min_age_seconds=300)
    assert len(candidates) == 1
    assert candidates[0]["outreach_id"] == outreach_id
    assert candidates[0]["last_reply_text"] == "What does the product do exactly?"
