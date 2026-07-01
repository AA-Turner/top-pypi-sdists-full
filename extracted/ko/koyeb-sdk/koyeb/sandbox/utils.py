# coding: utf-8

"""
Utility functions for Koyeb Sandbox
"""

import logging
import os
import shlex
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from koyeb.api import ApiClient, Configuration
from koyeb.api.api import (
    AppsApi,
    CatalogInstancesApi,
    DeploymentsApi,
    InstancesApi,
    SecretsApi,
    ServicesApi,
)
from koyeb.api.models.config_file import ConfigFile
from koyeb.api.models.deployment_definition import DeploymentDefinition
from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_env import DeploymentEnv
from koyeb.api.models.secret import Secret
from koyeb.api.models.deployment_instance_type import DeploymentInstanceType
from koyeb.api.models.deployment_port import DeploymentPort
from koyeb.api.models.deployment_proxy_port import DeploymentProxyPort
from koyeb.api.models.deployment_route import DeploymentRoute
from koyeb.api.models.deployment_scaling import DeploymentScaling
from koyeb.api.models.deployment_scaling_target import DeploymentScalingTarget
from koyeb.api.models.deployment_scaling_target_sleep_idle_delay import (
    DeploymentScalingTargetSleepIdleDelay,
)
from koyeb.api.models.deployment_mesh import DeploymentMesh
from koyeb.api.models.docker_source import DockerSource
from koyeb.api.models.proxy_port_protocol import ProxyPortProtocol

# Setup logging
logger = logging.getLogger(__name__)

# Constants
MIN_PORT = 1
MAX_PORT = 65535
DEFAULT_INSTANCE_WAIT_TIMEOUT = 60  # seconds
DEFAULT_POLL_INTERVAL = 0.5  # seconds
DEFAULT_COMMAND_TIMEOUT = 30  # seconds
DEFAULT_HTTP_TIMEOUT = 30  # seconds for HTTP requests

# Error messages
ERROR_MESSAGES = {
    "NO_SUCH_FILE": ["No such file", "not found", "No such file or directory"],
    "FILE_EXISTS": ["exists", "already exists"],
    "DIR_NOT_EMPTY": ["not empty", "Directory not empty"],
}

# Valid protocols for DeploymentPort (from OpenAPI spec: http, http2, tcp)
# For sandboxes, we only support http and http2
VALID_DEPLOYMENT_PORT_PROTOCOLS = ("http", "http2")


def _validate_port_protocol(protocol: str) -> str:
    """
    Validate port protocol using API model structure.

    Args:
        protocol: Protocol string to validate

    Returns:
        Validated protocol string

    Raises:
        ValueError: If protocol is invalid
    """
    # Validate by attempting to create a DeploymentPort instance
    # This ensures we're using the API model's validation structure
    try:
        port = DeploymentPort(port=3030, protocol=protocol)
        # Additional validation: check if protocol is in allowed values
        if protocol not in VALID_DEPLOYMENT_PORT_PROTOCOLS:
            raise ValueError(
                f"Invalid protocol '{protocol}'. Must be one of {VALID_DEPLOYMENT_PORT_PROTOCOLS}"
            )
        return port.protocol or "http"
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(
            f"Invalid protocol '{protocol}'. Must be one of {VALID_DEPLOYMENT_PORT_PROTOCOLS}"
        ) from e


@dataclass(frozen=True)
class ApiClients:
    """Bundle of Koyeb API clients sharing a single underlying ApiClient."""

    apps: AppsApi
    services: ServicesApi
    instances: InstancesApi
    catalog_instances: CatalogInstancesApi
    deployments: DeploymentsApi
    secrets: SecretsApi


_api_clients_cache: Dict[Tuple[str, str], ApiClients] = {}


