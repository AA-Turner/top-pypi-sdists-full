"""Detect installed AI clients independently of configured MCP servers."""

from __future__ import annotations

import importlib
import os
import platform
import plistlib
from dataclasses import dataclass, field
from itertools import islice, zip_longest
from pathlib import Path
from typing import Any, Callable, Iterable, Literal, Mapping, cast

import structlog

from runlayer_cli import regex_safe
from runlayer_cli.hook_install import runlayer_written_hook_artifact_paths
from runlayer_cli.scan.bin_shims import ShimFinding, sweep_shim_identities
from runlayer_cli.scan.cli_binaries import get_cli_version, locate_cli_binary
from runlayer_cli.scan.clients import (
    MCPClientDefinition,
    PlatformPath,
    _resolve_wsl_linux_paths,
    _wsl_homes,
)
from runlayer_cli.scan.device import DiscoveredWSLDistro, get_wsl_distro_inventory
from runlayer_cli.scan.hidden_space_sweep import (
    HiddenSpaceScanResult,
    scan_hidden_spaces,
)
from runlayer_cli.scan.npm_global import NpmGlobalPackage, scan_npm_global_packages
from runlayer_cli.scan.pip_global import PipGlobalPackage, scan_pip_global_packages
from runlayer_cli.scan.resource_governor import ScanResourceLimitExceeded
from runlayer_cli.scan.wsl_presence import (
    WSLBinaryFinding,
    WSLClientContext,
    scan_wsl_cli_binaries,
)
from runlayer_cli.scan.wsl_limits import MAX_WSL_CLIENT_CONTEXTS, MAX_WSL_HOMES_TOTAL
from runlayer_cli.scan.wsl_paths import parse_wsl_unc_path

logger = structlog.get_logger(__name__)

DetectionMethod = Literal[
    "app",
    "cli",
    "registry",
    "npm_global",
    "pip_global",
    "container",
    "config",
    "trace",
    "server",
    "skill",
    "plugin",
    "extension",
]

# Mirrored in docs/shadow-ai/detect/index.mdx ("AI Client Detection"); kept in
# lockstep by tests/test_docs_client_sync.py.
DETECTION_METHOD_ORDER: tuple[DetectionMethod, ...] = (
    "app",
    "cli",
    "registry",
    "npm_global",
    "pip_global",
    "container",
    "config",
    "trace",
    "server",
    "skill",
    "plugin",
    "extension",
)

_EXECUTABLE_SUFFIXES = {".exe", ".cmd", ".bat"}
_EXTENSION_HOST_DIRS = (
    ".vscode",
    ".vscode-insiders",
    ".vscode-oss",
    ".cursor",
    ".windsurf",
    ".vscode-server",
    ".vscode-server-insiders",
    ".cursor-server",
    ".windsurf-server",
)
_WINDOWS_ENV_PATTERN = regex_safe.compile(r"%([^%]+)%")
_DOLLAR_ENV_PATTERN = regex_safe.compile(
    r"\$(?:\{(?P<braced>[A-Za-z_][A-Za-z0-9_]*)\}|(?P<plain>[A-Za-z_][A-Za-z0-9_]*))"
)
_MAX_VERSIONED_CONFIG_DIRS = 64
_WINDOWS_USER_SID_UNSET = object()


@dataclass
class DetectedClient:
    """One installed client and the independent signals that identified it."""

    client: str
    display_name: str
    client_version: str | None = None
    detected_via: list[DetectionMethod] = field(default_factory=list)
    config_paths: list[str] = field(default_factory=list)
    wsl_contexts: list[WSLClientContext] = field(default_factory=list)
    container_ids: list[str] = field(default_factory=list, repr=False)

    def add_detection(
        self,
        method: DetectionMethod,
        *,
        version: str | None = None,
        config_path: Path | str | None = None,
        container_id: str | None = None,
        wsl_context: WSLClientContext | None = None,
    ) -> None:
        """Merge one signal while preserving a deterministic wire shape."""
        if method not in self.detected_via:
            self.detected_via.append(method)
            self.detected_via.sort(key=DETECTION_METHOD_ORDER.index)
        if self.client_version is None and version:
            self.client_version = version
        if config_path is not None:
            path = str(config_path)
            if path not in self.config_paths:
                self.config_paths.append(path)
                self.config_paths.sort()
        if container_id is not None and container_id not in self.container_ids:
            self.container_ids.append(container_id)
            self.container_ids.sort()
        if (
            wsl_context is not None
            and wsl_context not in self.wsl_contexts
            and len(self.wsl_contexts) < MAX_WSL_CLIENT_CONTEXTS
        ):
            self.wsl_contexts.append(wsl_context)
            self.wsl_contexts.sort(
                key=lambda context: (
                    context.distro.casefold(),
                    (context.user or "").casefold(),
                )
            )


