import dataclasses
import pathlib
from typing import Any, Dict, List, Optional, Sequence

import dacite

from pysen import PluginBase
from pysen.component import ComponentBase
from pysen.exceptions import InvalidConfigurationError
from pysen.mypy import MypyTarget
from pysen.pyproject_model import (
    Config,
    PluginConfig,
    _expand_path,
    _parse_mypy_targets,
    _parse_source,
)
from pysen.source import Source
from pysen_plugins.customizable_builtins.black import Black
from pysen_plugins.customizable_builtins.flake8 import Flake8
from pysen_plugins.customizable_builtins.isort import Isort
from pysen_plugins.customizable_builtins.mypy import Mypy


@dataclasses.dataclass
class CustomizablePysenConfigureLintOptions:
    enable_black: Optional[bool] = None
    enable_flake8: Optional[bool] = None
    enable_isort: Optional[bool] = None
    enable_mypy: Optional[bool] = None
    source: Optional[Source] = None
    mypy_targets: Optional[List[MypyTarget]] = None


@dataclasses.dataclass
class CustomizablePysenConfig:
    lint: Optional[CustomizablePysenConfigureLintOptions]
    settings_dir: Optional[pathlib.Path]


def _parse_dict(
    data: Dict[str, Any], base_dir: pathlib.Path
) -> CustomizablePysenConfig:
    dacite_config = dacite.Config(
        type_hooks={
            Source: lambda x: _parse_source(base_dir, x),
            pathlib.Path: lambda x: _expand_path(base_dir, x),
            List[MypyTarget]: lambda x: _parse_mypy_targets(base_dir, x),
        },
        strict=True,
    )

    try:
        config = dacite.from_dict(CustomizablePysenConfig, data, dacite_config)
        assert isinstance(config, CustomizablePysenConfig)
        return config
    except dacite.DaciteError as e:
        raise InvalidConfigurationError(f"invalid configuration: {e}") from None


class CustomizablePysenPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        base_dir = file_path.parent
        plugin_config = _parse_dict(data=config.config or {}, base_dir=base_dir)
        lint_config = plugin_config.lint or CustomizablePysenConfigureLintOptions()
        components: List[ComponentBase] = []
        if lint_config.enable_black:
            components.append(
                Black(
                    source=lint_config.source,
                    settings_dir=plugin_config.settings_dir or base_dir,
                )
            )
        if lint_config.enable_flake8:
            components.append(
                Flake8(
                    source=lint_config.source,
                    settings_dir=plugin_config.settings_dir or base_dir,
                )
            )
        if lint_config.enable_isort:
            components.append(
                Isort(
                    source=lint_config.source,
                    settings_dir=plugin_config.settings_dir or base_dir,
                )
            )
        if lint_config.enable_mypy:
            components.append(
                Mypy(
                    mypy_targets=lint_config.mypy_targets,
                    settings_dir=plugin_config.settings_dir or base_dir,
                )
            )

        return components


def customizable_builtins() -> CustomizablePysenPlugin:
    return CustomizablePysenPlugin()
