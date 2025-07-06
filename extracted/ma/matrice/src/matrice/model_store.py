"""Module providing model_store functionality."""

from matrice.utils import handle_response
import os
import json
import requests
import time
from datetime import datetime, timedelta


def list_public_model_families(
    session,
    project_type="classification",
    page_size=10,
    page_num=0,
):
    """
    Fetch public model families for a given project.

    Parameters
    ----------
    project_type : str, optional
        The type of the project (default is "classification")(Available types are "detection" and "instance_segmentation").
    page_size : int, optional
        The number of model families to fetch per page (default is 10).
    page_num : int, optional
        The page number to fetch (default is 0).

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = list_public_model_families(session,"classification")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Public model families: {resp}")
    """
    path = f"/v1/model_store/list_public_model_families?projectType={project_type}&pageSize={page_size}&pageNum={page_num}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        "Successfully fetched all public model families",
        "An error occurred while fetching the public model families",
    )


def list_private_model_families(
    session,
    project_id=None,
    project_name=None,
    page_size=10,
    page_num=0,
):
    """
    Fetch private model families for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_name : str
        The name of the project.
    page_size : int, optional
        The number of model families to fetch per page (default is 10).
    page_num : int, optional
        The page number to fetch (default is 0).

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = list_private_model_families(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Private model families: {resp}")
    """
    assert project_id is not None or project_name is not None
    path = f"/v1/model_store/list_private_model_families?projectId={project_id}&pageSize={page_size}&pageNum={page_num}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        "Successfully fetched all private model families",
        "An error occurred while fetching the private model families",
    )


def list_public_model_archs(
    session,
    project_type="classification",
    page_size=10,
    page_num=0,
):
    """
    Fetch public model architectures for a given project.

    Parameters
    ----------
    project_type : str, optional
        The type of the project (default is "classification")(Available types are "detection" and "instance_segmentation").
    page_size : int, optional
        The number of model architectures to fetch per page (default is 10).
    page_num : int, optional
        The page number to fetch (default is 0).

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = list_public_model_archs(session,"classification")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Public model architectures: {resp}")
    """
    path = f"/v1/model_store/list_public_model_archs?projectType={project_type}&pageSize={page_size}&pageNum={page_num}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        "Successfully fetched all public model architectures",
        "An error occurred while fetching the public model architectures",
    )


def list_private_model_archs(
    session,
    project_id=None,
    project_name=None,
    page_size=10,
    page_num=0,
):
    """
    Fetch private model architectures for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_name : str
        The name of the project.
    page_size : int, optional
        The number of model architectures to fetch per page (default is 10).
    page_num : int, optional
        The page number to fetch (default is 0).

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = list_private_model_archs(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Private model architectures: {resp}")
    """
    assert project_id is not None or project_name is not None
    path = f"/v1/model_store/list_private_model_archs?projectId={project_id}&pageSize={page_size}&pageNum={page_num}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        "Successfully fetched all private model architectures",
        "An error occurred while fetching the private model architectures",
    )


def get_all_models(
    session,
    project_id=None,
    project_name=None,
    project_type="classification",
):
    """
    Fetch all models for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_type : str, optional
        The type of the project (default is "classification")(Available types are "detection" and "instance_segmentation").

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = get_all_models(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"All models: {resp}")
    """
    path = f"/v1/model_store/get_all_models?projectId={project_id}&projectType={project_type}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        "Successfully fetched all model infos",
        "An error occurred while fetching the model family",
    )


def get_all_model_families(
    session,
    project_id,
    project_name=None,
    project_type="classification",
):
    """
    Fetch all model families for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_type : str, optional
        The type of the project (default is "classification").

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = get_all_model_families(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"All model families: {resp}")
    """
    path = (
        f"/v1/model_store/get_all_model_families?projectId={project_id}&projectType={project_type}"
    )
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        "Successfully fetched all model families",
        "An error occurred while fetching the model families",
    )


def byom_status_summary(session, project_id, project_name):
    """
    Fetch the BYOM (Bring Your Own Model) status summary for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_name : str
        The name of the project.

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = byom_status_summary(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"BYOM status summary: {resp}")
    """
    path = f"/v1/model_store/byom_status_summary?projectId={project_id}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        "Successfully fetched the BYOM status summary",
        "An error occurred while fetching the BYOM status summary",
    )


def check_family_exists_by_name(session, family_name):
    """
    Check if a model family exists by its name.

    Parameters
    ----------
    session : Session
        The session object containing authentication information.
    family_name : str
        The name of the model family to check.

    Returns
    -------
    bool
        True if the model family exists, False otherwise.

    Example
    -------
    >>> session = Session(account="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
    >>> family_name = "ResNet"
    >>> exists = check_family_exists_by_name(session, family_name)
    >>> if exists:
    >>>     print(f"The model family '{family_name}' exists.")
    >>> else:
    >>>     print(f"The model family '{family_name}' does not exist.")
    """
    path = f"/v1/model_store/check_family_exists_by_name?familyName={family_name}"
    resp = session.rpc.get(path=path)
    data, error, message = handle_response(
        resp,
        "Successfully checked model family existence",
        "An error occurred while checking model family existence",
    )
    if error:
        return False
    return data.get("exists", False)


