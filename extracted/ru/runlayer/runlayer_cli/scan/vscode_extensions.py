"""Inventory extensions installed by VS Code-family IDEs."""

from __future__ import annotations

import os
import platform
from collections import deque
from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, cast

import structlog

from runlayer_cli.scan.completeness import ScanCompletionStatus
from runlayer_cli.scan.plugin_scanner import DiscoveredPluginArtifact
from runlayer_cli.safe_parse import parse_json
from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    SymlinkLayoutResolver,
    bound_plugin_metadata,
    drain_round_robin,
    environment_value,
    has_link_or_reparse_component,
    is_contained_real_directory,
    is_link_or_reparse,
    is_real_directory,
    iter_directory_entries,
    plugin_artifact_identifier,
    read_bounded,
    read_safe_relative_file,
    realpath_key,
)
from runlayer_cli.scan.windows_users import is_windows_system_context

logger = structlog.get_logger(__name__)

MAX_MANIFEST_BYTES = 1024 * 1024
MAX_EXTENSIONS_PER_SCAN = 2000
MAX_EXPLICIT_EXTENSION_ROOTS = 64
MAX_REMOTE_SERVER_ROOT_CANDIDATES_PER_HOME = 100
MAX_FOLLOWED_SYMLINK_TARGETS = 64
MAX_RESOLVED_INTERMEDIATE_LINKS = 64
_ExtensionScope = Literal["global", "builtin", "process_override"]
_BuiltinBaseKind = Literal["absolute", "environment", "home"]
_BuiltinRootSpec = tuple[
    str,
    Path,
    tuple[tuple[_BuiltinBaseKind, str], ...],
]
_BuiltinRootLayout = tuple[_BuiltinRootSpec, ...]


@dataclass(frozen=True)
class VSCodeExtensionRoot:
    """One explicit extension collection root and its owning editor."""

    path: Path
    client: str
    wsl_distro: str | None = None


@dataclass(frozen=True)
class _RootContext:
    client: str
    scope: _ExtensionScope
    device_scope: bool
    target_status: ScanCompletionStatus | None
    wsl_distro: str | None = None


_HOST_CLIENTS: tuple[tuple[str, str], ...] = (
    (".vscode", "vscode"),
    (".vscode-insiders", "vscode"),
    (".vscode-oss", "vscode"),
    (".cursor", "cursor"),
    (".windsurf", "windsurf"),
    (".devin", "windsurf"),
    (".vscode-server", "vscode"),
    (".vscode-server-insiders", "vscode"),
    (".cursor-server", "cursor"),
    (".windsurf-server", "windsurf"),
    (".devin-server", "windsurf"),
    (".local/share/code-server", "vscode"),
    (".openvscode-server", "vscode"),
    (".var/app/com.visualstudio.code/data/vscode", "vscode"),
    (".var/app/com.visualstudio.code-oss/data/vscode", "vscode"),
    (".var/app/com.vscodium.codium/data/codium", "vscode"),
)

