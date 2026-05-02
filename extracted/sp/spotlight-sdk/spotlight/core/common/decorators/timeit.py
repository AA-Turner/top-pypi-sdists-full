import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TimeProfile:
    start_time: float
    end_time: float
    duration: float


def timeit(fxn, *, return_time_profile: bool = False):
    def timed(*args, **kwargs):
        start = time.time()
        result = fxn(*args, **kwargs)
        end = time.time()

        time_profile = TimeProfile(
            start_time=start, end_time=end, duration=(end - start)
        )
        logger.debug(f"func:{fxn.__name__} args:[{args}, {kwargs}]: {time_profile}")

        if return_time_profile:
            return result, time_profile
        return result

    return timed
