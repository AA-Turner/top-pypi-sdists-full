"""Audit fixture harness — the REAL crawler and the REAL checks over a site we control.

What is real here, and what stands in for what (every stand-in is named):

* **Real:** the HTTP server bytes (``tests/fixtures/audit_site/<site>/``), TLS
  (a throwaway CA the harness mints per run), ``SiteCrawler`` with the in-memory
  frontier production uses for short runs, the page parser, the snapshot
  column mapping (``persistence.snapshot_evidence_columns`` — the same function
  the DB persister writes), ``analysis._extract_page_facts`` /
  ``_extract_transport_facts``, every aggregate builder (``index_page_facts``,
  ``_accumulate_edge``, ``_bfs_depths``, ``_build_orphan_census``,
  ``build_site_graph`` + ``resolve_edge_rows`` + ``compute_link_scores``), the
  external link checker (``link_check.check_urls``), the site probe
  (``site_probe.probe_site``), the sitemap walk
  (``sitemaps.crawl_sitemap_documents``), the sitemap junk fold
  (``site_analysis.fold_sitemap_members``), and every check function in
  ``analysis.PAGE_CHECKS`` / ``analysis.SITE_CHECKS``.
* **Stand-in — the database.** ``FixtureWebStore`` keeps ``web.page`` /
  ``web.snapshot`` / ``web.link_edge`` / ``web.crawl_url`` rows in memory. It
  mirrors the four write rules the analysis depends on, each named at its
  method: crawl identity (``url_identity.resolve_crawl_page_identity`` — the
  declared same-site canonical, else the final URL, owns the snapshot; every
  other observed URL becomes its alias), failed-URL rows
  (``persistence._persist_failed_url_in_active_transaction`` +
  ``failed_fetch_disposition``), internal edge status
  (``link_check._select_internal_status``, called directly), and sitemap
  membership (``sitemap_sync._upsert_pages_and_memberships``).
* **Stand-in — the network policy.** The crawler's SSRF gate refuses loopback
  (``utils.url.validate_public_http_url`` rejects ``127.*``), so
  ``allow_fixture_origins`` lets EXACTLY the fixture origins through and
  delegates every other URL to the real gate; and ``block_outside_network``
  refuses any socket that is not loopback, so the suite runs with no network.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import ipaddress
import json
import random
import re
import socket
import ssl
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from urllib.parse import urlsplit

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "audit_site"
RAISED_STATUSES = frozenset({"warn", "fail"})
_TEMPLATE_TOKENS = ("{{origin}}", "{{external}}")


# ---------------------------------------------------------------------------
# TLS — a per-run CA, so the fixture is https:// like every site we audit.


@dataclass(frozen=True)
class FixtureTls:
    cert_chain: Path
    key: Path
    ca_bundle: Path  # certifi's public roots + this run's CA


def mint_fixture_tls(directory: Path, *, leaf_days: int = 90) -> FixtureTls:
    import certifi
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

    now = dt.datetime.now(dt.UTC)
    ca_key = ec.generate_private_key(ec.SECP256R1())
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Matrx audit fixture CA")])
    ca = (
        x509.CertificateBuilder()
        .subject_name(ca_name)
        .issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - dt.timedelta(days=1))
        .not_valid_after(now + dt.timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .sign(ca_key, hashes.SHA256())
    )
    leaf_key = ec.generate_private_key(ec.SECP256R1())
    leaf = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "127.0.0.1")]))
        .issuer_name(ca_name)
        .public_key(leaf_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - dt.timedelta(days=1))
        .not_valid_after(now + dt.timedelta(days=leaf_days))
        .add_extension(
            x509.SubjectAlternativeName(
                [x509.IPAddress(ipaddress.ip_address("127.0.0.1")), x509.DNSName("localhost")]
            ),
            critical=False,
        )
        .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(leaf_key.public_key()), critical=False
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )
    directory.mkdir(parents=True, exist_ok=True)
    pem = serialization.Encoding.PEM
    chain = directory / f"leaf-{leaf_days}.pem"
    key = directory / f"leaf-{leaf_days}.key"
    bundle = directory / f"bundle-{leaf_days}.pem"
    chain.write_bytes(leaf.public_bytes(pem) + ca.public_bytes(pem))
    key.write_bytes(
        leaf_key.private_bytes(pem, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    )
    bundle.write_bytes(Path(certifi.where()).read_bytes() + ca.public_bytes(pem))
    return FixtureTls(cert_chain=chain, key=key, ca_bundle=bundle)


def trust_fixture_ca(monkeypatch: Any, tls: FixtureTls) -> None:
    """Make every transport the pipeline uses trust this run's CA — and only add it."""

    import curl_cffi.curl as curl_module

    monkeypatch.setenv("SSL_CERT_FILE", str(tls.ca_bundle))
    monkeypatch.setattr(curl_module, "DEFAULT_CACERT", str(tls.ca_bundle))


# ---------------------------------------------------------------------------
# Network policy — loopback only, and only the fixture origins past the SSRF gate.


