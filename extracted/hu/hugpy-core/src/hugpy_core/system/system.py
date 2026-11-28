"""`hugpy-core system install | status | uninstall | key | set`: hugpy-core as a service of the host.

install (as root) lays down, saying each step:
  the account hugpy-core (it runs Core)
  /var/lib/hugpy/core              core.sqlite3 (the saved connections with every wrapper's key, the settings
                                   table, and everything collated: the call log holds what was asked and
                                   answered) and api.key. The account's own: nobody else reads it
  Core's API key                   made once and kept (api.key): what a caller on another host carries;
                                   `system key` prints it
  /etc/hugpy/core.local.key        the key of this host's own programs, made once and kept: every account of the
                                   host can read it and nothing outside the host can. Core's command line carries
                                   it. The door asks a key of every caller: where a call seems to come from says
                                   nothing behind a web front or a forward of the port
  hugpy-core.service               Core: its door and the collector
  /etc/hugpy/core.endpoint.json    where the door is, for the command line of any account of the host
  this host's own wrapper          connected, when the host has one (its install recorded where it listens) and
                                   Core has no saved connection yet; --no-local-wrapper leaves it out

hugpy-core before 0.5 was a web server with a collector, a downloader and a catalog process as units of their own,
on a PostgreSQL server and a toolserver of its own. An install over it stops those three processes and puts their
units aside (/var/backups/hugpy-core). Its database server and its toolserver are left as they are: what they
hold (that Core's history, the Discord store) is its record, and nothing of it is read here yet.

There is no settings file: --host and --port are saved in the settings table of the database, and `system set`
saves one later (the service is started again so that it takes hold).

Every `system` command runs with the host's data directory (HUGPY_DATA_DIR=/var/lib/hugpy; system/__init__.py),
so what it makes and reads is the service's.
"""
from ..imports import (
    EARLIER_UNITS,
    ENDPOINT_FILE,
    HOST_DATA_DIR,
    PACKAGE,
    SERVICE_ACCOUNT,
    SERVICE_BACKUPS,
    SERVICE_UNIT,
    SETTING_KEYS,
    WRAPPER_ENDPOINT_FILE,
    account_ids,
    archive_path,
    argparse,
    ensure_account,
    ensure_folder,
    ensure_secret,
    health_record,
    http_json,
    os,
    read_endpoint,
    read_secret,
    remove_unit,
    service_interpreter,
    system_say,
    systemctl,
    time,
    unit_installed,
    unit_state,
    write_endpoint,
    write_unit,
)
from .. import settings, sql
from ..serve import version

UNIT_TEXT = """[Unit]
Description=hugpy core: the coordinator of the wrappers of many hosts (hugpy-core {version})
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User={account}
Group={account}
# every hugpy tool of this host keeps its folder here: this one's is {home}
Environment=HUGPY_DATA_DIR={data}
Environment=HOME={home}
Environment=PYTHONUNBUFFERED=1
UnsetEnvironment=PYTHONPATH
# a wrapper that connects out holds a poll open, and every wrapper is read on a connection of its own
LimitNOFILE=65536
ExecStart={python} -P -m hugpy_core serve
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
"""


def folder() -> str:
    return settings.home()


def unit_text(python: str) -> str:
    return UNIT_TEXT.format(version=version(), account=SERVICE_ACCOUNT, data=HOST_DATA_DIR, home=folder(), python=python)


def own() -> None:
    """The database is the service account's: a file root made here (saving a setting, making the tables) is
    handed to it."""
    uid, gid = account_ids(SERVICE_ACCOUNT)
    for suffix in ('', '-wal', '-shm'):
        path = settings.database() + suffix
        if os.path.exists(path) and os.stat(path).st_uid != uid:
            os.chown(path, uid, gid)


def endpoint_record() -> dict:
    host, port = settings.address()
    return dict(service=PACKAGE, package=PACKAGE, mode='system', host=host, port=port, url=settings.url(),
                version=version(), settings=settings.database(), token_file=settings.local_key_file())


def save(args) -> list:
    """--host and --port, saved in the settings table. Returns what changed."""
    changes = {key: getattr(args, key) for key in SETTING_KEYS if getattr(args, key, None) not in (None, '')}
    if not changes:
        return []
    changed = settings.save(changes, by='hugpy-core system install')
    own()
    if changed:
        system_say('save', settings.database(), ', '.join(f'{key} = {changes[key]}' for key in changed))
    return changed


