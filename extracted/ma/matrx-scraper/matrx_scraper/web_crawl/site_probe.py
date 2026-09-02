"""Site-level evidence capture — robots.txt, sitemap locations, host variants.

The SITE-level catalogue checks (`robots_txt_health`, `sitemap_health`,
`sitemap_coverage`, `host_protocol_consistency`) score facts that belong to the
site as a whole, not to any page. Three of those facts were **captured nowhere**
before 2026-08-09:

- the crawler read robots.txt into an in-memory ``urllib.robotparser`` cache and
  threw it away (``crawler.py::_RobotsCache``) — the FILE was never persisted,
  so nothing could ever say why a site scored what it scored;
- whether a sitemap exists AT ALL was indistinguishable from "sitemap sync has
  never run" (both are zero ``web.sitemap`` rows);
- nothing ever fetched the www / non-www / http / https variants of the root,
  so "the site resolves on four different URLs" could not be observed.

This module captures all three, once, and persists them on the site row. The
checks then run over stored evidence like every other check —
``web_crawl/analysis.py`` stays network-free by contract.

**Storage.** ``web.site.metadata["site_probe"]``. Deliberately NOT
``crawl_session.stats``: that column is REPLACED wholesale by every
``CrawlProgressEvent`` and by the terminal ``CrawlCompletedEvent``
(``persistence.py::_stats_from_progress``), so anything written beside those
keys is silently erased mid-crawl. One row per site, latest capture wins,
timestamped — a stale probe is visible as a stale ``captured_at``, never as a
missing one.

**Failure is evidence.** A 5xx robots.txt and a connection reset are different
facts and are stored differently: ``http_status`` set means we got an answer,
``fetch_error`` set means we never did. A check may only score the first kind.

**Per-PAGE probes (2026-08-13).** The four root variants answer for the site;
they cannot answer for a path. Two catalogue rows needed exactly that and were
silently under-measuring:

- ``https_enforcement`` (weight 3.0) scored its redirect bands off the ORIGIN
  probe, so a server that redirects its root while happily answering
  ``http://host/deep/path`` scored ``pass`` on every page of the site.
- ``host_protocol_consistency`` (weight 1.5) names trailing-slash inconsistency
  in its own description and had no evidence for it — the slash/no-slash PAIR
  of a path is not a property of the root.

Both are fixed by SAMPLING real page URLs and probing them with the same
mechanism the root variants use: ``page_http_variants`` (the ``http://`` twin of
a sampled https page) and ``slash_pairs`` (``<path>`` vs ``<path>/``). Sampled,
HEAD-first, and hard-capped — this is a diagnostic probe, never a second crawl.
Both lists are ADDITIVE on the stored shape: a probe captured before they
existed simply carries none, and the checks fall back (origin evidence for
``https_enforcement``; no slash band for ``host_protocol_consistency``) instead
of being invalidated.
"""

from __future__ import annotations

import asyncio
import logging
import ssl
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urljoin, urlsplit

import httpx
from matrx_utils import utcnow

from matrx_scraper.db.models_web import Page as WebPage
from matrx_scraper.db.models_web import Site as WebSite
from matrx_scraper.robots_txt import ROBOTS_MAX_BYTES, RobotsDocument, parse_robots_txt
from matrx_scraper.utils.url import validate_public_http_url
from matrx_scraper.web_crawl.url_verify import HEAD_FALLBACK_STATUSES

logger = logging.getLogger(__name__)

# Where the probe lives on the site row, and the shape version. A probe written
# by an older format is IGNORED rather than misread — the checks fall back to
# their missing-evidence `n_a` path, which is the honest answer.
SITE_PROBE_METADATA_KEY = "site_probe"
SITE_PROBE_FORMAT_VERSION = 1

ROBOTS_PATH = "/robots.txt"
PROBE_TIMEOUT_SECONDS = 10.0
PROBE_USER_AGENT = "MatrxScraperBot/site-probe (+https://aimatrx.com)"

