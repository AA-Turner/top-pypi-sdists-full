# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""HTTP metrics collection using mitmproxy.

This module provides utilities for capturing HTTP traffic from connector
executions using mitmproxy as a local subprocess.
"""

from __future__ import annotations

import logging
import re
import shutil
import signal
import socket
import subprocess
import tempfile
import time
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import IO, Iterator, Sequence
from urllib.parse import parse_qsl, urlsplit, urlunsplit

try:
    from mitmproxy import http as mitmproxy_http
    from mitmproxy import io as mitmproxy_io
    from mitmproxy.addons.savehar import SaveHar

    MITMPROXY_AVAILABLE = True
except ImportError:
    mitmproxy_http = None  # type: ignore[assignment]
    mitmproxy_io = None  # type: ignore[assignment]
    SaveHar = None  # type: ignore[assignment, misc]
    MITMPROXY_AVAILABLE = False

logger = logging.getLogger(__name__)

MITMPROXY_DIR = Path.home() / ".mitmproxy"
CA_CERT_FILENAME = "mitmproxy-ca-cert.pem"

# Wait times for mitmdump subprocess startup
MITMDUMP_CA_BOOTSTRAP_WAIT_SECONDS = 2
PROCESS_KILL_TIMEOUT_SECONDS = 5

# How long a `SIGINT` gets before the `SIGKILL`. mitmproxy's `save` addon writes
# each flow through a block-buffered file and only flushes it, appends the flows
# still in flight and closes it in `done()` -- which a `SIGKILL` never reaches,
# so a kill silently shortens the dump `live_flow_count` is computed from, and
# always in the direction that makes a run look closer to the replay acceptance
# criterion than it was. Measured against mitmdump 11.1.3, `SIGINT` to exit takes
# ~4.1 s at the 256 MB corpus cap (158k flows) and ~10 s at 646 MB, so the 5 s
# `PROCESS_KILL_TIMEOUT_SECONDS` budget sat ~20% above the measured shutdown at
# the cap -- on a slower CI runner, under it. The process is exiting anyway, so a
# generous wait costs nothing on the happy path.
MITMDUMP_SHUTDOWN_TIMEOUT_SECONDS = 30

# mitmdump's stdout and stderr go to a file in the output directory, never to a
# pipe. `--flow-detail 0` silences flow summaries but not the log, which keeps
# emitting ~205 B of connection events per connection cycle; nothing here drains
# that pipe, so mitmdump blocks in `write()` once the ~64 KB pipe buffer fills
# (measured: a hard stall at ~330 connection cycles) and from then on every
# connector request hangs with no response, which reads as a regression in the
# version under test. It compounds: a blocked mitmdump is stuck inside its own
# event loop, so the `save` addon stops too and the shutdown `SIGINT` cannot be
# serviced. A file cannot fill, and it keeps the startup diagnosis that
# `DEVNULL` would throw away. At this verbosity the log holds host/port pairs
# rather than URLs, so it is not the customer-data surface the dumps are -- with
# one exception: with `server_replay_extra` set to anything but `forward`,
# `ServerPlayback` logs the full URL of every request it kills or fakes at
# warning level. The log *is* uploaded with the artifacts, so `redact_log_urls`
# masks those URLs before the run ends.
MITMDUMP_LOG_FILENAME = "mitmdump.log"
# Enough of the log's tail to carry a startup error, e.g. "Address already in use".
MITMDUMP_LOG_TAIL_BYTES = 4096

# The log is the one thing this feature writes with no natural bound, and unlike
# the dumps it is uploaded: nothing prunes it, `_discard_oversized_http_dumps`
# covers `http_traffic.mitm` only, and the workflow's upload steps exclude
# `**/*.mitm` and `**/*.har` but not `*.log`. Measured at `--flow-detail 0`
# against an origin that closes each connection, it grows ~226 B per connection
# cycle -- so a long `read` making 500k such requests writes ~113 MB, on a runner
# whose disk this module otherwise bounds. `--strict-replay` narrows the gap
# further: it logs a full URL line per unmatched request, and it is reached for
# precisely when coverage is poor, i.e. when there are many. Kept as a tail
# rather than a cap-and-drop because a proxy log's diagnostic value is at its
# end, and 8 MiB is ~37k connection cycles of it.
MITMDUMP_LOG_MAX_BYTES = 8 * 1024 * 1024

# mitmdump binds its listen port only after its addons are configured, and
# `ServerPlayback` reads and hashes the whole corpus during configuration:
# measured against mitmdump 11.1.3, a 256 MB corpus of 150k small flows takes
# ~23 s before the port accepts a connection, against ~0.6 s with no corpus.
# Waiting a fixed second and only checking that the process has not exited
# starts the connector against a connection-refused proxy, which reads as a
# regression in the version under test -- the misattribution replay exists to
# remove. So wait for the port itself, generously.
MITMDUMP_LISTEN_TIMEOUT_SECONDS = 60
MITMDUMP_LISTEN_POLL_INTERVAL_SECONDS = 0.1
MITMDUMP_LISTEN_PROBE_TIMEOUT_SECONDS = 1

# Bodies larger than this are streamed through the proxy rather than buffered,
# and mitmproxy never stores a streamed body on the flow. The previous value
# here was `1`, which `human.parse_size` reads as *one byte* -- so every
# response was streamed and the dump recorded `content=None` throughout, making
# the dumps useless for anything but counting requests.
#
# `1m` is a replay-coverage versus memory dial: a replay run holds every
# recorded body in RAM (roughly baseline + 1x the dump), and most REST pages sit
# well under 1 MB. Responses above the threshold are simply not recorded, so
# they are re-fetched live instead of replayed.
DEFAULT_STREAM_LARGE_BODIES = "1m"

# Ceiling on a dump we are about to load into memory in full. Both consumers
# that do so -- mitmdump's server-replay flowmap and the HAR export -- cost
# roughly the dump's size in RAM, and the regression workflows run on 7 GB
# `ubuntu-latest` runners shared with the connector's own container.
MAX_IN_MEMORY_DUMP_BYTES = 256 * 1024 * 1024
DEFAULT_MAX_REPLAY_DUMP_SIZE_MB = MAX_IN_MEMORY_DUMP_BYTES // (1024 * 1024)

# What mitmproxy does with a request that matches nothing in the replay corpus.
# `forward` sends it upstream, so replay can never silently truncate a run; the
# alternatives (`kill`, `404`) are for measuring exactly what did not match.
DEFAULT_REPLAY_EXTRA = "forward"

# The filtered copy of the control dump that the target run replays from. Never
# point `--server-replay` at a raw dump: see `build_replay_corpus`. It is a
# derived intermediate and is written to a scratch directory rather than the
# artifact tree -- it is a near-full copy of the control dump, so keeping it
# there would put a third copy of the recorded response bodies in the upload.
REPLAY_CORPUS_FILENAME = "http_replay_corpus.mitm"
REPLAY_CORPUS_DIR_PREFIX = "airbyte-replay-corpus-"

# How many live URLs a run reports. Enough to see the shape of what did not match
# without turning the report into a request log -- a `read` makes thousands.
MAX_LIVE_URLS_REPORTED = 20

# What a redacted query-parameter value is replaced with.
#
# Every URL that leaves this module is redacted first. Regression tests run
# against real customer connections, and the surfaces a URL reaches -- the step
# summary, the workflow log, the `regression_report` output, `report.html` in the
# uploaded artifact -- are readable by every member of an internal org, which is
# why the dumps themselves are excluded from the upload. Plenty of APIs still
# carry credentials in the query string (`access_token`, `api_key`, `signature`),
# and a URL is not worth widening that surface for.
#
# What makes an unmatched request diagnosable survives redaction: the path (where
# a per-run job id lives) and the parameter *names* (a `since`/`until` window
# computed from the clock is recognisable from the names appearing at all, on a
# request that never matched).
#
# Square brackets rather than angle ones: the step summary is markdown rendered
# through GitHub's HTML sanitizer, which *removes* a non-whitelisted tag instead
# of escaping it -- `<redacted>` would disappear and leave `?access_token=`,
# which reads as an empty parameter rather than a masked one. `[redacted]` is
# inert in markdown, HTML and JSON alike.
REDACTED_VALUE = "[redacted]"

# The same marker without its brackets, for the userinfo of a netloc. There,
# `[redacted]@host` is a bracketed *host* to `urlsplit`, which then rejects it
# for not being an IP address -- so redacting a URL twice would raise rather
# than return what it returned the first time. Nothing redacts twice today, but
# `redact_url` is applied once at the seam precisely so that every consumer can
# treat its output as safe, which invites a second call from anyone unsure
# whether a value has already been through it. The markdown constraint that
# chose the brackets applies to query values, which is where they are kept.
REDACTED_NETLOC_VALUE = REDACTED_VALUE.strip("[]")

# The URLs `ServerPlayback` logs when it kills or fakes an unmatched request.
_LOG_URL_PATTERN = re.compile(r"https?://\S+")


def redact_url(url: str) -> str:
    """Mask the credential-bearing parts of `url`, keeping what identifies it.

    Scheme, host, port, path and query-parameter *names* are kept; every
    parameter value is replaced with `REDACTED_VALUE` and any userinfo with
    `REDACTED_NETLOC_VALUE`. See those constants for why this is applied to
    every URL that leaves the module rather than to a denylist of parameter
    names, and why the netloc gets a marker of its own.

    What this makes safe is the *query string*, not the whole URL. The path is
    kept on purpose -- a per-run job id lives there, and that is the diagnostic
    the reported URLs exist for -- so an API that puts a credential in the path
    (`api.telegram.org/bot<token>/getUpdates`) still reports it. Weigh that
    before giving a new surface one of these URLs.

    A URL with no query string and no userinfo comes back unchanged, and
    redacting an already-redacted URL returns it unchanged as well: the callers
    below apply this once, at the point the counts are built, so that everything
    downstream can treat a URL as safe without knowing where it came from.

    Args:
        url: The URL as recorded on the flow.

    Returns:
        The URL with its values masked, or `REDACTED_VALUE` alone when it cannot
        be parsed -- unparseable must not mean unredacted, and this is called
        from `parse_http_dump` and from `_stop`'s log rewrite, where raising
        would cost a finished run its metrics or leave the log unmasked.
    """
    try:
        parts = urlsplit(url)
    except ValueError as exc:
        # `urlsplit` rejects a netloc whose brackets are not a valid IP, among
        # others. Whatever the reason, a URL this function cannot take apart is
        # one it cannot promise anything about, so nothing of it is reported.
        # Only the exception's *type* is logged: several of `urlsplit`'s messages
        # quote the netloc they rejected, which is the part that carries userinfo,
        # so interpolating `exc` would leak here what the return value masks.
        logger.debug(
            f"Could not parse a URL to redact it ({type(exc).__name__}); reporting nothing"
        )
        return REDACTED_VALUE

    netloc = parts.netloc
    if "@" in netloc:
        netloc = f"{REDACTED_NETLOC_VALUE}@{netloc.rsplit('@', 1)[1]}"

    query = ""
    if parts.query:
        # `keep_blank_values` so a valueless parameter is still reported as one:
        # its name is the diagnostic, and it carries nothing to mask.
        query = "&".join(
            f"{name}={REDACTED_VALUE}" if value else name
            for name, value in parse_qsl(parts.query, keep_blank_values=True)
        )

    # The fragment is dropped rather than masked: it is never sent upstream, so
    # it cannot be part of what a request matched or failed to match.
    return urlunsplit((parts.scheme, netloc, parts.path, query, ""))


@dataclass
class HttpMetrics:
    """HTTP traffic metrics from a connector execution."""

    flow_count: int
    duplicate_flow_count: int
    # Redacted (see `redact_url`); deduplication happens on the raw URLs, so
    # `duplicate_flow_count` still counts genuinely repeated requests.
    unique_urls: list[str]
    cache_hits_count: int = 0
    # `live_flow_count` on a replaying target run is the acceptance criterion for
    # HTTP replay: zero means the two versions saw byte-identical upstream data,
    # and anything else is a request the corpus could not answer.
    replayed_flow_count: int = 0
    live_flow_count: int = 0
    replay_source: str | None = None
    # Which URLs those live requests were, and how often each was made. On a
    # replaying run this is the only thing that can explain a coverage shortfall
    # after the fact: the dumps are deliberately kept out of the uploaded
    # artifacts, so without it the aggregate count is all that survives the run.
    #
    # Keyed by *redacted* URL -- see `redact_url`. Redacting on the way in rather
    # than on the way out means no consumer can leak a raw URL by reading the
    # field directly, and requests that differ only in a masked value (a rotated
    # `access_token`, a per-page cursor) group into one entry, which is the shape
    # a coverage shortfall usually has.
    live_url_counts: dict[str, int] = field(default_factory=dict)

    @property
    def cache_hit_ratio(self) -> str:
        """Calculate cache hit ratio as a percentage string."""
        if self.flow_count == 0:
            return "N/A"
        return f"{(self.cache_hits_count / self.flow_count) * 100:.2f}%"

    @property
    def replay_hit_ratio(self) -> str:
        """Share of requests served from the recording, as a percentage string."""
        if self.flow_count == 0:
            return "N/A"
        return f"{(self.replayed_flow_count / self.flow_count) * 100:.2f}%"

    def top_live_urls(
        self, limit: int = MAX_LIVE_URLS_REPORTED
    ) -> list[dict[str, object]]:
        """The URLs fetched live, most-repeated first, capped at `limit`.

        Ordered by count so a whole class of unmatched request -- an async report
        polled under a per-run job id, a `since`/`until` window computed from the
        clock -- leads, since that is the shape a low replay ratio usually has.

        The URLs are redacted; see `live_url_counts` and `redact_url`.
        """
        ordered = sorted(
            self.live_url_counts.items(), key=lambda item: (-item[1], item[0])
        )
        return [{"url": url, "count": count} for url, count in ordered[:limit]]

    @classmethod
    def empty(cls) -> HttpMetrics:
        """Create empty metrics when HTTP capture is unavailable."""
        return cls(
            flow_count=0, duplicate_flow_count=0, unique_urls=[], cache_hits_count=0
        )


@dataclass(frozen=True)
class ReplayOptions:
    """How the target run should replay the control run's recorded traffic.

    Attributes:
        reuse: Serve a recorded response more than once. The default pops each
            flow as it is matched, which preserves recorded ordering when the
            same request legitimately returned different responses -- and lets
            the flowmap shrink as the run proceeds. `True` never releases a
            flow, so the whole corpus stays resident for the entire run.
        extra: What to do with a request that matches nothing. See
            `DEFAULT_REPLAY_EXTRA`.
        ignore_params: Query parameters to exclude from the match key, for
            connectors that put a timestamp or nonce in the URL.
        max_dump_bytes: Skip replay entirely when the corpus is larger than
            this. mitmdump holds the whole corpus in RAM before serving a single
            request (measured at baseline + ~1.0x the corpus size), so a live
            target run is the better failure mode.
    """

    reuse: bool = False
    extra: str = DEFAULT_REPLAY_EXTRA
    ignore_params: tuple[str, ...] = ()
    max_dump_bytes: int = MAX_IN_MEMORY_DUMP_BYTES


@dataclass
class MitmproxySession:
    """Active mitmproxy session information."""

    proxy_host: str
    proxy_port: int
    dump_file_path: Path
    ca_cert_path: Path | None
    # The corpus this run is replaying from, or `None` when it is recording
    # only. `replay_skipped_reason` says why replay was asked for and not
    # delivered, so the report can say so rather than presenting a live run as
    # a replayed one.
    replay_source: Path | None = None
    replay_skipped_reason: str | None = None
    unreplayable_flow_count: int = 0

    @property
    def proxy_url(self) -> str:
        """Get the proxy URL for HTTP_PROXY/HTTPS_PROXY env vars."""
        return f"http://{self.proxy_host}:{self.proxy_port}"


def find_free_port() -> int:
    """Find a free port on the local machine."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.listen(1)
        return s.getsockname()[1]


