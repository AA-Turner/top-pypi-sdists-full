"""Measuring the region record's probes to choose a region: a deployment's ``auto`` (DSL-359).

No connect uses this. A session's probe is ``region_probe``'s, unchanged; this measures the
live regions' probes (``POST /v1/regions/probe-candidates`` with ``region_probes_v1``) and only
reports, for choosing where something should run. It is bounded so a caller never waits long:

- every region in parallel, each resolving its own name in its own task, under one deadline
  (1 s direct, 2 s through httpx);
- direct: one keep-alive TLS connection per region, where the TCP connect is the first sample
  (a cold-starting probe can't slow it) and each request after the handshake another; every
  resolved address is tried in turn, IPv4 and IPv6 interleaved;
- failed requests are retried, on a fresh connection, until the deadline;
- behind a proxy (``HTTPS_PROXY``, ``ALL_PROXY`` or the system's) or with custom certificates
  (``SSL_CERT_FILE``, ``SSL_CERT_DIR``) it measures through httpx, which honours them; each
  sample is one request, timed from its headers going out to the response headers coming back;
- it stops early once the leader is clear: every other region is beyond the tie window behind
  it, judged by its own samples (on httpx not by its first request, which may be a cold start)
  or, direct, by how long its own TCP connect has been pending;
- when a direct TLS handshake fails the region is measured by TCP connects; if two or more
  regions measured that way all answer within 2 ms of each other, a transparent intercepting
  proxy is answering for them, and the result is ``degraded`` with no winner.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import socket
import ssl
import statistics
import time
import urllib.request
from collections.abc import AsyncIterator, Callable, Collection, Mapping
from dataclasses import dataclass, replace
from typing import Any, Protocol
from urllib.parse import urlsplit

import httpx

from dreamscale.policy.config import OptimizationConfig
from dreamscale.region_probe import (
    REGION_CHOICE,
    REGION_PROBE_MIN_SUCCESSES,
    REGION_PROBE_SAMPLES_PER_REGION,
    RegionProbeResult,
    _accepted_kwargs,
    rank_region_samples,
)

# Asks the control plane for the region record's probes on Modal routes too.
REGION_PROBES_FEATURE = "region_probes_v1"
DIRECT_DEADLINE_S = 1.0
HTTPX_DEADLINE_S = 2.0
# The control plane's tie rule: two regions within 10 ms or 15% are a tie.
TIE_MS = 10.0
TIE_FRACTION = 0.15
# How long one address may take to connect before the next is tried.
CONNECT_ATTEMPT_S = 0.3
RETRY_PAUSE_S = 0.05
# TCP connects through a transparent intercepting proxy all answer from the proxy.
INTERCEPTED_SPREAD_MS = 2.0
_EARLY_STOP_TICK_S = 0.01


class Sampler(Protocol):
    """Where RTT samples come from: the network, or a test."""

    deadline_s: float
    # Whether a region's first sample is a TCP connect (no server work in it).
    trusts_first_sample: bool
    # Probe URLs measured by TCP connects because TLS failed.
    tcp_only: set[str]

    async def resolve(self, url: str) -> Any: ...

    def samples(
        self, url: str, resolved: Any, limit: int, *, on_connecting: Callable[[], None]
    ) -> AsyncIterator[float]: ...


async def measure_region_choice(
    control: Any,
    model: str,
    *,
    optimization_config: OptimizationConfig | dict[str, Any] | None = None,
    provider: str | None = None,
    speed: str | None = None,
    sampler: Sampler | None = None,
) -> RegionProbeResult | None:
    """Measure the region record's probes for choosing a region (a deployment's ``auto``):
    the live regions with a probe, from a control plane that knows ``region_probes_v1``.
    None when there is nothing to measure or anything fails; never raises."""
    probe_candidates = getattr(control, "probe_candidates", None)
    if probe_candidates is None:
        return None
    options: dict[str, Any] = {
        "optimization_config": optimization_config,
        "client_features": [REGION_PROBES_FEATURE],
    }
    if provider is not None:
        options["provider"] = provider
    if speed == "fast":
        options["speed"] = speed
    try:
        found = await probe_candidates(model, **_accepted_kwargs(probe_candidates, options))
        candidates = [
            {"region": str(c["region"]), "url": str(c["url"])}
            for c in found or ()
            if isinstance(c, Mapping)
            and c.get("purpose") == REGION_CHOICE
            and c.get("region")
            and c.get("url")
        ]
        if not candidates:
            return None
        return await measure_regions(candidates, sampler=sampler)
    except Exception:
        return None


async def measure_regions(
    candidates: list[dict[str, str]],
    *,
    sampler: Sampler | None = None,
    timeout_s: float | None = None,
    samples_per_region: int = REGION_PROBE_SAMPLES_PER_REGION,
    clock: Callable[[], float] = time.monotonic,
) -> RegionProbeResult:
    """Measure every candidate region in parallel within the deadline and rank them."""
    regions = list({c["region"]: c["url"] for c in candidates}.items())
    if not regions:
        return RegionProbeResult((), (), "failed", None)
    sampler = sampler or default_sampler()
    trusts_first = getattr(sampler, "trusts_first_sample", False)
    tcp_only: set[str] = getattr(sampler, "tcp_only", set())
    budget = getattr(sampler, "deadline_s", DIRECT_DEADLINE_S)
    deadline = clock() + (timeout_s if timeout_s is not None else budget)
    limit = max(1, samples_per_region)
    samples: dict[str, list[float]] = {region: [] for region, _ in regions}
    connecting_since: dict[str, float] = {}
    finished: set[str] = set()
    changed = asyncio.Event()

    async def run(region: str, url: str) -> None:
        def connecting() -> None:
            connecting_since.setdefault(region, clock())

        try:
            # Each region resolves its own name: a slow lookup holds only that region.
            resolved = await sampler.resolve(url)
            stream = sampler.samples(url, resolved, limit, on_connecting=connecting)
            async with contextlib.aclosing(stream) as values:
                async for elapsed_ms in values:
                    samples[region].append(float(elapsed_ms))
                    changed.set()
                    if len(samples[region]) >= limit:
                        break
        except Exception:
            pass
        finally:
            finished.add(region)
            changed.set()

    tasks = [asyncio.create_task(run(region, url)) for region, url in regions]
    try:
        while len(finished) < len(tasks):
            now = clock()
            if now >= deadline:
                break
            waited = {r: (now - t) * 1000.0 for r, t in connecting_since.items()}
            if leader_is_clear(
                samples, finished, waited_ms=waited, trusts_first_sample=trusts_first
            ):
                break
            changed.clear()
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(
                    changed.wait(), timeout=min(_EARLY_STOP_TICK_S, deadline - now)
                )
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    result = rank_region_samples(
        samples, candidate_order=tuple(region for region, _ in regions), attempted_samples=limit
    )
    intercepted = [
        statistics.median(samples[region])
        for region, url in regions
        if url in tcp_only and samples[region]
    ]
    if len(intercepted) >= 2 and max(intercepted) - min(intercepted) <= INTERCEPTED_SPREAD_MS:
        # A transparent intercepting proxy answered every TCP connect: no region is nearer.
        return replace(result, status="degraded", confident_winner=None, intercepted=True)
    return result


@dataclass(frozen=True)
class NearestRegion:
    region: str
    # This machine's round trip to it, when it was measured.
    median_ms: float | None
    source: str
    # The place the control plane located this machine in, when that decided it.
    location: str | None = None


def nearest_region(
    candidates: list[dict[str, str]],
    *,
    ask: Callable[[list[dict[str, object]]], Any] | None = None,
    allowed: Collection[str] | None = None,
) -> NearestRegion | None:
    """The region nearest this machine: measured twice at most (a probe that was cold the first
    time answers the second), then decided by the control plane (``ask``, POST
    /v1/regions/resolve), which also knows where this machine is and the regions with no probe.

    A control plane that can't answer leaves the measurement alone: a clear winner, even when the
    early stop left slower regions short of samples (degraded); a tie among fully measured
    regions, the fastest; nothing after an intercepting proxy (no winner, degraded) or a failure.
    None when nothing decided it."""
    result = None
    for _ in range(2 if candidates else 0):
        try:
            result = asyncio.run(measure_regions(candidates))
        except Exception:
            continue
        if _clear_winner(result) is not None:
            break
    measured = {m.region: m.median_ms for m in result.measurements} if result else {}
    answer = None
    if ask is not None:
        trusted = result is not None and not result.intercepted
        try:
            answer = ask([m.to_wire() for m in result.measurements] if trusted else [])
        except Exception:
            answer = None
    if isinstance(answer, Mapping) and answer.get("source") in ("measured", "location"):
        region = answer.get("region")
        if isinstance(region, str) and (allowed is None or region in allowed):
            location = answer.get("location")
            return NearestRegion(
                region,
                measured.get(region),
                str(answer["source"]),
                location if isinstance(location, str) else None,
            )
    chosen = _clear_winner(result) if result is not None else None
    return NearestRegion(chosen, measured.get(chosen), "measured") if chosen else None


def _clear_winner(result: RegionProbeResult) -> str | None:
    return result.confident_winner or (
        result.order[0] if result.status == "ok" and result.order else None
    )


def leader_is_clear(
    samples: Mapping[str, list[float]],
    finished: set[str] | frozenset[str] = frozenset(),
    *,
    waited_ms: Mapping[str, float],
    trusts_first_sample: bool,
) -> bool:
    """Whether more samples can't change the winner.

    The leader is the lowest median among regions with three samples. Every other region
    must be more than the tie window behind it: by its median once it has three samples; by
    its best sample before that (on httpx not counting its first request, which a cold start
    can slow); direct, with no sample yet, by how long its own TCP connect has been pending
    (its round trip is longer). A region that finished without three samples counts as slower
    than every region with them. Anything else can't be ruled out yet."""
    usable = {
        region: statistics.median(values)
        for region, values in samples.items()
        if len(values) >= REGION_PROBE_MIN_SUCCESSES
    }
    if not usable:
        return False
    leader = min(usable, key=lambda region: usable[region])
    lead_ms = usable[leader]
    window = max(TIE_MS, TIE_FRACTION * lead_ms)
    for region, values in samples.items():
        if region == leader or region in finished and region not in usable:
            continue
        if region in usable:
            floor = usable[region]
        elif values and trusts_first_sample:
            floor = min(values)
        elif len(values) >= 2:
            floor = min(values[1:])
        elif not values and trusts_first_sample and region in waited_ms:
            floor = waited_ms[region]
        else:
            return False
        if floor - lead_ms <= window:
            return False
    return True


