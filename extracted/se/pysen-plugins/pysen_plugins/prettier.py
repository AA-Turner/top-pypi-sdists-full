import dataclasses
import errno
import pathlib
from typing import Sequence

import dacite

from pysen import (
    CommandBase,
    ComponentBase,
    Config,
    PluginBase,
    PluginConfig,
    RunOptions,
    Source,
    git_utils,
    process_utils,
)
from pysen.reporter import Reporter
from pysen.runner_options import PathContext
from pysen.types import TargetName


def prettier() -> PluginBase:
    return PrettierPlugin()


@dataclasses.dataclass
class PrettierConfig:
    extensions: Sequence[str]
    strict_extentions: bool = False


class PrettierPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint and root.lint.source:
            source = root.lint.source
        else:
            source = Source(includes=["."])

        prettier_config = dacite.from_dict(
            PrettierConfig,
            config.config or {},
            config=dacite.Config(strict=True),
        )
        assert isinstance(prettier_config, PrettierConfig)

        return [PrettierComponent(prettier_config, source)]


class PrettierComponent(ComponentBase):
    def __init__(self, config: PrettierConfig, source: Source) -> None:
        self._config = config
        self._source = source

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint", "format"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return PrettierCommand(
            self._config, paths.base_dir, self._source, target == "format"
        )


class PrettierCommand(CommandBase):
    def __init__(
        self,
        config: PrettierConfig,
        base_dir: pathlib.Path,
        source: Source,
        inplace_edit: bool,
    ) -> None:
        self._config = config
        self._base_dir = base_dir
        self._source = source
        self._inplace_edit = inplace_edit

    @property
    def name(self) -> str:
        return "prettier"

    @property
    def has_side_effects(self) -> bool:
        return self._inplace_edit

    def __call__(self, reporter: Reporter) -> int:
        def extention_check(file_path: pathlib.Path) -> bool:
            return file_path.suffix in self._config.extensions

        sources = [
            file_path
            for file_path in self._source.resolve_files(
                self._base_dir,
                extention_check,
                git_utils.check_git_available(self._base_dir),
                reporter,
            )
        ]

        if self._config.strict_extentions:
            sources = list(filter(extention_check, sources))
        str_sources = [str(s) for s in sources]

        command = ["prettier"]
        if self._inplace_edit:
            command.append("--write")
        else:
            command.append("--check")

        code = 0
        chunks = [str_sources]
        while len(chunks) > 0:
            chunk = chunks.pop()
            if len(chunk) == 0:
                continue
            try:
                returncode, _, _ = process_utils.run(command + chunk, reporter)
                if returncode != 0:
                    code = returncode
            except OSError as e:
                if len(chunk) >= 2 and e.errno == errno.E2BIG:
                    c = len(chunk) // 2
                    chunks.append(chunk[:c])
                    chunks.append(chunk[c:])
                else:
                    raise

        return code
