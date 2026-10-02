"""OpenSEO Wave 1 Lane B (OPENSEO-TOOLS-SPEC §5.3, §9 T3): the organic rank is
counted by CODE, and the rank notation is decided by code.

The payload is a REAL DataForSEO live response (``fixtures/dataforseo_serp_organic_
w3c_validator_live.json``, captured from seo.collection_run 3c0e126b…, trimmed to
the keys read) — a People-also-ask box at absolute 3 and an AI overview at 6 sit
above organic listings, so organic rank and ``rank_absolute`` part ways.

Each test here fails on the pre-Lane-B tree: ``rank_notation`` did not exist, and
an untagged organic payload raised ``NotImplementedError`` (owned by Lane B).
"""

from __future__ import annotations

import copy
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from matrx_seo.contracts import (
    CollectionRequest,
    NormalizationContext,
    ProviderResponse,
    ResolvedSeoIdentity,
    SeoCapability,
    SerpSnapshotObservation,
)
from matrx_seo.providers.dataforseo import DataForSeoAdapter
from matrx_seo.providers.dataforseo.serp_organic import (
    SerpTaskFailedError,
    serp_rows,
    snapshot_rows_from_payload,
)
from matrx_seo.providers.dataforseo.serp_prospect import SERP_ORGANIC_OPERATION
from matrx_seo.rank_notation import rank_notation
from matrx_seo.repository import InMemorySeoRepository

FIXTURE = Path(__file__).parent / "fixtures" / "dataforseo_serp_organic_w3c_validator_live.json"
FETCHED_AT = datetime(2026, 9, 28, 6, 9, 32, tzinfo=UTC)


def _payload() -> dict:
    return json.loads(FIXTURE.read_text())


# ── rank notation: the table ──────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("organic_rank", "depth", "ok", "expected"),
    [
        (1, 20, True, "#1 (page 1)"),
        (10, 20, True, "#10 (page 1)"),
        (11, 20, True, "#11 (page 2)"),
        (20, 20, True, "#20 (page 2)"),
        (21, 30, True, "#21 (page 3)"),
        (None, 20, True, "not in the first 20 results"),
        (None, 100, True, "not in the first 100 results"),
        (None, 20, False, "unknown"),
        (3, 20, False, "unknown"),
    ],
)
def test_rank_notation_table(organic_rank, depth, ok, expected) -> None:
    assert rank_notation(organic_rank, depth, ok) == expected


@pytest.mark.parametrize(
    ("organic_read", "expected"),
    [
        (15, "not in the first 15 organic results read (15 < 20)"),
        (19, "not in the first 19 organic results read (19 < 20)"),
        (20, "not in the first 20 results"),
        (None, "not in the first 20 results"),
    ],
)
def test_not_found_states_what_was_actually_read(organic_read, expected) -> None:
    assert rank_notation(None, 20, True, organic_read=organic_read) == expected
    assert rank_notation(7, 20, True, organic_read=organic_read) == "#7 (page 1)"


# ── organic rank is counted over organic items only ───────────────────────────


def test_organic_rank_is_counted_and_differs_from_rank_absolute_when_features_precede() -> None:
    result = _payload()["tasks"][0]["result"][0]
    rows = serp_rows(result)
    by_abs = {r.absolute_rank: r for r in rows}
    # The real page: organic 1, 2, PAA at 3, organic at 4 — the fourth item is organic #3.
    assert by_abs[3].result_type == "people_also_ask" and by_abs[3].organic_rank is None
    assert by_abs[4].result_type == "organic" and by_abs[4].organic_rank == 3
    assert by_abs[6].result_type == "ai_overview" and by_abs[6].organic_rank is None
    assert by_abs[7].organic_rank == 5
    organic = [r for r in rows if r.organic_rank is not None]
    assert [r.organic_rank for r in organic] == list(range(1, len(organic) + 1))
    assert len(organic) == sum(1 for i in result["items"] if i["type"] == "organic")
    assert any(r.organic_rank != r.absolute_rank for r in organic)


