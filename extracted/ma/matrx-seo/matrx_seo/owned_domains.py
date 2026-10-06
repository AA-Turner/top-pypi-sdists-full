"""Owned-domain provider evidence and reconciliation, independent of host credentials.

An account inventory is a candidate list, not an assertion that every domain serves
one customer's site. Hosting, DNS and registrar observations remain distinct.
"""

from __future__ import annotations

import ipaddress
import math
import xml.etree.ElementTree as ET
from typing import Any, Literal
from urllib.parse import urlsplit

import httpx
import tldextract
from pydantic import BaseModel, Field

DomainProvider = Literal["vercel", "cloudflare", "name_com", "godaddy", "namecheap"]
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "vercel": ("api_token",),
    "cloudflare": ("api_token",),
    "name_com": ("username", "api_token"),
    "godaddy": ("api_key", "api_secret"),
    "namecheap": ("api_user", "api_key", "username", "client_ip"),
}


class DomainSource(BaseModel):
    provider: str
    connection_id: str | None = None
    resource_ref: str
    observed_at: str
    basis: Literal["dns_zone", "host_account", "registrar", "manual", "brand_search"]
    state: Literal["current", "stale"] = "current"
    nameservers: list[str] = Field(default_factory=list)
    dns_records: list[dict[str, str]] = Field(default_factory=list)
    details_complete: bool = True


class OwnedDomain(BaseModel):
    domain: str
    sources: list[DomainSource] = Field(default_factory=list)


class DomainInventory(BaseModel):
    provider: DomainProvider
    account_ref: str | None = None
    account_label: str | None = None
    domains: list[OwnedDomain] = Field(default_factory=list)
    complete: bool = True
    pages: int = 0
    observed_at: str
    warnings: list[str] = Field(default_factory=list)


class DomainProviderError(RuntimeError):
    """A safe provider error, never a URL carrying credentials."""


def normalize_domain(value: str) -> str:
    raw = value.strip()
    parts = urlsplit(raw if "://" in raw else "//" + raw)
    if parts.username or parts.password or parts.port or not parts.hostname:
        raise ValueError("Enter a domain without credentials or a port.")
    host = parts.hostname.rstrip(".").encode("idna").decode("ascii").lower()
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("Enter a public domain, not an IP address.")
    if "." not in host or any(
        not label
        or len(label) > 63
        or label.startswith("-")
        or label.endswith("-")
        or not all(c.isalnum() or c == "-" for c in label)
        for label in host.split(".")
    ):
        raise ValueError("Enter a valid public domain.")
    return host


def merge_inventory(
    existing: list[OwnedDomain], inventory: DomainInventory, connection_id: str
) -> list[OwnedDomain]:
    """Replace just this source; only complete inventories can retire omissions."""
    merged = {row.domain: row.model_copy(deep=True) for row in existing}
    observed = {row.domain for row in inventory.domains}
    if inventory.complete:
        for row in merged.values():
            if row.domain not in observed:
                for source in row.sources:
                    if (
                        source.provider == inventory.provider
                        and source.connection_id == connection_id
                    ):
                        source.state = "stale"
    for row in inventory.domains:
        current = merged.setdefault(row.domain, OwnedDomain(domain=row.domain))
        for source in row.sources:
            current.sources = [
                old
                for old in current.sources
                if not (
                    old.provider == source.provider
                    and old.connection_id == source.connection_id
                    and old.resource_ref == source.resource_ref
                )
            ] + [source]
    return sorted(merged.values(), key=lambda row: row.domain)


