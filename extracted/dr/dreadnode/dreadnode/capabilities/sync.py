"""Capability sync — downloads capabilities from the platform.

See specs/capabilities/runtime.md (CAP-LOAD-010..013).
"""

from __future__ import annotations

import asyncio
import io
import posixpath
import shutil
import tarfile
import time
import typing as t
from dataclasses import dataclass, field

from loguru import logger

from dreadnode.capabilities.capability import (
    read_local_capability_records,
    write_local_capability_records,
)

if t.TYPE_CHECKING:
    from pathlib import Path

    from dreadnode.app.api.client import ApiClient


def install_local(
    *,
    source_path: Path,
    local_dir: Path,
    state_path: Path,
    name: str,
    version: str,
    overwrite: bool,
    copy: bool = False,
) -> LocalInstallResult:
    """Install a capability from a local directory into the user store.

    By default, creates a symlink so edits to the source are live.
    Pass ``copy=True`` to create a frozen snapshot instead.

    The caller is responsible for validating the capability before calling
    this function (e.g. via ``Capability(source_path)``).
    """
    import pathlib

    local_dir.mkdir(parents=True, exist_ok=True)
    target_dir = local_dir / name

    if target_dir.exists() or target_dir.is_symlink():
        if not overwrite:
            raise FileExistsError(f"Capability already exists locally: {name}")
        if target_dir.is_symlink() or target_dir.is_file():
            target_dir.unlink()
        else:
            shutil.rmtree(target_dir)

    resolved_source = pathlib.Path(source_path).resolve()

    if copy:
        temp_dir = local_dir / f".tmp-{name}"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        try:
            shutil.copytree(resolved_source, temp_dir)
            temp_dir.rename(target_dir)
        except Exception:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            raise
    else:
        target_dir.symlink_to(resolved_source)

    records = read_local_capability_records(state_path)
    records[name] = {
        "enabled": True,
        "source": "local",
        "version": version,
        "artifact_identity": name,
    }
    write_local_capability_records(state_path, records)

    return LocalInstallResult(
        installed_name=name,
        source="local",
        overwritten=overwrite,
    )


@dataclass
class SyncError:
    """A capability that failed to sync."""

    name: str
    error: str


@dataclass
class SyncResult:
    """Result of runtime sync operation."""

    synced: list[str] = field(default_factory=list)
    cached: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    errors: list[SyncError] = field(default_factory=list)
    bindings: list[dict[str, t.Any]] = field(default_factory=list)


@dataclass
class LocalInstallResult:
    """Result of a local registry-backed capability install."""

    installed_name: str
    source: str
    overwritten: bool = False


@dataclass
class LocalUninstallResult:
    """Result of uninstalling a local capability."""

    name: str
    removed_disk: bool
    removed_state: bool
    was_symlink: bool


def uninstall_local(
    *,
    name: str,
    local_dir: Path,
    state_path: Path,
) -> LocalUninstallResult:
    """Uninstall a locally-managed capability.

    Removes the on-disk entry first (symlink or directory), then the state
    record. Idempotent: a missing disk entry or state record is not an error.

    Symlinks (created by ``install_local`` for local-path installs) are
    unlinked, never followed. ``shutil.rmtree`` would refuse a symlink with
    ``OSError`` — we mirror the install-side branching at ``install_local``.
    """
    target_dir = local_dir / name
    was_symlink = target_dir.is_symlink()
    removed_disk = False

    if target_dir.is_symlink() or target_dir.is_file():
        target_dir.unlink()
        removed_disk = True
    elif target_dir.is_dir():
        shutil.rmtree(target_dir)
        removed_disk = True

    records = read_local_capability_records(state_path)
    removed_state = name in records
    if removed_state:
        records.pop(name, None)
        write_local_capability_records(state_path, records)

    return LocalUninstallResult(
        name=name,
        removed_disk=removed_disk,
        removed_state=removed_state,
        was_symlink=was_symlink,
    )


def encode_capability_dirname(name: str) -> str:
    """Encode a capability name for use as a directory name.

    Replaces '/' with '_' to avoid nested directories. This is bijective
    because capability name parts follow [a-z0-9][a-z0-9-]* (no underscores).
    e.g., 'acme/github' -> 'acme_github'
    """
    return name.replace("/", "_")


