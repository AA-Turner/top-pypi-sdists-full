"""Policy tests for the SSRF-hardened fetch. All offline."""

import socket

import httpx
import pytest

import importlib

sf = importlib.import_module("xpander_sdk.utils.safe_fetch")


@pytest.fixture(autouse=True)
def _no_ambient_proxy(monkeypatch):
    """Pin every test to the direct path unless it sets proxy env itself."""
    for var in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
                "http_proxy", "https_proxy", "all_proxy", "no_proxy"):
        monkeypatch.delenv(var, raising=False)



@pytest.mark.parametrize(
    "ip,blocked",
    [
        ("127.0.0.1", True), ("10.0.0.1", True), ("172.16.0.1", True),
        ("172.31.255.255", True), ("192.168.1.1", True), ("169.254.169.254", True),
        ("100.64.0.1", True), ("100.127.255.255", True), ("0.0.0.0", True),
        ("::1", True), ("fd00::1", True), ("fe80::1", True),
        ("::ffff:127.0.0.1", True), ("::ffff:10.0.0.1", True), ("224.0.0.1", True),
        ("8.8.8.8", False), ("1.1.1.1", False), ("172.32.0.1", False),
        ("100.128.0.1", False), ("::ffff:8.8.8.8", False), ("2606:4700::1", False),
    ],
)
def test_ip_classifier(ip, blocked):
    assert sf._ip_is_blocked(ip) is blocked



@pytest.mark.parametrize("host,blocked", [
    ("127.0.0.1", True), ("2130706433", True), ("0x7f000001", True), ("127.1", True),
    ("::1", True), ("[::1]", True), ("169.254.169.254", True), ("localhost", True),
    ("10.0.0.1", True), ("172.16.0.1", True), ("100.64.0.1", True),
    ("8.8.8.8", False), ("example.com", False), ("2606:4700::1", False),
])
def test_literal_host_blocked(host, blocked):
    assert sf.literal_host_blocked(host) is blocked



def _stub_getaddrinfo(monkeypatch, mapping):
    """host -> list of IP strings; unknown hosts raise gaierror."""
    def fake(host, port, *a, **k):
        if host not in mapping:
            raise socket.gaierror("name not resolved")
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port)) for ip in mapping[host]]
    monkeypatch.setattr(sf.socket, "getaddrinfo", fake)


@pytest.mark.parametrize("url", [
    "http://2130706433/", "http://0x7f000001/", "http://127.1/",
    "http://[::1]/", "http://169.254.169.254/latest/meta-data/",
])
def test_encoded_localhost_blocked(url):
    blocked, _ = sf.is_blocked_host(url)
    assert blocked


def test_cluster_dns_name_blocked(monkeypatch):
    _stub_getaddrinfo(monkeypatch, {})  # nothing resolves
    assert sf.is_blocked_host("http://deployment-manager:8000/orgs.json")[0]
    assert sf.is_blocked_host("http://redis:6379/")[0]


def test_scheme_and_host_required():
    assert sf.is_blocked_host("file:///etc/passwd")[0]
    assert sf.is_blocked_host("gopher://x/")[0]
    assert sf.is_blocked_host("http:///nohost")[0]


def test_any_private_address_refuses(monkeypatch):
    # a host that returns [public, private] must be refused, not raced
    _stub_getaddrinfo(monkeypatch, {"evil.example": ["8.8.8.8", "10.0.0.5"]})
    with pytest.raises(sf.SafeFetchError):
        sf._resolve_validated("evil.example", 443)


def test_public_host_allowed(monkeypatch):
    _stub_getaddrinfo(monkeypatch, {"cdn.example": ["8.8.8.8", "1.1.1.1"]})
    assert sf._resolve_validated("cdn.example", 443) == ["8.8.8.8", "1.1.1.1"]



def _mock_pinned(monkeypatch, handler):
    """Replace the pinned transport with a MockTransport running `handler`."""
    def factory(ip, *, is_async, verify):
        return httpx.MockTransport(handler)
    monkeypatch.setattr(sf, "_pinned_transport", factory)