@dataclass(frozen=True)
class _ConfigPresenceCandidate:
    path: Path
    template: str
    kind: Literal["configured_path", "file", "dir"]


def _safe_is_file(path: Path) -> bool:
    try:
        return path.is_file()
    except OSError:
        return False


def _safe_is_dir(path: Path) -> bool:
    try:
        return path.is_dir()
    except OSError:
        return False


def _wsl_context_for_path(path: Path) -> WSLClientContext | None:
    parsed = parse_wsl_unc_path(path)
    if parsed is None:
        return None
    return WSLClientContext(distro=parsed.distro, user=parsed.user)


def _filter_hidden_package_roots(
    paths: Iterable[Path],
    *,
    system: str,
    wsl_homes: Iterable[Path],
) -> tuple[Path, ...]:
    """Keep host roots and roots from only the selected WSL home contexts."""
    if system != "Windows":
        return tuple(paths)

    selected_contexts = {
        (parsed.distro.casefold(), parsed.user)
        for home in wsl_homes
        if (parsed := parse_wsl_unc_path(home)) is not None
    }
    return tuple(
        path
        for path in paths
        if (parsed := parse_wsl_unc_path(path)) is None
        or (parsed.distro.casefold(), parsed.user) in selected_contexts
    )


def _path_parts_equal(left: str, right: str, *, system: str) -> bool:
    if system == "Windows":
        return left.casefold() == right.casefold()
    return left == right


def _relative_path_parts(
    path: Path,
    parent: Path,
    *,
    system: str,
) -> tuple[str, ...] | None:
    path_parts = path.parts
    parent_parts = parent.parts
    if len(path_parts) < len(parent_parts):
        return None
    if not all(
        _path_parts_equal(path_part, parent_part, system=system)
        for path_part, parent_part in zip(path_parts, parent_parts)
    ):
        return None
    return path_parts[len(parent_parts) :]


def _is_runlayer_written_artifact(
    path: Path,
    artifacts: Iterable[Path],
    *,
    system: str,
) -> bool:
    return any(
        _relative_path_parts(path, artifact, system=system) == ()
        for artifact in artifacts
    )


def _presence_artifact_paths(
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
) -> frozenset[Path]:
    """Runlayer hook artifacts for every home this scan resolves paths under.

    A Windows scan also probes WSL user homes, where Runlayer hook artifacts sit
    at their Linux paths. Windows-profile artifact paths never match those, so a
    WSL tree holding nothing but a Runlayer hook install would otherwise read as
    client evidence.
    """
    artifacts = set(
        runlayer_written_hook_artifact_paths(
            home=home,
            system=system,
            environment=environment,
        )
    )
    if system == "Windows":
        for wsl_home in _wsl_homes():
            artifacts |= runlayer_written_hook_artifact_paths(
                home=wsl_home,
                system="Linux",
                # Host overrides (APPDATA, COPILOT_HOME) describe Windows paths,
                # not paths inside a WSL distro.
                environment={},
            )
    return frozenset(artifacts)


