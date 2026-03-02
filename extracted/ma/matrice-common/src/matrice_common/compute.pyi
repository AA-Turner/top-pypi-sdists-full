"""Auto-generated stub for module: compute."""
from typing import Any, Dict, List, Optional, Tuple

from .utils import handle_response

# Classes
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

    def __init__(self: Any, session: Any) -> None:
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

class PortRange:
    # Class to represent a port range for instance configuration.

    def __init__(self: Any, from_port: int, to_port: int) -> None: ...

    def to_dict(self: Any) -> Any: ...

