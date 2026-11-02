"""Explicit project discovery and safe project-relative file ownership."""

from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from labqoat.projects.project_declaration import ProjectDeclaration


@dataclass(frozen=True)
class ProjectDirectory:
    """Locate static project files without importing authored Python or consulting remote state."""

    root: Path

    @classmethod
    def discover(cls, start: Path | None = None) -> "ProjectDirectory":
        """Find the nearest explicitly marked project from a directory or one of its source files."""
        project = cls.find(start)
        if project is None:
            raise ValueError("This command must run inside a Labqoat project")
        return project

    @classmethod
    def find(cls, start: Path | None = None) -> "ProjectDirectory | None":
        """Find an optional local alias scope while still surfacing malformed project declarations."""
        declaration = ProjectDeclaration.nearest(start)
        return None if declaration is None else cls(declaration.path.parent)

    def path(self, relative: str) -> Path:
        """Reject absolute paths, traversal and symlinks crossing the project's ownership boundary."""
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or not path.parts or "\\" in relative:
            raise ValueError("Expected a nonempty project-relative path")
        target = self.root / relative
        if not target.resolve().is_relative_to(self.root.resolve()):
            raise ValueError("Path escapes the Labqoat project")
        return target
