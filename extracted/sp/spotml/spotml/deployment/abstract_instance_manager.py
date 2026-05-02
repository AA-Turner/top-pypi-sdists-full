import subprocess
from abc import ABC, abstractmethod
from spotml.commands.writers.abstract_output_writrer import AbstractOutputWriter
from spotml.config.abstract_instance_config import AbstractInstanceConfig
from spotml.config.project_config import ProjectConfig
from spotml.deployment.container.abstract_container_commands import AbstractContainerCommands


class AbstractInstanceManager(ABC):

    def __init__(self, project_config: ProjectConfig, instance_config: dict):
        self._project_config = project_config
        self._instance_config = self._get_instance_config(instance_config)

    @property
    def project_config(self) -> ProjectConfig:
        return self._project_config

    @property
    def instance_config(self) -> AbstractInstanceConfig:
        return self._instance_config

    @property
    def ssh_key_path(self):
        raise NotImplementedError

    @abstractmethod
    def _get_instance_config(self, instance_config: dict) -> AbstractInstanceConfig:
        """A factory method to create a provider's instance config."""
        raise NotImplementedError

    @property
    @abstractmethod
    def container_commands(self) -> AbstractContainerCommands:
        """A collection of commands to manage a container from the host OS."""
        raise NotImplementedError

    @abstractmethod
    def is_running(self) -> bool:
        """Checks if the instance is running."""
        raise NotImplementedError

    @abstractmethod
    def start(self, output: AbstractOutputWriter, dry_run=False):
        """Creates a stack with the instance."""
        raise NotImplementedError

    @abstractmethod
    def start_container(self, output: AbstractOutputWriter, dry_run=False):
        """Starts or restarts container on the host OS."""
        raise NotImplementedError

    @abstractmethod
    def stop(self, only_shutdown: bool, output: AbstractOutputWriter):
        """Deletes the stack."""
        raise NotImplementedError

    def exec(self, command: str, tty: bool = True) -> int:
        """Executes a command on the host OS."""
        result = subprocess.run(command, shell=True)
        return result.returncode

    def exec_capture_output(self, command: str) -> subprocess.CompletedProcess:
        """Executes a command on the host OS."""
        return subprocess.run(command, shell=True, stdout=subprocess.PIPE)

    @abstractmethod
    def clean(self, output: AbstractOutputWriter):
        """Deletes the stack."""
        raise NotImplementedError

    @abstractmethod
    def sync(self, output: AbstractOutputWriter, dry_run=False):
        """Synchronizes the project code with the instance."""
        raise NotImplementedError

    @abstractmethod
    def sync_to_bucket(self, output: AbstractOutputWriter, dry_run=False):
        """Synchronizes the project code with the instance."""
        raise NotImplementedError

    @abstractmethod
    def create_or_get_bucket(self, output: AbstractOutputWriter, dry_run: bool = False):
        """Synchronizes the project code with the instance."""
        raise NotImplementedError

    @abstractmethod
    def sync_to_instance(self, output: AbstractOutputWriter, dry_run=False):
        """Synchronizes the project code with the instance."""
        raise NotImplementedError

    @abstractmethod
    def download(self, download_filters: list, output: AbstractOutputWriter, dry_run=False):
        """Downloads files from the instance."""
        raise NotImplementedError

    @abstractmethod
    def get_status_text(self) -> str:
        """Returns information about the started instance.

        It will be shown to the user once the instance is started and by using the "status" command.
        """
        raise NotImplementedError

    @abstractmethod
    def sendConfigCredentialFiles(self) -> None:
        """Gets spotml config and credentials needed to run commands remotely."""
        raise NotImplementedError

    @abstractmethod
    def check_dockerfile_exists(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def maybe_create_key(self) -> None:
        raise NotImplementedError

    @property
    def use_tmux(self) -> bool:
        """Use tmux when running a custom script or connecting to the instance."""
        return False
