"""Mode detection, the app API client and the credentials helpers of the local kernel."""

import os
import unittest
from datetime import datetime, timedelta, timezone
from unittest import mock

from sagemaker_studio import local_kernel
from sagemaker_studio._test.unit.local_app_fixture import (
    FakeApp,
    LocalKernelTestCase,
    lakehouse_record,
    s3_record,
)
from sagemaker_studio.exceptions import LocalAppError, LocalAppUnavailableError
from sagemaker_studio.local_kernel import (
    AppApiClient,
    RuntimeMode,
    configure_local_kernel,
    current_context,
    expires_soon,
    is_local_kernel,
    parse_expiration,
    refreshable_credentials,
    reset_local_kernel,
    runtime_mode,
)


class ModeDetectionTest(unittest.TestCase):
    def setUp(self):
        reset_local_kernel()

    def tearDown(self):
        reset_local_kernel()

    def test_without_the_app_url_the_sdk_is_remote(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertFalse(is_local_kernel())
            context = current_context()
            self.assertIs(runtime_mode(), RuntimeMode.REMOTE)
        self.assertIs(context.mode, RuntimeMode.REMOTE)
        self.assertIn("AWS_NOTEBOOK_APP_URL", context.reason)
        self.assertEqual(context.describe()["mode"], "REMOTE")

    def test_the_app_url_makes_a_local_kernel_without_any_call(self):
        env = {"AWS_NOTEBOOK_APP_URL": "http://127.0.0.1:53211/", "AWS_NOTEBOOK_APP_TOKEN": "tok"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertTrue(is_local_kernel())
            context = current_context()
            self.assertIs(runtime_mode(), RuntimeMode.LOCAL)
        self.assertIs(context.mode, RuntimeMode.LOCAL)
        self.assertEqual(context.app_url, "http://127.0.0.1:53211")
        self.assertIsNone(context.signed_in)  # nothing has asked for credentials yet
        self.assertNotIn("tok", repr(context))

    def test_a_blank_app_url_is_remote(self):
        with mock.patch.dict(os.environ, {"AWS_NOTEBOOK_APP_URL": "   "}, clear=True):
            self.assertFalse(is_local_kernel())

    def test_the_decision_is_made_once_until_reset(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertFalse(is_local_kernel())
            os.environ["AWS_NOTEBOOK_APP_URL"] = "http://127.0.0.1:1"
            self.assertFalse(is_local_kernel())  # still the first decision
            reset_local_kernel()
            self.assertTrue(is_local_kernel())

    def test_configure_local_kernel_overrides_the_environment(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            context = configure_local_kernel("http://localhost:9", "t")
            self.assertIs(context.mode, RuntimeMode.LOCAL)
            self.assertTrue(is_local_kernel())
            reset_local_kernel()
            self.assertFalse(is_local_kernel())

    def test_reset_listeners_run_on_configure_and_reset(self):
        calls = []
        local_kernel.add_reset_listener(lambda: calls.append("x"))
        try:
            configure_local_kernel("http://127.0.0.1:9", "t")
            reset_local_kernel()
        finally:
            local_kernel._reset_listeners.remove(local_kernel._reset_listeners[-1])
        self.assertEqual(calls, ["x", "x"])

    def test_a_failing_reset_listener_is_logged_and_does_not_stop_the_others(self):
        calls = []

        def broken():
            raise RuntimeError("listener broke")

        def working():
            calls.append("ok")

        local_kernel.add_reset_listener(broken)
        local_kernel.add_reset_listener(broken)  # registering twice keeps one entry
        local_kernel.add_reset_listener(working)
        try:
            self.assertEqual(local_kernel._reset_listeners.count(broken), 1)
            with self.assertLogs("sagemaker_studio.local_kernel", level="WARNING") as logs:
                reset_local_kernel()
        finally:
            local_kernel._reset_listeners.remove(broken)
            local_kernel._reset_listeners.remove(working)
        self.assertEqual(calls, ["ok"])
        self.assertIn("reset listener failed", logs.output[0])
        self.assertIn("listener broke", logs.output[0])  # the traceback is kept


class AppApiClientTest(unittest.TestCase):
    """The HTTP client against a server behaving like the app's callback listener."""

    def setUp(self):
        self.app = FakeApp()
        self.app.add(s3_record())

    def tearDown(self):
        self.app.close()

    def client(self, **kwargs) -> AppApiClient:
        return AppApiClient(self.app.url, self.app.token, **kwargs)

    def test_get_connection_posts_the_datazone_shaped_request_with_the_bearer_token(self):
        row = self.client().get_connection("s3raw", with_secret=True)
        self.assertEqual(row["name"], "raw")
        self.assertEqual(row["connectionCredentials"]["accessKeyId"], "AKIA_TEST")
        operation, body, authorization = self.app.calls[0]
        self.assertEqual(operation, "connections/get")
        self.assertEqual(body, {"identifier": "s3raw", "withSecret": True})
        self.assertEqual(authorization, f"Bearer {self.app.token}")

    def test_without_with_secret_the_row_has_no_credentials(self):
        row = self.client().get_connection("s3raw", with_secret=False)
        self.assertNotIn("connectionCredentials", row)
        self.assertEqual(self.app.calls[0][1]["withSecret"], False)

    def test_list_connections_posts_the_filter_and_reads_the_bare_array(self):
        self.app.add(lakehouse_record())
        rows = self.client().list_connections()
        self.assertEqual(sorted(r["connectionId"] for r in rows), ["lakehouse1", "s3raw"])
        self.assertTrue(all("connectionCredentials" not in r for r in rows))
        operation, body, authorization = self.app.calls[0]
        self.assertEqual((operation, body), ("connections/list", {}))
        self.assertEqual(authorization, f"Bearer {self.app.token}")
        self.assertEqual(
            [r["connectionId"] for r in self.client().list_connections("S3")], ["s3raw"]
        )
        self.assertEqual(self.app.calls[-1][1], {"type": "S3"})

    def test_a_list_answered_with_an_object_or_junk_rows_is_unavailable(self):
        for body in (b'{"items": []}', b"[1, 2]"):
            self.app.raw_list_response = (200, body, "application/json")
            with self.assertRaises(LocalAppUnavailableError) as raised:
                self.client().list_connections()
            self.assertIn("not an array of objects", str(raised.exception))

    def test_a_list_refused_with_an_envelope_keeps_the_apps_code(self):
        self.app.raw_list_response = (
            403,
            b'{"error": {"code": "AccessDeniedException", "message": "no"}}',
            "application/json",
        )
        with self.assertRaises(LocalAppError) as raised:
            self.client().list_connections()
        self.assertEqual(
            (raised.exception.code, raised.exception.status), ("AccessDeniedException", 403)
        )

    def test_signed_out_is_access_denied_with_the_apps_message(self):
        self.app.sign_out()
        with self.assertRaises(LocalAppError) as raised:
            self.client().get_connection("s3raw")
        self.assertEqual(raised.exception.code, "AccessDeniedException")
        self.assertEqual(raised.exception.status, 403)
        self.assertIn("Sign in to AWS", raised.exception.detail)
        self.assertIn("connections/get", str(raised.exception))

    def test_unknown_connection_is_resource_not_found(self):
        with self.assertRaises(LocalAppError) as raised:
            self.client().get_connection("nosuchid")
        self.assertEqual(
            (raised.exception.code, raised.exception.status), ("ResourceNotFoundException", 404)
        )

    def test_a_wrong_token_is_unrecognized_client(self):
        with self.assertRaises(LocalAppError) as raised:
            AppApiClient(self.app.url, "wrong").get_connection("s3raw")
        self.assertEqual(
            (raised.exception.code, raised.exception.status), ("UnrecognizedClientException", 401)
        )

    def test_a_missing_token_fails_before_any_request(self):
        for token in (None, "   "):  # unset, or blank: no token
            with self.assertRaises(LocalAppUnavailableError) as raised:
                AppApiClient(self.app.url, token).get_connection("s3raw")
            self.assertIn("AWS_NOTEBOOK_APP_TOKEN", str(raised.exception))
        self.assertEqual(self.app.calls, [])

    def test_an_empty_url_fails_before_any_request(self):
        for url in ("", "   ", None):
            with self.assertRaises(LocalAppUnavailableError) as raised:
                AppApiClient(url, "t").get_connection("s3raw")
            self.assertIn("AWS_NOTEBOOK_APP_URL is empty", str(raised.exception))
        self.assertEqual(self.app.calls, [])

    def test_a_non_loopback_url_fails_before_any_request(self):
        for url in ("http://example.com:53211", "file:///tmp/x", "ftp://127.0.0.1:1"):
            with self.assertRaises(LocalAppUnavailableError):
                AppApiClient(url, "t").get_connection("s3raw")
        self.assertEqual(self.app.calls, [])

    def test_a_non_json_error_body_is_unavailable_not_an_envelope(self):
        self.app.raw_responses["broken"] = (500, b"oops", "text/plain")
        with self.assertRaises(LocalAppUnavailableError) as raised:
            self.client().get_connection("broken")
        self.assertIn("HTTP 500", str(raised.exception))

    def test_a_json_error_without_an_envelope_is_unavailable(self):
        self.app.raw_responses["odd"] = (500, b'{"message": "no envelope"}', "application/json")
        with self.assertRaises(LocalAppUnavailableError):
            self.client().get_connection("odd")

    def test_an_error_whose_body_cannot_be_read_is_unavailable(self):
        import urllib.error

        class Unreadable:
            """The response body of an error whose connection dropped before it was read."""

            def read(self, *args):
                raise OSError("connection reset")

            def close(self):
                pass

        error = urllib.error.HTTPError(
            f"{self.app.url}/api/connections/get", 502, "Bad Gateway", {}, Unreadable()
        )
        client = self.client()
        with mock.patch.object(client._opener, "open", side_effect=error):
            with self.assertRaises(LocalAppUnavailableError) as raised:
                client.get_connection("s3raw")
        self.assertIn("HTTP 502 without an error envelope", str(raised.exception))

    def test_a_200_with_an_error_envelope_is_still_an_error(self):
        self.app.raw_responses["weird"] = (
            200,
            b'{"error": {"code": "Odd", "message": "m"}}',
            "application/json",
        )
        with self.assertRaises(LocalAppError) as raised:
            self.client().get_connection("weird")
        self.assertEqual(raised.exception.code, "Odd")

    def test_a_200_that_is_not_a_json_object_is_unavailable(self):
        self.app.raw_responses["list"] = (200, b"[1, 2]", "application/json")
        with self.assertRaises(LocalAppUnavailableError):
            self.client().get_connection("list")

    def test_an_unreachable_app_is_unavailable(self):
        port = self.app._server.server_port
        self.app.close()
        try:
            with self.assertRaises(LocalAppUnavailableError) as raised:
                AppApiClient(f"http://127.0.0.1:{port}", "t", timeout=1).get_connection("s3raw")
            self.assertIn("Could not reach the AWS Notebook app", str(raised.exception))
        finally:
            self.app = FakeApp()  # so tearDown has something to close

    def test_a_connection_dropped_mid_body_is_unavailable(self):
        import http.client

        client = AppApiClient(self.app.url, self.app.token)
        with mock.patch.object(
            client._opener, "open", side_effect=http.client.IncompleteRead(b'{"conn')
        ):
            with self.assertRaises(LocalAppUnavailableError) as raised:
                client.get_connection("s3raw")
        self.assertIn("Could not reach the AWS Notebook app", str(raised.exception))
        self.assertIsInstance(raised.exception.__cause__, http.client.IncompleteRead)

    def test_proxy_environment_is_ignored(self):
        proxies = {"HTTP_PROXY": "http://127.0.0.1:9", "http_proxy": "http://127.0.0.1:9"}
        with mock.patch.dict(os.environ, proxies):
            self.assertEqual(self.client().get_connection("s3raw")["name"], "raw")

    def test_a_redirect_is_refused_and_the_token_never_leaves_the_app(self):
        # urllib's default redirect handler would follow a 3xx with a new request for wherever
        # Location points, copying the request headers, the bearer token among them, without
        # checking that host. The client refuses redirects instead, whatever the status.
        elsewhere = FakeApp(token="another-token")
        try:
            for status in (301, 302, 303, 307, 308):
                self.app.redirects["s3raw"] = (status, f"{elsewhere.url}/api/connections/get")
                with self.assertRaises(LocalAppUnavailableError) as raised:
                    self.client().get_connection("s3raw")
                self.assertIn(f"HTTP {status} with a redirect", str(raised.exception))
                self.assertIn("connections/get", str(raised.exception))
            self.assertEqual(len(self.app.get_calls("s3raw")), 5)  # the app was asked each time
            self.assertEqual(elsewhere.requests, [])  # nothing, with or without the token, went on
        finally:
            elsewhere.close()

    def test_from_env_reads_the_two_variables(self):
        with mock.patch.dict(os.environ, self.app.env(), clear=True):
            client = AppApiClient.from_env()
        self.assertIsNotNone(client)
        self.assertEqual(client.url, self.app.url)
        self.assertEqual(client.get_connection("s3raw")["name"], "raw")
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(AppApiClient.from_env())

    def test_the_token_never_appears_in_repr(self):
        self.assertNotIn(self.app.token, repr(self.client()))
        self.assertIn("token=set", repr(self.client()))


class ExpirationTest(unittest.TestCase):
    def test_parse_accepts_the_apps_z_suffix_offsets_naive_and_datetimes(self):
        z = parse_expiration("2026-10-06T21:00:00.000Z")
        self.assertEqual(z, datetime(2026, 10, 6, 21, 0, tzinfo=timezone.utc))
        offset = parse_expiration("2026-10-06T23:00:00+02:00")
        self.assertEqual(offset, z)
        naive = parse_expiration("2026-10-06T21:00:00")
        self.assertEqual(naive, z)  # naive is read as UTC
        self.assertEqual(parse_expiration(datetime(2026, 10, 6, 21, 0, tzinfo=timezone.utc)), z)
        self.assertIsNone(parse_expiration(None))
        self.assertIsNone(parse_expiration(""))
        self.assertIsNone(parse_expiration("not a date"))

    def test_fractional_seconds_of_any_length_are_read(self):
        # The app's records carry nanoseconds (DataZone's wire format); Python 3.10's
        # fromisoformat accepts exactly 3 or 6 digits, so they are cut (or padded) to microseconds
        # instead of being dropped as unreadable, which would silently disable the refresh.
        nanos = parse_expiration("2026-10-12T18:09:38.848541480Z")
        self.assertEqual(nanos, datetime(2026, 10, 12, 18, 9, 38, 848541, tzinfo=timezone.utc))
        four = parse_expiration("2026-10-12T18:09:38.8485+02:00")
        self.assertEqual(four, datetime(2026, 10, 12, 16, 9, 38, 848500, tzinfo=timezone.utc))
        comma = parse_expiration("2026-10-12T18:09:38,5Z")
        self.assertEqual(comma, datetime(2026, 10, 12, 18, 9, 38, 500000, tzinfo=timezone.utc))
        soon = (datetime.now(timezone.utc) + timedelta(minutes=1)).strftime(
            "%Y-%m-%dT%H:%M:%S.123456789Z"
        )
        self.assertTrue(expires_soon(soon))

    def test_expires_soon_uses_the_refresh_window(self):
        soon = datetime.now(timezone.utc) + timedelta(minutes=2)
        later = datetime.now(timezone.utc) + timedelta(minutes=30)
        self.assertTrue(expires_soon(soon))
        self.assertFalse(expires_soon(later))
        self.assertTrue(
            expires_soon(datetime.now(timezone.utc) - timedelta(minutes=1), timedelta(0))
        )
        self.assertFalse(expires_soon(None))


class _Creds:
    def __init__(self, key, minutes):
        self.access_key_id = key
        self.secret_access_key = f"{key}-s"
        self.session_token = f"{key}-t"
        self.expiration = datetime.now(timezone.utc) + timedelta(minutes=minutes)


class RefreshableCredentialsTest(unittest.TestCase):
    def test_fetches_once_now_and_again_when_about_to_expire(self):
        answers = [_Creds("FIRST", minutes=1), _Creds("SECOND", minutes=60)]
        calls = []

        def fetch():
            calls.append(1)
            return answers.pop(0)

        creds = refreshable_credentials(fetch)
        self.assertEqual(len(calls), 1)  # fetched at build time
        frozen = creds.get_frozen_credentials()  # within botocore's refresh window: fetched again
        self.assertEqual((frozen.access_key, frozen.token), ("SECOND", "SECOND-t"))
        self.assertEqual(len(calls), 2)
        creds.get_frozen_credentials()
        self.assertEqual(len(calls), 2)  # fresh for an hour: no third fetch

    def test_credentials_without_expiration_get_the_default_lifetime(self):
        class NoExpiry(_Creds):
            def __init__(self):
                super().__init__("K", 60)
                self.expiration = None

        creds = refreshable_credentials(lambda: NoExpiry())
        self.assertEqual(creds.get_frozen_credentials().access_key, "K")

    def test_a_fetch_without_keys_raises(self):
        class Empty:
            access_key_id = None
            secret_access_key = None
            session_token = None
            expiration = None

        with self.assertRaises(RuntimeError):
            refreshable_credentials(lambda: Empty())


class KernelContextTest(LocalKernelTestCase):
    def test_context_reports_the_app_and_the_sign_in_observation(self):
        context = current_context()
        self.assertIs(context.mode, RuntimeMode.LOCAL)
        self.assertEqual(context.app_url, self.app.url)
        self.assertIsNone(context.signed_in)
        self.kernel.observe_credentials(False, "Sign in.")
        self.assertEqual(
            (current_context().signed_in, current_context().signed_in_detail), (False, "Sign in.")
        )
        self.kernel.observe_credentials(True)
        self.assertEqual(
            (current_context().signed_in, current_context().signed_in_detail), (True, "")
        )


if __name__ == "__main__":
    unittest.main()
