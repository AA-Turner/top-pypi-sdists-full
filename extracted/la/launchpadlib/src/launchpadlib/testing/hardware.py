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

"""A software CTAP2 key and WebAuthn server for hardware-key tests."""

from datetime import timedelta
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from fido2 import cbor, client
from fido2.cose import ES256
from fido2.ctap import CtapError
from fido2.hid import CAPABILITY, CTAPHID, STATUS
from fido2.server import Fido2Server
from fido2.utils import sha256
from fido2.webauthn import (
    AttestationObject,
    AttestedCredentialData,
    AuthenticatorData,
    CollectedClientData,
    PublicKeyCredentialRpEntity,
    UserVerificationRequirement,
)

from launchpadlib.fido2compat import decode_base64url, encode_base64url
from launchpadlib.hardware_tokens import (
    HardwareTokenGrantError,
    MintedAccessToken,
    MintingChallenge,
    utcnow,
)


class SoftwareHardwareKey:
    """Implement the CTAP2 operations needed by hardware-token tests."""

    capabilities = CAPABILITY.CBOR

    def __init__(self, rp_id="launchpad.test"):
        self.rp_id = rp_id
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.credential_id = os.urandom(32)
        self.credential = AttestedCredentialData.create(
            b"\0" * 16,
            self.credential_id,
            ES256.from_cryptography_key(self.private_key.public_key()),
        )
        self.counter = 0
        self.closed = 0
        self.bad_signature = False

    def close(self):
        self.closed += 1

    def call(
        self,
        cmd,
        data=b"",
        event=None,
        on_keepalive=None,
    ):
        if event is not None and event.is_set():
            raise CtapError(CtapError.ERR.KEEPALIVE_CANCEL)

        if cmd != CTAPHID.CBOR:
            raise CtapError(CtapError.ERR.INVALID_COMMAND)

        operation = data[0]
        args = cbor.decode(data[1:]) if len(data) > 1 else {}

        if operation == 4:  # authenticatorGetInfo
            result = {
                1: ["FIDO_2_0"],
                2: [],
                3: b"\0" * 16,
                4: {
                    "uv": True,
                    "up": True,
                    "rk": False,
                },
                6: [1],
            }

        elif operation == 1:  # authenticatorMakeCredential
            if args[2]["id"] != self.rp_id:
                raise CtapError(CtapError.ERR.INVALID_PARAMETER)

            if any(
                credential["id"] == self.credential_id
                for credential in args.get(5, [])
            ):
                raise CtapError(CtapError.ERR.CREDENTIAL_EXCLUDED)

            if on_keepalive:
                on_keepalive(STATUS.UPNEEDED)

            auth_data = AuthenticatorData.create(
                sha256(self.rp_id.encode()),
                0x45,
                0,
                self.credential,
            )
            result = {
                1: "none",
                2: bytes(auth_data),
                3: {},
            }

        elif operation == 2:  # authenticatorGetAssertion
            allowed = args.get(3)
            if args[1] != self.rp_id or (
                allowed
                and self.credential_id
                not in [credential["id"] for credential in allowed]
            ):
                raise CtapError(CtapError.ERR.NO_CREDENTIALS)

            opts = args.get(5, {})
            up = opts.get("up", True)
            if up:
                if on_keepalive:
                    on_keepalive(STATUS.UPNEEDED)
                self.counter += 1

            flags = (1 if up else 0) | (4 if opts.get("uv") else 0)
            auth_data = AuthenticatorData.create(
                sha256(self.rp_id.encode()),
                flags,
                self.counter,
            )

            signing_key = (
                ec.generate_private_key(ec.SECP256R1())
                if self.bad_signature
                else self.private_key
            )
            signature = signing_key.sign(
                bytes(auth_data) + args[2],
                ec.ECDSA(hashes.SHA256()),
            )
            result = {
                1: {
                    "type": "public-key",
                    "id": self.credential_id,
                },
                2: bytes(auth_data),
                3: signature,
            }

        else:
            raise CtapError(CtapError.ERR.INVALID_COMMAND)

        return b"\0" + cbor.encode(result)