def test_redirect_to_private_is_blocked(monkeypatch):
    _stub_getaddrinfo(monkeypatch, {"public.example": ["8.8.8.8"]})
    # target of the redirect resolves private → the second hop must refuse

    def add_private(host, port, *a, **k):
        table = {"public.example": ["8.8.8.8"], "internal.example": ["10.0.0.9"]}
        if host not in table:
            raise socket.gaierror("nope")
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port)) for ip in table[host]]
    monkeypatch.setattr(sf.socket, "getaddrinfo", add_private)

    def handler(request):
        return httpx.Response(302, headers={"location": "http://internal.example/secret"})
    _mock_pinned(monkeypatch, handler)

    with pytest.raises(sf.SafeFetchError):
        sf.safe_fetch("http://public.example/start", timeout=5)


def test_redirect_chain_followed(monkeypatch):
    table = {"a.example": ["8.8.8.8"], "b.example": ["1.1.1.1"]}

    def gai(host, port, *a, **k):
        if host not in table:
            raise socket.gaierror("nope")
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port)) for ip in table[host]]
    monkeypatch.setattr(sf.socket, "getaddrinfo", gai)

    def handler(request):
        if request.url.host == "8.8.8.8":  # first hop, pinned IP
            return httpx.Response(302, headers={"location": "http://b.example/final"})
        return httpx.Response(200, content=b"ok", headers={"content-type": "text/plain"})
    _mock_pinned(monkeypatch, handler)

    r = sf.safe_fetch("http://a.example/start", timeout=5)
    assert r.status == 200 and r.content == b"ok"


def test_next_redirect_joins_hostname_not_pinned_ip():
    # response.url carries the pinned IP; the relative Location must resolve against
    # the logical hostname base_url, never the IP
    resp = httpx.Response(
        302,
        headers={"location": "/final"},
        request=httpx.Request("GET", "http://8.8.8.8/start"),  # pinned-IP request url
    )
    assert sf._next_redirect(resp, "http://a.example/start") == "http://a.example/final"


def test_relative_redirect_keeps_hostname(monkeypatch):
    # a relative Location must resolve against the hostname, not the pinned IP
    table = {"a.example": ["8.8.8.8"]}

    def gai(host, port, *a, **k):
        if host not in table:
            raise socket.gaierror("nope")
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port)) for ip in table[host]]
    monkeypatch.setattr(sf.socket, "getaddrinfo", gai)

    seen = {}

    def handler(request):
        seen.setdefault("targets", []).append(str(request.url))
        if request.url.path == "/start":
            return httpx.Response(302, headers={"location": "/final"})  # relative
        return httpx.Response(200, content=b"ok")
    _mock_pinned(monkeypatch, handler)

    r = sf.safe_fetch("http://a.example/start", timeout=5)
    assert r.status == 200 and r.content == b"ok"
    assert r.final_url == "http://a.example/final"  # hostname preserved, not the IP


def test_http_error_not_retried_across_ips(monkeypatch):
    # a 403 is a real answer, not a connection failure: no per-IP retry, real status
    monkeypatch.setattr(sf.socket, "getaddrinfo",
                        lambda *a, **k: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 443)),
                                         (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("1.1.1.1", 443))])
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(403, content=b"denied")
    _mock_pinned(monkeypatch, handler)

    with pytest.raises(sf.SafeFetchError) as ei:
        sf.safe_fetch("http://multi.example/x", timeout=5)
    assert "403" in str(ei.value)
    assert calls["n"] == 1  # not retried against the second IP


def test_headers_only_probe_survives_range_ignoring_host(monkeypatch):
    # max_bytes=0 returns headers without consuming a body the server streamed anyway
    monkeypatch.setattr(sf.socket, "getaddrinfo",
                        lambda *a, **k: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 443))])

    def handler(request):
        return httpx.Response(200, content=b"x" * 5_000_000,
                              headers={"content-length": "5000000"})
    _mock_pinned(monkeypatch, handler)

    r = sf.safe_fetch("http://big.example/f", max_bytes=0, timeout=5)
    assert r.headers.get("content-length") == "5000000"
    assert r.content == b""


def test_byte_cap_mid_stream(monkeypatch):
    _stub_getaddrinfo(monkeypatch, {"big.example": ["8.8.8.8"]})

    def handler(request):
        return httpx.Response(200, content=b"x" * 5000)
    _mock_pinned(monkeypatch, handler)

    with pytest.raises(sf.SafeFetchError):
        sf.safe_fetch("http://big.example/blob", max_bytes=1000, timeout=5)


