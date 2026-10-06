"""Failure cases for source reconciliation and measured redirect truth."""

import httpx
import pytest

from matrx_seo.domain_redirects import RedirectSettings, check_redirects
from matrx_seo.owned_domains import (
    DomainInventory,
    DomainSource,
    OwnedDomain,
    discover_domains,
    merge_inventory,
    normalize_domain,
)

SETTINGS = RedirectSettings(
    timeout_seconds=2,
    max_bytes=10000,
    max_hops=4,
    concurrency=2,
    similarity_threshold=0.9,
    minimum_content_words=10,
)
HTML = b"<html><body>" + b" ".join(f"word{i}".encode() for i in range(100)) + b"</body></html>"


@pytest.mark.asyncio
@pytest.mark.parametrize("broken", [200, 302, 307, 404, "loop", "wrong", "timeout", 403])
async def test_noncanonical_break_cannot_pass(broken):
    def route(request):
        if request.url.host == "canonical.example":
            return httpx.Response(200, content=HTML, headers={"content-type": "text/html"})
        if broken == "timeout":
            raise httpx.ReadTimeout("test timeout")
        if broken in {"loop", "wrong"}:
            return httpx.Response(
                301,
                headers={
                    "location": str(request.url) if broken == "loop" else "https://wrong.example/"
                },
            )
        if broken in {302, 307}:
            return httpx.Response(broken, headers={"location": "https://canonical.example/"})
        return httpx.Response(broken, content=HTML, headers={"content-type": "text/html"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(route)) as http:
        result = await check_redirects(
            "https://canonical.example",
            ["duplicate.example"],
            observed_at="2026-10-05",
            settings=SETTINGS,
            http=http,
        )
    assert result.status == ("error" if broken in {"timeout", 403} else "fail")
    if broken == 200:
        assert all(variant.duplicate is True for variant in result.variants)


@pytest.mark.asyncio
async def test_permanent_repair_clears_and_temporary_hop_remains_failed():
    def route(request):
        if request.url.host == "canonical.example":
            return httpx.Response(200, content=HTML, headers={"content-type": "text/html"})
        return httpx.Response(308, headers={"location": "https://canonical.example/"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(route)) as http:
        result = await check_redirects(
            "https://canonical.example",
            ["duplicate.example"],
            observed_at="2026-10-05",
            settings=SETTINGS,
            http=http,
        )
    assert result.status == "pass"
    assert len(result.variants) == 4


@pytest.mark.asyncio
async def test_truncated_or_tiny_content_never_claims_duplicate():
    def route(request):
        return httpx.Response(
            200, content=b"<html>Login</html>", headers={"content-type": "text/html"}
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(route)) as http:
        result = await check_redirects(
            "https://canonical.example",
            ["duplicate.example"],
            observed_at="2026-10-05",
            settings=SETTINGS,
            http=http,
        )
    assert result.status == "fail"
    assert all(row.duplicate is None for row in result.variants)


def test_complete_refresh_retires_only_its_source_and_partial_retains_it():
    sources = [
        DomainSource(
            provider=provider,
            connection_id=connection,
            resource_ref="one",
            observed_at="yesterday",
            basis="dns_zone" if provider == "cloudflare" else "manual",
        )
        for provider, connection in [("cloudflare", "a"), ("manual", None), ("cloudflare", "b")]
    ]
    existing = [OwnedDomain(domain="example.com", sources=sources)]
    inventory = DomainInventory(provider="cloudflare", observed_at="today", complete=False)
    assert all(s.state == "current" for s in merge_inventory(existing, inventory, "a")[0].sources)
    inventory.complete = True
    assert [s.state for s in merge_inventory(existing, inventory, "a")[0].sources] == [
        "stale",
        "current",
        "current",
    ]


def test_domain_normalizes_idna_case_and_trailing_dot():
    assert normalize_domain("HTTPS://BÜCHER.EXAMPLE./") == "xn--bcher-kva.example"
    for address in [
        "127.0.0.1",
        "localhost",
        "https://user:secret@example.com",
        "example.com:8080",
    ]:
        with pytest.raises(ValueError):
            normalize_domain(address)


@pytest.mark.asyncio
async def test_cloudflare_pagination_truncation_and_dns_authority_not_host_claim():
    def route(request):
        if request.url.path.endswith("dns_records"):
            return httpx.Response(
                200,
                json={
                    "success": True,
                    "result": [
                        {"type": "CNAME", "name": "www.example.com", "content": "host.example.net"}
                    ],
                    "result_info": {"total_pages": 2},
                },
            )
        return httpx.Response(
            200,
            json={
                "success": True,
                "result": [
                    {"id": "zone", "name": "example.com", "name_servers": ["ns.cloudflare.com"]}
                ],
                "result_info": {"total_pages": 2},
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(route)) as http:
        inventory = await discover_domains(
            "cloudflare",
            {"api_token": "fake"},
            connection_id="a",
            observed_at="today",
            page_budget=1,
            detail_budget=1,
            http=http,
        )
    assert inventory.complete is False
    assert inventory.domains[0].sources[0].basis == "dns_zone"
    assert inventory.domains[0].sources[0].details_complete is False
    assert inventory.domains[0].sources[0].dns_records[0]["value"] == "host.example.net"


@pytest.mark.asyncio
async def test_branded_search_candidate_is_not_owned_without_matching_content():
    def route(request):
        content = (
            HTML
            if request.url.host == "canonical.example"
            else b"<html>" + b" unrelated " * 50 + b"</html>"
        )
        return httpx.Response(200, content=content, headers={"content-type": "text/html"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(route)) as http:
        result = await check_redirects(
            "https://canonical.example",
            [],
            external_candidates=["unrelated.example"],
            observed_at="today",
            settings=SETTINGS,
            http=http,
        )
    assert result.status == "pass"
    assert all(v.duplicate is False for v in result.variants)


@pytest.mark.asyncio
async def test_malformed_inventory_cannot_retire_existing_domains():
    from matrx_seo.owned_domains import DomainProviderError

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _: httpx.Response(200, json={"success": True}))
    ) as http:
        with pytest.raises(DomainProviderError, match="unreadable domain list"):
            await discover_domains(
                "cloudflare",
                {"api_token": "fake"},
                connection_id="a",
                observed_at="today",
                page_budget=2,
                detail_budget=1,
                http=http,
            )


@pytest.mark.asyncio
@pytest.mark.parametrize("rows", [[{}], [None], [{"id": "zone"}]])
async def test_malformed_domain_row_is_safe_refusal(rows):
    from matrx_seo.owned_domains import DomainProviderError

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda _: httpx.Response(200, json={"success": True, "result": rows})
        )
    ) as http:
        with pytest.raises(DomainProviderError):
            await discover_domains(
                "cloudflare",
                {"api_token": "fake"},
                connection_id="a",
                observed_at="today",
                page_budget=1,
                detail_budget=1,
                http=http,
            )


