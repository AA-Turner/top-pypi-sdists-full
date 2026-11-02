"""The parts of `databaas.yml` a DAG deploy reads.

```yaml
bundle:
  name: marine-pipeline
targets:
  dev:
    mode: development
  prod:
    mode: production
artifacts:
  dags: airflow/
```

Other keys are ignored, so the file can carry settings for other tools.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from databaas_utils.errors import ConfigurationError

CONFIG_NAME = "databaas.yml"
MODES = ("development", "production")

# The rule CI applied before this command existed; bundle names already in use
# (e.g. `marine-pipeline`) follow it.
_BUNDLE_NAME = re.compile(r"^[a-z][a-z0-9-]*$")


@dataclass(frozen=True)
class Target:
    """One entry under ``targets``.

    Attributes:
        name: Key under ``targets``, passed as ``-t``.
        mode: ``development`` or ``production``.
        default: Whether ``-t`` may be omitted to pick this target.
    """

    name: str
    mode: str
    default: bool = False

    @property
    def production(self) -> bool:
        """Whether ``mode`` is ``production``."""
        return self.mode == "production"


@dataclass(frozen=True)
class DagsConfig:
    """A parsed `databaas.yml`.

    Attributes:
        name: ``bundle.name``; the last path segment of every target's prefix.
        root: Directory holding the config file.
        source: The ``artifacts.dags`` directory, resolved against ``root``.
        targets: Targets by name.
    """

    name: str
    root: Path
    source: Path
    targets: Mapping[str, Target] = field(default_factory=dict)

    def target(self, name: str | None = None) -> Target:
        """The named target, else the ``default: true`` one, else the only one.

        Raises:
            ConfigurationError: If ``name`` is unknown, or none is given and
                the choice is ambiguous.
        """
        if name:
            if name not in self.targets:
                raise ConfigurationError(
                    f"no target {name!r} in {CONFIG_NAME} — known: {sorted(self.targets)}"
                )
            return self.targets[name]
        defaults = [t for t in self.targets.values() if t.default]
        if len(defaults) == 1:
            return defaults[0]
        if len(self.targets) == 1:
            return next(iter(self.targets.values()))
        raise ConfigurationError(
            f"choose a target with -t ({', '.join(sorted(self.targets))}) or mark one "
            f"'default: true' in {CONFIG_NAME}"
        )


def find_config(start: Path | None = None) -> Path:
    """`databaas.yml` in `start` or the nearest parent directory.

    Raises:
        ConfigurationError: If there is none.
    """
    here = Path(start or Path.cwd()).resolve()
    for directory in (here, *here.parents):
        candidate = directory / CONFIG_NAME
        if candidate.is_file():
            return candidate
    raise ConfigurationError(f"no {CONFIG_NAME} found in {here} or its parents")


def load_config(path: Path | None = None) -> DagsConfig:
    """Read `databaas.yml`, found from the working directory if `path` is omitted.

    Raises:
        ConfigurationError: If PyYAML is missing, or the file is unreadable or
            invalid.
    """
    try:
        import yaml
    except ImportError as exc:
        raise ConfigurationError(
            "reading databaas.yml needs PyYAML — install databaas-utils[deploy]"
        ) from exc

    config_path = Path(path) if path else find_config()
    try:
        raw = yaml.safe_load(config_path.read_text())
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigurationError(f"could not read {config_path}: {exc}") from exc
    return parse_config(raw, root=config_path.parent)


def _mapping(value: Any, where: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"{where} in {CONFIG_NAME} must be a mapping")
    return value


def parse_config(raw: Any, *, root: Path) -> DagsConfig:
    """Validate parsed YAML; `root` resolves ``artifacts.dags``.

    Raises:
        ConfigurationError: On a missing or invalid bundle name, DAG directory
            or target, or more than one production or default target.
    """
    doc = _mapping(raw, "the top level")
    bundle = _mapping(doc.get("bundle"), "'bundle'")
    name = str(bundle.get("name") or "")
    if not _BUNDLE_NAME.fullmatch(name):
        raise ConfigurationError(
            f"bundle.name {name!r} must be lower-case letters, digits and hyphens, "
            "starting with a letter"
        )

    artifacts = _mapping(doc.get("artifacts"), "'artifacts'")
    dags = artifacts.get("dags")
    if not dags:
        raise ConfigurationError(f"{CONFIG_NAME} needs artifacts.dags")
    source = (root / str(dags)).resolve()
    if not source.is_dir():
        raise ConfigurationError(f"artifacts.dags {source} is not a directory")

    raw_targets = _mapping(doc.get("targets"), "'targets'")
    if not raw_targets:
        raise ConfigurationError(f"{CONFIG_NAME} needs at least one target")
    targets: dict[str, Target] = {}
    for target_name, raw_values in raw_targets.items():
        values = _mapping(raw_values or {}, f"target {target_name!r}")
        mode = values.get("mode")
        if mode not in MODES:
            raise ConfigurationError(
                f"target {target_name!r} needs mode: {' or '.join(MODES)}"
            )
        targets[str(target_name)] = Target(
            name=str(target_name), mode=mode, default=bool(values.get("default"))
        )
    if sum(t.production for t in targets.values()) > 1:
        raise ConfigurationError(
            "only one production target is allowed: it deploys to dags/prod/<bundle>/"
        )
    if sum(t.default for t in targets.values()) > 1:
        raise ConfigurationError("only one target can be 'default: true'")
    return DagsConfig(name=name, root=root, source=source, targets=targets)
