# Copyright 2026 Canonical Ltd.

# This file is part of launchpadlib.
#
# launchpadlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# launchpadlib is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with launchpadlib. If not, see <http://www.gnu.org/licenses/>.

"""Tests for hardware-bound OAuth grants and the tokens minted from them."""

import http.client
import importlib.util
import io
import json
import os
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlencode

import httplib2
from lazr.restfulclient._browser import RestfulHttp
from lazr.restfulclient.authorize.oauth import Consumer
from lazr.restfulclient.errors import HTTPError

from launchpadlib import fido2compat
from launchpadlib.hardware import HardwareKeyClient
from launchpadlib.hardware_tokens import (
    HardwareTokenAuthorizationEngine,
    HardwareTokenCredentials,
    HardwareTokenError,
    HardwareTokenGrant,
    HardwareTokenGrantError,
    HardwareTokenHttp,
    HttpMintingTransport,
    KeyringHardwareTokenCredentialStore,
    MemoryHardwareTokenCredentialStore,
    MintedAccessToken,
    MintingChallenge,
    UnencryptedFileHardwareTokenCredentialStore,
)
from launchpadlib.launchpad import Launchpad
from launchpadlib.testing.helpers import (
    OfflineLaunchpad,
    QuietInteraction,
    WebserviceResponse,
)


requires_fido2 = unittest.skipUnless(
    importlib.util.find_spec("fido2") is not None,
    "The optional fido2 dependency is not installed.",
)


