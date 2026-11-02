"""The project a directory pins in the ``[tool.labqoat]`` table of its ``pyproject.toml``."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from labqoat.projects.project_names import ProjectNames


@dataclass(frozen=True)
class ProjectDeclaration:
    """Read ``project = "<name>"`` statically, without importing authored Python or consulting remote state."""

    path: Path
    name: str

    @classmethod
    def read(cls, root: Path) -> "ProjectDeclaration | None":
        """Return the project one directory pins; None when it has no file, table or key."""
        path = root / "pyproject.toml"
        if not path.is_file():
            return None
        try:
            document = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise ValueError(f"Cannot read {path}: {error}") from error
        tool = document.get("tool", {})
        table = tool.get("labqoat", {}) if isinstance(tool, dict) else {}
        if not isinstance(table, dict) or "project" not in table:
            return None
        return cls(path, ProjectNames.project(table["project"], f"[tool.labqoat] project in {path}"))

    @classmethod
    def nearest(cls, start: Path | None = None) -> "ProjectDeclaration | None":
        """Walk up from a directory, or from the directory of a file, to the first pinned project."""
        selected = (start or Path.cwd()).resolve()
        selected = selected.parent if selected.is_file() else selected
        for candidate in (selected, *selected.parents):
            declaration = cls.read(candidate)
            if declaration is not None:
                return declaration
        return None
