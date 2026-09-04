import hashlib
import json
import os
import threading
import time
import typing as t
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import fsspec
from fsspec import AbstractFileSystem
from loguru import logger

from dreadnode.app.api.models import StorageCredentials
from dreadnode.app.config import Profile
from dreadnode.core.util import resolve_endpoint
from dreadnode.storage.providers import StorageProvider, from_provider
from dreadnode.storage.session_store import SessionStore

if t.TYPE_CHECKING:
    from dreadnode.app.api.client import ApiClient
    from dreadnode.packaging.oci import OCIRegistryClient

T = t.TypeVar("T")

PackageType = t.Literal["datasets", "models", "environments", "capabilities"]


class Storage:
    """Storage manager for local and remote storage.

    Directory structure:

    ```
    ~/.dreadnode/
      packages/
        datasets/
        agents/
        models/
        tools/
        environments/
      capabilities/
        <capability_name>/
          capability.yaml
      cas/
        sha256/
          ab/cd/...
      artifacts/
      reports/
        <YYYYMMDD-HHMMSS>-<title>.md
      tool-output/
        <YYYYMMDD-HHMMSS>-<tool_call_id>.txt
      projects/
        <project_key>/
          <run_id>/
            spans.jsonl
            metrics.jsonl
      sessions/
        sessions.sqlite3
        <session_id>/
          spans_<session_id>.jsonl
      optimizations/
        <job_id>/
          iter-<NNNN>/
            <candidate_short_hash>/   ← materialized capability tree
            candidate.json            ← input dict
          job.json                    ← terminal-only frontier hashes
    ```

    Remote operations use an fsspec-compatible object-storage client. In a
    managed sandbox, the local cache remains on the sandbox filesystem; it is
    not an object-storage mount.
    """

    def __init__(
        self,
        profile: Profile | None = None,
        cache: Path | None = None,
        api: "ApiClient | None" = None,
        provider: StorageProvider | None = None,
        *,
        default_project: str | None = None,
    ):
        """Create storage manager.

        Args:
            profile: Authenticated profile for RBAC context.
            cache: Root cache directory. Defaults to ~/.dreadnode.
            api: API client for remote operations (blob credentials + registry uploads).
            provider: Storage provider for remote operations (s3, r2, minio).
            default_project: Default project key.
        """
        self._profile = profile
        self._cache = cache or Path.home() / ".dreadnode"
        self._api = api
        self._provider = provider
        self._default_project = default_project

        # Remote filesystem state
        self._remote_fs: AbstractFileSystem | None = None
        self._local_fs: AbstractFileSystem | None = None
        self._credentials: StorageCredentials | None = None
        self._expiration: datetime | None = None
        self._lock = threading.Lock()
        self._session_store: SessionStore | None = None

    @property
    def profile(self) -> Profile | None:
        """Get the current profile."""
        return self._profile

    @property
    def api(self) -> "ApiClient | None":
        """Get the API client."""
        return self._api

    @property
    def project_key(self) -> str:
        """Get the project key."""
        if self._profile is not None:
            return self._profile.project_key or "default"
        return self._default_project or "default"

    @property
    def can_sync(self) -> bool:
        """Whether remote sync is possible (has API client and profile)."""
        return self._api is not None and self._profile is not None and not self._provider

    # =========================================================================
    # Path Properties
    # =========================================================================

    @property
    def packages_path(self) -> Path:
        """Path to packages directory."""
        return self._cache / "packages"

    @property
    def cas_path(self) -> Path:
        """Path to CAS directory."""
        return self._cache / "cas"

    @property
    def artifacts_path(self) -> Path:
        """Path to artifacts CAS."""
        return self._cache / "artifacts"

    @property
    def reports_path(self) -> Path:
        """Path to the reports directory written by the ``report`` tool."""
        return self._cache / "reports"

    @property
    def tool_output_path(self) -> Path:
        """Path to the offloaded tool-output directory."""
        return self._cache / "tool-output"

    @property
    def capabilities_path(self) -> Path:
        """Path to capabilities directory."""
        return self._cache / "capabilities"

    @property
    def workspace_capabilities_path(self) -> Path:
        """Path to workspace capability cache directory (CAP-LOAD-007)."""
        override = os.environ.get("DREADNODE_WORKSPACE_CAPABILITIES_DIR")
        if override:
            return Path(override)
        return self._cache / "workspace-capabilities"

    @property
    def local_capability_state_path(self) -> Path:
        """Path to persisted local capability state."""
        return self._cache / "local-capability-state.json"

    @property
    def sessions_path(self) -> Path:
        """Path to sessions directory."""
        return self._cache / "sessions"

    @property
    def session_db_path(self) -> Path:
        """Path to the local SQLite session index."""
        self.sessions_path.mkdir(parents=True, exist_ok=True)
        return self.sessions_path / "sessions.sqlite3"

    @property
    def session_store(self) -> SessionStore:
        """Lazy SQLite-backed session metadata and message store."""
        if self._session_store is None:
            self._session_store = SessionStore(self.session_db_path)
        return self._session_store

    def session_path(self, session_id: str | UUID) -> Path:
        """Path to a session directory."""
        return self.sessions_path / str(session_id)

    def session_spans_path(self, session_id: str | UUID, ext: str = "jsonl") -> Path:
        """Path to a session-scoped tracing file."""
        session_dir = self.session_path(session_id)
        session_dir.mkdir(parents=True, exist_ok=True)
        session_str = str(session_id)
        return session_dir / f"spans_{session_str}.{ext}"

    @property
    def projects_path(self) -> Path:
        """Path to projects directory."""
        return self._cache / "projects"

    @property
    def project_path(self) -> Path:
        """Path to current project directory."""
        return self.projects_path / self.project_key

    def run_path(self, run_id: str | UUID) -> Path:
        """Path to run directory for trace data."""
        return self.project_path / str(run_id)

    def trace_path(self, run_id: str | UUID, filename: str = "spans.jsonl") -> Path:
        """Path to trace file within a run directory.

        Args:
            run_id: The run identifier.
            filename: Full filename with extension (e.g., 'spans.jsonl', 'spans.parquet').

        Returns:
            Full path to the trace file.
        """
        run_dir = self.run_path(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir / filename

    @property
    def optimizations_path(self) -> Path:
        """Path to optimization artifacts directory."""
        return self._cache / "optimizations"

    def optimization_job_path(self, job_id: str | UUID) -> Path:
        """Path to a specific optimization job's artifacts."""
        return self.optimizations_path / str(job_id)

    def optimization_iteration_path(
        self,
        job_id: str | UUID,
        iteration: int,
    ) -> Path:
        """Path to a specific iteration's artifacts under a job.

        Iterations are zero-padded so directory listings sort correctly.
        """
        return self.optimization_job_path(job_id) / f"iter-{iteration:04d}"

    def optimization_candidate_path(
        self,
        job_id: str | UUID,
        iteration: int,
        candidate_hash: str,
    ) -> Path:
        """Path to a specific candidate's materialized capability tree.

        ``candidate_hash`` is shortened to 12 chars in the path so directory
        names stay readable; pass a content-derived hex digest (e.g.
        ``hashlib.sha256(canonical_json).hexdigest()``).
        """
        short = candidate_hash[:12]
        return self.optimization_iteration_path(job_id, iteration) / short

    def list_local_runs(self) -> list[str]:
        """List locally cached run IDs for the current project."""
        if not self.project_path.exists():
            return []

        run_ids: list[str] = []
        for entry in self.project_path.iterdir():
            if not entry.is_dir():
                continue
            if any(
                child.is_file() and child.name.startswith("spans.") for child in entry.iterdir()
            ):
                run_ids.append(entry.name)

        return sorted(run_ids)

    # =========================================================================
    # Remote Filesystem
    # =========================================================================

    @property
    def remote_bucket(self) -> str:
        """Get the remote storage bucket from credentials."""
        if self._credentials is None:
            self._get_filesystem()
        if self._credentials is None:
            raise RuntimeError("No credentials available for remote storage")
        return self._credentials.bucket

    @property
    def remote_prefix(self) -> str:
        """Get the remote storage prefix from credentials."""
        if self._credentials is None:
            self._get_filesystem()
        if self._credentials is None:
            raise RuntimeError("No credentials available for remote storage")
        return self._credentials.prefix

    def _get_filesystem(self) -> AbstractFileSystem:
        """Get filesystem, refreshing credentials if needed.

        Falls back to local filesystem if no API client.
        """
        with self._lock:
            if self._remote_fs is not None and not self._credentials_expired():
                return self._remote_fs

            if not self.can_sync:
                self._remote_fs = from_provider("local")
                return self._remote_fs

            try:
                self._credentials = self._refresh_credentials()
                provider = self._provider or ("minio" if self._credentials.endpoint else "s3")
                resolved_endpoint = resolve_endpoint(self._credentials.endpoint)

                logger.debug(
                    "Storage credentials obtained: provider={}, bucket={}, prefix={}, endpoint={}, expires={}",
                    provider,
                    self._credentials.bucket,
                    self._credentials.prefix,
                    resolved_endpoint,
                    self._credentials.expiration,
                )

                self._remote_fs = from_provider(
                    provider,
                    {
                        "access_key_id": self._credentials.access_key_id,
                        "secret_access_key": self._credentials.secret_access_key,
                        "session_token": self._credentials.session_token,
                        "endpoint_url": resolved_endpoint,
                        "region": self._credentials.region,
                    },
                )
                self._expiration = self._credentials.expiration

            except Exception as exc:
                logger.debug(
                    "Remote storage credentials unavailable, using local filesystem: {}", exc
                )
                self._remote_fs = from_provider("local")

            return self._remote_fs

    def _refresh_credentials(self) -> StorageCredentials:
        """Refresh storage credentials from the API."""
        if self._api is None:
            raise RuntimeError("No API client configured for remote storage")
        if self._profile is None:
            raise RuntimeError("No profile configured for storage credentials")
        return self._api.get_storage_access(
            self._profile.org_key,
            self._profile.workspace_key,
        )

    def _credentials_expired(self) -> bool:
        """Check if credentials are expired or about to expire."""
        if self._expiration is None:
            return False
        now = datetime.now(UTC)
        expiry = self._expiration
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=UTC)
        # Refresh 15 minutes before expiry
        return (expiry - now).total_seconds() < 900

    def _is_local_filesystem(self) -> bool:
        """Check if the current filesystem is local."""
        from fsspec.implementations.local import LocalFileSystem

        fs = self._get_filesystem()
        return isinstance(fs, LocalFileSystem)

    def _execute_with_retry(
        self,
        operation: t.Callable[[], T],
        max_retries: int = 3,
        sleep_fn: t.Callable[[float], None] = time.sleep,
    ) -> T:
        """Execute a remote fs operation with retry on auth errors.

        On auth failure (expired/invalid STS credentials), invalidates the
        cached filesystem so the next _get_filesystem() call refreshes
        credentials, then retries with linear backoff.
        """
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                if _is_auth_error(e) and attempt < max_retries - 1:
                    logger.debug(
                        "Auth error on attempt {}/{}, refreshing credentials: {}",
                        attempt + 1,
                        max_retries,
                        e,
                    )
                    with self._lock:
                        self._remote_fs = None
                    sleep_fn(attempt + 1)
                    continue
                raise
        raise RuntimeError("Max retries exhausted")  # unreachable

    # =========================================================================
    # Blob Operations (CAS)
    # =========================================================================

    def blob_path(self, oid: str) -> Path:
        """Path to blob in CAS."""
        algo, hash_val = oid.split(":", 1)
        return self.cas_path / algo / hash_val[:2] / hash_val[2:4] / hash_val

    def remote_blob_path(self, oid: str) -> str:
        """Remote path for blob, including the provider bucket."""
        algo, hash_val = oid.split(":", 1)
        bucket = self._credentials.bucket if self._credentials else "user-data"
        return f"{bucket}/{self.remote_prefix}/cas/{algo}/{hash_val[:2]}/{hash_val[2:4]}/{hash_val}"

    def blob_exists(self, oid: str) -> bool:
        """Check if blob exists in local CAS."""
        return self.blob_path(oid).exists()

    def remote_blob_exists(self, oid: str) -> bool:
        """Check if blob exists in remote storage."""

        def _op() -> bool:
            fs = self._get_filesystem()
            return bool(fs.exists(self.remote_blob_path(oid)))

        return self._execute_with_retry(_op)

    def store_blob(self, oid: str, source: Path) -> Path:
        """Store blob in local CAS."""
        dest = self.blob_path(oid)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(source.read_bytes())
        return dest

    def get_blob(self, oid: str) -> Path:
        """Get blob from local CAS."""
        path = self.blob_path(oid)
        if not path.exists():
            raise FileNotFoundError(f"Blob not found: {oid}")
        return path

    # =========================================================================
    # Artifact Operations (Workspace-scoped CAS)
    # =========================================================================

    def artifact_blob_path(self, oid: str) -> Path:
        """Path to artifact blob in workspace CAS."""
        algo, hash_val = oid.split(":", 1)
        return self.artifacts_path / algo / hash_val[:2] / hash_val[2:4] / hash_val

    def remote_artifact_path(self, oid: str) -> str:
        """Remote path for artifact blob."""
        algo, hash_val = oid.split(":", 1)
        bucket = self._credentials.bucket if self._credentials else "user-data"
        return f"{bucket}/{self.remote_prefix}/artifacts/{algo}/{hash_val[:2]}/{hash_val[2:4]}/{hash_val}"

    def store_artifact(self, source: Path, *, upload: bool = True) -> str:
        """Store artifact in workspace CAS and optionally upload to remote.

        Args:
            source: Path to the file to store.
            upload: Whether to upload to remote storage immediately.

        Returns:
            The oid (sha256:<hash>) of the stored artifact.
        """
        file_hash = hash_file(source)
        oid = f"sha256:{file_hash}"

        # Store locally
        dest = self.artifact_blob_path(oid)
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(source.read_bytes())

        # Upload to remote if enabled (best-effort — local store already succeeded)
        if upload and self.can_sync:
            try:
                self.upload_artifact(oid)
            except Exception as exc:
                billing_message = _extract_credit_block_message(exc)
                if billing_message:
                    logger.warning(billing_message)
                else:
                    logger.warning(
                        "Remote artifact upload failed for {} (stored locally)", oid, exc_info=True
                    )

        return oid

    def upload_artifact(self, oid: str) -> None:
        """Upload artifact from workspace CAS to remote storage."""
        source = self.artifact_blob_path(oid)
        if not source.exists():
            raise FileNotFoundError(f"Artifact not found locally: {oid}")

        if not self.can_sync:
            return

        def _op() -> None:
            from fsspec.implementations.local import LocalFileSystem

            fs = self._get_filesystem()
            if isinstance(fs, LocalFileSystem):
                return

            remote_path = self.remote_artifact_path(oid)
            if not fs.exists(remote_path):
                fs.put_file(str(source), remote_path)

        self._execute_with_retry(_op)

    def get_artifact(self, oid: str) -> Path:
        """Get artifact from workspace CAS, downloading if needed."""
        local_path = self.artifact_blob_path(oid)
        if local_path.exists():
            return local_path

        # Try to download from remote
        if not self.can_sync:
            raise FileNotFoundError(f"Artifact not found: {oid}")

        def _op() -> Path:
            from fsspec.implementations.local import LocalFileSystem

            fs = self._get_filesystem()
            if isinstance(fs, LocalFileSystem):
                raise FileNotFoundError(f"Artifact not found: {oid}")

            remote_path = self.remote_artifact_path(oid)
            local_path.parent.mkdir(parents=True, exist_ok=True)
            fs.get_file(remote_path, str(local_path))

            # Verify hash
            _algo, expected = oid.split(":", 1)
            actual = hash_file(local_path)
            if actual != expected:
                local_path.unlink()
                raise ValueError(f"Artifact hash mismatch: expected {expected}, got {actual}")

            return local_path

        return self._execute_with_retry(_op)

    # =========================================================================
    # Batch Operations
    # =========================================================================

    def hash_files(self, paths: list[Path], algo: str = "sha256") -> dict[Path, str]:
        """Compute hashes for multiple files.

        Args:
            paths: Files to hash.
            algo: Hash algorithm.

        Returns:
            Mapping of path to hash.
        """
        return {p: hash_file(p, algo) for p in paths}

    def upload_blobs(
        self,
        files: dict[Path, str],
        *,
        skip_existing: bool = True,
    ) -> tuple[int, int]:
        """Upload multiple blobs to remote storage.

        Args:
            files: Mapping of local path to oid.
            skip_existing: Skip blobs that already exist remotely.

        Returns:
            Tuple of (uploaded_count, skipped_count).
        """

        def _op() -> tuple[int, int]:
            from fsspec.implementations.local import LocalFileSystem

            fs = self._get_filesystem()
            is_local = isinstance(fs, LocalFileSystem)

            sources: list[str] = []
            targets: list[str] = []
            skipped = 0

            for local_path, oid in files.items():
                target_path = str(self.blob_path(oid)) if is_local else self.remote_blob_path(oid)

                if skip_existing and fs.exists(target_path):
                    skipped += 1
                    continue

                sources.append(str(local_path))
                targets.append(target_path)

            if sources:
                if is_local:
                    for target in targets:
                        Path(target).parent.mkdir(parents=True, exist_ok=True)
                fs.put(sources, targets)

            return len(sources), skipped

        try:
            return self._execute_with_retry(_op)
        except Exception as exc:
            billing_message = _extract_credit_block_message(exc)
            if billing_message:
                logger.warning(billing_message)
            raise

    def download_blobs(
        self,
        oids: list[str],
        *,
        skip_existing: bool = True,
    ) -> tuple[int, int]:
        """Download multiple blobs from remote storage.

        Args:
            oids: Object IDs to download.
            skip_existing: Skip blobs that already exist locally.

        Returns:
            Tuple of (downloaded_count, skipped_count).
        """

        def _op() -> tuple[int, int]:
            fs = self._get_filesystem()

            sources: list[str] = []
            targets: list[str] = []
            downloaded_oids: list[str] = []
            skipped = 0

            for oid in oids:
                local_path = self.blob_path(oid)

                if skip_existing and local_path.exists():
                    skipped += 1
                    continue

                local_path.parent.mkdir(parents=True, exist_ok=True)
                sources.append(self.remote_blob_path(oid))
                targets.append(str(local_path))
                downloaded_oids.append(oid)

            if sources:
                fs.get(sources, targets)

                # Verify hashes
                for oid, target in zip(downloaded_oids, targets, strict=True):
                    algo, expected = oid.split(":", 1)
                    actual = hash_file(Path(target), algo)
                    if actual != expected:
                        Path(target).unlink()
                        raise ValueError(f"Hash mismatch for {oid}")

            return len(sources), skipped

        return self._execute_with_retry(_op)

    # =========================================================================
    # Single Blob Remote Operations
    # =========================================================================

    def download_blob(self, oid: str) -> Path:
        """Download blob from remote to local CAS."""
        dest = self.blob_path(oid)
        if dest.exists():
            return dest

        def _op() -> Path:
            fs = self._get_filesystem()
            remote_path = self.remote_blob_path(oid)

            dest.parent.mkdir(parents=True, exist_ok=True)
            fs.get_file(remote_path, str(dest))

            # Verify
            algo, expected = oid.split(":", 1)
            actual = hash_file(dest, algo)
            if actual != expected:
                dest.unlink()
                raise ValueError(f"Hash mismatch: expected {expected}, got {actual}")

            return dest

        return self._execute_with_retry(_op)

    def upload_blob(self, oid: str) -> None:
        """Upload blob from local CAS to remote."""
        source = self.blob_path(oid)
        if not source.exists():
            raise FileNotFoundError(f"Blob not found: {oid}")

        def _op() -> None:
            fs = self._get_filesystem()
            remote_path = self.remote_blob_path(oid)
            fs.put_file(str(source), remote_path)

        try:
            self._execute_with_retry(_op)
        except Exception as exc:
            billing_message = _extract_credit_block_message(exc)
            if billing_message:
                logger.warning(billing_message)
            raise

    # =========================================================================
    # Package Operations
    # =========================================================================

    def package_path(
        self,
        package_type: PackageType,
        name: str,
        version: str | None = None,
    ) -> Path:
        """Path to package directory.

        Returns: ~/.dreadnode/packages/<package_type>/<name>/[version/]
        """
        base = self.packages_path / package_type / name
        if version:
            return base / version
        return base

    def manifest_path(
        self,
        package_type: PackageType,
        name: str,
        version: str,
    ) -> Path:
        """Path to manifest.json."""
        return self.package_path(package_type, name, version) / "manifest.json"

    def store_manifest(
        self,
        package_type: PackageType,
        name: str,
        version: str,
        content: str,
    ) -> Path:
        """Store manifest.json."""
        path = self.manifest_path(package_type, name, version)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def get_manifest(
        self,
        package_type: PackageType,
        name: str,
        version: str,
    ) -> str:
        """Get manifest.json content."""
        return self.manifest_path(package_type, name, version).read_text()

    def manifest_exists(
        self,
        package_type: PackageType,
        name: str,
        version: str,
    ) -> bool:
        """Check if manifest exists."""
        return self.manifest_path(package_type, name, version).exists()

    def list_versions(
        self,
        package_type: PackageType,
        name: str,
    ) -> list[str]:
        """List available versions."""
        import re

        base = self.package_path(package_type, name)
        if not base.exists():
            return []
        version_pattern = re.compile(r"^\d+\.\d+\.\d+.*$")
        versions = [v.name for v in base.iterdir() if v.is_dir() and version_pattern.match(v.name)]
        return sorted(versions, reverse=True)

    def latest_version(
        self,
        package_type: PackageType,
        name: str,
    ) -> str | None:
        """Get latest version."""
        versions = self.list_versions(package_type, name)
        return versions[0] if versions else None

    # =========================================================================
    # OCI Registry
    # =========================================================================

    @property
    def oci_registry_url(self) -> str:
        """Get the OCI Distribution v2 registry URL."""
        if self._api is None:
            raise RuntimeError("No API client configured")
        return self._api.oci_registry_url

    def oci_client(self) -> "OCIRegistryClient":
        """Create an OCI registry client for push/pull operations."""
        from dreadnode.packaging.oci import OCIRegistryClient

        if self._api is None:
            raise RuntimeError("No API client configured")
        return OCIRegistryClient(
            self._api.oci_registry_url,
            auth=self._api.oci_basic_auth,
        )

    # =========================================================================
    # URI Resolution
    # =========================================================================

    def resolve(self, uri: str, **storage_options: t.Any) -> tuple[AbstractFileSystem, str]:
        """Resolve URI to filesystem and path."""
        fs, path = fsspec.url_to_fs(uri, **storage_options)
        return fs, path


