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

"""External USB security-key assertions.

No device access occurs at import time.
"""

import getpass
import logging
import sys
import threading
from contextlib import contextmanager
from urllib.parse import urlsplit

from launchpadlib import fido2compat

logger = logging.getLogger(__name__)


class HardwareKeyError(Exception):
    pass


class HardwareKeyCancelledError(HardwareKeyError):
    pass


class HardwareKeyTimeoutError(HardwareKeyError):
    pass


def validate_origin(origin):
    parsed = urlsplit(origin)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("The WebAuthn origin must be an HTTPS origin.")
    return origin.rstrip("/")


class ConsoleInteraction:
    """A fresh PIN budget for each serialized ceremony."""

    def __init__(self, max_pin_attempts=3):
        if max_pin_attempts < 1:
            raise ValueError("max_pin_attempts must be positive.")
        self.limit = max_pin_attempts
        self.attempts = 0
        self.lock = threading.Lock()

    @contextmanager
    def ceremony(self):
        with self.lock:
            self.attempts = 0
            try:
                yield
            finally:
                self.attempts = 0

    def prompt_up(self):
        print("Touch your security key.", file=sys.stderr)

    def request_pin(self, permissions, rp_id):
        if self.attempts >= self.limit:
            raise HardwareKeyCancelledError("PIN attempt limit reached.")

        self.attempts += 1
        value = getpass.getpass("Security key PIN: ")
        if not value:
            raise HardwareKeyCancelledError("PIN entry cancelled.")
        return value

    def request_uv(self, permissions, rp_id):
        return True

    def choose(self, labels, description):
        if len(labels) == 1:
            return 0

        for number, label in enumerate(labels, 1):
            print("%d. %s" % (number, label), file=sys.stderr)
        try:
            value = input(
                "Choose %s (1-%d; blank cancels): "
                % (description, len(labels))
            )
            if not value:
                raise HardwareKeyCancelledError("Selection cancelled.")
            index = int(value) - 1
        except ValueError as error:
            raise HardwareKeyError("Invalid selection.") from error

        if not 0 <= index < len(labels):
            raise HardwareKeyError("Invalid selection.")
        return index


class NonInteractiveInteraction(ConsoleInteraction):
    def prompt_up(self):
        raise HardwareKeyError(
            "This ceremony requires a person to touch the key."
        )

    def request_pin(self, permissions, rp_id):
        raise HardwareKeyError("This ceremony requires PIN entry.")

    def request_uv(self, permissions, rp_id):
        raise HardwareKeyError("This ceremony requires user verification.")

    def choose(self, labels, description):
        if len(labels) != 1:
            raise HardwareKeyError("An interactive selection is required.")
        return 0


class HardwareKeyClient:
    def __init__(
        self,
        interaction=None,
        device_lister=None,
        client_factory=None,
    ):
        self.interaction = interaction or ConsoleInteraction()
        self.device_lister = device_lister
        self.client_factory = client_factory or fido2compat.build_client

    def get_assertion(self, options, origin, cancel_event=None):
        return self._perform(
            options,
            origin,
            cancel_event,
            registration=False,
        )

    def register(self, options, origin, cancel_event=None):
        return self._perform(
            options,
            origin,
            cancel_event,
            registration=True,
        )

    def _perform(self, options, origin, cancel_event, registration):
        fido2compat.require_fido2()

        from fido2.client import ClientError
        from fido2.ctap import CtapError
        from fido2.hid import CtapHidDevice
        from fido2.rpid import verify_rp_id

        origin = validate_origin(origin)
        parsed = (
            fido2compat.creation_options(options)
            if registration
            else fido2compat.request_options(options)
        )
        rp_id = parsed.rp.id if registration else parsed.rp_id
        if not verify_rp_id(rp_id, origin):
            raise HardwareKeyError(
                "The RP ID does not match the configured origin."
            )

        event = cancel_event or threading.Event()
        if event.is_set():
            raise HardwareKeyCancelledError("Ceremony cancelled.")

        devices = []
        try:
            with self.interaction.ceremony():
                lister = self.device_lister or CtapHidDevice.list_devices
                devices.extend(lister())

                if not devices:
                    raise HardwareKeyError("No USB FIDO2 key found.")

                labels = [
                    getattr(device, "product_name", None)
                    or "Unknown security key"
                    for device in devices
                ]
                index = self.interaction.choose(labels, "security key")
                if type(index) is not int or not 0 <= index < len(devices):
                    raise HardwareKeyError("Invalid device selection.")

                client = self.client_factory(
                    devices[index],
                    origin,
                    self.interaction,
                )

                if registration:
                    return fido2compat.registration_json(
                        client.make_credential(parsed, event=event)
                    )

                selection = client.get_assertion(parsed, event=event)
                assertions = selection.get_assertions()
                if not assertions:
                    raise HardwareKeyError("The key returned no assertions.")

                labels = [
                    (assertion.user or {}).get("name")
                    or "Credential %d" % number
                    for number, assertion in enumerate(assertions, 1)
                ]
                index = self.interaction.choose(labels, "credential")
                if type(index) is not int or not 0 <= index < len(assertions):
                    raise HardwareKeyError("Invalid credential selection.")

                return fido2compat.assertion_json(selection, index)
        except (ClientError, CtapError) as error:
            code = getattr(getattr(error, "cause", None), "code", None)
            if code is None:
                code = error.code
            code = getattr(code, "name", "")

            if event.is_set() or code in (
                "KEEPALIVE_CANCEL",
                "OPERATION_DENIED",
            ):
                raise HardwareKeyCancelledError(
                    "Security-key operation cancelled."
                ) from error

            if code in (
                "TIMEOUT",
                "ACTION_TIMEOUT",
                "USER_ACTION_TIMEOUT",
            ):
                raise HardwareKeyTimeoutError(
                    "Security-key operation timed out."
                ) from error

            messages = {
                "PIN_INVALID": ("Incorrect security-key PIN."),
                "PIN_AUTH_INVALID": ("Incorrect security-key PIN."),
                "PIN_BLOCKED": (
                    "The PIN is blocked; follow the key "
                    "vendor's recovery instructions."
                ),
                "PIN_AUTH_BLOCKED": (
                    "PIN authentication is temporarily "
                    "blocked; reconnect the key."
                ),
                "PIN_NOT_SET": ("Configure a PIN on the key first."),
                "NO_CREDENTIALS": ("This key has no matching credential."),
            }
            raise HardwareKeyError(
                messages.get(code, "Security-key operation failed.")
            ) from error
        except (EOFError, KeyboardInterrupt) as error:
            raise HardwareKeyCancelledError("Ceremony cancelled.") from error
        except OSError as error:
            raise HardwareKeyError(
                "Cannot access the key; check USB "
                "permissions and connection."
            ) from error
        finally:
            for device in devices:
                try:
                    device.close()
                except Exception:
                    # Continue cleanup without replacing the original
                    # ceremony error.
                    logger.warning("Failed to close a security-key device.")
