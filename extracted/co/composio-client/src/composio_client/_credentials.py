"""The credential transport boundary — a port of ``src/compat/credentials.ts``.

The design record makes authentication part of the runtime contract in both
languages, with four rules. Three are enforced here and in
:mod:`._base_client`; the fourth is a property of what this client's messages
are built from, and is pinned by test rather than by code:

0. **A request carries exactly one credential header**, chosen from the
   operation's declared security schemes by :func:`select_scheme`. Not a record
   rule — it is a measured property of the API (two credential headers on one
   request is a 401, even where either alone is a 200), so the four rules below
   are all stated about *the* credential a request carries. On this client the
   selector is **inert today and correct when the surface widens**: every
   operation in ``python/surface-coverage.json`` is ``tool_router``, and all 16
   resolve to ``ApiKeyAuth``.
1. **A credentialed API origin must use HTTPS.** Plain ``http://`` is permitted
   only for loopback development endpoints — which is exactly what the
   sanctioned ``environment="local"`` default (``http://localhost:9900``) is.
   Enforced by :func:`assert_credential_transport` at construction and again by
   :func:`credential_for_request` at dispatch, since ``base_url`` and
   ``base_url`` is a plain attribute a caller can reassign.
2. **The credential is attached only to requests whose origin matches the
   configured API origin.** :func:`credential_for_request` returns ``None``
   off-origin and the header is simply not sent.
3. **Credentials are never forwarded across an origin-changing redirect.** The
   kernel follows redirects *itself* — ``follow_redirects=False`` on every
   dispatch, then its own hop loop — so every hop re-enters the header build
   and the credential decision is re-derived from that hop's URL. Rule 3 mostly
   falls out of rule 2 that way. What does not fall out is the caller's own
   credential headers, which rule 2 deliberately leaves alone;
   :func:`withdraw_credentials` removes those once a chain has changed origin.
   Passing the flag per request is also what makes this true for a
   caller-supplied ``http_client``, the only way httpx's default could have
   been flipped. TypeScript has one branch this port deliberately does **not**
   copy: it delegates the first dispatch to ``fetch`` when the request carries
   no credential-bearing header, because that is the only way a *browser* can
   follow a redirect. Python has no browser and no opaque redirect, so the
   branch would buy nothing — and it would cost: ``httpx.TooManyRedirects`` is
   a ``RequestError``, so a delegated redirect loop would be *retried* and then
   surface as a generic connection error, where the hand-rolled loop raises a
   named, terminal one exactly as TypeScript does. Identical behavior, one
   mechanism fewer. One httpx-side asymmetry with TypeScript: httpx precomputes
   ``response.next_request`` even when it is not following, so a ``Location``
   it cannot parse into a request (``data:…``) raises ``httpx.InvalidURL``
   before the kernel sees the response, where TypeScript hands the 3xx back.
   A ``Location`` httpx *can* parse but this client does not speak (``ftp:…``)
   takes the same path in both.
4. **Credential-bearing values are redacted from logs and error messages.**
   Nothing here to do: ``_error_message`` builds from the status and the
   response *body*, ``APIConnectionError`` / ``APITimeoutError`` carry fixed
   strings, and the deprecation notice is built from the operation template and
   parsed public response-header values. Pinned in ``tests/test_credentials.py``
   so it stays true.

Failure modes differ per rule, deliberately, and match the TypeScript
reference. Rule 1 **raises** ``ComposioError``: a plaintext credentialed origin
is a configuration mistake with no safe reading, and dropping the key instead
would turn it into 401s that never name the cause. Rule 2 **drops the
credential and continues**: the record states it as an attachment rule, and an
off-origin fetch can be legitimate (this API mints presigned upload and
download URLs on a storage origin). Rule 3 **follows the hop without the
credential** rather than refusing to hop — refusing was the first spelling and
was overruled, because Stainless followed redirects and no wire-parity fixture
redirects, so a green suite would have proved only that the *tests* do not.

Deliberate divergence from the Stainless client, which enforces none of it —
though redirect *following* is not part of the divergence, only what rides
along on the hop. See ``python/MIGRATION.md`` §6.
"""

from __future__ import annotations

import ipaddress
from collections.abc import Mapping, Sequence
from typing import NamedTuple
from urllib.parse import urlsplit

from ._exceptions import ComposioError

__all__ = [
    "CREDENTIAL_SCHEME_HEADERS",
    "DEFAULT_SCHEME",
    "Credentials",
    "assert_credential_transport",
    "credential_destination",
    "credential_for_request",
    "has_alternate_credential",
    "is_loopback_host",
    "same_origin",
    "select_scheme",
    "withdraw_credentials",
]

_DEFAULT_PORTS = {"http": 80, "https": 443}
_LOOPBACK_DESCRIPTION = "localhost, *.localhost, 127.0.0.0/8, [::1]"