def fetch_supported_runtimes_metrics(
    session,
    project_id,
    model_inputs,
    model_outputs,
):
    """
    Fetch supported runtimes and metrics for a given project.

    Parameters
    ----------
    model_inputs : list
        List of model inputs.
    model_outputs : list
        List of model outputs.

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = fetch_supported_runtimes_metrics(session,["image"], ["classification"])
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Supported runtimes and metrics: {resp}")
    """
    path = f"/v1/model_store/fetch_supported_runtimes_metrics?projectId={project_id}"
    payload = {
        "modelInputs": model_inputs,
        "modelOutputs": model_outputs,
    }
    headers = {"Content-Type": "application/json"}
    resp = session.rpc.post(
        path=path,
        headers=headers,
        payload=payload,
    )
    data, error, message = handle_response(
        resp,
        "Successfully fetched supported runtimes and metrics",
        "An error occurred while fetching supported runtimes and metrics",
    )
    if error:
        return data, error, message
    return data, error, message


def get_automl_config(
    session,
    project_id,
    model_count,
    recommended_runtime,
    performance_tradeoff,
    tuning_type="auto",
):
    """
    Generate AutoML configurations for model training based on specified parameters.

    This static method fetches recommended model configurations from the backend and
    processes them into a format suitable for model training. It calculates the
    number of model variants based on hyperparameter combinations.

    Parameters
    ----------
    session : Session
        Active session object for making API calls
    project_id : str
        Identifier for the project
    model_count : int
        Number of models to request configurations for
    recommended_runtime : bool
        Flag to indicate whether to only include models within recommended runtime
    performance_tradeoff : float
        Value indicating the trade-off between performance and resource usage
    tuning_type : str, optional
        Type of hyperparameter tuning strategy (default: "auto")

    Returns
    -------
    tuple
        A tuple containing three elements:
        - model_archs (list): List of ModelArch instances for recommended models
        - configs (list): List of configuration dictionaries for each model
          Each config contains:
            - is_autoML (bool): Set to True for AutoML
            - tuning_type (str): Type of tuning strategy
            - model_checkpoint (str): Checkpoint configuration
            - checkpoint_type (str): Type of checkpoint
            - action_config (dict): Raw configuration parameters
            - model_config (dict): Processed configuration values
        - model_counts (list): List of integers representing the number of
          model variants for each model based on hyperparameter combinations

    Example
    -------
    >>> session = Session()
    >>> model_archs, configs, counts = get_automl_config(
    ...     session=session,
    ...     project_id="project123",
    ...     model_count=5,
    ...     recommended_runtime=True,
    ...     performance_tradeoff=0.7
    ... )
    >>> for arch, config, count in zip(model_archs, configs, counts):
    ...     print(f"Model: {arch.model_key}, Variants: {count}")
    ...     print(f"Config: {config}")

    Notes
    -----
    The number of model variants (model_counts) is calculated by multiplying the
    number of unique values for batch size, epochs, and learning rate for each model.
    This represents the total number of training configurations that will be generated
    for each model architecture.
    """
    payload = {
        "_idProject": project_id,
        "recommendedOnly": recommended_runtime,
        "modelCount": model_count,
        "performanceTradeof": performance_tradeoff,
        "searchType": tuning_type,
    }
    path = f"/v1/model_store/get_recommended_models/v2?projectId={project_id}"
    headers = {"Content-Type": "application/json"}
    resp = session.rpc.post(
        path=path,
        headers=headers,
        payload=payload,
    )
    data, error, message = handle_response(
        resp,
        "Successfully fetched recommended models",
        "An error occurred while fetching recommended models",
    )
    if error:
        return [], [], []
    model_archs = []
    configs = []
    model_counts = []
    for model_data in data:
        model_key = model_data.get("modelKey")
        model_family_name = model_data.get("modelFamilyName")
        action_config_list = model_data.get("actionConfig", [])
        action_config = {item["keyName"]: item for item in action_config_list}
        model_config = {item["keyName"]: item["selectedValues"] for item in action_config_list}
        batch_size_count = len(model_config.get("batch", [1]))
        epochs_count = len(model_config.get("epochs", [1]))
        learning_rate_count = len(model_config.get("learning_rate", [1]))
        model_specific_count = batch_size_count * epochs_count * learning_rate_count
        model_counts.append(model_specific_count)
        config = {
            "is_autoML": True,
            "tuning_type": tuning_type,
            "model_checkpoint": "auto",
            "checkpoint_type": "predefined",
            "action_config": action_config,
            "model_config": model_config,
        }
        model_arch = ModelArch(
            session=session,
            model_family_name=model_family_name,
            model_key=model_key,
        )
        model_archs.append(model_arch)
        configs.append(config)
    return model_archs, configs, model_counts


