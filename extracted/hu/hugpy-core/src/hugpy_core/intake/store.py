"""Database boundary shared by the independent collector and HTTP readers."""
from abstract_database import PgStateStore

from hugpy_core.imports.functions import core_dsn


def store():
    return PgStateStore(core_dsn(), bootstrap=False, connect_timeout=5)


def workers():
    return [row[0] for row in store().sql("SELECT payload FROM worker_presence ORDER BY worker")]
