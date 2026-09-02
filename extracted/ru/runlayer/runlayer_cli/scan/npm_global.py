"""Detect allowlisted globally installed npm packages without executing code."""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from dataclasses import dataclass
from itertools import islice
from pathlib import Path, PurePosixPath, PureWindowsPath
from string import Template, ascii_letters, digits
from typing import Iterable, Literal, Mapping, Protocol, cast

from runlayer_cli.scan.hidden_space_sweep import scan_hidden_spaces
from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    commit_approved_links,
    environment_value,
    has_link_or_reparse_component,
    is_link_or_reparse,
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
MAX_PREFIXES = 32
MAX_MANIFEST_BYTES = 512 * 1024
MAX_NPMRC_BYTES = 64 * 1024
MAX_MANAGER_ENTRIES = 64
MAX_MANAGER_PREFIXES = 8
MAX_NODE_MODULES_PATHS = 256
MAX_PATH_ENTRIES = 64
MAX_PATH_PREFIXES = 8
MAX_PREFIX_COMPONENTS = 64
MAX_VERSION_LENGTH = 128
_VERSION_INITIAL_CHARACTERS = frozenset(ascii_letters + digits)
_VERSION_CHARACTERS = _VERSION_INITIAL_CHARACTERS | frozenset("._+~-")


class NpmPackageSpec(Protocol):
    """Package identity consumed without importing the client registry."""

    name: str
    bin_name: str


@dataclass(frozen=True)
class NpmGlobalRoot:
    """One candidate npm prefix and its global-package layout."""

    prefix: Path
    layout: Literal["unix", "windows", "direct"]

    @property
    def node_modules(self) -> Path:
        if self.layout == "direct":
            return self.prefix
        if self.layout == "windows":
            return self.prefix / "node_modules"
        return self.prefix / "lib" / "node_modules"


@dataclass(frozen=True)
class NpmGlobalPackage:
    """Validated package metadata used as client-presence evidence."""

    package_name: str
    version: str
    manifest_path: Path


@dataclass(frozen=True)
class ValidatedNpmManifest:
    """Rename-resistant package identity parsed from bounded manifest bytes."""

    version: str
    bin_target: PurePosixPath


def _absolute_path(
    value: str,
    *,
    home: Path,
    environment: Mapping[str, str],
) -> Path | None:
    stripped = value.strip().strip("\"'")
    variables = dict(environment)
    variables["HOME"] = str(home)
    variables["USERPROFILE"] = str(home)
    try:
        stripped = Template(stripped).safe_substitute(variables)
    except ValueError:
        return None
    if stripped == "~":
        path = home
    elif stripped.startswith("~/") or stripped.startswith("~\\"):
        path = home / stripped[2:]
    else:
        path = Path(stripped)
    return path if path.is_absolute() else None


def _npmrc_prefix(
    path: Path,
    *,
    home: Path,
    environment: Mapping[str, str],
) -> Path | None:
    if is_link_or_reparse(path) or not is_regular_file(path):
        return None
    raw = read_bounded(path, max_bytes=MAX_NPMRC_BYTES)
    if raw is None:
        return None
    try:
        content = raw.decode()
    except UnicodeDecodeError:
        return None

    prefix: Path | None = None
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", ";")) or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip().casefold() == "prefix":
            prefix = _absolute_path(
                value,
                home=home,
                environment=environment,
            )
    return prefix


def _npmrc_paths(
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
) -> tuple[Path, ...]:
    paths: list[Path] = []
    configured = environment_value(environment, "NPM_CONFIG_USERCONFIG", system=system)
    if configured:
        configured_path = _absolute_path(
            configured,
            home=home,
            environment=environment,
        )
        if configured_path is not None:
            paths.append(configured_path)
    default = home / ".npmrc"
    if default not in paths:
        paths.append(default)
    return tuple(paths)


def _path_prefixes(
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
) -> tuple[Path, ...]:
    value = environment_value(environment, "PATH", system=system)
    if not value:
        return ()
    separator = ";" if system == "Windows" else ":"
    prefixes: list[Path] = []
    for entry in value.split(separator)[:MAX_PATH_ENTRIES]:
        path = _absolute_path(entry, home=home, environment=environment)
        if path is None:
            continue
        if system == "Windows":
            prefix = path
        elif path.name == "bin":
            prefix = path.parent
        else:
            continue
        prefixes.append(prefix)
        if len(prefixes) == MAX_PATH_PREFIXES:
            break
    return tuple(prefixes)


