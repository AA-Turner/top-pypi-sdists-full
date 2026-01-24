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


def shfmt() -> PluginBase:
    return ShfmtPlugin()


class ShfmtPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint and root.lint.source:
            source = root.lint.source
        else:
            source = Source(includes=["."])
        return [ShfmtComponent(source)]


class ShfmtComponent(ComponentBase):
    def __init__(self, source: Source) -> None:
        self._source = source

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint", "format"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return ShfmtCommand(paths.base_dir, self._source, target == "format")


class ShfmtCommand(SingleFileFormatCommandBase):
    @property
    def name(self) -> str:
        return "shfmt"

    @property
    def has_side_effects(self) -> bool:
        return self.inplace_edit

    def filter(self, file_path: pathlib.Path) -> bool:
        return file_path.suffix in {".bash", ".sh"}

    def format(self, file_path: pathlib.Path, reporter: Reporter) -> Optional[str]:
        returncode, stdout, _ = process_utils.run(
            ("shfmt", str(file_path)),
            reporter,
            stdout_loglevel=logging.NOTSET,
        )
        if returncode == 0:
            return stdout
        else:
            return None
