"""Module for custom authentication."""

from __future__ import annotations

import json
import logging
import os
import ssl
import sys
import threading
import time as time_module
from datetime import datetime, timedelta, timezone

import requests
from dateutil.parser import parse
from requests import PreparedRequest
from requests.auth import AuthBase
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ConnectionError as RequestsConnectionError
from urllib3.exceptions import ProtocolError

logger = logging.getLogger(__name__)


class RefreshToken(AuthBase):
    """Implements a custom authentication scheme."""

    # Class-level lock for thread-safe token refresh
    _refresh_lock = threading.Lock()

    def __init__(self, access_key: str, secret_key: str) -> None:
        self.bearer_token = None
        self.expiry_time = None
        self.access_key = access_key
        self.secret_key = secret_key
        base_url = (
            os.environ.get("MATRICE_BASE_URL") or f"https://{os.environ.get('ENV', 'prod')}.backend.app.matrice.ai"
        )
        self.VALIDATE_ACCESS_KEY_URL = f"{base_url}/v1/accounting/validate_access_key"

    def is_expired(self, buffer_seconds: int = 300) -> bool:
        """Check if token is expired or will expire within buffer_seconds.

        Args:
            buffer_seconds: Number of seconds before actual expiry to consider token expired.
                          Default is 300 (5 minutes) to allow proactive refresh.

        Returns:
            True if token is None, has no expiry, or will expire within buffer_seconds.
        """
        if self.bearer_token is None or self.expiry_time is None:
            return True
        buffer = timedelta(seconds=buffer_seconds)
        now = datetime.now(timezone.utc)
        expiry = self.expiry_time if self.expiry_time.tzinfo else self.expiry_time.replace(tzinfo=timezone.utc)
        return now >= expiry - buffer

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        """Attach an API token to a custom auth header."""
        self.set_bearer_token()
        if self.bearer_token is None:
            raise ValueError(
                "Failed to obtain refresh token. Cannot authenticate request. "
                "Please check your access_key and secret_key credentials."
            )
        r.headers["Authorization"] = self.bearer_token
        return r

    def set_bearer_token(self) -> None:
        """Obtain a bearer token using the provided access key and secret key.

        Thread-safe: Uses a lock to prevent concurrent refresh attempts.
        On failure, resets bearer_token to None to ensure stale tokens aren't used.
        """
        with self._refresh_lock:
            # Check if token is still valid (another thread may have refreshed it)
            if self.bearer_token and not self.is_expired(buffer_seconds=60):
                return  # Already valid

            payload_dict = {
                "accessKey": self.access_key,
                "secretKey": self.secret_key,
            }
            payload = json.dumps(payload_dict)
            headers = {"Content-Type": "text/plain"}
            max_retries = 3
            retry_delay = 1.0
            response = None
            for attempt in range(max_retries):
                try:
                    response = requests.request(
                        "GET",
                        self.VALIDATE_ACCESS_KEY_URL,
                        headers=headers,
                        data=payload,
                        timeout=(10, 120),
                    )
                    # Retry on transient server errors (502, 503, 504)
                    if response.status_code in (502, 503, 504):
                        if attempt < max_retries - 1:
                            logging.warning(
                                "RefreshToken auth request got HTTP %d (attempt %d/%d). Retrying in %.1fs...",
                                response.status_code,
                                attempt + 1,
                                max_retries,
                                retry_delay,
                            )
                            time_module.sleep(retry_delay)
                            retry_delay = min(retry_delay * 2, 30.0)
                            continue
                    break  # Success or non-retryable status, exit retry loop
                except (
                    RequestsConnectionError,
                    ChunkedEncodingError,
                    ProtocolError,
                    ConnectionResetError,
                    ssl.SSLError,
                    OSError,
                ) as e:
                    if attempt < max_retries - 1:
                        # nosemgrep: python.lang.security.audit.logging.logger-credential-leak.python-logger-credential-disclosure
                        logging.warning(
                            "RefreshToken request failed (attempt %d/%d): %s. Retrying in %.1fs...",
                            attempt + 1,
                            max_retries,
                            str(e),
                            retry_delay,
                        )
                        time_module.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, 30.0)
                        continue
                    # Last attempt failed
                    self.bearer_token = None
                    self.expiry_time = None
                    from .utils import process_error_log

                    process_error_log(
                        error=e,
                        service_name="matrice_common",
                        default_return=None,
                        raise_exception=False,
                        log_error=True,
                    )
                    return
                except Exception as e:
                    # Non-retryable error
                    self.bearer_token = None
                    self.expiry_time = None
                    from .utils import process_error_log

                    process_error_log(
                        error=e,
                        service_name="matrice_common",
                        default_return=None,
                        raise_exception=False,
                        log_error=True,
                    )
                    return

            if not response or response.status_code != 200:
                # Reset token on failure to prevent stale token usage
                self.bearer_token = None
                self.expiry_time = None
                error_msg = f"Error response from the auth server in RefreshToken (status: {getattr(response, 'status_code', 'unknown')}): {getattr(response, 'text', 'No response text')}"
                from .utils import process_error_log

                process_error_log(
                    error=Exception(error_msg),
                    service_name="matrice_common",
                    default_return=None,
                    raise_exception=False,
                    log_error=True,
                )
                return

            try:
                res_dict = response.json()
            except Exception as e:
                # Reset token on failure to prevent stale token usage
                self.bearer_token = None
                self.expiry_time = None
                from .utils import process_error_log

                process_error_log(
                    error=Exception(f"Invalid JSON in RefreshToken response: {str(e)}"),
                    service_name="matrice_common",
                    default_return=None,
                    raise_exception=False,
                    log_error=True,
                )
                return

            if res_dict.get("success") and res_dict.get("data", {}).get("refreshToken"):
                logging.debug(f"res_dict: {res_dict}")
                self.bearer_token = "Bearer " + res_dict["data"]["refreshToken"]
                # Track expiry time - use server-provided value or default to 23 hours
                if res_dict.get("data", {}).get("expiresAt"):
                    self.expiry_time = parse(res_dict["data"]["expiresAt"])
                else:
                    # Conservative default: 23 hours (most refresh tokens last 24h+)
                    self.expiry_time = datetime.now(timezone.utc) + timedelta(hours=23)
                logging.debug(f"RefreshToken expiry set to: {self.expiry_time}")
            else:
                # Reset token on failure to prevent stale token usage
                self.bearer_token = None
                self.expiry_time = None
                error_msg = f"The provided credentials are incorrect in RefreshToken. Response: {res_dict}"
                logging.error(error_msg)
                from .utils import process_error_log

                process_error_log(
                    error=Exception(error_msg),
                    service_name="matrice_common",
                    default_return=None,
                    raise_exception=False,
                    log_error=True,
                )

    def reset_and_refresh(self):
        """Reset token state and attempt to refresh.

        This method is used for in-place token updates to avoid
        creating new token objects that would leave concurrent threads
        with stale references.
        """
        with self._refresh_lock:
            self.bearer_token = None
            self.expiry_time = None
        self.set_bearer_token()


