"""Latency benchmark pass/fail contract."""

import ssl
import urllib.request
from pathlib import Path

from hooks.debug_hook_binary import (
    _frozen_startup_command,
    _print_results,
    _shim_command,
    _start_stub_server,
)


def test_stub_server_uses_trusted_https(tmp_path) -> None:
    server, thread, host, ca_bundle = _start_stub_server(
        tmp_path,
        response_delay_seconds=0,
    )
    try:
        context = ssl.create_default_context(cafile=str(ca_bundle))
        request = urllib.request.Request(host, method="HEAD")
        with urllib.request.urlopen(request, context=context, timeout=2) as response:
            assert response.status == 200
        assert host.startswith("https://")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_frozen_probe_uses_packaged_thin_dispatch() -> None:
    binary = Path(r"C:\Program Files\Runlayer\AIWatch\aiwatch.exe")

    assert _frozen_startup_command(binary) == [
        str(binary),
        "daemon",
        "--help",
    ]


def test_native_shim_uses_hook_dispatch_and_explicit_client() -> None:
    binary = Path(r"C:\Program Files\Runlayer\AIWatch\aiwatch-hook.exe")

    assert _shim_command(binary) == [
        str(binary),
        "hook",
        "--client",
        "claude_code",
    ]


def test_benchmark_only_requires_daemon_to_beat_both_inline_modes() -> None:
    assert _print_results(
        {
            "cold-inline": [100.0],
            "thin-inline": [110.0],
            "daemon-served": [50.0],
        }
    )


def test_benchmark_fails_when_daemon_beats_only_one_inline_mode() -> None:
    assert not _print_results(
        {
            "cold-inline": [100.0],
            "thin-inline": [40.0],
            "daemon-served": [50.0],
        }
    )


def test_benchmark_checks_p95_independently_from_p50() -> None:
    assert not _print_results(
        {
            "cold-inline": [100.0] * 20,
            "thin-inline": [110.0] * 20,
            "daemon-served": ([50.0] * 10) + ([150.0] * 10),
        }
    )


def test_benchmark_requires_shim_p50_to_beat_python_client() -> None:
    assert _print_results(
        {
            "cold-inline": [100.0],
            "thin-inline": [110.0],
            "daemon-served": [50.0],
            "daemon-via-shim": [5.0],
        }
    )
    assert not _print_results(
        {
            "cold-inline": [100.0],
            "thin-inline": [110.0],
            "daemon-served": [50.0],
            "daemon-via-shim": [60.0],
        }
    )
