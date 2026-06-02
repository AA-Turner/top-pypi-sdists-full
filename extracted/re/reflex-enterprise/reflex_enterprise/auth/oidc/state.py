"""Reflex state for OIDC authentication."""

import asyncio
import base64
import contextlib
import dataclasses
import datetime
import hashlib
import logging
import random
import secrets
import sys
import time
import uuid
from collections.abc import AsyncGenerator, Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Coroutine, Literal, Sequence
from urllib.parse import parse_qsl, urlencode, urlparse

import reflex as rx
from joserfc.jwt import Token
from reflex.event import EventSpec, EventType, IndividualEventType
from reflex.state import Delta
from reflex.vars import BaseStateMeta

from reflex_enterprise.app import AppEnterprise
from reflex_enterprise.auth.cookie import HTTPCookie
from reflex_enterprise.auth.oidc.config import ConfigMixin
from reflex_enterprise.auth.oidc.types import OIDCUserInfo, is_ok
from reflex_enterprise.auth.oidc.utils import compute_at_hash, verify_jwt
from reflex_enterprise.components.message_listener import (
    CLOSE_POPUP,
    POST_MESSAGE_AND_CLOSE_POPUP,
    WINDOW_OPEN,
    WindowMessage,
    message_listener,
)
from reflex_enterprise.utils import (
    call_event_from_computed_var,
    chain_event_out_of_band,
)

logger = logging.getLogger("reflex_enterprise.auth.oidc")
# Time in seconds to cache access token in computed var (adjusted dynamically
# based on token expiry)
ACCESS_TOKEN_CACHE_INTERVAL = 60  # 1 minute
USERINFO_CACHE_INTERVAL = 1800  # 30 minutes

COOKIE_MAX_AGE = 604800
COOKIE_ACCESS_TOKEN = HTTPCookie(
    max_age=COOKIE_MAX_AGE,
    secure=True,
    same_site="strict",
    _sync_on_set=False,
)
COOKIE_ID_TOKEN = HTTPCookie(
    max_age=COOKIE_MAX_AGE,
    secure=True,
    same_site="strict",
    _sync_on_set=False,
)
COOKIE_REFRESH_TOKEN = HTTPCookie(
    max_age=COOKIE_MAX_AGE,
    secure=True,
    same_site="strict",
    _sync_on_set=False,
)
COOKIE_GRANTED_SCOPES = HTTPCookie(
    max_age=COOKIE_MAX_AGE,
    secure=True,
    same_site="strict",
    _sync_on_set=False,
)


class UserinfoFetchError(RuntimeError):
    """Exception raised when fetching userinfo fails."""


class MissingUserinfoEndpointError(RuntimeError):
    """Exception raised when the OIDC issuer does not have a userinfo endpoint."""


class MissingAccessTokenError(RuntimeError):
    """Exception raised when an access token is required but not available."""


class NestedExceptionError(Exception):
    """Exception raised when an error occurs in a nested error context."""


class DefaultUserErrorMessage(str):
    """Sentinel value for default user error message."""


class IsIframedState(rx.State):
    """State to determine if the app is running inside an iframe.

    Attributes:
        checked_this_session: Whether the iframe check has been performed in this session.
        is_iframed: Whether the app is running inside an iframe.
    """

    checked_this_session: rx.Field[bool] = rx.field(False)
    is_iframed: rx.Field[bool] = rx.field(False)

    @rx.event
    def check_if_iframed(self):
        """Run a short client-side check to determine whether the page is iframed.

        The result is reported to `check_if_iframed_cb`.
        """
        if self.checked_this_session:
            return
        self.checked_this_session = True
        return rx.call_function(
            """() => {
    try {
        return window.self !== window.top;
    } catch (e) {
        // This catch block handles potential security errors (Same-Origin Policy)
        // if the iframe content and the parent are from different origins.
        // In such cases, access to window.top might be restricted, implying it's in an iframe.
        return true;
    }
}""",
            callback=self.__class__.check_if_iframed_cb,
        )

    @rx.event
    def check_if_iframed_cb(self, is_iframed: bool):
        """Callback invoked with the iframe detection result.

        Args:
            is_iframed: True if the page is inside an iframe or cross-origin
                access prevented detection.
        """
        self.is_iframed = is_iframed


@dataclasses.dataclass
class AccessTokenMetadata:
    """Metadata about an access token stored in a cookie."""

    access_token: str
    expires_at: float

    @classmethod
    def from_exchange(
        cls, exchange_response: Mapping[str, Any]
    ) -> "AccessTokenMetadata":
        """Create AccessTokenMetadata from token exchange response.

        Args:
            exchange_response: The token exchange response from the OIDC provider.

        Returns:
            An AccessTokenMetadata instance.
        """
        access_token = exchange_response["access_token"]
        expires_in = exchange_response.get("expires_in")
        if expires_in is not None:
            expires_at = time.time() + int(expires_in)
        else:
            expires_at = float("inf")
        return cls(
            access_token=access_token,
            expires_at=expires_at,
        )

    @classmethod
    def from_cookie_value(cls, at_data_qs: str) -> "AccessTokenMetadata | None":
        """Parse the access token metadata from the cookie value.

        Args:
            at_data_qs: The access token data query string from the cookie.

        Returns:
            An AccessTokenMetadata instance or None if parsing fails.
        """
        try:
            data = dict(parse_qsl(at_data_qs))
        except Exception:
            return None
        if not data or not (access_token := data.get("access_token")):
            return None
        try:
            expires_at = float(data["expires_at"])
        except (KeyError, TypeError, ValueError):
            expires_at = float("inf")
        return cls(
            access_token=access_token,
            expires_at=expires_at,
        )

    def to_cookie_value(self) -> str:
        """Serialize the access token metadata to a cookie value.

        Returns:
            The access token metadata as a query string.
        """
        return urlencode(
            {
                "access_token": self.access_token,
                "expires_at": str(self.expires_at),
            }
        )

    def sha256_hash(self) -> str:
        """Compute a SHA-256 hash of the access token for change detection."""
        return hashlib.sha256(self.access_token.encode("utf-8")).hexdigest()


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class RefreshQueueEntry:
    """Data about a queued access token refresh."""

    queued_at: float
    queued_by_session_id: str


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class UserinfoCacheEntry:
    """Data about cached userinfo."""

    userinfo: OIDCUserInfo
    updated_at: float
    access_token_hash: str


class OIDCCookieMeta(BaseStateMeta):
    """Meta class to assign HTTPCookie descriptors to the final class."""

    if TYPE_CHECKING:
        _access_token_data: str = COOKIE_ACCESS_TOKEN
        _id_token: str = COOKIE_ID_TOKEN
        _granted_scopes: str = COOKIE_GRANTED_SCOPES
        _refresh_token: str = COOKIE_REFRESH_TOKEN

    def __new__(cls, name: str, bases: tuple, attrs: dict[str, Any], **kwargs):
        """Assign HTTPCookie descriptors to the final class."""
        if not kwargs.get("mixin"):
            inherited_fields = {}
            for base in bases[::-1]:
                if hasattr(base, "__inherited_fields__"):
                    inherited_fields.update(base.__inherited_fields__)

            provider = attrs.get("__provider__", "generic")
            annotations = attrs.setdefault("__annotations__", {})

            def apply_cookie(name: str, cookie: HTTPCookie):
                if name not in inherited_fields:
                    annotations[name] = str
                    attrs[name] = cookie._replace(name=f"_oidc_{provider}{name}")

            apply_cookie("_access_token_data", COOKIE_ACCESS_TOKEN)
            apply_cookie("_id_token", COOKIE_ID_TOKEN)
            apply_cookie("_refresh_token", COOKIE_REFRESH_TOKEN)
            apply_cookie("_granted_scopes", COOKIE_GRANTED_SCOPES)
        return super().__new__(cls, name, bases, attrs, **kwargs)