def hash_file(path: Path, algo: str = "sha256") -> str:
    """Compute hash of file."""
    hasher = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def write_timestamped(directory: Path, name: str, content: str) -> Path:
    """Write text content to ``<directory>/<YYYYMMDD-HHMMSS>-<name>``.

    Creates ``directory`` if needed. On collision (same second + same name),
    appends ``-1``, ``-2``, ... before the file extension until a free name
    is found. Reservation is atomic via ``O_EXCL``.
    """
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    base = Path(name)
    stem, suffix = base.stem, base.suffix

    counter = 0
    while True:
        candidate = (
            f"{timestamp}-{name}" if counter == 0 else f"{timestamp}-{stem}-{counter}{suffix}"
        )
        path = directory / candidate
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            counter += 1
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        return path


def _is_auth_error(exc: Exception) -> bool:
    """Check if exception is a botocore auth error (expired/invalid credentials).

    Also checks the __cause__ chain to catch s3fs-wrapped exceptions
    (e.g. PermissionError wrapping botocore ClientError).
    """
    current: BaseException | None = exc
    while current is not None:
        if (
            type(current).__name__ == "ClientError"
            and hasattr(current, "response")
            and getattr(type(current), "__module__", "").startswith("botocore")
        ):
            error_code = getattr(current, "response", {}).get("Error", {}).get("Code", "")
            if error_code in (
                "ExpiredToken",
                "InvalidAccessKeyId",
                "SignatureDoesNotMatch",
                "AccessDenied",
            ):
                return True
        current = getattr(current, "__cause__", None)
    return False


