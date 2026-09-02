"""Detect allowlisted Python distributions without importing or executing them."""

from __future__ import annotations

import os
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from email.parser import BytesParser
from itertools import islice, zip_longest
from pathlib import Path
from typing import Protocol

from runlayer_cli.scan.hidden_space_sweep import scan_hidden_spaces
from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    commit_approved_links,
    environment_value,
    has_link_or_reparse_component,
    is_real_directory,
    is_regular_file,
    read_bounded,
    resolve_approved_path,
    resolve_relative_components,
    resolved_directory_candidate,
)
from runlayer_cli.scan.windows_users import is_windows_system_context
from runlayer_cli.scan.wsl_limits import MAX_WSL_HOMES_TOTAL

MAX_FOLLOWED_SYMLINK_TARGETS = 64
MAX_ENV_ROOTS = 64
MAX_TOOL_ENVS_PER_ROOT = 64
MAX_CHILD_ENTRIES = 512
MAX_SITE_PACKAGES = 128
MAX_SITE_ENTRIES = 512
MAX_METADATA_BYTES = 512 * 1024
MAX_VERSION_LENGTH = 128
MAX_PATH_COMPONENTS = 64
_POSIX_SYSTEM_PYTHON_LIB_ROOTS = (Path("/usr/local/lib"), Path("/usr/lib"))
_DARWIN_SYSTEM_PYTHON_LIB_ROOTS = (Path("/opt/homebrew/lib"),)
_DARWIN_FRAMEWORK_VERSIONS = Path("/Library/Frameworks/Python.framework/Versions")


class PipPackageSpec(Protocol):
    name: str


@dataclass(frozen=True)
class PipGlobalPackage:
    """Validated Python distribution metadata used as presence evidence."""

    package_name: str
    version: str
    metadata_path: Path


def _canonical_name(value: str) -> str | None:
    if not value or any(
        not (character.isalnum() or character in "-_.") for character in value
    ):
        return None
    canonical: list[str] = []
    separator = False
    for character in value.casefold():
        if character in "-_.":
            if not separator:
                canonical.append("-")
            separator = True
        else:
            canonical.append(character)
            separator = False
    normalized = "".join(canonical).strip("-")
    return normalized or None


def _validated_metadata(
    raw: bytes,
    packages: Mapping[str, PipPackageSpec],
) -> tuple[PipPackageSpec, str] | None:
    try:
        metadata = BytesParser().parsebytes(raw, headersonly=True)
    except (TypeError, ValueError):
        return None
    names = metadata.get_all("Name", [])
    versions = metadata.get_all("Version", [])
    if len(names) != 1 or len(versions) != 1:
        return None
    name = _canonical_name(names[0])
    version = versions[0].strip()
    package = packages.get(name or "")
    if (
        package is None
        or not version
        or len(version) > MAX_VERSION_LENGTH
        or not version.isprintable()
        or any(character.isspace() for character in version)
    ):
        return None
    return package, version


def _bounded_child_directories(
    root: Path,
    *,
    name_prefix: str | None = None,
    checkpoint: Callable[[], None] | None = None,
    windows_system_context: bool = False,
) -> list[Path]:
    resolved_root = resolved_directory_candidate(
        root,
        windows_system_context=windows_system_context,
        max_components=MAX_PATH_COMPONENTS,
    )
    if resolved_root is None:
        return []
    entries: list[str] = []
    try:
        with os.scandir(resolved_root) as directory_entries:
            for index, entry in enumerate(
                islice(directory_entries, MAX_CHILD_ENTRIES + 1)
            ):
                if index == MAX_CHILD_ENTRIES:
                    break
                if checkpoint is not None:
                    checkpoint()
                entries.append(entry.name)
    except OSError:
        return []

    children: list[Path] = []
    for name in sorted(entries, key=lambda value: (value.casefold(), value)):
        if name_prefix is not None and not name.casefold().startswith(name_prefix):
            continue
        path = root / name
        if (
            resolved_directory_candidate(
                path,
                windows_system_context=windows_system_context,
                max_components=MAX_PATH_COMPONENTS,
            )
            is None
        ):
            continue
        children.append(path)
        if len(children) == MAX_TOOL_ENVS_PER_ROOT:
            break
    return children


def _environment_path(
    environment: Mapping[str, str],
    key: str,
    *,
    system: str,
) -> Path | None:
    value = environment_value(environment, key, system=system)
    if not value:
        return None
    path = Path(value).expanduser()
    return path if path.is_absolute() else None


