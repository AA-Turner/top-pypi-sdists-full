######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.558435                                                            #
######################################################################################################

from __future__ import annotations

import typing
from typing import TypedDict
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config
    import typing
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs

from .unified_config import CoreConfig as CoreConfig

TYPE_CHECKING: bool

class ResourceConfigDict(TypedDict, total=False):
    cpu: typing.Optional[str]
    memory: typing.Optional[str]
    gpu: typing.Optional[str]
    disk: typing.Optional[str]

class AuthConfigDict(TypedDict, total=False):
    type: typing.Optional[str]
    public: typing.Optional[bool]

class ReplicaConfigDict(TypedDict, total=False):
    fixed: typing.Optional[int]
    min: typing.Optional[int]
    max: typing.Optional[int]

class DependencyConfigDict(TypedDict, total=False):
    from_requirements_file: typing.Optional[str]
    from_pyproject_toml: typing.Optional[str]
    python: typing.Optional[str]
    pypi: typing.Optional[dict]
    conda: typing.Optional[dict]

class PackageConfigDict(TypedDict, total=False):
    src_path: typing.Optional[str]
    suffixes: typing.Optional[list]

class TypedCoreConfig(object, metaclass=type):
    def __init__(self, name: typing.Optional[str] = None, port: typing.Optional[int] = None, description: typing.Optional[str] = None, app_type: typing.Optional[str] = None, image: typing.Optional[str] = None, tags: typing.Optional[list] = None, secrets: typing.Optional[list] = None, compute_pools: typing.Optional[list] = None, environment: typing.Optional[dict] = None, commands: typing.Optional[list] = None, resources: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.ResourceConfigDict] = None, auth: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.AuthConfigDict] = None, replicas: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.ReplicaConfigDict] = None, dependencies: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.DependencyConfigDict] = None, package: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.PackageConfigDict] = None, no_deps: typing.Optional[bool] = None, force_upgrade: typing.Optional[bool] = None, persistence: typing.Optional[str] = None, project: typing.Optional[str] = None, branch: typing.Optional[str] = None, models: typing.Optional[list] = None, data: typing.Optional[list] = None, **kwargs):
        ...
    def create_config(self) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config.CoreConfig:
        ...
    def to_dict(self) -> typing.Dict[str, typing.Any]:
        ...
    ...

