import itertools
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Literal, Mapping, Optional, cast

import yaml

from chalk._version import __version__
from chalk.config._validator import Validator


@dataclass
class EnvironmentSettings:
    runtime: Optional[Literal["python310", "python311", "python312"]]
    requirements: Optional[str]
    dockerfile: Optional[str]
    platform_version: Optional[str]

    @staticmethod
    def from_py(value: Any, environment_name: str) -> "EnvironmentSettings":
        prefix = f"environments.{environment_name}"
        value = Validator.dict_with_str_keys(value, name=prefix)
        return EnvironmentSettings(
            runtime=cast(
                Optional[Literal["python310", "python311", "python312"]],
                Validator.optional_string(
                    value.get("runtime"),
                    f"{prefix}.runtime",
                    one_of=("python310", "python311", "python312"),
                ),
            ),
            requirements=Validator.optional_string(value.get("requirements"), f"{prefix}.requirements"),
            dockerfile=Validator.optional_string(value.get("dockerfile"), f"{prefix}.dockerfile"),
            platform_version=Validator.optional_string(value.get("platform_version"), f"{prefix}.platform_version"),
        )

    def as_dict(self):
        return {
            "runtime": self.runtime,
            "requirements": self.requirements,
            "dockerfile": self.dockerfile,
            "platform_version": self.platform_version,
        }


@dataclass
class MetadataSettings:
    name: str
    missing: str

    @staticmethod
    def from_py(value: Any, kind: str) -> "MetadataSettings":
        value = Validator.dict_with_str_keys(value, name=f"validation.{kind}.metadata")
        return MetadataSettings(
            name=Validator.string(value.get("name"), f"validation.{kind}.metadata.name"),
            missing=Validator.string(value.get("missing"), f"validation.{kind}.metadata.missing"),
        )

    def as_dict(self):
        return {
            "name": self.name,
            "missing": self.missing,
        }


@dataclass
class FeatureSettings:
    metadata: Optional[List[MetadataSettings]]

    @staticmethod
    def from_py(value: Any) -> "FeatureSettings":
        value = Validator.dict_with_str_keys(value, name="validation.feature")
        metadata = value.get("metadata", None)
        if metadata is None:
            return FeatureSettings(metadata=None)
        if not isinstance(metadata, list):
            raise ValueError(f"Expected list, got '{metadata}' for validation.feature.metadata")
        return FeatureSettings(metadata=[MetadataSettings.from_py(m, "feature") for m in metadata])

    def as_dict(self):
        return {
            "metadata": [m.as_dict() for m in self.metadata] if self.metadata is not None else None,
        }


@dataclass
class ResolverSettings:
    metadata: Optional[List[MetadataSettings]]

    @staticmethod
    def from_py(value: Any) -> "ResolverSettings":
        value = Validator.dict_with_str_keys(value, name="validation.resolver")
        metadata = value.get("metadata", None)
        if metadata is None:
            return ResolverSettings(metadata=None)
        if not isinstance(metadata, list):
            raise ValueError(f"Expected list, got '{metadata}' for validation.resolver.metadata")
        return ResolverSettings(metadata=[MetadataSettings.from_py(m, "resolver") for m in metadata])

    def as_dict(self):
        return {
            "metadata": [m.as_dict() for m in self.metadata] if self.metadata is not None else None,
        }


@dataclass
class ValidationSettings:
    feature: Optional[FeatureSettings]
    resolver: Optional[ResolverSettings]

    @staticmethod
    def from_py(value: Any) -> "ValidationSettings":
        d = Validator.dict_with_str_keys(value, name="validation")
        raw_feature = d.get("feature", None)
        raw_resolver = d.get("resolver", None)
        return ValidationSettings(
            feature=FeatureSettings.from_py(raw_feature) if raw_feature is not None else None,
            resolver=ResolverSettings.from_py(raw_resolver) if raw_resolver is not None else None,
        )

    def as_dict(self):
        return {
            "feature": self.feature.as_dict() if self.feature is not None else None,
            "resolver": self.resolver.as_dict() if self.resolver is not None else None,
        }


@dataclass
class ProjectSettings:
    project: str
    environments: Optional[Mapping[str, EnvironmentSettings]]
    validation: Optional[ValidationSettings]
    local_path: str
    chalkpy: str

    @staticmethod
    def from_py(value: Any, local_path: str):
        value = Validator.dict_with_str_keys(value, name="root")
        raw_envs = Validator.dict_with_str_keys_or_none(value.get("environments", None), "environments")
        raw_validation = value.get("validation", None)
        return ProjectSettings(
            project=Validator.string(value.get("project"), "project"),
            environments=(
                None
                if raw_envs is None
                else {
                    environment_name: EnvironmentSettings.from_py(
                        value=v,
                        environment_name=environment_name,
                    )
                    for environment_name, v in raw_envs.items()
                }
            ),
            validation=ValidationSettings.from_py(raw_validation) if raw_validation is not None else None,
            local_path=local_path,
            chalkpy=__version__,
        )

    def as_dict(self):
        return {
            "project": self.project,
            "environments": {k: v.as_dict() for k, v in self.environments.items()} if self.environments else None,
            "validation": self.validation.as_dict() if self.validation else None,
            "local_path": self.local_path,
            "chalkpy": self.chalkpy,
        }


def _load_project_config_at_path(filename: Path) -> Optional[ProjectSettings]:
    has_default_requirements = os.path.exists(filename.parent / "requirements.txt")
    try:
        with open(filename, "r") as f:
            parsed = yaml.safe_load(f)
            settings = ProjectSettings.from_py(
                parsed,
                local_path=str(filename.absolute().resolve()),
            )
            if has_default_requirements and settings.environments is not None:
                for cfg in settings.environments.values():
                    if cfg.requirements is None:
                        cfg.requirements = "requirements.txt"
            return settings
    except OSError:
        return None
    except ValueError as e:
        raise ValueError(f"Failed to load project config from {filename} (chalkpy=={__version__}): {e}") from e


def load_project_config() -> Optional[ProjectSettings]:
    base = Path(os.getcwd())

    for d in itertools.chain([base], base.parents):
        project = _load_project_config_at_path(d / "chalk.yaml") or _load_project_config_at_path(d / "chalk.yml")

        if project is not None:
            return project

    return None
