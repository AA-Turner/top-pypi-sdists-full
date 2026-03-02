"""GitHub OAuth Device Flow authentication.

This module implements GitHub's device flow for CLI authentication,
similar to how `gh auth login` works.

Device Flow Steps:
1. Request device and user codes from GitHub
2. Display user code and open browser to github.com/login/device
3. Poll GitHub until user completes authorization
4. Store access token securely

Reference: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps#device-flow
"""

import json
import os
import subprocess
import time
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from ..utils.logger import log


# Em Dash GitHub OAuth App Client ID
GITHUB_CLIENT_ID = "Ov23liMPlw6JMmzUainJ"

# GitHub OAuth endpoints
DEVICE_CODE_URL = "https://github.com/login/device/code"
ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"

# Default scopes for Rove (repo access for code search, PRs, etc.)
DEFAULT_SCOPES = ["repo", "read:user"]


@dataclass
class AuthConfig:
    """Stored authentication configuration."""

    access_token: str
    token_type: str = "bearer"
    scope: str = ""
    username: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "scope": self.scope,
            "username": self.username,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AuthConfig":
        return cls(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "bearer"),
            scope=data.get("scope", ""),
            username=data.get("username"),
        )


@dataclass
class DeviceCodeResponse:
    """Response from device code request."""

    device_code: str
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int


def get_config_dir() -> Path:
    """Get the Rove config directory.

    Returns:
        Path to ~/.config/emdash/
    """
    # Follow XDG spec on Linux/Mac
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        config_dir = Path(xdg_config) / "emdash"
    else:
        config_dir = Path.home() / ".config" / "emdash"

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_auth_file() -> Path:
    """Get path to the auth config file."""
    return get_config_dir() / "auth.json"


def _make_request(url: str, data: dict, headers: dict = None) -> dict:
    """Make a POST request and return JSON response."""
    headers = headers or {}
    headers["Accept"] = "application/json"

    encoded_data = urlencode(data).encode("utf-8")
    request = Request(url, data=encoded_data, headers=headers, method="POST")

    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        log.error(f"HTTP error {e.code}: {error_body}")
        raise
    except URLError as e:
        log.error(f"URL error: {e.reason}")
        raise


def _get_request(url: str, token: str) -> dict:
    """Make a GET request with auth token."""
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    request = Request(url, headers=headers)

    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


