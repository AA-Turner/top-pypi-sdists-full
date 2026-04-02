"""One-time script: Reactivate the 'Existing Network' campaign to process 34 stuck prospects.

These prospects are status='connected', followup_count=0, sdr_msgs=0 — they accepted
invitations but never received a DM because of BUG-1 (no initial DM scheduling for
invitation-based campaigns).

After the Sprint 1-4 fixes, reactivating the campaign will let the scheduler's
_plan_dms() and _rescue_orphans() handle them automatically.

Usage:
    python3.12 scripts/reactivate_existing_network.py [--dry-run]
"""

import sqlite3
import sys
import time

DB_PATH = "/Users/denyschumak/.heylead/data/heylead.db"
CAMPAIGN_ID = "6cc658fb"  # prefix match


def main():
    dry_run = "--dry-run" in sys.argv
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row

    # Find full campaign ID
    row = db.execute(
        "SELECT id, name, status FROM campaigns WHERE id LIKE ?",
        (f"{CAMPAIGN_ID}%",),
    ).fetchone()

    if not row:
        print(f"Campaign {CAMPAIGN_ID}* not found")
        db.close()
        return

    full_id = row["id"]
    print(f"Campaign: {row['name']}")
    print(f"ID: {full_id}")
    print(f"Current status: {row['status']}")

    # Count stuck prospects
    stuck = db.execute(
        """SELECT COUNT(*) as cnt FROM outreaches
           WHERE campaign_id = ? AND status = 'connected' AND followup_count = 0""",
        (full_id,),
    ).fetchone()["cnt"]

    print(f"Stuck prospects (connected, followup_count=0): {stuck}")

    if stuck == 0:
        print("No stuck prospects — nothing to do.")
        db.close()
        return

    if row["status"] == "active":
        print("Campaign is already active.")
        db.close()
        return

    if dry_run:
        print("\n[DRY RUN] Would reactivate campaign to status='active', mode='autopilot'")
        db.close()
        return

    # Reactivate
    now = int(time.time())
    db.execute(
        "UPDATE campaigns SET status = 'active', mode = 'autopilot', updated_at = ? WHERE id = ?",
        (now, full_id),
    )
    db.commit()
    print(f"\nReactivated campaign at {now}")
    print("The scheduler will now pick up the 34 stuck prospects via _plan_dms().")
    print("Once all prospects are messaged, archive again with:")
    print(f"  campaign(action='archive', campaign_id='{full_id[:8]}', force=True)")

    db.close()


if __name__ == "__main__":
    main()
