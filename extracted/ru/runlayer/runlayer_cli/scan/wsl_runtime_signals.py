"""File-only runtime signals reachable through WSL UNC shares."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import replace
from pathlib import Path

from runlayer_cli.scan.device import DiscoveredWSLDistro, get_wsl_distro_root
from runlayer_cli.scan.wsl_limits import MAX_WSL_DISTROS

_RUNTIME_PATHS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("docker", ("var", "lib", "docker")),
    ("docker", ("var", "run", "docker.sock")),
    ("docker", ("run", "docker.sock")),
    ("podman", ("var", "lib", "containers")),
)


def _safe_exists(path: Path) -> bool | None:
    try:
        path.stat()
    except FileNotFoundError:
        return False
    except OSError:
        return None
    return True


def scan_wsl_runtime_file_signals(
    distros: Iterable[DiscoveredWSLDistro],
    *,
    checkpoint: Callable[[], None] | None = None,
) -> list[DiscoveredWSLDistro]:
    """Annotate reachable running distros with container-runtime file signals."""
    annotated: list[DiscoveredWSLDistro] = []
    for index, distro in enumerate(distros):
        if index >= MAX_WSL_DISTROS or not distro.is_running:
            annotated.append(distro)
            continue
        distro_root = get_wsl_distro_root(distro.name)
        if distro_root is None:
            annotated.append(distro)
            continue
        runtimes: set[str] = set()
        all_probes_definitive = True
        for runtime, relative_parts in _RUNTIME_PATHS:
            if checkpoint is not None:
                checkpoint()
            exists = _safe_exists(distro_root.joinpath(*relative_parts))
            if exists is None:
                all_probes_definitive = False
            elif exists:
                runtimes.add(runtime)
        annotated.append(
            replace(
                distro,
                scanned=all_probes_definitive,
                container_runtimes=tuple(sorted(runtimes)),
            )
        )
    return annotated