# The four forms a site can answer on. Every one is probed, every time — the
# whole point of `host_protocol_consistency` is to find the ones that answer
# when they should redirect.
HOST_VARIANT_SCHEMES: tuple[str, ...] = ("https", "http")
HOST_VARIANT_WWW: tuple[bool, ...] = (False, True)

# Conventional sitemap locations, probed only to tell "this site has no
# sitemap" apart from "we never looked". Robots' own `Sitemap:` directives are
# probed first; the total is capped so a robots.txt listing 500 sitemaps cannot
# turn one probe into 500 requests.
CONVENTIONAL_SITEMAP_PATHS: tuple[str, ...] = ("/sitemap.xml", "/sitemap_index.xml")
SITEMAP_LOCATION_PROBE_LIMIT = 5

# --- per-page sampling caps. CAPS constants, never env vars.
#: How many distinct page paths get an `http://` twin probe. 20 paths is enough
#: to prove "this server answers deep paths over HTTP" (the failure the origin
#: probe cannot see) while keeping the whole probe a few dozen requests.
PAGE_HTTP_VARIANT_PROBE_LIMIT = 20
#: How many distinct page paths get the slash/no-slash pair. Each one costs TWO
#: requests, so it is deliberately half the http-variant sample.
SLASH_PAIR_PROBE_LIMIT = 10
#: Page rows pulled from the registry before sampling. The sample is chosen in
#: Python (canonical, https, non-root, one per path), so the query is bounded
#: rather than the sample being whatever the first N rows happened to be.
PAGE_SAMPLE_QUERY_LIMIT = 300
#: Concurrent page probes. The root probe fires ~9 requests at once; a sampled
#: page pass can fire 40, and it is the SAME host every time.
PAGE_PROBE_CONCURRENCY = 4


@dataclass
class UrlProbe:
    """One URL fetched once, with the redirect chain it went through."""

    url: str
    # Status of the FIRST response — a 301 here is the fact being measured, so
    # it must never be replaced by the status of where it landed.
    http_status: int | None = None
    final_url: str | None = None
    final_status: int | None = None
    redirect_chain: list[dict[str, Any]] = field(default_factory=list)
    fetch_error: str | None = None

    @property
    def answered(self) -> bool:
        return self.http_status is not None

    @property
    def redirects(self) -> bool:
        return self.http_status is not None and 300 <= self.http_status < 400


@dataclass
class SlashPairProbe:
    """One path fetched in BOTH forms — ``<path>`` and ``<path>/``.

    The duplicate this measures is the pair answering 200 independently. A pair
    where one form redirects to the other is CORRECT consolidation, which is why
    the verdict compares where each form LANDED, not what it returned.
    """

    path: str
    bare: UrlProbe
    slashed: UrlProbe

    @property
    def both_answered(self) -> bool:
        return self.bare.answered and self.slashed.answered

    @property
    def duplicated(self) -> bool:
        """Both forms serve their own 200 — two addresses, one page."""

        if not self.both_answered:
            return False
        if self.bare.final_status != 200 or self.slashed.final_status != 200:
            return False
        # Landing on the SAME url is consolidation working, whatever the hops.
        # The comparison is exact: `/a` and `/a/` are different addresses, and
        # normalising the slash away here would erase the very fact measured.
        bare_final = self.bare.final_url or self.bare.url
        slashed_final = self.slashed.final_url or self.slashed.url
        return bare_final != slashed_final


@dataclass
class RobotsCapture:
    """The robots.txt file itself, exactly as the site served it."""

    url: str
    http_status: int | None = None
    fetch_error: str | None = None
    content: str | None = None
    truncated: bool = False

    @property
    def answered(self) -> bool:
        return self.http_status is not None

    def parsed(self) -> RobotsDocument | None:
        """The parsed document, or None when there is nothing to parse."""
        if self.content is None or self.http_status is None:
            return None
        if not (200 <= self.http_status < 300):
            return None
        return parse_robots_txt(self.content)


@dataclass
class TlsCapture:
    """One real certificate handshake against the site's canonical hostname."""

    hostname: str
    port: int = 443
    trusted: bool | None = None
    hostname_match: bool | None = None
    expired: bool | None = None
    issuer: str | None = None
    not_after: str | None = None
    fetch_error: str | None = None


