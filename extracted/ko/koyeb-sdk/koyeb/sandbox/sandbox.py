# coding: utf-8

"""
Koyeb Sandbox - Python SDK for creating and managing Koyeb sandboxes
"""

from __future__ import annotations

import asyncio
import os
import secrets
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from koyeb.api.api.deployments_api import DeploymentsApi
from koyeb.api.exceptions import ApiException, NotFoundException
from koyeb.api.models.create_app import AppLifeCycle, CreateApp
from koyeb.api.models.create_service import CreateService, ServiceLifeCycle
from koyeb.api.models.deployment_status import DeploymentStatus
from koyeb.api.models.update_service import UpdateService

from .executor_client import ConnectionInfo
from .utils import (
    DEFAULT_INSTANCE_WAIT_TIMEOUT,
    DEFAULT_POLL_INTERVAL,
    SandboxDeploymentError,
    SandboxError,
    SandboxTimeoutError,
    build_config_files,
    build_env_vars,
    create_deployment_definition,
    create_docker_source,
    create_koyeb_sandbox_routes,
    create_sandbox_client,
    get_api_clients,
    logger,
    validate_port,
)

if TYPE_CHECKING:
    from .exec import AsyncSandboxExecutor, SandboxExecutor
    from .executor_client import AsyncSandboxClient, SandboxClient
    from .filesystem import AsyncSandboxFilesystem, SandboxFilesystem


@dataclass
class ProcessInfo:
    """Type definition for process information returned by list_processes."""

    id: str  # Process ID (UUID string)
    command: str  # The command that was executed
    status: str  # Process status (e.g., "running", "completed")
    pid: Optional[int] = None  # OS process ID (if running)
    exit_code: Optional[int] = None  # Exit code (if completed)
    started_at: Optional[str] = None  # ISO 8601 timestamp when process started
    completed_at: Optional[str] = (
        None  # ISO 8601 timestamp when process completed (if applicable)
    )


@dataclass
class ExposedPort:
    """Result of exposing a port via TCP proxy."""

    port: int
    exposed_at: str

    def __str__(self) -> str:
        return f"ExposedPort(port={self.port}, exposed_at='{self.exposed_at}')"


