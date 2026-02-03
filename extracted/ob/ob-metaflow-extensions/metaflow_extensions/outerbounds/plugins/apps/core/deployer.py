from .config import TypedCoreConfig, TypedDict
from .perimeters import PerimeterExtractor
from .capsule import CapsuleApi
import time
import os
import tempfile
from ._state_machine import DEPLOYMENT_READY_CONDITIONS, LogLine
from .app_config import AppConfig, AppConfigError
from .code_package import CodePackager
from .config import PackagedCode, BakedImage
from .app_config import CODE_PACKAGE_PREFIX, AuthType
from .capsule import (
    CapsuleDeployer,
    list_and_filter_capsules,
    _format_url_string,
)
from .exceptions import (
    CapsuleDeploymentException,
    CapsuleApiException,
    CapsuleCrashLoopException,
    CapsuleReadinessException,
    CapsuleConcurrentUpgradeException,
    CapsuleDeletedDuringDeploymentException,
    AppConcurrentUpgradeException,
    AppCrashLoopException,
    AppCreationFailedException,
    AppDeletedDuringDeploymentException,
    AppDeploymentException,
    AppNotFoundException,
    AppReadinessException,
    AppUpgradeInProgressException,
    CodePackagingException,
)
from .dependencies import ImageBakingException
from functools import partial
import sys
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime


def _resolve_fast_bakery_url():
    config = PerimeterExtractor.config_during_programmatic_access()
    fast_bakery_url = config.get("METAFLOW_FAST_BAKERY_URL")
    default_container_image = config.get("METAFLOW_KUBERNETES_CONTAINER_IMAGE")
    if fast_bakery_url is None:
        raise ImageBakingException(
            "METAFLOW_FAST_BAKERY_URL is not set. Please set the METAFLOW_FAST_BAKERY_URL environment variable or add it to your metaflow config. Please contact outerbounds support for assistance."
        )
    return fast_bakery_url, default_container_image


def bake_image(
    pypi: Optional[Dict[str, str]] = None,
    conda: Optional[Dict[str, str]] = None,
    requirements_file: Optional[str] = None,
    pyproject_toml: Optional[str] = None,
    base_image: Optional[str] = None,
    python: Optional[str] = None,
    logger: Optional[Callable[[str], Any]] = None,
    cache_name: Optional[str] = None,
) -> BakedImage:
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
    from metaflow.ob_internal import internal_bake_image as _internal_bake  # type: ignore
    from metaflow.plugins.pypi.parsers import (
        requirements_txt_parser,
        pyproject_toml_parser,
    )

    from metaflow.metaflow_config import (
        DEFAULT_DATASTORE,
        get_pinned_conda_libs,
    )

    # Count how many dependency sources are provided
    dep_sources = sum(
        [
            pypi is not None,
            conda is not None,
            requirements_file is not None,
            pyproject_toml is not None,
        ]
    )

    fast_bakery_url, default_base_image = _resolve_fast_bakery_url()

    if dep_sources > 1:
        raise ImageBakingException(
            "Only one of pypi, conda, requirements_file, or pyproject_toml can be specified."
        )

    # Set defaults
    _base_image = base_image or default_base_image
    _python_version = python  # Keep it None to use image python
    _logger = logger or (lambda x: None)
    _cache_name = cache_name or "default"

    # Set up cache directory (internal - not exposed to users)
    cache_dir = os.path.join(tempfile.gettempdir(), f"ob-bake-{_cache_name}")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file_path = os.path.join(cache_dir, "image_cache")

    # Collect packages
    pypi_packages: Dict[str, str] = {}
    conda_packages: Dict[str, str] = {}

    # Parse from file if provided
    if requirements_file:
        if not os.path.exists(requirements_file):
            raise ImageBakingException(
                f"Requirements file not found: {requirements_file}"
            )
        with open(requirements_file, "r") as f:
            parsed = requirements_txt_parser(f.read())
        pypi_packages = parsed.get("packages", {})
        _python_version = parsed.get("python_version", _python_version)
        _logger(f"📦 Parsed {len(pypi_packages)} packages from {requirements_file}")

    elif pyproject_toml:
        if not os.path.exists(pyproject_toml):
            raise ImageBakingException(f"pyproject.toml not found: {pyproject_toml}")
        with open(pyproject_toml, "r") as f:
            parsed = pyproject_toml_parser(f.read())
        pypi_packages = parsed.get("packages", {})
        _python_version = parsed.get("python_version", _python_version)
        _logger(f"📦 Parsed {len(pypi_packages)} packages from {pyproject_toml}")

    elif pypi:
        pypi_packages = pypi.copy()

    elif conda:
        conda_packages = conda.copy()

    # Check if there are any packages to bake
    if not pypi_packages and not conda_packages:
        _logger("⚠️ No packages to bake. Returning base image.")
        return BakedImage(image=_base_image, python_path="python")

    # Add pinned conda libs required by the platform
    pinned_libs = get_pinned_conda_libs(_python_version, DEFAULT_DATASTORE)
    if len(conda_packages) > 0:
        conda_packages.update(pinned_libs)
    else:
        pypi_packages.update(pinned_libs)

    _logger(f"🍞 Baking image with {len(pypi_packages)} PyPI packages...")

    # Call the internal bake function
    fb_response = _internal_bake(
        cache_file_path=cache_file_path,
        pypi_packages=pypi_packages,
        conda_packages=conda_packages,
        ref=_cache_name,
        python=_python_version,
        base_image=_base_image,
        logger=_logger,
        fast_bakery_url=fast_bakery_url,
    )

    if fb_response.failure:
        raise ImageBakingException(f"Failed to bake image: {fb_response.response}")

    _logger(f"🐳 Baked image: {fb_response.container_image}")

    return BakedImage(
        image=fb_response.container_image,
        python_path=fb_response.python_path,
    )