def _extract_credit_block_message(exc: Exception) -> str | None:
    """Extract a storage billing error message from nested upload exceptions."""
    fallback = "Insufficient credits for storage — purchase credits to continue"

    for candidate in _iter_exception_chain(exc):
        status_code = _extract_status_code(candidate)
        detail = _extract_error_detail(candidate)

        if status_code == 429:
            return detail or fallback

        if detail and "credit" in detail.lower():
            return detail

    return None


def _iter_exception_chain(exc: Exception) -> t.Iterator[BaseException]:
    seen: set[int] = set()
    current: BaseException | None = exc

    while current is not None:
        marker = id(current)
        if marker in seen:
            return
        seen.add(marker)
        yield current
        current = getattr(current, "__cause__", None) or getattr(current, "__context__", None)


def _extract_status_code(exc: BaseException) -> int | None:
    raw_status = getattr(exc, "status_code", None)
    if isinstance(raw_status, int):
        return raw_status

    raw_status = getattr(exc, "status", None)
    if isinstance(raw_status, int):
        return raw_status

    response = getattr(exc, "response", None)
    if response is None:
        return None

    if isinstance(response, dict):
        response_status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if isinstance(response_status, int):
            return response_status
        return None

    response_status = getattr(response, "status_code", None)
    if isinstance(response_status, int):
        return response_status

    response_status = getattr(response, "status", None)
    if isinstance(response_status, int):
        return response_status

    return None


def _extract_error_detail(exc: BaseException) -> str | None:
    response = getattr(exc, "response", None)
    if response is not None:
        detail = _extract_detail_from_response(response)
        if detail:
            return detail

    for arg in getattr(exc, "args", ()):
        if isinstance(arg, str) and arg:
            return arg

    message = str(exc)
    return message or None


def _extract_detail_from_response(response: t.Any) -> str | None:
    if isinstance(response, dict):
        error_section = response.get("Error", {})
        if isinstance(error_section, dict):
            message = error_section.get("Message")
            if isinstance(message, str) and message:
                return message
        return None

    if hasattr(response, "json"):
        try:
            payload = response.json()
        except Exception:
            payload = None
        if isinstance(payload, dict):
            detail = payload.get("detail")
            if isinstance(detail, str) and detail:
                return detail

    text = getattr(response, "text", None)
    if isinstance(text, str) and text:
        try:
            payload = json.loads(text)
        except (TypeError, ValueError):
            return text
        if isinstance(payload, dict):
            detail = payload.get("detail")
            if isinstance(detail, str) and detail:
                return detail
        return text

    return None
