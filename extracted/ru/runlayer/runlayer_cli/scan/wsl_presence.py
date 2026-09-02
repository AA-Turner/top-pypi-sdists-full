"""Bounded file-only AI client presence probes inside running WSL distros."""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from itertools import islice
from pathlib import Path

from runlayer_cli.scan.cli_binaries import posix_bin_roots
from runlayer_cli.scan.clients import MCPClientDefinition
from runlayer_cli.scan.device import (
    DiscoveredWSLDistro,
    get_wsl_distro_root,
    get_wsl_user_homes,
)
from runlayer_cli.scan.wsl_limits import MAX_WSL_DISTROS, MAX_WSL_HOMES
from runlayer_cli.scan.wsl_paths import parse_wsl_unc_path

MAX_WSL_BINARY_CANDIDATES_PER_DISTRO = 4096
WSL_PRESENCE_TIME_BUDGET_S = 30.0

_SYSTEM_BIN_ROOTS = (
    ("usr", "local", "bin"),
    ("usr", "bin"),
    ("snap", "bin"),
    ("nix", "var", "nix", "profiles", "default", "bin"),
)


@dataclass(frozen=True)
class WSLClientContext:
    """One distro/home that supplied client presence evidence."""

    distro: str
    user: str | None

    def to_api_payload(self) -> dict[str, str | None]:
        return {"distro": self.distro, "user": self.user}


@dataclass(frozen=True)
class WSLBinaryFinding:
    """One allowlisted CLI basename found via a WSL UNC path."""

    client: str
    binary: str
    path: Path
    context: WSLClientContext


def _safe_is_file(path: Path) -> bool:
    try:
        return path.is_file()
    except OSError:
        return False


def _home_context(home: Path, distro: str) -> WSLClientContext:
    parsed = parse_wsl_unc_path(home)
    if parsed is not None:
        return WSLClientContext(distro=parsed.distro, user=parsed.user)
    return WSLClientContext(
        distro=distro,
        user="root" if home.name == "root" else home.name or None,
    )


def _user_bin_roots(home: Path) -> list[Path]:
    home_key = str(home).casefold().rstrip("\\/")
    return [
        root
        for root in posix_bin_roots(home=home, system="Linux")
        if str(root).casefold().rstrip("\\/").startswith(home_key)
    ]


def scan_wsl_cli_binaries(
    clients: Iterable[MCPClientDefinition],
    distros: Iterable[DiscoveredWSLDistro],
    *,
    checkpoint: Callable[[], None] | None = None,
) -> list[WSLBinaryFinding]:
    """Find registered CLI basenames without executing WSL-owned files."""
    client_binaries = [
        (client.name, binary)
        for client in clients
        if client.install_probe is not None
        for binary in client.install_probe.cli_binaries
    ]
    if not client_binaries:
        return []

    deadline = time.monotonic() + WSL_PRESENCE_TIME_BUDGET_S
    findings: list[WSLBinaryFinding] = []
    seen: set[tuple[str, str, str | None, str]] = set()
    for distro in tuple(distros)[:MAX_WSL_DISTROS]:
        if time.monotonic() >= deadline:
            break
        if not distro.is_running:
            continue
        distro_root = get_wsl_distro_root(distro.name)
        if distro_root is None:
            continue
        if time.monotonic() >= deadline:
            break

        homes = tuple(islice(get_wsl_user_homes(distro.name), MAX_WSL_HOMES))
        if time.monotonic() >= deadline:
            break
        candidates_checked = 0
        for client, binary in client_binaries:
            candidates: list[tuple[Path, WSLClientContext]] = []
            for home in homes:
                context = _home_context(home, distro.name)
                candidates.extend(
                    (root / binary, context) for root in _user_bin_roots(home)
                )
            system_context = WSLClientContext(distro=distro.name, user=None)
            candidates.extend(
                (distro_root.joinpath(*parts, binary), system_context)
                for parts in _SYSTEM_BIN_ROOTS
            )
            candidates.append(
                (
                    distro_root / "opt" / binary / "bin" / binary,
                    system_context,
                )
            )

            for path, context in candidates:
                if (
                    time.monotonic() >= deadline
                    or candidates_checked >= MAX_WSL_BINARY_CANDIDATES_PER_DISTRO
                ):
                    break
                candidates_checked += 1
                if checkpoint is not None:
                    checkpoint()
                key = (client, context.distro.casefold(), context.user, str(path))
                if key in seen or not _safe_is_file(path):
                    continue
                seen.add(key)
                findings.append(
                    WSLBinaryFinding(
                        client=client,
                        binary=binary,
                        path=path,
                        context=context,
                    )
                )
            if (
                time.monotonic() >= deadline
                or candidates_checked >= MAX_WSL_BINARY_CANDIDATES_PER_DISTRO
            ):
                break
    return findings
