from __future__ import annotations

import asyncio
import hashlib
import json
import socket
import tempfile
import time
import webbrowser
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any, Literal, cast
from urllib.parse import urlparse

import anyio
import httpx
import structlog
from mcp.client.auth import (
    OAuthClientProvider,
    OAuthRegistrationError,
    OAuthTokenError,
    TokenStorage,
)
from mcp.shared.auth import (
    OAuthClientInformationFull,
    OAuthClientMetadata,
    OAuthMetadata,
    OAuthToken,
)
from pydantic import AnyHttpUrl, ValidationError
from runlayer_cli import oauth_guidance
from runlayer_cli.oauth_callback import create_oauth_callback_server
from runlayer_cli.paths import get_runlayer_dir


logger = structlog.get_logger(__name__)
TokenEndpointAuthMethod = Literal[
    "none", "client_secret_post", "client_secret_basic", "private_key_jwt"
]


def _is_expired_authorization_code_error(exc: OAuthTokenError) -> bool:
    # mcp 1.x exposes this failure only through SDK-formatted IdP text.
    # Fail closed when either side changes its wording.
    message = str(exc).lower()
    return (
        "token exchange failed" in message
        and "invalid_grant" in message
        and "authorization code" in message
        and ("expired" in message or "unknown" in message)
    )


class OAuthCallbackTimeoutError(TimeoutError):
    """The local OAuth callback server timed out waiting for the redirect.

    Distinct subclass so flow telemetry can classify it as
    ``oauth_flow_timeout`` (a user never finished the browser flow) instead of
    a generic network ``timeout`` (see ``error_classification.py``).
    """


def default_cache_dir() -> Path:
    return get_runlayer_dir() / "oauth-mcp-client-cache"


