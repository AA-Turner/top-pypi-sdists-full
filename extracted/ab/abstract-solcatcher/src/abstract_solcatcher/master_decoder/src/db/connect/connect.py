from contextlib import contextmanager
import threading
import psycopg2
from psycopg2.pool import SimpleConnectionPool
ENV_PATH = '/home/flerb/.env'
from abstract_utilities import get_env_value, eatAll
CRED_VALUES = {
    "postgres":{
        "prefix":'SOLCATCHER_POSTGRESQL',"defaults":{
        "host":'localhost',
        "port":'1234',
        "user":'solcatcher',
        "name":'solcatcher',
        "password":'solcatcher'
    }
        },
    "amqp":{
        "prefix":'SOLCATCHER_AMQP',
        "defaults":{
            "host":'localhost',
            "port":'1234',
            "user":'solcatcher',
            "name":'solcatcher',
            "password":'solcatcher'
            }
        }
    }


# ─────────────────────────────────────────────────────────────
# ENV / CREDENTIAL UTILITIES
# ─────────────────────────────────────────────────────────────

def get_env_val(key, path=None):
    path = path or ENV_PATH
    return get_env_value(key=key, path=path)


def if_list_get_single(obj):
    while isinstance(obj, list) and len(obj) == 1:
        obj = obj[0]
    return obj


def update_defaults(dict_obj, defaults_obj):
    if not defaults_obj:
        return dict_obj
    nu = {}
    for key, value in dict_obj.items():
        nu[key] = value if value is not None else defaults_obj.get(key)
    return nu


def get_creds(prefix, path=None, defaults=None):
    defaults = defaults or {}
    prefix = eatAll(prefix.upper(), ['_'])

    cred_keys = [
        "host",
        "port",
        "user",
        {"dbname": ["name", "dbname"]},
        {"password": ["password", "pass"]},
    ]

    creds = {}
    for key in cred_keys:
        if isinstance(key, dict):
            for final_key, variants in key.items():
                for variant in variants:
                    env_key = f"{prefix}_{variant.upper()}"
                    val = get_env_val(env_key, path=path)
                    if val is not None:
                        creds[final_key] = val
                        break
        else:
            env_key = f"{prefix}_{key.upper()}"
            creds[key] = get_env_val(env_key, path)

    return update_defaults(creds, defaults)


def get_credentials(typ="postgres", path=None, prefix=None, defaults=None):
    values = {
        "prefix": prefix,
        "defaults": defaults,
    }
    values = update_defaults(CRED_VALUES.get(typ), values)
    return get_creds(path=path, **values)


def create_db_url(prefix=None, user=None, host=None, dbname=None, port=None, password=None, **_):
    prefix = prefix or "postgresql"
    if prefix == "postgres":
        prefix = "postgresql"
    return f"{prefix}://{user}:{password}@{host}:{port}/{dbname}"


def get_db_url(typ="postgres", path=None, prefix=None):
    creds = get_credentials(typ=typ, path=path, prefix=prefix)
    return create_db_url(prefix=typ, **creds)


# ─────────────────────────────────────────────────────────────
# CONNECTION POOL (SAFE, REUSED, BOUNDED)
# ─────────────────────────────────────────────────────────────

_POOL = None
_POOL_LOCK = threading.Lock()


def _init_pool(typ="postgres", path=None, prefix=None, minconn=1, maxconn=10):
    creds = get_credentials(typ=typ, path=path, prefix=prefix)
    return SimpleConnectionPool(
        minconn=minconn,
        maxconn=maxconn,
        **creds,
    )


def get_pool(typ="postgres", path=None, prefix=None, minconn=1, maxconn=10):
    global _POOL
    if _POOL is None:
        with _POOL_LOCK:
            if _POOL is None:
                _POOL = _init_pool(
                    typ=typ,
                    path=path,
                    prefix=prefix,
                    minconn=minconn,
                    maxconn=maxconn,
                )
    return _POOL


def get_connection(typ="postgres", path=None, prefix=None):
    """
    Acquire a pooled database connection.
    MUST be released via release_connection().
    """
    return get_pool(typ=typ, path=path, prefix=prefix).getconn()


def release_connection(conn):
    if conn is not None:
        get_pool().putconn(conn)


@contextmanager
def db_connection(typ="postgres", path=None, prefix=None):
    """
    Safe context-managed DB connection.
    """
    conn = get_connection(typ=typ, path=path, prefix=prefix)
    try:
        yield conn
    finally:
        release_connection(conn)
@contextmanager
def db_conn():
    conn = get_connection()
    try:
        yield conn
    finally:
        release_connection(conn)
