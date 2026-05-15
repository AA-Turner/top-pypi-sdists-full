"""Auto-generated stubs for package: matrice_common."""
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

# Constants
logger: Any = ...  # From rpc
logger: Any = ...  # From session
logger: Any = ...  # From token_auth
ERROR_TYPE_TO_MESSAGE: Dict[Any, Any] = ...  # From utils
LoggingIntegration: None = ...  # From utils
configure_scope: None = ...  # From utils
logger: Any = ...  # From utils
sentry_sdk: None = ...  # From utils

# Functions
# From logging_config
def configure_logging() -> None:
    """
    Configure the root logger from the LOG_LEVEL environment variable.
    
    Call once at application startup. If the root logger already has
    handlers, this is a no-op to avoid duplicate configuration.
    
    Environment
    -----------
    LOG_LEVEL : str, optional
        One of DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is WARNING
        so that debug/info output is silent in production.
    """
    ...

# From session
def create_session(account_number: str, access_key: str, secret_key: str) -> Session:
    """
    Create and initialize a new session with specified credentials.
    
    Parameters
    ----------
    account_number : str
        The account number to associate with the new session.
    access_key : str
        The access key for authentication.
    secret_key : str
        The secret key for authentication.
    
    Returns
    -------
    Session
        An instance of the Session class initialized with the given credentials.
    
    Example
    -------
    >>> session = create_session("9625383462734064921642156", "HREDGFXB6KI0TWH6UZEYR",
    "UY8LP0GQRKLSFPZAW1AUF")
    >>> print(session)
    <Session object at 0x...>
    """
    ...

# From utils
def cacheable(f: Any) -> Any:
    """
    Wraps a function to make its args hashable before caching.
    """
    ...

# From utils
def check_for_duplicate(session: Any, service: str, name: str) -> Tuple[Any, Optional[str], str]:
    """
    Check if an item with the given name already exists for the specified service.
    """
    ...

# From utils
def dependencies_check(package_names: Union[List[str], str]) -> None:
    """
    Check and install required dependencies.
    """
    ...

# From utils
def extract_service_from_path(path: str) -> str:
    """
    Helper: Extracts 'actions' from '/v1/actions/get_kafka_info'.
    """
    ...

# From utils
def generate_error_dedup_key(error_type: str, filename: str, function_name: str, service_name: str) -> str:
    """
    Generate a consistent deduplication key based on error location and type, not message content.
    
        This ensures the same error from the same location is not logged multiple times,
        regardless of slight variations in error messages.
    """
    ...

# From utils
def get_deduplication_config() -> dict:
    """
    Get the current deduplication configuration.
    """
    ...

# From utils
def get_summary(session: Any, project_id: str, service_name: str) -> Tuple[Any, Optional[str]]:
    """
    Fetch a summary of the specified service in the project.
    """
    ...

# From utils
def handle_response(response: Optional[Dict[str, Any]], success_message: str, failure_message: str) -> Tuple[Any, Optional[str], str]:
    """
    Handle API response and return appropriate result.
    """
    ...

# From utils
def hash_error(*parts: Any) -> str:
    """
    Generate a hash for error deduplication.
    """
    ...

# From utils
def log_errors(func: Any = None, default_return: Any = None, raise_exception: Any = False, log_error: Any = True, service_name: str = 'py_common') -> Any:
    """
    Decorator to automatically log exceptions with dynamic path-based service detection.
    """
    ...

# From utils
def process_error_log(error: Any, service_name: str = 'py_common', default_return: Any = None, raise_exception: bool = False, log_error: bool = True) -> Any:
    """
    Enhanced reusable error logging handler.
    Automatically extracts file, function, and parameter info
    from the traceback of a caught exception.
    
    Deduplication Behavior:
    - Errors are deduplicated based on: error_type, filename, function_name, and service_name
    - Deduplication check happens ONCE at the process_error_log level (not in individual logging functions)
    - Deduplication is ALWAYS enforced - if an error was logged before (within TTL), it will not be logged again
    - Deduplication is controlled by environment variables:
        * MATRICE_ERROR_DEDUPLICATION_ENABLED (default: true)
        * MATRICE_ERROR_CACHE_TTL_SECONDS (default: 86400 = 24 hours)
        * MATRICE_ERROR_CACHE_MAX_SIZE (default: 1000)
    - Same errors will be logged again after the TTL expires
    """
    ...

