from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseAuthManager(ABC):
    def __init__(self):
        self._tokens: Dict[str, str] = {}

    def get_access_token(self, app_name: str) -> Optional[str]:
        """Fetch a new access token for app_name."""
        creds = self._get_credentials(app_name)
        if creds is None:
            return None

        token_info = self._fetch_token(app_name, creds)
        token = token_info.get("access_token")
        if not token:
            raise Exception("Failed to obtain access token")

        # Store the token in memory
        self._tokens[app_name] = token
        return token

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