def decode_capability_dirname(dirname: str) -> str:
    """Decode a directory name back to a capability name.

    Replaces the first '_' with '/' (canonical names have exactly one '/').
    e.g., 'acme_github' -> 'acme/github'
    """
    return dirname.replace("_", "/", 1)


def bare_capability_name(qualified_name: str) -> str:
    """Extract the bare name from an org-qualified capability name.

    e.g., 'acme/github' -> 'github'
    If no '/' present, returns the name as-is.
    """
    if "/" in qualified_name:
        return qualified_name.split("/", 1)[1]
    return qualified_name


def _extract_tar_to_dir(data: bytes, target: Path) -> None:
    """Extract a tar.gz bundle into target directory with path safety checks."""
    target.mkdir(parents=True, exist_ok=True)

    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.issym() or member.islnk():
                raise ValueError(f"Tar entry contains symlink/hardlink: {member.name}")
            if not member.isfile():
                continue

            normalized = posixpath.normpath(member.name)
            if normalized.startswith(("..", "/")):
                raise ValueError(f"Tar entry escapes boundary: {member.name}")
            if "\x00" in member.name or "\\" in member.name:
                raise ValueError(f"Tar entry has invalid characters: {member.name}")
            if normalized.startswith(".git/") or normalized == ".git":
                continue

            f = tar.extractfile(member)
            if f is None:
                continue

            dest = target / normalized
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(f.read())
            # Preserve the executable bit from the tar member. Capability
            # scripts (install scripts, tool wrappers like scripts/pd-tool)
            # ship as 0755 but write_bytes creates 0644, so a stripped +x
            # left runtime checks (`test -x`) and direct execs failing.
            if member.mode & 0o111:
                dest.chmod(dest.stat().st_mode | (member.mode & 0o111))