def get_free_port() -> int:
    """
    Find and return a free port on localhost.

    Returns:
        An available port number
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))
        s.listen(1)
        port = s.getsockname()[1]
        return port


def _ensure_callback_port_available(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("127.0.0.1", port))
            s.listen(1)
        except OSError as e:
            raise RuntimeError(
                f"OAuth callback port {port} is already in use. Another "
                "`runlayer run` OAuth flow may be running - finish it first, "
                "or pass a different --oauth-callback-port (and allowlist "
                "http://localhost:<port>/callback for that port in your IdP)."
            ) from e


def get_browser_lockfile_path(server_url: str) -> Path:
    """
    Get a deterministic lockfile path for a server URL.

    Args:
        server_url: The server URL to generate a lockfile for

    Returns:
        Path to the lockfile in the system's temporary directory
    """
    # Create a deterministic hash of the server URL
    url_hash = hashlib.sha256(server_url.encode()).hexdigest()[:16]
    temp_dir = Path(tempfile.gettempdir())
    return temp_dir / f"runlayer_oauth_browser_{url_hash}.lock"


def _reset_browser_lockfile(server_url: str) -> None:
    try:
        get_browser_lockfile_path(server_url).unlink(missing_ok=True)
    except OSError as exc:
        logger.warning(
            "oauth_browser_lock_reset_failed",
            server_url=server_url,
            error=str(exc),
        )


def should_open_browser(server_url: str, window_seconds: float = 3.0) -> bool:
    """
    Check if a browser should be opened for the given server.

    Prevents opening multiple browser tabs within the specified time window.
    Uses atomic file creation to avoid race conditions.

    Args:
        server_url: The server URL to check
        window_seconds: Time window in seconds (default: 3.0)

    Returns:
        True if browser should be opened, False otherwise
    """
    lockfile = get_browser_lockfile_path(server_url)
    current_time = time.time()

    try:
        # Try to atomically create the lockfile (prevents race condition)
        with lockfile.open("x") as f:
            f.write(str(current_time))
        return True

    except FileExistsError:
        # Lockfile exists - check if it's still valid
        try:
            last_opened = float(lockfile.read_text().strip())
            time_since_last = current_time - last_opened

            if time_since_last < window_seconds:
                logger.debug(
                    f"Skipping browser open for {server_url} "
                    f"(last opened {time_since_last:.1f}s ago)"
                )
                return False

            # Lockfile is stale - try to update it
            lockfile.write_text(str(current_time))
            return True

        except (OSError, ValueError) as e:
            logger.debug(f"Error reading lockfile: {e}")
            # If we can't read the lockfile, try to recreate it
            try:
                lockfile.unlink()
                lockfile.write_text(str(current_time))
                return True
            except OSError:
                # If all else fails, allow browser to open
                return True

    except (OSError, ValueError) as e:
        # If anything goes wrong with lockfile creation, err on the side of opening the browser
        logger.debug(f"Error checking browser lockfile: {e}")
        return True


class FileTokenStorage(TokenStorage):
    """
    File-based token storage implementation for OAuth credentials and tokens.
    Implements the mcp.client.auth.TokenStorage protocol.

    Each instance is tied to a specific server URL for proper token isolation.
    """

    def __init__(self, server_url: str, cache_dir: Path | None = None):
        """Initialize storage for a specific server URL."""
        self.server_url = server_url
        self.cache_dir = cache_dir or default_cache_dir()
        self.cache_dir.mkdir(exist_ok=True, parents=True)

    @staticmethod
    def get_base_url(url: str) -> str:
        """Extract the base URL (scheme + host + path) from a URL.

        The path is preserved so that cache keys are unique per MCP endpoint
        and so the URL matches the ``resource`` field returned by the PRM
        endpoint (required by MCP SDK >= 1.27.0 / RFC 8707).
        """
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    def get_cache_key(self) -> str:
        """Generate a safe filesystem key from the server's base URL."""
        base_url = self.get_base_url(self.server_url)
        return (
            base_url.replace("://", "_")
            .replace(".", "_")
            .replace("/", "_")
            .replace(":", "_")
        )

    def _get_file_path(self, file_type: Literal["client_info", "tokens"]) -> Path:
        """Get the file path for the specified cache file type."""
        key = self.get_cache_key()
        return self.cache_dir / f"{key}_{file_type}.json"

    async def get_tokens(self) -> OAuthToken | None:
        """Load tokens from file storage."""
        path = self._get_file_path("tokens")

        try:
            data = json.loads(path.read_text())

            # Load token from format
            if "token" in data:
                token = OAuthToken.model_validate(data["token"])
            else:
                # Old format - just the token fields directly
                token = OAuthToken.model_validate(data)

            return token
        except (FileNotFoundError, json.JSONDecodeError, ValidationError) as e:
            logger.info(
                f"Could not load tokens for {self.get_base_url(self.server_url)}: {e}"
            )
            return None

    def get_token_expiry_time(self) -> float | None:
        """Load the absolute expiration timestamp from file storage."""
        path = self._get_file_path("tokens")
        try:
            data = json.loads(path.read_text())
            # New format includes expiry_time alongside token
            expiry_time = data.get("expiry_time")
            if expiry_time is not None and not isinstance(expiry_time, (int, float)):
                logger.warning(
                    "Invalid expiry_time in token cache",
                    expiry_time=expiry_time,
                    server_url=self.get_base_url(self.server_url),
                )
                return None
            return expiry_time
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def get_oauth_metadata(self) -> dict[str, Any] | None:
        """Load OAuth metadata from client_info file storage."""
        path = self._get_file_path("client_info")
        try:
            data = json.loads(path.read_text())
            return data.get("oauth_metadata")
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def get_callback_port(self) -> int | None:
        """Load a cached localhost callback port from client information."""
        path = self._get_file_path("client_info")
        try:
            data = json.loads(path.read_text())
            redirect_uris = data.get("redirect_uris")
            if not isinstance(redirect_uris, list) or not redirect_uris:
                return None
            redirect_uri = redirect_uris[0]
            if not isinstance(redirect_uri, str):
                return None
            parsed = urlparse(redirect_uri)
            if parsed.scheme != "http" or parsed.hostname != "localhost":
                return None
            return parsed.port
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return None

    def set_oauth_metadata(self, oauth_metadata: dict[str, Any]) -> None:
        """Save OAuth metadata to client_info file storage."""
        path = self._get_file_path("client_info")
        try:
            # Load existing data
            data = json.loads(path.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, create new structure
            data = {}

        # Add/update oauth_metadata
        data["oauth_metadata"] = oauth_metadata
        path.write_text(json.dumps(data, indent=2))
        logger.info(f"Saved OAuth metadata for {self.get_base_url(self.server_url)}")

    async def set_tokens(self, tokens: OAuthToken) -> None:
        """Save tokens to file storage."""

        # Calculate absolute expiration timestamp
        # We store this alongside the token because OAuthToken only contains a relative `expires_in` field
        expiry_time = (
            time.time() + tokens.expires_in if tokens.expires_in is not None else None
        )

        # Store token and expiry_time
        path = self._get_file_path("tokens")
        data = {
            "token": tokens.model_dump(mode="json"),
            "expiry_time": expiry_time,
        }
        path.write_text(json.dumps(data, indent=2))

        logger.info(
            f"Saved tokens for {self.get_base_url(self.server_url)}",
            expiry_time=expiry_time,
        )

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        """Load client information from file storage."""
        path = self._get_file_path("client_info")

        try:
            data = json.loads(path.read_text())

            # Extract client_info (the file contains both client_info and oauth_metadata)
            # The parent class expects just the client_info fields
            if "client_id" in data:
                # New format: client_info fields are at root level alongside oauth_metadata
                # Create a copy without oauth_metadata for validation
                client_info_data = {
                    k: v for k, v in data.items() if k != "oauth_metadata"
                }
                return OAuthClientInformationFull.model_validate(client_info_data)
            else:
                # Invalid format
                logger.warning(
                    f"Invalid cache format for {self.get_base_url(self.server_url)} "
                    "(missing client_id). Clearing cache."
                )
                self.clear()
                return None

        except (FileNotFoundError, json.JSONDecodeError, ValidationError) as e:
            logger.info(
                f"Could not load client info for {self.get_base_url(self.server_url)}: {e}"
            )
            return None

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        """Save client information to file storage, preserving oauth_metadata if it exists."""
        path = self._get_file_path("client_info")

        # Try to preserve existing oauth_metadata
        existing_oauth_metadata = None
        try:
            existing_data = json.loads(path.read_text())
            existing_oauth_metadata = existing_data.get("oauth_metadata")
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # Start with client_info data
        data = client_info.model_dump(mode="json")

        # Preserve oauth_metadata if it exists
        if existing_oauth_metadata is not None:
            data["oauth_metadata"] = existing_oauth_metadata

        path.write_text(json.dumps(data, indent=2))
        logger.info(f"Saved client info for {self.get_base_url(self.server_url)}")

    def clear(self) -> None:
        """Clear all cached data for this server."""
        file_types: list[Literal["client_info", "tokens"]] = [
            "client_info",
            "tokens",
        ]
        for file_type in file_types:
            path = self._get_file_path(file_type)
            path.unlink(missing_ok=True)
        logger.info(f"Cleared OAuth cache for {self.get_base_url(self.server_url)}")

    def clear_tokens(self) -> None:
        """Clear cached tokens while preserving client and OAuth metadata."""
        self._get_file_path("tokens").unlink(missing_ok=True)

    @classmethod
    def clear_all(cls, cache_dir: Path | None = None) -> None:
        """Clear all cached data for all servers."""
        cache_dir = cache_dir or default_cache_dir()
        if not cache_dir.exists():
            return

        file_types: list[Literal["client_info", "tokens"]] = [
            "client_info",
            "tokens",
        ]
        for file_type in file_types:
            for file in cache_dir.glob(f"*_{file_type}.json"):
                file.unlink(missing_ok=True)
        logger.info("Cleared all OAuth client cache data.")


class OAuth(OAuthClientProvider):
    """
    OAuth client provider for MCP servers with browser-based authentication.

    This class provides OAuth authentication for Runlayer clients by opening
    a browser for user authorization and running a local callback server.
    """

    def __init__(
        self,
        mcp_url: str,
        scopes: str | list[str] | None = None,
        client_name: str = "Runlayer Client",
        token_storage_cache_dir: Path | None = None,
        additional_client_metadata: dict[str, Any] | None = None,
        callback_port: int | None = None,
        manual_client_id: str | None = None,
        manual_client_secret: str | None = None,
        token_endpoint_auth_method: str | None = None,
    ):
        """
        Initialize OAuth client provider for an MCP server.

        Args:
            mcp_url: Full URL to the MCP endpoint (e.g. "http://host/mcp/sse/")
            scopes: OAuth scopes to request. Can be a
            space-separated string or a list of strings.
            client_name: Name for this client during registration
            token_storage_cache_dir: Directory for FileTokenStorage
            additional_client_metadata: Extra fields for OAuthClientMetadata
            callback_port: Fixed port for OAuth callback (default: random available port)
        """
        parsed_url = urlparse(mcp_url)
        # Pass the full URL (scheme + host + path) as server_url so it matches
        # the `resource` field returned by the PRM endpoint. MCP SDK >= 1.27.0
        # validates this match per RFC 8707 and raises OAuthFlowError on mismatch,
        # which silently aborts the entire OAuth flow.
        server_base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        storage = FileTokenStorage(
            server_url=server_base_url, cache_dir=token_storage_cache_dir
        )

        # Keep the redirect URI stable across CLI runs. OAuth providers often
        # require it to match the URI registered for the client exactly.
        self.redirect_port = (
            callback_port or storage.get_callback_port() or get_free_port()
        )
        redirect_uri = f"http://localhost:{self.redirect_port}/callback"

        if isinstance(scopes, list):
            scopes = " ".join(scopes)

        client_metadata = OAuthClientMetadata(
            client_name=client_name,
            redirect_uris=[AnyHttpUrl(redirect_uri)],
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
            # token_endpoint_auth_method="client_secret_post",
            scope=scopes,
            **(additional_client_metadata or {}),
        )

        self.manual_client_info = None
        if manual_client_id is not None:
            # Empty string = absent, matching the backend's truthiness-based
            # completeness rule — authenticating with an empty secret can
            # only fail the token exchange.
            manual_client_secret = manual_client_secret or None
            # No secret = public PKCE client; the token endpoint must not
            # expect client authentication. This overrides any conflicting
            # confidential preference — client_secret_post/basic without a
            # secret can only fail the token exchange.
            if manual_client_secret is None:
                resolved_auth_method = "none"
            else:
                resolved_auth_method = (
                    token_endpoint_auth_method or "client_secret_post"
                )
            self.manual_client_info = OAuthClientInformationFull(
                client_id=manual_client_id,
                client_secret=manual_client_secret,
                redirect_uris=[AnyHttpUrl(redirect_uri)],
                token_endpoint_auth_method=cast(
                    TokenEndpointAuthMethod,
                    resolved_auth_method,
                ),
            )

        # Store server_base_url for use in callback_handler
        self.server_base_url = server_base_url

        # Initialize parent class
        super().__init__(
            server_url=server_base_url,
            client_metadata=client_metadata,
            storage=storage,
            redirect_handler=self.redirect_handler,
            callback_handler=self.callback_handler,
        )

    async def _initialize(self) -> None:
        """
        Override parent's _initialize to properly calculate token expiry and restore OAuth metadata.

        The parent class loads tokens from storage but doesn't calculate
        the token_expiry_time, which causes is_token_valid() to always
        return True (since token_expiry_time is None). This prevents
        token refresh from ever being triggered.

        We use an absolute expiration timestamp stored separately to ensure
        the relative `expires_in` field that we receive when we save the tokens is respected across CLI restarts.

        Additionally, we restore oauth_metadata which is needed for token refresh but not cached by the parent class.

        Finally, when a manual OAuth client is configured we seed it into the
        context, invalidating cached tokens minted for a different client_id.
        """
        # Call parent's initialization to load tokens and client info
        await super()._initialize()

        if self.manual_client_info is not None:
            cached_client_id = (
                self.context.client_info.client_id
                if self.context.client_info is not None
                else None
            )
            # Invalidate only on client_id change: rotating just the secret or
            # auth method keeps cached tokens; server-side expiry forces re-auth.
            if (
                self.context.current_tokens is not None
                and cached_client_id != self.manual_client_info.client_id
            ):
                if isinstance(self.context.storage, FileTokenStorage):
                    self.context.storage.clear_tokens()
                self.context.current_tokens = None
            self.context.client_info = self.manual_client_info
            await self.context.storage.set_client_info(self.manual_client_info)

        logger.info(
            "OAuth context after initialization",
            has_tokens=bool(self.context.current_tokens),
            has_client_info=bool(self.context.client_info),
            token_expiry_time=self.context.token_expiry_time,
            has_oauth_metadata=bool(self.context.oauth_metadata),
        )

        if isinstance(self.context.storage, FileTokenStorage):
            # If we loaded tokens, restore the absolute expiry time
            if self.context.current_tokens:
                # Get expiry time if using FileTokenStorage
                expiry_time = self.context.storage.get_token_expiry_time()

                if expiry_time:
                    self.context.token_expiry_time = expiry_time
                    logger.info(
                        "Initialized tokens with stored expiry",
                        token_expiry_time=expiry_time,
                        seconds_until_expiry=expiry_time - time.time(),
                    )

            # Restore oauth_metadata if available - critical for token refresh
            oauth_metadata_dict = self.context.storage.get_oauth_metadata()
            if oauth_metadata_dict:
                try:
                    self.context.oauth_metadata = OAuthMetadata.model_validate(
                        oauth_metadata_dict
                    )
                    logger.info(
                        "Restored OAuth metadata from cache",
                        token_endpoint=str(self.context.oauth_metadata.token_endpoint)
                        if self.context.oauth_metadata.token_endpoint
                        else None,
                    )
                except ValidationError as e:
                    logger.warning(
                        f"Failed to validate cached OAuth metadata: {e}",
                    )

    async def _handle_token_response(self, response: httpx.Response) -> None:
        """
        Override parent's _handle_token_response to persist oauth_metadata after successful token acquisition.

        The parent class discovers oauth_metadata during the 401 handling in async_auth_flow,
        but doesn't persist it. We need to save it so that token refresh can use the correct
        token endpoint URL on subsequent CLI runs.
        """
        # Let parent handle the token response (validates and saves tokens)
        await super()._handle_token_response(response)

        # Now save oauth_metadata if we have it - this is critical for token refresh
        if self.context.oauth_metadata and isinstance(
            self.context.storage, FileTokenStorage
        ):
            self.context.storage.set_oauth_metadata(
                self.context.oauth_metadata.model_dump(mode="json")
            )
            logger.info(
                "Saved OAuth metadata to cache",
                token_endpoint=str(self.context.oauth_metadata.token_endpoint)
                if self.context.oauth_metadata.token_endpoint
                else None,
            )

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        """Drive the parent auth flow with bounded OAuth recovery and DCR guidance.

        For the observed consumed/expired authorization-code failure, retry once
        after dropping the in-memory token and header, resetting browser
        deduplication, and forcing the MCP SDK to reload storage. Persisted tokens
        stay intact so the retry can adopt one written by another process.

        When the upstream IdP rejects dynamic client registration with a 4xx
        (e.g. Okta's ``403 E0000005 Invalid session``), the mcp SDK raises an
        OAuthRegistrationError whose message is the raw IdP body — no hint
        that the fix is Manual OAuth in the Runlayer server settings. Re-raise
        with actionable guidance (sanitized/truncated original kept for
        support); non-4xx registration errors pass through unchanged.
        """
        retried_expired_authorization_code = False
        while True:
            inner = super().async_auth_flow(request)
            try:
                response: httpx.Response | None = None
                while True:
                    try:
                        if response is None:
                            next_request = await inner.__anext__()
                        else:
                            next_request = await inner.asend(response)
                    except StopAsyncIteration:
                        return
                    response = yield next_request
            except OAuthTokenError as exc:
                if (
                    retried_expired_authorization_code
                    or not _is_expired_authorization_code_error(exc)
                ):
                    raise
                retried_expired_authorization_code = True
                # Memory-only: another process may have persisted a fresh token.
                self.context.clear_tokens()
                _reset_browser_lockfile(self.server_base_url)
                request.headers.pop("Authorization", None)
                # mcp 1.x has no public re-init API; this gate reloads storage.
                self._initialized = False
                logger.warning(
                    "oauth_authorization_code_expired_retrying",
                    server_url=self.server_base_url,
                )
            except OAuthRegistrationError as exc:
                guidance = oauth_guidance.classify_registration_failure(str(exc))
                if guidance is None:
                    raise
                logger.error(
                    "oauth_client_registration_rejected",
                    server_url=self.server_base_url,
                    guidance=guidance,
                )
                raise OAuthRegistrationError(guidance) from exc

    async def redirect_handler(self, authorization_url: str) -> None:
        """Open browser for authorization, with protection against multiple tabs."""
        logger.info(f"OAuth authorization URL: {authorization_url}")
        # The flow now waits on a human in a browser; record it so timeouts
        # elsewhere (e.g. the tools/list upstream bound) can explain that the
        # IdP must allow http://localhost:<port>/callback instead of
        # surfacing a bare timeout.
        oauth_guidance.mark_oauth_flow_started(self.redirect_port)

        # Only open browser if we haven't opened one recently for this server
        if should_open_browser(self.server_base_url):
            webbrowser.open(authorization_url)
        else:
            logger.info(
                "Skipping browser open - a tab was recently opened for this server. "
                "Please use the existing browser tab to complete authorization."
            )

    async def callback_handler(self) -> tuple[str, str | None]:
        """Handle OAuth callback and return (auth_code, state)."""
        # Create a future to capture the OAuth response
        response_future = asyncio.get_running_loop().create_future()
        oauth_guidance.mark_oauth_flow_started(self.redirect_port)
        _ensure_callback_port_available(self.redirect_port)

        # Create server with the future
        server = create_oauth_callback_server(
            port=self.redirect_port,
            server_url=self.server_base_url,
            response_future=response_future,
        )

        # Run server until response is received with timeout logic
        async with anyio.create_task_group() as tg:
            tg.start_soon(server.serve)
            logger.info(
                f"OAuth callback server started at http://localhost:{self.redirect_port}"
            )

            TIMEOUT = 300.0  # 5 minute timeout
            try:
                with anyio.fail_after(TIMEOUT):
                    auth_code, state = await response_future
                    # The browser callback delivered an auth code — the flow
                    # is no longer waiting on a human. (Deliberately NOT
                    # cleared on timeout/cancellation: a flow that died
                    # waiting is exactly what the pending-timeout guidance
                    # describes; the staleness window self-heals the marker.)
                    oauth_guidance.mark_oauth_flow_finished()
                    return auth_code, state
            except TimeoutError:
                guidance = oauth_guidance.oauth_pending_timeout_message(
                    self.redirect_port
                )
                logger.error(
                    "oauth_callback_timed_out",
                    callback_port=self.redirect_port,
                    timeout_seconds=TIMEOUT,
                    guidance=guidance,
                )
                raise OAuthCallbackTimeoutError(
                    f"OAuth callback timed out after {TIMEOUT} seconds. {guidance}"
                )
            finally:
                server.should_exit = True
                await anyio.sleep(0.1)  # Allow server to shutdown gracefully
                tg.cancel_scope.cancel()