def get_api_clients(
    api_token: Optional[str] = None, host: Optional[str] = None
) -> ApiClients:
    """
    Get configured API clients for Koyeb operations.

    Caches clients by (token, host) to reuse the underlying HTTP connection pool.

    Args:
        api_token: Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
        host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

    Returns:
        ApiClients with apps, services, instances, catalog_instances, deployments, and secrets attributes

    Raises:
        ValueError: If API token is not provided
    """
    token = api_token or os.getenv("KOYEB_API_TOKEN")
    if not token:
        raise ValueError(
            "API token is required. Set KOYEB_API_TOKEN environment variable or pass api_token parameter"
        )

    api_host = os.getenv("KOYEB_API_HOST", host)
    if not api_host:
        api_host = "https://app.koyeb.com"
    cache_key = (token, api_host)

    if cache_key in _api_clients_cache:
        return _api_clients_cache[cache_key]

    configuration = Configuration(host=api_host)
    configuration.api_key["Bearer"] = token
    configuration.api_key_prefix["Bearer"] = "Bearer"

    api_client = ApiClient(configuration)
    clients = ApiClients(
        apps=AppsApi(api_client),
        services=ServicesApi(api_client),
        instances=InstancesApi(api_client),
        catalog_instances=CatalogInstancesApi(api_client),
        deployments=DeploymentsApi(api_client),
        secrets=SecretsApi(api_client),
    )
    _api_clients_cache[cache_key] = clients
    return clients


# --- Async API clients ---

from koyeb.api_async import ApiClient as AsyncApiClient
from koyeb.api_async import Configuration as AsyncConfiguration
from koyeb.api_async.api import (
    AppsApi as AsyncAppsApi,
    CatalogInstancesApi as AsyncCatalogInstancesApi,
    DeploymentsApi as AsyncDeploymentsApi,
    InstancesApi as AsyncInstancesApi,
    SecretsApi as AsyncSecretsApi,
    ServicesApi as AsyncServicesApi,
)


@dataclass(frozen=True)
class AsyncApiClients:
    """Bundle of async Koyeb API clients sharing a single underlying AsyncApiClient."""

    apps: AsyncAppsApi
    services: AsyncServicesApi
    instances: AsyncInstancesApi
    catalog_instances: AsyncCatalogInstancesApi
    deployments: AsyncDeploymentsApi
    secrets: AsyncSecretsApi


_async_api_clients_cache: Dict[Tuple[str, str], AsyncApiClients] = {}


def get_async_api_clients(
    api_token: Optional[str] = None, host: Optional[str] = None
) -> AsyncApiClients:
    """
    Get configured async API clients for Koyeb operations.

    Caches clients by (token, host) to reuse the underlying HTTP connection pool.

    Args:
        api_token: Koyeb API token. If not provided, will try to get from KOYEB_API_TOKEN env var
        host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var

    Returns:
        AsyncApiClients with async API client instances

    Raises:
        ValueError: If API token is not provided
    """
    token = api_token or os.getenv("KOYEB_API_TOKEN")
    if not token:
        raise ValueError(
            "API token is required. Set KOYEB_API_TOKEN environment variable or pass api_token parameter"
        )

    api_host = os.getenv("KOYEB_API_HOST", host)
    if not api_host:
        api_host = "https://app.koyeb.com"
    cache_key = (token, api_host)

    if cache_key in _async_api_clients_cache:
        return _async_api_clients_cache[cache_key]

    configuration = AsyncConfiguration(host=api_host)
    configuration.api_key["Bearer"] = token
    configuration.api_key_prefix["Bearer"] = "Bearer"

    api_client = AsyncApiClient(configuration)
    clients = AsyncApiClients(
        apps=AsyncAppsApi(api_client),
        services=AsyncServicesApi(api_client),
        instances=AsyncInstancesApi(api_client),
        catalog_instances=AsyncCatalogInstancesApi(api_client),
        deployments=AsyncDeploymentsApi(api_client),
        secrets=AsyncSecretsApi(api_client),
    )
    _async_api_clients_cache[cache_key] = clients
    return clients


# --- Model building helpers (shared by sync and async) ---


