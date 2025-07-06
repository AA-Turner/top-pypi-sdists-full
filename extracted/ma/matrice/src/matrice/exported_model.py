"""Module providing exported_model functionality."""

import sys
from matrice.utils import (
    handle_response,
    get_summary,
)
from datetime import datetime, timedelta
import requests


class ExportedModel:
    """
    A class to handle operations related to model export within a project.

    The `ExportedModel` class facilitates managing model export processes,
    including fetching summaries, listing available exported models, and performing
    evaluation tasks on optimized inferences.

    Parameters
    ----------
    session : Session
        An active session object that holds project information such as the project ID and RPC
            client.
    model_export_id : str, optional
        A unique identifier for the model export or inference optimization. Defaults to None.
    model_export_name : str, optional
        The name of the model export or inference optimization. Defaults to an empty string.

    Attributes
    ----------
    project_id : str
        The project ID associated with the current session.
    model_export_id : str or None
        The unique identifier for the model export, provided at initialization or set later.
    model_export_name : str
        The name of the model export, provided at initialization or set later.
    rpc : object
        The RPC client used to make API requests.

    Example
    -------
    >>> session = Session(account_number=account_number)
    >>> exported_model = ExportedModel(session=session, model_export_id="12345", model_export_name="sample_export")
    >>> print(exported_model.model_export_name)  # Output: "sample_export"
    """

    def __init__(
        self,
        session,
        model_export_id=None,
        model_export_name="",
    ):
        self.session = session
        self.project_id = session.project_id
        self.last_refresh_time = datetime.now()
        assert (
            model_export_id or model_export_name
        ), "At least one of 'model_export_id' or 'model_export_name' must be provided."
        self.model_export_id = model_export_id
        self.model_export_name = model_export_name
        self.rpc = session.rpc
        (
            self.summary_response,
            self.err,
            self.msg,
        ) = get_summary(
            self.session,
            self.project_id,
            service_name="exports",
        )
        if self.summary_response:
            summary_data = self.summary_response
            model_count_by_status = summary_data.get("modelCountByStatus", {})
            self.error_model_count = model_count_by_status.get("error", 0)
            self.exported_model_count = model_count_by_status.get("exported", 0)
            self.exporting_model_count = model_count_by_status.get("exporting", 0)
            self.queued_model_count = model_count_by_status.get("queued", 0)
            self.total_models = summary_data.get("total", 0)
        else:
            print(f"Error fetching summary: {self.summary_response.get('message')}")
        details_response, err, msg = self.get_details()
        self.details = details_response
        self.model_train_id = details_response.get("_idModelTrain")
        self.model_train_name = details_response.get("modelTrainName")
        self.dataset_name = details_response.get("datasetName")
        self.model_name = details_response.get("modelName")
        self.model_inputs = details_response.get("modelInputs", [])
        self.model_arch_id = details_response.get("_idModelArch")
        self.user_id = details_response.get("_idUser")
        self.user_name = details_response.get("userName")
        self.model_export_name = details_response.get("modelExportName")
        self.model_outputs = details_response.get("modelOutputs", [])
        self.export_format = details_response.get("exportFormat")
        self.dataset_id = details_response.get("_idDataset")
        self.project_id = details_response.get("_idProject")
        self.action_id = details_response.get("_idAction")
        self.dataset_version = details_response.get("datasetVersion")
        self.gpu_required = details_response.get("gpuRequired")
        self.action_config = details_response.get("actionConfig", {})
        self.model_config = details_response.get("modelConfig", {})
        self.val_split_results = details_response.get("valSplitResults", [])
        self.test_split_results = details_response.get("testSplitStruct", [])
        self.status = details_response.get("status")
        self.cloud_path = details_response.get("cloudPath")
        self.created_at = details_response.get("createdAt")
        self.baseModel = details_response.get("modelTrainName")
        self.architecture = details_response.get("modelName")
        self.training_framework = details_response.get("trainingFramework")
        self.lastUpdated = details_response.get("updatedAt")

    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise Exception("Refresh can only be called after two minutes since the last refresh.")
        self.__dict__.copy()
        init_params = {
            "session": self.session,
            "model_export_name": self.model_export_name,
        }
        self.__init__(**init_params)
        self.last_refresh_time = datetime.now()

    def get_details(self):
        """
        Retrieve details of the model export based on the model export ID or name.

        This method fetches details by ID if available; otherwise, it attempts
        to fetch by name. Raises a ValueError if neither identifier is provided.

        Returns
        -------
        tuple
            A tuple containing the model export details, error message (if any), and a status
                message.

        Raises
        ------
        ValueError
            If neither 'model_export_id' nor 'model_export_name' is provided.

        Example
        -------
        >>> details, err, msg = exported_model.get_details()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Details: {details}")
        """
        id = self.model_export_id
        name = self.model_export_name
        if id:
            try:
                return self._get_model_export_by_id()
            except Exception as e:
                print(f"Error retrieving model_export by id: {e}")
        elif name:
            try:
                return self._get_model_export_by_name()
            except Exception as e:
                print(f"Error retrieving model_export by name: {e}")
        else:
            raise ValueError(
                "At least one of 'model_export_id' or 'model_export_name' must be provided."
            )

    def _get_model_export_by_id(self):
        """
        Fetch details of a specific model export by its ID.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> details, err, msg = exported_model._get_model_export_by_id()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Details: {details}")
        """
        path = f"/v1/model/get_model_export_by_id?modelExportId={self.model_export_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Model export by ID fetched successfully",
            "Could not fetch model export by ID",
        )

    def _get_model_export_by_name(self):
        """
        Fetch details of a specific model export by its name.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> details, err, msg = exported_model._get_model_export_by_name()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Details: {details}")
        """
        if self.model_export_name == "":
            print(
                "Model export name not set for this Model export. Cannot perform the operation for Model export without model export name."
            )
            sys.exit(0)
        path = f"/v1/model/model_export/get_model_export_by_name?modelExportName={self.model_export_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Model export by name fetched successfully",
            "Could not fetch model export by name",
        )

    def rename(self, updated_name):
        """
        Update the name of a model export.

        Parameters
        ----------
        updated_name : str
            The new name for the model export.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> result, err, msg = exported_model.rename("NewModelExportName")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Name Updated: {result}")
        """
        body = {
            "modelExportId": self.model_export_id,
            "name": updated_name,
        }
        headers = {"Content-Type": "application/json"}
        path = f"/v1/model/{self.model_export_id}/update_modelExport_name"
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            f"Model export name updated to {updated_name}",
            "Could not update the model export name",
        )

    def delete(self):
        """
        Delete a model export.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> result, err, msg = exported_model.delete()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Deleted: {result}")
        """
        path = f"/v1/model/model_export/{self.model_export_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Model export deleted",
            "Could not delete the model export",
        )

    def add_evaluation(
        self,
        dataset_id,
        dataset_version,
        split_types,
        is_gpu_required=True,
        is_pruned=False,
    ):
        """
        Add a new model evaluation using specified parameters.

        Parameters
        ----------
        is_pruned : bool
            Whether the model is pruned.
        id_dataset : str
            The ID of the dataset used for evaluation.
        dataset_version : str
            The version of the dataset.
        is_gpu_required : bool
            Whether the model requires GPU for inference.
        split_types : list
            A list of split types used in the evaluation.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> eval_result, err, msg = exported_model.add_evaluation(
                is_pruned=False,
                id_dataset="dataset123", dataset_version="v1.0",
                is_gpu_required=True, split_types=["train", "test"])
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Evaluation added: {eval_result}")
        """
        model_info, err, msg = self.get_details()
        runtime_framework = model_info["exportFormat"]
        model_train_info, err, msg = self.get_trained_model()
        path = "/v1/model/add_model_eval"
        headers = {"Content-Type": "application/json"}
        model_payload = {
            "_idModel": self.model_export_id,
            "_idProject": self.project_id,
            "isOptimized": True,
            "isPruned": is_pruned,
            "runtimeFramework": runtime_framework,
            "_idDataset": dataset_id,
            "datasetVersion": dataset_version,
            "gpuRequired": is_gpu_required,
            "splitTypes": split_types,
            "modelType": "exported",
            "computeAlias": "",
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=model_payload,
        )
        return handle_response(
            resp,
            "Model eval added successfully",
            "An error occurred while adding model eval",
        )

    def get_trained_model(self):
        """
        Fetch details of a model training associated with a specific export ID.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> training_data, err, msg = exported_model.get_model_train_of_the_export()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Training Data: {training_data}")
        """
        path = f"/v1/model/get_model_train_by_export_id?exportId={self.model_export_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Model train by export ID fetched successfully",
            "Could not fetch model train by export ID",
        )

    def get_evaluation_result(
        self,
        dataset_id,
        dataset_version,
        split_types,
    ):
        """
        Fetch the evaluation result of a trained model using a specific dataset version and split
            type.

        Parameters
        ----------
        dataset_id : str
            The ID of the dataset.
        dataset_version : str
            The version of the dataset.
        split_type : list
            The types of splits used for the evaluation.

        Returns
        -------
        tuple
            A tuple with the evaluation result, error message, and status message.

        Example
        -------
        >>> eval_result, error, message = exported_model.get_evaluation_result("dataset123", "v1.0",
        ["train"])
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Evaluation result: {eval_result}")
        """
        path = "/v1/model/get_eval_result"
        headers = {"Content-Type": "application/json"}
        model_payload = {
            "_idDataset": dataset_id,
            "_idModel": self.model_export_id,
            "datasetVersion": dataset_version,
            "splitType": split_types,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=model_payload,
        )
        return handle_response(
            resp,
            "Eval result fetched successfully",
            "An error occurred while fetching Eval result",
        )

    def get_prediction(self, input_path):
        """
        Tests a exported model for a given image.

        Parameters:
        -----------
        input_path : str
            The path to the input for testing.

        Returns:
        --------
        tuple:
            A tuple consisting of (result, error, message) with the test results.

        Example:
        --------
        >>> result, error, message = exported_model.get_prediction("/path/to/test_image.jpg")
        >>> print(result)
        {'test_result': 'success', 'confidence': 0.85}
        """
        files = {"input": open(input_path, "rb")}
        url = f"/v1/model_prediction/model_test/{self.model_arch_id}?projectId={self.project_id}"
        resp = self.rpc.post(url, files=files)
        success_message = "Model test completed successfully"
        error_message = "An error occurred while testing the model."
        return handle_response(resp, success_message, error_message)

    def get_download_path(self):
        """
        Get the download path for the specified model type. There are 2 types of model types:
            trained and exported.

        Parameters
        ----------
        model_type : str
            The type of the model to download.

        Returns
        -------
        tuple
            A tuple with the download path, error message, and status message.

        Example
        -------
        >>> download_path, error, message = exported_model.get_model_download_path()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Download path: {download_path}")
        """
        if self.model_export_id is None:
            print(
                "Model id not set for this model. Cannot perform the operation for model without model id"
            )
            sys.exit(0)
        path = "/v1/model/get_model_download_path"
        headers = {"Content-Type": "application/json"}
        model_payload = {
            "modelID": self.model_export_id,
            "modelType": "exported",
            "expiryTimeInMinutes": 15,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=model_payload,
        )
        return handle_response(
            resp,
            "Model download path fetched successfully and it will expire in 15 mins",
            "An error occured while downloading the model",
        )

    def download_model(self, file_name):
        """
        Download the specified model type to a local file. There are 2 types of model types:
            trained and exported.

        Parameters
        ----------

        file_name : str
            The name of the file to save the downloaded model.
        model_type : str
            The type of the model to download. Default is "trained".

        Returns
        -------
        tuple
            A tuple with the download status, error message, and status message.

        Example
        -------
        >>> result, error, message = exported_model.download_model("model.pth")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model downloaded: {result}")
        """
        presigned_url = self.rpc.post(
            path="/v1/model/get_model_download_path",
            payload={
                "modelID": self.model_export_id,
                "modelType": "exported",
                "expiryTimeInMinutes": 59,
                "exportFormat": self.export_format,
            },
        )["data"]
        response = requests.get(presigned_url, timeout=30)
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                file.write(response.content)
            print("Model downloaded successfully")
            return file_name
        else:
            print(f"Model download failed with status code: {response.status_code}")
            return ""
