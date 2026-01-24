import pathlib
from typing import List, Optional, Sequence

from pysen.command import CommandBase
from pysen.component import ComponentBase
from pysen.ext.mypy_wrapper import MypyTarget
from pysen.mypy import MypyCommand
from pysen.runner_options import PathContext, RunOptions


class Mypy(ComponentBase):
    def __init__(
        self,
        name: str = "mypy",
        mypy_targets: Optional[Sequence[MypyTarget]] = None,
        settings_dir: Optional[pathlib.Path] = None,
    ) -> None:
        self._name = name
        self._mypy_targets = list(mypy_targets or [])
        self._settings_dir = settings_dir or pathlib.Path(".")

    @property
    def name(self) -> str:
        return self._name

    @property
    def mypy_targets(self) -> List[MypyTarget]:
        return self._mypy_targets

    @property
    def targets(self) -> Sequence[str]:
        return ["lint"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        paths = PathContext(base_dir=paths.base_dir, settings_dir=self._settings_dir)
        if target == "lint":
            return MypyCommand(
                self.name, paths, self.mypy_targets, options.require_diagnostics
            )

        raise AssertionError(f"unknown {target}")
