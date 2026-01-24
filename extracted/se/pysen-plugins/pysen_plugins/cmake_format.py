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
from pysen.component import LintComponentBase
from pysen.reporter import Reporter
from pysen.runner_options import PathContext


def cmake_format() -> PluginBase:
    return CMakeFormatPlugin()


class CMakeFormatPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, raw_config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint is not None and root.lint.source is not None:
            source = root.lint.source
        else:
            source = Source(includes=["."])

        config: CMakeFormatConfig
        if raw_config.config is not None:
            config = dacite.from_dict(
                CMakeFormatConfig,
                raw_config.config or {},
                config=dacite.Config(
                    type_hooks={pathlib.Path: lambda p: file_path.parent / p},
                    strict=True,
                ),
            )
            assert isinstance(config, CMakeFormatConfig)
        else:
            config = CMakeFormatConfig()

        return [CMakeFormatComponent(source, config)]


@dataclasses.dataclass
class CMakeFormatConfig:
    config_files: Optional[Sequence[pathlib.Path]] = None


class CMakeFormatComponent(LintComponentBase):
    def __init__(self, source: Source, config: CMakeFormatConfig) -> None:
        super().__init__("cmake_format", source)
        self._config = config

    @property
    def targets(self) -> Sequence[str]:
        return ["lint", "format"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return CMakeFormatCommand(
            paths.base_dir, self.source, self._config, target == "format"
        )


class CMakeFormatCommand(SingleFileFormatCommandBase):
    def __init__(
        self,
        base_dir: pathlib.Path,
        source: Source,
        config: CMakeFormatConfig,
        inplace_edit: bool,
    ) -> None:
        super().__init__(base_dir, source, inplace_edit)
        self._config = config

    @property
    def name(self) -> str:
        return "cmake_format"

    @property
    def has_side_effects(self) -> bool:
        return self.inplace_edit

    def filter(self, file_path: pathlib.Path) -> bool:
        return file_path.name == "CMakeLists.txt" or file_path.suffix == ".cmake"

    def __call__(self, reporter: Reporter) -> int:
        if self._config.config_files is not None:
            for p in self._config.config_files:
                if not p.exists():
                    raise RuntimeError(f"config_file: {p} does not exist")

        return super().__call__(reporter)

    def format(self, file_path: pathlib.Path, reporter: Reporter) -> Optional[str]:
        cmd = [
            "cmake-format",
        ]
        if self._config.config_files is not None:
            cmd.append("--config-files")
            cmd.extend(map(str, self._config.config_files))

        cmd += [
            "--",
            str(file_path),
        ]
        returncode, stdout, _ = process_utils.run(
            cmd,
            reporter,
            stdout_loglevel=logging.NOTSET,
        )
        if returncode == 0:
            return stdout
        else:
            return None