def _directory_has_presence_trace(
    directory: Path,
    artifacts: Iterable[Path],
    *,
    system: str,
) -> bool:
    """Ignore only trees made entirely from known Runlayer artifact paths.

    Traversal follows known artifact-prefix directories only. An unrelated
    direct child is enough evidence, so arbitrary client trees are never walked.
    A genuinely empty candidate remains weak evidence on its own.
    """
    suffixes = tuple(
        suffix
        for artifact in artifacts
        if (suffix := _relative_path_parts(artifact, directory, system=system))
    )

    def inspect(
        current: Path,
        expected_suffixes: tuple[tuple[str, ...], ...],
        *,
        empty_is_trace: bool,
    ) -> bool:
        saw_child = False
        try:
            children = current.iterdir()
            for child in children:
                saw_child = True
                matching = tuple(
                    suffix[1:]
                    for suffix in expected_suffixes
                    if _path_parts_equal(child.name, suffix[0], system=system)
                )
                if not matching:
                    return True

                exact_match = () in matching
                nested_matches = tuple(suffix for suffix in matching if suffix)
                if exact_match and not nested_matches:
                    if _safe_is_dir(child):
                        return True
                    continue
                if child.is_symlink() or not _safe_is_dir(child):
                    return True
                if inspect(
                    child,
                    nested_matches,
                    empty_is_trace=False,
                ):
                    return True
        except OSError:
            return False
        return empty_is_trace and not saw_child

    return inspect(directory, suffixes, empty_is_trace=True)


def _expand_environment_vars(
    value: str,
    environment: Mapping[str, str],
    *,
    system: str,
) -> str:
    """Expand Windows and POSIX variable syntax from an explicit environment."""
    casefolded = {key.casefold(): item for key, item in environment.items()}

    def replace_windows(match: regex_safe.Match) -> str:
        name = match.group(1)
        return environment.get(name, casefolded.get(name.casefold(), match.group(0)))

    def replace_dollar(match: regex_safe.Match) -> str:
        name = match.group("braced") or match.group("plain")
        if system == "Windows":
            return environment.get(
                name, casefolded.get(name.casefold(), match.group(0))
            )
        return environment.get(name, match.group(0))

    expanded = _WINDOWS_ENV_PATTERN.sub(replace_windows, value)
    return _DOLLAR_ENV_PATTERN.sub(replace_dollar, expanded)


def _resolve_platform_path(
    path_def: PlatformPath,
    *,
    system: str,
    home: Path,
    environment: Mapping[str, str],
) -> Path | None:
    current_platform = {
        "Darwin": "macos",
        "Windows": "windows",
        "Linux": "linux",
    }.get(system)
    if path_def.platform != "all" and path_def.platform != current_platform:
        return None

    expanded = _expand_environment_vars(
        path_def.path,
        environment,
        system=system,
    )
    if expanded == "~":
        resolved = home
    elif expanded.startswith("~/") or expanded.startswith("~\\"):
        resolved = home / expanded[2:]
    else:
        resolved = Path(expanded).expanduser()
    return resolved if resolved.is_absolute() else None


def _macos_app_roots(home: Path) -> tuple[Path, Path]:
    return Path("/Applications"), home / "Applications"


def _macos_app_version(bundle: Path) -> str | None:
    info_plist = bundle / "Contents" / "Info.plist"
    try:
        with info_plist.open("rb") as file:
            info = plistlib.load(file)
    except (OSError, plistlib.InvalidFileException):
        return None
    if not isinstance(info, dict):
        return None
    version = info.get("CFBundleShortVersionString")
    return str(version) if version is not None else None


def _vscode_extension_version(remainder: str) -> str | None:
    match = regex_safe.match(r"^\d+(?:\.\d+)*", remainder)
    return match.group(0) if match else None


def _detect_vscode_extension_presence(
    detected: DetectedClient,
    *,
    system: str,
    home: Path,
    extension_ids: Iterable[str],
) -> None:
    prefixes = tuple(
        (f"{extension_id}-".casefold(), len(extension_id) + 1)
        for extension_id in extension_ids
    )
    if not prefixes:
        return

    def scan_extension_roots(
        extension_home: Path,
        method: Literal["app", "config"],
    ) -> None:
        for host_dir in _EXTENSION_HOST_DIRS:
            root = extension_home / host_dir / "extensions"
            try:
                for child in root.iterdir():
                    if not _safe_is_dir(child):
                        continue
                    child_name = child.name
                    casefolded_name = child_name.casefold()
                    for prefix, remainder_start in prefixes:
                        if casefolded_name.startswith(prefix):
                            detected.add_detection(
                                method,
                                version=_vscode_extension_version(
                                    child_name[remainder_start:]
                                ),
                                config_path=child if method == "config" else None,
                            )
                            break
            except OSError:
                continue

    scan_extension_roots(home, "app")
    if system == "Windows":
        try:
            wsl_homes = _wsl_homes()
        except OSError:
            return
        for wsl_home in wsl_homes:
            scan_extension_roots(wsl_home, "config")