class GitHubAuth:
    """GitHub OAuth device flow authentication."""

    def __init__(self, client_id: str = GITHUB_CLIENT_ID):
        self.client_id = client_id

    def request_device_code(self, scopes: list[str] = None) -> DeviceCodeResponse:
        """Request a device code from GitHub.

        Args:
            scopes: OAuth scopes to request

        Returns:
            DeviceCodeResponse with codes and URIs
        """
        scopes = scopes or DEFAULT_SCOPES

        data = {
            "client_id": self.client_id,
            "scope": " ".join(scopes),
        }

        response = _make_request(DEVICE_CODE_URL, data)

        return DeviceCodeResponse(
            device_code=response["device_code"],
            user_code=response["user_code"],
            verification_uri=response["verification_uri"],
            expires_in=response["expires_in"],
            interval=response["interval"],
        )

    def poll_for_token(
        self,
        device_code: str,
        interval: int = 5,
        timeout: int = 900,
    ) -> Optional[AuthConfig]:
        """Poll GitHub for access token after user authorizes.

        Args:
            device_code: Device code from request_device_code
            interval: Polling interval in seconds
            timeout: Maximum time to wait in seconds

        Returns:
            AuthConfig if successful, None if timeout/cancelled
        """
        data = {
            "client_id": self.client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = _make_request(ACCESS_TOKEN_URL, data)

                if "access_token" in response:
                    # Success!
                    config = AuthConfig(
                        access_token=response["access_token"],
                        token_type=response.get("token_type", "bearer"),
                        scope=response.get("scope", ""),
                    )

                    # Fetch username
                    try:
                        user_info = _get_request(USER_API_URL, config.access_token)
                        config.username = user_info.get("login")
                    except Exception as e:
                        log.warning(f"Failed to fetch username: {e}")

                    return config

                error = response.get("error")

                if error == "authorization_pending":
                    # User hasn't authorized yet, keep polling
                    time.sleep(interval)
                    continue
                elif error == "slow_down":
                    # We're polling too fast
                    interval += 5
                    time.sleep(interval)
                    continue
                elif error == "expired_token":
                    log.error("Device code expired. Please try again.")
                    return None
                elif error == "access_denied":
                    log.error("Authorization was denied.")
                    return None
                else:
                    log.error(f"Unexpected error: {error}")
                    return None

            except Exception as e:
                log.error(f"Error polling for token: {e}")
                time.sleep(interval)

        log.error("Timeout waiting for authorization.")
        return None

    def login(self, scopes: list[str] = None, open_browser: bool = True) -> Optional[AuthConfig]:
        """Perform full device flow login.

        Args:
            scopes: OAuth scopes to request
            open_browser: Whether to open browser automatically

        Returns:
            AuthConfig if successful, None otherwise
        """
        # Request device code
        device_response = self.request_device_code(scopes)

        # Display instructions
        print()
        print(f"! First, copy your one-time code: {device_response.user_code}")
        print(f"- Then visit: {device_response.verification_uri}")

        if open_browser:
            input("- Press Enter to open github.com in your browser...")
            webbrowser.open(device_response.verification_uri)

        print()
        print("Waiting for authorization...")

        # Poll for token
        config = self.poll_for_token(
            device_response.device_code,
            interval=device_response.interval,
        )

        if config:
            # Save to disk
            save_auth_config(config)

            # Configure git credentials for clone/push/pull
            if configure_git_credentials(config.access_token, config.username):
                print()
                if config.username:
                    print(f"✓ Authentication complete. Logged in as @{config.username}")
                    print("✓ Git credentials configured for github.com")
                else:
                    print("✓ Authentication complete.")
                    print("✓ Git credentials configured for github.com")
            else:
                print()
                if config.username:
                    print(f"✓ Authentication complete. Logged in as @{config.username}")
                else:
                    print("✓ Authentication complete.")
                print("⚠ Could not configure git credentials automatically")

        return config

    def logout(self) -> bool:
        """Remove stored authentication and git credentials.

        Returns:
            True if logout successful
        """
        auth_file = get_auth_file()
        removed_auth = False

        if auth_file.exists():
            auth_file.unlink()
            removed_auth = True

        # Also remove git credentials
        remove_git_credentials()

        return removed_auth


def save_auth_config(config: AuthConfig) -> None:
    """Save authentication config to disk.

    Args:
        config: AuthConfig to save
    """
    auth_file = get_auth_file()

    # Set restrictive permissions (owner read/write only)
    with open(auth_file, "w") as f:
        json.dump(config.to_dict(), f, indent=2)

    # chmod 600
    os.chmod(auth_file, 0o600)

    log.debug(f"Saved auth config to {auth_file}")


def configure_git_credentials(token: str, username: str = None) -> bool:
    """Configure git to use the GitHub token for authentication.

    This stores the credentials using git's credential helper system,
    allowing git clone, push, pull, etc. to work with GitHub.

    Args:
        token: GitHub access token
        username: GitHub username (optional, defaults to 'x-access-token')

    Returns:
        True if successful, False otherwise
    """
    # Use 'x-access-token' as username if not provided (GitHub accepts this)
    git_username = username or "x-access-token"

    # Format credentials for git credential helper
    # Protocol format: https://username:token@github.com
    credential_input = f"""protocol=https
host=github.com
username={git_username}
password={token}
"""

    try:
        # Store credentials using git credential approve
        # This works with whatever credential helper is configured
        result = subprocess.run(
            ["git", "credential", "approve"],
            input=credential_input,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            log.debug("Git credentials configured successfully")
            return True
        else:
            log.warning(f"git credential approve failed: {result.stderr}")
            # Fall back to .netrc approach
            return _configure_netrc(token, git_username)

    except FileNotFoundError:
        log.warning("git not found, skipping git credential configuration")
        return False
    except subprocess.TimeoutExpired:
        log.warning("git credential approve timed out")
        return False
    except Exception as e:
        log.warning(f"Failed to configure git credentials: {e}")
        return False


def _configure_netrc(token: str, username: str) -> bool:
    """Configure .netrc file for GitHub authentication.

    Fallback method if git credential helper doesn't work.

    Args:
        token: GitHub access token
        username: GitHub username

    Returns:
        True if successful, False otherwise
    """
    netrc_path = Path.home() / ".netrc"

    try:
        # Read existing .netrc
        existing_content = ""
        if netrc_path.exists():
            existing_content = netrc_path.read_text()

        # Check if github.com entry already exists
        lines = existing_content.split("\n")
        new_lines = []
        skip_until_machine = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("machine github.com"):
                skip_until_machine = True
                continue
            if skip_until_machine and stripped.startswith("machine "):
                skip_until_machine = False
            if not skip_until_machine:
                new_lines.append(line)

        # Add new GitHub entry
        github_entry = f"""
machine github.com
  login {username}
  password {token}
"""
        new_content = "\n".join(new_lines).strip() + github_entry

        # Write .netrc
        netrc_path.write_text(new_content)

        # chmod 600 (required for .netrc)
        os.chmod(netrc_path, 0o600)

        log.debug(f"Configured {netrc_path} for GitHub authentication")
        return True

    except Exception as e:
        log.warning(f"Failed to configure .netrc: {e}")
        return False


def remove_git_credentials() -> bool:
    """Remove stored GitHub credentials from git.

    Returns:
        True if successful, False otherwise
    """
    credential_input = """protocol=https
host=github.com
"""

    try:
        # Remove credentials using git credential reject
        subprocess.run(
            ["git", "credential", "reject"],
            input=credential_input,
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Also try to remove from .netrc
        _remove_netrc_entry()

        log.debug("Git credentials removed")
        return True

    except Exception as e:
        log.warning(f"Failed to remove git credentials: {e}")
        return False


def _remove_netrc_entry() -> None:
    """Remove GitHub entry from .netrc file."""
    netrc_path = Path.home() / ".netrc"

    if not netrc_path.exists():
        return

    try:
        content = netrc_path.read_text()
        lines = content.split("\n")
        new_lines = []
        skip_until_machine = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("machine github.com"):
                skip_until_machine = True
                continue
            if skip_until_machine and stripped.startswith("machine "):
                skip_until_machine = False
            if not skip_until_machine:
                new_lines.append(line)

        netrc_path.write_text("\n".join(new_lines))

    except Exception as e:
        log.warning(f"Failed to remove .netrc entry: {e}")


def load_auth_config() -> Optional[AuthConfig]:
    """Load authentication config from disk.

    Returns:
        AuthConfig or None if not found
    """
    auth_file = get_auth_file()

    if not auth_file.exists():
        return None

    try:
        with open(auth_file) as f:
            data = json.load(f)
        return AuthConfig.from_dict(data)
    except Exception as e:
        log.warning(f"Failed to load auth config: {e}")
        return None


def get_github_token() -> Optional[str]:
    """Get GitHub token from auth config or environment.

    Priority:
    1. Rove auth config (~/.config/emdash/auth.json)
    2. GITHUB_TOKEN environment variable
    3. GITHUB_PERSONAL_ACCESS_TOKEN environment variable

    Returns:
        GitHub access token or None
    """
    # Check Rove auth first
    config = load_auth_config()
    if config and config.access_token:
        return config.access_token

    # Fall back to environment variables
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")


def is_authenticated() -> bool:
    """Check if user is authenticated.

    Returns:
        True if authenticated (either via Rove auth or env var)
    """
    return get_github_token() is not None


def get_auth_status() -> dict:
    """Get current authentication status.

    Returns:
        Dict with status info
    """
    config = load_auth_config()
    env_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")

    if config and config.access_token:
        return {
            "authenticated": True,
            "source": "emdash auth",
            "username": config.username,
            "scopes": config.scope.split() if config.scope else [],
        }
    elif env_token:
        return {
            "authenticated": True,
            "source": "environment variable",
            "username": None,
            "scopes": [],
        }
    else:
        return {
            "authenticated": False,
            "source": None,
            "username": None,
            "scopes": [],
        }


def setup_git_credentials() -> bool:
    """Set up git credentials from existing auth config.

    Call this to configure git credentials if you've already
    authenticated but git isn't set up.

    Returns:
        True if successful, False otherwise
    """
    config = load_auth_config()
    if not config or not config.access_token:
        log.warning("No auth config found. Run 'emdash auth login' first.")
        return False

    return configure_git_credentials(config.access_token, config.username)
