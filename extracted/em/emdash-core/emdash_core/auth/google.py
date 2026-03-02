"""Google OAuth authentication for Emdash.

This module provides Google OAuth 2.0 authentication using the Authorization Code flow
with a localhost redirect. This allows users to authenticate with their Google account
to access Gmail, Calendar, Drive, and other Google Workspace services.

Usage:
    from emdash_core.auth.google import GoogleAuth

    auth = GoogleAuth()
    auth.login()  # Opens browser for OAuth

    # Check status
    if auth.is_authenticated():
        token = auth.get_access_token()
"""

import json
import os
import secrets
import socket
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode, parse_qs, urlparse

import requests

from ..utils.logger import log


# Emdash OAuth App credentials
# For desktop/CLI apps, Google allows embedding these in open-source code
# See: https://developers.google.com/identity/protocols/oauth2/native-app
GOOGLE_CLIENT_ID = os.getenv(
    "EMDASH_GOOGLE_CLIENT_ID",
    # Default Emdash OAuth app - users can override with their own
    ""  # Will be set when Emdash registers with Google Cloud
)
GOOGLE_CLIENT_SECRET = os.getenv(
    "EMDASH_GOOGLE_CLIENT_SECRET",
    ""  # Will be set when Emdash registers with Google Cloud
)

# OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
GOOGLE_REVOKE_URL = "https://oauth2.googleapis.com/revoke"

# Default scopes for Google Workspace access
DEFAULT_SCOPES = [
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]


def get_config_dir() -> Path:
    """Get the configuration directory for emdash."""
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        config_dir = Path(xdg_config) / "emdash"
    else:
        config_dir = Path.home() / ".config" / "emdash"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_google_auth_file() -> Path:
    """Get the path to the Google auth config file."""
    return get_config_dir() / "google_auth.json"


def save_google_auth_config(config: dict) -> None:
    """Save Google auth config to disk with secure permissions."""
    auth_file = get_google_auth_file()
    with open(auth_file, "w") as f:
        json.dump(config, f, indent=2)
    # Set restrictive permissions (owner read/write only)
    os.chmod(auth_file, 0o600)


