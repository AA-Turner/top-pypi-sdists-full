from typing import Any

from typing_extensions import Self

from rock.actions import IsAliveResponse
from rock.deployments.abstract import AbstractDeployment
from rock.deployments.config import RemoteDeploymentConfig
from rock.deployments.hooks.abstract import CombinedDeploymentHook, DeploymentHook
from rock.logger import init_logger
from rock.rocklet.exceptions import DeploymentNotStartedError
from rock.sandbox.remote_sandbox import RemoteSandboxRuntime

logger = init_logger(__name__)


class RemoteDeployment(AbstractDeployment):
    def __init__(self, **kwargs: Any):
        """This deployment is only a thin wrapper around the `RemoteRuntime`.
        Use this if you have deployed a runtime somewhere else but want to interact with it
        through the `AbstractDeployment` interface.
        For example, if you have an agent that you usually use with a `DocerkDeployment` interface,
        you sometimes might want to manually start a docker container for debugging purposes.
        Then you can use this deployment to explicitly connect to your manually started runtime.

        Args:
            **kwargs: Keyword arguments (see `RemoteDeploymentConfig` for details).
        """
        self._config = RemoteDeploymentConfig(**kwargs)
        self._runtime: RemoteSandboxRuntime | None = None
        self._hooks = CombinedDeploymentHook()

    def add_hook(self, hook: DeploymentHook):
        self._hooks.add_hook(hook)

    @classmethod
    def from_config(cls, config: RemoteDeploymentConfig) -> Self:
        return cls(**config.model_dump())

    @property
    def runtime(self) -> RemoteSandboxRuntime:
        """Returns the runtime if running.

        Raises:
            DeploymentNotStartedError: If the deployment was not started.
        """
        if self._runtime is None:
            raise DeploymentNotStartedError()
        return self._runtime

    async def is_alive(self) -> IsAliveResponse:
        """Checks if the runtime is alive. The return value can be
        tested with bool().

        Raises:
            DeploymentNotStartedError: If the deployment was not started.
        """
        return await self.runtime.is_alive()

    async def start(self):
        """Starts the runtime."""
        logger.info("Starting remote runtime")
        self._runtime = RemoteSandboxRuntime(
            host=self._config.host,
            port=self._config.port,
            timeout=self._config.timeout,
        )

    async def stop(self):
        """Stops the runtime."""
        self.runtime.close()
        self._runtime = None
