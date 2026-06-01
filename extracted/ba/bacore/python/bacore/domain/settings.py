"""Settings module for settings of BACore and its components."""

import platform
from bacore.domain.files import TOMLFile
from pathlib import Path
from pydantic import BaseModel, Field, computed_field, field_validator, SecretStr
from pydantic_settings import BaseSettings
from typing import Optional, cast


class Project(BaseModel):
    """Project information."""

    name: str
    version: Optional[str] = None
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_must_not_contain_spaces(cls, v: str) -> str:
        """Validate that the name does not contain spaces."""
        if " " in v:
            raise ValueError("No spaces allowed in project name.")
        return v


class Secret(BaseModel):
    """Credential details."""

    secret: SecretStr

    @field_validator("secret")
    @classmethod
    def coerce_to_secretstr(cls, v: str) -> SecretStr:
        """If a string is given as input, then coerce into secret string (`SecretStr`)."""
        if isinstance(v, str):
            cast(SecretStr, v)
        return SecretStr(v)


class System(BaseModel):
    """System information."""

    os: str

    @field_validator("os")
    @classmethod
    def os_must_be_supported(cls, v: str) -> str:
        """Validate that the operating system is supported."""
        supported_oses = ["Darwin", "Linux", "Windows"]
        if v not in supported_oses:
            raise ValueError(f"Operating system '{v}' is not supported.")
        return v


class Credentials(BaseSettings):
    """Credential details."""

    username: str
    password: Secret

    @field_validator("username")
    @classmethod
    def username_must_not_contain_spaces(cls, v: str) -> str:
        """Validate that the username does not contain spaces."""
        if " " in v:
            raise ValueError("No spaces allowed in username.")
        return v


class ProjectSettings(BaseSettings):
    """Project settings assumes that the project will use a pyproject.toml file."""

    path: Path = Field(default=Path("."), alias="project_root_dir")

    @field_validator("path")
    @classmethod
    def path_must_be_directory(cls, v: Path) -> Path:
        """Validate that the path is a directory."""
        if v.is_dir() is False:
            raise ValueError(f"Path '{v}' is not a directory.")
        return v

    @computed_field
    @property
    def _pyproject_file(self) -> Path:
        project_file = self.path / "pyproject.toml"
        if project_file.is_file() is False:
            raise FileNotFoundError(f"Unable to find pyproject.toml file, got '{project_file}'")
        return project_file

    @computed_field
    @property
    def _project_info_as_dict(self) -> dict:
        """pyproject.toml file as dictionary."""
        return TOMLFile(path=self._pyproject_file).data_to_dict()

    @computed_field
    @property
    def _project_info(self) -> Project:
        """Project information."""
        info = Project(
            name=self._project_info_as_dict["project"]["name"],
            version=self._project_info_as_dict["project"]["version"],
            description=self._project_info_as_dict["project"]["description"],
        )
        return info

    @property
    def name(self) -> str:
        """Project name."""
        return self._project_info.name

    @property
    def version(self) -> str:
        """Project name."""
        project_version = self._project_info.version
        return project_version if project_version is not None else "No project version set."

    @property
    def description(self) -> str:
        """Project description."""
        project_description = self._project_info.description
        return project_description if project_description is not None else "No project description given."


class SystemSettings(BaseSettings):
    """System settings."""

    @computed_field
    @property
    def _system_info(self) -> System:
        """System information."""
        info = System(os=platform.system())
        return info

    @property
    def os(self) -> str:
        """Operating system."""
        return self._system_info.os
