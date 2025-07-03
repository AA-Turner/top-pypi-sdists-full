"""OAuth 2.1 authentication manager for MCP servers."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Tuple, List
from pathlib import Path
import httpx
import logging
import json
import time
import secrets
import base64
import hashlib
import asyncio
from urllib.parse import urlencode
import typer

from mcp_cli.auth.utils import generate_code_challenge, generate_code_verifier

from .discovery import discover_mcp_oauth_config
from ..exceptions import (
    MCPOAuthError,
    NotOAuthCompliantError,
    OAuthDiscoveryError,
    OAuthClientRegistrationError,
    OAuthAuthorizationError,
    OAuthTokenExchangeError
)
from .config import OAuthConfig
from ..types import OAuthClientData, OAuthServerData, OAuthTokens

logger = logging.getLogger(__name__)


class WebserverClient:
    def __init__(self, config: OAuthConfig):
        self.config = config

    async def poll_for_code(self, state: str, timeout: int = 300) -> str:
        poll_url = f"{self.config.redirect_service_base_url}{self.config.redirect_poll_path}/{state}"

        auth_header = self.config.auth_header
        poll_count = 0
        httpx_retry_count = 0

        start_time = time.time()
        async with httpx.AsyncClient() as client:
            while time.time() - start_time < timeout:
                poll_count += 1

                try:
                    response = await client.get(poll_url, timeout=10.0, headers=auth_header)

                    if response.status_code == 200:
                        data = response.json()

                        if code := data.get('code'):
                            logger.info(f"  ✓ Authorization code received after {poll_count} polls")
                            return code

                        if error := data.get('error'):
                            raise OAuthAuthorizationError(f"Authorization denied: {error}")

                    elif response.status_code == 404:
                        # State not found yet, keep polling
                        pass
                    else:
                        logger.warning(f"Unexpected status code from redirect service: {response.status_code}")
                        raise OAuthAuthorizationError(f"Authorization error: {response.status_code} {response.text}")

                    if poll_count % 5 == 0:  # Log every 10 seconds
                        elapsed = int(time.time() - start_time)
                        logger.debug(f"  Still polling... ({elapsed}s elapsed)")
                        typer.secho(f"⏳ Still waiting... ({elapsed}s)", fg=typer.colors.YELLOW)

                except httpx.RequestError as e:
                    httpx_retry_count += 1
                    if httpx_retry_count < 3:
                        logger.warning(f"  Poll request {poll_count} failed: {e}")
                    else:
                        raise OAuthAuthorizationError(f"Error getting authorization code after 3 retries: {e}")

                await asyncio.sleep(2)

        raise asyncio.TimeoutError("Authorization timeout - no code received")

    async def get_org_tokens(self):
        auth_header = self.config.auth_header
        url = f"{self.config.redirect_service_base_url}{self.config.tokens_path}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=auth_header)
            response.raise_for_status()
            return response.json()

    async def put_org_tokens(self, server_name: str, oauth_data: OAuthServerData):
        url = f"{self.config.redirect_service_base_url}{self.config.tokens_path}/{server_name}"
        auth_header = self.config.auth_header
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=oauth_data.model_dump(mode="json"), headers=auth_header)
            response.raise_for_status()
            return response.json()
        
    async def delete_tokens(self, server_name: str):
        url = f"{self.config.redirect_service_base_url}{self.config.tokens_path}/{server_name}"
        auth_header = self.config.auth_header
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=auth_header)
            response.raise_for_status()
            return response.json()


class TokenStorage:
    """
    Token file storage for OAuth tokens.
    """
    def __init__(self, config: OAuthConfig, webserver_client: WebserverClient):
        self.config = config
        self._tokens_cache_path = config.get_base_cache_dir().joinpath("tokens.json")
        self.webserver_client = webserver_client

    async def save_tokens(self, server_name: str, tokens: Dict[str, Any], oauth_client_data: OAuthClientData):
        """Save tokens, client data, and endpoints in our format."""
        # Load existing data
        tokens_file = self._tokens_cache_path
        if tokens_file.exists():
            raw_data = json.loads(tokens_file.read_text())
            # Convert raw data back to Pydantic models
            all_data: Dict[str, OAuthServerData] = {}
            for name, data in raw_data.items():
                all_data[name] = OAuthServerData.model_validate(data)
        else:
            all_data: Dict[str, OAuthServerData] = {}

        # Save all data for this server
        tokens_data: OAuthTokens = OAuthTokens(
            access_token=tokens['access_token'],
            expires_at=tokens['expires_at'],
            refresh_token=tokens.get('refresh_token'),
            scope=tokens.get('scope'),
            obtained_at=tokens['obtained_at']
        )
        oauth_data: OAuthServerData = OAuthServerData(
            server_name=server_name,
            tokens=tokens_data,
            oauth_client_data=oauth_client_data,
        )
        all_data[server_name] = oauth_data

        # Convert to dictionaries for JSON serialization
        serializable_data = {name: data.model_dump(mode="json") for name, data in all_data.items()}
        
        # Write back
        tokens_file.write_text(json.dumps(serializable_data, indent=2))
        logger.info(f"Saved tokens for '{server_name}' into local cache")

        await self.webserver_client.put_org_tokens(server_name, oauth_data)

    async def _download_tokens(self):
        """Download tokens from the server."""
        tokens = await self.webserver_client.get_org_tokens()
        self._tokens_cache_path.write_text(json.dumps(tokens, indent=2))

    async def load_tokens(self, server_name: str) -> Optional[OAuthServerData]:
        """Load tokens for a specific server."""
        tokens_file = self._tokens_cache_path

        if not tokens_file.exists():
            logger.info(f"No tokens found for '{server_name}', downloading from server")
            await self._download_tokens()

        raw_data = json.loads(tokens_file.read_text())
        server_data = raw_data.get(server_name)
        if server_data:
            return OAuthServerData.model_validate(server_data)
        return None

    async def clear_tokens(self, server_name: str):
        """Clear tokens for a specific server."""
        tokens_file = self._tokens_cache_path
        if not tokens_file.exists():
            return
        
        raw_data = json.loads(tokens_file.read_text())
        raw_data.pop(server_name, None)
        tokens_file.write_text(json.dumps(raw_data, indent=2))
        
        await self.webserver_client.delete_tokens(server_name)


class OAuthManager:
    """Manages OAuth 2.1 authentication for MCP servers."""

    def __init__(self):
        """Initialize OAuth manager with token cache."""

        # Load OAuth configuration
        self.config = OAuthConfig()
        self.webserver_client = WebserverClient(self.config)
        self.token_storage = TokenStorage(self.config, self.webserver_client)


    async def _perform_oauth_discovery(self, server_config: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 1: Discover and validate OAuth metadata."""

        mcp_server_url = server_config.get('url')
        if not mcp_server_url:
            raise NotOAuthCompliantError("Server URL is required")

        logger.info(f"  Discovering OAuth metadata from: {mcp_server_url}")

        try:
            auth_server_url, auth_metadata = await discover_mcp_oauth_config(mcp_server_url)

            # Validate required OAuth fields
            required_fields = ['authorization_endpoint', 'token_endpoint']
            missing = [f for f in required_fields if f not in auth_metadata]

            if missing:
                raise NotOAuthCompliantError(
                    f"Server metadata missing required OAuth fields: {', '.join(missing)}"
                )

            logger.info(f"  ✓ Discovery successful")
            logger.debug(f"  Authorization endpoint: {auth_metadata['authorization_endpoint']}")
            logger.debug(f"  Token endpoint: {auth_metadata['token_endpoint']}")
            logger.debug(f"  Registration endpoint: {auth_metadata.get('registration_endpoint', 'Not available')}")
            logger.debug(f"  Supported grants: {auth_metadata.get('grant_types_supported', [])}")

            # Validate authorization code grant support
            if 'grant_types_supported' in auth_metadata:
                if 'authorization_code' not in auth_metadata['grant_types_supported']:
                    raise NotOAuthCompliantError(
                        "Server does not support authorization_code grant type"
                    )

            # Store auth server URL in metadata for later use
            auth_metadata['_auth_server_url'] = auth_server_url

            return auth_metadata

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise NotOAuthCompliantError(
                    f"OAuth discovery endpoint not found at {mcp_server_url}/.well-known/oauth-authorization-server"
                )
            raise OAuthDiscoveryError(f"HTTP {e.response.status_code} during discovery")

        except httpx.RequestError as e:
            raise OAuthDiscoveryError(f"Network error during discovery: {e}")

    async def _register_client(
        self,
        registration_endpoint: str,
        server_name: str,
        redirect_uris: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Implement OAuth 2.0 Dynamic Client Registration (RFC 7591).
        This is required by MCP spec for clients without pre-registered credentials.

        Returns:
            Registration data from the server
        """
        # Use provided redirect URIs or default to configured redirect URI
        if redirect_uris is None:
            redirect_uris = [self.config.callback_url]

        payload = {
            "client_name": "Devin",
            "redirect_uris": redirect_uris,
            "grant_types": ["authorization_code"],
            "response_types": ["code"],
            "token_endpoint_auth_method": "none",  # Public client
            "code_challenge_method": "S256",        # PKCE required
            "logo_uri": "https://mintlify.s3.us-west-1.amazonaws.com/cognitionai/logo/devin.png"
        }

        logger.info(f"Registering OAuth client for '{server_name}'...")
        logger.debug(f"  Redirect URIs: {redirect_uris}")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(registration_endpoint, json=payload)
                response.raise_for_status()

                reg_data = response.json()

                # Log registration details
                logger.info(f"Client registration successful for '{server_name}'")
                reg_details = [
                    f"  Client ID: {reg_data.get('client_id', 'N/A')}",
                    f"  Client name: {reg_data.get('client_name', 'N/A')}"
                ]
                if 'client_secret' in reg_data:
                    reg_details.append("  Client secret: ****** (received)")
                if 'client_id_issued_at' in reg_data:
                    reg_details.append(f"  Issued at: {reg_data.get('client_id_issued_at')}")
                if 'client_secret_expires_at' in reg_data:
                    reg_details.append(f"  Secret expires at: {reg_data.get('client_secret_expires_at')}")

                logger.info("Registration response:\n" + "\n".join(reg_details))

                # Return the full registration data
                return reg_data

            except httpx.HTTPStatusError as e:
                error_msg = [f"Client registration failed with status {e.response.status_code}"]
                if e.response.text:
                    error_msg.append(f"Error details: {e.response.text}")
                logger.error("\n".join(error_msg))
                raise
            except Exception as e:
                logger.exception(f"Client registration error: {e}")
                raise

    async def _register_oauth_client(self, server_name: str, auth_metadata: Dict[str, Any]) -> OAuthClientData:
        """Phase 2: Register or retrieve client credentials."""

        logger.info(f"  Checking for existing client registration...")

        # Check cache first
        cached_creds = await self._load_client_credentials(server_name)
        if cached_creds:
            logger.info(f"  ✓ Using previous client registration")
            logger.debug(f"  Client ID: {cached_creds.client_id}")
            return cached_creds

        # Dynamic registration
        if not auth_metadata.get('registration_endpoint'):
            raise OAuthClientRegistrationError(
                "No client_id configured and server doesn't support Dynamic Client Registration"
            )

        logger.info(f"  Registering new OAuth client...")

        # Use the configured redirect URI (handles both local and remote modes)
        redirect_uris = [self.config.callback_url]

        logger.debug(f"  Redirect URIs: {redirect_uris}")

        try:
            oauth_client_data = await self._register_client(
                auth_metadata['registration_endpoint'],
                server_name,
                redirect_uris
            )
            client_id = oauth_client_data.get('client_id')
            if not client_id:
                raise ValueError("Registration response missing client_id")

            logger.info(f"  ✓ Client registered successfully")
            logger.debug(f"  Client ID: {client_id}")
            return OAuthClientData(client_id=client_id)

        except Exception as e:
            raise OAuthClientRegistrationError(f"Failed to register client: {e}")

    async def _prepare_authorization_request(self, auth_metadata: Dict[str, Any], oauth_client_data: OAuthClientData) -> Dict[str, Any]:
        """Phase 3: Prepare authorization request."""

        logger.info(f"  Generating PKCE parameters...")

        # Generate security parameters
        code_verifier = generate_code_verifier()
        code_challenge = generate_code_challenge(code_verifier)
        state = secrets.token_urlsafe(32)

        logger.debug(f"  State: {state[:8]}...")
        logger.debug(f"  Code challenge: {code_challenge[:8]}...")

        # Determine redirect URI
        redirect_uri = self.config.callback_url

        logger.info(f"  ✓ Authorization prepared")
        logger.debug(f"  Redirect URI: {redirect_uri}")

        return {
            'client_id': oauth_client_data.client_id,
            'code_verifier': code_verifier,
            'code_challenge': code_challenge,
            'state': state,
            'redirect_uri': redirect_uri,
            'auth_endpoint': auth_metadata['authorization_endpoint'],
            'token_endpoint': auth_metadata['token_endpoint'],
            'scopes': auth_metadata.get('scopes_supported', []),
            '_auth_server_url': auth_metadata.get('_auth_server_url')
        }

    async def _remote_oauth_flow(self, server_name: str, auth_request: Dict[str, Any], oauth_client_data: OAuthClientData) -> httpx.Auth:
        """Custom implementation for remote redirect flow."""

        logger.info("🌐 Phase 4/6: Requesting Authorization (Remote)")

        # Build authorization URL
        auth_params = {
            'client_id': auth_request['client_id'],
            'redirect_uri': auth_request['redirect_uri'],
            'response_type': 'code',
            'state': auth_request['state'],
            'code_challenge': auth_request['code_challenge'],
            'code_challenge_method': 'S256',
        }

        if auth_request['scopes']:
            auth_params['scope'] = ' '.join(auth_request['scopes'])

        auth_url = f"{auth_request['auth_endpoint']}?{urlencode(auth_params)}"

        logger.info(f"  Authorization URL: {auth_url}")
        logger.info(f"  Auth params: {auth_params}")

        # Display instructions
        typer.secho(
            "\n🔐 Please visit this URL to authorize:",
            fg=typer.colors.BLUE
        )
        typer.secho(f"\n{auth_url}\n", fg=typer.colors.BRIGHT_BLUE, bold=True)
        typer.secho(
            "Waiting for authorization...",
            fg=typer.colors.YELLOW
        )

        logger.info(f"  Authorization URL generated")
        logger.debug(f"  URL: {auth_url}")

        # Poll for code
        auth_code = await self._poll_for_code(auth_request['state'], auth_request['code_verifier'])

        logger.info("🎫 Phase 5/6: Token Exchange")

        # Exchange code for tokens
        tokens = await self._exchange_code_for_tokens(
            auth_code=auth_code,
            code_verifier=auth_request['code_verifier'],
            redirect_uri=auth_request['redirect_uri'],
            client_id=oauth_client_data.client_id,
            token_endpoint=auth_request['token_endpoint']
        )
        logger.debug(f"Tokens: {tokens}")

        logger.info("✅ Phase 6/6: Authentication Completed")

        # Also save to our format
        await self.token_storage.save_tokens(
            server_name=server_name,
            tokens=tokens,
            oauth_client_data=oauth_client_data,
        )

        await self._log_token_update(server_name)

        typer.secho("✓ Authentication successful!", fg=typer.colors.GREEN)

        return self._create_bearer_auth(tokens)

    async def _poll_for_code(self, state: str, code_verifier: str, timeout: int = 300) -> str:
        """Poll remote service for authorization code."""

        logger.info(f"  Polling for authorization (timeout: 5 minutes)...")
        return await self.webserver_client.poll_for_code(state, timeout)

    async def _exchange_code_for_tokens(
        self,
        auth_code: str,
        code_verifier: str,
        redirect_uri: str,
        client_id: str,
        token_endpoint: str
    ) -> Dict[str, Any]:
        """Exchange authorization code for access and refresh tokens."""

        logger.info(f"  Exchanging authorization code for tokens...")

        token_data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'code_verifier': code_verifier,
        }

        logger.debug(f"  Token endpoint: {token_endpoint}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    token_endpoint,
                    data=token_data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )

                if response.status_code != 200:
                    error_data = response.json()
                    raise OAuthTokenExchangeError(
                        f"Token exchange failed: {error_data.get('error_description', error_data.get('error', 'Unknown error'))}"
                    )

                tokens = response.json()

                logger.info(f"  ✓ Tokens received successfully")
                logger.debug(f"  Access token: {tokens['access_token'][:10]}...")
                logger.debug(f"  Token type: {tokens.get('token_type', 'Bearer')}")
                logger.debug(f"  Expires in: {tokens.get('expires_in', 'Not specified')} seconds")
                logger.debug(f"  Refresh token: {'Present' if tokens.get('refresh_token') else 'Not provided'}")

                tokens['obtained_at'] = datetime.now(timezone.utc)
                if 'expires_in' in tokens:
                    tokens['expires_at'] = tokens['obtained_at'] + timedelta(seconds=tokens['expires_in'])

                return tokens

        except httpx.RequestError as e:
            raise OAuthTokenExchangeError(f"Network error during token exchange: {e}")

    async def _refresh_access_token(
        self,
        server_name: str,
        refresh_token: str,
        client_id: str,
        token_endpoint: str
    ) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.

        Args:
            server_name: Name of the server
            refresh_token: The refresh token to use
            client_id: OAuth client ID
            token_endpoint: Token endpoint URL

        Returns:
            Dictionary containing new tokens
        """
        logger.info(f"Refreshing access token for '{server_name}'")

        token_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
        }

        logger.debug(f"Token endpoint: {token_endpoint}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    token_endpoint,
                    data=token_data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )

                if response.status_code != 200:
                    error_data = response.json()
                    logger.error(f"Token refresh failed: {error_data}")
                    raise OAuthTokenExchangeError(
                        f"Token refresh failed: {error_data.get('error_description', error_data.get('error', 'Unknown error'))}"
                    )

                tokens = response.json()

                logger.debug(f'Token refresh response: {tokens}')
                logger.debug(f"New access token: {tokens['access_token'][:10]}...")
                logger.debug(f"Expires in: {tokens.get('expires_in', 'Not specified')} seconds")

                # Add metadata for token management
                tokens['obtained_at'] = datetime.now(timezone.utc)
                if 'expires_in' in tokens:
                    tokens['expires_at'] = tokens['obtained_at'] + timedelta(seconds=tokens['expires_in'])

                # If no new refresh token provided, keep the old one
                if 'refresh_token' not in tokens:
                    tokens['refresh_token'] = refresh_token
                    logger.debug("Reusing existing refresh token")

                return tokens

        except httpx.RequestError as e:
            logger.error(f"Network error during token refresh: {e}")
            raise OAuthTokenExchangeError(f"Network error during token refresh: {e}")

    async def _refresh_token_with_discovery(self, server_name: str, server_config: Dict[str, Any]) -> Optional[httpx.Auth]:
        """
        Refresh tokens using fresh OAuth discovery.

        This method implements the proper pattern:
        1. Load cached refresh token and client credentials
        2. Do fresh OAuth discovery to get current endpoints
        3. Use refresh token to get new access token
        4. Cache the new tokens

        Args:
            server_name: Name of the server to refresh tokens for
            server_config: Server configuration (for discovery)

        Returns:
            New auth object or None if refresh fails
        """
        logger.info(f"Refreshing tokens with fresh discovery for '{server_name}'")

        # Step 1: Load cached tokens from our format
        server_data = await self.token_storage.load_tokens(server_name)
        if not server_data:
            logger.warning("No cached tokens found")
            return None

        tokens = server_data.tokens
        refresh_token = tokens.refresh_token

        if not refresh_token:
            logger.warning("No refresh token available")
            return None

        # Step 2: Load client credentials from our format
        client_data = server_data.oauth_client_data
        client_id = client_data.client_id

        if not client_id:
            logger.warning("No client credentials found")
            return None

        # Step 3: Do fresh OAuth discovery
        logger.info("Performing fresh OAuth discovery...")
        try:
            auth_metadata = await self._perform_oauth_discovery(server_config)
            token_endpoint = auth_metadata['token_endpoint']
            logger.info(f"✓ Fresh discovery successful, token endpoint: {token_endpoint}")
        except Exception as e:
            logger.error(f"OAuth discovery failed: {e}")
            return None

        # Step 4: Refresh the token
        try:
            logger.info("Refreshing access token...")
            new_tokens = await self._refresh_access_token(
                server_name=server_name,
                refresh_token=refresh_token,
                client_id=client_id,
                token_endpoint=token_endpoint
            )
            logger.info("✓ Token refresh successful")
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            return None

        await self.token_storage.save_tokens(
            server_name=server_name,
            tokens=new_tokens,
            oauth_client_data=client_data,
        )
        logger.info("✓ New tokens cached")

        # Step 6: Return auth object
        auth = self._create_bearer_auth(new_tokens)
        logger.info("✓ Token refresh with discovery completed successfully")
        return auth

    def _create_bearer_auth(self, tokens: Dict[str, Any]) -> httpx.Auth:
        """Create simple bearer token auth for httpx."""

        class BearerTokenAuth(httpx.Auth):
            def __init__(self, access_token):
                self.access_token = access_token

            def auth_flow(self, request):
                request.headers['Authorization'] = f'Bearer {self.access_token}'
                yield request

        return BearerTokenAuth(tokens['access_token'])

    async def _load_client_credentials(self, server_name: str) -> Optional[OAuthClientData]:
        """Load client credentials from consolidated tokens file."""
        server_data = await self.token_storage.load_tokens(server_name)
        if server_data:
            return server_data.oauth_client_data
        return None

    async def _log_token_update(self, server_name: str):
        """Log information about newly obtained or refreshed tokens.

        This should be called after tokens are updated.
        """
        server_data = await self.token_storage.load_tokens(server_name)

        if server_data:
            tokens = server_data.tokens

            # Check if this is a new token or refresh
            current_time = datetime.now(timezone.utc)
            expires_at = tokens.expires_at
            obtained_at = tokens.obtained_at

            if current_time - obtained_at < timedelta(seconds=10):
                logger.info(f"New OAuth tokens obtained for '{server_name}'")
            else:
                logger.info(f"OAuth tokens refreshed for '{server_name}'")

            token_details = []

            # Log expiration info
            if expires_at > current_time:
                expires_in_seconds = int((expires_at - current_time).total_seconds())
                hours = expires_in_seconds // 3600
                minutes = (expires_in_seconds % 3600) // 60
                token_details.append(f"  Access token expires in: {hours}h {minutes}m")
            else:
                token_details.append("  Access token: EXPIRED")

            if tokens.refresh_token:
                token_details.append("  Refresh token: obtained")

            if token_details:
                logger.info("Token details:\n" + "\n".join(token_details))
        else:
            logger.debug(f"No valid tokens found for logging update for '{server_name}'")

    async def clear_tokens(self, server_name: str):
        """Clear cached OAuth data for a specific server.

        Args:
            server_name: Name of the server to clear data for
        """

        await self.token_storage.clear_tokens(server_name)
        logger.info(f"OAuth data cleared from tokens.json for '{server_name}'")

    async def get_cached_token(self, server_name: str, server_config: Dict[str, Any]) -> Optional[str]:
        """Get cached token for a server if available.

        This method checks for valid cached tokens and automatically attempts to refresh
        expired tokens using the refresh token if available.

        Args:
            server_name: Name of the server
            server_config: Server configuration (needed for potential refresh)

        Returns:
            Cached token string or None if not available
        """
        logger.info(f"Retrieving tokens for server '{server_name}'")

        # Check our token format
        server_data = await self.token_storage.load_tokens(server_name)

        if server_data:
            tokens = server_data.tokens
            access_token = tokens.access_token
            expires_at = tokens.expires_at
            refresh_token = tokens.refresh_token

            current_time = datetime.now(timezone.utc)
            is_expired = expires_at <= current_time

            if access_token and not is_expired:
                # Token is valid
                logger.info(f"Using cached OAuth token for '{server_name}'")

                expires_in_seconds = int((expires_at - current_time).total_seconds())
                hours = expires_in_seconds // 3600
                minutes = (expires_in_seconds % 3600) // 60
                logger.debug(f"  Access token expires in: {hours}h {minutes}m")

                if refresh_token:
                    logger.debug("  Refresh token: available")

                return access_token

            elif access_token and is_expired and refresh_token:
                # Token expired but we have refresh token
                logger.warning(f"Cached OAuth token for '{server_name}' is expired")
                logger.info(f"Attempting to refresh expired token for '{server_name}'")

                try:
                    refreshed_auth = await self._refresh_token_with_discovery(server_name, server_config)
                    if refreshed_auth:
                        logger.info(f"Successfully refreshed token for '{server_name}'")
                        # Re-read the updated token
                        updated_data = await self.token_storage.load_tokens(server_name)
                        if updated_data:
                            return updated_data.tokens.access_token
                    else:
                        logger.warning(f"Token refresh failed for '{server_name}', will need re-authentication")
                except Exception as e:
                    logger.warning(f"Token refresh failed for '{server_name}', will need re-authentication: {e}")

                return None

        logger.debug(f"No valid cached token found for '{server_name}'")
        return None

    async def check_oauth_compatibility(self, server_config: Dict[str, Any]) -> bool:
        """Check if a server supports OAuth without raising exceptions."""
        try:
            await self._perform_oauth_discovery(server_config)
            return True
        except NotOAuthCompliantError:
            return False

    async def authenticate(self, server_name: str, server_config: Dict[str, Any]) -> httpx.Auth:
        """Main entry point with comprehensive error handling."""

        logger.info("=" * 60)
        logger.info(f"Starting OAuth authentication for server: {server_name}")
        logger.info("=" * 60)

        try:
            # Phase 1: Metadata Discovery
            logger.info("📡 Phase 1/6: OAuth Metadata Discovery")
            auth_metadata = await self._perform_oauth_discovery(server_config)

            # Phase 2: Client Registration
            logger.info("📝 Phase 2/6: Client Registration")
            oauth_client_data = await self._register_oauth_client(server_name, auth_metadata)

            # Phase 3: Preparing Authorization
            logger.info("🔧 Phase 3/6: Preparing Authorization")
            auth_request = await self._prepare_authorization_request(auth_metadata, oauth_client_data)

            logger.info("🌐 Using remote redirect OAuth flow")
            auth = await self._remote_oauth_flow(server_name, auth_request, oauth_client_data)
            return auth

        except NotOAuthCompliantError as e:
            logger.error(f"❌ Server is not OAuth compliant: {e}")
            typer.secho(
                f"\n❌ Error: {server_name} does not support OAuth authentication, it might use a different authentication method.",
                fg=typer.colors.RED,
                err=True
            )
            raise

        except MCPOAuthError as e:
            logger.error(f"❌ OAuth error during {e.__class__.__name__}: {e}")
            raise

        except Exception as e:
            logger.exception(f"❌ Unexpected error during OAuth flow")
            raise
