"""Inventory plugins installed by JetBrains IDEs."""

from __future__ import annotations

import os
import stat
from collections import deque
from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass
from itertools import islice
from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

import structlog

from runlayer_cli.scan.plugin_scanner import DiscoveredPluginArtifact
from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    SymlinkLayoutResolver,
    bound_plugin_metadata,
    drain_round_robin,
    has_link_or_reparse_component,
    is_contained_real_directory,
    is_link_or_reparse,
    is_real_directory,
    iter_directory_entries,
    plugin_artifact_identifier,
    read_safe_relative_file,
    realpath_key,
)
from runlayer_cli.scan.windows_users import is_windows_system_context

logger = structlog.get_logger(__name__)

MAX_PLUGIN_XML_BYTES = 1024 * 1024
MAX_PLUGINS_PER_SCAN = 2000
MAX_PRODUCT_DIRS_PER_ROOT = 100
MAX_JARS_PER_PLUGIN = 100
MAX_FOLLOWED_SYMLINK_TARGETS = 64
MAX_RESOLVED_INTERMEDIATE_LINKS = 64

_PRODUCT_CLIENTS: tuple[tuple[str, str], ...] = (
    ("IdeaIC", "intellij_idea_community"),
    ("IdeaIU", "intellij_idea_ultimate"),
    ("IntelliJIdea", "intellij_idea"),
    ("PyCharmCE", "pycharm_community"),
    ("PyCharm", "pycharm"),
    ("WebStorm", "webstorm"),
    ("GoLand", "goland"),
    ("Rider", "rider"),
    ("CLion", "clion"),
    ("RubyMine", "rubymine"),
    ("PhpStorm", "phpstorm"),
    ("DataGrip", "datagrip"),
)


@dataclass(frozen=True)
class _DataRoot:
    approved_root: Path
    relative: Path
    plugin_subdirectory: str | None

    @property
    def path(self) -> Path:
        return self.approved_root / self.relative


@dataclass(frozen=True)
class _MetadataDirectory:
    """Directory targets admitted only after bounded metadata is found."""

    path: Path
    followed_targets: tuple[Path, ...] = ()


def _safe_subdirectory(
    install_root: Path,
    relative: str,
    *,
    windows_system_context: bool,
    resolver: SymlinkLayoutResolver,
) -> _MetadataDirectory | None:
    try:
        install_root = install_root.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    candidate = install_root / relative
    if is_link_or_reparse(candidate):
        if windows_system_context:
            return None
        target = resolver.resolve_intermediate_link(
            candidate,
            current=install_root,
        )
        return (
            _MetadataDirectory(path=target, followed_targets=(target,))
            if target is not None
            else None
        )
    return _MetadataDirectory(path=candidate) if is_real_directory(candidate) else None


def _resolve_top_level_jar_link(
    path: Path,
    *,
    policy: SymlinkFollowPolicy,
) -> Path | None:
    if path.suffix.casefold() != ".jar":
        return None
    target = policy.inspect(path)
    if target is None:
        return None
    try:
        target_mode = target.lstat().st_mode
    except OSError:
        return None
    if not stat.S_ISREG(target_mode) or not policy.claim(target):
        return None
    return target


def _product_client(product_dir_name: str) -> str:
    for prefix, client in _PRODUCT_CLIENTS:
        if product_dir_name.startswith(prefix):
            return client
    product = product_dir_name
    for index, character in enumerate(product):
        if character.isdigit():
            product = product[:index]
            break
    normalized = "".join(
        character.lower() if character.isalnum() else "_" for character in product
    ).strip("_")
    return normalized or "jetbrains"


def _read_xml_file(
    install_root: Path,
    relative: Path,
    *,
    resolver: SymlinkLayoutResolver,
) -> bytes | None:
    result = read_safe_relative_file(
        install_root,
        relative,
        resolver=resolver,
        max_bytes=MAX_PLUGIN_XML_BYTES,
    )
    return result["content"] if result is not None else None


