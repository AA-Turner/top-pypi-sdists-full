# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Retryability classification for object-store / namespace errors."""

import pytest
from lance_namespace.errors import (
    ServiceUnavailableError,
    TableNotFoundError,
    ThrottlingError,
)

from geneva.utils.object_store_retry import is_retryable_object_store_error


class _StatusCodeError(RuntimeError):
    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code


def _with_cause(outer: BaseException, inner: BaseException) -> BaseException:
    outer.__cause__ = inner
    return outer


@pytest.mark.parametrize(
    ("exc", "expected"),
    [
        pytest.param(
            TableNotFoundError("Table not found: table id 'tbl'"),
            False,
            id="not-found-only",
        ),
        pytest.param(
            TableNotFoundError(
                "Table not found: table id 'tbl': 503 Service Unavailable ServerBusy"
            ),
            True,
            id="not-found-plus-503-serverbusy",
        ),
        pytest.param(
            ValueError("table not found; too many requests, please slow down"),
            True,
            id="not-found-plus-429-marker",
        ),
        pytest.param(
            _with_cause(
                ValueError("table not found"),
                _StatusCodeError("object store overloaded", 503),
            ),
            True,
            id="not-found-outer-503-inner",
        ),
        pytest.param(
            _StatusCodeError("service unavailable 503 serverbusy", 401),
            False,
            id="401-status-beats-throttle",
        ),
        pytest.param(
            _StatusCodeError("table not found 503 serverbusy", 403),
            False,
            id="403-status-beats-throttle-and-not-found",
        ),
        pytest.param(
            ValueError("access denied: 503 service unavailable"),
            False,
            id="auth-marker-beats-throttle",
        ),
        pytest.param(
            TableNotFoundError("Column 'request_timeout' not found"),
            False,
            id="not-found-with-timeout-substring-not-retryable",
        ),
        pytest.param(
            ValueError("table not found; connection reset by peer"),
            False,
            id="not-found-plus-generic-marker-not-retryable",
        ),
        pytest.param(
            ValueError("table not found; the server is busy, retry later"),
            True,
            id="not-found-plus-throttle-marker-retryable",
        ),
        pytest.param(
            _StatusCodeError("rate limited", 429),
            False,
            id="429-without-object-store-context",
        ),
        pytest.param(ThrottlingError("slow down"), True, id="typed-throttling"),
        pytest.param(
            ServiceUnavailableError("unavailable"),
            True,
            id="typed-service-unavailable",
        ),
    ],
)
def test_predicate_classification(exc: BaseException, expected: bool) -> None:
    assert is_retryable_object_store_error(exc) is expected