async def _discover_domains(
    provider: DomainProvider,
    fields: dict[str, str],
    *,
    connection_id: str,
    observed_at: str,
    page_budget: int,
    detail_budget: int,
    http: httpx.AsyncClient,
) -> DomainInventory:
    missing = [key for key in REQUIRED_FIELDS[provider] if not fields.get(key)]
    if missing:
        raise ValueError("Vault credential needs fields: " + ", ".join(missing))
    result = DomainInventory(provider=provider, observed_at=observed_at)

    async def request(url: str, **kwargs: Any) -> dict[str, Any] | list[Any]:
        try:
            response = await http.get(url, **kwargs)
        except httpx.HTTPError as exc:
            raise DomainProviderError(
                f"{provider}: {type(exc).__name__}; refresh to retry."
            ) from None
        if response.status_code != 200:
            raise DomainProviderError(f"{provider} returned HTTP {response.status_code}.")
        try:
            payload = response.json()
        except ValueError:
            raise DomainProviderError(f"{provider} returned an unreadable response.") from None
        if isinstance(payload, dict) and payload.get("success") is False:
            raise DomainProviderError(f"{provider} refused the request.")
        expected = {"cloudflare": "result", "vercel": "domains", "name_com": "domains"}
        if url.endswith("/zones") or url.endswith("/domains") and provider != "godaddy":
            key = expected[provider]
            if not isinstance(payload, dict) or not isinstance(payload.get(key), list):
                raise DomainProviderError(f"{provider} returned an unreadable domain list.")
        return payload

    def add(domain: str, resource: str, basis: str, nameservers: list[str] | None = None) -> None:
        result.domains.append(
            OwnedDomain(
                domain=normalize_domain(domain),
                sources=[
                    DomainSource(
                        provider=provider,
                        connection_id=connection_id,
                        resource_ref=resource,
                        observed_at=observed_at,
                        basis=basis,
                        nameservers=nameservers or [],
                    )
                ],
            )
        )

    headers = {"Authorization": f"Bearer {fields.get('api_token', '')}"}
    if provider == "cloudflare":
        accounts: dict[str, str] = {}
        for page in range(1, page_budget + 1):
            payload = await request(
                "https://api.cloudflare.com/client/v4/zones",
                headers=headers,
                params={"page": page, "per_page": 50},
            )
            result.pages = page
            for zone in payload.get("result", []):
                account = zone.get("account", {})
                if account.get("id"):
                    accounts[account["id"]] = account.get("name") or account["id"]
                add(zone["name"], zone["id"], "dns_zone", zone.get("name_servers", []))
            if page >= payload.get("result_info", {}).get("total_pages", 1):
                break
        else:
            result.complete = False
        if accounts:
            identities = sorted(accounts)
            result.account_ref = (
                identities[0] if len(identities) == 1 else "accounts:" + ",".join(identities)
            )
            result.account_label = ", ".join(accounts[key] for key in identities)
    elif provider == "vercel":
        identity = await request("https://api.vercel.com/v2/user", headers=headers)
        result.account_ref = fields.get("team_id") or identity["user"]["id"]
        result.account_label = identity["user"].get("username")
        cursor = None
        for page in range(1, page_budget + 1):
            params = {"limit": 100}
            if fields.get("team_id"):
                params["teamId"] = fields["team_id"]
            if cursor:
                params["until"] = cursor
            payload = await request(
                "https://api.vercel.com/v5/domains", headers=headers, params=params
            )
            result.pages = page
            for domain in payload.get("domains", []):
                add(domain["name"], domain["name"], "host_account")
            cursor = payload.get("pagination", {}).get("next")
            if not cursor:
                break
        else:
            result.complete = False
    elif provider == "name_com":
        result.account_ref = fields["username"]
        result.account_label = fields["username"]
        for page in range(1, page_budget + 1):
            payload = await request(
                "https://api.name.com/core/v1/domains",
                auth=(fields["username"], fields["api_token"]),
                params={"page": page, "perPage": 100},
            )
            result.pages = page
            for domain in payload.get("domains", []):
                add(
                    domain["domainName"],
                    domain["domainName"],
                    "registrar",
                    domain.get("nameservers", []),
                )
            if not payload.get("nextPage"):
                break
        else:
            result.complete = False
    elif provider == "godaddy":
        headers = {"Authorization": f"sso-key {fields['api_key']}:{fields['api_secret']}"}
        marker = None
        for page in range(1, page_budget + 1):
            params = {"limit": 1000}
            if marker:
                params["marker"] = marker
            payload = await request(
                "https://api.godaddy.com/v1/domains", headers=headers, params=params
            )
            if not isinstance(payload, list):
                raise DomainProviderError("GoDaddy returned an unreadable domain list.")
            result.pages = page
            for domain in payload:
                add(domain["domain"], domain["domain"], "registrar", domain.get("nameServers", []))
            if len(payload) < 1000:
                break
            marker = payload[-1]["domain"]
        else:
            result.complete = False
    else:
        result.account_ref = fields["api_user"]
        result.account_label = fields["username"]
        # Namecheap's API requires query authentication. Never report/log a request URL.
        params = {
            "ApiUser": fields["api_user"],
            "ApiKey": fields["api_key"],
            "UserName": fields["username"],
            "ClientIp": fields["client_ip"],
            "Command": "namecheap.domains.getList",
            "PageSize": 100,
        }
        for page in range(1, page_budget + 1):
            try:
                response = await http.get(
                    "https://api.namecheap.com/xml.response", params={**params, "Page": page}
                )
                response.raise_for_status()
                root = ET.fromstring(response.content)
            except (httpx.HTTPError, ET.ParseError) as exc:
                raise DomainProviderError(f"Namecheap: {type(exc).__name__}.") from None
            if root.attrib.get("Status") != "OK":
                errors = root.findall(".//{*}Error")
                codes = ", ".join(e.attrib.get("Number", "unknown") for e in errors)
                raise DomainProviderError(f"Namecheap refused the request (codes {codes}).")
            for domain in root.findall(".//{*}Domain"):
                add(domain.attrib["Name"], domain.attrib["ID"], "registrar")
            result.pages = page
            total = int(root.findtext(".//{*}TotalItems", "0"))
            if page >= math.ceil(total / 100):
                break
        else:
            result.complete = False

    # DNS is evidence of a destination, never proof of the web host itself.
    for row in result.domains[:detail_budget]:
        source = row.sources[0]
        try:
            if provider == "cloudflare":
                payload = await request(
                    f"https://api.cloudflare.com/client/v4/zones/{source.resource_ref}/dns_records",
                    headers=headers,
                    params={"per_page": 100},
                )
                records = payload.get("result", [])
                source.details_complete = payload.get("result_info", {}).get("total_pages", 1) == 1
            elif provider == "vercel":
                payload = await request(
                    f"https://api.vercel.com/v4/domains/{row.domain}/records",
                    headers=headers,
                    params={"teamId": fields["team_id"]} if fields.get("team_id") else {},
                )
                records = payload.get("records", [])
                source.details_complete = not bool(payload.get("pagination", {}).get("next"))
            elif provider == "name_com":
                payload = await request(
                    f"https://api.name.com/core/v1/domains/{row.domain}/records",
                    auth=(fields["username"], fields["api_token"]),
                    params={"perPage": 100},
                )
                records = payload.get("records", [])
                source.details_complete = not bool(payload.get("nextPage"))
            elif provider == "godaddy":
                records = await request(
                    f"https://api.godaddy.com/v1/domains/{row.domain}/records", headers=headers
                )
            else:
                suffix = tldextract.TLDExtract(suffix_list_urls=())(row.domain)
                try:
                    response = await http.get(
                        "https://api.namecheap.com/xml.response",
                        params={
                            **params,
                            "Command": "namecheap.domains.dns.getHosts",
                            "SLD": suffix.domain,
                            "TLD": suffix.suffix,
                        },
                    )
                    response.raise_for_status()
                    root = ET.fromstring(response.content)
                except (httpx.HTTPError, ET.ParseError) as exc:
                    raise DomainProviderError(f"Namecheap DNS: {type(exc).__name__}.") from None
                if root.attrib.get("Status") != "OK":
                    raise DomainProviderError("Namecheap refused DNS discovery.")
                records = [
                    {
                        "type": node.attrib.get("Type"),
                        "name": node.attrib.get("Name"),
                        "value": node.attrib.get("Address"),
                    }
                    for node in root.findall(".//{*}host")
                ]
            source.dns_records = [
                {
                    "type": str(record.get("type", "")),
                    "name": str(record.get("name", record.get("host", ""))),
                    "value": str(
                        record.get(
                            "content",
                            record.get("data", record.get("answer", record.get("value", ""))),
                        )
                    ),
                }
                for record in records
                if record.get("type") in {"A", "AAAA", "CNAME"}
            ]
        except (DomainProviderError, KeyError, AttributeError, TypeError, ValueError) as exc:
            source.details_complete = False
            result.warnings.append(
                str(exc)
                if isinstance(exc, DomainProviderError)
                else f"{provider}: DNS details unreadable."
            )
    for row in result.domains[detail_budget:]:
        row.sources[0].details_complete = False
    if not result.complete:
        result.warnings.append(
            "Domain pagination budget reached; existing observations were retained."
        )
    return result


async def discover_domains(
    provider: DomainProvider,
    fields: dict[str, str],
    *,
    connection_id: str,
    observed_at: str,
    page_budget: int,
    detail_budget: int,
    http: httpx.AsyncClient,
) -> DomainInventory:
    try:
        return await _discover_domains(
            provider,
            fields,
            connection_id=connection_id,
            observed_at=observed_at,
            page_budget=page_budget,
            detail_budget=detail_budget,
            http=http,
        )
    except (KeyError, AttributeError, TypeError, ValueError):
        raise DomainProviderError(
            f"{provider} returned invalid domain evidence; prior observations were retained."
        ) from None