class ModelArch:
    """
    A class to interact with model architectures through the model architecture API.

    This class handles fetching and storing model architecture information, including
    configuration parameters, export formats, and other model metadata.

    Parameters
    ----------
    session : Session
        Active session object for making API calls
    model_family_name : str
        Name of the model family this architecture belongs to
    model_key : str
        Unique identifier key for the model architecture

    Attributes
    ----------
    account_number : str
        Account number from the session
    project_id : str
        Project identifier from the session
    model_family_name : str
        Name of the model family
    model_key : str
        Model's unique identifier key
    last_refresh_time : datetime
        Timestamp of last data refresh
    rpc : RPCClient
        RPC client object from session for API calls
    model_arch_id : str or None
        Model information unique identifier
    model_name : str or None
        Human readable name of the model
    model_family_id : str or None
        Unique identifier of the model family
    params_millions : float or None
        Number of parameters in millions
    export_formats : list or None
        List of supported export formats
    model_config : dict or None
        Default configuration parameters for model training

    Notes
    -----
    Upon initialization, the class automatically fetches:
    - Model information using _get_model_arch()
    - Training configuration using get_model_train_config()
    - Export formats using get_export_formats()

    If model_key is not provided, these fetches are skipped and the class
    initializes with minimal information.

    Example
    -------
    >>> session = Session()
    >>> model = ModelArch(
    ...     session=session,
    ...     model_family_name="resnet",
    ...     model_key="resnet50"
    ... )
    >>> print(f"Model: {model.model_name}")
    >>> print(f"Parameters: {model.params_millions}M")
    >>> print(f"Export formats: {model.export_formats}")

    Raises
    ------
    AssertionError
        If neither ((model_family_name or model_family_id) and model_key) nor model_arch_id is provided.
    """

    def __init__(
        self,
        session,
        model_family_name=None,
        model_key=None,
        model_family_id=None,
        model_arch_id=None,
    ):
        self.session = session
        self.account_number = session.account_number
        self.project_id = session.project_id
        self.rpc = session.rpc
        self.last_refresh_time = datetime.now()
        assert (
            model_family_name is not None and model_key is not None or model_arch_id is not None
        ), "Either both model_family_name and model_key must be provided, or model_arch_id must be provided."
        self.model_family_name = model_family_name
        self.model_key = model_key
        self.model_arch_id = model_arch_id
        model_arch, error, message = self._get_model_arch()
        if not error:
            self.model_arch_id = model_arch.get("_id", self.model_arch_id)
            self.model_name = model_arch.get("modelName")
            self.model_key = model_arch.get("modelKey")
            self.model_family_id = model_arch.get("_idModelFamily")
            self.params_millions = model_arch.get("paramsInMillion")
            self.model_family_name = model_arch.get("modelFamilyName")
            self.input_size = model_arch.get("inputSize")
            model_train_config, error, message = self.get_train_action_config()
            try:
                if not error:
                    self.default_model_config = {
                        param["keyName"]: [param["defaultValue"]]
                        for param in model_train_config["actionConfig"]
                    }
            except Exception as e:
                print(
                    "Error in default model config: ",
                    e,
                )
                self.default_model_config = {}
            export_formats, error, message = self.get_export_formats()
            try:
                if not error:
                    self.export_formats = export_formats
            except Exception as e:
                print("Error in export formats: ", e)
                self.export_formats = []
            self.model_family = ModelFamily(
                session=self.session,
                model_family_id=self.model_family_id,
            )

    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise Exception("Refresh can only be called after two minutes since the last refresh.")
        init_params = {
            "session": self.session,
            "model_family_name": self.model_family_name,
            "model_key": self.model_key,
        }
        self.__init__(**init_params)
        self.last_refresh_time = datetime.now()

    def _get_model_arch(self):
        """
        Fetch model information by its ID.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> model_arch, error, message = model_arch._get_model_arch()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model info: {model_arch}")
        """
        if self.model_arch_id is not None:
            path = f"/v1/model_store/get_model_arch/{self.model_arch_id}"
        else:
            path = f"/v1/model_store/get_model_arch_from_model_key_and_family/{self.model_key}/{self.model_family_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Successfully fetched the model info",
            "An error occurred while fetching the model info",
        )

    def get_export_formats(self):
        """
        Fetch export formats for the model.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> export_formats, error, message = model_arch.get_export_formats()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Export formats: {export_formats}")
        """
        if self.model_arch_id is not None:
            path = f"/v1/model_store/get_export_formats?modelArchId={self.model_arch_id}"
        else:
            path = f"/v1/model_store/get_model_export_formats_from_model_key_and_family/{self.model_key}/{self.model_family_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Successfully fetched export formats",
            "An error occurred while fetching export formats",
        )

    def get_train_config(
        self,
        tuning_type="default",
        model_checkpoint="auto",
    ):
        """
        Get training configuration for the model.

        Parameters
        ----------
        tuning_type : str, optional
            Type of tuning to use (default is "default")
        model_checkpoint : str, optional
            Model checkpoint to use (default is "auto")

        Returns
        -------
        dict
            Training configuration for the model

        Example
        -------
        >>> train_config = model_arch.get_train_config()
        >>> print(f"Training config: {train_config}")
        """
        payload = {
            "modelCheckpoint": [model_checkpoint],
            "paramsSearchType": tuning_type,
            "_idModelArch": self.model_arch_id,
        }
        path = f"/v1/model_store/get_model_params/v2?projectId={self.project_id}&accountNumber={self.account_number}"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=payload,
        )
        data, error, message = handle_response(
            resp,
            "Successfully fetched model parameters",
            "An error occurred while fetching model parameters",
        )
        if error is not None:
            print(error)
            return error
        return {
            "model_key": self.model_key,
            "params_millions": self.params_millions,
            "model_name": self.model_name,
            "model_arch_id": self.model_arch_id,
            "model_family_name": self.model_family_name,
            "action_config": {},
            "is_autoML": False,
            "tuning_type": tuning_type,
            "model_checkpoint": model_checkpoint,
            "checkpoint_type": "predefined",
            "model_inputs": self.model_family.model_inputs,
            "model_outputs": self.model_family.model_outputs,
            "model_config": {item["keyName"]: item["selectedValues"] for item in data},
        }

    def get_export_config(self, export_format):
        """
        Get export configuration for the model.

        Parameters
        ----------
        export_format : str
            The format to export to

        Returns
        -------
        dict
            Export configuration for the specified format

        Example
        -------
        >>> export_config = model_arch.get_export_config("ONNX")
        >>> print(f"Export config: {export_config}")
        """
        model_export_config, error, message = self.get_export_action_config(export_format)
        if error:
            return None
        return {
            param["keyName"]: param["defaultValue"]
            for param in model_export_config["actionConfig"]
        }

    def get_export_action_config(self, export_format):
        """
        Get action configuration for model export.

        Parameters
        ----------
        export_format : str
            The format to export to

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> config, error, message = model_arch.get_export_action_config("ONNX")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Export action config: {config}")
        """
        path = f"/v1/model_store/get_action_config_for_model_export?modelArchId={self.model_arch_id}&exportFormat={export_format}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Successfully fetched export action config",
            "An error occurred while fetching export action config",
        )

    def get_train_action_config(self):
        """
        Get action configuration for model training.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> config, error, message = model_arch.get_train_action_config()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Train action config: {config}")
        """
        if self.model_arch_id is not None:
            path = f"/v1/model_store/get_train_config/{self.model_arch_id}"
        else:
            path = f"/v1/model_store/get_model_train_config_from_model_key_and_family/{self.model_key}/{self.model_family_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Successfully fetched train action config",
            "An error occurred while fetching train action config",
        )


