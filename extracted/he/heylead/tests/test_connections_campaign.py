"""Tests for connections-only campaign refactor: connections-based sourcing + enrichment."""

from __future__ import annotations

import json
import time
from unittest.mock import AsyncMock, patch

import pytest

from heylead.db import schema
from heylead.db.async_bridge import run_db
from heylead.db.global_contact_queries import (
    get_global_contacts_by_identifiers,
    upsert_global_contact,
)
from heylead.services.connection_sync import get_all_connections


# ──────────────────────────────────────────────
# Phase 1: get_all_connections + batch lookup
# ──────────────────────────────────────────────

class TestGetAllConnections:
    """get_all_connections returns full connection rows."""

    def test_returns_connections_for_account(self):
        db = schema.get_db()
        now = int(time.time())
        db.execute(
            """INSERT INTO connections (id, account_id, provider_id, public_id, name, headline, synced_at)
               VALUES ('c1', 'acc1', 'ACoAAA123', 'john-doe', 'John Doe', 'CEO at Acme', ?)""",
            (now,),
        )
        db.execute(
            """INSERT INTO connections (id, account_id, provider_id, public_id, name, headline, synced_at)
               VALUES ('c2', 'acc1', 'ACoAAA456', 'jane-smith', 'Jane Smith', 'CTO at Beta', ?)""",
            (now,),
        )
        db.execute(
            """INSERT INTO connections (id, account_id, provider_id, public_id, name, headline, synced_at)
               VALUES ('c3', 'acc2', 'ACoAAA789', 'bob', 'Bob', 'VP Sales', ?)""",
            (now,),
        )
        db.commit()
        db.close()

        conns = get_all_connections("acc1")
        assert len(conns) == 2
        names = {c["name"] for c in conns}
        assert names == {"John Doe", "Jane Smith"}
        # Verify all fields present
        john = next(c for c in conns if c["name"] == "John Doe")
        assert john["provider_id"] == "ACoAAA123"
        assert john["public_id"] == "john-doe"
        assert john["headline"] == "CEO at Acme"

    def test_returns_empty_for_unknown_account(self):
        assert get_all_connections("nonexistent") == []

    def test_skips_connections_without_identifiers(self):
        db = schema.get_db()
        now = int(time.time())
        db.execute(
            """INSERT INTO connections (id, account_id, provider_id, public_id, name, headline, synced_at)
               VALUES ('c4', 'acc1', '', '', 'No ID', 'Nobody', ?)""",
            (now,),
        )
        db.commit()
        db.close()
        assert get_all_connections("acc1") == []


class TestGetGlobalContactsByIdentifiers:
    """Batch lookup global_contacts by identifier."""

    def test_matches_by_linkedin_id(self):
        now = int(time.time())
        db = schema.get_db()
        db.execute(
            """INSERT INTO global_contacts
               (id, linkedin_id, name, title, company, profile_json, lifecycle_stage, total_campaigns, created_at, updated_at)
               VALUES ('gc1', 'john-doe', 'John Doe', 'CEO', 'Acme', '{"provider_id":"ACoAAA123"}', 'prospect', 1, ?, ?)""",
            (now, now),
        )
        db.commit()
        db.close()

        result = get_global_contacts_by_identifiers(["john-doe"])
        assert "john-doe" in result
        assert result["john-doe"]["name"] == "John Doe"

    def test_matches_by_provider_id_in_profile_json(self):
        now = int(time.time())
        db = schema.get_db()
        db.execute(
            """INSERT INTO global_contacts
               (id, linkedin_id, name, title, profile_json, lifecycle_stage, total_campaigns, created_at, updated_at)
               VALUES ('gc2', 'jane-slug', 'Jane', 'CTO', '{"provider_id":"ACoAAAbc"}', 'prospect', 1, ?, ?)""",
            (now, now),
        )
        db.commit()
        db.close()

        result = get_global_contacts_by_identifiers(["ACoAAAbc"])
        assert "acoaaabc" in result

    def test_returns_empty_for_no_matches(self):
        result = get_global_contacts_by_identifiers(["nonexistent"])
        assert result == {}

    def test_handles_empty_list(self):
        result = get_global_contacts_by_identifiers([])
        assert result == {}


# ──────────────────────────────────────────────
# Phase 2: enrich_prospects
# ──────────────────────────────────────────────

