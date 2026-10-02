"""OpenSEO Wave 1 Lane A — the Labs / Google Ads keyword normalizer, on REAL payloads.

Every fixture under ``tests/fixtures/dataforseo/labs_keywords/`` is a DataForSEO
response stored in ``seo.raw_payload`` by a live collection (the run id is in each
file's ``_source``), with only size fields trimmed. Nothing here is a hand-made
provider body.

Pins (OPENSEO-TOOLS-SPEC §4.1, §5.1, §9 T1):

* the registered normalizer is live: a normalized Labs keyword collection passes
  the pre-run gate and runs through ``SeoCollectionService.collect`` end to end;
* ``related_keywords`` rows are unwrapped from ``keyword_data``; difficulty and
  provider intent are read; Labs' 0-1 competition becomes a 0-100 index;
* Google Ads ``keywords_for_keywords`` persists only ``settings.max_items`` rows
  and carries no difficulty or intent;
* a difficulty-only observation (``bulk_keyword_difficulty``) never overwrites the
  stored volume fields (the orm upsert's volume winner ignores it).
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from matrx_seo.contracts import (
    CollectionRequest,
    KeywordMarketObservation,
    MonthlySearch,
    ProviderResponse,
    ResolvedCredential,
    ResolvedSeoIdentity,
    SeoCapability,
)
from matrx_seo.providers.dataforseo import DataForSeoAdapter
from matrx_seo.providers.dataforseo.labs_keywords import (
    NORMALIZED_OPERATIONS,
    normalize_labs_keywords,
    parse_keyword_rows,
)
from matrx_seo.providers.dataforseo.transport import ReplayTransport
from matrx_seo.repository import InMemorySeoRepository
from matrx_seo.service import SeoCollectionService

FIXTURES = Path(__file__).parent / "fixtures" / "dataforseo" / "labs_keywords"


def _fixture(name: str) -> dict[str, Any]:
    return json.loads((FIXTURES / f"{name}.json").read_text())


class _Identities:
    """Identity resolver double: one stable id per (phrase, language), exactly the
    contract the real ``OrmSeoIdentityResolver.resolve_many`` answers."""

    def __init__(self) -> None:
        self.ids: dict[tuple[str, str], str] = {}

    async def resolve_many(self, _request, identities):
        out = []
        for identity in identities:
            key = (identity.keyword.lower(), identity.language)
            self.ids.setdefault(key, str(uuid4()))
            out.append(ResolvedSeoIdentity(keyword_id=self.ids[key]))
        return out

    async def resolve(self, request, identity):
        return (await self.resolve_many(request, [identity]))[0]


async def _credential(*_: object) -> ResolvedCredential:
    return ResolvedCredential(
        values={"DATA_FOR_SEO_EMAIL": "fixture@example.invalid", "DATA_FOR_SEO_PASSWORD": "x"}
    )


async def _authorize(request: CollectionRequest) -> CollectionRequest:
    return request


def _request(operation: str, settings: dict[str, Any]) -> CollectionRequest:
    return CollectionRequest(
        organization_id=str(uuid4()),
        created_by=str(uuid4()),
        capability=SeoCapability.KEYWORD_METRICS,
        operation=operation,
        target_ref="lane-a",
        observation_period="2026-09-28",
        settings=settings,
        execution_id=uuid4(),
    )


@pytest.mark.parametrize("operation", NORMALIZED_OPERATIONS)
def test_the_gate_is_open_for_every_labs_keyword_operation(operation: str) -> None:
    adapter = DataForSeoAdapter()
    assert adapter._normalizers[operation] is normalize_labs_keywords
    assert not hasattr(normalize_labs_keywords, "pending_owner")
    request = _request(
        operation,
        {"workflow": "live", "tasks": [{"keywords": ["seo"], "location_code": 2840}]},
    )
    assert adapter.unsupported_request_reason(request) is None


def test_related_rows_are_unwrapped_with_difficulty_and_provider_intent() -> None:
    body = _fixture("related_data_destruction_us")
    rows = parse_keyword_rows(body["operation"], body["raw"])
    assert len(rows) == 76
    dban = next(r for r in rows if r.phrase == "dban")
    assert dban.difficulty == 15
    assert dban.provider_intent is not None and dban.provider_intent.label == "informational"
    assert dban.location_code == 2840 and dban.search_volume == 3600
    assert all(r.competition_index is None or 0 <= r.competition_index <= 100 for r in rows)
    assert sum(1 for r in rows if r.difficulty is not None) >= 50


def test_an_empty_labs_result_is_zero_rows_not_an_error() -> None:
    body = _fixture("related_empty_seed_us")
    assert parse_keyword_rows(body["operation"], body["raw"]) == []


@pytest.mark.asyncio
async def test_a_labs_collection_runs_through_the_funnel_and_persists_difficulty() -> None:
    body = _fixture("related_data_destruction_us")
    transport = ReplayTransport([body["raw"]])
    adapter = DataForSeoAdapter(transport=transport)
    repository = InMemorySeoRepository()
    identities = _Identities()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credential,
        collection_authorizer=_authorize,
        identity_resolver=identities,
    )
    receipt = await service.collect(adapter, _request(body["operation"], body["settings"]))
    assert [path for _, path, _ in transport.requests] == [
        "/v3/dataforseo_labs/google/related_keywords/live"
    ]
    assert receipt.created_observations == len(repository.keyword_markets) >= 70
    history = [h["observation"] for h in repository.keyword_market_observations.values()]
    dban_id = identities.ids[("dban", "en")]
    assert next(o for o in history if o.keyword_id == dban_id).difficulty == 15


@pytest.mark.asyncio
async def test_keywords_for_keywords_keeps_only_max_items_rows_and_no_difficulty() -> None:
    body = _fixture("keywords_for_keywords_iceland")
    assert len(body["raw"]["tasks"][0]["result"]) > 150
    request = _request(body["operation"], {**body["settings"], "max_items": 150})
    context_run = await InMemorySeoRepository().start_run("dataforseo", request)
    from matrx_seo.contracts import NormalizationContext

    observations = await normalize_labs_keywords(
        ProviderResponse(raw=body["raw"], fetched_at=datetime(2026, 9, 28, tzinfo=UTC)),
        NormalizationContext(
            request=request,
            run=context_run,
            raw_payload_id="raw",
            identity_resolver=_Identities(),
            host_binding_resolver=object(),
        ),
    )
    assert len(observations) == 150
    assert all(o.location_code == 2352 and o.difficulty is None for o in observations)


# --- the orm upsert: a difficulty-only observation never wins the volume fields --


def _obs(keyword_id: str, at: datetime, **fields: Any) -> KeywordMarketObservation:
    return KeywordMarketObservation(keyword_id=keyword_id, location_code=2840, observed_at=at, **fields)


async def _captured_rows(monkeypatch: pytest.MonkeyPatch, observations) -> list[dict[str, Any]]:
    from matrx_seo import orm_repository as orm

    captured: list[dict[str, Any]] = []

    async def fake_upsert(_model, rows, **_kw):
        captured.extend(rows)
        return [{**r, "_matrx_inserted": True} for r in rows]

    async def noop(*_a, **_k):
        return None

    async def history(self, run, raw, obs, base):
        return [str(uuid4()) for _ in obs], [True for _ in obs]

    monkeypatch.setattr(orm, "bulk_upsert_increment", fake_upsert)
    monkeypatch.setattr(orm, "bulk_update_by_pk", noop)
    monkeypatch.setattr(orm.OrmSeoRepository, "_ensure_location_codes", lambda self, codes: noop())
    monkeypatch.setattr(orm.OrmSeoRepository, "_persist_keyword_market_observations_batch", history)
    request = _request("labs.google.bulk_keyword_difficulty", {"workflow": "live", "tasks": [{}]})
    run = await InMemorySeoRepository().start_run("dataforseo", request)
    repo = orm.OrmSeoRepository.__new__(orm.OrmSeoRepository)
    await repo._upsert_keyword_markets_batch(run, object(), observations, {})
    return captured


@pytest.mark.asyncio
async def test_difficulty_only_observation_does_not_win_the_volume_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    t1 = datetime(2026, 9, 28, 12, tzinfo=UTC)
    volume = _obs(
        "kw-1", t1, search_volume=1000, cpc=19.76,
        monthly_searches=[MonthlySearch(year=2026, month=8, search_volume=1000)],
    )
    difficulty_only = _obs("kw-1", t1 + timedelta(minutes=5), difficulty=27)
    [row] = await _captured_rows(monkeypatch, [volume, difficulty_only])
    assert row["search_volume"] == 1000
    assert row["last_observed_at"] == t1
    assert row["difficulty"] == 27


@pytest.mark.asyncio
async def test_a_group_of_only_difficulty_is_never_authoritative_for_volume(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    [row] = await _captured_rows(
        monkeypatch, [_obs("kw-2", datetime(2026, 9, 28, tzinfo=UTC), difficulty=40)]
    )
    # NULL last_observed_at: the SQL guard never lets this row overwrite a stored
    # volume (Excluded(last_observed_at) >= current is NULL, i.e. not true).
    assert row["last_observed_at"] is None
    assert row["difficulty"] == 40