def block_outside_network(monkeypatch: Any) -> None:
    """Refuse every non-loopback socket: the harness must never touch the internet."""

    real_connect = socket.socket.connect
    real_connect_ex = socket.socket.connect_ex
    real_getaddrinfo = socket.getaddrinfo

    def _local(address: Any) -> bool:
        if not isinstance(address, tuple) or not address:
            return True  # AF_UNIX and friends
        host = str(address[0])
        if host == "localhost":
            return True
        try:
            return ipaddress.ip_address(host.split("%")[0]).is_loopback
        except ValueError:
            return False

    def connect(self: socket.socket, address: Any) -> Any:
        if not _local(address):
            raise OSError(f"audit fixture harness: outside network refused ({address!r})")
        return real_connect(self, address)

    def connect_ex(self: socket.socket, address: Any) -> Any:
        if not _local(address):
            raise OSError(f"audit fixture harness: outside network refused ({address!r})")
        return real_connect_ex(self, address)

    def getaddrinfo(host: Any, *args: Any, **kwargs: Any) -> Any:
        name = host.decode() if isinstance(host, bytes) else host
        if name not in (None, "localhost") and not _local((name,)):
            raise socket.gaierror(f"audit fixture harness: outside DNS refused ({host!r})")
        return real_getaddrinfo(host, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", connect)
    monkeypatch.setattr(socket.socket, "connect_ex", connect_ex)
    monkeypatch.setattr(socket, "getaddrinfo", getaddrinfo)
    # The datacenter proxy pool is our infrastructure, not the site's; the
    # fixture crawl goes direct exactly as a proxy-less deployment does.
    monkeypatch.delenv("DATACENTER_PROXIES", raising=False)


def allow_fixture_origins(monkeypatch: Any, origins: list[str]) -> None:
    """The ONE test-only SSRF allowlist: exactly these origins, nothing else.

    ``validate_public_http_url`` (DNS + non-global IP refusal) and
    ``validate_and_correct_url`` (literal ``127.*`` refusal) both reject a
    loopback fixture. Every consumer on the audit path is patched to a wrapper
    that returns a URL on an allowed origin unchanged and delegates every other
    URL to the real gate — so a fixture link pointing anywhere else is still
    refused exactly as production would refuse it.
    """

    from matrx_scraper import crawler, image_evidence, sitemaps
    from matrx_scraper.utils import url as url_utils
    from matrx_scraper.web_crawl import site_probe, sitemap_sync

    allowed = {_origin(o) for o in origins}
    real_public = url_utils.validate_public_http_url
    real_correct = url_utils.validate_and_correct_url

    async def validate_public(url: str) -> str:
        if _origin(url) in allowed:
            return url
        return await real_public(url)

    def validate_correct(url: str) -> str:
        if _origin(url) in allowed:
            return url
        return real_correct(url)

    for module in (crawler, site_probe, sitemaps, image_evidence):
        monkeypatch.setattr(module, "validate_public_http_url", validate_public)
    monkeypatch.setattr(sitemap_sync, "validate_and_correct_url", validate_correct)
    # `enrich_image_inventory` binds its validator as a keyword DEFAULT at
    # definition time; patching the module name alone would not reach it.
    defaults = dict(image_evidence.enrich_image_inventory.__kwdefaults__ or {})
    defaults["validate_url"] = validate_public
    monkeypatch.setattr(image_evidence.enrich_image_inventory, "__kwdefaults__", defaults)

    # Every send-time layer of the address check (guarded clients, fetch(),
    # curl's per-hop pin, the browser request guard): exactly these origins.
    from fixture_origins import allow_fixture_origins

    allow_fixture_origins(monkeypatch, *sorted(allowed))


def _origin(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}".lower()


# ---------------------------------------------------------------------------
# The fixture server — byte-level control of status, headers, timing, bodies.


@dataclass
class Route:
    path: str
    status: int = 200
    file: str | None = None
    body: str | None = None
    content_type: str = "text/html; charset=utf-8"
    headers: dict[str, str] = field(default_factory=dict)
    delay_ms: int = 0
    expected_checks: list[str] | None = None
    why: str = ""
    trap: str | None = None
    #: The route produces no page verdict of its own (a redirect source whose
    #: evidence lands on its target, an asset, robots.txt, a sitemap).
    no_verdict: bool = False
    #: Answers in sequence, one per request (the last repeats): each may set
    #: ``status``, ``headers`` and ``body`` — a 429 that later recovers.
    responses: list[dict[str, Any]] = field(default_factory=list)
    #: This page links to walled or rate-limited targets, which must surface as
    #: ``blocked_targets`` on ``broken_internal_links`` — never as broken.
    expect_blocked_link_targets: bool = False


@dataclass
class FixtureSite:
    name: str
    directory: Path
    about: str
    routes: dict[str, Route]
    default_headers: dict[str, str]
    site_expected_checks: list[str]
    external_routes: dict[str, Route]
    #: What the http:// twin does: "redirect" (301 to https://, the healthy
    #: default) or "mirror" (serves every page over plain HTTP too).
    plain_http: str = "redirect"
    #: Crawl-level expectations: ``status``, ``stop_reason``, ``pause_sources``.
    expected_crawl: dict[str, Any] = field(default_factory=dict)
    #: Sitemap-only paths that must be fetched after link discovery is exhausted.
    fetched_after_links: list[str] = field(default_factory=list)
    nav: list[tuple[str, str]] = field(default_factory=list)
    leaf_days: int = 90

    @property
    def nav_html(self) -> str:
        items = "".join(f'<li><a href="{path}">{label}</a></li>' for path, label in self.nav)
        return f"<nav><ul>{items}</ul></nav>" if items else ""

    @classmethod
    def load(cls, name: str) -> FixtureSite:
        directory = FIXTURE_ROOT / name
        manifest = json.loads((directory / "site.json").read_text())

        def routes(raw: dict[str, Any]) -> dict[str, Route]:
            return {path: Route(path=path, **spec) for path, spec in raw.items()}

        return cls(
            name=name,
            directory=directory,
            about=manifest["about"],
            routes=routes(manifest["routes"]),
            default_headers=dict(manifest.get("default_headers") or {}),
            site_expected_checks=list(manifest.get("site_expected_checks") or []),
            external_routes=routes(manifest.get("external_routes") or {}),
            plain_http=str(manifest.get("plain_http", "redirect")),
            expected_crawl=dict(manifest.get("expected_crawl") or {}),
            fetched_after_links=list(manifest.get("fetched_after_links") or []),
            nav=[(str(path), str(label)) for path, label in manifest.get("nav") or []],
            leaf_days=int(manifest.get("tls_leaf_days", 90)),
        )


def fixture_site_names() -> list[str]:
    return sorted(p.name for p in FIXTURE_ROOT.iterdir() if (p / "site.json").is_file())


_PROSE_TOKEN = re.compile(r"\{\{prose:([a-z0-9-]+):(\d+)\}\}")
_PROSE_WORDS = (
    "archive audit balance bearing border bracket bridge cabinet canvas carbon cargo "
    "cellar channel charter circuit climate column comfort compass copper corridor "
    "cotton courier crystal culture current cushion daylight delta desert detail "
    "diamond digest domain drawer engine estate fabric factor feather ferry fiber "
    "fields filter finish forest formula fortune fossil fountain frame freight "
    "garden garment gateway glacier granite gravel harbor harvest haven helmet "
    "horizon island jacket journal kettle kitchen ladder lantern leather lesson "
    "letter lumber magnet marble market meadow medal mirror module monitor mortar "
    "motion museum needle network notebook orchard outline oyster paddle palace "
    "panel parcel pattern pebble pencil pepper pillar pioneer planet plaster pocket "
    "portal powder prairie quarry quartz rabbit railway ribbon ridge river rocket "
    "saddle salmon sample satellite schedule season shelter signal silver sketch "
    "socket spiral station summit surface tablet temple thread timber tractor "
    "treasure tunnel valley velvet venture vessel village vintage voyage wagon "
    "window winter workshop yard zenith"
).split()
_PROSE_GLUE = "the a its our their every each this that with from under over near beyond".split()
_PROSE_VERBS = (
    "anchors balances carries crosses defines echoes frames gathers guides holds "
    "joins lifts marks measures moves opens places reaches shapes shows supports "
    "tracks turns welcomes"
).split()


_PAD_TOKEN = re.compile(r"\{\{pad:(\d+)\}\}")


def _pad(size: int) -> str:
    unit = "0123456789abcdef "
    return (unit * (size // len(unit) + 1))[:size]


def _prose(seed: str, words: int) -> str:
    """Deterministic, seed-unique sentences grouped into paragraphs."""

    rng = random.Random(f"audit-fixture-prose:{seed}")
    out: list[str] = []
    sentence: list[str] = []
    paragraphs: list[str] = []
    count = 0
    while count < words:
        length = rng.randint(9, 15)
        sentence = []
        for i in range(length):
            pool = _PROSE_VERBS if i == 2 else _PROSE_GLUE if i % 3 == 0 else _PROSE_WORDS
            sentence.append(rng.choice(pool))
        count += length
        out.append(" ".join(sentence).capitalize() + ".")
        if len(out) == 5:
            paragraphs.append("<p>" + " ".join(out) + "</p>")
            out = []
    if out:
        paragraphs.append("<p>" + " ".join(out) + "</p>")
    return "\n".join(paragraphs)


class FixtureServer:
    """One https origin (plus its http:// twin) serving a route table.

    ``origin`` / ``plain_origin`` are known after ``start``.
    """

    def __init__(
        self,
        routes: dict[str, Route],
        directory: Path,
        tls: FixtureTls,
        *,
        host: str,
        default_headers: dict[str, str] | None = None,
        plain_http: str = "redirect",
    ) -> None:
        self.routes = routes
        self.directory = directory
        self.tls = tls
        self.host = host
        self.default_headers = default_headers or {}
        self.origin = ""
        self.external_origin = ""
        self.plain_origin = ""
        self.requests: list[str] = []
        self.nav_html = ""
        self.plain_http = plain_http
        self.hits: dict[str, int] = {}

    async def start(self) -> None:
        """Listen on ONE port that speaks both TLS and plain HTTP.

        A real host answers ``https://host/x`` and ``http://host/x`` on the same
        name; the http:// twin is what `https_enforcement` and
        `host_protocol_consistency` probe. The front listener peeks the first
        byte (0x16 opens a TLS handshake) and hands the connection to the TLS
        app or the plain one, so ``{{origin}}`` and ``{{plain}}`` differ only in
        scheme — exactly the pair a crawler sees on a real host.
        """

        from aiohttp import web

        runners = []
        ports = {}
        for kind, handler in (("tls", self._handle), ("plain", self._handle_plain)):
            app = web.Application()
            app.router.add_route("*", "/{tail:.*}", handler)
            runner = web.AppRunner(app, access_log=None)
            await runner.setup()
            context = None
            if kind == "tls":
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(str(self.tls.cert_chain), str(self.tls.key))
            site = web.TCPSite(runner, "127.0.0.1", 0, ssl_context=context)
            await site.start()
            ports[kind] = site._server.sockets[0].getsockname()[1]  # noqa: SLF001
            runners.append(runner)
        self._runners = runners

        async def front(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            try:
                first = await reader.read(1)
                if not first:
                    writer.close()
                    return
                port = ports["tls"] if first == b"\x16" else ports["plain"]
                up_reader, up_writer = await asyncio.open_connection("127.0.0.1", port)
                up_writer.write(first)

                async def pipe(src: asyncio.StreamReader, dst: asyncio.StreamWriter) -> None:
                    try:
                        while chunk := await src.read(65536):
                            dst.write(chunk)
                            await dst.drain()
                    except (ConnectionError, asyncio.CancelledError):
                        pass
                    finally:
                        if not dst.is_closing():
                            dst.close()

                await asyncio.gather(pipe(reader, up_writer), pipe(up_reader, writer))
            except ConnectionError:
                writer.close()

        self._front = await asyncio.start_server(front, "127.0.0.1", 0)
        port = self._front.sockets[0].getsockname()[1]
        self.origin = f"https://{self.host}:{port}"
        self.plain_origin = f"http://{self.host}:{port}"

    async def stop(self) -> None:
        front = getattr(self, "_front", None)
        if front is not None:
            front.close()
        for runner in getattr(self, "_runners", []):
            await runner.cleanup()

    async def _handle_plain(self, request: Any) -> Any:
        """The http:// twin: a permanent redirect to https://, or a live mirror."""

        from aiohttp import web

        if self.plain_http == "mirror":
            return await self._handle(request)
        self.requests.append(f"plain:{request.path_qs}")
        target = self.origin + request.path_qs
        return web.Response(status=301, headers={"Location": target})

    def render(self, text: str) -> str:
        """Fill the fixture template tokens — the server's own "CMS".

        ``{{origin}}`` / ``{{external}}`` / ``{{plain}}`` — this site's, the
        off-site host's, and this site's plain-HTTP twin's absolute origins
        (ports are only known at start). ``{{nav}}`` — the
        site navigation from ``site.json``. ``{{prose:SEED:WORDS}}`` —
        deterministic body copy, different for every seed, so pages have real
        word counts without being near-duplicates of each other.
        ``{{pad:BYTES}}`` — exactly BYTES of inert filler (inside a comment or a
        style block), for weight and text-to-HTML fixtures.
        """

        text = _PROSE_TOKEN.sub(lambda m: _prose(m.group(1), int(m.group(2))), text)
        text = _PAD_TOKEN.sub(lambda m: _pad(int(m.group(1))), text)
        text = text.replace("{{nav}}", self.nav_html)
        return (
            text.replace("{{origin}}", self.origin)
            .replace("{{external}}", self.external_origin)
            .replace("{{plain}}", self.plain_origin)
        )

    async def _handle(self, request: Any) -> Any:
        from aiohttp import web

        path = request.path_qs if request.query_string else request.path
        self.requests.append(path)
        route = self.routes.get(path)
        if route is None:
            # A route ending in "*" answers every path under its prefix.
            route = next(
                (
                    r
                    for key, r in self.routes.items()
                    if key.endswith("*") and path.startswith(key[:-1])
                ),
                None,
            )
        if route is None:
            return web.Response(status=404, text="Not found", content_type="text/plain")
        if route.delay_ms:
            await asyncio.sleep(route.delay_ms / 1000)
        if route.responses:
            hits = self.hits.get(route.path, 0)
            self.hits[route.path] = hits + 1
            answer = route.responses[min(hits, len(route.responses) - 1)]
            if "file" not in answer and "body" not in answer and answer.get("status", 200) >= 300:
                return web.Response(
                    status=int(answer["status"]),
                    headers={k: self.render(v) for k, v in (answer.get("headers") or {}).items()},
                    text=str(answer.get("text", "")),
                    content_type="text/plain",
                )
        headers = {**self.default_headers, **{k: self.render(v) for k, v in route.headers.items()}}
        if route.file is not None:
            raw = (self.directory / route.file).read_bytes()
            if route.content_type.startswith(("text/", "application/xml")):
                raw = self.render(raw.decode("utf-8")).encode("utf-8")
        else:
            raw = self.render(route.body or "").encode("utf-8")
        headers["Content-Type"] = route.content_type
        if request.method == "HEAD":
            return web.Response(status=route.status, headers=headers)
        return web.Response(status=route.status, body=raw, headers=headers)


# ---------------------------------------------------------------------------
# The in-memory stand-in for the web.* rows the analysis reads.


def _stable_id(kind: str, key: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"audit-fixture:{kind}:{key}"))


@dataclass
class _Page:
    id: str
    url: str
    url_hash: str
    canonical_page_id: str
    status: str = "active"
    http_status_last: int | None = None
    content_type_last: str | None = None
    latest_snapshot_id: str | None = None
    link_score: float | None = None
    target_keyword: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    deleted_at: Any = None


@dataclass
class FixtureWebStore:
    root_url: str
    session_id: str = "audit-fixture-session"
    pages: dict[str, _Page] = field(default_factory=dict)  # url_hash -> page
    snapshots: dict[str, SimpleNamespace] = field(default_factory=dict)
    edges: list[dict[str, Any]] = field(default_factory=list)
    crawl_urls: list[dict[str, Any]] = field(default_factory=list)
    fetched: dict[str, Any] = field(default_factory=dict)  # normalized url -> fetched event
    sitemap_members: dict[str, set[str]] = field(default_factory=dict)  # page id -> sitemap urls
    sitemap_lastmod_pages: set[str] = field(default_factory=set)
    sitemap_docs: list[Any] = field(default_factory=list)
    sitemap_sync_ran: bool = False
    events: list[Any] = field(default_factory=list)

    # --- page registry --------------------------------------------------------

    def page_for(self, url: str) -> _Page:
        from matrx_scraper.utils.url import normalize_url, url_hash

        normalized = normalize_url(url)
        digest = url_hash(normalized)
        page = self.pages.get(digest)
        if page is None:
            page_id = _stable_id("page", digest)
            page = _Page(id=page_id, url=normalized, url_hash=digest, canonical_page_id=page_id)
            self.pages[digest] = page
        return page

    def by_id(self, page_id: str) -> _Page | None:
        return next((p for p in self.pages.values() if p.id == page_id), None)

    # --- crawl writes -----------------------------------------------------------

    def record_fetched(self, event: Any) -> None:
        from matrx_scraper.web_crawl.persistence import _normalise_url

        self.fetched[_normalise_url(event.url)] = event

    def record_success(self, request: Any) -> None:
        """``resolve_crawl_page_identity`` + ``_persist_rows``, in memory."""

        from matrx_scraper.utils.url import normalize_url
        from matrx_scraper.web_crawl.persistence import _normalise_url, snapshot_evidence_columns
        from matrx_scraper.web_crawl.url_identity import crawl_identity_target

        summary = request.page_summary
        requested = normalize_url(request.url)
        # THE identity rule, called as-is: the fetched URL is the page; the request
        # and its redirect hops collapse into it; a declared canonical never does.
        final, observed = crawl_identity_target(
            requested, request.final_url or request.url, summary.redirect_chain
        )
        target = self.page_for(final)
        for url in observed:
            page = self.page_for(url)
            page.canonical_page_id = target.id
            page.status = "active"
        snapshot_id = _stable_id("snapshot", f"{target.id}:{len(self.snapshots)}")
        snapshot = SimpleNamespace(
            id=snapshot_id,
            session_id=self.session_id,
            page_id=target.id,
            http_status=summary.http_status,
            word_count=summary.word_count,
            final_url=final,
            **snapshot_evidence_columns(
                summary,
                requested_url=requested,
                final_url=final,
                extractor_results=request.extractor_results,
            ),
        )
        self.snapshots[snapshot_id] = snapshot
        target.latest_snapshot_id = snapshot_id
        target.http_status_last = summary.http_status
        target.content_type_last = summary.mime_type
        for position, link in enumerate(summary.links):
            self.edges.append(
                {
                    "id": _stable_id("edge", f"{snapshot_id}:{position}"),
                    "snapshot_id": snapshot_id,
                    "source_page_id": target.id,
                    "target_url": _normalise_url(link.target_url),
                    "is_internal": link.link_type != "external",
                    "rel": link.rel or ("nofollow" if link.nofollow else None),
                    "anchor_text": link.anchor_text,
                    "http_status": None,
                }
            )
        self.crawl_urls.append(
            {
                "normalized_url": requested,
                "http_status": summary.http_status,
                "final_url": final,
                "metadata": {"redirect_chain": list(summary.redirect_chain or [])},
                "outcome": "redirected" if requested != final else "captured",
                "reason_code": None,
            }
        )

    def record_failure(self, event: Any) -> None:
        """``_persist_failed_url_in_active_transaction`` (first crawl), in memory."""

        from matrx_scraper.web_crawl.persistence import (
            _normalise_url,
            crawl_url_fetch_metadata,
            failed_fetch_disposition,
        )

        normalized = _normalise_url(event.url)
        fetched = self.fetched.get(normalized)
        http_status = fetched.http_status if fetched else None
        existed = any(p.url == normalized for p in self.pages.values())
        page = self.page_for(normalized)
        if not existed:
            page.status = "missing"
            page.http_status_last = http_status
            page.content_type_last = fetched.mime_type if fetched else None
        disposition = failed_fetch_disposition(http_status, 0)
        if existed and disposition.authoritative:
            page.status = disposition.status or page.status
            page.http_status_last = http_status
        elif existed and http_status is not None:
            page.http_status_last = http_status
        if disposition.soft_delete:
            page.status = "gone"
            page.deleted_at = "now"
        self.crawl_urls.append(
            {
                "normalized_url": normalized,
                "page_id": page.id,
                "http_status": http_status,
                "outcome": "failed",
                "reason_code": ("http_410" if http_status == 410 else event.error_class)[:200],
                "metadata": crawl_url_fetch_metadata(
                    getattr(fetched, "redirect_chain", None) if fetched else None
                ),
                "sequence": len(self.crawl_urls),
                "completed_at": dt.datetime.now(dt.UTC),
            }
        )

    # --- link status (link_check) -------------------------------------------

    def resolve_internal_statuses(self) -> None:
        """``link_check._check_internal_edges``, same-session, in memory."""

        from matrx_scraper.utils.url import url_hash
        from matrx_scraper.web_crawl.link_check import (
            _select_internal_status,
            material_redirect_status,
        )
        from matrx_scraper.web_crawl.persistence import _normalise_url

        session_by_snapshot = {sid: self.session_id for sid in self.snapshots}
        same_session_status_by_page: dict[tuple[str, str], int] = {}
        for snap in self.snapshots.values():
            if snap.http_status is not None:
                same_session_status_by_page.setdefault(
                    (self.session_id, snap.page_id), int(snap.http_status)
                )
        crawl_status_by_session_hash: dict[tuple[str, str], int] = {}
        redirect_status_by_session_hash: dict[tuple[str, str], int] = {}
        for row in reversed(self.crawl_urls):  # newest attempt first, as the query orders
            if row.get("http_status") is None:
                continue
            key = (self.session_id, url_hash(row["normalized_url"]))
            if key in crawl_status_by_session_hash:
                continue
            crawl_status_by_session_hash[key] = int(row["http_status"])
            redirect_status = material_redirect_status(
                row["normalized_url"],
                row.get("final_url"),
                (row.get("metadata") or {}).get("redirect_chain"),
            )
            if redirect_status is not None:
                redirect_status_by_session_hash[key] = redirect_status
        snapshot_by_page = {
            p.id: p.latest_snapshot_id for p in self.pages.values() if p.latest_snapshot_id
        }
        statuses_by_snapshot = {
            sid: int(s.http_status) for sid, s in self.snapshots.items() if s.http_status
        }
        for edge in self.edges:
            if not edge["is_internal"]:
                continue
            target = self.pages.get(url_hash(_normalise_url(edge["target_url"])))
            edge["target_page_id"] = target.canonical_page_id if target else None
            edge["http_status"] = _select_internal_status(
                source_snapshot_id=edge["snapshot_id"],
                target_url=edge["target_url"],
                target_page_id=edge["target_page_id"],
                session_by_snapshot=session_by_snapshot,
                same_session_status_by_page=same_session_status_by_page,
                crawl_status_by_session_hash=crawl_status_by_session_hash,
                snapshot_by_page=snapshot_by_page,
                statuses_by_snapshot=statuses_by_snapshot,
                redirect_status_by_session_hash=redirect_status_by_session_hash,
            )

    async def resolve_external_statuses(self, *, polite: bool = False) -> None:
        """``link_check._check_external_edges`` through the one real checker."""

        from matrx_scraper.web_crawl.link_check import check_urls

        targets = [e["target_url"] for e in self.edges if not e["is_internal"]]
        statuses = (
            await check_urls(targets)
            if polite
            else await check_urls(targets, per_host_spacing_s=0.0)
        )
        for edge in self.edges:
            if not edge["is_internal"]:
                edge["http_status"] = statuses.get(edge["target_url"])

    # --- sitemap (sitemap_sync) ---------------------------------------------

    def record_sitemaps(self, crawl: Any) -> None:
        """``sitemap_sync`` document + membership rows, in memory."""

        from matrx_scraper.web_crawl.sitemap_sync import normalize_sitemap_loc

        self.sitemap_docs = list(crawl.documents)
        self.sitemap_sync_ran = bool(crawl.documents)
        for doc in crawl.documents:
            if doc.kind != "urlset":
                continue
            for entry in doc.entries:
                normalized = normalize_sitemap_loc(entry.loc)
                if normalized is None:
                    continue
                page = self.page_for(normalized)
                self.sitemap_members.setdefault(page.id, set()).add(doc.url)
                if entry.lastmod is not None:
                    self.sitemap_lastmod_pages.add(page.id)


# ---------------------------------------------------------------------------
# Crawl, then analyze — the production order.


@dataclass
class AuditRun:
    site: FixtureSite | None
    origin: str
    raised_by_page: dict[str, set[str]]  # route path -> raised check keys
    outcomes_by_page: dict[str, dict[str, Any]]
    site_raised: set[str]
    site_outcomes: dict[str, Any]
    crawl_completed: Any
    requests: list[str]
    events: list[Any] = field(default_factory=list)


async def crawl_into_store(origin: str, *, polite: bool = False) -> tuple[FixtureWebStore, Any]:
    from matrx_scraper.crawler import (
        RENDER_HTTP_ONLY,
        PersistResult,
        SiteCrawler,
        SiteCrawlerConfig,
    )
    from matrx_scraper.events import (
        CrawlCompletedEvent,
        CrawlPageFailedEvent,
        CrawlPageFetchedEvent,
    )
    from matrx_scraper.queue_backend import InMemoryQueueBackend

    root_url = f"{origin}/"
    store = FixtureWebStore(root_url=root_url)
    completed: list[Any] = []

    class Sink:
        async def emit(self, event: Any) -> None:
            store.events.append(event)
            if isinstance(event, CrawlPageFetchedEvent):
                store.record_fetched(event)
            elif isinstance(event, CrawlPageFailedEvent) and not event.will_retry:
                store.record_failure(event)
            elif isinstance(event, CrawlCompletedEvent):
                completed.append(event)

    async def persist(request: Any) -> Any:
        store.record_success(request)
        page = store.page_for(request.url)
        return PersistResult(page_id=page.canonical_page_id, snapshot_id=page.latest_snapshot_id)

    crawler = SiteCrawler(
        run_id="audit-fixture",
        config=SiteCrawlerConfig(
            base_url=root_url,
            max_pages=500,
            concurrency=2 if polite else 4,
            respect_robots=True,
            seed_from_sitemap=True,
            render_mode=RENDER_HTTP_ONLY,
            # A fixture host is ours and pinned fast; a public host gets the
            # production defaults (adaptive, opening low, 4 req/s ceiling).
            **(
                {} if polite else {"host_rps": 200.0, "host_burst": 200.0, "adaptive_pacing": False}
            ),
        ),
        event_sink=Sink(),
        queue_backend=InMemoryQueueBackend(),
        body_persister=persist,
        strict_persistence=True,
        retain_results=False,
    )
    await asyncio.wait_for(crawler.run(), timeout=240)
    return store, (completed[0] if completed else None)


def build_page_facts(store: FixtureWebStore) -> tuple[list[Any], Any, Any]:
    """``analysis._load_page_facts`` + ``_load_link_stats`` over the in-memory rows."""

    from matrx_scraper.pagerank import compute_link_scores
    from matrx_scraper.utils.url import url_hash
    from matrx_scraper.web_crawl import analysis
    from matrx_scraper.web_crawl.link_score import build_site_graph, resolve_edge_rows
    from matrx_scraper.web_crawl.persistence import _normalise_url
    from matrx_utils.web_page_class import is_machine_resource

    live = [p for p in store.pages.values() if p.deleted_at is None]
    graph_rows = [
        {
            "id": p.id,
            "url_hash": p.url_hash,
            "canonical_page_id": p.canonical_page_id,
            "latest_snapshot_id": p.latest_snapshot_id,
        }
        for p in live
    ]
    # link_score.score_site_links — the score `internal_link_equity` ranks on.
    graph = build_site_graph(graph_rows)
    current = {p.latest_snapshot_id for p in live if p.latest_snapshot_id}
    internal = [e for e in store.edges if e["is_internal"] and e["snapshot_id"] in current]
    edges, _dropped = resolve_edge_rows(graph, internal)
    nodes = [(cid, cid, None) for cid in graph.group_members]
    scores = compute_link_scores(nodes, edges) if nodes else {}
    for canonical_id, members in graph.group_members.items():
        for member in members:
            page = store.by_id(member)
            if page is not None and canonical_id in scores:
                page.link_score = float(scores[canonical_id])

    registry = analysis._PageRegistry(graph_rows=graph_rows)
    facts_list: list[Any] = []
    without_snapshot: list[_Page] = []
    for page in sorted(live, key=lambda p: p.id):
        if page.canonical_page_id != page.id:
            continue
        if is_machine_resource(page.url, page.content_type_last):
            continue
        if page.status != "gone":
            registry.census_rows.append((page.id, page.url, page.latest_snapshot_id is not None))
        if page.latest_snapshot_id is None:
            without_snapshot.append(page)
            continue
        facts_list.append(
            analysis._extract_page_facts(page, store.snapshots[page.latest_snapshot_id])
        )
    for page in without_snapshot:
        attempts = [
            row
            for row in store.crawl_urls
            if row.get("page_id") == page.id and row["outcome"] == "failed"
        ]
        if attempts:
            facts_list.append(analysis._extract_transport_facts(page, attempts[-1]))

    aggregates = analysis.SiteAggregates()
    analysis.index_page_facts(facts_list, aggregates)
    snapshot_to_page = {f.latest_snapshot_id: f.page_id for f in facts_list if f.latest_snapshot_id}
    adjacency: dict[str, set[str]] = {}
    for edge in store.edges:
        page_id = snapshot_to_page.get(edge["snapshot_id"])
        if page_id is None:
            continue
        stats = aggregates.link_stats.setdefault(page_id, analysis.PageLinkStats())
        analysis._accumulate_edge(edge, stats, graph, aggregates, adjacency)
    # `_exclude_blocked_link_targets`: the target's LATEST fetch verdict decides —
    # a wall / rate-limit give-up is never a broken link, a redirect loop is one.
    # The rule itself is `analysis.apply_target_fetch_verdicts`, called as-is.
    latest_reason: dict[str, Any] = {}
    for row in store.crawl_urls:  # appended in completion order; the last one wins
        if row["outcome"] in analysis._FETCH_VERDICT_OUTCOMES:
            latest_reason[url_hash(row["normalized_url"])] = row.get("reason_code")
    analysis.apply_target_fetch_verdicts(aggregates.link_stats, latest_reason)
    aggregates.homepage_page_id = graph.canonical_by_hash.get(
        url_hash(_normalise_url(store.root_url))
    )
    if aggregates.homepage_page_id is not None:
        aggregates.depth_by_page = analysis._bfs_depths(aggregates.homepage_page_id, adjacency)
    aggregates.orphans = analysis._build_orphan_census(registry, aggregates)
    return facts_list, aggregates, graph


async def run_fixture_audit(
    site: FixtureSite | None, server: Any, *, polite: bool = False
) -> AuditRun:
    """Audit ``server.origin`` exactly as production orders it.

    ``server`` needs only ``origin``, ``plain_origin`` and ``requests``.
    ``polite=True`` is for a real public host (badseo.dev): production pacing
    and a small concurrency instead of the fixture's pinned fast rate.
    """
    from matrx_scraper.sitemaps import crawl_sitemap_documents
    from matrx_scraper.web_crawl import analysis, site_analysis
    from matrx_scraper.web_crawl.site_probe import SiteProbe, host_form, probe_site

    origin = server.origin
    root_url = f"{origin}/"
    # Production order: sitemap sync, crawl, link status, link score, probe, analysis.
    sitemap_crawl = await crawl_sitemap_documents(root_url)
    store, completed = await crawl_into_store(origin, polite=polite)
    store.record_sitemaps(sitemap_crawl)
    store.resolve_internal_statuses()
    await store.resolve_external_statuses(polite=polite)
    facts_list, aggregates, _graph = build_page_facts(store)

    probe_sample = [f.url for f in facts_list if f.http_status and 200 <= f.http_status < 300]
    probe = SiteProbe.from_dict((await probe_site(root_url, probe_sample)).to_dict())
    degraded = analysis.stamp_http_variant_evidence(facts_list, probe, root_url)
    del degraded  # evidence quality note, not a verdict

    outcomes_by_url: dict[str, dict[str, Any]] = {}
    for facts in facts_list:
        outcomes_by_url[facts.url] = {
            key: check(facts, aggregates) for key, check in analysis.PAGE_CHECKS.items()
        }

    site_facts = analysis._build_site_facts("audit-fixture-site", facts_list)
    site_facts.tls = analysis._tls_facts_from_probe(probe, computed_at=dt.datetime.now(dt.UTC))
    evidence = site_analysis.SiteEvidence(
        site_id="audit-fixture-site",
        root_url=root_url,
        canonical_host_form=host_form(root_url),
        probe=probe,
    )
    if probe is not None and probe.robots is not None:
        evidence.robots = probe.robots.parsed()
    facts_by_page = {f.page_id: f for f in facts_list if f.page_id}
    evidence.sitemap_sync_ran = store.sitemap_sync_ran
    evidence.sitemaps = [
        site_analysis.SitemapDocFacts(
            url=doc.url,
            kind=doc.kind,
            status_code=doc.status_code,
            fetch_error=doc.fetch_error,
            url_count=doc.url_count,
            is_active=True,
            last_fetched_at=dt.datetime.now(dt.UTC),
        )
        for doc in store.sitemap_docs
    ]
    member_ids = set(store.sitemap_members)
    site_analysis.fold_sitemap_members(
        evidence,
        member_page_ids=member_ids,
        pages_with_lastmod=store.sitemap_lastmod_pages & member_ids,
        member_pages=[p for p in (store.by_id(i) for i in sorted(member_ids)) if p],
        facts_by_page=facts_by_page,
    )
    site_analysis._load_coverage(evidence, facts_by_page)
    # `_load_internal_link_host_forms`: distinct scheme://host forms on internal edges.
    for edge in store.edges:
        if edge["is_internal"] and "://" in edge["target_url"]:
            evidence.internal_link_host_forms.add(host_form(edge["target_url"]))
    site_facts.crawlability = evidence
    site_outcomes = {key: check(site_facts) for key, check in analysis.SITE_CHECKS.items()}

    path_by_url = {}
    for url in outcomes_by_url:
        plain_origin = getattr(server, "plain_origin", "")
        if plain_origin and url.startswith(plain_origin):
            path_by_url["plain:" + _route_key(url, plain_origin)] = url
        else:
            path_by_url[_route_key(url, origin)] = url
    raised_by_page: dict[str, set[str]] = {}
    outcomes_by_page: dict[str, dict[str, Any]] = {}
    for path, url in path_by_url.items():
        outcomes = outcomes_by_url[url]
        outcomes_by_page[path] = outcomes
        raised_by_page[path] = {k for k, o in outcomes.items() if o.status in RAISED_STATUSES}
    return AuditRun(
        site=site,
        origin=origin,
        raised_by_page=raised_by_page,
        outcomes_by_page=outcomes_by_page,
        site_raised={k for k, o in site_outcomes.items() if o.status in RAISED_STATUSES},
        site_outcomes=site_outcomes,
        crawl_completed=completed,
        requests=list(getattr(server, "requests", [])),
        events=list(store.events),
    )


def _route_key(url: str, origin: str) -> str:
    """A page URL as its route path (the stored identity strips a trailing slash)."""

    rest = url[len(origin) :] if url.startswith(origin) else url
    return rest or "/"


def route_page_key(path: str) -> str:
    """The key a declared route's verdict is filed under after URL normalization."""

    from matrx_scraper.utils.url import normalize_url

    probe_origin = "https://fixture.invalid"
    return _route_key(normalize_url(probe_origin + path), probe_origin)


async def audit_fixture_site(name: str, monkeypatch: Any, tmp_path: Path) -> AuditRun:
    """Serve one fixture site (plus its external host), crawl it, analyze it."""

    site = FixtureSite.load(name)
    tls = mint_fixture_tls(tmp_path / "tls", leaf_days=site.leaf_days)
    trust_fixture_ca(monkeypatch, tls)
    block_outside_network(monkeypatch)
    server = FixtureServer(
        site.routes,
        site.directory,
        tls,
        host="127.0.0.1",
        default_headers=site.default_headers,
        plain_http=site.plain_http,
    )
    external = FixtureServer(site.external_routes, site.directory, tls, host="localhost")
    servers = (server, external)
    for each in servers:
        await each.start()
    for each in servers:
        each.external_origin = external.origin
        each.nav_html = site.nav_html
    allow_fixture_origins(
        monkeypatch, [o for each in servers for o in (each.origin, each.plain_origin)]
    )
    try:
        return await run_fixture_audit(site, server)
    finally:
        for each in servers:
            await each.stop()


__all__ = [
    "FIXTURE_ROOT",
    "AuditRun",
    "FixtureSite",
    "audit_fixture_site",
    "fixture_site_names",
    "route_page_key",
]