#: The three credential classes this API accepts and the header each puts on the
#: wire -- the ``apiKey``-in-header schemes ``spec/openapi.json`` declares. The
#: fourth, ``CookieAuth``, is referenced by no operation and is not something a
#: client library places. Kept in step with ``src/compat/credentials.ts``.
CREDENTIAL_SCHEME_HEADERS: Mapping[str, str] = {
    "ApiKeyAuth": "x-api-key",
    "UserApiKeyAuth": "x-user-api-key",
    "OrgApiKeyAuth": "x-org-api-key",
}

#: The scheme a request authenticates with when its operation names none.
DEFAULT_SCHEME = "ApiKeyAuth"


class Credentials(NamedTuple):
    """What an ``AutoAuth`` client holds, per scheme: a key, a provider of one,
    or ``None`` for a class it was not given. Selection asks only whether a
    class is present, so a provider is never called to answer it."""

    api_key: object | None
    user_api_key: object | None = None
    org_api_key: object | None = None

    def value_for(self, scheme: str) -> object | None:
        if scheme == "ApiKeyAuth":
            return self.api_key
        if scheme == "UserApiKeyAuth":
            return self.user_api_key
        if scheme == "OrgApiKeyAuth":
            return self.org_api_key
        return None


def has_alternate_credential(credentials: Credentials) -> bool:
    """Whether anything beyond the project key is configured -- the condition
    that makes per-operation selection able to change an outcome at all.

    Load-bearing rather than an optimization. With only ``api_key`` set every
    branch of :func:`select_scheme` lands on ``ApiKeyAuth``, so the client every
    existing caller constructs never consults the operation table and emits
    byte-identical requests by construction rather than by assertion.
    """
    return credentials.user_api_key is not None or credentials.org_api_key is not None


def select_scheme(schemes: Sequence[str] | None, credentials: Credentials) -> str:
    """Which credential a request declaring ``schemes`` should carry.

    **Exactly one, always.** Measured against production on 2026-08-06: a
    request carrying two credential headers is answered ``401
    HTTP_Unauthorized`` even on an operation that accepts either one alone. So
    there is no additive model available and the choice is made per request.

    Precedence, matching ``selectScheme`` in ``src/compat/credentials.ts``:
    ``ApiKeyAuth`` wins wherever the operation accepts it and a project key is
    configured; otherwise the first scheme the operation names that this client
    both recognizes and holds a credential for; otherwise ``ApiKeyAuth``, which
    is what this client did before any of this existed. That last branch is
    also where an unrecognized scheme name lands -- the spec references
    ``no_auth`` and ``workbench_access_key`` without declaring either, and those
    operations receive ``x-api-key`` today.
    """
    if not schemes:
        return DEFAULT_SCHEME
    if DEFAULT_SCHEME in schemes and credentials.api_key is not None:
        return DEFAULT_SCHEME
    for scheme in schemes:
        if scheme in CREDENTIAL_SCHEME_HEADERS and credentials.value_for(scheme) is not None:
            return scheme
    return DEFAULT_SCHEME


#: ``(scheme, host, port)`` with the default port made explicit, so
#: ``https://api.test`` and ``https://api.test:443`` compare equal.
_Origin = tuple[str, str, int]


def is_loopback_host(host: str) -> bool:
    """What counts as loopback, pinned rather than assumed.

    ``localhost`` is not the whole set:

    - ``localhost`` and any name under it (``api.localhost``). RFC 6761 §6.3
      reserves the whole ``.localhost`` TLD to the loopback interface.
    - The entire IPv4 loopback block ``127.0.0.0/8``, not just ``127.0.0.1``.
    - The IPv6 loopback ``::1``, in any spelling :mod:`ipaddress` accepts.

    Everything else is not loopback, deliberately — ``0.0.0.0`` included: it is
    the unspecified address, it reaches the local host on some platforms and
    fails on others, and a rule that depends on the platform is not a rule. The
    IPv4-mapped spelling ``::ffff:127.0.0.1`` is refused for the same reason:
    :attr:`ipaddress.IPv6Address.is_loopback` answers it differently across
    interpreter versions, and nobody configures a development endpoint that
    way.

    One known asymmetry with TypeScript, in the safe direction. The WHATWG
    ``URL`` parser normalizes shorthand IPv4 (``127.1`` -> ``127.0.0.1``) before
    this rule sees it; :mod:`urllib.parse` does not, and :mod:`ipaddress`
    rejects the shorthand. So Python refuses ``http://127.1`` where TypeScript
    accepts it. Stricter, never looser.
    """
    candidate = host.strip().lower()
    if candidate.startswith("[") and candidate.endswith("]"):
        candidate = candidate[1:-1]
    if candidate == "localhost" or candidate.endswith(".localhost"):
        return True
    try:
        address = ipaddress.ip_address(candidate)
    except ValueError:
        return False
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        return False
    return address.is_loopback


def _origin(url: str) -> _Origin | None:
    """The URL's origin, or ``None`` when it is not an absolute http(s) URL."""
    try:
        parts = urlsplit(url)
        port = parts.port
        host = parts.hostname
    except ValueError:  # malformed port or IPv6 literal
        return None
    scheme = parts.scheme.lower()
    if scheme not in _DEFAULT_PORTS or not host:
        return None
    return (scheme, host.lower(), port or _DEFAULT_PORTS[scheme])


