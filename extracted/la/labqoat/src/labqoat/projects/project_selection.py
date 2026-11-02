"""The project every request acts on, and what selected it."""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from labqoat.projects.project_declaration import ProjectDeclaration
from labqoat.projects.project_names import ProjectNames


@dataclass(frozen=True)
class ProjectSelection:
    """Resolve an explicit name, then LABQOAT_PROJECT, then the nearest pinned pyproject.toml; nothing else selects one."""

    name: str | None
    source: str
    path: Path | None = None

    variable: ClassVar[str] = "LABQOAT_PROJECT"
    missing: ClassVar[str] = (
        "No project selected. Pass --project NAME, export LABQOAT_PROJECT=NAME, or pin one with "
        "[tool.labqoat] project = NAME in pyproject.toml (lab init does this)."
    )

    @classmethod
    def resolve(
        cls, explicit: str | None = None, environ: Mapping[str, str] | None = None, start: Path | None = None
    ) -> "ProjectSelection":
        """Take the first source that names a project; an invalid name fails instead of falling through."""
        if explicit is not None:
            return cls(ProjectNames.project(explicit, "--project"), "flag")
        exported = (os.environ if environ is None else environ).get(cls.variable)
        if exported:
            return cls(ProjectNames.project(exported, cls.variable), "environment")
        declaration = ProjectDeclaration.nearest(start)
        if declaration is not None:
            return cls(declaration.name, "pyproject", declaration.path)
        return cls(None, "none")

    def required(self) -> str:
        """The selected name, or a ValueError saying how to select one."""
        if self.name is None:
            raise ValueError(self.missing)
        return self.name

    def origin(self) -> str | None:
        """Name what selected the project the way a person would point at it."""
        if self.path is not None:
            return str(self.path)
        return {"flag": "--project", "environment": self.variable}.get(self.source)
