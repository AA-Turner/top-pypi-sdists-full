#!/usr/bin/env python3
"""Print the dependency versions that populate doc/versions/news.md.

Designed to be called from each wheel-build CI job. Auto-detects the
platform and gathers each version using the appropriate mechanism
(pkg-config on Linux, micromamba list on macOS, filename/header parsing
plus env vars on Windows). Always exits 0 so a missing dependency does
not fail the CI job; missing values are printed as "?" in the table.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROWS = [
    "cpptango",
    "omniorb / omniorb-libs",
    "libzmq / zeromq",
    "cppzmq",
    "libjpeg-turbo",
    "abseil",
    "protobuf",
    "c-ares",
    "re2",
    "OpenSSL",
    "curl",
    "gRPC",
    "opentelemetry-cpp",
]


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=False)
    except (FileNotFoundError, OSError):
        return None


def pkg_config(*candidates: str) -> str | None:
    for pc in candidates:
        r = _run(["pkg-config", "--modversion", pc])
        if r is not None and r.returncode == 0:
            return r.stdout.strip()
    return None


def cppzmq_from_header(zmq_hpp: Path) -> str | None:
    if not zmq_hpp.is_file():
        return None
    parts: dict[str, str] = {}
    pat = re.compile(r"^\s*#define\s+(CPPZMQ_VERSION_(?:MAJOR|MINOR|PATCH))\s+(\d+)")
    for line in zmq_hpp.read_text(errors="replace").splitlines():
        m = pat.match(line)
        if m:
            parts[m.group(1)] = m.group(2)
    if len(parts) != 3:
        return None
    return f"{parts['CPPZMQ_VERSION_MAJOR']}.{parts['CPPZMQ_VERSION_MINOR']}.{parts['CPPZMQ_VERSION_PATCH']}"


def gather_linux() -> dict[str, str | None]:
    cpptango = pkg_config("tango")
    if cpptango is None:
        libtango = Path("/usr/local/lib/libtango.so")
        if libtango.exists():
            target = os.path.realpath(libtango)
            m = re.search(r"libtango\.so\.([\d.]+)", target)
            if m:
                cpptango = m.group(1)
    return {
        "cpptango": cpptango,
        "omniorb / omniorb-libs": pkg_config("omniORB4"),
        "libzmq / zeromq": pkg_config("libzmq"),
        "cppzmq": cppzmq_from_header(Path("/usr/local/include/zmq.hpp")),
        "libjpeg-turbo": pkg_config("libturbojpeg", "libjpeg"),
        "abseil": pkg_config("absl_base"),
        "protobuf": pkg_config("protobuf"),
        "c-ares": pkg_config("libcares"),
        "re2": pkg_config("re2"),
        "OpenSSL": pkg_config("openssl"),
        "curl": pkg_config("libcurl"),
        "gRPC": pkg_config("grpc++", "grpc"),
        "opentelemetry-cpp": pkg_config("opentelemetry_api", "opentelemetry_sdk"),
    }


def _conda_prefix() -> Path | None:
    """Find an active conda/mamba prefix without depending on a subprocess.

    Subprocess-based ``micromamba list`` is unreliable in CI when the
    activation state hasn't propagated to the Python child process; reading
    ``$CONDA_PREFIX/conda-meta`` directly is much more robust.
    """
    prefix = os.environ.get("CONDA_PREFIX")
    if prefix and (Path(prefix) / "conda-meta").is_dir():
        return Path(prefix)
    for candidate in (Path.home() / "micromamba", Path("/Users/gitlab/micromamba")):
        if (candidate / "conda-meta").is_dir():
            return candidate
    return None


def gather_macos() -> dict[str, str | None]:
    prefix = _conda_prefix()
    if prefix is None:
        return dict.fromkeys(ROWS)
    installed: dict[str, str] = {}
    for f in (prefix / "conda-meta").glob("*.json"):
        try:
            data = json.loads(f.read_text())
            installed[data["name"]] = data["version"]
        except (OSError, ValueError, KeyError):
            continue

    def pick(*names: str) -> str | None:
        for n in names:
            if n in installed:
                return installed[n]
        return None

    return {
        "cpptango": pick("cpptango"),
        "omniorb / omniorb-libs": pick("omniorb-libs", "omniorb"),
        "libzmq / zeromq": pick("zeromq"),
        "cppzmq": pick("cppzmq"),
        "libjpeg-turbo": pick("libjpeg-turbo"),
        "abseil": pick("libabseil"),
        "protobuf": pick("libprotobuf"),
        "c-ares": pick("c-ares"),
        "re2": pick("re2"),
        "OpenSSL": pick("openssl"),
        "curl": pick("libcurl"),
        "gRPC": pick("libgrpc"),
        "opentelemetry-cpp": pick("opentelemetry-cpp", "libopentelemetry-cpp"),
    }


def gather_windows() -> dict[str, str | None]:
    tango_root_env = os.environ.get("TANGO_ROOT")
    tango_root = Path(tango_root_env) if tango_root_env else None

    omniorb = libzmq = jpeg = cppzmq = None
    if tango_root and tango_root.exists():
        bin_dir = tango_root / "bin"
        if bin_dir.is_dir():
            for dll in bin_dir.iterdir():
                name = dll.name
                m = re.match(r"omniORB(\d)(\d)(\d)_", name)
                if m:
                    omniorb = f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
                m = re.search(r"libzmq.*?-(\d+)_(\d+)_(\d+)", name)
                if m:
                    libzmq = f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
                # jpeg62.dll only carries the SONAME; the full libjpeg-turbo
                # version is not exposed by the bundle, fill manually.
        cppzmq = cppzmq_from_header(tango_root / "include" / "zmq.hpp")
    return {
        "cpptango": os.environ.get("CPP_TANGO_VERSION_TAG"),
        "omniorb / omniorb-libs": omniorb,
        "libzmq / zeromq": libzmq,
        "cppzmq": cppzmq,
        "libjpeg-turbo": jpeg,
        "abseil": None,
        "protobuf": None,
        "c-ares": None,
        "re2": None,
        "OpenSSL": None,
        "curl": None,
        "gRPC": None,
        "opentelemetry-cpp": None,
    }


def detect_platform() -> tuple[str, callable]:
    if sys.platform.startswith("linux"):
        return "Linux", gather_linux
    if sys.platform == "darwin":
        return "MacOS", gather_macos
    if sys.platform.startswith("win"):
        return "Windows", gather_windows
    return sys.platform, lambda: dict.fromkeys(ROWS)


def print_table(plat: str, versions: dict[str, str | None]) -> None:
    label_w = max(len("Dependency"), max(len(r) for r in ROWS))
    value_w = max(len(plat), max(len(v or "?") for v in versions.values()))
    print(f"| {'Dependency'.ljust(label_w)} | {plat.ljust(value_w)} |")
    print(f"| {'-' * label_w} | {'-' * value_w} |")
    for row in ROWS:
        v = versions[row] or "?"
        print(f"| {row.ljust(label_w)} | {v.ljust(value_w)} |")


def main() -> int:
    plat, gather = detect_platform()
    print(f"=== Dependency versions ({plat}) ===")
    try:
        versions = gather()
    except Exception as e:
        print(f"(failed to gather: {e})")
        versions = dict.fromkeys(ROWS)
    print_table(plat, versions)
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
