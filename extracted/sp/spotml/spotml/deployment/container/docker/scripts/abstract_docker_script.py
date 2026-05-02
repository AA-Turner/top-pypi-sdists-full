from abc import ABC
from spotml.deployment.container.docker.docker_commands import DockerCommands
from spotml.deployment.container.abstract_container_script import AbstractContainerScript


class AbstractDockerScript(AbstractContainerScript, ABC):

    @property
    def commands(self) -> DockerCommands:
        return self._commands
