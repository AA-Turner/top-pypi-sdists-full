import asyncio
from datetime import datetime

from arpakitlib.ar_datetime_util import now_dt
from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_type_util import raise_if_none
from project.core.settings import get_cached_settings


def setup_logging():
    setup_normal_logging(log_filepath=get_cached_settings().log_filepath)


def now_local_dt() -> datetime:
    raise_if_none(get_cached_settings().local_timezone_as_pytz)
    return now_dt(tz=get_cached_settings().local_timezone_as_pytz)


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
