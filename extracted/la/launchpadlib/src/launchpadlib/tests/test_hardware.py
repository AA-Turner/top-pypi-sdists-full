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

"""Tests for USB FIDO2 security keys."""

import importlib
import importlib.util
import io
import json
import multiprocessing
import sys
import threading
import unittest
from contextlib import redirect_stderr
from unittest.mock import Mock, patch
from urllib.parse import parse_qs

from lazr.restfulclient.errors import HTTPError

from launchpadlib import fido2compat
from launchpadlib.hardware import (
    ConsoleInteraction,
    HardwareKeyCancelledError,
    HardwareKeyClient,
    HardwareKeyError,
    HardwareKeyTimeoutError,
    NonInteractiveInteraction,
)
from launchpadlib.launchpad import _cookie_header
from launchpadlib.testing.helpers import (
    OfflineLaunchpad,
    QuietInteraction,
    WebserviceResponse,
)


def check_imports_without_fido2():
    """Check fresh library imports in an isolated child interpreter."""
    # Spawn imports this test module before invoking the target. Remove
    # those cached modules so the imports below exercise initialization.
    for name in list(sys.modules):
        if name == "launchpadlib" or name.startswith("launchpadlib."):
            del sys.modules[name]
        elif name == "fido2" or name.startswith("fido2."):
            del sys.modules[name]
    sys.modules["fido2"] = None

    importlib.import_module("launchpadlib.launchpad")
    importlib.import_module("launchpadlib.hardware")
    importlib.import_module("launchpadlib.hardware_tokens")
    compatibility = importlib.import_module("launchpadlib.fido2compat")

    case = unittest.TestCase()
    with case.assertRaises(compatibility.Fido2SupportError) as caught:
        compatibility.require_fido2()
    case.assertIn("launchpadlib[fido2]", str(caught.exception))


def close_process(process):
    """Reap the dependency-check process even when the test fails."""
    if process.is_alive():
        process.terminate()
    process.join()
    process.close()


class HardwareKeyTestCase(unittest.TestCase):
    """Provide an independent software authenticator for each test."""

    def setUp(self):
        super().setUp()
        if importlib.util.find_spec("fido2") is None:
            self.skipTest("The optional fido2 dependency is not installed.")

        from launchpadlib.testing.hardware import (
            SoftwareHardwareKey,
            SoftwareRelyingParty,
        )

        self.key = SoftwareHardwareKey()
        self.relying_party = SoftwareRelyingParty(self.key)
        self.origin = self.relying_party.origin
        self.client = HardwareKeyClient(QuietInteraction(), lambda: [self.key])

    def creation_options(self):
        options, state = self.relying_party.server.register_begin(
            {"id": b"alice", "name": "alice", "displayName": "Alice"}
        )
        options = options.public_key
        envelope = {
            "publicKey": {
                "rp": {"id": self.key.rp_id, "name": "Tests"},
                "user": {
                    "id": fido2compat.encode_base64url(b"alice"),
                    "name": "alice",
                    "displayName": "Alice",
                },
                "challenge": fido2compat.encode_base64url(options.challenge),
                "pubKeyCredParams": [{"type": "public-key", "alg": -7}],
                "authenticatorSelection": {"userVerification": "required"},
                "attestation": "none",
            }
        }
        return envelope, state


