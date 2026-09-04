######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.2+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-04T00:14:52.287639                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import typing
    import metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config
    import datetime
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.deployer

from .config.typed_configs import TypedCoreConfig as TypedCoreConfig
from .perimeters import PerimeterExtractor as PerimeterExtractor
from .capsule import CapsuleApi as CapsuleApi
from ._state_machine import DEPLOYMENT_READY_CONDITIONS as DEPLOYMENT_READY_CONDITIONS
from ._state_machine import LogLine as LogLine
from .app_config import AppConfig as AppConfig
from .app_config import AppConfigError as AppConfigError
from .code_package.code_packager import CodePackager as CodePackager
from .config.unified_config import PackagedCode as PackagedCode
from .config.unified_config import BakedImage as BakedImage
from .config.unified_config import CapsuleType as CapsuleType
from .config.unified_config import AuthType as AuthType
from .capsule import CapsuleDeployer as CapsuleDeployer
from .capsule import list_and_filter_capsules as list_and_filter_capsules
from .exceptions import CapsuleDeploymentException as CapsuleDeploymentException
from .exceptions import CapsuleApiException as CapsuleApiException
from .exceptions import CapsuleCrashLoopException as CapsuleCrashLoopException
from .exceptions import CapsuleReadinessException as CapsuleReadinessException
from .exceptions import CapsuleConcurrentUpgradeException as CapsuleConcurrentUpgradeException
from .exceptions import CapsuleDeletedDuringDeploymentException as CapsuleDeletedDuringDeploymentException
from .exceptions import AppConcurrentUpgradeException as AppConcurrentUpgradeException
from .exceptions import AppCrashLoopException as AppCrashLoopException
from .exceptions import AppCreationFailedException as AppCreationFailedException
from .exceptions import AppDeletedDuringDeploymentException as AppDeletedDuringDeploymentException
from .exceptions import AppDeploymentException as AppDeploymentException
from .exceptions import AppNotFoundException as AppNotFoundException
from .exceptions import AppReadinessException as AppReadinessException
from .exceptions import AppUpgradeInProgressException as AppUpgradeInProgressException
from .exceptions import CodePackagingException as CodePackagingException
from .dependencies import ImageBakingException as ImageBakingException

CODE_PACKAGE_PREFIX: str

UNASSIGNED_PROJECT_BRANCH: str

def bake_image(pypi: typing.Union[typing.Dict[str, str], None] = None, conda: typing.Union[typing.Dict[str, str], None] = None, anaconda: typing.Union[typing.Dict[str, str], None] = None, requirements_file: typing.Union[str, None] = None, pyproject_toml: typing.Union[str, None] = None, base_image: typing.Union[str, None] = None, python: typing.Union[str, None] = None, logger: typing.Union[typing.Callable[[str], typing.Any], None] = None, cache_name: typing.Union[str, None] = None, extra_configs: typing.Union[dict, None] = None) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config.BakedImage:
    """
    Bake a Docker image with the specified dependencies.
    
    This is a composable building block that can be used standalone or
    combined with AppDeployer to deploy apps with custom images.
    
    Parameters
    ----------
    pypi : Dict[str, str], optional
        Dictionary of PyPI packages to install. Keys are package names,
        values are version specifiers. Example: {"flask": ">=2.0", "requests": ""}
        Mutually exclusive with requirements_file and pyproject_toml.
    conda : Dict[str, str], optional
        Dictionary of Conda packages to install.
    anaconda : Dict[str, Any], optional
        Dictionary of Anaconda packages to install, mutually exclusive with
        pypi, conda, requirements_file and pyproject_toml. Keys are package
        names and values are version specifiers (str)
    requirements_file : str, optional
        Path to a requirements.txt file.
        Mutually exclusive with pypi and pyproject_toml.
    pyproject_toml : str, optional
        Path to a pyproject.toml file.
        Mutually exclusive with pypi and requirements_file.
    base_image : str, optional
        Base Docker image to build from. Defaults to the platform default image.
    python : str, optional
        Python version to use (e.g., "3.11.0"). If None (default), uses the Python
        already present in the base_image and installs dependencies into it. If a
        version is specified, a new Python environment at that version is created
        inside the base image, and all dependencies are installed into it.
    logger : Callable, optional
        Logger function for progress messages.
    
    Returns
    -------
    BakedImage
        Named tuple containing:
        - image: The baked Docker image URL
        - python_path: Path to Python executable in the image
    
    Raises
    ------
    ImageBakingException
        If baking fails or if invalid parameters are provided.
    
    Examples
    --------
    Bake with PyPI packages:
    
    ```python
    result = bake_image(pypi={"flask": ">=2.0", "requests": ""})
    print(result.image)
    ```
    
    Bake from requirements.txt:
    
    ```python
    result = bake_image(requirements_file="./requirements.txt")
    ```
    
    Bake from pyproject.toml:
    
    ```python
    result = bake_image(pyproject_toml="./pyproject.toml")
    ```
    
    Combine with AppDeployer:
    
    ```python
    from metaflow.apps import bake_image, AppDeployer
    
    baked = bake_image(pypi={"flask": ">=2.0"})
    deployer = AppDeployer(name="my-app", port=8080, image=baked.image)
    deployed = deployer.deploy()
    ```
    """
    ...