class ModelFamily:
    """
    Class to interact with the model family API to get model configuration info and model-related info.

    This class handles fetching and storing model family information, including model inputs, outputs,
    supported runtimes, metrics, and other metadata.

    Parameters
    ----------
    session : Session
        The session object containing authentication information.
    model_family_id : str, optional
        The ID of the model family to fetch.
    model_family_name : str, optional
        The name of the model family to fetch.

    Attributes
    ----------
    session : Session
        The session object containing authentication information.
    account_number : str
        The account number from the session.
    project_id : str
        The project identifier from the session.
    rpc : RPCClient
        The RPC client object from the session for API calls.
    model_family_id : str
        The ID of the model family.
    model_family_name : str
        The name of the model family.
    family_data : dict
        The data of the model family fetched from the API.
    model_inputs : list
        List of model inputs.
    model_outputs : list
        List of model outputs.
    model_keys : dict
        Dictionary mapping model keys to model names.
    description : str
        Description of the model family.
    training_framework : str
        Training framework used for the model family.
    supported_runtimes : list
        List of supported runtimes.
    benchmark_datasets : list
        List of benchmark datasets.
    supported_metrics : list
        List of supported metrics.
    input_format : str
        Input format for the model family.

    Methods
    -------
    get_model_family_details()
        Fetch a model family by its ID or name.
    get_model_archs(model_name=None, model_key=None)
        Fetch model information by model family or by name and key.

    Example
    -------
    >>> session = Session(account_number="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
    >>> model_family = ModelFamily(session, model_family_name="resnet")
    >>> print(f"Model Family: {model_family.model_family_name}")
    >>> print(f"Model Inputs: {model_family.model_inputs}")
    >>> print(f"Model Outputs: {model_family.model_outputs}")
    >>> print(f"Supported Runtimes: {model_family.supported_runtimes}")
    >>> print(f"Supported Metrics: {model_family.supported_metrics}")

    Raises
    ------
    AssertionError
        If neither model_family_id nor model_family_name is provided.
    """

    def __init__(
        self,
        session,
        model_family_name=None,
        model_family_id=None,
    ):
        self.session = session
        self.account_number = session.account_number
        self.project_id = session.project_id
        self.rpc = session.rpc
        assert (
            model_family_id is not None or model_family_name is not None
        ), "Either model_family_id or model_family_name must be provided"
        self.model_family_id = model_family_id
        self.model_family_name = model_family_name
        family_data, error, message = self.get_model_family_details()
        if error:
            print(f"Error: {error}")
            return
        self.family_data = family_data
        self.model_family_id = family_data.get("_id")
        self.model_family_name = family_data.get("modelFamily")
        self.model_inputs = family_data.get("modelInputs")
        self.model_outputs = family_data.get("modelOutputs")
        self.description = family_data.get("description")
        self.training_framework = family_data.get("trainingFramework")
        self.supported_runtimes = family_data.get("exportFormats")
        self.supported_metrics = family_data.get("supportedMetrics")
        self.input_format = family_data.get("inputFormat")

    def get_model_family_details(self):
        """
        Fetch a model family by its ID or name.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> session = Session(account_number="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
        >>> model_family = ModelFamily(session, model_family_name="resnet")
        >>> resp, error, message = model_family.get_model_family_details()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model family: {resp}")
        """
        if self.model_family_id is not None:
            path = f"/v1/model_store/get_model_family/{self.model_family_id}"
        else:
            path = f"/v1/model_store/get_model_family/{self.model_family_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Successfully fetched the model family",
            "An error occured while fetching the model family",
        )

    def get_model_archs(self, model_name=None, model_key=None):
        """
        Fetch a model family by its ID or name.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> session = Session(account_number="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
        >>> model_family = ModelFamily(session, model_family_name="resnet")
        >>> resp, error, message = model_family.__get_model_family()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model family: {resp}")
        """
        if self.model_family_id:
            path = (
                f"/v1/model_store/get_models_by_modelfamily?modelFamilyId={self.model_family_id}"
            )
        else:
            path = f"/v1/model_store/get_models_by_modelfamily?modelFamilyName={self.model_family_name}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Successfully fetched model info",
            "An error occurred while fetching model info",
        )
        if error:
            return data, error, message
        if isinstance(data, list):
            data_list = data
        elif isinstance(data, dict):
            data_list = [data]
        else:
            error = "Data is not in the expected format. Expected a list or dictionary."
            return None, error, message
        if model_name and model_key:
            model_arch_list = [
                {
                    "model_key": item["modelKey"],
                    "model_arch_instance": ModelArch(
                        self.session,
                        self.model_family_name,
                        item["modelKey"],
                    ),
                }
                for item in data_list
            ]
            return model_arch_list, error, message
        else:
            model_archs = {
                item["modelKey"]: ModelArch(
                    self.session,
                    self.model_family_name,
                    item["modelKey"],
                )
                for item in data_list
            }
            return model_archs, error, message

    def get_model_arch(self, model_key):
        return ModelArch(
            self.session,
            self.model_family_name,
            model_key,
        )


