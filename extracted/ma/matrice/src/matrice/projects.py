"""Module for interacting with backend API to manage projects."""

import sys
import logging
from typing import Dict, List, Optional, Tuple
from matrice.action import Action
from matrice.annotation import Annotation
from matrice.dataset import Dataset
from matrice.deployment import Deployment
from matrice.exported_model import ExportedModel
from matrice.models import Model
from matrice.utils import handle_response
from collections import OrderedDict
from datetime import datetime, timedelta


class Projects:
    """
    A class for handling project-related operations using the backend API.

    Attributes
    ----------
    session : Session
        The session object used for API interactions.
    account_number : str
        The account number associated with the session.
    project_name : str
        The name of the project.
    project_id : str
        The ID of the project (initialized in the constructor).
    project_input : str
        The input type for the project (initialized in the constructor).
    output_type : str
        The output type for the project (initialized in the constructor).

    Parameters
    ----------
    session : Session
        The session object used for API interactions.
    project_name : str
        The name of the project.
    """

    def __init__(
        self,
        session,
        project_name=None,
        project_id=None,
    ):
        """
        Initialize a Projects object with project details.

        Parameters
        ----------
        session : Session
            The session object used for API interactions.
        project_name : str
            The name of the project.
        """
        assert project_name is not None or project_id is not None
        self.session = session
        self.account_number = session.account_number
        self.last_refresh_time = datetime.now()
        self.project_name = project_name
        self.project_id = project_id
        self.rpc = session.rpc
        if project_name:
            project_info, error, message = self._get_project_by_name()
        else:
            project_info, error, message = self._get_a_project_by_id()
        if error:
            raise Exception(f"Error fetching project info: {error}")
        else:
            if not project_info["isDisabled"]:
                self.status = "enabled"
            else:
                self.status = "disabled"
            self.project_id = project_info["_id"]
            self.project_name = project_info["name"]
            self.project_input = project_info["inputType"]
            self.output_type = project_info["outputType"]
            self.created_at = project_info["createdAt"]
            self.updated_at = project_info["updatedAt"]

    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise Exception("Refresh can only be called after two minutes since the last refresh.")
        init_params = {
            "session": self.session,
            "project_name": self.project_name,
            "project_id": self.project_id,
        }
        self.__init__(**init_params)
        self.last_refresh_time = datetime.now()

    def _get_service_and_action_ids(self, resp, error, message):
        """
        Extract service and action IDs from the response.

        Parameters
        ----------
        resp : dict
            The response dictionary from the API.
        error : str
            An error message if extraction fails.

        Returns
        -------
        tuple
            A tuple containing:
            - The service ID if extraction is successful, or None if it fails.
            - The action ID if extraction is successful, or None if it fails.
            - An error message if extraction fails, or None if successful.

        Example
        -------
        >>> resp = {"data": {"service_id": "123", "action_id": "456"}}
        >>> service_id, action_id, error = project._get_service_and_action_ids(resp, None)
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Service ID: {service_id}, Action ID: {action_id}")
        """
        if error:
            print(message, error)
            return None, None
        data = resp
        return data["_id"], data["_idAction"]

    def __job_cost_estimate(self, data):
        pass

    def _get_project_by_name(self):
        """
        Fetch project details by project name.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project._get_project_by_name()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """
        path = f"/v1/accounting/get_project_by_name?name={self.project_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Project details Fetched Successfully",
            "Could not fetch project details",
        )

    def _get_a_project_by_id(self):
        """
        Fetch project information by project ID.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project._get_a_project_by_id()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """
        path = f"/v1/accounting/{self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            f"Project info fetched for project with id {self.project_id}",
            f"Could not fetch project info for project with id {self.project_id}",
        )

    def get_service_action_logs(self, service_id, service_name):
        """
        Fetch action logs for a specific service.

        Parameters
        ----------
        service_id : str
            The ID of the service for which to fetch action logs.
        service_name : str
            The name of the service for which to fetch action logs.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project.get_service_action_logs("service123")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """
        assert service_id or service_name, "Service ID or name is required to fetch action logs"
        path = f"/v1/project/service/{service_id}/logs?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Action logs fected succesfully",
            "Could not fetch action logs",
        )

    def get_latest_action_record(self, service_id):
        """
        Fetch the latest action logs for a specific service ID.

        Parameters
        ----------
        service_id : str
            The ID of the service for which to fetch the latest action logs.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project.get_latest_action_record("service123")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """
        path = f"/v1/project/get_latest_action_record/{service_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Action logs fected succesfully",
            "Could not fetch action logs",
        )

    def _create_dataset(
        self,
        project_type,
        dataset_name,
        dataset_type="detection",
        input_type="MSCOCO",
        dataset_path="",
        source_url="",
        url_type="",
        bucket_alias="",
        compute_alias="",
        target_cloud_storage="",
        source_credential_alias="",
        bucket_alias_service_provider="auto",
    ):
        """
        Create a new dataset.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.
        dataset_type : str, optional
            The type of dataset (default is "detection")
        input_type : str, optional
            The input type for the dataset (default is "MSCOCO")
        dataset_path : str, optional
            Local path to dataset files (default is "")
        source_url : str, optional
            URL to dataset source (default is "")
        url_type : str, optional
            Type of URL source (default is "")
        bucket_alias : str, optional
            Alias for cloud storage bucket (default is "")
        compute_alias : str, optional
            Alias for compute resources (default is "")
        target_cloud_storage : str, optional
            Target cloud storage location (default is "")
        source_credential_alias : str, optional
            Alias for source credentials (default is "")
        bucket_alias_service_provider : str, optional
            Service provider for bucket alias (default is "auto")

        Returns
        -------
        Dataset
            A Dataset object for the created dataset.

        Example
        -------
        >>> dataset = project._create_dataset(
        ...     dataset_name="MyDataset",
        ...     dataset_path="/path/to/data",
        ...     dataset_type="detection"
        ... )
        >>> print(f"Dataset created: {dataset}")
        """
        from matrice.data_processing.create_dataset import create_dataset
        return create_dataset(
            self.session,
            self.project_id,
            self.account_number,
            project_type,
            dataset_name,
            dataset_type=dataset_type,
            input_type=input_type,
            dataset_path=dataset_path,
            source_url=source_url,
            url_type=url_type,
            bucket_alias=bucket_alias,
            compute_alias=compute_alias,
            target_cloud_storage=target_cloud_storage,
            source_credential_alias=source_credential_alias,
            bucket_alias_service_provider=bucket_alias_service_provider
        )

    def import_local_dataset(
        self,
        dataset_name,
        file_path,
        dataset_type,
        input_type="image",
        project_type='detection',
        bucket_alias="",
        compute_alias="",
        source_credential_alias="",
        bucket_alias_service_provider="auto",
        target_cloud_storage="AWS",
    ):
        """
        Import a local dataset.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.
        file_path : str
            The path to the local file.
        dataset_type : str
            The type of the dataset.
        input_type : str, optional
            The input type for the dataset (default is "image").
        bucket_alias : str, optional
            The bucket alias for the dataset (default is "").
        compute_alias : str, optional
            The compute alias (default is "").
        source_credential_alias : str, optional
            The source credential alias (default is "").
        bucket_alias_service_provider : str, optional
            The bucket alias service provider (default is "auto").
        target_cloud_storage : str, optional
            The target cloud storage provider (default is "AWS").

        Returns
        -------
        Dataset
            A Dataset object for the created dataset.

        Example
        -------
        >>> dataset = project.import_local_dataset("MyLocalDataset", "path/to/data.csv", "image")
        >>> print(f"Dataset created: {dataset}")
        """
        return self._create_dataset(
            dataset_name=dataset_name,
            dataset_type=dataset_type,
            project_type=project_type,
            input_type=input_type,
            dataset_path=file_path,
            bucket_alias=bucket_alias,
            compute_alias=compute_alias,
            source_credential_alias=source_credential_alias,
            bucket_alias_service_provider=bucket_alias_service_provider,
            target_cloud_storage=target_cloud_storage,
        )

    def import_cloud_dataset(
        self,
        dataset_name,
        source_url,
        cloud_provider,
        dataset_type,
        input_type="image",
        bucket_alias="",
        compute_alias="",
        source_credential_alias="",
        bucket_alias_service_provider="auto",
        target_cloud_storage="AWS",
    ):
        """
        Import a cloud dataset.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.
        source_url : str
            The URL of the source.
        cloud_provider : str
            The cloud provider for the dataset.
        dataset_type : str
            The type of the dataset.
        input_type : str, optional
            The input type for the dataset (default is "image").
        bucket_alias : str, optional
            The bucket alias for the dataset (default is "").
        compute_alias : str, optional
            The compute alias (default is "").
        source_credential_alias : str, optional
            The source credential alias (default is "").
        bucket_alias_service_provider : str, optional
            The bucket alias service provider (default is "auto").
        target_cloud_storage : str, optional
            The target cloud storage provider (default is "AWS").

        Returns
        -------
        Dataset
            A Dataset object for the created dataset.

        Example
        -------
        >>> dataset = project.import_cloud_dataset("MyCloudDataset", "http://source.url", "AWS",
        "image")
        >>> print(f"Dataset created: {dataset}")
        """
        return self._create_dataset(
            dataset_name=dataset_name,
            dataset_type=dataset_type,
            input_type=input_type,
            source_url=source_url,
            url_type=cloud_provider,
            bucket_alias=bucket_alias,
            compute_alias=compute_alias,
            source_credential_alias=source_credential_alias,
            bucket_alias_service_provider=bucket_alias_service_provider,
            target_cloud_storage=target_cloud_storage,
        )

    def create_annotation(
        self,
        project_type,
        ann_title,
        dataset_id,
        dataset_version,
        labels,
        only_unlabeled,
        is_ML_assisted,
        labellers,
        reviewers,
        guidelines,
    ):
        """
        Create a new annotation for a dataset.

        Parameters
        ----------
        project_type : str
            The type of the project for which the annotation is being created.
        ann_title : str
            The title of the annotation.
        dataset_id : str
            The ID of the dataset to annotate.
        dataset_version : str
            The version of the dataset.
        labels : list
            The list of labels for the annotation.
        only_unlabeled : bool
            Whether to annotate only unlabeled data.
        is_ML_assisted : bool
            Whether the annotation is ML-assisted.
        labellers : list
            The list of labellers for the annotation.
        reviewers : list
            The list of reviewers for the annotation.
        guidelines : str
            The guidelines for the annotation.

        Returns
        -------
        tuple
            A tuple containing:
            - An `Annotation` object for the created annotation.
            - An `Action` object related to the annotation creation process.

        Example
        -------
        >>> annotation, action = project.create_annotation("object_detection", "MyAnnotation",
        "dataset123", "v1.0", ["label1", "label2"], True, False, [{"email": "user-email",
        "name": "username", "percentageWork": '100'}],[{"email": "user-email", "name": "username",
        "percentageWork": '100'}], "Follow these guidelines")
        >>> if action:
        >>>     print(f"Annotation created: {annotation}")
        >>> else:
        >>>     print(f"Error: {annotation}")
        """
        validated_labellers = self._validate_labellers_and_reviewers(labellers)
        validated_reviewers = self._validate_labellers_and_reviewers(reviewers)
        path = f"/v1/annotations?projectId={self.project_id}&projectType={project_type}"
        payload = {
            "title": ann_title,
            "_idDataset": dataset_id,
            "datasetVersion": dataset_version,
            "labels": labels,
            "onlyUnlabeled": only_unlabeled,
            "isMLAssisted": is_ML_assisted,
            "labellers": validated_labellers,
            "reviewers": validated_reviewers,
            "guidelines": guidelines,
            "type": project_type,
            "modelType": "",
            "modelId": "",
        }
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=payload,
        )
        resp, error, message = handle_response(
            resp,
            "Annotation creation in progress",
            "An error occurred while trying to create new annotation",
        )
        annotation_id = resp["_id"]
        service_id, action_id = self._get_service_and_action_ids(resp, error, message)
        return Annotation(self.session, annotation_id, ann_title), Action(self.session, action_id)

    def add_models_for_training(
        self,
        model_train_configs,
        primary_metric,
        dataset_id=None,
        dataset_name=None,
        dataset_version="v1.0",
        target_runtime=["PyTorch"],
        compute_alias="",
    ):
        """
        Add models to the training queue for the project.

        This method prepares and sends model configurations to the backend for training.
        It supports both single model and batch model submissions. Additionally, it dynamically
        adds all values from the `model_config` dictionary into the payload sent to the backend.

        Parameters
        ----------
        model_train_configs : dict or list of dict
            Configuration dictionary or list of dictionaries containing model settings.
            Each dictionary should include:
            - model_key (str): Model key
            - is_autoML (bool): Flag for AutoML usage
            - tuning_type (str): Type of model tuning
            - model_checkpoint (str): Model checkpoint information
            - checkpoint_type (str): Type of checkpoint
            - action_config (dict): Configuration for model actions
            - model_config (dict): Model-specific configuration, where all keys and values in this
            dictionary will be added dynamically to the final payload.
            - model_name (str, optional): The name of the model.
            - params_millions (int or float, optional): The number of parameters in millions.

        compute_alias : str, optional
            Alias for the compute resource to use for training (default: "").

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): Status message indicating success or failure.

        Notes
        -----
        The method accumulates model configurations in `self.models_for_training` and
        sends them as a batch to the backend. The list is cleared after submission.

        All keys and values from the `model_config` dictionary are added dynamically to the payload
        that is sent for training, which allows flexible inclusion of model-specific parameters.

        Example
        -------
        >>> model = ModelArch(session, model_key="resnet50")
        >>> config = {
        ...     "model_key": "resnet50",
        ...     "is_autoML": True,
        ...     "tuning_type": "auto",
        ...     "model_checkpoint": "predefined",
        ...     "checkpoint_type": "auto",
        ...     "action_config": {},
        ...     "model_config": {
        ...         "learning_rate": 0.001,
        ...         "batch_size": 32
        ...     },
        ...     "model_name": "ResNet50",
        ...     "params_millions": 25
        ... }
        >>> resp, err, msg = project.add_models_for_training(config, "GPU-A100")
        >>> if err:
        ...     print(f"Error: {err}")
        ... else:
        ...     print(f"Success: {msg}")
        """
        if not dataset_id and not dataset_name:
            raise ValueError("Either dataset_id or dataset_name must be provided.")
        if not (dataset_id and dataset_name):
            dataset = Dataset(
                session=self.session,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
            )
            dataset_id = dataset.dataset_id
            dataset_name = dataset.dataset_name
        if not isinstance(model_train_configs, list):
            model_train_configs = [model_train_configs]
        payload = [
            {
                "modelKey": model_config["model_key"],
                "autoML": model_config["is_autoML"],
                "tuningType": model_config["tuning_type"],
                "modelCheckpoint": model_config["model_checkpoint"],
                "checkpointType": model_config["checkpoint_type"],
                "_idModelArch": model_config["model_arch_id"],
                "modelFamilyName": model_config["model_family_name"],
                "actionConfig": model_config["action_config"],
                "modelConfig": model_config["model_config"],
                "modelName": model_config["model_name"],
                "paramsInMillion": model_config["params_millions"],
                "modelInputs": model_config["model_inputs"],
                "modelOutputs": model_config["model_outputs"],
                "targetRuntime": target_runtime,
                "_idDataset": dataset_id,
                "datasetVersion": dataset_version,
                "primaryMetric": primary_metric,
                "datasetName": dataset_name,
                "computeAlias": compute_alias,
            }
            for model_config in model_train_configs
        ]
        print(payload)
        path = f"/v1/model/add_model_train_list?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=payload,
        )
        print(resp)
        return handle_response(
            resp,
            "Training started successfully",
            "Could not start training",
        )

    def stop_training(self):
        pass

    def create_model_export(
        self,
        model_train_id,
        export_formats,
        model_config,
        is_gpu_required=False,
    ):
        """
        Add export configurations to a trained model.

        Parameters
        ----------
        model_train_id : str
            The ID of the trained model.
        export_formats : list
            The list of formats to export the model.
        model_config : dict
            The configuration settings for the model export.
        is_gpu_required : bool, optional
            Flag to indicate if GPU is required for the export (default is False).

        Returns
        -------
        tuple
            A tuple containing:
            - An `InferenceOptimization` object related to the model export.
            - An `Action` object related to the export process.

        Example
        -------
        >>> inference_opt, action = project.add_model_export("model123", ["format1", "format2"],
        {"configKey": "configValue"}, is_gpu_required=True)
        >>> if action:
        >>>     print(f"Model export added: {inference_opt}")
        >>> else:
        >>>     print(f"Error: {inference_opt}")
        """
        if not isinstance(export_formats, list):
            export_formats = [export_formats]
        M = Model(self.session, model_train_id)
        if M.created_at == "0001-01-01T00:00:00Z":
            print("No model exists with the given model train id")
            sys.exit(0)
        path = f"/v1/model/{model_train_id}/add_model_export?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        model_payload = {
            "_idProject": self.project_id,
            "_idModelTrain": model_train_id,
            "modelName": M.model_name,
            "modelInputs": M.model_inputs,
            "_idModelArch": M.model_arch_id,
            "modelOutputs": M.model_outputs,
            "exportFormats": export_formats,
            "_idDataset": M.dataset_id,
            "datasetVersion": M.dataset_version,
            "gpuRequired": is_gpu_required,
            "actionConfig": M.action_config,
            "modelConfig": model_config,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=model_payload,
        )
        resp, error, message = handle_response(
            resp,
            "Model Export added successfully",
            "An error occurred while adding model export",
        )
        service_id, action_id = self._get_service_and_action_ids(resp, error, message)
        return ExportedModel(self.session, service_id), Action(self.session, action_id)

    def create_fastapi_deployment(
        self,
        deployment_name,
        model_id,
        gpu_required=True,
        auto_scale=True,
        auto_shutdown=True,
        shutdown_threshold=5,
        compute_alias="",
        model_type="trained",
        runtime_framework="Pytorch",
        is_kafka_enabled=False,
        is_optimized=False,
        post_processing_config=None,
    ):
        return self._create_deployment(
            deployment_name=deployment_name,
            model_id=model_id,
            gpu_required=gpu_required,
            auto_scale=auto_scale,
            auto_shutdown=auto_shutdown,
            shutdown_threshold=shutdown_threshold,
            compute_alias=compute_alias,
            model_type=model_type,
            runtime_framework=runtime_framework,
            server_type="fastapi",
            is_kafka_enabled=is_kafka_enabled,
            is_optimized=is_optimized,
            post_processing_config=post_processing_config,
        )

    def create_triton_deployment(
        self,
        deployment_name,
        model_id,
        gpu_required=True,
        auto_scale=True,
        auto_shutdown=True,
        shutdown_threshold=5,
        compute_alias="",
        model_type="trained",
        runtime_framework="Pytorch",
        connection_protocol="rest",
        max_batch_size=8,
        num_model_instances=1,
        input_data_type="TYPE_FP32",
        output_data_type="TYPE_FP32",
        dynamic_batching=False,
        preferred_batch_size=[2, 4, 8],
        max_queue_delay_microseconds=100,
        input_pinned_memory=True,
        output_pinned_memory=True,
        is_kafka_enabled=False,
        is_optimized=False,
        post_processing_config=None,
    ):
        deployment_params = {
            "max_batch_size": max_batch_size,
            "num_model_instances": num_model_instances,
            "input_data_type": input_data_type,
            "output_data_type": output_data_type,
            "dynamic_batching": dynamic_batching,
            "preferred_batch_size": preferred_batch_size,
            "max_queue_delay_microseconds": max_queue_delay_microseconds,
            "input_pinned_memory": input_pinned_memory,
            "output_pinned_memory": output_pinned_memory,
        }
        return self._create_deployment(
            deployment_name=deployment_name,
            model_id=model_id,
            gpu_required=gpu_required,
            auto_scale=auto_scale,
            auto_shutdown=auto_shutdown,
            shutdown_threshold=shutdown_threshold,
            compute_alias=compute_alias,
            model_type=model_type,
            runtime_framework=runtime_framework,
            server_type=f"triton_{connection_protocol}",
            deployment_params=deployment_params,
            is_kafka_enabled=is_kafka_enabled,
            is_optimized=is_optimized,
            post_processing_config=post_processing_config,
        )

    def _create_deployment(
        self,
        deployment_name,
        model_id="",
        gpu_required=True,
        auto_scale=False,
        auto_shutdown=True,
        shutdown_threshold=5,
        compute_alias="",
        model_type="trained",
        deployment_type="regular",
        checkpoint_type="pretrained",
        checkpoint_value="",
        checkpoint_dataset="COCO",
        runtime_framework="Pytorch",
        server_type="fastapi",
        deployment_params={},
        model_input="image",
        model_output="classification",
        suggested_classes=[],
        model_family="",
        model_key="",
        is_kafka_enabled=False,
        is_optimized=False,
        instance_range=[1, 1],
        custom_schedule=False,
        schedule_deployment=[],
        post_processing_config=None,
        create_deployment_config={},
        return_id_only=False,
    ):
        """
        Create a deployment for a model.

        Parameters
        ----------
        deployment_name : str
            The name of the deployment.
        model_id : str
            The ID of the model to be deployed.
        gpu_required : bool, optional
            Flag to indicate if GPU is required for the deployment (default is True).
        auto_scale : bool, optional
            Flag to indicate if auto-scaling is enabled (default is False).
        auto_shutdown : bool, optional
            Flag to indicate if auto-shutdown is enabled (default is True).
        shutdown_threshold : int, optional
            The threshold for auto-shutdown (default is 5).
        compute_alias : str, optional
            The alias for the compute (default is an empty string).
        model_type : str, optional
            The type of model (default is "trained").
        deployment_type : str, optional
            The type of deployment (default is "regular").
        checkpoint_type : str, optional
            The type of checkpoint (default is "pretrained").
        checkpoint_value : str, optional
            The value of the checkpoint (default is an empty string).
        checkpoint_dataset : str, optional
            The dataset for the checkpoint (default is "COCO").
        runtime_framework : str, optional
            The runtime framework (default is "Pytorch").
        server_type : str, optional
            The type of server (default is "fastapi").
        deployment_params : dict, optional
            Additional deployment parameters (default is an empty dict).
        model_input : str, optional
            The model input type (default is "image").
        model_output : str, optional
            The model output type (default is "classification").
        suggested_classes : list, optional
            List of suggested classes (default is an empty list).
        model_family : str, optional
            The model family (default is an empty string).
        model_key : str, optional
            The model key (default is an empty string).
        is_kafka_enabled : bool, optional
            Flag to indicate if Kafka is enabled (default is False).
        is_optimized : bool, optional
            Flag to indicate if the deployment is optimized (default is False).
        instance_range : list, optional
            The range of instances (default is [1, 1]).
        custom_schedule : bool, optional
            Flag to indicate if custom scheduling is enabled (default is False).
        schedule_deployment : list, optional
            List of scheduled deployments (default is an empty list).
        post_processing_config : dict, optional
            The post-processing configuration (default is None).
        create_deployment_config : dict, optional
            The deployment configuration (default is None).
        return_id_only : bool, optional
            Flag to indicate if only the deployment ID is returned (default is False).
        Returns
        -------
        tuple
            A tuple containing:
            - A `Deployment` object for the created deployment.
            - An `Action` object related to the deployment process.

        Example
        -------
        >>> deployment, action = project._create_deployment("Deployment1", "model123",
        auto_scale=True)
        >>> if action:
        >>>     print(f"Deployment created: {deployment}")
        >>> else:
        >>>     print(f"Error: {deployment}")
        """
        if model_type == "trained":
            model = Model(self.session, model_id=model_id)
            model_input = model.model_inputs[0]
            model_output = model.model_outputs[0]
            checkpoint_type = "model_id"
            checkpoint_value = model_id
        elif model_type == "exported":
            model = ExportedModel(
                self.session,
                model_export_id=model_id,
            )
            runtime_framework = model.export_format
            model_input = model.model_inputs[0]
            model_output = model.model_outputs[0]
            checkpoint_type = "model_id"
            checkpoint_value = model_id
        if post_processing_config:
            deployment_params["postProcessingConfig"] = post_processing_config
        body = {
            "deploymentName": deployment_name,
            "_idModel": model_id,
            "runtimeFramework": runtime_framework,
            "modelInput": model_input,
            "modelOutput": model_output,
            "autoShutdown": auto_shutdown,
            "autoScale": auto_scale,
            "gpuRequired": gpu_required,
            "shutdownThreshold": shutdown_threshold,
            "computeAlias": compute_alias,
            "serverType": server_type,
            "checkpointType": checkpoint_type,
            "checkpointValue": checkpoint_value,
            "dataset": checkpoint_dataset,
            "modelFamilyName": model_family,
            "modelKey": model_key,
            "suggestedClasses": suggested_classes,
            "deploymentType": deployment_type,
            "modelType": model_type,
            "isKafkaEnabled": is_kafka_enabled,
            "isOptimized": is_optimized,
            "instanceRange": instance_range,
            "customSchedule": custom_schedule,
            "scheduleDeployment": schedule_deployment,
            "deploymentParams": deployment_params,
        }
        if create_deployment_config:
            body.update(create_deployment_config)
        headers = {"Content-Type": "application/json"}
        path = f"/v1/deployment?projectId={self.project_id}"
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        resp, error, message = handle_response(
            resp,
            "Deployment created successfully.",
            "An error occurred while trying to create deployment.",
        )
        if resp:
            if return_id_only:
                return resp["data"]["_id"]
            service_id, action_id = self._get_service_and_action_ids(resp, error, message)
            return Deployment(self.session, service_id), Action(self.session, action_id)
        else:
            logging.error(f"Deployment creation failed: {resp}")
            return None, None

    def create_inference_pipeline(
        self, 
        name: str = None, 
        description: str = None, 
        applications: List[Dict] = None
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a new inference pipeline with model configuration.

        Args:
            name: pipeline name
            description: pipeline description
            applications: List of application IDs

        Returns:
            tuple: (result, error, message)
                - result: API response data if successful, None otherwise
                - error: Error message if failed, None otherwise
                - message: Status message
        """
        
        if not applications:
            return (
                None,
                "At least one application is required",
                "No applications specified",
            )

        path = "/v1/inference/inference_pipeline"
        payload = {
            "name": name,
            "description": description,
            "applications": applications,
            "_idProject": self.project_id,
        }

        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Inference pipeline created successfully",
            "Failed to create inference pipeline",
        )

    def list_inference_pipelines(
        self, page: int = 1, limit: int = 10, status: str = None, search: str = None
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Retrieve all inference pipelines for the authenticated user.

        Args:
            page: Page number for pagination
            limit: Items per page (max 100)
            status: Filter by status ("deploying", "ready", "active", "stopped", "error")
            search: Search term for name/description

        Returns:
            tuple: (result, error, message)
        """
        path = f"/v1/inference/list_inference_pipelines/{self.project_id}"
        params = {"page": page, "limit": min(limit, 100)}

        if status:
            params["status"] = status
        if search:
            params["search"] = search

        resp = self.rpc.get(path=path, params=params)
        return  handle_response(
            resp,
            "User pipelines retrieved successfully",
            "Failed to retrieve user pipelines",
        )
    
    def delete(self):
        """
        Delete a project by project ID.

        Returns
        -------
        tuple
            A tuple containing:
            - A success message if the project is deleted successfully.
            - An error message if the deletion fails.

        Example
        -------
        >>> success_message, error = project.delete()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(success_message)
        """
        _, error, _ = self._get_a_project_by_id()
        if error:
            print("Project is not found")
            sys.exit(1)
        path = f"/v1/accounting/delete_project/{self.project_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Project deleted successfully",
            "An error occurred while trying to delete project",
        )

    def change_status(self, enable=True):
        """
        Enables or disable a project. It is set to enable by default.

        Parameters
        ----------
        type : str
            The type of action to perform: "enable" or "disable".

        Returns
        -------
        tuple
            A tuple containing:
            - A success message if the project is enabled or disabled successfully.
            - An error message if the action fails.

        Example
        -------
        >>> success_message, error = project.change_status(enable=True)
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(success_message)
        """
        if enable:
            type = "enable"
        else:
            type = "disable"
        _, error, _ = self._get_a_project_by_id()
        if error:
            print("Project is not found")
            sys.exit(1)
        path = f"/v1/project/enable-disable-project/{type}/{self.project_id}"
        resp = self.rpc.put(path=path)
        return handle_response(
            resp,
            f"Project {self.project_id} {type}d successfully",
            f"Could not {type} project {self.project_id}",
        )

    def get_actions_logs(self, action_id):
        """
        Fetch action logs for a specific action.

        Parameters
        ----------
        action_id : str
            The ID of the action for which logs are to be fetched.

        Returns
        -------
        tuple
            A tuple containing:
            - The action logs if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> logs, error = project.get_actions_logs_for_action("action123")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Action logs: {logs}")
        """
        path = f"/v1/project/action_logs_from_record_id/{action_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Action logs fected succesfully",
            "Could not fetch action logs",
        )

    def list_collaborators(self):
        """
        List all collaborators associated with the current project along with the permissions.

        This function retrieves a list of all collaborators for the specified project ID.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg =project.list_collaborators()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Collaborators : {resp}")
        """
        path = f"/v1/user/project/{self.project_id}/collaborators"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Collaborators fetched successfully",
            "Could not fetch collaborators",
        )

    def invite_user_to_project(self, email, permissions):
        """
        Invite a user to the current project with specific permissions.

        This function sends an invitation to a user, identified by their email address,
        to join the specified project.
        The user will be assigned the provided permissions for different project services.

        Args:
            email (str): The email address of the user to invite.
            permissions (dict): A dictionary specifying the permissions for various project
                services.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> email = "ashray.gupta@matrice.ai"
        >>> permissions = {
        ...     'datasetsService': {
        ...         'read': True,
        ...         'write': True,
        ...         'admin': True
        ...     },
        ...     'annotationService': {
        ...         'read': True,
        ...         'write': False,
        ...         'admin': False
        ...     },
        ...     'modelsService': {
        ...         'read': True,
        ...         'write': False,
        ...         'admin': False
        ...     },
        ...     'inferenceService': {
        ...         'read': True,
        ...         'write': False,
        ...         'admin': False
        ...     },
        ...     'deploymentService': {
        ...         'read': True,
        ...         'write': True,
        ...         'admin': False
        ...     },
        ...     'byomService': {
        ...         'read': True,
        ...         'write': False,
        ...         'admin': False
        ...     }
        ... }
        >>> resp, err, msg = project.invite_user_to_project(email, permissions)
        >>> if err:
        ...     print(f"Error: {err}")
        ... else:
        ...     print("User invited successfully")
        """
        path = "/v1/user/project/invite"
        headers = {"Content-Type": "application/json"}
        body = {
            "_idProject": self.project_id,
            "email": email,
            "projectName": self.project_name,
            "permissions": permissions,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "User invited to the project successfully",
            "Could not invite user to the project",
        )

    def update_permissions(self, collaborator_id, permissions):
        """
        Update the permissions for a collaborator in the current project.

        This function updates the permissions for a specified collaborator in the current project.

        Args:
            collaborator_id (str): The ID of the collaborator whose permissions are to be updated.
            permissions (list): A list containing the updated permissions for various project
                services.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> collaborator_id = "12345"
        >>> permissions = [
        ...     "v1.0",
        ...     True,  # isProjectAdmin
        ...     {"read": True, "write": True, "admin": False},  # datasetsService
        ...     {"read": True, "write": False, "admin": False},  # modelsService
        ...     {"read": True, "write": False, "admin": False},  # annotationService
        ...     {"read": True, "write": False, "admin": False},  # byomService
        ...     {"read": True, "write": True, "admin": False},  # deploymentService
        ...     {"read": True, "write": False, "admin": False},  # inferenceService
        ... ]
        >>> resp, err, msg = project.update_permissions(collaborator_id, permissions)
        >>> if err:
        ...     print(f"Error: {err}")
        ... else:
        ...     print("Permissions updated successfully")
        """
        path = f"/v1/user/project/{self.project_id}/collaborators/{collaborator_id}?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "version": permissions[0],
            "isProjectAdmin": permissions[1],
            "datasetsService": permissions[2],
            "modelsService": permissions[3],
            "annotationService": permissions[4],
            "byomService": permissions[5],
            "deploymentService": permissions[6],
            "inferenceService": permissions[7],
        }
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "Collaborator permissions updated successfully",
            "Could not update collaborator permissions",
        )

    def list_deployments(self, page_size=10, page_number=0):
        """
        List all deployments inside the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of deployments if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> deployments, error = project.list_deployments()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Deployments: {deployments}")
        """
        print("project_id", self.project_id)
        path = f"/v1/inference/list_deployments/v2?projectId={self.project_id}&pageSize={page_size}&pageNumber={page_number}"
        resp = self.rpc.get(path=path)
        print("path", path)
        data, error, message = handle_response(
            resp,
            "Deployment list fetched successfully",
            "An error occurred while trying to fetch deployment list.",
        )
        if error:
            return {}, error, message
        if data is None:
            return (
                {},
                "",
                "No Deployments , create one.",
            )
        items = data.get("items", [])
        deployments = {
            item["deploymentName"]: Deployment(
                self.session,
                deployment_id=item["_id"],
            )
            for item in items
        }
        return deployments, None, message

    def list_datasets(
        self,
        status="total",
        page_size=10,
        page_number=0,
    ):
        """
        List all datasets in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of datasets if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> datasets, error = project.list_datasets()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Datasets: {datasets}")
        """
        path = f"/v2/dataset/list/{self.project_id}?pageSize={page_size}&pageNumber={page_number}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Dataset list fetched successfully",
            "Could not fetch dataset list",
        )
        if error:
            return {}, error
        if data is None:
            return (
                {},
                "",
                "No Datasets , create one.",
            )
        items = data.get("items", [])
        datasets = {
            item["name"]: Dataset(
                self.session,
                dataset_id=item["_id"],
            )
            for item in items
        }
        return datasets, None

    def list_annotations(self, page_size=10, page_number=0):
        """
        List all annotations in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of annotations if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> annotations, error = project.list_annotations()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Annotations: {annotations}")
        """
        path = f"/v1/annotations/v2?projectId={self.project_id}&pageSize={page_size}&pageNumber={page_number}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Annotations fetched successfully",
            "Could not fetch annotations",
        )
        if error:
            return {}, error
        if data is None:
            return (
                {},
                "",
                "No annotations , create one.",
            )
        items = data.get("items", [])
        annotations = {
            item["title"]: Annotation(
                self.session,
                annotation_id=item["_id"],
            )
            for item in items
        }
        return annotations, None

    def list_trained_models(self, page_size=10, page_number=0):
        """
        List model training sessions in the project with pagination.

        Returns
        -------
        tuple
            A tuple containing:
            - A paginated list of model training sessions if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> model_train_sessions, error = project.list_trained_models()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model training sessions: {model_train_sessions}")
        """
        path = f"/v1/model/model_train?projectId={self.project_id}&pageSize={page_size}&pageNumber={page_number}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Model train list fetched successfully",
            "Could not fetch models train list",
        )
        if error:
            return {}, error
        if data is None:
            return (
                {},
                "No models trained , create one.",
            )
        items = data.get("items", [])
        models = {
            item["modelTrainName"]: Model(self.session, model_id=item["_id"]) for item in items
        }
        return models, None

    def list_exported_models(self, page_size=10, page_number=0):
        """
        List all exported models in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of exported models if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> exported_models, error = project.list_exported_models()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Exported models: {exported_models}")
        """
        path = f"/v1/model/get_model_exports/v2?projectId={self.project_id}&pageSize={page_size}&pageNumber={page_number}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Model train list fetched successfully",
            "Could not fetch models train list",
        )
        if error:
            return {}, error
        if data is None:
            return (
                {},
                "No models exported , create one.",
            )
        items = data.get("items", [])
        exported_models = {
            item["modelExportName"]: ExportedModel(
                self.session,
                model_export_id=item["_id"],
            )
            for item in items
        }
        return exported_models, None

    def list_drift_monitorings(self, page_size=10, page_number=0):
        """
        Fetch a list of all drift monitorings.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = projects.list_drift_monitorings()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Drift Monitoring detail : {resp}")
        """
        print(self.project_id)
        path = f"/v1/inference/list_drift_monitorings?pageSize={page_size}&pageNumber={page_number}&projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Model train list fetched successfully",
            "Could not fetch models train list",
        )
        if error:
            return {}, error
        if data is None:
            return (
                {},
                "No drift monitorings done , create one.",
            )
        items = data.get("items", [])
        deployments = {}
        for item in items:
            if "deploymentName" in item and "_id" in item:
                deployments[item["deploymentName"]] = Deployment(
                    self.session,
                    deployment_id=item["_idDeployment"],
                )
            else:
                raise ValueError(
                    f"Missing required parameters for Deployment initialization in item: {item}"
                )
        return deployments, None

    def get_exported_models(self):
        """
        Fetch all model exports for the project.

        Returns
        -------
        tuple
            A tuple containing:
            - The model export data if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> model_exports, error = project.get_model_exports()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model exports: {model_exports}")
        """
        path = f"/v1/model/get_model_exports?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Model exports fetched successfully",
            "Could not fetch model exports",
        )

    def get_trained_models(self):
        path = f"/v1/model/model_train?projectId={self.project_id}&pageSize=10000&pageNumber=0"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Model trains fetched successfully",
            "Could not fetch model trains",
        )

    def get_dataset(self, dataset_id=None, dataset_name=""):
        """
        Get a Dataset instance.

        Parameters
        ----------
        dataset_id : str, optional
            The ID of the dataset.
        dataset_name : str, optional
            The name of the dataset.

        Returns
        -------
        Dataset
            A Dataset instance with the specified ID and/or name.

        Example
        -------
        >>> dataset = project.get_dataset(dataset_id="dataset123")
        >>> print(dataset)
        """
        return Dataset(self.session, dataset_id, dataset_name)

    def get_annotation(
        self,
        dataset_id=None,
        annotation_id=None,
        annotation_name="",
    ):
        """
        Get an Annotation instance.

        Parameters
        ----------
        dataset_id : str, optional
            The ID of the dataset associated with the annotation.
        annotation_id : str, optional
            The ID of the annotation.
        annotation_name : str, optional
            The name of the annotation.

        Returns
        -------
        Annotation
            An Annotation instance with the specified dataset ID, annotation ID, and/or name.

        Example
        -------
        >>> annotation = project.get_annotation(annotation_id="annotation123")
        >>> print(annotation)
        """
        return Annotation(
            self.session,
            dataset_id,
            annotation_id,
            annotation_name,
        )

    def get_model(self, model_id=None, model_name=""):
        """
        Get a Model instance.

        Parameters
        ----------
        model_id : str, optional
            The ID of the model.
        model_name : str, optional
            The name of the model.

        Returns
        -------
        Model
            A Model instance with the specified ID and/or name.

        Example
        -------
        >>> model = project.get_model(model_id="model123")
        >>> print(model)
        """
        return Model(self.session, model_id, model_name)

    def get_exported_model(
        self,
        model_export_id=None,
        model_export_name="",
    ):
        """
        Get an InferenceOptimization instance.

        Parameters
        ----------
        model_export_id : str, optional
            The ID of the model export.
        model_export_name : str, optional
            The name of the model export.

        Returns
        -------
        InferenceOptimization
            An InferenceOptimization instance with the specified ID and/or name.

        Example
        -------
        >>> inference_optimization = project.get_inference_optimization(model_export_id="export123")
        >>> print(inference_optimization)
        """
        return ExportedModel(
            self.session,
            model_export_id,
            model_export_name,
        )

    def get_deployment(
        self,
        deployment_id=None,
        deployment_name="",
    ):
        """
        Get a Deployment instance.

        Parameters
        ----------
        deployment_id : str, optional
            The ID of the deployment.
        deployment_name : str, optional
            The name of the deployment.

        Returns
        -------
        Deployment
            A Deployment instance with the specified ID and/or name.

        Example
        -------
        >>> deployment = project.get_deployment(deployment_id="deployment123")
        >>> print(deployment)
        """
        return Deployment(
            self.session,
            deployment_id,
            deployment_name,
        )

    def get_dataset_status_summary(self):
        """
        Get the dataset status summary for the project.

        Returns
        -------
        OrderedDict
            An ordered dictionary with dataset status and their counts.

        Example
        -------
        >>> dataset_status = project.get_dataset_status_summary()
        >>> print(dataset_status)
        """
        path = f"/v1/dataset/get_dataset_status?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Successfully fetched dataset status summary",
            "An error occurred while fetching dataset status summary",
        )
        if error:
            return OrderedDict(), error
        dataset_status_summary = OrderedDict(data.get("data", {}))
        return dataset_status_summary, None

    def get_annotations_status_summary(self):
        """
        Get the annotations status summary for the project.

        Returns
        -------
        OrderedDict
            An ordered dictionary with annotations status and their counts.

        Example
        -------
        >>> annotations_status = project.get_annotations_status_summary()
        >>> print(annotations_status)
        """
        path = f"/v1/annotations/summary?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Successfully fetched annotations status summary",
            "An error occurred while fetching annotations status summary",
        )
        if error:
            return OrderedDict(), error
        annotations_status_summary = OrderedDict(data.get("data", {}))
        return annotations_status_summary, None

    def get_model_status_summary(self):
        """
        Get the model status summary for the project.

        Returns
        -------
        OrderedDict
            An ordered dictionary with model status and their counts.

        Example
        -------
        >>> model_status = project.get_model_status_summary()
        >>> print(model_status)
        """
        path = f"/v1/model/summary?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Successfully fetched model status summary",
            "An error occurred while fetching model status summary",
        )
        if error:
            return OrderedDict(), error
        model_status_summary = OrderedDict(data.get("data", {}).get("modelCountByStatus", {}))
        model_status_summary["total"] = data.get("data", {}).get("total", 0)
        return model_status_summary, None

    def get_model_export_status_summary(self):
        """
        Get the model export status summary for the project.

        Returns
        -------
        OrderedDict
            An ordered dictionary with model export status and their counts.

        Example
        -------
        >>> model_export_status = project.get_model_export_status_summary()
        >>> print(model_export_status)
        """
        path = f"/v1/model/summaryExported?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Successfully fetched model export status summary",
            "An error occurred while fetching model export status summary",
        )
        if error:
            return OrderedDict(), error
        model_export_status_summary = OrderedDict(
            data.get("data", {}).get("modelCountByStatus", {})
        )
        model_export_status_summary["total"] = data.get("data", {}).get("total", 0)
        return model_export_status_summary, None

    def get_deployment_status_summary(self):
        """
        Get the deployment status summary for the project.

        Returns
        -------
        OrderedDict
            An ordered dictionary with deployment status and their counts.

        Example
        -------
        >>> deployment_status = project.get_deployment_status_summary()
        >>> print(deployment_status)
        """
        path = f"/v1/inference/summary?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Successfully fetched deployment status summary",
            "An error occurred while fetching deployment status summary",
        )
        if error:
            return OrderedDict(), error
        deployment_status_summary = OrderedDict(data.get("data", {}))
        return deployment_status_summary, None

    def _validate_labellers_and_reviewers(self, users_list):
        """
        Validate labellers and reviewers by ensuring they are collaborators and extracting their
            user IDs.

        Parameters
        ----------
        users_list : list
            A list of dictionaries, each containing 'email', 'name', and 'percentageWork'.

        Returns
        -------
        list
            A list of dictionaries containing '_idUser', 'name', and 'percentageWork'.

        Raises
        ------
        ValueError
            If a user is not added as a collaborator to the project.
        """
        collaborators, _, _ = self.list_collaborators()
        collaborator_map = {
            (
                collaborator.get("email"),
                collaborator.get("userName"),
            ): collaborator.get("_idUser")
            for collaborator in collaborators
        }
        validated_users = []
        for user in users_list:
            email = user.get("email")
            name = user.get("name")
            percentage_work = user.get("percentageWork")
            user_id = collaborator_map.get((email, name))
            if not user_id:
                raise ValueError(
                    f"The user with name '{name}' is not added as a collaborator to the project."
                )
            validated_users.append(
                {
                    "_idUser": user_id,
                    "name": name,
                    "percentageWork": int(percentage_work),
                }
            )
        return validated_users
