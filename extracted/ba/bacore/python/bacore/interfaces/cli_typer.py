"""CLI Typer interface."""

from bacore.domain import files, settings
from bacore.interactors.file_handler import file_as_dict
from pathlib import Path
from typing import Optional


class ProjectInfo:
    """ProjectInfo information."""

    def __init__(self, pyproject_file: Path):
        """Initialize."""
        self._pyproject_file_toml_object = files.TOML(path=pyproject_file)
        self._project_info_dict = file_as_dict(
            file=self._pyproject_file_toml_object
        )
        self._project_info = settings.Project(
            name=self._project_info_dict["project"]["name"],
            version=self._project_info_dict["project"]["version"],
            description=self._project_info_dict["project"]["description"],
        )

    @property
    def name(self) -> str:
        """ProjectInfo name."""
        return self._project_info.name

    @property
    def version(self) -> Optional[str]:
        """ProjectInfo version."""
        return self._project_info.version

    @property
    def description(self) -> Optional[str]:
        """ProjectInfo description."""
        return self._project_info.description