def build_env_vars(env: Optional[Dict[str, Any]]) -> List[DeploymentEnv]:
    """
    Build environment variables list from dictionary.

    Args:
        env: Dictionary of environment variables. Values can be plain strings
            or ``Secret`` instances. A ``Secret`` value is rendered as
            ``"{{ secret.<name> }}"`` so the Koyeb API substitutes the secret
            value at deploy time.

    Returns:
        List of DeploymentEnv objects
    """
    env_vars = []
    if env:
        for key, value in env.items():
            if isinstance(value, Secret):
                value = "{{ secret." + value.name + " }}"
            env_vars.append(DeploymentEnv(key=key, value=value))
    return env_vars


DEFAULT_CONFIG_FILE_PERMISSIONS = "0644"


def build_config_files(
    config_files: Optional[Dict[str, Any]],
) -> List[ConfigFile]:
    """
    Build config files list from dictionary.

    Args:
        config_files: Dictionary mapping file paths to file contents.
            Values can be plain strings (default permissions 0644) or
            ``ConfigFile`` instances (custom permissions). The dict key is
            always used as the file path.

    Returns:
        List of ConfigFile objects
    """
    result = []
    if config_files:
        for path, value in config_files.items():
            if isinstance(value, ConfigFile):
                result.append(
                    ConfigFile(
                        path=path,
                        content=value.content,
                        permissions=value.permissions
                        or DEFAULT_CONFIG_FILE_PERMISSIONS,
                    )
                )
            else:
                result.append(
                    ConfigFile(
                        path=path,
                        content=value,
                        permissions=DEFAULT_CONFIG_FILE_PERMISSIONS,
                    )
                )
    return result


def create_docker_source(
    image: str,
    privileged: Optional[bool] = None,
    image_registry_secret: Optional[str] = None,
    entrypoint: Optional[List[str]] = None,
    command: Optional[str] = None,
    args: Optional[List[str]] = None,
) -> DockerSource:
    """
    Create Docker source configuration.

    Args:
        image: Docker image name
        privileged: If True, run the container in privileged mode (default: None/False)
        image_registry_secret: Name of the secret containing registry credentials
            for pulling private images
        entrypoint: Override the default entrypoint of the Docker image
        command: Override the default command of the Docker image
        args: Arguments to pass to the command

    Returns:
        DockerSource object
    """
    return DockerSource(
        image=image,
        command=command,
        args=args,
        privileged=privileged,
        image_registry_secret=image_registry_secret,
        entrypoint=entrypoint,
    )


def create_koyeb_sandbox_ports(protocol: str = "http") -> List[DeploymentPort]:
    """
    Create port configuration for koyeb/sandbox image.

    Creates two ports:
    - Port 3030 exposed on HTTP, mounted on /koyeb-sandbox/
    - Port 3031 exposed with the specified protocol, mounted on /

    Args:
        protocol: Protocol to use for port 3031 ("http" or "http2"), defaults to "http"

    Returns:
        List of DeploymentPort objects configured for koyeb/sandbox
    """
    return [
        DeploymentPort(
            port=3030,
            protocol="http",
        ),
        DeploymentPort(
            port=3031,
            protocol=protocol,
        ),
    ]


def create_koyeb_sandbox_proxy_ports() -> List[DeploymentProxyPort]:
    """
    Create TCP proxy port configuration for koyeb/sandbox image.

    Creates proxy port for direct TCP access:
    - Port 3031 exposed via TCP proxy

    Returns:
        List of DeploymentProxyPort objects configured for TCP proxy access
    """
    return [
        DeploymentProxyPort(
            port=3031,
            protocol=ProxyPortProtocol.TCP,
        ),
    ]


def create_koyeb_sandbox_routes() -> List[DeploymentRoute]:
    """
    Create route configuration for koyeb/sandbox image to make it publicly accessible.

    Creates two routes:
    - Port 3030 accessible at /koyeb-sandbox/
    - Port 3031 accessible at /

    Returns:
        List of DeploymentRoute objects configured for koyeb/sandbox
    """
    return [
        DeploymentRoute(port=3030, path="/koyeb-sandbox/"),
        DeploymentRoute(port=3031, path="/"),
    ]


