"""Module providing compute functionality."""

from matrice.utils import handle_response
from datetime import datetime
from collections import OrderedDict


class ComputeInstance:
    """
    Represents a single compute instance and allows performing operations on the instance such as update, delete, and refresh.

    Attributes:
        Alias : str
        Status : str
        Price_Hour : float
        Machine_EFF : float
        Service_Provider : str
        Launched_At : str
        Launch_Duration : int
        Shutdown_Threshold : int
        GPU_Type : str
        GPU_Memory : int
        CPU : str
        Cores : int
        Memory_GB : int
        Storage_GB : int
        Storage_Type : str
    """

    def __init__(self, session, alias):
        """
        Initialize the ComputeInstance object by fetching the compute instance details
        from the server based on the provided alias.

        Parameters
        ----------
        session : object
            The session object containing account and RPC information.
        alias : str
            The alias of the compute instance to fetch details for.
        """
        self.session = session
        self.rpc = session.rpc
        self.account_number = session.account_number
        self.alias = alias
        self.last_refresh_time = datetime.now()
        self._fetch_instance_details()

    def _fetch_instance_details(self):
        """
        Internal method to fetch and populate instance details from the server using the alias.

        Raises
        ------
        ValueError
            If the instance details cannot be fetched.
        """
        path = f"/v1/scaling/get_instance_by_alias/{self.account_number}/{self.alias}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            f"Successfully fetched instance details for alias: {self.alias}",
            f"Could not fetch instance details for alias: {self.alias}",
        )
        if error:
            raise ValueError(f"Error fetching instance details: {message}")
        data = data[0]
        self.status = data.get("status")
        self.price_hour = data.get("price")
        self.machine_eff = data.get("machineEfficiency")
        self.service_provider = data.get("serviceProvider")
        self.launched_at = data.get("launchedAt")
        self.launch_duration = data.get("launchDuration")
        self.shutdown_threshold = data.get("shutdownThreshold")
        self.gpu_type = data.get("gpuType")
        self.gpu_memory = data.get("gpuMemory")
        self.cpu = data.get("cpuType")
        self.cpu_cores = data.get("cpuCores")
        self.memory_mb = data.get("memory")
        self.storage_gb = data.get("storageSize")
        self.storage_type = data.get("storage")
        self.lease_type = data.get("leaseType")

    @staticmethod
    def _from_json(data, session):
        """
        Convert JSON data to an instance of ComputeInstance.

        Parameters
        ----------
        data : dict
            JSON data representing a compute instance.
        session : object
            The session object containing account and RPC information.

        Returns
        -------
        ComputeInstance
            A ComputeInstance object initialized with the data.
        """
        return ComputeInstance(
            alias=data.get("alias"),
            session=session,
        )

    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        self.__dict__.copy()
        init_params = {
            "session": self.session,
            "alias": self.alias,
        }
        self.__init__(**init_params)
        self.last_refresh_time = datetime.now()

    def stop(self):
        """
        Stop an on-demand compute instance.

        Returns
        -------
        dict or None
            Server response indicating the result of the stop request, or None if an error occurred.
        """
        path = f"/v1/scaling/stop_account_compute/{self.account_number}/{self.alias}"
        resp = self.rpc.put(path=path)
        data, error, message = handle_response(
            resp,
            f"Successfully stopped on-demand instance: {self.alias}",
            f"An error occurred while stopping the instance: {self.alias}",
        )
        return data if not error else None

    def delete(self):
        """
        Update the compute instance attributes if it is not a dedicated instance.

        Returns
        -------
        dict or None
            Server response indicating the result of the update request, or None if update is not
                allowed or fails.
        """
        if self.lease_type == "dedicated":
            print("delete for dedicated instance is not an allowed operation")
            return
        path = f"/v1/scaling/delete_account_compute/{self.account_number}/{self.alias}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Successfully deleted the given compute",
            "Error deleting the given compute",
        )

    def update(self):
        """
        Static method to update the compute instance attributes.

        Returns
        -------
        dict or None
            Server response indicating the result of the update request, or None if update is not
                allowed or fails.
        """
        if self.lease_type == "dedicated":
            print("Update for dedicated instance is not an allowed operation")
            return
        path = "/v1/scaling/update_account_compute"
        headers = {"Content-Type": "application/json"}
        body = {
            "accountNumber": self.account_number,
            "computeAlias": self.alias,
            "launchDuration": self.launch_duration,
            "shutDownTime": self.shutdown_threshold,
        }
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "Successfully updated the given compute",
            "Error updating the given compute",
        )