def package_code(src_paths: typing.List[str], suffixes: typing.Union[typing.List[str], None] = None, logger: typing.Union[typing.Callable[[str], typing.Any], None] = None) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config.PackagedCode:
    """
    Package code for deployment to the Outerbounds Platform.
    
    This is a composable building block that can be used standalone or
    combined with AppDeployer to deploy apps with custom code packages.
    
    Parameters
    ----------
    src_paths : List[str]
        List of directories to include in the package. All paths must exist
        and be directories.
    suffixes : List[str], optional
        File extensions to include (e.g., [".py", ".json", ".yaml"]).
        If None, uses default suffixes: .py, .txt, .yaml, .yml, .json,
        .html, .css, .js, .jsx, .ts, .tsx, .md, .rst
    logger : Callable, optional
        Logger function for progress messages. Receives a single string argument.
    
    Returns
    -------
    PackagedCode
        Named tuple containing:
        - url: The package URL in object storage
        - key: Unique content-addressed key identifying this package
    
    Raises
    ------
    CodePackagingException
        If packaging fails or if invalid paths are provided.
    
    Examples
    --------
    Package a directory:
    
    ```python
    pkg = package_code(src_paths=["./src"])
    print(pkg.url)
    ```
    
    Package multiple directories:
    
    ```python
    pkg = package_code(src_paths=["./src", "./configs"])
    ```
    
    Package with specific file types:
    
    ```python
    pkg = package_code(
        src_paths=["./app"],
        suffixes=[".py", ".yaml", ".json"]
    )
    ```
    """
    ...

def load_code_package(package: metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config.PackagedCode, target_dir: str, logger: typing.Union[typing.Callable[[str], typing.Any], None] = None) -> str:
    """
    Load and extract a previously packaged code package.
    
    This is the mirror operation of package_code(). Given a PackagedCode
    (as returned by package_code()), it downloads the package from object
    storage and extracts it into the specified directory.
    
    Parameters
    ----------
    package : PackagedCode
        The package to load, as returned by package_code(). Must contain
        a valid url and key.
    target_dir : str
        The directory to extract the package into. Will be created if it
        does not exist.
    logger : Callable, optional
        Logger function for progress messages. Receives a single string argument.
    
    Returns
    -------
    str
        The absolute path to the directory where the package was extracted.
    
    Raises
    ------
    CodePackagingException
        If the package cannot be loaded or extracted.
    
    Examples
    --------
    Round-trip with package_code:
    
    ```python
    from metaflow.apps import package_code, load_code_package
    
    pkg = package_code(src_paths=["./src"])
    extracted_dir = load_code_package(pkg, target_dir="./unpacked")
    ```
    
    Load a package from a previous deployment:
    
    ```python
    from metaflow.apps import load_code_package, PackagedCode
    
    pkg = PackagedCode(url="s3://...", key="abc123")
    extracted_dir = load_code_package(pkg, target_dir="/tmp/code")
    ```
    """
    ...