_BUILTIN_ROOT_LAYOUTS: dict[str, _BuiltinRootLayout] = {
    "Darwin": (
        (
            "vscode",
            Path("Visual Studio Code.app/Contents/Resources/app/extensions"),
            (("home", "Applications"), ("absolute", "/Applications")),
        ),
        (
            "vscode",
            Path("Visual Studio Code - Insiders.app/Contents/Resources/app/extensions"),
            (("home", "Applications"), ("absolute", "/Applications")),
        ),
        (
            "cursor",
            Path("Cursor.app/Contents/Resources/app/extensions"),
            (("home", "Applications"), ("absolute", "/Applications")),
        ),
        (
            "windsurf",
            Path("Windsurf.app/Contents/Resources/app/extensions"),
            (("home", "Applications"), ("absolute", "/Applications")),
        ),
        (
            "windsurf",
            Path("Devin.app/Contents/Resources/app/extensions"),
            (("home", "Applications"), ("absolute", "/Applications")),
        ),
    ),
    "Linux": (
        (
            "vscode",
            Path("code/resources/app/extensions"),
            (("absolute", "/usr/share"),),
        ),
        (
            "vscode",
            Path("code-insiders/resources/app/extensions"),
            (("absolute", "/usr/share"),),
        ),
        (
            "vscode",
            Path("code-oss/resources/app/extensions"),
            (("absolute", "/usr/share"),),
        ),
        (
            "vscode",
            Path("codium/resources/app/extensions"),
            (("absolute", "/usr/share"),),
        ),
        (
            "cursor",
            Path("cursor/resources/app/extensions"),
            (("absolute", "/usr/share"), ("absolute", "/opt")),
        ),
        (
            "cursor",
            Path("Cursor/resources/app/extensions"),
            (("absolute", "/opt"),),
        ),
        (
            "windsurf",
            Path("windsurf/resources/app/extensions"),
            (("absolute", "/usr/share"), ("absolute", "/opt")),
        ),
        (
            "windsurf",
            Path("Windsurf/resources/app/extensions"),
            (("absolute", "/opt"),),
        ),
        (
            "windsurf",
            Path("devin-desktop/resources/app/extensions"),
            (("absolute", "/usr/share"), ("absolute", "/opt")),
        ),
        (
            "vscode",
            Path("code/current/usr/share/code/resources/app/extensions"),
            (("absolute", "/snap"),),
        ),
        (
            "vscode",
            Path(
                "code-insiders/current/usr/share/code-insiders/resources/app/extensions"
            ),
            (("absolute", "/snap"),),
        ),
        (
            "vscode",
            Path("codium/current/usr/share/codium/resources/app/extensions"),
            (("absolute", "/snap"),),
        ),
        (
            "vscode",
            Path(
                "com.visualstudio.code/current/active/files/extra/vscode/"
                "resources/app/extensions"
            ),
            (
                ("absolute", "/var/lib/flatpak/app"),
                ("home", ".local/share/flatpak/app"),
            ),
        ),
        (
            "vscode",
            Path(
                "com.visualstudio.code-oss/current/active/files/main/"
                "resources/app/extensions"
            ),
            (
                ("absolute", "/var/lib/flatpak/app"),
                ("home", ".local/share/flatpak/app"),
            ),
        ),
        (
            "vscode",
            Path(
                "com.vscodium.codium/current/active/files/share/codium/"
                "resources/app/extensions"
            ),
            (
                ("absolute", "/var/lib/flatpak/app"),
                ("home", ".local/share/flatpak/app"),
            ),
        ),
    ),
    "Windows": (
        (
            "vscode",
            Path("Microsoft VS Code/resources/app/extensions"),
            (
                ("home", "AppData/Local/Programs"),
                ("environment", "ProgramFiles"),
            ),
        ),
        (
            "vscode",
            Path("Microsoft VS Code Insiders/resources/app/extensions"),
            (
                ("home", "AppData/Local/Programs"),
                ("environment", "ProgramFiles"),
            ),
        ),
        (
            "cursor",
            Path("Programs/cursor/resources/app/extensions"),
            (("home", "AppData/Local"),),
        ),
        (
            "cursor",
            Path("cursor/resources/app/extensions"),
            (
                ("environment", "ProgramFiles"),
                ("environment", "ProgramFiles(x86)"),
            ),
        ),
        (
            "windsurf",
            Path("Programs/Windsurf/resources/app/extensions"),
            (("home", "AppData/Local"),),
        ),
        (
            "windsurf",
            Path("Windsurf/resources/app/extensions"),
            (
                ("environment", "ProgramFiles"),
                ("environment", "ProgramFiles(x86)"),
            ),
        ),
        (
            "windsurf",
            Path("Programs/Devin/resources/app/extensions"),
            (("home", "AppData/Local"),),
        ),
        (
            "windsurf",
            Path("Devin/resources/app/extensions"),
            (
                ("environment", "ProgramFiles"),
                ("environment", "ProgramFiles(x86)"),
            ),
        ),
    ),
}

# Deliberately overlaps _HOST_CLIENTS: this scans built-ins, not user installs.
_REMOTE_SERVER_HOST_DIRS: tuple[tuple[str, str], ...] = (
    (".vscode-server", "vscode"),
    (".vscode-server-insiders", "vscode"),
    (".cursor-server", "cursor"),
    (".windsurf-server", "windsurf"),
    (".devin-server", "windsurf"),
)

_REMOTE_SERVER_LAYOUTS: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (("bin",), ("extensions",)),
    (("cli", "servers"), ("server", "extensions")),
)

_PLATFORM_SUFFIXES: tuple[str, ...] = (
    "-win32-x64",
    "-win32-arm64",
    "-linux-x64",
    "-linux-arm64",
    "-linux-armhf",
    "-alpine-x64",
    "-alpine-arm64",
    "-darwin-x64",
    "-darwin-arm64",
    "-universal",
    "-web",
)