class CapabilitySyncClient:
    """Downloads runtime capabilities from the platform into a local cache.

    CAP-LOAD-010: sync before runtime starts.
    CAP-LOAD-012: cache is runtime-managed.
    CAP-LOAD-013: produces same directory layout the loader expects.
    """

    def __init__(
        self,
        api: ApiClient,
        org: str,
        workspace: str,
        cache_dir: Path,
        runtime_id: str,
    ) -> None:
        self._api = api
        self._org = org
        self._workspace = workspace
        self._runtime_id = runtime_id
        self._cache_dir = cache_dir

    async def sync(self) -> SyncResult:
        """Sync runtime capabilities from the platform.

        Downloads enabled capabilities into the cache directory.
        Uses digest-based caching to skip unchanged capabilities.
        """
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        # 1. Fetch resolved capabilities (let exceptions propagate)
        try:
            resolved = self._api.get_runtime_capabilities_resolved(
                self._org,
                self._workspace,
                self._runtime_id,
            )
        except RuntimeError as exc:
            if self._is_not_found_error(exc):
                logger.debug(
                    "Runtime capability resolution returned 404 for '{}'; treating as empty result",
                    self._runtime_id,
                )
                return SyncResult()
            raise
        resolved_caps = resolved.get("capabilities", [])
        logger.info(
            "Resolved {} capabilities for runtime {}: {}",
            len(resolved_caps),
            self._runtime_id,
            [c["name"] for c in resolved_caps] or "(none)",
        )

        result = SyncResult()
        resolved_names: set[str] = set()

        # 2. Sync each resolved capability
        for cap_info in resolved_caps:
            name = cap_info["name"]
            resolved_names.add(name)
            encoded = encode_capability_dirname(name)
            cap_dir = self._cache_dir / encoded
            digest = cap_info.get("runtime_digest", "")

            # Check cache
            digest_file = cap_dir / ".runtime_digest"
            if digest_file.exists() and digest_file.read_text().strip() == digest:
                logger.debug("Capability '{}' unchanged (digest match), using cache", name)
                result.cached.append(name)
                continue

            # Download to temp dir, atomic rename on success
            temp_dir = self._cache_dir / f".tmp-{encoded}"
            try:
                self._download_capability(cap_info, temp_dir)

                # Write digest marker
                (temp_dir / ".runtime_digest").write_text(digest)

                # Atomic replace: remove old, rename temp
                if cap_dir.exists():
                    shutil.rmtree(cap_dir)
                temp_dir.rename(cap_dir)

                result.synced.append(name)
            except Exception as e:
                logger.warning("Failed to sync capability '{}': {}", name, e)
                result.errors.append(SyncError(name=name, error=str(e)))
                # Clean up temp dir on failure
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)

        # 3. Remove stale cached capabilities
        if self._cache_dir.exists():
            for entry in self._cache_dir.iterdir():
                if not entry.is_dir() or entry.name.startswith("."):
                    continue
                decoded = decode_capability_dirname(entry.name)
                if decoded not in resolved_names:
                    shutil.rmtree(entry)
                    result.removed.append(decoded)

        # 4. Fetch full binding list (best-effort — enrichment data)
        try:
            bindings_response = self._api.list_runtime_capabilities(
                self._org,
                self._workspace,
                self._runtime_id,
            )
            result.bindings = bindings_response.get("items", [])
        except Exception:
            logger.warning("Failed to fetch runtime bindings — proceeding without binding metadata")

        return result

    @staticmethod
    def _is_not_found_error(exc: RuntimeError) -> bool:
        return str(exc).startswith("404:")

    def _download_capability(
        self,
        cap_info: dict[str, t.Any],
        target_dir: Path,
    ) -> None:
        """Download all files for a single capability into target_dir."""
        from dreadnode.app.cli.shared import ArtifactRef

        ref = ArtifactRef.parse(cap_info["name"], self._org).with_version(cap_info["version"])

        # Clean target if it exists (partial previous attempt)
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True)

        # Try bulk download first, fall back to file-by-file
        if self._try_bulk_download(ref.org, ref.name, ref.version, target_dir):
            return

        # Fallback: download each file individually
        detail = self._api.get_capability(ref.org, ref.name, ref.version)
        file_manifest = detail.get("file_manifest", [])

        for entry in file_manifest:
            file_path = entry["path"]
            content = self._api.get_capability_file(ref.org, ref.name, ref.version, file_path)
            dest = target_dir / file_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content if isinstance(content, bytes) else content.encode())

    def _try_bulk_download(
        self,
        org: str,
        name: str,
        version: str,
        target_dir: Path,
    ) -> bool:
        """Attempt to download and extract the tar.gz bundle. Returns True on success."""
        try:
            data = self._api.download_capability_bundle(org, name, version)
            _extract_tar_to_dir(data, target_dir)
            logger.debug("Bulk download succeeded for capability '{}' v{}", name, version)
        except Exception as exc:
            logger.debug(
                "Bulk download unavailable for '{}' v{}, falling back to file-by-file: {}",
                name,
                version,
                exc,
            )
            return False
        else:
            return True