class HttpsSampler:
    """Direct round trips: per region one keep-alive TLS connection; the TCP connect is the
    first sample, the TLS handshake isn't sampled, each ``GET`` after it is one more. A failed
    request is retried on a fresh connection (whose connect is a sample too) until the
    deadline; a failed TLS handshake switches the region to TCP connects."""

    deadline_s = DIRECT_DEADLINE_S
    trusts_first_sample = True

    def __init__(
        self,
        *,
        context: ssl.SSLContext | None = None,
        clock: Callable[[], float] = time.perf_counter,
        connect_attempt_s: float = CONNECT_ATTEMPT_S,
        retry_pause_s: float = RETRY_PAUSE_S,
    ) -> None:
        self._clock = clock
        self._context = context or _ssl_context()
        self._connect_attempt_s = connect_attempt_s
        self._retry_pause_s = retry_pause_s
        self.tcp_only: set[str] = set()

    async def resolve(self, url: str) -> list[tuple[int, tuple[Any, ...]]]:
        parts = urlsplit(url)
        if parts.scheme != "https" or not parts.hostname:
            raise ValueError(f"not an https URL: {url!r}")
        infos = await asyncio.get_running_loop().getaddrinfo(
            parts.hostname, parts.port or 443, type=socket.SOCK_STREAM
        )
        return _interleave([(info[0], info[4]) for info in infos])

    async def samples(
        self,
        url: str,
        resolved: list[tuple[int, tuple[Any, ...]]],
        limit: int,
        *,
        on_connecting: Callable[[], None] = lambda: None,
    ) -> AsyncIterator[float]:
        parts = urlsplit(url)
        host = parts.hostname or ""
        path = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
        request = (
            f"GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\n"
            "User-Agent: dreamscale-sdk region-probe\r\nConnection: keep-alive\r\n\r\n"
        ).encode("ascii")
        addresses = list(resolved)
        count = 0
        on_connecting()
        while count < limit:
            try:
                reader, writer, connect_ms = await self._connect(addresses)
            except OSError:
                await asyncio.sleep(self._retry_pause_s)
                continue
            try:
                yield connect_ms
                count += 1
                if count >= limit:
                    return
                if url in self.tcp_only:
                    continue
                try:
                    await writer.start_tls(self._context, server_hostname=host)
                except (ssl.SSLError, ConnectionError, OSError):
                    # TLS refused (an inspecting middlebox, a clock or trust problem): a TCP
                    # connect is one round trip too, so keep measuring with those.
                    self.tcp_only.add(url)
                    continue
                while count < limit:
                    started = self._clock()
                    writer.write(request)
                    await writer.drain()
                    status, reusable = await _read_response(reader)
                    elapsed_ms = (self._clock() - started) * 1000.0
                    if not 200 <= status < 400:
                        break  # retried on a fresh connection
                    yield elapsed_ms
                    count += 1
                    if not reusable:
                        break
            except (OSError, asyncio.IncompleteReadError, asyncio.LimitOverrunError, ValueError):
                pass  # a reset or a garbled answer: retried on a fresh connection
            finally:
                writer.close()
            if count < limit:
                await asyncio.sleep(self._retry_pause_s)

    async def _connect(
        self, addresses: list[tuple[int, tuple[Any, ...]]]
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter, float]:
        """Connect to the first address that answers, in order (each but the last gets
        ``connect_attempt_s`` before the next is tried); the one that did goes first next time.
        Returns the connect's round trip (ms) with the streams."""
        error: OSError | None = None
        for index, (family, address) in enumerate(addresses):
            started = self._clock()
            last = index == len(addresses) - 1
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(address[0], address[1], family=family),
                    timeout=None if last else self._connect_attempt_s,
                )
            except (OSError, TimeoutError) as exc:
                error = exc if isinstance(exc, OSError) else OSError(str(exc) or "timeout")
                continue
            elapsed_ms = (self._clock() - started) * 1000.0
            if index:
                addresses.insert(0, addresses.pop(index))
            return reader, writer, elapsed_ms
        raise error or OSError("no address")


