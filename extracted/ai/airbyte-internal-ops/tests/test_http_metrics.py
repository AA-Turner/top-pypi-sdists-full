# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for mitmproxy-backed HTTP traffic capture."""

from __future__ import annotations

import gc
import io
import logging
import socket
import subprocess
import threading
import time
import weakref
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Iterator

import pytest

from airbyte_ops_mcp.regression_tests import http_metrics

if TYPE_CHECKING:
    from mitmproxy.http import HTTPFlow

# Per-test rather than a module-level `pytestmark`: mitmproxy is only installed
# with the `live-tests` group, and skipping the whole module hid the tests that
# need nothing from it -- the argv builder, the listener wait, the log tail, the
# startup and shutdown paths, URL redaction -- behind an optional dependency.
requires_mitmproxy = pytest.mark.skipif(
    not http_metrics.MITMPROXY_AVAILABLE,
    reason="this test reads or writes a mitmproxy dump",
)

if http_metrics.MITMPROXY_AVAILABLE:
    from mitmproxy import io as mitmproxy_io
    from mitmproxy.test import tflow
    from mitmproxy.utils import human


def _flow(url: str = "https://example.com/api/items?page=1") -> HTTPFlow:
    """A recorded flow with a request and a response body, as replay needs."""
    flow = tflow.tflow(resp=True)
    flow.request.url = url
    return flow


def _streamed_response_flow(url: str) -> HTTPFlow:
    """A flow whose response body was streamed away, chunked -- the silent case."""
    flow = _flow(url)
    assert flow.response is not None
    flow.response.headers["Transfer-Encoding"] = "chunked"
    flow.response.raw_content = None
    return flow


def _unanswered_flow(url: str) -> HTTPFlow:
    """A request that never got a response."""
    flow = tflow.tflow(resp=False)
    flow.request.url = url
    return flow


def _streamed_request_flow(url: str) -> HTTPFlow:
    """A flow whose *request* body was streamed away, so its match key collides."""
    flow = _flow(url)
    flow.request.raw_content = None
    return flow


