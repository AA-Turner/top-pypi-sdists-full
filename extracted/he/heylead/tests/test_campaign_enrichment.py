"""E2E tests for campaign enrichment service — all 12 collector sources + pipeline."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest

from heylead.db.queries import (
    create_campaign,
    create_outreach,
    get_contacts_for_campaign,
    save_contact,
    save_inbound_signal,
    update_campaign,
    update_inbound_signal,
)
from heylead.db.global_contact_queries import upsert_global_contact
from heylead.db.signal_queries import save_signal, update_signal, upsert_signal_account
from heylead.db.async_bridge import run_db
from heylead.db.post_queries import upsert_post_author
from heylead.db.schema import get_db


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

_ICP = {
    "segments": [
        {
            "keywords": "sales automation",
            "titles": ["VP Sales", "Head of Sales"],
            "has_structured": False,
        }
    ],
    "icps": [
        {
            "job_titles": {"include": ["VP Sales", "Head of Sales"], "exclude": []},
            "industries": {"include": ["software"], "exclude": []},
            "seniority": {"include": ["vp", "director"], "exclude": []},
            "locations": {"include": [], "exclude": []},
            "company_headcount": {"min": 10, "max": 10000},
            "keywords": ["sales", "automation", "outreach"],
        }
    ],
}


def _create_active_campaign(name: str = "Test Campaign") -> str:
    camp_id = create_campaign(name=name, icp_json=json.dumps(_ICP), status="active")
    return camp_id


def _insert_connection(account_id: str, provider_id: str, name: str, headline: str):
    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO connections (account_id, provider_id, public_id, name, headline, synced_at) VALUES (?, ?, ?, ?, ?, 0)",
        (account_id, provider_id, provider_id, name, headline),
    )
    db.commit()
    db.close()


# ──────────────────────────────────────────────
# Tier A: Person-level, full data
# ──────────────────────────────────────────────


class TestCollectFromGlobalContacts:
    async def test_collects_prospects_not_in_campaign(self):
        from heylead.services.campaign_refill_service import _collect_from_global_contacts

        def _seed():
            upsert_global_contact(
                linkedin_id="gc-alice", name="Alice", title="VP Sales",
                company="Acme", fit_score=0.6, source="search",
            )
            return _create_active_campaign()

        camp_id = await run_db(_seed)

        results = await _collect_from_global_contacts(camp_id)
        assert len(results) >= 1
        match = [p for p in results if p["linkedin_id"] == "gc-alice"]
        assert len(match) == 1
        assert match[0]["_source_tag"] == "global_contacts"
        assert match[0]["title"] == "VP Sales"

    async def test_excludes_contacts_already_in_campaign(self):
        from heylead.services.campaign_refill_service import _collect_from_global_contacts

        def _seed():
            upsert_global_contact(
                linkedin_id="gc-bob", name="Bob", title="CTO",
                company="Corp", fit_score=0.5, source="search",
            )
            camp_id = _create_active_campaign()
            save_contact(campaign_id=camp_id, name="Bob", linkedin_id="gc-bob")
            return camp_id

        camp_id = await run_db(_seed)

        results = await _collect_from_global_contacts(camp_id)
        match = [p for p in results if p["linkedin_id"] == "gc-bob"]
        assert len(match) == 0


class TestCollectFromBelowThresholdSignals:
    async def test_collects_below_threshold(self):
        from heylead.services.campaign_refill_service import _collect_from_below_threshold_signals

        def _seed():
            sig_id = save_signal(
                signal_type="keyword_mention", source="test",
                linkedin_id="bt-carol", prospect_name="Carol",
                prospect_title="Sales Director",
                metadata_json=json.dumps({"company": "SalesCo"}),
            )
            update_signal(sig_id, status="actioned", action_taken="below_threshold")

        await run_db(_seed)

        results = await _collect_from_below_threshold_signals()
        match = [p for p in results if p["linkedin_id"] == "bt-carol"]
        assert len(match) == 1
        assert match[0]["_source_tag"] == "signal_reeval"
        assert match[0]["title"] == "Sales Director"

    async def test_skips_non_below_threshold(self):
        from heylead.services.campaign_refill_service import _collect_from_below_threshold_signals

        def _seed():
            sig_id = save_signal(
                signal_type="keyword_mention", source="test",
                linkedin_id="bt-skip", prospect_name="Skip",
            )
            update_signal(sig_id, status="actioned", action_taken="auto_outreach")

        await run_db(_seed)

        results = await _collect_from_below_threshold_signals()
        match = [p for p in results if p["linkedin_id"] == "bt-skip"]
        assert len(match) == 0


class TestCollectFromJobChangers:
    async def test_collects_job_change_with_new_role(self):
        from heylead.services.campaign_refill_service import _collect_from_job_changers

        await run_db(
            save_signal,
            signal_type="job_change", source="test",
            linkedin_id="jc-dave", prospect_name="Dave",
            prospect_title="Old Title",
            metadata_json=json.dumps({
                "new_title": "VP Sales", "new_company": "NewCorp",
                "old_title": "Manager", "old_company": "OldCorp",
            }),
        )

        results = await _collect_from_job_changers()
        match = [p for p in results if p["linkedin_id"] == "jc-dave"]
        assert len(match) == 1
        assert match[0]["title"] == "VP Sales"
        assert match[0]["company"] == "NewCorp"
        assert match[0]["_source_tag"] == "job_change"


class TestCollectFromSignalAccounts:
    async def test_collects_high_score_accounts(self):
        from heylead.services.campaign_refill_service import _collect_from_signal_accounts

        def _seed():
            save_signal(
                signal_type="keyword_mention", source="test",
                linkedin_id="sa-eve", prospect_name="Eve",
                confidence=0.8,
            )
            update_signal(
                save_signal(
                    signal_type="prospect_post", source="test",
                    linkedin_id="sa-eve", prospect_name="Eve",
                    confidence=0.9,
                ),
                signal_score=0.9,
            )
            upsert_signal_account(linkedin_id="sa-eve", prospect_name="Eve", company="EveCo")

        await run_db(_seed)

        results = await _collect_from_signal_accounts()
        match = [p for p in results if p["linkedin_id"] == "sa-eve"]
        assert len(match) == 1
        assert match[0]["_source_tag"] == "signal_account"


# ──────────────────────────────────────────────
# Tier B: Partial data
# ──────────────────────────────────────────────


class TestCollectFromProfileViewers:
    async def test_collects_icp_matched_viewers(self):
        from heylead.services.campaign_refill_service import _collect_from_profile_viewers

        await run_db(
            save_signal,
            signal_type="profile_view", source="test",
            linkedin_id="pv-frank", prospect_name="Frank",
            prospect_title="Head of Sales",
            metadata_json=json.dumps({
                "is_icp_match": True,
                "viewer_company": "ViewCo",
                "viewer_title": "Head of Sales",
            }),
        )

        results = await _collect_from_profile_viewers()
        match = [p for p in results if p["linkedin_id"] == "pv-frank"]
        assert len(match) == 1
        assert match[0]["_source_tag"] == "profile_viewer"

    async def test_skips_non_icp_viewers(self):
        from heylead.services.campaign_refill_service import _collect_from_profile_viewers

        await run_db(
            save_signal,
            signal_type="profile_view", source="test",
            linkedin_id="pv-nobody", prospect_name="Nobody",
            metadata_json=json.dumps({"is_icp_match": False}),
        )

        results = await _collect_from_profile_viewers()
        match = [p for p in results if p["linkedin_id"] == "pv-nobody"]
        assert len(match) == 0


class TestCollectFromPostAuthors:
    async def test_collects_active_authors(self):
        from heylead.services.campaign_refill_service import _collect_from_post_authors

        def _seed():
            upsert_post_author(linkedin_id="pa-grace", name="Grace", headline="VP Sales at SaaS", company="SaaS Inc")
            upsert_post_author(linkedin_id="pa-grace", name="Grace", headline="VP Sales at SaaS", company="SaaS Inc")

        await run_db(_seed)

        results = await _collect_from_post_authors()
        match = [p for p in results if p["linkedin_id"] == "pa-grace"]
        assert len(match) == 1
        assert match[0]["title"] == "VP Sales at SaaS"
        assert match[0]["_source_tag"] == "post_author"

    async def test_skips_single_post_authors(self):
        from heylead.services.campaign_refill_service import _collect_from_post_authors

        await run_db(upsert_post_author, linkedin_id="pa-once", name="Once", headline="Intern")

        results = await _collect_from_post_authors()
        match = [p for p in results if p["linkedin_id"] == "pa-once"]
        assert len(match) == 0


class TestCollectFromCompetitorCommenters:
    async def test_collects_competitor_commenters(self):
        from heylead.services.campaign_refill_service import _collect_from_competitor_commenters

        await run_db(
            save_signal,
            signal_type="competitor_post_commenter", source="test",
            linkedin_id="cc-hank", prospect_name="Hank",
            prospect_title="Sales Director",
            metadata_json=json.dumps({"comment_text": "Interesting!"}),
        )

        results = await _collect_from_competitor_commenters()
        match = [p for p in results if p["linkedin_id"] == "cc-hank"]
        assert len(match) == 1
        assert match[0]["_source_tag"] == "competitor_commenter"


class TestCollectFromCompanyEngagers:
    async def test_collects_all_engagement_types(self):
        from heylead.services.campaign_refill_service import _collect_from_company_engagers

        def _seed():
            for sig_type, lid in [
                ("company_post_comment", "ce-ivan"),
                ("company_post_reaction", "ce-janet"),
                ("company_follower", "ce-karl"),
            ]:
                save_signal(
                    signal_type=sig_type, source="test",
                    linkedin_id=lid, prospect_name=lid.split("-")[1].title(),
                )

        await run_db(_seed)

        results = await _collect_from_company_engagers()
        ids = {p["linkedin_id"] for p in results}
        assert "ce-ivan" in ids
        assert "ce-janet" in ids
        assert "ce-karl" in ids
        assert all(p["_source_tag"] == "company_engager" for p in results if p["linkedin_id"].startswith("ce-"))


class TestCollectFromConnections:
    async def test_collects_connections(self):
        from heylead.services.campaign_refill_service import _collect_from_connections

        await run_db(_insert_connection, "acc-1", "ACoAAA111", "Lisa", "VP Sales at BigCo")

        results = await _collect_from_connections("acc-1")
        match = [p for p in results if p["linkedin_id"] == "ACoAAA111"]
        assert len(match) == 1
        assert match[0]["title"] == "VP Sales at BigCo"
        assert match[0]["_source_tag"] == "connection"


class TestCollectFromPostCommenters:
    async def test_collects_post_commenters(self):
        from heylead.services.campaign_refill_service import _collect_from_post_commenters

        await run_db(
            save_inbound_signal,
            signal_type="comment",
            sender_id="pc-mike", sender_name="Mike",
            sender_headline="Sales Lead", sender_company="MikeCo",
            content="Love this post!",
        )

        results = await _collect_from_post_commenters()
        match = [p for p in results if p["linkedin_id"] == "pc-mike"]
        assert len(match) == 1
        assert match[0]["_source_tag"] == "post_commenter"
        assert match[0]["company"] == "MikeCo"


class TestCollectFromLowConfidenceInbound:
    async def test_collects_low_conf_non_spam(self):
        from heylead.services.campaign_refill_service import _collect_from_low_confidence_inbound

        def _seed():
            sig_id = save_inbound_signal(
                signal_type="message",
                sender_id="lc-nina", sender_name="Nina",
                sender_headline="Director of Ops", sender_company="OpsCo",
                content="Hey, would love to connect",
            )
            update_inbound_signal(sig_id, status="qualified", confidence=0.3, intent="networking")

        await run_db(_seed)

        results = await _collect_from_low_confidence_inbound()
        match = [p for p in results if p["linkedin_id"] == "lc-nina"]
        assert len(match) == 1
        assert match[0]["_source_tag"] == "inbound_low_conf"

    async def test_skips_spam(self):
        from heylead.services.campaign_refill_service import _collect_from_low_confidence_inbound

        def _seed():
            sig_id = save_inbound_signal(
                signal_type="message",
                sender_id="lc-spam", sender_name="Spammer",
                content="Buy crypto now",
            )
            update_inbound_signal(sig_id, status="qualified", confidence=0.1, intent="spam")

        await run_db(_seed)

        results = await _collect_from_low_confidence_inbound()
        match = [p for p in results if p["linkedin_id"] == "lc-spam"]
        assert len(match) == 0

    async def test_skips_high_confidence(self):
        from heylead.services.campaign_refill_service import _collect_from_low_confidence_inbound

        def _seed():
            sig_id = save_inbound_signal(
                signal_type="invitation",
                sender_id="lc-high", sender_name="High",
                sender_headline="CTO",
            )
            update_inbound_signal(sig_id, status="qualified", confidence=0.8, intent="buying_signal")

        await run_db(_seed)

        results = await _collect_from_low_confidence_inbound()
        match = [p for p in results if p["linkedin_id"] == "lc-high"]
        assert len(match) == 0


# ──────────────────────────────────────────────
# Tier C: Company-level (needs mocked API)
# ──────────────────────────────────────────────


class TestCollectFromNewsEvents:
    @pytest.mark.asyncio
    async def test_resolves_companies_to_people(self):
        from heylead.services.campaign_refill_service import _collect_from_news_events

        await run_db(
            save_signal,
            signal_type="news_funding", source="test",
            linkedin_id="", prospect_name="",
            metadata_json=json.dumps({"company_name": "FundedStartup", "amount": "$10M"}),
        )

        mock_client = AsyncMock()
        mock_client.search_people.return_value = (
            [{"name": "Oscar", "title": "VP Sales", "public_id": "ne-oscar", "company": "FundedStartup"}],
            None,
        )

        results = await _collect_from_news_events(mock_client, "acc-1", _ICP)
        match = [p for p in results if p.get("public_id") == "ne-oscar"]
        assert len(match) == 1
        assert "news_" in match[0]["_source_tag"]

    @pytest.mark.asyncio
    async def test_empty_when_no_news(self):
        from heylead.services.campaign_refill_service import _collect_from_news_events

        mock_client = AsyncMock()
        results = await _collect_from_news_events(mock_client, "acc-1", _ICP)
        assert results == []


# ──────────────────────────────────────────────
# Full pipeline E2E
# ──────────────────────────────────────────────


class TestEnrichCampaignPipeline:
    @pytest.mark.asyncio
    async def test_full_pipeline_collects_dedupes_scores_saves(self, monkeypatch):
        """Seed multiple sources, run pipeline, verify contacts + outreaches created."""
        def _seed():
            camp_id = _create_active_campaign()
            upsert_global_contact(
                linkedin_id="e2e-alice", name="Alice", title="VP Sales",
                company="AliceCo", fit_score=0.7, source="search",
            )
            save_signal(
                signal_type="job_change", source="test",
                linkedin_id="e2e-bob", prospect_name="Bob",
                metadata_json=json.dumps({"new_title": "Head of Sales", "new_company": "BobCo"}),
            )
            upsert_post_author(linkedin_id="e2e-carol", name="Carol", headline="Sales Director at CarolCo", company="CarolCo")
            upsert_post_author(linkedin_id="e2e-carol", name="Carol", headline="Sales Director at CarolCo", company="CarolCo")
            return camp_id

        camp_id = await run_db(_seed)

        # Mock LinkedIn client
        mock_client = AsyncMock()
        mock_client.search_people.return_value = ([], None)
        mock_client.find_linkedin_account = AsyncMock(return_value=("acc-1", {}))

        monkeypatch.setattr("heylead.linkedin.get_linkedin_client", lambda: mock_client)
        monkeypatch.setattr("heylead.linkedin.get_account_id", lambda: "acc-1")

        from heylead.services.campaign_refill_service import _enrich_campaign

        added = await _enrich_campaign(
            campaign_id=camp_id,
            campaign_name="Test",
            icp=_ICP,
            config={},
            max_pages=1,
            batch_size=50,
        )

        assert added >= 3
        contacts = await run_db(get_contacts_for_campaign, camp_id)
        linkedin_ids = {c["linkedin_id"] for c in contacts}
        assert "e2e-alice" in linkedin_ids
        assert "e2e-bob" in linkedin_ids
        assert "e2e-carol" in linkedin_ids

        # Verify fit_score is set
        for c in contacts:
            assert c["fit_score"] >= 0.0

        # Verify source_detail tracks origin
        source_details = {c["linkedin_id"]: c.get("source_detail", "") for c in contacts}
        assert source_details["e2e-alice"] == "global_contacts"
        assert source_details["e2e-bob"] == "job_change"
        assert source_details["e2e-carol"] == "post_author"

    @pytest.mark.asyncio
    async def test_dedup_prevents_duplicates(self, monkeypatch):
        """Same linkedin_id from multiple sources should result in one contact."""
        def _seed():
            camp_id = _create_active_campaign()
            upsert_global_contact(
                linkedin_id="dup-dave", name="Dave", title="VP Sales",
                company="DaveCo", fit_score=0.6, source="search",
            )
            save_signal(
                signal_type="job_change", source="test",
                linkedin_id="dup-dave", prospect_name="Dave",
                metadata_json=json.dumps({"new_title": "VP Sales", "new_company": "DaveCo"}),
            )
            return camp_id

        camp_id = await run_db(_seed)

        mock_client = AsyncMock()
        mock_client.search_people.return_value = ([], None)

        monkeypatch.setattr("heylead.linkedin.get_linkedin_client", lambda: mock_client)
        monkeypatch.setattr("heylead.linkedin.get_account_id", lambda: "acc-1")

        from heylead.services.campaign_refill_service import _enrich_campaign

        added = await _enrich_campaign(
            campaign_id=camp_id,
            campaign_name="Test",
            icp=_ICP,
            config={},
            max_pages=1,
            batch_size=50,
        )

        contacts = await run_db(get_contacts_for_campaign, camp_id)
        dave_contacts = [c for c in contacts if c["linkedin_id"] == "dup-dave"]
        assert len(dave_contacts) == 1

    @pytest.mark.asyncio
    async def test_scoring_sorts_best_first(self, monkeypatch):
        """Higher ICP-matching prospects should get higher fit_score."""
        def _seed():
            camp_id = _create_active_campaign()
            upsert_global_contact(
                linkedin_id="score-good", name="Good", title="VP Sales",
                company="SaaS Co", fit_score=0.1, source="search",
            )
            upsert_global_contact(
                linkedin_id="score-poor", name="Poor", title="Junior Intern",
                company="Random", fit_score=0.1, source="search",
            )
            return camp_id

        camp_id = await run_db(_seed)

        mock_client = AsyncMock()
        mock_client.search_people.return_value = ([], None)

        monkeypatch.setattr("heylead.linkedin.get_linkedin_client", lambda: mock_client)
        monkeypatch.setattr("heylead.linkedin.get_account_id", lambda: "acc-1")

        from heylead.services.campaign_refill_service import _enrich_campaign

        await _enrich_campaign(
            campaign_id=camp_id,
            campaign_name="Test",
            icp=_ICP,
            config={},
            max_pages=1,
            batch_size=50,
        )

        contacts = await run_db(get_contacts_for_campaign, camp_id)
        good = next((c for c in contacts if c["linkedin_id"] == "score-good"), None)
        poor = next((c for c in contacts if c["linkedin_id"] == "score-poor"), None)
        assert good is not None
        assert poor is not None
        assert good["fit_score"] > poor["fit_score"]


class TestRefillCampaigns:
    @pytest.mark.asyncio
    async def test_respects_cooldown(self, monkeypatch):
        """Should skip campaigns within cooldown period."""
        import time

        def _seed():
            camp_id = _create_active_campaign()
            config = {"last_refill_at": int(time.time())}
            update_campaign(camp_id, config_json=json.dumps(config))
            return camp_id

        camp_id = await run_db(_seed)

        mock_client = AsyncMock()
        monkeypatch.setattr("heylead.linkedin.get_linkedin_client", lambda: mock_client)
        monkeypatch.setattr("heylead.linkedin.get_account_id", lambda: "acc-1")

        from heylead.services.campaign_refill_service import refill_campaigns

        result = await refill_campaigns()
        assert "skipped" in result.lower() or "No campaigns to enrich" == result