class SoftwareRelyingParty:
    """Verify WebAuthn ceremonies performed with a `SoftwareHardwareKey`."""

    def __init__(self, key):
        self.key = key
        self.origin = "https://" + key.rp_id
        self.server = Fido2Server(
            PublicKeyCredentialRpEntity(
                id=key.rp_id,
                name="Tests",
            ),
            verify_origin=lambda origin: origin == self.origin,
        )

    def begin_authentication(self):
        """Return JSON request options and the state needed to verify them."""
        options, state = self.server.authenticate_begin(
            credentials=[self.key.credential],
            user_verification=UserVerificationRequirement.REQUIRED,
        )
        options = options.public_key
        return (
            {
                "publicKey": {
                    "challenge": encode_base64url(options.challenge),
                    "rpId": options.rp_id,
                    "userVerification": "required",
                    "timeout": 30000,
                    "allowCredentials": [
                        {
                            "type": "public-key",
                            "id": encode_base64url(self.key.credential_id),
                        }
                    ],
                }
            },
            state,
        )

    def complete_authentication(self, state, assertion):
        """Verify an assertion and return its authenticator data."""
        response = assertion["response"]
        auth = AuthenticatorData(
            decode_base64url(response["authenticatorData"])
        )

        # FIDO2 2.x accepts the complete authentication response.
        # FIDO2 1.x requires its components as separate arguments.
        if hasattr(client, "DefaultClientDataCollector"):
            self.server.authenticate_complete(
                state,
                [self.key.credential],
                assertion,
            )
        else:
            self.server.authenticate_complete(
                state,
                [self.key.credential],
                decode_base64url(assertion["rawId"]),
                CollectedClientData(
                    decode_base64url(response["clientDataJSON"])
                ),
                auth,
                decode_base64url(response["signature"]),
            )
        return auth

    def complete_registration(self, state, registration):
        """Verify a registration response."""
        # See `complete_authentication` for the version differences.
        if hasattr(client, "DefaultClientDataCollector"):
            self.server.register_complete(state, registration)
        else:
            response = registration["response"]
            self.server.register_complete(
                state,
                CollectedClientData(
                    decode_base64url(response["clientDataJSON"])
                ),
                AttestationObject(
                    decode_base64url(response["attestationObject"])
                ),
            )


class FakeMintingTransport(SoftwareRelyingParty):
    """Real signature verification with fixture tokens and grants."""

    def __init__(
        self,
        key,
        clock=utcnow,
        lifetime=timedelta(seconds=30),
    ):
        super().__init__(key)
        self.clock = clock
        self.lifetime = lifetime
        self.states = {}
        self.grants = {"fixture-grant": "fixture-refresh-secret"}
        self.next_challenge_id = 0
        self.minted = 0
        self.last_counter = 0

    def request_challenge(self, grant):
        if self.grants.get(grant.token) != grant.secret:
            raise HardwareTokenGrantError("Unknown fixture grant.")

        options, state = self.begin_authentication()
        self.next_challenge_id += 1
        handle = self.next_challenge_id
        self.states[handle] = (
            grant.token,
            state,
            self.clock() + timedelta(minutes=5),
        )
        return MintingChallenge(handle, options)

    def verify_assertion(self, grant, handle, assertion):
        item = self.states.get(handle)
        if (
            item is None
            or self.grants.get(grant.token) != grant.secret
            or item[0] != grant.token
            or self.clock() >= item[2]
        ):
            raise HardwareTokenGrantError("Invalid fixture challenge/grant.")

        # Authenticate the grant before consuming its challenge, just as
        # the backend does. Assertion failures still consume the challenge.
        del self.states[handle]
        auth = self.complete_authentication(item[1], assertion)

        if auth.counter <= self.last_counter:
            raise HardwareTokenGrantError("Counter did not advance.")

        self.last_counter = auth.counter
        self.minted += 1

        return MintedAccessToken(
            "fixture-access-%d" % self.minted,
            "fixture-secret",
            None if self.lifetime is None else self.clock() + self.lifetime,
        )
