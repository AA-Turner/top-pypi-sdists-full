"""Module providing models functionality."""

import sys
from datetime import datetime, timedelta
import requests

from matrice.dataset import Dataset
from matrice.utils import handle_response


class Model:
    """
    The `Model` class provides methods for interacting with models in a project,
    including fetching summaries, listing models, and performing evaluations.

    Parameters
    ----------
    session : Session
        A session object containing the project ID and RPC client.
    model_id : str, optional
        The unique identifier for the model (default is None).
    model_name : str, optional
        The name of the model (default is an empty string).

    Example
    -------
    >>> session = Session(project_id="project123")
    >>> model = Model(session, model_id="model789")
    """

    def __init__(
        self,
        session,
        model_id=None,
        model_name="",
    ):
        """Initialize Model class."""
        self.session = session
        self.project_id = session.project_id
        self.last_refresh_time = datetime.now()
        assert model_id or model_name, "Either model_id or model_name must be provided"
        self.model_id = model_id
        self.model_name = model_name
        self.rpc = session.rpc
        details_response, _, _ = self.get_details()
        self.details = details_response
        self.model_id = details_response.get("_id")
        self.dataset_id = details_response.get("_idDataset")
        self.model_arch_id = details_response.get("_idModelArch")
        self.action_status_id = details_response.get("_idActionStatus")
        self.model_family_id = details_response.get("_idModelFamily")
        self.project_id = details_response.get("_idProject")
        self.user_name = details_response.get("userName")
        self.user_id = details_response.get("_idUser")
        self.model_key = details_response.get("modelKey")
        self.model_family_name = details_response.get("modelName")
        self.auto_ml = details_response.get("autoML")
        self.params_millions = details_response.get("paramsInMillion")
        self.tuning_type = details_response.get("tuningType")
        self.training_framework = details_response.get("trainingFramework")
        self.model_checkpoint = details_response.get("modelCheckpoint")
        self.checkpoint_type = details_response.get("checkpointType")
        self.primary_metric = details_response.get("primaryMetric")
        self.test_score = details_response.get("testScore")
        self.val_score = details_response.get("valScore")
        self.dataset_name = details_response.get("datasetName")
        self.status = details_response.get("status")
        self.dataset_version = details_response.get("datasetVersion")
        self.model_inputs = details_response.get("modelInputs", [])
        self.model_outputs = details_response.get("modelOutputs", [])
        self.target_runtime = details_response.get("targetRuntime", [])
        self.action_config = details_response.get("actionConfig", {})
        self.model_config = details_response.get("modelConfig", {})
        self.model_name = details_response.get("modelTrainName")
        self.val_split_result = details_response.get("valSplitResult", [])
        self.test_split_result = details_response.get("testSplitResult", [])
        self.index_to_cat = details_response.get("indexToCat", {})
        self.best_epoch = details_response.get("bestEpoch")
        self.cloud_path = details_response.get("cloudPath")
        self.created_at = details_response.get("createdAt")
        self.updated_at = details_response.get("updatedAt")
        self.architecture = details_response.get("modelKey")

    def refresh(self):
        """Refresh the instance by reinstantiating it with the previous values."""
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise ValueError(
                "Refresh can only be called after two minutes since the last refresh."
            )
        self.__dict__.copy()
        init_params = {
            "session": self.session,
            "model_name": self.model_name,
        }
        self.__init__(**init_params)
        self.last_refresh_time = datetime.now()

    def get_details(self):
        """
        Get model details based on the provided ID or name.

        Returns
        -------
        tuple
            A tuple containing the model details, error message, and status message.

        Example
        -------
        >>> details, error, message = model.get_details()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model details: {details}")
        """
        model_id = self.model_id
        name = self.model_name
        if model_id:
            try:
                return self._get_model_train_by_id()
            except Exception as err:
                print(f"Error retrieving model train by id: {err}")
        elif name:
            try:
                return self._get_model_train_by_name()
            except Exception as err:
                print(f"Error retrieving model train by name: {err}")
        else:
            raise ValueError("At least one of 'model_id' or 'model_name' must be provided.")
        return None, None, None

    def rename(self, name):
        """
        Update the name of the trained model.

        Parameters
        ----------
        name : str
            The new name for the trained model.

        Returns
        -------
        tuple
            A tuple with the update result, error message, and status message.

        Example
        -------
        >>> result, error, message = model.rename("NewModelName")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model name updated: {result}")
        """
        if self.model_id is None:
            print("Set Model Id for model object")
            sys.exit(0)
        path = f"/v1/model/{self.model_id}/update_modelTrain_name"
        headers = {"Content-Type": "application/json"}
        model_payload = {
            "modelTrainId": self.model_id,
            "name": name,
        }
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=model_payload,
        )
        return handle_response(
            resp,
            "Model train name updated successfully",
            "Could not update model train name",
        )

    def delete(self):
        """
        Delete the trained model.

        Returns
        -------
        tuple
            A tuple with the deletion result, error message, and status message.

        Example
        -------
        >>> result, error, message = model.delete()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model deleted: {result}")
        """
        if self.model_id is None:
            print("Set Model Id for model object")
            sys.exit(0)
        path = f"/v1/model/delete_model_train/{self.model_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Model train deleted successfully",
            "Could not delete model train",
        )

    def get_prediction(self, input_path):
        """
        Tests a trained model for a given image.

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
        >>> result, error, message = model.test_model("/path/to/test_image.jpg")
        >>> print(result)
        {'test_result': 'success', 'confidence': 0.85}
        """
        with open(input_path, "rb") as input_file:
            files = {"input": input_file}
            url = f"/v1/model_prediction/model_test/{self.model_id}?projectId={self.project_id}"
            resp = self.rpc.post(url, files=files)
            success_message = "Model test completed successfully"
            error_message = "An error occurred while testing the model."
            return handle_response(
                resp,
                success_message,
                error_message,
            )

    def get_eval_result(
        self,
        dataset_id,
        dataset_version,
        split_type,
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
        split_type : str
            The type of split used for the evaluation.

        Returns
        -------
        tuple
            A tuple with the evaluation result, error message, and status message.

        Example
        -------
        >>> eval_result, error, message = model.get_eval_result("dataset123", "v1.0", "train")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Evaluation result: {eval_result}")
        """
        dataset = Dataset(self.session, dataset_id)
        dataset_info, _, _ = dataset.get_processed_versions()
        if dataset_info is None:
            print("No datasets found")
            sys.exit(0)
        flag = False
        for data_info in dataset_info:
            if dataset_id == data_info["_id"]:
                if dataset_version in data_info["processedVersions"]:
                    flag = True
                    break
        if not flag:
            print(
                "Dataset or Dataset version does not exist. Can not use this dataset version to get/create a eval."
            )
            sys.exit(0)
        if self.model_id is None:
            print("Model Id is required for this operation")
            sys.exit(0)
        path = "/v1/model/get_eval_result"
        headers = {"Content-Type": "application/json"}
        model_payload = {
            "_idDataset": dataset_id,
            "_idModel": self.model_id,
            "datasetVersion": dataset_version,
            "splitType": split_type,
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

    def plot_eval_results(self):
        """
        Plot the evaluation results for the model.

        Example
        -------
        >>> model.plot_eval_results()
        """
        import matplotlib.pyplot as plt
        import pandas as pd
        import seaborn as sns

        eval_result = self.get_eval_result(
            dataset_id=self.dataset_id,
            dataset_version=self.dataset_version,
            split_type=["train", "val", "test"],
        )[0]
        df_results = pd.DataFrame(eval_result)
        plt.figure(figsize=(14, 12))
        metrics = df_results["metricName"].unique()
        num_metrics = len(metrics)
        for i, metric in enumerate(metrics, 1):
            plt.subplot((num_metrics + 1) // 2, 2, i)
            metric_data = df_results[df_results["metricName"] == metric]
            sns.barplot(
                data=metric_data,
                x="metricValue",
                y="splitType",
                hue="category",
                orient="h",
            )
            plt.xlabel(metric)
            plt.xlim(0, 1)
            plt.legend(title="Category")
        plt.tight_layout()
        plt.show()

    def _get_model_train_by_id(self):
        """
        Fetch details of a specific trained model by its ID.

        Returns
        -------
        tuple
            A tuple with the model training data, error message, and status message.

        Example
        -------
        >>> model_data, error, message = model._get_model_train_by_id()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model data: {model_data}")
        """
        path = f"/v1/model/model_train/{self.model_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Model train by ID fetched successfully",
            "Could not fetch model train by ID",
        )

    def _get_model_train_by_name(self):
        """
        Fetch details of a specific trained model by its name.

        Returns
        -------
        tuple
            A tuple with the model training data, error message, and status message.

        Example
        -------
        >>> model_data, error, message = model._get_model_train_by_name()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model data: {model_data}")
        """
        if not self.model_name:
            print(
                "Model name not set for this Model train. Cannot perform the operation for Model without model name"
            )
            sys.exit(0)
        path = f"/v1/model/model_train/get_model_train_by_name?modelTrainName={self.model_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Model train by name fetched successfully",
            "Could not fetch model train by name",
        )

    def add_evaluation(
        self,
        dataset_id,
        dataset_version,
        split_types,
        is_pruned=False,
        is_gpu_required=False,
    ):
        """
        Add a new model evaluation using specified parameters.

        Parameters
        ----------
        dataset_id : str
            The ID of the dataset.
        dataset_version : str
            The version of the dataset.
        split_types : list
            The split types used in the evaluation.
        is_pruned : bool, optional
            Whether the model is pruned (default is False).
        is_gpu_required : bool, optional
            Whether the model requires a GPU (default is False).

        Returns
        -------
        tuple
            A tuple with the evaluation result, error message, and status message.

        Example
        -------
        >>> result, error, message = model.add_model_eval(
        >>>     id_dataset="dataset123",
        >>>     dataset_version="v1.0",
        >>>     split_types=["train", "val"],
        >>> )
        """
        if self.model_id is None:
            print("Set Model Id for model object")
            sys.exit(0)
        _, _, _ = self._get_model_train_by_id()
        path = "/v1/model/add_model_eval"
        headers = {"Content-Type": "application/json"}
        model_payload = {
            "_idModel": self.model_id,
            "_idProject": self.project_id,
            "isOptimized": False,
            "isPruned": is_pruned,
            "runtimeFramework": "Pytorch",
            "_idDataset": dataset_id,
            "datasetVersion": dataset_version,
            "gpuRequired": is_gpu_required,
            "splitTypes": split_types,
            "modelType": "trained",
            "exportFormat": None,
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
        >>> download_path, error, message = model.get_model_download_path("trained")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Download path: {download_path}")
        """
        if self.model_id is None:
            print(
                "Model id not set for this model. Cannot perform the operation for model without model id"
            )
            sys.exit(0)
        path = "/v1/model/get_model_download_path"
        headers = {"Content-Type": "application/json"}
        model_payload = {
            "modelID": self.model_id,
            "modelType": "trained",
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
        >>> result, error, message = model.download_model("model.pth", model_type="trained")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model downloaded: {result}")
        """
        presigned_url = self.rpc.post(
            path="/v1/model/get_model_download_path",
            payload={
                "modelID": self.model_id,
                "modelType": "trained",
                "expiryTimeInMinutes": 59,
            },
        )["data"]
        response = requests.get(presigned_url, timeout=30)
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                file.write(response.content)
            print("Model downloaded successfully")
            return file_name
        print(f"Model download failed with status code: {response.status_code}")
        return ""

    def get_model_training_logs(self):
        """
        Fetch training logs for the specified model.

        This method retrieves the logs of the training epochs for a model, including
        both training and validation metrics such as losses and accuracy.

        Returns
        -------
        tuple
            A tuple containing:
            - A dictionary with the response from the RPC call.
            - An error message if the request fails.
            - A success message if the request succeeds.

        Example
        -------
        >>> response, error, message = model_logging.get_model_training_logs()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Success: {message}")
        """
        path = f"/v1/model_logging/model/{self.model_id}/train_epoch_logs"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            error = None
            message = "Successfully fetched model logs."
        else:
            error = resp.get("message")
            message = "Failed to fetch model logs."
        return resp, error, message

    def plot_epochs_losses(self):
        """
        Plot training and validation losses over epochs.

        This method generates two subplots: one for the training losses and one for
        the validation losses, displaying how these metrics evolve over the epochs.

        Returns
        -------
        None

        Example
        -------
        >>> model_logging.plot_epochs_losses()
        """
        import matplotlib.pyplot as plt
        import seaborn as sns

        resp, _, _ = self.get_model_training_logs()
        training_logs = resp["data"]
        epochs = []
        metrics = {"train": {}, "val": {}}
        for epoch_data in training_logs:
            epochs.append(epoch_data["epoch"])
            for detail in epoch_data["epochDetails"]:
                metric_name = detail["metricName"]
                metric_value = detail["metricValue"]
                split_type = detail["splitType"]
                if "loss" in metric_name:
                    if split_type not in metrics:
                        metrics[split_type] = []
                    if metric_name not in metrics[split_type]:
                        metrics[split_type][metric_name] = []
                    metrics[split_type][metric_name].append(metric_value)
        sns.set(style="whitegrid")
        fig, axs = plt.subplots(2, 1, figsize=(12, 18))
        for (
            split_type,
            split_metrics,
        ) in metrics.items():
            for metric_name in split_metrics:
                if split_type == "train":
                    axs[0].plot(
                        epochs,
                        split_metrics[metric_name],
                        label=f"{split_type} {metric_name}",
                    )
                elif split_type == "val":
                    axs[1].plot(
                        epochs,
                        split_metrics[metric_name],
                        label=f"{split_type} {metric_name}",
                    )
        axs[0].set_xlabel("Epoch", fontsize=14)
        axs[0].set_ylabel("Loss", fontsize=14)
        axs[0].legend(fontsize=12)
        axs[0].set_title(
            "Training Losses over Epochs",
            fontsize=16,
        )
        axs[0].grid(True)
        axs[1].set_xlabel("Epoch", fontsize=14)
        axs[1].set_ylabel("Loss", fontsize=14)
        axs[1].legend(fontsize=12)
        axs[1].set_title(
            "Validation Losses over Epochs",
            fontsize=16,
        )
        axs[1].grid(True)
        plt.tight_layout()
        plt.show()

    def plot_epochs_metrics(self):
        """
        Plot training and validation metrics (excluding losses) over epochs.

        This method generates subplots for each non-loss metric, such as accuracy,
        showing how these metrics change during training epochs for both training
        and validation splits.

        Returns
        -------
        None

        Example
        -------
        >>> model_logging.plot_epochs_metrics()
        """
        import matplotlib.pyplot as plt
        import seaborn as sns

        resp, _, _ = self.get_model_training_logs()
        training_logs = resp["data"]
        epochs = []
        metrics = {"train": {}, "val": {}}
        metrics_names = set()
        for epoch_data in training_logs:
            epochs.append(epoch_data["epoch"])
            for detail in epoch_data["epochDetails"]:
                metric_name = detail["metricName"]
                metric_value = detail["metricValue"]
                split_type = detail["splitType"]
                if "loss" not in metric_name:
                    if split_type not in metrics:
                        metrics[split_type] = []
                    if metric_name not in metrics[split_type]:
                        metrics[split_type][metric_name] = []
                    metrics[split_type][metric_name].append(metric_value)
                    metrics_names.add(metric_name)
        metrics_names = list(metrics_names)
        num_graphs = len(metrics_names)
        sns.set(style="whitegrid")
        fig, axs = plt.subplots(num_graphs, 1, figsize=(12, 18))
        for (
            metric_index,
            metric_name,
        ) in enumerate(metrics_names):
            for (
                split_type,
                split_metrics,
            ) in metrics.items():
                if metric_name in metrics[split_type]:
                    axs[metric_index].plot(
                        epochs,
                        split_metrics[metric_name],
                        label=f"{split_type} {metric_name}",
                    )
            axs[metric_index].set_xlabel("Epoch", fontsize=14)
            axs[metric_index].set_ylabel(metric_name, fontsize=14)
            axs[metric_index].legend(fontsize=12)
            axs[metric_index].set_title(
                f"{metric_name} over Epochs",
                fontsize=16,
            )
            axs[metric_index].grid(True)
        plt.tight_layout()
        plt.show()

    def model_test(self, model_type="trained"):
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
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Examples
        --------
        >>> resp, err, msg = model.model_test("trained")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Deployment server details : {resp}")
        """
        path = f"/v1/inference/get_deploy_server/{self.model_id}/{model_type}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Deployment server fetched successfully",
            "An error occurred while trying to fetch deployment server.",
        )