def _write_dump(path: Path, flows: list[HTTPFlow]) -> Path:
    """Write `flows` to `path` in mitmproxy's dump format."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as dump_file:
        writer = mitmproxy_io.FlowWriter(dump_file)
        for flow in flows:
            writer.add(flow)
    return path


@requires_mitmproxy
def test_stream_large_bodies_default_is_a_real_size_threshold() -> None:
    """The recorded dump must actually contain bodies.

    `stream_large_bodies=1` parses as one *byte*, so mitmproxy streamed every
    body and stored none of them: the dumps recorded `content=None` throughout
    and nothing could ever be replayed from them.
    """
    threshold = human.parse_size(http_metrics.DEFAULT_STREAM_LARGE_BODIES)

    assert threshold is not None
    assert threshold >= 1024 * 1024, (
        f"stream_large_bodies={http_metrics.DEFAULT_STREAM_LARGE_BODIES!r} is "
        f"{threshold} bytes; anything this small streams every body away"
    )


@requires_mitmproxy
def test_parse_http_dump_counts_flows_and_duplicates(tmp_path: Path) -> None:
    dump = _write_dump(
        tmp_path / "http_traffic.mitm",
        [
            _flow("https://example.com/a"),
            _flow("https://example.com/a"),
            _flow("https://example.com/b"),
        ],
    )

    metrics = http_metrics.parse_http_dump(dump)

    assert metrics.flow_count == 3
    assert metrics.duplicate_flow_count == 1
    assert metrics.unique_urls == ["https://example.com/a", "https://example.com/b"]


@requires_mitmproxy
def test_parse_http_dump_tells_replayed_requests_from_live_ones(
    tmp_path: Path,
) -> None:
    """`live_flow_count` on a replaying target run is the acceptance criterion.

    mitmproxy marks a served-from-recording flow `is_replay == "response"` and
    serializes that marker, which is the only machine-readable evidence that
    the two connector versions saw the same upstream data.
    """
    replayed = _flow("https://example.com/a")
    replayed.is_replay = "response"
    also_replayed = _flow("https://example.com/b")
    also_replayed.is_replay = "response"
    dump = _write_dump(
        tmp_path / "http_traffic.mitm",
        [replayed, also_replayed, _flow("https://example.com/c")],
    )
    corpus = tmp_path / "http_replay_corpus.mitm"

    metrics = http_metrics.parse_http_dump(dump, corpus)

    assert metrics.flow_count == 3
    assert metrics.replayed_flow_count == 2
    assert metrics.live_flow_count == 1
    assert metrics.replay_hit_ratio == "66.67%"
    assert metrics.replay_source == str(corpus)


def test_redact_url_keeps_what_identifies_a_request_and_masks_the_rest() -> None:
    """A reported URL must not be able to carry a credential.

    The path is where a per-run job id lives and the parameter names are what
    make a clock-derived window recognisable, so both are kept; every value is
    masked, because `access_token`, `key` and `signature` are all real names in
    real connector query strings.
    """
    redacted = http_metrics.redact_url(
        "https://api.example.com/v1/report/9911?access_token=SUPERSECRET&since=2026-08-01"
    )

    assert redacted == (
        "https://api.example.com/v1/report/9911"
        "?access_token=[redacted]&since=[redacted]"
    )
    assert "SUPERSECRET" not in redacted
    assert "2026-08-01" not in redacted


def test_the_redaction_marker_survives_a_markdown_sanitizer() -> None:
    """The step summary is markdown, rendered through GitHub's HTML sanitizer.

    An angle-bracketed marker is a non-whitelisted *tag* there: it is removed
    rather than escaped, leaving `?access_token=` -- an empty parameter, which is
    a different claim from a masked one, and the parameter names are the whole
    diagnostic.
    """
    assert "<" not in http_metrics.REDACTED_VALUE
    assert ">" not in http_metrics.REDACTED_VALUE


def test_redact_url_leaves_a_url_with_nothing_to_mask_alone() -> None:
    assert (
        http_metrics.redact_url("https://api.example.com/v1/items")
        == "https://api.example.com/v1/items"
    )


def test_redact_url_masks_credentials_outside_the_query_string() -> None:
    """Basic-auth userinfo and a fragment are credential surfaces too."""
    assert http_metrics.redact_url("https://user:pw@api.example.com/v1/items") == (
        "https://redacted@api.example.com/v1/items"
    )
    assert http_metrics.redact_url("https://api.example.com/v1/items#token=abc") == (
        "https://api.example.com/v1/items"
    )


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("https://user:pw@api.example.com/v1/x?a=1", id="userinfo"),
        pytest.param("https://api.example.com/v1/x?a=1&b=2", id="query"),
        pytest.param("https://[::1]:8443/v1/x?a=1", id="ipv6-host"),
        pytest.param("https://api.example.com/v1/x#token=abc", id="fragment"),
    ],
)
def test_redacting_an_already_redacted_url_returns_it_unchanged(url: str) -> None:
    """Applied once at the seam, so a second call has to be harmless.

    Redacting where the counts are built is what lets everything downstream
    treat a URL as safe without tracing its provenance -- and that invites a
    consumer unsure whether a value has been through this to call it again.

    A bracketed marker in the userinfo used to make that raise: `[redacted]@host`
    is a bracketed *host* to `urlsplit`, which rejects it for not being an IP
    address. That failure was worse than it looks -- `redact_log_urls` catches
    `OSError` only, so it escaped out through `MitmproxyManager._stop` and left
    the log it was rewriting unmasked.
    """
    once = http_metrics.redact_url(url)

    assert http_metrics.redact_url(once) == once


def test_a_url_that_cannot_be_parsed_reports_nothing_rather_than_raising() -> None:
    """Unparseable must not mean unredacted, and must not mean no metrics either.

    This runs over every recorded URL in `parse_http_dump` and over every URL in
    the proxy's log during shutdown, so raising would cost a finished three-hour
    read its metrics, or leave `mitmdump.log` unmasked in the artifacts.
    """
    assert http_metrics.redact_url("https://[not-an-ip]@host/x?token=SUPERSECRET") == (
        http_metrics.REDACTED_VALUE
    )


def test_the_unparseable_url_log_line_carries_no_part_of_the_url(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """The one path that guarantees nothing escapes must not print it either.

    `urlsplit`'s `ValueError` is not always the message-free `Invalid IPv6 URL`:
    the NFKC and IP-address branches quote the netloc they rejected, which is the
    part that carries userinfo. Interpolating the exception would leak in a
    `--enable-debug-logs` run exactly what the return value masks.
    """
    url = "http://user:SUPERSECRET@ex\u2100mple.com/x"
    with caplog.at_level(logging.DEBUG, logger=http_metrics.logger.name):
        assert http_metrics.redact_url(url) == http_metrics.REDACTED_VALUE

    logged = caplog.text
    assert "SUPERSECRET" not in logged
    assert "ValueError" in logged


def test_redact_url_keeps_a_valueless_parameter_as_a_name() -> None:
    """Its name is the whole diagnostic; there is nothing to mask."""
    assert http_metrics.redact_url("https://api.example.com/v1/items?debug") == (
        "https://api.example.com/v1/items?debug"
    )


@requires_mitmproxy
def test_reported_live_urls_never_carry_query_parameter_values(
    tmp_path: Path,
) -> None:
    """These URLs reach surfaces the dumps are deliberately kept out of.

    `live_urls` renders into the step summary, the workflow log, the
    `regression_report` output and `report.html` -- all readable by every member
    of an internal org, on runs against real customer connections. Redacting on
    the way *in* is what makes reading the field directly safe as well.
    """
    dump = _write_dump(
        tmp_path / "http_traffic.mitm",
        [_flow("https://api.example.com/v1/report/9911?access_token=SUPERSECRET")],
    )

    metrics = http_metrics.parse_http_dump(dump, tmp_path / "corpus.mitm")

    assert "SUPERSECRET" not in str(metrics.live_url_counts)
    assert "SUPERSECRET" not in str(metrics.top_live_urls())
    assert "SUPERSECRET" not in str(metrics.unique_urls)
    assert metrics.top_live_urls() == [
        {
            "url": "https://api.example.com/v1/report/9911?access_token=[redacted]",
            "count": 1,
        }
    ]


@requires_mitmproxy
def test_two_pages_of_one_endpoint_are_not_counted_as_duplicate_requests(
    tmp_path: Path,
) -> None:
    """Redaction must not reach the duplicate count.

    Paging is a query value, so masking before deduplicating would make every
    paginated read look like it repeated one request -- and `cache_hits_count`
    is derived from that count.
    """
    dump = _write_dump(
        tmp_path / "http_traffic.mitm",
        [
            _flow("https://api.example.com/v1/items?page=1"),
            _flow("https://api.example.com/v1/items?page=2"),
        ],
    )

    metrics = http_metrics.parse_http_dump(dump)

    assert metrics.duplicate_flow_count == 0
    assert metrics.cache_hits_count == 0
    # Redacted on the way out, so the two pages read as one URL in the report --
    # which is the grouping a coverage shortfall wants.
    assert metrics.unique_urls == ["https://api.example.com/v1/items?page=[redacted]"]


@requires_mitmproxy
def test_parse_http_dump_records_which_urls_went_live(tmp_path: Path) -> None:
    """The aggregate live count cannot explain a coverage shortfall; these can.

    A replaying run's live requests are the ones the corpus could not answer, and
    the recorded dumps are deliberately excluded from the uploaded artifacts --
    so a URL that is not reported here is not recoverable after the run.
    """
    replayed = _flow("https://example.com/replayed")
    replayed.is_replay = "response"
    dump = _write_dump(
        tmp_path / "http_traffic.mitm",
        [
            replayed,
            _flow("https://example.com/report/1"),
            _flow("https://example.com/report/1"),
            _flow("https://example.com/other"),
        ],
    )

    metrics = http_metrics.parse_http_dump(dump, tmp_path / "corpus.mitm")

    assert metrics.live_url_counts == {
        "https://example.com/report/1": 2,
        "https://example.com/other": 1,
    }
    # Most-repeated first: a whole class of unmatched request leads, which is the
    # shape a low replay ratio usually has.
    assert metrics.top_live_urls() == [
        {"url": "https://example.com/report/1", "count": 2},
        {"url": "https://example.com/other", "count": 1},
    ]
    assert metrics.top_live_urls(limit=1) == [
        {"url": "https://example.com/report/1", "count": 2}
    ]


def test_replay_hit_ratio_is_not_a_number_without_traffic() -> None:
    assert http_metrics.HttpMetrics.empty().replay_hit_ratio == "N/A"


@requires_mitmproxy
def test_parse_http_dump_reports_a_recording_run_as_entirely_live(
    tmp_path: Path,
) -> None:
    dump = _write_dump(tmp_path / "http_traffic.mitm", [_flow(), _flow()])

    metrics = http_metrics.parse_http_dump(dump)

    assert (metrics.replayed_flow_count, metrics.live_flow_count) == (0, 2)
    assert metrics.replay_source is None


def test_parse_http_dump_returns_empty_metrics_for_a_missing_dump(
    tmp_path: Path,
) -> None:
    metrics = http_metrics.parse_http_dump(tmp_path / "absent.mitm")

    assert metrics == http_metrics.HttpMetrics.empty()


@requires_mitmproxy
def test_parse_http_dump_does_not_hold_the_whole_dump_in_memory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Memory must be O(unique URLs), not O(dump).

    Now that bodies are recorded, a list of every flow costs roughly the dump's
    size in RAM -- measured at +127 MB for a 100 MB dump, on a 7 GB CI runner
    that also hosts the connector container. The reader below fails as soon as
    the consumer keeps an already-yielded flow alive, which a list comprehension
    does for every single one.
    """
    flow_count = 25
    dump = _write_dump(
        tmp_path / "http_traffic.mitm",
        [_flow(f"https://example.com/{index}") for index in range(flow_count)],
    )
    peak_live = 0

    class LivenessCheckingReader:
        """A `FlowReader` that tracks how many yielded flows stay reachable."""

        def __init__(self, fileobj: object) -> None:
            self._inner = mitmproxy_io.FlowReader(fileobj)

        def stream(self) -> Iterator[object]:
            nonlocal peak_live
            refs: list[weakref.ref] = []
            for flow in self._inner.stream():
                refs.append(weakref.ref(flow))
                yield flow
                # Drop this generator's own reference before counting, so the
                # only ones left are the consumer's.
                del flow
                gc.collect()
                peak_live = max(peak_live, sum(1 for ref in refs if ref() is not None))

    monkeypatch.setattr(
        http_metrics,
        "mitmproxy_io",
        SimpleNamespace(FlowReader=LivenessCheckingReader),
    )

    metrics = http_metrics.parse_http_dump(dump)

    assert metrics.flow_count == flow_count
    # One: the flow the consumer's loop variable still names while it asks for
    # the next one. Two would already mean something is accumulating.
    assert peak_live <= 1, (
        f"{peak_live} recorded flows were reachable at once; parse_http_dump "
        "must reduce over the stream rather than materialize it"
    )