class HttpxSampler:
    """Round trips through httpx, which honours ``HTTPS_PROXY``/``ALL_PROXY`` (and the
    system's proxy settings) and ``SSL_CERT_FILE``/``SSL_CERT_DIR``.

    One client (one keep-alive connection) per region. Each sample is one request's round
    trip, timed from its headers going out to the response headers coming back, so connection
    setup (and a proxy's CONNECT) is never counted. Failed requests are retried until the
    deadline."""

    deadline_s = HTTPX_DEADLINE_S
    trusts_first_sample = False

    def __init__(
        self,
        *,
        clock: Callable[[], float] = time.perf_counter,
        retry_pause_s: float = RETRY_PAUSE_S,
    ) -> None:
        self._clock = clock
        self._retry_pause_s = retry_pause_s
        self.tcp_only: set[str] = set()

    async def resolve(self, url: str) -> str:
        return url  # httpx (or the proxy) resolves

    async def samples(
        self,
        url: str,
        resolved: Any,
        limit: int,
        *,
        on_connecting: Callable[[], None] = lambda: None,
    ) -> AsyncIterator[float]:
        marks: dict[str, float] = {}

        async def trace(event: str, _info: dict) -> None:
            if event.endswith("send_request_headers.started"):
                marks["sent"] = self._clock()
            elif event.endswith("receive_response_headers.complete"):
                marks["answered"] = self._clock()

        count = 0
        on_connecting()
        timeout = httpx.Timeout(HTTPX_DEADLINE_S)
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
            while count < limit:
                marks.clear()
                started = self._clock()
                try:
                    response = await client.get(url, extensions={"trace": trace})
                except httpx.HTTPError:
                    await asyncio.sleep(self._retry_pause_s)
                    continue
                ended = self._clock()
                if not 200 <= response.status_code < 400:
                    await asyncio.sleep(self._retry_pause_s)
                    continue
                if "sent" in marks and "answered" in marks:
                    yield (marks["answered"] - marks["sent"]) * 1000.0
                else:
                    yield (ended - started) * 1000.0
                count += 1


