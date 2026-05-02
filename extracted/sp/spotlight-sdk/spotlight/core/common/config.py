"""
Configuration classes used for configuring the Spotlight SDK.
"""

import os
from typing import Optional


class Auth:
    """
    Configuration class for getting the authentication information from the environment.
    """

    # Feature to keep values hidden from printing (not totally)
    # Allows for dynamic rendering of auth values
    @property
    def username(self) -> Optional[str]:
        return os.getenv("SPOTLIGHT_USER", None)

    @property
    def password(self) -> Optional[str]:
        return os.getenv("SPOTLIGHT_PWD", None)

    @property
    def access_token(self) -> Optional[str]:
        return os.getenv("SPOTLIGHT_ACCESS_TOKEN", None)

    @property
    def refresh_token(self) -> Optional[str]:
        return os.getenv("SPOTLIGHT_REFRESH_TOKEN", None)

    @property
    def barchart_api_token(self) -> Optional[str]:
        return os.getenv("SPOTLIGHT_BARCHART_API_TOKEN", None)

    def can_authenticate(self) -> bool:
        """
        Check environment to see if the user provided enough info to authenticate requests.

        Returns:
            bool: A boolean that represents whether you can authenticate requests
        """
        auth_options = (
            self.access_token or self.refresh_token or (self.username and self.password)
        )
        return auth_options is not None

    def __eq__(self, other: "Auth"):
        return (
            self.access_token == other.access_token
            and self.username == self.username
            and self.password == self.password
        )


class EnvironmentConfig:
    """
    Configuration class for getting environment information.
    """

    auth_config: Auth = Auth()

    @property
    def environment(self) -> str:
        env = os.getenv("SPOTLIGHT_ENV", "production")
        return env

    @property
    def urls(self) -> dict:
        env_url_map = {
            "production": {
                "spotlight": "https://api.spotlight.dev",
                "keycloak_admin": "https://auth.spotlight.dev/auth/admin/realms/production",
                "keycloak": "https://auth.spotlight.dev/auth/realms/production",
                "barchart": "https://ondemand.websol.barchart.com",
            },
            "development": {
                "spotlight": "https://api.dev.spotlight.dev",
                "keycloak_admin": "https://auth.dev.spotlight.dev/auth/admin/realms/production",
                "keycloak": "https://auth.dev.spotlight.dev/auth/realms/production",
                "barchart": "https://ondemand.websol.barchart.com",
            },
        }
        return env_url_map.get(self.environment, env_url_map["production"])

    def get_url(self, key: str = "spotlight") -> str:
        """
        Get base URL given key.

        Args:
            key (str): URL key; 'spotlight', 'keycloak_admin', 'keycloak' or 'fred'

        Returns:
            str: Base URL string
        """
        return self.urls.get(key, self.urls["spotlight"])
