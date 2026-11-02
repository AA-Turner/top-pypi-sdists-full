from typing import Any

import httpx

from rock.sdk.envhub.schema import EnvHubClientConfig, RockEnvInfo
from rock.utils import HttpUtils


class EnvHubError(Exception):
    """Exception class for EnvHub."""

    pass


class EnvHubClient:
    """EnvHub client for communicating with EnvHub server."""

    def __init__(self, config: EnvHubClientConfig | None = None):
        """
        Initialize the EnvHub client.

        Args:
            config: EnvHub configuration object.
        """
        if config:
            self.config = config
        else:
            self.config = EnvHubClientConfig()
        self.base_url = self.config.base_url
        self.headers = {"Content-Type": "application/json"}

    async def register(
        self,
        env_name: str,
        image: str,
        owner: str = "",
        description: str = "",
        tags: list[str] | None = None,
        extra_spec: dict[str, Any] | None = None,
    ) -> RockEnvInfo:
        """
        Register or update an environment.

        Args:
            env_name: Environment name.
            image: Docker image.
            owner: Environment owner.
            description: Environment description.
            tags: List of environment tags.
            extra_spec: Additional environment specifications.

        Returns:
            Environment information dictionary.

        Raises:
            EnvHubError: Raised when registration fails.
        """
        url = f"{self.base_url}/env/register"
        payload = {
            "env_name": env_name,
            "image": image,
            "owner": owner,
            "description": description,
            "tags": tags or [],
            "extra_spec": extra_spec,
        }

        try:
            response = await HttpUtils.post(url, self.headers, payload)
            return RockEnvInfo.from_dict(response)
        except Exception as e:
            raise EnvHubError(f"Failed to register environment: {e}") from e

    async def get_env(self, env_name: str) -> RockEnvInfo:
        """
        Get environment by name.

        Args:
            env_name: Environment name.

        Returns:
            Environment information dictionary.

        Raises:
            EnvHubError: Raised when getting environment fails.
        """
        url = f"{self.base_url}/env/get"
        payload = {"env_name": env_name}

        try:
            response = await HttpUtils.post(url, self.headers, payload)
            return RockEnvInfo.from_dict(response)
        except Exception as e:
            raise EnvHubError(f"Failed to get environment {env_name}: {e}") from e

    async def list_envs(self, owner: str | None = None, tags: list[str] | None = None) -> list[RockEnvInfo]:
        """
        List environments, supporting filtering by owner and tags.

        Args:
            owner: Environment owner.
            tags: List of environment tags.

        Returns:
            List of environment information dictionaries.

        Raises:
            EnvHubError: Raised when listing environments fails.
        """
        url = f"{self.base_url}/env/list"
        payload = {"owner": owner, "tags": tags}

        try:
            response = await HttpUtils.post(url, self.headers, payload)
            envs_data = response.get("envs", [])
            return [RockEnvInfo.from_dict(env_data) for env_data in envs_data]
        except Exception as e:
            raise EnvHubError(f"Failed to list environments: {e}") from e

    async def delete_env(self, env_name: str) -> bool:
        """
        Delete environment.

        Args:
            env_name: Environment name.

        Returns:
            True if deletion is successful, False otherwise.

        Raises:
            EnvHubError: Raised when environment deletion fails.
        """
        url = f"{self.base_url}/env/delete"
        payload = {"env_name": env_name}

        try:
            response = await HttpUtils.post(url, self.headers, payload)
            return response
        except httpx.HTTPStatusError as e:
            # If it's a 404 error, it means the environment doesn't exist, return False
            if e.response.status_code == 404:
                return False
            # Other HTTP errors still raise the exception
            raise EnvHubError(f"Failed to delete environment {env_name}: {e}") from e
        except Exception as e:
            raise EnvHubError(f"Failed to delete environment {env_name}: {e}") from e

    async def health_check(self) -> dict[str, str]:
        """
        Health check.

        Returns:
            Health status dictionary.

        Raises:
            EnvHubError: Raised when health check fails.
        """
        url = f"{self.base_url}/health"

        try:
            response = await HttpUtils.get(url, self.headers)
            return response
        except Exception as e:
            raise EnvHubError(f"Failed to health check: {e}") from e
