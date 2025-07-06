from calendar import timegm
from datetime import datetime, timezone


def datetime_to_epoch(dt: datetime) -> int:
    return timegm(dt.utctimetuple())


def aware_utcnow(use_tz=False) -> datetime:
    dt = datetime.now(tz=timezone.utc)
    if not use_tz:
        dt = dt.replace(tzinfo=None)

    return dt


def get_utc_now() -> int:
    return datetime_to_epoch(aware_utcnow())
