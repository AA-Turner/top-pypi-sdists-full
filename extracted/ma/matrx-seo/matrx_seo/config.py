from __future__ import annotations

from collections.abc import Awaitable, Callable
from decimal import Decimal
from typing import Any

from .contracts import CollectionRequest, ResolvedCredential, StoredPayloadReceipt

CredentialResolver = Callable[[CollectionRequest, str], Awaitable[ResolvedCredential]]
CollectionAuthorizer = Callable[[CollectionRequest], Awaitable[CollectionRequest]]
HostResourceResolver = Callable[[str, str], Awaitable[dict[str, Any]]]
PayloadStore = Callable[[CollectionRequest, str, bytes, str], Awaitable[StoredPayloadReceipt]]
#: Reads one offloaded payload back by its ``cloud_file_id``, as the exact
#: bytes the store was handed. The store's inverse — a package that can write
#: a payload out of Postgres and cannot read it back has not offloaded it, it
#: has lost it.
PayloadFetcher = Callable[[str], Awaitable[bytes]]
#: Renders a USD cost as the words a PERSON reads. The package has no opinion on
#: the unit: a host with a credit unit injects its formatter (aidream injects
#: ``format_points`` — people see points, never dollars); a bare host gets dollars.
CostText = Callable[[Decimal], str]

_credential_resolver: CredentialResolver | None = None
_host_resource_resolver: HostResourceResolver | None = None
_payload_store: PayloadStore | None = None
_payload_fetcher: PayloadFetcher | None = None
_collection_authorizer: CollectionAuthorizer | None = None
_cost_text: CostText | None = None


def configure(
    *,
    credential_resolver: CredentialResolver | None = None,
    host_resource_resolver: HostResourceResolver | None = None,
    payload_store: PayloadStore | None = None,
    payload_fetcher: PayloadFetcher | None = None,
    collection_authorizer: CollectionAuthorizer | None = None,
    cost_text: CostText | None = None,
) -> None:
    global _collection_authorizer, _credential_resolver, _host_resource_resolver
    global _payload_fetcher, _payload_store, _cost_text
    if credential_resolver is not None:
        _credential_resolver = credential_resolver
    if host_resource_resolver is not None:
        _host_resource_resolver = host_resource_resolver
    if payload_store is not None:
        _payload_store = payload_store
    if payload_fetcher is not None:
        _payload_fetcher = payload_fetcher
    if collection_authorizer is not None:
        _collection_authorizer = collection_authorizer
    if cost_text is not None:
        _cost_text = cost_text


def person_cost_text(amount_usd: Decimal | float | str | None) -> str:
    """A cost in a sentence a person reads, through the host's injected
    formatter (``configure(cost_text=...)``). Without one the package states
    dollars, the only unit it knows on its own."""
    if amount_usd is None:
        return "—"
    amount = Decimal(str(amount_usd))
    if _cost_text is not None:
        return _cost_text(amount)
    return "$" + str(amount)


async def battery_credential_resolver(
    request: CollectionRequest, provider: str
) -> ResolvedCredential:
    """Default resolver: read every declared credential key for the requesting
    user or organization from the canonical secrets battery (users.user_secrets
    via matrx-orm). Personal values take precedence over organization values.
    No environment fallback exists — a missing/undecryptable secret raises."""
    from matrx_orm.secrets_battery import require_secret

    if not request.credential_keys:
        raise RuntimeError(
            f"SEO provider {provider!r} declared no credential keys; the battery "
            "resolver has nothing to resolve — declare them on the operation"
        )
    values = {
        key: await require_secret(request.created_by, request.organization_id, key)
        for key in request.credential_keys
    }
    return ResolvedCredential(
        reference_id=request.credential_reference_id,
        reference_kind=request.credential_reference_kind,
        values=values,
    )


def get_credential_resolver() -> CredentialResolver:
    if _credential_resolver is None:
        return battery_credential_resolver
    return _credential_resolver


def get_host_resource_resolver() -> HostResourceResolver:
    if _host_resource_resolver is None:
        raise RuntimeError(
            "matrx-seo has no host-resource resolver. Inject one with matrx_seo.configure()."
        )
    return _host_resource_resolver


def get_payload_store() -> PayloadStore:
    if _payload_store is None:
        raise RuntimeError("matrx-seo has no payload store. Inject one with matrx_seo.configure().")
    return _payload_store


def get_payload_fetcher() -> PayloadFetcher:
    if _payload_fetcher is None:
        raise RuntimeError(
            "matrx-seo has no payload fetcher, so an offloaded raw payload cannot "
            "be read back. Inject one with matrx_seo.configure(payload_fetcher=...)."
        )
    return _payload_fetcher


def get_collection_authorizer() -> CollectionAuthorizer:
    if _collection_authorizer is None:
        raise RuntimeError(
            "matrx-seo has no collection authorizer. Inject one with matrx_seo.configure()."
        )
    return _collection_authorizer