class AppDeployer(metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.TypedCoreConfig, metaclass=type):
    """
    Programmatic API For deploying Outerbounds Apps.
    
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
    
    Examples
    --------
    Basic deployment with bake_image and package_code:
    
    ```python
    from metaflow.apps import bake_image, package_code, AppDeployer
    
    # Step 1: Bake dependencies into an image
    baked = bake_image(pypi={"flask": ">=2.0", "requests": ""})
    
    # Step 2: Package your application code
    pkg = package_code(src_paths=["./src"])
    
    # Step 3: Create deployer and deploy
    deployer = AppDeployer(
        name="my-flask-app",
        port=8000,
        image=baked.image,
        code_package=pkg,
        commands=["python server.py"],
        replicas={"min": 1, "max": 3},
        resources={"cpu": "1", "memory": "2048Mi"},
    )
    deployed = deployer.deploy()
    print(deployed.public_url)
    ```
    
    Deployment with API authentication:
    
    ```python
    deployer = AppDeployer(
        name="my-api",
        port=8000,
        image=baked.image,
        code_package=pkg,
        commands=["python api.py"],
        auth={"type": "API"},
    )
    deployed = deployer.deploy()
    ```
    
    Naming the app's URL instead of having one generated for it:
    
    ```python
    deployer = AppDeployer(
        name="my-api",
        port=8000,
        image=baked.image,
        code_package=pkg,
        commands=["python api.py"],
        auth={"type": "API"},
        url_slug="my-api",  # served at api-my-api.<your platform domain>
    )
    deployed = deployer.deploy()
    ```
    
    Deployment with environment variables and secrets:
    
    ```python
    deployer = AppDeployer(
        name="my-app",
        port=8000,
        image=baked.image,
        code_package=pkg,
        commands=["python app.py"],
        environment={"DEBUG": "false", "LOG_LEVEL": "info"},
        secrets=["my-api-keys"],
    )
    deployed = deployer.deploy()
    ```
    
    Fronting a workload that is already running in the cluster (a proxy app). The app
    runs no container of its own, so it takes no image, commands or code package:
    
    ```python
    # Point at a service that already exists. Its port is part of the URL.
    deployer = AppDeployer(
        name="my-proxy",
        capsule_type="Proxy",
        proxy={"service_url": "my-svc.my-ns.svc.cluster.local:8080"},
        auth={"type": "API"},
    )
    deployed = deployer.deploy()
    
    # Or point at pods, and let the platform put a service in front of them.
    deployer = AppDeployer(
        name="my-pod-proxy",
        port=8080,
        capsule_type="Proxy",
        proxy={"namespace": "jobs-default", "selector_labels": {"app": "my-app"}},
    )
    deployed = deployer.deploy()
    ```
    
    Interacting with a deployed app:
    
    ```python
    # Get app info
    info = deployed.info()
    
    # Get logs from all workers
    logs = deployed.logs()
    
    # Scale to zero workers
    deployed.scale_to_zero()
    
    # Delete the app
    deployed.delete()
    ```
    """
    def __init__(self, name: typing.Union[str, None] = None, port: typing.Union[int, None] = None, description: typing.Union[str, None] = None, app_type: typing.Union[str, None] = None, image: typing.Union[str, None] = None, tags: typing.Union[list, None] = None, secrets: typing.Union[list, None] = None, compute_pools: typing.Union[list, None] = None, environment: typing.Union[dict, None] = None, commands: typing.Union[list, None] = None, resources: typing.Union[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.ResourceConfigDict, None] = None, auth: typing.Union[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.AuthConfigDict, None] = None, replicas: typing.Union[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.ReplicaConfigDict, None] = None, code_package: typing.Union[tuple, None] = None, force_upgrade: typing.Union[bool, None] = None, use_base_image_command: typing.Union[bool, None] = None, skip_code_package: typing.Union[bool, None] = None, capsule_type: typing.Union[str, None] = None, proxy: typing.Union[metaflow.mf_extensions.outerbounds.plugins.apps.core.config.typed_configs.ProxyConfigDict, None] = None, url_slug: typing.Union[str, None] = None, persistence: typing.Union[str, None] = None, project: typing.Union[str, None] = None, branch: typing.Union[str, None] = None, models: typing.Union[list, None] = None, data: typing.Union[list, None] = None, generate_static_url: typing.Union[bool, None] = None, **kwargs):
        ...
    @property
    def _deploy_config(self) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config.AppConfig:
        ...
    def deploy(self, readiness_condition: str = 'at_least_one_running', max_wait_time = 600, readiness_wait_time = 60, logger_fn = ..., **kwargs) -> DeployedApp:
        """
        Deploy the app to the Outerbounds Platform.
        
        This method packages and deploys the configured app, waiting for it to reach
        the specified readiness condition before returning.
        
        Parameters
        ----------
        readiness_condition : str, optional
            The condition that must be met for the deployment to be considered ready.
            Default is ATLEAST_ONE_RUNNING.
        
            Deployment ready conditions define what is considered a successful completion
            of the current deployment instance. This allows users or platform designers
            to configure the criteria for deployment readiness.
        
            Why do we need deployment readiness conditions?
                - Deployments might be taking place from a CI/CD-esque environment.
                  In these setups, the downstream build triggers might be depending on
                  a specific criteria for deployment completion. Having readiness conditions
                  allows the CI/CD systems to get a signal of when the deployment is ready.
                - Users might be calling the deployment API under different conditions:
                    - Some users might want a cluster of workers ready before serving
                      traffic while others might want just one worker ready to start
                      serving traffic.
        
            Available readiness conditions:
        
            ATLEAST_ONE_RUNNING ("at_least_one_running")
                At least min(min_replicas, 1) workers of the current deployment
                instance's version have started running.
                Usecase: Some endpoints may be deployed ephemerally and are considered
                ready when at least one instance is running; additional instances are
                for load management.
        
            ALL_RUNNING ("all_running")
                At least min_replicas number of workers are running for the deployment
                to be considered ready.
                Usecase: Operators may require that all replicas are available before
                traffic is routed. Needed when inference endpoints may be under some
                SLA or require a larger load.
        
            FULLY_FINISHED ("fully_finished")
                At least min_replicas number of workers are running for the deployment
                and there are no pending or crashlooping workers from previous versions
                lying around.
                Usecase: Ensuring endpoint is fully available and no other versions are
                running or endpoint has been fully scaled down.
        
            ASYNC ("async")
                The deployment will be assumed ready as soon as the server acknowledges
                it has registered the app in the backend.
                Usecase: Operators may only care that the URL is minted for the deployment
                or the operator wants the deployment to eventually scale down to 0.
        
        max_wait_time : int, optional
            Maximum time in seconds to wait for the deployment to reach readiness.
            Default is 600 (10 minutes).
        
        readiness_wait_time : int, optional
            Once the deployment meets the readiness_condition, workers are monitored
            for an additional readiness_wait_time seconds to catch crashloops that
            surface shortly after startup. If a worker enters a crashloop during this
            window the deploy will fail with AppCrashLoopException. Increase this
            value for apps with slow startups or when infrastructure may not be
            quickly available for apps.
            Default is 60.
        
        logger_fn : Callable, optional
            Function to use for logging progress messages. Default prints to stderr.
        
        Returns
        -------
        DeployedApp
            An object representing the deployed app with methods to interact with it
            (logs, info, scale_to_zero, delete, etc.) and properties like public_url.
        
        Raises
        ------
        CodePackagingException
            If code_package is not provided or is not a valid PackagedCode instance.
        
        AppConfigError
            If the app configuration is invalid.
        
        AppCreationFailedException
            If the app deployment submission fails due to an API error.
            Contains status_code and error_text attributes for debugging.
        
        AppCrashLoopException
            If a worker enters CrashLoopBackOff or Failed state during deployment.
            Contains worker_id and logs attributes for debugging.
        
        AppReadinessException
            If the app fails to meet readiness conditions within max_wait_time.
        
        AppUpgradeInProgressException
            If an upgrade is already in progress when deployment starts.
            Use force_upgrade=True to override. Contains upgrader attribute.
        
        AppConcurrentUpgradeException
            If another deployment was triggered while this deployment was in progress,
            invalidating the current deployment. Contains expected_version and actual_version.
        
        OuterboundsBackendUnhealthyException
            If the Outerbounds backend is unreachable (network issues, DNS failures) or
            returns server errors (HTTP 5xx). This indicates a platform-side issue, not a
            problem with your configuration. Retry the deployment or contact Outerbounds support.
        
        AppDeletedDuringDeploymentException
            If the app was deleted by another process or user while this deployment was
            in progress. This can occur when concurrent operations conflict.
        
        Examples
        --------
        Basic deployment:
        
        ```python
        from metaflow.apps import bake_image, package_code, AppDeployer
        baked = bake_image(pypi={"flask": ">=2.0"})
        pkg = package_code(src_paths=["./src"])
        deployer = AppDeployer(
            name="my-app",
            port=8000,
            image=baked.image,
            code_package=pkg,
            commands=["python server.py"],
        )
        deployed = deployer.deploy()
        print(deployed.public_url)
        ```
        
        Wait for all replicas to be ready:
        
        ```python
        deployed = deployer.deploy(
            readiness_condition="all_running"
        )
        ```
        
        Async deployment (don't wait for workers):
        
        ```python
        deployed = deployer.deploy(
            readiness_condition="async"
        )
        ```
        
        Handling deployment errors:
        
        ```python
        from metaflow.apps import AppDeployer
        from metaflow.apps.exceptions import (
            AppReadinessException,
        )
        
        try:
            deployed = deployer.deploy()
        except AppReadinessException as e:
            print(f"App {e.app_id} failed to become ready in time but we can move forward")
            deployed_app:DeployedApp = e.deployed_app
            # use DeployedApp to do what ever you need
        ```
        """
        ...
    @classmethod
    def list_deployments(cls, name: str = None, project: str = None, branch: str = None, tags: typing.List[typing.Dict[str, str]] = None) -> typing.List["DeployedApp"]:
        """
        List deployed apps, optionally filtered by name, project, branch, or tags.
        
        Parameters
        ----------
        name : str, optional
            Filter by app name.
        project : str, optional
            Filter by project name.
        branch : str, optional
            Filter by branch name.
        tags : List[Dict[str, str]], optional
            Filter by tags. Each tag is a dict with a single key-value pair,
            e.g., [{"env": "prod"}] or [{"team": "ml"}, {"version": "v2"}].
            Apps must have all specified tags to match.
        
        Returns
        -------
        List[DeployedApp]
            List of deployed apps matching the filters.
        
        Examples
        --------
        List all apps:
        
        ```python
        apps = AppDeployer.list_deployments()
        ```
        
        Filter by name:
        
        ```python
        apps = AppDeployer.list_deployments(name="my-app")
        ```
        
        Filter by project and branch:
        
        ```python
        apps = AppDeployer.list_deployments(project="ml-pipeline", branch="main")
        ```
        
        Filter by a single tag:
        
        ```python
        apps = AppDeployer.list_deployments(tags=[{"env": "prod"}])
        ```
        
        Filter by multiple tags (AND logic - must match all):
        
        ```python
        apps = AppDeployer.list_deployments(tags=[{"env": "prod"}, {"team": "ml"}])
        ```
        
        Combine filters:
        
        ```python
        apps = AppDeployer.list_deployments(
            project="recommendations",
            tags=[{"env": "staging"}]
        )
        ```
        """
        ...
    ...

