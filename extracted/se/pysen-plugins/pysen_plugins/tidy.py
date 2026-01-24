import dataclasses
import logging
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
    process_utils,
)
from pysen.reporter import Reporter
from pysen.runner_options import PathContext
from pysen.types import TargetName


def tidy() -> PluginBase:
    return TidyPlugin()


class TidyPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint and root.lint.source:
            source = root.lint.source
        else:
            source = Source(includes=["."])

        tidy_config = dacite.from_dict(
            TidyConfig,
            config.config or {},
            config=dacite.Config(
                type_hooks={pathlib.Path: lambda p: file_path.parent / p},
                strict=True,
            ),
        )
        assert isinstance(tidy_config, TidyConfig)

        return [TidyComponent(source, tidy_config)]


@dataclasses.dataclass
class TidyConfig:
    config: pathlib.Path
    extensions: Sequence[str]


class TidyComponent(ComponentBase):
    def __init__(self, source: Source, config: TidyConfig) -> None:
        self._source = source
        self._config = config

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint", "format"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return TidyCommand(
            paths.base_dir, self._source, target == "format", self._config
        )


class TidyCommand(SingleFileFormatCommandBase):
    def __init__(
        self,
        base_dir: pathlib.Path,
        source: Source,
        inplace_edit: bool,
        config: TidyConfig,
    ) -> None:
        super().__init__(base_dir, source, inplace_edit)
        self._config = config

    @property
    def name(self) -> str:
        return "tidy"

    @property
    def has_side_effects(self) -> bool:
        return self.inplace_edit

    def filter(self, file_path: pathlib.Path) -> bool:
        return file_path.suffix in self._config.extensions

    def format(self, file_path: pathlib.Path, reporter: Reporter) -> Optional[str]:
        returncode, stdout, stderr = process_utils.run(
            ("tidy", "-quiet", "-config", str(self._config.config), str(file_path)),
            reporter,
            stdout_loglevel=logging.NOTSET,
            stderr_loglevel=logging.NOTSET,
        )
        if returncode == 0:
            return stdout
        else:
            reporter.process_output.log(logging.WARNING, file_path)
            reporter.process_output.log(logging.WARNING, stderr.rstrip("\n"))
            return None
