"""Tests for cross-campaign dedup fixes (provider_id matching, merge, fit_score threshold)."""

from __future__ import annotations

import json
import time

from heylead.db import schema
from heylead.db.global_contact_queries import (
    find_duplicate_global_contacts,
    merge_global_contacts,
    upsert_global_contact,
)
from heylead.services.dedup_service import get_all_known_linkedin_ids


class TestGetAllKnownLinkedinIdsIncludesProviderIds:
    """Fix 1: get_all_known_linkedin_ids should return provider_ids from profile_json."""

    def test_returns_provider_id_from_profile_json(self):
        db = schema.get_db()
        now = int(time.time())
        profile = json.dumps({"provider_id": "ACoAABv1cucBtest"})
        db.execute(
            """INSERT INTO global_contacts
               (id, linkedin_id, name, profile_json, lifecycle_stage, total_campaigns, created_at, updated_at)
               VALUES ('gc1', 'john-doe-123', 'John', ?, 'prospect', 1, ?, ?)""",
            (profile, now, now),
        )
        db.commit()
        db.close()

        ids = get_all_known_linkedin_ids()
        assert "acoaabv1cucbtest" in ids  # provider_id lowercase
        assert "john-doe-123" in ids  # public_id also present

    def test_returns_provider_id_even_without_linkedin_id(self):
        db = schema.get_db()
        now = int(time.time())
        profile = json.dumps({"provider_id": "ACoAAOrphan123"})
        db.execute(
            """INSERT INTO global_contacts
               (id, linkedin_id, name, profile_json, lifecycle_stage, total_campaigns, created_at, updated_at)
               VALUES ('gc2', NULL, 'Orphan', ?, 'prospect', 1, ?, ?)""",
            (profile, now, now),
        )
        db.commit()
        db.close()

        ids = get_all_known_linkedin_ids()
        assert "acoaaorphan123" in ids

    def test_two_contacts_same_provider_id_both_in_set(self):
        """Same provider_id with different linkedin_ids — both should be in the dedup set."""
        db = schema.get_db()
        now = int(time.time())
        profile = json.dumps({"provider_id": "ACoAASharedPid"})
        db.execute(
            """INSERT INTO global_contacts
               (id, linkedin_id, name, profile_json, lifecycle_stage, total_campaigns, created_at, updated_at)
               VALUES ('gc3', 'alice-slug', 'Alice', ?, 'prospect', 1, ?, ?)""",
            (profile, now, now),
        )
        db.execute(
            """INSERT INTO global_contacts
               (id, linkedin_id, name, profile_json, lifecycle_stage, total_campaigns, created_at, updated_at)
               VALUES ('gc4', 'alice-other', 'Alice Other', ?, 'prospect', 1, ?, ?)""",
            (profile, now, now),
        )
        db.commit()
        db.close()

        ids = get_all_known_linkedin_ids()
        assert "acoaasharedpid" in ids
        assert "alice-slug" in ids
        assert "alice-other" in ids


class TestUpsertGlobalContactProviderIdFallback:
    """Fix 2: upsert_global_contact should match by provider_id when linkedin_id doesn't match."""

    def test_matches_by_provider_id_when_linkedin_id_differs(self):
        profile = json.dumps({"provider_id": "ACoAAMatch123"})

        # Create initial contact with one linkedin_id
        gid1 = upsert_global_contact(
            linkedin_id="slug-one",
            name="Test Person",
            profile_json=profile,
        )

        # Upsert with different linkedin_id but same provider_id
        gid2 = upsert_global_contact(
            linkedin_id="slug-two",
            name="Test Person Updated",
            profile_json=profile,
        )

        # Should return same global contact ID (matched by provider_id)
        assert gid1 == gid2

    def test_backfills_linkedin_id_on_provider_id_match(self):
        profile = json.dumps({"provider_id": "ACoAABackfill"})

        # Create contact without linkedin_id
        gid = upsert_global_contact(
            linkedin_id="",
            name="No Slug",
            profile_json=profile,
        )

        # Upsert with linkedin_id and same provider_id
        gid2 = upsert_global_contact(
            linkedin_id="now-has-slug",
            name="No Slug",
            profile_json=profile,
        )

        assert gid == gid2

        # Verify linkedin_id was backfilled
        db = schema.get_db()
        row = db.execute("SELECT linkedin_id FROM global_contacts WHERE id = ?", (gid,)).fetchone()
        db.close()
        assert row["linkedin_id"] == "now-has-slug"

    def test_creates_new_when_no_provider_id_match(self):
        profile1 = json.dumps({"provider_id": "ACoAAUnique1"})
        profile2 = json.dumps({"provider_id": "ACoAAUnique2"})

        gid1 = upsert_global_contact(linkedin_id="slug-a", name="A", profile_json=profile1)
        gid2 = upsert_global_contact(linkedin_id="slug-b", name="B", profile_json=profile2)

        assert gid1 != gid2


