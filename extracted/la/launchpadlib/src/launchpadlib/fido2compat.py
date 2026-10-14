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

"""Lazy imports and compatibility helpers for python-fido2."""

import base64
import binascii


# Allow one minute for interaction when the server omits its timeout hint.
# This does not control the server-side expiry of the challenge.
DEFAULT_WEBAUTHN_TIMEOUT_MS = 60_000

# Expected challenge size for Launchpad's token-minting protocol.
MINTING_CHALLENGE_BYTES = 32

# Base64 encodes each complete block as four characters, with at most two
# trailing padding characters for an incomplete block.
BASE64_ENCODED_BLOCK_SIZE = 4
BASE64_MAX_PADDING = 2


class Fido2SupportError(Exception):
    """Hardware support is unavailable because python-fido2 is missing."""


def require_fido2():
    """Import python-fido2, explaining how to install it if unavailable."""
    try:
        import fido2
    except ModuleNotFoundError as error:
        # Preserve errors caused by missing dependencies within python-fido2.
        if error.name != "fido2":
            raise
        raise Fido2SupportError(
            "Install hardware support with "
            "pip install 'launchpadlib[fido2]' "
            "or apt install python3-fido2."
        ) from error
    return fido2


def encode_base64url(value):
    """Encode bytes as an unpadded base64url string."""
    return base64.urlsafe_b64encode(bytes(value)).rstrip(b"=").decode("ascii")


def decode_base64url(value):
    """Decode a non-empty base64url string with optional trailing padding."""
    if not isinstance(value, str) or not value:
        raise ValueError("Expected a non-empty base64url string.")

    raw = value.rstrip("=")
    padding_length = len(value) - len(raw)
    if padding_length > BASE64_MAX_PADDING:
        raise ValueError("Invalid base64url encoding.")

    required_padding = -len(raw) % BASE64_ENCODED_BLOCK_SIZE
    try:
        result = base64.b64decode(
            raw + "=" * required_padding,
            altchars=b"-_",
            validate=True,
        )
    except (binascii.Error, ValueError) as error:
        raise ValueError("Invalid base64url encoding.") from error

    # The decoder also accepts the standard Base64 alphabet and non-zero
    # pad bits. Re-encoding enforces the canonical URL-safe representation.
    if encode_base64url(result) != raw:
        raise ValueError("Non-canonical base64url encoding.")

    return result


def _get_timeout_ms(options):
    """Return the server timeout hint, or our default when omitted."""
    timeout = options.get("timeout", DEFAULT_WEBAUTHN_TIMEOUT_MS)
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, int)
        or timeout <= 0
    ):
        raise ValueError(
            "Timeout must be a positive integer number of milliseconds."
        )
    return timeout


def build_client(device, origin, interaction):
    """Construct a client using the available python-fido2 interface."""
    require_fido2()
    from fido2 import client

    # Newer versions take a client-data collector instead of an origin.
    collector = getattr(client, "DefaultClientDataCollector", None)
    return client.Fido2Client(
        device,
        collector(origin) if collector else origin,
        user_interaction=interaction,
    )


def request_options(envelope):
    """Convert JSON minting options into a WebAuthn request."""
    require_fido2()
    from fido2.webauthn import (
        PublicKeyCredentialDescriptor,
        PublicKeyCredentialRequestOptions,
    )

    try:
        data = envelope["publicKey"]
        challenge = decode_base64url(data["challenge"])
        if len(challenge) != MINTING_CHALLENGE_BYTES:
            raise ValueError(
                "The minting challenge must contain "
                f"{MINTING_CHALLENGE_BYTES} bytes."
            )

        rp_id = data["rpId"]
        if not isinstance(rp_id, str) or not rp_id:
            raise ValueError("Missing RP ID.")

        timeout = _get_timeout_ms(data)

        allowed = data.get("allowCredentials")
        if allowed is not None and not isinstance(allowed, list):
            raise ValueError("Invalid allowed credentials.")

        descriptors = (
            None
            if allowed is None
            else [
                PublicKeyCredentialDescriptor(
                    type=item["type"],
                    id=decode_base64url(item["id"]),
                    transports=item.get("transports"),
                )
                for item in allowed
            ]
        )

        uv = data.get("userVerification", "preferred")
        if uv not in ("required", "preferred", "discouraged"):
            raise ValueError("Invalid user-verification policy.")

        return PublicKeyCredentialRequestOptions(
            challenge=challenge,
            rp_id=rp_id,
            timeout=timeout,
            allow_credentials=descriptors,
            user_verification=uv,
            extensions=data.get("extensions"),
        )
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError("Malformed WebAuthn request options.") from error


