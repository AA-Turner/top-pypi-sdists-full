"""The http.* nodes never reach a private, loopback, or metadata address.

Use case: Harbor Dental's new-patient intake workflow posts each finished
intake to the practice's scheduling webhook. The person who builds the
workflow controls the URL, so the server must refuse to send that request to
anything inside our own network (ECS metadata, VPC hosts, loopback), even when
a public-looking name resolves there or a public host redirects there.

The network is stubbed at the lowest layer (``httpcore``'s connection pool,
plus ``socket.getaddrinfo``) — never at ``httpx.AsyncClient``, because the
transport the client uses IS the guard under test. Each test names the break
it catches: "the node sends the request anyway".
"""

from __future__ import annotations

import socket
from typing import Any

import httpcore
import pytest
from matrx_graph.nodes.http.custom_api import (
    CustomApiConfig,
    CustomApiInput,
    CustomApiExecutor,
)
from matrx_graph.nodes.http.get import HttpGetConfig, HttpGetExecutor, HttpGetInput
from matrx_graph.nodes.http.graphql import (
    GraphQLConfig,
    GraphQLInput,
    HttpGraphQLExecutor,
)
from matrx_graph.nodes.http.post import HttpPostConfig, HttpPostExecutor, HttpPostInput

# Names the fake DNS answers. 151.101.x is a real public CDN range; 10.x is a VPC.
_DNS = {
    "hooks.harbordentalcare.com": "151.101.65.140",
    "scheduling.harbordentalcare.com": "151.101.1.140",
    "intake-sync.harbordentalcare.com": "10.20.4.17",
    "localhost": "127.0.0.1",
}


class _FakeNetwork:
    """DNS + wire below httpx. Records every request that would leave the box."""

    def __init__(self, responder: Any = None) -> None:
        self.sent: list[httpcore.Request] = []
        self.lookups: list[str] = []
        self._responder = responder or (lambda _req: httpcore.Response(200, content=b"{}"))

    def getaddrinfo(self, host: Any, port: Any, family: int = 0, type: int = 0, proto: int = 0, flags: int = 0):  # noqa: A002
        name = host.decode() if isinstance(host, bytes) else str(host)
        self.lookups.append(name)
        ip = _DNS.get(name.lower().rstrip("."), name)
        try:
            import ipaddress

            parsed = ipaddress.ip_address(ip)
        except ValueError as exc:
            raise socket.gaierror(socket.EAI_NONAME, "Name or service not known") from exc
        fam = socket.AF_INET6 if parsed.version == 6 else socket.AF_INET
        sockaddr = (ip, int(port or 0), 0, 0) if parsed.version == 6 else (ip, int(port or 0))
        return [(fam, socket.SOCK_STREAM, 6, "", sockaddr)]

    async def handle(self, _pool: Any, request: httpcore.Request) -> httpcore.Response:
        self.sent.append(request)
        return self._responder(request)

    def install(self, monkeypatch: pytest.MonkeyPatch) -> _FakeNetwork:
        monkeypatch.setattr(socket, "getaddrinfo", self.getaddrinfo)
        net = self

        async def _pool_handle(pool: Any, request: httpcore.Request) -> httpcore.Response:
            return await net.handle(pool, request)

        monkeypatch.setattr(httpcore.AsyncConnectionPool, "handle_async_request", _pool_handle)
        return self

    def hosts(self) -> list[str]:
        return [r.url.host.decode() for r in self.sent]


@pytest.mark.parametrize(
    "url",
    [
        "https://10.20.4.17/intake",
        "https://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "https://169.254.170.2/v2/credentials",
        "https://localhost/intake",
        "https://intake-sync.harbordentalcare.com/intake",  # resolves to 10.x
    ],
)
async def test_post_to_an_internal_address_is_refused_before_any_request(
    monkeypatch: pytest.MonkeyPatch, url: str
) -> None:
    net = _FakeNetwork().install(monkeypatch)

    out = await HttpPostExecutor().execute(
        ctx=None,  # type: ignore[arg-type]
        inputs=HttpPostInput(url=url, json_body={"patient": "Marisol Ortega", "visit": "cleaning"}),
        config=HttpPostConfig(),
    )

    assert net.sent == [], f"request left the server for {url}: {net.hosts()}"
    assert out.status == "error"
    assert out.error.code == "outbound_address_refused"
    assert "private or internal" in out.error.message