def _linux_desktop_roots(home: Path) -> tuple[Path, ...]:
    return (
        Path("/usr/share/applications"),
        home / ".local/share/applications",
        Path("/var/lib/flatpak/exports/share/applications"),
        home / ".local/share/flatpak/exports/share/applications",
        Path("/var/lib/snapd/desktop/applications"),
    )


def _windows_install_present(path: Path) -> bool:
    if _safe_is_file(path):
        return path.suffix.lower() in _EXECUTABLE_SUFFIXES
    if not _safe_is_dir(path):
        return False
    try:
        return any(
            _safe_is_file(child) and child.suffix.lower() in _EXECUTABLE_SUFFIXES
            for child in path.iterdir()
        )
    except OSError:
        return False


def _windows_uninstall_entries(
    user_sid: str | None | object = _WINDOWS_USER_SID_UNSET,
) -> list[tuple[str, str | None]]:
    """Read uninstall entries from machine hives and the intended user hive.

    No-argument callers retain the historical ``HKCU`` probe. Supplying a SID
    reads that user's ``HKU`` hive instead; explicitly supplying ``None`` skips
    user-level registry detection, which prevents SYSTEM's ``HKCU`` from being
    mistaken for the console user's state.
    """
    try:
        # winreg is a Windows-only stdlib module; import lazily so this module stays cross-platform.
        winreg = cast(Any, importlib.import_module("winreg"))
    except ImportError:
        return []

    uninstall = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    locations = [
        (winreg.HKEY_LOCAL_MACHINE, uninstall),
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        ),
    ]
    if user_sid is _WINDOWS_USER_SID_UNSET:
        locations.append((winreg.HKEY_CURRENT_USER, uninstall))
    elif isinstance(user_sid, str):
        locations.append((winreg.HKEY_USERS, rf"{user_sid}\{uninstall}"))
    entries: list[tuple[str, str | None]] = []
    for hive, key_path in locations:
        try:
            root = winreg.OpenKey(hive, key_path)
        except OSError:
            continue
        try:
            index = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(root, index)
                except OSError:
                    break
                index += 1
                try:
                    subkey = winreg.OpenKey(root, subkey_name)
                except OSError:
                    continue
                try:
                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    try:
                        display_version = winreg.QueryValueEx(subkey, "DisplayVersion")[
                            0
                        ]
                    except OSError:
                        display_version = None
                except OSError:
                    continue
                finally:
                    winreg.CloseKey(subkey)
                if isinstance(display_name, str):
                    version = (
                        str(display_version) if display_version is not None else None
                    )
                    entries.append((display_name, version))
        finally:
            winreg.CloseKey(root)
    return entries


def _template_has_specific_parent(template: str) -> bool:
    normalized = template.replace("\\", "/")
    if normalized.startswith("~/"):
        return "/" in normalized[2:]
    percent_match = regex_safe.match(r"^%[^%]+%/(.+)$", normalized)
    if percent_match:
        return "/" in percent_match.group(1)
    dollar_match = regex_safe.match(r"^\$[A-Za-z_][A-Za-z0-9_]*/(.+)$", normalized)
    if dollar_match:
        return "/" in dollar_match.group(1)
    return True


def _meaningful_config_parent(path: Path, *, template: str, home: Path) -> Path | None:
    parent = path.parent
    if not _template_has_specific_parent(template):
        return None
    try:
        if parent.resolve() == home.resolve():
            return None
    except OSError:
        if parent == home:
            return None
    if parent == Path(parent.anchor):
        return None
    return parent


