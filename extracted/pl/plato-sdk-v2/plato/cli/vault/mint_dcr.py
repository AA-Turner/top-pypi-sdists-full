"""OAuth dynamic client registration for `plato vault mint token`: a vendor server (a hosted MCP
server, most often) that registers clients itself needs no app made in a developer console.

* Discovery: the server's protected resource metadata (RFC 9728), from its 401's
  ``WWW-Authenticate: Bearer resource_metadata=...`` or the well-known path, names its
  authorization server; with none, the server's own origin is the authorization server (MCP
  2025-03-26). Then that server's metadata (RFC 8414, or OpenID Connect discovery).
* Registration (RFC 7591): code registers a client for the mint's redirect URI with the
  ``authorization_code`` and ``refresh_token`` grants, and keeps its id and secret in memory;
  the grant stores them with the token endpoint and client auth method the metadata gave, so
  Chronos refreshes it like any other grant.

Nothing here is vendor-specific: every value comes from what the server publishes.
"""

from __future__ import annotations

from typing import Any, TypeVar
from urllib.parse import urlparse

import httpx
from pydantic import BaseModel, ConfigDict, SecretStr, ValidationError

from plato.cli.vault import app_oauth
from plato.cli.vault.app_models import ClientAuth

DISCOVERY_TIMEOUT_S = 30.0
PRM_PATH = "/.well-known/oauth-protected-resource"
AS_PATH = "/.well-known/oauth-authorization-server"
OIDC_PATH = "/.well-known/openid-configuration"
# The client auth methods code can run, best first: a public client with PKCE has no secret
# that can expire or leak; else HTTP Basic (RFC 7591's default), else the body.
AUTH_PREFERENCE = (ClientAuth.none, ClientAuth.basic, ClientAuth.post)
# A well-known document the server does not have.
ABSENT_STATUSES = (404, 410)
M = TypeVar("M", bound=BaseModel)


class DcrError(Exception):
    """Discovery or registration failed. The message holds no request or reply body."""


class ResourceMetadata(BaseModel):
    """RFC 9728 protected resource metadata: the fields used here."""

    model_config = ConfigDict(extra="ignore")

    resource: str | None = None
    authorization_servers: list[str] = []
    scopes_supported: list[str] = []


class ServerMetadata(BaseModel):
    """RFC 8414 authorization server metadata: the fields used here."""

    model_config = ConfigDict(extra="ignore")

    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    registration_endpoint: str | None = None
    scopes_supported: list[str] = []
    grant_types_supported: list[str] = ["authorization_code", "implicit"]
    # RFC 8414 2: omitted means client_secret_basic.
    token_endpoint_auth_methods_supported: list[str] = [ClientAuth.basic.value]
    code_challenge_methods_supported: list[str] = []


class Discovered(BaseModel):
    """What discovery found for one server URL. No secret."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    server_url: str
    metadata: ServerMetadata
    # The RFC 8707 resource indicator: the protected resource metadata's ``resource``, sent on
    # the authorize and every token call. None when the server publishes no such metadata.
    resource: str | None = None
    scopes: list[str] = []


class RegisteredClient(BaseModel):
    """A registered client. Never print it."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    client_id: SecretStr
    client_secret: SecretStr | None = None
    client_auth: ClientAuth
    # 0 or None: the secret never expires (RFC 7591 3.2.1).
    client_secret_expires_at: int | None = None


class RegistrationReply(BaseModel):
    model_config = ConfigDict(extra="ignore")

    client_id: str
    client_secret: str | None = None
    token_endpoint_auth_method: str | None = None
    client_secret_expires_at: int | None = None


