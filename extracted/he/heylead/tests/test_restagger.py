"""Tests for post-outage backlog re-stagger logic.

Covers:
- count_stale_ready_jobs() — detecting stale job backlog
- restagger_stale_jobs() — spreading stale jobs over time
- Priority ordering — core outreach gets earlier slots than warm-up
"""

from __future__ import annotations

import time

import pytest

from heylead.db.queries import (
    count_stale_ready_jobs,
    create_campaign,
    create_outreach,
    create_scheduler_job,
    get_ready_jobs,
    restagger_stale_jobs,
    save_contact,
)


# ── Helpers ──


def _make_jobs(n: int, job_type: str = "profile_view_warmup", age_seconds: int = 1800) -> str:
    """Create n stale scheduler jobs. Returns campaign_id."""
    camp_id = create_campaign(name="Test", status="active")
    now = int(time.time())
    for i in range(n):
        cid = save_contact(
            campaign_id=camp_id,
            name=f"Person {i}",
            title="VP",
            company="Co",
            linkedin_id=f"person-{i}",
        )
        oid = create_outreach(campaign_id=camp_id, contact_id=cid, status="pending")
        create_scheduler_job(
            campaign_id=camp_id,
            job_type=job_type,
            scheduled_at=now - age_seconds + i,  # stale by age_seconds
            outreach_id=oid,
        )
    return camp_id


# ── count_stale_ready_jobs ──


class TestCountStaleReadyJobs:
    def test_no_jobs(self):
        assert count_stale_ready_jobs(600) == 0

    def test_fresh_jobs_not_counted(self):
        """Jobs scheduled for the future or within threshold are not stale."""
        camp_id = create_campaign(name="Test", status="active")
        cid = save_contact(campaign_id=camp_id, name="A", title="T", company="C", linkedin_id="a1")
        oid = create_outreach(campaign_id=camp_id, contact_id=cid, status="pending")
        # Scheduled 5 min ago — within 10 min threshold
        create_scheduler_job(
            campaign_id=camp_id, job_type="invite", scheduled_at=int(time.time()) - 300, outreach_id=oid,
        )
        assert count_stale_ready_jobs(600) == 0

    def test_stale_jobs_counted(self):
        _make_jobs(30, age_seconds=1800)  # 30 min old
        assert count_stale_ready_jobs(600) == 30


# ── restagger_stale_jobs ──


class TestRestaggerStaleJobs:
    def test_no_stale_jobs_noop(self):
        assert restagger_stale_jobs(600, 30) == 0

    def test_stale_jobs_restaggered(self):
        _make_jobs(50, age_seconds=1800)
        now_before = int(time.time())

        restaggered = restagger_stale_jobs(600, 30)
        assert restaggered == 50

        # All jobs should now be scheduled in the future, spread 30s apart
        ready_now = get_ready_jobs(limit=100)
        # At most a couple might be ready right now (index 0 = now + 0)
        assert len(ready_now) <= 2

    def test_priority_ordering(self):
        """Core outreach jobs get earlier time slots than warm-up jobs."""
        camp_id = create_campaign(name="Test", status="active")
        now = int(time.time())

        # Create one warm-up job and one core job, both stale
        for job_type in ["profile_view_warmup", "invite"]:
            cid = save_contact(
                campaign_id=camp_id, name=f"P-{job_type}", title="T", company="C",
                linkedin_id=f"id-{job_type}",
            )
            oid = create_outreach(campaign_id=camp_id, contact_id=cid, status="pending")
            create_scheduler_job(
                campaign_id=camp_id, job_type=job_type,
                scheduled_at=now - 1800, outreach_id=oid,
            )

        restagger_stale_jobs(600, 60)

        # Invite (priority 1) should be ready before profile_view (priority 5)
        from heylead.db.schema import get_db
        db = get_db()
        rows = db.execute(
            "SELECT job_type, scheduled_at FROM scheduler_jobs WHERE status = 'pending' ORDER BY scheduled_at ASC"
        ).fetchall()
        db.close()
        types = [dict(r)["job_type"] for r in rows]
        assert types == ["invite", "profile_view_warmup"]

    def test_fresh_jobs_untouched(self):
        """Jobs within the staleness threshold are not re-staggered."""
        camp_id = create_campaign(name="Test", status="active")
        now = int(time.time())
        cid = save_contact(campaign_id=camp_id, name="Fresh", title="T", company="C", linkedin_id="fresh-1")
        oid = create_outreach(campaign_id=camp_id, contact_id=cid, status="pending")
        original_time = now - 300  # only 5 min old
        create_scheduler_job(
            campaign_id=camp_id, job_type="invite", scheduled_at=original_time, outreach_id=oid,
        )

        restagger_stale_jobs(600, 30)

        from heylead.db.schema import get_db
        db = get_db()
        row = db.execute("SELECT scheduled_at FROM scheduler_jobs WHERE status = 'pending'").fetchone()
        db.close()
        assert dict(row)["scheduled_at"] == original_time  # untouched