def load_google_auth_config() -> Optional[dict]:
    """Load Google auth config from disk."""
    auth_file = get_google_auth_file()
    if auth_file.exists():
        try:
            with open(auth_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            log.warning(f"Failed to load Google auth config: {e}")
    return None


def get_google_access_token() -> Optional[str]:
    """Get Google access token, refreshing if necessary.

    Returns:
        Access token string or None if not authenticated
    """
    config = load_google_auth_config()
    if not config:
        return None

    access_token = config.get("access_token")
    refresh_token = config.get("refresh_token")

    # Check if token needs refresh (we don't store expiry, so just try to use it)
    # If it fails, the caller can trigger a refresh
    if access_token:
        return access_token

    # Try to refresh
    if refresh_token:
        auth = GoogleAuth()
        new_token = auth.refresh_access_token(refresh_token)
        if new_token:
            return new_token

    return None


def is_google_authenticated() -> bool:
    """Check if Google authentication is configured."""
    config = load_google_auth_config()
    return config is not None and "access_token" in config


def get_google_auth_status() -> dict:
    """Get detailed Google authentication status."""
    config = load_google_auth_config()

    if not config:
        return {
            "authenticated": False,
            "source": None,
            "email": None,
            "scopes": [],
        }

    return {
        "authenticated": True,
        "source": "emdash auth",
        "email": config.get("email"),
        "scopes": config.get("scope", "").split(),
    }


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""

    auth_code: Optional[str] = None
    error: Optional[str] = None
    state: Optional[str] = None

    def log_message(self, format, *args):
        """Suppress HTTP server logs."""
        pass

    def do_GET(self):
        """Handle OAuth callback GET request."""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if "code" in params:
            OAuthCallbackHandler.auth_code = params["code"][0]
            OAuthCallbackHandler.state = params.get("state", [None])[0]
            self._send_success_response()
        elif "error" in params:
            OAuthCallbackHandler.error = params.get("error_description", params["error"])[0]
            self._send_error_response(OAuthCallbackHandler.error)
        else:
            self._send_error_response("Unknown callback")

    def _send_success_response(self):
        """Send success HTML response."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Emdash - Authentication Successful</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                       display: flex; justify-content: center; align-items: center; height: 100vh;
                       margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
                .card { background: white; padding: 40px; border-radius: 12px; text-align: center;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2); max-width: 400px; }
                h1 { color: #333; margin-bottom: 10px; }
                p { color: #666; }
                .success { color: #22c55e; font-size: 48px; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="success">✓</div>
                <h1>Authentication Successful!</h1>
                <p>You can close this window and return to Emdash.</p>
            </div>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def _send_error_response(self, error: str):
        """Send error HTML response."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Emdash - Authentication Failed</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                       display: flex; justify-content: center; align-items: center; height: 100vh;
                       margin: 0; background: #f5f5f5; }}
                .card {{ background: white; padding: 40px; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.1); max-width: 400px; }}
                h1 {{ color: #333; margin-bottom: 10px; }}
                p {{ color: #666; }}
                .error {{ color: #ef4444; font-size: 48px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="error">✕</div>
                <h1>Authentication Failed</h1>
                <p>{error}</p>
            </div>
        </body>
        </html>
        """
        self.send_response(400)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


class GoogleAuth:
    """Google OAuth 2.0 authentication handler."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        """Initialize Google auth handler.

        Args:
            client_id: OAuth client ID (uses default if not provided)
            client_secret: OAuth client secret (uses default if not provided)
        """
        self.client_id = client_id or GOOGLE_CLIENT_ID or os.getenv("GOOGLE_CLIENT_ID", "")
        self.client_secret = client_secret or GOOGLE_CLIENT_SECRET or os.getenv("GOOGLE_CLIENT_SECRET", "")

    def _find_free_port(self) -> int:
        """Find a free port for the OAuth callback server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            return s.getsockname()[1]

    def login(
        self,
        scopes: Optional[list[str]] = None,
        open_browser: bool = True,
    ) -> dict:
        """Perform Google OAuth login.

        Args:
            scopes: OAuth scopes to request (uses defaults if not provided)
            open_browser: Whether to automatically open the browser

        Returns:
            Dict with authentication result
        """
        if not self.client_id or not self.client_secret:
            return {
                "success": False,
                "error": "Google OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables, "
                         "or configure them in Google Cloud Console.",
            }

        scopes = scopes or DEFAULT_SCOPES

        # Find a free port and start callback server
        port = self._find_free_port()
        redirect_uri = f"http://localhost:{port}"

        # Generate state for CSRF protection
        state = secrets.token_urlsafe(32)

        # Build authorization URL
        auth_params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(scopes),
            "state": state,
            "access_type": "offline",  # Request refresh token
            "prompt": "consent",  # Always show consent to get refresh token
        }
        auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(auth_params)}"

        # Reset handler state
        OAuthCallbackHandler.auth_code = None
        OAuthCallbackHandler.error = None
        OAuthCallbackHandler.state = None

        # Start callback server
        server = HTTPServer(("localhost", port), OAuthCallbackHandler)
        server.timeout = 300  # 5 minute timeout

        # Open browser
        if open_browser:
            webbrowser.open(auth_url)

        result = {
            "success": False,
            "auth_url": auth_url,
            "message": "Please authorize Emdash in your browser...",
        }

        try:
            # Wait for callback
            while OAuthCallbackHandler.auth_code is None and OAuthCallbackHandler.error is None:
                server.handle_request()

            if OAuthCallbackHandler.error:
                result["error"] = OAuthCallbackHandler.error
                return result

            # Verify state
            if OAuthCallbackHandler.state != state:
                result["error"] = "State mismatch - possible CSRF attack"
                return result

            # Exchange code for tokens
            token_data = self._exchange_code_for_tokens(
                OAuthCallbackHandler.auth_code,
                redirect_uri,
            )

            if "error" in token_data:
                error_msg = token_data.get("error_description", token_data["error"])
                log.error(f"Google OAuth error: {error_msg}, redirect_uri={redirect_uri}")
                result["error"] = error_msg
                return result

            # Get user info
            user_info = self._get_user_info(token_data["access_token"])

            # Save auth config
            auth_config = {
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token"),
                "token_type": token_data.get("token_type", "Bearer"),
                "scope": token_data.get("scope", " ".join(scopes)),
                "email": user_info.get("email"),
                "name": user_info.get("name"),
            }
            save_google_auth_config(auth_config)

            result["success"] = True
            result["email"] = user_info.get("email")
            result["name"] = user_info.get("name")
            result["message"] = f"Successfully authenticated as {user_info.get('email')}"

        except Exception as e:
            result["error"] = str(e)
            log.exception("Google OAuth login failed")

        finally:
            server.server_close()

        return result

    def _exchange_code_for_tokens(self, code: str, redirect_uri: str) -> dict:
        """Exchange authorization code for access and refresh tokens."""
        response = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
            timeout=30,
        )
        result = response.json()
        if response.status_code != 200:
            log.error(f"Google token exchange failed: status={response.status_code}, response={result}")
        return result

    def _get_user_info(self, access_token: str) -> dict:
        """Get user info from Google."""
        response = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()
        return {}

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Refresh the access token using the refresh token.

        Args:
            refresh_token: The refresh token

        Returns:
            New access token or None if refresh failed
        """
        if not self.client_id or not self.client_secret:
            return None

        try:
            response = requests.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
                timeout=30,
            )

            if response.status_code == 200:
                token_data = response.json()

                # Update stored config with new access token
                config = load_google_auth_config() or {}
                config["access_token"] = token_data["access_token"]
                save_google_auth_config(config)

                return token_data["access_token"]
            else:
                log.warning(f"Failed to refresh Google token: {response.text}")

        except Exception as e:
            log.exception(f"Error refreshing Google token: {e}")

        return None

    def logout(self) -> dict:
        """Revoke Google authentication and delete stored tokens.

        Returns:
            Dict with logout result
        """
        config = load_google_auth_config()
        result = {"success": False}

        if config and config.get("access_token"):
            # Revoke token at Google
            try:
                requests.post(
                    GOOGLE_REVOKE_URL,
                    params={"token": config["access_token"]},
                    timeout=30,
                )
            except Exception as e:
                log.warning(f"Failed to revoke Google token: {e}")

        # Delete local auth file
        auth_file = get_google_auth_file()
        if auth_file.exists():
            auth_file.unlink()
            result["success"] = True
            result["message"] = "Successfully logged out from Google"
        else:
            result["success"] = True
            result["message"] = "No Google authentication found"

        return result

    def is_authenticated(self) -> bool:
        """Check if authenticated with Google."""
        return is_google_authenticated()

    def get_access_token(self) -> Optional[str]:
        """Get the current access token, refreshing if necessary."""
        return get_google_access_token()

    def get_status(self) -> dict:
        """Get authentication status."""
        return get_google_auth_status()