def _standard_env_roots(
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
    checkpoint: Callable[[], None] | None,
    windows_system_context: bool,
) -> list[Path]:
    roots: list[Path] = []
    for key in ("VIRTUAL_ENV", "CONDA_PREFIX", "UV_PROJECT_ENVIRONMENT"):
        path = _environment_path(environment, key, system=system)
        if (
            path is not None
            and resolved_directory_candidate(
                path,
                windows_system_context=windows_system_context,
                max_components=MAX_PATH_COMPONENTS,
            )
            is not None
        ):
            roots.append(path)
    tool_roots: list[Path] = []
    pipx_home = _environment_path(environment, "PIPX_HOME", system=system)
    uv_tool_dir = _environment_path(environment, "UV_TOOL_DIR", system=system)
    if pipx_home is not None:
        tool_roots.append(pipx_home / "venvs")
    if uv_tool_dir is not None:
        tool_roots.append(uv_tool_dir)
    tool_roots.extend(
        [
            home / ".local" / "share" / "pipx" / "venvs",
            home / ".local" / "pipx" / "venvs",
            home / ".local" / "share" / "uv" / "tools",
        ]
    )
    if system == "Windows":
        tool_roots.extend(
            [
                home / "AppData" / "Local" / "pipx" / "venvs",
                home / "AppData" / "Roaming" / "uv" / "tools",
            ]
        )
    tool_env_groups = [
        _bounded_child_directories(
            tool_root,
            checkpoint=checkpoint,
            windows_system_context=windows_system_context,
        )
        for tool_root in tool_roots
    ]
    seen = {os.path.normcase(str(root.absolute())) for root in roots}
    for candidates in zip_longest(*tool_env_groups):
        for candidate in candidates:
            if candidate is None:
                continue
            key = os.path.normcase(str(candidate.absolute()))
            if key not in seen:
                seen.add(key)
                roots.append(candidate)
            if len(roots) >= MAX_ENV_ROOTS:
                return roots
    return roots


def _site_packages_for_env(
    env_root: Path,
    *,
    checkpoint: Callable[[], None] | None,
    windows_system_context: bool,
) -> list[Path]:
    candidates = [
        env_root / "Lib" / "site-packages",
        env_root / "Lib" / "dist-packages",
    ]
    lib = env_root / "lib"
    for python_dir in _bounded_child_directories(
        lib,
        name_prefix="python",
        checkpoint=checkpoint,
        windows_system_context=windows_system_context,
    ):
        candidates.extend(
            (
                python_dir / "site-packages",
                python_dir / "dist-packages",
            )
        )
    return [
        candidate
        for candidate in candidates
        if resolved_directory_candidate(
            candidate,
            windows_system_context=windows_system_context,
            max_components=MAX_PATH_COMPONENTS,
        )
        is not None
    ]


def _user_site_packages(
    home: Path,
    system: str,
    *,
    checkpoint: Callable[[], None] | None,
    windows_system_context: bool,
) -> list[Path]:
    candidates: list[Path] = []
    if system == "Windows":
        roots = [
            (home / "AppData" / "Roaming" / "Python", ("site-packages",)),
            (
                home / "AppData" / "Local" / "Programs" / "Python",
                ("Lib", "site-packages"),
            ),
        ]
        for root, suffix in roots:
            for python_dir in _bounded_child_directories(
                root,
                name_prefix="python",
                checkpoint=checkpoint,
                windows_system_context=windows_system_context,
            ):
                candidates.append(python_dir.joinpath(*suffix))
    else:
        for python_dir in _bounded_child_directories(
            home / ".local" / "lib",
            name_prefix="python",
            checkpoint=checkpoint,
            windows_system_context=windows_system_context,
        ):
            candidates.append(python_dir / "site-packages")
        if system == "Darwin":
            for python_dir in _bounded_child_directories(
                home / "Library" / "Python",
                checkpoint=checkpoint,
                windows_system_context=windows_system_context,
            ):
                candidates.append(python_dir / "lib" / "python" / "site-packages")
    return [
        candidate
        for candidate in candidates
        if resolved_directory_candidate(
            candidate,
            windows_system_context=windows_system_context,
            max_components=MAX_PATH_COMPONENTS,
        )
        is not None
    ]