@dataclass
class SiteProbe:
    """Everything the site-level checks read. Serialized whole onto the site."""

    captured_at: str
    root_url: str
    format_version: int = SITE_PROBE_FORMAT_VERSION
    robots: RobotsCapture | None = None
    tls: TlsCapture | None = None
    variants: list[UrlProbe] = field(default_factory=list)
    sitemap_locations: list[UrlProbe] = field(default_factory=list)
    #: The `http://` twin of each sampled https page URL. Empty means the sample
    #: was never taken (an older probe, or a site with no crawled pages yet) —
    #: `https_enforcement` then falls back to the origin probe.
    page_http_variants: list[UrlProbe] = field(default_factory=list)
    #: `<path>` vs `<path>/` for each sampled page path.
    slash_pairs: list[SlashPairProbe] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: object) -> SiteProbe | None:
        if not isinstance(raw, dict):
            return None
        if raw.get("format_version") != SITE_PROBE_FORMAT_VERSION:
            return None
        captured_at = raw.get("captured_at")
        root_url = raw.get("root_url")
        if not isinstance(captured_at, str) or not isinstance(root_url, str):
            return None
        robots_raw = raw.get("robots")
        robots = RobotsCapture(**robots_raw) if isinstance(robots_raw, dict) else None
        tls_raw = raw.get("tls")
        tls = TlsCapture(**tls_raw) if isinstance(tls_raw, dict) else None
        return cls(
            captured_at=captured_at,
            root_url=root_url,
            robots=robots,
            tls=tls,
            variants=_probes_from(raw.get("variants")),
            sitemap_locations=_probes_from(raw.get("sitemap_locations")),
            page_http_variants=_probes_from(raw.get("page_http_variants")),
            slash_pairs=_slash_pairs_from(raw.get("slash_pairs")),
        )

    @property
    def reachable_sitemap_locations(self) -> list[UrlProbe]:
        return [p for p in self.sitemap_locations if p.final_status == 200]


def _probes_from(raw: object) -> list[UrlProbe]:
    if not isinstance(raw, list):
        return []
    out: list[UrlProbe] = []
    for item in raw:
        if isinstance(item, dict):
            try:
                out.append(UrlProbe(**item))
            except TypeError:
                # A shape we do not recognize is dropped, never guessed at.
                continue
    return out


def _slash_pairs_from(raw: object) -> list[SlashPairProbe]:
    if not isinstance(raw, list):
        return []
    out: list[SlashPairProbe] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        bare, slashed = item.get("bare"), item.get("slashed")
        path = item.get("path")
        if not isinstance(path, str) or not isinstance(bare, dict) or not isinstance(slashed, dict):
            continue
        try:
            out.append(
                SlashPairProbe(path=path, bare=UrlProbe(**bare), slashed=UrlProbe(**slashed))
            )
        except TypeError:
            # A shape we do not recognize is dropped, never guessed at.
            continue
    return out


def host_form(url: str) -> str:
    """``scheme://host`` — the identity `host_protocol_consistency` compares."""

    parts = urlsplit(url)
    host = parts.netloc.lower().rstrip(".")
    # A default port is the same origin as no port at all.
    if (parts.scheme == "https" and host.endswith(":443")) or (
        parts.scheme == "http" and host.endswith(":80")
    ):
        host = host.rsplit(":", 1)[0]
    return f"{parts.scheme}://{host}"


def variant_urls(root_url: str) -> list[str]:
    """The four www/non-www × http/https forms of a site's root."""

    parts = urlsplit(root_url)
    bare = parts.netloc.lower().rstrip(".")
    bare = bare[4:] if bare.startswith("www.") else bare
    urls: list[str] = []
    for scheme in HOST_VARIANT_SCHEMES:
        for www in HOST_VARIANT_WWW:
            host = f"www.{bare}" if www else bare
            url = f"{scheme}://{host}/"
            if url not in urls:
                urls.append(url)
    return urls


