######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.7.5+obcheckpoint(0.2.7);ob(v1)                                                    #
# Generated on 2025-09-23T01:34:30.689496                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config
    import datetime
    import metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.deployer

from .config.typed_configs import TypedCoreConfig as TypedCoreConfig
from .perimeters import PerimeterExtractor as PerimeterExtractor
from .capsule import CapsuleApi as CapsuleApi
from ._state_machine import DEPLOYMENT_READY_CONDITIONS as DEPLOYMENT_READY_CONDITIONS
from ._state_machine import LogLine as LogLine
from .app_config import AppConfig as AppConfig
from .app_config import AppConfigError as AppConfigError
from .capsule import CapsuleDeployer as CapsuleDeployer
from .capsule import list_and_filter_capsules as list_and_filter_capsules

class AppDeployer(metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.TypedCoreConfig, metaclass=type):
    """
    """
    def __init__(self, name: typing.Optional[str] = None, port: typing.Optional[int] = None, description: typing.Optional[str] = None, app_type: typing.Optional[str] = None, image: typing.Optional[str] = None, tags: typing.Optional[list] = None, secrets: typing.Optional[list] = None, compute_pools: typing.Optional[list] = None, environment: typing.Optional[dict] = None, commands: typing.Optional[list] = None, resources: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.ResourceConfigDict] = None, auth: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.AuthConfigDict] = None, replicas: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.ReplicaConfigDict] = None, dependencies: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.DependencyConfigDict] = None, package: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.PackageConfigDict] = None, no_deps: typing.Optional[bool] = None, force_upgrade: typing.Optional[bool] = None, persistence: typing.Optional[str] = None, project: typing.Optional[str] = None, branch: typing.Optional[str] = None, models: typing.Optional[list] = None, data: typing.Optional[list] = None, **kwargs):
        ...
    @property
    def _deploy_config(self) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config.AppConfig:
        ...
    def deploy(self, readiness_condition = 'at_least_one_running', max_wait_time = 600, readiness_wait_time = 10, logger_fn = ..., status_file = None, no_loader = False, **kwargs) -> DeployedApp:
        ...
    ...

class DeployedApp(object, metaclass=type):
    def __init__(self, _id: str, capsule_type: str, public_url: str, name: str, deployed_version: str, deployed_at: str):
        ...
    def logs(self, previous = False) -> typing.Dict[str, typing.List[metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.LogLine]]:
        """
        Returns a dictionary of worker_id to logs.
        If `previous` is True, it will return the logs from the previous execution of the workers. Useful when debugging a crashlooping worker.
        """
        ...
    def info(self) -> dict:
        """
        Returns a dictionary representing the deployed app.
        """
        ...
    def replicas(self):
        ...
    def scale_to_zero(self):
        """
        Scales the DeployedApp to 0 replicas.
        """
        ...
    def delete(self):
        """
        Deletes the DeployedApp.
        """
        ...
    @property
    def id(self) -> str:
        ...
    @property
    def auth_style(self) -> str:
        ...
    @property
    def public_url(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def deployed_version(self) -> str:
        ...
    def to_dict(self) -> dict:
        ...
    @classmethod
    def from_dict(cls, data: dict):
        ...
    @property
    def deployed_at(self) -> datetime.datetime:
        ...
    def __repr__(self) -> str:
        ...
    ...

class apps(object, metaclass=type):
    @classmethod
    def set_name_prefix(cls, name_prefix: str):
        ...
    @property
    def name_prefix(self) -> str:
        ...
    @property
    def Deployer(self) -> typing.Type[metaflow.mf_extensions.outerbounds.plugins.apps.core.deployer.AppDeployer]:
        ...
    ...

