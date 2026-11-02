"""Content-addressed local trees with normalized metadata and bounded capture."""

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path, PurePosixPath

from labqoat.json_document import JsonValue
from labqoat.schemas.identity import Identity


@dataclass(frozen=True)
class InputTree:
    """Keep captured bytes separate from host paths and filesystem timestamps."""

    entries: tuple[tuple[str, bytes, int], ...]

    @classmethod
    def capture(cls, files: dict[str, Path], *, root: Path | None = None) -> "InputTree":
        """Read regular files with private-path checks confined to an explicit capture root when supplied."""
        if not 1 <= len(files) <= 4000:
            raise ValueError("Image inputs must contain 1..4000 files")
        for name, path in files.items():
            cls._validate(name, path, root)
        if sum(path.stat().st_size for path in files.values()) > 256 * 1024 * 1024:
            raise ValueError("Image inputs must contain at most 256 MiB")
        entries = tuple(cls._entry(name, files[name]) for name in sorted(files))
        if not entries or len(entries) > 4000 or sum(len(data) for _, data, _ in entries) > 256 * 1024 * 1024:
            raise ValueError("Image inputs must contain 1..4000 files and at most 256 MiB")
        return cls(entries)

    @staticmethod
    def _validate(name: str, path: Path, root: Path | None) -> None:
        """Reject symlink parents, special files and private inputs before opening a file."""
        from labqoat.compute.context_files import ContextFiles

        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or relative.as_posix() != name or not relative.parts:
            raise ValueError(f"Invalid image input name: {name}")
        if any(item.is_symlink() for item in (path, *path.parents)) or not path.is_file():
            raise ValueError(f"Image inputs must be regular files without links: {path}")
        if any(ContextFiles.private(part) for part in InputTree._scoped_path(path, root).parts):
            raise ValueError(f"Image inputs cannot include private configuration: {path}")

    @staticmethod
    def _scoped_path(path: Path, root: Path | None) -> Path:
        """Confine package inputs to their root without resolving links or allowing parent traversal."""
        if root is None:
            return path
        relative = path.absolute().relative_to(root.absolute())
        if ".." in relative.parts:
            raise ValueError(f"Image inputs must remain inside capture root: {path}")
        return relative

    @staticmethod
    def _entry(name: str, path: Path) -> tuple[str, bytes, int]:
        """Read validated file bytes with an upper bound even if the file grows during capture."""
        with path.open("rb") as source:
            data = source.read(256 * 1024 * 1024 + 1)
        return name, data, 0o755 if path.stat().st_mode & 0o111 else 0o644

    def manifest(self) -> dict[str, JsonValue]:
        """Describe every available byte and executable mode in portable canonical form."""
        return {name: {"sha256": digest, "mode": mode} for name, digest, mode in self._descriptors}

    @cached_property
    def _descriptors(self) -> tuple[tuple[str, str, int], ...]:
        """Hash captured immutable bytes once while keeping returned manifests independently mutable."""
        return tuple((name, Identity.hash(data), mode) for name, data, mode in self.entries)

    @cached_property
    def prefix(self) -> str:
        """Use content identity as the stable build-context path."""
        return "inputs/" + Identity.digest(self.manifest()).removeprefix("sha256:")

    def write(self, directory: Path) -> dict[str, JsonValue]:
        """Stage immutable bytes and return their full context-relative manifest."""
        prefix = self.prefix
        for name, data, mode in self.entries:
            path = directory / prefix / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            path.chmod(mode)
        return {f"{prefix}/{name}": descriptor for name, descriptor in self.manifest().items()}