def test_redirect_budget(monkeypatch):
    _stub_getaddrinfo(monkeypatch, {"loop.example": ["8.8.8.8"]})

    def handler(request):
        return httpx.Response(302, headers={"location": "http://loop.example/again"})
    _mock_pinned(monkeypatch, handler)

    with pytest.raises(sf.SafeFetchError):
        sf.safe_fetch("http://loop.example/", timeout=5)


def test_legacy_mode_skips_policy(monkeypatch):
    monkeypatch.setenv("XPANDER_SAFE_FETCH", "legacy")
    # is_blocked_host must report allowed under the kill switch
    assert sf.is_blocked_host("http://169.254.169.254/")[0] is False


def test_warn_mode_reports_but_allows(monkeypatch):
    monkeypatch.setenv("XPANDER_SAFE_FETCH", "warn")
    _stub_getaddrinfo(monkeypatch, {})  # everything fails to resolve

    calls = {"n": 0}

    def legacy(url, method, headers, max_bytes, timeout):
        calls["n"] += 1
        return sf.FetchResult(b"", None, url, 200, {})
    monkeypatch.setattr(sf, "_legacy_sync", legacy)

    sf.safe_fetch("http://redis:6379/", timeout=1)
    assert calls["n"] == 1  # warned, then fetched via legacy


def test_fetch_resolves_exactly_once(monkeypatch):
    """No second name lookup happens, so there is nothing for a rebind to flip."""
    resolved = {"n": 0}

    def gai(host, port, *a, **k):
        resolved["n"] += 1
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", port))]
    monkeypatch.setattr(sf.socket, "getaddrinfo", gai)
    _mock_pinned(monkeypatch, lambda request: httpx.Response(200, content=b"ok"))

    sf.safe_fetch("http://rebind.example/", timeout=5)
    assert resolved["n"] == 1


def test_pin_rewrite_dials_ip_keeps_host():
    """The transport dials the validated IP while Host + SNI stay the hostname."""
    transport = sf._pinned_transport("8.8.8.8", is_async=False, verify=False)
    request = httpx.Request("GET", "http://rebind.example:8080/x")
    rewritten = transport._rewrite(request)
    assert rewritten.url.host == "8.8.8.8"                       # socket target
    assert rewritten.headers["Host"] == "rebind.example:8080"   # vhost preserved
    assert rewritten.extensions["sni_hostname"] == "rebind.example"  # TLS name preserved


def test_is_blocked_host_warn_mode(monkeypatch):
    # warn never blocks, but marks the reason so a caller can log a would-block
    monkeypatch.setenv("XPANDER_SAFE_FETCH", "warn")
    blocked, reason = sf.is_blocked_host("http://169.254.169.254/")
    assert blocked is False
    assert reason.startswith("warn-would-block")


def test_malformed_port_is_policy_error_not_valueerror():
    # http://h:abc/ must not raise a raw ValueError past the (blocked, reason) contract
    blocked, reason = sf.is_blocked_host("http://host:abc/")
    assert blocked is True
    with pytest.raises(sf.SafeFetchError):
        sf._split_target("http://host:abc/")


def test_authority_brackets_ipv6():
    assert sf._authority("::1", 8080) == "[::1]:8080"
    assert sf._authority("2606:4700::1", 443) == "[2606:4700::1]"
    assert sf._authority("example.com", 8080) == "example.com:8080"
    assert sf._authority("example.com", 443) == "example.com"


def test_deadline_raises_when_spent():
    import time
    with pytest.raises(sf.SafeFetchError):
        sf._remaining(time.monotonic() - 1)


def test_asafe_fetch_happy_path(monkeypatch):
    import asyncio
    monkeypatch.setattr(sf.socket, "getaddrinfo",
                        lambda *a, **k: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 443))])
    _mock_pinned(monkeypatch, lambda request: httpx.Response(200, content=b"ok",
                                                             headers={"content-type": "text/plain"}))
    r = asyncio.run(sf.asafe_fetch("http://a.example/x", timeout=5))
    assert r.status == 200 and r.content == b"ok" and r.content_type == "text/plain"