def _read_xml_from_jar(path: Path) -> bytes | None:
    descriptor: int | None = None
    try:
        initial = path.lstat()
        if is_link_or_reparse(path) or not stat.S_ISREG(initial.st_mode):
            return None
        flags = (
            os.O_RDONLY
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_NONBLOCK", 0)
        )
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or (
            opened.st_dev,
            opened.st_ino,
        ) != (initial.st_dev, initial.st_ino):
            return None
        with os.fdopen(descriptor, "rb") as jar_file:
            descriptor = None
            with ZipFile(jar_file) as archive:
                info = archive.getinfo("META-INF/plugin.xml")
                if info.file_size > MAX_PLUGIN_XML_BYTES:
                    return None
                with archive.open(info) as plugin_xml:
                    content = plugin_xml.read(MAX_PLUGIN_XML_BYTES + 1)
                return content if len(content) <= MAX_PLUGIN_XML_BYTES else None
    except (BadZipFile, KeyError, OSError, RuntimeError):
        return None
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass


def _jar_paths(lib_dir: Path) -> Generator[Path, None, None]:
    """Yield jar paths from a real generator so callers can close it.

    ``Path.glob`` returns a ``map`` object (no ``close()``) on newer Pythons,
    which can leave the underlying ``os.scandir`` handle open until GC. The
    ``with`` block here releases it deterministically.
    """
    try:
        with os.scandir(lib_dir) as entries:
            for entry in entries:
                if entry.name.casefold().endswith(".jar"):
                    yield Path(entry.path)
    except OSError:
        return


def _plugin_xml(
    plugin_path: Path,
    *,
    windows_system_context: bool,
    policy: SymlinkFollowPolicy,
    resolver: SymlinkLayoutResolver,
) -> bytes | None:
    if plugin_path.is_file():
        return _read_xml_from_jar(plugin_path)
    if windows_system_context and any(
        is_link_or_reparse(plugin_path / marker_ancestor)
        for marker_ancestor in ("META-INF", "lib")
    ):
        return None

    direct = _read_xml_file(
        plugin_path,
        Path("META-INF") / "plugin.xml",
        resolver=resolver,
    )
    if direct is not None:
        return direct

    lib_dir = _safe_subdirectory(
        plugin_path,
        "lib",
        windows_system_context=windows_system_context,
        resolver=resolver,
    )
    if lib_dir is None:
        return None
    jar_iterator = _jar_paths(lib_dir.path)
    try:
        jars = list(jar_iterator)
    finally:
        jar_iterator.close()
    plugin_name = plugin_path.name.casefold()
    jars.sort(
        key=lambda jar_path: (
            not jar_path.stem.casefold().startswith(plugin_name),
            jar_path.name.casefold(),
            jar_path.name,
        )
    )
    for jar_path in islice(jars, MAX_JARS_PER_PLUGIN):
        content = _read_xml_from_jar(jar_path)
        if content is not None:
            return content if policy.admit_targets(lib_dir.followed_targets) else None
    return None


def _children(root: ElementTree.Element) -> dict[str, ElementTree.Element]:
    return {child.tag.rsplit("}", 1)[-1]: child for child in root}


def _element_text(element: ElementTree.Element | None) -> str | None:
    if element is None:
        return None
    text = "".join(element.itertext()).strip()
    return text or None


def _parse_plugin_xml(content: bytes) -> dict[str, str | None] | None:
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError:
        return None
    values = _children(root)
    plugin_id = _element_text(values.get("id"))
    name = _element_text(values.get("name"))
    if plugin_id is None:
        plugin_id = name
    if plugin_id is None:
        return None
    return {
        "id": plugin_id,
        "name": name or plugin_id,
        "version": _element_text(values.get("version")),
        "author": _element_text(values.get("vendor")),
        "description": _element_text(values.get("description")),
    }


def _artifact(
    plugin_path: Path,
    client: str,
    *,
    windows_system_context: bool,
    policy: SymlinkFollowPolicy,
    resolver: SymlinkLayoutResolver,
) -> DiscoveredPluginArtifact | None:
    if is_link_or_reparse(plugin_path):
        return None
    content = _plugin_xml(
        plugin_path,
        windows_system_context=windows_system_context,
        policy=policy,
        resolver=resolver,
    )
    if content is None:
        return None
    metadata = _parse_plugin_xml(content)
    if metadata is None:
        return None
    plugin_id = metadata["id"]
    assert plugin_id is not None
    bounded = bound_plugin_metadata(
        source_identifier=plugin_id,
        name=metadata["name"] or plugin_id,
        version=metadata["version"],
        author=metadata["author"],
    )
    if bounded is None:
        return None
    return DiscoveredPluginArtifact(
        name=bounded["name"],
        plugin_type="jetbrains_plugin",
        client=client,
        install_path=str(plugin_path),
        identifier=plugin_artifact_identifier(
            "jetbrains_plugin",
            bounded["source_identifier"],
            bounded["version"],
        ),
        source_identifier=bounded["source_identifier"],
        version=bounded["version"],
        description=metadata["description"],
        author=bounded["author"],
        scope="global",
        marketplace="jetbrains-marketplace",
    )


