from typing import Sequence

from pysen import CommandBase, ComponentBase, RunOptions, Source
from pysen.runner_options import PathContext
from pysen.types import TargetName

from .command import PylintCommand


class PylintComponent(ComponentBase):
    def __init__(self, source: Source) -> None:
        self._source = source

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return PylintCommand(paths.base_dir, self._source, paths.settings_dir)