def test_asafe_fetch_blocks_internal(monkeypatch):
    import asyncio
    monkeypatch.setattr(sf.socket, "getaddrinfo",
                        lambda *a, **k: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.1", 443))])
    with pytest.raises(sf.SafeFetchError):
        asyncio.run(sf.asafe_fetch("http://internal.example/x", timeout=5))


# ---------------------------------------------------------------------------
# egress allowlist (XPANDER_EGRESS_ALLOWLIST)
# ---------------------------------------------------------------------------

def test_allowlist_unset_is_passthrough(monkeypatch):
    monkeypatch.delenv("XPANDER_EGRESS_ALLOWLIST", raising=False)
    _stub_getaddrinfo(monkeypatch, {"anything.example": ["8.8.8.8"]})
    assert sf.is_blocked_host("https://anything.example/f")[0] is False


def test_allowlist_blank_is_passthrough(monkeypatch):
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "   ")
    _stub_getaddrinfo(monkeypatch, {"anything.example": ["8.8.8.8"]})
    assert sf.is_blocked_host("https://anything.example/f")[0] is False


def test_allowlist_blocks_unlisted_host(monkeypatch):
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "example.com")
    _stub_getaddrinfo(monkeypatch, {"other.example": ["8.8.8.8"]})
    blocked, reason = sf.is_blocked_host("https://other.example/f")
    assert blocked is True
    assert "approved host" in reason


def test_allowlist_allows_listed_host_and_subdomain(monkeypatch):
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "example.com, cdn.other.net")
    _stub_getaddrinfo(monkeypatch, {
        "example.com": ["8.8.8.8"],
        "sub.example.com": ["8.8.8.8"],
        "cdn.other.net": ["8.8.8.8"],
    })
    for url in ("https://example.com/", "https://sub.example.com/", "https://cdn.other.net/"):
        assert sf.is_blocked_host(url)[0] is False
    # suffix must match on a label boundary, not a substring
    _stub_getaddrinfo(monkeypatch, {"evilexample.com": ["8.8.8.8"]})
    assert sf.is_blocked_host("https://evilexample.com/")[0] is True


def test_allowlist_fetch_listed_host_succeeds(monkeypatch):
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "example.com")
    _stub_getaddrinfo(monkeypatch, {"sub.example.com": ["8.8.8.8"]})
    _mock_pinned(monkeypatch, lambda request: httpx.Response(200, content=b"ok"))
    r = sf.safe_fetch("https://sub.example.com/f", timeout=5)
    assert r.status == 200 and r.content == b"ok"


def test_allowlist_fetch_unlisted_host_refused(monkeypatch):
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "example.com")
    _stub_getaddrinfo(monkeypatch, {"other.example": ["8.8.8.8"]})
    with pytest.raises(sf.SafeFetchError, match="approved host"):
        sf.safe_fetch("https://other.example/f", timeout=5)


def test_allowlist_redirect_to_unlisted_host_refused(monkeypatch):
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "example.com")
    _stub_getaddrinfo(monkeypatch, {"example.com": ["8.8.8.8"], "other.example": ["1.1.1.1"]})
    _mock_pinned(monkeypatch, lambda request: httpx.Response(
        302, headers={"location": "https://other.example/leak"}))
    with pytest.raises(sf.SafeFetchError, match="approved host"):
        sf.safe_fetch("https://example.com/f", timeout=5)


def test_allowlist_overrides_legacy_and_warn_modes(monkeypatch):
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "example.com")
    for mode in ("legacy", "warn"):
        monkeypatch.setenv("XPANDER_SAFE_FETCH", mode)
        assert sf.is_blocked_host("http://169.254.169.254/latest/meta-data/")[0] is True


def test_allowlist_metadata_denied_even_if_listed(monkeypatch):
    """A listed link-local/metadata literal is still refused by the address policy."""
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "169.254.169.254,example.com")
    assert sf.is_blocked_host("http://169.254.169.254/latest/meta-data/")[0] is True


def test_allowlist_asafe_fetch(monkeypatch):
    import asyncio
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "example.com")
    monkeypatch.setattr(sf.socket, "getaddrinfo",
                        lambda *a, **k: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 443))])
    _mock_pinned(monkeypatch, lambda request: httpx.Response(200, content=b"ok"))
    r = asyncio.run(sf.asafe_fetch("https://example.com/f", timeout=5))
    assert r.status == 200
    with pytest.raises(sf.SafeFetchError, match="approved host"):
        asyncio.run(sf.asafe_fetch("https://other.example/f", timeout=5))


# ---------------------------------------------------------------------------
# internal-fetch allowlist (XPANDER_INTERNAL_FETCH_ALLOWLIST)
# ---------------------------------------------------------------------------

