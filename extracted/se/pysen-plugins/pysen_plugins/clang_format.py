import dataclasses
import logging
import pathlib
from typing import List, Optional, Sequence

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


def clang_format() -> PluginBase:
    return ClangFormatPlugin()


@dataclasses.dataclass
class ClangFormatConfig:
    extensions: Optional[List[str]] = None
    command: Optional[List[str]] = None


class ClangFormatPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint and root.lint.source:
            source = root.lint.source
        else:
            source = Source(includes=["."])

        plugin_config = dacite.from_dict(
            ClangFormatConfig,
            config.config or {},
            config=dacite.Config(strict=True),
        )
        assert isinstance(plugin_config, ClangFormatConfig)
        return [ClangFormatComponent(plugin_config, source)]


class ClangFormatComponent(ComponentBase):
    def __init__(self, config: ClangFormatConfig, source: Source) -> None:
        self._config = config
        self._source = source

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint", "format"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return ClangFormatCommand(
            self._config, paths.base_dir, self._source, target == "format"
        )


class ClangFormatCommand(SingleFileFormatCommandBase):
    def __init__(
        self,
        config: ClangFormatConfig,
        base_dir: pathlib.Path,
        source: Source,
        inplace_edit: bool,
    ) -> None:
        super().__init__(base_dir, source, inplace_edit)

        self._config = config
        self._extensions = set(self._config.extensions or {".c", ".cpp", ".h", "hpp"})

    @property
    def name(self) -> str:
        return "clang_format"

    @property
    def has_side_effects(self) -> bool:
        return self.inplace_edit

    def filter(self, file_path: pathlib.Path) -> bool:
        return file_path.suffix in self._extensions

    def format(self, file_path: pathlib.Path, reporter: Reporter) -> Optional[str]:
        returncode, stdout, _ = process_utils.run(
            (self._config.command or ["clang-format"]) + [str(file_path)],
            reporter,
            stdout_loglevel=logging.NOTSET,
        )
        if returncode == 0:
            return stdout
        else:
            return None
