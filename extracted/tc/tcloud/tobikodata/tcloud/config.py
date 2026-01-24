from __future__ import annotations

import os
import typing as t
from dataclasses import asdict, dataclass
from pathlib import Path

from ruamel.yaml import YAML

from tobikodata.tcloud import constants as c

ENV_PROJECT = "from_env"
DEFAULT_PROJECT = "default_project"


@dataclass
class TCloudProject:
    url: str
    token: t.Optional[str]
    gateway: t.Optional[str]
    extras: t.Optional[t.List[str]]
    pip_executable: t.Optional[str] = None


def _load_yaml(path: Path) -> t.Optional[t.Dict[str, t.Any]]:
    if not path.exists():
        return None
    yaml = YAML(typ="safe")
    with open(path, "r", encoding="utf-8") as fd:
        config_str = fd.read()
        if not config_str:
            return None
    return yaml.load(config_str)


def load_project_configs(
    paths: t.Optional[t.List[Path]] = None,
    ignore_env: bool = False,
) -> t.Tuple[t.Optional[t.Dict[str, TCloudProject]], t.Optional[str]]:
    loaded_projects = {}
    if not ignore_env and "TCLOUD_URL" in os.environ:
        extras = None
        extras_raw = os.environ.get("TCLOUD_EXTRAS")
        if extras_raw is not None:
            extras = extras_raw.split(",")
        loaded_projects[ENV_PROJECT] = TCloudProject(
            url=os.environ["TCLOUD_URL"],
            token=os.environ.get("TCLOUD_TOKEN"),
            gateway=os.environ.get("TCLOUD_GATEWAY"),
            extras=extras,
            pip_executable=os.environ.get("TCLOUD_PIP_EXECUTABLE"),
        )

    if paths is None:
        paths = [
            c.TCLOUD_PATH / "tcloud.yaml",
            c.TCLOUD_PATH / "tcloud.yml",
            Path(".") / "tcloud.yaml",
            Path(".") / "tcloud.yml",
        ]

    found_config_file = False
    default_project_name = None
    for path in paths:
        config = _load_yaml(path)
        if config:
            found_config_file = True
            for project_name, settings in config.get("projects", {}).items():
                loaded_projects[project_name] = _to_tcloud_project(project_name, settings)
            if not default_project_name and DEFAULT_PROJECT in config:
                default_project_name = config[DEFAULT_PROJECT]
    if not found_config_file and not loaded_projects:
        return None, default_project_name
    return loaded_projects, default_project_name


def load_project_config(
    project: t.Optional[str],
    paths: t.Optional[t.List[Path]] = None,
) -> TCloudProject:
    projects, default_project = load_project_configs(paths)
    if projects is None:
        raise ValueError("Could not find tcloud configuration.")

    if not projects:
        raise ValueError("No projects found in configuration.")

    if project is None:
        project = ENV_PROJECT if ENV_PROJECT in projects else default_project

    if project is not None:
        if project not in projects:
            raise ValueError(f"Project '{project}' not found in configuration.")
        return projects[project]

    return list(projects.values())[0]


def _to_tcloud_project(project: str, raw: t.Dict[str, str]) -> TCloudProject:
    missing_fields = []
    token = os.environ.get("TCLOUD_TOKEN", raw.get("token"))
    for field in ("url", "gateway"):
        if field not in raw:
            missing_fields.append(field)
    if missing_fields:
        raise ValueError(
            f"""{", ".join([f"'{x}'" for x in missing_fields])} is missing in configuration for project '{project}'."""
        )
    extras = raw.get("extras")
    if isinstance(extras, str):
        extras = extras.split(",")  # type: ignore
    if extras is not None and not isinstance(extras, list):
        raise ValueError(f"'extras' is expected to be a list but got: {extras}.")
    return TCloudProject(
        url=raw["url"],
        token=token,  # type: ignore
        gateway=raw["gateway"],
        extras=extras,  # type: ignore
        pip_executable=raw.get("pip_executable"),
    )


def _load_previous_extras_contents(path: t.Optional[Path] = None) -> t.Dict[str, t.List[str]]:
    return _load_yaml(path or c.EXTRAS_PATH) or {}


def load_previous_extras(project_url: str, path: t.Optional[Path] = None) -> t.List[str]:
    contents = _load_previous_extras_contents(path)
    return contents.get(project_url, [])


def save_previous_extras(
    project_url: str, extras: t.List[str], path: t.Optional[Path] = None
) -> None:
    contents = _load_previous_extras_contents(path)
    contents[project_url] = extras
    yaml = YAML(typ="safe")
    path = path or c.EXTRAS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fd:
        yaml.dump(contents, fd)


def save_project_config(
    path: Path,
    project_config: t.Dict[str, TCloudProject],
    default_project: t.Optional[str] = None,
) -> None:
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=2)
    config = {"projects": {k: asdict(v) for k, v in project_config.items()}}
    if default_project:
        config[DEFAULT_PROJECT] = default_project  # type: ignore
    with open(path, "w", encoding="utf-8") as fd:
        yaml.dump(config, fd)
