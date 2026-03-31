######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-03-31T03:38:01.665979                                                            #
######################################################################################################

from __future__ import annotations

import typing
from typing import TypedDict
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs
    import typing
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config

from .unified_config import CoreConfig as CoreConfig

TYPE_CHECKING: bool

class ResourceConfigDict(TypedDict, total=False):
    cpu: typing.Optional[str]
    memory: typing.Optional[str]
    gpu: typing.Optional[str]
    disk: typing.Optional[str]
    shared_memory: typing.Optional[str]

class AuthConfigDict(TypedDict, total=False):
    type: typing.Optional[str]
    public: typing.Optional[bool]

class ReplicaConfigDict(TypedDict, total=False):
    fixed: typing.Optional[int]
    min: typing.Optional[int]
    max: typing.Optional[int]
    scaling_policy: typing.Optional["ScalingPolicyConfigDict"]

class ScalingPolicyConfigDict(TypedDict, total=False):
    rpm: typing.Optional[int]

class DependencyConfigDict(TypedDict, total=False):
    from_requirements_file: typing.Optional[str]
    from_pyproject_toml: typing.Optional[str]
    python: typing.Optional[str]
    pypi: typing.Optional[dict]
    conda: typing.Optional[dict]

class PackageConfigDict(TypedDict, total=False):
    src_paths: typing.Optional[list]
    suffixes: typing.Optional[list]

class TypedCoreConfig(object, metaclass=type):
    """
    Parameters
    ----------
    name : str, optional
        The name of the app to deploy.
    
    port : int, optional
        Port where the app is hosted. When deployed this will be port on which we will deploy the app.
    
    description : str, optional
        The description of the app to deploy.
    
    app_type : str, optional
        The User defined type of app to deploy. Its only used for bookkeeping purposes.
    
    image : str, optional
        The Docker image to deploy with the App.
    
    tags : list, optional
        The tags of the app to deploy.
    
    secrets : list, optional
        Outerbounds integrations to attach to the app. You can use the value you set in the `@secrets` decorator in your code.
    
    compute_pools : list, optional
        A list of compute pools to deploy the app to.
    
    environment : dict, optional
        Environment variables to deploy with the App.
    
    commands : list, optional
        A list of commands to run the app with.
    
    resources : ResourceConfigDict, optional
        Resource configuration for the app.
            - cpu (str)
                CPU requests
            - memory (str)
                Memory requests
            - gpu (str)
                GPU requests
            - disk (str)
                Storage disk size.
            - shared_memory (str)
                Shared memory
    
    auth : AuthConfigDict, optional
        Auth related configurations.
            - type (str)
                The type of authentication to use for the app.
            - public (bool)
                Whether the app is public or not.
    
    replicas : ReplicaConfigDict, optional
        The number of replicas to deploy the app with.
            - fixed (int)
                The fixed number of replicas to deploy the app with. If min and max are set, this will raise an error.
            - min (int)
                The minimum number of replicas to deploy the app with.
            - max (int)
                The maximum number of replicas to deploy the app with.
            - scaling_policy (ScalingPolicyConfigDict)
                Scaling policy defines the the metric based on which the replicas will horizontally scale. If min and max replicas are set and are not the same, then a scaling policy will be applied. Default scaling policies can be 60 rpm (ie 1 rps).
                - rpm (int)
                    Scale up replicas when the requests per minute crosses this threshold. If nothing is provided and the replicas.max and replicas.min is set then the default rpm would be 60.
    
    code_package : tuple, optional
        Pre-packaged code from package_code(). A PackagedCode namedtuple containing url and key.
    
    force_upgrade : bool, optional
        Force upgrade the app even if it is currently being upgraded.
    
    use_base_image_command : bool, optional
        When True, skip providing startup commands and rely on the container's entrypoint/CMD. Only available in the programmatic API. In CLI mode, use `--no-deps` along side passing no command to enable this behavior.
    
    skip_code_package : bool, optional
        When True, skip code packaging and rely on the container's embedded source code. When running the deployer programmatically, If this field is set, then the user cannot pass `package-code`
    
    persistence : str, optional
        The persistence mode to deploy the app with.
        [Experimental] May change in the future.
    
    project : str, optional
        The project name to deploy the app to.
        [Experimental] May change in the future.
    
    branch : str, optional
        The branch name to deploy the app to.
        [Experimental] May change in the future.
    
    models : list, optional
        [Experimental] May change in the future.
    
    data : list, optional
        [Experimental] May change in the future.
    
    generate_static_url : bool, optional
        Generate a static URL for the app based on its name.
    """
    def __init__(self, name: typing.Optional[str] = None, port: typing.Optional[int] = None, description: typing.Optional[str] = None, app_type: typing.Optional[str] = None, image: typing.Optional[str] = None, tags: typing.Optional[list] = None, secrets: typing.Optional[list] = None, compute_pools: typing.Optional[list] = None, environment: typing.Optional[dict] = None, commands: typing.Optional[list] = None, resources: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.ResourceConfigDict] = None, auth: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.AuthConfigDict] = None, replicas: typing.Optional[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.ReplicaConfigDict] = None, code_package: typing.Optional[tuple] = None, force_upgrade: typing.Optional[bool] = None, use_base_image_command: typing.Optional[bool] = None, skip_code_package: typing.Optional[bool] = None, persistence: typing.Optional[str] = None, project: typing.Optional[str] = None, branch: typing.Optional[str] = None, models: typing.Optional[list] = None, data: typing.Optional[list] = None, generate_static_url: typing.Optional[bool] = None, **kwargs):
        ...
    def create_config(self) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config.CoreConfig:
        ...
    def to_dict(self) -> typing.Dict[str, typing.Any]:
        ...
    ...

