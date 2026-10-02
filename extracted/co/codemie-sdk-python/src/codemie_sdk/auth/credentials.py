"""Authentication credentials module for CodeMie SDK."""

import base64
import json as _json
import time
import requests
from typing import Callable


def _decode_jwt_exp(token: str) -> float | None:
    """Return the exp claim from a JWT payload without signature verification."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += "=" * padding
        claims = _json.loads(base64.urlsafe_b64decode(payload))
        exp = claims.get("exp")
        return float(exp) if exp is not None else None
    except Exception:
        return None


class LocalAuthCredentials:
    """Authenticates against the backend local-auth endpoint and caches the JWT."""

    _TOKEN_EXPIRY_BUFFER_SECONDS = 30

    def __init__(
        self,
        api_domain: str,
        email: str,
        password: str,
        verify_ssl: bool = True,
    ):
        self._login_url = f"{api_domain.rstrip('/')}/v1/local-auth/login"
        self._email = email
        self._password = password
        self._verify_ssl = verify_ssl
        self._cached_token: str | None = None
        self._token_expires_at: float = 0.0

    def get_token(self) -> str:
        """Return cached JWT, re-logging in when expired."""
        now = time.monotonic()
        if self._cached_token and now < self._token_expires_at:
            return self._cached_token

        response = requests.post(
            self._login_url,
            json={"email": self._email, "password": self._password},
            verify=self._verify_ssl,
        )
        response.raise_for_status()
        self._cached_token = response.json()["access_token"]

        exp = _decode_jwt_exp(self._cached_token)
        if exp is not None:
            ttl = exp - time.time()
            self._token_expires_at = now + max(
                ttl - self._TOKEN_EXPIRY_BUFFER_SECONDS, 0
            )
        else:
            self._token_expires_at = now + 3570  # 1 h fallback
        return self._cached_token


class KeycloakCredentials:
    """Keycloak authentication credentials handler."""

    _TOKEN_EXPIRY_BUFFER_SECONDS = 30

    def __init__(
        self,
        server_url: str,
        realm_name: str,
        client_id: str | None = None,
        client_secret: str | None = None,
        username: str | None = None,
        password: str | None = None,
        external_token: str | Callable[[], str] | None = None,
        external_idp: str | None = None,
        verify_ssl: bool = True,
    ):
        """Initialize Keycloak credentials.

        Args:
            server_url: Keycloak server URL
            realm_name: Realm name
            client_id: Client ID (optional if using username/password)
            client_secret: Client secret (optional if using username/password)
            username: Username/email for password grant (optional)
            password: Password for password grant (optional)
            external_token: External token for authentication (optional)
            external_idp: Identity provider ID to validate token (optional)
            verify_ssl: Whether to verify SSL certificates (default: True)
        """
        self.server_url = server_url.rstrip("/")
        self.realm_name = realm_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.external_token = external_token
        self.external_idp = external_idp
        self.verify_ssl = verify_ssl
        self._cached_token: str | None = None
        self._token_expires_at: float = 0.0

    def get_token(self) -> str:
        """Get access token, returning cached value if still valid."""
        now = time.monotonic()
        if self._cached_token and now < self._token_expires_at:
            return self._cached_token

        if not (
            (self.client_id and self.client_secret)
            or (self.username and self.password)
            or (self.external_token and self.external_idp)
        ):
            raise ValueError(
                "Either client credentials (client_id, client_secret) or "
                "user credentials (username, password) must be provided"
            )
        url = (
            f"{self.server_url}/realms/{self.realm_name}/protocol/openid-connect/token"
        )

        if self.external_token and self.external_idp:
            subject_token = (
                self.external_token()
                if callable(self.external_token)
                else self.external_token
            )
            payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                "subject_token": subject_token,
                "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
                "subject_issuer": self.external_idp,
                "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
            }
        elif self.username and self.password:
            payload = {
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
                "client_id": self.client_id or "codemie-sdk",
            }
            if self.client_secret:
                payload["client_secret"] = self.client_secret
        else:
            payload = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

        response = requests.post(url, data=payload, verify=self.verify_ssl)
        response.raise_for_status()
        data = response.json()
        self._cached_token = data["access_token"]
        expires_in = data.get("expires_in", 300)
        self._token_expires_at = now + expires_in - self._TOKEN_EXPIRY_BUFFER_SECONDS
        return self._cached_token

    def exchange_token_for_user(self, email: str, access_token: str) -> str:
        """Exchange service account token for user token."""
        user_id = self.find_user_by_email(email, access_token)
        return self._exchange_token_for_user(user_id, access_token)

    def find_user_by_email(self, email: str, access_token: str) -> str:
        """Find user ID by email."""
        url = f"{self.server_url}/admin/realms/{self.realm_name}/users?email={email}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers, verify=self.verify_ssl)
        response.raise_for_status()

        users = response.json()
        if not users:
            raise ValueError(f"User with email {email} not found")
        return users[0]["id"]

    def _exchange_token_for_user(self, user_id: str, service_account_token: str) -> str:
        """Exchange token for specific user."""
        url = (
            f"{self.server_url}/realms/{self.realm_name}/protocol/openid-connect/token"
        )
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": service_account_token,
            "requested_subject": user_id,
        }

        response = requests.post(
            url, headers=headers, data=payload, verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.json()["access_token"]
