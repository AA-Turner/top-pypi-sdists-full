######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.529328                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.deployer

from .config.typed_configs import TypedCoreConfig as TypedCoreConfig
from ._state_machine import DEPLOYMENT_READY_CONDITIONS as DEPLOYMENT_READY_CONDITIONS
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
    def app_config(self) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config.AppConfig:
        ...
    def deploy(self, readiness_condition = 'at_least_one_running', max_wait_time = 600, readiness_wait_time = 10, logger_fn = ..., status_file = None, no_loader = False, **kwargs):
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