def create_deployment_definition(
    name: str,
    docker_source: DockerSource,
    env_vars: List[DeploymentEnv],
    instance_type: str,
    exposed_port_protocol: Optional[str] = None,
    region: Optional[str] = None,
    routes: Optional[List[DeploymentRoute]] = None,
    idle_timeout: int = 300,
    enable_tcp_proxy: bool = False,
    _experimental_enable_light_sleep: bool = False,
    _experimental_deep_sleep_value: int = 3900,
    enable_mesh: bool = None,
    config_files: Optional[List[ConfigFile]] = None,
) -> DeploymentDefinition:
    """
    Create deployment definition for a sandbox service.

    Args:
        name: Service name
        docker_source: Docker configuration
        env_vars: Environment variables
        instance_type: Instance type
        exposed_port_protocol: Protocol to expose ports with ("http" or "http2").
            If None, defaults to "http".
            If provided, must be one of "http" or "http2".
        region: Region to deploy to. Defaults to KOYEB_REGION env var, or "na" if not set.
        routes: List of routes for public access
        idle_timeout: Number of seconds to wait before sleeping the instance if it receives no traffic
        enable_tcp_proxy: If True, enables TCP proxy for direct TCP access to port 3031
        _experimental_enable_light_sleep: If True, uses light sleep when reaching idle_timeout.
            Light Sleep reduces cold starts to ~200ms. After scaling to zero, the service stays in Light Sleep for idle_timeout seconds before going into Deep Sleep.
        _experimental_deep_sleep_value: Number of seconds for deep sleep when light sleep is enabled (default: 3900).
            Only used if _experimental_enable_light_sleep is True. Ignored otherwise.
        enable_mesh: Enable or disable mesh for this sandbox. Disabled by default

    Returns:
        DeploymentDefinition object
    """
    if region is None:
        region = os.getenv("KOYEB_REGION", "na")

    # Convert single region string to list for API
    regions_list = [region]

    # Always create ports with protocol (default to "http" if not specified)
    protocol = exposed_port_protocol if exposed_port_protocol is not None else "http"
    # Validate protocol using API model structure
    protocol = _validate_port_protocol(protocol)
    ports = create_koyeb_sandbox_ports(protocol)

    # Create TCP proxy ports if enabled
    proxy_ports = None
    if enable_tcp_proxy:
        proxy_ports = create_koyeb_sandbox_proxy_ports()

    # Always use SANDBOX type
    deployment_type = DeploymentDefinitionType.SANDBOX

    # Process idle_timeout
    if idle_timeout == 0:
        sleep_idle_delay = None
    elif _experimental_enable_light_sleep:
        # Experimental mode: idle_timeout sets light_sleep value, deep_sleep uses _experimental_deep_sleep_value
        sleep_idle_delay = DeploymentScalingTargetSleepIdleDelay(
            light_sleep_value=idle_timeout,
            deep_sleep_value=_experimental_deep_sleep_value,
        )
    else:
        # Normal mode: only use deep_sleep
        sleep_idle_delay = DeploymentScalingTargetSleepIdleDelay(
            deep_sleep_value=idle_timeout,
        )

    # Create scaling configuration
    # If idle_timeout is 0, explicitly disable scale-to-zero (min=1, always-on)
    # Otherwise (int > 0), enable scale-to-zero (min=0)
    min_scale = 1 if idle_timeout == 0 else 0
    targets = None
    if sleep_idle_delay is not None:
        scaling_target = DeploymentScalingTarget(sleep_idle_delay=sleep_idle_delay)
        targets = [scaling_target]

    scalings = [DeploymentScaling(min=min_scale, max=1, targets=targets)]

    # Set mesh configuration
    mesh = DeploymentMesh.DEPLOYMENT_MESH_AUTO
    if enable_mesh is None:
        mesh = DeploymentMesh.DEPLOYMENT_MESH_AUTO
    elif not enable_mesh:
        mesh = DeploymentMesh.DEPLOYMENT_MESH_DISABLED
    elif enable_mesh:
        mesh = DeploymentMesh.DEPLOYMENT_MESH_ENABLED

    return DeploymentDefinition(
        name=name,
        type=deployment_type,
        docker=docker_source,
        env=env_vars,
        ports=ports,
        proxy_ports=proxy_ports,
        routes=routes,
        instance_types=[DeploymentInstanceType(type=instance_type)],
        scalings=scalings,
        regions=regions_list,
        mesh=mesh,
        config_files=config_files if config_files else None,
    )


