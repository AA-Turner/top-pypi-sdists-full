"""OAuth configuration management."""

import os
import logging  
import json
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Default values
DEFAULT_REMOTE_REDIRECT_SERVER = 'https://api.devin.ai'
DEFAULT_CALLBACK_PATH = '/mcp-cli/callback'
DEFAULT_POLL_PATH = '/mcp-cli/code'
DEFAULT_TOKENS_PATH = '/mcp-cli/tokens'

# Load oauth.env from project root
# override=False ensures that existing env vars take precedence
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file, override=False)


def get_custom_remote_config() -> dict | None:
    remote_config = Path('/opt/.devin/custom_remote_config.json')
    if not remote_config.exists():
        return None
    
    with open(remote_config, 'r') as f:
        return json.load(f)
    
def get_backend_url() -> str:
    backend_url = os.getenv('MCP_OAUTH_REDIRECT_SERVER')
    if backend_url:
        return backend_url
    
    remote_config = get_custom_remote_config()
    if remote_config:
        return remote_config.get('api_host', DEFAULT_REMOTE_REDIRECT_SERVER)
    
    return 'https://api.devin.ai'

def get_cli_auth_token() -> str | None:
    token = os.getenv("MCP_OAUTH_AUTH_TOKEN")
    if token:
        return token
    
    remote_config = get_custom_remote_config()
    if remote_config:
        token = remote_config.get('auth_token', None)

        if token:
            return token
    
    logger.warning("MCP CLI auth token not found")
    return None

class OAuthConfig:
    """Simple OAuth configuration from environment variables."""
    
    def __init__(self):
        self.redirect_service_base_url = get_backend_url()
        
        self.redirect_callback_path = os.getenv(
            'MCP_OAUTH_REDIRECT_CALLBACK_PATH',
            DEFAULT_CALLBACK_PATH
        )
        
        self.redirect_poll_path = os.getenv(
            'MCP_OAUTH_CODE_POLL_PATH',
            DEFAULT_POLL_PATH
        )

        self.tokens_path = os.getenv(
            'MCP_OAUTH_TOKENS_PATH',
            DEFAULT_TOKENS_PATH
        )

        self.cli_auth_token = get_cli_auth_token()

    def get_oauth_code_polling_url(self, state: str) -> str:
        url = f"{self.redirect_service_base_url}{self.redirect_poll_path}/{state}"
        return url
    
    def get_base_cache_dir(self) -> Path:
        # Base directory for OAuth cache
        base_cache_dir = Path.home().joinpath('.mcp').joinpath('auth')
        base_cache_dir.mkdir(parents=True, exist_ok=True)
        return base_cache_dir
    
    @property
    def callback_url(self) -> str:
        """
        Full redirect URL (only used for remote mode).
        """
        return f"{self.redirect_service_base_url}{self.redirect_callback_path}"
    
    @property
    def auth_header(self) -> dict | None:
        """
        Get the authentication header for the redirect service.
        """
        if self.cli_auth_token:
            return {'Authorization': f'Bearer {self.cli_auth_token}'}
        return None