@pytest.mark.asyncio
async def test_unreadable_dns_keeps_domain_and_announces_partial_details():
    def route(request):
        if request.url.path.endswith("dns_records"):
            return httpx.Response(200, json={"result": [None]})
        return httpx.Response(
            200, json={"success": True, "result": [{"id": "zone", "name": "example.com"}]}
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(route)) as http:
        result = await discover_domains(
            "cloudflare",
            {"api_token": "fake"},
            connection_id="a",
            observed_at="today",
            page_budget=1,
            detail_budget=1,
            http=http,
        )
    assert result.complete
    assert result.domains[0].domain == "example.com"
    assert not result.domains[0].sources[0].details_complete
    assert result.warnings == ["cloudflare: DNS details unreadable."]


@pytest.mark.asyncio
async def test_cloudflare_multiple_accounts_identity_order_independent():
    for accounts in [("one", "two"), ("two", "one")]:
        body = {
            "success": True,
            "result": [
                {
                    "id": account,
                    "name": account + ".example",
                    "account": {"id": account, "name": account.title()},
                }
                for account in accounts
            ],
        }
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(lambda _: httpx.Response(200, json=body))
        ) as http:
            inventory = await discover_domains(
                "cloudflare",
                {"api_token": "fake"},
                connection_id="a",
                observed_at="today",
                page_budget=1,
                detail_budget=0,
                http=http,
            )
        assert inventory.account_ref == "accounts:one,two"
        assert inventory.account_label == "One, Two"