class AuthToken(AuthBase):
    """Implements a custom authentication scheme."""

    # Class-level lock for thread-safe token refresh
    _refresh_lock = threading.Lock()

    def __init__(
        self,
        access_key,
        secret_key,
        refresh_token,
    ):
        self.bearer_token = None
        self.access_key = access_key
        self.secret_key = secret_key
        self.refresh_token = refresh_token
        self.expiry_time = datetime.now(timezone.utc)
        base_url = (
            os.environ.get("MATRICE_BASE_URL") or f"https://{os.environ.get('ENV', 'prod')}.backend.app.matrice.ai"
        )
        self.REFRESH_TOKEN_URL = f"{base_url}/v1/accounting/refresh"

    def is_expired(self, buffer_seconds: int = 300) -> bool:
        """Check if token is expired or will expire within buffer_seconds.

        Args:
            buffer_seconds: Number of seconds before actual expiry to consider token expired.
                          Default is 300 (5 minutes) to allow proactive refresh.

        Returns:
            True if token is None, has no expiry, or will expire within buffer_seconds.
        """
        if self.bearer_token is None or self.expiry_time is None:
            return True
        buffer = timedelta(seconds=buffer_seconds)
        now = datetime.now(timezone.utc)
        expiry = self.expiry_time if self.expiry_time.tzinfo else self.expiry_time.replace(tzinfo=timezone.utc)
        return now >= expiry - buffer

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        """Attach an API token to a custom auth header."""
        self.set_bearer_token()
        if self.bearer_token is None:
            raise ValueError(
                "Failed to obtain authentication token. Cannot authenticate request. "
                "This may be due to invalid credentials or server issues."
            )
        r.headers["Authorization"] = self.bearer_token
        return r

    def set_bearer_token(self) -> None:
        """Obtain an authentication bearer token using the provided refresh token.

        Thread-safe: Uses a lock to prevent concurrent refresh attempts.
        On failure, resets bearer_token to None to ensure stale tokens aren't used.
        """
        with self._refresh_lock:
            # Check if token is still valid (another thread may have refreshed it)
            if self.bearer_token and not self.is_expired(buffer_seconds=60):
                return  # Already valid

            # Ensure refresh token is valid - check expiry, not just None
            if self.refresh_token.bearer_token is None or self.refresh_token.is_expired():
                try:
                    logging.debug("RefreshToken is None or expired, refreshing...")
                    self.refresh_token.set_bearer_token()
                except Exception as e:
                    error_msg = f"Failed to obtain refresh token before getting auth token: {e}"
                    logging.error(error_msg)
                    # Reset token on failure
                    self.bearer_token = None
                    self.expiry_time = None
                    return

            # Check if refresh token is still None after refresh attempt
            if self.refresh_token.bearer_token is None:
                logging.error("RefreshToken is still None after refresh attempt")
                self.bearer_token = None
                self.expiry_time = None
                return

            # Use the refresh token bearer_token as an authorization header
            headers = {"Content-Type": "application/json", "Authorization": self.refresh_token.bearer_token}
            max_retries = 3
            retry_delay = 1.0
            response = None
            for attempt in range(max_retries):
                try:
                    response = requests.request(
                        "POST",
                        self.REFRESH_TOKEN_URL,
                        headers=headers,
                        timeout=(10, 120),
                    )
                    # Retry on transient server errors (502, 503, 504)
                    if response.status_code in (502, 503, 504):
                        if attempt < max_retries - 1:
                            logging.warning(
                                "AuthToken auth request got HTTP %d (attempt %d/%d). Retrying in %.1fs...",
                                response.status_code,
                                attempt + 1,
                                max_retries,
                                retry_delay,
                            )
                            time_module.sleep(retry_delay)
                            retry_delay = min(retry_delay * 2, 30.0)
                            continue
                    break  # Success or non-retryable status, exit retry loop
                except (
                    RequestsConnectionError,
                    ChunkedEncodingError,
                    ProtocolError,
                    ConnectionResetError,
                    ssl.SSLError,
                    OSError,
                ) as e:
                    if attempt < max_retries - 1:
                        # nosemgrep: python.lang.security.audit.logging.logger-credential-leak.python-logger-credential-disclosure
                        logging.warning(
                            "AuthToken request failed (attempt %d/%d): %s. Retrying in %.1fs...",
                            attempt + 1,
                            max_retries,
                            str(e),
                            retry_delay,
                        )
                        time_module.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, 30.0)
                        continue
                    # Last attempt failed
                    self.bearer_token = None
                    self.expiry_time = None
                    from .utils import process_error_log

                    process_error_log(
                        error=e,
                        service_name="matrice_common",
                        default_return=None,
                        raise_exception=False,
                        log_error=True,
                    )
                    return
                except Exception as e:
                    # Non-retryable error
                    self.bearer_token = None
                    self.expiry_time = None
                    from .utils import process_error_log

                    process_error_log(
                        error=e,
                        service_name="matrice_common",
                        default_return=None,
                        raise_exception=False,
                        log_error=True,
                    )
                    return

            if not response or response.status_code != 200:
                # Reset token on failure to prevent stale token usage
                self.bearer_token = None
                self.expiry_time = None
                error_msg = f"Error response from the auth server in AuthToken (status: {getattr(response, 'status_code', 'unknown')}): {getattr(response, 'text', 'No response text')}"
                from .utils import process_error_log

                process_error_log(
                    error=Exception(error_msg),
                    service_name="matrice_common",
                    default_return=None,
                    raise_exception=False,
                    log_error=True,
                )
                return

            try:
                res_dict = response.json()
            except Exception as e:
                # Reset token on failure to prevent stale token usage
                self.bearer_token = None
                self.expiry_time = None
                from .utils import process_error_log

                process_error_log(
                    error=Exception(f"Invalid JSON in AuthToken response: {str(e)}"),
                    service_name="matrice_common",
                    default_return=None,
                    raise_exception=False,
                    log_error=True,
                )
                return

            if res_dict.get("success") and res_dict.get("data", {}).get("token"):
                self.bearer_token = "Bearer " + res_dict["data"]["token"]
                self.expiry_time = parse(res_dict["data"]["expiresAt"])
            else:
                # Reset token on failure to prevent stale token usage
                self.bearer_token = None
                self.expiry_time = None
                error_msg = f"The provided credentials are incorrect in AuthToken. Response: {res_dict}"
                logging.error(error_msg)
                from .utils import process_error_log

                process_error_log(
                    error=Exception(error_msg),
                    service_name="matrice_common",
                    default_return=None,
                    raise_exception=False,
                    log_error=True,
                )

    def reset_and_refresh(self):
        """Reset token state and attempt to refresh.

        This method is used for in-place token updates to avoid
        creating new token objects that would leave concurrent threads
        with stale references.
        """
        with self._refresh_lock:
            self.bearer_token = None
            self.expiry_time = None
        self.set_bearer_token()