def _resolved_config_candidates(
    client: MCPClientDefinition,
    *,
    system: str,
    home: Path,
    environment: Mapping[str, str],
) -> Iterable[_ConfigPresenceCandidate]:
    """Yield resolved config and state candidates with their probe semantics."""

    def _expanded_paths(path: Path) -> tuple[Path, ...]:
        pattern = path.name
        if not any(character in pattern for character in "*?["):
            return (path,)
        if any(character in str(path.parent) for character in "*?["):
            return ()
        try:
            matches = islice(
                path.parent.glob(pattern),
                _MAX_VERSIONED_CONFIG_DIRS,
            )
            return tuple(sorted(matches))
        except OSError:
            return ()

    def _yield_for(
        path_defs: Iterable[PlatformPath],
        kind: Literal["configured_path", "file", "dir"],
    ) -> Iterable[_ConfigPresenceCandidate]:
        for path_def in path_defs:
            resolved = _resolve_platform_path(
                path_def,
                system=system,
                home=home,
                environment=environment,
            )
            if resolved is not None:
                for candidate_path in _expanded_paths(resolved):
                    yield _ConfigPresenceCandidate(
                        path=candidate_path,
                        template=path_def.path,
                        kind=kind,
                    )
            if system == "Windows" and path_def.platform in {"all", "linux"}:
                for wsl_path in _resolve_wsl_linux_paths(path_def.path):
                    for candidate_path in _expanded_paths(wsl_path):
                        yield _ConfigPresenceCandidate(
                            path=candidate_path,
                            template=path_def.path,
                            kind=kind,
                        )

    yield from _yield_for(client.paths, "configured_path")

    probe = client.install_probe
    if probe is None:
        return
    yield from _yield_for(probe.config_files, "file")
    yield from _yield_for(probe.config_dirs, "dir")


def _detect_config_presence(
    detected: DetectedClient,
    client: MCPClientDefinition,
    *,
    system: str,
    home: Path,
    environment: Mapping[str, str],
) -> None:
    try:
        runlayer_artifacts = _presence_artifact_paths(
            home=home,
            system=system,
            environment=environment,
        )
        for candidate in _resolved_config_candidates(
            client,
            system=system,
            home=home,
            environment=environment,
        ):
            if candidate.kind == "dir":
                if _safe_is_dir(candidate.path):
                    if _directory_has_presence_trace(
                        candidate.path,
                        runlayer_artifacts,
                        system=system,
                    ):
                        detected.add_detection("trace", config_path=candidate.path)
                continue

            exact_file_exists = _safe_is_file(candidate.path)
            exact_file_is_runlayer_artifact = _is_runlayer_written_artifact(
                candidate.path,
                runlayer_artifacts,
                system=system,
            )
            if exact_file_exists and not exact_file_is_runlayer_artifact:
                detected.add_detection("config", config_path=candidate.path)
                continue

            if candidate.kind == "configured_path" and (
                client.install_probe is None
                or client.install_probe.probe_config_parents
            ):
                parent = _meaningful_config_parent(
                    candidate.path,
                    template=candidate.template,
                    home=home,
                )
                if (
                    parent is not None
                    and _safe_is_dir(parent)
                    and _directory_has_presence_trace(
                        parent,
                        runlayer_artifacts,
                        system=system,
                    )
                ):
                    detected.add_detection("trace", config_path=parent)
    except (OSError, RuntimeError):
        return