class TestHardwareKeyClient(HardwareKeyTestCase):
    def test_assertion_is_verified_by_server(self):
        options, state = self.relying_party.begin_authentication()
        assertion = self.client.get_assertion(options, self.origin)
        self.relying_party.complete_authentication(state, assertion)
        self.assertEqual(1, self.key.closed)

    def test_invalid_signature_is_rejected_by_server(self):
        self.key.bad_signature = True
        options, state = self.relying_party.begin_authentication()
        assertion = self.client.get_assertion(options, self.origin)
        with self.assertRaises(ValueError):
            self.relying_party.complete_authentication(state, assertion)

    def test_registration_is_verified_by_server(self):
        options, state = self.creation_options()
        registration = self.client.register(options, self.origin)
        self.relying_party.complete_registration(state, registration)
        self.assertEqual(1, self.key.closed)

    def test_cancel_and_wrong_origin_fail_before_device_enumeration(self):
        lister = Mock(return_value=[self.key])
        client = HardwareKeyClient(QuietInteraction(), lister)
        options, _ = self.relying_party.begin_authentication()
        event = threading.Event()
        event.set()
        with self.assertRaises(HardwareKeyCancelledError):
            client.get_assertion(options, self.origin, event)
        with self.assertRaises(HardwareKeyError):
            client.get_assertion(options, "https://example.com")
        lister.assert_not_called()

    def test_client_error_without_cause_keeps_its_code(self):
        from fido2.client import ClientError

        fido2_client = Mock()
        fido2_client.get_assertion.side_effect = ClientError(
            ClientError.ERR.TIMEOUT
        )
        client = HardwareKeyClient(
            QuietInteraction(),
            lambda: [self.key],
            lambda device, origin, interaction: fido2_client,
        )
        options, _ = self.relying_party.begin_authentication()
        with self.assertRaises(HardwareKeyTimeoutError):
            client.get_assertion(options, self.origin)

    def test_noninteractive_refuses_user_verification(self):
        client = HardwareKeyClient(
            NonInteractiveInteraction(), lambda: [self.key]
        )
        options, _ = self.relying_party.begin_authentication()
        with self.assertRaises(HardwareKeyError):
            client.get_assertion(options, self.origin)
        self.assertEqual(1, self.key.closed)

    def test_two_devices_close_even_on_bad_selection(self):
        other = Mock(product_name="Other key")
        interaction = QuietInteraction()
        interaction.choose = Mock(return_value=-1)
        client = HardwareKeyClient(interaction, lambda: [self.key, other])
        options, _ = self.relying_party.begin_authentication()
        with self.assertRaises(HardwareKeyError):
            client.get_assertion(options, self.origin)
        interaction.choose.assert_called_once_with(
            ["Unknown security key", "Other key"], "security key"
        )
        self.assertEqual(1, self.key.closed)
        other.close.assert_called_once()


def queue_registration(launchpad, options, authenticator_url=None):
    """Queue the begin and complete responses of a registration."""
    if authenticator_url is None:
        authenticator_url = launchpad.me.self_link + "/+authenticator/17"
    launchpad.load = Mock(
        return_value=Mock(id=17, self_link=authenticator_url)
    )
    launchpad.connection.request.side_effect = [
        (
            WebserviceResponse(
                **{
                    "set-cookie": (
                        "launchpad_session=test-session; Path=/; HttpOnly"
                    )
                }
            ),
            json.dumps(options).encode(),
        ),
        (WebserviceResponse(status=201, location=authenticator_url), b""),
    ]


class TestRegisterHardwareKeyWithSoftwareKey(HardwareKeyTestCase):
    def test_registration_preserves_session_cookie(self):
        launchpad = OfflineLaunchpad()
        options, state = self.creation_options()
        queue_registration(launchpad, options)

        authenticator = launchpad.register_hardware_key(
            "My key", hardware_client=self.client
        )

        self.assertIs(launchpad.load.return_value, authenticator)
        self.assertEqual(17, authenticator.id)
        launchpad.load.assert_called_once_with(authenticator.self_link)
        begin, complete = launchpad.connection.request.call_args_list
        self.assertEqual((launchpad.me.self_link,), begin.args)
        self.assertEqual("POST", begin.kwargs["method"])
        self.assertEqual(0, begin.kwargs["redirections"])
        self.assertEqual(
            {"ws.op": ["beginWebAuthnRegistration"]},
            parse_qs(begin.kwargs["body"].decode()),
        )
        form = parse_qs(complete.kwargs["body"].decode())
        self.assertEqual(["completeWebAuthnRegistration"], form["ws.op"])
        self.assertEqual(["My key"], form["name"])
        self.assertEqual(
            "launchpad_session=test-session",
            complete.kwargs["headers"]["Cookie"],
        )

        # The web service decodes the `response` Text parameter from JSON,
        # and the registration inside it is itself JSON.
        registration = json.loads(json.loads(form["response"][0]))
        self.relying_party.complete_registration(state, registration)


