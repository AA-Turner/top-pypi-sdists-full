from datetime import datetime

from arpakitlib.ar_datetime_util import now_dt
from arpakitlib.ar_type_util import raise_if_none
from project.core.settings import get_cached_settings


def now_local_dt() -> datetime:
    raise_if_none(get_cached_settings().local_timezone_as_pytz)
    return now_dt(tz=get_cached_settings().local_timezone_as_pytz)
