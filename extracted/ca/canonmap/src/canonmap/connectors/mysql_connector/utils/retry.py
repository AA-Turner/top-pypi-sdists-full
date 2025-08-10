# src/canonmap/connectors/mysql_connector/utils/retry.py

from __future__ import annotations

import time
from typing import Any, Callable

from mysql.connector import errors as mysql_errors


def with_retry(fn: Callable[[], Any], *, max_attempts: int = 5, base_delay: float = 0.5) -> Any:
    attempt = 0
    while True:
        attempt += 1
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            errno = getattr(exc, "errno", None)
            if isinstance(exc, mysql_errors.Error) and errno in {1205, 1213} and attempt < max_attempts:
                delay = base_delay * (2 ** (attempt - 1))
                time.sleep(min(delay, 5.0))
                continue
            raise


