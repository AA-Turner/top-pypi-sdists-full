from __future__ import annotations

import logging
import os
import subprocess
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

try:
    from langgraph_api_core_bin import binary_path
except ImportError:
    binary_path = None

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = logging.getLogger(__name__)

# Hands the address of a core started by ``langgraph dev`` to its server process.
ADDRESS_ENV = "LANGGRAPH_EMBEDDED_CORE_ADDRESS"
SQLITE_PATH = os.path.join(".langgraph_api", "core.sqlite")
# Local data formats this version no longer reads. Add a pattern whenever a
# change drops local dev data instead of migrating it.
DROPPED_LOCAL_DATA = (
    ".langgraph_*.pckl",  # Python in-memory runtime
)


@contextmanager
def start(sqlite_path: str | None = None) -> Iterator[str]:
    """Run Go core on SQLite; in-memory unless ``sqlite_path`` is given."""
    if binary_path is None:
        raise RuntimeError(
            "Local development requires the inmem extra: "
            "pip install 'langgraph-api[inmem]'"
        )

    with tempfile.TemporaryDirectory(prefix="langgraph-core-") as temp_dir:
        address_file = Path(temp_dir, "address")
        env = os.environ.copy()
        env.update(
            DATABASE_URI="",
            DISPATCH_MODE="single-process",
            LANGGRAPH_STORE_BACKEND="grpc",
            LSD_GRPC_SERVER_ADDRESS="127.0.0.1:0",
            PPROF_ADDR="127.0.0.1:0",
        )
        # An empty DATABASE_URI falls back to POSTGRES_URI, which sqlite_only cores refuse.
        env.pop("POSTGRES_URI", None)
        env.pop("REDIS_URI", None)
        env.pop("REDIS_URI_CUSTOM", None)
        env["LOG_LEVEL"] = _core_log_level(env.get("LOG_LEVEL", ""))
        # Core exits when this pipe closes, so it never outlives this process.
        args = [
            binary_path(),
            "-apply-db-schema",
            "-exit-on-stdin-close",
            "-address-file",
            address_file,
        ]
        if sqlite_path:
            Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
            _warn_dropped_local_data(Path(sqlite_path).parent)
            args += ["-sqlite-path", sqlite_path]
        process = subprocess.Popen(
            args,
            env=env,
            stdin=subprocess.PIPE,
        )
        try:
            yield _wait_for_address(process, address_file)
        finally:
            # Closing stdin shuts core down gracefully on every OS; terminate()
            # would be a hard kill on Windows.
            if process.stdin:
                process.stdin.close()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def _core_log_level(level: str) -> str:
    """Map Python's LOG_LEVEL to core's; unknown values make core log at INFO.

    Defaults to WARN: core's startup INFO logs drown out the dev server.
    """
    level = {"WARNING": "WARN", "CRITICAL": "ERROR"}.get(level.upper(), level.upper())
    return level if level in ("DEBUG", "INFO", "WARN", "ERROR", "FATAL") else "WARN"


def _warn_dropped_local_data(data_dir: Path) -> None:
    dropped = sorted(
        str(f) for pattern in DROPPED_LOCAL_DATA for f in data_dir.glob(pattern)
    )
    if dropped:
        logger.warning(
            "Ignoring local data from an older format that this version no longer "
            "reads; threads, runs and store items saved there won't appear: %s",
            ", ".join(dropped),
        )


def _wait_for_address(
    process: subprocess.Popen[bytes], address_file: Path, timeout: float = 30
) -> str:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(
                f"LangGraph API core exited with code {process.returncode}"
            )
        try:
            if address := address_file.read_text().strip():
                return address
        except FileNotFoundError:
            pass
        time.sleep(0.05)
    raise RuntimeError("Timed out waiting for LangGraph API core to start")


__all__ = ["ADDRESS_ENV", "SQLITE_PATH", "start"]
