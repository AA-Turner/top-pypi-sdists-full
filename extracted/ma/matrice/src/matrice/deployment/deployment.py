"""Module providing deployment functionality."""

import sys
import time
import json
from matrice.utils import (
    handle_response,
    get_summary,
)
from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Dict

# Import camera and streaming gateway managers and instances
from .camera_manager import (
    CameraManager, 
    CameraGroupConfig, 
    CameraConfig,
    Camera,
    CameraGroup
)
from .streaming_gateway_manager import (
    StreamingGatewayManager,
    StreamingGatewayConfig,
    StreamingGateway
)


class Deployment:
    """
    Class to manage deployment-related operations within a project.

    The `Deployment` class initializes with a given session and deployment details,
    allowing users to access and manage the deployment attributes such as status,
    configuration, and associated project information.

    Parameters
    ----------
    session : object
        The session object containing project and RPC information.
    deployment_id : str, optional
        The ID of the deployment to manage. Default is None.
    deployment_name : str, optional
        The name of the deployment. Default is None.

    Attributes
    ----------
    session : object
        The session object for RPC communication.
    rpc : object
        The RPC interface for backend API communication.
    project_id : str
        The project ID associated with the deployment.
    deployment_id : str
        The unique ID of the deployment.
    deployment_name : str
        Name of the deployment.
    model_id : str
        ID of the model associated with the deployment.
    user_id : str
        User ID of the deployment owner.
    user_name : str
        Username of the deployment owner.
    action_id : str
        ID of the action associated with the deployment.
    auth_keys : list
        List of authorization keys for the deployment.
    runtime_framework : str
        Framework used for the runtime of the model in the deployment.
    model_input : dict
        Input format expected by the model.
    model_type : str
        Type of model deployed (e.g., classification, detection).
    model_output : dict
        Output format of the deployed model.
    deployment_type : str
        Type of deployment (e.g., real-time, batch).
    suggested_classes : list
        Suggested classes for classification models.
    running_instances : list
        List of currently running instances.
    auto_shutdown : bool
        Whether the deployment has auto-shutdown enabled.
    auto_scale : bool
        Whether the deployment is configured for auto-scaling.
    gpu_required : bool
        Whether GPU is required for the deployment.
    status : str
        Current status of the deployment.
    hibernation_threshold : int
        Threshold for auto-hibernation in minutes.
    image_store_confidence_threshold : float
        Confidence threshold for storing images.
    image_store_count_threshold : int
        Count threshold for storing images.
    images_stored_count : int
        Number of images currently stored.
    bucket_alias : str
        Alias for the storage bucket associated with the deployment.
    credential_alias : str
        Alias for credentials used in the deployment.
    created_at : str
        Timestamp when the deployment was created.
    updated_at : str
        Timestamp when the deployment was last updated.
    compute_alias : str
        Alias of the compute resource associated with the deployment.
    is_optimized : bool
        Indicates whether the deployment is optimized.
    status_cards : list
        List of status cards related to the deployment.
    total_deployments : int or None
        Total number of deployments in the project.
    active_deployments : int or None
        Number of active deployments in the project.
    total_running_instances_count : int or None
        Total count of running instances in the project.
    hibernated_deployments : int or None
        Number of hibernated deployments.
    error_deployments : int or None
        Number of deployments with errors.
    camera_manager : CameraManager
        Manager for camera groups and configurations.
    streaming_gateway_manager : StreamingGatewayManager
        Manager for streaming gateways.

    Example
    -------
    >>> session = Session(account_number="account_number")
    >>> deployment = Deployment(session=session, deployment_id="deployment_id", deployment_name="MyDeployment")
    """

    def __init__(
        self,
        session,
        deployment_id=None,
        deployment_name=None,
    ):
        if not (deployment_id or deployment_name):
            raise ValueError("Either deployment_id or deployment_name must be provided")
        self.session = session
        self.project_id = session.project_id
        self.last_refresh_time = datetime.now()
        self.deployment_id = deployment_id
        self.deployment_name = deployment_name
        self.session = session
        self.rpc = session.rpc
        
        self.details, err, message = self._get_details()
        self.deployment_id = self.details.get("_id")
        self.deployment_name = self.details.get("deploymentName")
        self.project_id = self.details.get("_idProject")
        self.model_id = self.details.get("_idModel")
        self.user_id = self.details.get("_idUser")
        self.user_name = self.details.get("userName")
        self.action_id = self.details.get("_idAction")
        self.auth_keys = self.details.get("authKeys", [])
        self.runtime_framework = self.details.get("runtimeFramework")
        self.model_input = self.details.get("modelInput")
        self.model_type = self.details.get("modelType")
        self.model_output = self.details.get("modelOutput")
        self.deployment_type = self.details.get("deploymentType")
        self.suggested_classes = self.details.get("suggestedClasses", [])
        self.running_instances = self.details.get("runningInstances", [])
        self.auto_shutdown = self.details.get("autoShutdown")
        self.auto_scale = self.details.get("autoScale")
        self.gpu_required = self.details.get("gpuRequired")
        self.status = self.details.get("status")
        self.hibernation_threshold = self.details.get("shutdownThreshold")
        self.image_store_confidence_threshold = self.details.get("imageStoreConfidenceThreshold")
        self.image_store_count_threshold = self.details.get("imageStoreCountThreshold")
        self.images_stored_count = self.details.get("imagesStoredCount")
        self.bucket_alias = self.details.get("bucketAlias")
        self.credential_alias = self.details.get("credentialAlias")
        self.created_at = self.details.get("createdAt")
        self.updated_at = self.details.get("updatedAt")
        self.compute_alias = self.details.get("computeAlias")
        self.is_optimized = self.details.get("isOptimized")
        self.auth_key = ""
        self.status_cards = self._get_deployment_status_cards()
        summary_response, err, message = get_summary(
            self.session,
            self.project_id,
            "deployments",
        )
        if summary_response:
            summary_data = summary_response
            self.total_deployments = summary_data.get("TotalDeployments")
            self.active_deployments = summary_data.get("ActiveDeployments")
            self.total_running_instances_count = summary_data.get("TotalRunningInstancesCount")
            self.hibernated_deployments = summary_data.get("hibernatedDeployments")
            self.error_deployments = summary_data.get("errorDeployments")
        else:
            self.total_deployments = None
            self.active_deployments = None
            self.total_running_instances_count = None
            self.hibernated_deployments = None
            self.error_deployments = None
        
        self.camera_manager = CameraManager(self.session, service_id=self.deployment_id)
        self.streaming_gateway_manager = StreamingGatewayManager(self.session, service_id=self.deployment_id)

    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise Exception("Refresh can only be called after two minutes since the last refresh.")
        init_params = {
            "session": self.session,
            "deployment_id": self.deployment_id,
            "deployment_name": self.deployment_name,
        }
        self.__init__(**init_params)
        self.last_refresh_time = datetime.now()

    def _get_details(self):
        """
        Fetch deployment details using either the deployment ID or deployment name.

        This method attempts to retrieve deployment details by `deployment_id` if it is set.
        If `deployment_id` is not available, it uses `deployment_name`. If neither identifier
        is provided, a `ValueError` is raised.

        Returns
        -------
        dict
            A dictionary containing the deployment details, including keys such as:
                - `_id` (str): Unique identifier for the deployment.
                - `deploymentName` (str): Name of the deployment.
                - `_idProject` (str): Project ID associated with the deployment.
                - `_idModel` (str): Model ID used in the deployment.
                - `status` (str): Current status of the deployment.

        Raises
        ------
        ValueError
            If neither `deployment_id` nor `deployment_name` is provided.

        Example
        -------
        >>> from pprint import pprint
        >>> deployment_details = deployment._get_details()
        >>> if isinstance(deployment_details, dict):
        >>>     pprint(deployment_details)
        >>> else:
        >>>     print("Failed to retrieve deployment details.")
        """
        id = self.deployment_id
        name = self.deployment_name
        if id:
            try:
                return self._get_deployment_by_id()
            except Exception as e:
                print(f"Error retrieving deployment by id: {e}")
        elif name:
            try:
                return self._get_deployment_by_name()
            except Exception as e:
                print(f"Error retrieving deployment by name: {e}")
        else:
            raise ValueError(
                "At least one of 'deployment_id' or 'deployment_name' must be provided."
            )

    def _get_deployment_by_id(self):
        """
        Fetch details of the specified deployment using its deployment ID.

        This method retrieves the deployment details directly from the backend API based on
        the deployment ID set in the instance.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The raw response from the API with deployment details.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Examples
        --------
        >>> from pprint import pprint
        >>> deployment = Deployment(session, deployment_id="1234")
        >>> details, error, status = deployment._get_deployment_by_id()
        >>> if error:
        >>>     pprint(error)
        >>> else:
        >>>     pprint(details)
        """
        path = f"/v1/inference/{self.deployment_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Deployment fetched successfully",
            "An error occurred while trying to fetch deployment.",
        )

    def _get_deployment_by_name(self):
        """
        Fetch deployment details using the deployment name.

        This method retrieves deployment details from the backend API based on
        the deployment name set in the instance.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The raw response from the API with deployment details.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Raises
        ------
        SystemExit
            If `deployment_name` is not set.

        Examples
        --------
        >>> details, err, msg = deployment._get_deployment_by_name()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(details)
        """
        if self.deployment_name == "":
            print(
                "Deployment name not set for this Deployment. Cannot perform the operation for Deployment without deployment name"
            )
            sys.exit(0)
        path = f"/v1/inference/get_deployment_by_name?deploymentName={self.deployment_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Deployment by name fetched successfully",
            "Could not fetch Deployment by name",
        )

    def rename(self, updated_name):
        """
        Update the deployment name for the current deployment.

        Parameters
        ----------
        updated_name : str
            The new name for the deployment.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with details of the rename operation.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Raises
        ------
        SystemExit
            If `deployment_id` is not set.

        Examples
        --------
        >>> from pprint import pprint
        >>> deployment = Deployment(session, deployment_id="1234")
        >>> rename, err, msg = deployment.rename("NewDeploymentName")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(rename)
        """
        if self.deployment_id is None:
            print("Deployment id not set for this model.")
            sys.exit(0)
        body = {"deploymentName": updated_name}
        headers = {"Content-Type": "application/json"}
        path = f"/v1/inference/update_deployment_name/{self.deployment_id}"
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            f"Deployment name updated to {updated_name}",
            "Could not update the deployment name",
        )

    def delete(self):
        """
        Delete the specified deployment.

        This method deletes the deployment identified by `deployment_id` from the backend system.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response confirming the deletion.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Raises
        ------
        SystemExit
            If `deployment_id` is not set.

        Examples
        --------
        >>> delete, err, msg = deployment.delete()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(delete)
        """
        path = f"/v1/inference/delete_deployment/{self.deployment_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Deployment deleted successfully.",
            "An error occurred while trying to delete the deployment.",
        )

    def get_deployment_server(self, model_train_id, model_type):
        """
        Fetch information about the deployment server for a specific model.

        Parameters
        ----------
        model_train_id : str
            The ID of the model training instance.
        model_type : str
            The type of model (e.g., 'trained', 'exported').

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with details of the deployment server.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Examples
        --------
        >>> deployment_server, err, msg = deployment.get_deployment_server("train123", "trained")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(deployment_server)
        """
        path = f"/v1/inference/get_deploy_server/{model_train_id}/{model_type}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Deployment server fetched successfully",
            "An error occurred while trying to fetch deployment server.",
        )

    def wakeup_deployment_server(self):
        """
        Wake up the deployment server associated with the current deployment.
        The `deployment_id` must be set during initialization.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with details of the wake-up operation.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Raises
        ------
        SystemExit
            If `deployment_id` is not set.

        Examples
        --------
        >>> wakeup, err, msg = deployment.wakeup_deployment_server()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(wakeup)
        """
        path = f"/v1/inference/wake_up_deploy_server/{self.deployment_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Deployment server has been successfully awakened",
            "An error occurred while attempting to wake up the deployment server.",
        )

    def _get_deployment_status_cards(self):
        """
        Fetch status cards for the deployments within the current project.
        The `project_id` must be set during initialization.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with deployment status card details.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Examples
        --------
        >>> status, err, msg = deployment._get_deployment_status_cards()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(status)
        """
        path = f"/v1/inference/status_cards?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Deployment status cards fetched successfully.",
            "An error occurred while trying to fetch deployment status cards.",
        )

    def create_auth_key(self, expiry_days):
        """
        Create a new authentication key for the deployment, valid for the specified number of days.
        The `deployment_id` and `project_id` must be set during initialization.

        Parameters
        ----------
        expiry_days : int
            The number of days before the authentication key expires.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with details of the created authentication key,
            including keys such as:
                - `authKey` (str): The newly created authentication key.
                - `expiryDate` (str): Expiration date of the key.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Examples
        --------
        >>> auth_key, err, msg = deployment.create_auth_key(30)
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(auth_key)
        """
        body = {
            "expiryDays": expiry_days,
            "authType": "external",
        }
        headers = {"Content-Type": "application/json"}
        path = f"/v1/inference/add_auth_key/{self.deployment_id}?projectId={self.project_id}"
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "Auth Key created successfully.",
            "An error occurred while trying to create auth key.",
        )

    def delete_auth_key(self, auth_key):
        """
        Delete a specified authentication key for the current deployment.
        The `deployment_id` must be set during initialization.

        Parameters
        ----------
        auth_key : str
            The authentication key to be deleted.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response indicating the result of the delete operation.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Raises
        ------
        SystemExit
            If `deployment_id` is not set.

        Examples
        --------
        >>> delete_auth_key, err, msg = deployment.delete_auth_key("abcd1234")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(delete_auth_key)
        """
        if self.deployment_id is None:
            print("Deployment id not set for this deployment.")
            sys.exit(0)
        path = f"/v1/inference/delete_auth_key/{self.deployment_id}/{auth_key}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Auth key deleted successfully.",
            "An error occurred while trying to delete the auth key.",
        )

    def request_total_monitor(self):
        """
        Monitor the total number of requests for the current deployment.

        This method checks the total request count for a deployment by its `deployment_id`.
        If `deployment_id` is not set, it attempts to fetch it using `deployment_name`.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with the total request count.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Raises
        ------
        SystemExit
            If both `deployment_id` and `deployment_name` are not set.

        Examples
        --------
        >>> from pprint import pprint
        >>> monitor, error, message = deployment.request_total_monitor()
        >>> if error:
        >>>     pprint(error)
        >>> else:
        >>>     pprint(monitor)
        """
        if self.deployment_id:
            deployment_id_url = self.deployment_id
        elif self.deployment_name:
            _, error, _ = self._get_deployment_by_name()
            if error:
                return (
                    None,
                    error,
                    "Failed to fetch deployment ID using the deployment name.",
                )
            deployment_id_url = self.deployment_id
        else:
            return (
                None,
                "Deployment ID and name are not set.",
                "Cannot perform operation without a deployment ID or name.",
            )
        path = f"/v1/model_prediction/monitor/req_total/{deployment_id_url}?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "Request total monitored successfully",
            "An error occurred while monitoring the request total.",
        )

    def request_count_monitor(
        self,
        start_date,
        end_date,
        granularity="second",
    ):
        """
        Monitor the count of requests within a specified time range and granularity for the current
            deployment.

        Parameters
        ----------
        start_date : str
            The start date of the monitoring period in ISO format (e.g., "YYYY-MM-DDTHH:MM:SSZ").
        end_date : str
            The end date of the monitoring period in ISO format.
        granularity : str, optional
            The time granularity for the request count (e.g., "second", "minute")
            . Default is "second".

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with the request count details, structured as:
                - `counts` (list of dict): Each entry contains:
                    - `timestamp` (str): The timestamp of the request count.
                    - `count` (int): The number of requests at that timestamp.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Examples
        --------
        >>> start = "2024-01-28T18:30:00.000Z"
        >>> end = "2024-02-29T10:11:27.000Z"
        >>> count_monitor, error, message = deployment.request_count_monitor(start, end)
        >>> if error:
        >>>     pprint(error)
        >>> else:
        >>>     pprint(count_monitor)
        """
        path = "/v1/model_prediction/monitor/request_count"
        headers = {"Content-Type": "application/json"}
        body = {
            "granularity": granularity,
            "startDate": start_date,
            "endDate": end_date,
            "status": "REQ. COUNT",
            "deploymentId": self.deployment_id,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "Request count monitored successfully",
            "An error occurred while monitoring the request count.",
        )

    def request_latency_monitor(
        self,
        start_date,
        end_date,
        granularity="second",
    ):
        """
        Monitor the request latency within a specified time range and granularity for the current
            deployment.

        Parameters
        ----------
        start_date : str
            The start date of the monitoring period in ISO format (e.g., "YYYY-MM-DDTHH:MM:SSZ").
        end_date : str
            The end date of the monitoring period in ISO format.
        granularity : str, optional
            The time granularity for latency tracking (e.g., "second", "minute"). Default is
                "second".

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with latency details, structured as:
                - `latencies` (list of dict): Each entry contains:
                    - `timestamp` (str): The timestamp of the latency record.
                    - `avg_latency` (float): The average latency in seconds for the requests at
                        that timestamp.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Examples
        --------
        >>> from pprint import pprint
        >>> start = "2024-01-28T18:30:00.000Z"
        >>> end = "2024-02-29T10:11:27.000Z"
        >>> result, error, message = deployment.request_latency_monitor(start, end)
        >>> if error:
        >>>     pprint(error)
        >>> else:
        >>>     pprint(result)
        """
        path = "/v1/model_prediction/monitor/latency"
        headers = {"Content-Type": "application/json"}
        body = {
            "granularity": granularity,
            "startDate": start_date,
            "endDate": end_date,
            "status": "AVG. LATENCY",
            "deploymentId": self.deployment_id,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "Latency count monitored successfully",
            "An error occurred while monitoring the latency count.",
        )

    def create_dataset(
        self,
        dataset_name,
        is_unlabeled,
        source,
        source_url,
        is_public,
        dataset_description="",
        version_description="",
    ):
        """
        Create a new dataset from a deployment. Only zip files are supported for upload,
        and the deployment ID must be set for this operation.

        Parameters
        ----------
        dataset_name : str
            The name of the new dataset.
        is_unlabeled : bool
            Indicates whether the dataset is unlabeled.
        source : str
            The source of the dataset (e.g., "aws").
        source_url : str
            The URL of the dataset to be created.
        is_public : bool
            Specifies if the dataset is public.
        dataset_description : str, optional
            A description for the dataset. Default is an empty string.
        version_description : str, optional
            A description for this version of the dataset. Default is an empty string.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with details of the dataset creation, structured as:
                - `datasetId` (str): ID of the created dataset.
                - `status` (str): Status of the dataset creation request.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Example
        -------
        >>> from pprint import pprint
        >>> resp, err, msg = deployment.create_dataset(
        ...     dataset_name="New Dataset",
        ...     is_unlabeled=False,
        ...     source="aws",
        ...     source_url="https://example.com/dataset.zip",
        ...     is_public=True,
        ...     dataset_description="Dataset description",
        ...     version_description="Version description"
        ... )
        >>> if err:
        ...     pprint(err)
        >>> else:
        ...     pprint(resp)
        """
        dataset_size, err, msg = self._get_dataset_size(source_url)
        print(f"dataset size is = {dataset_size}")
        path = f"/v1/dataset/deployment?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "name": dataset_name,
            "isUnlabeled": is_unlabeled,
            "source": source,
            "sourceUrl": source_url,
            "_idDeployment": self.deployment_id,
            "cloudProvider": "AWS",
            "isCreateNew": True,
            "oldDatasetVersion": None,
            "newDatasetVersion": "v1.0",
            "datasetDescription": dataset_description,
            "newVersionDescription": version_description,
            "isPublic": is_public,
            "computeAlias": "",
            "targetCloudStorage": "GCP",
            "inputType": self.model_input,
            "copyData": False,
            "isPrivateStorage": False,
            "cloudStoragePath": "",
            "urlType": "",
            "datasetSize": 0,
            "deleteDeploymentDataset": False,
            "_idProject": self.project_id,
            "type": self.model_type,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        print(resp)
        return handle_response(
            resp,
            "Dataset creation in progress",
            "An error occured while trying to create new dataset",
        )

    def set_auth_key(self, auth_key):
        self.auth_key = auth_key

    def get_prediction(
        self,
        input_path=None,
        auth_key="",
        input_url=None,
        extra_params={},
    ):
        """
        Fetch model predictions for a given image using a deployment.

        This method sends an image to the deployment for prediction. Either `deployment_id`
        or `deployment_name` must be provided in the instance to locate the deployment.

        Parameters
        ----------
        input_path : str
            The path to the input for prediction.
        auth_key : str
            The authentication key required for authorizing the prediction request.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with the prediction results, structured as:
                - `predictions` (list of dict): Each entry contains:
                    - `class` (str): The predicted class label.
                    - `confidence` (float): Confidence score of the prediction.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the prediction request.

        Raises
        ------
        ValueError
            If `auth_key` is not provided or if neither `deployment_id` nor `deployment_name` is
                set.

        Examples
        --------
        >>> from pprint import pprint
        >>> result, error, message = deployment.get_prediction(
        ...     input_path="/path/to/input.jpg",
        ...     auth_key="auth123"
        ... )
        >>> if error:
        ...     pprint(error)
        >>> else:
        ...     pprint(result)
        """
        if not auth_key:
            auth_key = self.auth_key
            if not auth_key:
                raise ValueError("auth_key is required for deployment predictions.")
        
        if not any([input_path, input_url]):
            raise ValueError("Either input_path or input_url must be provided.")
        
        files = {}
        data = {"authKey": auth_key}
        if input_path:
            files = {"input": open(input_path, "rb")}
        if input_url:
            data["inputUrl"] = input_url
        if extra_params:
            data["extraParams"] = json.dumps(extra_params)
        
        if self.deployment_id:
            url = f"/v1/model_prediction/inference/{self.deployment_id}/predict"
        elif self.deployment_name:
            url = f"/v1/model_prediction/deployment_name/{self.deployment_name}/predict"
        else:
            raise ValueError("Either deployment_id or deployment_name must be provided.")
        
        server_status, error, message = self._get_details()
        if error:
            print(f"Error checking server status: {error}")
            return None, error, message
        
        if server_status["status"] != "active":
            (
                wakeup_resp,
                wakeup_error,
                wakeup_message,
            ) = self.wakeup_deployment_server()
            if wakeup_error:
                print(f"Error waking up server: {wakeup_error}")
                return (
                    None,
                    wakeup_error,
                    wakeup_message,
                )
            time.sleep(10)
        
        headers = {"Authorization": f"Bearer {self.rpc.AUTH_TOKEN.bearer_token}"}
        resp = self.rpc.post(
            url,
            headers=headers,
            data=data,
            files=files,
        )
        success_message = "Model prediction fetched successfully"
        error_message = "An error occurred while fetching the model prediction."
        result, error, message = handle_response(resp, success_message, error_message)
        if error:
            print(f"Error fetching model prediction: {error}")
            return None, error, message
        return result

    def _get_dataset_size(self, url):
        """
        Fetch the size of the dataset from the specified URL.

        Parameters
        ----------
        url : str
            The URL of the dataset to retrieve the size for.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with dataset size information, typically structured as:
                - `size_in_mb` (float): The size of the dataset in megabytes.
            - str or None: Error message if an error occurred, otherwise None.
            - str: Status message indicating success or failure of the API call.

        Examples
        --------
        >>> from pprint import pprint
        >>> size, err, msg = dataset._get_dataset_size(url="https://example.com/dataset.zip")
        >>> if err:
        ...     pprint(err)
        >>> else:
        ...     print(f"Dataset size: {size['size_in_mb']} MB")
        """
        path = f"/v1/dataset/get_dataset_size_in_mb_from_url?projectId={self.project_id}"
        requested_payload = {"datasetUrl": url}
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=requested_payload,
        )
        return handle_response(
            resp,
            "Dataset size fetched successfully",
            "Could not fetch dataset size",
        )

    # Camera Management Methods
    def create_camera_group(self, group: CameraGroupConfig) -> Tuple[Optional['CameraGroup'], Optional[str], str]:
        """
        Create a new camera group for this deployment.
        
        Args:
            group: CameraGroup object containing the group configuration
            
        Returns:
            tuple: (camera_group_instance, error, message)
        """
        return self.camera_manager.create_camera_group(group)
    
    def get_camera_group_by_id(self, group_id: str) -> Tuple[Optional['CameraGroup'], Optional[str], str]:
        """
        Get a camera group by its ID.
        
        Args:
            group_id: The ID of the camera group to retrieve
            
        Returns:
            tuple: (camera_group_instance, error, message)
        """
        return self.camera_manager.get_camera_group_by_id(group_id)
    
    def get_camera_groups(self, page: int = 1, limit: int = 10, search: str = None) -> Tuple[Optional[List['CameraGroup']], Optional[str], str]:
        """
        Get all camera groups for this deployment.
        
        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term
            
        Returns:
            tuple: (camera_group_instances, error, message)
        """
        return self.camera_manager.get_camera_groups(page, limit, search)
    
    def update_camera_group(self, group_id: str, group: CameraGroupConfig) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update an existing camera group.
        
        Args:
            group_id: The ID of the camera group to update
            group: CameraGroup object with updated configuration
            
        Returns:
            tuple: (result, error, message)
        """
        return self.camera_manager.update_camera_group(group_id, group)
    
    def delete_camera_group(self, group_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a camera group by its ID.
        
        Args:
            group_id: The ID of the camera group to delete
            
        Returns:
            tuple: (result, error, message)
        """
        return self.camera_manager.delete_camera_group(group_id)
    
    def create_camera(self, camera_config: CameraConfig) -> Tuple[Optional['Camera'], Optional[str], str]:
        """
        Create a new camera for this deployment.
        
        Args:
            camera_config: CameraConfig object containing the camera configuration
            
        Returns:
            tuple: (camera_instance, error, message)
        """
        return self.camera_manager.create_camera(camera_config)
    
    def get_camera_by_id(self, camera_id: str) -> Tuple[Optional['Camera'], Optional[str], str]:
        """
        Get a camera by its ID.
        
        Args:
            camera_id: The ID of the camera to retrieve
            
        Returns:
            tuple: (camera_instance, error, message)
        """
        return self.camera_manager.get_camera_by_id(camera_id)
    
    def get_cameras(self, page: int = 1, limit: int = 10, search: str = None, group_id: str = None) -> Tuple[Optional[List['Camera']], Optional[str], str]:
        """
        Get all cameras for this deployment.
        
        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term
            group_id: Optional filter by camera group ID
            
        Returns:
            tuple: (camera_instances, error, message)
        """
        return self.camera_manager.get_cameras(page, limit, search, group_id)
    
    def update_camera(self, camera_id: str, camera_config: CameraConfig) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update an existing camera.
        
        Args:
            camera_id: The ID of the camera to update
            camera_config: CameraConfig object with updated configuration
            
        Returns:
            tuple: (result, error, message)
        """
        return self.camera_manager.update_camera(camera_id, camera_config)
    
    def delete_camera(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a camera by its ID.
        
        Args:
            camera_id: The ID of the camera to delete
            
        Returns:
            tuple: (result, error, message)
        """
        return self.camera_manager.delete_camera(camera_id)
    
    def add_cameras_to_group(self, group_id: str, camera_configs: List[CameraConfig]) -> Tuple[Optional[List['Camera']], Optional[str], str]:
        """
        Add multiple cameras to a camera group in this deployment.
        
        Args:
            group_id: The ID of the camera group
            camera_configs: List of CameraConfig objects
            
        Returns:
            tuple: (camera_instances, error, message)
        """
        return self.camera_manager.add_cameras_to_group(group_id, camera_configs)
    
    def delete_all_cameras(self, confirm: bool = False) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete all cameras for this deployment.
        
        Args:
            confirm: Must be True to confirm bulk deletion
            
        Returns:
            tuple: (result, error, message)
        """
        return self.camera_manager.delete_all_cameras(confirm)

    # Legacy method aliases for backward compatibility
    def add_camera_config(self, config: CameraConfig):
        """Legacy method - use create_camera instead."""
        return self.create_camera(config)
    
    def get_camera_configs(self, page: int = 1, limit: int = 10, search: str = None, group_id: str = None):
        """Legacy method - use get_cameras instead."""
        return self.get_cameras(page, limit, search, group_id)

    # Streaming Gateway Management Methods  
    def create_streaming_gateway(self, gateway_config: StreamingGatewayConfig) -> Tuple[Optional['StreamingGateway'], Optional[str], str]:
        """
        Create a new streaming gateway for this deployment.
        
        Args:
            gateway_config: StreamingGatewayConfig object containing the gateway configuration
            
        Returns:
            tuple: (streaming_gateway, error, message)
        """
        return self.streaming_gateway_manager.create_streaming_gateway(gateway_config)
    
    def get_streaming_gateway_by_id(self, gateway_id: str) -> Tuple[Optional['StreamingGateway'], Optional[str], str]:
        """
        Get a streaming gateway by its ID.
        
        Args:
            gateway_id: The ID of the streaming gateway to retrieve
            
        Returns:
            tuple: (streaming_gateway, error, message)
        """
        return self.streaming_gateway_manager.get_streaming_gateway_by_id(gateway_id)
    
    def get_streaming_gateways(self, page: int = 1, limit: int = 10, search: str = None) -> Tuple[Optional[List['StreamingGateway']], Optional[str], str]:
        """
        Get all streaming gateways for this deployment.
        
        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term
            
        Returns:
            tuple: (streaming_gateways, error, message)
        """
        return self.streaming_gateway_manager.get_streaming_gateways(page, limit, search)
    
    def update_streaming_gateway(self, gateway_id: str, gateway_config: StreamingGatewayConfig) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update an existing streaming gateway.
        
        Args:
            gateway_id: The ID of the streaming gateway to update
            gateway_config: StreamingGatewayConfig object with updated configuration
            
        Returns:
            tuple: (result, error, message)
        """
        try:
            gateway = StreamingGateway(self.session, gateway_id=gateway_id)
            # Update the configuration
            gateway.config = gateway_config
            return gateway.update()
        except Exception as e:
            return None, str(e), "Failed to update streaming gateway"
    
    def delete_streaming_gateway(self, gateway_id: str, force: bool = False) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a streaming gateway by its ID.
        
        Args:
            gateway_id: The ID of the streaming gateway to delete
            force: Force delete even if active
            
        Returns:
            tuple: (result, error, message)
        """
        try:
            gateway = StreamingGateway(self.session, gateway_id=gateway_id)
            return gateway.delete(force=force)
        except Exception as e:
            return None, str(e), "Failed to delete streaming gateway"
    
    def add_camera_groups_to_streaming_gateway(self, gateway_id: str, camera_group_ids: List[str]) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Add camera groups to a streaming gateway.
        
        Args:
            gateway_id: The ID of the streaming gateway
            camera_group_ids: List of camera group IDs to add
            
        Returns:
            tuple: (result, error, message)
        """
        try:
            gateway = StreamingGateway(self.session, gateway_id=gateway_id)
            return gateway.add_camera_groups(camera_group_ids)
        except Exception as e:
            return None, str(e), "Failed to add camera groups to streaming gateway"
    
    def remove_camera_groups_from_streaming_gateway(self, gateway_id: str, camera_group_ids: List[str]) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Remove camera groups from a streaming gateway.
        
        Args:
            gateway_id: The ID of the streaming gateway
            camera_group_ids: List of camera group IDs to remove
            
        Returns:
            tuple: (result, error, message)
        """
        try:
            gateway = StreamingGateway(self.session, gateway_id=gateway_id)
            return gateway.remove_camera_groups(camera_group_ids)
        except Exception as e:
            return None, str(e), "Failed to remove camera groups from streaming gateway"
