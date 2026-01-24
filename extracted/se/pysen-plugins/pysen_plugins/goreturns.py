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


def goreturns() -> PluginBase:
    return GoreturnsPlugin()


class GoreturnsPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint and root.lint.source:
            source = root.lint.source
        else:
            source = Source(includes=["."])
        return [GoreturnsComponent(source)]


class GoreturnsComponent(ComponentBase):
    def __init__(self, source: Source) -> None:
        self._source = source

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint", "format"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return GoreturnsCommand(paths.base_dir, self._source, target == "format")


class GoreturnsCommand(SingleFileFormatCommandBase):
    @property
    def name(self) -> str:
        return "goreturns"

    @property
    def has_side_effects(self) -> bool:
        return self.inplace_edit

    def filter(self, file_path: pathlib.Path) -> bool:
        return file_path.suffix in {".go"}

    def format(self, file_path: pathlib.Path, reporter: Reporter) -> Optional[str]:
        returncode, stdout, _ = process_utils.run(
            ("goreturns", str(file_path)),
            reporter,
            stdout_loglevel=logging.NOTSET,
        )
        if returncode == 0:
            return stdout
        else:
            return None