def assertion_json(selection, index):
    """Serialize a selected assertion into a JSON-compatible dictionary."""
    result = selection.get_response(index)
    if hasattr(result, "response"):
        response = result.response
        raw_id = result.raw_id
        extensions = getattr(result, "client_extension_results", None)
    else:
        response = result
        raw_id = response.credential_id
        extensions = getattr(response, "extension_results", None)

    if not raw_id:
        raise ValueError("The authenticator omitted its credential ID.")

    data = {
        "id": encode_base64url(raw_id),
        "rawId": encode_base64url(raw_id),
        "type": "public-key",
        "response": {
            "clientDataJSON": encode_base64url(response.client_data),
            "authenticatorData": encode_base64url(response.authenticator_data),
            "signature": encode_base64url(response.signature),
            "userHandle": (
                None
                if response.user_handle is None
                else encode_base64url(response.user_handle)
            ),
        },
    }
    if extensions:
        data["clientExtensionResults"] = dict(extensions)
    return data


def creation_options(envelope):
    """Convert JSON registration options into a WebAuthn creation request."""
    require_fido2()
    from fido2.webauthn import (
        AuthenticatorSelectionCriteria,
        PublicKeyCredentialCreationOptions,
        PublicKeyCredentialDescriptor,
        PublicKeyCredentialParameters,
        PublicKeyCredentialRpEntity,
        PublicKeyCredentialUserEntity,
    )

    try:
        data = envelope["publicKey"]
        user = data["user"]
        selection = data.get("authenticatorSelection", {})
        timeout = _get_timeout_ms(data)

        return PublicKeyCredentialCreationOptions(
            rp=PublicKeyCredentialRpEntity(**data["rp"]),
            user=PublicKeyCredentialUserEntity(
                id=decode_base64url(user["id"]),
                name=user["name"],
                display_name=user["displayName"],
            ),
            challenge=decode_base64url(data["challenge"]),
            pub_key_cred_params=[
                PublicKeyCredentialParameters(**parameter)
                for parameter in data["pubKeyCredParams"]
            ],
            timeout=timeout,
            exclude_credentials=[
                PublicKeyCredentialDescriptor(
                    type=credential["type"],
                    id=decode_base64url(credential["id"]),
                    transports=credential.get("transports"),
                )
                for credential in data.get("excludeCredentials", [])
            ],
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=selection.get(
                    "authenticatorAttachment"
                ),
                resident_key=selection.get("residentKey"),
                require_resident_key=selection.get(
                    "requireResidentKey", False
                ),
                user_verification=selection.get("userVerification"),
            ),
            attestation=data.get("attestation"),
            extensions=data.get("extensions"),
        )
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError("Malformed WebAuthn creation options.") from error


def registration_json(result):
    """Serialize a registration result into a JSON-compatible dictionary."""
    response = getattr(result, "response", result)
    credential = response.attestation_object.auth_data.credential_data
    if credential is None:
        raise ValueError("Missing attested credential data.")

    return {
        "id": encode_base64url(credential.credential_id),
        "rawId": encode_base64url(credential.credential_id),
        "type": "public-key",
        "response": {
            "clientDataJSON": encode_base64url(response.client_data),
            "attestationObject": encode_base64url(response.attestation_object),
        },
    }