_PRIVATE_SVC = {"fake-llm": ["10.96.254.50"]}


def test_internal_unset_keeps_private_blocked(monkeypatch):
    """Unset env is byte-identical to today: every private resolution refuses."""
    monkeypatch.delenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", raising=False)
    _stub_getaddrinfo(monkeypatch, _PRIVATE_SVC)
    blocked, reason = sf.is_blocked_host("http://fake-llm/docs")
    assert blocked is True and "blocked address" in reason


def test_internal_blank_is_passthrough(monkeypatch):
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "  , ")
    _stub_getaddrinfo(monkeypatch, _PRIVATE_SVC)
    assert sf.is_blocked_host("http://fake-llm/docs")[0] is True


def test_internal_listed_host_private_allowed(monkeypatch):
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "fake-llm")
    _stub_getaddrinfo(monkeypatch, _PRIVATE_SVC)
    assert sf.is_blocked_host("http://fake-llm/docs")[0] is False
    _mock_pinned(monkeypatch, lambda request: httpx.Response(200, content=b"ok"))
    r = sf.safe_fetch("http://fake-llm/docs", timeout=5)
    assert r.status == 200 and r.content == b"ok"


def test_internal_suffix_entry_matches_cluster_names(monkeypatch):
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", ".svc, .cluster.local")
    _stub_getaddrinfo(monkeypatch, {
        "fake-llm.xpander-cert.svc": ["10.96.254.50"],
        "kb.xpander-cert.svc.cluster.local": ["10.96.1.2"],
        "othersvc": ["10.96.9.9"],
    })
    assert sf.is_blocked_host("http://fake-llm.xpander-cert.svc/docs")[0] is False
    assert sf.is_blocked_host("http://kb.xpander-cert.svc.cluster.local/x")[0] is False
    # a bare name outside the listed suffixes stays blocked
    assert sf.is_blocked_host("http://othersvc/x")[0] is True


def test_internal_unlisted_private_refused(monkeypatch):
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "fake-llm")
    _stub_getaddrinfo(monkeypatch, {"redis": ["10.96.0.7"]})
    with pytest.raises(sf.SafeFetchError, match="blocked address"):
        sf.safe_fetch("http://redis:6379/", timeout=5)


def test_internal_metadata_refused_even_when_listed(monkeypatch):
    """Link-local/metadata is the always-deny: no allowlist entry reopens it."""
    monkeypatch.setenv(
        "XPANDER_INTERNAL_FETCH_ALLOWLIST",
        "169.254.169.254,169.254.0.0/16,metadata.internal,0.0.0.0/0",
    )
    assert sf.is_blocked_host("http://169.254.169.254/latest/meta-data/")[0] is True
    _stub_getaddrinfo(monkeypatch, {"metadata.internal": ["169.254.169.254"]})
    with pytest.raises(sf.SafeFetchError):
        sf.safe_fetch("http://metadata.internal/latest/meta-data/", timeout=5)


@pytest.mark.parametrize("ip", ["169.254.0.9", "fe80::1", "224.0.0.1", "0.0.0.0", "240.0.0.1"])
def test_internal_hard_ranges_survive_catch_all_cidr(monkeypatch, ip):
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "0.0.0.0/0,::/0")
    _stub_getaddrinfo(monkeypatch, {"h.example": [ip]})
    assert sf.is_blocked_host("http://h.example/")[0] is True


def test_internal_cidr_entry_allows_range_only(monkeypatch):
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "10.96.0.0/12")
    _stub_getaddrinfo(monkeypatch, {"inrange.local": ["10.96.254.50"], "outofrange.local": ["10.0.0.5"]})
    assert sf.is_blocked_host("http://inrange.local/")[0] is False
    assert sf.is_blocked_host("http://outofrange.local/")[0] is True
    # literal IPs inside the CIDR pass too
    _stub_getaddrinfo(monkeypatch, {"10.96.254.50": ["10.96.254.50"]})
    assert sf.is_blocked_host("http://10.96.254.50/")[0] is False


def test_internal_redirect_to_unlisted_private_refused(monkeypatch):
    """A listed internal host 302ing to an unlisted private IP is refused at the hop."""
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "fake-llm")
    _stub_getaddrinfo(monkeypatch, {"fake-llm": ["10.96.254.50"], "10.0.0.9": ["10.0.0.9"]})
    _mock_pinned(monkeypatch, lambda request: httpx.Response(
        302, headers={"location": "http://10.0.0.9/secret"}))
    with pytest.raises(sf.SafeFetchError, match="blocked address"):
        sf.safe_fetch("http://fake-llm/docs", timeout=5)