def package_code(
    src_paths: List[str],
    suffixes: Optional[List[str]] = None,
    logger: Optional[Callable[[str], Any]] = None,
) -> PackagedCode:
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
    from metaflow.metaflow_config import DEFAULT_DATASTORE

    _logger = logger or (lambda x: None)

    # Validate paths
    for path in src_paths:
        if not os.path.exists(path):
            raise CodePackagingException(f"Source path does not exist: {path}")
        if not os.path.isdir(path):
            raise CodePackagingException(f"Source path is not a directory: {path}")

    _logger(f"📦 Packaging {len(src_paths)} directory(ies)...")

    # Create packager and store
    packager = CodePackager(
        datastore_type=DEFAULT_DATASTORE,
        code_package_prefix=CODE_PACKAGE_PREFIX,
    )

    try:
        package_url, package_key = packager.store(
            paths_to_include=src_paths,
            file_suffixes=suffixes,  # None uses defaults in CodePackager
        )
    except Exception as e:
        raise CodePackagingException(f"Failed to package code: {e}") from e

    _logger(f"📦 Code package stored: {package_url}")

    return PackagedCode(url=package_url, key=package_key)


class AppDeployer(TypedCoreConfig):

    __examples__ = """
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

    __doc__ = (
        """Programmatic API For deploying Outerbounds Apps.\n"""
        + TypedCoreConfig.__doc__
        + __examples__
    )

    __init__ = TypedCoreConfig.__init__

    _app_config: AppConfig

    # What is `_state` ?
    # `_state` is a dictionary that will hold all information that might need
    # to be passed down without the user explicity setting them.
    # Setting `_state` will ensure that values are explicity passed down from
    # top level when the class is used under different context.
    # So for example if we need to set some things like project/branches etc
    # during metaflow context, we can do so easily. We also like to set state like
    # perimeters at class level since users current cannot also switch perimeters within
    # the same interpreter.
    _state = {}

    __state_items = [
        # perimeter and api_url come from config setups
        # need to happen before AppDeployer and need to
        # come from _set_state
        "perimeter",
        "api_url",
        # code package URL / code package key
        # can come from CodePackager so its fine
        # if its in _set_state
        "code_package_url",
        "code_package_key",
        # Image can be explicitly set by the user
        # or requre some external fast-bakery API
        "image",
        # project/branch have to come from _set_state
        # if users do this through current. Otherwise
        # can come from the
        "project",
        "branch",
    ]

    def _init(self):
        perimeter, api_url = PerimeterExtractor.during_programmatic_access()
        self._set_state("perimeter", perimeter)
        self._set_state("api_url", api_url)

    @property
    def _deploy_config(self) -> AppConfig:
        if not hasattr(self, "_app_config"):
            self._app_config = AppConfig(self._config)
        return self._app_config

    # Things that need to be set before deploy
    @classmethod
    def _set_state(cls, key, value):
        cls._state[key] = value

    def deploy(
        self,
        readiness_condition: str = DEPLOYMENT_READY_CONDITIONS.ATLEAST_ONE_RUNNING,
        max_wait_time=600,
        readiness_wait_time=10,
        logger_fn=partial(print, file=sys.stderr),
        **kwargs,
    ) -> "DeployedApp":
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
            Time in seconds to wait between readiness checks. Default is 10.

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
        if len(self._state.get("default_tags", [])) > 0:
            self._deploy_config._core_config.tags = (
                self._deploy_config._core_config.tags or []
            ) + self._state["default_tags"]

        # Handle code_package if provided - extract url and key to state
        code_package = getattr(self._deploy_config._core_config, "code_package", None)
        if code_package is not None:
            # Validate that code_package is a PackagedCode namedtuple
            if not isinstance(code_package, PackagedCode):
                raise CodePackagingException(
                    f"code_package must be a PackagedCode instance returned by package_code(). "
                    f"Got {type(code_package).__name__} instead.\n\n"
                    "Use package_code() to create a valid code package:\n\n"
                    "    from metaflow.apps import package_code, AppDeployer\n\n"
                    "    pkg = package_code(src_paths=['./src'])\n"
                    "    deployer = AppDeployer(..., code_package=pkg)\n"
                )
            self._set_state("code_package_url", code_package.url)
            self._set_state("code_package_key", code_package.key)
            # Clear the code_package field to avoid serialization issues
            self._deploy_config._core_config.code_package = None

        # Verify code_package is present (either from code_package param or from state)
        if (
            self._state.get("code_package_url") is None
            and self._deploy_config.get_state("code_package_url") is None
        ):
            raise CodePackagingException(
                "code_package is required for deployment. "
                "Use package_code() to create a code package:\n\n"
                "    from metaflow.apps import package_code, AppDeployer\n\n"
                "    pkg = package_code(src_paths=['./src'])\n"
                "    deployer = AppDeployer(..., code_package=pkg)\n"
            )

        self._deploy_config.commit()
        # Set any state that might have been passed down from the top level
        for k in self.__state_items:
            if self._deploy_config.get_state(k) is None and (
                k in self._state and self._state[k] is not None
            ):
                self._deploy_config.set_state(k, self._state[k])

        capsule = CapsuleDeployer(
            self._deploy_config,
            self._state["api_url"],
            create_timeout=max_wait_time,
            debug_dir=None,
            success_terminal_state_condition=readiness_condition,
            readiness_wait_time=readiness_wait_time,
            logger_fn=logger_fn,
        )

        currently_present_capsules = list_and_filter_capsules(
            capsule.capsule_api,
            None,
            None,
            capsule.name,
            None,
            None,
            None,
        )

        force_upgrade = self._deploy_config.get_state("force_upgrade", False)

        if len(currently_present_capsules) > 0:
            # Only update the capsule if there is no upgrade in progress
            # Only update a "already updating" capsule if the `--force-upgrade` flag is provided.
            _curr_cap = currently_present_capsules[0]
            this_capsule_is_being_updated = _curr_cap.get("status", {}).get(
                "updateInProgress", False
            )

            if this_capsule_is_being_updated and not force_upgrade:
                _upgrader = _curr_cap.get("metadata", {}).get("lastModifiedBy", None)
                raise AppUpgradeInProgressException(
                    app_id=_curr_cap.get("id"),
                    upgrader=_upgrader,
                )

            logger_fn(
                f"🚀 {'' if not force_upgrade else 'Force'} Upgrading {capsule.capsule_type.lower()} `{capsule.name}`....",
            )
        else:
            logger_fn(
                f"🚀 Deploying {capsule.capsule_type.lower()} `{capsule.name}`....",
            )

        try:
            capsule.create()
        except CapsuleApiException as e:
            raise AppCreationFailedException(
                app_name=capsule.name,
                status_code=e.status_code,
                error_text=e.text,
            ) from e
        try:
            final_status = capsule.wait_for_terminal_state()
        except CapsuleCrashLoopException as e:
            raise AppCrashLoopException(
                app_id=e.capsule_id,
                worker_id=e.worker_id,
                logs=e.logs,
            ) from e
        except CapsuleReadinessException as e:
            raise AppReadinessException(
                app_id=e.capsule_id,
            ) from e
        except CapsuleConcurrentUpgradeException as e:
            raise AppConcurrentUpgradeException(
                app_id=e.capsule_id,
                expected_version=e.expected_version,
                actual_version=e.actual_version,
                modified_by=e.modified_by,
                modified_at=e.modified_at,
            ) from e
        except CapsuleDeletedDuringDeploymentException as e:
            raise AppDeletedDuringDeploymentException(
                app_id=e.capsule_id,
            ) from e

        return DeployedApp(
            final_status["id"],
            final_status["auth_type"],
            _format_url_string(final_status["public_url"], True),
            final_status["name"],
            final_status["deployed_version"],
            final_status["deployed_at"],
        )

    @classmethod
    def list_deployments(
        cls,
        name: str = None,
        project: str = None,
        branch: str = None,
        tags: List[Dict[str, str]] = None,
    ) -> List["DeployedApp"]:
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
        # Transform tags from {key: value} to {"key": key, "value": value}
        transformed_tags = None
        if tags:
            transformed_tags = [
                {"key": k, "value": v} for tag in tags for k, v in tag.items()
            ]

        capsule_api = DeployedApp._get_capsule_api()
        list_of_capsules = list_and_filter_capsules(
            capsule_api,
            project=project,
            branch=branch,
            name=name,
            tags=transformed_tags,
            auth_type=None,
            capsule_id=None,
        )
        apps = []
        for cap in list_of_capsules:
            apps.append(DeployedApp._from_capsule(cap))
        return apps


class TTLCachedObject:
    """
    Caches a value with a time-to-live (TTL) per instance.
    Returns None if accessed after TTL has expired.
    """

    def __init__(self, ttl_seconds: float):
        self._ttl = ttl_seconds
        self._attr_name = None

    def __set_name__(self, owner, name):
        self._attr_name = f"_ttl_cache_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        cache = getattr(instance, self._attr_name, None)
        if cache is None:
            return None
        value, last_set = cache
        if (time.time() - last_set) > self._ttl:
            return None
        return value

    def __set__(self, instance, val):
        setattr(instance, self._attr_name, (val, time.time()))

    def __delete__(self, instance):
        if hasattr(instance, self._attr_name):
            delattr(instance, self._attr_name)


class DeployedApp:
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

    # Keep a 3ish second TTL so that we can be gentler
    # the backend API.
    _capsule_info_cached = TTLCachedObject(3)

    def __init__(
        self,
        _id: str,
        capsule_type: str,
        public_url: str,
        name: str,
        deployed_version: str,
        deployed_at: str,
    ):
        self._id = _id  # This ID is the capsule's ID
        self._capsule_type = capsule_type
        self._public_url = public_url
        self._name = name
        self._deployed_version = deployed_version
        self._deployed_at = deployed_at

    @classmethod
    def _get_capsule_api(cls) -> CapsuleApi:
        perimeter, api_server = PerimeterExtractor.during_programmatic_access()
        # In this setting capsules maybe getting managed/deployed in a remote
        # programmatic setting where the user might have no "hands-on" control
        # In those situations its better to retry to 5xx errors
        return CapsuleApi(api_server, perimeter, retry_500s=True)

    @property
    def _capsule_info(self):
        # self._capsule_info_cached will be None every 3ish seconds
        if self._capsule_info_cached is not None:
            return self._capsule_info_cached
        self._capsule_info_cached = self.info()
        return self._capsule_info_cached

    @classmethod
    def _from_capsule(cls, capsule: dict) -> "DeployedApp":
        capsule_id = capsule.get("id")
        capsule_type = (
            capsule.get("spec", {}).get("authConfig", {}).get("authType", None)
        )
        status = capsule.get("status", {})
        public_url = None
        if status is None:
            status = {}
        if status.get("accessInfo", {}):
            public_url = status.get("accessInfo", {}).get("outOfClusterURL", None)
        name = capsule.get("spec", {}).get(
            "displayName",
        )
        deployed_version = capsule.get(
            "version",
        )
        deployed_at = capsule.get("metadata", {}).get(
            "lastModifiedAt",
            capsule.get("metadata", {}).get(
                "createdAt",
            ),
        )
        if any(i is None for i in [capsule_type, name]):
            raise ValueError(f"Invalid capsule id: {capsule_id}")
        cpsule = cls(
            capsule_id,
            capsule_type,
            public_url if public_url is None else _format_url_string(public_url, True),
            name,
            deployed_version,
            deployed_at,
        )

        cpsule._capsule_info_cached = capsule
        return cpsule

    @classmethod
    def _from_capsule_id(cls, capsule_id: str) -> "DeployedApp":
        try:
            capsule_api = cls._get_capsule_api()
            capsule = capsule_api.get(capsule_id)
        except CapsuleApiException as e:
            if e.status_code == 404:
                raise AppNotFoundException("App with id '%s' could not be found") from e
            raise

        return cls._from_capsule(capsule)

    def logs(self, previous: bool = False) -> Dict[str, List[LogLine]]:
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
        capsule_api = self._get_capsule_api()
        # extract workers from capsule
        workers = capsule_api.get_workers(self._id)
        # get logs from workers
        logs = {
            # worker_id: logs
        }
        for worker in workers:
            # TODO: Handle exceptions better over here.
            logs[worker["workerId"]] = capsule_api.logs(
                self._id, worker["workerId"], previous=previous
            )
        return logs

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
        capsule_api = self._get_capsule_api()
        capsule = capsule_api.get(self._id)
        return capsule

    def replicas(self) -> List[dict]:
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
        capsule_api = self._get_capsule_api()
        return capsule_api.get_workers(self._id)

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
        capsule_api = self._get_capsule_api()
        return capsule_api.patch(
            self._id,
            {
                "autoscalingConfig": {
                    "minReplicas": 0,
                    "maxReplicas": 0,
                }
            },
        )

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
        capsule_api = self._get_capsule_api()
        return capsule_api.delete(self._id)

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
        if self.auth_type == AuthType.BROWSER:
            raise ValueError(
                "Only API auth style is supported for accessing auth headers"
            )
        from metaflow.metaflow_config import SERVICE_HEADERS

        return SERVICE_HEADERS

    @property
    def id(self) -> str:
        """
        Unique identifier for the deployed app.

        Returns
        -------
        str
            The unique app identifier assigned by the platform.
        """
        return self._id

    @property
    def auth_type(self) -> str:
        """
        Authentication type configured for this app. Can be either `Browser` , `API`, `BrowserAndApi`

        Returns
        -------
        str
            The authentication type
        """
        return self._capsule_type

    @property
    def public_url(self) -> str:
        """
        Public URL to access the deployed app.

        Returns
        -------
        str
            The publicly accessible URL for this app.
        """
        if self._public_url is None:
            info = self._capsule_info
            status = info.get("status", {})
            if status is None:
                status = {}
            access_info = status.get("accessInfo", {}) or {}
            self._public_url = access_info.get("outOfClusterURL", None)
            if self._public_url is not None:
                self._public_url = _format_url_string(self._public_url, True)
        return self._public_url

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

        info = self._capsule_info
        status = info.get("status", {})
        if status is None:
            status = {}
        access_info = status.get("accessInfo", {}) or {}
        internal_url = access_info.get("inClusterURL", None)
        if internal_url is not None:
            internal_url = _format_url_string(internal_url, False)
        return internal_url

    @property
    def name(self) -> str:
        """
        Logical name given to the app.

        Returns
        -------
        str
            The human-readable name of the app.
        """
        return self._name

    @property
    def deployed_version(self) -> str:
        """
        Current deployment version of the app.

        Returns
        -------
        str
            The version identifier for the current deployment.
        """
        return self._deployed_version

    @property
    def deployed_at(self) -> datetime:
        """
        Timestamp when the app was last deployed.

        Returns
        -------
        datetime
            The datetime of the last deployment.
        """
        return datetime.fromisoformat(self._deployed_at)

    @property
    def tags(self) -> List[str]:
        """
        Tags associated with this app.

        Returns
        -------
        List[str]
            List of tags assigned to this app.
        """
        capsule_info = self._capsule_info
        return capsule_info.get("spec", {}).get("tags", [])

    def __repr__(self) -> str:
        return (
            f"DeployedApp(id='{self._id}', "
            f"name='{self._name}', "
            f"public_url='{self._public_url}', "
            f"deployed_version='{self._deployed_version}')"
        )