class TestIssueHardwareBoundOAuthToken(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.launchpad = OfflineLaunchpad()
        self.person = Mock()
        self.authenticator = Mock()
        self.launchpad.load = Mock(return_value=self.person)
        self.person.issueHardwareBoundOAuthToken.return_value = {
            "oauth_token": "refresh-key",
            "oauth_token_secret": "refresh-secret",
        }

    def issue(self, **kwargs):
        return self.launchpad.issue_hardware_bound_oauth_token(
            consumer_key="hardware-client",
            authenticator=self.authenticator,
            permission="Change Anything",
            **kwargs,
        )

    def test_issue_calls_generated_operation(self):
        result = self.issue()

        self.assertEqual(
            {
                "oauth_token": "refresh-key",
                "oauth_token_secret": "refresh-secret",
            },
            result,
        )
        self.launchpad.load.assert_called_once_with(
            self.launchpad.me.self_link
        )
        self.person.issueHardwareBoundOAuthToken.assert_called_once_with(
            consumer_key="hardware-client",
            authenticator=self.authenticator,
            permission="Change Anything",
            context=None,
            date_expires=None,
        )
        self.launchpad.connection.request.assert_not_called()

    def test_issue_rejects_resource_representation(self):
        self.person.issueHardwareBoundOAuthToken.return_value = {
            "name": "alice",
            "self_link": self.launchpad.me.self_link,
        }
        with self.assertRaisesRegex(
            HardwareTokenError, "malformed refresh-grant response"
        ):
            self.issue()

    def test_issue_rejects_non_dictionary_response(self):
        self.person.issueHardwareBoundOAuthToken.return_value = None
        with self.assertRaisesRegex(
            HardwareTokenError, "malformed refresh-grant response"
        ):
            self.issue()

    def test_issue_passes_optional_parameters(self):
        expiry = datetime(2026, 10, 1, 12, 30, tzinfo=timezone.utc)

        self.issue(context="ubuntu/hello", date_expires=expiry)

        self.person.issueHardwareBoundOAuthToken.assert_called_once_with(
            consumer_key="hardware-client",
            authenticator=self.authenticator,
            permission="Change Anything",
            context="ubuntu/hello",
            date_expires=expiry,
        )

    def test_issue_rejects_naive_expiry(self):
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            self.issue(date_expires=datetime(2026, 10, 1))
        self.launchpad.load.assert_not_called()

    def test_issue_discards_unrelated_fields(self):
        self.person.issueHardwareBoundOAuthToken.return_value["extra"] = "data"

        result = self.issue()

        self.assertEqual({"oauth_token", "oauth_token_secret"}, set(result))

    def test_issue_propagates_http_error(self):
        self.person.issueHardwareBoundOAuthToken.side_effect = HTTPError(
            WebserviceResponse(status=400), b"Invalid authenticator."
        )
        with self.assertRaises(HTTPError):
            self.issue()


class TestRevokeHardwareBoundOAuthToken(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.launchpad = OfflineLaunchpad()
        self.person = Mock()
        self.launchpad.load = Mock(return_value=self.person)

    def test_revoke_calls_write_operation(self):
        grant_key = "refresh-key"
        self.assertIsNone(
            self.launchpad.revoke_hardware_bound_oauth_token(grant_key)
        )

        self.launchpad.load.assert_called_once_with(
            self.launchpad.me.self_link
        )
        self.person.revokeHardwareBoundOAuthToken.assert_called_once_with(
            token_key=grant_key
        )
        self.launchpad.connection.request.assert_not_called()

    def test_revoke_propagates_http_error(self):
        self.person.revokeHardwareBoundOAuthToken.side_effect = HTTPError(
            WebserviceResponse(status=400),
            b"No such hardware-bound OAuth token.",
        )
        with self.assertRaises(HTTPError):
            self.launchpad.revoke_hardware_bound_oauth_token("refresh-key")


API_URI = "https://api.launchpad.test/devel/"


def raw_response(status, body=b"", **headers):
    headers["Content-Length"] = str(len(body))
    lines = ["HTTP/1.1 %d Fixture" % status] + [
        "%s: %s" % item for item in headers.items()
    ]
    return ("\r\n".join(lines) + "\r\n\r\n").encode() + body


class ScriptedServer:
    """Answer httplib2's HTTPS requests with scripted raw responses.

    The real `http.client` code runs, including its debug output; only the
    socket is replaced.
    """

    def __init__(self, test, *responses):
        self.responses = list(responses)
        self.sent = []
        self.connections = 0
        server = self

        class Socket:
            def sendall(self, data):
                server.sent.append(data)

            def makefile(self, mode):
                return io.BytesIO(server.responses.pop(0))

            def close(self):
                pass

        class Connection(http.client.HTTPConnection):
            def __init__(self, authority, timeout=None, proxy_info=None):
                super().__init__(authority, timeout=timeout)

            def connect(self):
                server.connections += 1
                self.sock = Socket()

        patcher = patch.dict(
            httplib2.SCHEME_TO_CONNECTION, {"https": Connection}
        )
        patcher.start()
        test.addCleanup(patcher.stop)


class NoServiceRootLaunchpad(Launchpad):
    """Skip fetching the service root and leave the cache untouched."""

    me = SimpleNamespace(name="alice")

    @classmethod
    def _get_paths(cls, service_root, launchpadlib_dir=None):
        return service_root, None, None, None

    def __init__(
        self, credentials, authorization_engine, credential_store, *args
    ):
        self.credentials = credentials
        self.credential_store = credential_store


class HardwareTestCase(unittest.TestCase):
    """Provide an independent software authenticator for each test."""

    def setUp(self):
        super().setUp()
        if importlib.util.find_spec("fido2") is None:
            self.skipTest("The optional fido2 dependency is not installed.")

        from launchpadlib.testing.hardware import (
            FakeMintingTransport,
            SoftwareHardwareKey,
        )

        self.now = [datetime(2026, 1, 1, tzinfo=timezone.utc)]
        self.key = SoftwareHardwareKey()
        self.client = HardwareKeyClient(QuietInteraction(), lambda: [self.key])
        self.transport = FakeMintingTransport(self.key, lambda: self.now[0])
        self.grant = HardwareTokenGrant(
            "fixture-grant",
            "fixture-refresh-secret",
            "alice",
            fido2compat.encode_base64url(self.key.credential_id),
        )
        self.consumer = Consumer("tests", application_name="Current app")
        self.engine = HardwareTokenAuthorizationEngine(
            "dev",
            self.consumer,
            "alice",
            self.transport.origin,
            self.transport,
            self.client,
            lambda: self.now[0],
        )
        self.credentials = HardwareTokenCredentials(
            self.grant, "dev", self.consumer, self.transport.origin
        )
        self.credentials.attach(self.engine)

    def make_temporary_directory(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return Path(directory.name)


class TestHttpMintingTransport(unittest.TestCase):
    """Check the wire format of Launchpad's token-minting endpoints."""

    def setUp(self):
        super().setUp()
        self.now = datetime(2026, 9, 22, tzinfo=timezone.utc)
        self.grant = HardwareTokenGrant(
            "refresh&key", "refresh+secret", "alice"
        )
        self.credential_id = fido2compat.encode_base64url(b"credential")
        self.options = {
            "publicKey": {
                "challenge": fido2compat.encode_base64url(b"c" * 32),
                "rpId": "launchpad.net",
                "allowCredentials": [
                    {"type": "public-key", "id": self.credential_id}
                ],
                "userVerification": "required",
            }
        }
        self.assertion = {
            "rawId": self.credential_id,
            "response": {"signature": "abc"},
        }
        self.http = Mock(connections={})
        self.transport = HttpMintingTransport(
            "https://launchpad.net", http=self.http
        )

    def response(self, payload, status=200):
        return SimpleNamespace(status=status), payload

    def minted_body(self, **extra):
        result = {
            "oauth_token": "access&key",
            "oauth_token_secret": "access+secret",
            "expires_at": (self.now + timedelta(hours=1)).isoformat(),
            "lp.context": "None",
        }
        result.update(extra)
        return urlencode(result).encode()

    def queue_exchange(self):
        self.http.request.side_effect = [
            self.response(
                json.dumps(dict(self.options, challenge_id=123)).encode()
            ),
            self.response(self.minted_body()),
        ]

    def test_transport_respects_ssl_validation_environment(self):
        for value, disabled in ((None, False), ("", False), ("1", True)):
            with self.subTest(value=value):
                environment = (
                    {}
                    if value is None
                    else {"LP_DISABLE_SSL_CERTIFICATE_VALIDATION": value}
                )
                with patch.dict(os.environ, environment, clear=True):
                    transport = HttpMintingTransport("https://launchpad.net")
                self.assertIs(
                    disabled, transport.http.disable_ssl_certificate_validation
                )

    def test_supplied_http_keeps_ssl_configuration(self):
        self.http.disable_ssl_certificate_validation = False
        with patch.dict(
            os.environ, {"LP_DISABLE_SSL_CERTIFICATE_VALIDATION": "1"}
        ):
            transport = HttpMintingTransport(
                "https://launchpad.net", http=self.http
            )
        self.assertIs(self.http, transport.http)
        self.assertIs(False, self.http.disable_ssl_certificate_validation)

    def test_challenge_form_and_top_level_options(self):
        self.queue_exchange()
        challenge = self.transport.request_challenge(self.grant)
        self.assertEqual(123, challenge.handle)
        self.assertEqual(self.options, challenge.options)
        args, kw = self.http.request.call_args
        self.assertEqual(("https://launchpad.net/+hw-challenge",), args)
        self.assertEqual(
            {
                "oauth_token": ["refresh&key"],
                "oauth_token_secret": ["refresh+secret"],
            },
            parse_qs(kw["body"].decode()),
        )
        self.assertEqual("POST", kw["method"])
        self.assertEqual(
            "application/x-www-form-urlencoded", kw["headers"]["Content-Type"]
        )
        self.assertFalse(self.http.follow_redirects)

    def test_assertion_json_inside_form_and_token_response(self):
        self.http.request.return_value = self.response(self.minted_body())
        token = self.transport.verify_assertion(
            self.grant, 123, self.assertion
        )
        args, kw = self.http.request.call_args
        self.assertEqual(("https://launchpad.net/+hw-access-token",), args)
        form = parse_qs(kw["body"].decode())
        self.assertEqual(["123"], form["challenge_id"])
        self.assertEqual(self.assertion, json.loads(form["assertion"][0]))
        self.assertEqual(["refresh+secret"], form["oauth_token_secret"])
        self.assertEqual("access&key", token.key)
        self.assertEqual("access+secret", token.secret)
        self.assertIsNone(token.context)
        self.assertEqual(self.now + timedelta(hours=1), token.expires_at)

    def test_context_is_preserved(self):
        self.http.request.return_value = self.response(
            self.minted_body(**{"lp.context": "ubuntu/hello"})
        )
        token = self.transport.verify_assertion(
            self.grant, 123, self.assertion
        )
        self.assertEqual("ubuntu/hello", token.context)

    def test_invalid_responses(self):
        """Reject malformed challenges, ambiguous tokens and naive expiry."""
        for body in (
            b"{}",
            b"[]",
            b"not json",
            json.dumps(dict(self.options, challenge_id=True)).encode(),
        ):
            with self.subTest(body=body):
                self.http.request.return_value = self.response(body)
                with self.assertRaises(HardwareTokenError):
                    self.transport.request_challenge(self.grant)
        for body in (
            b"{}",
            self.minted_body() + b"&oauth_token=duplicate",
            self.minted_body(expires_at="2026-09-22T01:00:00"),
        ):
            with self.subTest(body=body):
                self.http.request.return_value = self.response(body)
                with self.assertRaises(HardwareTokenError):
                    self.transport.verify_assertion(
                        self.grant, 123, self.assertion
                    )

    def test_rejection_and_redirect_are_not_retried(self):
        for status, error in (
            (401, HardwareTokenGrantError),
            (400, HardwareTokenError),
            (302, HardwareTokenError),
        ):
            self.http.reset_mock()
            self.http.request.return_value = self.response(b"rejected", status)
            with self.assertRaises(error):
                self.transport.verify_assertion(
                    self.grant, 123, self.assertion
                )
            self.http.request.assert_called_once()

    def test_each_request_uses_new_connection_without_debugging(self):
        """A cached connection can be stale or still have debugging on."""
        server = ScriptedServer(
            self,
            raw_response(200),
            raw_response(
                200, json.dumps(dict(self.options, challenge_id=123)).encode()
            ),
            raw_response(200, self.minted_body()),
        )
        http = httplib2.Http(proxy_info=None)
        with patch.object(httplib2, "debuglevel", 1):
            with redirect_stdout(io.StringIO()):
                http.request("https://launchpad.net/")
        transport = HttpMintingTransport("https://launchpad.net", http=http)
        output = io.StringIO()
        with redirect_stdout(output):
            challenge = transport.request_challenge(self.grant)
            token = transport.verify_assertion(
                self.grant, challenge.handle, self.assertion
            )
        self.assertEqual("access&key", token.key)
        self.assertEqual(3, server.connections)
        self.assertEqual([], server.responses)
        self.assertEqual("", output.getvalue())

    def test_protocol_errors_are_hardware_token_errors(self):
        server = ScriptedServer(self, b"garbled\r\n", b"garbled\r\n")
        transport = HttpMintingTransport(
            "https://launchpad.net", proxy_info=None
        )
        with self.assertRaisesRegex(HardwareTokenError, "request failed"):
            transport.request_challenge(self.grant)
        self.assertEqual([], server.responses)

    def test_old_record_rejected(self):
        with self.assertRaises(HardwareTokenError):
            HardwareTokenCredentials.from_string(
                '{"version": 1, "kind": "hardware-token"}'
            )

    @requires_fido2
    def test_login_default_transport_and_reload(self):
        """Omitting service_root uses staging for minting and stored login."""
        self.options["publicKey"]["rpId"] = "staging.launchpad.net"
        hardware = Mock()
        hardware.get_assertion.return_value = self.assertion
        kwargs = dict(
            account="alice",
            consumer_name="app",
            credential_store=MemoryHardwareTokenCredentialStore(),
            hardware_client=hardware,
            clock=lambda: self.now,
        )
        with patch(
            "launchpadlib.launchpad.HttpMintingTransport",
            return_value=self.transport,
        ) as factory:
            self.queue_exchange()
            lp = NoServiceRootLaunchpad.login_with_hardware_token(
                grant={
                    "oauth_token": self.grant.token,
                    "oauth_token_secret": self.grant.secret,
                },
                **kwargs,
            )
            self.assertEqual(
                "https://staging.launchpad.net/", factory.call_args.args[0]
            )
            self.assertEqual("access&key", lp.credentials.access_token.key)
            self.assertEqual(
                "https://staging.launchpad.net", lp.credentials.origin
            )
            self.queue_exchange()
            restored = NoServiceRootLaunchpad.login_with_hardware_token(
                **kwargs
            )
            self.assertEqual(self.grant, restored.credentials.grant)

    @requires_fido2
    def test_http_adapter_mints_through_real_fido2_client(self):
        from launchpadlib.testing.hardware import (
            FakeMintingTransport,
            SoftwareHardwareKey,
        )

        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        key = SoftwareHardwareKey()
        server = FakeMintingTransport(key, lambda: now)
        grant = HardwareTokenGrant(
            "fixture-grant",
            "fixture-refresh-secret",
            "alice",
            fido2compat.encode_base64url(key.credential_id),
        )

        def request(url, method, body, headers, redirections):
            form = {k: v[0] for k, v in parse_qs(body.decode()).items()}
            if url.endswith("/+hw-challenge"):
                challenge = server.request_challenge(grant)
                result = dict(challenge.options, challenge_id=challenge.handle)
                return SimpleNamespace(status=200), json.dumps(result).encode()
            token = server.verify_assertion(
                grant, int(form["challenge_id"]), json.loads(form["assertion"])
            )
            result = {
                "oauth_token": token.key,
                "oauth_token_secret": token.secret,
                "expires_at": token.expires_at.isoformat(),
            }
            return SimpleNamespace(status=200), urlencode(result).encode()

        self.http.request.side_effect = request
        engine = HardwareTokenAuthorizationEngine(
            "dev",
            Consumer("tests"),
            "alice",
            server.origin,
            HttpMintingTransport("https://launchpad.test", http=self.http),
            HardwareKeyClient(QuietInteraction(), lambda: [key]),
            lambda: now,
        )
        token = engine.mint(grant)
        self.assertEqual("fixture-access-1", token.key)
        self.assertEqual(now + server.lifetime, token.expires_at)
        self.assertEqual(1, server.minted)
        self.assertEqual(1, key.closed)


class TestHardwareTokenAuthorizationEngine(HardwareTestCase):
    """Check the engine's validation even with injected hardware providers."""

    def setUp(self):
        super().setUp()
        self.challenge = self.transport.request_challenge(self.grant)
        self.hardware = Mock()
        self.assertion = {"rawId": self.grant.credential_id}
        self.hardware.get_assertion.return_value = self.assertion
        self.minting = Mock()
        self.minting.request_challenge.return_value = self.challenge
        self.token = MintedAccessToken("access", "secret")
        self.minting.verify_assertion.return_value = self.token
        self.engine.hardware = self.hardware
        self.engine.transport = self.minting

    def test_malformed_options_rejected_before_hardware(self):
        """Injected hardware cannot bypass WebAuthn option validation."""
        self.challenge.options["publicKey"]["challenge"] = (
            fido2compat.encode_base64url(b"short")
        )
        with self.assertRaises(ValueError):
            self.engine.mint(self.grant)
        self.hardware.get_assertion.assert_not_called()
        self.minting.verify_assertion.assert_not_called()

    def test_unexpected_rp_id_rejected_before_hardware(self):
        self.challenge.options["publicKey"]["rpId"] = "evil.example"
        with self.assertRaisesRegex(HardwareTokenError, "Unexpected RP ID"):
            self.engine.mint(self.grant)
        self.hardware.get_assertion.assert_not_called()
        self.minting.verify_assertion.assert_not_called()

    def test_challenge_excluding_grant_key_rejected_before_hardware(self):
        """A nonempty server allowlist must contain the grant's key."""
        self.challenge.options["publicKey"]["allowCredentials"] = [
            {
                "type": "public-key",
                "id": fido2compat.encode_base64url(b"other"),
            }
        ]
        with self.assertRaisesRegex(HardwareTokenError, "does not permit"):
            self.engine.mint(self.grant)
        self.hardware.get_assertion.assert_not_called()
        self.minting.verify_assertion.assert_not_called()

    def test_grant_key_restricts_hardware_options_without_mutating_challenge(
        self,
    ):
        """Restrict broad, empty and absent allowlists to the selected key."""
        selected = {"type": "public-key", "id": self.grant.credential_id}
        other = {
            "type": "public-key",
            "id": fido2compat.encode_base64url(b"other"),
        }
        for allowed in ([other, selected], [], None):
            with self.subTest(allowed=allowed):
                options = deepcopy(self.challenge.options)
                if allowed is None:
                    options["publicKey"].pop("allowCredentials")
                else:
                    options["publicKey"]["allowCredentials"] = allowed
                original = deepcopy(options)
                self.minting.request_challenge.return_value = MintingChallenge(
                    self.challenge.handle, options
                )
                self.hardware.reset_mock()
                self.minting.verify_assertion.reset_mock()
                self.assertIs(self.token, self.engine.mint(self.grant))
                expected = deepcopy(original)
                expected["publicKey"]["allowCredentials"] = [selected]
                self.hardware.get_assertion.assert_called_once_with(
                    expected, self.engine.origin
                )
                self.assertEqual(original, options)
                self.minting.verify_assertion.assert_called_once_with(
                    self.grant, self.challenge.handle, self.assertion
                )

    def test_unselected_grant_preserves_server_allowlist(self):
        """Without a selected key, pass the server's allowlist through."""
        grant = HardwareTokenGrant(
            self.grant.token, self.grant.secret, "alice"
        )
        original = deepcopy(self.challenge.options)
        self.assertIs(self.token, self.engine.mint(grant))
        self.minting.request_challenge.assert_called_once_with(grant)
        self.hardware.get_assertion.assert_called_once_with(
            original, self.engine.origin
        )
        self.minting.verify_assertion.assert_called_once_with(
            grant, self.challenge.handle, self.assertion
        )

    def test_wrong_or_missing_assertion_credential_rejected_before_exchange(
        self,
    ):
        """Injected hardware must return the grant's selected credential."""
        for assertion in (
            {},
            {"rawId": fido2compat.encode_base64url(b"other")},
        ):
            with self.subTest(assertion=assertion):
                self.hardware.get_assertion.return_value = assertion
                with self.assertRaisesRegex(
                    HardwareTokenError, "different credential"
                ):
                    self.engine.mint(self.grant)
                self.minting.verify_assertion.assert_not_called()

    def test_invalid_transport_result_rejected(self):
        self.minting.verify_assertion.return_value = {"oauth_token": "access"}
        with self.assertRaisesRegex(HardwareTokenError, "MintedAccessToken"):
            self.engine.mint(self.grant)
        self.minting.verify_assertion.assert_called_once_with(
            self.grant, self.challenge.handle, self.assertion
        )

    def test_challenge_rejection_stops_before_hardware(self):
        error = HardwareTokenGrantError("Rejected grant")
        self.minting.request_challenge.side_effect = error
        with self.assertRaises(HardwareTokenGrantError) as caught:
            self.credentials.ensure_access_token()
        self.assertIs(error, caught.exception)
        self.minting.request_challenge.assert_called_once_with(self.grant)
        self.hardware.get_assertion.assert_not_called()
        self.minting.verify_assertion.assert_not_called()
        self.assertIsNone(self.credentials.access_token)

    def test_assertion_rejection_is_not_retried_or_cached(self):
        error = HardwareTokenGrantError("Rejected assertion")
        self.minting.verify_assertion.side_effect = error
        with self.assertRaises(HardwareTokenGrantError) as caught:
            self.credentials.ensure_access_token()
        self.assertIs(error, caught.exception)
        self.minting.request_challenge.assert_called_once_with(self.grant)
        self.hardware.get_assertion.assert_called_once()
        self.minting.verify_assertion.assert_called_once_with(
            self.grant, self.challenge.handle, self.assertion
        )
        self.assertIsNone(self.credentials.access_token)


class TestHardwareTokenCredentials(HardwareTestCase):
    def test_real_client_mints_signs_reuses_and_renews(self):
        credentials = self.credentials
        headers = {}
        credentials.authorizeRequest(
            "https://api.launchpad.test/devel/", "GET", None, headers
        )
        self.assertIn(
            'oauth_token="fixture-access-1"', headers["Authorization"]
        )
        self.assertEqual(1, self.transport.minted)
        credentials.ensure_access_token()
        self.assertEqual(1, self.transport.minted)
        self.now[0] += timedelta(seconds=28)
        credentials.ensure_access_token()
        self.assertEqual(2, self.transport.minted)
        self.assertEqual(2, self.key.closed)

    def test_invalid_signature_mints_nothing(self):
        self.key.bad_signature = True
        with self.assertRaises(ValueError):
            self.credentials.ensure_access_token()
        self.assertIsNone(self.credentials.access_token)
        self.assertEqual(1, self.key.closed)

    def test_all_serializers_exclude_access_token(self):
        tmp_path = self.make_temporary_directory()
        credentials = self.credentials
        credentials.ensure_access_token()
        stream = io.StringIO()
        credentials.save(stream)
        self.assertNotIn("fixture-secret", stream.getvalue())
        path = tmp_path / "credentials"
        credentials.save_to_path(path)
        restored = credentials.load_from_path(path)
        self.assertIsNone(restored.access_token)
        self.assertEqual(credentials.grant, restored.grant)
        self.assertNotIn(self.grant.secret, repr(self.grant))
        self.assertEqual(0o600, os.stat(path).st_mode & 0o777)
        credentials.load(io.StringIO(stream.getvalue()))
        self.assertIsNone(credentials.access_token)
        self.assertIsNone(credentials.engine)

    def test_file_store_loads_without_account_but_attach_rejects_mismatch(
        self,
    ):
        """Lookup ignores the account; attaching still checks ownership."""
        tmp_path = self.make_temporary_directory()
        store = UnencryptedFileHardwareTokenCredentialStore(
            tmp_path / "credentials"
        )
        store.save(self.credentials, self.credentials.storage_key)
        key = HardwareTokenCredentials.storage_key_for("dev", self.consumer)
        restored = store.load(key)
        self.assertEqual(self.grant, restored.grant)
        self.assertIsNone(restored.access_token)
        bob = HardwareTokenAuthorizationEngine(
            "dev",
            self.consumer,
            "bob",
            self.transport.origin,
            self.transport,
            self.client,
            lambda: self.now[0],
        )
        with self.assertRaisesRegex(HardwareTokenError, "account"):
            restored.attach(bob)
        self.assertIsNone(restored.engine)
        restored.attach(self.engine)
        self.assertIs(self.engine, restored.engine)

    def test_storage_key_uses_service_and_consumer_only(self):
        """Accounts share a slot, but services and consumers do not."""
        bob = HardwareTokenCredentials(
            HardwareTokenGrant("b", "bob-secret", "bob"),
            "dev",
            self.consumer,
            self.transport.origin,
        )
        self.assertEqual(self.credentials.storage_key, bob.storage_key)
        for service, consumer in (
            ("staging", self.consumer),
            ("dev", Consumer("other")),
        ):
            with self.subTest(service=service, consumer=consumer.key):
                self.assertNotEqual(
                    self.credentials.storage_key,
                    HardwareTokenCredentials.storage_key_for(
                        service, consumer
                    ),
                )

    def test_memory_store_restores_without_access_token(self):
        self.credentials.ensure_access_token()
        store = MemoryHardwareTokenCredentialStore()
        store.save(self.credentials, self.credentials.storage_key)
        restored = store.load(self.credentials.storage_key)
        self.assertIsNone(restored.access_token)
        self.assertIsNot(restored, self.credentials)

    def test_other_origins_are_unsigned_without_minting(self):
        """Downloads may leave the API origin without receiving its token."""
        for uri in (
            "https://launchpadlibrarian.net/123/file",
            "https://api.launchpad.test.evil.example/",
            "http://api.launchpad.test/",
            "https://api.launchpad.test:444/",
        ):
            for name in ("Authorization", "authorization", "AUTHORIZATION"):
                with self.subTest(uri=uri, header=name):
                    headers = {name: "OAuth stale", "Accept": "text/plain"}
                    with patch.object(
                        self.credentials, "ensure_access_token"
                    ) as mint:
                        self.credentials.authorizeRequest(
                            uri, "GET", None, headers
                        )
                    mint.assert_not_called()
                    self.assertEqual({"Accept": "text/plain"}, headers)
        self.assertIsNone(self.credentials.access_token)

    def test_unknown_expiry_reused_and_expired_result_rejected(self):
        self.transport.lifetime = None
        self.credentials.ensure_access_token()
        self.now[0] += timedelta(days=1)
        self.credentials.ensure_access_token()
        self.assertEqual(1, self.transport.minted)
        self.credentials.invalidate()
        self.transport.lifetime = timedelta(seconds=-1)
        with self.assertRaisesRegex(HardwareTokenError, "already expired"):
            self.credentials.ensure_access_token()
        self.assertIsNone(self.credentials.access_token)

    def test_store_failure_callback_and_keyring_namespace(self):
        callback = Mock()
        store = KeyringHardwareTokenCredentialStore(callback)
        backend = Mock()
        backend.set_password.side_effect = OSError("fixture failure")
        with patch.object(store, "backend", return_value=backend):
            store.save(self.credentials, self.credentials.storage_key)
        callback.assert_called_once_with()
        self.assertNotEqual(
            "launchpadlib", backend.set_password.call_args.args[0]
        )

    def test_serialized_record_validation(self):
        """Reject a boolean version even though bool is a subclass of int."""
        data = json.loads(self.credentials.serialize())
        data["version"] = True
        with self.assertRaises(HardwareTokenError):
            HardwareTokenCredentials.from_string(json.dumps(data))

    def test_coalesced_minting(self):
        """Concurrent callers share one minted access token."""
        barrier = threading.Barrier(4, timeout=10)

        def ensure_token(_):
            barrier.wait()
            self.credentials.ensure_access_token()

        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(ensure_token, range(4)))
        self.assertEqual(1, self.transport.minted)


class TestLoginWithHardwareToken(HardwareTestCase):
    def login(self, **kwargs):
        args = {
            "application_name": "App",
            "consumer_name": "tests",
            "service_root": "dev",
            "account": "alice",
            "minting_transport": self.transport,
            "hardware_client": self.client,
            "clock": lambda: self.now[0],
        }
        args.update(kwargs)
        return NoServiceRootLaunchpad.login_with_hardware_token(**args)

    def test_login_restore_and_failed_import(self):
        """A failed import must keep the previously stored working grant."""
        store = MemoryHardwareTokenCredentialStore()
        first = self.login(grant=self.grant, credential_store=store)
        second = self.login(credential_store=store)
        self.assertIsInstance(second, NoServiceRootLaunchpad)
        self.assertEqual(2, self.transport.minted)
        self.assertEqual("App", second.credentials.consumer.application_name)
        with self.assertRaises(HardwareTokenGrantError):
            self.login(
                grant=HardwareTokenGrant("wrong", "wrong-secret", "alice"),
                credential_store=store,
            )
        self.assertEqual(
            self.grant, store.load(first.credentials.storage_key).grant
        )

    def test_failed_login_keeps_stored_grant(self):
        """Minting succeeds, but the grant is not stored unless it logs in."""
        store = MemoryHardwareTokenCredentialStore()
        first = self.login(grant=self.grant, credential_store=store)
        key = first.credentials.storage_key
        record = store.read(key)
        self.transport.grants["other-grant"] = "other-secret"
        other = HardwareTokenGrant("other-grant", "other-secret", "alice")
        for name, value, error in (
            ("me", SimpleNamespace(name="bob"), HardwareTokenError),
            ("__init__", Mock(side_effect=ValueError("rejected")), ValueError),
        ):
            with self.subTest(name=name):
                with patch.object(NoServiceRootLaunchpad, name, value):
                    with self.assertRaises(error):
                        self.login(grant=other, credential_store=store)
                self.assertEqual(record, store.read(key))

    def test_credential_id_selects_key_for_unselected_grant(self):
        selector = self.grant.credential_id
        unselected = replace(self.grant, credential_id=None)
        lp = self.login(
            grant=unselected,
            credential_id=selector,
            credential_store=MemoryHardwareTokenCredentialStore(),
        )
        self.assertEqual(self.grant, lp.credentials.grant)

        store = MemoryHardwareTokenCredentialStore()
        self.login(grant=unselected, credential_store=store)
        lp = self.login(credential_id=selector, credential_store=store)
        self.assertEqual(
            self.grant, store.load(lp.credentials.storage_key).grant
        )
        with self.assertRaisesRegex(HardwareTokenError, "different"):
            self.login(
                credential_id=fido2compat.encode_base64url(b"other"),
                credential_store=store,
            )

    def test_first_credentials_file_in_home(self):
        """Create a missing private directory below an expanded `~`."""
        home = self.make_temporary_directory()
        filename = "~/.config/launchpadlib/hardware.json"
        with patch.dict(os.environ, {"HOME": str(home)}):
            self.login(grant=self.grant, credentials_file=filename)
            lp = self.login(credentials_file=filename)
        self.assertEqual(self.grant, lp.credentials.grant)
        directory = home / ".config" / "launchpadlib"
        self.assertTrue((directory / "hardware.json").exists())
        self.assertEqual(0o700, os.stat(directory).st_mode & 0o777)

    def test_uses_hardware_token_http(self):
        lp = self.login(
            grant=self.grant,
            credential_store=MemoryHardwareTokenCredentialStore(),
        )
        http = lp.httpFactory(lp.credentials, None, None, None)
        self.assertIsInstance(http, HardwareTokenHttp)

    def test_missing_grant(self):
        with self.assertRaisesRegex(HardwareTokenError, "No grant stored"):
            self.login(credential_store=MemoryHardwareTokenCredentialStore())
        self.assertEqual(0, self.transport.minted)

    def test_grant_for_another_account_rejected(self):
        with self.assertRaisesRegex(HardwareTokenError, "different account"):
            self.login(
                grant=HardwareTokenGrant("b", "bob-secret", "bob"),
                credential_store=MemoryHardwareTokenCredentialStore(),
            )

    def test_interaction_and_client_are_exclusive(self):
        with self.assertRaisesRegex(ValueError, "interaction"):
            self.login(
                grant=self.grant,
                interaction=QuietInteraction(),
                credential_store=MemoryHardwareTokenCredentialStore(),
            )

    def test_credentials_file_and_store_are_exclusive(self):
        with self.assertRaisesRegex(ValueError, "credentials_file"):
            self.login(
                grant=self.grant,
                credentials_file="credentials",
                credential_store=MemoryHardwareTokenCredentialStore(),
            )

    def test_credentials_file_only_falls_back_when_none(self):
        """An explicit empty filename must not select the environment file."""
        for filename, expected in ((None, "environment-file"), ("", "")):
            with self.subTest(filename=filename):
                with (
                    patch.dict(
                        os.environ,
                        {"LP_HARDWARE_CREDENTIALS_FILE": "environment-file"},
                    ),
                    patch(
                        "launchpadlib.launchpad."
                        "UnencryptedFileHardwareTokenCredentialStore"
                    ) as factory,
                ):
                    factory.return_value.load.return_value = None
                    with self.assertRaisesRegex(
                        HardwareTokenError, "No grant stored"
                    ):
                        self.login(credentials_file=filename)
                factory.assert_called_once_with(expected, None)

    def test_sudo_uses_memory_store(self):
        with (
            patch.object(
                NoServiceRootLaunchpad, "_is_sudo", return_value=True
            ),
            patch.dict(os.environ, {}, clear=True),
        ):
            lp = self.login(grant=self.grant)
        self.assertIsInstance(
            lp.credential_store, MemoryHardwareTokenCredentialStore
        )


class TestHardwareTokenHttp(unittest.TestCase):
    def request(self, authorizer, method, uri, response, body):
        http = HardwareTokenHttp(authorizer, None, None, None)
        args = (Mock(), "host", uri, "/", method, None, {}, 0, None)
        with patch.object(
            RestfulHttp, "_request", return_value=(response, body)
        ) as request:
            http._request(*args)
        return request.call_count

    def test_http_retry_is_bounded(self):
        for status, body, calls in [
            (401, b"Expired token", 2),
            (401, b"Unrelated", 1),
            (403, b"Forbidden", 1),
        ]:
            with self.subTest(status=status, body=body, calls=calls):
                response = SimpleNamespace(status=status)
                self.assertEqual(
                    calls,
                    self.request(Mock(), "GET", API_URI, response, body),
                )

    def test_mutations_are_not_replayed(self):
        authorizer = Mock()
        response = SimpleNamespace(status=401)
        self.assertEqual(
            1,
            self.request(
                authorizer, "POST", API_URI, response, b"Expired token"
            ),
        )
        authorizer.invalidate.assert_called_once()

    def test_rejection_from_other_origin_keeps_token(self):
        """Requests to other origins are unsigned, so ignore their 401s."""
        authorizer = Mock()
        authorizer.is_api_uri.return_value = False
        response = SimpleNamespace(status=401)
        uri = "https://example.com/file"
        self.assertEqual(
            1, self.request(authorizer, "GET", uri, response, b"Expired token")
        )
        authorizer.invalidate.assert_not_called()


class TestHardwareTokenHttpConnections(HardwareTestCase):
    def test_redirect_chain_refreshes_token_once(self):
        redirect = raw_response(302, Location=API_URI + "~alice")
        expired = raw_response(401, b"Expired token (fixture).")
        server = ScriptedServer(self, redirect, expired, redirect, expired)
        http = HardwareTokenHttp(self.credentials, None, None, None)
        response, _ = http.request(API_URI + "people/+me")
        self.assertEqual(401, response.status)
        self.assertEqual([], server.responses)
        self.assertEqual(2, self.transport.minted)

    def test_cached_debug_connection_does_not_print_token(self):
        """Disabling debugging after a refused request must take effect."""
        server = ScriptedServer(self, raw_response(200, b"{}"))
        http = HardwareTokenHttp(self.credentials, None, None, None)
        with patch.object(httplib2, "debuglevel", 1):
            with self.assertRaisesRegex(HardwareTokenError, "debugging"):
                http.request(API_URI)
        output = io.StringIO()
        with redirect_stdout(output):
            http.request(API_URI)
        self.assertIn(b"fixture-secret", b"".join(server.sent))
        self.assertEqual("", output.getvalue())