def path_key(url: str) -> tuple[str, str]:
    """``(path, query)`` — the identity a per-page probe is matched on.

    Scheme and host are deliberately excluded: the whole point of the
    ``http://`` twin is that it differs from the page's URL in exactly the
    scheme. A missing path reads as ``/``.
    """

    parts = urlsplit(url)
    return (parts.path or "/", parts.query)


def http_variant_url(url: str) -> str | None:
    """The ``http://`` twin of an https URL, or None when there isn't one."""

    parts = urlsplit(url)
    if parts.scheme.lower() != "https" or not parts.netloc:
        return None
    return parts._replace(scheme="http").geturl()


def slash_pair_urls(url: str) -> tuple[str, str] | None:
    """``(<path>, <path>/)`` for one URL, or None when the pair is meaningless.

    The root, a URL carrying a query string, and anything that looks like a file
    (``/report.pdf``) are excluded: a trailing slash on those is not the
    duplicate-URL family the check is about.
    """

    parts = urlsplit(url)
    path = parts.path or "/"
    if path == "/" or parts.query or "." in path.rsplit("/", 1)[-1]:
        return None
    bare = path.rstrip("/")
    if not bare:
        return None
    return (parts._replace(path=bare).geturl(), parts._replace(path=bare + "/").geturl())


async def _probe_url(client: httpx.AsyncClient, url: str, *, method: str = "GET") -> UrlProbe:
    """Fetch one URL, recording the chain. Never raises.

    ``method="HEAD"`` is the sampled-page mode: dozens of probes against one
    host, where a body is never read anyway. A host that dislikes HEAD says so
    with a status in ``HEAD_FALLBACK_STATUSES``, and that is a complaint about
    the method, not an answer about the URL — those retry as GET so a per-page
    verdict is never scored off a 405.
    """

    probe = UrlProbe(url=url)
    try:
        # SSRF gate, part 1 — the target host is caller-influenced (a site's
        # own root_url), so it is address-checked exactly like `preview.py`.
        await validate_public_http_url(url)
    except Exception as exc:
        probe.fetch_error = f"blocked: {type(exc).__name__}"
        logger.warning("site probe BLOCKED %s: %s", url, exc)
        return probe
    try:
        response = await client.request(method, url)
        if method != "GET" and response.status_code in HEAD_FALLBACK_STATUSES:
            response = await client.get(url)
    except Exception as exc:
        probe.fetch_error = f"{type(exc).__name__}: {exc}"
        return probe
    try:
        # SSRF gate, part 2 — redirects can land on an internal host.
        await validate_public_http_url(str(response.url))
    except Exception as exc:
        probe.fetch_error = f"blocked after redirect: {type(exc).__name__}"
        logger.warning("site probe discarded a non-public final url for %s: %s", url, exc)
        return probe
    history = list(response.history)
    probe.http_status = history[0].status_code if history else response.status_code
    probe.redirect_chain = [{"url": str(r.url), "status": r.status_code} for r in history]
    probe.final_url = str(response.url)
    probe.final_status = response.status_code
    return probe


async def _probe_robots(client: httpx.AsyncClient, root_url: str) -> RobotsCapture:
    url = urljoin(root_url, ROBOTS_PATH)
    capture = RobotsCapture(url=url)
    try:
        await validate_public_http_url(url)
    except Exception as exc:
        capture.fetch_error = f"blocked: {type(exc).__name__}"
        logger.warning("robots probe BLOCKED %s: %s", url, exc)
        return capture
    try:
        response = await client.get(url)
    except Exception as exc:
        capture.fetch_error = f"{type(exc).__name__}: {exc}"
        return capture
    try:
        await validate_public_http_url(str(response.url))
    except Exception as exc:
        capture.fetch_error = f"blocked after redirect: {type(exc).__name__}"
        logger.warning("robots probe discarded a non-public final url for %s: %s", url, exc)
        return capture
    capture.http_status = response.status_code
    if 200 <= response.status_code < 300:
        body = response.text
        encoded = body.encode("utf-8", errors="replace")
        if len(encoded) > ROBOTS_MAX_BYTES:
            body = encoded[:ROBOTS_MAX_BYTES].decode("utf-8", errors="ignore")
            capture.truncated = True
        capture.content = body
    return capture


