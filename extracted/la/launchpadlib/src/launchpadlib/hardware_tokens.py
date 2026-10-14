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

"""Hardware-bound grants and short-lived OAuth 1 access tokens."""

import hashlib
import http.client
import json
import os
import tempfile
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlencode, urlsplit

import httplib2
from lazr.restfulclient._browser import RestfulHttp
from lazr.restfulclient.authorize.oauth import Consumer

from launchpadlib import fido2compat, uris
from launchpadlib.credentials import (
    AccessToken,
    CredentialStore,
    Credentials,
    _ssl_certificate_validation_disabled,
)
from launchpadlib.hardware import (
    HardwareKeyClient,
    HardwareKeyError,
    validate_origin,
)


class HardwareTokenError(HardwareKeyError):
    pass


class HardwareTokenGrantError(HardwareTokenError):
    pass


def utcnow():
    return datetime.now(timezone.utc)


def text(value, name):
    if not isinstance(value, str) or not value:
        raise ValueError("%s must be a non-empty string." % name)
    return value


def atomic_write(filename, data):
    directory = os.path.dirname(os.path.abspath(filename))
    fd, temporary = tempfile.mkstemp(
        prefix=".launchpad-hardware-",
        dir=directory,
    )
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, filename)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@dataclass(frozen=True)
class HardwareTokenGrant:
    """A refresh-token pair issued for one registered authenticator."""

    token: str = field(repr=False)
    secret: str = field(repr=False)
    account: str
    credential_id: str = None

    def __post_init__(self):
        text(self.token, "refresh token")
        text(self.secret, "refresh-token secret")
        text(self.account, "account")
        if self.credential_id is not None:
            object.__setattr__(
                self,
                "credential_id",
                fido2compat.encode_base64url(
                    fido2compat.decode_base64url(self.credential_id)
                ),
            )


@dataclass(frozen=True)
class MintingChallenge:
    handle: object
    options: dict


@dataclass(frozen=True)
class MintedAccessToken:
    key: str = field(repr=False)
    secret: str = field(repr=False)
    expires_at: datetime = None
    context: str = None

    def __post_init__(self):
        text(self.key, "access token")
        text(self.secret, "access-token secret")

        if self.expires_at is not None:
            if (
                not isinstance(self.expires_at, datetime)
                or self.expires_at.utcoffset() is None
            ):
                raise ValueError("Token expiry must be timezone-aware.")

        if self.context is not None:
            text(self.context, "context")


