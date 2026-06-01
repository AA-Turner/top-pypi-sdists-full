# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""HTTP metrics collection using mitmproxy.

This module provides utilities for capturing HTTP traffic from connector
executions using mitmproxy as a local subprocess.
"""

from __future__ import annotations

import logging
import shutil
import signal
import socket
import subprocess
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

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
MITMDUMP_STARTUP_WAIT_SECONDS = 1


@dataclass
class HttpMetrics:
    """HTTP traffic metrics from a connector execution."""

    flow_count: int
    duplicate_flow_count: int
    unique_urls: list[str]
    cache_hits_count: int = 0

    @property
    def cache_hit_ratio(self) -> str:
        """Calculate cache hit ratio as a percentage string."""
        if self.flow_count == 0:
            return "N/A"
        return f"{(self.cache_hits_count / self.flow_count) * 100:.2f}%"

    @classmethod
    def empty(cls) -> HttpMetrics:
        """Create empty metrics when HTTP capture is unavailable."""
        return cls(
            flow_count=0, duplicate_flow_count=0, unique_urls=[], cache_hits_count=0
        )


@dataclass
class MitmproxySession:
    """Active mitmproxy session information."""

    proxy_host: str
    proxy_port: int
    dump_file_path: Path
    ca_cert_path: Path | None

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
    try:
        subprocess.run(
            [mitmdump_path, "--version"],
            capture_output=True,
            timeout=10,
        )

        proc = subprocess.Popen(
            [mitmdump_path],
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


class MitmproxyManager:
    """Manages a mitmproxy subprocess for HTTP traffic capture.

    This class starts mitmdump as a local subprocess and provides
    the proxy URL and CA cert path for connector containers to use.

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
    ) -> None:
        """Initialize the mitmproxy manager.

        Args:
            output_dir: Directory to write the dump file to.
            port: Specific port to use, or None to find a free port.
        """
        self.output_dir = output_dir
        self.port = port or find_free_port()
        self.dump_file_path = output_dir / "http_traffic.mitm"
        self._process: subprocess.Popen | None = None

    @classmethod
    @contextmanager
    def start(
        cls,
        output_dir: Path,
        port: int | None = None,
    ) -> Iterator[MitmproxySession | None]:
        """Start mitmproxy and yield a session, stopping on exit.

        This is a context manager that ensures mitmproxy is properly
        stopped even if an exception occurs.

        Args:
            output_dir: Directory to write the dump file to.
            port: Specific port to use, or None to find a free port.

        Yields:
            MitmproxySession with proxy info, or None if startup failed.
        """
        manager = cls(output_dir, port)
        session = manager._start()
        try:
            yield session
        finally:
            manager._stop()

    def _start(self) -> MitmproxySession | None:
        """Start the mitmproxy subprocess.

        Returns:
            MitmproxySession with proxy info, or None if startup failed.
        """
        mitmdump_path = shutil.which("mitmdump")
        if not mitmdump_path:
            logger.warning("mitmdump not found in PATH, HTTP metrics disabled")
            return None

        ca_cert_path = ensure_mitmproxy_ca_cert()

        self.output_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            mitmdump_path,
            "--listen-port",
            str(self.port),
            "--save-stream-file",
            str(self.dump_file_path),
            "--flow-detail",
            "0",
            "--set",
            "stream_large_bodies=1",
        ]

        logger.info(f"Starting mitmproxy on port {self.port}")
        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Give mitmdump a moment to start before checking if it exited
            time.sleep(MITMDUMP_STARTUP_WAIT_SECONDS)

            if self._process.poll() is not None:
                stderr = (
                    self._process.stderr.read().decode() if self._process.stderr else ""
                )
                logger.warning(f"Mitmproxy failed to start: {stderr}")
                return None

            logger.info(f"Mitmproxy started on port {self.port}")
            return MitmproxySession(
                proxy_host="host.docker.internal",
                proxy_port=self.port,
                dump_file_path=self.dump_file_path,
                ca_cert_path=ca_cert_path,
            )

        except FileNotFoundError:
            logger.warning("mitmdump not found, HTTP metrics disabled")
            return None

    def _stop(self) -> None:
        """Stop the mitmproxy subprocess."""
        if self._process is None:
            return

        logger.info("Stopping mitmproxy...")
        try:
            self._process.send_signal(signal.SIGINT)
            self._process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logger.warning("Mitmproxy did not stop gracefully, killing...")
            self._process.kill()
            self._process.wait(timeout=5)

        self._process = None
        logger.info("Mitmproxy stopped")


def parse_http_dump(dump_file_path: Path) -> HttpMetrics:
    """Parse a mitmproxy dump file and compute HTTP metrics.

    Args:
        dump_file_path: Path to the .mitm dump file.

    Returns:
        HttpMetrics with flow counts and URL information.
    """
    if not MITMPROXY_AVAILABLE:
        logger.warning("mitmproxy Python package not installed; HTTP metrics disabled")
        return HttpMetrics.empty()

    if not dump_file_path.exists():
        logger.warning(f"HTTP dump file not found: {dump_file_path}")
        return HttpMetrics.empty()

    with open(dump_file_path, "rb") as f:
        flows = [
            flow
            for flow in mitmproxy_io.FlowReader(f).stream()
            if isinstance(flow, mitmproxy_http.HTTPFlow)
        ]

    all_urls = [flow.request.url for flow in flows]
    unique_urls = list(set(all_urls))
    duplicate_count = len(all_urls) - len(unique_urls)

    # Cache hits are interpreted as duplicate requests to the same URL
    # (requests that could potentially be served from cache)
    cache_hits = duplicate_count

    return HttpMetrics(
        flow_count=len(flows),
        duplicate_flow_count=duplicate_count,
        unique_urls=sorted(unique_urls),
        cache_hits_count=cache_hits,
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
) -> Path:
    """Convert a mitmproxy HTTP stream file to a HAR file.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/utils.py#L142-L154

    HAR (HTTP Archive) is a standard JSON format for recording HTTP transactions.
    This allows HTTP traffic captured by mitmproxy to be viewed in browser dev tools
    or other HAR viewers.

    Args:
        mitm_http_stream_path: Path to the mitmproxy HTTP stream file (.mitm).
        har_file_path: Path where the HAR file will be saved.

    Returns:
        Path to the generated HAR file.

    Raises:
        RuntimeError: If mitmproxy is not available.
    """
    if not MITMPROXY_AVAILABLE or SaveHar is None:
        raise RuntimeError(
            "mitmproxy Python package not installed; cannot convert to HAR"
        )

    flows = get_http_flows_from_mitm_dump(mitm_http_stream_path)
    if not flows:
        logger.warning(f"No HTTP flows found in {mitm_http_stream_path}")
        return har_file_path

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