class Sandbox:
    """
    Synchronous sandbox for running code on Koyeb infrastructure.
    Provides creation and deletion functionality with proper health polling.
    """

    def __init__(
        self,
        sandbox_id: str,
        app_id: str,
        service_id: str,
        name: Optional[str] = None,
        api_token: Optional[str] = None,
        sandbox_secret: Optional[str] = None,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        host: Optional[str] = None,
    ):
        self.sandbox_id = sandbox_id
        self.app_id = app_id
        self.service_id = service_id
        self.name = name
        self.api_token = api_token
        self.sandbox_secret = sandbox_secret
        self.poll_interval = poll_interval
        self.host = host
        self._created_at = time.time()
        self._sandbox_url: Optional[Tuple[str, Optional[str]]] = None
        self._domain: Optional[str] = None
        self._url: Optional[str] = None
        self._client = None
        self._deployment_id: Optional[str] = None
        self._executor = None
        self._filesystem = None

    @property
    def id(self) -> str:
        """Get the service ID of the sandbox."""
        return self.service_id

    @classmethod
    def create(
        cls,
        image: str = "koyeb/sandbox",
        name: str = "quick-sandbox",
        wait_ready: bool = True,
        instance_type: str = "micro",
        exposed_port_protocol: Optional[str] = None,
        env: Optional[Dict[str, Any]] = None,
        config_files: Optional[Dict[str, Any]] = None,
        region: Optional[str] = None,
        api_token: Optional[str] = None,
        timeout: int = 300,
        idle_timeout: int = 300,
        enable_tcp_proxy: bool = False,
        privileged: bool = False,
        registry_secret: Optional[str] = None,
        _experimental_enable_light_sleep: bool = False,
        _experimental_deep_sleep_value: int = 3900,
        delete_after_delay: int = 0,
        delete_after_inactivity_delay: int = 0,
        app_id: Optional[str] = None,
        enable_mesh: bool = None,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        entrypoint: Optional[List[str]] = None,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        host: Optional[str] = None,
    ) -> Sandbox:
        """
            Create a new sandbox instance.

            Args:
                image: Docker image to use (default: koyeb/sandbox)
                name: Name of the sandbox
                wait_ready: Wait for sandbox to be ready (default: True)
                instance_type: Instance type (default: micro)
                exposed_port_protocol: Protocol to expose ports with ("http" or "http2").
                    If None, defaults to "http".
                    If provided, must be one of "http" or "http2".
                env: Environment variables
                config_files: Config files to create in the sandbox, as a dictionary mapping
                    file paths to file contents. Values can be plain strings (default permissions 0644)
                    or ``ConfigFile`` instances for custom permissions
                    (e.g., {"/etc/myapp/config.yaml": "key: value", "/etc/myapp/cert.pem": ConfigFile(content="...", permissions="0600")})
                region: Region to deploy to. Defaults to KOYEB_REGION env var, or "na" if not set.
                api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
                timeout: Timeout for sandbox creation in seconds
                idle_timeout: Sleep timeout in seconds. Behavior depends on _experimental_enable_light_sleep:
                    - If _experimental_enable_light_sleep is True: sets light_sleep value (deep_sleep=3900)
                    - If _experimental_enable_light_sleep is False: sets deep_sleep value
                    - If 0: disables scale-to-zero (keep always-on)
                    - If None: uses default values
                enable_tcp_proxy: If True, enables TCP proxy for direct TCP access to port 3031
                privileged: If True, run the container in privileged mode (default: False)
                registry_secret: Name of a Koyeb secret containing registry credentials for
                    pulling private images. Create the secret via Koyeb dashboard or CLI first.
                _experimental_enable_light_sleep: If True, uses idle_timeout for light_sleep and sets
                    deep_sleep=3900. If False, uses idle_timeout for deep_sleep (default: False)
                delete_after_delay: If >0, automatically delete the sandbox if there was no activity
                    after this many seconds since creation.
                delete_after_inactivity_delay: If >0, automatically delete the sandbox if service sleeps due to inactivity
                    after this many seconds.
                app_id: If provided, create the sandbox service in an existing app instead of creating a new one.
                enable_mesh: Enable or disable mesh for this sandbox. Disabled by default
                poll_interval: Time between health checks in seconds when wait_ready is True (default: 0.5)
                entrypoint: Override the default entrypoint of the Docker image (e.g., ["/bin/sh", "-c"])
                command: Override the default command of the Docker image (e.g., "python app.py")
                host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

        Returns:
                Sandbox: A new Sandbox instance

        Raises:
                ValueError: If API token is not provided
                SandboxTimeoutError: If wait_ready is True and sandbox does not become ready within timeout

        Example:
            >>> # Public image (default)
            >>> sandbox = Sandbox.create()

            >>> # Private image with registry secret
            >>> sandbox = Sandbox.create(
            ...     image="ghcr.io/myorg/myimage:latest",
            ...     registry_secret="my-ghcr-secret"
            ... )
        """
        if api_token is None:
            api_token = os.getenv("KOYEB_API_TOKEN")
            if not api_token:
                raise ValueError(
                    "API token is required. Set KOYEB_API_TOKEN environment variable or pass api_token parameter"
                )

        sandbox = cls._create_sync(
            name=name,
            image=image,
            instance_type=instance_type,
            exposed_port_protocol=exposed_port_protocol,
            env=env,
            config_files=config_files,
            region=region,
            api_token=api_token,
            timeout=timeout,
            idle_timeout=idle_timeout,
            enable_tcp_proxy=enable_tcp_proxy,
            privileged=privileged,
            registry_secret=registry_secret,
            _experimental_enable_light_sleep=_experimental_enable_light_sleep,
            _experimental_deep_sleep_value=_experimental_deep_sleep_value,
            delete_after_delay=delete_after_delay,
            delete_after_inactivity_delay=delete_after_inactivity_delay,
            app_id=app_id,
            enable_mesh=enable_mesh,
            poll_interval=poll_interval,
            entrypoint=entrypoint,
            command=command,
            args=args,
            host=host,
        )

        if wait_ready:
            is_ready = sandbox.wait_ready(timeout=timeout)
            if not is_ready:
                raise SandboxTimeoutError(
                    f"Sandbox '{sandbox.name}' did not become ready within {timeout} seconds. "
                    f"The sandbox was created but may not be ready yet. "
                    f"You can check its status with sandbox.is_healthy() or call sandbox.wait_ready() again."
                )

        return sandbox

    @classmethod
    def _create_sync(
        cls,
        name: str,
        image: str = "koyeb/sandbox",
        instance_type: str = "micro",
        exposed_port_protocol: Optional[str] = None,
        env: Optional[Dict[str, Any]] = None,
        config_files: Optional[Dict[str, Any]] = None,
        region: Optional[str] = None,
        api_token: Optional[str] = None,
        timeout: int = 300,
        idle_timeout: int = 0,
        enable_tcp_proxy: bool = False,
        privileged: bool = False,
        registry_secret: Optional[str] = None,
        _experimental_enable_light_sleep: bool = False,
        _experimental_deep_sleep_value: int = 3900,
        delete_after_delay: int = 0,
        delete_after_inactivity_delay: int = 0,
        app_id: Optional[str] = None,
        enable_mesh: bool = None,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        entrypoint: Optional[List[str]] = None,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        host: Optional[str] = None,
    ) -> Sandbox:
        """
        Synchronous creation method that returns creation parameters.
        Subclasses can override to return their own type.
        """

        clients = get_api_clients(api_token, host)
        apps_api = clients.apps
        services_api = clients.services

        # Always create routes (ports are always exposed, default to "http")
        routes = create_koyeb_sandbox_routes()

        # Generate secure sandbox secret
        sandbox_secret = secrets.token_urlsafe(32)

        # Add SANDBOX_SECRET to environment variables
        if env is None:
            env = {}
        env["SANDBOX_SECRET"] = sandbox_secret

        # Use provided app_id or create a new app
        if app_id is None:
            app_name = f"sandbox-app-{name}-{int(time.time())}"
            app_response = apps_api.create_app(
                app=CreateApp(
                    name=app_name, life_cycle=AppLifeCycle(delete_when_empty=True)
                )
            )
            app_id = app_response.app.id

        env_vars = build_env_vars(env)
        config_file_objects = build_config_files(config_files)
        docker_source = create_docker_source(
            image, privileged=privileged, image_registry_secret=registry_secret,
            entrypoint=entrypoint, command=command, args=args,
        )

        deployment_definition = create_deployment_definition(
            name=name,
            docker_source=docker_source,
            env_vars=env_vars,
            instance_type=instance_type,
            exposed_port_protocol=exposed_port_protocol,
            region=region,
            routes=routes,
            idle_timeout=idle_timeout,
            enable_tcp_proxy=enable_tcp_proxy,
            _experimental_enable_light_sleep=_experimental_enable_light_sleep,
            _experimental_deep_sleep_value=_experimental_deep_sleep_value,
            enable_mesh=enable_mesh,
            config_files=config_file_objects if config_file_objects else None,
        )

        service_life_cycle = ServiceLifeCycle(
            delete_after_create=delete_after_delay,
            delete_after_sleep=delete_after_inactivity_delay,
        )
        create_service = CreateService(
            app_id=app_id,
            definition=deployment_definition,
            life_cycle=service_life_cycle,
        )
        service_response = services_api.create_service(service=create_service)
        service_id = service_response.service.id

        return cls(
            sandbox_id=name,
            app_id=app_id,
            service_id=service_id,
            name=name,
            api_token=api_token,
            sandbox_secret=sandbox_secret,
            poll_interval=poll_interval,
            host=host,
        )

    @classmethod
    def get_from_id(
        cls,
        id: str,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "Sandbox":
        """
        Get a sandbox by service ID.

        Args:
            id: Service ID of the sandbox
            api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
            host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

        Returns:
            Sandbox: The Sandbox instance

        Raises:
            ValueError: If API token is not provided or id is invalid
            SandboxError: If sandbox is not found or retrieval fails
        """
        if api_token is None:
            api_token = os.getenv("KOYEB_API_TOKEN")
            if not api_token:
                raise ValueError(
                    "API token is required. Set KOYEB_API_TOKEN environment variable or pass api_token parameter"
                )

        if not id:
            raise ValueError("id is required")

        clients = get_api_clients(api_token, host)
        services_api = clients.services
        deployments_api = clients.deployments

        # Get service by ID
        try:
            service_response = services_api.get_service(id=id)
            service = service_response.service
        except NotFoundException as e:
            raise SandboxError(f"Sandbox not found with id: {id}") from e
        except ApiException as e:
            raise SandboxError(f"Failed to retrieve sandbox with id: {id}: {e}") from e

        if service is None:
            raise SandboxError(f"Sandbox not found with id: {id}")

        sandbox_name = service.name

        # Get deployment to extract sandbox_secret and metadata
        deployment_id = service.active_deployment_id or service.latest_deployment_id
        sandbox_secret = None
        sandbox_metadata = None

        if deployment_id:
            try:
                deployment_response = deployments_api.get_deployment(id=deployment_id)
                deployment = deployment_response.deployment
                if deployment and deployment.definition and deployment.definition.env:
                    # Find SANDBOX_SECRET in env vars
                    for env_var in deployment.definition.env:
                        if env_var.key == "SANDBOX_SECRET":
                            sandbox_secret = env_var.value
                            break
                if deployment and deployment.metadata:
                    sandbox_metadata = deployment.metadata
            except Exception as e:
                logger.debug(f"Could not get deployment {deployment_id}: {e}")

        sandbox = cls(
            sandbox_id=service.id,
            app_id=service.app_id,
            service_id=service.id,
            name=sandbox_name,
            api_token=api_token,
            sandbox_secret=sandbox_secret,
            host=host,
        )
        if deployment_id:
            sandbox._deployment_id = deployment_id

        # Pre-cache sandbox URL from deployment metadata or app domain
        if sandbox_metadata and sandbox_metadata.sandbox:
            sandbox._sandbox_url = (
                f"{sandbox_metadata.sandbox.public_url}/koyeb-sandbox",
                sandbox_metadata.sandbox.routing_key,
            )
        else:
            # Fallback: resolve domain from app (we already have app_id)
            try:
                app_response = clients.apps.get_app(service.app_id)
                app = app_response.app
                if hasattr(app, "domains") and app.domains:
                    sandbox._sandbox_url = (
                        f"https://{app.domains[0].name}/koyeb-sandbox",
                        None,
                    )
            except Exception:
                pass

        return sandbox

    _DEPLOYMENT_ERROR_STATUSES = {
        DeploymentStatus.ERROR,
        DeploymentStatus.ERRORING,
    }

    def _resolve_deployment_id(self) -> Optional[str]:
        """Resolve and cache the deployment ID for this sandbox's service."""
        if self._deployment_id is not None:
            return self._deployment_id
        clients = get_api_clients(self.api_token, self.host)
        service_response = clients.services.get_service(self.service_id)
        service = service_response.service
        deployment_id = service.active_deployment_id or service.latest_deployment_id
        if deployment_id:
            self._deployment_id = deployment_id
        return deployment_id

    def _is_deployment_healthy(self) -> bool:
        """
        Check if the sandbox deployment status is HEALTHY via the API.
        When the deployment becomes healthy, also caches the sandbox URL
        from deployment metadata if available.

        Returns:
            bool: True if the deployment status is HEALTHY, False otherwise

        Raises:
            SandboxDeploymentError: If the deployment has reached a terminal error state
        """
        try:
            deployment_id = self._resolve_deployment_id()
            if not deployment_id:
                return False
            clients = get_api_clients(self.api_token, self.host)
            deployment_response = clients.deployments.get_deployment(deployment_id)
            deployment = deployment_response.deployment
            status = deployment.status
            if status in self._DEPLOYMENT_ERROR_STATUSES:
                raise SandboxDeploymentError(
                    f"Sandbox '{self.name}' deployment reached status {status.value}. "
                    f"The sandbox will not become ready."
                )
            is_healthy = status == DeploymentStatus.HEALTHY
            # Cache sandbox URL from metadata when deployment is healthy
            if is_healthy and self._sandbox_url is None:
                metadata = deployment.metadata
                if metadata and metadata.sandbox:
                    self._sandbox_url = (
                        f"{metadata.sandbox.public_url}/koyeb-sandbox",
                        metadata.sandbox.routing_key,
                    )
            return is_healthy
        except SandboxDeploymentError:
            raise
        except Exception as e:
            logger.debug(f"Could not get deployment for service {self.service_id}: {e}")
            return False

    def wait_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: Optional[float] = None,
    ) -> bool:
        """
        Wait for sandbox to become ready with exponential backoff polling.

        First waits for the deployment status to become HEALTHY, then polls the
        sandbox health endpoint to confirm the executor is responsive.

        Starts polling at 0.1s intervals, doubling each time up to poll_interval.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Maximum time between health checks in seconds (defaults to instance poll_interval)

        Returns:
            bool: True if sandbox became ready, False if timeout
        """
        if poll_interval is None:
            poll_interval = self.poll_interval
        start_time = time.time()
        deployment_healthy = False
        current_interval = 0.1

        while time.time() - start_time < timeout:
            # First, wait for the deployment to be healthy before sending traffic
            if not deployment_healthy:
                deployment_healthy = self._is_deployment_healthy()
                if not deployment_healthy:
                    time.sleep(current_interval)
                    current_interval = min(current_interval * 2, poll_interval)
                    continue

            # Deployment is already confirmed healthy above, skip redundant
            # _is_deployment_healthy() check and go straight to executor health
            if self._check_executor_health():
                return True

            time.sleep(current_interval)
            current_interval = min(current_interval * 2, poll_interval)

        return False

    def wait_tcp_proxy_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: Optional[float] = None,
    ) -> bool:
        """
        Wait for TCP proxy to become ready and available.

        Polls the deployment metadata with exponential backoff until the TCP proxy
        information is available. Starts at 0.1s intervals, doubling up to poll_interval.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Maximum time between checks in seconds (defaults to instance poll_interval)

        Returns:
            bool: True if TCP proxy became ready, False if timeout
        """
        if poll_interval is None:
            poll_interval = self.poll_interval
        start_time = time.time()
        current_interval = 0.1

        while time.time() - start_time < timeout:
            tcp_proxy_info = self.get_tcp_proxy_info()
            if tcp_proxy_info is not None:
                return True

            time.sleep(current_interval)
            current_interval = min(current_interval * 2, poll_interval)

        return False

    def delete(self) -> None:
        """Delete the sandbox instance."""
        clients = get_api_clients(self.api_token, self.host)
        clients.apps.delete_app(self.app_id)

    def _get_url_and_header_from_metadata(self) -> Optional[Tuple[str, str]]:
        """
        Get the public url of the sandbox and the routing key to use to reach it.
        """
        try:
            from koyeb.api.exceptions import ApiException, NotFoundException

            deployment_id = self._resolve_deployment_id()
            if not deployment_id:
                return None

            from .utils import get_api_clients

            clients = get_api_clients(self.api_token, self.host)
            deployment = clients.deployments.get_deployment(deployment_id)
            metadata = deployment.deployment.metadata
            if metadata and metadata.sandbox:
                return metadata.sandbox.public_url, metadata.sandbox.routing_key
            return None

        except (NotFoundException, ApiException, Exception):
            return None

    def _get_domain(self) -> Optional[str]:
        """
        Internal method to get the public domain of the sandbox.

        Returns the domain name (e.g., "app-name-org.koyeb.app") without protocol or path.

        Returns:
            Optional[str]: The domain name or None if unavailable
        """
        try:
            from koyeb.api.exceptions import ApiException, NotFoundException

            if not self.app_id:
                return None

            from .utils import get_api_clients

            clients = get_api_clients(self.api_token, self.host)
            app_response = clients.apps.get_app(self.app_id)
            app = app_response.app
            if hasattr(app, "domains") and app.domains:
                # Use the first public domain
                return app.domains[0].name
            return None
        except (NotFoundException, ApiException, Exception):
            return None

    def _get_url(self) -> Optional[str]:
        """
        Get the public URL of the sandbox with protocol.

        Returns the full URL (e.g., "https://app-name-org.koyeb.app/r/routing_key/" or
        "https://app-name-org.koyeb.app").

        Returns:
            Optional[str]: The full URL or None if unavailable
        """
        if self._url is None:
            url_data = self._get_url_and_header_from_metadata()
            if url_data:
                self._url = f"{url_data[0]}/r/{url_data[1]}/"
                return self._url

            domain = self._get_domain()
            if domain:
                self._url = f"https://{domain}"
        return self._url

    def get_domain(self) -> Optional[str]:
        """
        Get the public domain of the sandbox.

        Returns the domain (e.g., "app-name-org.koyeb.app/r/routing_key/" or
        "app-name-org.koyeb.app") without protocol. To get the full URL with protocol,
        use sandbox._get_url()

        Returns:
            Optional[str]: The domain or None if unavailable
        """
        url = self._get_url()
        if url:
            if url.startswith("https://"):
                return url[8:]
            elif url.startswith("http://"):
                return url[7:]
        return url

    def get_tcp_proxy_info(self) -> Optional[tuple[str, int]]:
        """
        Get the TCP proxy host and port for the sandbox.

        Returns the TCP proxy host and port as a tuple (host, port) for direct TCP access to port 3031.
        This is only available if enable_tcp_proxy=True was set when creating the sandbox.

        Returns:
            Optional[tuple[str, int]]: A tuple of (host, port) or None if unavailable
        """
        try:
            from koyeb.api.exceptions import ApiException, NotFoundException

            from .utils import get_api_clients

            clients = get_api_clients(self.api_token, self.host)
            services_api = clients.services
            service_response = services_api.get_service(self.service_id)
            service = service_response.service

            if not service.active_deployment_id:
                return None

            # Get the active deployment
            deployments_api = DeploymentsApi()
            deployments_api.api_client = services_api.api_client
            deployment_response = deployments_api.get_deployment(
                service.active_deployment_id
            )
            deployment = deployment_response.deployment

            if not deployment.metadata or not deployment.metadata.proxy_ports:
                return None

            # Find the proxy port for port 3031
            for proxy_port in deployment.metadata.proxy_ports:
                if (
                    proxy_port.port == 3031
                    and proxy_port.host
                    and proxy_port.public_port
                ):
                    return (proxy_port.host, proxy_port.public_port)

            return None
        except (NotFoundException, ApiException, Exception):
            return None

    def _get_sandbox_url(self) -> Optional[Tuple[str, Optional[str]]]:
        """
        Internal method to get the sandbox URL for health checks and client initialization.
        Caches the URL after first retrieval.

        Returns:
            str: the public url where to reach the sandbox
            Optional[str]: the routing key to use to reach the sandbox, if needed
        """
        if self._sandbox_url is None:
            url_data = self._get_url_and_header_from_metadata()
            if url_data:
                self._sandbox_url = (f"{url_data[0]}/koyeb-sandbox", url_data[1])
                return self._sandbox_url

            domain = self._get_domain()
            if domain:
                self._sandbox_url = (f"https://{domain}/koyeb-sandbox", None)
        return self._sandbox_url

    def _get_conn_info(self) -> Optional[ConnectionInfo]:
        """
        Internal method to get the parameters needed to connect to the sandbox.
        Caches the info after first retrieval.

        Returns:
            Optional[ConnectionInfo]: the information needed to connect to the sandbox
        """
        sandbox_url, routing_key = self._get_sandbox_url()
        if sandbox_url:
            return ConnectionInfo(sandbox_url, routing_key, self.sandbox_secret)

        return None

    def _get_client(self) -> "SandboxClient":  # type: ignore[name-defined]
        """
        Get or create SandboxClient instance with validation.

        Returns:
            SandboxClient: Configured client instance

        Raises:
            SandboxError: If sandbox URL or secret is not available
        """
        if self._client is None:
            sandbox_url, routing_key = self._get_sandbox_url()
            conn_info = ConnectionInfo(sandbox_url, routing_key, self.sandbox_secret)
            self._client = create_sandbox_client(conn_info)
        return self._client

    def _check_response_error(self, response: Dict, operation: str) -> None:
        """
        Check if a response indicates an error and raise SandboxError if so.

        Args:
            response: The response dictionary to check
            operation: Description of the operation (e.g., "expose port 8080")

        Raises:
            SandboxError: If response indicates failure
        """
        if not response.get("success", False):
            error_msg = response.get("error", "Unknown error")
            raise SandboxError(f"Failed to {operation}: {error_msg}")

    def _check_executor_health(self) -> bool:
        """Check if the sandbox executor is responsive. Assumes deployment is already healthy."""
        try:
            client = self._get_client()
            health_response = client.health()
            if isinstance(health_response, dict):
                status = health_response.get("status", "").lower()
                return status in ["ok", "healthy", "ready"]
            return True  # If we got a response, consider it healthy
        except Exception:
            return False

    def is_healthy(self) -> bool:
        """Check if sandbox is healthy and ready for operations"""
        # Check deployment status first to avoid sending traffic to a non-ready sandbox
        if not self._is_deployment_healthy():
            return False

        return self._check_executor_health()

    @property
    def filesystem(self) -> "SandboxFilesystem":
        """Get filesystem operations interface"""
        if self._filesystem is None:
            from .filesystem import SandboxFilesystem

            self._filesystem = SandboxFilesystem(self)
        return self._filesystem

    @property
    def exec(self) -> "SandboxExecutor":
        """Get command execution interface"""
        if self._executor is None:
            from .exec import SandboxExecutor

            self._executor = SandboxExecutor(self)
        return self._executor

    def expose_port(self, port: int) -> ExposedPort:
        """
        Expose a port to external connections via TCP proxy.

        Binds the specified internal port to the TCP proxy, allowing external
        connections to reach services running on that port inside the sandbox.
        Automatically unbinds any existing port before binding the new one.

        Args:
            port: The internal port number to expose (must be a valid port number between 1 and 65535)

        Returns:
            ExposedPort: An object with `port` and `exposed_at` attributes:
                - port: The exposed port number
                - exposed_at: The full URL with https:// protocol (e.g., "https://app-name-org.koyeb.app")

        Raises:
            ValueError: If port is not in valid range [1, 65535]
            SandboxError: If the port binding operation fails

        Notes:
            - Only one port can be exposed at a time
            - Any existing port binding is automatically unbound before binding the new port
            - The port must be available and accessible within the sandbox environment
            - The TCP proxy is accessed via get_tcp_proxy_info() which returns (host, port)

        Example:
            >>> result = sandbox.expose_port(8080)
            >>> result.port
            8080
            >>> result.exposed_at
            'https://app-name-org.koyeb.app'
        """
        validate_port(port)
        client = self._get_client()
        try:
            # Always unbind any existing port first
            try:
                client.unbind_port()
            except Exception as e:
                # Ignore errors when unbinding - it's okay if no port was bound
                logger.debug(f"Error unbinding existing port (this is okay): {e}")
                pass

            # Now bind the new port
            response = client.bind_port(port)
            self._check_response_error(response, f"expose port {port}")

            # Get URL for exposed_at
            url = self._get_url()
            if not url:
                raise SandboxError("URL not available for exposed port")

            # Return the port from response if available, otherwise use the requested port
            exposed_port = int(response.get("port", port))
            exposed_at = url
            return ExposedPort(port=exposed_port, exposed_at=exposed_at)
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to expose port {port}: {str(e)}") from e

    def unexpose_port(self) -> None:
        """
        Unexpose a port from external connections.

        Removes the TCP proxy port binding, stopping traffic forwarding to the
        previously bound port.

        Raises:
            SandboxError: If the port unbinding operation fails

        Notes:
            - After unexposing, the TCP proxy will no longer forward traffic
            - Safe to call even if no port is currently bound
        """
        client = self._get_client()
        try:
            response = client.unbind_port()
            self._check_response_error(response, "unexpose port")
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to unexpose port: {str(e)}") from e

    def launch_process(
        self, cmd: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Launch a background process in the sandbox.

        Starts a long-running background process that continues executing even after
        the method returns. Use this for servers, workers, or other long-running tasks.

        Args:
            cmd: The shell command to execute as a background process
            cwd: Optional working directory for the process
            env: Optional environment variables to set/override for the process

        Returns:
            str: The unique process ID (UUID string) that can be used to manage the process

        Raises:
            SandboxError: If the process launch fails

        Example:
            >>> process_id = sandbox.launch_process("python -u server.py")
            >>> print(f"Started process: {process_id}")
        """
        client = self._get_client()
        try:
            response = client.start_process(cmd, cwd, env)
            # Check for process ID - if it exists, the process was launched successfully
            process_id = response.get("id")
            if process_id:
                return process_id
            # If no ID, check for explicit error
            error_msg = response.get("error", response.get("message", "Unknown error"))
            raise SandboxError(f"Failed to launch process: {error_msg}")
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to launch process: {str(e)}") from e

    def kill_process(self, process_id: str) -> None:
        """
        Kill a background process by its ID.

        Terminates a running background process. This sends a SIGTERM signal to the process,
        allowing it to clean up gracefully. If the process doesn't terminate within a timeout,
        it will be forcefully killed with SIGKILL.

        Args:
            process_id: The unique process ID (UUID string) to kill

        Raises:
            SandboxError: If the process kill operation fails

        Example:
            >>> sandbox.kill_process("550e8400-e29b-41d4-a716-446655440000")
        """
        client = self._get_client()
        try:
            response = client.kill_process(process_id)
            self._check_response_error(response, f"kill process {process_id}")
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to kill process {process_id}: {str(e)}") from e

    def list_processes(self) -> List[ProcessInfo]:
        """
        List all background processes.

        Returns information about all currently running and recently completed background
        processes. This includes both active processes and processes that have completed
        (which remain in memory until server restart).

        Returns:
            List[ProcessInfo]: List of process objects, each containing:
                - id: Process ID (UUID string)
                - command: The command that was executed
                - status: Process status (e.g., "running", "completed")
                - pid: OS process ID (if running)
                - exit_code: Exit code (if completed)
                - started_at: ISO 8601 timestamp when process started
                - completed_at: ISO 8601 timestamp when process completed (if applicable)

        Raises:
            SandboxError: If listing processes fails

        Example:
            >>> processes = sandbox.list_processes()
            >>> for process in processes:
            ...     print(f"{process.id}: {process.command} - {process.status}")
        """
        client = self._get_client()
        try:
            response = client.list_processes()
            processes_data = response.get("processes", [])
            return [ProcessInfo(**process) for process in processes_data]
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to list processes: {str(e)}") from e

    def kill_all_processes(self) -> int:
        """
        Kill all running background processes.

        Convenience method that lists all processes and kills them all. This is useful
        for cleanup operations.

        Returns:
            int: The number of processes that were killed

        Raises:
            SandboxError: If listing or killing processes fails

        Example:
            >>> count = sandbox.kill_all_processes()
            >>> print(f"Killed {count} processes")
        """
        processes = self.list_processes()
        killed_count = 0
        for process in processes:
            process_id = process.id
            status = process.status
            # Only kill running processes
            if process_id and status == "running":
                try:
                    self.kill_process(process_id)
                    killed_count += 1
                except SandboxError:
                    # Continue killing other processes even if one fails
                    pass
        return killed_count

    def update_lifecycle(
        self,
        delete_after_delay: Optional[int] = None,
        delete_after_inactivity: Optional[int] = None,
    ) -> None:
        """
        Update the sandbox's life cycle settings.

        Args:
            delete_after_delay: If >0, automatically delete the sandbox if there was no activity
                after this many seconds since creation.
            delete_after_inactivity: If >0, automatically delete the sandbox if service sleeps due to inactivity
                after this many seconds.

        Raises:
            SandboxError: If updating life cycle fails

        Example:
            >>> sandbox.update_life_cycle(delete_after_delay=600, delete_after_inactivity=300)
        """
        try:
            clients = get_api_clients(self.api_token, self.host)
            services_api = clients.services
            deployments_api = clients.deployments
            service_response = services_api.get_service(self.service_id)
            service = service_response.service

            deployment_response = deployments_api.get_deployment(
                service.latest_deployment_id
            )
            deployment = deployment_response.deployment

            if not service:
                raise SandboxError("Sandbox service not found")

            # Update life cycle settings
            life_cycle = service.life_cycle or ServiceLifeCycle()
            if delete_after_delay is not None:
                life_cycle.delete_after_create = delete_after_delay
            if delete_after_inactivity is not None:
                life_cycle.delete_after_sleep = delete_after_inactivity

            # Send update request
            services_api.update_service(
                id=self.service_id,
                service=UpdateService(
                    definition=deployment.definition,
                    life_cycle=life_cycle,
                ),
            )
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to update life cycle: {str(e)}") from e

    def __enter__(self) -> "Sandbox":
        """Context manager entry - returns self."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - automatically deletes the sandbox."""
        try:
            # Clean up client if it exists
            if self._client is not None:
                self._client.close()
            self.delete()
        except Exception as e:
            logger.warning(f"Error during sandbox cleanup: {e}")


class AsyncSandbox(Sandbox):
    """
    Async sandbox for running code on Koyeb infrastructure.
    Inherits from Sandbox and provides native async implementations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._async_client = None

    def _get_async_client(self) -> "AsyncSandboxClient":
        """Get or create AsyncSandboxClient instance."""
        if self._async_client is None:
            from .utils import create_async_sandbox_client

            sandbox_url, routing_key = self._get_sandbox_url()
            conn_info = ConnectionInfo(sandbox_url, routing_key, self.sandbox_secret)
            self._async_client = create_async_sandbox_client(conn_info)
        return self._async_client

    @classmethod
    async def get_from_id(
        cls,
        id: str,
        api_token: Optional[str] = None,
        host: Optional[str] = None,
    ) -> "AsyncSandbox":
        """
        Get a sandbox by service ID asynchronously.

        Args:
            id: Service ID of the sandbox
            api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
            host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

        Returns:
            AsyncSandbox: The AsyncSandbox instance

        Raises:
            ValueError: If API token is not provided or id is invalid
            SandboxError: If sandbox is not found or retrieval fails
        """
        if api_token is None:
            api_token = os.getenv("KOYEB_API_TOKEN")
            if not api_token:
                raise ValueError(
                    "API token is required. Set KOYEB_API_TOKEN environment variable or pass api_token parameter"
                )

        if not id:
            raise ValueError("id is required")

        from .utils import get_async_api_clients
        from koyeb.api_async.exceptions import ApiException as AsyncApiException
        from koyeb.api_async.exceptions import NotFoundException as AsyncNotFoundException

        clients = get_async_api_clients(api_token, host)

        try:
            service_response = await clients.services.get_service(id=id)
            service = service_response.service
        except AsyncNotFoundException as e:
            raise SandboxError(f"Sandbox not found with id: {id}") from e
        except AsyncApiException as e:
            raise SandboxError(f"Failed to retrieve sandbox with id: {id}: {e}") from e

        if service is None:
            raise SandboxError(f"Sandbox not found with id: {id}")

        sandbox_name = service.name

        deployment_id = service.active_deployment_id or service.latest_deployment_id
        sandbox_secret = None
        sandbox_metadata = None

        if deployment_id:
            try:
                deployment_response = await clients.deployments.get_deployment(id=deployment_id)
                deployment = deployment_response.deployment
                if deployment and deployment.definition and deployment.definition.env:
                    for env_var in deployment.definition.env:
                        if env_var.key == "SANDBOX_SECRET":
                            sandbox_secret = env_var.value
                            break
                if deployment and deployment.metadata:
                    sandbox_metadata = deployment.metadata
            except Exception as e:
                logger.debug(f"Could not get deployment {deployment_id}: {e}")

        sandbox = cls(
            sandbox_id=service.id,
            app_id=service.app_id,
            service_id=service.id,
            name=sandbox_name,
            api_token=api_token,
            sandbox_secret=sandbox_secret,
            host=host,
        )
        if deployment_id:
            sandbox._deployment_id = deployment_id

        if sandbox_metadata and sandbox_metadata.sandbox:
            sandbox._sandbox_url = (
                f"{sandbox_metadata.sandbox.public_url}/koyeb-sandbox",
                sandbox_metadata.sandbox.routing_key,
            )
        else:
            try:
                app_response = await clients.apps.get_app(service.app_id)
                app = app_response.app
                if hasattr(app, "domains") and app.domains:
                    sandbox._sandbox_url = (
                        f"https://{app.domains[0].name}/koyeb-sandbox",
                        None,
                    )
            except Exception:
                pass

        return sandbox

    @classmethod
    async def create(
        cls,
        image: str = "koyeb/sandbox",
        name: str = "quick-sandbox",
        wait_ready: bool = True,
        instance_type: str = "micro",
        exposed_port_protocol: Optional[str] = None,
        env: Optional[Dict[str, Any]] = None,
        config_files: Optional[Dict[str, Any]] = None,
        region: Optional[str] = None,
        api_token: Optional[str] = None,
        timeout: int = 300,
        idle_timeout: int = 0,
        enable_tcp_proxy: bool = False,
        privileged: bool = False,
        registry_secret: Optional[str] = None,
        _experimental_enable_light_sleep: bool = False,
        _experimental_deep_sleep_value: int = 3900,
        delete_after_delay: int = 0,
        delete_after_inactivity_delay: int = 0,
        app_id: Optional[str] = None,
        enable_mesh: bool = False,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        entrypoint: Optional[List[str]] = None,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        host: Optional[str] = None,
    ) -> AsyncSandbox:
        """
            Create a new sandbox instance with async support.

            Args:
                image: Docker image to use (default: koyeb/sandbox)
                name: Name of the sandbox
                wait_ready: Wait for sandbox to be ready (default: True)
                instance_type: Instance type (default: micro)
                exposed_port_protocol: Protocol to expose ports with ("http" or "http2").
                    If None, defaults to "http".
                    If provided, must be one of "http" or "http2".
                env: Environment variables
                config_files: Config files to create in the sandbox, as a dictionary mapping
                    file paths to file contents. Values can be plain strings (default permissions 0644)
                    or ``ConfigFile`` instances for custom permissions
                    (e.g., {"/etc/myapp/config.yaml": "key: value", "/etc/myapp/cert.pem": ConfigFile(content="...", permissions="0600")})
                region: Region to deploy to. Defaults to KOYEB_REGION env var, or "na" if not set.
                api_token: Koyeb API token (if None, will try to get from KOYEB_API_TOKEN env var)
                timeout: Timeout for sandbox creation in seconds
                idle_timeout: Sleep timeout in seconds. Behavior depends on _experimental_enable_light_sleep:
                    - If _experimental_enable_light_sleep is True: sets light_sleep value (deep_sleep uses _experimental_deep_sleep_value)
                    - If _experimental_enable_light_sleep is False: sets deep_sleep value
                    - If 0: disables scale-to-zero (keep always-on)
                    - If None: uses default values
                enable_tcp_proxy: If True, enables TCP proxy for direct TCP access to port 3031
                privileged: If True, run the container in privileged mode (default: False)
                registry_secret: Name of a Koyeb secret containing registry credentials for
                    pulling private images. Create the secret via Koyeb dashboard or CLI first.
                _experimental_enable_light_sleep: If True, uses idle_timeout for light_sleep and configurable
                    deep_sleep (default: False)
                _experimental_deep_sleep_value: Number of seconds for deep sleep when light sleep is enabled (default: 3900).
                    Only used if _experimental_enable_light_sleep is True
                delete_after_delay: If >0, automatically delete the sandbox if there was no activity
                    after this many seconds since creation.
                delete_after_inactivity_delay: If >0, automatically delete the sandbox if service sleeps due to inactivity
                    after this many seconds.
                app_id: If provided, create the sandbox service in an existing app instead of creating a new one.
                enable_mesh: Enable or disable mesh for this sandbox. Disabled by default
                poll_interval: Time between health checks in seconds when wait_ready is True (default: 0.5)
                entrypoint: Override the default entrypoint of the Docker image (e.g., ["/bin/sh", "-c"])
                command: Override the default command of the Docker image (e.g., "python app.py")
                host: Koyeb API host URL. If not provided, will try to get from KOYEB_API_HOST env var (defaults to https://app.koyeb.com)

        Returns:
                AsyncSandbox: A new AsyncSandbox instance

        Raises:
                ValueError: If API token is not provided
                SandboxTimeoutError: If wait_ready is True and sandbox does not become ready within timeout
        """
        if api_token is None:
            api_token = os.getenv("KOYEB_API_TOKEN")
            if not api_token:
                raise ValueError(
                    "API token is required. Set KOYEB_API_TOKEN environment variable or pass api_token parameter"
                )

        from .utils import get_async_api_clients
        from koyeb.api_async.models.create_app import CreateApp as AsyncCreateApp
        from koyeb.api_async.models.create_app import AppLifeCycle as AsyncAppLifeCycle
        from koyeb.api_async.models.create_service import CreateService as AsyncCreateService
        from koyeb.api_async.models.create_service import ServiceLifeCycle as AsyncServiceLifeCycle

        clients = get_async_api_clients(api_token, host)

        # Always create routes
        routes = create_koyeb_sandbox_routes()

        # Generate secure sandbox secret
        sandbox_secret = secrets.token_urlsafe(32)

        # Add SANDBOX_SECRET to environment variables
        if env is None:
            env = {}
        env["SANDBOX_SECRET"] = sandbox_secret

        # Use provided app_id or create a new app
        if app_id is None:
            app_name = f"sandbox-app-{name}-{int(time.time())}"
            app_response = await clients.apps.create_app(
                app=AsyncCreateApp(
                    name=app_name, life_cycle=AsyncAppLifeCycle(delete_when_empty=True)
                )
            )
            app_id = app_response.app.id

        env_vars = build_env_vars(env)
        config_file_objects = build_config_files(config_files)
        docker_source = create_docker_source(
            image, privileged=privileged, image_registry_secret=registry_secret,
            entrypoint=entrypoint, command=command, args=args,
        )

        deployment_definition = create_deployment_definition(
            name=name,
            docker_source=docker_source,
            env_vars=env_vars,
            instance_type=instance_type,
            exposed_port_protocol=exposed_port_protocol,
            region=region,
            routes=routes,
            idle_timeout=idle_timeout,
            enable_tcp_proxy=enable_tcp_proxy,
            _experimental_enable_light_sleep=_experimental_enable_light_sleep,
            _experimental_deep_sleep_value=_experimental_deep_sleep_value,
            enable_mesh=enable_mesh,
            config_files=config_file_objects if config_file_objects else None,
        )

        service_life_cycle = AsyncServiceLifeCycle(
            delete_after_create=delete_after_delay,
            delete_after_sleep=delete_after_inactivity_delay,
        )
        # Convert sync DeploymentDefinition to dict so the async Pydantic model
        # (which expects koyeb.api_async.models.DeploymentDefinition) can coerce it.
        create_service = AsyncCreateService(
            app_id=app_id,
            definition=deployment_definition.to_dict(),
            life_cycle=service_life_cycle,
        )
        service_response = await clients.services.create_service(service=create_service)
        service_id = service_response.service.id

        sandbox = cls(
            sandbox_id=name,
            app_id=app_id,
            service_id=service_id,
            name=name,
            api_token=api_token,
            sandbox_secret=sandbox_secret,
            poll_interval=poll_interval,
            host=host,
        )

        if wait_ready:
            is_ready = await sandbox.wait_ready(timeout=timeout)
            if not is_ready:
                raise SandboxTimeoutError(
                    f"Sandbox '{sandbox.name}' did not become ready within {timeout} seconds. "
                    f"The sandbox was created but may not be ready yet. "
                    f"You can check its status with sandbox.is_healthy() or call sandbox.wait_ready() again."
                )

        return sandbox

    async def _async_is_deployment_healthy(self) -> bool:
        """Check deployment health via async API."""
        try:
            from .utils import get_async_api_clients

            deployment_id = self._deployment_id
            if not deployment_id:
                # Resolve deployment ID via async API
                clients = get_async_api_clients(self.api_token, self.host)
                service_response = await clients.services.get_service(self.service_id)
                service = service_response.service
                deployment_id = service.active_deployment_id or service.latest_deployment_id
                if deployment_id:
                    self._deployment_id = deployment_id
                else:
                    return False

            clients = get_async_api_clients(self.api_token, self.host)
            deployment_response = await clients.deployments.get_deployment(deployment_id)
            deployment = deployment_response.deployment
            status = deployment.status
            if status in self._DEPLOYMENT_ERROR_STATUSES:
                raise SandboxDeploymentError(
                    f"Sandbox '{self.name}' deployment reached status {status.value}. "
                    f"The sandbox will not become ready."
                )
            is_healthy = status == DeploymentStatus.HEALTHY
            if is_healthy and self._sandbox_url is None:
                metadata = deployment.metadata
                if metadata and metadata.sandbox:
                    self._sandbox_url = (
                        f"{metadata.sandbox.public_url}/koyeb-sandbox",
                        metadata.sandbox.routing_key,
                    )
            return is_healthy
        except SandboxDeploymentError:
            raise
        except Exception as e:
            logger.debug(f"Could not get deployment for service {self.service_id}: {e}")
            return False

    async def _async_check_executor_health(self) -> bool:
        """Check executor health via async client."""
        try:
            client = self._get_async_client()
            health_response = await client.health()
            if isinstance(health_response, dict):
                status = health_response.get("status", "").lower()
                return status in ["ok", "healthy", "ready"]
            return True
        except Exception:
            return False

    async def wait_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: Optional[float] = None,
    ) -> bool:
        """
        Wait for sandbox to become ready with exponential backoff async polling.

        First waits for the deployment status to become HEALTHY, then polls the
        sandbox health endpoint to confirm the executor is responsive.

        Starts polling at 0.1s intervals, doubling each time up to poll_interval.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Maximum time between health checks in seconds (defaults to instance poll_interval)

        Returns:
            bool: True if sandbox became ready, False if timeout
        """
        if poll_interval is None:
            poll_interval = self.poll_interval
        start_time = time.time()
        deployment_healthy = False
        current_interval = 0.1

        while time.time() - start_time < timeout:
            if not deployment_healthy:
                deployment_healthy = await self._async_is_deployment_healthy()
                if not deployment_healthy:
                    await asyncio.sleep(current_interval)
                    current_interval = min(current_interval * 2, poll_interval)
                    continue

            is_healthy = await self._async_check_executor_health()
            if is_healthy:
                return True

            await asyncio.sleep(current_interval)
            current_interval = min(current_interval * 2, poll_interval)

        return False

    async def wait_tcp_proxy_ready(
        self,
        timeout: int = DEFAULT_INSTANCE_WAIT_TIMEOUT,
        poll_interval: Optional[float] = None,
    ) -> bool:
        """
        Wait for TCP proxy to become ready and available asynchronously.

        Polls the deployment metadata with exponential backoff until the TCP proxy
        information is available. Starts at 0.1s intervals, doubling up to poll_interval.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Maximum time between checks in seconds (defaults to instance poll_interval)

        Returns:
            bool: True if TCP proxy became ready, False if timeout
        """
        if poll_interval is None:
            poll_interval = self.poll_interval
        start_time = time.time()
        current_interval = 0.1

        while time.time() - start_time < timeout:
            from .utils import get_async_api_clients
            from koyeb.api_async.api.deployments_api import DeploymentsApi as AsyncDeploymentsApi

            try:
                clients = get_async_api_clients(self.api_token, self.host)
                service_response = await clients.services.get_service(self.service_id)
                service = service_response.service

                if service.active_deployment_id:
                    deployment_response = await clients.deployments.get_deployment(
                        service.active_deployment_id
                    )
                    deployment = deployment_response.deployment

                    if deployment.metadata and deployment.metadata.proxy_ports:
                        for proxy_port in deployment.metadata.proxy_ports:
                            if (
                                proxy_port.port == 3031
                                and proxy_port.host
                                and proxy_port.public_port
                            ):
                                return True
            except Exception:
                pass

            await asyncio.sleep(current_interval)
            current_interval = min(current_interval * 2, poll_interval)

        return False

    async def delete(self) -> None:
        """Delete the sandbox instance asynchronously."""
        from .utils import get_async_api_clients
        clients = get_async_api_clients(self.api_token, self.host)
        await clients.apps.delete_app(self.app_id)

    async def is_healthy(self) -> bool:
        """Check if sandbox is healthy and ready for operations asynchronously."""
        if not await self._async_is_deployment_healthy():
            return False
        return await self._async_check_executor_health()

    @property
    def exec(self) -> "AsyncSandboxExecutor":
        """Get async command execution interface"""
        if self._executor is None:
            from .exec import AsyncSandboxExecutor

            self._executor = AsyncSandboxExecutor(self)
        return self._executor

    @property
    def filesystem(self) -> "AsyncSandboxFilesystem":
        """Get filesystem operations interface"""
        if self._filesystem is None:
            from .filesystem import AsyncSandboxFilesystem

            self._filesystem = AsyncSandboxFilesystem(self)
        return self._filesystem

    async def expose_port(self, port: int) -> ExposedPort:
        """Expose a port to external connections via TCP proxy asynchronously."""
        validate_port(port)
        client = self._get_async_client()
        try:
            try:
                await client.unbind_port()
            except Exception as e:
                logger.debug(f"Error unbinding existing port (this is okay): {e}")

            response = await client.bind_port(port)
            self._check_response_error(response, f"expose port {port}")

            url = self._get_url()
            if not url:
                raise SandboxError("URL not available for exposed port")

            exposed_port = int(response.get("port", port))
            return ExposedPort(port=exposed_port, exposed_at=url)
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to expose port {port}: {str(e)}") from e

    async def unexpose_port(self) -> None:
        """Unexpose a port from external connections asynchronously."""
        client = self._get_async_client()
        try:
            response = await client.unbind_port()
            self._check_response_error(response, "unexpose port")
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to unexpose port: {str(e)}") from e

    async def launch_process(
        self, cmd: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None
    ) -> str:
        """Launch a background process in the sandbox asynchronously."""
        client = self._get_async_client()
        try:
            response = await client.start_process(cmd, cwd, env)
            process_id = response.get("id")
            if process_id:
                return process_id
            error_msg = response.get("error", response.get("message", "Unknown error"))
            raise SandboxError(f"Failed to launch process: {error_msg}")
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to launch process: {str(e)}") from e

    async def kill_process(self, process_id: str) -> None:
        """Kill a background process by its ID asynchronously."""
        client = self._get_async_client()
        try:
            response = await client.kill_process(process_id)
            self._check_response_error(response, f"kill process {process_id}")
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to kill process {process_id}: {str(e)}") from e

    async def list_processes(self) -> List[ProcessInfo]:
        """List all background processes asynchronously."""
        client = self._get_async_client()
        try:
            response = await client.list_processes()
            processes_data = response.get("processes", [])
            return [ProcessInfo(**process) for process in processes_data]
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to list processes: {str(e)}") from e

    async def kill_all_processes(self) -> int:
        """Kill all running background processes asynchronously."""
        processes = await self.list_processes()
        killed_count = 0
        for process in processes:
            process_id = process.id
            status = process.status
            # Only kill running processes
            if process_id and status == "running":
                try:
                    await self.kill_process(process_id)
                    killed_count += 1
                except SandboxError:
                    # Continue killing other processes even if one fails
                    pass
        return killed_count

    async def update_lifecycle(
        self,
        delete_after_delay: Optional[int] = None,
        delete_after_inactivity: Optional[int] = None,
    ) -> None:
        """Update the sandbox's life cycle settings asynchronously."""
        try:
            from .utils import get_async_api_clients
            from koyeb.api_async.models.create_service import ServiceLifeCycle as AsyncServiceLifeCycle
            from koyeb.api_async.models.update_service import UpdateService as AsyncUpdateService

            clients = get_async_api_clients(self.api_token, self.host)
            service_response = await clients.services.get_service(self.service_id)
            service = service_response.service

            if not service:
                raise SandboxError("Sandbox service not found")

            deployment_response = await clients.deployments.get_deployment(
                service.latest_deployment_id
            )
            deployment = deployment_response.deployment

            life_cycle = service.life_cycle or AsyncServiceLifeCycle()
            if delete_after_delay is not None:
                life_cycle.delete_after_create = delete_after_delay
            if delete_after_inactivity is not None:
                life_cycle.delete_after_sleep = delete_after_inactivity

            await clients.services.update_service(
                id=self.service_id,
                service=AsyncUpdateService(
                    definition=deployment.definition,
                    life_cycle=life_cycle,
                ),
            )
        except Exception as e:
            if isinstance(e, SandboxError):
                raise
            raise SandboxError(f"Failed to update life cycle: {str(e)}") from e

    async def __aenter__(self) -> "AsyncSandbox":
        """Async context manager entry - returns self."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit - automatically deletes the sandbox."""
        try:
            # Clean up clients if they exist
            if self._async_client is not None:
                await self._async_client.close()
            if self._client is not None:
                self._client.close()
            await self.delete()
        except Exception as e:
            logger.warning(f"Error during sandbox cleanup: {e}")