def _kill_if_running(proc: subprocess.Popen | None) -> None:
    """Make sure a mitmdump we started is gone, whatever went wrong.

    A `terminate`/`wait` that timed out leaves the process alive and holding a
    listen port; nothing later in the run would ever reap it.
    """
    if proc is None or proc.poll() is not None:
        return

    proc.kill()
    try:
        proc.wait(timeout=PROCESS_KILL_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        logger.warning(f"Could not reap mitmdump (pid {proc.pid})")


def read_log_tail(
    log_path: Path | None,
    max_bytes: int = MITMDUMP_LOG_TAIL_BYTES,
) -> str:
    """The end of mitmdump's log, for reporting why it exited.

    Its output goes to a file rather than a pipe (see `MITMDUMP_LOG_FILENAME`),
    so this -- not `proc.stderr` -- is where a startup error is to be found.
    """
    if log_path is None or not log_path.exists():
        return "no log output"

    with open(log_path, "rb") as log:
        log.seek(max(0, log_path.stat().st_size - max_bytes))
        return log.read().decode(errors="replace").strip() or "no log output"


def truncate_log_to_tail(
    log_path: Path,
    max_bytes: int = MITMDUMP_LOG_MAX_BYTES,
) -> None:
    """Keep only the last `max_bytes` of mitmdump's log, in place.

    The log is unbounded and uploaded with the artifacts (see
    `MITMDUMP_LOG_MAX_BYTES`), while the dump it sits next to is discarded above
    a cap. This closes that asymmetry from the front, because what a proxy log is
    read for -- why it exited, which requests it killed last -- is at its end.

    Drops the partial first line so the file still parses line by line, and says
    in the file itself how much went, so a truncated log cannot be mistaken for
    the whole run. Best effort: losing a diagnostic is better than failing a
    finished run over it.

    Args:
        log_path: mitmdump's log for the run.
        max_bytes: How much of the tail to keep.
    """
    try:
        size = log_path.stat().st_size
    except OSError:
        return

    if size <= max_bytes:
        return

    scratch = log_path.with_suffix(log_path.suffix + ".truncating")
    try:
        with open(log_path, "rb") as source, open(scratch, "wb") as dest:
            source.seek(size - max_bytes)
            source.readline()  # Discard the line the seek landed inside.
            dest.write(f"[{size - source.tell()} earlier byte(s) truncated]\n".encode())
            shutil.copyfileobj(source, dest)
        scratch.replace(log_path)
    except OSError as exc:
        scratch.unlink(missing_ok=True)
        logger.warning(
            f"Could not truncate {log_path} ({exc}); left it at {size} bytes"
        )


def redact_log_urls(log_path: Path) -> None:
    """Mask the URLs `ServerPlayback` logged for unmatched requests, in place.

    Only reached when `server_replay_extra` is not `forward`: on that path
    mitmproxy logs the full URL of every request it kills or fakes at warning
    level, unbounded, and `mitmdump.log` is uploaded with the artifacts. Strict
    replay is also exactly the mode reached for when coverage is poor, i.e. when
    there are many such requests to log.

    Rewrites through a sibling temporary file so a failure cannot leave a
    half-masked log, and streams line by line because the log is unbounded.
    Called after mitmdump has exited, so nothing is still appending to it.

    Args:
        log_path: mitmdump's log for the run.
    """
    if not log_path.exists():
        return

    scratch = log_path.with_suffix(log_path.suffix + ".redacting")
    try:
        with open(log_path, "rb") as source, open(scratch, "wb") as dest:
            for line in source:
                dest.write(
                    _LOG_URL_PATTERN.sub(
                        lambda match: redact_url(match.group(0)),
                        line.decode(errors="replace"),
                    ).encode()
                )
        scratch.replace(log_path)
    except OSError as exc:
        # The log is a diagnostic; failing the run over it would be worse than
        # losing it. Unredacted is not an option, so drop it and say why.
        scratch.unlink(missing_ok=True)
        log_path.unlink(missing_ok=True)
        logger.warning(
            f"Could not redact {log_path} ({exc}); discarded it rather than "
            "leaving unredacted URLs in the artifacts"
        )


def wait_for_proxy_listener(
    proc: subprocess.Popen,
    port: int,
    timeout: float = MITMDUMP_LISTEN_TIMEOUT_SECONDS,
    log_path: Path | None = None,
) -> str | None:
    """Wait until `proc` accepts connections on `port`.

    The probe is a plain TCP connect, so it creates no flow and does not appear
    in the recorded dump.

    Args:
        proc: The mitmdump process being waited on.
        port: The port it was told to listen on.
        timeout: How long to wait before giving up. See
            `MITMDUMP_LISTEN_TIMEOUT_SECONDS` for why it is this generous.
        log_path: Where `proc` writes its log, read for the reason it exited.

    Returns:
        `None` once the port is accepting connections, or why it never did.
    """
    deadline = time.monotonic() + timeout
    while True:
        if proc.poll() is not None:
            return f"mitmproxy exited during startup: {read_log_tail(log_path)}"

        try:
            with socket.create_connection(
                ("127.0.0.1", port), timeout=MITMDUMP_LISTEN_PROBE_TIMEOUT_SECONDS
            ):
                return None
        except OSError:
            pass

        if time.monotonic() >= deadline:
            return f"mitmproxy did not accept connections on port {port} in {timeout}s"

        time.sleep(MITMDUMP_LISTEN_POLL_INTERVAL_SECONDS)


def ensure_mitmproxy_ca_cert() -> Path | None:
    """Ensure mitmproxy CA certificate exists.

    Mitmproxy generates its CA cert on first run. This function runs
    mitmdump briefly to generate the cert if it doesn't exist.

    Returns:
        Path to the CA cert file, or None if generation failed.
    """
    ca_cert_path = MITMPROXY_DIR / CA_CERT_FILENAME

    if ca_cert_path.exists():
        logger.debug(f"Mitmproxy CA cert already exists at {ca_cert_path}")
        return ca_cert_path

    mitmdump_path = shutil.which("mitmdump")
    if not mitmdump_path:
        logger.warning("mitmdump not found in PATH, cannot generate CA cert")
        return None

    logger.info("Generating mitmproxy CA certificate...")
    proc: subprocess.Popen | None = None
    try:
        # On a free port, not mitmproxy's default 8080: a port clash here means
        # no CA, and without the CA the connector cannot verify the proxy, so
        # the capture comes back near-empty instead of failing.
        proc = subprocess.Popen(
            [mitmdump_path, "--listen-port", str(find_free_port())],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Wait for mitmdump to start and generate CA cert on first run
        time.sleep(MITMDUMP_CA_BOOTSTRAP_WAIT_SECONDS)
        proc.terminate()
        proc.wait(timeout=5)

        if ca_cert_path.exists():
            logger.info(f"Generated mitmproxy CA cert at {ca_cert_path}")
            return ca_cert_path
        else:
            logger.warning("Failed to generate mitmproxy CA cert")
            return None

    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        logger.warning(f"Failed to generate mitmproxy CA cert: {e}")
        return None

    finally:
        # A `terminate` that timed out leaves a bootstrap proxy holding a port
        # for the rest of the session, which the next run then collides with.
        _kill_if_running(proc)


def discard_oversized_dump(dump_file_path: Path, max_bytes: int) -> int | None:
    """Delete a recorded dump too large to keep, once nothing needs it.

    Recording bodies means the dump grows with everything the connector
    downloads -- a `read` has a three-hour budget -- and both runs' dumps sit in
    the directory the workflow uploads wholesale, on a runner with ~14 GB of
    disk shared with the connector container's own output.

    This bounds what a run *leaves behind*; it cannot bound the peak while the
    capture is running, which would need mitmproxy to stop recording mid-run and
    it has no size cap of its own. A dump this big is also past the point of
    being useful to open by hand.

    Args:
        dump_file_path: The recorded dump.
        max_bytes: Size above which the dump is discarded rather than kept.

    Returns:
        The size it had when discarded, or `None` when it was kept.
    """
    if not dump_file_path.exists():
        return None

    size = dump_file_path.stat().st_size
    if size <= max_bytes:
        return None

    dump_file_path.unlink()
    logger.warning(
        f"Discarded {dump_file_path}: {size / 1024 / 1024:.0f} MB exceeds the "
        f"{max_bytes / 1024 / 1024:.0f} MB retention cap"
    )
    return size


def build_mitmdump_command(
    mitmdump_path: str,
    port: int,
    dump_file_path: Path,
    replay_from: Path | None = None,
    *,
    replay_reuse: bool = False,
    replay_extra: str = DEFAULT_REPLAY_EXTRA,
    replay_ignore_params: Sequence[str] = (),
    stream_large_bodies: str = DEFAULT_STREAM_LARGE_BODIES,
) -> list[str]:
    """Build the `mitmdump` argv for a recording or a replaying run.

    A replaying run still records: the target's own dump is what tells us how
    much of the run was served from the corpus and how much went live.

    Options deliberately left at their mitmproxy defaults: `server_replay_refresh`
    (on -- adjusts `Date`/`Expires` and cookie expiry, so the connector does not
    see stale-cache behaviour) and `server_replay_ignore_host`/`_port`/`_content`
    (off). Headers are not part of the match key either, so a rotated
    `Authorization` header does not break matching. Query parameters *are*, in
    the order they appear in the URL -- `ServerPlayback._hash` does not sort
    them, so a version that reorders its query string matches nothing.

    Args:
        mitmdump_path: Path to the `mitmdump` executable.
        port: Port for the proxy to listen on.
        dump_file_path: Where this run writes its own traffic dump.
        replay_from: A filtered replay corpus, or `None` to record only.
        replay_reuse: See `ReplayOptions.reuse`.
        replay_extra: See `ReplayOptions.extra`.
        replay_ignore_params: See `ReplayOptions.ignore_params`.
        stream_large_bodies: Body-size threshold above which mitmproxy streams
            rather than records. Never pass a bare number: it means bytes.

    Returns:
        The argv to run.
    """
    cmd = [
        mitmdump_path,
        "--listen-port",
        str(port),
        "--save-stream-file",
        str(dump_file_path),
        "--flow-detail",
        "0",
        "--set",
        f"stream_large_bodies={stream_large_bodies}",
    ]

    if replay_from is None:
        return cmd

    cmd.extend(
        [
            "--server-replay",
            str(replay_from),
            "--set",
            f"server_replay_reuse={'true' if replay_reuse else 'false'}",
            "--set",
            f"server_replay_extra={replay_extra}",
        ]
    )
    # A sequence option takes one `--set` per value; mitmproxy groups them.
    for param in replay_ignore_params:
        cmd.extend(["--set", f"server_replay_ignore_params={param}"])

    return cmd


def build_replay_corpus(source: Path, dest: Path) -> tuple[int, int]:
    """Copy the replayable flows of `source` into `dest`.

    A response whose body was streamed (see `DEFAULT_STREAM_LARGE_BODIES`) is
    recorded as a flow that *has* a response object with no content, and
    mitmproxy's server-replay addon neither filters those out nor notices them:
    the flow matches, wins, and is served. The client then gets a 200 with no
    body -- an `IncompleteRead` when `Content-Length` was recorded, and, for
    `Transfer-Encoding: chunked`, a well-formed empty page with no error at all.
    A connector reading that page most likely treats it as end-of-pagination and
    finishes "successfully" with fewer records, which is a false regression.

    Requests are the quieter half of the same problem: the match key includes
    `str(request.raw_content)`, so two different requests whose bodies were both
    streamed hash identically as `"None"` and serve each other's responses.

    Dropping both kinds means those requests match nothing and go upstream
    instead (with `server_replay_extra=forward`), returning real data.

    Streaming by construction, so it costs O(1) memory regardless of dump size.

    Args:
        source: The recorded dump, typically the control run's.
        dest: Where to write the filtered corpus.

    Returns:
        The number of flows kept and the number dropped as unreplayable.

    Raises:
        RuntimeError: If the mitmproxy Python package is not installed.
    """
    if not MITMPROXY_AVAILABLE:
        raise RuntimeError(
            "mitmproxy Python package not installed; cannot build a replay corpus"
        )

    kept = dropped = 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(source, "rb") as fin, open(dest, "wb") as fout:
        writer = mitmproxy_io.FlowWriter(fout)
        for flow in mitmproxy_io.FlowReader(fin).stream():
            if (
                isinstance(flow, mitmproxy_http.HTTPFlow)
                and flow.response is not None
                and flow.response.raw_content is not None
                and flow.request.raw_content is not None
            ):
                writer.add(flow)
                kept += 1
            else:
                dropped += 1

    return kept, dropped


class MitmproxyManager:
    """Manages a mitmproxy subprocess for HTTP traffic capture.

    This class starts mitmdump as a local subprocess and provides
    the proxy URL and CA cert path for connector containers to use.

    Pass `replay_from` a previous run's dump to serve its recorded responses
    instead of hitting the upstream API, so two connector versions see identical
    data. The dump is filtered into a replay corpus first -- see
    `build_replay_corpus` -- and replay is skipped, with a reason on the session,
    when the corpus is unusable or too large to hold in memory.

    Usage:
        with MitmproxyManager.start(output_dir) as session:
            # Run connector with session.proxy_url
            pass
        # After context exits, parse session.dump_file_path for metrics
    """

    def __init__(
        self,
        output_dir: Path,
        port: int | None = None,
        *,
        replay_from: Path | None = None,
        replay_options: ReplayOptions | None = None,
        stream_large_bodies: str = DEFAULT_STREAM_LARGE_BODIES,
    ) -> None:
        """Initialize the mitmproxy manager.

        Args:
            output_dir: Directory to write the dump file to.
            port: Specific port to use, or None to find a free port.
            replay_from: A previous run's dump to replay responses from, or
                None to record only.
            replay_options: Replay tuning; defaults apply when omitted.
            stream_large_bodies: Body-size threshold above which mitmproxy
                streams rather than records.
        """
        self.output_dir = output_dir
        self.port = port or find_free_port()
        self.dump_file_path = output_dir / "http_traffic.mitm"
        self.log_file_path = output_dir / MITMDUMP_LOG_FILENAME
        self.replay_from = replay_from
        self.replay_options = replay_options or ReplayOptions()
        self.stream_large_bodies = stream_large_bodies
        # Why `_start` returned no session, and whether the dump it recorded is
        # short. Both live on the manager rather than on the session: the first
        # is set exactly when there is no session to carry it, and the second is
        # only known once `_stop` has run, i.e. after the session is gone.
        self.startup_failure_reason: str | None = None
        self.metrics_incomplete_reason: str | None = None
        self._process: subprocess.Popen | None = None
        self._log_file: IO[bytes] | None = None
        self._corpus_dir: Path | None = None

    @classmethod
    @contextmanager
    def start(
        cls,
        output_dir: Path,
        port: int | None = None,
        *,
        replay_from: Path | None = None,
        replay_options: ReplayOptions | None = None,
        stream_large_bodies: str = DEFAULT_STREAM_LARGE_BODIES,
    ) -> Iterator[MitmproxySession | None]:
        """Start mitmproxy and yield a session, stopping on exit.

        This is a context manager that ensures mitmproxy is properly
        stopped even if an exception occurs.

        Args:
            output_dir: Directory to write the dump file to.
            port: Specific port to use, or None to find a free port.
            replay_from: A previous run's dump to replay responses from, or
                None to record only.
            replay_options: Replay tuning; defaults apply when omitted.
            stream_large_bodies: Body-size threshold above which mitmproxy
                streams rather than records.

        Yields:
            MitmproxySession with proxy info, or None if startup failed.
        """
        manager = cls(
            output_dir,
            port,
            replay_from=replay_from,
            replay_options=replay_options,
            stream_large_bodies=stream_large_bodies,
        )
        with manager.running() as session:
            yield session

    @contextmanager
    def running(self) -> Iterator[MitmproxySession | None]:
        """Run the proxy for the duration of the block, stopping it on exit.

        What `start` uses, and what to use instead of it when the caller needs
        `startup_failure_reason` or `metrics_incomplete_reason` -- neither can
        travel on the session, so they are only reachable through the manager.

        Yields:
            MitmproxySession with proxy info, or None if startup failed.
        """
        try:
            # Inside the `try`: `_start` spawns a process and may write a replay
            # corpus, so a failure part-way through it still has to be cleaned up.
            yield self._start()
        finally:
            self._stop()

    def _prepare_replay_corpus(self) -> tuple[Path | None, str | None, int]:
        """Filter the recorded dump into the corpus mitmdump will replay from.

        Every reason to give up here degrades to a live run rather than raising:
        a target run against the real API is always better than no target run,
        and the reason travels on the session so the report can say the
        comparison was not made against identical data.

        Returns:
            The corpus to replay from (None to record only), why replay was
            skipped, and how many flows were dropped as unreplayable.
        """
        source = self.replay_from
        if source is None:
            return None, None, 0

        if not source.exists() or source.stat().st_size == 0:
            reason = f"replay source {source} is missing or empty"
            logger.warning(f"{reason}; recording only")
            return None, reason, 0

        if not MITMPROXY_AVAILABLE:
            reason = "mitmproxy Python package not installed, cannot filter the corpus"
            logger.warning(f"{reason}; recording only")
            return None, reason, 0

        # Before the copy, not only after it: filtering can only shrink the
        # dump, and a dump already over the cap would otherwise be streamed out
        # in full -- a transient second copy of a multi-gigabyte file on a
        # runner with ~14 GB shared with the connector's own output -- just to
        # be unlinked. The post-copy check below stays as the precise gate for
        # dumps near the cap.
        source_bytes = source.stat().st_size
        if source_bytes > self.replay_options.max_dump_bytes:
            reason = (
                f"replay source is {source_bytes / 1024 / 1024:.0f} MB "
                f"(cap {self.replay_options.max_dump_bytes / 1024 / 1024:.0f} MB)"
            )
            logger.warning(f"{reason}; running live to avoid exhausting runner memory")
            return None, reason, 0

        self._corpus_dir = Path(tempfile.mkdtemp(prefix=REPLAY_CORPUS_DIR_PREFIX))
        corpus_path = self._corpus_dir / REPLAY_CORPUS_FILENAME
        try:
            kept, dropped = build_replay_corpus(source, corpus_path)
        except Exception as exc:
            corpus_path.unlink(missing_ok=True)
            reason = f"could not read replay source {source}: {exc}"
            logger.warning(f"{reason}; recording only")
            return None, reason, 0

        if kept == 0:
            corpus_path.unlink(missing_ok=True)
            reason = f"replay source {source} holds no replayable flows"
            logger.warning(f"{reason}; recording only")
            return None, reason, dropped

        corpus_bytes = corpus_path.stat().st_size
        if corpus_bytes > self.replay_options.max_dump_bytes:
            corpus_path.unlink(missing_ok=True)
            reason = (
                f"replay corpus is {corpus_bytes / 1024 / 1024:.0f} MB "
                f"(cap {self.replay_options.max_dump_bytes / 1024 / 1024:.0f} MB)"
            )
            logger.warning(f"{reason}; running live to avoid exhausting runner memory")
            return None, reason, dropped

        logger.info(
            f"Replaying from {corpus_path}: kept {kept} flow(s), "
            f"dropped {dropped} as unreplayable"
        )
        return corpus_path, None, dropped

    def _start(self) -> MitmproxySession | None:
        """Start the mitmproxy subprocess.

        Returns:
            MitmproxySession with proxy info, or None if startup failed.
        """
        mitmdump_path = shutil.which("mitmdump")
        if not mitmdump_path:
            self.startup_failure_reason = "mitmdump was not found on PATH"
            logger.warning("mitmdump not found in PATH, HTTP metrics disabled")
            return None

        ca_cert_path = ensure_mitmproxy_ca_cert()

        self.output_dir.mkdir(parents=True, exist_ok=True)

        replay_source, replay_skipped_reason, unreplayable = (
            self._prepare_replay_corpus()
        )

        cmd = build_mitmdump_command(
            mitmdump_path,
            self.port,
            self.dump_file_path,
            replay_source,
            replay_reuse=self.replay_options.reuse,
            replay_extra=self.replay_options.extra,
            replay_ignore_params=self.replay_options.ignore_params,
            stream_large_bodies=self.stream_large_bodies,
        )

        logger.info(f"Starting mitmproxy on port {self.port}")
        try:
            # To a file, never to a pipe -- see `MITMDUMP_LOG_FILENAME`. It has
            # to outlive this scope, since mitmdump writes to it for the whole
            # run; `_stop` closes it once the process has exited.
            self._log_file = open(self.log_file_path, "wb")  # noqa: SIM115
            self._process = subprocess.Popen(
                cmd,
                stdout=self._log_file,
                stderr=subprocess.STDOUT,
            )

            # Wait for the listener, not for a fixed interval: with a corpus,
            # mitmdump binds the port only after loading it, which can take
            # tens of seconds.
            failure = wait_for_proxy_listener(
                self._process, self.port, log_path=self.log_file_path
            )
            if failure is not None:
                self.startup_failure_reason = failure
                logger.warning(f"Mitmproxy failed to start: {failure}")
                return None

            logger.info(f"Mitmproxy started on port {self.port}")
            return MitmproxySession(
                proxy_host="host.docker.internal",
                proxy_port=self.port,
                dump_file_path=self.dump_file_path,
                ca_cert_path=ca_cert_path,
                replay_source=replay_source,
                replay_skipped_reason=replay_skipped_reason,
                unreplayable_flow_count=unreplayable,
            )

        except FileNotFoundError:
            self.startup_failure_reason = "mitmdump could not be executed"
            logger.warning("mitmdump not found, HTTP metrics disabled")
            return None

    def _stop(self) -> None:
        """Stop the mitmproxy subprocess and discard the replay corpus."""
        if self._process is not None:
            logger.info("Stopping mitmproxy...")
            try:
                self._process.send_signal(signal.SIGINT)
                self._process.wait(timeout=MITMDUMP_SHUTDOWN_TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired:
                # Recorded, not just logged: the kill costs the dump its
                # unflushed tail, so the counts derived from it -- including the
                # replay acceptance criterion -- are a lower bound rather than
                # exact. See `MITMDUMP_SHUTDOWN_TIMEOUT_SECONDS`.
                self.metrics_incomplete_reason = (
                    f"mitmproxy did not shut down within "
                    f"{MITMDUMP_SHUTDOWN_TIMEOUT_SECONDS}s and was killed, so the "
                    "flows it had not flushed are missing from its dump"
                )
                logger.warning(f"{self.metrics_incomplete_reason}; killing...")
                _kill_if_running(self._process)

            self._process = None
            logger.info("Mitmproxy stopped")

        # After the process has exited, so nothing is still writing to it.
        if self._log_file is not None:
            self._log_file.close()
            self._log_file = None

        # Both rewrites need the file closed first, and truncation runs before
        # redaction so redaction only ever walks the bytes that are kept.
        truncate_log_to_tail(self.log_file_path)

        # Only this mode logs URLs at all -- see `MITMDUMP_LOG_FILENAME`.
        if self.replay_options.extra != DEFAULT_REPLAY_EXTRA:
            redact_log_urls(self.log_file_path)

        # Only after mitmdump has exited: it holds the corpus open for the run.
        if self._corpus_dir is not None:
            shutil.rmtree(self._corpus_dir, ignore_errors=True)
            self._corpus_dir = None


def parse_http_dump(
    dump_file_path: Path,
    replay_source: Path | None = None,
) -> HttpMetrics:
    """Parse a mitmproxy dump file and compute HTTP metrics.

    Reduces over the flow stream rather than materializing it: now that bodies
    are actually recorded (see `DEFAULT_STREAM_LARGE_BODIES`), a list of every
    flow costs roughly the dump's size in RAM. Memory here is O(unique URLs).

    mitmproxy marks a served-from-recording flow `is_replay == "response"` and
    serializes that marker into the dump, which is how a replayed request is
    told apart from one that went to the real API.

    Args:
        dump_file_path: Path to the .mitm dump file.
        replay_source: The corpus this run replayed from, recorded on the
            metrics so a reader can tell a replaying run from a live one.

    Returns:
        HttpMetrics with flow counts and URL information.
    """
    if not MITMPROXY_AVAILABLE:
        logger.warning("mitmproxy Python package not installed; HTTP metrics disabled")
        return HttpMetrics.empty()

    if not dump_file_path.exists():
        logger.warning(f"HTTP dump file not found: {dump_file_path}")
        return HttpMetrics.empty()

    flow_count = 0
    replayed_count = 0
    unique_urls: set[str] = set()
    # The per-URL replayed/live split the loop already has the marker for; still
    # O(unique URLs), the bound this function's memory test pins.
    live_url_counts: Counter[str] = Counter()

    with open(dump_file_path, "rb") as f:
        for flow in mitmproxy_io.FlowReader(f).stream():
            if not isinstance(flow, mitmproxy_http.HTTPFlow):
                continue
            flow_count += 1
            # Bound once: `Request.url` builds a new string on every access, so
            # reading it twice keeps two equal copies of every URL alive in the
            # structures below -- in the function whose point is memory discipline.
            url = flow.request.url
            # Deduplicated raw, redacted on the way out: two pages of the same
            # endpoint differ only in a query value, and merging them here would
            # count them as duplicate requests, i.e. as cache hits.
            unique_urls.add(url)
            if getattr(flow, "is_replay", None) == "response":
                replayed_count += 1
            else:
                live_url_counts[redact_url(url)] += 1

    duplicate_count = flow_count - len(unique_urls)

    # Cache hits are interpreted as duplicate requests to the same URL
    # (requests that could potentially be served from cache)
    cache_hits = duplicate_count

    return HttpMetrics(
        flow_count=flow_count,
        duplicate_flow_count=duplicate_count,
        unique_urls=sorted({redact_url(url) for url in unique_urls}),
        cache_hits_count=cache_hits,
        replayed_flow_count=replayed_count,
        live_flow_count=flow_count - replayed_count,
        replay_source=str(replay_source) if replay_source else None,
        live_url_counts=dict(live_url_counts),
    )


def compute_http_metrics_comparison(
    control_metrics: HttpMetrics,
    target_metrics: HttpMetrics,
) -> dict[str, dict[str, int | str] | int | str]:
    """Compute HTTP metrics comparison between control and target.

    This produces output in the same format as the legacy
    TestReport.get_http_metrics_per_command method.

    Args:
        control_metrics: HTTP metrics from control connector run.
        target_metrics: HTTP metrics from target connector run.

    Returns:
        Dictionary with control/target metrics and difference.
    """
    return {
        "control": {
            "flow_count": control_metrics.flow_count,
            "duplicate_flow_count": control_metrics.duplicate_flow_count,
            "cache_hits_count": control_metrics.cache_hits_count,
            "cache_hit_ratio": control_metrics.cache_hit_ratio,
        },
        "target": {
            "flow_count": target_metrics.flow_count,
            "duplicate_flow_count": target_metrics.duplicate_flow_count,
            "cache_hits_count": target_metrics.cache_hits_count,
            "cache_hit_ratio": target_metrics.cache_hit_ratio,
        },
        "difference": target_metrics.flow_count - control_metrics.flow_count,
    }


def get_http_flows_from_mitm_dump(
    mitm_dump_path: Path,
) -> list[mitmproxy_http.HTTPFlow]:  # type: ignore[name-defined]
    """Get HTTP flows from a mitmproxy dump file.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/utils.py#L129-L139

    Args:
        mitm_dump_path: Path to the mitmproxy dump file.

    Returns:
        List of HTTP flows from the dump file.
    """
    if not MITMPROXY_AVAILABLE:
        logger.warning("mitmproxy Python package not installed")
        return []

    if not mitm_dump_path.exists():
        logger.warning(f"Mitmproxy dump file not found: {mitm_dump_path}")
        return []

    with open(mitm_dump_path, "rb") as dump_file:
        return [
            f
            for f in mitmproxy_io.FlowReader(dump_file).stream()
            if isinstance(f, mitmproxy_http.HTTPFlow)
        ]


def mitm_http_stream_to_har(
    mitm_http_stream_path: Path,
    har_file_path: Path,
    max_source_bytes: int = MAX_IN_MEMORY_DUMP_BYTES,
) -> Path | None:
    """Convert a mitmproxy HTTP stream file to a HAR file.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/utils.py#L142-L154

    HAR (HTTP Archive) is a standard JSON format for recording HTTP transactions.
    This allows HTTP traffic captured by mitmproxy to be viewed in browser dev tools
    or other HAR viewers.

    Args:
        mitm_http_stream_path: Path to the mitmproxy HTTP stream file (.mitm).
        har_file_path: Path where the HAR file will be saved.
        max_source_bytes: Skip the export above this dump size. The export holds
            every flow *and* a base64 copy of every body in memory at once
            (~1.33x expansion), so it is the first thing to OOM a CI runner on
            exactly the runs whose dumps are already large.

    Returns:
        Path to the generated HAR file, or `None` when nothing was written --
        the source dump held no flows, or was larger than `max_source_bytes`.

    Raises:
        RuntimeError: If mitmproxy is not available.
    """
    if not MITMPROXY_AVAILABLE or SaveHar is None:
        raise RuntimeError(
            "mitmproxy Python package not installed; cannot convert to HAR"
        )

    if (
        mitm_http_stream_path.exists()
        and mitm_http_stream_path.stat().st_size > max_source_bytes
    ):
        logger.warning(
            f"Skipping HAR export of {mitm_http_stream_path}: "
            f"{mitm_http_stream_path.stat().st_size / 1024 / 1024:.0f} MB exceeds the "
            f"{max_source_bytes / 1024 / 1024:.0f} MB cap"
        )
        return None

    flows = get_http_flows_from_mitm_dump(mitm_http_stream_path)
    if not flows:
        logger.warning(f"No HTTP flows found in {mitm_http_stream_path}")
        return None

    har_file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        SaveHar().export_har(flows, str(har_file_path))
    except Exception as e:
        logger.error(f"Failed to export HAR file to {har_file_path}: {e}")
        raise

    if har_file_path.exists() and har_file_path.stat().st_size > 0:
        logger.info(f"Generated HAR file at {har_file_path}")
    else:
        logger.error(f"Failed to generate valid HAR file at {har_file_path}")
        raise RuntimeError(f"Failed to generate valid HAR file at {har_file_path}")

    return har_file_path