def _bounded_child_dirs(
    root: Path,
    *,
    name_prefix: str = "",
    checkpoint: Callable[[], None] | None = None,
    windows_system_context: bool = False,
) -> list[Path]:
    children: list[Path] = []
    resolved_root = resolved_directory_candidate(
        root,
        windows_system_context=windows_system_context,
        max_components=MAX_PREFIX_COMPONENTS,
    )
    if resolved_root is None:
        return []
    try:
        with os.scandir(resolved_root) as entries:
            for index, entry in enumerate(islice(entries, MAX_MANAGER_ENTRIES + 1)):
                if index == MAX_MANAGER_ENTRIES:
                    break
                if checkpoint is not None:
                    checkpoint()
                if name_prefix and not entry.name.startswith(name_prefix):
                    continue
                path = root / entry.name
                if is_link_or_reparse(path):
                    children.append(path)
                    continue
                try:
                    if not entry.is_dir(follow_symlinks=False):
                        continue
                except OSError:
                    continue
                children.append(path)
    except OSError:
        return []
    children.sort(key=lambda path: path.name)
    return children


def _node_manager_prefixes(
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
    checkpoint: Callable[[], None] | None = None,
    windows_system_context: bool = False,
) -> tuple[Path, ...]:
    roots: list[tuple[Path, str, str | None]] = []

    # Volta's node images hold only runtimes (npm/corepack); its sandboxed
    # global packages are resolved separately in _volta_package_prefixes.
    for key, suffix, child_suffix in (
        ("NVM_DIR", ("versions", "node"), None),
        ("FNM_DIR", ("node-versions",), "installation"),
        ("VOLTA_HOME", ("tools", "image", "node"), None),
    ):
        configured = environment_value(environment, key, system=system)
        if not configured:
            continue
        configured_path = _absolute_path(
            configured,
            home=home,
            environment=environment,
        )
        if configured_path is not None:
            roots.append((configured_path.joinpath(*suffix), "", child_suffix))

    # Default manager trees must stay probed directly, not via the home crawl:
    # privileged hook-install reconciliation and WSL homes resolve without the
    # user's shell environment, and the crawl prunes AppData and
    # Library/Application Support where nvm/fnm install by default.
    if system == "Windows":
        app_data_value = environment_value(environment, "APPDATA", system=system)
        app_data = (
            Path(app_data_value) if app_data_value else home / "AppData" / "Roaming"
        )
        roots.extend(
            [
                (app_data / "nvm", "v", None),
                (app_data / "fnm" / "node-versions", "", "installation"),
            ]
        )
    else:
        roots.extend(
            [
                (home / ".nvm" / "versions" / "node", "", None),
                (
                    home / ".local" / "share" / "fnm" / "node-versions",
                    "",
                    "installation",
                ),
                (home / ".asdf" / "installs" / "nodejs", "", None),
                (home / ".mise" / "installs" / "node", "", None),
            ]
        )
        if system == "Darwin":
            roots.append(
                (
                    home / "Library" / "Application Support" / "fnm" / "node-versions",
                    "",
                    "installation",
                )
            )

    prefixes: list[Path] = []
    for root, name_prefix, child_suffix in roots:
        if len(prefixes) == MAX_MANAGER_PREFIXES:
            break
        children = _bounded_child_dirs(
            root,
            name_prefix=name_prefix,
            checkpoint=checkpoint,
            windows_system_context=windows_system_context,
        )
        for child in children:
            candidate = child / child_suffix if child_suffix else child
            node_modules = (
                candidate / "node_modules"
                if system == "Windows"
                else candidate / "lib" / "node_modules"
            )
            if (
                resolved_directory_candidate(
                    candidate,
                    windows_system_context=windows_system_context,
                    max_components=MAX_PREFIX_COMPONENTS,
                )
                is None
                or resolved_directory_candidate(
                    node_modules,
                    windows_system_context=windows_system_context,
                    max_components=MAX_PREFIX_COMPONENTS,
                )
                is None
            ):
                continue
            prefixes.append(candidate)
            if len(prefixes) == MAX_MANAGER_PREFIXES:
                break
    return tuple(prefixes)