class TTLCachedObject(object, metaclass=type):
    """
    Caches a value with a time-to-live (TTL) per instance.
    Returns None if accessed after TTL has expired.
    """
    def __init__(self, ttl_seconds: float):
        ...
    def __set_name__(self, owner, name):
        ...
    def __get__(self, instance, owner):
        ...
    def __set__(self, instance, val):
        ...
    def __delete__(self, instance):
        ...
    ...

class DeployedApp(object, metaclass=type):
    """
    A deployed app on the Outerbounds Platform.
    
    Obtain instances via `AppDeployer.deploy()` or `AppDeployer.list_deployments()`.
    
    Examples
    --------
    After deployment:
    
    ```python
    deployed = deployer.deploy()
    print(deployed.public_url)
    ```
    
    After listing:
    
    ```python
    apps = AppDeployer.list_deployments(tags=[{"env": "staging"}])
    for app in apps:
        print(f"{app.name}: {app.public_url}")
    ```
    
    Inspect and manage:
    
    ```python
    # Get logs
    for worker_id, lines in deployed.logs().items():
        print(f"Worker {worker_id}: {len(lines)} log lines")
    
    # Scale down
    deployed.scale_to_zero()
    
    # Clean up
    deployed.delete()
    ```
    
    Make authenticated requests (API auth):
    
    ```python
    import requests
    response = requests.get(deployed.public_url, headers=deployed.auth())
    ```
    """
    def __init__(self, _id: str, capsule_type: str, public_url: str, name: str, deployed_version: str, deployed_at: str):
        ...
    @property
    def _capsule_info(self):
        ...
    def logs(self, previous: bool = False) -> typing.Dict[str, typing.List[metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.LogLine]]:
        """
        Get logs from all worker replicas.
        
        Parameters
        ----------
        previous : bool, optional
            If True, returns logs from the previous execution of workers.
            Useful for debugging crashlooping workers. Default is False.
        
        Returns
        -------
        Dict[str, List[LogLine]]
            Dictionary mapping worker IDs to their log lines.
        
        Examples
        --------
        ```python
        # Get current logs
        logs = deployed.logs()
        for worker_id, lines in logs.items():
            print(f"Worker {worker_id}:")
            for line in lines:
                print(f"  {line}")
        
        # Get logs from crashed workers
        previous_logs = deployed.logs(previous=True)
        ```
        """
        ...
    def info(self) -> dict:
        """
        Get detailed information about the deployed app.
        
        Returns
        -------
        dict
            Dictionary containing full app details including spec, status,
            metadata, and configuration.
        
        Examples
        --------
        ```python
        info = deployed.info()
        print(f"Status: {info.get('status')}")
        print(f"Spec: {info.get('spec')}")
        ```
        """
        ...
    def replicas(self) -> typing.List[dict]:
        """
        List all active worker replicas for this app.
        
        Returns
        -------
        List[dict]
            List of dictionaries containing worker information including
            workerId, status, and other metadata.
        
        Examples
        --------
        ```python
        workers = deployed.replicas()
        for worker in workers:
            print(f"Worker {worker['workerId']}: {worker.get('status')}")
        ```
        """
        ...
    def scale_to_zero(self):
        """
        Scale the app down to zero replicas.
        
        This stops all running workers while preserving the app configuration.
        The app can be scaled back up by sending traffic to the public URL
        (if autoscaling is configured) or by redeploying.
        
        Examples
        --------
        ```python
        # Scale down to save resources
        deployed.scale_to_zero()
        ```
        """
        ...
    def delete(self):
        """
        Delete the deployed app.
        
        This permanently removes the app from the platform, including all
        workers, configuration, and the public URL. This action cannot be undone.
        
        Examples
        --------
        ```python
        # Clean up the app
        deployed.delete()
        ```
        """
        ...
    def auth(self) -> dict:
        """
        Get authentication headers for making requests to this app.
        
        Only available for apps configured with API authentication type.
        Use these headers when making HTTP requests to the app's public URL.
        
        Returns
        -------
        dict
            Dictionary of HTTP headers to include in requests.
        
        Raises
        ------
        ValueError
            If the app is not configured with API authentication.
        
        Examples
        --------
        ```python
        import requests
        response = requests.get(deployed.public_url, headers=deployed.auth())
        ```
        """
        ...
    @property
    def id(self) -> str:
        """
        Unique identifier for the deployed app.
        
        Returns
        -------
        str
            The unique app identifier assigned by the platform.
        """
        ...
    @property
    def auth_type(self) -> str:
        """
        Authentication type configured for this app. Can be either `Browser` , `API`, `BrowserAndApi`
        
        Returns
        -------
        str
            The authentication type
        """
        ...
    @property
    def public_url(self) -> str:
        """
        Public URL to access the deployed app.
        
        Returns
        -------
        str
            The publicly accessible URL for this app.
        """
        ...
    @property
    def internal_url(self) -> str:
        """
        Internal in-cluster URL to access the deployed app.
        
        This URL bypasses external network routing and can be used from within
        Metaflow tasks running on Kubernetes. Authentication headers are not
        required when accessing the app via this URL from within the cluster.
        
        Returns
        -------
        str
            The in-cluster URL for this app.
        """
        ...
    @property
    def name(self) -> str:
        """
        Logical name given to the app.
        
        Returns
        -------
        str
            The human-readable name of the app.
        """
        ...
    @property
    def deployed_version(self) -> str:
        """
        Current deployment version of the app.
        
        Returns
        -------
        str
            The version identifier for the current deployment.
        """
        ...
    @property
    def deployed_at(self) -> datetime.datetime:
        """
        Timestamp when the app was last deployed.
        
        Returns
        -------
        datetime
            The datetime of the last deployment.
        """
        ...
    @property
    def tags(self) -> typing.List[str]:
        """
        Tags associated with this app.
        
        Returns
        -------
        List[str]
            List of tags assigned to this app.
        """
        ...
    def __repr__(self) -> str:
        ...
    ...

