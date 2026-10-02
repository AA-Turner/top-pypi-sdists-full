import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest


def _load_smoke_module():
    superdoc = ModuleType('superdoc')
    superdoc.__path__ = []
    for name in (
        'AsyncSuperDocClient',
        'SuperDocClient',
        'choose_tools',
        'dispatch_superdoc_tool',
        'dispatch_superdoc_tool_async',
        'get_system_prompt',
        'get_tool_catalog',
        'list_presets',
    ):
        setattr(superdoc, name, object())
    superdoc.SuperDocError = RuntimeError

    runtime = ModuleType('superdoc.runtime')
    runtime.SuperDocSyncRuntime = object

    module_path = Path(__file__).with_name('smoke_core_preset.py')
    spec = importlib.util.spec_from_file_location('_smoke_core_preset_under_test', module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    original_sys_path = sys.path.copy()
    try:
        with patch.dict(sys.modules, {'superdoc': superdoc, 'superdoc.runtime': runtime}):
            spec.loader.exec_module(module)
    finally:
        sys.path[:] = original_sys_path
    return module


smoke_core_preset = _load_smoke_module()


def _sdk_root_for(repo_root: Path) -> Path:
    return repo_root / 'packages' / 'sdk' / 'langs' / 'python'


def test_cli_environment_overrides_uses_local_dist(monkeypatch, tmp_path):
    repo_root = tmp_path / 'public'
    built_cli = repo_root / 'apps' / 'cli' / 'dist' / 'index.js'
    built_cli.parent.mkdir(parents=True)
    built_cli.touch()
    monkeypatch.delenv('SUPERDOC_CLI_BIN', raising=False)
    monkeypatch.setattr(smoke_core_preset, 'SDK_ROOT', _sdk_root_for(repo_root))

    state_dir = tmp_path / 'cli-state'
    overrides = smoke_core_preset._cli_environment_overrides(state_dir)

    assert smoke_core_preset._resolve_cli_bin() == str(built_cli)
    assert overrides == {
        'SUPERDOC_CLI_STATE_DIR': str(state_dir),
        'SUPERDOC_CLI_BIN': str(built_cli),
    }


def test_cli_environment_overrides_leaves_cli_bin_unset_without_local_dist(monkeypatch, tmp_path):
    repo_root = tmp_path / 'public'
    monkeypatch.delenv('SUPERDOC_CLI_BIN', raising=False)
    monkeypatch.setattr(smoke_core_preset, 'SDK_ROOT', _sdk_root_for(repo_root))

    state_dir = tmp_path / 'cli-state'
    overrides = smoke_core_preset._cli_environment_overrides(state_dir)

    assert smoke_core_preset._resolve_cli_bin() is None
    assert overrides == {'SUPERDOC_CLI_STATE_DIR': str(state_dir)}
    assert 'SUPERDOC_CLI_BIN' not in overrides


def test_resolve_cli_bin_fails_fast_on_invalid_override(monkeypatch, tmp_path):
    monkeypatch.setenv('SUPERDOC_CLI_BIN', str(tmp_path / 'nonexistent-cli-binary'))

    with pytest.raises(RuntimeError, match='SUPERDOC_CLI_BIN'):
        smoke_core_preset._resolve_cli_bin()