def _issuer_name(cert: dict[str, Any]) -> str | None:
    parts = [f"{key}={value}" for group in cert.get("issuer", ()) for key, value in group]
    return ", ".join(parts) or None


async def _capture_tls(root_url: str) -> TlsCapture | None:
    parts = urlsplit(root_url)
    if parts.scheme.lower() != "https" or not parts.hostname:
        return None
    hostname = parts.hostname.rstrip(".")
    port = parts.port or 443
    capture = TlsCapture(hostname=hostname, port=port)
    try:
        await validate_public_http_url(root_url)
    except Exception as exc:
        capture.fetch_error = f"blocked: {type(exc).__name__}"
        logger.warning("TLS probe BLOCKED %s: %s", root_url, exc)
        return capture
    context = ssl.create_default_context()
    try:
        _reader, writer = await asyncio.wait_for(
            asyncio.open_connection(
                hostname,
                port,
                ssl=context,
                server_hostname=hostname,
            ),
            timeout=PROBE_TIMEOUT_SECONDS,
        )
        ssl_object = writer.get_extra_info("ssl_object")
        cert = ssl_object.getpeercert() if ssl_object is not None else {}
        capture.trusted = True
        capture.hostname_match = True
        capture.expired = False
        capture.issuer = _issuer_name(cert)
        raw_not_after = cert.get("notAfter")
        if isinstance(raw_not_after, str):
            capture.not_after = datetime.fromtimestamp(
                ssl.cert_time_to_seconds(raw_not_after), tz=UTC
            ).isoformat()
        writer.close()
        await writer.wait_closed()
    except ssl.SSLCertVerificationError as exc:
        # OpenSSL verify codes are stable: 10 = expired, 62 = hostname mismatch.
        capture.expired = exc.verify_code == 10
        capture.hostname_match = exc.verify_code != 62
        capture.trusted = exc.verify_code in {10, 62}
        capture.fetch_error = f"SSLCertVerificationError[{exc.verify_code}]: {exc.verify_message}"
    except Exception as exc:
        capture.fetch_error = f"{type(exc).__name__}: {exc}"
    return capture


def _sitemap_candidates(root_url: str, robots: RobotsCapture) -> list[str]:
    candidates: list[str] = []
    document = robots.parsed()
    if document is not None:
        candidates.extend(document.sitemaps)
    candidates.extend(urljoin(root_url, path) for path in CONVENTIONAL_SITEMAP_PATHS)
    unique: list[str] = []
    for url in candidates:
        if url not in unique:
            unique.append(url)
    return unique[:SITEMAP_LOCATION_PROBE_LIMIT]


def sample_page_urls(urls: Iterable[str]) -> list[str]:
    """The https, non-root, one-per-path sample the per-page probes run over.

    Sampling is deterministic in the order given (the caller ranks; this only
    filters and dedupes), so two runs over an unchanged registry probe the same
    paths and their verdicts are comparable.
    """

    seen: set[tuple[str, str]] = set()
    out: list[str] = []
    for url in urls:
        parts = urlsplit(url)
        if parts.scheme.lower() != "https" or not parts.netloc:
            continue
        key = path_key(url)
        if key[0] == "/" or key in seen:
            continue
        seen.add(key)
        out.append(url)
        if len(out) >= PAGE_HTTP_VARIANT_PROBE_LIMIT:
            break
    return out