def _is_credential_safe(origin: _Origin) -> bool:
    scheme, host, _ = origin
    return scheme == "https" or (scheme == "http" and is_loopback_host(host))


def _insecure_message(base_url: str) -> str:
    return (
        f"Refusing to send a Composio API credential to {base_url}: a credentialed API origin must "
        f"use HTTPS. Plain http:// is permitted only for loopback development endpoints "
        f"({_LOOPBACK_DESCRIPTION}). Pass an https:// base_url, use environment='local', or "
        f"construct the client with auth=NoAuth()."
    )


def assert_credential_transport(base_url: str, credentialed: bool) -> None:
    """Rule 1 at construction time: a client configured with a credential must
    be pointed at an origin that can carry one.

    A ``base_url`` that is not an absolute http(s) URL fails the same way — a
    credential cannot be sent over a scheme this client does not speak.

    ``credentialed`` is whether ``auth`` is anything but ``NoAuth``: which
    credential a given request carries may be decided per operation, or by a
    provider at call time, so a client configured with *any* can put one on
    the wire.
    """
    if not credentialed:
        return
    origin = _origin(base_url)
    if origin is None or not _is_credential_safe(origin):
        raise ComposioError(_insecure_message(base_url))


def credential_destination(base_url: str, request_url: str) -> bool:
    """Whether a credential may ride on a request to ``request_url``.

    Rules 1 and 2 at dispatch time. ``False`` off the configured API origin
    (rule 2: the credential is simply not sent); raises ``ComposioError`` when
    the request is for the API origin and that origin cannot carry a credential
    (rule 1). The origin comparison is not a tautology: the request URL is
    ``base_url`` concatenated with a path, and a path that does not begin with
    ``/`` extends the *authority* instead (``.evil.example/x`` ->
    ``https://backend.composio.dev.evil.example/x``, ``@evil.example/x`` ->
    ``https://evil.example/x`` with the API host demoted to userinfo — httpx,
    unlike ``fetch``, dispatches that one happily).
    """
    base = _origin(base_url)
    target = _origin(request_url)
    if base is None or target is None or base != target:
        return False
    if not _is_credential_safe(target):
        raise ComposioError(_insecure_message(base_url))
    return True


def credential_for_request(
    base_url: str, credential: tuple[str, str] | None, request_url: str
) -> tuple[str, str] | None:
    """The resolved ``(header, value)`` this request may carry, or ``None``
    for none (see :func:`credential_destination`)."""
    if credential is None:
        return None
    return credential if credential_destination(base_url, request_url) else None


def same_origin(a: str, b: str) -> bool:
    """Whether two absolute URLs share a scheme, host and port. An unparseable
    side is never the same origin as anything, including itself."""
    origin_a = _origin(a)
    return origin_a is not None and origin_a == _origin(b)


#: Header names that carry a credential and must not survive an origin change.
#:
#: The first three are what a redirect-following HTTP stack strips for you —
#: the Fetch spec deletes ``Authorization`` across a cross-origin redirect, and
#: ``Cookie`` / ``Proxy-Authorization`` are managed by the stack rather than the
#: caller. Following redirects by hand means taking that job on. ``x-api-key``
#: joins them because it is *this* API's credential, and because no HTTP stack
#: would have stripped it: a custom header rides along a cross-origin redirect,
#: which is the hole this module exists to close.
#:
#: ``x-user-api-key`` and ``x-org-api-key`` are the spec's other two credential
#: schemes (``UserApiKeyAuth``, ``OrgApiKeyAuth``). The kernel attaches all three
#: and a caller can place the latter two directly besides,
#: so the withdrawal set covers them. They were listed here *before*
#: the attachment work: Python has no delegation branch, so the cost of omitting
#: them was the missed withdrawal alone; the TypeScript twin additionally
#: mis-classified such a request as credential-free. Kept in step with
#: ``src/compat/credentials.ts``.
_CREDENTIAL_HEADERS = (
    "authorization",
    "cookie",
    "proxy-authorization",
    "x-api-key",
    "x-user-api-key",
    "x-org-api-key",
)


def withdraw_credentials(headers: dict[str, str]) -> dict[str, str]:
    """Rule 3 for headers the caller placed, applied once a redirect chain
    changes origin.

    Rule 2 deliberately leaves a caller's own ``default_headers`` / per-request
    headers alone on the *initial* request, even off-origin: the caller chose
    that URL. A redirect target is chosen by the *server*, so the same consent
    does not extend to it.

    Withdrawal is **sticky** for the rest of the chain: once a hop has left the
    origin it started on, no later hop re-attaches a credential, not even one
    landing back on the configured API origin. A real API does not bounce a
    caller off-site and back, and "no credential after the chain leaves" is one
    sentence rather than a case analysis.
    """
    return {name: value for name, value in headers.items() if name.lower() not in _CREDENTIAL_HEADERS}
