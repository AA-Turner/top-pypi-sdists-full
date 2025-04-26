import os
from pathlib import Path
from typing import Type, Optional

import toml
from pydantic import BaseModel, ConfigDict

from vessl.util.constant import TRACING_AGREEMENT

DEFAULT_VESSL_DIR = os.path.join(str(Path.home()), ".vessl")
DEFAULT_CONFIG_PATH = os.environ.get("VESSL_CONFIG_PATH", os.path.join(DEFAULT_VESSL_DIR, "config"))
SAVE_CONFIG = os.environ.get("VESSL_SAVE_CONFIG", "true").lower() == "true"


class ConfigLoader:
    def __init__(self, filename: str, schema: Type[BaseModel]):
        self.filename = filename
        self.config = schema.model_validate(self._load())

    def _load(self):
        if not Path(self.filename).is_file():
            return {}

        with open(self.filename) as f:
            return toml.load(f)

    def reset(self):
        self.config = self.config.model_validate({})
        self.save()

    def save(self):
        if not SAVE_CONFIG:
            return
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "w") as f:
            toml.dump(self.config.model_dump(), f)


class UserConfig(BaseModel):
    access_token: Optional[str] = None
    default_organization: Optional[str] = None
    default_project: Optional[str] = None
    workspace: Optional[int] = None
    cluster_kubeconfig: Optional[str] = None
    kubernetes_namespace: Optional[str] = None
    use_k0s_in_docker: Optional[bool] = None
    default_ssh_private_key_path: Optional[str] = None

    model_config = ConfigDict(extra='ignore')


class VesslConfig(BaseModel):
    user: Optional[UserConfig] = UserConfig()


class VesslConfigLoader(ConfigLoader):
    config: VesslConfig

    def __init__(self, path: str = DEFAULT_CONFIG_PATH):
        super().__init__(path, VesslConfig)

    @property
    def access_token(self):
        return self.config.user.access_token

    @access_token.setter
    def access_token(self, access_token: str):
        if access_token:
            self.config.user.access_token = access_token
        self.save()

    @property
    def default_organization(self):
        return self.config.user.default_organization

    @default_organization.setter
    def default_organization(self, default_organization_name: str):
        self.config.user.default_organization = default_organization_name
        self.save()

    @property
    def default_project(self):
        return self.config.user.default_project

    @default_project.setter
    def default_project(self, default_project_name: str):
        self.config.user.default_project = default_project_name
        self.save()

    @property
    def workspace(self):
        return self.config.user.workspace

    @workspace.setter
    def workspace(self, workspace_id):
        self.config.user.workspace = workspace_id
        self.save()

    @property
    def cluster_kubeconfig(self) -> str:
        return self.config.user.cluster_kubeconfig

    @cluster_kubeconfig.setter
    def cluster_kubeconfig(self, cluster_kubeconfig_path: str):
        self.config.user.cluster_kubeconfig = cluster_kubeconfig_path
        self.save()

    @property
    def kubernetes_namespace(self) -> str:
        return self.config.user.kubernetes_namespace

    @kubernetes_namespace.setter
    def kubernetes_namespace(self, kubernetes_namespace: str):
        self.config.user.kubernetes_namespace = kubernetes_namespace
        self.save()

    @property
    def use_k0s_in_docker(self) -> bool:
        return self.config.user.use_k0s_in_docker

    @use_k0s_in_docker.setter
    def use_k0s_in_docker(self, use_k0s_in_docker: bool):
        self.config.user.use_k0s_in_docker = use_k0s_in_docker
        self.save()

    @property
    def default_ssh_private_key_path(self) -> str:
        return self.config.user.default_ssh_private_key_path

    @default_ssh_private_key_path.setter
    def default_ssh_private_key_path(self, default_ssh_private_key_path: str):
        self.config.user.default_ssh_private_key_path = default_ssh_private_key_path
        self.save()


def notified_user_data_collection() -> bool:
    file_path = os.path.join(DEFAULT_VESSL_DIR, "tracing-agreement")
    return Path(file_path).is_file()


def create_user_data_collection_file():
    path = os.path.join(DEFAULT_VESSL_DIR, "tracing-agreement")
    os.makedirs(DEFAULT_VESSL_DIR, exist_ok=True)
    with open(path, "w") as f:
        f.write(TRACING_AGREEMENT)