def test_internal_redirect_between_listed_hosts_ok(monkeypatch):
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", ".svc")
    _stub_getaddrinfo(monkeypatch, {
        "a.ns.svc": ["10.96.0.1"], "b.ns.svc": ["10.96.0.2"],
    })

    def handler(request):
        if request.url.host == "10.96.0.1":
            return httpx.Response(302, headers={"location": "http://b.ns.svc/final"})
        return httpx.Response(200, content=b"ok")
    _mock_pinned(monkeypatch, handler)
    r = sf.safe_fetch("http://a.ns.svc/start", timeout=5)
    assert r.status == 200 and r.content == b"ok"


def test_internal_and_egress_gates_both_apply(monkeypatch):
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "example.com,fake-llm")
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "fake-llm,intranet.corp")
    _stub_getaddrinfo(monkeypatch, {
        "fake-llm": ["10.96.254.50"],       # listed in both -> passes
        "intranet.corp": ["10.1.2.3"],      # internal-listed only -> egress refuses
        "example.com": ["10.9.9.9"],        # egress-listed only -> private resolve refuses
    })
    assert sf.is_blocked_host("http://fake-llm/docs")[0] is False
    blocked, reason = sf.is_blocked_host("http://intranet.corp/")
    assert blocked is True and "approved host" in reason
    blocked, reason = sf.is_blocked_host("https://example.com/")
    assert blocked is True and "blocked address" in reason


def test_internal_public_hosts_unaffected(monkeypatch):
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "fake-llm")
    _stub_getaddrinfo(monkeypatch, {"cdn.example": ["8.8.8.8"]})
    assert sf.is_blocked_host("https://cdn.example/")[0] is False


def test_internal_asafe_fetch(monkeypatch):
    import asyncio
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "fake-llm")
    _stub_getaddrinfo(monkeypatch, {"fake-llm": ["10.96.254.50"], "redis": ["10.96.0.7"]})
    _mock_pinned(monkeypatch, lambda request: httpx.Response(200, content=b"ok"))
    r = asyncio.run(sf.asafe_fetch("http://fake-llm/docs", timeout=5))
    assert r.status == 200 and r.content == b"ok"
    with pytest.raises(sf.SafeFetchError, match="blocked address"):
        asyncio.run(sf.asafe_fetch("http://redis:6379/", timeout=5))


def test_internal_proxied_path_honors_list(monkeypatch):
    """A proxied hop tolerates a listed locally-private name; unlisted stays refused."""
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.corp.example:3128")
    monkeypatch.setenv("XPANDER_INTERNAL_FETCH_ALLOWLIST", "intranet.corp,10.96.0.0/12")
    _stub_getaddrinfo(monkeypatch, {"intranet.corp": ["10.1.2.3"], "other.corp": ["10.1.2.4"]})

    def fake_hop(proxy, current, method, headers, max_bytes, deadline, host):
        return sf.FetchResult(b"ok", "text/plain", current, 200, {}), None
    monkeypatch.setattr(sf, "_proxied_hop_sync", fake_hop)

    assert sf.safe_fetch("https://intranet.corp/doc", timeout=5).content == b"ok"
    with pytest.raises(sf.SafeFetchError, match="blocked address"):
        sf.safe_fetch("https://other.corp/doc", timeout=5)
    # a literal IP inside a listed CIDR passes the proxied literal check
    _stub_getaddrinfo(monkeypatch, {})
    assert sf.safe_fetch("https://10.96.254.50/doc", timeout=5).content == b"ok"
    # metadata literal stays refused regardless
    with pytest.raises(sf.SafeFetchError):
        sf.safe_fetch("https://169.254.169.254/latest", timeout=5)


# ---------------------------------------------------------------------------
# corporate proxy (HTTP_PROXY / HTTPS_PROXY / NO_PROXY)
# ---------------------------------------------------------------------------

_PROXY = "http://proxy.corp.example:3128"