async def test_redirect_to_a_private_address_is_refused_at_the_hop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def responder(req: httpcore.Request) -> httpcore.Response:
        # The public host answers with a redirect into the VPC.
        return httpcore.Response(
            307, headers=[(b"location", b"https://10.20.4.17/admin/export")], content=b""
        )

    net = _FakeNetwork(responder).install(monkeypatch)

    out = await HttpPostExecutor().execute(
        ctx=None,  # type: ignore[arg-type]
        inputs=HttpPostInput(
            url="https://hooks.harbordentalcare.com/new-patient",
            json_body={"patient": "Marisol Ortega"},
        ),
        config=HttpPostConfig(follow_redirects=True),
    )

    # The first hop (public) went out; the second (10.x) never did.
    assert net.hosts() == ["151.101.65.140"]
    assert out.status == "error"
    assert out.error.code == "outbound_address_refused"


async def test_get_and_graphql_and_custom_api_refuse_the_metadata_address(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    net = _FakeNetwork().install(monkeypatch)
    metadata = "https://169.254.169.254/latest/meta-data/"

    got = await HttpGetExecutor().execute(
        ctx=None,  # type: ignore[arg-type]
        inputs=HttpGetInput(url=metadata),
        config=HttpGetConfig(),
    )
    gql = await HttpGraphQLExecutor().execute(
        ctx=None,  # type: ignore[arg-type]
        inputs=GraphQLInput(endpoint=metadata, query="{ patients { id } }"),
        config=GraphQLConfig(),
    )
    custom = await CustomApiExecutor().execute(
        ctx=None,  # type: ignore[arg-type]
        inputs=CustomApiInput(url=metadata, method="GET"),
        config=CustomApiConfig(max_retries=3, backoff_base_s=0.0, max_backoff_s=0.1),
    )

    assert net.sent == []
    assert [got.error.code, gql.error.code, custom.error.code] == ["outbound_address_refused"] * 3


async def test_custom_api_never_retries_a_refused_address(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    net = _FakeNetwork().install(monkeypatch)

    out = await CustomApiExecutor().execute(
        ctx=None,  # type: ignore[arg-type]
        inputs=CustomApiInput(url="https://intake-sync.harbordentalcare.com/export", method="POST"),
        config=CustomApiConfig(max_retries=4, backoff_base_s=0.0, max_backoff_s=0.1),
    )

    assert net.sent == []
    assert net.lookups == ["intake-sync.harbordentalcare.com"]
    assert out.status == "error"
    assert out.error.code == "outbound_address_refused"


async def test_plain_http_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    net = _FakeNetwork().install(monkeypatch)
    out = await HttpPostExecutor().execute(
        ctx=None,  # type: ignore[arg-type]
        inputs=HttpPostInput(url="http://hooks.harbordentalcare.com/new-patient", json_body={}),
        config=HttpPostConfig(),
    )
    assert net.sent == []
    assert out.status == "error"
    assert "https://" in out.error.message


@pytest.mark.parametrize(
    ("url", "pinned_ip", "host_header"),
    [
        ("https://hooks.harbordentalcare.com/new-patient", "151.101.65.140", "hooks.harbordentalcare.com"),
        ("https://scheduling.harbordentalcare.com/v1/visits", "151.101.1.140", "scheduling.harbordentalcare.com"),
    ],
)
async def test_public_https_post_is_sent_pinned_to_the_ip_that_was_checked(
    monkeypatch: pytest.MonkeyPatch, url: str, pinned_ip: str, host_header: str
) -> None:
    net = _FakeNetwork(
        lambda _r: httpcore.Response(
            201, headers=[(b"content-type", b"application/json")], content=b'{"visit_id": "v-8841"}'
        )
    ).install(monkeypatch)

    out = await HttpPostExecutor().execute(
        ctx=None,  # type: ignore[arg-type]
        inputs=HttpPostInput(url=url, json_body={"patient": "Marisol Ortega"}),
        config=HttpPostConfig(),
    )

    assert out.status == "success"
    assert out.result.status == 201
    assert out.result.body == {"visit_id": "v-8841"}
    # The person sees their own URL, never our pinned IP.
    assert out.result.url == url
    [sent] = net.sent
    assert sent.url.host.decode() == pinned_ip
    assert dict(sent.headers)[b"Host"].decode() == host_header
    assert sent.extensions.get("sni_hostname") == host_header


def test_fake_network_resolves_like_the_real_one() -> None:
    """Self-check of the double: unknown names fail like real DNS does."""
    net = _FakeNetwork()
    assert net.getaddrinfo("hooks.harbordentalcare.com", 443)[0][4][0] == "151.101.65.140"
    with pytest.raises(socket.gaierror):
        net.getaddrinfo("no-such-host.harbordentalcare.com", 443)