def default_sampler(environ: Mapping[str, str] | None = None) -> Sampler:
    """httpx behind a proxy or with custom certificates (what it honours); else direct."""
    environ = os.environ if environ is None else environ
    if environ.get("SSL_CERT_FILE") or environ.get("SSL_CERT_DIR") or _proxied(environ):
        return HttpxSampler()
    return HttpsSampler()


def _proxied(environ: Mapping[str, str]) -> bool:
    if environ is os.environ:
        proxies = urllib.request.getproxies()  # the environment, then the system's settings
    else:
        proxies = {
            k.lower()[: -len("_proxy")]: v
            for k, v in environ.items()
            if k.lower().endswith("_proxy") and v
        }
    return bool(proxies.get("https") or proxies.get("all"))


def _interleave(
    addresses: list[tuple[int, tuple[Any, ...]]],
) -> list[tuple[int, tuple[Any, ...]]]:
    """Distinct addresses, alternating families from the resolver's first (RFC 8305)."""
    seen: set[tuple[int, Any]] = set()
    unique = []
    for family, address in addresses:
        key = (family, address[0])
        if key not in seen:
            seen.add(key)
            unique.append((family, address))
    if not unique:
        raise OSError("no address")
    first = unique[0][0]
    ours = [a for a in unique if a[0] == first]
    others = [a for a in unique if a[0] != first]
    out = []
    for index in range(max(len(ours), len(others))):
        out.extend(group[index] for group in (ours, others) if index < len(group))
    return out


async def _read_response(reader: asyncio.StreamReader) -> tuple[int, bool]:
    """Read one HTTP/1.1 response; ``(status, connection reusable)``."""
    head = await reader.readuntil(b"\r\n\r\n")
    lines = head.decode("latin-1").split("\r\n")
    status = int(lines[0].split(" ", 2)[1])
    headers = {}
    for line in lines[1:]:
        name, _, value = line.partition(":")
        if name:
            headers[name.strip().lower()] = value.strip().lower()
    keep = headers.get("connection") != "close"
    if status in (204, 304) or 100 <= status < 200:
        return status, keep
    if "chunked" in headers.get("transfer-encoding", ""):
        while True:
            size = int((await reader.readuntil(b"\r\n")).split(b";")[0], 16)
            await reader.readexactly(size + 2)
            if size == 0:
                return status, keep
    if "content-length" in headers:
        await reader.readexactly(int(headers["content-length"]))
        return status, keep
    return status, False


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        context = ssl.create_default_context(cafile=certifi.where())
    except ImportError:  # pragma: no cover - certifi comes with httpx
        context = ssl.create_default_context()
    context.set_alpn_protocols(["http/1.1"])
    return context