def start() -> bool:
    """Enable the unit and start it on what is installed now; wait until Core answers at its door."""
    systemctl('enable', SERVICE_UNIT)
    systemctl('restart', SERVICE_UNIT)
    url, found = settings.url(), None
    for _ in range(60):
        found = health_record(url, timeout=3)
        if found and found.get('package') == PACKAGE:
            system_say('start', SERVICE_UNIT, f"{found.get('status')}: {url}/health")
            return True
        if unit_state(SERVICE_UNIT) == 'failed':
            break
        time.sleep(1)
    other = (f" ({found.get('package') or found.get('service') or 'another program'} answers there: "
             f"sudo hugpy-core system set port N)") if found else ''
    system_say('FAILED', SERVICE_UNIT, f'{url} is not answered by this service{other}: journalctl -u {SERVICE_UNIT}')
    return False


def connect_local() -> None:
    """This host's own wrapper, connected, when it has one and Core has no saved connection yet."""
    wrapper = read_endpoint(WRAPPER_ENDPOINT_FILE).get('url')
    if not wrapper:
        return
    key = read_secret(settings.local_key_file())
    try:
        _, have = http_json(settings.url() + '/v1/wrappers', bearer=key, timeout=10)
        if (have or {}).get('wrappers'):
            return                          # the operator already has connections: none is added unasked
        status, said = http_json(settings.url() + '/api/fleet/workers/connect', dict(url=wrapper, key=''), bearer=key,
                                 timeout=30)
    except OSError as exc:
        system_say('note', wrapper, f"this host's wrapper was not connected ({exc}): hugpy-core connect local")
        return
    if status == 200:
        system_say('connect', wrapper, f"this host's own wrapper, as {said.get('name')}")
    else:
        system_say('note', wrapper, f"this host's wrapper was not connected: {(said or {}).get('error') or f'HTTP {status}'}")


def install(args) -> int:
    if os.geteuid() != 0:
        raise SystemExit('hugpy-core system install changes /: run it as root (sudo hugpy-core system install)')
    print(f'hugpy-core system install ({version()})', flush=True)
    ensure_account(SERVICE_ACCOUNT, folder(), ())
    # before anything else is laid down: an install the account cannot run (a venv in a person's home) stops here
    python = service_interpreter(SERVICE_ACCOUNT, 'hugpy_core')
    ensure_folder(folder(), 0o750, SERVICE_ACCOUNT)
    ensure_secret(settings.api_key_file(), SERVICE_ACCOUNT, what="Core's API key (sudo hugpy-core system key prints it)")
    ensure_secret(settings.local_key_file(), what="the key of this host's own programs: every account of the host reads it",
                  mode=0o644)
    save(args)
    system_say('ok', sql.prepare(), 'the saved connections, the settings table and what is collated')
    own()
    for earlier in EARLIER_UNITS:           # an install over a hugpy-core before 0.5: its other processes go
        if unit_installed(earlier):
            remove_unit(earlier, SERVICE_BACKUPS)
    write_unit(SERVICE_UNIT, unit_text(python))
    write_endpoint(ENDPOINT_FILE, endpoint_record())
    if args.no_start:
        system_say('skip', 'start', '--no-start')
        return 0
    if not start():
        return 1
    if not args.no_local_wrapper:
        connect_local()
    print(closing(), flush=True)
    return 0


def closing() -> str:
    host, port = settings.address()
    lines = ['', f'Core is at {settings.url()} (its data: {folder()}).',
             '  hugpy-core                       how it stands and the wrappers it has',
             '  hugpy-core connect URL --key K   connect a wrapper of another host (there: sudo hugpy-wrapper system key)',
             f'  journalctl -u {SERVICE_UNIT} -f  the service as it runs',
             '  Its door asks a key of every caller. Programs of this host carry the one in',
             f'  {settings.local_key_file()}; another host is given its API key (sudo hugpy-core system key).',
             '  A wrapper enters itself with either:',
             f'    sudo hugpy-wrapper system register --core {settings.url()} --core-key KEY']
    if host in ('127.0.0.1', 'localhost', '::1'):
        lines += ['  It listens on this machine only. For other hosts to reach it:',
                  '    sudo hugpy-core system set host 0.0.0.0']
    return '\n'.join(lines)


