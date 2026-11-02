"""Account, catalog, and agent-signup request/response mapping (SPEC 2.7, 3.7).

Pure functions that build the HTTP request pieces and map raw JSON bodies into
the public models. The sync and async clients share these so the wire mapping
lives in one place. Discovery bodies are safety-scanned, then projected into
customer-safe public models so additive gateway fields remain compatible.
"""

from __future__ import annotations

from typing import Any, cast

from ._errors import AnyAPIError, error_for_status
from ._transport import as_dict, error_details
from .types import (
    AccountProfile,
    AgentSignupResult,
    Balance,
    CatalogEntry,
    CatalogSearchResults,
)

__all__ = [
    "balance_path",
    "me_path",
    "catalog_request",
    "search_request",
    "describe_path",
    "signup_request",
    "parse_balance",
    "parse_me",
    "parse_catalog",
    "parse_describe",
    "parse_search",
    "parse_signup",
    "map_error",
]

balance_path = "/v1/balance"
me_path = "/v1/me"


def catalog_request(category: str | None) -> tuple[str, dict[str, str]]:
    """Path and query params for ``catalog()`` (GET /v1/apis)."""
    params: dict[str, str] = {}
    if category is not None:
        params["category"] = category
    return "/v1/apis", params


def search_request(
    query: str | None,
    category: str | None,
    platform: str | None,
    limit: int | None,
) -> tuple[str, dict[str, str]]:
    """Path and query params for dedicated ranked discovery search.

    The gateway needs at least one of query, category or platform, in any
    combination, so a scope with no query at all is a valid search. An absent or
    empty query omits ``q`` entirely, because an empty ``q`` is a different
    request.
    """
    if not query and category is None and platform is None:
        raise AnyAPIError(
            "search needs at least one of query, category, or platform",
            status=0,
        )
    params: dict[str, str] = {}
    if query:
        params["q"] = query
    if category is not None:
        params["category"] = category
    if platform is not None:
        params["platform"] = platform
    if limit is not None:
        params["limit"] = str(limit)
    return "/catalog/search", params


def describe_path(slug: str) -> str:
    return f"/v1/apis/{slug}"


def signup_request(sponsor_email: str | None, label: str | None) -> dict[str, Any]:
    """JSON body for ``agent_signup()`` (POST /agent/signup, no auth)."""
    body: dict[str, Any] = {}
    if sponsor_email is not None:
        body["sponsorEmail"] = sponsor_email
    if label is not None:
        body["label"] = label
    return body


def parse_balance(body: Any) -> Balance:
    return Balance.model_validate(body)


def parse_me(body: Any) -> AccountProfile:
    """Map /v1/me, dropping clerkUserId and signupGrantApplied (SPEC 2.7)."""
    return AccountProfile.model_validate(body)


def _reject_unsafe_discovery_fields(value: object, path: str) -> None:
    if isinstance(value, list):
        for index, item in enumerate(cast("list[object]", value)):
            _reject_unsafe_discovery_fields(item, f"{path}[{index}]")
        return
    if not isinstance(value, dict):
        return
    for key, item in cast("dict[object, object]", value).items():
        if isinstance(key, str) and "credit" in key.lower():
            raise ValueError(f"malformed discovery response: {path}.{key}")
        if key == "provider" and item != "AnyAPI":
            raise ValueError(f"malformed discovery response: {path}.{key}")
        _reject_unsafe_discovery_fields(item, f"{path}.{key}")


def parse_catalog(body: object) -> list[CatalogEntry]:
    """Map {apis:[...]} into CatalogEntry[] (SPEC 2.7)."""
    _reject_unsafe_discovery_fields(body, "catalog")
    envelope = as_dict(body)
    raw = envelope.get("apis")
    if not isinstance(raw, list):
        raise ValueError("malformed discovery response: catalog.apis")
    apis: list[object] = list(cast("list[object]", raw))
    return [CatalogEntry.model_validate(item, strict=True) for item in apis]


def parse_describe(body: object) -> CatalogEntry:
    """Map a single /v1/apis/{slug} entry into one CatalogEntry."""
    _reject_unsafe_discovery_fields(body, "api")
    raw = as_dict(body)
    entry = CatalogEntry.model_validate(body, strict=True)
    if entry.input_schema is None or entry.output_schema is None:
        raise ValueError("malformed discovery response: detail schemas are required")
    if "latency" not in raw:
        raise ValueError("malformed discovery response: detail latency is required")
    return entry


def parse_search(body: object) -> CatalogSearchResults:
    """Validate the dedicated search result envelope."""
    _reject_unsafe_discovery_fields(body, "search")
    return CatalogSearchResults.model_validate(body, strict=True)


def parse_signup(body: Any) -> AgentSignupResult:
    return AgentSignupResult.model_validate(body)


def map_error(status: int, body: object, request_id: str | None) -> AnyAPIError:
    """Map a non-2xx account/catalog response to the frozen error hierarchy."""
    message, code = error_details(body, status)
    return error_for_status(status, message, request_id=request_id, code=code)