class OIDCAuthState(ConfigMixin, rx.State, mixin=True, metaclass=OIDCCookieMeta):
    """Reflex base state class for managing OIDC authentication flows.

    This state class handles the OAuth 2.0 Authorization Code flow with PKCE
    for OIDC authentication, including token storage, validation, and user
    information retrieval.

    Users should subclass this state and set the `__provider__` attribute
    to specify the OIDC provider (e.g., "okta", "databricks"), and supply
    appropriate environment variables for client ID, secret, and issuer URI.

    For example:
    ```python
    class OktaAuthState(OIDCAuthState, rx.State):
        __provider__ = "okta"
    ```

    Then use the `OktaAuthState.get_login_button()` method to render a login
    button in your app.

    Cookies from metaclass OIDCCookieMeta:
        _access_token: The OAuth 2.0 access token stored in cookie.
        _id_token: The OpenID Connect ID token stored in cookie.
        _granted_scopes: The scopes granted for the access_token stored in cookie.
        _refresh_token: The OAuth 2.0 refresh token stored in cookie.

    Attributes:
        from_popup: Whether the current page was opened as a popup.
        user_error_message: A user-friendly error message to display in the UI when authentication errors occur.
        latest_access_token_hash_ls: A hash of the latest access token stored in local storage for cross-tab synchronization.

        redirect_to_url: URL to redirect to after successful authentication, stored in SessionStorage.
        app_state: Random state parameter for CSRF protection, stored in SessionStorage.
        code_verifier: PKCE code verifier for secure authorization, stored in SessionStorage.
        _requested_scopes: Scopes requested during authentication.
        _expected_at_hash: Expected at_hash value for access token validation in ID token.

        _error_context_depth: Internal counter to track nested error contexts for proper logging indentation.
        _last_error_message: Error message for authentication failures.
        _last_error_txid: Transaction ID for correlating logs related to a specific authentication flow.

        _last_auth_callback_exchange: The token exchange response from the last authentication callback, used for debugging and logging.
        _last_access_token_hash: A hash of the last access token seen in this session, updated when the access token changes.
        _last_refresh_queued_entry: Data about the last queued access token refresh, used to avoid duplicate refreshes.
        _cached_userinfo: Cached user information retrieved from the userinfo endpoint.

    ClassVars:
        _tasks: A set of currently running asyncio tasks spawned by this state, used to keep references to tasks until they complete to avoid garbage collection.
    """

    __provider__: ClassVar[str] = "generic"
    _has_registered_endpoints: ClassVar[bool] = False
    _logger: ClassVar[logging.Logger] = logger
    _default_user_error_message: ClassVar[str] = (
        "Authentication error, please try again."
    )

    from_popup: bool = False
    user_error_message: str
    # Auto-sync local storage var allows other tabs to know when they need to re-sync cookies.
    latest_access_token_hash_ls: rx.Field[str] = rx.field(rx.LocalStorage(sync=True))

    redirect_to_url: str = rx.SessionStorage()
    app_state: str = rx.SessionStorage()
    code_verifier: str = rx.SessionStorage()
    _requested_scopes: str = "openid email profile"
    _expected_at_hash: str | None = None
    _error_context_depth: int = 0
    _last_error_message: str
    _last_error_txid: str
    _last_auth_callback_exchange: dict | None = None
    _last_access_token_hash: str | None = None
    _last_refresh_queued_entry: RefreshQueueEntry | None = None
    _cached_userinfo: UserinfoCacheEntry | None = None

    _tasks: ClassVar[set[asyncio.Task]] = set()

    def _queue_async_task(self, coro: Coroutine) -> asyncio.Task:
        """Helper to queue an async task from sync context.

        Keeps a reference to the task until it is complete to avoid garbage collection.

        Args:
            coro: The coroutine to run as a task.

        Returns:
            The created asyncio.Task.
        """
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    @rx.var(
        interval=COOKIE_MAX_AGE,
        deps=["_access_token_data"],
        auto_deps=False,
        initial_value=None,
    )
    def _access_token_metadata(self) -> AccessTokenMetadata | None:
        """Get the access token metadata from the cookie."""
        return AccessTokenMetadata.from_cookie_value(self._access_token_data)

    @rx.var(
        interval=ACCESS_TOKEN_CACHE_INTERVAL,
        deps=["_access_token_metadata"],
        auto_deps=False,
        initial_value="",
    )
    async def _access_token(self) -> str:
        """Get the access token from the cookie."""
        if (at_metadata := self._access_token_metadata) is not None:
            return at_metadata.access_token
        return ""

    @rx.event
    async def update_access_token_hash_in_browser(
        self, redirect_url: str | None = None
    ):
        """Update the current access token hash in local storage to notify other tabs.

        This is a callback for HTTPCookie.sync and should only be called after
        the updated cookies are set in the browser.

        Args:
            redirect_url: Optional URL to redirect to after syncing the access token hash.
        """
        if (at_metadata := self._access_token_metadata) is not None:
            if (
                current_at_hash := at_metadata.sha256_hash()
            ) != self.latest_access_token_hash_ls:
                # Set the local storage var to notify other tabs/windows.
                self.latest_access_token_hash_ls = current_at_hash
        else:
            self.latest_access_token_hash_ls = ""
        if redirect_url:
            return rx.redirect(redirect_url)

    @rx.event
    async def update_access_token_hash_in_session(self):
        """Update the current access token hash in state to notice refreshed tokens."""
        if (at_metadata := self._access_token_metadata) is not None:
            if (current_at_hash := at_metadata.sha256_hash()) != (
                last_access_token_hash := self._last_access_token_hash
            ):
                self._last_access_token_hash = current_at_hash
                if (
                    self.__class__._on_refresh_access_token
                    is not OIDCAuthState._on_refresh_access_token
                    or self.__class__._on_access_token_change
                    is not OIDCAuthState._on_access_token_change
                ):
                    is_refresh = last_access_token_hash is not None
                    return self.__class__.on_access_token_change(is_refresh)
        else:
            self._last_access_token_hash = None

    def _cookie_sync_token_update(
        self,
        callback: EventType[Any] | None = None,
        redirect_url: str | None = None,
    ) -> EventSpec:
        """Queue a cookie sync from the browser and update the access token hash after."""
        if callback is not None and not isinstance(callback, Sequence):
            callback = [callback]
        return HTTPCookie.sync(
            callback=[
                self.__class__.update_access_token_hash_in_browser(redirect_url),
                *(callback if callback is not None else []),
            ]
        )

    def _handle_latest_access_token_hash_ls_in_delta(self, delta: Delta) -> Delta:
        """Check the latest_access_token_hash_ls from the frontend delta.

        This avoids a local storage sync race where multiple tab sessions fight
        to update the latest_access_token_hash_ls, particularly when their
        access_token is NOT up to date.

        In case this session's _access_token hash does not match the latest
        hash, or if there is no current access token, we remove the
        latest_access_token_hash_ls from the delta so it does not trigger
        updates on other tabs, allowing this session to perform the cookie sync
        and bring in the latest access token from the browser.

        If the latest hash does match the access token that we have, and there
        is a refresh token available, trigger_access_token_refresh to
        proactively refresh the access token before it expires.

        Args:
            delta: The original delta.

        Returns:
            The modified delta with latest_access_token_hash_ls removed if the
            access token is not up to date.
        """
        subdelta = delta.get(self.get_full_name())
        key = self.__class__.latest_access_token_hash_ls._js_expr.rpartition(".")[2]
        if (
            subdelta is not None
            and (latest_access_token_hash := subdelta.get(key)) is not None
        ):
            at_metadata = self._access_token_metadata
            if not latest_access_token_hash:
                # If token hash was cleared: reset everything
                if at_metadata is not None:
                    self._queue_async_task(
                        call_event_from_computed_var(self, self.__class__.reset_auth)
                    )
            else:
                events: list[IndividualEventType] = []
                if self._last_access_token_hash != latest_access_token_hash:
                    events.append(self.__class__.update_access_token_hash_in_session())
                # Check if this session needs to perform a cookie sync:
                if (
                    # Session has no token, but the browser has a token hash.
                    at_metadata is None
                    # Session has a token, but browser token does not match session's token hash.
                    or latest_access_token_hash != at_metadata.sha256_hash()
                ):
                    events.append(self.__class__.trigger_access_token_refresh())
                    self._queue_async_task(
                        chain_event_out_of_band(self, HTTPCookie.sync(callback=events))
                    )
                    # Don't include the key in the delta to avoid triggering updates in other tabs.
                    del subdelta[key]
                else:
                    if self._should_trigger_access_token_refresh():
                        # Tokens are synced, so queue a frontend task to trigger proactive access token refresh if possible.
                        events.append(self.__class__.trigger_access_token_refresh())
                    if events:
                        self._queue_async_task(
                            call_event_from_computed_var(self, events)
                        )
        return delta

    async def _update_access_token_cache_expiry(self):
        """Update the access token computed var cache expiry based on token metadata."""
        if (at_metadata := self._access_token_metadata) is not None:
            new_update_time = datetime.datetime.fromtimestamp(
                at_metadata.expires_at
            ) - datetime.timedelta(seconds=ACCESS_TOKEN_CACHE_INTERVAL)
            setattr(
                self,
                self.computed_vars["_access_token"]._last_updated_attr,
                new_update_time,
            )

    @rx.var(deps=["_access_token", "_id_token"], auto_deps=False, initial_value=False)
    async def has_any_token(self) -> bool:
        """Whether any authentication token is present."""
        has_any_token = bool((await self._access_token) or self._id_token)
        # This var updates whenever _access_token changes, so fix the _access_token cache expiry time here.
        await self._update_access_token_cache_expiry()
        return has_any_token

    @rx.var(initial_value="")
    def granted_scopes(self) -> str:
        """Get the granted scopes from the cookie."""
        return self._granted_scopes or ""

    def _reset_auth(self):
        """Reset authentication state and clear tokens."""
        del self._access_token_data
        del self._id_token
        del self._refresh_token
        del self._granted_scopes
        self.latest_access_token_hash_ls = ""
        self._expected_at_hash = None
        self._last_access_token_hash = None
        self._last_refresh_queued_entry = None
        self._cached_userinfo = None
        self._logger.debug(self._format_log_message("Reset auth cookies"))

    @rx.event
    def reset_auth(self):
        """Reset authentication state then sync cookies."""
        self._reset_auth()
        return HTTPCookie.sync()

    async def _verify_jwt(self, token_json: str) -> Token:
        """Subclasses can override to customize id_token JWT verification.

        Args:
            token_json: The JWT as a string.

        Returns:
            The verified Token object.
        """
        return await verify_jwt(
            token_json,
            issuer=await self._issuer_uri(),
            audience=await self._client_id(),
            at_hash=self._expected_at_hash,
            client=self._http_client(),
            valid_issuers=await self._valid_issuers(),
        )

    async def _validate_tokens(self) -> bool:
        """Subclasses can override to customize access_token and id_token validation.

        Returns:
            True if tokens are valid, False otherwise.
        """
        if not await self._access_token or not self._id_token:
            return False

        try:
            async with self._error_context(
                "ID Token verification",
                user_error_message=None,
            ) as errors:
                await self._verify_jwt(self._id_token)
        except NestedExceptionError:
            # Verification failed inside a nested error context; treat as invalid.
            return False
        return not errors

    def _ensure_last_error_txid(self):
        """Ensure there is a transaction ID for logging correlation."""
        if not self._last_error_txid:
            self._last_error_txid = uuid.uuid4().hex

    def _clear_last_error(self):
        """Called when starting a new auth operation to clear previous saved errors."""
        self.user_error_message = ""
        self._error_context_depth = 0
        self._last_error_message = ""
        self._last_error_txid = ""
        self._ensure_last_error_txid()

    def _format_log_message(self, msg: str) -> str:
        """Format a log message with client token and transaction ID.

        Args:
            msg: The message to format.

        Returns:
            The formatted log message.
        """
        error_context_prefix = "".join(
            [
                " " if self._error_context_depth > 1 else "",
                "─" * max(self._error_context_depth - 1, 0),
            ]
        )
        self._ensure_last_error_txid()
        return (
            f"{self.router.session.client_token} "
            f"[txid={self._last_error_txid}]{error_context_prefix} {msg}"
        )

    def _set_last_error_message(
        self, msg: str, user_error_message: str | None = DefaultUserErrorMessage()
    ):
        """Store and log the last error message and user-facing error message.

        Args:
            msg: The error message to set and log.
            user_error_message: Message to show to the user via toast.

        Returns:
            A toast component with the user error message, or None.
        """
        self._last_error_message = msg
        self._logger.info(
            self._format_log_message(self._last_error_message), exc_info=sys.exc_info()
        )
        if isinstance(user_error_message, DefaultUserErrorMessage):
            user_error_message = self._default_user_error_message
        if user_error_message is not None:
            self.user_error_message = user_error_message
            return rx.toast.error(user_error_message)
        return None

    @contextlib.asynccontextmanager
    async def _error_context(
        self,
        operation: str,
        user_error_message: str | None = DefaultUserErrorMessage(),
        clear_last_error: bool = False,
    ):
        """Async context manager to wrap auth operations and handle errors.

        Args:
            operation: Description of the operation being performed.
            user_error_message: Message to show to the user via toast on error.
            clear_last_error: Whether to clear the last error at the start.

        Yields: a list of exceptions encountered in the block.
        """
        if clear_last_error:
            self._clear_last_error()
        self._error_context_depth += 1
        self._logger.debug(self._format_log_message(f"{operation}"))
        exceptions = []
        try:
            yield exceptions
        except NestedExceptionError as nested_exc:
            exceptions.append(nested_exc.__cause__ or nested_exc)
            # No re-logging or re-toasting for nested exceptions, just stop processing.
            return
        except Exception as e:
            exceptions.append(e)
            if (
                error_toast := self._set_last_error_message(
                    f"{operation} failed: {e}",
                    user_error_message=user_error_message,
                )
            ) is not None:
                await chain_event_out_of_band(self, error_toast)
            if self._error_context_depth > 1:
                # Also raise the error in nested contexts to stop further processing.
                raise NestedExceptionError from e
        finally:
            self._error_context_depth = max(self._error_context_depth - 1, 0)

    @rx.var(initial_value=False)
    def has_error(self) -> bool:
        """Whether there was an authentication error."""
        return bool(self._last_error_message)

    @rx.var
    def last_error_txid(self) -> str:
        """Get the last error transaction ID for logging correlation."""
        return self._last_error_txid

    async def _fetch_userinfo(self) -> OIDCUserInfo:
        """Retrievfe data from the OIDC userinfo endpoint.

        Returns:
            The userinfo data as a dictionary.

        Raises:
            UserinfoFetchError: If the userinfo request is made and returns a non-OK
                response.
            MissingUserinfoEndpointError: If the OIDC issuer does not have a userinfo endpoint.
            MissingAccessTokenError: If there is no access token available to fetch userinfo.
        """
        if not (userinfo_endpoint := await self._issuer_endpoint("userinfo_endpoint")):
            raise MissingUserinfoEndpointError(
                "OIDC issuer does not have a userinfo endpoint"
            )
        if not (access_token := await self._access_token):
            raise MissingAccessTokenError("No access token available to fetch userinfo")
        async with self._http_client().get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
        ) as resp:
            if not is_ok(resp):
                raise UserinfoFetchError(
                    f"Userinfo request failed with status {resp.status}: {await resp.text()}"
                )
            return await resp.json()  # pyright: ignore[reportReturnType]

    async def _get_id_token_claims(self) -> OIDCUserInfo:
        """Get the claims from the ID token."""
        return (await self._verify_jwt(self._id_token)).claims  # pyright: ignore[reportReturnType]

    async def _try_refresh_access_token(self) -> str:
        """Refresh the access token using the refresh token, if available.

        Wraps `_refresh_access_token` with the current access token's
        `expires_at` so the de-duplication check is performed when there is
        existing metadata.

        Returns:
            The new access token on success, or empty string when no refresh
            token is available or the refresh failed.
        """
        if not self._refresh_token:
            return ""
        at_metadata = self._access_token_metadata
        return await self._refresh_access_token(
            at_metadata.expires_at if at_metadata is not None else None
        )

    async def _get_userinfo(self) -> OIDCUserInfo | None:
        """Get the authenticated user's information from OIDC token."""
        if not await self._validate_tokens():
            await self._try_refresh_access_token()
            if not await self._validate_tokens():
                await call_event_from_computed_var(self, self.__class__.reset_auth)
                return None
        # Get the latest userinfo
        async with self._error_context("Fetching userinfo", user_error_message=None):
            try:
                return await self._fetch_userinfo()
            except MissingUserinfoEndpointError:
                # Have to just trust the ID token claims.
                return await self._get_id_token_claims()
            except UserinfoFetchError:
                # The access token may have been rejected; refresh and retry.
                if not self._refresh_token:
                    raise
                await self._try_refresh_access_token()
                if not await self._validate_tokens():
                    await call_event_from_computed_var(self, self.__class__.reset_auth)
                    raise
                return await self._fetch_userinfo()

    @rx.var(
        interval=datetime.timedelta(seconds=USERINFO_CACHE_INTERVAL),
        deps=["_access_token", "_id_token", "_cached_userinfo"],
        auto_deps=False,
        initial_value=None,
    )
    async def userinfo(self) -> OIDCUserInfo | None:
        """Get the authenticated user's information from OIDC token.

        This property retrieves the user's profile information from the OIDC
        userinfo endpoint using the stored access token. The result is cached
        for 30 minutes and automatically revalidated.

        Returns:
            OIDCUserInfo or subclass containing user profile data if authentication is valid,
            None if tokens are invalid or the request fails.
        """
        if (
            (at_metadata := self._access_token_metadata) is None
            or not self._id_token
            or not await self._access_token
        ):
            return None
        current_at_hash = None
        if (
            self._cached_userinfo is None
            or time.time() - self._cached_userinfo.updated_at > USERINFO_CACHE_INTERVAL
            or (
                self._cached_userinfo.access_token_hash
                != (current_at_hash := at_metadata.sha256_hash())
            )
        ) and (userinfo := await self._get_userinfo()) is not None:
            self._cached_userinfo = UserinfoCacheEntry(
                userinfo=userinfo,
                updated_at=time.time(),
                access_token_hash=current_at_hash or at_metadata.sha256_hash(),
            )
        return (
            self._cached_userinfo.userinfo
            if self._cached_userinfo is not None
            else None
        )

    def _redirect_uri(self) -> str:
        """Construct the redirect URI for the OAuth 2.0 authorization code flow.

        This must match the redirect URI registered with the OIDC provider.

        Returns:
            The redirect URI as a string.
        """
        current_url = urlparse(self.router.url)
        return current_url._replace(
            path=self._authorization_code_endpoint(),
            query=None,
            fragment=None,
        ).geturl()

    def _index_uri(self) -> str:
        """Get the app's index URI.

        Returns:
            The current page's url without path, query, or fragment.
        """
        current_url = urlparse(self.router.url)
        return current_url._replace(path="/", query=None, fragment=None).geturl()

    async def _use_popup_flow(self) -> bool:
        """Determine whether to use the popup flow for authentication.

        This can be used to detect if the app is embedded in a context where
        redirects are not possible (e.g., inside another app's iframe) and
        switch to a popup-based flow instead.

        Returns:
            True if the popup flow should be used, False otherwise.
        """
        return await self.get_var_value(IsIframedState.is_iframed)

    async def _popup_login_url(self) -> str:
        """Get the popup login endpoint URL.

        Returns:
            The popup login endpoint URL.
        """
        return self._popup_login_endpoint()

    async def _popup_login_options(self) -> tuple[str, str]:
        """Get the popup login window name and features.

        Returns:
            A tuple of (window_name, window_features).
        """
        window_name = f"{self.__provider__}_popup_login"
        window_features = "width=600,height=600"
        return window_name, window_features

    _popup_logout_options = _popup_login_options

    @rx.event
    async def redirect_to_login_popup(self):
        """Open a small popup window to initiate the login flow.

        This is used when the app detects it's embedded and needs to open a
        dedicated popup for the authorization flow.
        """
        window_name, window_features = await self._popup_login_options()
        return rx.call_script(
            WINDOW_OPEN(
                await self._popup_login_url(),
                window_name,
                window_features,
            )
        )

    async def _popup_logout_url(self) -> str:
        """Get the popup logout endpoint URL.

        Returns:
            The popup logout endpoint URL.
        """
        return self._popup_logout_endpoint()

    @rx.event
    async def redirect_to_logout_popup(self):
        """Open a small popup window to initiate the logout flow."""
        window_name, window_features = await self._popup_logout_options()
        return rx.call_script(
            WINDOW_OPEN(
                await self._popup_logout_url(),
                window_name,
                window_features,
            )
        )

    @rx.event
    def set_from_popup(self, from_popup: bool):
        """Set whether the current page was opened as a popup."""
        self.from_popup = from_popup
        if from_popup:
            return self.__class__.popup_on_load()

    @rx.event
    def popup_on_load(self):
        """Handler to run when a popup login or logout page is loaded."""

    async def _post_auth_message_payload(self) -> dict[str, str]:
        """Get the token payload to send to the opener via postMessage.

        Received by `on_iframe_auth_success` and passed to `_set_tokens`.
        """
        return {
            "access_token": self._access_token_data,
            "id_token": self._id_token,
            "refresh_token": self._refresh_token,
            "scope": self._granted_scopes,
        }

    @rx.event
    async def post_auth_message(self):
        """Post tokens to the opening window and close the popup.

        Used to transfer tokens to an opener that cannot read the popup's
        cookies or localStorage (e.g., the opener is iframed in a different
        storage partition).
        """
        async with self._error_context("Posting auth message to opener"):
            payload = {
                "type": f"post_auth_{self.__provider__}",
                **(await self._post_auth_message_payload()),
            }
            return rx.call_script(
                POST_MESSAGE_AND_CLOSE_POPUP(payload, self.origin, 500)
            )

    @rx.event
    async def post_logout_message(self):
        """Post a logout notification to the opening window and close the popup."""
        async with self._error_context("Posting logout message to opener"):
            payload = {
                "type": f"post_logout_{self.__provider__}",
            }
            return rx.call_script(
                POST_MESSAGE_AND_CLOSE_POPUP(payload, self.origin, 500)
            )

    @rx.event
    async def on_iframe_auth_success(self, event: WindowMessage):
        """Handle an auth or logout message posted from the popup.

        Persists the tokens to this state's cookies (or clears them on logout)
        so the opener stays in sync with the popup.

        Args:
            event: The window message; `data["type"]` must be either
                `post_auth_<provider>` or `post_logout_<provider>`.
        """
        msg_type = event["data"].get("type")
        if msg_type == f"post_logout_{self.__provider__}":
            return self.__class__.reset_auth()
        if msg_type != f"post_auth_{self.__provider__}":
            return
        event_data = dict(event["data"])
        event_data.pop("type", None)
        new_access_token = event_data.pop("access_token", "")
        new_id_token = event_data.pop("id_token", None) or None
        new_refresh_token = event_data.pop("refresh_token", None) or None
        new_granted_scopes = event_data.pop("scope", None) or None
        # Skip the redundant set + cookie sync if the tokens already match.
        if (
            new_access_token == self._access_token_data
            and (new_id_token or "") == (self._id_token or "")
            and (new_refresh_token or "") == (self._refresh_token or "")
            and (new_granted_scopes or "") == (self._granted_scopes or "")
        ):
            return
        async with self._error_context(
            "Processing popup auth success", clear_last_error=True
        ):
            await self._set_tokens(
                access_token=new_access_token,
                id_token=new_id_token,
                refresh_token=new_refresh_token,
                granted_scopes=new_granted_scopes,
                **event_data,
            )
            return self._cookie_sync_token_update()

    async def _redirect_to_login_payload(self) -> dict:
        """Get the payload for initial authorization request.

        Returns:
            A dictionary containing any necessary parameters for login redirection.
        """
        # store app state and code verifier in session
        self.app_state = secrets.token_urlsafe(64)
        self.code_verifier = secrets.token_urlsafe(64)
        self.redirect_to_url = self.router.url

        # calculate code challenge
        hashed = hashlib.sha256(self.code_verifier.encode("ascii")).digest()
        encoded = base64.urlsafe_b64encode(hashed)
        code_challenge = encoded.decode("ascii").strip("=")

        # get request params
        return {
            "client_id": await self._client_id(),
            "redirect_uri": self._redirect_uri(),
            "scope": self._requested_scopes,
            "state": self.app_state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "response_type": "code",
            "response_mode": "query",
        }

    @rx.event
    async def redirect_to_login(self):
        """Initiate the OAuth 2.0 authorization code flow with PKCE.

        This method generates the necessary state and code verifier for PKCE,
        constructs the authorization URL, and redirects the user to OIDC
        authorization endpoint.

        If the user's token is already valid (popup flow), then post the tokens
        to the opener and close the popup.

        Returns:
            - If iframed, a script to open the login popup window.
            - If already authenticated in the popup, a post-authentication
              message to the opener followed by closing the popup window.
            - If already authenticated outside the popup, a success toast.
            - If login flow cannot be initiated due to error, None.
            - A redirect response to the provider's OIDC authorization endpoint
        """
        if not self.from_popup and await self._use_popup_flow():
            return self.__class__.redirect_to_login_popup()

        async with self._error_context("Processing login flow", clear_last_error=True):
            if (await self.userinfo) is not None:
                events: list[IndividualEventType] = [rx.toast("You are logged in.")]
                if self.from_popup:
                    # Hand off tokens to the opener and close this window.
                    events.append(self.__class__.post_auth_message)
                return events
        if await self.has_any_token:
            # Tokens were present but userinfo could not be fetched; clear the
            # now-untrustworthy cookies before initiating a new login.
            await call_event_from_computed_var(self, self.__class__.reset_auth)
        async with self._error_context("Building authorization request"):
            query_params = await self._redirect_to_login_payload()
            request_uri = f"{await self._issuer_endpoint('authorization_endpoint')}?{urlencode(query_params)}"
            return rx.redirect(request_uri)

    async def _redirect_to_logout_payload(self) -> dict[str, str]:
        """Get the payload for initiating logout request.

        Returns:
            A dictionary containing any necessary parameters for logout redirection.
        """
        self.app_state = secrets.token_urlsafe(64)
        query_params = {
            "state": self.app_state,
        }
        if self._id_token:
            query_params["id_token_hint"] = self._id_token
        post_logout_redirect_uri = self._index_uri()
        if self.from_popup:
            post_logout_redirect_uri = (
                post_logout_redirect_uri.rstrip("/") + await self._popup_logout_url()
            )
        query_params["post_logout_redirect_uri"] = post_logout_redirect_uri
        return query_params

    @rx.event
    async def redirect_to_logout(self):
        """Initiate the OAuth 2.0 logout flow.

        This method generates a new state parameter, constructs the logout URL
        with the ID token hint, and redirects the user to OIDC's logout endpoint.

        The user's tokens are cleared from cookies after this event.

        Returns:
            - If iframed, a script to open the logout popup window if supported by the provider.
            - If logout flow cannot be initiated due to error or omission, None.
            - A redirect response to the provider's OIDC end_session endpoint
        """
        from_popup = self.from_popup
        async with self._error_context(
            f"Processing logout flow ({from_popup=})",
            user_error_message="Logout error",
            clear_last_error=True,
        ):
            end_session_endpoint = await self._issuer_endpoint("end_session_endpoint")
            if await self._use_popup_flow():
                if end_session_endpoint:
                    # Open the logout popup when the provider gives a logout endpoint.
                    yield self.__class__.redirect_to_logout_popup
                else:
                    # Reset the tokens and the app is effectively logged out.
                    yield self.reset_auth()
                return
            if from_popup and not await self.has_any_token:
                # Re-entry after provider logout completed; just close.
                yield rx.call_script(CLOSE_POPUP(self.origin, 500))
                return
            try:
                if end_session_endpoint:
                    # Get the logout redirect payload while we still have the tokens.
                    query_params = await self._redirect_to_logout_payload()
                    # Redirect to initiate provider logout flow.
                    redirect_url = f"{end_session_endpoint}?{urlencode(query_params)}"
                else:
                    # No end_session_endpoint, so just redirect to the app index after clearing tokens.
                    redirect_url = self._index_uri()
            finally:
                # Clear browser tokens after user requested logout.
                self._reset_auth()
            if from_popup:
                # Notify the opener to clear its tokens too. The window-close
                # timer scheduled by post_logout_message is cancelled by the
                # subsequent navigation to the provider's logout endpoint.
                yield self.__class__.post_logout_message
            yield self._cookie_sync_token_update(redirect_url=redirect_url)

    async def _validate_auth_callback_request_params(
        self, request_params: Mapping[str, Any]
    ) -> Literal[True]:
        """Validate the auth callback request parameters.

        Args:
            request_params: The request parameters from the callback.

        Returns:
            True if the request parameters are valid.

        Raises:
            ValueError: If the request parameters are invalid.
        """
        app_state = request_params.get("state")
        if app_state != self.app_state:
            raise ValueError("App state mismatch. Possible CSRF attack.")
        return True

    async def _auth_callback_payload_from_request_params(
        self, request_params: Mapping[str, Any]
    ) -> dict[str, str]:
        """Get the payload for the token exchange request from auth callback request parameters.

        Args:
            request_params: The request parameters from the callback.

        Returns:
            A dictionary containing the necessary parameters for the auth callback.

        Raises:
            ValueError: If any required parameters are missing.
        """
        if not (code := request_params.get("code")):
            raise ValueError("No code provided in the callback.")
        query_params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self._redirect_uri(),
            "code_verifier": self.code_verifier,
            "scope": self._requested_scopes,
        }
        if not await self._client_secret():
            query_params["client_id"] = await self._client_id()
        return query_params

    async def _auth_callback_authorization_headers(self) -> dict[str, str] | None:
        """Get the authorization headers for the token exchange request.

        Returns:
            A dictionary containing the authorization headers if client_secret is set,
            None otherwise.
        """
        if client_secret := await self._client_secret():
            return {
                "Authorization": f"Basic {base64.b64encode(f'{await self._client_id()}:{client_secret}'.encode()).decode()}"
            }
        return None

    async def _validate_auth_callback_exchange(
        self, exchange: Mapping[str, Any]
    ) -> dict[str, Any] | None:
        """Validate the token exchange response from the auth callback.

        Subclasses may override this method to implement additional validation
        logic on the token exchange response.

        Args:
            exchange: The token exchange dictionary.

        Returns:
            The validated exchange dictionary if valid, None otherwise.

        Raises:
            ValueError: If the exchange is invalid.
        """
        if (
            (token_type := exchange.get("token_type")) is None
            or not isinstance(token_type, str)
            or token_type.lower().strip() != "bearer"
        ):
            raise ValueError(
                f"Unsupported token type {token_type!r}. Should be 'Bearer'."
            )
        return dict(exchange)

    async def _set_tokens_payload_from_exchange(
        self, exchange: Mapping[str, Any]
    ) -> dict[str, str]:
        """Get the payload for setting tokens from the token exchange.

        The returned value will be passed as keyword arguments to `_set_tokens`.

        Args:
            exchange: The token exchange dictionary.

        Returns:
            A dictionary containing the authentication tokens and scopes.
        """
        payload = {
            "access_token": AccessTokenMetadata.from_exchange(
                exchange
            ).to_cookie_value(),
        }
        if "id_token" in exchange:
            payload["id_token"] = exchange["id_token"]
        if "refresh_token" in exchange:
            payload["refresh_token"] = exchange["refresh_token"]
        if "scope" in exchange:
            payload["granted_scopes"] = exchange["scope"]
        return payload

    @rx.event
    async def auth_callback(self):
        """Handle the OAuth 2.0 authorization-code callback.

        This method is called when the user is redirected back from OIDC
        authorization endpoint. It validates the state parameter to prevent CSRF
        attacks, exchanges the authorization code for tokens using PKCE, and
        stores the tokens for future use.

        Returns:
            A redirect response to the original requested URL, or an error toast
            if authentication fails.
        """
        self._last_auth_callback_exchange = None
        async with self._error_context(
            "Processing auth callback", clear_last_error=True
        ):
            async with self._error_context("Validating auth callback request"):
                await self._validate_auth_callback_request_params(
                    self.router.url.query_parameters
                )
            async with self._error_context("Building token request payload"):
                query_params = await self._auth_callback_payload_from_request_params(
                    self.router.url.query_parameters
                )
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                if auth_headers := await self._auth_callback_authorization_headers():
                    headers.update(auth_headers)
            async with (
                self._error_context("Exchanging authorization code for tokens"),
                self._http_client().post(
                    await self._issuer_endpoint("token_endpoint"),
                    headers=headers,
                    data=query_params,
                ) as resp,
            ):
                if not is_ok(resp):
                    raise RuntimeError(
                        f"Token request failed with status {resp.status}: {await resp.text()}"
                    )
                if exchange := (
                    await self._validate_auth_callback_exchange(await resp.json())
                ):
                    self._last_auth_callback_exchange = exchange
                else:
                    return
            # Store tokens.
            async with self._error_context("Setting authentication tokens"):
                await self._set_tokens(
                    **await self._set_tokens_payload_from_exchange(
                        self._last_auth_callback_exchange
                    )
                )
                return self._cookie_sync_token_update(
                    redirect_url=self.redirect_to_url,
                )

    def _trigger_access_token_refresh_script(self, delay: float) -> EventSpec:
        """Generate JavaScript code to trigger access token refresh after a delay.

        Args:
            delay: The delay in seconds before triggering the refresh.

        Returns:
            An EventSpec representing the JavaScript code to set a timeout for refreshing the access token.
        """
        timer_ref = f"refs['rxe_oidc_{self.__provider__}_access_token_refresh_timer']"
        ls_last_updated_key = f"rxe_oidc_{self.__provider__}_last_access_token_update"
        do_refresh = HTTPCookie._get_sync_javascript_code().then(
            rx.Var.create(
                rx.event.EventChain.create(
                    self.__class__.do_access_token_refresh,
                    args_spec=rx.event.no_args_event_spec,
                    invocation=rx.vars.function.ArgsFunctionOperation.create(
                        args_names=["events"],
                        return_expr=rx.Var(
                            "queueEvents(events, {current: socket}, false, navigate, params)"
                        ),
                    ),
                )
            )
        )
        return rx.call_script(
            "const trigger_refresh = (delayMs) => {"
            f"let current_timer = {timer_ref};"
            "if (current_timer) {window.clearTimeout(current_timer);};"
            f"{timer_ref} = window.setTimeout(() => {{"
            f"delete {timer_ref};"
            f'if ((new Date()).getTime() - (parseInt(window.localStorage.getItem("{ls_last_updated_key}")) || 0) > {ACCESS_TOKEN_CACHE_INTERVAL * 1000}) {{'
            f'window.localStorage.setItem("{ls_last_updated_key}", (new Date()).getTime().toString());'
            f"{do_refresh!s};"
            f"}} else {{"
            f"trigger_refresh({ACCESS_TOKEN_CACHE_INTERVAL * 1000});"
            f"}}}}, delayMs);"
            f"}}; trigger_refresh({int(delay * 1000)});"
        )

    def _should_trigger_access_token_refresh(self) -> bool:
        """Determine whether an access token refresh should be triggered.

        This checks if there is valid access token metadata and a refresh token,
        and whether a refresh is not already queued by this session.

        Returns:
            True if an access token refresh should be triggered, False otherwise.
        """
        return bool(
            self._access_token_metadata is not None
            and self._refresh_token
            and (
                self._last_refresh_queued_entry is None
                or (
                    self.router.session.session_id
                    != self._last_refresh_queued_entry.queued_by_session_id
                )
                or (
                    time.time() - self._last_refresh_queued_entry.queued_at
                    > ACCESS_TOKEN_CACHE_INTERVAL
                )
            )
        )

    @rx.event
    async def trigger_access_token_refresh(self):
        """Trigger an access token refresh from the browser."""
        if (
            at_metadata := self._access_token_metadata
        ) is None or not self._should_trigger_access_token_refresh():
            return
        self._last_refresh_queued_entry = RefreshQueueEntry(
            queued_at=time.time(),
            queued_by_session_id=self.router.session.session_id,
        )
        expires_in = max(at_metadata.expires_at - time.time(), 0)
        # Add jitter to avoid multiple tabs refreshing at the same time.
        delay = max(
            expires_in
            - (1.5 * ACCESS_TOKEN_CACHE_INTERVAL)
            + random.uniform(0, ACCESS_TOKEN_CACHE_INTERVAL),
            0,
        )
        return self._trigger_access_token_refresh_script(delay)

    @rx.event
    async def do_access_token_refresh(self):
        """Initiate an access token refresh on the backend if needed.

        If the token is not imminently expiring (i.e. another tab already refreshed),
        then requeue the frontend refresh trigger to check again later.
        """
        if not self._refresh_token:
            return
        self._last_refresh_queued_entry = None
        at_metadata = self._access_token_metadata
        if at_metadata is not None:
            expires_in = max(at_metadata.expires_at - time.time(), 0)
            time_before_refresh = expires_in - ACCESS_TOKEN_CACHE_INTERVAL
            if time_before_refresh > 0:
                return self.__class__.trigger_access_token_refresh()
        await self._try_refresh_access_token()

    async def _refresh_access_token_payload(self) -> dict[str, str]:
        """Get the payload for refreshing the access token.

        Returns:
            A dictionary containing the necessary parameters for token refresh.
        """
        query_params = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
            "scope": self._requested_scopes,
        }
        if not await self._client_secret():
            query_params["client_id"] = await self._client_id()
        return query_params

    async def _on_access_token_change(
        self, new_access_token: str, refresh: bool = False
    ) -> Sequence[IndividualEventType] | None:
        """Called when the access token is set or refreshed.

        Args:
            new_access_token: The new access token value.
            refresh: Whether this change is due to a token refresh (True) or an initial set (False).

        Returns:
            An iterable of events to trigger in response to the access token change.
        """
        pass

    async def _on_refresh_access_token(
        self, new_access_token: str
    ) -> Sequence[IndividualEventType] | None:
        """Called when the access token is successfully refreshed.

        Args:
            new_access_token: The new access token value.

        Returns:
            An iterable of events to trigger in response to the access token refresh.
        """
        pass

    @rx.event
    async def on_access_token_change(
        self, refresh: bool = False
    ) -> AsyncGenerator[Sequence[IndividualEventType] | None]:
        """Event handler called when the access token is refreshed.

        Downstream implementations should override `_on_refresh_access_token` or
        `_on_access_token_change` to perform any necessary actions when the
        access token changes.
        """
        if (at_metadata := self._access_token_metadata) is not None:
            yield await self._on_access_token_change(at_metadata.access_token, refresh)
            if refresh:
                yield await self._on_refresh_access_token(at_metadata.access_token)

    async def _refresh_access_token(self, expires_at: float | None) -> str:
        """Refresh the access token using the refresh token.

        Args:
            expires_at: The expiration timestamp of the current access token,
                used to check if another task has already refreshed it. Pass
                ``None`` to skip the de-duplication check (e.g., when there is
                no current access token).

        Returns:
            The new access token as a string.

        Raises:
            Exception: If the token refresh fails.
        """
        if not self._refresh_token:
            # Cannot refresh without a refresh token.
            return ""
        if (
            expires_at is not None
            and (at_metadata := self._access_token_metadata) is not None
            and at_metadata.expires_at != expires_at
        ):
            # The token has already been refreshed by another task, so just return the current token.
            return at_metadata.access_token
        async with self._error_context("Refreshing access token"):
            query_params = await self._refresh_access_token_payload()
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            if auth_headers := await self._auth_callback_authorization_headers():
                headers.update(auth_headers)
            async with self._http_client().post(
                await self._issuer_endpoint("token_endpoint"),
                headers=headers,
                data=query_params,
            ) as resp:
                if is_ok(resp):
                    exchange = await self._validate_auth_callback_exchange(
                        await resp.json()
                    )
                    if not exchange:
                        raise ValueError("Invalid token refresh response.")
                    await self._set_tokens(
                        **await self._set_tokens_payload_from_exchange(exchange)
                    )
                    await chain_event_out_of_band(
                        self, self._cookie_sync_token_update()
                    )
                    return exchange.get("access_token", "")
        # If we failed to refresh, reset the tokens.
        await chain_event_out_of_band(self, self.__class__.reset_auth)
        return ""

    async def _set_tokens(
        self,
        access_token: str,
        id_token: str | None = None,
        refresh_token: str | None = None,
        granted_scopes: str | None = None,
        **kwargs,
    ):
        """Validate and set the authentication tokens in state.

        Subclasses may override this method when handling additional data
        returned from the token exchange that must be persisted in the state or
        validated in some way.

        Args:
            access_token: The urlencoded OAuth 2.0 access token and expires_at value.
            id_token: The OpenID Connect ID token.
            refresh_token: The OAuth 2.0 refresh token.
            granted_scopes: The scopes granted for the access_token.
            kwargs: Additional keyword arguments (ignored in default implementation).
        """
        self._access_token_data = access_token
        if id_token is not None:
            self._id_token = id_token
        if refresh_token is not None:
            self._refresh_token = refresh_token
        if granted_scopes is not None:
            self._granted_scopes = granted_scopes
        self._expected_at_hash = None

        # compute at_hash and store for additional validation
        if id_token is not None:
            try:
                token = await self._verify_jwt(id_token)
                alg = token.header.get("alg")
                at_hash = compute_at_hash(await self._access_token, alg)
                # store expected at_hash in a transient property (not persisted)
                self._expected_at_hash = at_hash
            except Exception:
                self._expected_at_hash = None

        # Validate again after setting expected_at_hash
        if not await self._validate_tokens():
            self.reset_auth()

    @rx.var
    def origin(self) -> str:
        """Return the app origin URL (used as postMessage target origin)."""
        return self._index_uri().rstrip("/")

    @rx.state._override_base_method
    def get_delta(self) -> Delta:
        """Override BaseState.get_delta to perform post-event filtering."""
        return self._handle_latest_access_token_hash_ls_in_delta(super().get_delta())

    @classmethod
    def get_login_button(cls, *children) -> rx.Component:
        """Return a login button component that initiates OIDC auth.

        If `children` are provided they will be placed inside the clickable
        element; otherwise a default button label is used. When iframed, the
        component also mounts a message listener to receive auth tokens
        posted from the popup window.
        """
        cls.register_auth_endpoints()
        if not children:
            children = [rx.button(f"Login with {cls.display_name()}")]
        return rx.el.div(
            *children,
            rx.cond(
                IsIframedState.is_iframed,
                message_listener(
                    allowed_origin=cls.origin,
                    on_message=cls.on_iframe_auth_success,
                    filter_attributes={
                        "type": f"^post_(auth|logout)_{cls.__provider__}$",
                    },
                ),
            ),
            on_click=cls.redirect_to_login,
            on_mount=rx.cond(
                ~IsIframedState.checked_this_session,
                IsIframedState.check_if_iframed.throttle(100),
                rx.noop(),
            ),
            width="fit-content",
        )

    @classmethod
    def get_state_hydrating_component(cls) -> rx.Component:
        """Loading spinner shown before state is hydrated."""
        return rx.vstack(
            rx.spinner(),
            align="center",
            justify="center",
            height="50vh",
            width="100%",
        )

    @classmethod
    def _with_hydrated(cls, *components: rx.Component) -> rx.Component:
        """Wrap components to wait for state hydration before rendering.

        Args:
            components: The components to render after hydration.

        Returns:
            A component that shows a loading spinner until state is hydrated,
            then renders the provided components.
        """
        return rx.cond(
            rx.State.is_hydrated,
            rx.fragment(*components),
            cls.get_state_hydrating_component(),
        )

    @classmethod
    def get_error_component(
        cls,
        operation: Literal["authentication", "logout"],
        suggestion: str,
        error_id: rx.Var[str],
    ) -> rx.Component:
        """Return a component to display an error message.

        Args:
            operation: The operation during which the error occurred.
            suggestion: A suggestion for the user to resolve the error.
            error_id: The error transaction ID for logging correlation.

        Returns:
            A component that displays the error message, suggestion, and error ID.
        """
        return rx.container(
            rx.vstack(
                rx.heading(f"An error occurred during {operation}."),
                rx.text(suggestion),
                rx.text(
                    "An administrator may provide more information about error ID: ",
                    rx.badge(error_id),
                ),
            )
        )

    @classmethod
    def get_authentication_error_component(cls) -> rx.Component:
        """Return a component to display an authentication error message."""
        return cls.get_error_component(
            operation="authentication",
            suggestion="Please close this window and try again.",
            error_id=cls.last_error_txid,
        )

    @classmethod
    def get_logout_error_component(cls) -> rx.Component:
        """Return a component to display a logout error message."""
        return cls.get_error_component(
            operation="logout",
            suggestion="Please close this window and clear browser cookies to manually log out.",
            error_id=cls.last_error_txid,
        )

    @classmethod
    def get_validating_authentication_component(cls) -> rx.Component:
        """Return a component to display a validating authentication message."""
        return rx.container(
            rx.hstack(
                rx.heading("Validating Authentication..."),
                rx.spinner(),
                width="50%",
                justify="between",
            )
        )

    @classmethod
    def get_redirecting_component(cls) -> rx.Component:
        """Return a component to display a redirecting message."""
        return rx.container(rx.heading("Redirecting to app..."))

    @classmethod
    def get_logout_process_component(cls) -> rx.Component:
        """Return a component to display a logout process message."""
        return rx.container(
            rx.hstack(
                rx.heading("Complete logout process."),
                rx.spinner(),
                width="50%",
                justify="between",
            )
        )

    @classmethod
    def get_logout_success_component(cls) -> rx.Component:
        """Return a component to display a logout success message."""
        return rx.container(
            rx.heading("You are logged out. You may close this window.")
        )

    @classmethod
    def get_authentication_loading_page(cls) -> rx.Component:
        """Small loading page shown while authentication is validated.

        This page is registered by the package as the callback target when the
        authorization response is being processed.
        """
        return cls._with_hydrated(
            rx.cond(
                cls.has_error,
                cls.get_authentication_error_component(),
                rx.cond(
                    ~cls.userinfo,
                    cls.get_validating_authentication_component(),
                    cls.get_redirecting_component(),
                ),
            ),
        )

    @classmethod
    def get_authentication_popup_logout(cls) -> rx.Component:
        """Simple page shown during the logout flow.

        Registered at `/_reflex_oidc_{provider}/popup-logout` to complete the sign-out handshake.
        """
        return cls._with_hydrated(
            rx.cond(
                cls.has_error,
                cls.get_logout_error_component(),
                rx.cond(
                    cls.has_any_token,
                    cls.get_logout_process_component(),
                    cls.get_logout_success_component(),
                ),
            ),
        )

    @classmethod
    def display_name(cls) -> str:
        """Return the display name of the authentication provider."""
        return cls.__provider__.title()

    @classmethod
    def register_auth_endpoints(cls, app: AppEnterprise | None = None):
        """Register the Okta authentication endpoints with the Reflex app.

        This function sets up the necessary OAuth callback endpoint for handling
        authentication responses from OIDC providers. The callback endpoint
        handles the authorization code exchange and redirects users.
        """
        if app is None and cls._has_registered_endpoints:
            return
        if app is None:
            from reflex.utils.prerequisites import get_app

            app = get_app().app
        if not isinstance(app, AppEnterprise):
            raise TypeError("The app must be an instance of reflex_enterprise.App.")
        cls._has_registered_endpoints = True
        context = {"sitemap": None}
        app.add_page(
            cls.get_authentication_loading_page(),
            route=cls._authorization_code_endpoint(),
            on_load=cls.auth_callback,
            title=f"{cls.display_name()} Auth Callback",
            context=context,
        )
        app.add_page(
            cls.get_authentication_loading_page(),
            route=cls._popup_login_endpoint(),
            on_load=[
                cls.set_from_popup(True),
                cls.redirect_to_login,
            ],
            title=f"{cls.display_name()} Auth Initiator",
            context=context,
        )
        app.add_page(
            cls.get_authentication_popup_logout(),
            route=cls._popup_logout_endpoint(),
            on_load=[
                cls.set_from_popup(True),
                cls.redirect_to_logout,
            ],
            title=f"{cls.display_name()} Auth Logout",
            context=context,
        )