def _data_roots(
    home: Path,
    *,
    include_native_env: bool,
) -> tuple[_DataRoot, ...]:
    # Linux installs use both layouts: Toolbox/newer IDEs keep plugins as
    # direct children of <Product>/, while tarball/older/relocated installs
    # nest them under <Product>/plugins/. Emit both shapes per Linux root; a
    # flat install has no plugins/ subdir (layout resolution skips it) and a
    # nested install's plugins/ dir itself carries no plugin.xml, so the two
    # walks never double-count one plugin.
    linux_relative = Path(".local") / "share" / "JetBrains"
    roots = [
        _DataRoot(home, linux_relative, None),
        _DataRoot(home, linux_relative, "plugins"),
        _DataRoot(
            home,
            Path("Library") / "Application Support" / "JetBrains",
            "plugins",
        ),
        _DataRoot(
            home,
            Path("AppData") / "Roaming" / "JetBrains",
            "plugins",
        ),
    ]
    if include_native_env:
        appdata = os.environ.get("APPDATA")
        xdg_data_home = os.environ.get("XDG_DATA_HOME")
        if appdata:
            roots.append(_DataRoot(Path(appdata), Path("JetBrains"), "plugins"))
        if xdg_data_home:
            xdg_root = Path(xdg_data_home)
            roots.extend(
                (
                    _DataRoot(xdg_root, Path("JetBrains"), None),
                    _DataRoot(xdg_root, Path("JetBrains"), "plugins"),
                )
            )
    return tuple(dict.fromkeys(roots))


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


def _resolve_data_root(
    current_home: Path,
    data_root: _DataRoot,
    *,
    resolver: SymlinkLayoutResolver,
) -> Path | None:
    try:
        base_relative = data_root.approved_root.relative_to(current_home)
    except ValueError:
        base_relative = None
    if base_relative is not None:
        return resolver.resolve_directory(
            current_home,
            base_relative / data_root.relative,
        )
    if is_link_or_reparse(
        data_root.approved_root
    ) and not has_link_or_reparse_component(data_root.approved_root.parent):
        resolved_base = resolver.resolve_intermediate_link(
            data_root.approved_root,
            current=data_root.approved_root.parent,
        )
        return (
            resolver.resolve_directory(
                resolved_base,
                data_root.relative,
                claim_final=True,
            )
            if resolved_base is not None
            else None
        )
    if is_real_directory(data_root.approved_root) and not has_link_or_reparse_component(
        data_root.approved_root
    ):
        return resolver.resolve_directory(
            data_root.approved_root,
            data_root.relative,
        )
    return None


def _iter_product_dirs(
    resolved_data_root: Path,
    *,
    current_home: Path,
    checkpoint: Callable[[], None] | None,
) -> Generator[Path, None, None]:
    # A generator can be closed explicitly when the bounded collection ends.
    product_dir_iterator = iter_directory_entries(resolved_data_root)
    product_dirs: list[Path] = []
    try:
        for product_dir in islice(
            product_dir_iterator,
            MAX_PRODUCT_DIRS_PER_ROOT + 1,
        ):
            if checkpoint is not None:
                checkpoint()
            product_dirs.append(product_dir)
    finally:
        product_dir_iterator.close()
    yield from sorted(product_dirs[:MAX_PRODUCT_DIRS_PER_ROOT])
    if len(product_dirs) > MAX_PRODUCT_DIRS_PER_ROOT:
        logger.warning(
            "jetbrains_plugin_scan_capped",
            home=str(current_home),
            host_root=str(resolved_data_root),
            cap=MAX_PRODUCT_DIRS_PER_ROOT,
        )