class ComputeType:
    """
    Initialize a ComputeType instance with the provided attributes.

    Parameters
    ----------
    session : object
        The session object containing account and RPC information.
    instance_type : str
        The type of compute instance.
    price_hour : float
        Hourly price of the instance.
    service_provider : str
        Service provider offering the instance.
    machine_eff : float
        Efficiency rating of the machine.
    compute_eff : float
        Efficiency rating of the compute.
    gpu_type : str
        Type of GPU in the instance.
    gpu_memory : int
        GPU memory in GB.
    cpu : str
        CPU type in the instance.
    cores : int
        Number of CPU cores.
    memory_mb : int
        Memory size in MB.
    storage_gb : int
        Storage size in GB.
    storage_type : str
        Type of storage in the instance.
    """

    def __init__(
        self,
        session,
        instance_type,
        price_hour,
        service_provider,
        machine_eff,
        compute_eff,
        gpu_type,
        gpu_memory,
        cpu,
        cores,
        memory_mb,
        storage_gb,
        storage_type,
    ):
        self.instance_type = instance_type
        self.price_hour = price_hour
        self.service_provider = service_provider
        self.machine_eff = machine_eff
        self.compute_eff = compute_eff
        self.gpu_type = gpu_type
        self.gpu_memory = gpu_memory
        self.cpu = cpu
        self.cores = cores
        self.memory_mb = memory_mb
        self.storage_gb = storage_gb
        self.storage_type = storage_type
        self.rpc = session.rpc
        self.account_number = session.account_number

    @staticmethod
    def _from_json(data, session):
        """
        Convert JSON data to an instance of ComputeType.

        Parameters
        ----------
        data : dict
            JSON data representing a compute type.
        session : object
            The session object containing account and RPC information.

        Returns
        -------
        ComputeType
            A ComputeType object initialized with the data.
        """
        return ComputeType(
            session=session,
            instance_type=data.get("instanceType"),
            price_hour=data.get("pricePerHour"),
            service_provider=data.get("serviceProvider"),
            machine_eff=data.get("machineEfficiency"),
            compute_eff=data.get("computeEfficiency"),
            gpu_type=data.get("gpu"),
            gpu_memory=data.get("gpuMemory"),
            cpu=data.get("cpu"),
            cores=data.get("cores"),
            memory_mb=data.get("memory"),
            storage_gb=data.get("storageSize"),
            storage_type=data.get("storage"),
        )


def list_instance_types(
    session,
    providers=None,
    gpu_types=None,
    price_range=None,
    page_size=10,
    page_num=0,
):
    """
    List all available compute types on the platform with optional filters.

    Parameters
    ----------
    session : object
        The session object containing account and RPC information.
    providers : list, optional
        List of service providers to filter instances.
    gpu_types : list, optional
        List of GPU types to filter instances.
    price_range : tuple, optional
        A tuple containing min and max price to filter instances by price range.
    page_size : int, optional
        The number of instances to return per page.
    page_num : int, optional
        The page number for pagination.

    Returns
    -------
    dict or None
        Dictionary of `ComputeType` objects indexed by `instanceType`, or None if no data is
            available.
    """
    path = "/v1/scaling/get_all_instances_type"
    params = {
        "page_size": page_size,
        "page_num": page_num,
    }
    if providers:
        params["providers"] = ",".join(providers)
    if gpu_types:
        params["gpu_types"] = ",".join(gpu_types)
    if price_range:
        min_price, max_price = price_range
        params["min_price"] = min_price
        params["max_price"] = max_price
    resp = session.rpc.get(path=path, params=params)
    data = handle_response(
        resp,
        "Instance list fetched successfully",
        "Could not fetch instance list",
    )
    if data:
        return {
            instance["instanceType"]: ComputeType._from_json(instance, session)
            for instance in data[0]
        }
    return None


def list_account_compute(session, status="all"):
    """
    List all compute instances associated with an account, with an optional status filter.

    Parameters
    ----------
    session : object
        The session object containing account and RPC information.
    status : str, optional
        Status filter for instances (e.g., 'all', 'active', 'terminated').

    Returns
    -------
    dict or None
        Dictionary of `ComputeInstance` objects indexed by `alias`, or None if no data is available.
    """
    path = f"/v1/scaling/get_all_account_compute/{session.account_number}"
    resp = session.rpc.get(path=path)
    data = handle_response(
        resp,
        f"Instance list fetched successfully for account: {session.account_number}",
        f"Could not fetch instance list for account: {session.account_number}",
    )
    if data:
        return {
            instance["alias"]: ComputeInstance._from_json(instance, session)
            for instance in data[0]
        }
    return None


def get_compute_status_summary(session, lease_type="on-demand"):
    """
    Get a summary of compute statuses for the current account based on the lease type.

    Parameters
    ----------
    session : object
        The session object containing account and RPC information.
    lease_type : str, optional
        The lease type of computes (e.g., 'dedicated', 'shared'). Default is 'on-demand'.

    Returns
    -------
    OrderedDict
        An ordered dictionary with compute statuses and their counts.
    """
    path = f"/v1/scaling/get_all_account_compute/{session.account_number}/{lease_type}"
    resp = session.rpc.get(path=path)
    data, error, message = handle_response(
        resp,
        "Successfully fetched compute status summary",
        "An error occurred while fetching compute status summary",
    )
    if error:
        return OrderedDict(), error
    compute_status_summary = OrderedDict(data.get("data", {}).get("computeCountByStatus", {}))
    compute_status_summary["total"] = data.get("data", {}).get("total", 0)
    return compute_status_summary, None


def add_on_demand_instance(
    session,
    alias,
    compute_type,
    service_provider,
    launch_duration_hours,
    shutdown_thres_minutes,
):
    """
    Add an on-demand instance.

    Parameters
    ----------
    session : object
        The session object containing account and RPC information.
    alias : str
        Alias for the new compute instance.
    compute_type : str
        Type of compute instance to launch.
    service_provider : str
        Service provider offering the instance.
    launch_duration_hours : int
        Duration in hours for the compute instance.
    shutdown_thres_minutes : int
        Shutdown threshold in minutes for automatic shutdown.

    Returns
    -------
    dict or None
        Server response indicating the result of the add request, or None if an error occurred.
    """
    path = "/v1/scaling/add_account_compute"
    payload = {
        "accountNumber": session.account_number,
        "alias": alias,
        "launchDuration": launch_duration_hours,
        "shutDownTime": shutdown_thres_minutes,
        "serviceProvider": service_provider,
        "instanceType": compute_type,
        "leaseType": "on-demand",
    }
    resp = session.rpc.post(path=path, json=payload)
    data, error, message = handle_response(
        resp,
        "Successfully added on-demand instance",
        "An error occurred while adding on-demand instance",
    )
    return data if not error else None