@requires_mitmproxy
def test_mitm_http_stream_to_har_exports_a_small_dump(tmp_path: Path) -> None:
    dump = _write_dump(tmp_path / "http_traffic.mitm", [_flow()])

    har = http_metrics.mitm_http_stream_to_har(dump, tmp_path / "traffic.har")

    assert har is not None
    assert har.exists()
    assert har.stat().st_size > 0


@requires_mitmproxy
def test_mitm_http_stream_to_har_reports_a_dump_with_no_flows(tmp_path: Path) -> None:
    empty = tmp_path / "http_traffic.mitm"
    empty.touch()

    assert http_metrics.mitm_http_stream_to_har(empty, tmp_path / "traffic.har") is None


@requires_mitmproxy
def test_mitm_http_stream_to_har_skips_an_oversized_dump(tmp_path: Path) -> None:
    """The HAR export materializes every body base64-encoded; cap it by size.

    A skip returns `None` rather than a path to a file that was never written,
    so a caller cannot mistake it for a successful export.
    """
    dump = _write_dump(tmp_path / "http_traffic.mitm", [_flow()])
    har_path = tmp_path / "traffic.har"

    result = http_metrics.mitm_http_stream_to_har(dump, har_path, max_source_bytes=1)

    assert result is None
    assert not har_path.exists()


def test_build_mitmdump_command_records_without_replay_flags(tmp_path: Path) -> None:
    cmd = http_metrics.build_mitmdump_command(
        "/usr/bin/mitmdump", 8080, tmp_path / "http_traffic.mitm"
    )

    assert "--server-replay" not in cmd
    assert not [arg for arg in cmd if arg.startswith("server_replay")]
    assert "--save-stream-file" in cmd
    assert str(tmp_path / "http_traffic.mitm") in cmd


def test_build_mitmdump_command_never_streams_every_body_away(tmp_path: Path) -> None:
    """`stream_large_bodies=1` means one byte, and a streamed body is not stored."""
    cmd = http_metrics.build_mitmdump_command(
        "/usr/bin/mitmdump", 8080, tmp_path / "http_traffic.mitm"
    )

    assert "stream_large_bodies=1" not in cmd
    thresholds = [
        arg.split("=", 1)[1] for arg in cmd if arg.startswith("stream_large_bodies=")
    ]
    assert thresholds == [http_metrics.DEFAULT_STREAM_LARGE_BODIES]


