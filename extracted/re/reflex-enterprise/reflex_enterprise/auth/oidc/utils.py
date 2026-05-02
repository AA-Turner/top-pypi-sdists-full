"""OIDC helpers: metadata, JWKS, and JWT verification."""

import base64
import hashlib
import logging
from collections.abc import Awaitable
from typing import Any

import httpx
from joserfc import jwk, jwt

from reflex_enterprise.auth.oidc.types import (
    AsyncHTTPClientProtocol,
    AsyncHTTPResponse,
    AsyncHTTPResponseContext,
    is_ok,
)

# Simple cached OIDC metadata + JWKS loader
_OIDC_CACHE: dict[str, dict] = {}


# Default HTTP client for OIDC operations, can be overridden by ConfigMixin or passed in for testing
class HTTPXResponseWrapper(AsyncHTTPResponse):
    """Wrapper for httpx.Response to conform to AsyncHTTPResponse protocol."""

    def __init__(self, response: httpx.Response):
        """Initialize the wrapper with an httpx.Response."""
        self._response = response
        self.status = response.status_code

    async def json(self) -> Any:
        """Parse and return the JSON content of the HTTP response."""
        return self._response.json()

    async def text(self) -> str:
        """Return the text content of the HTTP response."""
        return self._response.text


class HTTPXResponseContext(AsyncHTTPResponseContext):
    """Async context manager for httpx.Response to conform to AsyncHTTPResponseContext protocol."""

    def __init__(self, response_coro: Awaitable[httpx.Response]):
        """Initialize the context manager with a coroutine that yields an httpx.Response."""
        self._response_coro = response_coro
        self._response = None

    async def __aenter__(self) -> HTTPXResponseWrapper:
        """Enter the asynchronous context manager."""
        self._response = await self._response_coro
        return HTTPXResponseWrapper(self._response)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: Any,
    ) -> None:
        """Exit the asynchronous context manager."""
        if self._response is not None:
            await self._response.aclose()


