"""Append-only, content-addressed artifact registry for ``~/.agdt/registry.json``.

Supports FR-002 multi-repo coexistence (partial): the registry provides an
append-only *reference index* so that recording one repository's setup artifacts
never removes the reference another repository holds on a shared artifact.

The registry tracks which repository *contexts* (keyed by a stable
``repository_context_id`` derived from the canonical absolute repository root
path) reference which shared artifacts (certificate bundles, ``.npmrc``
fragments).  Artifacts are content-addressed in the *index*: identical content is
recorded once, keyed by its SHA-256 hash, and referenced by every context that
installed it.  Because setup only ever *adds* a context reference (never removes
another context's reference), the registry itself cannot degrade another
repository's entry.

Scope note: this module records references only — it does **not** yet store each
artifact's bytes at a hash-derived path.  The shared artifact files still live at
singleton paths (e.g. ``~/.agdt/certs/unified-ca-bundle.pem``), so a later setup
that rebuilds a singleton with *different* content overwrites the previous bytes
in place even though both hashes remain recorded.  Hash-derived artifact storage
and repo-scoped shell-profile block markers remain follow-up work.

The on-disk JSON is written deterministically (sorted keys, sorted reference
lists) so the file is stable and diff-friendly across reruns.  Mutating
operations (:func:`register_context`, :func:`deregister_context`) acquire an
exclusive lock on a sidecar ``registry.json.lock`` file around the
read-modify-write cycle so concurrent setups in different repositories do not
race.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agentic_devtools.cli.setup.script_generators.atomic_write import atomic_write
from agentic_devtools.file_locking import locked_file

#: Schema version written to ``registry.json``.  Bumped only on breaking schema
#: changes so future readers can migrate older layouts.
SCHEMA_VERSION = 1

#: Number of hex characters retained from the SHA-256 of the canonical repo path
#: when deriving a ``repository_context_id``.
_CONTEXT_ID_LENGTH = 16

#: Chunk size (bytes) used when hashing artifact file contents.
_HASH_CHUNK_SIZE = 65536


class RegistryError(RuntimeError):
    """Raised when the registry file cannot be read or parsed."""


def _require_str(value: Any, field_name: str) -> str:
    """Return *value* when it is a ``str``, else raise :class:`RegistryError`.

    Used to validate scalar registry fields loaded from the user-global JSON
    file instead of silently coercing them (e.g. ``str(None) == "None"`` or
    ``str(1) == "1"``), which would rewrite corrupt external data as apparently
    valid registry state.
    """
    if not isinstance(value, str):
        raise RegistryError(f"Registry field '{field_name}' must be a string, got {type(value).__name__}")
    return value


def _require_nonempty_str(value: Any, field_name: str) -> str:
    """Return *value* when it is a non-empty ``str``, else raise :class:`RegistryError`.

    Extends :func:`_require_str` to also reject empty strings for required
    registry fields (``path``, ``type``, ``content_hash``, ``last_setup_utc``).
    An empty string in these positions indicates a corrupt or truncated registry
    entry that should not be silently persisted.
    """
    s = _require_str(value, field_name)
    if not s:
        raise RegistryError(f"Registry field '{field_name}' must not be empty")
    return s


@dataclass
class ArtifactEntry:
    """A single shared artifact stored under ``~/.agdt/``.

    Attributes:
        type: Artifact kind (e.g. ``"cert_bundle"`` or ``"npmrc"``).
        path: Absolute path to the artifact on disk.
        content_hash: SHA-256 hex digest of the artifact's content; the
            registry key under which this entry is stored.
        referenced_by: Sorted list of ``repository_context_id`` values whose
            setup installed (and therefore depends on) this artifact.
    """

    type: str
    path: str
    content_hash: str
    referenced_by: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict with a deterministic reference list."""
        return {
            "type": self.type,
            "path": self.path,
            "content_hash": self.content_hash,
            "referenced_by": sorted(self.referenced_by),
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ArtifactEntry:
        """Build an :class:`ArtifactEntry` from parsed JSON, validating types."""
        if not isinstance(raw, dict):
            raise RegistryError(f"Expected artifact entry to be a dict, got {type(raw).__name__}")
        referenced_by = raw.get("referenced_by", [])
        if not isinstance(referenced_by, list):
            raise RegistryError("Artifact 'referenced_by' must be a list")
        return cls(
            type=_require_nonempty_str(raw.get("type"), "type"),
            path=_require_nonempty_str(raw.get("path"), "path"),
            content_hash=_require_nonempty_str(raw.get("content_hash"), "content_hash"),
            referenced_by=[_require_str(item, "referenced_by item") for item in referenced_by],
        )


@dataclass
class ContextEntry:
    """A registered repository context.

    Attributes:
        path: Canonical absolute path of the repository root.
        last_setup_utc: ISO-8601 UTC timestamp of the most recent setup run.
        artifacts: Sorted list of artifact ``content_hash`` values this context
            references.
    """

    path: str
    last_setup_utc: str
    artifacts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict with a deterministic artifact list."""
        return {
            "path": self.path,
            "last_setup_utc": self.last_setup_utc,
            "artifacts": sorted(self.artifacts),
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ContextEntry:
        """Build a :class:`ContextEntry` from parsed JSON, validating types."""
        if not isinstance(raw, dict):
            raise RegistryError(f"Expected context entry to be a dict, got {type(raw).__name__}")
        artifacts = raw.get("artifacts", [])
        if not isinstance(artifacts, list):
            raise RegistryError("Context 'artifacts' must be a list")
        return cls(
            path=_require_nonempty_str(raw.get("path"), "path"),
            last_setup_utc=_require_nonempty_str(raw.get("last_setup_utc"), "last_setup_utc"),
            artifacts=[_require_str(item, "artifacts item") for item in artifacts],
        )


@dataclass
class RegistryData:
    """The full contents of ``registry.json``.

    Attributes:
        schema_version: On-disk schema version.
        contexts: Mapping of ``repository_context_id`` to :class:`ContextEntry`.
        artifacts: Mapping of ``content_hash`` to :class:`ArtifactEntry`.
    """

    schema_version: int = SCHEMA_VERSION
    contexts: dict[str, ContextEntry] = field(default_factory=dict)
    artifacts: dict[str, ArtifactEntry] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a fully deterministic JSON-serializable dict (sorted keys)."""
        return {
            "schema_version": self.schema_version,
            "contexts": {key: self.contexts[key].to_dict() for key in sorted(self.contexts)},
            "artifacts": {key: self.artifacts[key].to_dict() for key in sorted(self.artifacts)},
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> RegistryData:
        """Build :class:`RegistryData` from parsed JSON, validating types."""
        if not isinstance(raw, dict):
            raise RegistryError(f"Expected registry root to be a dict, got {type(raw).__name__}")
        contexts_raw = raw.get("contexts", {})
        artifacts_raw = raw.get("artifacts", {})
        version_raw = raw.get("schema_version", SCHEMA_VERSION)
        if not isinstance(contexts_raw, dict):
            raise RegistryError("Registry 'contexts' must be a dict")
        if not isinstance(artifacts_raw, dict):
            raise RegistryError("Registry 'artifacts' must be a dict")
        if isinstance(version_raw, bool) or not isinstance(version_raw, int):
            raise RegistryError("Registry 'schema_version' must be an integer")
        if version_raw < 1 or version_raw > SCHEMA_VERSION:
            raise RegistryError(
                f"Unsupported registry schema_version {version_raw}; "
                f"this installation supports versions 1 through {SCHEMA_VERSION}"
            )
        return cls(
            schema_version=version_raw,
            contexts={str(key): ContextEntry.from_dict(value) for key, value in contexts_raw.items()},
            artifacts={str(key): ArtifactEntry.from_dict(value) for key, value in artifacts_raw.items()},
        )


def get_registry_path() -> Path:
    """Return the canonical path to the user-global ``~/.agdt/registry.json``."""
    return Path.home() / ".agdt" / "registry.json"


def derive_context_id(repo_root: Path) -> str:
    """Derive a stable ``repository_context_id`` from a repository root path.

    The identifier is the first :data:`_CONTEXT_ID_LENGTH` hex characters of the
    SHA-256 of the *canonical* absolute path (symlinks resolved, path
    normalized).  Reruns in the same clone resolve to the same id; different
    clones of the same repo at different paths produce distinct ids (path-based,
    not remote-based), per FR-002.
    """
    canonical = str(Path(repo_root).resolve())
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return digest[:_CONTEXT_ID_LENGTH]


def compute_content_hash(path: Path) -> str:
    """Return the SHA-256 hex digest of the file at *path* (read in chunks)."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(_HASH_CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def load_registry(registry_path: Path | None = None) -> RegistryData:
    """Load and parse the registry, returning an empty one when absent.

    Args:
        registry_path: Explicit registry path; defaults to
            :func:`get_registry_path`.

    Returns:
        The parsed :class:`RegistryData`, or an empty instance when the file
        does not exist.

    Raises:
        RegistryError: When the file exists but cannot be read or parsed.
    """
    path = registry_path if registry_path is not None else get_registry_path()
    if not path.exists():
        return RegistryData()
    try:
        raw_text = path.read_text(encoding="utf-8")
        parsed = json.loads(raw_text)
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        raise RegistryError(f"Could not read registry at {path}: {exc}") from exc
    return RegistryData.from_dict(parsed)


def save_registry(data: RegistryData, registry_path: Path | None = None) -> None:
    """Atomically write *data* to the registry with deterministic formatting."""
    path = registry_path if registry_path is not None else get_registry_path()
    serialized = json.dumps(data.to_dict(), indent=2, sort_keys=True) + "\n"
    atomic_write(path, serialized)


def register_artifact(
    data: RegistryData,
    context_id: str,
    artifact_type: str,
    path: str,
    content_hash: str,
) -> ArtifactEntry:
    """Register (or reference) an artifact by content hash, appending the context.

    If an artifact with *content_hash* already exists, *context_id* is appended
    to its ``referenced_by`` list (deduplicated) and the existing entry is
    returned unchanged otherwise — content-addressed deduplication.  If it does
    not exist, a new entry is created referenced solely by *context_id*.

    This function never removes an existing reference, which is what preserves
    the multi-repo non-clobbering guarantee.
    """
    existing = data.artifacts.get(content_hash)
    if existing is not None:
        if context_id not in existing.referenced_by:
            existing.referenced_by.append(context_id)
        return existing
    entry = ArtifactEntry(
        type=artifact_type,
        path=path,
        content_hash=content_hash,
        referenced_by=[context_id],
    )
    data.artifacts[content_hash] = entry
    return entry


def register_context(
    repo_root: Path,
    artifact_paths: list[tuple[str, Path]],
    registry_path: Path | None = None,
) -> str:
    """Append-only upsert of a repository context and its artifact references.

    Acquires an exclusive lock around the load-modify-save cycle so concurrent
    setups do not race.  Hashes each artifact file *inside* the lock so the
    recorded content hash matches the file's bytes at the moment of
    registration.  Upserts the context for *repo_root* (updating its
    ``path``/``last_setup_utc``) and registers each artifact via
    :func:`register_artifact`, adding the artifact's content hash to the
    context's reference list.  Other contexts' references are never touched.

    Args:
        repo_root: The repository root whose context is being registered.
        artifact_paths: ``(artifact_type, artifact_file_path)`` pairs for
            artifacts installed by this setup run.  Hashing is deferred to
            inside the lock so the recorded hash matches what is actually on
            disk at registration time.
        registry_path: Explicit registry path; defaults to
            :func:`get_registry_path`.

    Returns:
        The ``repository_context_id`` that was upserted.
    """
    path = registry_path if registry_path is not None else get_registry_path()
    context_id = derive_context_id(repo_root)
    canonical = str(Path(repo_root).resolve())
    lock_path = path.with_name(path.name + ".lock")
    with locked_file(lock_path, "a+"):
        data = load_registry(path)
        context = data.contexts.get(context_id)
        if context is None:
            context = ContextEntry(path=canonical, last_setup_utc=_utc_now(), artifacts=[])
            data.contexts[context_id] = context
        context.path = canonical
        context.last_setup_utc = _utc_now()
        for artifact_type, artifact_file in artifact_paths:
            content_hash = compute_content_hash(artifact_file)
            register_artifact(data, context_id, artifact_type, str(artifact_file), content_hash)
            if content_hash not in context.artifacts:
                context.artifacts.append(content_hash)
        save_registry(data, path)
    return context_id


def deregister_context(context_id: str, registry_path: Path | None = None) -> bool:
    """Remove a context and drop its references from every artifact.

    Artifact *entries* are retained even when their ``referenced_by`` becomes
    empty (append-only for the artifact files themselves); only this context's
    references are removed, leaving other contexts' references intact.

    Args:
        context_id: The context id to remove.
        registry_path: Explicit registry path; defaults to
            :func:`get_registry_path`.

    Returns:
        ``True`` if the context existed and was removed, ``False`` otherwise.
    """
    path = registry_path if registry_path is not None else get_registry_path()
    lock_path = path.with_name(path.name + ".lock")
    with locked_file(lock_path, "a+"):
        data = load_registry(path)
        if context_id not in data.contexts:
            return False
        data.contexts.pop(context_id)
        for entry in data.artifacts.values():
            if context_id in entry.referenced_by:
                entry.referenced_by.remove(context_id)
        save_registry(data, path)
    return True


def get_context_artifacts(data: RegistryData, context_id: str) -> list[ArtifactEntry]:
    """Return the artifacts referenced by *context_id*, sorted by content hash."""
    context = data.contexts.get(context_id)
    if context is None:
        return []
    resolved = [data.artifacts[content_hash] for content_hash in context.artifacts if content_hash in data.artifacts]
    return sorted(resolved, key=lambda entry: entry.content_hash)


def _utc_now() -> str:
    """Return the current UTC time as an ISO-8601 ``...Z`` string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
