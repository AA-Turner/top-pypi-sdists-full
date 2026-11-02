"""Account, catalog, describe, and agent-signup mapping (SPEC 2.7, 3.7)."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import cast

import httpx
import pytest

from conftest import json_response, make_async_client, make_sync_client
from getanyapi import (
    AnyAPIError,
    DiscoveryPricing,
    FlatPricingOffer,
    LinearPricingOffer,
    NotFoundError,
    agent_signup,
)

GOLDEN_PATH = Path(__file__).parents[3] / "testdata" / "discovery-v1.json"
DISCOVERY_GOLDEN = cast("dict[str, object]", json.loads(GOLDEN_PATH.read_text()))


def clone_record(value: object) -> dict[str, object]:
    return cast("dict[str, object]", deepcopy(value))


def golden_rest() -> dict[str, object]:
    return cast("dict[str, object]", DISCOVERY_GOLDEN["rest"])


def discovery_browse() -> dict[str, object]:
    return clone_record(golden_rest()["browse"])


def discovery_api() -> dict[str, object]:
    apis = cast("list[object]", discovery_browse()["apis"])
    return clone_record(apis[0])


def flat_discovery_api() -> dict[str, object]:
    apis = cast("list[object]", discovery_browse()["apis"])
    return clone_record(apis[1])


def discovery_search() -> dict[str, object]:
    return clone_record(golden_rest()["search"])


def discovery_detail(slug: str = "linear.data") -> dict[str, object]:
    details = cast("dict[str, object]", golden_rest()["detail"])
    return clone_record(details[slug])


def discovery_latency() -> dict[str, object]:
    return clone_record(discovery_detail()["latency"])


@pytest.mark.parametrize("value", [float("inf"), float("nan")], ids=["inf", "nan"])
@pytest.mark.parametrize(
    ("model", "field"),
    [
        (FlatPricingOffer, "maxUsd"),
        (FlatPricingOffer, "maxPer1kUsd"),
        (LinearPricingOffer, "baseUsd"),
        (LinearPricingOffer, "perUnitUsd"),
        (DiscoveryPricing, "failoverMaxUsd"),
        (DiscoveryPricing, "failoverMaxPer1kUsd"),
    ],
    ids=[
        "max-usd",
        "max-per-1k-usd",
        "base-usd",
        "per-unit-usd",
        "failover-max-usd",
        "failover-max-per-1k-usd",
    ],
)
def test_discovery_pricing_rejects_non_finite_usd_values(
    model: type[FlatPricingOffer | LinearPricingOffer | DiscoveryPricing],
    field: str,
    value: float,
) -> None:
    if model is FlatPricingOffer:
        raw: dict[str, object] = {
            "model": "flat",
            "unit": "request",
            "maxUsd": 0.00325,
            "maxPer1kUsd": 3.25,
        }
    elif model is LinearPricingOffer:
        raw = {
            "model": "linear",
            "unit": "result",
            "baseUsd": 0.00005,
            "perUnitUsd": 0.0008,
            "maxUsd": 0.04002,
            "maxPer1kUsd": 40.02,
        }
    else:
        raw = {
            "from": {
                "model": "flat",
                "unit": "request",
                "maxUsd": 0.00325,
                "maxPer1kUsd": 3.25,
            },
            "failoverMaxUsd": 0.00325,
            "failoverMaxPer1kUsd": 3.25,
        }
    raw[field] = value
    with pytest.raises(ValueError, match="finite_number"):
        model.model_validate(raw)


def test_balance() -> None:
    def respond(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/v1/balance"
        return json_response(200, {"usd": 12.34})

    client, _ = make_sync_client(respond)
    bal = client.balance()
    assert bal.usd == 12.34


def test_me_drops_internal_fields() -> None:
    def respond(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/v1/me"
        return json_response(
            200,
            {
                "id": "acct_1",
                "email": "a@b.com",
                "status": "active",
                "createdAt": "2026-01-01T00:00:00Z",
                "onboardingComplete": True,
                "clerkUserId": "user_x",
                "signupGrantApplied": True,
            },
        )

    client, _ = make_sync_client(respond)
    profile = client.me()
    assert profile.id == "acct_1"
    assert profile.email == "a@b.com"
    assert profile.status == "active"
    assert profile.created_at == "2026-01-01T00:00:00Z"
    assert profile.onboarding_complete is True
    # Internal fields are dropped from the public model.
    assert not hasattr(profile, "clerk_user_id")
    assert not hasattr(profile, "signup_grant_applied")


def test_catalog_reads_every_shared_browse_field() -> None:
    body = discovery_browse()

    def respond(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/v1/apis"
        assert "query" not in req.url.params
        assert req.url.params["category"] == "data"
        return json_response(200, body)

    client, _ = make_sync_client(respond)
    entries = client.catalog(category="data")
    assert [
        entry.model_dump(by_alias=True, exclude_defaults=True) for entry in entries
    ] == body["apis"]


def test_catalog_rejects_legacy_partial_contract() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, {"apis": [{"slug": "x.y"}]})

    client, _ = make_sync_client(respond)
    with pytest.raises(ValueError):
        client.catalog()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("method", "GET"),
        ("path", "operations/linear.data"),
        ("execution", {"mode": "async"}),
    ],
)
def test_catalog_rejects_malformed_operation_authority(
    field: str, value: object
) -> None:
    api = discovery_api()
    api[field] = value
    client, _ = make_sync_client(lambda _req: json_response(200, {"apis": [api]}))
    with pytest.raises(ValueError):
        client.catalog()


def test_catalog_normalizes_omitted_heavy_and_rejects_non_boolean() -> None:
    omitted = flat_discovery_api()
    assert "heavy" not in omitted
    client, _ = make_sync_client(lambda _req: json_response(200, {"apis": [omitted]}))
    assert client.catalog()[0].heavy is False

    malformed = {**flat_discovery_api(), "heavy": "false"}
    client, _ = make_sync_client(lambda _req: json_response(200, {"apis": [malformed]}))
    with pytest.raises(ValueError):
        client.catalog()


def test_catalog_accepts_safe_additions_and_gateway_owned_disagreements() -> None:
    api = discovery_api()
    api["unexpected"] = True
    lanes = cast("list[dict[str, object]]", api["lanes"])
    lane = clone_record(lanes[1])
    lane["source"] = {**cast("dict[str, object]", lane["source"]), "unexpected": True}
    lane["health"] = {
        **cast("dict[str, object]", lanes[0]["health"]),
        "unexpected": True,
    }
    lane["unexpected"] = True
    api["lanes"] = [lane]
    pricing = cast("dict[str, object]", api["pricing"])
    pricing["failoverMaxUsd"] = 0.004
    pricing["unexpected"] = True
    offer = cast("dict[str, object]", pricing["from"])
    offer["maxUsd"] = 0.02
    offer["unexpected"] = True
    client, _ = make_sync_client(
        lambda _req: json_response(200, {"apis": [api], "unexpected": True})
    )
    entry = client.catalog()[0]
    assert entry.slug == "linear.data"
    assert entry.pricing.from_offer.max_usd == pytest.approx(0.02)
    assert entry.pricing.failover_max_usd == pytest.approx(0.004)
    assert entry.lanes[0].pricing.model == "flat"
    assert entry.lanes[0].health is not None
    assert entry.lanes[0].health.window == "30d"
    assert entry.failover is True
    assert entry.excludes_caller_delay is True
    assert entry.model_extra is None
    assert entry.pricing.model_extra is None
    assert entry.pricing.from_offer.model_extra is None


def test_catalog_accepts_empty_lanes_and_older_optional_field_shape() -> None:
    api = discovery_api()
    api["lanes"] = []
    del api["failover"]
    del api["excludesCallerDelay"]
    client, _ = make_sync_client(lambda _req: json_response(200, {"apis": [api]}))
    entry = client.catalog()[0]
    assert entry.lanes == []
    assert entry.failover is None
    assert entry.excludes_caller_delay is None


def per1k_discovery_api() -> dict[str, object]:
    """A browse row priced like production booking.search: 0.0966 -> 96.6 per 1,000."""
    api = discovery_api()
    pricing = cast("dict[str, object]", api["pricing"])
    offer = cast("dict[str, object]", pricing["from"])
    offer["maxUsd"] = 0.0966
    offer["maxPer1kUsd"] = 96.6
    pricing["failoverMaxUsd"] = 0.0966
    pricing["failoverMaxPer1kUsd"] = 96.6
    lanes = cast("list[dict[str, object]]", api["lanes"])
    api["lanes"] = [{**lanes[0], "pricing": clone_record(offer)}]
    return api


def test_catalog_reads_published_per_1k_rate_without_multiplying() -> None:
    # 0.0966 * 1000 is 96.60000000000001 in Python, so the reader must take the
    # gateway's published maxPer1kUsd verbatim.
    assert 0.0966 * 1000 != 96.6
    api = per1k_discovery_api()
    client, _ = make_sync_client(lambda _req: json_response(200, {"apis": [api]}))
    entry = client.catalog()[0]
    assert entry.pricing.from_offer.max_usd == 0.0966
    assert entry.pricing.from_offer.max_per1k_usd == 96.6
    assert entry.pricing.failover_max_per1k_usd == 96.6
    assert entry.lanes[0].pricing.max_per1k_usd == 96.6


@pytest.mark.parametrize(
    ("scope", "key"),
    [("from", "maxPer1kUsd"), ("wrapper", "failoverMaxPer1kUsd")],
)
def test_catalog_rejects_pricing_without_the_per_1k_rate(scope: str, key: str) -> None:
    api = per1k_discovery_api()
    pricing = cast("dict[str, object]", api["pricing"])
    target = cast("dict[str, object]", pricing["from"]) if scope == "from" else pricing
    del target[key]
    client, _ = make_sync_client(lambda _req: json_response(200, {"apis": [api]}))
    with pytest.raises(ValueError, match=key):
        client.catalog()


@pytest.mark.parametrize(
    ("unsafe", "message"),
    [
        ({"creditBalance": 1}, "catalog.apis[0].future.creditBalance"),
        ({"provider": "upstream"}, "catalog.apis[0].future.provider"),
    ],
)
def test_catalog_rejects_unsafe_fields_before_projection(
    unsafe: dict[str, object], message: str
) -> None:
    api = discovery_api()
    api["future"] = unsafe
    client, _ = make_sync_client(lambda _req: json_response(200, {"apis": [api]}))
    with pytest.raises(ValueError, match=message.replace("[", r"\[")):
        client.catalog()


def test_search_reads_every_shared_ranked_field_and_forwards_filters() -> None:
    body = discovery_search()

    def respond(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/catalog/search"
        assert dict(req.url.params) == {
            "q": "data",
            "category": "data",
            "platform": "linear",
            "limit": "2",
        }
        return json_response(200, body)

    client, _ = make_sync_client(respond)
    found = client.search(query="data", category="data", platform="linear", limit=2)
    assert found.model_dump(by_alias=True, exclude_defaults=True) == body


def test_search_scopes_without_a_query_and_omits_q_entirely() -> None:
    body = discovery_search()

    def respond(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/catalog/search"
        assert dict(req.url.params) == {"platform": "reddit"}
        return json_response(200, body)

    client, _ = make_sync_client(respond)
    assert client.search(platform="reddit").results


def test_search_omits_an_empty_query_rather_than_sending_it_empty() -> None:
    body = discovery_search()

    def respond(req: httpx.Request) -> httpx.Response:
        assert "q" not in dict(req.url.params)
        return json_response(200, body)

    client, _ = make_sync_client(respond)
    assert client.search(query="", category="social").results


def test_search_without_query_category_or_platform_never_calls_the_gateway() -> None:
    client, recorder = make_sync_client(
        lambda _req: json_response(200, discovery_search())
    )
    with pytest.raises(
        AnyAPIError, match="at least one of query, category, or platform"
    ):
        client.search(limit=5)
    assert recorder.requests == []


def test_search_drops_safe_additive_result_and_envelope_fields() -> None:
    body = discovery_search()
    results = cast("list[dict[str, object]]", body["results"])
    result = clone_record(results[0])
    pricing = cast("dict[str, object]", result["pricing"])
    pricing["future"] = True
    pricing["from"] = {
        **cast("dict[str, object]", pricing["from"]),
        "future": True,
    }
    result["lanes"] = discovery_api()["lanes"]
    result["future"] = True
    result["highlightFields"] = [
        {
            "path": "items[].title",
            "type": "string",
            "why": "title",
            "future": True,
        }
    ]
    body.update(
        {"results": [result], "total": 1, "ranking": "keyword", "unexpected": True}
    )
    client, _ = make_sync_client(lambda _req: json_response(200, body))
    found = client.search(query="x")
    assert len(found.results) == 1
    assert found.model_extra is None
    assert found.results[0].model_extra is None
    assert found.results[0].pricing.model_extra is None
    assert found.results[0].pricing.from_offer.model_extra is None
    assert found.results[0].highlight_fields is not None
    assert [
        field.model_dump(by_alias=True) for field in found.results[0].highlight_fields
    ] == [{"path": "items[].title", "type": "string", "why": "title"}]
    assert found.results[0].highlight_fields[0].model_extra is None


def test_describe_reads_every_shared_populated_and_nullable_field() -> None:
    linear = discovery_detail()
    flat = discovery_detail("flat.data")

    def respond(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/v1/apis/linear.data":
            return json_response(200, linear)
        assert req.url.path == "/v1/apis/flat.data"
        return json_response(200, flat)

    client, _ = make_sync_client(respond)
    described = client.describe("linear.data")
    assert described.model_dump(by_alias=True, exclude_defaults=True) == linear

    described_flat = client.describe("flat.data")
    flat_dump = described_flat.model_dump(by_alias=True, exclude_defaults=True)
    flat_dump["latency"] = described_flat.latency
    assert flat_dump == flat


def test_describe_accepts_gateway_owned_pricing_and_lane_disagreement() -> None:
    api = discovery_detail()
    pricing = cast("dict[str, object]", api["pricing"])
    offer = cast("dict[str, object]", pricing["from"])
    pricing["failoverMaxUsd"] = offer["maxUsd"]
    api["latency"] = None
    client, _ = make_sync_client(lambda _req: json_response(200, api))
    entry = client.describe("linear.data")
    assert entry.pricing.failover_max_usd == offer["maxUsd"]
    assert entry.lanes[2].pricing.max_usd > entry.pricing.failover_max_usd
    assert entry.latency is None


def test_describe_rejects_missing_schemas() -> None:
    client, _ = make_sync_client(lambda _req: json_response(200, discovery_api()))
    with pytest.raises(ValueError, match="detail schemas are required"):
        client.describe("linear.data")


def test_describe_requires_nullable_latency_and_validates_complete_shape() -> None:
    api = discovery_detail()
    del api["latency"]
    client, _ = make_sync_client(lambda _req: json_response(200, api))
    with pytest.raises(ValueError, match="detail latency is required"):
        client.describe("linear.data")

    api["latency"] = {**discovery_latency(), "p95Ms": "invalid"}
    client, _ = make_sync_client(lambda _req: json_response(200, api))
    with pytest.raises(ValueError, match="p95Ms"):
        client.describe("linear.data")


def test_describe_404_raises_not_found() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(404, {"error": "no such sku"})

    client, _ = make_sync_client(respond)
    with pytest.raises(NotFoundError):
        client.describe("nope.gone")


SIGNUP_BODY: dict[str, object] = {"secret": "sk_live_x", "capUsd": 0.15, "keyId": "key_1"}
# The gateway still sends these retired claim-flow fields until it drops them.
RETIRED_SIGNUP_FIELDS: dict[str, object] = {
    "verificationStatus": "pending",
    "claimToken": "",
    "claimUrl": "https://getanyapi.com/dashboard",
}


@pytest.mark.parametrize(
    "body",
    [SIGNUP_BODY, {**SIGNUP_BODY, **RETIRED_SIGNUP_FIELDS}],
    ids=["without-retired-fields", "with-retired-fields"],
)
def test_agent_signup_maps_result(
    monkeypatch: pytest.MonkeyPatch, body: dict[str, object]
) -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["auth"] = request.headers.get("authorization")
        captured["body"] = json.loads(request.content)
        return json_response(200, body)

    transport = httpx.MockTransport(handler)
    import getanyapi._client as client_mod

    real_client = httpx.Client

    def fake_client(*_a: object, **_k: object) -> httpx.Client:
        return real_client(transport=transport)

    monkeypatch.setattr(client_mod.httpx, "Client", fake_client)
    result = agent_signup(sponsor_email="me@x.com", label="bot")

    assert captured["path"] == "/agent/signup"
    assert captured["auth"] is None  # no auth header on signup
    assert captured["body"] == {"sponsorEmail": "me@x.com", "label": "bot"}
    assert result.secret == "sk_live_x"
    assert result.cap_usd == 0.15


async def test_async_account() -> None:
    def respond(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/v1/balance":
            return json_response(200, {"usd": 5.0})
        return json_response(
            200,
            {
                "id": "a",
                "status": "active",
                "createdAt": "t",
                "onboardingComplete": False,
            },
        )

    client, _ = make_async_client(respond)
    assert (await client.balance()).usd == 5.0
    assert (await client.me()).onboarding_complete is False
    await client.aclose()


async def test_async_discovery_methods() -> None:
    browse = discovery_browse()
    search = discovery_search()
    detail = discovery_detail()

    def respond(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/v1/apis":
            return json_response(200, browse)
        if req.url.path == "/catalog/search":
            return json_response(200, search)
        return json_response(200, detail)

    client, _ = make_async_client(respond)
    assert (await client.catalog(category="data"))[0].slug == "linear.data"
    assert (await client.search(query="data")).ranking == "semantic"
    assert (await client.describe("linear.data")).input_schema is not None
    await client.aclose()