def test_build_mitmdump_command_replays_and_still_records(tmp_path: Path) -> None:
    """A replaying run records too: its own dump is how replay is measured."""
    corpus = tmp_path / "http_replay_corpus.mitm"
    dump = tmp_path / "http_traffic.mitm"

    cmd = http_metrics.build_mitmdump_command(
        "/usr/bin/mitmdump", 8080, dump, corpus, replay_ignore_params=("nonce", "ts")
    )

    assert cmd[cmd.index("--server-replay") + 1] == str(corpus)
    assert cmd[cmd.index("--save-stream-file") + 1] == str(dump)
    settings = [cmd[i + 1] for i, arg in enumerate(cmd) if arg == "--set"]
    # Pop-on-match preserves recorded ordering; forward keeps an unmatched
    # request going live rather than truncating the run.
    assert "server_replay_reuse=false" in settings
    assert "server_replay_extra=forward" in settings
    # A sequence option takes one `--set` per value.
    assert "server_replay_ignore_params=nonce" in settings
    assert "server_replay_ignore_params=ts" in settings


def test_build_mitmdump_command_honours_replay_overrides(tmp_path: Path) -> None:
    cmd = http_metrics.build_mitmdump_command(
        "/usr/bin/mitmdump",
        8080,
        tmp_path / "http_traffic.mitm",
        tmp_path / "corpus.mitm",
        replay_reuse=True,
        replay_extra="kill",
    )

    settings = [cmd[i + 1] for i, arg in enumerate(cmd) if arg == "--set"]
    assert "server_replay_reuse=true" in settings
    assert "server_replay_extra=kill" in settings


@requires_mitmproxy
def test_build_replay_corpus_drops_flows_that_cannot_be_replayed(
    tmp_path: Path,
) -> None:
    """The correctness invariant of HTTP replay.

    mitmproxy's server-replay addon serves a recorded flow whose body was
    streamed away as an empty 200 -- with no error at all when the response was
    chunked, which is exactly the encoding large responses use. The connector
    reads a well-formed empty page, treats it as the end of pagination, and the
    run "succeeds" with fewer records. A request whose body was streamed is the
    quieter half: its match key hashes to the literal `"None"`, so two unrelated
    requests collide and serve each other's responses.

    Every one of those must be dropped here, so the request goes live and comes
    back with real data instead.
    """
    source = _write_dump(
        tmp_path / "http_traffic.mitm",
        [
            _flow("https://example.com/replayable"),
            _streamed_response_flow("https://example.com/chunked-empty"),
            _unanswered_flow("https://example.com/no-response"),
            _streamed_request_flow("https://example.com/streamed-request"),
        ],
    )
    corpus = tmp_path / "http_replay_corpus.mitm"

    kept, dropped = http_metrics.build_replay_corpus(source, corpus)

    assert (kept, dropped) == (1, 3)
    with corpus.open("rb") as corpus_file:
        survivors = list(mitmproxy_io.FlowReader(corpus_file).stream())
    assert [flow.request.url for flow in survivors] == [
        "https://example.com/replayable"
    ]
    assert survivors[0].response is not None
    assert survivors[0].response.raw_content == b"message"


@requires_mitmproxy
def test_build_replay_corpus_keeps_a_fully_recorded_dump_intact(
    tmp_path: Path,
) -> None:
    """The filter must not cost replay coverage on a well-recorded dump."""
    source = _write_dump(
        tmp_path / "http_traffic.mitm",
        [_flow(f"https://example.com/{index}") for index in range(5)],
    )

    kept, dropped = http_metrics.build_replay_corpus(
        source, tmp_path / "http_replay_corpus.mitm"
    )

    assert (kept, dropped) == (5, 0)


