import pathlib
from typing import Optional, Sequence

from pysen.black import BlackCommand
from pysen.command import CommandBase
from pysen.component import LintComponentBase
from pysen.runner_options import PathContext, RunOptions
from pysen.source import Source


class Black(LintComponentBase):
    def __init__(
        self,
        name: str = "black",
        source: Optional[Source] = None,
        settings_dir: Optional[pathlib.Path] = None,
    ) -> None:
        super().__init__(name, source)
        self._settings_dir = settings_dir or pathlib.Path(".")

    @property
    def targets(self) -> Sequence[str]:
        return ["lint", "format"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        paths = PathContext(base_dir=paths.base_dir, settings_dir=self._settings_dir)
        if target == "lint":
            return BlackCommand(self.name, paths, self.source, False)
        elif target == "format":
            return BlackCommand(self.name, paths, self.source, True)

        raise AssertionError(f"unknown {target}")