def test_count_ignores_the_providers_rank_group() -> None:
    """A lying rank_group never reaches the organic rank: code counts."""
    result = copy.deepcopy(_payload()["tasks"][0]["result"][0])
    for item in result["items"]:
        item["rank_group"] = 99
    organic = [r for r in serp_rows(result) if r.organic_rank is not None]
    assert organic[0].organic_rank == 1 and organic[2].organic_rank == 3


def test_items_out_of_page_order_are_counted_in_page_order() -> None:
    result = copy.deepcopy(_payload()["tasks"][0]["result"][0])
    result["items"].reverse()
    organic = [r for r in serp_rows(result) if r.organic_rank is not None]
    assert organic[0].absolute_rank == 1 and organic[0].organic_rank == 1


# ── the untagged branch through the adapter as constructed everywhere ────────


class _Identity:
    async def resolve(self, request, identity):
        assert identity.engine == "google" and identity.search_type == "organic"
        return ResolvedSeoIdentity(keyword_id="kw-1", rank_target_id=None)

    async def resolve_many(self, request, identities):
        return [await self.resolve(request, i) for i in identities]


async def _context(request: CollectionRequest) -> NormalizationContext:
    run = await InMemorySeoRepository().start_run("dataforseo", request)
    return NormalizationContext(
        request=request,
        run=run,
        raw_payload_id="raw-id",
        identity_resolver=_Identity(),
        host_binding_resolver=object(),
    )


def _request(**update) -> CollectionRequest:
    return CollectionRequest(
        organization_id=str(uuid4()),
        created_by=str(uuid4()),
        capability=SeoCapability.SERP_RANK,
        operation=SERP_ORGANIC_OPERATION,
        target_ref="w3c validator@2840/en/desktop/d20",
        observation_period="2026-09-28",
        settings={
            "tasks": [
                {
                    "keyword": "w3c validator",
                    "location_code": 2840,
                    "language_code": "en",
                    "depth": 20,
                    "device": "desktop",
                }
            ],
            "workflow": "live",
        },
        execution_id=uuid4(),
    ).model_copy(update=update)


@pytest.mark.asyncio
async def test_untagged_payload_yields_a_rank_snapshot() -> None:
    adapter = DataForSeoAdapter()
    request = _request()
    assert adapter.unsupported_request_reason(request) is None
    observations = await adapter.normalize(
        ProviderResponse(raw=_payload(), fetched_at=FETCHED_AT), await _context(request)
    )
    assert len(observations) == 1
    snap = observations[0]
    assert isinstance(snap, SerpSnapshotObservation)
    assert snap.keyword_id == "kw-1" and snap.engine == "google" and snap.search_type == "organic"
    assert snap.rank_target_id is None
    assert snap.query_settings["location_code"] == 2840 and snap.query_settings["depth"] == 20
    assert snap.query_settings["organic_count"] == 16
    assert snap.results == snapshot_rows_from_payload(_payload())
    fourth = next(r for r in snap.results if r.absolute_rank == 4)
    assert fourth.organic_rank == 3


@pytest.mark.asyncio
async def test_failed_task_fails_the_run_and_no_results_is_an_empty_answer() -> None:
    adapter = DataForSeoAdapter()
    failed = _payload()
    failed["tasks"][0].update(
        status_code=40501, status_message="Invalid Field: 'depth'.", result=None
    )
    with pytest.raises(SerpTaskFailedError, match="40501"):
        await adapter.normalize(
            ProviderResponse(raw=failed, fetched_at=FETCHED_AT), await _context(_request())
        )
    with pytest.raises(SerpTaskFailedError):
        snapshot_rows_from_payload(failed)

    empty = _payload()
    empty["tasks"][0].update(status_code=40102, status_message="No Search Results.", result=None)
    [snap] = await adapter.normalize(
        ProviderResponse(raw=empty, fetched_at=FETCHED_AT), await _context(_request())
    )
    assert snap.results == [] and snap.query_settings["outcome"] == "empty"
    assert snapshot_rows_from_payload(empty) == []