def _system_site_packages(
    system: str,
    environment: Mapping[str, str],
    *,
    checkpoint: Callable[[], None] | None,
    windows_system_context: bool,
) -> list[Path]:
    candidates: list[Path] = []
    if system == "Windows":
        program_roots = [
            path
            for key in ("ProgramFiles", "ProgramFiles(x86)")
            if (path := _environment_path(environment, key, system=system)) is not None
        ]
        for root in program_roots:
            for python_dir in _bounded_child_directories(
                root,
                name_prefix="python",
                checkpoint=checkpoint,
                windows_system_context=windows_system_context,
            ):
                candidates.append(python_dir / "Lib" / "site-packages")
    else:
        lib_roots = list(_POSIX_SYSTEM_PYTHON_LIB_ROOTS)
        if system == "Darwin":
            lib_roots.extend(_DARWIN_SYSTEM_PYTHON_LIB_ROOTS)
        for root in lib_roots:
            for python_dir in _bounded_child_directories(
                root,
                name_prefix="python",
                checkpoint=checkpoint,
                windows_system_context=windows_system_context,
            ):
                candidates.extend(
                    (
                        python_dir / "site-packages",
                        python_dir / "dist-packages",
                    )
                )
        if system == "Darwin":
            for version_root in _bounded_child_directories(
                _DARWIN_FRAMEWORK_VERSIONS,
                checkpoint=checkpoint,
                windows_system_context=windows_system_context,
            ):
                candidates.extend(
                    _site_packages_for_env(
                        version_root,
                        checkpoint=checkpoint,
                        windows_system_context=windows_system_context,
                    )
                )
    return [
        candidate
        for candidate in candidates
        if resolved_directory_candidate(
            candidate,
            windows_system_context=windows_system_context,
            max_components=MAX_PATH_COMPONENTS,
        )
        is not None
    ]


def _site_packages_roots(
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
    python_env_roots: Iterable[Path],
    checkpoint: Callable[[], None] | None,
    windows_system_context: bool,
    include_system: bool = True,
) -> list[Path]:
    hidden_env_roots: list[Path] = []
    for env_root in islice(python_env_roots, MAX_CHILD_ENTRIES):
        if (
            resolved_directory_candidate(
                env_root,
                windows_system_context=windows_system_context,
                max_components=MAX_PATH_COMPONENTS,
            )
            is None
        ):
            continue
        hidden_env_roots.append(env_root)
        if len(hidden_env_roots) == MAX_ENV_ROOTS:
            break
    standard_env_roots = _standard_env_roots(
        home=home,
        system=system,
        environment=environment,
        checkpoint=checkpoint,
        windows_system_context=windows_system_context,
    )
    standard_site_packages = (
        site_packages
        for env_root in standard_env_roots
        for site_packages in _site_packages_for_env(
            env_root,
            checkpoint=checkpoint,
            windows_system_context=windows_system_context,
        )
    )
    hidden_site_packages = (
        site_packages
        for env_root in hidden_env_roots
        for site_packages in _site_packages_for_env(
            env_root,
            checkpoint=checkpoint,
            windows_system_context=windows_system_context,
        )
    )
    system_site_packages = (
        _system_site_packages(
            system,
            environment,
            checkpoint=checkpoint,
            windows_system_context=windows_system_context,
        )
        if include_system
        else ()
    )
    candidate_groups = (
        _user_site_packages(
            home,
            system,
            checkpoint=checkpoint,
            windows_system_context=windows_system_context,
        ),
        standard_site_packages,
        system_site_packages,
        hidden_site_packages,
    )
    roots: list[Path] = []
    seen: set[str] = set()
    for candidates in zip_longest(*candidate_groups):
        for candidate in candidates:
            if candidate is None:
                continue
            key = os.path.normcase(str(candidate.absolute()))
            if key not in seen:
                seen.add(key)
                roots.append(candidate)
            if len(roots) >= MAX_SITE_PACKAGES:
                return roots
    return roots