def _safe_manifest_path(
    install_root: Path,
    *,
    windows_system_context: bool,
) -> Path | None:
    try:
        install_root = install_root.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not is_real_directory(install_root):
        return None
    manifest_path = install_root / "package.json"
    if windows_system_context and is_link_or_reparse(manifest_path):
        return None
    return manifest_path


def _read_manifest(
    install_root: Path,
    *,
    resolver: SymlinkLayoutResolver,
    windows_system_context: bool,
) -> dict[str, Any] | None:
    path = _safe_manifest_path(
        install_root,
        windows_system_context=windows_system_context,
    )
    if path is None:
        return None
    if is_link_or_reparse(path):
        result = read_safe_relative_file(
            install_root,
            Path("package.json"),
            resolver=resolver,
            max_bytes=MAX_MANIFEST_BYTES,
            follow_final_symlink=True,
        )
        content = result["content"] if result is not None else None
    else:
        content = read_bounded(path, max_bytes=MAX_MANIFEST_BYTES)
    if content is None:
        return None
    return parse_vscode_extension_manifest(content)


def parse_vscode_extension_manifest(content: bytes) -> dict[str, Any] | None:
    """Parse one bounded VS Code extension manifest."""
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return None
    value = parse_json(text)["value"]
    return value if isinstance(value, dict) else None


def _text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _author_name(value: object) -> str | None:
    if isinstance(value, str):
        return value or None
    if isinstance(value, dict):
        author = cast(dict[str, object], value)
        return _text(author.get("name"))
    return None


def _folder_identity(folder_name: str) -> tuple[str, str | None] | None:
    versioned_name = folder_name
    for suffix in _PLATFORM_SUFFIXES:
        if versioned_name.endswith(suffix):
            versioned_name = versioned_name[: -len(suffix)]
            break

    extension_id, separator, version = versioned_name.rpartition("-")
    if not separator or not version[:1].isdigit():
        extension_id = folder_name
        version = ""
    if "." not in extension_id:
        return None
    return extension_id, version or None


def build_vscode_extension_artifact(
    *,
    manifest: dict[str, Any],
    install_path: str,
    folder_name: str,
    client: str,
    scope: _ExtensionScope = "global",
) -> DiscoveredPluginArtifact | None:
    """Build an extension artifact from a parsed host or container manifest."""
    publisher = _text(manifest.get("publisher"))
    package_name = _text(manifest.get("name"))
    builtin = scope == "builtin"
    if builtin and (
        publisher is None or package_name is None or publisher.casefold() == "vscode"
    ):
        return None

    fallback = None if builtin else _folder_identity(folder_name)
    if publisher is not None and package_name is not None:
        extension_id = f"{publisher}.{package_name}"
        fallback_version = fallback[1] if fallback is not None else None
    elif fallback is not None:
        extension_id, fallback_version = fallback
    else:
        return None

    bounded = bound_plugin_metadata(
        source_identifier=extension_id.casefold(),
        name=_text(manifest.get("displayName")) or extension_id,
        version=_text(manifest.get("version")) or fallback_version,
        author=_author_name(manifest.get("author")),
    )
    if bounded is None:
        return None
    return DiscoveredPluginArtifact(
        name=bounded["name"],
        plugin_type="vscode_extension",
        client=client,
        install_path=install_path,
        identifier=plugin_artifact_identifier(
            "vscode_extension",
            bounded["source_identifier"],
            bounded["version"],
        ),
        source_identifier=bounded["source_identifier"],
        version=bounded["version"],
        description=_text(manifest.get("description")),
        author=bounded["author"],
        scope=scope,
        marketplace="visual-studio-marketplace",
    )


def _artifact_for_extension(
    extension_dir: Path,
    client: str,
    scope: _ExtensionScope = "global",
    *,
    folder_name: str | None = None,
    resolver: SymlinkLayoutResolver,
    windows_system_context: bool,
    on_builtin_manifest_failure: Callable[[], None] | None = None,
) -> DiscoveredPluginArtifact | None:
    if is_link_or_reparse(extension_dir):
        return None
    if windows_system_context and is_link_or_reparse(extension_dir / "package.json"):
        if scope == "builtin" and on_builtin_manifest_failure is not None:
            on_builtin_manifest_failure()
        return None

    manifest = _read_manifest(
        extension_dir,
        resolver=resolver,
        windows_system_context=windows_system_context,
    )
    if manifest is None:
        if scope == "builtin" and on_builtin_manifest_failure is not None:
            on_builtin_manifest_failure()
        manifest = {}
    return build_vscode_extension_artifact(
        manifest=manifest,
        install_path=str(extension_dir),
        folder_name=folder_name or extension_dir.name,
        client=client,
        scope=scope,
    )