def _resolve_plugin_root(
    product_entry: Path,
    data_root: _DataRoot,
    *,
    current_home: Path,
    resolved_data_root: Path,
    resolver: SymlinkLayoutResolver,
) -> Path | None:
    if is_link_or_reparse(product_entry):
        product_dir = (
            resolver.resolve_intermediate_link(
                product_entry,
                current=resolved_data_root,
            )
            if data_root.plugin_subdirectory is not None
            else resolver.resolve_policy_link(
                product_entry,
                current=resolved_data_root,
            )
        )
    elif is_real_directory(product_entry):
        try:
            product_dir = product_entry.resolve(strict=True)
        except (OSError, RuntimeError):
            product_dir = None
    else:
        product_dir = None
    if product_dir is None or not is_real_directory(product_dir):
        logger.debug(
            "jetbrains_plugin_scan_directory_skipped",
            stage="product_dir",
            home=str(current_home),
            path=str(product_entry),
            reason="not_contained_real_directory",
        )
        return None
    plugin_root = (
        resolver.resolve_directory(
            product_dir,
            Path(data_root.plugin_subdirectory),
            claim_final=is_link_or_reparse(product_entry),
        )
        if data_root.plugin_subdirectory is not None
        else product_dir
    )
    if plugin_root is None:
        logger.debug(
            "jetbrains_plugin_scan_directory_skipped",
            stage="plugin_root",
            home=str(current_home),
            path=str(product_dir / (data_root.plugin_subdirectory or "")),
            reason="not_contained_real_directory",
        )
    return plugin_root


def scan_jetbrains_plugins(
    *,
    home: Path | None = None,
    extra_home_roots: Sequence[Path] = (),
    checkpoint: Callable[[], None] | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Enumerate JetBrains plugins fairly within one scan-wide entry budget."""
    native_home = home or Path.home()
    artifacts: list[DiscoveredPluginArtifact] = []
    windows_system_context = is_windows_system_context()
    homes = _resolve_home_roots(
        (native_home, *extra_home_roots),
        windows_system_context=windows_system_context,
    )
    data_roots = tuple(
        (current_home, data_root)
        for home_index, current_home in enumerate(homes)
        for data_root in _data_roots(
            current_home,
            include_native_env=home is None and home_index == 0,
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
    scheduled_plugin_roots: set[str] = set()
    seen_plugin_paths: set[str] = set()
    root_iterators: deque[tuple[str, Generator[Path, None, None]]] = deque()

    for current_home, data_root in data_roots:
        resolved_data_root = _resolve_data_root(
            current_home,
            data_root,
            resolver=resolver,
        )
        if resolved_data_root is None:
            logger.debug(
                "jetbrains_plugin_scan_directory_skipped",
                stage="data_root",
                home=str(current_home),
                path=str(data_root.path),
                reason="not_contained_real_directory",
            )
            continue
        symlink_policy.add_scan_area(resolved_data_root, 0)
        for product_entry in _iter_product_dirs(
            resolved_data_root,
            current_home=current_home,
            checkpoint=checkpoint,
        ):
            product_name = product_entry.name
            plugin_root = _resolve_plugin_root(
                product_entry,
                data_root,
                current_home=current_home,
                resolved_data_root=resolved_data_root,
                resolver=resolver,
            )
            if plugin_root is None:
                continue
            symlink_policy.add_scan_area(plugin_root, 0)
            root_key = realpath_key(plugin_root)
            if root_key in scheduled_plugin_roots:
                continue
            scheduled_plugin_roots.add(root_key)
            client = _product_client(product_name)
            root_iterators.append((client, iter_directory_entries(plugin_root)))

    def _visit(client: str, plugin_path: Path) -> None:
        try:
            if is_link_or_reparse(plugin_path):
                target = resolver.resolve_policy_link(
                    plugin_path,
                    current=plugin_path.parent,
                )
                if target is None:
                    target = _resolve_top_level_jar_link(
                        plugin_path,
                        policy=symlink_policy,
                    )
                if target is None:
                    return
                plugin_path = target
            plugin_path = plugin_path.resolve(strict=True)
            plugin_key = realpath_key(plugin_path)
            if plugin_key in seen_plugin_paths:
                return
            seen_plugin_paths.add(plugin_key)
            symlink_policy.mark_visited(plugin_path)
            artifact = _artifact(
                plugin_path,
                client,
                windows_system_context=windows_system_context,
                policy=symlink_policy,
                resolver=resolver,
            )
        except (OSError, RuntimeError):
            return
        if artifact is not None:
            artifacts.append(artifact)

    entries_consumed = drain_round_robin(
        root_iterators,
        visit=_visit,
        max_entries=MAX_PLUGINS_PER_SCAN,
        checkpoint=checkpoint,
    )

    if entries_consumed == MAX_PLUGINS_PER_SCAN:
        logger.warning(
            "jetbrains_plugin_scan_capped",
            cap=MAX_PLUGINS_PER_SCAN,
        )

    return artifacts
