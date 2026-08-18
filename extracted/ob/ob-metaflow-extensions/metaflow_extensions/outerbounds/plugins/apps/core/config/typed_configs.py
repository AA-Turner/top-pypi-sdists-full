"""
Auto-generated typed classes for ConfigMeta classes.

This module provides IDE-friendly typed interfaces for all configuration classes.
The reason we auto-generate this file is because we want to provide a bridge between what is the ConfigMeta classes and the typed programmatic interface.
The CoreConfig class is setup in a way that if any additionally params are missed out from being auto-generated then it will not affect the core functionality of the programmatic API.
The new parameters will just not show up in IDE autocompletions.
It is fine if this file is not regularly updated by running the script in the .pre-commit-config.app-changes.yaml
but it is recommended that this file not be deleted or manually edited.

"""

from typing import Optional, List, Dict, Any
from .unified_config import CoreConfig

import sys
from typing import TYPE_CHECKING

# on 3.8+ use the stdlib TypedDict;
# in TYPE_CHECKING blocks mypy/pyright still pick it up on older Pythons
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    if TYPE_CHECKING:
        # for the benefit of type-checkers
        from typing import TypedDict  # noqa: F401
    # runtime no-op TypedDict shim
    class _TypedDictMeta(type):
        def __new__(cls, name, bases, namespace, total=True):
            # ignore total at runtime
            return super().__new__(cls, name, bases, namespace)

    class TypedDict(dict, metaclass=_TypedDictMeta):
        # Runtime stand-in for typing.TypedDict on <3.8.
        pass


class ResourceConfigDict(TypedDict, total=False):
    cpu: Optional[str]
    memory: Optional[str]
    gpu: Optional[str]
    disk: Optional[str]
    shared_memory: Optional[str]


class AuthConfigDict(TypedDict, total=False):
    type: Optional[str]
    public: Optional[bool]


class ReplicaConfigDict(TypedDict, total=False):
    fixed: Optional[int]
    min: Optional[int]
    max: Optional[int]
    scaling_policy: Optional["ScalingPolicyConfigDict"]


class ScalingPolicyConfigDict(TypedDict, total=False):
    rpm: Optional[int]


class DependencyConfigDict(TypedDict, total=False):
    from_requirements_file: Optional[str]
    from_pyproject_toml: Optional[str]
    python: Optional[str]
    pypi: Optional[dict]
    conda: Optional[dict]


class PackageConfigDict(TypedDict, total=False):
    src_paths: Optional[list]
    suffixes: Optional[list]


class ProxyConfigDict(TypedDict, total=False):
    namespace: Optional[str]
    selector_labels: Optional[dict]
    service_url: Optional[str]


class TypedCoreConfig:
    """
    Parameters
    ----------
    name : str, optional
        The name of the app to deploy.

    port : int, optional
        Port where the app is hosted. When deployed this will be port on which we will deploy the app. For a `Proxy` capsule this is the port of the pods being proxied, and it is not needed when `proxy.service_url` is used.

    description : str, optional
        The description of the app to deploy.

    app_type : str, optional
        The User defined type of app to deploy. Its only used for bookkeeping purposes.

    image : str, optional
        The Docker image to deploy with the App.

    tags : list, optional
        The tags of the app to deploy.

    secrets : list, optional
        Outerbounds integrations to attach to the app. You can use the value you set in the `@secrets` decorator in your code without the outerbounds prefix.

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
        When True, skip code packaging and rely on the container's embedded source code. When running the deployer programmatically, If this field is set, then the user cannot pass `code_package` parameter to the AppDeployer

    capsule_type : str, optional
        What the platform runs for this deployment. `Standard` (the default) runs the image and commands configured here. `Proxy` runs nothing of its own and only fronts a workload that is already running in the cluster, described by `proxy`.

    proxy : ProxyConfigDict, optional
        The workload a `Proxy` capsule forwards traffic to. Can only be set when `capsule_type` is `Proxy`.
            - namespace (str)
                The namespace where the pods being proxied live. The service fronting them is created here. Required unless `service_url` is set.
            - selector_labels (dict)
                The labels of the pods being proxied. They become the selector of the service that fronts those pods, so they must match the labels on them. Required unless `service_url` is set.
            - service_url (str)
                The address of a service that already exists, e.g. `my-svc.my-ns.svc.cluster.local:8080`. The scheme is optional and defaults to http, a port must be included if the target isn't on the scheme's default port, and a path may be appended to rewrite requests into a subpath of the target. The address is not checked at deploy time: if it doesn't resolve, the proxy crashloops until it does.

    url_slug : str, optional
        Names the app's URL instead of having one generated for it: `api-<url_slug>.<your platform domain>`, or `ui-<url_slug>` for an app with browser-only auth. Cannot be combined with `generate_static_url`, which is the other way of deciding the same URL. A slug belongs to a single app across the whole platform deployment, and cannot be changed once an app has one.

    persistence : str, optional
        The persistence mode to deploy the app with.
        [Experimental] May change in the future.

    project : str, optional
        The project name for the app. Defaults to __unassigned__.

    branch : str, optional
        The branch name for the app. Defaults to __unassigned__.

    models : list, optional
        [Experimental] May change in the future.

    data : list, optional
        [Experimental] May change in the future.

    generate_static_url : bool, optional
        Generate a static URL for the app based on its name. Cannot be combined with `url_slug`, which names the URL instead.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        port: Optional[int] = None,
        description: Optional[str] = None,
        app_type: Optional[str] = None,
        image: Optional[str] = None,
        tags: Optional[list] = None,
        secrets: Optional[list] = None,
        compute_pools: Optional[list] = None,
        environment: Optional[dict] = None,
        commands: Optional[list] = None,
        resources: Optional[ResourceConfigDict] = None,
        auth: Optional[AuthConfigDict] = None,
        replicas: Optional[ReplicaConfigDict] = None,
        code_package: Optional[tuple] = None,
        force_upgrade: Optional[bool] = None,
        use_base_image_command: Optional[bool] = None,
        skip_code_package: Optional[bool] = None,
        capsule_type: Optional[str] = None,
        proxy: Optional[ProxyConfigDict] = None,
        url_slug: Optional[str] = None,
        persistence: Optional[str] = None,
        project: Optional[str] = None,
        branch: Optional[str] = None,
        models: Optional[list] = None,
        data: Optional[list] = None,
        generate_static_url: Optional[bool] = None,
        **kwargs
    ) -> None:
        self._kwargs = {
            "name": name,
            "port": port,
            "description": description,
            "app_type": app_type,
            "image": image,
            "tags": tags,
            "secrets": secrets,
            "compute_pools": compute_pools,
            "environment": environment,
            "commands": commands,
            "resources": resources,
            "auth": auth,
            "replicas": replicas,
            "code_package": code_package,
            "force_upgrade": force_upgrade,
            "use_base_image_command": use_base_image_command,
            "skip_code_package": skip_code_package,
            "capsule_type": capsule_type,
            "proxy": proxy,
            "url_slug": url_slug,
            "persistence": persistence,
            "project": project,
            "branch": branch,
            "models": models,
            "data": data,
            "generate_static_url": generate_static_url,
        }
        # Add any additional kwargs
        self._kwargs.update(kwargs)
        # Remove None values
        self._kwargs = {k: v for k, v in self._kwargs.items() if v is not None}
        self._config_class = CoreConfig
        self._config = self.create_config()
        self._init()

    def create_config(self) -> CoreConfig:
        return CoreConfig.from_dict(self._kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return self._config.to_dict()

    def _init(self):
        raise NotImplementedError