class HttpMintingTransport:
    """Exchange refresh credentials using Launchpad's browser endpoints.

    Both requests are form encoded. The challenge response is JSON; the
    access-token response is form encoded.
    """

    def __init__(
        self,
        web_root,
        timeout=30,
        proxy_info=httplib2.proxy_info_from_environment,
        ca_certs=None,
        http=None,
    ):
        web_root = validate_origin(web_root)
        self.challenge_url = web_root + "/+hw-challenge"
        self.verify_url = web_root + "/+hw-access-token"
        self.http = (
            http
            if http is not None
            else httplib2.Http(
                cache=None,
                timeout=timeout,
                proxy_info=proxy_info,
                ca_certs=ca_certs,
                disable_ssl_certificate_validation=(
                    _ssl_certificate_validation_disabled()
                ),
            )
        )
        self.http.follow_redirects = False
        self.http.follow_all_redirects = False

    def _post(self, url, payload, accept):
        if httplib2.debuglevel:
            raise HardwareTokenError(
                "Disable httplib2 debugging before sending token secrets."
            )
        # A cached connection may have gone stale while the user touched
        # the key, which makes httplib2 resend the request. It also keeps
        # the debug level it was created with.
        for connection in self.http.connections.values():
            connection.close()
        self.http.connections.clear()
        try:
            response, body = self.http.request(
                url,
                method="POST",
                body=urlencode(payload).encode("ascii"),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": accept,
                },
                redirections=0,
            )
        except (
            httplib2.HttpLib2Error,
            http.client.HTTPException,
            OSError,
        ) as error:
            raise HardwareTokenError("Minting request failed.") from error
        if response.status in (401, 403, 410):
            raise HardwareTokenGrantError(
                "The exchange was rejected; check the refresh token and key."
            )
        if response.status != 200:
            raise HardwareTokenError(
                "Minting returned HTTP %d." % response.status
            )
        return body

    def request_challenge(self, grant):
        body = self._post(
            self.challenge_url,
            {"oauth_token": grant.token, "oauth_token_secret": grant.secret},
            "application/json",
        )
        try:
            result = json.loads(body)
            if not isinstance(result, dict):
                raise ValueError()
            challenge_id = result.pop("challenge_id")
            if type(challenge_id) is not int or challenge_id <= 0:
                raise ValueError()
            if not isinstance(result.get("publicKey"), dict):
                raise ValueError()
            return MintingChallenge(challenge_id, result)
        except (KeyError, TypeError, ValueError, UnicodeError) as error:
            raise HardwareTokenError("Malformed minting challenge.") from error

    def verify_assertion(self, grant, handle, assertion):
        body = self._post(
            self.verify_url,
            {
                "oauth_token": grant.token,
                "oauth_token_secret": grant.secret,
                "challenge_id": handle,
                "assertion": json.dumps(assertion),
            },
            "application/x-www-form-urlencoded",
        )
        try:
            result = parse_qs(
                body.decode("utf-8"),
                keep_blank_values=True,
                strict_parsing=True,
            )
            # Duplicate values are ambiguous, including optional fields.
            if any(len(values) != 1 for values in result.values()):
                raise ValueError()
            expiry = datetime.fromisoformat(
                text(result["expires_at"][0], "expiry").replace("Z", "+00:00")
            )
            context = result.get("lp.context", [None])[0]
            # The current endpoint URL-encodes Python None as the text "None".
            if context in ("", "None"):
                context = None
            return MintedAccessToken(
                result["oauth_token"][0],
                result["oauth_token_secret"][0],
                expiry,
                context,
            )
        except (KeyError, TypeError, ValueError, UnicodeError) as error:
            raise HardwareTokenError(
                "Malformed minted access token."
            ) from error


