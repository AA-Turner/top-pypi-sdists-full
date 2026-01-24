import logging
import pathlib
from typing import Optional, Sequence

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


def jq() -> PluginBase:
    return JqPlugin()


class JqPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint and root.lint.source:
            source = root.lint.source
        else:
            source = Source(includes=["."])
        return [JqComponent(source)]


class JqComponent(ComponentBase):
    def __init__(self, source: Source) -> None:
        self._source = source

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint", "format"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return JqCommand(paths.base_dir, self._source, target == "format")


class JqCommand(SingleFileFormatCommandBase):
    @property
    def name(self) -> str:
        return "jq"

    @property
    def has_side_effects(self) -> bool:
        return self.inplace_edit

    def filter(self, file_path: pathlib.Path) -> bool:
        return file_path.suffix in {".json"}

    def format(self, file_path: pathlib.Path, reporter: Reporter) -> Optional[str]:
        returncode, stdout, _ = process_utils.run(
            ("jq", ".", str(file_path)),
            reporter,
            stdout_loglevel=logging.NOTSET,
        )
        if returncode == 0:
            return stdout
        else:
            return None