def _volta_package_prefixes(
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
    package_names: Iterable[str],
) -> tuple[Path, ...]:
    """Volta sandboxes each global package as its own npm-prefix-shaped image.

    There is no shared global node_modules: ``volta install <pkg>`` lands in
    ``$VOLTA_HOME/tools/image/packages/<name>/`` (scoped names nest one extra
    directory), so candidate prefixes come straight from the allowlist instead
    of directory enumeration.
    """
    volta_home = home / ".volta"
    configured = environment_value(environment, "VOLTA_HOME", system=system)
    if configured:
        configured_path = _absolute_path(
            configured,
            home=home,
            environment=environment,
        )
        if configured_path is None:
            return ()
        volta_home = configured_path
    packages_root = volta_home / "tools" / "image" / "packages"
    prefixes: list[Path] = []
    for name in islice(package_names, MAX_PREFIXES):
        components = _package_components(name)
        if components is not None:
            prefixes.append(packages_root.joinpath(*components))
    return tuple(prefixes)


def resolve_npm_global_roots(
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
    wsl_homes: Iterable[Path] = (),
    package_names: Iterable[str] = (),
    checkpoint: Callable[[], None] | None = None,
    windows_system_context: bool = False,
) -> tuple[NpmGlobalRoot, ...]:
    """Return bounded candidate prefixes in deterministic precedence order."""
    layout: Literal["unix", "windows"] = "windows" if system == "Windows" else "unix"
    package_name_list = tuple(package_names)
    candidates: list[Path] = []
    configured_prefix = environment_value(
        environment, "NPM_CONFIG_PREFIX", system=system
    )
    if configured_prefix:
        resolved_prefix = _absolute_path(
            configured_prefix,
            home=home,
            environment=environment,
        )
        if resolved_prefix is not None:
            candidates.append(resolved_prefix)
    for npmrc_path in _npmrc_paths(
        home=home,
        system=system,
        environment=environment,
    ):
        if checkpoint is not None:
            checkpoint()
        npmrc_prefix = _npmrc_prefix(
            npmrc_path,
            home=home,
            environment=environment,
        )
        if npmrc_prefix is not None:
            candidates.append(npmrc_prefix)
    candidates.extend(_path_prefixes(home=home, system=system, environment=environment))
    candidates.extend(
        _node_manager_prefixes(
            home=home,
            system=system,
            environment=environment,
            checkpoint=checkpoint,
            windows_system_context=windows_system_context,
        )
    )
    candidates.extend(
        _volta_package_prefixes(
            home=home,
            system=system,
            environment=environment,
            package_names=package_name_list,
        )
    )
    candidates.extend([home / ".npm-global", home / ".local", home])
    if system == "Windows":
        app_data = environment_value(environment, "APPDATA", system=system)
        candidates.append(
            Path(app_data) / "npm"
            if app_data
            else home / "AppData" / "Roaming" / "npm",
        )
    else:
        candidates.extend([Path("/usr/local"), Path("/usr")])
        if system == "Darwin":
            candidates.append(Path("/opt/homebrew"))

    seen: set[tuple[str, str]] = set()
    roots: list[NpmGlobalRoot] = []
    for candidate in candidates:
        if checkpoint is not None:
            checkpoint()
        path_key = str(candidate).casefold() if system == "Windows" else str(candidate)
        key = (layout, path_key)
        if key in seen:
            continue
        seen.add(key)
        roots.append(NpmGlobalRoot(prefix=candidate, layout=layout))
        if len(roots) == MAX_PREFIXES:
            break

    if system == "Windows" and len(roots) < MAX_PREFIXES:
        for wsl_home in islice(wsl_homes, MAX_WSL_HOMES_TOTAL):
            if checkpoint is not None:
                checkpoint()
            wsl_candidates: list[Path] = []
            wsl_environment = {"HOME": str(wsl_home)}
            npmrc_prefix = _npmrc_prefix(
                wsl_home / ".npmrc",
                home=wsl_home,
                environment=wsl_environment,
            )
            if npmrc_prefix is not None:
                wsl_candidates.append(npmrc_prefix)
            wsl_candidates.extend(
                [
                    wsl_home / ".npm-global",
                    wsl_home / ".local",
                    wsl_home,
                ]
            )
            # WSL trees are outside the home crawl and carry no shell
            # environment, so default manager roots are the only way in.
            wsl_candidates.extend(
                _node_manager_prefixes(
                    home=wsl_home,
                    system="Linux",
                    environment=wsl_environment,
                    checkpoint=checkpoint,
                    windows_system_context=windows_system_context,
                )
            )
            wsl_candidates.extend(
                _volta_package_prefixes(
                    home=wsl_home,
                    system="Linux",
                    environment=wsl_environment,
                    package_names=package_name_list,
                )
            )
            for candidate in wsl_candidates:
                if checkpoint is not None:
                    checkpoint()
                key = ("unix", str(candidate))
                if key in seen:
                    continue
                seen.add(key)
                roots.append(NpmGlobalRoot(prefix=candidate, layout="unix"))
                if len(roots) == MAX_PREFIXES:
                    return tuple(roots)
    return tuple(roots)


