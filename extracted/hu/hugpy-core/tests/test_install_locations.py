"""Installation and runtime consumers agree on locations on an arbitrary host."""
import io
import json
import os
from pathlib import Path
import shlex
from types import SimpleNamespace

from hugpy_core.install import system, system_layout
from hugpy_resources.imports.functions.application_paths import resolve_paths
from hugpy_settings import local_settings


def test_install_generates_units_and_discovery_uses_same_profile(tmp_path, monkeypatch):
    for key in list(os.environ):
        if key.startswith(('HUGPY_', 'XDG_')):
            monkeypatch.delenv(key)
    account_home = tmp_path / 'account home'
    account = SimpleNamespace(pw_name='test-operator', pw_uid=os.getuid(), pw_gid=os.getgid(), pw_dir=str(account_home))
    root = tmp_path / 'chosen runtime'
    units = tmp_path / 'system units'
    monkeypatch.setenv('HUGPY_SERVICE_USER', account.pw_name)
    monkeypatch.setenv('HUGPY_HOME', str(root))
    monkeypatch.setenv('HUGPY_SYSTEMD_UNIT_DIR', str(units))
    monkeypatch.setattr(system.os, 'geteuid', lambda: 0)
    monkeypatch.setattr(system.os, 'chown', lambda *args: None)
    monkeypatch.setattr(system.os, 'fchown', lambda *args: None)
    monkeypatch.setattr(system.pwd, 'getpwnam', lambda name: account)
    calls = []
    monkeypatch.setattr(system, 'run', lambda *args, **kwargs: calls.append(args))
    monkeypatch.setattr(system, 'db_command', lambda *args: {'ready': True, 'dsn': 'dbname=test'})
    monkeypatch.setattr(system.subprocess, 'run', lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout='', stderr=''))
    class Response(io.BytesIO):
        status = 200
    monkeypatch.setattr(system.urllib.request, 'urlopen', lambda *args, **kwargs: Response(b'{}'))
    args = SimpleNamespace(host=None, port=None, database=None, central_models_home=None)
    assert system.install(args) == 0
    roots = resolve_paths()
    config = system.read_env(Path(roots['config']) / 'core.env')
    assert config['HUGPY_SERVICE_USER'] == account.pw_name
    for name in (system.CORE_UNIT, system.INTAKE_UNIT, system.TS_UNIT):
        unit = (units / name).read_text()
        assert f'User={account.pw_name}\n' in unit
        env_line = next(line.partition('=')[2] for line in unit.splitlines() if line.startswith('EnvironmentFile='))
        env_path = Path(env_line.replace('%%', '%'))
        assert env_path.parent == Path(roots['config'])
        assert system.read_env(env_path)['HUGPY_DATA_DIR'] == roots['data']
    for key, value in config.items():
        if key.startswith('HUGPY_'):
            monkeypatch.setenv(key, value)
    local_settings.update({'discovery_database': str(tmp_path / 'curated.sqlite3')})
    from hugpy_core.models import catalog_live
    endpoint = Path(roots['config']) / 'wrapper.endpoint.json'
    wrapper_state = tmp_path / 'existing wrapper state'
    endpoint.write_text(json.dumps({'store': str(wrapper_state)}))
    assert catalog_live.wrapper_path() == str(wrapper_state / 'fitevict.sqlite3')
    monkeypatch.setattr(catalog_live, 'DISCOVERY_DB', '')
    monkeypatch.setattr(catalog_live, 'DISCOVERY_DIR', '')
    assert catalog_live.discovery_path() == local_settings.values(('discovery',))['discovery_database']
    monkeypatch.setenv('HUGPY_DISCOVERY_DATABASE', str(tmp_path / 'explicit.sqlite3'))
    assert catalog_live.discovery_path() == str(tmp_path / 'explicit.sqlite3')
    monkeypatch.setattr(catalog_live, 'DISCOVERY_DB', str(tmp_path / 'legacy-override.sqlite3'))
    assert catalog_live.discovery_path() == str(tmp_path / 'legacy-override.sqlite3')


def test_upgrade_keeps_recorded_locations_and_explicit_overrides_win(tmp_path):
    units = tmp_path / 'units'
    units.mkdir()
    config = tmp_path / 'existing config' / 'core.env'
    state = tmp_path / 'existing state'
    (units / 'hugpy-core.service').write_text(
        f'User=existing-owner\nWorkingDirectory={state}\nEnvironmentFile={config}\n')
    name, unit_dir, existing = system_layout.select_identity({'HUGPY_SYSTEMD_UNIT_DIR': str(units)})
    account = SimpleNamespace(pw_name=name, pw_uid=os.getuid(), pw_gid=os.getgid(), pw_dir=str(tmp_path / 'home'))
    lay = system_layout.resolve(account, unit_dir, existing, environ={})
    assert lay.account == 'existing-owner'
    assert lay.config == config and lay.state == state
    assert not config.parent.exists()  # resolution never provisions
    custom = tmp_path / 'override'
    lay = system_layout.resolve(account, unit_dir, existing,
                                saved={'HUGPY_CORE_HOME': str(state)},
                                environ={'HUGPY_CORE_HOME': str(custom), 'HUGPY_CONFIG_DIR': str(custom / 'config')})
    assert lay.state == custom and lay.config_dir == custom / 'config'


def test_user_defaults_and_system_paths_are_derived_from_selected_account(tmp_path, monkeypatch):
    home = tmp_path / 'different-machine-account'
    roots = resolve_paths({}, home=home)
    assert all(Path(value).is_relative_to(home) for value in roots.values())
    env = {'HUGPY_HOME': str(tmp_path / 'runtime'), 'HUGPY_DATA_DIR': str(tmp_path / 'data-override')}
    resolved = resolve_paths(env, home=home)
    assert resolved['data'] == env['HUGPY_DATA_DIR']
    assert Path(resolved['config']).is_relative_to(env['HUGPY_HOME'])
    monkeypatch.setattr(system_layout.subprocess, 'check_output', lambda *args, **kwargs: str(tmp_path / 'os-config') + '\n')
    assert system_layout.unit_directory({}) == tmp_path / 'os-config/systemd/system'
    assert not home.exists()