def test_env_proxy_for_matches_scheme_and_no_proxy(monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", _PROXY)
    monkeypatch.setenv("NO_PROXY", "internal.example,.svc")
    assert sf._env_proxy_for("https", "api.vendor.example") == _PROXY
    assert sf._env_proxy_for("http", "api.vendor.example") is None
    assert sf._env_proxy_for("https", "internal.example") is None
    assert sf._env_proxy_for("https", "redis.ns.svc") is None


def test_env_proxy_for_unset_env_means_direct():
    assert sf._env_proxy_for("https", "api.vendor.example") is None


def test_proxied_fetch_on_sealed_network(monkeypatch):
    """DNS for external names may not exist at all; the proxy owns resolution."""
    monkeypatch.setenv("HTTPS_PROXY", _PROXY)
    _stub_getaddrinfo(monkeypatch, {})
    seen = {}

    def fake_hop(proxy, current, method, headers, max_bytes, deadline, host):
        seen["proxy"], seen["url"] = proxy, current
        return sf.FetchResult(b"ok", "text/plain", current, 200, {}), None

    monkeypatch.setattr(sf, "_proxied_hop_sync", fake_hop)
    r = sf.safe_fetch("https://api.vendor.example/data", timeout=5)
    assert r.content == b"ok"
    assert seen["proxy"] == _PROXY and seen["url"] == "https://api.vendor.example/data"


def test_proxied_fetch_still_refuses_internal_literal(monkeypatch):
    monkeypatch.setenv("HTTP_PROXY", _PROXY)
    with pytest.raises(sf.SafeFetchError):
        sf.safe_fetch("http://169.254.169.254/latest/meta-data/", timeout=5)


def test_proxied_fetch_still_refuses_locally_internal_name(monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", _PROXY)
    _stub_getaddrinfo(monkeypatch, {"intranet.example": ["10.0.0.5"]})
    with pytest.raises(sf.SafeFetchError):
        sf.safe_fetch("https://intranet.example/", timeout=5)


def test_proxied_fetch_still_enforces_allowlist(monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", _PROXY)
    monkeypatch.setenv("XPANDER_EGRESS_ALLOWLIST", "example.com")
    _stub_getaddrinfo(monkeypatch, {})
    with pytest.raises(sf.SafeFetchError, match="approved host"):
        sf.safe_fetch("https://other.example/f", timeout=5)


def test_proxied_redirect_hops_are_rechecked(monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", _PROXY)
    monkeypatch.setenv("HTTP_PROXY", _PROXY)
    _stub_getaddrinfo(monkeypatch, {})

    def fake_hop(proxy, current, method, headers, max_bytes, deadline, host):
        return None, "http://169.254.169.254/latest"

    monkeypatch.setattr(sf, "_proxied_hop_sync", fake_hop)
    with pytest.raises(sf.SafeFetchError):
        sf.safe_fetch("https://public.vendor.example/", timeout=5)


def test_no_proxy_host_keeps_pinned_direct_path(monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", _PROXY)
    monkeypatch.setenv("NO_PROXY", "pinned.example")
    _stub_getaddrinfo(monkeypatch, {"pinned.example": ["8.8.8.8"]})
    _mock_pinned(monkeypatch, lambda request: httpx.Response(200, content=b"direct"))
    r = sf.safe_fetch("https://pinned.example/x", timeout=5)
    assert r.content == b"direct"


def test_is_blocked_host_proxy_aware(monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", _PROXY)
    _stub_getaddrinfo(monkeypatch, {})
    assert sf.is_blocked_host("https://api.vendor.example/")[0] is False
    # direct classification is unchanged for NO_PROXY targets
    monkeypatch.setenv("NO_PROXY", "api.vendor.example")
    assert sf.is_blocked_host("https://api.vendor.example/")[0] is True


def test_proxied_asafe_fetch(monkeypatch):
    import asyncio
    monkeypatch.setenv("HTTPS_PROXY", _PROXY)
    _stub_getaddrinfo(monkeypatch, {})
    seen = {}

    async def fake_hop(proxy, current, method, headers, max_bytes, deadline, host):
        seen["proxy"] = proxy
        return sf.FetchResult(b"ok", "text/plain", current, 200, {}), None

    monkeypatch.setattr(sf, "_proxied_hop_async", fake_hop)
    r = asyncio.run(sf.asafe_fetch("https://api.vendor.example/data", timeout=5))
    assert r.content == b"ok" and seen["proxy"] == _PROXY