def _direct_node_modules_roots(
    paths: Iterable[Path],
    *,
    system: str,
    existing_roots: Iterable[NpmGlobalRoot],
) -> tuple[NpmGlobalRoot, ...]:
    """Normalize bounded crawl discoveries into direct package roots."""
    windows = system == "Windows"

    def key(path: Path) -> str:
        value = str(path)
        return value.casefold() if windows else value

    seen = {key(root.node_modules) for root in existing_roots}
    roots: list[NpmGlobalRoot] = []
    for path in islice(paths, MAX_NODE_MODULES_PATHS):
        if path.name.casefold() != "node_modules":
            continue
        path_key = key(path)
        if path_key in seen:
            continue
        seen.add(path_key)
        roots.append(NpmGlobalRoot(prefix=path, layout="direct"))
    return tuple(roots)


def _contained_path(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, RuntimeError, ValueError):
        return False
    return True


def _package_components(package_name: str) -> tuple[str, ...] | None:
    components = tuple(package_name.split("/"))
    if package_name.startswith("@"):
        valid = (
            len(components) == 2
            and components[0].startswith("@")
            and len(components[0]) > 1
            and bool(components[1])
        )
    else:
        valid = len(components) == 1 and bool(components[0])
    if not valid or any(part in {".", ".."} for part in components):
        return None
    return components


def _valid_version(value: object) -> str | None:
    if (
        isinstance(value, str)
        and 0 < len(value) <= MAX_VERSION_LENGTH
        and value[0] in _VERSION_INITIAL_CHARACTERS
        and all(character in _VERSION_CHARACTERS for character in value)
    ):
        return value
    return None


def _bin_target(
    manifest: Mapping[str, object],
    package: NpmPackageSpec,
) -> str | None:
    value = manifest.get("bin")
    if isinstance(value, dict):
        target = cast(dict[str, object], value).get(package.bin_name)
        return target if isinstance(target, str) else None
    package_basename = package.name.rsplit("/", 1)[-1]
    if isinstance(value, str) and package.bin_name == package_basename:
        return value
    return None


def _safe_relative_target(value: str) -> PurePosixPath | None:
    windows_path = PureWindowsPath(value)
    normalized = PurePosixPath(value.replace("\\", "/"))
    if (
        not value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
        or windows_path.is_absolute()
        or normalized.is_absolute()
        or ".." in normalized.parts
    ):
        return None
    return normalized


def validate_npm_manifest(
    raw: bytes,
    package: NpmPackageSpec,
) -> ValidatedNpmManifest | None:
    """Validate exact package identity without executing package code."""
    if not raw or len(raw) > MAX_MANIFEST_BYTES:
        return None
    try:
        manifest = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(manifest, dict) or manifest.get("name") != package.name:
        return None
    version = _valid_version(manifest.get("version"))
    target_value = _bin_target(manifest, package)
    target_relative = (
        _safe_relative_target(target_value) if target_value is not None else None
    )
    if version is None or target_relative is None:
        return None
    return ValidatedNpmManifest(version=version, bin_target=target_relative)