class BYOM:
    """
    A class to interact with the BYOM (Bring Your Own Model) API for managing model families, model information,
    and model action configurations.

    Attributes:
    -----------
    session : Session
        A session object containing account information and RPC (Remote Procedure Call) details.
    account_number : str
        The account number associated with the session.
    rpc : RPC
        The RPC object used to make API calls.

    Methods:
    --------

    delete_model_family(model_family_id)
        Deletes a model family using its ID.

    delete_model_arch(model_arch_id)
        Deletes model information using its ID.

    delete_model_action_config(model_action_config_id)
        Deletes a model action configuration using its ID.

    add_model_family(...)
        Adds a new model family.

    add_model_arch(...)
        Adds new model information.

    add_model_action_config(...)
        Adds a new model action configuration.

    update_model_family(...)
        Updates a model family.

    update_model_arch(...)
        Updates model information.

    update_model_action_config(...)
        Updates a model action configuration.

    add_model_family_action_config(...)
        Adds an action configuration to a model family.
    """

    def __init__(self, session):
        """
        Initializes the BYOM class with a session object.

        Parameters:
        -----------
        session : Session
            A session object containing account information and RPC details.
        """
        self.session = session
        self.account_number = session.account_number
        self.rpc = session.rpc
        self.project_id = session.project_id

    def _load_config(self, config):
        if isinstance(config, str) and os.path.isfile(config):
            with open(config, "r") as file:
                return json.load(file)
        elif isinstance(config, dict):
            return config
        else:
            raise ValueError("Invalid config. Must be a dictionary or a valid file path.")

    def _get_model_faimly_id(self, model_family_name):
        model_faimly = ModelFamily(self.session, model_family_name)
        return model_faimly.model_family_id

    def _get_model_arch_id(self, model_family_name, model_key):
        model_arch = ModelArch(
            self.session,
            model_family_name,
            model_key,
        )
        return model_arch.model_arch_id

    def _get_model_action_config_id(
        self,
        model_family_name,
        model_key,
        action_type,
        export_format=None,
    ):
        model_arch = ModelArch(
            self.session,
            model_family_name,
            model_key,
        )
        if action_type == "train_model":
            return model_arch.get_train_action_config()[0]["_id"]
        elif action_type == "export_model":
            return model_arch.get_export_action_config(export_format)[0]["_id"]

    def add_model_family(self, model_family_info):
        """
        Adds a new model family to the model store.

        This function sends a POST request to add a new model family with the provided parameters.

        Parameters:
        -----------
        model_family_info : str or dict
            The path to the local JSON file containing the model config or the model config dictionary.

        Returns:
        --------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises:
        -------
        ValueError
            If the config is neither a valid file path nor a dictionary.
        """
        model_family_info = self._load_config(model_family_info)
        model_family_info["accountNumber"] = self.account_number
        path = "/v1/model_store/add_model_family"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=model_family_info,
        )
        return handle_response(
            resp,
            "New model family created",
            "An error occurred while creating model family",
        )

    def update_model_family(self, model_family_name, model_family_info):
        """
        Updates an existing model family in the model store.

        This function sends a PUT request to update a model family with the provided parameters.

        Parameters:
        -----------
        model_family_name : str
            The unique identifier of the model family to update.
        model_family_info : str or dict
            The path to the local JSON file containing the model config or the model config dictionary.

        Returns:
        --------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises:
        -------
        ValueError
            If the config is neither a valid file path nor a dictionary.
        """
        model_store_payload = self._load_config(model_family_info)
        model_family_id = self._get_model_faimly_id(model_family_name)
        model_store_payload["accountNumber"] = self.account_number
        path = f"/v1/model_store/update_model_family/{model_family_id}"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=model_store_payload,
        )
        return handle_response(
            resp,
            "Model family successfully updated",
            "An error occurred while updating model family",
        )

    def delete_model_family(self, model_family_name):
        """Delete a model family"""
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = f"/v1/model_store/model_family/{model_family_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Successfully deleted the model family",
            "An error occurred while deleting the model family",
        )

    def get_model_family(self, model_family_name):
        return ModelFamily(
            session=self.session,
            model_family_name=model_family_name,
        )

    def delete_model_arch(self, model_family_name, model_key):
        """
        Deletes model information using its ID.

        Parameters:
        -----------
        model_arch_id : str
            The ID of the model information to delete.

        Returns:
        --------
        tuple
            A tuple containing the API response, error message (or None if successful), and a status message.
        """
        model_arch_id = self._get_model_arch_id(model_family_name, model_key)
        path = f"/v1/model_store/model_arch/{model_arch_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Successfully deleted the model family",
            "An error occured while deleting the model family",
        )

    def add_train_action_config(self, model_family_name, action_config):
        """
        Adds a new action configuration for a specific model in the model store.

        This function sends a POST request to add a new action configuration for a model with the provided parameters.

        Parameters:
        -----------
        model_family_name : str
            The name of the model family.
        action_config : dict
            Configuration details for the action.

        Returns:
        --------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises:
        -------
        May raise exceptions related to network issues or API errors.

        Notes:
        ------
        This function uses the self.rpc.post method to send the request and
        handle_response to process the response.
        """
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = "/v1/model_store/add_model_family_config"
        model_store_payload = {
            "_idModelFamily": model_family_id,
            "actionType": "model_train",
            "actionConfigs": action_config["actionConfig"],
        }
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=model_store_payload,
        )
        return handle_response(
            resp,
            "New model action config created",
            "An error occured while creating model action config",
        )

    def add_export_action_config(self, model_family_name, action_config):
        """
        Adds a new action configuration for a specific model in the model store.

        This function sends a POST request to add a new action configuration for a model with the provided parameters.

        Parameters:
        -----------
        model_family_name : str
            The name of the model family.
        action_config : dict
            Configuration details for the action.

        Returns:
        --------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises:
        -------
        May raise exceptions related to network issues or API errors.

        Notes:
        ------
        This function uses the self.rpc.post method to send the request and
        handle_response to process the response.
        """
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = "/v1/model_store/add_model_family_config"
        model_store_payload = {
            "_idModelFamily": model_family_id,
            "actionType": "model_export",
            "actionConfigs": action_config["actionConfig"],
        }
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=model_store_payload,
        )
        return handle_response(
            resp,
            "New model action config created",
            "An error occured while creating model action config",
        )

    def delete_model_action_config(
        self,
        model_family_name,
        model_key,
        action_type,
        action_config,
        export_format=None,
    ):
        model_action_config_id = self._get_model_action_config_id(
            model_family_name,
            model_key,
            action_type,
            action_config,
            export_format,
        )
        path = f"/v1/model_store/model_action_config/{model_action_config_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Successfully deleted the model action config",
            "An error occured while deleting the model action config",
        )

    def get_public_model_families_docker(self, project_type):
        path = f"/v1/model_store/get_public_model_families_docker?projectType={project_type}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Successfully retrieved public model families docker info",
            "Error getting public model families docker info",
        )

    def use_docker_image_from_public_model_family(
        self,
        model_family_name,
        docker_image_model_family_name,
        project_type,
    ):
        payload = {
            "sourceModelFamilyId": self._get_model_faimly_id(docker_image_model_family_name),
            "targetModelFamilyId": self._get_model_faimly_id(model_family_name),
            "accountNumber": self.account_number,
        }
        docker_repos_info, error, message = self.get_public_model_families_docker(project_type)
        if error:
            return None, error, message
        for docker_repo in docker_repos_info:
            if docker_repo.get("modelFamily") == docker_image_model_family_name:
                payload["dockerRepo"] = docker_repo.get("dockerRepo")
                break
        if not payload.get("dockerRepo"):
            return (
                None,
                "Docker repo not found",
                "Docker repo not found",
            )
        path = f"/v1/model_store/model_family_repo/{model_family_name}"
        resp = self.rpc.put(
            path=path,
            headers={"Content-Type": "application/json"},
            payload=payload,
        )
        return handle_response(
            resp,
            "Successfully updated model family repo",
            "Error updating model family repo",
        )

    def add_family_requirement_file(
        self,
        model_family_name,
        requirement_path
    ):
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = f"/v1/model_store/get_user_requirements_upload_path?fileName={model_family_id}"
        presigned_url = self.rpc.get(path=path).get("data")
        with open(requirement_path, "rb") as file:
            response = requests.put(
                presigned_url,
                data=file,
                timeout=30,
            )
        if response.status_code == 200:
            pass
        else:
            raise Exception(f"Upload failed with status code: {response.status_code}")
        payload = {
            "cloudPath": presigned_url.split("?")[0],
            "modelFamilyId": model_family_id,
        }
        path = "/v1/model_store/update_user_requirements_download_path"
        resp = self.rpc.put(
            path=path,
            headers={"Content-Type": "application/json"},
            payload=payload,
        )
        return handle_response(
            resp,
            "Model requirement file added",
            "Error adding model requirement file",
        )
    
    def add_family_docker_file(
        self,
        model_family_name,
        docker_path
    ):
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = f"/v1/model_store/get_user_docker_upload_path?fileName={model_family_id}"
        presigned_url = self.rpc.get(path=path).get("data")
        with open(docker_path, "rb") as file:
            response = requests.put(
                presigned_url,
                data=file,
                timeout=30,
            )
        if response.status_code == 200:
            pass
        else:
            raise Exception(f"Upload failed with status code: {response.status_code}")
        payload = {
            "cloudPath": presigned_url.split("?")[0],
            "modelFamilyId": model_family_id,
        }
        path = "/v1/model_store/update_user_docker_download_path"
        resp = self.rpc.put(
            path=path,
            headers={"Content-Type": "application/json"},
            payload=payload,
        )
        return handle_response(
            resp,
            "Model Docker file added",
            "Error adding model Dockerfile",
        )
    
    def upload_model_family_codebase(
        self,
        model_family_name,
        code_zip_path,
        matrice_sdk_version,
        cuda_version
    ):
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = f"/v1/model_store/get_user_code_upload_path?fileName={model_family_id}"
        presigned_url = self.rpc.get(path=path).get("data")
        with open(code_zip_path, "rb") as file:
            response = requests.put(
                presigned_url,
                data=file,
                timeout=30,
            )
        if response.status_code == 200:
            pass
        else:
            raise Exception(f"Upload failed with status code: {response.status_code}")
        payload = {
            "imageName": os.path.basename(code_zip_path),
            "cloudPath": presigned_url.split("?")[0],
            "cloudProvider": "aws",
            "sdk_version": matrice_sdk_version,
            "pytorch_version": cuda_version,
            "accountNumber": self.account_number,
            "_idModelFamily": model_family_id
        }
        path = "/v1/model_store/add_model_image"
        resp = self.rpc.post(
            path=path,
            headers={"Content-Type": "application/json"},
            payload=payload,
        )
        return handle_response(
            resp,
            "Model code base added",
            "Error adding model code base",
        )

    def download_model_family_codebase(self, model_family_name, download_path):
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = f"/v1/model_store/get_user_code_download_path/{model_family_id}"
        presigned_url = self.rpc.get(path=path).get("data")
        with open(download_path, "wb") as file:
            response = requests.get(presigned_url, timeout=30)
            file.write(response.content)
        if response.status_code == 200:
            return download_path
        else:
            raise Exception(f"Download failed with status code: {response.status_code}")

    def wait_for_codebase_upload(self, model_family_name, delay=120):
        while True:
            resp, error, message = self.get_model_family_codebase_details(model_family_name)
            if error:
                print(f"Error checking status: {error}")
                return False
            if resp.get("status") == "uploaded":
                print("Codebase upload completed successfully")
                return True
            print(f"Current status: {resp.get('status')}. Waiting {delay} seconds...")
            time.sleep(delay)

    def get_model_family_codebase_details(self, model_family_name):
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = f"/v1/model_store/get_user_code_details/{model_family_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Code details retrieved",
            "Error getting code details",
        )

    def _parse_test_cases(self, test_cases):
        model_test_cases = {}
        for test_case in test_cases:
            if test_case.get("modelKey") not in model_test_cases:
                model_test_cases[test_case.get("modelKey")] = []
            model_test_case = {
                "actionType": test_case.get("actionType"),
                "batchSize": test_case.get("batchSize"),
                "exportFormat": test_case.get("exportFormat"),
            }
            model_test_cases[test_case.get("modelKey")].append(model_test_case)
        return model_test_cases

    def get_test_cases_by_type(
        self,
        model_family_name,
        test_cases_type="default",
    ):
        path = f"/v1/model_store/get_selected_test_cases?modelFamily={model_family_name}&testType={test_cases_type}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Successfully fetched the selected test cases",
            "An error occured while fetching the selected test cases",
        )
        if not error:
            return (
                self._parse_test_cases(data),
                error,
                message,
            )
        else:
            return None, error, message

    def start_test_cases(
        self,
        model_family_name,
        model_key,
        project_type,
        test_cases,
    ):
        """Start selected test cases for a specific model family and key.

        This method runs specified test cases for a given model family and key.

        Args:
            model_family_name (str): Name of the model family (e.g. "RESNET-89", "EfficientNet V2")
            model_key (str): Specific model key (e.g. "resnet18", "efficientnet_v2_l")
            test_cases (list): List of action dictionaries with structure:
                [
                    {
                        "actionType": str,  # e.g. "model_predict", "train_model"
                        "batchSize": int,   # batch size for the action
                        "exportFormat": str  # e.g. "PyTorch", "ONNX"
                    },
                    ...
                ]
        Returns:
            dict: Response from the API containing success/failure status

        Raises:
            May raise exceptions from handle_response() if API call fails
        """
        payload = {
            "modelFamilyName": model_family_name,
            "modelKey": model_key,
            "projectType": project_type,
            "modelActions": [],
        }
        for test_case in test_cases:
            model_action = {
                "actionType": test_case.get("actionType"),
            }
            batch_size = test_case.get("batchSize")
            if batch_size is not None:
                model_action["batchSize"] = batch_size

            export_format = test_case.get("exportFormat")
            if export_format is not None:
                model_action["exportFormat"] = export_format
            payload["modelActions"].append(model_action)
        path = "/v1/model_store/add_model_family_testcases"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=payload,
        )
        return handle_response(
            resp,
            "Successfully started the test cases",
            "An error occured while starting the test cases",
        )

    def get_started_test_cases(self, model_family_name, model_key=None):
        path = f"/v1/model_store/get_model_family_testcases?modelFamily={model_family_name}"
        if model_key:
            path += f"&modelKey={model_key}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Successfully fetched the model family test cases",
            "An error occured while fetching the model family test cases",
        )

    def get_model_family_actions(self, model_family_name):

        def _format_actions(actions):
            action_type_mapping = {
                "training": "model_train",
                "evaluation": "model_eval",
                "deployment": "model_predict",
                "export": "model_export",
            }
            formated_actions = {}
            for action_dict in actions:
                for (
                    model_key,
                    model_actions,
                ) in action_dict.items():
                    if model_key not in formated_actions:
                        formated_actions[model_key] = []
                    for (
                        action_type,
                        action_configs,
                    ) in model_actions.items():
                        for action_config in action_configs:
                            formated_actions[model_key].append(
                                {
                                    "actionType": action_type_mapping[action_type],
                                    "exportFormat": action_config.get("exportFormat"),
                                    "batchSize": action_config.get("batchSize"),
                                    "status": action_config.get("status"),
                                }
                            )
            return formated_actions

        path = f"/v1/model_store/get_allowed_actions/{model_family_name}"
        resp = self.rpc.get(path=path)
        data, error, message = handle_response(
            resp,
            "Successfully fetched the model family allowed actions",
            "An error occured while fetching the model family allowed actions",
        )
        if not error:
            return (
                _format_actions(data),
                error,
                message,
            )
        else:
            return None, error, message

    def integrate_model_actions(
        self,
        model_family_name,
        model_key,
        model_actions,
    ):
        """Integrate model actions for a specific model family and key.

        This method integrates actions like training, prediction etc. for a given model.
        Currently hardcoded to add a train_model action with batch size 1 and ONNX format.

        Args:
            model_family_name (str): Name of the model family (e.g. "RESNET-89", "EfficientNet V2")
            model_key (str): Specific model key (e.g. "resnet18", "efficientnet_v2_l")
            model_actions (list): List of action dictionaries with structure:
                [
                    {
                        "actionType": str,  # e.g. "model_predict", "train_model"
                        "batchSize": int,   # batch size for the action
                        "exportFormat": str  # e.g. "PyTorch", "ONNX"
                    },
                    ...
                ]

        Returns:
            dict: Response from the API containing success/failure status

        Raises:
            May raise exceptions from handle_response() if API call fails
        """
        payload = {"actions": []}
        for action in model_actions:
            model_aciton = {
                "modelFamily": model_family_name,
                "modelKey": model_key,
                "actionType": action.get("actionType"),
                "batchSize": action.get("batchSize"),
                "exportFormat": action.get("exportFormat"),
            }
            payload["actions"].append(model_aciton)
        path = "/v1/model_store/integrate_actions"
        resp = self.rpc.put(path=path, payload=payload)
        return handle_response(
            resp,
            "Successfully integrated the actions",
            "An error occured while integrating the actions",
        )

    def publish_model_family(self, model_family_name):
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = f"/v1/model_store/request_publish_model_family/{model_family_id}"
        resp = self.rpc.put(path=path)
        return handle_response(
            resp,
            "Successfully published the model family",
            "An error occured while publishing the model family",
        )

    def get_model_family_benchmark_results(self, model_family_name):
        path = f"/v1/model_store/get_benchmark_results_by_model_family?modelFamily={model_family_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Successfully fetched the benchmark results",
            "An error occured while fetching the benchmark results",
        )

    def update_model_family_benchmark_results(self, model_family_name):
        model_family_id = self._get_model_faimly_id(model_family_name)
        path = f"/v1/model_store/update_model_family_benchmarks/{model_family_id}"
        resp = self.rpc.put(path=path)
        return handle_response(
            resp,
            "Successfully updated the benchmark results",
            "An error occured while updating the benchmark results",
        )
