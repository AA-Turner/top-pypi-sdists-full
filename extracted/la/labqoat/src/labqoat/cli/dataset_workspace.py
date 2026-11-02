"""Project discovery and verified local dataset views over captured JSON selections."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING

from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.projects.pinned_schema import PinnedSchema
    from labqoat.references import DatasetRef
    from labqoat.storage.shared_asset_cache import SharedAssetCache


class DatasetWorkspace:
    """Own managed views and shared content verification independently of publication staging."""

    repository_pattern = r"[a-z][a-z0-9-]*(?:/[a-z][a-z0-9-]*)+"

    def __init__(self, root: Path) -> None:
        """Store the discovered project root."""
        self._root = root.resolve()

    @property
    def root(self) -> Path:
        """Return the project root."""
        return self._root

    @classmethod
    def discover(cls, start: Path | None = None) -> DatasetWorkspace:
        """Find the nearest project identified by its tracked lock file."""
        selected = (start or Path.cwd()).resolve()
        selected = selected.parent if selected.is_file() else selected
        for candidate in (selected, *selected.parents):
            if (candidate / "labqoat.lock").is_file() or cls._declares_project(candidate):
                return cls(candidate)
        raise ValueError("dataset commands must run inside a Labqoat project")

    @staticmethod
    def _declares_project(candidate: Path) -> bool:
        """Return whether one pyproject pins a valid project name; unreadable settings select nothing."""
        from labqoat.projects.project_declaration import ProjectDeclaration

        try:
            return ProjectDeclaration.read(candidate) is not None
        except ValueError:
            return False

    @classmethod
    def normalize_repository(cls, repository: str) -> str:
        """Validate and return a lowercase namespace/name repository."""
        import re

        if re.fullmatch(cls.repository_pattern, repository) is None:
            raise ValueError("dataset name must use lowercase namespace/name form")
        return repository

    def read_pins(self) -> dict[str, PinnedSchema]:
        """Read only captured schema-verified selections from the versioned JSON lock."""
        from labqoat.projects.project_directory import ProjectDirectory
        from labqoat.projects.project_schemas import ProjectSchemas

        return {pin.alias: pin for pin in ProjectSchemas.read(ProjectDirectory(self.root)).pins}

    def reference(self, selector: str) -> DatasetRef[object]:
        """Carry the captured schema requirement when selecting a pinned project alias."""
        from labqoat.references import DatasetRef

        pin = self.read_pins().get(selector)
        if pin is not None:
            return DatasetRef(pin.dataset, pin.revision, pin.schema.digest)
        return DatasetRef.parse(selector)

    def resolve_selector(self, selector: str) -> str:
        """Resolve a friendly pin or validate a direct remote selector."""
        pin = self.read_pins().get(selector)
        if pin is not None:
            return pin.revision
        if "@" not in selector:
            raise ValueError("dataset view requires a pin or repository@selector reference")
        repository, revision = selector.rsplit("@", 1)
        self.normalize_repository(repository)
        if not revision:
            raise ValueError("dataset revision selector cannot be empty")
        return selector

    def mount_path(self, selector: str) -> Path:
        """Return the deterministic path for one local dataset view."""
        pin = self.read_pins().get(selector)
        if pin is not None:
            relative = self._logical_path(selector)
        else:
            reference = self.resolve_selector(selector)
            repository, revision = reference.rsplit("@", 1)
            relative = self._logical_path(f"{repository}/{revision}")
        return self._root / ".labqoat" / "mounts" / relative

    def materialize(
        self,
        selector: str,
        files: Sequence[Mapping[str, JsonValue]],
        fetch: Callable[[str, Path], int],
        mode: str,
        cache: SharedAssetCache | None = None,
    ) -> JsonDocument:
        """Build a cache-backed mount or standalone materialized view."""
        if mode not in {"mount", "materialize"}:
            raise ValueError("dataset view mode must be mount or materialize")
        reference = self.resolve_selector(selector)
        destination = self.mount_path(selector)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
        downloaded = 0
        try:
            for entry in files:
                downloaded += self._materialize_entry(temporary, entry, fetch, mode, cache)
            self._prepare_mount(destination)
            temporary.replace(destination)
        except BaseException:
            shutil.rmtree(temporary, ignore_errors=True)
            raise
        self._write_mount_state(selector, reference, destination, mode, len(files))
        return JsonDocument(
            {
                "dataset": reference,
                "downloaded": downloaded,
                "files": len(files),
                "mode": mode,
                "path": str(destination),
                "reused": len(files) - downloaded,
            }
        )

    def _materialize_entry(
        self,
        temporary: Path,
        entry: Mapping[str, JsonValue],
        fetch: Callable[[str, Path], int],
        mode: str,
        shared: SharedAssetCache | None,
    ) -> int:
        """Verify and install one manifest file."""
        logical = entry.get("path")
        sha = entry.get("sha256")
        if not isinstance(logical, str) or not isinstance(sha, str):
            raise ValueError("dataset manifest contains a malformed file")
        target = temporary / self._logical_path(logical)
        from labqoat.cli.mounted_asset_file import MountedAssetFile

        cache, downloaded = (
            self._cached_asset(sha, fetch)
            if shared is None
            else MountedAssetFile.acquire(self._root, entry, shared, fetch)
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        if mode == "mount":
            target.symlink_to(cache)
        else:
            shutil.copyfile(cache, target)
            target.chmod(0o444)
        return int(downloaded)

    def _cached_asset(self, sha: str, fetch: Callable[[str, Path], int]) -> tuple[Path, bool]:
        """Return a checksum-verified project-local cached blob."""
        if len(sha) != 64 or any(character not in "0123456789abcdef" for character in sha):
            raise ValueError("dataset manifest contains an invalid sha256")
        path = self._root / ".labqoat" / "cache" / "sha256" / sha
        if path.is_file() and self._sha256_file(path) == sha:
            return path, False
        self._fetch_verified(path, sha, fetch)
        path.chmod(0o444)
        return path, True

    def _prepare_mount(self, destination: Path) -> None:
        """Remove a prior managed view while refusing unrelated paths."""
        record = self._mount_record(destination)
        if destination.exists() or destination.is_symlink():
            if record is None:
                raise ValueError(f"dataset mount path is not managed: {destination}")
            if destination.is_dir() and not destination.is_symlink():
                shutil.rmtree(destination)
            else:
                destination.unlink()
        if record is not None:
            self._mount_state_path(destination).unlink(missing_ok=True)

    def mounts(self) -> JsonDocument:
        """List every managed local dataset view."""
        root = self._root / ".labqoat" / "state" / "mounts"
        if not root.is_dir():
            return JsonDocument({"items": []})
        items: list[JsonValue] = [
            JsonDocument.expect_dict(json.loads(path.read_text(encoding="utf-8")))
            for path in sorted(root.glob("*.json"))
        ]
        return JsonDocument({"items": items})

    def unmount(self, selector: str) -> JsonDocument:
        """Remove one managed view while retaining cached blobs."""
        destination = self.mount_path(selector)
        if self._mount_record(destination) is None:
            raise ValueError("dataset mount is not managed by Labqoat")
        if destination.is_dir() and not destination.is_symlink():
            shutil.rmtree(destination)
        elif destination.exists() or destination.is_symlink():
            destination.unlink()
        self._mount_state_path(destination).unlink()
        return JsonDocument({"path": str(destination), "status": "unmounted"})

    @staticmethod
    def _fetch_verified(target: Path, sha: str, fetch: Callable[[str, Path], int]) -> None:
        """Stream into a private sibling and publish only verified bytes."""
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
        os.close(descriptor)
        temporary = Path(name)
        try:
            fetch(f"sha256:{sha}", temporary)
            if DatasetWorkspace._sha256_file(temporary) != sha:
                raise ValueError("downloaded dataset asset checksum does not match")
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)

    def _write_mount_state(self, selector: str, reference: str, destination: Path, mode: str, file_count: int) -> None:
        """Record ownership of one local view."""
        from labqoat.projects.atomic_project_file import AtomicProjectFile

        document = {
            "dataset": reference,
            "files": file_count,
            "mode": mode,
            "path": str(destination),
            "selector": selector,
        }
        content = json.dumps(document, separators=(",", ":"), sort_keys=True).encode()
        AtomicProjectFile.write(self._mount_state_path(destination), content)

    def _mount_record(self, destination: Path) -> JsonDocument | None:
        """Read one mount ownership record when present."""
        path = self._mount_state_path(destination)
        if not path.is_file():
            return None
        return JsonDocument.expect_dict(json.loads(path.read_text(encoding="utf-8")))

    def _mount_state_path(self, destination: Path) -> Path:
        """Return the stable state path corresponding to a mount path."""
        digest = hashlib.sha256(str(destination).encode()).hexdigest()
        return self._root / ".labqoat" / "state" / "mounts" / f"{digest}.json"

    @staticmethod
    def _logical_path(value: str) -> PurePosixPath:
        """Validate one portable dataset-relative path."""
        path = PurePosixPath(value)
        raw_parts = value.split("/")
        if not value or path.is_absolute() or any(part in {"", ".", ".."} for part in raw_parts):
            raise ValueError(f"dataset path must be safe and relative: {value}")
        return path

    @staticmethod
    def _sha256_file(path: Path) -> str:
        """Hash one local file without whole-file buffering."""
        with path.open("rb") as stream:
            return hashlib.file_digest(stream, "sha256").hexdigest()