def scan_pip_global_packages(
    packages: Iterable[PipPackageSpec],
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
    python_env_roots: Iterable[Path] = (),
    wsl_homes: Iterable[Path] = (),
    discover_hidden: bool = True,
    checkpoint: Callable[[], None] | None = None,
) -> dict[str, PipGlobalPackage]:
    """Return first validated hit per exact allowlisted distribution identity."""
    package_list = tuple(packages)
    package_map = {
        canonical: package
        for package in package_list
        if (canonical := _canonical_name(package.name)) is not None
    }
    if not package_map:
        return {}
    windows_system = is_windows_system_context()
    env_roots = list(islice(python_env_roots, MAX_CHILD_ENTRIES))
    if discover_hidden:
        env_roots.extend(
            scan_hidden_spaces(
                home=home,
                system=system,
                include_files=False,
                temp_roots=(),
                checkpoint=checkpoint,
            ).python_env_roots
        )
    site_package_groups = [
        _site_packages_roots(
            home=home,
            system=system,
            environment=environment,
            python_env_roots=env_roots,
            checkpoint=checkpoint,
            windows_system_context=windows_system,
        )
    ]
    if system == "Windows":
        for wsl_home in islice(wsl_homes, MAX_WSL_HOMES_TOTAL):
            site_package_groups.append(
                _site_packages_roots(
                    home=wsl_home,
                    system="Linux",
                    environment={"HOME": str(wsl_home)},
                    python_env_roots=(),
                    checkpoint=checkpoint,
                    windows_system_context=windows_system,
                    include_system=False,
                )
            )
    site_packages_roots = list(
        islice(
            (
                path
                for group in zip_longest(*site_package_groups)
                for path in group
                if path is not None
            ),
            MAX_SITE_PACKAGES,
        )
    )
    scan_areas = [
        (site_packages, 0)
        for site_packages in site_packages_roots
        if not has_link_or_reparse_component(
            site_packages,
            max_components=MAX_PATH_COMPONENTS,
        )
        and is_real_directory(site_packages)
    ]
    committed_links: dict[str, Path] = {}
    # Per-root and per-item policies validate attempts; committed_targets owns the cap.
    committed_targets: set[str] = set()
    findings: dict[str, PipGlobalPackage] = {}
    for site_packages_path in site_packages_roots:
        if checkpoint is not None:
            checkpoint()
        symlink_policy = SymlinkFollowPolicy(
            scan_areas=scan_areas,
            max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
            windows_system_context=windows_system,
        )
        root_links = dict(committed_links)
        site_packages = resolve_approved_path(
            site_packages_path,
            policy=symlink_policy,
            approved_links=root_links,
            max_components=MAX_PATH_COMPONENTS,
        )
        if site_packages is None or not is_real_directory(site_packages):
            continue
        entry_names: list[str] = []
        try:
            with os.scandir(site_packages) as entries:
                for index, entry in enumerate(islice(entries, MAX_SITE_ENTRIES + 1)):
                    if index == MAX_SITE_ENTRIES:
                        break
                    if checkpoint is not None:
                        checkpoint()
                    entry_names.append(entry.name)
        except OSError:
            continue
        for entry_name in sorted(
            entry_names,
            key=lambda value: (value.casefold(), value),
        ):
            if len(findings) == len(package_map):
                return findings
            if not entry_name.casefold().endswith(".dist-info"):
                continue
            symlink_policy = SymlinkFollowPolicy(
                scan_areas=[*scan_areas, (site_packages, 0)],
                max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
                windows_system_context=windows_system,
            )
            attempt_links = dict(root_links)
            dist_info = resolve_relative_components(
                site_packages,
                (entry_name,),
                policy=symlink_policy,
                approved_links=attempt_links,
                max_components=MAX_PATH_COMPONENTS,
            )
            if dist_info is None or not is_real_directory(dist_info):
                continue
            symlink_policy.add_scan_area(dist_info, 0)
            metadata_path = resolve_relative_components(
                dist_info,
                ("METADATA",),
                policy=symlink_policy,
                approved_links=attempt_links,
                max_components=MAX_PATH_COMPONENTS,
                follow_final_symlink=False,
            )
            if metadata_path is None or not is_regular_file(metadata_path):
                continue
            raw = read_bounded(metadata_path, max_bytes=MAX_METADATA_BYTES)
            if raw is None:
                continue
            validated = _validated_metadata(raw, package_map)
            if validated is None:
                continue
            package, version = validated
            canonical = _canonical_name(package.name)
            if (
                canonical is not None
                and package.name not in findings
                and commit_approved_links(
                    committed_links,
                    committed_targets,
                    attempt_links,
                    max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
                )
            ):
                findings[package.name] = PipGlobalPackage(
                    package_name=package.name,
                    version=version,
                    metadata_path=metadata_path,
                )
    return findings
