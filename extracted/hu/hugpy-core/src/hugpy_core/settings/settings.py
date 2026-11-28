"""The settings of hugpy-core: one place they live, read at every use.

A saved value is a row of the ``settings`` table of Core's own database (hugpy_resources read_settings and
write_settings). A setting with no saved value takes ``HUGPY_CORE_<NAME>`` from the process environment or the one
``.env`` file (``~/.hugpy/.env``), else its default in the code (imports/constants.py). There is no settings file.

Everything Core keeps is under one folder (hugpy_resources host_data_dir): the host's, ``/var/lib/hugpy/core``,
once `hugpy-core system install` has made it; else this account's own, ``~/.local/share/hugpy/core``. On a host
where Core is a service that folder is the service account's own (it holds every wrapper's key and the call log,
with what was asked and answered): any other account is a client of the service, and finds its door by the record
the install wrote (ENDPOINT_FILE) and asks it with the key of the host's own programs (local_key_file).
"""
from ..imports import (
    API_KEY_NAME,
    DEFAULTS,
    ENDPOINT_FILE,
    ENV_FILE,
    HOME_NAME,
    HOST_DATA_DIR,
    LOCAL_KEY_FILE,
    LOCAL_KEY_NAME,
    PREFIX,
    SETTING_KEYS,
    env_setting,
    host_data_dir,
    os,
    read_endpoint,
    read_settings,
    write_settings,
)

_HOME = host_data_dir(HOME_NAME)


def home() -> str:
    """Core's own folder: the host's when a system install made it, else this account's own."""
    return _HOME


def is_client() -> bool:
    """Whether this account is a client of the host's Core service: its folder is there and is not this
    account's to read."""
    return os.path.isdir(_HOME) and not os.access(_HOME, os.R_OK | os.X_OK)


def located(path):
    """A path as an absolute path: ~ is the home directory, and one that is not absolute is under Core's folder."""
    path = os.path.expanduser(path)
    return path if os.path.isabs(path) else os.path.normpath(os.path.join(home(), path))


def typed(raw):
    """A value of the environment or the .env file, as the setting's type: a whole number, else text."""
    if not isinstance(raw, str):
        return raw
    text = raw.strip()
    return int(text) if text.isdigit() else (text or None)


def default(name: str):
    """(value, where it comes from) of HUGPY_CORE_<NAME>: the process environment, else the .env file, else the
    default in the code."""
    key = PREFIX + name
    found = env_setting(key, ENV_FILE)
    if found not in (None, ''):
        return typed(found), ('environment:' + key if os.environ.get(key) is not None else 'env-file:' + ENV_FILE)
    return DEFAULTS.get(name), 'default'


def database() -> str:
    """Core's database: its settings table, the saved connections and everything collated."""
    return located(default('DATABASE')[0])


def console_dir() -> str:
    """The folder of the console's built files (HUGPY_CORE_CONSOLE names another than the one Core carries)."""
    return located(default('CONSOLE')[0])


def api_key_file() -> str:
    """Core's API key: what a caller on another host carries. The service account's to read."""
    return os.path.join(home(), API_KEY_NAME)


def is_service_host() -> bool:
    """Whether Core's folder is the host's (the service's), not one account's own."""
    return os.path.dirname(home()) == HOST_DATA_DIR


def local_key_file() -> str:
    """The key of this host's own programs (Core's command line carries it). Where Core is the host's service it
    is a file every account of the host can read; for one account's own Core it is beside the database."""
    return LOCAL_KEY_FILE if is_service_host() else os.path.join(home(), LOCAL_KEY_NAME)


def resolve() -> dict:
    """{key: {value, source}} of every setting as it is in effect now. For a client of the host's service the
    address is the one the service recorded; its saved settings are its own to read."""
    client = is_client()
    saved = {} if client else read_settings(database())
    served = read_endpoint(ENDPOINT_FILE) if client else {}
    out = {}
    for key in SETTING_KEYS:
        if key in saved:
            out[key] = dict(value=saved[key], source='saved:' + database())
        elif served.get(key) is not None:
            out[key] = dict(value=served[key], source='service:' + ENDPOINT_FILE)
        else:
            value, source = default(key.upper())
            out[key] = dict(value=value, source=source)
    return out


def current() -> dict:
    """{key: value} of the settings in effect now."""
    return {key: row['value'] for key, row in resolve().items()}


def address() -> tuple:
    """(host, port): where Core's door listens."""
    values = current()
    return str(values['host']), int(values['port'])


def url() -> str:
    """Core's door as a client on this host reaches it."""
    host, port = address()
    host = '127.0.0.1' if host in ('0.0.0.0', '::', '') else host
    return f"http://{'[' + host + ']' if ':' in host else host}:{port}"


def save(changes: dict, by: str = 'hugpy-core set') -> list:
    """Save settings in the settings table (a value of None drops the saved one: its default applies again).
    Returns the keys that changed."""
    unknown = sorted(set(changes) - set(SETTING_KEYS))
    if unknown:
        raise ValueError(f"not settings of hugpy-core: {', '.join(unknown)} (they are {', '.join(SETTING_KEYS)})")
    os.makedirs(os.path.dirname(database()), exist_ok=True)
    return write_settings(database(), {key: value for key, value in changes.items() if value is not None},
                          remove=tuple(key for key, value in changes.items() if value is None), by=by)