class TestRegisterHardwareKey(unittest.TestCase):
    options = {"publicKey": {"rp": {"id": "launchpad.test"}}}

    def setUp(self):
        super().setUp()
        self.launchpad = OfflineLaunchpad()
        self.client = Mock()
        self.client.register.return_value = {"id": "credential"}

    def test_name_is_checked_before_the_ceremony(self):
        for name in (None, ""):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, "name"):
                    self.launchpad.register_hardware_key(
                        name, hardware_client=self.client
                    )
        self.client.register.assert_not_called()
        self.launchpad.connection.request.assert_not_called()

    def test_cookie_header_keeps_quoting(self):
        response = {"set-cookie": 'a="x\\073y"; Path=/'}
        self.assertEqual('a="x\\073y"', _cookie_header(response))

    def test_origin_defaults_to_web_root(self):
        queue_registration(self.launchpad, self.options)
        self.launchpad.register_hardware_key(
            "My key", hardware_client=self.client
        )
        self.client.register.assert_called_once_with(
            self.options, "https://launchpad.test"
        )

    def test_explicit_origin(self):
        queue_registration(self.launchpad, self.options)
        self.launchpad.register_hardware_key(
            "My key",
            origin="https://example.com/",
            hardware_client=self.client,
        )
        self.client.register.assert_called_once_with(
            self.options, "https://example.com"
        )

    def test_invalid_origin_rejected_before_requests(self):
        with self.assertRaisesRegex(ValueError, "HTTPS origin"):
            self.launchpad.register_hardware_key(
                "My key",
                origin="http://launchpad.test",
                hardware_client=self.client,
            )
        self.launchpad.connection.request.assert_not_called()

    def test_interaction_is_passed_to_default_client(self):
        queue_registration(self.launchpad, self.options)
        interaction = QuietInteraction()
        with patch("launchpadlib.launchpad.HardwareKeyClient") as factory:
            factory.return_value.register.return_value = {}
            self.launchpad.register_hardware_key(
                "My key", interaction=interaction
            )
        factory.assert_called_once_with(interaction=interaction)

    def test_interaction_and_client_are_exclusive(self):
        with self.assertRaisesRegex(ValueError, "interaction"):
            self.launchpad.register_hardware_key(
                "My key",
                interaction=QuietInteraction(),
                hardware_client=self.client,
            )
        self.launchpad.connection.request.assert_not_called()

    def test_malformed_options_rejected_before_hardware(self):
        queue_registration(self.launchpad, {"name": "alice"})
        with self.assertRaisesRegex(HardwareKeyError, "creation options"):
            self.launchpad.register_hardware_key(
                "My key", hardware_client=self.client
            )
        self.client.register.assert_not_called()

    def test_missing_authenticator_url_rejected(self):
        queue_registration(self.launchpad, self.options, "")
        with self.assertRaisesRegex(HardwareKeyError, "authenticator URL"):
            self.launchpad.register_hardware_key(
                "My key", hardware_client=self.client
            )
        self.launchpad.load.assert_not_called()

    def test_completion_error_raises_http_error(self):
        queue_registration(self.launchpad, self.options)
        responses = list(self.launchpad.connection.request.side_effect)
        responses[1] = (
            WebserviceResponse(status=400),
            b"Credential rejected",
        )
        self.launchpad.connection.request.side_effect = responses
        with self.assertRaises(HTTPError):
            self.launchpad.register_hardware_key(
                "My key", hardware_client=self.client
            )
        self.launchpad.load.assert_not_called()


class TestConsoleInteraction(unittest.TestCase):
    def test_choose_lists_labels(self):
        output = io.StringIO()
        with patch("builtins.input", return_value="2"):
            with redirect_stderr(output):
                index = ConsoleInteraction().choose(
                    ["Key A", "Key B"], "security key"
                )
        self.assertEqual(1, index)
        self.assertEqual("1. Key A\n2. Key B\n", output.getvalue())

    def test_pin_budget_resets(self):
        interaction = ConsoleInteraction(max_pin_attempts=1)
        with patch("getpass.getpass", return_value="fixture-pin"):
            for _ in range(4):
                with interaction.ceremony():
                    self.assertEqual(
                        "fixture-pin",
                        interaction.request_pin(None, "launchpad.test"),
                    )
                    with self.assertRaises(HardwareKeyCancelledError):
                        interaction.request_pin(None, "launchpad.test")


class TestBase64url(unittest.TestCase):
    def test_canonical_validation(self):
        self.assertEqual("_w", fido2compat.encode_base64url(b"\xff"))
        for value in ("_w", "_w=="):
            self.assertEqual(b"\xff", fido2compat.decode_base64url(value))
        for value in ("/w==", "_x", "_w===", "", "a"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                fido2compat.decode_base64url(value)


class TestOptionalFido2(unittest.TestCase):
    def test_no_fido2_import_needed(self):
        context = multiprocessing.get_context("spawn")
        process = context.Process(target=check_imports_without_fido2)
        process.start()
        self.addCleanup(close_process, process)
        process.join(timeout=30)
        self.assertFalse(process.is_alive(), "Dependency check timed out.")
        self.assertEqual(0, process.exitcode)