@pytest.fixture
def fake_mitmdump(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    """Let `MitmproxyManager` "start" without spawning a proxy; capture the argv."""
    started: list[list[str]] = []

    class FakeProcess:
        stderr = None

        def poll(self) -> None:
            return None

        def send_signal(self, _signal: int) -> None:
            return None

        def wait(self, timeout: float | None = None) -> int:
            return 0

    def fake_popen(cmd: list[str], **_kwargs: object) -> FakeProcess:
        started.append(cmd)
        return FakeProcess()

    monkeypatch.setattr(http_metrics.shutil, "which", lambda _name: "/usr/bin/mitmdump")
    monkeypatch.setattr(http_metrics, "ensure_mitmproxy_ca_cert", lambda: None)
    monkeypatch.setattr(http_metrics.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(http_metrics.subprocess, "Popen", fake_popen)
    # A fake process listens on nothing; startup waits on the port for real.
    monkeypatch.setattr(
        http_metrics, "wait_for_proxy_listener", lambda *_args, **_kwargs: None
    )
    return started


@requires_mitmproxy
def test_replay_source_is_the_filtered_corpus_never_the_raw_dump(
    tmp_path: Path, fake_mitmdump: list[list[str]]
) -> None:
    source = _write_dump(
        tmp_path / "control" / "http_traffic.mitm",
        [_flow("https://example.com/ok"), _streamed_response_flow("https://x/big")],
    )

    output_dir = tmp_path / "target"

    with http_metrics.MitmproxyManager.start(output_dir, replay_from=source) as session:
        assert session is not None
        assert session.replay_source is not None
        assert session.replay_source.name == http_metrics.REPLAY_CORPUS_FILENAME
        assert session.replay_source.exists()
        assert session.replay_skipped_reason is None
        assert session.unreplayable_flow_count == 1
        assert fake_mitmdump[0][fake_mitmdump[0].index("--server-replay") + 1] == str(
            session.replay_source
        )
        corpus = session.replay_source

    # The corpus is a near-full copy of the control dump. Leaving it in the
    # output directory would upload a third copy of the recorded response
    # bodies -- control dump, corpus, target dump -- as a workflow artifact.
    assert output_dir not in corpus.parents
    assert not corpus.exists()


@pytest.mark.parametrize("write_empty_file", [False, True], ids=["missing", "empty"])
def test_missing_or_empty_replay_source_falls_back_to_recording(
    tmp_path: Path, fake_mitmdump: list[list[str]], write_empty_file: bool
) -> None:
    source = tmp_path / "control" / "http_traffic.mitm"
    if write_empty_file:
        source.parent.mkdir(parents=True)
        source.touch()

    with http_metrics.MitmproxyManager.start(
        tmp_path / "target", replay_from=source
    ) as session:
        assert session is not None
        assert session.replay_source is None
        assert session.replay_skipped_reason is not None
        assert "--server-replay" not in fake_mitmdump[0]


@requires_mitmproxy
def test_a_dump_with_nothing_replayable_falls_back_to_recording(
    tmp_path: Path, fake_mitmdump: list[list[str]]
) -> None:
    source = _write_dump(
        tmp_path / "control" / "http_traffic.mitm",
        [_streamed_response_flow("https://example.com/big")],
    )

    with http_metrics.MitmproxyManager.start(
        tmp_path / "target", replay_from=source
    ) as session:
        assert session is not None
        assert session.replay_source is None
        assert session.replay_skipped_reason is not None
        assert session.unreplayable_flow_count == 1
        assert "--server-replay" not in fake_mitmdump[0]


@pytest.mark.parametrize(
    "cap_delta,expect_replay",
    [
        pytest.param(0, True, id="at-the-cap"),
        pytest.param(-1, False, id="over-the-cap"),
    ],
)
@requires_mitmproxy
def test_an_oversized_corpus_degrades_to_a_live_run(
    tmp_path: Path,
    fake_mitmdump: list[list[str]],
    cap_delta: int,
    expect_replay: bool,
) -> None:
    """mitmdump loads the whole corpus into RAM; a live target beats an OOM.

    The cap has to be measured on the *filtered* corpus, since that is the file
    mitmdump actually loads.
    """
    source = _write_dump(
        tmp_path / "control" / "http_traffic.mitm",
        [_flow(f"https://example.com/{index}") for index in range(4)],
    )
    sized_corpus = tmp_path / "sizing" / "corpus.mitm"
    http_metrics.build_replay_corpus(source, sized_corpus)
    corpus_bytes = sized_corpus.stat().st_size

    with http_metrics.MitmproxyManager.start(
        tmp_path / "target",
        replay_from=source,
        replay_options=http_metrics.ReplayOptions(
            max_dump_bytes=corpus_bytes + cap_delta
        ),
    ) as session:
        assert session is not None
        assert (session.replay_source is not None) is expect_replay
        assert (session.replay_skipped_reason is None) is expect_replay
        assert ("--server-replay" in fake_mitmdump[0]) is expect_replay


@requires_mitmproxy
def test_an_oversized_source_is_never_copied_before_it_is_rejected(
    tmp_path: Path, fake_mitmdump: list[list[str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The cap has to be checked before the copy, not only after it.

    Filtering can only shrink a dump, so a source already over the cap is going
    to be rejected -- writing the full filtered copy first costs a transient
    second copy of a multi-gigabyte file on a runner that has ~14 GB shared with
    the connector's own output.
    """
    source = _write_dump(
        tmp_path / "control" / "http_traffic.mitm",
        [_flow(f"https://example.com/{index}") for index in range(4)],
    )

    def _must_not_copy(*_args: object, **_kwargs: object) -> tuple[int, int]:
        raise AssertionError("the corpus was written before the cap was applied")

    monkeypatch.setattr(http_metrics, "build_replay_corpus", _must_not_copy)

    with http_metrics.MitmproxyManager.start(
        tmp_path / "target",
        replay_from=source,
        replay_options=http_metrics.ReplayOptions(
            max_dump_bytes=source.stat().st_size - 1
        ),
    ) as session:
        assert session is not None
        assert session.replay_source is None
        assert session.replay_skipped_reason is not None
        assert "replay source is" in session.replay_skipped_reason
        assert "--server-replay" not in fake_mitmdump[0]


class _LiveProcess:
    """A process that has not exited, with nothing to read on stderr."""

    stderr = None

    def poll(self) -> None:
        return None


def test_startup_waits_for_the_listen_port_not_a_fixed_interval() -> None:
    """mitmdump binds the port only after `ServerPlayback` loads the corpus.

    Measured against mitmdump 11.1.3, a 256 MB corpus of small flows takes ~23 s
    to that point. Returning after a fixed second -- with only `poll()` as the
    check -- starts the connector against a connection-refused proxy, which
    reads as a regression in the version under test.
    """
    port = http_metrics.find_free_port()
    listener: list[socket.socket] = []

    def _bind_later() -> None:
        time.sleep(0.3)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", port))
        server.listen(1)
        listener.append(server)

    binder = threading.Thread(target=_bind_later)
    binder.start()
    try:
        started = time.monotonic()
        failure = http_metrics.wait_for_proxy_listener(
            _LiveProcess(),  # type: ignore[arg-type]
            port,
            timeout=30,
        )
        waited = time.monotonic() - started
    finally:
        binder.join()
        for server in listener:
            server.close()

    assert failure is None
    assert waited >= 0.3


def test_a_port_that_never_opens_is_a_startup_failure() -> None:
    port = http_metrics.find_free_port()

    failure = http_metrics.wait_for_proxy_listener(
        _LiveProcess(),  # type: ignore[arg-type]
        port,
        timeout=0.3,
    )

    assert failure is not None
    assert str(port) in failure


def test_a_proxy_that_exits_during_startup_reports_why(tmp_path: Path) -> None:
    """The reason comes from the log file, since nothing is piped any more."""

    class ExitedProcess:
        def poll(self) -> int:
            return 1

    log_path = tmp_path / http_metrics.MITMDUMP_LOG_FILENAME
    log_path.write_bytes(b"Address already in use")

    failure = http_metrics.wait_for_proxy_listener(
        ExitedProcess(),  # type: ignore[arg-type]
        http_metrics.find_free_port(),
        timeout=30,
        log_path=log_path,
    )

    assert failure is not None
    assert "Address already in use" in failure


def test_a_startup_failure_with_no_log_still_reports_a_reason(tmp_path: Path) -> None:
    """An empty or absent log must not produce a blank reason."""

    class ExitedProcess:
        def poll(self) -> int:
            return 1

    failure = http_metrics.wait_for_proxy_listener(
        ExitedProcess(),  # type: ignore[arg-type]
        http_metrics.find_free_port(),
        timeout=30,
        log_path=tmp_path / "never-written.log",
    )

    assert failure == "mitmproxy exited during startup: no log output"


def test_only_the_tail_of_a_long_log_is_read(tmp_path: Path) -> None:
    """The log is unbounded; the reason a proxy exited is at its end."""
    log_path = tmp_path / http_metrics.MITMDUMP_LOG_FILENAME
    log_path.write_bytes(
        b"x" * (http_metrics.MITMDUMP_LOG_TAIL_BYTES * 4) + b"Address already in use"
    )

    tail = http_metrics.read_log_tail(log_path)

    assert tail.endswith("Address already in use")
    assert len(tail) <= http_metrics.MITMDUMP_LOG_TAIL_BYTES


def test_a_log_over_the_cap_keeps_its_tail_and_says_what_it_dropped(
    tmp_path: Path,
) -> None:
    """The log is the one unbounded thing this feature uploads.

    The dump next to it is discarded above a cap; the log had nothing pruning it,
    and it grows ~226 B per connection cycle. Truncated from the front because
    what a proxy log is read for -- why it exited, what it killed last -- is at
    its end, and it has to say so in the file so a truncated log cannot be read
    as the whole run.
    """
    log_path = tmp_path / http_metrics.MITMDUMP_LOG_FILENAME
    log_path.write_bytes(b"early line\n" * 4000 + b"server connect last:443\n")

    http_metrics.truncate_log_to_tail(log_path, max_bytes=1024)

    kept = log_path.read_bytes()
    assert len(kept) <= 1024 + 64  # The marker line is added, not counted.
    assert kept.startswith(b"[")
    assert b"truncated]" in kept.splitlines()[0]
    assert kept.endswith(b"server connect last:443\n")
    # Whole lines only, so the log still parses line by line.
    assert b"early line\n" in kept


def test_a_log_under_the_cap_is_left_exactly_as_it_is(tmp_path: Path) -> None:
    """The happy path must not grow a marker or rewrite the file."""
    log_path = tmp_path / http_metrics.MITMDUMP_LOG_FILENAME
    log_path.write_bytes(b"client connect\n")

    http_metrics.truncate_log_to_tail(log_path, max_bytes=1024)

    assert log_path.read_bytes() == b"client connect\n"


def test_a_log_that_cannot_be_truncated_is_kept_rather_than_lost(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Unlike redaction, failing here is not a disclosure -- only a big file.

    So the fallback is the opposite one: keep the log, say the size it stayed at.
    """
    log_path = tmp_path / http_metrics.MITMDUMP_LOG_FILENAME
    log_path.write_bytes(b"line\n" * 500)

    def _fail(*_args: object, **_kwargs: object) -> None:
        raise OSError("no space left on device")

    monkeypatch.setattr(http_metrics, "open", _fail, raising=False)

    http_metrics.truncate_log_to_tail(log_path, max_bytes=10)

    assert log_path.read_bytes() == b"line\n" * 500


def test_the_log_is_truncated_before_it_is_redacted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Redaction walks the log line by line, so it should only walk what is kept.

    Asserted as an order rather than a count: reversing them still produces a
    correct file, which is why the order is easy to lose in a refactor.
    """
    events: list[str] = []
    monkeypatch.setattr(
        http_metrics,
        "truncate_log_to_tail",
        lambda *_args, **_kwargs: events.append("truncated"),
    )
    monkeypatch.setattr(
        http_metrics, "redact_log_urls", lambda *_args: events.append("redacted")
    )

    class FakeProcess:
        def poll(self) -> None:
            return None

        def send_signal(self, _signal: int) -> None:
            return None

        def wait(self, timeout: float | None = None) -> int:
            return 0

    monkeypatch.setattr(http_metrics.shutil, "which", lambda _name: "/usr/bin/mitmdump")
    monkeypatch.setattr(http_metrics, "ensure_mitmproxy_ca_cert", lambda: None)
    monkeypatch.setattr(
        http_metrics.subprocess, "Popen", lambda *_args, **_kwargs: FakeProcess()
    )
    monkeypatch.setattr(
        http_metrics, "wait_for_proxy_listener", lambda *_args, **_kwargs: None
    )

    manager = http_metrics.MitmproxyManager(
        tmp_path / "target",
        replay_options=http_metrics.ReplayOptions(extra="kill"),
    )
    with manager.running() as session:
        assert session is not None

    assert events == ["truncated", "redacted"]


def test_a_failure_inside_start_still_stops_what_it_started(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`start()` promises cleanup "even if an exception occurs".

    Startup is the part most likely to fail, and it is the part that spawns the
    proxy and writes the replay corpus -- so it has to run inside the `try`, or
    a failure there leaks both.
    """
    stopped: list[bool] = []
    monkeypatch.setattr(
        http_metrics.MitmproxyManager,
        "_start",
        lambda _self: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    monkeypatch.setattr(
        http_metrics.MitmproxyManager,
        "_stop",
        lambda _self: stopped.append(True),
    )

    def _run_under_the_context_manager() -> None:
        with http_metrics.MitmproxyManager.start(tmp_path / "target"):
            pass

    with pytest.raises(RuntimeError, match="boom"):
        _run_under_the_context_manager()

    assert stopped == [True]


def test_a_bootstrap_proxy_that_ignores_terminate_is_killed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Otherwise it keeps holding a listen port for the rest of the session."""
    killed: list[bool] = []

    class StubbornProcess:
        pid = 4242
        returncode = None

        def poll(self) -> int | None:
            return None if not killed else 0

        def terminate(self) -> None:
            return None

        def wait(self, timeout: float | None = None) -> int:
            if not killed:
                raise subprocess.TimeoutExpired("mitmdump", timeout or 0)
            return 0

        def kill(self) -> None:
            killed.append(True)

    monkeypatch.setattr(http_metrics, "MITMPROXY_DIR", tmp_path)
    monkeypatch.setattr(http_metrics.shutil, "which", lambda _name: "/usr/bin/mitmdump")
    monkeypatch.setattr(http_metrics.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(
        http_metrics.subprocess, "Popen", lambda *_args, **_kwargs: StubbornProcess()
    )

    assert http_metrics.ensure_mitmproxy_ca_cert() is None
    assert killed == [True]


def test_mitmdump_logs_to_a_file_and_is_never_given_a_pipe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A pipe nothing drains stalls the proxy partway through a run.

    `--flow-detail 0` silences flow summaries but not the log, which emits ~205 B
    of connection events per connection cycle. Nothing here reads that pipe, so
    mitmdump blocks in `write()` once the ~64 KB buffer fills -- measured at ~330
    connection cycles -- and every connector request after that hangs, which
    reads as a regression in the version under test.
    """
    captured: dict[str, object] = {}

    class FakeProcess:
        def poll(self) -> None:
            return None

        def send_signal(self, _signal: int) -> None:
            return None

        def wait(self, timeout: float | None = None) -> int:
            return 0

    def fake_popen(cmd: list[str], **kwargs: object) -> FakeProcess:
        captured.update(kwargs)
        return FakeProcess()

    monkeypatch.setattr(http_metrics.shutil, "which", lambda _name: "/usr/bin/mitmdump")
    monkeypatch.setattr(http_metrics, "ensure_mitmproxy_ca_cert", lambda: None)
    monkeypatch.setattr(http_metrics.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(
        http_metrics, "wait_for_proxy_listener", lambda *_args, **_kwargs: None
    )

    output_dir = tmp_path / "target"
    manager = http_metrics.MitmproxyManager(output_dir)
    with manager.running() as session:
        assert session is not None
        assert captured["stdout"] is not subprocess.PIPE
        assert captured["stderr"] == subprocess.STDOUT
        log_file = captured["stdout"]
        assert isinstance(log_file, io.IOBase)
        assert Path(log_file.name) == output_dir / http_metrics.MITMDUMP_LOG_FILENAME

    # The handle is closed with the process, not left open for the session.
    assert log_file.closed


def test_the_log_is_redacted_when_mitmproxy_logs_the_urls_it_killed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`mitmdump.log` is uploaded, and strict replay puts full URLs in it.

    `ServerPlayback` logs the URL of every request it kills at warning level,
    unbounded -- and `--strict-replay` is exactly the mode reached for when
    coverage is poor, i.e. when there are many of them. The log is deliberately
    not excluded from the artifact upload, so the URLs have to be masked instead.
    """
    log_lines = (
        b"server_playback: killed non-replay request "
        b"https://api.example.com/v1/report/9911?access_token=SUPERSECRET\n"
        b"[13:37:00.000] client connect\n"
    )

    class FakeProcess:
        def poll(self) -> None:
            return None

        def send_signal(self, _signal: int) -> None:
            return None

        def wait(self, timeout: float | None = None) -> int:
            return 0

    monkeypatch.setattr(http_metrics.shutil, "which", lambda _name: "/usr/bin/mitmdump")
    monkeypatch.setattr(http_metrics, "ensure_mitmproxy_ca_cert", lambda: None)
    monkeypatch.setattr(
        http_metrics.subprocess, "Popen", lambda *_args, **_kwargs: FakeProcess()
    )
    monkeypatch.setattr(
        http_metrics, "wait_for_proxy_listener", lambda *_args, **_kwargs: None
    )

    manager = http_metrics.MitmproxyManager(
        tmp_path / "target",
        replay_options=http_metrics.ReplayOptions(extra="kill"),
    )
    with manager.running() as session:
        assert session is not None
        # mitmdump is fake here, so stand in for what it would have written.
        manager.log_file_path.write_bytes(log_lines)

    written = manager.log_file_path.read_bytes()
    assert b"SUPERSECRET" not in written
    assert b"access_token=[redacted]" in written
    # Only the URLs: the rest of the log is what a startup failure is read from.
    assert b"client connect" in written


def test_the_log_is_left_alone_when_nothing_logs_a_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """At `--flow-detail 0` with the default `forward`, the log holds no URLs.

    Rewriting it anyway would mean reading an unbounded file on every run for
    nothing.
    """
    redacted: list[Path] = []
    monkeypatch.setattr(
        http_metrics, "redact_log_urls", lambda path: redacted.append(path)
    )

    class FakeProcess:
        def poll(self) -> None:
            return None

        def send_signal(self, _signal: int) -> None:
            return None

        def wait(self, timeout: float | None = None) -> int:
            return 0

    monkeypatch.setattr(http_metrics.shutil, "which", lambda _name: "/usr/bin/mitmdump")
    monkeypatch.setattr(http_metrics, "ensure_mitmproxy_ca_cert", lambda: None)
    monkeypatch.setattr(
        http_metrics.subprocess, "Popen", lambda *_args, **_kwargs: FakeProcess()
    )
    monkeypatch.setattr(
        http_metrics, "wait_for_proxy_listener", lambda *_args, **_kwargs: None
    )

    manager = http_metrics.MitmproxyManager(tmp_path / "target")
    with manager.running() as session:
        assert session is not None

    assert redacted == []


def test_a_log_that_cannot_be_redacted_is_discarded_rather_than_published(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Failing to mask must not fall back to publishing the raw log."""
    log_path = tmp_path / http_metrics.MITMDUMP_LOG_FILENAME
    log_path.write_bytes(b"killed non-replay request https://x/y?token=SUPERSECRET\n")

    def _fail(*_args: object, **_kwargs: object) -> None:
        raise OSError("no space left on device")

    monkeypatch.setattr(http_metrics, "open", _fail, raising=False)

    http_metrics.redact_log_urls(log_path)

    assert not log_path.exists()


def test_a_shutdown_that_has_to_be_killed_is_recorded_not_only_logged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A `SIGKILL` costs the dump the flows mitmproxy had not flushed.

    The `save` addon flushes, appends its in-flight flows and closes the file
    only in `done()`, which a kill never reaches -- and the loss only ever lowers
    `live_flow_count`, i.e. flatters the replay acceptance criterion. So the run
    has to carry the fact, not just a log line.
    """
    killed: list[bool] = []

    class StubbornProcess:
        pid = 5150

        def poll(self) -> int | None:
            return 0 if killed else None

        def send_signal(self, _signal: int) -> None:
            return None

        def wait(self, timeout: float | None = None) -> int:
            if not killed:
                raise subprocess.TimeoutExpired("mitmdump", timeout or 0)
            return 0

        def kill(self) -> None:
            killed.append(True)

    monkeypatch.setattr(http_metrics.shutil, "which", lambda _name: "/usr/bin/mitmdump")
    monkeypatch.setattr(http_metrics, "ensure_mitmproxy_ca_cert", lambda: None)
    monkeypatch.setattr(
        http_metrics.subprocess, "Popen", lambda *_args, **_kwargs: StubbornProcess()
    )
    monkeypatch.setattr(
        http_metrics, "wait_for_proxy_listener", lambda *_args, **_kwargs: None
    )

    manager = http_metrics.MitmproxyManager(tmp_path / "target")
    with manager.running() as session:
        assert session is not None
        assert manager.metrics_incomplete_reason is None

    assert killed == [True]
    assert manager.metrics_incomplete_reason is not None
    assert "was killed" in manager.metrics_incomplete_reason


def test_shutdown_gets_more_than_the_measured_time_to_flush_the_corpus_cap() -> None:
    """Graceful shutdown at the 256 MB cap measured ~4.1 s against a 5 s budget.

    A slower CI runner crossing that budget turns every run near the cap into a
    silently shortened dump, so the shutdown wait is its own, generous constant
    rather than the process-kill timeout.
    """
    assert (
        http_metrics.MITMDUMP_SHUTDOWN_TIMEOUT_SECONDS
        > http_metrics.PROCESS_KILL_TIMEOUT_SECONDS
    )
    assert http_metrics.MITMDUMP_SHUTDOWN_TIMEOUT_SECONDS >= 30


def test_startup_failures_keep_their_reason_on_the_manager(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`None` session plus a fixed string tells a reader to install mitmproxy.

    The two failures the listener wait exists to detect -- a proxy that died on
    startup, a corpus slower to load than the ceiling -- point at a code fix, so
    the caller has to be able to tell them apart from a missing binary.
    """
    monkeypatch.setattr(http_metrics.shutil, "which", lambda _name: None)

    manager = http_metrics.MitmproxyManager(tmp_path / "target")
    with manager.running() as session:
        assert session is None

    assert manager.startup_failure_reason == "mitmdump was not found on PATH"

    class FakeProcess:
        def poll(self) -> None:
            return None

        def send_signal(self, _signal: int) -> None:
            return None

        def wait(self, timeout: float | None = None) -> int:
            return 0

    monkeypatch.setattr(http_metrics.shutil, "which", lambda _name: "/usr/bin/mitmdump")
    monkeypatch.setattr(http_metrics, "ensure_mitmproxy_ca_cert", lambda: None)
    monkeypatch.setattr(
        http_metrics.subprocess, "Popen", lambda *_args, **_kwargs: FakeProcess()
    )
    monkeypatch.setattr(
        http_metrics,
        "wait_for_proxy_listener",
        lambda *_args, **_kwargs: "mitmproxy exited during startup: boom",
    )

    slow = http_metrics.MitmproxyManager(tmp_path / "slow")
    with slow.running() as session:
        assert session is None

    assert slow.startup_failure_reason == "mitmproxy exited during startup: boom"


def test_discard_oversized_dump_keeps_what_fits(tmp_path: Path) -> None:
    dump = tmp_path / "http_traffic.mitm"
    dump.write_bytes(b"x" * 1024)

    assert http_metrics.discard_oversized_dump(dump, max_bytes=10 * 1024 * 1024) is None
    assert dump.exists()


def test_discard_oversized_dump_drops_what_cannot_be_uploaded(tmp_path: Path) -> None:
    """Recording bodies makes the dump grow with everything the run downloads.

    Nothing bounds it while mitmproxy is writing, so the least a run can do is
    not leave a multi-gigabyte file behind for the artifact upload.
    """
    dump = tmp_path / "http_traffic.mitm"
    dump.write_bytes(b"x" * 1024)
    size = dump.stat().st_size

    discarded = http_metrics.discard_oversized_dump(dump, max_bytes=size - 1)

    assert discarded == size
    assert not dump.exists()
