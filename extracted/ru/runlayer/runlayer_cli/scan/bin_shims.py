"""Resolved-target identity sweep over already-probed bin directories (POSIX).

A renamed launcher hides from every name-keyed probe, but a symlink's
realpath still lands on the real tool — the one signal the rename cannot
change without breaking the launcher. Sweep the same bounded bin-directory
set the CLI candidate probe uses (plus ``PATH`` entries) and classify each
symlink by where it resolves:

* the resolved target's basename is a known CLI binary name, or
* the resolved target lands inside an allowlisted ``node_modules/<pkg>/``
  whose ``package.json`` validates against the exact package identity.

The shim's own name and location are never classifiers. Nothing here is
executed — the sweep only lstats, resolves, and reads bounded manifests.
This sweep detects POSIX symlinks by resolved target identity. Linux process
discovery can recover some running renamed copies via ``/proc/<pid>/exe``, but
only while they are running and when the resolved executable provides a known
identity. macOS process enumeration reports ``argv[0]`` rather than an
independently resolved executable. Idle copied or renamed binaries remain
undetected on every OS.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from runlayer_cli.scan.cli_binaries import posix_bin_roots
from runlayer_cli.scan.npm_global import (
    MAX_MANIFEST_BYTES,
    NpmPackageSpec,
    validate_npm_manifest,
)
from runlayer_cli.scan.scanner_primitives import is_regular_file, read_bounded

MAX_SWEPT_DIRS = 64
MAX_PATH_DIRS = 32
MAX_ENTRIES_PER_DIR = 4096
MAX_RESOLVED_SYMLINKS = 4096


@dataclass(frozen=True)
class ShimFinding:
    """One renamed launcher classified by its resolved target identity."""

    shim_path: Path
    target_path: Path
    version: str | None


def _path_environment_dirs(environment: Mapping[str, str]) -> list[Path]:
    value = environment.get("PATH", "")
    dirs: list[Path] = []
    for element in value.split(os.pathsep):
        if len(dirs) >= MAX_PATH_DIRS:
            break
        if element and os.path.isabs(element):
            dirs.append(Path(element))
    return dirs


def _npm_package_for_target(target: Path) -> str | None:
    """Return the ``node_modules`` package name owning *target*, if any.

    Uses the last ``node_modules`` component so nested dependencies resolve
    to the innermost (owning) package. Scoped packages span two components.
    """
    parts = target.parts
    for index in range(len(parts) - 2, -1, -1):
        if parts[index] != "node_modules":
            continue
        first = parts[index + 1]
        if first.startswith("@"):
            if index + 2 < len(parts) - 1:
                return f"{first}/{parts[index + 2]}"
            return None
        if index + 1 < len(parts) - 1:
            return first
        return None
    return None


def _npm_finding(
    shim: Path,
    target: Path,
    npm_packages: Mapping[str, NpmPackageSpec],
) -> tuple[str, ShimFinding] | None:
    package_name = _npm_package_for_target(target)
    if package_name is None:
        return None
    package = npm_packages.get(package_name)
    if package is None:
        return None
    parts = target.parts
    component_count = 2 if "/" in package_name else 1
    package_end = len(parts)
    for index in range(len(parts) - 2, -1, -1):
        if parts[index] == "node_modules":
            package_end = index + 1 + component_count
            break
    package_dir = Path(*parts[:package_end])
    raw = read_bounded(package_dir / "package.json", max_bytes=MAX_MANIFEST_BYTES)
    if raw is None:
        return None
    manifest = validate_npm_manifest(raw, package)
    if manifest is None:
        return None
    return package_name, ShimFinding(
        shim_path=shim,
        target_path=target,
        version=manifest.version,
    )


def sweep_shim_identities(
    *,
    cli_basenames: Sequence[str],
    npm_packages: Mapping[str, NpmPackageSpec],
    home: Path,
    system: str,
    environment: Mapping[str, str],
    include_host_dirs: bool = True,
    checkpoint: Callable[[], None] | None = None,
) -> tuple[dict[str, list[ShimFinding]], dict[str, list[ShimFinding]]]:
    """Classify symlinked launchers in probed bin dirs by target identity.

    Returns ``(by_cli_basename, by_npm_package)`` — findings keyed by the
    known CLI basename and by the validated npm package name respectively.
    *include_host_dirs* additionally sweeps machine-wide bin dirs and ``PATH``
    entries; callers probing a synthetic home (tests, per-profile fan-out)
    disable it so host state never leaks into the result.
    """
    by_basename: dict[str, list[ShimFinding]] = {}
    by_package: dict[str, list[ShimFinding]] = {}
    if system == "Windows" or (not cli_basenames and not npm_packages):
        return by_basename, by_package

    known_basenames = frozenset(cli_basenames)
    directories: list[Path] = [
        root
        for root in posix_bin_roots(home=home, system=system)
        if include_host_dirs or root.is_relative_to(home)
    ]
    if include_host_dirs:
        directories.extend(_path_environment_dirs(environment))
    seen_dirs: set[str] = set()
    swept = 0
    resolved_symlinks = 0

    for directory in directories:
        if swept >= MAX_SWEPT_DIRS or resolved_symlinks >= MAX_RESOLVED_SYMLINKS:
            break
        try:
            dir_key = os.path.realpath(directory)
        except OSError:
            continue
        if dir_key in seen_dirs:
            continue
        seen_dirs.add(dir_key)
        try:
            entries = os.scandir(directory)
        except OSError:
            continue
        swept += 1
        with entries:
            inspected = 0
            for entry in entries:
                if checkpoint is not None:
                    checkpoint()
                inspected += 1
                if (
                    inspected > MAX_ENTRIES_PER_DIR
                    or resolved_symlinks >= MAX_RESOLVED_SYMLINKS
                ):
                    break
                try:
                    if not entry.is_symlink():
                        continue
                except OSError:
                    continue
                resolved_symlinks += 1
                shim = Path(entry.path)
                try:
                    target = Path(os.path.realpath(entry.path, strict=True))
                except OSError:
                    continue
                if target == shim or not is_regular_file(target):
                    continue
                if target.name in known_basenames:
                    by_basename.setdefault(target.name, []).append(
                        ShimFinding(
                            shim_path=shim,
                            target_path=target,
                            version=None,
                        )
                    )
                    continue
                npm_match = _npm_finding(shim, target, npm_packages)
                if npm_match is not None:
                    package_name, finding = npm_match
                    by_package.setdefault(package_name, []).append(finding)

    return by_basename, by_package