def _probe_client_presence(
    detected: DetectedClient,
    client: MCPClientDefinition,
    *,
    system: str,
    home: Path,
    environment: Mapping[str, str],
    registry_entries: Iterable[tuple[str, str | None]],
    npm_findings: Mapping[str, NpmGlobalPackage],
    pip_findings: Mapping[str, PipGlobalPackage],
    shim_findings_by_basename: Mapping[str, list[ShimFinding]] | None = None,
    shim_findings_by_package: Mapping[str, list[ShimFinding]] | None = None,
) -> None:
    """Collect independent presence signals for one client."""
    shim_findings_by_basename = shim_findings_by_basename or {}
    shim_findings_by_package = shim_findings_by_package or {}
    _detect_config_presence(
        detected,
        client,
        system=system,
        home=home,
        environment=environment,
    )

    probe = client.install_probe
    if probe is None:
        return

    _detect_vscode_extension_presence(
        detected,
        system=system,
        home=home,
        extension_ids=probe.vscode_extension_ids,
    )

    if system == "Darwin":
        for bundle_name in probe.macos_app_bundles:
            for app_root in _macos_app_roots(home):
                bundle = app_root / bundle_name
                if _safe_is_dir(bundle):
                    detected.add_detection(
                        "app",
                        version=_macos_app_version(bundle),
                    )
                    break

    if system == "Linux":
        for desktop_id in probe.linux_desktop_ids:
            filename = (
                desktop_id
                if desktop_id.endswith(".desktop")
                else f"{desktop_id}.desktop"
            )
            if any(
                _safe_is_file(root / filename) for root in _linux_desktop_roots(home)
            ):
                detected.add_detection("app")

    if system == "Windows":
        prefixes = tuple(
            prefix.casefold() for prefix in probe.windows_display_name_prefixes
        )
        for display_name, version in registry_entries:
            if prefixes and display_name.casefold().startswith(prefixes):
                detected.add_detection("registry", version=version)
        for install_dir in probe.windows_install_dirs:
            path = _resolve_platform_path(
                PlatformPath(install_dir, platform="windows"),
                system=system,
                home=home,
                environment=environment,
            )
            if path is not None and _windows_install_present(path):
                detected.add_detection("app")

    for package in probe.npm_packages:
        finding = npm_findings.get(package.name)
        if finding is not None:
            detected.add_detection(
                "npm_global",
                version=finding.version,
                config_path=finding.manifest_path,
                wsl_context=_wsl_context_for_path(finding.manifest_path),
            )

    for package in probe.pip_packages:
        finding = pip_findings.get(package.name)
        if finding is not None:
            detected.add_detection(
                "pip_global",
                version=finding.version,
                config_path=finding.metadata_path,
                wsl_context=_wsl_context_for_path(finding.metadata_path),
            )

    # Package-backed probes rely on validated metadata and never execute
    # user-owned npm/pip shims during inventory.
    may_probe_cli_version = (
        probe.probe_cli_version and not probe.npm_packages and not probe.pip_packages
    )
    for binary in probe.cli_binaries:
        cli_path = locate_cli_binary(
            binary,
            home=home,
            system=system,
        )
        if cli_path is not None:
            detected.add_detection(
                "cli",
                version=(
                    get_cli_version(cli_path)
                    if detected.client_version is None and may_probe_cli_version
                    else None
                ),
            )

    # Renamed launchers: evidence keys on the resolved target identity, never
    # the shim's own name or location. Nothing here is executed.
    for binary in probe.cli_binaries:
        for finding in shim_findings_by_basename.get(binary, ()):
            detected.add_detection(
                "cli",
                config_path=finding.target_path,
            )
    for package in probe.npm_packages:
        for finding in shim_findings_by_package.get(package.name, ()):
            detected.add_detection(
                "cli",
                version=finding.version,
                config_path=finding.target_path,
            )