async def _probe_page_variants(
    client: httpx.AsyncClient, page_urls: list[str]
) -> tuple[list[UrlProbe], list[SlashPairProbe]]:
    """The ``http://`` twin of each sampled page, and its slash pair.

    Bounded by a semaphore: this is the same host, every request. A failure in
    any single probe is stored as evidence, exactly like a root variant.
    """

    semaphore = asyncio.Semaphore(PAGE_PROBE_CONCURRENCY)

    async def probe(url: str) -> UrlProbe:
        async with semaphore:
            return await _probe_url(client, url, method="HEAD")

    variant_targets = [u for u in (http_variant_url(p) for p in page_urls) if u is not None]
    pair_targets: list[tuple[str, str, str]] = []
    for page_url in page_urls:
        pair = slash_pair_urls(page_url)
        if pair is None:
            continue
        pair_targets.append((path_key(page_url)[0].rstrip("/") or "/", pair[0], pair[1]))
        if len(pair_targets) >= SLASH_PAIR_PROBE_LIMIT:
            break

    variants = await asyncio.gather(*(probe(url) for url in variant_targets))
    pair_probes = await asyncio.gather(
        *(probe(url) for _path, bare, slashed in pair_targets for url in (bare, slashed))
    )
    pairs = [
        SlashPairProbe(path=path, bare=pair_probes[2 * i], slashed=pair_probes[2 * i + 1])
        for i, (path, _bare, _slashed) in enumerate(pair_targets)
    ]
    return list(variants), pairs


async def probe_site(root_url: str, page_urls: Iterable[str] = ()) -> SiteProbe:
    """Fetch robots.txt, the four host variants, and the sitemap locations.

    ``page_urls`` (optional) is the site's known page URLs, ranked by the
    caller. A sample of them gets an ``http://`` twin probe and a slash-pair
    probe — the per-PATH evidence the root variants cannot supply. Passing none
    is a supported, smaller probe: the two consuming checks fall back rather
    than guess.

    Every individual fetch fails soft into the returned evidence — one dead
    variant must never cost us the rest of the picture.
    """

    headers = {"User-Agent": PROBE_USER_AGENT}
    sampled = sample_page_urls(page_urls)
    async with httpx.AsyncClient(
        timeout=PROBE_TIMEOUT_SECONDS, follow_redirects=True, headers=headers
    ) as client:
        robots, tls, *variants = await asyncio.gather(
            _probe_robots(client, root_url),
            _capture_tls(root_url),
            *(_probe_url(client, url) for url in variant_urls(root_url)),
        )
        locations = await asyncio.gather(
            *(_probe_url(client, url) for url in _sitemap_candidates(root_url, robots))
        )
        page_variants, slash_pairs = await _probe_page_variants(client, sampled)
    return SiteProbe(
        captured_at=utcnow().isoformat(),
        root_url=root_url,
        robots=robots,
        tls=tls,
        variants=list(variants),
        sitemap_locations=list(locations),
        page_http_variants=page_variants,
        slash_pairs=slash_pairs,
    )


async def load_page_probe_sample(site_id: str) -> list[str]:
    """The page URLs a site's per-page probes should run over.

    Bounded read of the registry, newest-seen first, filtered to canonical rows
    that last answered 2xx — probing an alias or a known 404 would spend the
    sample on a URL whose verdict says nothing about the site.
    """

    rows = (
        await WebPage.filter(
            site_id=site_id,
            deleted_at__isnull=True,
            http_status_last__gte=200,
            http_status_last__lt=300,
        )
        .order_by("-last_seen")
        .limit(PAGE_SAMPLE_QUERY_LIMIT)
        .all()
    )
    return [str(row.url) for row in rows if str(row.canonical_page_id) == str(row.id)]


def http_origin_probe(probe: SiteProbe | None, root_url: str) -> dict[str, Any] | None:
    """The site's own http:// origin result, in `https_enforcement` shape.

    The probe already fetches all four host variants for
    `host_protocol_consistency`; the http:// one is exactly the evidence the
    per-page HTTPS check was missing (its catalogue row's declared capture gap).
    It is an ORIGIN fact, not a per-URL one — a server that answers a deep path
    over HTTP while redirecting its root is possible — so the returned dict says
    so (`scope: "origin"`), and the check's wording never claims more.

    Returns None when the probe never ran or never reached the http:// origin,
    which keeps `check_https_enforcement` on its `n_a` path.
    """

    if probe is None:
        return None
    parts = urlsplit(root_url)
    bare = parts.netloc.lower().rstrip(".")
    bare = bare[4:] if bare.startswith("www.") else bare
    wanted = {f"http://{bare}", f"http://www.{bare}"}
    for candidate in probe.variants:
        if host_form(candidate.url) not in wanted or not candidate.answered:
            continue
        # Prefer the form the site itself canonicalizes to; the bare host is
        # probed first, so the first answering http:// variant is that one.
        return {
            "scope": "origin",
            "origin": host_form(candidate.url),
            "status": candidate.http_status,
            "location": candidate.final_url,
        }
    return None


