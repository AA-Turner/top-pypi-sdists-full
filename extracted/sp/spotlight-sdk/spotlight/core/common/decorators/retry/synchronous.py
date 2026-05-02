import random
import time


def exponential_backoff_retry(func, max_retries=5, delay=1):
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < max_retries - 1:
                    sleep_time = delay * (2**attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
                else:
                    raise e

    return wrapper