class HardwareTokenCredentials(Credentials):
    """Credentials that store a hardware-bound grant, not its tokens."""

    def __init__(
        self,
        grant=None,
        service_root=None,
        consumer=None,
        origin=None,
    ):
        super().__init__(None)
        self.grant = grant
        self.service_root = (
            uris.lookup_service_root(service_root)
            if service_root is not None
            else None
        )
        if self.service_root is not None:
            validate_origin(self.service_root)
        self.consumer = consumer
        self.origin = validate_origin(origin) if origin else None
        self.engine = None
        self._renew_at = None
        self._lock = threading.RLock()

    def __repr__(self):
        return "HardwareTokenCredentials(service_root=%r)" % self.service_root

    @property
    def storage_key(self):
        return self.storage_key_for(self.service_root, self.consumer)

    @staticmethod
    def storage_key_for(service_root, consumer):
        """Identify a stored grant without needing to know its account."""
        values = [uris.lookup_service_root(service_root), consumer.key]
        return "v2:" + hashlib.sha256(json.dumps(values).encode()).hexdigest()

    def compatible(self, service, consumer, account, origin):
        return (
            self.service_root == service
            and self.consumer is not None
            and self.consumer.key == consumer.key
            and self.grant.account == account
            and self.origin == origin
        )

    def attach(self, engine):
        if not self.compatible(
            engine.service,
            engine.consumer,
            engine.account,
            engine.origin,
        ):
            raise HardwareTokenError(
                "Stored grant has different service, "
                "consumer, account or origin."
            )

        self.engine = engine
        self.consumer.application_name = engine.consumer.application_name

    def ensure_access_token(self):
        with self._lock:
            if self.engine is None:
                raise HardwareTokenError(
                    "Attach a minting engine before "
                    "using these credentials."
                )

            now = self.engine.clock()
            if self.access_token is not None and (
                self._renew_at is None or now < self._renew_at
            ):
                return

            minted = self.engine.mint(self.grant)
            received = self.engine.clock()
            renew_at = None

            if minted.expires_at is not None:
                remaining = minted.expires_at - received
                if remaining <= timedelta(0):
                    raise HardwareTokenError(
                        "The server returned an already " "expired token."
                    )

                # Preserve most of even a short token lifetime.
                margin = min(
                    timedelta(seconds=60),
                    remaining / 10,
                )
                renew_at = minted.expires_at - margin

            self.access_token = AccessToken(
                minted.key,
                minted.secret,
                minted.context,
            )
            self._renew_at = renew_at

    def invalidate(self):
        with self._lock:
            self.access_token = None
            self._renew_at = None

    def is_api_uri(self, uri):
        """Return whether requests to `uri` are signed with our token."""
        parsed = urlsplit(uri)
        expected = urlsplit(self.service_root)
        return (parsed.scheme, parsed.hostname, parsed.port or 443) == (
            expected.scheme,
            expected.hostname,
            expected.port or 443,
        )

    def authorizeRequest(self, absolute_uri, method, body, headers):
        if httplib2.debuglevel:
            raise HardwareTokenError(
                "Disable httplib2 debugging before " "sending token secrets."
            )

        if not self.is_api_uri(absolute_uri):
            # Downloads and redirects may leave the API origin. Permit
            # those requests, but never send our OAuth token to that host.
            for name in list(headers):
                if name.lower() == "authorization":
                    del headers[name]
            return

        with self._lock:
            self.ensure_access_token()
            return super().authorizeRequest(
                absolute_uri, method, body, headers
            )

    def serialize(self):
        if self.grant is None or self.consumer is None or not self.origin:
            raise HardwareTokenError("Incomplete hardware credentials.")

        return json.dumps(
            {
                "version": 2,
                "kind": "hardware-token",
                "refresh_token": self.grant.token,
                "refresh_token_secret": self.grant.secret,
                "account": self.grant.account,
                "credential_id": self.grant.credential_id,
                "service_root": self.service_root,
                "origin": self.origin,
                "consumer": self.consumer.key,
            },
            sort_keys=True,
        ).encode("utf-8")

    @classmethod
    def from_string(cls, value):
        try:
            data = json.loads(value)
            if (
                not isinstance(data, dict)
                or type(data.get("version")) is not int
                or data["version"] != 2
                or data.get("kind") != "hardware-token"
            ):
                raise ValueError()

            return cls(
                HardwareTokenGrant(
                    data["refresh_token"],
                    data["refresh_token_secret"],
                    data["account"],
                    data.get("credential_id"),
                ),
                data["service_root"],
                Consumer(text(data["consumer"], "consumer")),
                data["origin"],
            )
        except (
            KeyError,
            TypeError,
            ValueError,
            UnicodeError,
        ) as error:
            raise HardwareTokenError(
                "Invalid hardware credential record."
            ) from error

    def save(self, writable_file):
        writable_file.write(self.serialize().decode("utf-8"))

    def load(self, readable_file):
        restored = self.from_string(readable_file.read())
        self.__dict__.update(restored.__dict__)

    def save_to_path(self, path):
        atomic_write(path, self.serialize())

    @classmethod
    def load_from_path(cls, path):
        with open(path, "rb") as stream:
            return cls.from_string(stream.read())


class HardwareTokenCredentialStore(CredentialStore):
    """Subclasses store serialized bytes, never live credentials."""

    def do_save(self, credentials, unique_key):
        if (
            not isinstance(credentials, HardwareTokenCredentials)
            or credentials.storage_key != unique_key
        ):
            raise HardwareTokenError("Credential storage identity mismatch.")

        self.write(unique_key, credentials.serialize())

    def do_load(self, unique_key):
        value = self.read(unique_key)
        if value is None:
            return None

        credentials = HardwareTokenCredentials.from_string(value)
        if credentials.storage_key != unique_key:
            raise HardwareTokenError(
                "Stored credentials belong " "to another identity."
            )
        return credentials

    def read(self, key):
        raise NotImplementedError()

    def write(self, key, value):
        raise NotImplementedError()


class MemoryHardwareTokenCredentialStore(HardwareTokenCredentialStore):
    def __init__(self, credential_save_failed=None):
        super().__init__(credential_save_failed)
        self.records = {}

    def read(self, key):
        return self.records.get(key)

    def write(self, key, value):
        self.records[key] = value


