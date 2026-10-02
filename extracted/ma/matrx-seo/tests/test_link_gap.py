"""The competitor link-gap normalizer, pinned against a REAL provider payload.

``fixtures/dataforseo_domain_intersection_live.json`` is an actual
``/v3/backlinks/domain_intersection/live`` response captured on 2026-08-14
(targets: shredit.com + shrednations.com, excluding datadestruction.com).
It exists because the payload shape is genuinely counter-intuitive and a
hand-written fixture would have encoded the same mistake as the parser.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from matrx_seo.providers.dataforseo.link_gap import (
    DOMAIN_INTERSECTION,
    PAGE_INTERSECTION,
    normalize_link_gap_payload,
    supports_intersection_endpoint,
)

FIXTURE = Path(__file__).parent / "fixtures" / "dataforseo_domain_intersection_live.json"
FETCHED_AT = datetime(2026, 8, 14, 12, 0, tzinfo=UTC)


@pytest.fixture
def payload() -> dict:
    return json.loads(FIXTURE.read_text())


def _observe(payload: dict):
    return normalize_link_gap_payload(
        endpoint=DOMAIN_INTERSECTION,
        raw=payload,
        site_id="38eff4c9-b021-451a-b995-7d9b3d17db5e",
        excluded_targets=["datadestruction.com"],
        fetched_at=FETCHED_AT,
    )


class TestTheInversionTrap:
    """The single mistake that would silently invert the whole feature."""

    def test_the_referring_domain_is_read_from_target_not_the_numbered_key(self, payload):
        [observation] = _observe(payload)
        domains = {d.normalized_domain for d in observation.domains}
        # These are the REFERRING domains in the real payload.
        assert "livelycity.com" in domains
        # The competitors must never appear as gap domains — that is what
        # reading `target` as the competitor would produce.
        assert "shredit.com" not in domains
        assert "shrednations.com" not in domains

    def test_each_match_names_the_competitor_from_the_submitted_target_map(self, payload):
        [observation] = _observe(payload)
        assert observation.competitor_targets == {
            "1": "shredit.com",
            "2": "shrednations.com",
        }
        for domain in observation.domains:
            named = {m.competitor_domain for m in domain.matches}
            assert named <= {"shredit.com", "shrednations.com"}
            # A gap domain whose matches name itself is the inverted read.
            assert domain.normalized_domain not in named

    def test_a_numbered_key_with_no_submitted_target_is_refused(self, payload):
        """Recording a match against an unknown competitor would be a lie."""
        payload["tasks"][0]["result"][0]["targets"] = {"1": "shredit.com"}
        with pytest.raises(ValueError, match="no matching submitted target"):
            _observe(payload)


class TestMatchCount:
    def test_match_count_comes_from_the_provider_not_from_our_own_arithmetic(self, payload):
        [observation] = _observe(payload)
        for domain in observation.domains:
            assert domain.match_count == 2
            assert len(domain.matches) == 2

    def test_the_gap_is_meaningless_without_recording_what_it_excluded(self, payload):
        [observation] = _observe(payload)
        assert observation.excluded_targets == ["datadestruction.com"]


class TestFieldMapping:
    def test_per_competitor_metrics_are_kept_separate(self, payload):
        [observation] = _observe(payload)
        lively = next(d for d in observation.domains if d.normalized_domain == "livelycity.com")
        by_competitor = {m.competitor_domain: m for m in lively.matches}
        # Real values from the captured payload: 133 backlinks to competitor 1,
        # 1 to competitor 2. Collapsing these would destroy the evidence.
        assert by_competitor["shredit.com"].backlinks == 133
        assert by_competitor["shrednations.com"].backlinks == 1
        assert by_competitor["shredit.com"].domain_rank == Decimal("220")
        assert by_competitor["shrednations.com"].domain_rank == Decimal("23")

    def test_domain_level_rollups_take_the_strongest_and_worst(self, payload):
        [observation] = _observe(payload)
        lively = next(d for d in observation.domains if d.normalized_domain == "livelycity.com")
        assert lively.domain_rank == Decimal("220")  # best rank across targets
        assert lively.spam_score == Decimal("3")  # worst spam across targets
        assert lively.total_backlinks == 134

    def test_provider_timestamps_parse_to_utc(self, payload):
        [observation] = _observe(payload)
        lively = next(d for d in observation.domains if d.normalized_domain == "livelycity.com")
        assert lively.first_seen_at is not None
        assert lively.first_seen_at.tzinfo is not None
        assert lively.first_seen_at.year == 2025

    def test_unmodelled_provider_detail_survives_in_extras(self, payload):
        [observation] = _observe(payload)
        lively = next(d for d in observation.domains if d.normalized_domain == "livelycity.com")
        extras = lively.matches[0].extras
        assert "referring_links_platform_types" in extras
        assert "referring_links_tld" in extras

    def test_total_available_is_carried_so_the_ui_can_say_how_much_is_left(self, payload):
        [observation] = _observe(payload)
        assert observation.total_available == 355


class TestPageIntersection:
    def test_referring_page_and_exact_competitor_page_are_preserved(self):
        raw = {
            "tasks": [
                {
                    "result": [
                        {
                            "targets": {
                                "1": "https://rival.example/guide-a",
                                "2": "https://peer.example/guide-b",
                            },
                            "total_count": 1,
                            "items": [
                                {
                                    "page_intersection": {
                                        "1": [
                                            {
                                                "domain_from": "publisher.example",
                                                "url_from": "https://publisher.example/resources",
                                                "url_to": "https://rival.example/guide-a",
                                                "domain_from_rank": 812,
                                                "backlink_spam_score": 2,
                                                "dofollow": True,
                                                "links_count": 1,
                                                "first_seen": "2026-01-01 10:00:00 +00:00",
                                                "last_seen": "2026-08-01 10:00:00 +00:00",
                                                "anchor": "best guide",
                                            }
                                        ],
                                        "2": [
                                            {
                                                "domain_from": "publisher.example",
                                                "url_from": "https://publisher.example/resources",
                                                "url_to": "https://peer.example/guide-b",
                                                "domain_from_rank": 812,
                                                "backlink_spam_score": 2,
                                                "dofollow": False,
                                                "links_count": 2,
                                            }
                                        ],
                                    },
                                    "summary": {"intersections_count": 2},
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        [observation] = normalize_link_gap_payload(
            endpoint=PAGE_INTERSECTION,
            raw=raw,
            site_id="site",
            excluded_targets=["https://ours.example/guide"],
            fetched_at=FETCHED_AT,
        )
        [domain] = observation.domains
        assert domain.normalized_domain == "publisher.example"
        assert domain.match_count == 2
        assert domain.total_backlinks == 3
        assert len(domain.matches) == 2
        first = domain.matches[0]
        assert first.competitor_domain == "rival.example"
        assert first.source_url == "https://publisher.example/resources"
        assert first.target_url == "https://rival.example/guide-a"
        assert first.is_dofollow is True
        assert first.last_seen_at == datetime(2026, 8, 1, 10, 0, tzinfo=UTC)
        assert first.extras["anchor"] == "best guide"

    def test_page_intersection_requires_array_entries(self):
        raw = {
            "tasks": [
                {
                    "result": [
                        {
                            "targets": {"1": "https://rival.example/guide"},
                            "items": [
                                {
                                    "page_intersection": {
                                        "1": {"domain_from": "publisher.example"}
                                    },
                                    "summary": {"intersections_count": 1},
                                }
                            ],
                        }
                    ]
                }
            ],
        }
        with pytest.raises(ValueError, match="non-empty arrays"):
            normalize_link_gap_payload(
                endpoint=PAGE_INTERSECTION,
                raw=raw,
                site_id="site",
                fetched_at=FETCHED_AT,
            )


class TestFailureModes:
    def test_an_unsupported_endpoint_is_refused(self, payload):
        with pytest.raises(ValueError, match="unsupported"):
            normalize_link_gap_payload(
                endpoint="/v3/backlinks/summary/live",
                raw=payload,
                site_id="site",
                fetched_at=FETCHED_AT,
            )

    def test_a_malformed_envelope_raises_rather_than_reporting_no_opportunities(self):
        """An empty gap list reads to a user as 'you have no opportunities'.
        That is a far worse outcome than a loud parse failure."""
        with pytest.raises(ValueError):
            normalize_link_gap_payload(
                endpoint=DOMAIN_INTERSECTION,
                raw={"tasks": []},
                site_id="site",
                fetched_at=FETCHED_AT,
            )

    def test_blank_site_id_is_refused(self, payload):
        with pytest.raises(ValueError, match="site_id"):
            normalize_link_gap_payload(
                endpoint=DOMAIN_INTERSECTION,
                raw=payload,
                site_id="  ",
                fetched_at=FETCHED_AT,
            )

    def test_endpoint_support_check(self):
        assert supports_intersection_endpoint(DOMAIN_INTERSECTION)
        assert supports_intersection_endpoint("/v3/backlinks/page_intersection/live")
        assert not supports_intersection_endpoint("/v3/backlinks/competitors/live")
        assert not supports_intersection_endpoint(None)
