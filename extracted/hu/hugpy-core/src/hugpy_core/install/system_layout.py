"""Resolve system installation locations; provisioning remains in system.py."""
from dataclasses import dataclass
import os
from pathlib import Path
import pwd
import shlex
import subprocess

from hugpy_resources.imports.functions.application_paths import resolve_paths, service_account


@dataclass(frozen=True)
class Layout:
    account: str
    account_home: Path
    group: int
    roots: dict
    state: Path
    unit_dir: Path

    @property
    def config_dir(self): return Path(self.roots['config'])
    @property
    def config(self): return self.config_dir / 'core.env'
    @property
    def flask_config(self): return self.config_dir / 'core.service-flask-db.env'
    @property
    def toolserver_config(self): return self.config_dir / 'toolserver.env'
    @property
    def endpoint(self): return self.config_dir / 'core.endpoint.json'
    @property
    def wrapper_endpoint(self): return self.config_dir / 'wrapper.endpoint.json'
    @property
    def wrapper_config(self): return self.config_dir / 'wrapper.env'
    @property
    def ts_home(self): return self.state / 'toolserver'

    def environment(self):
        return {'HOME': str(self.account_home), 'HUGPY_SERVICE_USER': self.account,
                'HUGPY_HOME': self.roots['home'],
                **{'HUGPY_' + key.upper() + '_DIR': self.roots[key] for key in ('config', 'data', 'cache')},
                'HUGPY_CORE_HOME': str(self.state), 'HUGPY_SYSTEMD_UNIT_DIR': str(self.unit_dir)}


def unit_directory(environ):
    if environ.get('HUGPY_SYSTEMD_UNIT_DIR'):
        return Path(environ['HUGPY_SYSTEMD_UNIT_DIR']).expanduser().absolute()
    # Ask this systemd installation for its configuration root.
    base = subprocess.check_output(['systemd-path', 'system-configuration'], text=True).strip()
    if not Path(base).is_absolute():
        raise ValueError('systemd did not report an absolute configuration directory')
    return Path(base) / 'systemd' / 'system'


def unit_values(path):
    """Read only the installation pointers from our existing generated unit."""
    result = {}
    if path.exists():
        for line in path.read_text().splitlines():
            key, sep, value = line.partition('=')
            if sep and key in ('User', 'WorkingDirectory', 'EnvironmentFile'):
                words = [value.strip()] if key in ("WorkingDirectory", "EnvironmentFile") and not value.startswith('"') else shlex.split(value)
                if words and key not in result:
                    result[key] = words[0].lstrip('-').replace('%%', '%')
    return result


def select_identity(environ=None):
    env = os.environ if environ is None else environ
    units = unit_directory(env)
    existing = unit_values(units / 'hugpy-core.service')
    name = env.get('HUGPY_SERVICE_USER') or existing.get('User') or service_account(env)
    return name, units, existing


def resolve(account, units, existing, saved=None, environ=None):
    """Explicit installer environment > recorded configuration > shared defaults."""
    env = os.environ if environ is None else environ
    saved = saved or {}
    # Do not inherit root/sudo's HOME or XDG folders for a different service user.
    location_env = {key: value for key, value in saved.items()
                    if key.startswith(('HUGPY_', 'XDG_'))}
    location_env.update({key: value for key, value in env.items() if key.startswith('HUGPY_')})
    if account.pw_uid == os.geteuid():
        location_env.update({key: value for key, value in env.items() if key.startswith('XDG_')})
    if 'HUGPY_CONFIG_DIR' not in location_env and existing.get('EnvironmentFile'):
        location_env['HUGPY_CONFIG_DIR'] = str(Path(existing['EnvironmentFile']).parent)
    roots = resolve_paths(location_env, home=account.pw_dir)
    state = location_env.get('HUGPY_CORE_HOME') or existing.get('WorkingDirectory') or str(Path(roots['data']) / 'core')
    if state == '~' or state.startswith('~/'):
        state = account.pw_dir + state[1:]
    state = Path(state).absolute()
    return Layout(account.pw_name, Path(account.pw_dir), account.pw_gid, roots, state, units)