def _extension_collection_root(
    home: Path,
    host_dir: str,
    *,
    resolver: SymlinkLayoutResolver,
) -> Path | None:
    return resolver.resolve_directory(
        home,
        Path(host_dir) / "extensions",
    )


def _remote_builtin_extension_roots(
    home: Path,
    *,
    symlink_policy: SymlinkFollowPolicy,
    resolver: SymlinkLayoutResolver,
    checkpoint: Callable[[], None] | None,
    scan_status: ScanCompletionStatus | None,
) -> Generator[tuple[str, Path], None, None]:
    candidates_seen = 0
    for host_dir, client in _REMOTE_SERVER_HOST_DIRS:
        host_root = resolver.resolve_directory(
            home,
            Path(host_dir),
            final_is_intermediate=True,
        )
        if host_root is None:
            continue
        for collection_parts, extension_parts in _REMOTE_SERVER_LAYOUTS:
            collection_root = resolver.resolve_directory(
                host_root,
                Path(*collection_parts),
                claim_final=is_link_or_reparse(home / host_dir),
            )
            if collection_root is None:
                continue
            symlink_policy.add_scan_area(collection_root, 0)
            candidates = iter_directory_entries(
                collection_root,
                on_error=(
                    lambda _exc: (
                        scan_status.mark_incomplete(
                            "vscode_extension_directory_read_failed"
                        )
                        if scan_status is not None
                        else None
                    )
                ),
            )
            try:
                for candidate in candidates:
                    if checkpoint is not None:
                        checkpoint()
                    candidates_seen += 1
                    if candidates_seen > MAX_REMOTE_SERVER_ROOT_CANDIDATES_PER_HOME:
                        if scan_status is not None:
                            scan_status.mark_incomplete(
                                "vscode_remote_server_root_scan_capped"
                            )
                        logger.warning(
                            "vscode_remote_server_root_scan_capped",
                            home=str(home),
                            cap=MAX_REMOTE_SERVER_ROOT_CANDIDATES_PER_HOME,
                        )
                        return
                    candidate_was_link = is_link_or_reparse(candidate)
                    if candidate_was_link:
                        target = resolver.resolve_intermediate_link(
                            candidate,
                            current=collection_root,
                        )
                        if target is None or not is_real_directory(target):
                            continue
                        candidate = target
                    elif not is_real_directory(candidate):
                        continue
                    extensions_dir = resolver.resolve_directory(
                        candidate,
                        Path(*extension_parts),
                        claim_final=candidate_was_link,
                    )
                    if extensions_dir is not None:
                        yield client, extensions_dir
            finally:
                candidates.close()


def _builtin_extension_roots(
    homes: Sequence[Path],
    *,
    system: str,
    machine_scope: bool,
    symlink_policy: SymlinkFollowPolicy,
    resolver: SymlinkLayoutResolver,
    checkpoint: Callable[[], None] | None,
    scan_status: ScanCompletionStatus | None,
) -> Generator[tuple[str, Path, bool], None, None]:
    layout = _BUILTIN_ROOT_LAYOUTS.get(system)
    if layout is not None:
        for client, app_tail, base_dirs in layout:
            for base_kind, base_value in base_dirs:
                if not machine_scope and base_kind != "home":
                    continue
                resolved_bases: tuple[tuple[Path, Path | None], ...]
                if base_kind == "home":
                    resolved_bases = tuple(
                        (current_home / base_value, current_home)
                        for current_home in homes
                    )
                elif base_kind == "environment":
                    environment_base = environment_value(
                        os.environ,
                        base_value,
                        system=system,
                    )
                    resolved_bases = (
                        ((Path(environment_base), None),) if environment_base else ()
                    )
                else:
                    resolved_bases = ((Path(base_value), None),)

                for base_dir, containing_home in resolved_bases:
                    if containing_home is None:
                        if is_link_or_reparse(base_dir):
                            if has_link_or_reparse_component(base_dir.parent):
                                continue
                            target = resolver.resolve_intermediate_link(
                                base_dir,
                                current=Path(base_dir.anchor),
                            )
                            if target is None:
                                continue
                            extensions_dir = resolver.resolve_directory(
                                target,
                                app_tail,
                                claim_final=True,
                            )
                        else:
                            if not is_real_directory(
                                base_dir
                            ) or has_link_or_reparse_component(base_dir):
                                continue
                            extensions_dir = resolver.resolve_directory(
                                base_dir,
                                app_tail,
                            )
                    else:
                        extensions_dir = resolver.resolve_directory(
                            containing_home,
                            Path(base_value) / app_tail,
                        )
                    if extensions_dir is not None:
                        yield client, extensions_dir, base_kind != "home"

    for current_home in homes:
        for client, extensions_dir in _remote_builtin_extension_roots(
            current_home,
            symlink_policy=symlink_policy,
            resolver=resolver,
            checkpoint=checkpoint,
            scan_status=scan_status,
        ):
            yield client, extensions_dir, False