# From utils
def seen_error(hash_str: str) -> bool:
    """
    Check if an error has been seen recently, and update cache.
    
        This function is thread-safe and atomically checks and updates the cache
        to prevent race conditions where multiple threads might log the same error.
    """
    ...

# From utils
def send_error_log(filename: str, function_name: str, error_message: str, traceback_str: Optional[str] = None, additional_info: Optional[dict] = None, error_type: str = ErrorType.INTERNAL, service_name: str = 'py_common', action_id: Optional[str] = None, session_id: Optional[str] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None, sentryIssueLink: Optional[str] = None) -> Any:
    """
    Log error to the backend system, sending to Kafka.
    
        Note: Deduplication is now handled at the process_error_log level.
        This function should only be called after deduplication checks have passed.
    """
    ...

# From utils
def send_sentry_log(filename: str, function_name: str, error_message: str, traceback_str: Optional[str] = None, additional_info: Optional[dict] = None, error_type: str = ErrorType.INTERNAL, service_name: str = 'py_common', action_id: Optional[str] = None, session_id: Optional[str] = None) -> Any:
    """
    Sentry is disabled — this is a no-op stub.
    """
    ...

# Classes
# From compute
class Compute:
    # Class to manage compute instances and clusters.
    #
    #     This class provides methods to create, manage and control compute instances
    #     and clusters through the Matrice.ai backend API.
    #
    #     Parameters
    #     ----------
    #     session : Session
    #         An active session instance with valid authentication
    #
    #     Example
    #     -------
    #     >>> from matrice_common import Session
    #     >>> session = Session(account_number="9625383462734064921642156")
    #     >>> compute = Compute(session)

    def __init__(self: Any, session: Session) -> None:
        """
        Initialize Compute class with an existing session.
        """
        ...

    def add_account_compute(self: Any, alias: str, instance_type: str, service_provider: str, lease_type: str = 'hourly', **kwargs: Any) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Add account compute configuration.
        
        Parameters
        ----------
        alias : str
            Alias for the compute configuration
        instance_type : str
            Type of compute instance
        service_provider : str
            Cloud service provider
        lease_type : str, optional
            Type of lease (default: "hourly")
        **kwargs
            Additional configuration parameters
        
        Returns
        -------
        tuple
            A tuple containing (response_data, error_message)
        
        Example
        -------
        >>> response, error = compute.add_account_compute(
        ...     alias="production-cluster",
        ...     instance_type="g4dn.2xlarge",
        ...     service_provider="aws"
        ... )
        """
        ...

    def add_user_instance(self: Any, instance_id: str, alias: str, instance_type: str, device_type: str, launch_duration: int, shutdown_threshold: int, service_provider: str = '', os: Optional[str] = None, os_version: Optional[str] = None, gpu_type: Optional[str] = None, gpu_count: int = 0, total_gpu_memory: Optional[int] = None, ram: Optional[int] = None, storage: Optional[int] = None, cpu_type: Optional[str] = None, encryption_key: Optional[str] = None, open_ports: Optional[List[Any]] = None, instance_ip: Optional[str] = None) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Register a user instance for compute operations.
        
        Parameters
        ----------
        instance_id : str
            Unique identifier for the compute instance
        alias : str
            Human-readable alias for the instance
        instance_type : str
            Type of the compute instance
        device_type : str
            Type of device (e.g., 'gpu', 'cpu')
        launch_duration : int
            Duration in minutes for instance launch
        shutdown_threshold : int
            Threshold time in minutes before auto-shutdown
        service_provider : str, optional
            Cloud service provider (empty for local instances)
        os : str, optional
            Operating system of the instance
        os_version : str, optional
            Version of the operating system
        gpu_type : str, optional
            Type of GPU if applicable
        gpu_count : int, optional
            Number of GPUs (default: 0)
        total_gpu_memory : int, optional
            Total GPU memory in GB
        ram : int, optional
            RAM size in GB
        storage : int, optional
            Storage size in GB
        cpu_type : str, optional
            Type of CPU
        encryption_key : str, optional
            Encryption key for the instance
        open_ports : List[PortRange], optional
            List of open port ranges
        instance_ip : str, optional
            IP address of the instance
        
        Returns
        -------
        tuple
            A tuple containing (response_data, error_message)
        
        Example
        -------
        >>> response, error = compute.add_user_instance(
        ...     instance_id="i-1234567890abcdef0",
        ...     alias="my-gpu-instance",
        ...     instance_type="g4dn.xlarge",
        ...     device_type="gpu",
        ...     launch_duration=60,
        ...     shutdown_threshold=30,
        ...     service_provider="aws",
        ...     gpu_count=1,
        ...     gpu_type="T4"
        ... )
        >>> if error:
        ...     print(f"Error: {error}")
        >>> else:
        ...     print("Instance registered successfully")
        """
        ...

    def create_compute_cluster(self: Any, cluster_id: str, name: str, description: str = '', region: str = '', public_ip: str = '') -> Tuple[Optional[Dict], Optional[str]]:
        """
        Create a new compute cluster.
        
        Parameters
        ----------
        cluster_id : str
            Unique identifier for the cluster
        name : str
            Name of the cluster
        description : str, optional
            Description of the cluster
        region : str, optional
            Region where the cluster is located
        public_ip : str, optional
            Public IP address of the cluster
        
        Returns
        -------
        tuple
            A tuple containing (response_data, error_message)
        
        Example
        -------
        >>> response, error = compute.create_compute_cluster(
        ...     cluster_id="cluster-001",
        ...     name="Production Cluster",
        ...     description="Main production cluster for ML workloads",
        ...     region="us-west-2"
        ... )
        """
        ...

    def create_port_range(self: Any, from_port: int, to_port: int) -> Any:
        """
        Create a port range object for instance configuration.
        
        Parameters
        ----------
        from_port : int
            Starting port number
        to_port : int
            Ending port number
        
        Returns
        -------
        PortRange
            A port range object
        
        Example
        -------
        >>> port_range = compute.create_port_range(8080, 8090)
        >>> # Use in add_user_instance
        >>> response, error = compute.add_user_instance(
        ...     instance_id="i-123",
        ...     alias="web-server",
        ...     # ... other params ...
        ...     open_ports=[port_range]
        ... )
        """
        ...

    def get_instance_details_by_account(self: Any, alias: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get detailed information about compute instances for the account.
        
        Parameters
        ----------
        alias : str
            Alias of the compute configuration
        
        Returns
        -------
        tuple
            A tuple containing (instance_details, error_message)
        
        Example
        -------
        >>> details, error = compute.get_instance_details_by_account("my-cluster")
        >>> if error:
        ...     print(f"Error: {error}")
        >>> else:
        ...     print(f"Running instances: {details.get('countRunning', 0)}")
        """
        ...

    def list_clusters_by_account(self: Any) -> Tuple[List[Dict], Optional[str]]:
        """
        List all compute clusters for the current account.
        
        Returns
        -------
        tuple
            A tuple containing (list_of_clusters, error_message)
        
        Example
        -------
        >>> clusters, error = compute.list_clusters_by_account()
        >>> if error:
        ...     print(f"Error: {error}")
        >>> else:
        ...     for cluster in clusters:
        ...         print(f"Cluster: {cluster['name']} (ID: {cluster['id']})")
        """
        ...

    def restart_account_compute(self: Any, alias: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Restart account compute instance.
        
        Parameters
        ----------
        alias : str
            Alias of the compute configuration to restart
        
        Returns
        -------
        tuple
            A tuple containing (response_data, error_message)
        
        Example
        -------
        >>> response, error = compute.restart_account_compute("production-cluster")
        """
        ...

    def stop_account_compute(self: Any, alias: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Stop account compute instance.
        
        Parameters
        ----------
        alias : str
            Alias of the compute configuration to stop
        
        Returns
        -------
        tuple
            A tuple containing (response_data, error_message)
        
        Example
        -------
        >>> response, error = compute.stop_account_compute("production-cluster")
        """
        ...


# From compute
class PortRange:
    # Class to represent a port range for instance configuration.

    def __init__(self: Any, from_port: int, to_port: int) -> None: ...

    def to_dict(self: Any) -> Dict[str, int]:
        """
        Return port range as dict with 'from' and 'to' keys.
        """
        ...


# From rpc
class RPC:
    # RPC class for handling backend API requests with token-based authentication.

    def __init__(self: Any, access_key: Optional[str] = None, secret_key: Optional[str] = None, project_id: Optional[str] = None, base_url: Optional[str] = None, max_workers: int = 5) -> None:
        """
        Initialize the RPC client with optional project ID and base URL.
        
                Args:
                    access_key: API access key (or set MATRICE_ACCESS_KEY_ID env var)
                    secret_key: API secret key (or set MATRICE_SECRET_ACCESS_KEY env var)
                    project_id: Optional project ID to include in requests
                    base_url: Optional custom base URL (or set MATRICE_BASE_URL env var)
                    max_workers: Maximum number of workers for background request queue (default: 5)
        """
        ...

    def add_project_id(self: Any, url: str) -> str:
        """
        Add project ID to the URL if present and not already included.
        """
        ...

    async def async_send_request(self: Any, method: str = '', path: str = '', headers: Optional[Any] = None, payload: Optional[Any] = None, files: Optional[Any] = None, data: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
        """
        Send an async HTTP request to the specified endpoint with retry support.
        
                Args:
                    method: HTTP method (GET, POST, PUT, DELETE, etc.)
                    path: API endpoint path (also accepts 'endpoint' as alias)
                    headers: Optional request headers
                    payload: Optional JSON payload
                    files: Optional files to upload
                    data: Optional raw data
                    timeout: Request timeout in seconds (default: 60)
                    raise_exception: Whether to raise exceptions on error (default: True)
                    base_url: Optional custom base URL
                    max_retries: Maximum number of retry attempts on failure (default: 0)
                    retry_delay: Initial delay between retries in seconds (default: 1.0)
                    exponential_backoff: Whether to use exponential backoff for retries (default: True)
                    default_return_value: Value to return on failure when raise_exception=False
        
                Returns:
                    Response data dict
        """
        ...

    def clear_completed_background_requests(self: Any) -> int:
        """
        Clear completed background requests from the queue.
        
                Returns:
                    Number of completed requests that were cleared
        """
        ...

    def delete(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Any], None]] = None, **kwargs: Any) -> Optional[Any]:
        """
        Send a DELETE request to the specified endpoint.
        """
        ...

    async def delete_async(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, **kwargs: Any) -> Any:
        """
        Send an async DELETE request to the specified endpoint.
        """
        ...

    def get(self: Any, path: str = '', params: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Any], None]] = None, **kwargs: Any) -> Optional[Any]:
        """
        Send a GET request to the specified endpoint.
        """
        ...

    async def get_async(self: Any, path: str = '', params: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, **kwargs: Any) -> Any:
        """
        Send an async GET request to the specified endpoint.
        """
        ...

    def get_background_request_count(self: Any) -> Tuple[int, int]:
        """
        Get the count of pending and completed background requests.
        
                Returns:
                    Tuple of (pending_count, completed_count)
        """
        ...

    def post(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, files: Optional[Any] = None, data: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Any], None]] = None, **kwargs: Any) -> Optional[Any]:
        """
        Send a POST request to the specified endpoint.
        """
        ...

    async def post_async(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, files: Optional[Any] = None, data: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, **kwargs: Any) -> Any:
        """
        Send an async POST request to the specified endpoint.
        """
        ...

    def put(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Any], None]] = None, **kwargs: Any) -> Optional[Any]:
        """
        Send a PUT request to the specified endpoint.
        """
        ...

    async def put_async(self: Any, path: str = '', payload: Optional[Any] = None, headers: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, **kwargs: Any) -> Any:
        """
        Send an async PUT request to the specified endpoint.
        """
        ...

    def refresh_token(self: Any) -> None:
        """
        Refresh authentication token with automatic fallback to full re-auth.
        
                Uses a cascading approach:
                1. Check if AuthToken is expired/expiring soon (5 min buffer)
                2. Try normal AuthToken refresh via RefreshToken
                3. If that fails, fall back to complete re-authentication from credentials
        
                Thread-safe: Uses _token_lock to prevent concurrent refresh attempts.
                Never raises exceptions - logs errors and attempts recovery silently.
        """
        ...

    def send_request(self: Any, method: str = '', path: str = '', headers: Optional[Dict[str, str]] = None, payload: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None, data: Optional[Any] = None, timeout: int = 120, raise_exception: bool = True, base_url: Optional[str] = None, max_retries: int = 0, retry_delay: float = 1.0, exponential_backoff: bool = True, default_return_value: Optional[Any] = None, background: bool = False, on_complete: Optional[Callable[[Dict[str, Any]], None]] = None, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Send an HTTP request to the specified endpoint with retry and background execution support.
        
                Args:
                    method: HTTP method (GET, POST, PUT, DELETE, etc.)
                    path: API endpoint path (also accepts 'endpoint' as alias)
                    headers: Optional request headers
                    payload: Optional JSON payload
                    files: Optional files to upload
                    data: Optional raw data
                    timeout: Request timeout in seconds (default: 60)
                    raise_exception: Whether to raise exceptions on error (default: True)
                    base_url: Optional custom base URL
                    max_retries: Maximum number of retry attempts on failure (default: 0)
                    retry_delay: Initial delay between retries in seconds (default: 1.0)
                    exponential_backoff: Whether to use exponential backoff for retries (default: True)
                    default_return_value: Value to return on failure when raise_exception=False
                    background: Execute request in background without blocking (default: False)
                    on_complete: Optional callback function to call with the result when background=True
        
                Returns:
                    Response data dict, or None if background=True
        """
        ...

    def shutdown(self: Any, wait: bool = True, timeout: Optional[float] = None) -> None:
        """
        Shutdown the RPC client and cleanup resources.
        
                Args:
                    wait: Whether to wait for all background requests to complete before shutdown
                    timeout: Optional timeout in seconds when waiting for requests (only used if wait=True)
        """
        ...

    def wait_for_background_requests(self: Any, timeout: Optional[float] = None) -> int:
        """
        Wait for all background requests to complete.
        
                Args:
                    timeout: Optional timeout in seconds to wait for all requests to complete.
                            If None, waits indefinitely.
        
                Returns:
                    Number of requests that completed successfully
        """
        ...


# From session
class Session:
    # Class to manage sessions.
    #
    #     Initialize a new session instance.
    #
    #     Parameters
    #     ----------
    #     account_number : str
    #         The account number associated with the session.
    #     project_id : str, optional
    #         The ID of the project for this session.
    #     Example
    #     -------
    #     >>> session = Session(account_number="9625383462734064921642156")

    def __init__(self: Any, account_number: str, access_key: Optional[str] = None, secret_key: Optional[str] = None, project_id: Optional[str] = None, project_name: Optional[str] = None) -> None: ...

    def close(self: Any) -> None:
        """
        Close the current session by resetting the RPC and project details.
        
        Example
        -------
        >>> session.close()
        """
        ...

    def create_classification_project(self: Any, project_name: str, industries: Optional[List[str]] = None, tags: Optional[List[str]] = None, computeType: str = 'matrice', storageType: str = 'matrice', supportedDevices: str = 'nvidia_gpu', deploymentSupportedDevices: str = 'nvidia_gpu') -> Optional[Dict[str, Any]]:
        """
        Create a classification project.
        
        Parameters
        ----------
        project_name : str
            The name of the classification project to be created.
        
        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.
        
        Example
        -------
        >>> project = session.create_classification_project("Image Classification Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        ...

    def create_detection_project(self: Any, project_name: str) -> Optional[Dict[str, Any]]:
        """
        Create a detection project.
        
        Parameters
        ----------
        project_name : str
            The name of the detection project to be created.
        
        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.
        
        Example
        -------
        >>> project = session.create_detection_project("Object Detection Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        ...

    def create_segmentation_project(self: Any, project_name: str) -> Optional[Dict[str, Any]]:
        """
        Create a segmentation project.
        
        Parameters
        ----------
        project_name : str
            The name of the segmentation project to be created.
        
        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.
        
        Example
        -------
        >>> project = session.create_segmentation_project("Instance Segmentation Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        ...

    def get_project_type_summary(self: Any) -> Tuple[Dict[str, Any], Optional[str]]:
        """
        Get the count of different types of projects.
        
        Returns
        -------
        tuple
            A tuple containing:
            - A dictionary with project types as keys and their counts as values if the request is
                successful.
            - An error message if the request fails.
        
        Example
        -------
        >>> project_summary, error = session.get_project_type_summary()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Project type summary: {project_summary}")
        """
        ...

    def list_projects(self: Any, project_type: str = '', page_size: int = 10, page_number: int = 0) -> Tuple[List[Any], str]:
        """
        List projects based on the specified type.
        
        Parameters
        ----------
        project_type : str, optional
            The type of projects to list (e.g., 'classification', 'detection'). If empty,
            all projects are listed.
        
        Returns
        -------
        tuple
            A tuple containing the dictionary of projects and a message indicating the result of
                the fetch operation.
        
        Example
        -------
        >>> projects, message = session.list_projects("classification")
        >>> print(message)
        Projects fetched successfully
        >>> for project_name, project_instance in projects.items():
        >>>     print(project_name, project_instance)
        """
        ...

    def refresh(self: Any) -> None:
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        ...

    def update(self: Any, project_id: Optional[str]) -> None:
        """
        Update the session with new project details.
        
        Parameters
        ----------
        project_id : str, optional
            The new ID of the project.
        
        
        Example
        -------
        >>> session.update(project_id="660b96fc019dd5321fd4f8c7")
        """
        ...


# From token_auth
class AuthToken:
    # Implements a custom authentication scheme.

    def __init__(self: Any, access_key: Any, secret_key: Any, refresh_token: Any) -> None: ...

    def is_expired(self: Any, buffer_seconds: int = 300) -> bool:
        """
        Check if token is expired or will expire within buffer_seconds.
        
                Args:
                    buffer_seconds: Number of seconds before actual expiry to consider token expired.
                                  Default is 300 (5 minutes) to allow proactive refresh.
        
                Returns:
                    True if token is None, has no expiry, or will expire within buffer_seconds.
        """
        ...

    def reset_and_refresh(self: Any) -> Any:
        """
        Reset token state and attempt to refresh.
        
                This method is used for in-place token updates to avoid
                creating new token objects that would leave concurrent threads
                with stale references.
        """
        ...

    def set_bearer_token(self: Any) -> None:
        """
        Obtain an authentication bearer token using the provided refresh token.
        
                Thread-safe: Uses a lock to prevent concurrent refresh attempts.
                On failure, resets bearer_token to None to ensure stale tokens aren't used.
        """
        ...


# From token_auth
class RefreshToken:
    # Implements a custom authentication scheme.

    def __init__(self: Any, access_key: str, secret_key: str) -> None: ...

    def is_expired(self: Any, buffer_seconds: int = 300) -> bool:
        """
        Check if token is expired or will expire within buffer_seconds.
        
                Args:
                    buffer_seconds: Number of seconds before actual expiry to consider token expired.
                                  Default is 300 (5 minutes) to allow proactive refresh.
        
                Returns:
                    True if token is None, has no expiry, or will expire within buffer_seconds.
        """
        ...

    def reset_and_refresh(self: Any) -> Any:
        """
        Reset token state and attempt to refresh.
        
                This method is used for in-place token updates to avoid
                creating new token objects that would leave concurrent threads
                with stale references.
        """
        ...

    def set_bearer_token(self: Any) -> None:
        """
        Obtain a bearer token using the provided access key and secret key.
        
                Thread-safe: Uses a lock to prevent concurrent refresh attempts.
                On failure, resets bearer_token to None to ensure stale tokens aren't used.
        """
        ...


# From utils
class AppError(Exception):
    def __init__(self: Any, error_type: str, error: Any, service_name: str, details: Optional[List[Any]] = None, action_id: Optional[str] = None, session_id: Optional[str] = None) -> None: ...

    def append(self: Any, *details: Any) -> 'Any': ...

    def generate_hash(self: Any) -> str: ...


# From utils
class BenchmarkMetrics:
    # Accumulates per-stage timing samples with zero overhead when disabled.
    #
    #     When enabled=False, all methods return immediately with no allocations.
    #     When enabled=True, tracks sum/count/min/max/samples per named stage.
    #
    #     Usage::
    #
    #         bm = BenchmarkMetrics(enabled=True)
    #         t = bm.start()
    #         # ... do work ...
    #         bm.record("stage_name", t)
    #
    #         # Periodic reporting:
    #         print(bm.get_breakdown_str("My Title", interval_seconds=5.0, total_items=100))
    #         bm.reset()

    def __init__(self: Any, enabled: bool = False) -> None: ...

    def get_breakdown_str(self: Any, title: str = 'BENCHMARK METRICS', interval_seconds: float = 0.0, total_items: int = 0, item_label: str = 'frames') -> str:
        """
        Format a multi-line log string with per-stage breakdown.
        
                Args:
                    title: Header line for the metrics block.
                    interval_seconds: Wall-clock seconds for the reporting interval.
                        Used to compute throughput (items/sec) per stage.
                    total_items: Total items processed in the interval (e.g. frames, batches).
                    item_label: Label for the items (e.g. "frames", "batches").
        """
        ...

    def record(self: Any, stage_name: str, start_time: float) -> float:
        """
        Record elapsed time since start_time for the named stage.
                Returns elapsed seconds. No-op if disabled.
        """
        ...

    def record_value(self: Any, stage_name: str, value_seconds: float) -> Any:
        """
        Record a pre-computed value in seconds.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset all accumulators for the next reporting interval.
        """
        ...

    def start(self: Any) -> float:
        """
        Return current time if enabled, else 0.0.
        """
        ...


# From utils
class ErrorLog:
    def __init__(self: Any, service_name: str, stack_trace: str, error_type: str, description: str, file_name: str, function_name: str, hash: str, action_record_id: Optional[str] = None, created_at: Optional[Any] = None, is_resolved: bool = False, more_info: Optional[Any] = None, sentryIssueLink: Optional[str] = None) -> None: ...

    def to_dict(self: Any) -> dict: ...


# From utils
class ErrorType:
    # Constants for error type classification in error logging.

    INTERNAL: object = ...

# From utils
class SentryConfig:
    # Configuration for Sentry error reporting.

    def __init__(self: Any, dsn: str, environment: str = 'dev', sample_rate: float = 1.0, debug: bool = False, service_name: str = 'py_common', enable_tracing: bool = True) -> None: ...


from . import compute, logging_config, rpc, session, token_auth, utils

def __getattr__(name: str) -> Any: ...