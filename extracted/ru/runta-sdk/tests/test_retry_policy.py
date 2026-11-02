from __future__ import annotations

import asyncio
import ssl
import unittest
from unittest.mock import patch

import httpx

from runta import ApiError, AsyncRunta, Runta
from runta._internal.retry import _delay, retry_async, retry_sync, retryable_http_error


class RetryPolicyTests(unittest.TestCase):
    def test_client_passes_retry_limit_to_transports(self) -> None:
        for client_type in (Runta, AsyncRunta):
            client = client_type(
                endpoint="https://api.test", token="token", retry_max_attempts=4
            )
            try:
                self.assertEqual(client._http.retry_max_attempts, 4)
            finally:
                if isinstance(client, Runta):
                    client.close()
                else:
                    asyncio.run(client.close())

    def test_full_jitter_initial_and_maximum(self) -> None:
        with patch("runta._internal.retry.random.uniform", return_value=0) as random:
            _delay(1, None)
            _delay(16, None)
        self.assertEqual(random.call_args_list[0].args, (0.0, 1.0))
        self.assertEqual(random.call_args_list[1].args, (0.0, 60.0))

    def test_exhaustion_preserves_last_exception_and_logs_attempts(self) -> None:
        error = ApiError("unavailable", status_code=503)
        calls = 0

        def fail(_remaining: float | None) -> None:
            nonlocal calls
            calls += 1
            raise error

        with (
            patch("runta._internal.retry.random.uniform", return_value=0),
            self.assertLogs("runta._internal.retry", level="ERROR") as logs,
            self.assertRaises(ApiError) as raised,
        ):
            retry_sync(
                fail, name="create runtime", attempts=3, retryable=retryable_http_error
            )
        self.assertIs(raised.exception, error)
        self.assertEqual(calls, 3)
        self.assertIn("after 3 attempts", logs.output[0])

    def test_deterministic_http_error_exits_immediately(self) -> None:
        error = ApiError("forbidden", status_code=403)
        calls = 0

        def fail(_remaining: float | None) -> None:
            nonlocal calls
            calls += 1
            raise error

        with self.assertRaises(ApiError) as raised:
            retry_sync(
                fail, name="create runtime", attempts=16, retryable=retryable_http_error
            )
        self.assertIs(raised.exception, error)
        self.assertEqual(calls, 1)

    def test_certificate_error_is_not_transient(self) -> None:
        try:
            raise httpx.ConnectError(
                "certificate failed"
            ) from ssl.SSLCertVerificationError("invalid certificate")
        except httpx.ConnectError as cause:
            try:
                raise ApiError("HTTP request failed") from cause
            except ApiError as error:
                self.assertFalse(retryable_http_error(error))

    def test_client_rejects_invalid_retry_count(self) -> None:
        for client in (Runta, AsyncRunta):
            with self.subTest(client=client.__name__):
                for count in (0, 17, 1.5, True):
                    with self.subTest(count=count):
                        with self.assertRaisesRegex(ValueError, "retry_max_attempts"):
                            client(
                                endpoint="https://api.test",
                                token="token",
                                retry_max_attempts=count,
                            )


class AsyncRetryPolicyTests(unittest.IsolatedAsyncioTestCase):
    async def test_exhaustion_preserves_last_exception(self) -> None:
        error = ApiError("unavailable", status_code=503)
        calls = 0

        async def fail(_remaining: float | None) -> None:
            nonlocal calls
            calls += 1
            raise error

        with (
            patch("runta._internal.retry.random.uniform", return_value=0),
            self.assertLogs("runta._internal.retry", level="ERROR") as logs,
            self.assertRaises(ApiError) as raised,
        ):
            await retry_async(
                fail, name="patch runtime", attempts=2, retryable=retryable_http_error
            )
        self.assertIs(raised.exception, error)
        self.assertEqual(calls, 2)
        self.assertIn("after 2 attempts", logs.output[0])
