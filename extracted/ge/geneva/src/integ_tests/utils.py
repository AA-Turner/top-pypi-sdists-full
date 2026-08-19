# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
from importlib.metadata import version as distribution_version
from typing import Any

import ray
import ray.exceptions
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

_LOG = logging.getLogger(__name__)

# Default timeout for ray.get() calls in integration tests (seconds)
RAY_GET_TIMEOUT = 90
RAY_GET_RETRIES = 4


def installed_distribution_requirement(distribution: str) -> str:
    """Return an exact pip requirement for the driver's installed version."""
    return f"{distribution}=={distribution_version(distribution)}"


def ray_get_with_retry(
    obj_ref: ray.ObjectRef,
    timeout: float = RAY_GET_TIMEOUT,
    retries: int = RAY_GET_RETRIES,
) -> Any:
    """Call ray.get() with timeout and retries.

    Args:
        obj_ref: The Ray object reference to get.
        timeout: Timeout in seconds for each attempt.
        retries: Number of retry attempts after the first failure.

    Returns:
        The result of ray.get().

    Raises:
        ray.exceptions.GetTimeoutError: If all attempts timeout.
    """

    @retry(
        retry=retry_if_exception_type(ray.exceptions.GetTimeoutError),
        stop=stop_after_attempt(1 + retries),
        wait=wait_fixed(1),
        before_sleep=before_sleep_log(_LOG, logging.WARNING),
        reraise=True,
    )
    def _get_with_retry() -> Any:
        return ray.get(obj_ref, timeout=timeout)

    return _get_with_retry()


def safe_drop_table(conn: Any, table_name: str, **kwargs: Any) -> None:
    """``conn.drop_table`` that tolerates the GEN-543 azure 404.

    ``lance-namespace`` 0.7.7 ``DirectoryNamespace.drop_table`` raises
    ``InternalError: Failed to delete table directory ... _ckp ... 404`` on
    azure when the checkpoint store has been physically purged (sparser
    ``_ckp/`` tree). The data is gone and the test logic already passed;
    only the teardown trips. Remove this helper once GEN-543 lands upstream.

    Extra kwargs (e.g. ``namespace_path``) are forwarded to ``drop_table``.
    """
    try:
        conn.drop_table(table_name, **kwargs)
    except Exception as exc:
        msg = str(exc)
        if "_ckp" in msg and "404" in msg:
            _LOG.warning(
                "drop_table: swallowed GEN-543 azure 404 for %s: %s",
                table_name,
                msg,
            )
            return
        raise
