# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Origin pinning for the A2A client behind ``agents-cli run --mode a2a``.

An agent card is fetched from the user's ``--url``, but the card then declares
*its own* endpoints (``supportedInterfaces[].url``, which the legacy ``url`` /
``additionalInterfaces`` pair maps onto). The a2a-sdk sends to whatever the card
declares and never compares that host against the URL the card came from, so a
hostile — or merely compromised — card can aim the message at a third-party
host. With credentials attached as client-wide httpx default headers, that host
also received the caller's bearer token.

Two independent guards live here so neither is load-bearing on its own:

* :func:`create_pinned_client` rewrites every advertised endpoint back onto the
  origin of ``--url``, so the request goes where the user pointed it. This also
  restores reachability for agents whose card advertises an address the caller
  can't route to (``kubectl port-forward``, Agent Runtime passthrough).
* :class:`OriginPinnedAuth` attaches the caller's headers per request, and only
  when the outbound request is actually aimed at that origin — so anything the
  first guard misses still can't collect the token.
"""

from __future__ import annotations

from collections.abc import Generator, Mapping
from typing import NamedTuple
from urllib.parse import urlsplit, urlunsplit

import httpx
from a2a.client import A2ACardResolver, Client, ClientConfig, ClientFactory
from a2a.types import AgentCard, AgentInterface
from a2a.utils.constants import TransportProtocol

_DEFAULT_PORTS = {"http": 80, "https": 443, "ws": 80, "wss": 443}


class Origin(NamedTuple):
    """A normalized (scheme, host, port) triple — the unit of trust here.

    Two URLs share an origin when all three match, so ``https://h/a`` and
    ``https://h:443/b`` are the same origin while ``http://h`` is not.
    """

    scheme: str
    host: str
    port: int


def origin_of(url: str | httpx.URL) -> Origin:
    """Return the normalized :class:`Origin` of *url*.

    ``httpx.URL`` already lowercases the scheme and host and drops a redundant
    default port, so parsing through it keeps the comparison free of the
    spoofing tricks that trip up raw string matching.
    """
    parsed = url if isinstance(url, httpx.URL) else httpx.URL(url)
    scheme = parsed.scheme.lower()
    return Origin(
        scheme=scheme,
        host=(parsed.host or "").lower(),
        port=parsed.port or _DEFAULT_PORTS.get(scheme, 0),
    )


class OriginPinnedAuth(httpx.Auth):
    """Attach credential headers only to requests aimed at a single origin.

    httpx merges client-level default headers into *every* request regardless
    of destination, which is why credentials must not be set that way on a
    client whose destination is chosen by remote data. As an ``httpx.Auth`` the
    decision is instead made per request, after the target URL is known.
    """

    def __init__(self, headers: Mapping[str, str], origin: Origin) -> None:
        self._headers = dict(headers)
        self._origin = origin

    @property
    def origin(self) -> Origin:
        """The only origin these headers are ever sent to."""
        return self._origin

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        """Inject the credential headers iff *request* targets ``origin``.

        Used for both sync and async clients: httpx's default
        ``async_auth_flow`` delegates here, which is safe because this does no
        I/O.
        """
        if origin_of(request.url) == self._origin:
            request.headers.update(self._headers)
        yield request


def select_interface(card: AgentCard, config: ClientConfig) -> AgentInterface | None:
    """Find the interface ``ClientFactory.create`` will choose for *card*."""
    client_set = config.supported_protocol_bindings or [TransportProtocol.JSONRPC]
    interfaces = list(card.supported_interfaces)
    find_best = getattr(ClientFactory, "_find_best_interface", None)

    def _best(proto: str) -> AgentInterface | None:
        if find_best is not None:
            return find_best(interfaces, protocol_bindings=[proto])
        return next((i for i in interfaces if i.protocol_binding == proto), None)

    if config.use_client_preference:
        for proto in client_set:
            selected = _best(proto)
            if selected:
                return selected
    else:
        for iface in interfaces:
            if iface.protocol_binding in client_set:
                selected = _best(iface.protocol_binding)
                if selected:
                    return selected
    return None


async def create_pinned_client(
    base_url: str, config: ClientConfig
) -> tuple[Client, list[str]]:
    """Resolve the agent at ``base_url`` into a client that can only talk to it.

    Returns the client and the off-origin URL of the selected transport if it
    was rewritten onto ``base_url``'s origin, or an empty list if the selected
    transport was already same-origin.

    This exists as one function because the ordering is a security invariant,
    not a style choice: ``ClientFactory.create`` reads its transport endpoint
    straight out of the card and never compares it to ``base_url``, so the card
    must be pinned in between. Keeping resolve/pin/create together means a
    caller cannot accidentally build an unpinned client.
    """
    if config.httpx_client is None:
        raise ValueError("config.httpx_client is required")
    card = await A2ACardResolver(config.httpx_client, base_url).get_agent_card()
    selected = select_interface(card, config)
    redirected = (
        [selected.url]
        if selected and origin_of(selected.url) != origin_of(base_url)
        else []
    )
    pin_card_to_origin(card, base_url)
    return ClientFactory(config).create(card), redirected


def pin_card_to_origin(card: AgentCard, base_url: str) -> list[str]:
    """Rewrite *card*'s advertised endpoints onto the origin of ``base_url``.

    Mutates ``card.supported_interfaces`` in place. Each interface keeps its own
    path and query — only scheme, host and port are replaced — so an agent that
    legitimately serves its card at one path and its RPC endpoint at another
    keeps working, while the destination host stays the one the user asked for.

    Returns the distinct off-origin URLs that were rewritten, in the order
    encountered.
    """
    target = origin_of(base_url)
    rewritten: list[str] = []
    for interface in card.supported_interfaces:
        if origin_of(interface.url) == target:
            continue
        if interface.url not in rewritten:
            rewritten.append(interface.url)
        interface.url = _with_origin(interface.url, base_url)
    return rewritten


def _with_origin(url: str, base_url: str) -> str:
    """Return *url*'s path and query re-hosted on ``base_url``'s origin.

    A card URL that is empty or carries no path falls back to ``base_url``'s own
    path, which is the endpoint the card was just served from — the best
    available guess and, more importantly, one the caller already trusts.
    """
    base = urlsplit(base_url)
    parts = urlsplit(url)
    return urlunsplit(
        (base.scheme, base.netloc, parts.path or base.path, parts.query, "")
    )
