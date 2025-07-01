from abc import ABCMeta
from dataclasses import field, dataclass
from pathlib import Path
from typing import Optional

from qwak.clients.administration.eco_system.client import EcosystemClient
from qwak.clients.build_orchestrator import BuildOrchestratorClient
from qwak.clients.instance_template.client import InstanceTemplateManagementClient
from qwak.clients.model_management import ModelsManagementClient
from qwak.inner.build_logic.dependency_manager_type import DependencyManagerType
from qwak.inner.di_configuration.account import UserAccount, UserAccountConfiguration


@dataclass
class Context(metaclass=ABCMeta):
    # Clients
    client_builds_orchestrator: BuildOrchestratorClient = field(
        default_factory=BuildOrchestratorClient
    )
    client_models_management: ModelsManagementClient = field(
        default_factory=ModelsManagementClient
    )
    client_instance_template: InstanceTemplateManagementClient = field(
        default_factory=InstanceTemplateManagementClient
    )
    client_ecosystem: EcosystemClient = field(default_factory=EcosystemClient)

    # General
    user_account: UserAccount = field(
        default_factory=UserAccountConfiguration().get_user_config
    )

    # Pre fetch validation
    build_id: str = field(default="")
    model_id: str = field(default="")
    build_name: str = field(default="")
    project_uuid: str = field(default="")
    host_temp_local_build_dir: Path = field(default=None)
    model_uri: Path = field(default=None)
    git_credentials: str = field(default="")
    git_ssh_key: str = field(default="")

    # Fetch model
    git_commit_id: Optional[str] = field(default=None)

    # Post fetch validation
    dependency_manager_type: DependencyManagerType = field(
        default=DependencyManagerType.UNKNOWN
    )
    model_relative_dependency_file: Path = field(default=None)
    model_relative_dependency_lock_file: Path = field(default=None)

    # Upload model
    model_code_remote_url: Optional[str] = field(default=None)
    qwak_sdk_version: Optional[str] = field(default=None)

    # Image
    base_image: Optional[str] = field(default=None)

    # Upload Custom Wheels
    custom_runtime_wheel: Optional[Path] = field(default=None)
    custom_core_wheel: Optional[Path] = field(default=None)

    platform_url: Optional[str] = field(
        default_factory=UserAccountConfiguration().retrieve_platform_url
    )