class UnencryptedFileHardwareTokenCredentialStore(
    HardwareTokenCredentialStore
):
    def __init__(
        self,
        filename,
        credential_save_failed=None,
    ):
        super().__init__(credential_save_failed)
        self.filename = os.path.expanduser(filename)

    def read(self, key):
        try:
            with open(self.filename, "rb") as stream:
                return stream.read()
        except FileNotFoundError:
            return None

    def write(self, key, value):
        os.makedirs(
            os.path.dirname(os.path.abspath(self.filename)),
            mode=0o700,
            exist_ok=True,
        )
        atomic_write(self.filename, value)


class KeyringHardwareTokenCredentialStore(HardwareTokenCredentialStore):
    SERVICE = "launchpadlib.hardware-token.v2"

    @staticmethod
    def backend():
        try:
            import keyring
        except ModuleNotFoundError as error:
            if error.name != "keyring":
                raise
            raise HardwareTokenError(
                "Install keyring or specify "
                "credentials_file / a memory store."
            ) from error
        return keyring

    def read(self, key):
        return self.backend().get_password(self.SERVICE, key)

    def write(self, key, value):
        self.backend().set_password(
            self.SERVICE,
            key,
            value.decode("utf-8"),
        )


class HardwareTokenAuthorizationEngine:
    def __init__(
        self,
        service,
        consumer,
        account,
        origin,
        transport,
        hardware_client=None,
        clock=utcnow,
    ):
        self.service = uris.lookup_service_root(service)
        self.consumer = consumer
        self.account = text(account, "account")
        self.origin = validate_origin(origin)
        self.transport = transport
        self.hardware = hardware_client or HardwareKeyClient()
        self.clock = clock

    def mint(self, grant):
        challenge = self.transport.request_challenge(grant)

        # Validate even with an injected assertion provider.
        parsed = fido2compat.request_options(challenge.options)
        from fido2.rpid import verify_rp_id

        if not verify_rp_id(parsed.rp_id, self.origin):
            raise HardwareTokenError("Unexpected RP ID in minting challenge.")

        options = dict(challenge.options)
        options["publicKey"] = dict(options["publicKey"])

        if grant.credential_id is not None:
            wanted = fido2compat.decode_base64url(grant.credential_id)
            if parsed.allow_credentials and wanted not in [
                item.id for item in parsed.allow_credentials
            ]:
                raise HardwareTokenError(
                    "Challenge does not permit " "the grant's registered key."
                )

            options["publicKey"]["allowCredentials"] = [
                {
                    "type": "public-key",
                    "id": grant.credential_id,
                }
            ]

        assertion = self.hardware.get_assertion(options, self.origin)
        if (
            grant.credential_id
            and assertion.get("rawId") != grant.credential_id
        ):
            raise HardwareTokenError(
                "The key returned a different credential."
            )

        minted = self.transport.verify_assertion(
            grant,
            challenge.handle,
            assertion,
        )
        if not isinstance(minted, MintedAccessToken):
            raise HardwareTokenError(
                "Transport did not return MintedAccessToken."
            )
        return minted


class HardwareTokenHttp(RestfulHttp):
    """Retry safe requests once after an access token is rejected.

    Like httplib2.Http, this is not thread-safe.
    """

    _in_request = False

    @staticmethod
    def bad_token(response, content):
        return response.status == 401 and content.startswith(
            (
                b"Expired token",
                b"Unknown access token",
            )
        )

    def _request(
        self,
        conn,
        host,
        absolute_uri,
        request_uri,
        method,
        body,
        headers,
        redirections,
        cachekey,
    ):
        args = (
            conn,
            host,
            absolute_uri,
            request_uri,
            method,
            body,
            headers,
            redirections,
            cachekey,
        )
        conn.set_debuglevel(httplib2.debuglevel)
        if self._in_request:
            return super()._request(*args)

        self._in_request = True
        try:
            response, content = super()._request(*args)
            if not self.token_rejected(absolute_uri, response, content):
                return response, content

            self.authorizer.invalidate()
            if method.upper() not in ("GET", "HEAD", "OPTIONS"):
                return response, content

            response, content = super()._request(*args)
            if self.token_rejected(absolute_uri, response, content):
                self.authorizer.invalidate()
            return response, content
        finally:
            self._in_request = False

    def token_rejected(self, absolute_uri, response, content):
        # Requests to other origins are not signed, so their 401 responses
        # say nothing about our token.
        return self.authorizer.is_api_uri(absolute_uri) and self.bad_token(
            response, content
        )