class TestFindDuplicateGlobalContacts:
    """Fix 3: find_duplicate_global_contacts should detect duplicates by provider_id."""

    def test_finds_duplicates_with_same_provider_id(self):
        profile = json.dumps({"provider_id": "ACoAADupe"})
        db = schema.get_db()
        now = int(time.time())
        for i, lid in enumerate(["dupe-one", "dupe-two"]):
            db.execute(
                """INSERT INTO global_contacts
                   (id, linkedin_id, name, profile_json, lifecycle_stage,
                    total_campaigns, fit_score, created_at, updated_at)
                   VALUES (?, ?, ?, ?, 'prospect', 1, 0.5, ?, ?)""",
                (f"dup{i}", lid, f"Dupe {i}", profile, now, now),
            )
        db.commit()
        db.close()

        dupes = find_duplicate_global_contacts()
        assert len(dupes) == 1
        assert dupes[0]["provider_id"] == "ACoAADupe"

    def test_no_duplicates_when_unique_provider_ids(self):
        db = schema.get_db()
        now = int(time.time())
        for i in range(3):
            profile = json.dumps({"provider_id": f"ACoAAUniq{i}"})
            db.execute(
                """INSERT INTO global_contacts
                   (id, linkedin_id, name, profile_json, lifecycle_stage,
                    total_campaigns, created_at, updated_at)
                   VALUES (?, ?, ?, ?, 'prospect', 1, ?, ?)""",
                (f"uniq{i}", f"slug-{i}", f"Person {i}", profile, now, now),
            )
        db.commit()
        db.close()

        dupes = find_duplicate_global_contacts()
        assert len(dupes) == 0


class TestMergeGlobalContacts:
    """Fix 3: merge_global_contacts should consolidate two records into one."""

    def test_merge_reassigns_campaign_contacts(self):
        db = schema.get_db()
        now = int(time.time())
        profile = json.dumps({"provider_id": "ACoAAMerge"})

        # Create two global contacts
        for gid, lid in [("keep-id", "slug-keep"), ("merge-id", "slug-merge")]:
            db.execute(
                """INSERT INTO global_contacts
                   (id, linkedin_id, name, profile_json, lifecycle_stage,
                    total_campaigns, fit_score, created_at, updated_at)
                   VALUES (?, ?, 'Test', ?, 'prospect', 1, 0.5, ?, ?)""",
                (gid, lid, profile, now, now),
            )

        # Create a campaign
        db.execute(
            "INSERT INTO campaigns (id, name, status, icp_json, created_at) "
            "VALUES ('c1', 'Test', 'active', '{}', ?)",
            (now,),
        )

        # Create campaign contacts pointing to each global contact (unique linkedin_ids)
        for cid, gcid, lid in [("cc1", "keep-id", "slug-keep"), ("cc2", "merge-id", "slug-merge")]:
            db.execute(
                """INSERT INTO contacts
                   (id, campaign_id, name, title, company, linkedin_url,
                    linkedin_id, status, global_contact_id, created_at)
                   VALUES (?, 'c1', 'Test', '', '', '', ?, 'pending', ?, ?)""",
                (cid, lid, gcid, now),
            )
        db.commit()
        db.close()

        success = merge_global_contacts("keep-id", "merge-id")
        assert success is True

        # Verify merge-id is deleted
        db = schema.get_db()
        row = db.execute("SELECT * FROM global_contacts WHERE id = 'merge-id'").fetchone()
        assert row is None

        # Verify campaign contacts now point to keep-id
        rows = db.execute(
            "SELECT global_contact_id FROM contacts WHERE id IN ('cc1', 'cc2')"
        ).fetchall()
        db.close()
        assert all(r["global_contact_id"] == "keep-id" for r in rows)

    def test_merge_combines_tags(self):
        db = schema.get_db()
        now = int(time.time())

        db.execute(
            """INSERT INTO global_contacts
               (id, linkedin_id, name, lifecycle_stage, total_campaigns,
                tags_json, created_at, updated_at)
               VALUES ('tk', 'slug-tk', 'Keep', 'prospect', 1, '["enterprise"]', ?, ?)""",
            (now, now),
        )
        db.execute(
            """INSERT INTO global_contacts
               (id, linkedin_id, name, lifecycle_stage, total_campaigns,
                tags_json, created_at, updated_at)
               VALUES ('tm', 'slug-tm', 'Merge', 'engaged', 2, '["hot","enterprise"]', ?, ?)""",
            (now, now),
        )
        db.commit()
        db.close()

        merge_global_contacts("tk", "tm")

        db = schema.get_db()
        row = db.execute("SELECT * FROM global_contacts WHERE id = 'tk'").fetchone()
        db.close()
        row = dict(row)

        tags = json.loads(row["tags_json"])
        assert "enterprise" in tags
        assert "hot" in tags
        assert row["total_campaigns"] == 3  # 1 + 2
        assert row["lifecycle_stage"] == "engaged"  # promoted from prospect

    def test_merge_fails_for_nonexistent_ids(self):
        assert merge_global_contacts("nonexistent-1", "nonexistent-2") is False
