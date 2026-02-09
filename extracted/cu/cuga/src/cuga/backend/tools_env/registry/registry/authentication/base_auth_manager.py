from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseAuthManager(ABC):
    def __init__(self):
        self._tokens: Dict[str, str] = {}

    def get_access_token(self, app_name: str) -> Optional[str]:
        """Get access token for app_name, using stored token if available, otherwise fetch new one."""
        # First check if we already have a stored token
        stored_token = self._tokens.get(app_name)
        if stored_token:
            return stored_token

        # No stored token, fetch a new one
        creds = self._get_credentials(app_name)
        if creds is None:
            return None

        try:
            token_info = self._fetch_token(app_name, creds)
            token = token_info.get("access_token")
            if not token:
                raise Exception("Failed to obtain access token")

            # Store the token in memory
            self._tokens[app_name] = token
            return token
        except Exception:
            # Re-raise with original exception to preserve detailed error messages
            raise

    def clear_tokens(self):
        """Clear all stored tokens. Used when reset endpoint is called."""
        self._tokens.clear()

    def get_stored_token(self, app_name: str) -> Optional[str]:
        """Get token from memory by app_name."""
        return self._tokens.get(app_name)

    def get_stored_tokens(self) -> dict:
        """Get token from memory by app_name."""
        return self._tokens

    @abstractmethod
    def _get_credentials(self, app_name: str) -> Optional[str]:
        """Return password (or other creds) for app_name, or None if unknown."""
        pass

    @abstractmethod
    def _fetch_token(self, app_name: str, creds: str) -> dict:
        """Hit your auth endpoint and return its JSON response."""
        pass