def detect_client_presence(
    clients: Iterable[MCPClientDefinition],
    *,
    home: Path | None = None,
    system: str | None = None,
    environment: Mapping[str, str] | None = None,
    node_modules_paths: Iterable[Path] = (),
    hidden_space_result: HiddenSpaceScanResult | None = None,
    checkpoint: Callable[[], None] | None = None,
    windows_user_sid: str | None = None,
    include_current_user_registry: bool = True,
    wsl_distros: Iterable[DiscoveredWSLDistro] | None = None,
) -> list[DetectedClient]:
    """Run OS install probes for every enabled client definition."""
    client_list = list(clients)
    actual_home = home or Path.home()
    actual_system = system or platform.system()
    actual_environment = os.environ if environment is None else environment
    try:
        if actual_system != "Windows":
            registry_entries = []
        elif windows_user_sid is not None:
            registry_entries = _windows_uninstall_entries(user_sid=windows_user_sid)
        elif include_current_user_registry:
            registry_entries = _windows_uninstall_entries()
        else:
            registry_entries = _windows_uninstall_entries(user_sid=None)
    except Exception:
        logger.debug("client_registry_probe_failed", exc_info=True)
        registry_entries = []
    npm_packages = [
        package
        for client in client_list
        if client.install_probe is not None
        for package in client.install_probe.npm_packages
    ]
    pip_packages = [
        package
        for client in client_list
        if client.install_probe is not None
        for package in client.install_probe.pip_packages
    ]
    try:
        wsl_homes: tuple[Path, ...] = (
            tuple(islice(_wsl_homes(), MAX_WSL_HOMES_TOTAL))
            if actual_system == "Windows"
            else ()
        )
    except Exception:
        logger.debug("wsl_home_discovery_failed", exc_info=True)
        wsl_homes = ()
    hidden_result = hidden_space_result
    if (npm_packages or pip_packages) and hidden_result is None:
        # The standalone fallback must match the orchestrator sweep's home
        # coverage: WSL homes ride along as extra roots so hidden WSL
        # node_modules/python envs are still discovered with
        # discover_hidden=False below.
        hidden_result = scan_hidden_spaces(
            home=actual_home,
            system=actual_system,
            extra_home_roots=wsl_homes,
            include_files=False,
            temp_roots=() if home is not None else None,
            checkpoint=checkpoint,
        )
    hidden_node_modules_paths = _filter_hidden_package_roots(
        hidden_result.node_modules_paths if hidden_result is not None else (),
        system=actual_system,
        wsl_homes=wsl_homes,
    )
    effective_node_modules_paths = (
        path
        for pair in zip_longest(hidden_node_modules_paths, node_modules_paths)
        for path in pair
        if path is not None
    )
    effective_python_env_roots = _filter_hidden_package_roots(
        hidden_result.python_env_roots if hidden_result is not None else (),
        system=actual_system,
        wsl_homes=wsl_homes,
    )
    try:
        npm_findings = scan_npm_global_packages(
            npm_packages,
            home=actual_home,
            system=actual_system,
            environment=actual_environment,
            wsl_homes=wsl_homes,
            node_modules_paths=effective_node_modules_paths,
            discover_hidden=False,
            checkpoint=checkpoint,
        )
    except ScanResourceLimitExceeded:
        raise
    except Exception:
        logger.debug("npm_global_probe_failed", exc_info=True)
        npm_findings = {}
    try:
        pip_findings = scan_pip_global_packages(
            pip_packages,
            home=actual_home,
            system=actual_system,
            environment=actual_environment,
            python_env_roots=effective_python_env_roots,
            wsl_homes=wsl_homes,
            discover_hidden=False,
            checkpoint=checkpoint,
        )
    except ScanResourceLimitExceeded:
        raise
    except Exception:
        logger.debug("pip_global_probe_failed", exc_info=True)
        pip_findings = {}
    try:
        shim_findings_by_basename, shim_findings_by_package = sweep_shim_identities(
            cli_basenames=[
                binary
                for client in client_list
                if client.install_probe is not None
                for binary in client.install_probe.cli_binaries
            ],
            npm_packages={package.name: package for package in npm_packages},
            home=actual_home,
            system=actual_system,
            environment=actual_environment,
            include_host_dirs=home is None,
            checkpoint=checkpoint,
        )
    except ScanResourceLimitExceeded:
        raise
    except Exception:
        logger.debug("shim_identity_sweep_failed", exc_info=True)
        shim_findings_by_basename = {}
        shim_findings_by_package = {}
    wsl_findings_by_client: dict[str, list[WSLBinaryFinding]] = {}
    if actual_system == "Windows":
        try:
            if wsl_distros is None:
                inventory = get_wsl_distro_inventory()
                effective_wsl_distros = inventory.distros if inventory.success else ()
            else:
                effective_wsl_distros = tuple(wsl_distros)
            for finding in scan_wsl_cli_binaries(
                client_list,
                effective_wsl_distros,
                checkpoint=checkpoint,
            ):
                wsl_findings_by_client.setdefault(finding.client, []).append(finding)
        except ScanResourceLimitExceeded:
            raise
        except Exception:
            logger.debug("wsl_cli_presence_probe_failed", exc_info=True)
    detected: dict[str, DetectedClient] = {}

    for client in client_list:
        result = DetectedClient(
            client=client.name,
            display_name=client.display_name,
        )
        try:
            _probe_client_presence(
                result,
                client,
                system=actual_system,
                home=actual_home,
                environment=actual_environment,
                registry_entries=registry_entries,
                npm_findings=npm_findings,
                pip_findings=pip_findings,
                shim_findings_by_basename=shim_findings_by_basename,
                shim_findings_by_package=shim_findings_by_package,
            )
            for finding in wsl_findings_by_client.get(client.name, ()):
                result.add_detection(
                    "cli",
                    config_path=finding.path,
                    wsl_context=finding.context,
                )
        except Exception:
            logger.debug(
                "client_presence_probe_failed",
                client=client.name,
                exc_info=True,
            )

        if result.detected_via:
            detected[client.name] = result

    return [detected[c.name] for c in client_list if c.name in detected]