def _resolve_home_roots(
    configured_homes: Sequence[Path],
    *,
    windows_system_context: bool,
) -> tuple[Path, ...]:
    resolved_by_key: dict[str, Path] = {}
    for configured_home in configured_homes:
        if windows_system_context:
            resolved_home = configured_home.absolute()
            if not is_contained_real_directory(
                Path(resolved_home.anchor),
                resolved_home,
            ):
                continue
        else:
            try:
                resolved_home = configured_home.resolve(strict=True)
            except (OSError, RuntimeError):
                continue
        if is_real_directory(resolved_home):
            resolved_by_key.setdefault(realpath_key(resolved_home), resolved_home)
    return tuple(resolved_by_key.values())


def scan_vscode_extensions(
    *,
    home: Path | None = None,
    extra_home_roots: Sequence[Path] = (),
    extra_extension_roots: Sequence[VSCodeExtensionRoot] = (),
    include_standard_roots: bool = True,
    machine_scope: bool = True,
    checkpoint: Callable[[], None] | None = None,
    scan_status: ScanCompletionStatus | None = None,
    device_scan_status: ScanCompletionStatus | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Enumerate extensions fairly within one scan-wide entry budget."""
    system = platform.system()
    artifacts: list[DiscoveredPluginArtifact] = []
    windows_system_context = is_windows_system_context()
    configured_homes = (
        (home or Path.home(), *extra_home_roots) if include_standard_roots else ()
    )
    homes = _resolve_home_roots(
        configured_homes,
        windows_system_context=windows_system_context,
    )
    user_root_specs = tuple(
        (current_home, host_dir, client)
        for current_home in homes
        for host_dir, client in _HOST_CLIENTS
    )
    ordered_user_root_specs = tuple(
        sorted(
            user_root_specs,
            key=lambda spec: (
                not is_contained_real_directory(
                    spec[0],
                    spec[0] / spec[1] / "extensions",
                )
            ),
        )
    )
    symlink_policy = SymlinkFollowPolicy(
        scan_areas=[],
        max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
        windows_system_context=windows_system_context,
    )
    resolver = SymlinkLayoutResolver(
        policy=symlink_policy,
        windows_system_context=windows_system_context,
        max_intermediate_links=MAX_RESOLVED_INTERMEDIATE_LINKS,
    )
    scheduled_roots: set[str] = set()
    seen_extension_paths: set[str] = set()
    root_iterators: deque[tuple[_RootContext, Generator[Path, None, None]]] = deque()

    def _schedule_root(
        extensions_dir: Path,
        *,
        client: str,
        scope: _ExtensionScope,
        device_scope: bool,
        wsl_distro: str | None = None,
    ) -> None:
        symlink_policy.add_scan_area(extensions_dir, 0)
        root_key = realpath_key(extensions_dir)
        if root_key in scheduled_roots:
            return
        scheduled_roots.add(root_key)
        context = _RootContext(
            client=client,
            scope=scope,
            device_scope=device_scope,
            target_status=device_scan_status if device_scope else scan_status,
            wsl_distro=wsl_distro,
        )

        def _mark_directory_error(_exc: OSError) -> None:
            if context.target_status is not None:
                context.target_status.mark_incomplete(
                    "vscode_extension_directory_read_failed"
                )

        root_iterators.append(
            (
                context,
                iter_directory_entries(
                    extensions_dir,
                    on_error=_mark_directory_error,
                ),
            )
        )

    for current_home, host_dir, client in ordered_user_root_specs:
        extensions_dir = _extension_collection_root(
            current_home,
            host_dir,
            resolver=resolver,
        )
        if extensions_dir is None:
            continue
        _schedule_root(
            extensions_dir,
            client=client,
            scope="global",
            device_scope=False,
        )

    if (
        len(extra_extension_roots) > MAX_EXPLICIT_EXTENSION_ROOTS
        and scan_status is not None
    ):
        scan_status.mark_incomplete("vscode_explicit_extension_roots_capped")

    for root in extra_extension_roots[:MAX_EXPLICIT_EXTENSION_ROOTS]:
        resolved_roots = _resolve_home_roots(
            (root.path,),
            windows_system_context=windows_system_context,
        )
        if resolved_roots:
            _schedule_root(
                resolved_roots[0],
                client=root.client,
                scope="process_override",
                device_scope=False,
                wsl_distro=root.wsl_distro,
            )
        elif scan_status is not None:
            scan_status.mark_incomplete("vscode_explicit_extension_root_unresolved")

    if include_standard_roots:
        for client, extensions_dir, device_scope in _builtin_extension_roots(
            homes,
            system=system,
            machine_scope=machine_scope,
            symlink_policy=symlink_policy,
            resolver=resolver,
            checkpoint=checkpoint,
            scan_status=scan_status,
        ):
            _schedule_root(
                extensions_dir,
                client=client,
                scope="builtin",
                device_scope=device_scope,
            )

    def _visit(
        context: _RootContext,
        extension_dir: Path,
    ) -> None:
        folder_name = extension_dir.name

        def _mark_builtin_manifest_failure() -> None:
            if context.target_status is not None:
                context.target_status.mark_incomplete(
                    "vscode_builtin_manifest_read_failed"
                )

        try:
            if is_link_or_reparse(extension_dir):
                target = resolver.resolve_policy_link(
                    extension_dir,
                    current=extension_dir.parent,
                    target_is_walk_root=False,
                )
                if target is None:
                    return
                extension_dir = target
            if not is_real_directory(extension_dir):
                return
            extension_dir = extension_dir.resolve(strict=True)
            extension_key = realpath_key(extension_dir)
            if extension_key in seen_extension_paths:
                return
            seen_extension_paths.add(extension_key)
            symlink_policy.mark_visited(
                extension_dir,
                target_is_walk_root=False,
            )
            artifact = _artifact_for_extension(
                extension_dir,
                context.client,
                context.scope,
                folder_name=folder_name,
                resolver=resolver,
                windows_system_context=windows_system_context,
                on_builtin_manifest_failure=_mark_builtin_manifest_failure,
            )
        except (OSError, RuntimeError):
            if context.target_status is not None:
                context.target_status.mark_incomplete("vscode_extension_read_failed")
            return
        if artifact is not None:
            artifact.device_scope = context.device_scope
            artifact.wsl_distro = context.wsl_distro
            artifacts.append(artifact)

    drain_result = drain_round_robin(
        root_iterators,
        visit=_visit,
        max_entries=MAX_EXTENSIONS_PER_SCAN,
        checkpoint=checkpoint,
    )

    if drain_result["max_entries_exceeded"]:
        if scan_status is not None:
            scan_status.mark_incomplete("vscode_extension_scan_capped")
        if device_scan_status is not None:
            device_scan_status.mark_incomplete("vscode_extension_scan_capped")
        logger.warning(
            "vscode_extension_scan_capped",
            cap=MAX_EXTENSIONS_PER_SCAN,
        )
    if symlink_policy.follow_budget_exhausted and scan_status is not None:
        scan_status.mark_incomplete("vscode_extension_symlink_follow_capped")
    if symlink_policy.follow_budget_exhausted and device_scan_status is not None:
        device_scan_status.mark_incomplete("vscode_extension_symlink_follow_capped")

    return artifacts


def scan_vscode_extension_roots(
    roots: Sequence[VSCodeExtensionRoot],
    *,
    checkpoint: Callable[[], None] | None = None,
    scan_status: ScanCompletionStatus | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Inventory only explicit roots discovered from running editor processes."""

    return scan_vscode_extensions(
        extra_extension_roots=roots,
        include_standard_roots=False,
        checkpoint=checkpoint,
        scan_status=scan_status,
    )
