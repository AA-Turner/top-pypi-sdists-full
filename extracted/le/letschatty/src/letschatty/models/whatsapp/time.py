from datetime import datetime
from zoneinfo import ZoneInfo


def utc_now() -> datetime:
    return datetime.now(ZoneInfo("UTC"))