def coalesce_detected_clients(
    detected_clients: Iterable[DetectedClient],
) -> list[DetectedClient]:
    """Merge repeated signals for one client without dropping evidence."""
    merged: dict[str, DetectedClient] = {}
    for signal in detected_clients:
        target = merged.setdefault(
            signal.client,
            DetectedClient(
                client=signal.client,
                display_name=signal.display_name,
            ),
        )
        if target.client_version is None:
            target.client_version = signal.client_version
        for method in signal.detected_via:
            if method not in target.detected_via:
                target.detected_via.append(method)
        target.detected_via.sort(key=DETECTION_METHOD_ORDER.index)
        target.config_paths = sorted(
            set(target.config_paths) | set(signal.config_paths)
        )
        target.container_ids = sorted(
            set(target.container_ids) | set(signal.container_ids)
        )
        target.wsl_contexts = sorted(
            set(target.wsl_contexts) | set(signal.wsl_contexts),
            key=lambda context: (
                context.distro.casefold(),
                (context.user or "").casefold(),
            ),
        )[:MAX_WSL_CLIENT_CONTEXTS]
    return list(merged.values())


def merge_client_presence(
    detected_clients: Iterable[DetectedClient],
    *,
    clients: Iterable[MCPClientDefinition],
    configurations: Iterable[Any] = (),
    skills: Iterable[Any] = (),
    agent_definitions: Iterable[Any] = (),
    plugins: Iterable[Any] = (),
    extension_clients: Iterable[str] = (),
) -> list[DetectedClient]:
    """Fold config/server/skill/plugin/extension artifacts into install probes."""
    client_list = list(clients)
    definitions = {client.name: client for client in client_list}
    merged = {
        client.client: client for client in coalesce_detected_clients(detected_clients)
    }

    def result_for(client_name: str) -> DetectedClient | None:
        definition = definitions.get(client_name)
        if definition is None:
            return None
        return merged.setdefault(
            client_name,
            DetectedClient(
                client=client_name,
                display_name=definition.display_name,
            ),
        )

    for config in configurations:
        result = result_for(getattr(config, "client", ""))
        if result is None:
            continue
        scope = getattr(config, "config_scope", None)
        config_path = getattr(config, "config_path", None)
        if scope in {"global", "project", "wsl"} and config_path:
            result.add_detection("config", config_path=config_path)
        if scope == "container":
            result.add_detection(
                "container",
                version=getattr(config, "client_version", None),
                config_path=config_path,
            )
        if getattr(config, "servers", None):
            result.add_detection(
                "server",
                version=getattr(config, "client_version", None),
            )
        if scope == "plugin":
            result.add_detection("plugin")

    for skill in skills:
        result = result_for(getattr(skill, "tool", ""))
        if result is not None:
            if getattr(skill, "container_id", None):
                result.add_detection("container")
            result.add_detection("skill")

    for agent_definition in agent_definitions:
        result = result_for(getattr(agent_definition, "client", ""))
        if result is not None:
            # An agent definition file is a client config artifact, so it is
            # presence evidence on its own. Always record "config" (mirroring
            # how skills always record "skill"); otherwise a host-side
            # definition would create an empty DetectedClient via result_for()
            # and report the client with no detection methods.
            if getattr(agent_definition, "container_id", None):
                result.add_detection("container")
            result.add_detection("config")

    for plugin in plugins:
        result = result_for(getattr(plugin, "client", ""))
        if result is None:
            continue
        plugin_type = str(getattr(plugin, "plugin_type", ""))
        method: DetectionMethod = (
            "extension" if "extension" in plugin_type else "plugin"
        )
        result.add_detection(method)

    for client_name in extension_clients:
        result = result_for(client_name)
        if result is not None:
            result.add_detection("extension")

    return [merged[client.name] for client in client_list if client.name in merged]
