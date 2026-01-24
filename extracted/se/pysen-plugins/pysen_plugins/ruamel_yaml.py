import dataclasses
import io
import pathlib
from typing import Optional, Sequence

import dacite

from pysen import (
    CommandBase,
    ComponentBase,
    Config,
    PluginBase,
    PluginConfig,
    RunOptions,
    SingleFileFormatCommandBase,
    Source,
)
from pysen.reporter import Reporter
from pysen.runner_options import PathContext
from pysen.types import TargetName

try:
    import ruamel.yaml

    _ruamel_yaml_import_error = None
except ImportError as e:
    _ruamel_yaml_import_error = e


def ruamel_yaml() -> PluginBase:
    if _ruamel_yaml_import_error:
        raise _ruamel_yaml_import_error
    return RuamelYamlPlugin()


class RuamelYamlPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint and root.lint.source:
            source = root.lint.source
        else:
            source = Source(includes=["."])

        ruamel_yaml_config = dacite.from_dict(
            RuamelYamlConfig,
            config.config or {},
            config=dacite.Config(strict=True),
        )
        assert isinstance(ruamel_yaml_config, RuamelYamlConfig)

        return [RuamelYamlComponent(source, ruamel_yaml_config)]


@dataclasses.dataclass
class RuamelYamlConfig:
    explicit_start: Optional[bool] = None
    preserve_quotes: Optional[bool] = None


class RuamelYamlComponent(ComponentBase):
    def __init__(self, source: Source, config: RuamelYamlConfig) -> None:
        self._source = source
        self._config = config

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint", "format"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return RuamelYamlCommand(
            paths.base_dir, self._source, target == "format", self._config
        )


class RuamelYamlCommand(SingleFileFormatCommandBase):
    def __init__(
        self,
        base_dir: pathlib.Path,
        source: Source,
        inplace_edit: bool,
        config: RuamelYamlConfig,
    ) -> None:
        super().__init__(base_dir, source, inplace_edit)
        self._yaml = ruamel.yaml.YAML()
        self._yaml.explicit_start = config.explicit_start  # type: ignore
        self._yaml.preserve_quotes = config.preserve_quotes  # type: ignore

    @property
    def name(self) -> str:
        return "ruamel_yaml"

    @property
    def has_side_effects(self) -> bool:
        return self.inplace_edit

    def filter(self, file_path: pathlib.Path) -> bool:
        return file_path.suffix in {".yaml", ".yml"}

    def format(self, file_path: pathlib.Path, reporter: Reporter) -> Optional[str]:
        f = io.StringIO()
        try:
            self._yaml.dump(self._yaml.load(file_path), f)
        except ruamel.yaml.parser.ParserError as e:
            reporter.logger.exception(e)
            return None
        return f.getvalue()