def escape_shell_arg(arg: str) -> str:
    """
    Escape a shell argument for safe use in shell commands.

    Args:
        arg: The argument to escape

    Returns:
        Properly escaped shell argument
    """
    return shlex.quote(arg)


def validate_port(port: int) -> None:
    """
    Validate that a port number is in the valid range.

    Args:
        port: Port number to validate

    Raises:
        ValueError: If port is not in valid range [1, 65535]
    """
    if not isinstance(port, int) or port < MIN_PORT or port > MAX_PORT:
        raise ValueError(
            f"Port must be an integer between {MIN_PORT} and {MAX_PORT}, got {port}"
        )


def check_error_message(error_msg: str, error_type: str) -> bool:
    """
    Check if an error message matches a specific error type.
    Uses case-insensitive matching against known error patterns.

    Args:
        error_msg: The error message to check
        error_type: The type of error to check for (key in ERROR_MESSAGES)

    Returns:
        True if error message matches the error type
    """
    if error_type not in ERROR_MESSAGES:
        return False

    error_msg_lower = error_msg.lower()
    patterns = ERROR_MESSAGES[error_type]
    return any(pattern.lower() in error_msg_lower for pattern in patterns)


def create_sandbox_client(
    conn_info: Optional['ConnectionInfo'],
    existing_client: Optional[Any] = None,
) -> Any:
    """
    Create or return existing SandboxClient instance with validation.

    Helper function to create SandboxClient instances with consistent validation.
    Used by Sandbox, SandboxExecutor, and SandboxFilesystem to avoid duplication.

    Args:
        conn_info: The information needed to connect to the sandbox executor API
        existing_client: Existing client instance to return if not None

    Returns:
        SandboxClient: Configured client instance

    Raises:
        SandboxError: If sandbox URL or secret is not available
    """
    if existing_client is not None:
        return existing_client

    try:
        conn_info.validate()
    except ValueError as e:
        raise SandboxError(str(e))

    from .executor_client import SandboxClient

    return SandboxClient(conn_info)


def create_async_sandbox_client(
    conn_info: Optional['ConnectionInfo'],
    existing_client: Optional[Any] = None,
) -> Any:
    """
    Create or return existing AsyncSandboxClient instance with validation.

    Helper function to create AsyncSandboxClient instances with consistent validation.
    Used by AsyncSandbox to avoid duplication.

    Args:
        conn_info: The information needed to connect to the sandbox executor API
        existing_client: Existing client instance to return if not None

    Returns:
        AsyncSandboxClient: Configured async client instance

    Raises:
        SandboxError: If sandbox URL or secret is not available
    """
    if existing_client is not None:
        return existing_client

    try:
        conn_info.validate()
    except ValueError as e:
        raise SandboxError(str(e))

    from .executor_client import AsyncSandboxClient

    return AsyncSandboxClient(conn_info)


class SandboxError(Exception):
    """Base exception for sandbox operations"""


class SandboxTimeoutError(SandboxError):
    """Raised when a sandbox operation times out"""


class SandboxDeploymentError(SandboxError):
    """Raised when a sandbox deployment reaches an error state"""
