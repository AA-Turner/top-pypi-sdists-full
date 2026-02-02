"""Corvic sqlalchemy functions."""

import datetime

from corvic.orm.func.utc_func import UTCNow as _UTCNow
from corvic.orm.func.uuid_func import UUIDFunction as _UUIDFunction


def utc_now(offset: datetime.timedelta | None = None):
    """Sqlalchemy function returning utc now."""
    return _UTCNow(offset=offset)


def gen_uuid():
    """Sqlalchemy function returning a random uuid."""
    return _UUIDFunction()


__all__ = ["utc_now", "gen_uuid"]