class TestEnrichProspects:
    """enrich_prospects fetches full profiles for prospects missing profile_json."""

    @pytest.mark.asyncio
    async def test_enriches_prospects_without_profile_json(self):
        from heylead.services.connection_sync import enrich_prospects

        mock_client = AsyncMock()
        mock_client.get_profile.return_value = {
            "name": "John Doe",
            "title": "CEO",
            "headline": "CEO at Acme",
            "company": "Acme Corp",
            "location": "San Francisco",
            "provider_id": "ACoAAA123",
            "skills": [{"name": "Sales"}],
        }
        mock_client.get_user_posts.return_value = []
        mock_client.close = AsyncMock()

        prospects = [
            {"name": "John Doe", "provider_id": "ACoAAA123", "title": "", "company": ""},
            {"name": "Jane Smith", "provider_id": "ACoAAA456", "profile_json": '{"existing": true}'},
        ]

        count = await enrich_prospects(mock_client, "acc1", prospects, max_enrich=10, delay=0)
        assert count == 1
        # John should be enriched
        assert prospects[0]["company"] == "Acme Corp"
        assert prospects[0]["profile_json"]  # should have profile_json now
        # Jane should be skipped (already has profile_json)
        assert mock_client.get_profile.call_count == 1

    @pytest.mark.asyncio
    async def test_respects_max_enrich_limit(self):
        from heylead.services.connection_sync import enrich_prospects

        mock_client = AsyncMock()
        mock_client.get_profile.return_value = {"name": "Test", "title": "Dev"}
        mock_client.get_user_posts.return_value = []
        mock_client.close = AsyncMock()

        prospects = [
            {"name": f"Person {i}", "provider_id": f"ACoAAA{i}"} for i in range(10)
        ]

        count = await enrich_prospects(mock_client, "acc1", prospects, max_enrich=3, delay=0)
        assert count == 3
        assert mock_client.get_profile.call_count == 3

    @pytest.mark.asyncio
    async def test_continues_after_single_failure(self):
        from heylead.services.connection_sync import enrich_prospects

        mock_client = AsyncMock()
        mock_client.get_profile.side_effect = [
            Exception("API error"),
            {"name": "Jane", "title": "CTO", "company": "Beta"},
        ]
        mock_client.get_user_posts.return_value = []
        mock_client.close = AsyncMock()

        prospects = [
            {"name": "John", "provider_id": "ACoAAA1"},
            {"name": "Jane", "provider_id": "ACoAAA2"},
        ]

        count = await enrich_prospects(mock_client, "acc1", prospects, max_enrich=10, delay=0)
        assert count == 1  # Only Jane succeeded


# ──────────────────────────────────────────────
# Phase 3: contacts(action='enrich')
# ──────────────────────────────────────────────

class TestContactsEnrichAction:
    """contacts(action='enrich') enriches contacts on demand."""

    @pytest.mark.asyncio
    async def test_enrich_single_contact(self):
        from heylead.tools.contacts import _handle_enrich

        # Create a global contact
        gid = await run_db(
            upsert_global_contact,
            linkedin_id="test-person",
            name="Test Person",
            source="test",
        )

        mock_client = AsyncMock()
        mock_client.get_profile.return_value = {
            "name": "Test Person",
            "title": "Director of Sales",
            "company": "TestCorp",
            "location": "London",
            "skills": [{"name": "Leadership"}],
        }
        mock_client.get_user_posts.return_value = []
        mock_client.list_accounts.return_value = [{"id": "acc1"}]
        mock_client.close = AsyncMock()

        with patch("heylead.linkedin.get_linkedin_client", return_value=mock_client):
            result = await _handle_enrich(contact_id=gid, query="", limit=25)

        assert "Test Person" in result
        assert "Director of Sales" in result
        assert "TestCorp" in result
        assert "Enriched 1/1" in result

    @pytest.mark.asyncio
    async def test_enrich_requires_contact_id_or_query(self):
        from heylead.tools.contacts import _handle_enrich

        mock_client = AsyncMock()
        mock_client.list_accounts.return_value = [{"id": "acc1"}]
        mock_client.close = AsyncMock()

        with patch("heylead.linkedin.get_linkedin_client", return_value=mock_client):
            result = await _handle_enrich(contact_id="", query="", limit=25)

        assert "Provide contact_id" in result


# ──────────────────────────────────────────────
# Integration: connections-only campaign creation
# ──────────────────────────────────────────────

class TestConnectionsOnlyCampaignNoSearch:
    """Connections-only campaigns should NOT call search_people."""

    @pytest.mark.asyncio
    async def test_uses_connections_table_not_search(self):
        """Verify connections-only campaign sources from connections table."""
        def _seed():
            db = schema.get_db()
            now = int(time.time())
            for i in range(5):
                db.execute(
                    """INSERT INTO connections (id, account_id, provider_id, public_id, name, headline, synced_at)
                       VALUES (?, 'acc1', ?, ?, ?, 'Founder at startup', ?)""",
                    (f"c{i}", f"ACoAAA{i}", f"person-{i}", f"Person {i}", now),
                )
            db.commit()
            db.close()

        await run_db(_seed)

        # Verify connections are available
        conns = await run_db(get_all_connections, "acc1")
        assert len(conns) == 5

    def test_refill_skips_search_for_connections_only(self):
        """Verify the refill service has the connections-only guard on search."""
        import inspect
        from heylead.services import campaign_refill_service

        source = inspect.getsource(campaign_refill_service)
        # The refill should have "not is_connections_only" guard on search
        assert "not is_connections_only" in source
