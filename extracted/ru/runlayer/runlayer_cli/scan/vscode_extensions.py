"""Inventory extensions installed by VS Code-family IDEs."""

from __future__ import annotations

import json
import os
import platform
from collections import deque
from collections.abc import Callable, Generator, Sequence
from pathlib import Path
from typing import Any, Literal, cast

import structlog

from runlayer_cli.scan.plugin_scanner import DiscoveredPluginArtifact
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
MAX_REMOTE_SERVER_ROOT_CANDIDATES_PER_HOME = 100
MAX_FOLLOWED_SYMLINK_TARGETS = 64
MAX_RESOLVED_INTERMEDIATE_LINKS = 64
_ExtensionScope = Literal["global", "builtin"]
_BuiltinBaseKind = Literal["absolute", "environment", "home"]
_BuiltinRootLayout = tuple[
    tuple[Path, ...],
    tuple[tuple[_BuiltinBaseKind, str], ...],
]

_HOST_CLIENTS: tuple[tuple[str, str], ...] = (
    (".vscode", "vscode"),
    (".vscode-insiders", "vscode"),
    (".vscode-oss", "vscode"),
    (".cursor", "cursor"),
    (".windsurf", "windsurf"),
    (".vscode-server", "vscode"),
    (".vscode-server-insiders", "vscode"),
    (".cursor-server", "cursor"),
    (".windsurf-server", "windsurf"),
)

_BUILTIN_ROOT_LAYOUTS: dict[str, _BuiltinRootLayout] = {
    "Darwin": (
        (
            Path("Visual Studio Code.app/Contents/Resources/app/extensions"),
            Path("Visual Studio Code - Insiders.app/Contents/Resources/app/extensions"),
        ),
        (("home", "Applications"), ("absolute", "/Applications")),
    ),
    "Linux": (
        (
            Path("code/resources/app/extensions"),
            Path("code-insiders/resources/app/extensions"),
        ),
        (("absolute", "/usr/share"),),
    ),
    "Windows": (
        (
            Path("Microsoft VS Code/resources/app/extensions"),
            Path("Microsoft VS Code Insiders/resources/app/extensions"),
        ),
        (
            ("home", "AppData/Local/Programs"),
            ("environment", "ProgramFiles"),
        ),
    ),
}

# Deliberately overlaps _HOST_CLIENTS: this scans built-ins, not user installs.
_REMOTE_SERVER_HOST_DIRS: tuple[str, ...] = (
    ".vscode-server",
    ".vscode-server-insiders",
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
    try:
        value = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
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


def _artifact_for_extension(
    extension_dir: Path,
    client: str,
    scope: _ExtensionScope = "global",
    *,
    folder_name: str | None = None,
    resolver: SymlinkLayoutResolver,
    windows_system_context: bool,
) -> DiscoveredPluginArtifact | None:
    if is_link_or_reparse(extension_dir):
        return None
    if windows_system_context and is_link_or_reparse(extension_dir / "package.json"):
        return None

    manifest = (
        _read_manifest(
            extension_dir,
            resolver=resolver,
            windows_system_context=windows_system_context,
        )
        or {}
    )
    publisher = _text(manifest.get("publisher"))
    package_name = _text(manifest.get("name"))
    builtin = scope == "builtin"
    if builtin and (
        publisher is None or package_name is None or publisher.casefold() == "vscode"
    ):
        return None

    fallback = None if builtin else _folder_identity(folder_name or extension_dir.name)
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
        install_path=str(extension_dir),
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
) -> Generator[Path, None, None]:
    candidates_seen = 0
    for host_dir in _REMOTE_SERVER_HOST_DIRS:
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
            candidates = iter_directory_entries(collection_root)
            try:
                for candidate in candidates:
                    if checkpoint is not None:
                        checkpoint()
                    candidates_seen += 1
                    if candidates_seen > MAX_REMOTE_SERVER_ROOT_CANDIDATES_PER_HOME:
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
                        yield extensions_dir
            finally:
                candidates.close()


def _builtin_extension_roots(
    homes: Sequence[Path],
    *,
    system: str,
    symlink_policy: SymlinkFollowPolicy,
    resolver: SymlinkLayoutResolver,
    checkpoint: Callable[[], None] | None,
) -> Generator[Path, None, None]:
    layout = _BUILTIN_ROOT_LAYOUTS.get(system)
    if layout is not None:
        app_tails, base_dirs = layout
        for base_kind, base_value in base_dirs:
            resolved_bases: tuple[tuple[Path, Path | None], ...]
            if base_kind == "home":
                resolved_bases = tuple(
                    (current_home / base_value, current_home) for current_home in homes
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
                for app_tail in app_tails:
                    if containing_home is None:
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
                        yield extensions_dir

    for current_home in homes:
        yield from _remote_builtin_extension_roots(
            current_home,
            symlink_policy=symlink_policy,
            resolver=resolver,
            checkpoint=checkpoint,
        )


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
    checkpoint: Callable[[], None] | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Enumerate extensions fairly within one scan-wide entry budget."""
    system = platform.system()
    artifacts: list[DiscoveredPluginArtifact] = []
    windows_system_context = is_windows_system_context()
    homes = _resolve_home_roots(
        (home or Path.home(), *extra_home_roots),
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
    root_iterators: deque[
        tuple[tuple[str, _ExtensionScope], Generator[Path, None, None]]
    ] = deque()

    def _schedule_root(
        extensions_dir: Path,
        context: tuple[str, _ExtensionScope],
    ) -> None:
        symlink_policy.add_scan_area(extensions_dir, 0)
        root_key = realpath_key(extensions_dir)
        if root_key in scheduled_roots:
            return
        scheduled_roots.add(root_key)
        root_iterators.append((context, iter_directory_entries(extensions_dir)))

    for current_home, host_dir, client in ordered_user_root_specs:
        extensions_dir = _extension_collection_root(
            current_home,
            host_dir,
            resolver=resolver,
        )
        if extensions_dir is None:
            continue
        _schedule_root(extensions_dir, (client, "global"))

    for extensions_dir in _builtin_extension_roots(
        homes,
        system=system,
        symlink_policy=symlink_policy,
        resolver=resolver,
        checkpoint=checkpoint,
    ):
        _schedule_root(extensions_dir, ("vscode", "builtin"))

    def _visit(context: tuple[str, _ExtensionScope], extension_dir: Path) -> None:
        client, scope = context
        folder_name = extension_dir.name
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
                client,
                scope,
                folder_name=folder_name,
                resolver=resolver,
                windows_system_context=windows_system_context,
            )
        except (OSError, RuntimeError):
            return
        if artifact is not None:
            artifacts.append(artifact)

    entries_consumed = drain_round_robin(
        root_iterators,
        visit=_visit,
        max_entries=MAX_EXTENSIONS_PER_SCAN,
        checkpoint=checkpoint,
    )

    if entries_consumed == MAX_EXTENSIONS_PER_SCAN:
        logger.warning(
            "vscode_extension_scan_capped",
            cap=MAX_EXTENSIONS_PER_SCAN,
        )

    return artifacts
