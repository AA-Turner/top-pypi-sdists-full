"""Measure AI Watch hook subprocess latency across daemon rollout stages.

Each sample launches a fresh Python process and measures wall time around the
whole process. A local HTTPS/1.1 stub with configurable response delay keeps
backend work constant while exercising TLS. The daemon sample keeps one daemon
and its HTTP connection pool warm across hook events.

Usage::

    cd cli
    uv run python hooks/debug_hook_binary.py \
      --iterations 30 --warmups 3 --stub-delay-ms 40 \
      --shim-binary ../aiwatch-hook-shim/bin/aiwatch-hook

Historical reference (2026-08-05, unfrozen dev venv and plaintext loopback,
30 samples; direction only, not shipped-artifact latency):

    cold inline       p50 385.0 ms | p95 412.5 ms
    thin inline       p50 379.1 ms | p95 400.7 ms
    daemon-served     p50  82.3 ms | p95  89.2 ms

Observed ordering: daemon-served < thin inline < cold inline.

When a native shim is supplied or auto-detected, the benchmark also compares
daemon-via-shim against daemon-via-Python-client and requires the shim p50 to
be lower. Build it with the same version as ``cli/pyproject.toml`` so the live
daemon accepts it instead of returning ``restarting``.

At 30 samples, nearest-rank p95 is the 29th sample and is intentionally close
to a maximum; increase ``--iterations`` for a stable tail estimate. When
``dist/aiwatch/aiwatch[.exe]`` exists (or ``--frozen-binary`` is supplied), the
script also reports an actual onedir startup probe. The full local-stub hook
rows stay in the dev interpreter because release binaries intentionally accept
managed config only; they have no benchmark-only config bypass.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_WORKER_FLAG = "--worker"
_BENCHMARK_HOST_ENV = "_RUNLAYER_AIWATCH_BENCHMARK_HOST"
_DAEMON_ENDPOINT_ENV = "RUNLAYER_AIWATCH_DAEMON_SOCKET"
_CLI_ROOT = Path(__file__).resolve().parents[1]
_FIXTURE_PATH = (
    _CLI_ROOT
    / "tests"
    / "fixtures"
    / "hook_replay"
    / "claude_code"
    / "user_prompt_submit_event.json"
)


def _install_benchmark_managed_config(*, daemon_enabled: bool) -> None:
    from collections.abc import Callable

    sys.path.insert(0, str(_CLI_ROOT))
    from runlayer_cli import mdm_config

    host = os.environ[_BENCHMARK_HOST_ENV]

    def read_config() -> mdm_config.ManagedConfig:
        return {
            "daemon_enabled": daemon_enabled,
            "host": host,
            "org_api_key": "aiwatch-benchmark-key",
            "sessions": True,
        }

    mdm_config.set_managed_config_provider(None)
    mdm_config._read_managed_config_uncached: (  # noqa: SLF001
        Callable[[], mdm_config.ManagedConfig]
    ) = read_config


def _run_worker(mode: str) -> int:
    daemon_enabled = mode in {"daemon", "daemon-served"}
    _install_benchmark_managed_config(daemon_enabled=daemon_enabled)

    if mode == "cold-inline":
        from runlayer_cli import aiwatch
        from runlayer_cli.runtime import mark_aiwatch_runtime

        mark_aiwatch_runtime()
        aiwatch._build_app()  # noqa: SLF001 - deliberately recreate old import tax
        aiwatch._apply_managed_config()  # noqa: SLF001
        from runlayer_cli.hook.dispatch import run_hook

        sys.argv = ["aiwatch"]
        run_hook()
    elif mode in {"thin-inline", "daemon-served", "daemon"}:
        from runlayer_cli import aiwatch

        subcommand = "daemon" if mode == "daemon" else "hook"
        sys.argv = ["aiwatch", subcommand]
        aiwatch.main()
    else:
        raise ValueError(f"unknown worker mode: {mode}")
    return 0


def _percentile(samples: list[float], percentile: float) -> float:
    import math

    ordered = sorted(samples)
    index = max(0, math.ceil(percentile * len(ordered)) - 1)
    return ordered[index]


def _load_payload() -> str:
    import json

    fixture = json.loads(_FIXTURE_PATH.read_text())
    return json.dumps(fixture["input"], separators=(",", ":"))


def _worker_command(mode: str) -> list[str]:
    return [sys.executable, str(Path(__file__).resolve()), _WORKER_FLAG, mode]


def _shim_command(binary: Path) -> list[str]:
    return [str(binary), "hook", "--client", "claude_code"]


def _frozen_startup_command(binary: Path) -> list[str]:
    return [str(binary), "daemon", "--help"]


def _run_frozen_startup_sample(binary: Path) -> float:
    import subprocess
    import time

    started = time.perf_counter()
    completed = subprocess.run(
        _frozen_startup_command(binary),
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    elapsed_ms = (time.perf_counter() - started) * 1_000
    if completed.returncode != 0:
        raise RuntimeError(
            f"frozen startup probe exited {completed.returncode}: "
            f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
        )
    return elapsed_ms


def _measure_frozen_startup(
    binary: Path,
    *,
    iterations: int,
    warmups: int,
) -> list[float]:
    for _ in range(warmups):
        _run_frozen_startup_sample(binary)
    return [_run_frozen_startup_sample(binary) for _ in range(iterations)]


def _run_sample(mode: str, payload: str, env: dict[str, str]) -> float:
    import subprocess
    import time

    started = time.perf_counter()
    completed = subprocess.run(
        _worker_command(mode),
        input=payload,
        text=True,
        capture_output=True,
        env=env,
        timeout=30,
        check=False,
    )
    elapsed_ms = (time.perf_counter() - started) * 1_000
    if completed.returncode != 0:
        raise RuntimeError(
            f"{mode} worker exited {completed.returncode}: "
            f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
        )
    return elapsed_ms


def _run_shim_sample(binary: Path, payload: str, env: dict[str, str]) -> float:
    import subprocess
    import time

    started = time.perf_counter()
    completed = subprocess.run(
        _shim_command(binary),
        input=payload,
        text=True,
        capture_output=True,
        env=env,
        timeout=30,
        check=False,
    )
    elapsed_ms = (time.perf_counter() - started) * 1_000
    if completed.returncode != 0:
        raise RuntimeError(
            f"daemon-via-shim exited {completed.returncode}: "
            f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
        )
    return elapsed_ms


def _measure(
    mode: str,
    *,
    payload: str,
    env: dict[str, str],
    iterations: int,
    warmups: int,
) -> list[float]:
    for _ in range(warmups):
        _run_sample(mode, payload, env)
    return [_run_sample(mode, payload, env) for _ in range(iterations)]


def _measure_shim(
    binary: Path,
    *,
    payload: str,
    env: dict[str, str],
    iterations: int,
    warmups: int,
) -> list[float]:
    for _ in range(warmups):
        _run_shim_sample(binary, payload, env)
    return [_run_shim_sample(binary, payload, env) for _ in range(iterations)]


def _write_stub_certificate(temp_dir: Path) -> tuple[Path, Path]:
    import ipaddress
    from datetime import datetime, timedelta, timezone

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "AI Watch benchmark")])
    now = datetime.now(timezone.utc)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(days=1))
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    x509.DNSName("localhost"),
                    x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
                ]
            ),
            critical=False,
        )
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
            critical=False,
        )
        .sign(private_key, hashes.SHA256())
    )
    certificate_path = temp_dir / "benchmark-ca.pem"
    private_key_path = temp_dir / "benchmark-key.pem"
    certificate_path.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    private_key_path.write_bytes(
        private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    return certificate_path, private_key_path


def _start_stub_server(
    temp_dir: Path,
    *,
    response_delay_seconds: float,
) -> tuple[object, object, str, Path]:
    import ssl
    import threading
    import time
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from typing import Any

    class StubHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_HEAD(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            self._respond()

        def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            content_length = int(self.headers.get("Content-Length", "0"))
            self.rfile.read(content_length)
            self._respond()

        def _respond(self) -> None:
            time.sleep(response_delay_seconds)
            body = b"{}"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            del format, args

    server = ThreadingHTTPServer(("127.0.0.1", 0), StubHandler)
    certificate_path, private_key_path = _write_stub_certificate(temp_dir)
    context_type = ssl.SSLContext
    if context_type.__module__.startswith("truststore."):
        from truststore._api import (  # noqa: PLC0415
            _original_SSLContext,  # noqa: PLC2701
        )

        context_type = _original_SSLContext
    tls = context_type(ssl.PROTOCOL_TLS_SERVER)
    tls.load_cert_chain(
        certfile=str(certificate_path),
        keyfile=str(private_key_path),
    )
    server.socket = tls.wrap_socket(server.socket, server_side=True)
    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
        name="aiwatch-benchmark-https",
    )
    thread.start()
    return (
        server,
        thread,
        f"https://127.0.0.1:{server.server_port}",
        certificate_path,
    )


def _benchmark_endpoint(temp_dir: Path) -> str:
    if sys.platform == "win32":
        return rf"\\.\pipe\runlayer-aiwatch-benchmark-{os.getpid()}"
    return str(temp_dir / "aiwatch.sock")


def _start_daemon(env: dict[str, str], endpoint: str) -> object:
    import subprocess
    import time

    daemon = subprocess.Popen(
        _worker_command("daemon"),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    sys.path.insert(0, str(_CLI_ROOT))
    from runlayer_cli.hook.daemon_client import probe_daemon

    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if daemon.poll() is not None:
            stdout, stderr = daemon.communicate()
            raise RuntimeError(
                f"daemon exited {daemon.returncode}: "
                f"stdout={stdout!r} stderr={stderr!r}"
            )
        response = probe_daemon(endpoint)
        if response is not None and response["status"] == "ok":
            return daemon
        time.sleep(0.05)
    daemon.terminate()
    stdout, stderr = daemon.communicate(timeout=5)
    raise RuntimeError(
        f"daemon did not become healthy: stdout={stdout!r} stderr={stderr!r}"
    )


def _stop_daemon(daemon: object) -> None:
    import subprocess

    process = daemon
    assert isinstance(process, subprocess.Popen)
    if process.poll() is None:
        process.terminate()
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=5)


def _build_env(
    *,
    host: str,
    endpoint: str,
    home: Path,
    ca_bundle: Path,
) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            _BENCHMARK_HOST_ENV: host,
            _DAEMON_ENDPOINT_ENV: endpoint,
            "HOME": str(home),
            "NO_PROXY": "127.0.0.1,localhost",
            "RUNLAYER_CA_BUNDLE": str(ca_bundle),
            "RUNLAYER_HOOK_CLIENT": "claude_code",
            "USERPROFILE": str(home),
        }
    )
    return env


def _print_results(results: dict[str, list[float]]) -> bool:
    labels = {
        "cold-inline": "cold inline",
        "thin-inline": "thin inline",
        "daemon-served": "daemon via Python",
        "daemon-via-shim": "daemon via shim",
    }
    summaries: dict[str, tuple[float, float]] = {}
    print(f"{'mode':<20} {'p50 ms':>10} {'p95 ms':>10}")
    print("-" * 42)
    modes = ["cold-inline", "thin-inline", "daemon-served"]
    if "daemon-via-shim" in results:
        modes.append("daemon-via-shim")
    for mode in modes:
        samples = results[mode]
        summary = (_percentile(samples, 0.50), _percentile(samples, 0.95))
        summaries[mode] = summary
        print(f"{labels[mode]:<20} {summary[0]:>10.1f} {summary[1]:>10.1f}")

    p50_faster = summaries["daemon-served"][0] < min(
        summaries["thin-inline"][0],
        summaries["cold-inline"][0],
    )
    p95_faster = summaries["daemon-served"][1] < min(
        summaries["thin-inline"][1],
        summaries["cold-inline"][1],
    )
    print(
        "\ndaemon-served faster than both inline modes: "
        f"p50={'PASS' if p50_faster else 'FAIL'}, "
        f"p95={'PASS' if p95_faster else 'FAIL'}"
    )
    shim_faster = True
    if "daemon-via-shim" in summaries:
        shim_faster = summaries["daemon-via-shim"][0] < summaries["daemon-served"][0]
        print(
            "daemon-via-shim p50 faster than daemon-via-Python-client: "
            f"{'PASS' if shim_faster else 'FAIL'}"
        )
    return p50_faster and p95_faster and shim_faster


def _default_frozen_binary() -> Path:
    filename = "aiwatch.exe" if sys.platform == "win32" else "aiwatch"
    return _CLI_ROOT / "dist" / "aiwatch" / filename


def _default_shim_binary() -> Path:
    filename = "aiwatch-hook.exe" if sys.platform == "win32" else "aiwatch-hook"
    return _CLI_ROOT.parent / "aiwatch-hook-shim" / "bin" / filename


def _resolve_frozen_binary(requested: Path | None) -> Path | None:
    candidate = requested if requested is not None else _default_frozen_binary()
    return candidate.resolve() if candidate.is_file() else None


def _resolve_shim_binary(requested: Path | None) -> Path | None:
    candidate = requested if requested is not None else _default_shim_binary()
    return candidate.resolve() if candidate.is_file() else None


def _print_frozen_startup(binary: Path, samples: list[float]) -> None:
    print(
        f"\nfrozen onedir startup ({binary}): "
        f"p50={_percentile(samples, 0.50):.1f} ms, "
        f"p95={_percentile(samples, 0.95):.1f} ms"
    )


def _run_benchmark(
    *,
    iterations: int,
    warmups: int,
    response_delay_seconds: float,
    frozen_binary: Path | None,
    shim_binary: Path | None,
) -> int:
    import tempfile

    payload = _load_payload()
    passed = False
    with tempfile.TemporaryDirectory(prefix="aiwatch-benchmark-") as raw_temp_dir:
        temp_dir = Path(raw_temp_dir)
        server, server_thread, host, ca_bundle = _start_stub_server(
            temp_dir,
            response_delay_seconds=response_delay_seconds,
        )
        daemon = None
        try:
            home = temp_dir / "home"
            home.mkdir()
            endpoint = _benchmark_endpoint(temp_dir)
            env = _build_env(
                host=host,
                endpoint=endpoint,
                home=home,
                ca_bundle=ca_bundle,
            )

            results = {
                "cold-inline": _measure(
                    "cold-inline",
                    payload=payload,
                    env=env,
                    iterations=iterations,
                    warmups=warmups,
                ),
                "thin-inline": _measure(
                    "thin-inline",
                    payload=payload,
                    env=env,
                    iterations=iterations,
                    warmups=warmups,
                ),
            }
            daemon = _start_daemon(env, endpoint)
            results["daemon-served"] = _measure(
                "daemon-served",
                payload=payload,
                env=env,
                iterations=iterations,
                warmups=warmups,
            )
            if shim_binary is not None:
                results["daemon-via-shim"] = _measure_shim(
                    shim_binary,
                    payload=payload,
                    env=env,
                    iterations=iterations,
                    warmups=warmups,
                )
            passed = _print_results(results)
        finally:
            if daemon is not None:
                _stop_daemon(daemon)
            server.shutdown()
            server.server_close()
            server_thread.join(timeout=5)

    if frozen_binary is not None:
        samples = _measure_frozen_startup(
            frozen_binary,
            iterations=iterations,
            warmups=warmups,
        )
        _print_frozen_startup(frozen_binary, samples)
    return 0 if passed else 1


def _main() -> int:
    if len(sys.argv) >= 3 and sys.argv[1] == _WORKER_FLAG:
        return _run_worker(sys.argv[2])

    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--iterations",
        type=int,
        default=30,
        help="measured subprocesses per mode (default: 30)",
    )
    parser.add_argument(
        "--warmups",
        type=int,
        default=3,
        help="unmeasured subprocesses per mode (default: 3)",
    )
    parser.add_argument(
        "--stub-delay-ms",
        type=float,
        default=40.0,
        help="HTTPS stub response delay in milliseconds (default: 40)",
    )
    parser.add_argument(
        "--frozen-binary",
        type=Path,
        help=(
            "optional packaged aiwatch path for an onedir startup probe; "
            "auto-detects dist/aiwatch/aiwatch[.exe]"
        ),
    )
    parser.add_argument(
        "--shim-binary",
        type=Path,
        help=(
            "native aiwatch-hook built with the current CLI version; "
            "auto-detects ../aiwatch-hook-shim/bin/aiwatch-hook[.exe]"
        ),
    )
    args = parser.parse_args()
    if args.iterations < 1 or args.warmups < 0 or args.stub_delay_ms < 0:
        parser.error(
            "--iterations must be >= 1, --warmups >= 0, and --stub-delay-ms >= 0"
        )
    if args.frozen_binary is not None and not args.frozen_binary.is_file():
        parser.error(f"--frozen-binary does not exist: {args.frozen_binary}")
    if args.shim_binary is not None and not args.shim_binary.is_file():
        parser.error(f"--shim-binary does not exist: {args.shim_binary}")
    return _run_benchmark(
        iterations=args.iterations,
        warmups=args.warmups,
        response_delay_seconds=args.stub_delay_ms / 1_000,
        frozen_binary=_resolve_frozen_binary(args.frozen_binary),
        shim_binary=_resolve_shim_binary(args.shim_binary),
    )


if __name__ == "__main__":
    raise SystemExit(_main())