class AsyncHTTPXClient(AsyncHTTPClientProtocol):
    """AsyncHTTPClientProtocol implementation using httpx."""

    def __init__(self, client: httpx.AsyncClient):
        """Initialize the AsyncHTTPXClient."""
        self._client = client

    def get(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> AsyncHTTPResponseContext:
        """Perform an asynchronous HTTP GET request."""
        return HTTPXResponseContext(self._client.get(url, headers=headers))

    def post(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        data: Any = None,
    ) -> AsyncHTTPResponseContext:
        """Perform an asynchronous HTTP POST request."""
        return HTTPXResponseContext(self._client.post(url, headers=headers, data=data))


DEFAULT_HTTP_CLIENT = AsyncHTTPXClient(httpx.AsyncClient())


logger = logging.getLogger(__name__)


class ValidationError(ValueError):
    """Raised when token validation fails."""


async def _fetch_oidc_metadata(
    issuer: str, client: AsyncHTTPClientProtocol = DEFAULT_HTTP_CLIENT
) -> dict:
    key = f"metadata:{issuer}"
    if key in _OIDC_CACHE:
        return _OIDC_CACHE[key]
    url = issuer.rstrip("/") + "/.well-known/openid-configuration"
    async with client.get(url) as resp:
        if not is_ok(resp):
            raise RuntimeError(
                f"Failed to fetch OIDC metadata: {resp.status}: {await resp.text()}"
            )
        md = await resp.json()
    _OIDC_CACHE[key] = md
    return md


async def _fetch_jwks(
    jwks_uri: str, client: AsyncHTTPClientProtocol = DEFAULT_HTTP_CLIENT
) -> dict:
    key = f"jwks:{jwks_uri}"
    if key in _OIDC_CACHE:
        return _OIDC_CACHE[key]
    async with client.get(jwks_uri) as resp:
        if not is_ok(resp):
            raise RuntimeError(
                f"Failed to fetch JWKS: {resp.status}: {await resp.text()}"
            )
        jwks = await resp.json()
    _OIDC_CACHE[key] = jwks
    return jwks


async def issuer_endpoint(
    issuer_uri: str, service: str, client: AsyncHTTPClientProtocol = DEFAULT_HTTP_CLIENT
) -> str:
    """Fetch an endpoint URL (authorization/token/userinfo/etc) from OIDC metadata."""
    try:
        return (await _fetch_oidc_metadata(issuer_uri, client=client))[service]
    except KeyError:
        return ""


async def verify_jwt(
    token_json: str,
    issuer: str,
    audience: str | list[str] | None = None,
    nonce: str | None = None,
    at_hash: str | None = None,
    client: AsyncHTTPClientProtocol = DEFAULT_HTTP_CLIENT,
    *,
    valid_issuers: list[str] | None = None,
) -> jwt.Token:
    """Verify a JWT using OIDC discovery and JWKS per Microsoft docs.

    Args:
        token_json: The JWT as a string.
        issuer: The OIDC issuer URI used to fetch metadata and JWKS.
        audience: The expected audience claim value(s).
        nonce: The expected nonce claim value.
        at_hash: The expected at_hash claim value.
        client: The HTTP client to use for OIDC operations.
        valid_issuers: If provided, override the iss claim check with this
            list of acceptable values. The ``issuer`` arg is still used to
            fetch metadata/JWKS. When ``None``, the iss claim must equal
            ``issuer`` (with or without a trailing slash).

    Returns:
        The verified JWT token.
    """
    # Fetch metadata and keys from well-known endpoint.
    md = await _fetch_oidc_metadata(issuer, client=client)
    jwks_uri = md.get("jwks_uri")
    if not jwks_uri:
        raise RuntimeError("jwks_uri not found in oidc metadata")
    jwks = await _fetch_jwks(jwks_uri, client=client)

    # Build JsonWebKey set from HTTP response/cache.
    key_set = jwk.KeySet.import_key_set(jwks)  # pyright: ignore[reportArgumentType]

    # Decode and validate the JWT signature.
    token = jwt.decode(token_json, key_set)

    stripped_issuer = issuer.rstrip("/")

    # Validate specific claims, if provided.
    if valid_issuers is not None:
        iss_values = list(valid_issuers)
    else:
        iss_values = [stripped_issuer, stripped_issuer + "/"]
    iss_claim_request: jwt.ClaimsOption = {
        "essential": True,
        "values": iss_values,
    }
    aud_claim_request: jwt.ClaimsOption = {"essential": False}
    if audience is not None:
        aud_claim_request["essential"] = True
        if isinstance(audience, str):
            aud_claim_request["value"] = audience
        else:
            aud_claim_request["values"] = audience

    nonce_claim_request: jwt.ClaimsOption = {"essential": False}
    if nonce is not None:
        nonce_claim_request["essential"] = True
        nonce_claim_request["value"] = nonce

    at_hash_claim_request: jwt.ClaimsOption = {"essential": False}
    if at_hash:
        at_hash_claim_request["value"] = at_hash

    logger.debug(
        f"Verifying JWT claims: iss={iss_claim_request}, aud={aud_claim_request}, nonce={nonce_claim_request}, at_hash={at_hash_claim_request}"
    )

    claims_requests = jwt.JWTClaimsRegistry(
        iss=iss_claim_request,
        aud=aud_claim_request,
        nonce=nonce_claim_request,
        at_hash=at_hash_claim_request,
    )
    claims_requests.validate(token.claims)
    return token


def compute_at_hash(access_token: str, alg: str | None) -> str:
    """Compute at_hash value per OIDC spec for a given access token and alg."""
    if not alg:
        alg = "RS256"
    # map alg to hash
    if alg.endswith("256"):
        h = hashlib.sha256(access_token.encode("utf-8")).digest()
    elif alg.endswith("384"):
        h = hashlib.sha384(access_token.encode("utf-8")).digest()
    elif alg.endswith("512"):
        h = hashlib.sha512(access_token.encode("utf-8")).digest()
    else:
        h = hashlib.sha256(access_token.encode("utf-8")).digest()
    # left-most half
    half = h[: len(h) // 2]
    at_hash = base64.urlsafe_b64encode(half).decode("ascii").rstrip("=")
    return at_hash