def _origin(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _path(url: str) -> str:
    return urlparse(url).path.rstrip("/")


def _get_document(http: httpx.Client, url: str, model: type[M]) -> M | None:
    """A well-known document as ``model``; None only when the server has none there (404, 410).
    Any other answer raises: a refusal or an outage must not read as "no such document"."""
    try:
        response = http.get(url, headers={"Accept": "application/json"}, timeout=DISCOVERY_TIMEOUT_S)
    except httpx.HTTPError as e:
        raise DcrError(f"{url} did not answer ({type(e).__name__})") from None
    if response.status_code in ABSENT_STATUSES:
        return None
    if response.status_code != 200:
        raise DcrError(f"{url} answered HTTP {response.status_code}")
    try:
        return model.model_validate_json(response.content)
    except ValidationError:
        raise DcrError(f"{url} is not a {model.__name__} document") from None


def resource_metadata_url(www_authenticate: str) -> str | None:
    """The ``resource_metadata`` parameter of a Bearer challenge (RFC 9728 5.1)."""
    for part in www_authenticate.split(","):
        name, _, value = part.strip().removeprefix("Bearer ").strip().partition("=")
        if name.strip() == "resource_metadata" and value:
            return value.strip().strip('"')
    return None


def _challenge_metadata_url(http: httpx.Client, server_url: str) -> str | None:
    """The metadata URL a 401 from the server names; headers only, the body is never read (a
    streamable MCP endpoint may hold the GET open)."""
    try:
        with http.stream("GET", server_url, headers={"Accept": "application/json"}, timeout=DISCOVERY_TIMEOUT_S) as r:
            if r.status_code >= 500:
                raise DcrError(f"{server_url} answered HTTP {r.status_code}")
            # Any other answer but a 401 (a 405 to a GET, an open stream) only means no challenge.
            if r.status_code != 401:
                return None
            return resource_metadata_url(r.headers.get("www-authenticate", ""))
    except httpx.HTTPError as e:
        raise DcrError(f"{server_url} did not answer ({type(e).__name__})") from None


def protected_resource(http: httpx.Client, server_url: str) -> ResourceMetadata | None:
    """RFC 9728: from the 401's challenge, else the well-known URL with the server's path, else
    at the origin."""
    urls = [u for u in (_challenge_metadata_url(http, server_url),) if u]
    path = _path(server_url)
    if path:
        urls.append(f"{_origin(server_url)}{PRM_PATH}{path}")
    urls.append(f"{_origin(server_url)}{PRM_PATH}")
    for url in urls:
        if urlparse(url).scheme != "https":
            raise DcrError("the resource metadata URL the server names is not https")
        found = _get_document(http, url, ResourceMetadata)
        if found is not None:
            return found
    return None


def _metadata_urls(issuer: str) -> list[str]:
    """RFC 8414 3.1 (path after the well-known part), then OpenID Connect discovery both ways."""
    origin, path = _origin(issuer), _path(issuer)
    if not path:
        return [f"{origin}{AS_PATH}", f"{origin}{OIDC_PATH}"]
    return [f"{origin}{AS_PATH}{path}", f"{origin}{OIDC_PATH}{path}", f"{origin}{path}{OIDC_PATH}"]


def server_metadata(http: httpx.Client, issuer: str) -> ServerMetadata:
    for url in _metadata_urls(issuer):
        metadata = _get_document(http, url, ServerMetadata)
        if metadata is None:
            continue
        # RFC 8414 3.3: the metadata must be the issuer's own.
        if metadata.issuer.rstrip("/") != issuer.rstrip("/"):
            raise DcrError(f"{url} names another issuer than {issuer}")
        return metadata
    raise DcrError(f"{issuer} publishes no authorization server metadata")


def discover(http: httpx.Client, server_url: str) -> Discovered:
    """The authorization server of ``server_url`` and its metadata."""
    if urlparse(server_url).scheme != "https":
        raise DcrError("the server URL must be https")
    prm = protected_resource(http, server_url)
    if prm is not None and not prm.authorization_servers:
        raise DcrError(f"the resource metadata of {server_url} names no authorization server")
    issuer = prm.authorization_servers[0] if prm is not None else _origin(server_url)
    metadata = server_metadata(http, issuer)
    for name in ("authorization_endpoint", "token_endpoint", "registration_endpoint"):
        value = getattr(metadata, name)
        if value is not None and urlparse(value).scheme != "https":
            raise DcrError(f"the metadata's {name} is not https")
    return Discovered(
        server_url=server_url,
        metadata=metadata,
        resource=prm.resource if prm is not None else None,
        scopes=(prm.scopes_supported if prm is not None and prm.scopes_supported else metadata.scopes_supported),
    )


def pick_client_auth(metadata: ServerMetadata) -> ClientAuth:
    """The best method the server takes; a public client only when it takes S256 PKCE."""
    supported = set(metadata.token_endpoint_auth_methods_supported)
    for method in AUTH_PREFERENCE:
        if method.value not in supported:
            continue
        if method == ClientAuth.none and "S256" not in metadata.code_challenge_methods_supported:
            continue
        return method
    raise DcrError(
        "the server takes none of the client auth methods code runs "
        f"({', '.join(m.value for m in AUTH_PREFERENCE)}, a public client only with S256 PKCE)"
    )


def register(http: httpx.Client, found: Discovered, redirect_uri: str, client_name: str) -> RegisteredClient:
    """RFC 7591: register a client for ``redirect_uri`` that may refresh."""
    endpoint = found.metadata.registration_endpoint
    if endpoint is None:
        raise DcrError(
            f"{found.metadata.issuer} takes no dynamic client registration (no registration_endpoint): "
            "make an OAuth app in the vendor's developer console instead"
        )
    grants = found.metadata.grant_types_supported
    if "refresh_token" not in grants:
        raise DcrError(f"{found.metadata.issuer} does not list the refresh_token grant")
    method = pick_client_auth(found.metadata)
    body: dict[str, Any] = {
        "client_name": client_name,
        "redirect_uris": [redirect_uri],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": method.value,
    }
    if found.scopes:
        body["scope"] = " ".join(found.scopes)
    try:
        response = http.post(endpoint, json=body, headers={"Accept": "application/json"}, timeout=DISCOVERY_TIMEOUT_S)
    except httpx.HTTPError as e:
        raise DcrError(f"the registration got no answer ({type(e).__name__})") from None
    if response.status_code not in (200, 201):
        raise DcrError(f"the registration failed: HTTP {response.status_code} {app_oauth._error_code(response)}")
    try:
        reply = RegistrationReply.model_validate(response.json())
    except (ValueError, ValidationError):
        raise DcrError("the registration reply is not a client") from None
    try:
        # The server may give another method than the one asked for: its answer wins.
        auth = ClientAuth(reply.token_endpoint_auth_method or method.value)
    except ValueError:
        raise DcrError(f"the server registered the client for {reply.token_endpoint_auth_method}") from None
    if auth != ClientAuth.none and not reply.client_secret:
        raise DcrError(f"the server registered a {auth.value} client with no client_secret")
    return RegisteredClient(
        client_id=SecretStr(reply.client_id),
        client_secret=SecretStr(reply.client_secret) if reply.client_secret and auth != ClientAuth.none else None,
        client_auth=auth,
        client_secret_expires_at=reply.client_secret_expires_at,
    )
