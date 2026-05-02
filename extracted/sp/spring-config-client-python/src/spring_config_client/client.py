import os
import re
import requests
from typing import Optional


def _interpolate(value: str) -> str:
    """Replace ${VAR} with os.environ.get('VAR')"""
    pattern = r'\$\{([^}]+)\}'

    def replacer(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))

    return re.sub(pattern, replacer, value)


class SpringConfigClient:
    """Simple client for Spring Cloud Config Server"""

    def __init__(
            self,
            server_url: str,
            app_name: str,
            profile: str = "default",
            username: Optional[str] = None,
            password: Optional[str] = None,
            timeout: int = 10
    ):
        self.server_url = server_url.rstrip('/')
        self.app_name = app_name
        self.profile = profile
        self.auth = (username, password) if username and password else None
        self.timeout = timeout

    def fetch_and_load(self) -> dict:
        """Fetch config from server and load into os.environ

        Returns:
            dict: The merged configuration

        Raises:
            requests.RequestException: If config server is unreachable
        """
        url = f"{self.server_url}/{self.app_name}/{self.profile}"

        response = requests.get(url, auth=self.auth, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()

        # Merge property sources (last in list = lowest priority)
        merged = {}
        for source in reversed(data.get('propertySources', [])):
            merged.update(source.get('source', {}))

        # Load into environment with interpolation
        for key, value in merged.items():
            os.environ[key] = _interpolate(str(value))

        return merged

