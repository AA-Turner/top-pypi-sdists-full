"""Installation and runtime consumers agree on locations on an arbitrary host."""
import io
import os
from pathlib import Path
from types import SimpleNamespace

from hugpy_core.install import system, system_layout
from hugpy_resources.imports.functions.application_paths import resolve_paths


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
    # The catalog reads discovery's published export (api_*_v1 views), never a
    # live store or the wrapper's own database; explicit overrides win.
    from hugpy_core import discovery
    from hugpy_core.models import catalog_live
    assert catalog_live.discovery_path() == discovery.export_db()
    monkeypatch.setenv('HUGPY_DISCOVERY_EXPORT', str(tmp_path / 'export'))
    assert catalog_live.discovery_path() == str(tmp_path / 'export' / 'discovery.sqlite3')
    monkeypatch.setenv('HUGPY_CATALOG_DISCOVERY_DB', str(tmp_path / 'explicit.sqlite3'))
    assert catalog_live.discovery_path() == str(tmp_path / 'explicit.sqlite3')


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


def test_uninstall_removes_what_install_added_and_a_reinstall_finds_the_same_install(tmp_path, monkeypatch):
    """Uninstall takes the units and the endpoint away and keeps configuration, state and operator drop-ins.
    With the unit gone, a plain install must find the recorded account, configuration and state again, not
    guess a new account with an empty state beside the first."""
    for key in list(os.environ):
        if key.startswith(('HUGPY_', 'XDG_')):
            monkeypatch.delenv(key)
    config_dir, units, state = tmp_path / 'etc hugpy', tmp_path / 'units', tmp_path / 'state'
    for directory in (config_dir, units, state, units / (system.CORE_UNIT + '.d')):
        directory.mkdir(parents=True)
    (units / (system.CORE_UNIT + '.d') / 'operator.conf').write_text('[Service]\nEnvironment=X=1\n')
    for name in (system.CORE_UNIT, system.INTAKE_UNIT, system.PG_UNIT):
        (units / name).write_text(f'[Service]\nUser=core-account\nWorkingDirectory={state}\n'
                                  f'EnvironmentFile={config_dir / "core.env"}\n')
    (config_dir / 'core.env').write_text(f'HUGPY_SERVICE_USER="core-account"\nHUGPY_CONFIG_DIR="{config_dir}"\n'
                                         f'HUGPY_CORE_HOME="{state}"\nHUGPY_CORE_DB="dbname=kept"\n')
    (config_dir / 'core.endpoint.json').write_text('{}')
    account = SimpleNamespace(pw_name='core-account', pw_uid=os.getuid(), pw_gid=os.getgid(), pw_dir=str(tmp_path / 'home'))
    monkeypatch.setenv('HUGPY_SYSTEMD_UNIT_DIR', str(units))
    monkeypatch.setattr(system_layout, 'SYSTEM_CONFIG_DIR', config_dir)
    monkeypatch.setattr(system.os, 'geteuid', lambda: 0)
    monkeypatch.setattr(system.subprocess, 'run', lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout='', stderr=''))

    name, unit_dir, existing = system_layout.select_identity()
    lay = system_layout.resolve(account, unit_dir, existing, system.read_env(config_dir / 'core.env'))
    assert system.uninstall(lay) == 0
    assert not any((units / unit).exists() for unit in (system.CORE_UNIT, system.INTAKE_UNIT, system.PG_UNIT))
    assert not (config_dir / 'core.endpoint.json').exists()
    assert (units / (system.CORE_UNIT + '.d') / 'operator.conf').exists()
    assert system.read_env(config_dir / 'core.env')['HUGPY_CORE_DB'] == 'dbname=kept' and state.is_dir()

    name, unit_dir, existing = system_layout.select_identity()          # no unit left: the record in core.env
    assert name == 'core-account'
    again = system_layout.resolve(account, unit_dir, existing, system.read_env(config_dir / 'core.env'))
    assert (again.config, again.state) == (config_dir / 'core.env', state)
    # a caller that names its own location is not overridden by an old record
    monkeypatch.setenv('HUGPY_SERVICE_USER', 'someone-else')
    assert system_layout.select_identity()[0] == 'someone-else'
