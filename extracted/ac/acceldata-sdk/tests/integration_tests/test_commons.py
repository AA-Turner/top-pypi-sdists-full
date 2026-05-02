import logging
import time

LOGGER = logging.getLogger(__name__)


def retry_operation(operation, max_retries, retry_interval, *args, **kwargs):
    retry_count = 0
    max_attempts = max_retries + 1  # ensure at least one execution
    last_exception = None

    while retry_count < max_attempts:
        try:
            LOGGER.info("Attempt %s of %s", retry_count + 1, max_attempts)
            result = operation(*args, **kwargs)

            if result is None:
                raise ValueError("Operation returned None")

            return result

        except Exception as e:
            last_exception = e
            LOGGER.error("Attempt %s failed: %s", retry_count + 1, e)
            retry_count += 1

            if retry_count < max_attempts:
                LOGGER.info("Retrying in %s seconds...", retry_interval)
                time.sleep(retry_interval)


    raise last_exception
