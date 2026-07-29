"""Module for custom authentication."""

from __future__ import annotations

import json
import logging
import os
import sys
import threading
import time as time_module
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
from dateutil.parser import parse
from requests import PreparedRequest
from requests.auth import AuthBase
from urllib3.exceptions import ProtocolError

logger = logging.getLogger(__name__)


class _RefreshLockPicklingMixin:
    """Pickle support for token classes that hold a non-picklable RLock.

    ``threading.RLock`` cannot be pickled, so ``_refresh_lock`` is dropped on
    pickle and recreated on unpickle — letting objects that embed a token
    (e.g. ``RPC``) cross a multiprocessing boundary.
    """

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        state["_refresh_lock"] = None
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self._refresh_lock = threading.RLock()


class RefreshToken(_RefreshLockPicklingMixin, AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, access_key: str, secret_key: str) -> None:
        self.bearer_token: Optional[str] = None
        self.expiry_time: Optional[datetime] = None
        # Instance-level (re-entrant) lock so unrelated credential pairs do not
        # serialize their refreshes behind each other. RLock lets
        # reset_and_refresh hold the lock across null+refresh without a window
        # where other threads observe bearer_token is None.
        self._refresh_lock = threading.RLock()
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
                    # Retry on transient server errors (500, 502, 503, 504).
                    # 500 is included deliberately: a transient backend fault must
                    # not instantly null the token with no retry (root cause of the
                    # 2026-06-03 61h gateway outage, where a ~2min backend 500
                    # zeroed the bearer token and the control plane never recovered).
                    if response.status_code in (500, 502, 503, 504):
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
                    ProtocolError,
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
                status = getattr(response, "status_code", "unknown")
                if status in (401, 403):
                    # Fail closed: a 401/403 means the credentials were rejected.
                    # Surface this distinctly (not as a generic transient failure)
                    # so revoked/invalid keys are detectable rather than silently
                    # nulling the token and retrying a doomed credential.
                    logging.error(
                        "RefreshToken auth REJECTED by server (HTTP %s): credentials invalid/revoked. "
                        "Not a transient error — token will not be reissued until credentials are fixed.",
                        status,
                    )
                error_msg = f"Error response from the auth server in RefreshToken (status: {status}): {getattr(response, 'text', 'No response text')}"
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
                # SECURITY: never log res_dict here — it carries the raw refreshToken.
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
        # Hold the re-entrant lock across the reset AND the refresh so no other
        # thread can observe the transient bearer_token is None state.
        with self._refresh_lock:
            self.bearer_token = None
            self.expiry_time = None
            self.set_bearer_token()


class AuthToken(_RefreshLockPicklingMixin, AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(
        self,
        access_key,
        secret_key,
        refresh_token,
    ):
        self.bearer_token = None
        # Instance-level (re-entrant) lock: see RefreshToken.__init__.
        self._refresh_lock = threading.RLock()
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
                    # Retry on transient server errors (500, 502, 503, 504).
                    # 500 is included deliberately: a transient backend fault must
                    # not instantly null the token with no retry (root cause of the
                    # 2026-06-03 61h gateway outage, where a ~2min backend 500
                    # zeroed the bearer token and the control plane never recovered).
                    if response.status_code in (500, 502, 503, 504):
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
                    ProtocolError,
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
                status = getattr(response, "status_code", "unknown")
                if status in (401, 403):
                    # Fail closed: 401/403 == credentials rejected. Log distinctly
                    # so an invalid/revoked key is detectable rather than being
                    # absorbed as a generic non-200 and retried indefinitely.
                    logging.error(
                        "AuthToken auth REJECTED by server (HTTP %s): credentials invalid/revoked. "
                        "Not a transient error — token will not be reissued until credentials are fixed.",
                        status,
                    )
                error_msg = f"Error response from the auth server in AuthToken (status: {status}): {getattr(response, 'text', 'No response text')}"
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
        # Hold the re-entrant lock across the reset AND the refresh so no other
        # thread can observe the transient bearer_token is None state.
        with self._refresh_lock:
            self.bearer_token = None
            self.expiry_time = None
            self.set_bearer_token()
