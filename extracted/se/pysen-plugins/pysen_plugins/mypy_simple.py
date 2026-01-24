import pathlib
from dataclasses import dataclass
from typing import Any, DefaultDict, Dict, Mapping, Optional, Sequence

import dacite

from pysen import (
    CommandBase,
    ComponentBase,
    Config,
    MypyPreset,
    MypySetting,
    MypyTarget,
    PluginBase,
    PluginConfig,
    RunOptions,
    Source,
)
from pysen.component import LintComponentBase
from pysen.ext import mypy_wrapper
from pysen.lint_command import LintCommandBase
from pysen.path import resolve_path
from pysen.reporter import Reporter
from pysen.runner_options import PathContext
from pysen.setting import SettingFile
from pysen.source import PythonFileFilter
from pysen.types import TargetName

_SettingFileName = "setup.cfg"


def mypy_simple() -> PluginBase:
    return MypySimplePlugin()


def _parse_mypy_preset(s: Any) -> MypyPreset:
    if not isinstance(s, str):
        raise dacite.WrongTypeError(MypyPreset, s)

    try:
        return MypyPreset[s.upper()]
    except KeyError:
        raise dacite.DaciteError(f"invalid mypy_preset value: {s}") from None


@dataclass
class MypySimplePluginConfig:
    preset: Optional[MypyPreset] = None


class MypySimplePlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config_data: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint and root.lint.source:
            source = root.lint.source
        else:
            source = Source(includes=["."])

        config = dacite.from_dict(
            MypySimplePluginConfig,
            config_data.config or {},
            dacite.Config(type_hooks={MypyPreset: _parse_mypy_preset}, strict=True),
        )

        if root.lint:
            global_presest = root.lint.mypy_preset or MypyPreset.STRICT
        else:
            global_presest = MypyPreset.STRICT

        preset = config.preset or global_presest

        return [MypySimpleComponent(source, setting=preset.get_setting())]


class MypySimpleComponent(LintComponentBase):
    def __init__(
        self,
        source: Source,
        name: str = "mypy_simple",
        setting: Optional[MypySetting] = None,
        module_settings: Optional[Mapping[str, MypySetting]] = None,
    ) -> None:
        super().__init__(name, source)
        self._setting = setting or MypySetting()
        self._module_settings: Dict[str, MypySetting] = dict(module_settings or {})

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def setting(self) -> MypySetting:
        return self._setting

    @property
    def module_settings(self) -> Dict[str, MypySetting]:
        return self._module_settings

    def export_settings(
        self,
        paths: PathContext,
        files: DefaultDict[str, SettingFile],
    ) -> None:
        setting_file = files[_SettingFileName]
        global_section, global_setting = self._setting.export(paths.base_dir)
        setting_file.set_section(global_section, global_setting)

        for module_name, setting in self._module_settings.items():
            section, module_setting = setting.export(
                paths.base_dir, target_module=module_name
            )
            setting_file.set_section(section, module_setting)

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        if target == "lint":
            return MypySimpleCommand(
                self.name, paths, self.source, options.require_diagnostics
            )

        raise AssertionError(f"unknown {target}")


class MypySimpleCommand(LintCommandBase):
    def __init__(
        self, name: str, paths: PathContext, source: Source, require_diagnostics: bool
    ) -> None:
        super().__init__(paths.base_dir, source)
        self._name = name
        self._setting_path = resolve_path(paths.settings_dir, _SettingFileName)
        self._require_diagnostics = require_diagnostics

    @property
    def name(self) -> str:
        return self._name

    @property
    def has_side_effects(self) -> bool:
        return False

    def __call__(self, reporter: Reporter) -> int:
        sources = self._get_sources(reporter, PythonFileFilter)
        reporter.logger.info(f"Checking {len(sources)} files")
        target = MypyTarget(paths=list(sources))
        return mypy_wrapper.run(
            reporter,
            self.base_dir,
            self._setting_path,
            target,
            self._require_diagnostics,
        )

    def run_files(self, reporter: Reporter, files: Sequence[pathlib.Path]) -> int:
        covered_files = self._get_covered_files(reporter, files, PythonFileFilter)

        if len(covered_files) == 0:
            return 0

        return mypy_wrapper.run(
            reporter,
            self.base_dir,
            self._setting_path,
            MypyTarget(list(covered_files)),
            self._require_diagnostics,
        )