class LocalInstallClient:
    """Install registry-backed capabilities into the local user store."""

    def __init__(
        self,
        api: ApiClient,
        org: str,
        local_dir: Path,
        state_path: Path,
    ) -> None:
        self._api = api
        self._org = org
        self._local_dir = local_dir
        self._state_path = state_path

    async def install(
        self,
        *,
        name: str,
        version: str,
        source: str,
        overwrite: bool,
    ) -> LocalInstallResult:
        return await asyncio.to_thread(
            self._install_sync,
            name=name,
            version=version,
            source=source,
            overwrite=overwrite,
        )

    def _install_sync(
        self,
        *,
        name: str,
        version: str,
        source: str,
        overwrite: bool,
    ) -> LocalInstallResult:
        started_at = time.perf_counter()
        logger.info(
            "Local capability install start | name={} | version={} | source={} | overwrite={}",
            name,
            version,
            source,
            overwrite,
        )
        self._local_dir.mkdir(parents=True, exist_ok=True)

        resolve_started_at = time.perf_counter()
        detail, fetch_file = self._resolve_detail(name=name, version=version)
        resolve_ms = (time.perf_counter() - resolve_started_at) * 1000
        manifest = detail.get("manifest", {})
        local_name = str(manifest.get("name") or bare_capability_name(name))
        file_manifest = detail.get("file_manifest", [])
        total_files = len(file_manifest)
        manifest_total_bytes = sum(
            int(entry.get("size_bytes", 0))
            for entry in file_manifest
            if isinstance(entry.get("size_bytes"), int)
        )
        logger.debug(
            "Local capability install detail resolved | name={} | installed_name={} | files={} | manifest_bytes={} | resolve_ms={:.1f}",
            name,
            local_name,
            total_files,
            manifest_total_bytes,
            resolve_ms,
        )

        target_dir = self._local_dir / local_name
        temp_dir = self._local_dir / f".tmp-{local_name}"

        if target_dir.exists():
            if not overwrite:
                raise FileExistsError(f"Capability already exists locally: {local_name}")
            shutil.rmtree(target_dir)

        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)

        try:
            download_started_at = time.perf_counter()

            # Try bulk download first
            bulk_ok = self._try_bulk_download(name=name, version=version, target_dir=temp_dir)

            if not bulk_ok:
                # Fallback: download each file individually
                downloaded_bytes = 0
                for index, entry in enumerate(file_manifest, start=1):
                    file_path = entry["path"]
                    content = fetch_file(file_path)
                    content_bytes = content if isinstance(content, bytes) else content.encode()
                    dest = temp_dir / file_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(content_bytes)
                    downloaded_bytes += len(content_bytes)
                    if index in (1, total_files) or index % 25 == 0:
                        logger.debug(
                            "Local capability install progress | name={} | files={}/{} | downloaded_bytes={} | elapsed_ms={:.1f} | current_file={}",
                            name,
                            index,
                            total_files,
                            downloaded_bytes,
                            (time.perf_counter() - download_started_at) * 1000,
                            file_path,
                        )

            rename_started_at = time.perf_counter()
            temp_dir.rename(target_dir)
            rename_ms = (time.perf_counter() - rename_started_at) * 1000
        except Exception:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            raise

        state_write_started_at = time.perf_counter()
        route_org, bare_name = self._route(name)
        artifact_identity = f"{route_org}/{bare_name}"
        records = read_local_capability_records(self._state_path)
        records[local_name] = {
            "enabled": True,
            "source": source,
            "version": version,
            "artifact_identity": artifact_identity,
            "digest": detail.get("runtime_digest"),
            "artifact_sha256": detail.get("artifact_sha256"),
        }
        write_local_capability_records(self._state_path, records)
        state_write_ms = (time.perf_counter() - state_write_started_at) * 1000
        total_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "Local capability install complete | name={} | installed_name={} | files={} | manifest_bytes={} | total_ms={:.1f} | resolve_ms={:.1f} | rename_ms={:.1f} | state_write_ms={:.1f}",
            name,
            local_name,
            total_files,
            manifest_total_bytes,
            total_ms,
            resolve_ms,
            rename_ms,
            state_write_ms,
        )

        return LocalInstallResult(
            installed_name=local_name,
            source=source,
            overwritten=overwrite,
        )

    def _route(self, name: str) -> tuple[str, str]:
        """Resolve the owning org and bare name for API routing.

        Org-qualified names (``dreadnode/web-security``) route through the
        owning org; bare names fall back to ``self._org``.
        """
        from dreadnode.app.cli.shared import ArtifactRef

        ref = ArtifactRef.parse(name, self._org)
        return ref.org, ref.name

    def _try_bulk_download(
        self,
        *,
        name: str,
        version: str,
        target_dir: Path,
    ) -> bool:
        """Attempt bulk tar.gz download. Returns True on success."""
        org, bare_name = self._route(name)
        try:
            data = self._api.download_capability_bundle(org, bare_name, version)
            _extract_tar_to_dir(data, target_dir)
            logger.debug("Bulk download succeeded for capability '{}' v{}", name, version)
        except Exception as exc:
            logger.debug(
                "Bulk download unavailable for '{}' v{}, falling back to file-by-file: {}",
                name,
                version,
                exc,
            )
            return False
        else:
            return True

    def _resolve_detail(
        self,
        *,
        name: str,
        version: str,
    ) -> tuple[dict[str, t.Any], t.Callable[[str], bytes]]:
        org, bare_name = self._route(name)
        detail = self._api.get_capability(org, bare_name, version)

        def fetch_file(file_path: str) -> bytes:
            return self._api.get_capability_file(org, bare_name, version, file_path)

        return detail, fetch_file