def _read_valid_package(
    root: NpmGlobalRoot,
    package: NpmPackageSpec,
    *,
    policy: SymlinkFollowPolicy,
    approved_links: dict[str, Path],
) -> NpmGlobalPackage | None:
    components = _package_components(package.name)
    if components is None:
        return None

    resolved_prefix = resolve_approved_path(
        root.prefix,
        policy=policy,
        approved_links=approved_links,
        max_components=MAX_PREFIX_COMPONENTS,
    )
    if resolved_prefix is None or not is_real_directory(resolved_prefix):
        return None
    if root.layout == "unix":
        node_modules = resolve_relative_components(
            resolved_prefix,
            ("lib", "node_modules"),
            policy=policy,
            approved_links=approved_links,
            max_components=MAX_PREFIX_COMPONENTS,
        )
    elif root.layout == "windows":
        node_modules = resolve_relative_components(
            resolved_prefix,
            ("node_modules",),
            policy=policy,
            approved_links=approved_links,
            max_components=MAX_PREFIX_COMPONENTS,
        )
    else:
        node_modules = resolved_prefix
    if node_modules is None or not is_real_directory(node_modules):
        return None
    policy.add_scan_area(node_modules, 0)

    package_dir = resolve_relative_components(
        node_modules,
        components,
        policy=policy,
        approved_links=approved_links,
        max_components=MAX_PREFIX_COMPONENTS,
    )
    if package_dir is None or not is_real_directory(package_dir):
        return None
    if not _contained_path(package_dir, node_modules):
        policy.add_scan_area(package_dir, 0)

    manifest_path = resolve_relative_components(
        package_dir,
        ("package.json",),
        policy=policy,
        approved_links=approved_links,
        max_components=MAX_PREFIX_COMPONENTS,
        follow_final_symlink=False,
    )
    if manifest_path is None or not is_regular_file(manifest_path):
        return None

    raw = read_bounded(manifest_path, max_bytes=MAX_MANIFEST_BYTES)
    if raw is None:
        return None
    manifest = validate_npm_manifest(raw, package)
    if manifest is None:
        return None

    target_path = resolve_relative_components(
        package_dir,
        manifest.bin_target.parts,
        policy=policy,
        approved_links=approved_links,
        max_components=MAX_PREFIX_COMPONENTS,
        follow_final_symlink=False,
    )
    if target_path is None or not is_regular_file(target_path):
        return None
    return NpmGlobalPackage(
        package_name=package.name,
        version=manifest.version,
        manifest_path=manifest_path,
    )


def scan_npm_global_packages(
    packages: Iterable[NpmPackageSpec],
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
    wsl_homes: Iterable[Path] = (),
    node_modules_paths: Iterable[Path] = (),
    discover_hidden: bool = True,
    checkpoint: Callable[[], None] | None = None,
) -> dict[str, NpmGlobalPackage]:
    """Return first validated hit per exact allowlisted package identity."""
    package_list = tuple(packages)
    if not package_list:
        return {}
    windows_system = is_windows_system_context()
    wsl_home_list = tuple(islice(wsl_homes, MAX_WSL_HOMES_TOTAL))
    discovered_node_modules = list(islice(node_modules_paths, MAX_NODE_MODULES_PATHS))
    if discover_hidden:
        discovered_node_modules.extend(
            scan_hidden_spaces(
                home=home,
                system=system,
                include_files=False,
                temp_roots=(),
                checkpoint=checkpoint,
            ).node_modules_paths
        )
        for wsl_home in wsl_home_list:
            discovered_node_modules.extend(
                scan_hidden_spaces(
                    home=wsl_home,
                    system="Linux",
                    include_files=False,
                    temp_roots=(),
                    checkpoint=checkpoint,
                ).node_modules_paths
            )
    resolved_roots = resolve_npm_global_roots(
        home=home,
        system=system,
        environment=environment,
        wsl_homes=wsl_home_list,
        package_names=(package.name for package in package_list),
        checkpoint=checkpoint,
        windows_system_context=windows_system,
    )
    roots = (
        *resolved_roots,
        *_direct_node_modules_roots(
            discovered_node_modules,
            system=system,
            existing_roots=resolved_roots,
        ),
    )
    scan_areas = [
        (root.node_modules, 0)
        for root in roots
        if not has_link_or_reparse_component(
            root.node_modules,
            max_components=MAX_PREFIX_COMPONENTS,
        )
        and is_real_directory(root.node_modules)
    ]
    committed_links: dict[str, Path] = {}
    committed_targets: set[str] = set()
    findings: dict[str, NpmGlobalPackage] = {}
    for root in roots:
        for package in package_list:
            if checkpoint is not None:
                checkpoint()
            if package.name in findings:
                continue
            try:
                # This policy validates one attempt; committed_targets owns the cap.
                symlink_policy = SymlinkFollowPolicy(
                    scan_areas=scan_areas,
                    max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
                    windows_system_context=windows_system,
                )
                attempt_links = dict(committed_links)
                finding = _read_valid_package(
                    root,
                    package,
                    policy=symlink_policy,
                    approved_links=attempt_links,
                )
            except Exception:
                finding = None
            if finding is not None and commit_approved_links(
                committed_links,
                committed_targets,
                attempt_links,
                max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
            ):
                findings[package.name] = finding
    return findings