def page_http_variant_probe(probe: SiteProbe | None, page_url: str) -> dict[str, Any] | None:
    """This PAGE's own http:// probe result, in `https_enforcement` shape.

    The evidence `check_https_enforcement` actually wants: a server that
    redirects its root while answering `http://host/deep/path` is invisible to
    the origin probe, and every page of such a site used to score `pass`.

    Returns None when this page was not in the probe's sample, which sends the
    caller to `http_origin_probe` — weaker evidence, honestly labelled by its
    own `scope`, and still better than nothing.
    """

    if probe is None or not probe.page_http_variants:
        return None
    wanted = path_key(page_url)
    for candidate in probe.page_http_variants:
        if path_key(candidate.url) != wanted or not candidate.answered:
            continue
        return {
            "scope": "page",
            "url": candidate.url,
            "status": candidate.http_status,
            "location": candidate.final_url,
        }
    return None


def load_site_probe(site: WebSite) -> SiteProbe | None:
    """The last probe stored on a site row, or None if there is none."""

    metadata = site.metadata if isinstance(site.metadata, dict) else {}
    return SiteProbe.from_dict(metadata.get(SITE_PROBE_METADATA_KEY))


async def capture_site_probe(site_id: str) -> SiteProbe:
    """Probe the site and persist the result onto ``web.site.metadata``.

    The ONE capture entry point — the post-crawl step and the standalone
    analyze command both call this, so a site's probe is refreshed by exactly
    the same code on both paths. The site's existing metadata is MERGED, never
    replaced: this column is shared with everything else that hangs facts off a
    site.
    """

    site = await WebSite.get_or_none(id=site_id, deleted_at__isnull=True)
    if site is None:
        raise LookupError(f"site {site_id} not found")
    probe = await probe_site(str(site.root_url), await load_page_probe_sample(site_id))
    metadata = dict(site.metadata) if isinstance(site.metadata, dict) else {}
    metadata[SITE_PROBE_METADATA_KEY] = probe.to_dict()
    updated = await WebSite.update_where({"id": site_id}, metadata=metadata)
    if updated.rows_affected != 1:
        raise RuntimeError(
            f"site probe for {site_id} touched {updated.rows_affected} rows — "
            "the capture was NOT stored; site-level checks would score stale evidence"
        )
    return probe


__all__ = [
    "CONVENTIONAL_SITEMAP_PATHS",
    "HOST_VARIANT_SCHEMES",
    "HOST_VARIANT_WWW",
    "PAGE_HTTP_VARIANT_PROBE_LIMIT",
    "PAGE_PROBE_CONCURRENCY",
    "PAGE_SAMPLE_QUERY_LIMIT",
    "PROBE_TIMEOUT_SECONDS",
    "PROBE_USER_AGENT",
    "ROBOTS_PATH",
    "SITEMAP_LOCATION_PROBE_LIMIT",
    "SITE_PROBE_FORMAT_VERSION",
    "SITE_PROBE_METADATA_KEY",
    "SLASH_PAIR_PROBE_LIMIT",
    "RobotsCapture",
    "SiteProbe",
    "SlashPairProbe",
    "TlsCapture",
    "UrlProbe",
    "capture_site_probe",
    "host_form",
    "http_origin_probe",
    "http_variant_url",
    "load_page_probe_sample",
    "load_site_probe",
    "page_http_variant_probe",
    "path_key",
    "probe_site",
    "sample_page_urls",
    "slash_pair_urls",
    "variant_urls",
]