def status(_args) -> int:
    print(f'{SERVICE_UNIT:<24} {unit_state(SERVICE_UNIT)}')
    print(f"data      {folder()} ({'present' if os.path.isdir(folder()) else 'not made yet: sudo hugpy-core system install'})")
    print(f"endpoint  {ENDPOINT_FILE} ({'present' if os.path.isfile(ENDPOINT_FILE) else 'missing'})")
    if os.geteuid() != 0 and settings.is_client():
        print('settings  the service\'s own (sudo hugpy-core system status reads them)')
    else:
        for key, row in settings.resolve().items():
            print(f"setting   {key:<6} {row['value']}   [{row['source']}]")
    url = settings.url()
    found = health_record(url, timeout=5, bearer=read_secret(settings.local_key_file()))
    if found and found.get('package') == PACKAGE:
        wrappers = found.get('wrappers') or {}
        print(f"health    {found.get('status')} ({url}; hugpy-core {found.get('version')}); wrappers: {wrappers.get('saved', 0)} saved, "
              f"{wrappers.get('connected', 0)} connected, {wrappers.get('reachable', 0)} reachable"
              + ''.join(f'; {reason}' for reason in found.get('reasons') or []))
        return 0
    print(f"health    {url} is answered by {found.get('package') or found.get('service') or 'another program'}, not by hugpy-core"
          if found else f'health    nothing answers at {url}')
    return 1


def show_key(_args) -> int:
    key = read_secret(settings.api_key_file())
    if not key and os.path.exists(settings.home()) and os.geteuid() != 0:
        raise SystemExit("Core's API key is the service's to read: sudo hugpy-core system key")
    if not key:
        raise SystemExit(f'there is no API key at {settings.api_key_file()}: sudo hugpy-core system install makes it')
    print(key)
    return 0


def set_one(args) -> int:
    """`system set KEY VALUE`: save one setting; the service is started again so that it takes hold at once and
    the record of where it listens says the same. An empty VALUE drops the saved value (its default again)."""
    if os.geteuid() != 0:
        raise SystemExit('run as root (sudo hugpy-core system set KEY VALUE)')
    if args.key not in SETTING_KEYS:
        raise SystemExit(f"{args.key} is not one of: {', '.join(SETTING_KEYS)}")
    value = settings.typed(args.value)
    found = settings.resolve()[args.key]
    if found['value'] == value and found['source'].startswith('saved:'):
        system_say('keep', args.key, f'already saved as {value}')
        return 0                  # a value that only equals the default is saved all the same: a default may change
    settings.save({args.key: value}, by='hugpy-core system set')
    own()
    system_say('save', settings.database(), f"{args.key} = {value if value is not None else 'its default'}")
    write_endpoint(ENDPOINT_FILE, endpoint_record())
    if unit_state(SERVICE_UNIT) == 'active':
        return 0 if start() else 1
    return 0


def uninstall(_args) -> int:
    if os.geteuid() != 0:
        raise SystemExit('run as root')
    if not remove_unit(SERVICE_UNIT, SERVICE_BACKUPS):
        system_say('ok', SERVICE_UNIT, 'not installed')
    if os.path.isfile(ENDPOINT_FILE):
        archive_path(ENDPOINT_FILE, SERVICE_BACKUPS)
        system_say('remove', ENDPOINT_FILE, 'put aside')
    system_say('keep', folder(), 'the database (the saved connections, the settings, what was collated) and the API key are never removed')
    system_say('keep', settings.local_key_file(), "the key of this host's own programs")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog='hugpy-core system')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('install', help='the account, its folder, the key, the database, the unit and the endpoint record; start')
    p.add_argument('--host', metavar='ADDR', help='the address the door listens on (default 127.0.0.1: this machine only)')
    p.add_argument('--port', type=int, metavar='N', help='its port (default 7002)')
    p.add_argument('--no-local-wrapper', action='store_true', help="do not connect this host's own wrapper")
    p.add_argument('--no-start', action='store_true')
    sub.add_parser('status')
    sub.add_parser('key', help="print Core's API key (calls from the network carry it)")
    p = sub.add_parser('set', help='save one setting; the service is started again so it takes hold')
    p.add_argument('key')
    p.add_argument('value', help='an empty string drops the saved value')
    sub.add_parser('uninstall', help='stop and remove the unit (the database and the key are kept)')
    args = parser.parse_args(argv)
    return {'install': install, 'status': status, 'uninstall': uninstall, 'key': show_key, 'set': set_one}[args.command](args)
