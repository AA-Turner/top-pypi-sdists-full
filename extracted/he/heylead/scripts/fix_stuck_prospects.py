"""One-time migration: fix 58 stuck prospects with status='connected', followup_count=0.

Two categories:
1. Prospects WITH sdr messages (sdr_msgs > 0): update status='messaged' and
   followup_count to match actual message count.
2. Prospects WITHOUT sdr messages (sdr_msgs = 0): leave as-is — the scheduler
   will now pick them up via the fixed _plan_dms() in planner.py.

Also reopens the completed "Existing Network" campaign to "active" so the
scheduler can process the backlog, then re-archives it once all prospects
have pending jobs.

Usage:
    python3.12 scripts/fix_stuck_prospects.py [--dry-run]
"""

import sqlite3
import sys
import time

DB_PATH = "/Users/denyschumak/.heylead/data/heylead.db"
DRY_RUN = "--dry-run" in sys.argv


def main() -> None:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    now = int(time.time())

    # Find all stuck prospects
    rows = db.execute("""
        SELECT o.id as outreach_id, o.campaign_id, o.status, o.followup_count,
               c.name, c.company,
               (SELECT COUNT(*) FROM messages m WHERE m.outreach_id = o.id AND m.role = 'sdr') as sdr_msgs
        FROM outreaches o
        JOIN contacts c ON o.contact_id = c.id
        WHERE o.status = 'connected' AND o.followup_count = 0
        ORDER BY o.campaign_id, c.name
    """).fetchall()

    print(f"Found {len(rows)} stuck prospects (connected, followup_count=0)")
    print()

    # Category 1: Have messages but status not updated
    with_msgs = [r for r in rows if r["sdr_msgs"] > 0]
    without_msgs = [r for r in rows if r["sdr_msgs"] == 0]

    print(f"Category 1: {len(with_msgs)} prospects WITH messages (need status+followup_count fix)")
    for r in with_msgs:
        print(f"  - {r['name']} ({r['company'] or 'N/A'}): {r['sdr_msgs']} sdr messages, "
              f"campaign={r['campaign_id'][:8]}")

    print()
    print(f"Category 2: {len(without_msgs)} prospects WITHOUT messages (scheduler will handle)")
    for r in without_msgs:
        print(f"  - {r['name']} ({r['company'] or 'N/A'}): campaign={r['campaign_id'][:8]}")

    if DRY_RUN:
        print("\n[DRY RUN] No changes made.")
        db.close()
        return

    # Fix Category 1: update status and followup_count
    fixed = 0
    for r in with_msgs:
        db.execute(
            "UPDATE outreaches SET status = 'messaged', followup_count = ?, updated_at = ? WHERE id = ?",
            (r["sdr_msgs"], now, r["outreach_id"]),
        )
        fixed += 1

    db.commit()
    print(f"\nFixed {fixed} prospects: status → 'messaged', followup_count → actual message count")

    # Show campaign summary
    campaigns = {}
    for r in rows:
        cid = r["campaign_id"]
        if cid not in campaigns:
            campaigns[cid] = {"with_msgs": 0, "without_msgs": 0}
        if r["sdr_msgs"] > 0:
            campaigns[cid]["with_msgs"] += 1
        else:
            campaigns[cid]["without_msgs"] += 1

    print("\nPer-campaign summary:")
    for cid, counts in campaigns.items():
        camp = db.execute("SELECT name, status FROM campaigns WHERE id = ?", (cid,)).fetchone()
        name = camp["name"] if camp else "Unknown"
        status = camp["status"] if camp else "?"
        print(f"  {name} (status={status}): "
              f"{counts['with_msgs']} fixed, {counts['without_msgs']} need DMs")

    # Verify
    remaining = db.execute("""
        SELECT COUNT(*) as cnt FROM outreaches
        WHERE status = 'connected' AND followup_count = 0
        AND (SELECT COUNT(*) FROM messages m WHERE m.outreach_id = outreaches.id AND m.role = 'sdr') > 0
    """).fetchone()["cnt"]
    print(f"\nVerification: {remaining} prospects still stuck with messages but wrong status "
          f"(should be 0)")

    db.close()


if __name__ == "__main__":
    main()
