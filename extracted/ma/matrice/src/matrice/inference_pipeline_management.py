"""Module to handle inference pipeline management operations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from matrice_common.utils import handle_response


class InferencePipelineManagement:
    """
    A class for handling inference pipeline management operations using the backend API.

    This includes pipeline creation, control, monitoring, timing, and camera/application management.

    Attributes
    ----------
    session : Session
        The session object used for API interactions.
    account_number : str
        The account number associated with the session.
    rpc : RPC
        The RPC object for making API calls.

    Examples
    --------
    >>> from matrice_common.session import Session
    >>> session = Session(account_number="ACC123", access_key="key", secret_key="secret")
    >>> pipeline_mgmt = InferencePipelineManagement(session)
    >>>
    >>> # Create an inference pipeline
    >>> cameras = [{
    ...     "cameraId": "507f1f77bcf86cd799439016",
    ...     "applications": [{"_idApplication": "507f1f77bcf86cd799439020"}]
    ... }]
    >>> pipeline, error, message = pipeline_mgmt.create_inference_pipeline(
    ...     name="Parking Lot Pipeline",
    ...     project_id="507f1f77bcf86cd799439052",
    ...     cameras=cameras
    ... )
    """

    def __init__(self, session):
        """
        Initialize the InferencePipelineManagement class.

        Parameters
        ----------
        session : Session
            The session object with authentication credentials
        """
        self.session = session
        self.account_number = session.account_number
        self.rpc = session.rpc

    # ==================== Pipeline Management ====================

    def create_inference_pipeline(
        self,
        name: str,
        project_id: str,
        cameras: List[Dict[str, Any]],
        user_id: str,
        description: str = "",
        access_scale: str = "local",
        deploy_type: str = "real_time",
        server_type: str = "fastapi",
        facial_recognition_server_id: str = None,
        lpr_server_id: str = None,
        aggregators: Optional[List[Dict[str, Any]]] = None,
        status: str = "created",
        compute_alias: str = "",
        cluster_name: str = "",
        runtime_framework: str = "Triton",
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a new inference pipeline.

        Parameters
        ----------
        name : str
            Name of the pipeline
        project_id : str
            Project ID
        cameras : list of dict
            List of camera configurations. Each dict should contain:
            - cameraId: str (ID of the camera)
            - applications: list of dict with "_idApplication" and optional "postProcessingConfig"
        user_id : str
            User ID creating the pipeline (required by backend)
        description : str, optional
            Description of the pipeline
        access_scale : str, optional
            Access scale - "local", "regional", "global" (default: "local")
        deploy_type : str, optional
            Deploy type - "real_time", "batch", etc. (default: "real_time")
        server_type : str, optional
            Server type - "fastapi", "kafka", etc. (default: "fastapi")
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications)
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications)
        aggregators : list of dict, optional
            List of aggregator configurations
        status : str, optional
            Initial status (default: "created")
        compute_alias : str, optional
            Compute resource alias
        cluster_name : str, optional
            Cluster name for deployment (e.g., "thor2")
        runtime_framework : str, optional
            Runtime framework (default: "Triton")

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Pipeline details including ID, status, cameras, aggregators
            - str or None: Error message if failed
            - str: Status message

        Examples
        --------
        >>> cameras = [
        ...     {
        ...         "cameraId": "507f1f77bcf86cd799439016",
        ...         "applications": [
        ...             {
        ...                 "_idApplication": "507f1f77bcf86cd799439020",
        ...                 "postProcessingConfig": {
        ...                     "confidence_threshold": 0.75,
        ...                     "nms_threshold": 0.45
        ...                 }
        ...             }
        ...         ]
        ...     }
        ... ]
        >>> pipeline, error, message = pipeline_mgmt.create_inference_pipeline(
        ...     name="Vehicle Detection Pipeline",
        ...     project_id="507f1f77bcf86cd799439052",
        ...     cameras=cameras,
        ...     description="Real-time vehicle detection",
        ...     compute_alias="inference-compute-01"
        ... )
        """
        path = "/v1/inference/inference_pipeline"
        payload = {
            "name": name,
            "_idProject": project_id,
            "cameras": cameras,
            "description": description,
            "accessScale": access_scale,
            "deployType": deploy_type,
            "serverType": server_type,
            "status": status,
            "accountNumber": self.account_number,
            "computeAlias": compute_alias,
        }

        payload["_idUser"] = user_id

        if facial_recognition_server_id:
            payload["_idServerFacialRecognition"] = facial_recognition_server_id
        if lpr_server_id:
            payload["_idLPRServer"] = lpr_server_id
        if aggregators:
            payload["aggregators"] = aggregators
        if cluster_name:
            payload["clusterName"] = cluster_name
        if runtime_framework:
            payload["runtimeFramework"] = runtime_framework

        resp = self.rpc.post(path=path, payload=payload, timeout=300)
        return handle_response(
            resp,
            "Inference pipeline created successfully",
            "Failed to create inference pipeline",
        )

    def get_inference_pipeline_dashboard(
        self, page: int = 1, limit: int = 10
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get inference pipeline dashboard with pagination.

        Parameters
        ----------
        page : int, optional
            Page number (default: 1)
        limit : int, optional
            Items per page (default: 10)

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Dashboard data with pipelines and statistics
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_inference_pipeline_dashboard?page={page}&limit={limit}&account_number={self.account_number}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Inference pipeline dashboard retrieved successfully",
            "Failed to retrieve inference pipeline dashboard",
        )

    def get_inference_pipeline_by_id(self, pipeline_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get a specific inference pipeline by ID.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Pipeline details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_inference_pipeline/{pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Inference pipeline retrieved successfully",
            "Failed to retrieve inference pipeline",
        )

    def list_inference_pipelines(
        self,
        project_id: str,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "",
        sort_order: str = "asc",
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        List all inference pipelines for a project with pagination.

        Parameters
        ----------
        project_id : str
            The project ID
        page : int, optional
            Page number (default: 1)
        limit : int, optional
            Items per page (default: 10)
        sort_by : str, optional
            Field to sort by
        sort_order : str, optional
            Sort order - "asc" or "desc" (default: "asc")

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Paginated pipelines data
            - str or None: Error message if failed
            - str: Status message
        """
        params = {
            "page": page,
            "limit": limit,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        # Remove empty params
        params = {k: v for k, v in params.items() if v}

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        path = f"/v1/inference/list_inference_pipelines/{project_id}?{query_string}"

        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Inference pipelines list retrieved successfully",
            "Failed to retrieve inference pipelines list",
        )

    def get_applications_by_pipeline(self, pipeline_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all applications used in a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of application deployments
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_applications_by_pipeline/{pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Applications retrieved successfully",
            "Failed to retrieve applications for pipeline",
        )

    def get_cameras_by_streaming_gateway(self, pipeline_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get cameras grouped by streaming gateway for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Cameras grouped by streaming gateway
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_cameras_by_streaming_gateway/{pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Cameras by streaming gateway retrieved successfully",
            "Failed to retrieve cameras by streaming gateway",
        )

    def get_cameras_without_streaming_gateway(
        self, pipeline_id: str
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get cameras that don't have a streaming gateway assigned.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of cameras without streaming gateway
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_cameras_without_streaming_gateway/{pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Cameras without gateway retrieved successfully",
            "Failed to retrieve cameras without streaming gateway",
        )

    def start_inference_pipeline(
        self, pipeline_id: str, compute_alias: str = "", cluster_name: str = ""
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Start an inference pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID to start
        compute_alias : str, optional
            Compute resource alias to use
        cluster_name : str, optional
            Cluster name for deployment

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated pipeline with status "starting" or "running"
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/start_inference_pipeline/{pipeline_id}"
        payload = {}
        if compute_alias:
            payload["computeAlias"] = compute_alias
        if cluster_name:
            payload["clusterName"] = cluster_name

        resp = self.rpc.put(path=path, payload=payload, timeout=300)
        return handle_response(
            resp,
            "Inference pipeline started successfully",
            "Failed to start inference pipeline",
        )

    def stop_inference_pipeline(self, pipeline_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Stop an inference pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID to stop

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated pipeline with status "stopped"
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/stop_inference_pipeline/{pipeline_id}"
        resp = self.rpc.put(path=path, payload={})
        return handle_response(
            resp,
            "Inference pipeline stopped successfully",
            "Failed to stop inference pipeline",
        )

    def rename_inference_pipeline(self, pipeline_id: str, name: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Rename an inference pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID
        name : str
            New pipeline name

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated pipeline details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/rename_inference_pipeline/{pipeline_id}"
        payload = {"name": name}

        resp = self.rpc.put(path=path, payload=payload)
        return handle_response(
            resp,
            "Inference pipeline renamed successfully",
            "Failed to rename inference pipeline",
        )

    def update_aggregator_status(
        self,
        pipeline_id: str,
        aggregator_id: str,
        status: str,
        is_running: bool,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update the status of an aggregator in a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID
        aggregator_id : str
            The aggregator ID
        status : str
            New status
        is_running : bool
            Whether the aggregator is running

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated aggregator details
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/update_aggregator_status"
        payload = {
            "_idPipeline": pipeline_id,
            "_idAggregator": aggregator_id,
            "status": status,
            "isRunning": is_running,
        }

        resp = self.rpc.put(path=path, payload=payload)
        return handle_response(
            resp,
            "Aggregator status updated successfully",
            "Failed to update aggregator status",
        )

    def add_cameras_and_applications_to_pipeline(
        self,
        pipeline_id: str,
        cameras: List[Dict[str, Any]],
        compute_alias: str = "",
        cluster_name: str = "",
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Add cameras and applications to an existing pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID
        cameras : list of dict
            List of camera configurations with cameraId and applications
        compute_alias : str, optional
            Compute resource alias
        cluster_name : str, optional
            Cluster name for deployment

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated pipeline details
            - str or None: Error message if failed
            - str: Status message

        Examples
        --------
        >>> cameras = [
        ...     {
        ...         "cameraId": "507f1f77bcf86cd799439017",
        ...         "applications": [
        ...             {
        ...                 "_idApplication": "507f1f77bcf86cd799439023",
        ...                 "postProcessingConfig": {"confidence_threshold": 0.8}
        ...             }
        ...         ]
        ...     }
        ... ]
        >>> result, error, message = pipeline_mgmt.add_cameras_and_applications_to_pipeline(
        ...     pipeline_id="507f1f77bcf86cd799439022",
        ...     cameras=cameras,
        ...     compute_alias="inference-compute-01"
        ... )
        """
        path = "/v1/inference/add_cameras_and_applications_to_pipeline"
        payload: Dict[str, Any] = {
            "_idPipeline": pipeline_id,
            "cameras": cameras,
        }
        if compute_alias:
            payload["computeAlias"] = compute_alias
        if cluster_name:
            payload["clusterName"] = cluster_name

        resp = self.rpc.put(path=path, payload=payload, timeout=300)
        return handle_response(
            resp,
            "Cameras and applications added to pipeline successfully",
            "Failed to add cameras and applications to pipeline",
        )

    def delete_inference_pipeline(self, pipeline_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete an inference pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID to delete

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Deletion confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/delete_inference_pipeline/{pipeline_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Inference pipeline deleted successfully",
            "Failed to delete inference pipeline",
        )

    # ==================== Pipeline Timing Management ====================

    def create_inference_pipeline_timing(
        self,
        pipeline_id: str,
        project_id: str,
        user_id: str,
        run_type: str,
        start_time: str,
        status: str = "active",
        latency: Optional[int] = None,
        step_details: Optional[List[Dict[str, Any]]] = None,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a timing record for a pipeline run.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID
        project_id : str
            The project ID
        user_id : str
            The user ID who initiated the run
        run_type : str
            Type of run (e.g. "manual", "scheduled")
        start_time : str
            ISO 8601 timestamp of when the run started
        status : str, optional
            Status (default: "active")
        latency : int, optional
            Overall latency in nanoseconds
        step_details : list of dict, optional
            List of step timing details, each with:
            - stepName: str
            - stepTime: str (ISO 8601 timestamp)
            - latency: int (nanoseconds, optional)
            - status: str
            - description: str (optional)

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Timing record details
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/inference_pipeline_timing"
        payload: Dict[str, Any] = {
            "_idPipeline": pipeline_id,
            "_idProject": project_id,
            "_idUser": user_id,
            "runType": run_type,
            "status": status,
            "startTime": start_time,
        }

        if latency is not None:
            payload["latency"] = latency
        if step_details is not None:
            payload["stepDetails"] = step_details

        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Pipeline timing created successfully",
            "Failed to create pipeline timing",
        )

    def get_inference_pipeline_timing_by_id(self, timing_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get pipeline timing by timing ID.

        Parameters
        ----------
        timing_id : str
            The timing record ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Timing details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/inference_pipeline_timing/{timing_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Pipeline timing retrieved successfully",
            "Failed to retrieve pipeline timing",
        )

    def get_inference_pipeline_timing_by_pipeline(
        self, pipeline_id: str
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all timing records for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of timing records
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/inference_pipeline_timing_by_pipeline/{pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Pipeline timing records retrieved successfully",
            "Failed to retrieve pipeline timing records",
        )

    def get_latest_active_timing_by_pipeline(self, pipeline_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get the latest active timing record for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Latest active timing details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/inference_pipeline_timing_latest_active/{pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Latest active pipeline timing retrieved successfully",
            "Failed to retrieve latest active pipeline timing",
        )

    def update_inference_pipeline_timing(
        self,
        timing_id: str,
        status: str = None,
        end_time: str = None,
        duration: float = None,
        latency: int = None,
        step_details: Optional[List[Dict[str, Any]]] = None,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update a pipeline timing record.

        Parameters
        ----------
        timing_id : str
            The timing record ID
        status : str, optional
            New status
        end_time : str, optional
            ISO 8601 timestamp of when the run ended
        duration : float, optional
            Total duration in seconds
        latency : int, optional
            Overall latency in nanoseconds
        step_details : list of dict, optional
            Updated step timing details

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated timing details
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/inference_pipeline_timing"
        payload: Dict[str, Any] = {"_id": timing_id}

        if status is not None:
            payload["status"] = status
        if end_time is not None:
            payload["endTime"] = end_time
        if duration is not None:
            payload["duration"] = duration
        if latency is not None:
            payload["latency"] = latency
        if step_details is not None:
            payload["stepDetails"] = step_details

        resp = self.rpc.put(path=path, payload=payload)
        return handle_response(
            resp,
            "Pipeline timing updated successfully",
            "Failed to update pipeline timing",
        )

    def delete_inference_pipeline_timing(self, timing_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a pipeline timing record.

        Parameters
        ----------
        timing_id : str
            The timing record ID to delete

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Deletion confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/inference_pipeline_timing/{timing_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Pipeline timing deleted successfully",
            "Failed to delete pipeline timing",
        )

    # ==================== Pipeline Query Methods ====================

    def get_inference_pipelines_by_account(
        self,
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all inference pipelines for the account.

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of inference pipeline dictionaries
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/get_inference_pipelines_by_account"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Inference pipelines retrieved successfully",
            "Failed to retrieve inference pipelines",
        )

    def get_streaming_gateways_by_pipeline(self, pipeline_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get streaming gateways associated with a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The inference pipeline ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of streaming gateway dictionaries
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_streaming_gateways_by_pipeline/{pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Streaming gateways retrieved successfully",
            "Failed to retrieve streaming gateways for pipeline",
        )

    def get_compute_alias_by_pipeline(self, pipeline_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get compute alias for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The inference pipeline ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Compute alias information
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_compute_alias_by_pipeline/{pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Compute alias retrieved successfully",
            "Failed to retrieve compute alias for pipeline",
        )
