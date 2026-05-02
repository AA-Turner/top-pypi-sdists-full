import time
import pytest
import logging
from acceldata_sdk.errors import APIError

LOGGER = logging.getLogger(__name__)


def retry_operation(operation, max_retries, retry_interval, *args, **kwargs):
    retry_count = 0
    LOGGER.info("Retry count: %s", retry_count)
    while retry_count < max_retries+1:
        try:
            LOGGER.info("Executing operation...")
            result = operation(*args, **kwargs)
            LOGGER.info(f"Operation result: {result}")
            return result
        except Exception as e:
            LOGGER.error(str(e))

            # ✅ Non-retriable / acceptable API states → rethrow
            if isinstance(e, APIError):
                raise

            retry_count += 1
            if retry_count < max_retries:
                time.sleep(retry_interval)
            else:
                pytest.fail("Operation failed after multiple retries.")
    return None
