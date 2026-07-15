"""Auto-generated stubs for package: matrice."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from PIL import Image
from PIL import Image, ImageDraw
from __future__ import annotations
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from io import BytesIO
from matrice.action import Action
from matrice.action_tracker import ActionTracker, LocalActionTracker, _dotdict
from matrice.annotation import Annotation
from matrice.application import Application, find_application_by_name, get_application_by_id, get_application_cover_upload_path, get_application_versions, list_application_versions, list_applications, upload_application_cover_image
from matrice.camera_management import CameraManagement
from matrice.checkpoint import create_checkpoint, get_model_checkpoint_upload_path, list_checkpoints, upload_checkpoint_file
from matrice.dataset import Dataset
from matrice.exported_model import ExportedModel
from matrice.inference_pipeline_management import InferencePipelineManagement
from matrice.model_store import ModelArch, ModelFamily
from matrice.models import Model
from matrice.projects import Projects
from matrice.security_utils import redact_url
from matrice.security_utils import redact_url, safe_extractall_zip, validate_download_url
from matrice.security_utils import redact_url, validate_download_url
from matrice.streaming_automation import StreamingAutomation
from matrice.streaming_gateway_management import StreamingGatewayManagement
from matrice_common.rpc import RPC
from matrice_common.session import Session
from matrice_common.utils import get_summary, handle_response
from matrice_common.utils import handle_response
from matrice_common.utils import log_errors
from matrice_data_processing.data_processing.create_dataset import create_dataset
from matrice_streaming.deployment import Deployment
from pathlib import Path
from pycocotools.coco import COCO
from pydantic.main import BaseModel
from sklearn.metrics import average_precision_score, cohen_kappa_score, f1_score, log_loss, matthews_corrcoef, precision_score, recall_score, roc_auc_score
from sklearn.preprocessing import label_binarize
from urllib.parse import quote
from urllib.parse import urlparse
from urllib.parse import urlsplit, urlunsplit
import csv
import functools
import gc
import importlib
import io
import ipaddress
import json
import logging
import math
import matplotlib.pyplot as plt
import mimetypes
import os
import pandas as pd
import requests
import seaborn as sns
import shutil
import socket
import subprocess
import sys
import tarfile
import threading
import time
import torch
import torchvision
import traceback
import uuid
import warnings
import yaml
import zipfile

# Constants
logger: Any = ...  # From action_tracker
logger: Any = ...  # From app_integration
CameraConfig: Any = ...  # From inference_orchestrator
PipelineConfig: Any = ...  # From inference_orchestrator
R: Any = ...  # From testing

# Functions
# From action
def clone_project(session, source_project_id, new_project_name) -> Any:
    """
    Clone the project with the project ID
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    source_project_id : str
        ID of the project you want to copy.
    new_project_name: str
        Name of the new project.
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action details if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = clone_project(session, "ProjectID_1234", "New_Project_name")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def enable_disable_project(session, type, project_id) -> Any:
    """
    Enable or disable a project
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    type : str
        Action you want to perform i.e either enable or disable
    project_id: str
        Id of the project you want to enable or disable
    
    Returns
    -------
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in enabling or disabling the project.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = enable_disable_project(session, "enable", "ProjectID_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def get_action_details(session, action_id) -> Any:
    """
    Fetches action details from the API.
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    action_id : str
        The unique identifier of the action whose details are being fetched.
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action details if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_details(session, "action_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def get_action_docker_logs(session, action_record_id) -> Any:
    """
    Get the docker logs associated with a particular action record.
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    action_record_id : str
        The unique identifier of the action record whose docker logs are being fetched.
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action details if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_docker_logs(session, "action_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def get_action_graph(session, granularity, start_date, end_date) -> Any:
    """
    Get the action graph
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    granularity : str
        Unit for the created by time
    start_date: str
        Date and tiem
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action details if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_graph(session, "action_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def get_action_logs_from_action_record_id(session, action_record_id) -> Any:
    """
    Fetches action details from action record ID.
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    action_record_id : str
        The unique identifier of the service whose details are being fetched.
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action logs if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_logs_from_action_record_id(session, "action_record_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def get_action_logs_from_record_id(session, action_record_id) -> Any:
    """
    Fetches action details from action record ID.
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    action_record_id : str
        The unique identifier of the action logs whose details are being fetched.
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action logs if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_logs_from_record_id(session, "action_record_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def get_action_record_for_account_number(session) -> Any:
    """
    Fetches action details of the account number.
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action records if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_record_for_account_number(session)
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def get_project_id_by_service_id(session, service_id) -> Any:
    """
    Get the Project Id by the service ID.
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    service_id: str
        A unique identifier of a particular service associated with a project
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action records if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_project_id_by_service_id(session)
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def get_recent_actions(session) -> Any:
    """
    Fetches recent actions performed on the platform.
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action records if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_recent_actions(session)
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def get_service_action_logs(session, service_id) -> Any:
    """
    Fetches action details from service ID.
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    service_id : str
        The unique identifier of the service whose details are being fetched.
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action logs if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_details(session, "service_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From action
def list_all_account_action_details(session) -> Any:
    """
    List all account with there action details.
    
    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    
    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action records if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.
    
    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.
    
    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = list_all_account_action_details(session)
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    ...

# From application
def find_application_by_name(session, name: str, page: int = 1, page_size: int = 200) -> tuple[dict | None, str | None]:
    """
    Search a single list_applications page and return the first application
    whose name matches (case-sensitive). Same data source and parsing as 2b.
    
    Parameters
    ----------
    session : Any
        Session with rpc.
    name : str
        Application name to find (exact match after strip).
    page : int, optional
        Page number to search (default 1, same as 2b).
    page_size : int, optional
        Page size for list_applications (default 200, same as 2b).
    
    Returns
    -------
    tuple
        (app_dict, error). On success app_dict is the application object (_id, name, etc.)
        and error is None. On not found or API error, app_dict is None and error is a string.
    """
    ...

# From application
def get_application_by_id(session, application_id: str) -> tuple[dict | None, str | None, str]:
    """
    Get a single application by ID — GET /v1/applications/:id (API Backend §3).
    
    **Path:** id = Application ObjectID.
    
    Returns
    -------
    tuple
        (data, error, message). data is the application object on success.
    """
    ...

# From application
def get_application_cover_upload_path(session) -> tuple[str | None, str | None, str]:
    """
    Get a presigned PUT URL to upload an application cover image.
    
    Wraps ``GET /v1/applications/get_application_cover_upload_path``.
    
    Returns
    -------
    tuple
        ``(upload_url, error, message)``. On success ``upload_url`` is a full
        presigned URL string that accepts ``PUT``.
    """
    ...

# From application
def get_application_versions(session, application_id: str) -> tuple[list | None, str | None, str]:
    """
    Get all versions of a single application.
    
    Wraps ``GET /v1/applications/version/:id``.
    
    For freshly created applications with no versions yet, ``data`` is an empty
    list.
    
    Parameters
    ----------
    session : Any
        Matrice session.
    application_id : str
        Application ObjectID.
    
    Returns
    -------
    tuple
        ``(versions, error, message)``. ``versions`` is a list of version
        dicts with ``_idApplication``, ``applicationVersion``, ``status``, etc.
    """
    ...

# From application
def get_application_via_list(session, application_id: str) -> Any:
    """
    Resolve application by ID via list endpoint. Prefer get_application_by_id when available.
    
    Returns
    -------
    tuple
        (data, error, message).
    """
    ...

# From application
def list_application_versions(session, status = None) -> tuple[list | None, str | None, str]:
    """
    List all application versions — GET /v1/applications/versions (API Backend §8).
    
    **Middleware:** AuthTeamMemberMiddleware() (team member required).
    
    **Query:** status (optional) — filter by "published", "in-review", "created".
    
    **Response (200):** data is a list of version objects, each with _idProject, _idVersion,
    _idApplication, applicationVersion, accountOwnedBy, userOwnedBy, status, metric,
    benchmarkDataset, blogLink, notebookLink, deploySettings, colorMapping, createdAt, updatedAt.
    
    Returns
    -------
    tuple
        (data, error, message). data is list of version dicts; error is None on success.
    """
    ...

# From application
def list_applications(session, page_size: int = 200, page_number: int = 0, sort_by: str = '', sort_order: str = 'asc') -> tuple[dict | None, str | None, str]:
    """
    List applications — ``GET /v1/applications/list_applications``.
    
    The real backend query contract (from the captured request) uses four params:
    ``pageSize``, ``currentPage``, ``pageNumber``, ``sortBy``, ``sortOrder``. We
    send the same value for ``currentPage`` and ``pageNumber`` since the UI
    always does so.
    
    Parameters
    ----------
    session : Any
        Matrice session with ``session.rpc``.
    page_size : int, optional
        Items per page (default 200).
    page_number : int, optional
        0-based page index (default 0).
    sort_by : str, optional
        Field name to sort by; empty for server default.
    sort_order : str, optional
        ``"asc"`` or ``"desc"``.
    
    Returns
    -------
    tuple
        ``(data, error, message)``. ``data`` has keys ``pageSize``, ``page``,
        ``total``, ``items``. Each item has ``_id``, ``name``, ``coverImage``,
        ``currentVersion``, ``publishedBy``, ``blogLink``, ``notebookLink``,
        ``status`` (``created`` | ``in-review`` | ``published``), ``outputType``,
        ``latestVersion``, ``maintainedBy``, ``publishedVersion``, ``description``,
        ``categories``, ``industries``, ``appType``, ``releaseStage``,
        ``fpsRequirements``, ``createdAt``, ``updatedAt``.
    """
    ...

# From application
def list_applications_via_list(session) -> Any:
    """
    List applications via GET /v1/applications/list. Backend may not support this path.
    
    Returns
    -------
    tuple
        (data, error, message).
    """
    ...

# From application
def list_models_for_application(session, application_id: str) -> tuple[list, str | None, str]:
    """
    Get models (or application versions) attached to an application.
    
    **Viability (API Backend - Applications.md):**
    - There is no documented GET /v1/applications/:id/models. This function uses:
      1. **GET /v1/applications/:id** — if the response includes `models`, `modelVersions`, or `versions`, that list is returned.
      2. **GET /v1/applications/versions** (API §8) — list all versions, then filter by _idApplication == application_id. Each version corresponds to an application version (status, applicationVersion, etc.).
      3. **GET /v1/applications/:id/models** — tried as fallback (undocumented; may 404).
    - For published apps, **GET /v1/public/applications/:id** (AppStore) returns application details including "models"; use that for public/catalog view.
    
    Parameters
    ----------
    session : Any
        Session with rpc.
    application_id : str
        Application ObjectID.
    
    Returns
    -------
    tuple
        (items, error, message). items is a list of model/version dicts (possibly empty); error is None on success.
    """
    ...

# From application
def request_publish_model_family(session, model_family_id: str) -> tuple[dict | None, str | None, str]:
    """
    Request publication of a model family — PUT /v1/model_store/request_publish_model_family/:model_family (API Backend §5).
    
    **Service:** be-model-store. **Path:** model_family = Model Family ObjectID.
    **Middleware:** AuthMiddleware(), PermissionMiddleware(PERM_ModelsServiceWRITE).
    **Request body:** None.
    
    **Response (200):** data = "Model Family Publication Requested ", status = "success".
    **Errors:** 400 (invalid model family ID), 422 (not enough test cases passed), 500.
    
    Returns
    -------
    tuple
        (data, error, message).
    """
    ...

# From application
def upload_application_cover_image(session, image_path: str, content_type: str = 'image/png', timeout: int = 120) -> tuple[str | None, str | None, str]:
    """
    Upload a local image file and return the clean public cover URL.
    
    Two-step flow:
    
    1. ``GET /v1/applications/get_application_cover_upload_path`` — presigned URL
    2. ``PUT <presigned_url>`` — stream the image bytes
    
    The returned URL is the clean object URL (no querystring), suitable for the
    ``coverImage`` field of :func:`Application.create_application`.
    
    Parameters
    ----------
    session : Any
        Matrice session.
    image_path : str
        Local path to the cover image (PNG/JPG/WEBP).
    content_type : str, optional
        HTTP ``Content-Type`` header for the PUT. Detected from extension if the
        caller leaves the default and the extension is known; else
        ``image/png``.
    timeout : int, optional
        HTTP timeout in seconds (default 120).
    
    Returns
    -------
    tuple
        ``(public_url, error, message)``.
    """
    ...

# From checkpoint
def create_checkpoint(session, project_id: str, name: str, checkpoint_value: str, model_family: str, model_key: str, checkpoint_type: str = 'URL', dataset: str = '', class_index_map: dict[str, str] | None = None) -> tuple[dict | None, str | None, str]:
    """
    Add (register) a model checkpoint — POST /v1/model/checkpoint (API Backend §2.1).
    
    **Middleware:** AuthMiddleware(), PermissionMiddleware(PERM_ModelsServiceWRITE)
    
    **Request body (per API doc):**
    - modelFamily (string), modelKey (string), name (string), _idProject (ObjectID),
    - checkpointType (string), checkpointValue (string), dataset (string), classIndexMap (object).
    
    **Response (200):** data contains checkpoint document with _id, modelFamily, modelKey, name,
    _idProject, checkpointType, checkpointValue, dataset, classIndexMap, status ("valid"),
    createdAt, updatedAt.
    
    Parameters
    ----------
    session
        Session with rpc (session.rpc.post). Must have valid JWT.
    project_id : str
        Project ObjectID the checkpoint belongs to (_idProject). Required.
    name : str
        Checkpoint name (e.g. "dummy-checkpoint"). Required.
    checkpoint_value : str
        For checkpoint_type "URL", the full URL to the .pt file; otherwise identifier/value. Required.
    model_family : str
        Model family (e.g. "YOLOv8"). Required by backend.
    model_key : str
        Model key (e.g. "yolov8m"). Required by backend.
    checkpoint_type : str, optional
        e.g. "URL" (checkpoint at URL) or "model_id". Default "URL".
    dataset : str, optional
        Dataset identifier; can be empty string. Default "".
    class_index_map : dict, optional
        Map of class index (string key) to class name, e.g. {"0": "person", "1": "car"}.
        Omitted from payload if None.
    
    Returns
    -------
    tuple
        (data, error, message).
        - data: checkpoint document (with _id, name, status, etc.) on success; None on failure.
        - error: None on success, else error string.
        - message: status string (e.g. "Checkpoint created" or error message).
    
    Examples
    --------
    >>> data, err, msg = create_checkpoint(
    ...     session,
    ...     project_id="69a934e3743c2ef19edc2379",
    ...     name="my-checkpoint",
    ...     checkpoint_value="https://storage.example.com/model.pt",
    ...     model_family="YOLOv8",
    ...     model_key="yolov8m",
    ...     checkpoint_type="URL",
    ...     class_index_map={"0": "person"},
    ... )
    >>> if not err and data:
    ...     checkpoint_id = data.get("_id")
    """
    ...

# From checkpoint
def get_model_checkpoint_upload_path(session, project_id: str) -> tuple[str | None, str | None, str]:
    """
    Get a presigned PUT URL to upload a model checkpoint (.pt / .pth / …).
    
    Wraps ``GET /v1/model/get_model_checkpoint_upload_path?projectId=<id>``.
    
    Parameters
    ----------
    session : Any
        Matrice :class:`~matrice_common.session.Session` (must expose ``session.rpc``).
    project_id : str
        Project ObjectID that will own the checkpoint.
    
    Returns
    -------
    tuple
        ``(upload_url, error, message)``. On success ``upload_url`` is a full
        presigned URL (string) that accepts ``PUT``; ``error`` is ``None``.
    """
    ...

# From checkpoint
def list_checkpoints(session, project_id: str) -> tuple[list | None, str | None, str]:
    """
    List pretrained checkpoints registered under a project.
    
    Wraps ``GET /v1/model/checkpoints?projectId=<id>``.
    
    Parameters
    ----------
    session : Any
        Matrice session.
    project_id : str
        Project ObjectID.
    
    Returns
    -------
    tuple
        ``(items, error, message)``. ``items`` is a list of checkpoint documents
        (each with ``_id``, ``name``, ``modelFamily``, ``modelKey``,
        ``checkpointValue``, ``classIndexMap``, ``status``, …). Empty list if none.
    """
    ...

# From checkpoint
def upload_and_register_checkpoint(session, project_id: str, file_path: str, name: str, model_family: str, model_key: str, class_index_map: dict[str, str] | None = None, dataset: str = '') -> tuple[dict | None, str | None, str]:
    """
    Convenience wrapper: upload a checkpoint file AND register it in one call.
    
    Equivalent to::
    
        url, err, _ = upload_checkpoint_file(session, project_id, file_path)
        data, err, _ = create_checkpoint(session, project_id, name, url,
                                         model_family, model_key,
                                         class_index_map=class_index_map)
    
    Returns
    -------
    tuple
        ``(checkpoint_doc, error, message)``. ``checkpoint_doc["_id"]`` is the
        Model Checkpoint ObjectID you'll need to attach the model to an app.
    """
    ...

# From checkpoint
def upload_checkpoint_file(session, project_id: str, file_path: str, content_type: str = 'application/octet-stream', timeout: int = 300) -> tuple[str | None, str | None, str]:
    """
    Upload a local checkpoint file to Matrice storage in two steps.
    
    1. ``GET /v1/model/get_model_checkpoint_upload_path`` — obtain a presigned PUT URL.
    2. ``PUT <presigned_url>`` — stream the binary file to the presigned URL.
    
    The returned URL is the *public, unsigned* object URL (querystring stripped)
    that you should pass as ``checkpoint_value`` to :func:`create_checkpoint`.
    
    Parameters
    ----------
    session : Any
        Matrice session.
    project_id : str
        Project ObjectID that will own the checkpoint.
    file_path : str
        Local path to the checkpoint file (e.g. ``"./model.pt"``).
    content_type : str, optional
        HTTP ``Content-Type`` to send on the PUT. Most backends ignore it for
        presigned URLs; default ``"application/octet-stream"``.
    timeout : int, optional
        HTTP timeout in seconds for the PUT upload, default ``300``.
    
    Returns
    -------
    tuple
        ``(public_url, error, message)``. On success ``public_url`` is the clean
        object URL (no querystring); ``error`` is ``None``.
    """
    ...

# From compute
def add_on_demand_instance(session, alias, compute_type, service_provider, launch_duration_hours, shutdown_thres_minutes) -> Any:
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
    ...

# From compute
def get_compute_status_summary(session, lease_type = 'on-demand') -> Any:
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
    ...

# From compute
def list_account_compute(session, status = 'all') -> Any:
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
    ...

# From compute
def list_instance_types(session, providers = None, gpu_types = None, price_range = None, page_size = 10, page_num = 0) -> Any:
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
    ...

# From dataset
def get_dataset_size_in_mb_from_url(session, url, project_id) -> Any:
    """
    Fetch the size of a dataset from the specified URL.
    
    This function sends a request to retrieve the dataset size, measured in megabytes,
    for a given project.
    
    Parameters
    ----------
    session : Session
        The active session used to communicate with the API.
    url : str
        The URL of the dataset to fetch the size for.
    project_id : str
        The ID of the project associated with the dataset.
    
    Returns
    -------
    tuple
        A tuple containing three elements:
        - dict: API response with dataset size information (e.g., size in MB).
        - str or None: Error message if an error occurred, `None` otherwise.
        - str: Status message indicating success or failure.
    
    Example
    -------
    >>> size_info, err, msg = get_dataset_size(session=session,
    url="https://example.com/dataset.zip", project_id="12345")
    >>> if err:
    >>>     print(f"Error: {err}")
    >>> else:
    >>>     print(f"Dataset size: {size_info.get('size', 'N/A')} MB")
    """
    ...

# From dataset
def upload_file(session, file_path) -> Any:
    """
    Upload a file to the dataset. Only ZIP files are supported.
    
    This function uploads a ZIP file to the dataset server for the specified session. It generates an upload URL,
    then uses it to transfer the file.
    
    Parameters
    ----------
    session : Session
        The active session used to communicate with the API.
    file_path : str
        The local path of the file to upload.
    
    Returns
    -------
    dict
        A dictionary containing:
        - `success` (bool): Indicates if the upload was successful.
        - `data` (str): URL of the uploaded file if successful, empty string otherwise.
        - `message` (str): A status message indicating success or detailing any error.
    
    Example
    -------
    >>> result = upload_file(session=session, file_path="path/to/data.zip")
    >>> if result['success']:
    >>>     print(f"File uploaded successfully: {result['data']}")
    >>> else:
    >>>     print(f"Error: {result['message']}")
    """
    ...

# From docker_utils
def check_docker() -> None:
    """
    Check that Docker is installed and usable by the current (non-root) user.
    
    This no longer auto-installs Docker (which requires root). If Docker is
    already usable it returns; otherwise it raises with operator guidance.
    
    Raises:
        RuntimeError: If Docker is not installed / not usable.
    """
    ...

# From docker_utils
def install_docker() -> None:
    """
    No-op if Docker is already usable; otherwise raise with guidance.
    
    Docker installation requires root (apt-get / tee /etc/apt / systemctl), so
    it is no longer performed automatically. The public name/signature is kept
    for backward compatibility with callers.
    
    Raises:
        RuntimeError: If Docker is not installed / not usable.
    """
    ...

# From docker_utils
def pull_docker_image(docker_image: str) -> Optional[subprocess.Popen]:
    """
    Download a docker image.
    
    Args:
        docker_image: Name/URL of the docker image to pull
    
    Returns:
        subprocess.Popen object if successful, None if failed
    
    Raises:
        Exception: If docker pull fails
    """
    ...

# From docker_utils
def start_docker() -> None:
    """
    Ensure the Docker daemon is usable.
    
    Starting the daemon (systemctl / init.d) requires root, so this no longer
    shells out to start it. If Docker is already usable this is a no-op;
    otherwise it raises with operator guidance.
    
    Raises:
        RuntimeError: If the Docker daemon is not usable.
    """
    ...

# From docker_utils
def test_docker() -> bool:
    """
    Test if Docker is installed and running properly.
    
    Returns:
        bool: True if Docker is installed and running correctly, False otherwise
    """
    ...

# From docker_utils
def try_host_docker() -> bool:
    """
    Check whether the host already has a usable Docker.
    
    Previously this ran ``apt-get install`` (root). It now only *checks* the
    existing host Docker and never installs.
    
    Returns:
        bool: True if host Docker is usable, False otherwise.
    """
    ...

# From docker_utils
def uninstall_docker() -> None:
    """
    Deprecated no-op: uninstalling Docker requires root and is no longer
    performed automatically. Kept for backward compatibility.
    
    Raises:
        RuntimeError: Always — signals that manual, privileged action is needed.
    """
    ...

# From metrics_calculator
def accuracy(output, target, topk = (1,)) -> Any:
    """
    Computes the accuracy over the k top predictions for the specified values of k
    """
    ...

# From metrics_calculator
def accuracy_per_class(output, target) -> Any:
    ...

# From metrics_calculator
def calculate_ap(predictions, targets, iou_threshold) -> Any:
    """
    Calculate Average Precision for a single class at a specific IoU threshold
    """
    ...

# From metrics_calculator
def calculate_auc_pr(outputs, targets, num_classes) -> Any:
    ...

# From metrics_calculator
def calculate_auc_roc(outputs, targets, num_classes) -> Any:
    ...

# From metrics_calculator
def calculate_cohen_kappa(predictions, targets) -> Any:
    ...

# From metrics_calculator
def calculate_detection_metrics(outputs, targets, num_classes) -> Any:
    ...

# From metrics_calculator
def calculate_log_loss(outputs, targets) -> Any:
    ...

# From metrics_calculator
def calculate_mAP_metrics(outputs, targets, num_classes) -> Any:
    ...

# From metrics_calculator
def calculate_mAR_metrics(outputs, targets, num_classes) -> Any:
    """
    Calculate average recall metrics for object detection.
    """
    ...

# From metrics_calculator
def calculate_mcc(predictions, targets) -> Any:
    ...

# From metrics_calculator
def calculate_metrics(output, target) -> Any:
    """
    Calculate true positives, true negatives, false positives, and false negatives for a
        multi-class classification.
    """
    ...

# From metrics_calculator
def calculate_precision_recall(all_predictions, targets, matched_targets, iou_threshold, total_tp, total_fp, total_gt) -> Any:
    ...

# From metrics_calculator
def calculate_recall_at_iou(predictions, targets, iou_threshold) -> Any:
    """
    Calculate recall at a specific IoU threshold for a single class.
    """
    ...

# From metrics_calculator
def collect_predictions_and_targets(outputs, targets, label) -> Any:
    ...

# From metrics_calculator
def confusion_matrix(output, target) -> Any:
    ...

# From metrics_calculator
def confusion_matrix_per_class(output, target) -> Any:
    ...

# From metrics_calculator
def f1_score_per_class(output, target) -> Any:
    ...

# From metrics_calculator
def find_best_match(pred_box, targets, matched_targets, iou_threshold) -> Any:
    ...

# From metrics_calculator
def get_classification_evaluation_results(split_type, outputs, targets, index_to_labels) -> Any:
    ...

# From metrics_calculator
def get_object_detection_evaluation_results(split, all_outputs, all_targets, index_to_labels) -> Any:
    """
    Calculate and format object detection evaluation metrics.
    
    Args:
        split: Dataset split type (e.g., 'train', 'val', 'test')
        all_outputs: Model predictions
        all_targets: Ground truth annotations
        index_to_labels: Mapping from class indices to label names
    
    Returns:
        List of dictionaries containing formatted metrics
    """
    ...

# From metrics_calculator
def precision(output, target) -> Any:
    ...

# From metrics_calculator
def recall(output, target) -> Any:
    ...

# From metrics_calculator
def specificity(output, target) -> Any:
    ...

# From metrics_calculator
def specificity_all(output, target) -> Any:
    ...

# From metrics_calculator_oop
def accuracy(output, target, topk = (1,)) -> Any:
    """
    Compute accuracy for top k predictions
    """
    ...

# From metrics_calculator_oop
def calculate_metrics(output, target) -> Any:
    """
    Calculate TP, TN, FP, FN for multi-class classification
    """
    ...

# From metrics_calculator_oop
def get_classification_evaluation_results(split_type, outputs, targets, index_to_labels) -> Any:
    ...

# From metrics_calculator_oop
def get_object_detection_evaluation_results(split, outputs, targets, index_to_labels) -> Any:
    ...

# From model_store
def byom_status_summary(session, project_id, project_name) -> Any:
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
    ...

# From model_store
def check_family_exists_by_name(session, family_name) -> Any:
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
    ...

# From model_store
def fetch_supported_runtimes_metrics(session, project_id, model_inputs, model_outputs) -> Any:
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
    ...

# From model_store
def get_all_model_families(session, project_id, project_name = None, project_type = 'classification') -> Any:
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
    ...

# From model_store
def get_all_models(session, project_id = None, project_name = None, project_type = 'classification') -> Any:
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
    ...

# From model_store
def get_automl_config(session, project_id, model_count, recommended_runtime, performance_tradeoff, tuning_type = 'auto') -> Any:
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
    ...

# From model_store
def list_private_model_archs(session, project_id = None, project_name = None, page_size = 10, page_num = 0) -> Any:
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
    ...

# From model_store
def list_private_model_families(session, project_id = None, project_name = None, page_size = 10, page_num = 0) -> Any:
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
    ...

# From model_store
def list_public_model_archs(session, project_type = 'classification', page_size = 10, page_num = 0) -> Any:
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
    ...

# From model_store
def list_public_model_families(session, project_type = 'classification', page_size = 10, page_num = 0) -> Any:
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
    ...

# From security_utils
def redact_url(url) -> Any:
    """
    Return a URL that is safe to log.
    
        Strips the query string (which for presigned S3 URLs carries the signature
        that *is* the credential) and any ``user:pass@`` userinfo (RTSP camera feed
        credentials), keeping only scheme, host[:port] and path so logs remain
        useful without leaking secrets.
    """
    ...

# From security_utils
def safe_extractall_zip(zip_ref, dest_dir) -> Any:
    """
    Extract a ``zipfile.ZipFile`` with a zip-slip guard.
    
        Rejects members with absolute paths or ``..`` traversal that would resolve
        outside ``dest_dir`` before extracting anything.
    """
    ...

# From security_utils
def validate_download_url(url, allow_http = False) -> Any:
    """
    Validate an outbound download URL; fail closed on anything suspicious.
    
        * Enforces an https-only scheme allowlist (pass ``allow_http=True`` only for
          explicitly trusted internal callers).
        * Resolves the hostname and rejects the request if **any** resolved A/AAAA
          record is private/loopback/link-local/reserved/multicast or the cloud
          metadata endpoint (169.254.169.254), mitigating SSRF and DNS-rebinding
          that targets only a subset of records.
    
        Returns the URL unchanged when valid; raises ``ValueError`` otherwise.
    """
    ...

# Classes
# From action
class Action:
    """
    Represents an action within the system.
    
    This class provides an interface to interact with a specific action identified by its
    action_id. It retrieves the action's details such as type, project, user, status,
    creation time, and associated service from the API.
    
    Attributes
    ----------
    action_id : str
        The unique identifier for this action.
    action_type : str
        The type of action (retrieved from the API response).
    project_id : str
        The unique ID of the project associated with this action.
    user_id : str
        The unique ID of the user who triggered the action.
    step_code : str
        A code representing the current step of the action process.
    status : str
        The current status of the action (e.g., "pending", "completed").
    created_at : str
        The timestamp when the action was initiated.
    service_name : str
        The name of the service handling this action.
    
    Methods
    -------
    __init__(session, action_id)
        Initializes the Action object and fetches the action details from the API.
    
    refresh()
        Refreshes the action instance, updating its details by calling the API again.
    
    Examples
    --------
    >>> session = RPCSession()  # Assuming `RPCSession` is an existing session class
    >>> action = Action(session, "action_id_1234")
    >>> print(action.action_type)  # Output the type of action
    """

    def __init__(self, session, action_id) -> None:
        """
        Initializes the Action object and fetches the action details from the API.
        
        Parameters
        ----------
        session : RPCSession
            An active session object that is used to make API calls.
        action_id : str
            The unique identifier for the action whose details need to be fetched.
        
        Notes
        -----
        This constructor calls the `get_action_details` function to retrieve the action details,
        which are then set as attributes of the Action object.
        
        If an error occurs while fetching the action details, an error message will be printed.
        """
        ...

    pass

# From action_tracker
class ActionTracker:
    """
    Tracks and manages the status, actions, and related data of a model's lifecycle,
    including training, evaluation, and deployment processes.
    
    The `ActionTracker` is responsible for tracking various stages of an action (e.g.,
    model training, evaluation, or deployment),
    logging details, fetching configuration parameters, downloading model checkpoints,
    and handling error logging.
    It interacts with the backend system to retrieve and update action statuses.
    
    Parameters
    ----------
    action_id : str, optional
        The unique identifier of the action to be tracked. If not provided, the class will
            initialize without an active action.
        The `action_id` is typically linked to specific activities such as model training,
        evaluation, or deployment.
    
    Attributes
    ----------
    rpc : RPCClient
        A Remote Procedure Call (RPC) client for interacting with the backend API.
    action_id : bson.ObjectId
        The ObjectId representing the action being tracked. This is used for retrieving action
            details from the backend.
    action_id_str : str
        The string representation of the `action_id`.
    action_doc : dict
        The detailed document containing information about the action, including its status, type,
        and related model details.
    action_type : str
        The type of action being tracked, such as 'model_train', 'model_eval', or 'deploy_add'.
    _idModel : bson.ObjectId
        The ObjectId of the model associated with the current action.
    _idModel_str : str
        The string representation of `_idModel`.
    session : Session
        A session object that manages the user session and ensures that API requests are authorized.
    
    Examples
    --------
    >>> tracker = ActionTracker(action_id="60f5f5bfb5a1c2a123456789")
    >>> tracker.get_job_params()
    >>> tracker.update_status("training", "in_progress", "Model training started")
    >>> tracker.log_epoch_results(1, [{'loss': 0.25, 'accuracy': 0.92}])
    """

    def __init__(self, action_id = None, session = None) -> None:
        """
        Initializes the ActionTracker instance and retrieves details related to the specified
            action ID.
        
        This constructor fetches the action document, which contains metadata about the action,
        including the model's ID.
        If no `action_id` is provided, the tracker is initialized without an action.
        
        Parameters
        ----------
        action_id : str, optional
            The unique identifier of the action to track. If not provided, the instance is
                initialized without an action.
        
        Raises
        ------
        ConnectionError
            If there is an error retrieving action details from the backend.
        SystemExit
            If there is a critical error during initialization, causing the system to terminate.
        
        Examples
        --------
        >>> tracker = ActionTracker(action_id="60f5f5bfb5a1c2a123456789")
        >>> print(tracker.action_type)  # Outputs the action type, e.g., "model_train"
        """
        ...

    def add_index_to_category(self, indexToCat) -> Any:
        """
        Adds an index-to-category mapping to the model.
        
                This function is used to establish a relationship between numerical indices
                and their corresponding categorical labels for the model. This mapping is
                essential for interpreting the model's output, particularly when the
                model is designed to classify input data into distinct categories.
        
                When to Use:
                -------------
                - This function is typically called after the model has been trained
                but before deploying the model for inference. It ensures that the
                indices output by the model during predictions can be accurately
                translated to human-readable category labels.
                - It is also useful when there are changes in the class labels
                or when initializing a new model.
        
                Parameters
                ----------
                indexToCat : dict
                    A dictionary mapping integer indices to category names. For example,
                    `{0: 'cat', 1: 'dog', 2: 'bird'}` indicates that index 0 corresponds
                    to 'cat', index 1 to 'dog', and index 2 to 'bird'.
        
                Raises
                ------
                Exception
                    If an error occurs while trying to add the mapping, it logs the error
                    details and exits the process.
        
                Examples
                --------
                >>> index_mapping = {0: 'cat', 1: 'dog', 2: 'bird'}
                >>> add_index_to_category(index_mapping)
        """
        ...

    def calculate_metrics(self, split_type, outputs, targets, project_type, images = None) -> Any:
        ...

    def download_model(self, model_path, model_type = 'trained', model_id = None) -> Any:
        """
        Downloads a model from the backend system.
        
                Parameters
                ----------
                model_path : str
                    The path to save the downloaded model. The file will be saved at this location after
                        downloading.
                model_type : str, optional
                    The type of the model ("trained" or "exported"). Defaults to "trained".
        
                Returns
                -------
                bool
                    True if the download was successful, False otherwise. The function will log an error
                        and exit if an exception occurs during the download process.
        
                Examples
                --------
                >>> success = download_model("path/to/save/model.pth")
                >>> if success:
                >>>     print("Model downloaded successfully!")
                >>> else:
                >>>     print("Model download failed.")
        """
        ...

    def get_checkpoint_path(self, overrides = None) -> Any:
        """
        Determines the checkpoint path for the model based on the configuration provided.
        
        This function checks if the model's checkpoint should be retrieved from a pre-trained
            source or a specific model ID.
        It also handles downloading the model if necessary.
        
        Parameters
        ----------
        overrides : dict
            A dictionary containing configuration parameters to override the default job parameters,
            such as `checkpoint_type` and `checkpoint_value`.
        
        Returns
        -------
        tuple
            A tuple containing:
            - The absolute path of the model checkpoint if found, None otherwise
            - A boolean indicating whether the model is pre-trained
        
        Raises
        ------
        FileNotFoundError
            If the model checkpoint cannot be downloaded or located
        ConnectionError
            If there is an issue communicating with the model's API
        ValueError
            If an invalid checkpoint type is provided
        
        Examples
        --------
        >>> config = {"checkpoint_type": "model_id", "checkpoint_value": "12345abcde"}
        >>> checkpoint_path, is_pretrained = tracker.get_checkpoint_path(config)
        >>> print(checkpoint_path, is_pretrained)
        """
        ...

    def get_index_to_category(self, is_exported = None) -> Any:
        """
        Fetches the index-to-category mapping for the model.
        
                This function retrieves the current mapping of indices to categories
                from the backend system. This is crucial for understanding the model's
                predictions, as it allows users to decode the model outputs back
                into meaningful category labels.
        
                When to Use:
                -------------
                - This function is often called before making predictions with the model
                to ensure that the index-to-category mapping is up to date and correctly
                reflects the model's configuration.
                - It can also be used after exporting a model to validate that the
                expected mappings are correctly stored and accessible.
        
                Parameters
                ----------
                is_exported : bool, optional
                    A flag indicating whether to fetch the mapping for an exported model.
                    Defaults to False. If True, the mapping is retrieved based on the export ID.
        
                Returns
                -------
                dict
                    The index-to-category mapping as a dictionary, where keys are indices
                    and values are corresponding category names.
        
                Raises
                ------
                Exception
                    If an error occurs during the retrieval process, it logs the error
                    details and exits the process.
        
                Examples
                --------
                >>> mapping = get_index_to_category()
                >>> print(mapping)
                {0: 'cat', 1: 'dog', 2: 'bird'}
        
                >>> exported_mapping = get_index_to_category(is_exported=True)
                >>> print(exported_mapping)
                {0: 'cat', 1: 'dog'}
        """
        ...

    def get_input_size(self) -> Any:
        ...

    def get_job_params(self) -> Any:
        """
        Fetches the parameters for the job associated with the current action.
        
        This method retrieves the parameters required to perform a specific action,
        such as model training or evaluation.
        The parameters are returned as a dot-accessible dictionary (`_dotdict`) for convenience.
        
        Returns
        -------
        _dotdict
            A dot-accessible dictionary containing the job parameters.
        
        Raises
        ------
        KeyError
            If the job parameters cannot be found in the action document.
        SystemExit
            If the job parameters cannot be retrieved and the system needs to terminate.
        
        Examples
        --------
        >>> job_params = tracker.get_job_params()
        >>> print(job_params.learning_rate)  # Accessing parameters using dot notation
        """
        ...

    def get_model_details(self) -> Any:
        ...

    def get_model_train(self, is_exported = False) -> Any:
        ...

    def log_epoch_results(self, epoch, epoch_result_list) -> Any:
        """
        Logs the results of an epoch during model training or evaluation.
        
        This method records various metrics (like loss and accuracy) for a specific epoch.
        It updates the action status and logs the results for tracking purposes.
        
        Parameters
        ----------
        epoch : int
            The epoch number for which the results are being logged.
        results : list of dict
            A list of dictionaries containing the metric results for the epoch.
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            If the epoch number is invalid.
        
        Examples
        --------
        >>> tracker.log_epoch_results(1, [{'loss': 0.25, 'accuracy': 0.92}])
        """
        ...

    def round_metrics(self, epoch_result_list) -> Any:
        """
        Rounds the metrics in the epoch results to 4 decimal places.
        
                Parameters
                ----------
                epoch_result_list : list
                    A list of result dictionaries for the epoch. Each dictionary contains:
                        - "metricValue" (float): The value of the metric to be rounded.
        
                Returns
                -------
                list
                    The updated list of epoch results with rounded metrics. Each metric value is rounded to four decimal places, with special handling for invalid values (NaN or infinity).
        
                Examples
                --------
                >>> results = [{'metricValue': 0.123456}, {'metricValue': float('in')}, {'metricValue':
                    None}]
                >>> rounded_results = round_metrics(results)
                >>> print(rounded_results)
                [{'metricValue': 0.1235}, {'metricValue': 0}, {'metricValue': 0.0001}]
        """
        ...

    def save_benchmark_results(self, latency_ms, batch_size = 1) -> Any:
        ...

    def save_evaluation_results(self, list_of_result_dicts) -> Any:
        """
        Saves the evaluation results for a model.
        
                Parameters
                ----------
                list_of_result_dicts : list
                    A list of dictionaries containing the evaluation results. Each dictionary should
                        include relevant metrics and their values for the model's performance.
        
                Raises
                ------
                Exception
                    Logs an error and exits if an exception occurs during the saving process.
        
                Examples
                --------
                >>> evaluation_results = [
                >>>     {"metricName": "accuracy", "metricValue": 0.95, "splitType": "val",
                "category": "all"},
                >>>     {"metricName": "loss", "metricValue": 0.05, "splitType": "val",
                "category": "class_1"},
                >>> ]
                >>> save_evaluation_results(evaluation_results)
        """
        ...

    def store_inference_results(self, images, outputs, targets, split_type, project_type, format_inputs = True, pil_images = False, yolo_format = False) -> Any:
        ...

    def update_prediction_results(self, predictions) -> Any:
        """
        Update prediction results by converting category indices to category names.
        
                Handles various prediction formats:
                - Classification: single prediction dict or list of prediction dicts
                - Detection: list of detection results (each containing list of detections)
                - Frame-based: dict with frame keys and detection lists as values
        """
        ...

    def update_status(self, stepCode, status, status_description) -> None:
        """
        Updates the status of the tracked action in the backend system.
        
        This method allows changing the action's status, such as from "in progress" to "completed"
            or "error".
        It logs the provided message with the updated status.
        
        Parameters
        ----------
        action_name : str
            The name of the action being tracked (e.g., "training", "evaluation").
        status : str
            The new status to set for the action (e.g., "in_progress", "completed", "error").
        message : str
            A message providing context about the status update.
        
        Returns
        -------
        None
        
        Examples
        --------
        >>> tracker.update_status("training", "completed", "Training completed successfully")
        """
        ...

    def upload_checkpoint(self, checkpoint_path, model_type = 'trained') -> Any:
        """
        Uploads a model checkpoint to the backend system.
        
                Parameters
                ----------
                checkpoint_path : str
                    The file path of the checkpoint to upload. This should point to a valid model
                        checkpoint file.
                model_type : str, optional
                    The type of the model ("trained" or "exported"). Defaults to "trained",
                    which refers to a model that has been trained but not yet exported.
        
                Returns
                -------
                bool
                    True if the upload was successful, False otherwise. The function will log an error and
                        exit if an exception occurs during the upload process.
        
                Examples
                --------
                >>> success = upload_checkpoint("path/to/checkpoint.pth")
                >>> if success:
                >>>     print("Checkpoint uploaded successfully!")
                >>> else:
                >>>     print("Checkpoint upload failed.")
        """
        ...


# From action_tracker
class LocalActionTracker:
    """
    Placeholder class for local action tracking.
    """

    pass

# From annotation
class Annotation:
    """
    Initialize an Annotation instance for managing annotation-related operations.
    
    This constructor sets up the `Annotation` instance using the provided session, and either
    the `annotation_id` or `annotation_name`. If only `annotation_name` is provided, the
    class attempts to retrieve the `annotation_id` based on the name. Similarly, if both
    `annotation_id` and `annotation_name` are given, the method checks for consistency.
    
    Parameters
    ----------
    session : Session
        The session object that manages the connection to the API.
    annotation_id : str, optional
        The unique identifier for the annotation (default is None).
    annotation_name : str, optional
        The name of the annotation to fetch if `annotation_id` is not provided (default is "").
    
    Raises
    ------
    ValueError
        If neither `annotation_id` nor `annotation_name` is provided, or if there is a mismatch between
        `annotation_id` and `annotation_name`.
    
    Attributes
    ----------
    project_id : str
        Identifier for the project to which the annotation belongs.
    annotation_id : str
        Identifier for the annotation, retrieved based on the provided `annotation_name` if not specified.
    annotation_name : str
        Name of the annotation.
    rpc : RPC
        The RPC interface from the session for communicating with the API.
    annotation_details : dict
        Detailed information about the annotation, retrieved during initialization.
    version_status : str
        The processing status of the latest annotation version.
    latest_version : str
        Identifier of the latest version of the annotation dataset.
    last_updated_at : str
        Timestamp indicating when the annotation was last updated.
    project_type : str
        The type of project associated with the annotation.
    
    Example
    -------
    >>> session = Session(account_number="account_number", access_key="access_key", secret_key="secret_key")
    >>> annotation = Annotation(session, annotation_id="5678",annotation_name="annotation_name")
    >>> print(annotation.annotation_name)
    >>> print(annotation.version_status)
    """

    def __init__(self, session, annotation_id = None, annotation_name = None) -> None:
        ...

    def add_label(self, labelname) -> Any:
        """
        Adds a new label for the annotation. The `annotation_id` and `project_id`
        must be set in the class instance.
        
        Parameters
        ----------
        labelname : str
            The name of the new label.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response confirming the addition of the label, including:
                - `_id` (str): Unique identifier for the new label.
                - `name` (str): Name of the label.
                - `createdAt` (str): Timestamp when the label was created.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.
        
        Example
        -------
        >>> from pprint import pprint
        >>> label_resp, err, msg = annotation.add_label(labelname="Animal")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(label_resp)
        """
        ...

    def annotate_classification_item(self, file_id, annotation_item_id, classification_label, labeller, reviewer, status, issues, label_time, review_time) -> Any:
        """
        Add annotation data to a specific file. The `annotation_id` and `project_id`
        must be set in the class instance.
        
        Parameters
        ----------
        file_id : str
            The ID of the file being annotated.
        annotation_item_id : str
            The ID of the annotation item.
        classification_label : dict
            The classification label for the item, structured as:
                - `_idCategory` (str): The ID of the category.
                - `categoryName` (str): The name of the category.
        labeller : dict
            Information about the labeller, including:
                - `_idUser` (str): The user ID of the labeller.
                - `name` (str): Name of the labeller.
        reviewer : dict
            Information about the reviewer, including:
                - `_idUser` (str): The user ID of the reviewer.
                - `name` (str): Name of the reviewer.
        status : str
            The status of the annotation (e.g., "Completed").
        issues : str
            Any issues identified during the annotation process.
        label_time : int
            The time taken to label the item, in seconds.
        review_time : int
            The time taken to review the item, in seconds.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response confirming the addition of the annotation item.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Example
        -------
        >>> from pprint import pprint
        >>> annotation_resp, err, msg = annotation.annotate_classification_item(
        ...     file_id="file123", annotation_item_id="item456",
        ...     classification_label={"_idCategory": "cat1", "categoryName": "Dog"},
        ...     labeller={"_idUser": "user123", "name": "John Doe"},
        ...     reviewer={"_idUser": "user456", "name": "Jane Doe"},
        ...     status="Completed", issues="", label_time=120, review_time=30
        ... )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(annotation_resp)
        """
        ...

    def create_dataset(self, is_create_new, old_dataset_version, new_dataset_version, new_version_description) -> Any:
        """
        Create or update a dataset based on annotation data. The `annotation_id` and `project_id`
        must be set in the class instance.
        
        Parameters
        ----------
        is_create_new : bool
            Whether to create a new dataset version (`True`) or update an existing one (`False`).
        old_dataset_version : str
            The version identifier of the old dataset.
        new_dataset_version : str
            The version identifier of the new dataset.
        new_version_description : str
            The description for the new dataset version.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response confirming the creation or update of the dataset.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Example
        -------
        >>> from pprint import pprint
        >>> dataset_resp, err, msg = annotation.create_dataset(
        ...     is_create_new=True, old_dataset_version="v1.0",
        ...     new_dataset_version="v2.0", new_version_description="Updated Version"
        ... )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(dataset_resp)
        """
        ...

    def delete(self) -> Any:
        """
        Delete the entire annotation task. The `annotation_id` and `project_id` must be set in the class instance.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response confirming the annotation deletion.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.
        
        Example
        -------
        >>> from pprint import pprint
        >>> delete, err, msg = annotation.delete()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(delete)
        """
        ...

    def delete_item(self, annotation_item_id) -> Any:
        """
        Delete a specific annotation item. The `annotation_id` and `project_id` must be set
        in the class instance.
        
        Parameters
        ----------
        annotation_item_id : str
            The ID of the annotation item to delete.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response confirming the deletion of the annotation item.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.
        
        Example
        -------
        >>> from pprint import pprint
        >>> delete_resp, err, msg = annotation.delete_item(annotation_item_id="item123")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(delete_resp)
        """
        ...

    def get_annotation_files(self, page_size = 10, page_number = 0) -> Any:
        """
        Fetch the files associated with a specific annotation. The `annotation_id` and `project_id`
        must be set in the class instance.
        
        Parameters
        ----------
        page_size : int, optional
            Number of files to retrieve per page (default is 10).
        page_number : int, optional
            Page number to retrieve (default is 0).
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response with a list of files associated with the annotation.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Example
        -------
        >>> from pprint import pprint
        >>> files, err, msg = annotation.get_annotation_files(page_size=10, page_number=0)
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(files)
        """
        ...

    def get_categories(self) -> Any:
        """
        Fetch categories for a specific annotation by its ID. The `annotation_id` must be set in
        the class instance.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response with details about the categories.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Example
        -------
        >>> from pprint import pprint
        >>> categories, err, msg = annotation.get_categories()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(categories)
        """
        ...

    def get_item_history(self, annotation_item_id) -> Any:
        """
        Fetch the annotation history for a specific item. The `annotation_id` and `project_id`
        must be set in the class instance.
        
        Parameters
        ----------
        annotation_item_id : str
            The ID of the annotation item for which history is being fetched.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response with the annotation history details.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Example
        -------
        >>> from pprint import pprint
        >>> history, err, msg = annotation.get_annotation_history(annotation_item_id="12345")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(history)
        """
        ...

    def list_items(self, page_size = 10, page_number = 0) -> Any:
        """
        Retrieve a paginated list of items associated with the annotation. The `annotation_id` and
        `project_id` must be set in the class instance.
        
        Parameters
        ----------
        page_size : int, optional
            The number of items to retrieve per page (default is 10).
        page_number : int, optional
            The page number to retrieve (default is 0).
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response with the annotation items.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.
        
        Example
        -------
        >>> from pprint import pprint
        >>> items, err, msg = annotation.list_items(page_size=10, page_number=0)
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(items)
        """
        ...

    def rename(self, annotation_title) -> Any:
        """
        Rename the annotation with the specified title. The annotation ID must be set in the class instance.
        
        Parameters
        ----------
        annotation_title : str
            The new title for the annotation.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response confirming the annotation title update.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.
        
        Example
        -------
        >>> from pprint import pprint
        >>> rename, err, msg = annotation.rename(annotation_title="New Title")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(rename)
        """
        ...

    def update_classification_item(self, file_id, annotation_item_id, updated_classification_label, labeller, reviewer, status, issues, label_time, review_time) -> Any:
        """
        Update annotation data for a specific file. The `annotation_id` and `project_id` must
        be set in the class instance.
        
        Parameters
        ----------
        file_id : str
            The ID of the file being annotated.
        annotation_item_id : str
            The ID of the annotation item.
        updated_classification_label : dict
            The updated classification label for the item, structured as:
                - `_idCategory` (str): The ID of the category.
                - `categoryName` (str): The name of the category.
        labeller : dict
            Information about the labeller, including:
                - `_idUser` (str): The user ID of the labeller.
                - `name` (str): Name of the labeller.
        reviewer : dict
            Information about the reviewer, including:
                - `_idUser` (str): The user ID of the reviewer.
                - `name` (str): Name of the reviewer.
        status : str
            The status of the annotation (e.g., "Completed").
        issues : str
            Any issues identified during the annotation process.
        label_time : int
            The time taken to label the item, in seconds.
        review_time : int
            The time taken to review the item, in seconds.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response confirming the update of the annotation item.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.
        
        Example
        -------
        >>> from pprint import pprint
        >>> update_resp, err, msg = annotation.update_classification_item(
        ...     file_id="file123", annotation_item_id="item456",
        ...     updated_classification_label={"_idCategory": "cat1", "categoryName": "Dog"},
        ...     labeller={"_idUser": "user123", "name": "John Doe"},
        ...     reviewer={"_idUser": "user456", "name": "Jane Doe"},
        ...     status="Completed", issues="", label_time=120, review_time=30
        ... )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(update_resp)
        """
        ...


# From app_integration
class AppIntegrationError(Exception):
    """
    Raised when an individual step of the integration flow fails.
    
        Subclasses ``Exception`` directly; behaviour is unchanged for all callers,
        which catch ``AppIntegrationError`` directly.
    """

    pass

# From app_integration
class AppIntegrator:
    """
    High-level orchestrator that publishes a new application to the Matrice
    platform end-to-end.
    
    Parameters
    ----------
    access_key : str
        Matrice access key (``MATRICE_ACCESS_KEY_ID``).
    secret_key : str
        Matrice secret key (``MATRICE_SECRET_ACCESS_KEY``).
    account_number : str
        Matrice account number. Required when the key does not resolve to a
        single account.
    session : Session, optional
        Pre-built :class:`matrice_common.session.Session`. If supplied, it is
        used verbatim and ``access_key`` / ``secret_key`` / ``account_number``
        are ignored. Useful in notebooks where a session already exists.
    
    Attributes
    ----------
    session : Session
        Live session used for all RPC calls.
    rpc : RPC
        Shortcut to :attr:`Session.rpc`.
    account_number : str
        Account number tied to the session.
    application : Application
        Lower-level :class:`matrice.application.Application` wrapper.
    """

    def __init__(self, access_key = None, secret_key = None, account_number = None) -> None:
        ...

    def add_application_version(self, application_id: str, project_id: str, model_id: str, model_name: str, post_processing: list[dict], runtime: list[str] | None = None, fps_requirements: dict[str, int] | None = None, model_type: str = 'pretrained', gpu_memory_mb = 8000, blog_link: str = '', notebook_link = None, performance = None, metrics: list[dict] | None = None, color_mapping: dict[str, str] | None = None, arch_checkpoints: dict[str, str] | None = None) -> dict:
        """
        Attach a model version to an existing application.
        
        ``post_processing`` is a list of dicts; each dict **must** include at
        least ``usecase`` and ``category`` matching a use-case registered in
        ``matrice_analytics.post_processing``. All other keys map directly to
        fields on the corresponding ``*Config`` dataclass.
        """
        ...

    def approve_application(self, application_id: str, status: str = 'published') -> dict:
        """
        Approve / change the top-level application status.
        """
        ...

    def create_application(self, name: str, project_id: str, project_type: str, industries: list[str], categories: list[str], description: str, cover_image_url = None, blog_link: str = '', notebook_link: str = '', app_type: str = 'Standard', release_stage: str = 'beta', fps_requirements: dict[str, int] | None = None, objects: list[str] | None = None, server_type = None, business_analytics: list[str] | None = None, incident_types: list[dict] | None = None, alerts = None, reset_settings = None) -> dict:
        """
        Create an application. Returns the raw API response dict.
        
        Note that the backend does NOT return the new application's ``_id`` in
        this response; use :meth:`find_application_id` to resolve it by name
        after creation (this is exactly how the UI does it).
        """
        ...

    def delete_application(self, application_id: str) -> dict:
        """
        Delete an application.
        """
        ...

    def find_application_id(self, name: str, page_size: int = 200) -> str:
        """
        Look up an application's ``_id`` by exact name match.
        
        Raises :class:`AppIntegrationError` if the application is not in the
        first page of ``page_size`` results.
        """
        ...

    def get_application(self, application_id: str) -> dict:
        """
        Fetch a single application document.
        """
        ...

    def get_cover_upload_url(self) -> str:
        """
        Return only the presigned URL (caller performs the PUT themselves).
        """
        ...

    def get_model_checkpoint_upload_url(self, project_id: str) -> str:
        """
        Return only the presigned URL (if you want to PUT the file yourself).
        """
        ...

    def get_project_id_by_name(self, project_name: str) -> str:
        """
        Resolve a ``project_id`` from a project name.
        
        Raises :class:`AppIntegrationError` if the project is not found.
        """
        ...

    def integrate_new_app(self) -> dict:
        """
        Run the full end-to-end integration flow.
        
        Either ``project_id`` or ``project_name`` is required. Either
        ``cover_image_path`` (local file to upload) or ``cover_image_url``
        (already uploaded) is required. If ``post_processing`` is provided,
        ``model_name`` must also be provided so the application version can be
        attached.
        
        Parameters
        ----------
        auto_publish : bool, default False
            When ``True`` the top-level application status is flipped to
            ``"published"`` at the end of the flow. Leave ``False`` for the
            normal review workflow.
        
        Returns
        -------
        dict
            Dictionary describing what was done::
        
                {
                  "project_id": str,
                  "checkpoint_url": str,
                  "checkpoint_id": str,
                  "cover_image_url": str | None,
                  "application_id": str,
                  "application_version": dict | None,  # add_model_version response
                  "published": bool,
                }
        """
        ...

    def list_all_application_versions(self, status = None) -> list[dict]:
        """
        Account-wide listing — ``GET /v1/applications/versions``.
        
        Mostly useful for admins auditing approvals; for per-application
        versions use :meth:`list_application_versions`.
        """
        ...

    def list_application_versions(self, application_id: str) -> list[dict]:
        """
        List versions of a specific application.
        """
        ...

    def list_applications(self, page_size: int = 200, page_number: int = 0) -> list[dict]:
        """
        List applications visible to the caller.
        """
        ...

    def list_checkpoints(self, project_id: str) -> list[dict]:
        """
        List model checkpoints registered under a project.
        """
        ...

    def list_projects(self, project_type: str = '', page_size: int = 200, page_number: int = 0) -> list[dict]:
        """
        List all projects on the account.
        
        Thin wrapper around :meth:`Session.list_projects` returning only the
        item list. Use the returned ``_id`` as ``project_id`` when calling
        :meth:`upload_model_checkpoint`.
        """
        ...

    def publish_application_version(self, application_id: str, version: str, status: str = 'published') -> dict:
        """
        Publish a specific application version (e.g. ``"v1.1"``).
        """
        ...

    def register_checkpoint(self, project_id: str, name: str, checkpoint_url: str, model_family: str, model_key: str, class_index_map: dict[str, str] | None = None, dataset: str = '') -> dict:
        """
        Register an already-uploaded checkpoint as a Model Checkpoint.
        
        Returns
        -------
        dict
            The checkpoint document — ``doc["_id"]`` is the ``modelId`` you
            pass to :meth:`add_application_version`.
        
        Raises
        ------
        AppIntegrationError
            If the registration call fails.
        """
        ...

    def upload_and_register_checkpoint(self, project_id: str, checkpoint_path: str, name: str, model_family: str, model_key: str, class_index_map: dict[str, str] | None = None, dataset: str = '') -> dict:
        """
        Combined helper: :meth:`upload_model_checkpoint` +
        :meth:`register_checkpoint`. Returns the registered checkpoint dict.
        """
        ...

    def upload_cover_image(self, image_path: str) -> str:
        """
        Upload an application cover image and return the clean public URL.
        """
        ...

    def upload_model_checkpoint(self, project_id: str, checkpoint_path: str) -> str:
        """
        Upload a checkpoint file to Matrice storage.
        
        Returns
        -------
        str
            The clean public URL of the uploaded object (no querystring).
        
        Raises
        ------
        AppIntegrationError
            If the presigned-URL step or the PUT upload fails.
        """
        ...


# From app_store
class AppStore:
    """
    A class handling to App store operations using backend API.
    
    Attributes
    ----------
    
    session : Session
        The session object used for API interactions
    
        Examples
    --------
    >>> session = Session(account_number="account_number", access_key="access_key", secret_key="secret_key")
    >>> application = Application(session)
    >>> application_by_page = application.get_all_applications_public(page=1, limit=10)
    """

    def __init__(self, session) -> None:
        ...

    def get_all_applications(self, page = 0, limit = 10) -> Any:
        """
        Get all the applications on the platform
        
        This function returns all the applications details that are present on the platform
        
        Parameters
        ----------
        page : str
            The page you want to see. default = 0
        limit : str
            The number of applications in each page. default = 10
        
        Returns
        -------
        dict -
            Dictonary of the applications with the given page number
        """
        ...

    def get_public_application_by_id(self, application_id) -> Any:
        """
        Retrieve a specific public application by its ID.
        
        This endpoint fetches detailed information about a single public application,
        including its models, current version, and related demo information.
        
        Parameters
        ----------
        application_id : str
            The unique identifier of the public application.
        
        Returns
        -------
        tuple
            - dict: The application details including ID, name, cover image, current version, models, and demos.
            - str or None: Error message if any, else None.
            - str: Status message (e.g., "Successfully fetched application details").
        """
        ...


# From application
class Application:
    """
    A class for handling application operations using the backend API.
    
    Attributes
    ----------
    session : Session
        The session object used for API interactions.
    
    
    Examples
    --------
    >>> session = Session(account_number="account_number", access_key="access_key", secret_key="secret_key")
    >>> application = Application(session)
    >>> response = application.delete_application(session, applicationID="664b5df23abcf1c331234561")
    """

    def __init__(self, session) -> None:
        ...

    def add_model_version(self, application_id: str, project_id: str, model_id: str, model_type: str, model_name: str, blog_link: str, post_processing: list[dict], runtime: list[str], fps_requirements: dict[str, int], performance: dict, notebook_link = None, gpu_memory = None, metrics: list[dict] | None = None, color_mapping: dict[str, str] | None = None, arch_checkpoints: dict[str, str] | None = None) -> tuple[dict | None, str | None, str]:
        """
        Add a model version to an application — POST /v1/applications/:id/models (API Backend §4).
        
        **Path:** id = Application ObjectID.
        **Request body (per API):** modelName (required), modelId (required), projectId, modelType (required),
        blogLink, notebookLink, postProcessing, gpuMemory, runtime, metrics, fpsRequirements,
        performance (published, benchmarked, measuredIP), colorMapping, archCheckpoints.
        
        **Response (200):** data = "Model Added Successfully", status = "success".
        
        Parameters
        ----------
        application_id : str
            Application ObjectID (path param :id).
        project_id : str
            Project ID associated with the model.
        model_id : str
            Model ObjectID (e.g. checkpoint _id or trained/exported model id). Required.
        model_type : str
            Model type (e.g. "checkpoint", "trained", "pretrained"). Required.
        model_name : str
            Model version name. Required.
        blog_link : str
            Blog URL. Can be "".
        post_processing : list of dict
            Post-processing configs. Can be [].
        runtime : list of str
            Supported runtimes (e.g. ["pytorch"]). Required.
        fps_requirements : dict
            Must have "minimumFPS" and "maximumFPS" (int). Required.
        performance : dict
            Must have "published" (list of {hardwareName, latencyMS, throughputFPS}),
            "benchmarked" (list), "measuredIP" (list). Can be empty lists.
        notebook_link : str, optional
            Notebook URL. Omitted if None.
        gpu_memory : int, optional
            GPU memory. Omitted if None.
        metrics : list of dict, optional
            Each item: metricName (str), value (float). Omitted if None.
        color_mapping : dict, optional
            class_name -> "#hex_color". Omitted if None.
        arch_checkpoints : dict, optional
            key -> value. Omitted if None.
        
        Returns
        -------
        tuple
            (data, error, message). error is None on success.
        """
        ...

    def approve_application(self, application_id: str, status: str = 'published') -> tuple[dict | None, str | None, str]:
        """
        Approve or publish an application (top-level) — PUT /v1/applications/:id?status= (API Backend §7).
        
        **Middleware:** AuthTeamMemberMiddleware(). **Path:** id = Application ObjectID.
        **Query:** status (required) — "published", "in-review", or "created".
        **Response (200):** data = "Appliction Apporved Successfully", status = "success".
        **Side effects:** Redis cache is flushed after status update.
        
        Parameters
        ----------
        application_id : str
            Application ObjectID.
        status : str, optional
            Target status. Default "published". Use "in-review" or "created" for other states.
        
        Returns
        -------
        tuple
            (data, error, message). error is None on success.
        """
        ...

    def create_application(self, name: str, project_id: str, project_type: str, industries: list[str], categories: list[str], blog_link: str, notebook_link: str, app_type: str, release_stage: str, description: str, fps_requirements: dict[str, int], cover_image = None, objects: list[str] | None = None, server_type = None, business_analytics: list[str] | None = None, incident_types: list[dict] | None = None, alerts = None, reset_settings = None) -> tuple[dict | None, str | None, str]:
        """
        Create an application — POST /v1/applications/ (API Backend §3.1).
        
        **Request body (per API):** name, projectId (ObjectID), accountNumber, description,
        coverImage, notebookLink, projectType, blogLink, industries, categories, objects,
        serverType, appType, releaseStage, businessAnalytics, incidentTypes, alerts,
        resetSettings, fpsRequirements.
        
        **Response (200):** data = "Application Added SuccessFully", status = "success".
        Backend often does not return application _id; resolve via list_applications (match by name).
        
        Parameters
        ----------
        name : str
            Application name. Required.
        project_id : str
            Project ObjectID (projectId). Required.
        project_type : str
            Project type (e.g. "detection"). Sent as projectType.
        industries : list of str
            Industries (e.g. ["general"]). Required.
        categories : list of str
            Categories (e.g. ["general"]). Required.
        blog_link : str
            URL to blog post. Can be "".
        notebook_link : str
            URL to notebook. Can be "".
        app_type : str
            Application type (e.g. "Standard"). Required.
        release_stage : str
            Release stage (e.g. "alpha"). Required.
        description : str
            Short description. Required.
        fps_requirements : dict
            Must have "minimumFPS" and "maximumFPS" (int). Required.
        cover_image : str, optional
            Cover image URL. Omitted if None.
        objects : list of str, optional
            Objects list. Omitted if None.
        server_type : str, optional
            Server type. Omitted if None.
        business_analytics : list of str, optional
            Business analytics. Omitted if None.
        incident_types : list of dict, optional
            Each item: incidentType (str), thresholds (dict), order (str). Omitted if None.
        alerts : dict, optional
            Alerts config. Omitted if None.
        reset_settings : dict, optional
            Reset settings. Omitted if None.
        
        Returns
        -------
        tuple
            (data, error, message). data is API response; error is None on success.
        """
        ...

    def delete_application(self, application_id: str) -> tuple[dict | None, str | None, str]:
        """
        Delete an application — DELETE /v1/applications/:id (API Backend §3.3).
        
        **Middleware:** AuthTeamMemberMiddleware() (team member or owner).
        **Path:** id = Application ObjectID.
        **Response (200):** data = "Appliction Deleted Successfully", status = "success".
        **Side effects:** Redis cache is flushed after deletion.
        
        Parameters
        ----------
        application_id : str
            Application ObjectID.
        
        Returns
        -------
        tuple
            (data, error, message). error is None on success.
        """
        ...

    def delete_model(self, model_id) -> Any:
        """
        Delete a model by its ID.
        
        Only publishers or authorized team members can perform this action.
        
        Parameters
        ----------
        model_id : str
            The unique identifier of the model to be deleted.
        
        Returns
        -------
        tuple
            - dict: The API response indicating the deletion status.
            - str or None: Error message if any, else None.
            - str: Status message (e.g., "Model deleted successfully").
        """
        ...

    def publish_model(self, application_id: str, version: str, status: str = 'published') -> tuple[dict | None, str | None, str]:
        """
        Publish (approve) a specific application version — PUT /v1/applications/version/:id/approve/:version (API Backend §6).
        
        **Middleware:** AuthTeamMemberMiddleware(). **Path:** id = Application ObjectID, version = version string.
        **Query:** status (e.g. "published", "in-review"). **Request body:** None.
        **Response (200):** data = "Appliction Apporved Successfully", status = "success".
        **Side effects:** Redis cache is flushed.
        
        Parameters
        ----------
        application_id : str
            Application ObjectID.
        version : str
            Application version (e.g. "v1.1").
        status : str, optional
            Target status. Default "published".
        
        Returns
        -------
        tuple
            (data, error, message). error is None on success.
        """
        ...


# From camera_management
class CameraManagement:
    """
    A class for handling camera management operations using the backend API.
    
    This includes camera locations, camera groups, camera streams, and camera topics.
    
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
    >>> camera_mgmt = CameraManagement(session)
    >>>
    >>> # Create a location
    >>> location, error, message = camera_mgmt.create_location(
    ...     location_name="Building A",
    ...     street_address="123 Main St",
    ...     city="San Francisco",
    ...     state="CA",
    ...     country="USA"
    ... )
    """

    def __init__(self, session) -> None:
        """
        Initialize the CameraManagement class.
        
        Parameters
        ----------
        session : Session
            The session object with authentication credentials
        """
        ...

    def append_consuming_app_deployment_id(self, camera_id: str, streaming_id: str, topic_type: str, app_deployment_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Append a consuming app deployment ID to a topic.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        streaming_id : str
            The streaming gateway ID
        topic_type : str
            Topic type - "input" or "output"
        app_deployment_id : str
            Application deployment ID to append
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated topic details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def attach_gateway_to_cameras(self, camera_ids: List[str], streaming_gateway_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Attach a streaming gateway to multiple cameras.
        
        Parameters
        ----------
        camera_ids : list of str
            List of camera IDs
        streaming_gateway_id : str
            ID of the streaming gateway
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Operation result
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def check_camera_application_usage(self, camera_id: str, application_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Check if a camera-application combination is in use.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        application_id : str
            The application ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Usage information with 'inUse', 'pipelineIds', 'isActive', 'deploymentId'
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def create_camera_group(self, camera_group_name: str, lan_id: str = '', streaming_gateway_id: str = '', default_stream_settings: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a new camera group.
        
        Parameters
        ----------
        camera_group_name : str
            Name of the camera group
        lan_id : str, optional
            ID of the LAN
        streaming_gateway_id : str, optional
            ID of the streaming gateway
        default_stream_settings : dict, optional
            Default stream settings including make, model, aspectRatio, height, width,
            videoQuality, streamingFPS
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Camera group details
            - str or None: Error message if failed
            - str: Status message
        
        Examples
        --------
        >>> settings = {
        ...     "make": "Hikvision",
        ...     "model": "DS-2CD2143G0-I",
        ...     "aspectRatio": "16:9",
        ...     "height": 1080,
        ...     "width": 1920,
        ...     "videoQuality": 85,
        ...     "streamingFPS": 30
        ... }
        >>> group, error, message = camera_mgmt.create_camera_group(
        ...     camera_group_name="Parking Cameras",
        ...     lan_id="507f1f77bcf86cd799439011",
        ...     streaming_gateway_id="507f1f77bcf86cd799439012",
        ...     default_stream_settings=settings
        ... )
        """
        ...

    def create_camera_group_vms(self, camera_ids: List[str], group_name: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a VMS camera group.
        
                Parameters
                ----------
                camera_ids : list of str
                    List of camera IDs to include in the VMS group
                group_name : str
                    Name of the VMS group
        
                Returns
                -------
                tuple
                    A tuple containing:
                    - dict: VMS group details
                    - str or None: Error message if failed
                    - str: Status message
        """
        ...

    def create_camera_stream(self, camera_name: str, lan_id: str = '', streaming_gateway_id: str = '', cluster_name: str = '', protocol_type: str = 'RTSP', camera_feed_path: str = '', simulation_video_path: str = '', custom_stream_settings: Optional[Dict[str, Any]] = None, applications: Optional[List[Dict[str, Any]]] = None, memory_usage_mb: float = 0.0, is_active: bool = True, custom_schedule: bool = False, location_id: str = '') -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a new camera stream.
        
        When ``cluster_name`` is provided the backend automatically resolves the
        streaming gateway and media storage for the given account + cluster, so
        ``streaming_gateway_id`` can be omitted.
        
        Parameters
        ----------
        camera_name : str
            Name of the camera
        lan_id : str, optional
            ID of the LAN (Local Area Network) the camera belongs to
        streaming_gateway_id : str, optional
            ID of the streaming gateway (not required when cluster_name is set)
        cluster_name : str, optional
            Cluster name – backend auto-assigns gateway and media storage
        protocol_type : str, optional
            Protocol type - "RTSP", "IP", or "FILE" (default: "RTSP")
        camera_feed_path : str, optional
            RTSP URL for live camera feed
        simulation_video_path : str, optional
            S3 path for simulation video (for FILE protocol)
        custom_stream_settings : dict, optional
            Custom stream settings
        applications : list of dict, optional
            List of applications to attach to the camera
        memory_usage_mb : float, optional
            Estimated memory usage in MB
        is_active : bool, optional
            Whether the camera is active (default: True)
        custom_schedule : bool, optional
            Whether the camera uses a custom schedule (default: False)
        location_id : str, optional
            DEPRECATED – use ``lan_id`` instead
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Camera stream details
            - str or None: Error message if failed
            - str: Status message
        
        Examples
        --------
        >>> camera, error, message = camera_mgmt.create_camera_stream(
        ...     camera_name="Entrance Camera 1",
        ...     lan_id="507f1f77bcf86cd799439011",
        ...     cluster_name="thor2",
        ...     protocol_type="RTSP",
        ...     camera_feed_path="rtsp://admin:pass@192.168.1.100:554/stream1"  # pragma: allowlist secret
        ... )
        
        Security note: ``camera_feed_path`` embeds camera credentials in the URL
        (``user:pass@``). Treat this value as a secret -- it is transmitted and
        stored by the backend, so it must never be written to logs or exports.
        Redact it (strip userinfo and query string) before printing.
        """
        ...

    def create_camera_stream_topic(self, camera_id: str, streaming_gateway_id: str, server_id: str, server_type: str, topic_name: str, topic_type: str, ip_address: str, port: int, status: str = 'active', is_active: bool = True, consuming_apps_deployment_ids: Optional[List[str]] = None, app_deployment_id: Optional[str] = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a camera stream topic (Kafka/Redis).
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        streaming_gateway_id : str
            The streaming gateway ID
        server_id : str
            The server ID
        server_type : str
            Server type - "kafka" or "redis"
        topic_name : str
            Name of the topic
        topic_type : str
            Topic type - "input" or "output"
        ip_address : str
            IP address of the server
        port : int
            Port number
        status : str, optional
            Status of the topic (default: "active")
        is_active : bool, optional
            Whether the topic is active (default: True)
        consuming_apps_deployment_ids : list of str, optional
            List of consuming application deployment IDs
        app_deployment_id : str, optional
            Application deployment ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Topic details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def create_camera_streams_batch(self, cameras: List[Dict[str, Any]]) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Create multiple camera streams in batch.
        Checks for existing cameras before creating to avoid duplicate errors.
        Camera group removed from flow.
        
        Parameters
        ----------
        cameras : list of dict
            List of camera configurations. Each dict should contain:
            - accountNumber: str
            - lanId: str (optional – LAN ID)
            - clusterName: str (optional – backend auto-assigns gateway)
            - streamingGatewayId: str (optional if clusterName provided)
            - cameraName: str (optional, auto-generated if not provided)
            - protocolType: str ("RTSP", "IP", or "FILE")
            - cameraFeedPath: str (for RTSP/IP)
            - simulationVideoPath: str (for FILE)
            - customStreamSettings: dict (optional)
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of created/existing camera streams
            - str or None: Error message if failed
            - str: Status message
        
        Examples
        --------
        >>> cameras = [
        ...     {
        ...         "accountNumber": "ACC123",
        ...         "clusterName": "thor2",
        ...         "lanId": "507f1f77bcf86cd799439011",  # pragma: allowlist secret
        ...         "cameraName": "Camera 1",
        ...         "protocolType": "RTSP",
        ...         "cameraFeedPath": "rtsp://192.168.1.100:554/stream1"
        ...     },
        ...     {
        ...         "accountNumber": "ACC123",
        ...         "clusterName": "thor2",
        ...         "lanId": "507f1f77bcf86cd799439011",  # pragma: allowlist secret
        ...         "cameraName": "Camera 2",
        ...         "protocolType": "FILE",
        ...         "simulationVideoPath": "https://s3.amazonaws.com/bucket/video.mp4"
        ...     }
        ... ]
        >>> created_cameras, error, message = camera_mgmt.create_camera_streams_batch(cameras)
        """
        ...

    def delete_camera_group(self, group_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a camera group.
        
                Parameters
                ----------
                group_id : str
                    The camera group ID to delete
        
                Returns
                -------
                tuple
                    A tuple containing:
                    - dict: Deletion confirmation
                    - str or None: Error message if failed
                    - str: Status message
        """
        ...

    def delete_camera_stream(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a camera stream.
        
        Parameters
        ----------
        camera_id : str
            The camera ID to delete
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Deletion confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_camera_group_by_id(self, group_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get a specific camera group by ID.
        
                Parameters
                ----------
                group_id : str
                    The camera group ID
        
                Returns
                -------
                tuple
                    A tuple containing:
                    - dict: Camera group details
                    - str or None: Error message if failed
                    - str: Status message
        """
        ...

    def get_camera_group_dashboard(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get camera group dashboard with pagination.
        
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
                    - dict: Dashboard data with groups and statistics
                    - str or None: Error message if failed
                    - str: Status message
        """
        ...

    def get_camera_group_id_by_camera(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get the camera group ID for a specific camera.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Camera group info
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_camera_group_vms_by_account(self) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all VMS camera groups for the account.
        
                Returns
                -------
                tuple
                    A tuple containing:
                    - list: List of VMS camera groups
                    - str or None: Error message if failed
                    - str: Status message
        """
        ...

    def get_camera_groups_by_account(self) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all camera groups for the account.
        
                Returns
                -------
                tuple
                    A tuple containing:
                    - list: List of camera group dictionaries
                    - str or None: Error message if failed
                    - str: Status message
        """
        ...

    def get_camera_groups_by_gateway_id(self, gateway_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all camera groups for a specific gateway.
        
                Parameters
                ----------
                gateway_id : str
                    The streaming gateway ID
        
                Returns
                -------
                tuple
                    A tuple containing:
                    - list: List of camera groups
                    - str or None: Error message if failed
                    - str: Status message
        """
        ...

    def get_camera_groups_by_group_id_vms(self, group_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get camera groups by VMS group ID.
        
                Parameters
                ----------
                group_id : str
                    The VMS group ID
        
                Returns
                -------
                tuple
                    A tuple containing:
                    - list: List of camera groups
                    - str or None: Error message if failed
                    - str: Status message
        """
        ...

    def get_camera_input_topic_by_camera_id(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get the input topic for a camera.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Input topic details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_camera_output_topic_by_cam_id_and_app_deployment_id(self, camera_id: str, app_deployment_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get camera output topic by camera ID and app deployment ID.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        app_deployment_id : str
            The application deployment ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Output topic details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_camera_output_topics_by_camera_id(self, camera_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all output topics for a camera.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of output topics
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_camera_stream_by_id(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get a specific camera stream by ID.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Camera stream details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_camera_stream_dashboard(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get camera stream dashboard with pagination.
        
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
            - dict: Dashboard data with cameras and statistics
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_camera_streams_by_account(self) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all camera streams for the account.
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of camera streams
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_camera_streams_with_filters(self, camera_group_id: Optional[str] = None, page: int = 1, limit: int = 10, search: Optional[str] = None, protocol_type: Optional[str] = None, feed_path_contains: Optional[str] = None, aspect_ratio: Optional[str] = None, width: Optional[int] = None, height: Optional[int] = None, streaming_fps: Optional[int] = None, memory_min_mb: Optional[float] = None, memory_max_mb: Optional[float] = None) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get camera streams with filtering and pagination support.
        
        All filters are applied client-side after fetching the full camera list
        from the API. They match exactly the column filters exposed in the
        Matrice UI camera table.
        
        Parameters
        ----------
        camera_group_id : str, optional
            DEPRECATED - no longer used.
        page : int, optional
            Page number for pagination (default: 1).
        limit : int, optional
            Number of cameras per page returned by the API (default: 10).
            Increase this when using local filters so enough results are fetched
            before filtering (e.g. ``limit=1000``).
        search : str, optional
            **UI: Camera Name contains** — case-insensitive substring match
            on ``cameraName``, applied client-side.
        protocol_type : str, optional
            **UI: Protocol Type equals** — ``"RTSP"``, ``"FILE"``, or ``"IP"``.
        feed_path_contains : str, optional
            **UI: Feed Path contains** — substring match on ``cameraFeedPath``
            (RTSP/IP) or ``simulationVideoPath`` (FILE), case-insensitive.
        aspect_ratio : str, optional
            **UI: Aspect Ratio equals** — e.g. ``"16:9"``, ``"4:3"``.
            Reads ``customStreamSettings.aspectRatio``.
        width : int, optional
            **UI: Dimensions width equals** — reads ``customStreamSettings.width``.
        height : int, optional
            **UI: Dimensions height equals** — reads ``customStreamSettings.height``.
        streaming_fps : int, optional
            **UI: Streaming FPS equals** — reads ``customStreamSettings.streamingFPS``.
        memory_min_mb : float, optional
            **UI: Memory Usage >=** — lower bound on ``memoryUsageMB``.
        memory_max_mb : float, optional
            **UI: Memory Usage <=** — upper bound on ``memoryUsageMB``.
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: Camera streams matching all supplied filters.
            - str or None: Error message if the API call failed.
            - str: Status message.
        
        Examples
        --------
        >>> # Filter by name (server-side)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     search="entrance", limit=50
        ... )
        
        >>> # Filter by protocol type (local)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     protocol_type="FILE", limit=200
        ... )
        
        >>> # Filter by dimensions + FPS (local)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     width=1920, height=1080, streaming_fps=30, limit=200
        ... )
        
        >>> # Filter by feed path substring (local)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     feed_path_contains="s3.us-west", limit=200
        ... )
        
        >>> # Filter by memory usage range (local)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     memory_min_mb=100, memory_max_mb=500, limit=200
        ... )
        """
        ...

    def get_cameras_batch_info(self, camera_ids: List[str]) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get batch information for multiple cameras.
        
        Parameters
        ----------
        camera_ids : list of str
            List of camera IDs to get info for
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of camera info dictionaries
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_cameras_by_app_deployment(self, app_deployment_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get cameras using a specific application deployment.
        
        Parameters
        ----------
        app_deployment_id : str
            The application deployment ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of cameras
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_cameras_by_group_id(self, group_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all cameras in a specific group.
        
        Parameters
        ----------
        group_id : str
            The camera group ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of cameras
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_cameras_by_inference_pipeline(self, pipeline_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all cameras associated with an inference pipeline.
        
        Parameters
        ----------
        pipeline_id : str
            The inference pipeline ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of camera dictionaries
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_cameras_by_inference_pipeline_filtered(self, pipeline_id: str, **filters) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get cameras for an inference pipeline with filters.
        
        Parameters
        ----------
        pipeline_id : str
            The inference pipeline ID
        **filters
            Query parameters to filter cameras (e.g., status="active")
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of filtered camera dictionaries
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_cameras_by_streaming_gateway_id(self, gateway_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all cameras for a specific streaming gateway.
        
        Parameters
        ----------
        gateway_id : str
            The streaming gateway ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of cameras
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_input_topics_by_app_deployment_id(self, app_deployment_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get input topics for an application deployment.
        
        Parameters
        ----------
        app_deployment_id : str
            The application deployment ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of input topics
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_output_topics_by_app_deployment_id(self, app_deployment_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get output topics for an application deployment.
        
        Parameters
        ----------
        app_deployment_id : str
            The application deployment ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of output topics
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_presigned_url_for_video(self, file_name: str) -> Tuple[Optional[str], Optional[str], str]:
        """
        Get a presigned URL for video upload to S3.
        
        Parameters
        ----------
        file_name : str
            Name of the file to upload
        
        Returns
        -------
        tuple
            A tuple containing:
            - str: Presigned URL for upload
            - str or None: Error message if failed
            - str: Status message
        
        Examples
        --------
        >>> url, error, message = camera_mgmt.get_presigned_url_for_video("my_video.mp4")
        >>> if not error:
        ...     # Use the presigned URL to upload the video
        ...     pass
        """
        ...

    def get_simulated_stream_url(self, camera_id: str) -> Tuple[Optional[str], Optional[str], str]:
        """
        Get the simulated stream URL for a camera.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - str: Simulated stream URL
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_topics_by_server_id(self, server_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all topics for a server.
        
        Parameters
        ----------
        server_id : str
            The server ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of topics
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_topics_by_streaming_id_and_server_id(self, streaming_id: str, server_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get topics by streaming gateway ID and server ID.
        
        Parameters
        ----------
        streaming_id : str
            The streaming gateway ID
        server_id : str
            The server ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of topics
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def list_camera_groups(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        List all camera groups with pagination.
        
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
                    - dict: Paginated camera groups data
                    - str or None: Error message if failed
                    - str: Status message
        """
        ...

    def list_camera_streams(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        List all camera streams with pagination.
        
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
            - dict: Paginated camera streams data
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def remove_camera_application_from_pipeline(self, camera_id: str, application_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Remove a camera application from its pipeline.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        application_id : str
            The application ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Operation result
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def start_recording(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Start recording for a camera.
        
        Parameters
        ----------
        camera_id : str
            The camera ID to start recording
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Recording start confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def stop_recording(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Stop recording for a camera.
        
        Parameters
        ----------
        camera_id : str
            The camera ID to stop recording
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Recording stop confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def update_camera_group(self, group_id: str, camera_group_name: Optional[str] = None, lan_id: Optional[str] = None, streaming_gateway_id: Optional[str] = None, default_stream_settings: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update a camera group.
        
        Parameters
        ----------
        group_id : str
            The camera group ID to update
        camera_group_name : str, optional
            New camera group name
        lan_id : str, optional
            New LAN ID
        streaming_gateway_id : str, optional
            New streaming gateway ID
        default_stream_settings : dict, optional
            New default stream settings
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated camera group details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def update_camera_stream(self, camera_id: str, camera_name: Optional[str] = None, lan_id: Optional[str] = None, streaming_gateway_id: Optional[str] = None, cluster_name: Optional[str] = None, protocol_type: Optional[str] = None, camera_feed_path: Optional[str] = None, simulation_video_path: Optional[str] = None, custom_stream_settings: Optional[Dict[str, Any]] = None, applications: Optional[List[Dict[str, Any]]] = None, is_active: Optional[bool] = None, custom_schedule: Optional[bool] = None, media_storage_id: Optional[str] = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update a camera stream.
        
        Parameters
        ----------
        camera_id : str
            The camera ID to update
        camera_name : str, optional
            New camera name
        lan_id : str, optional
            New LAN ID
        streaming_gateway_id : str, optional
            New streaming gateway ID
        cluster_name : str, optional
            New cluster name
        protocol_type : str, optional
            New protocol type
        camera_feed_path : str, optional
            New camera feed path
        simulation_video_path : str, optional
            New simulation video path
        custom_stream_settings : dict, optional
            New custom stream settings
        applications : list of dict, optional
            New applications list
        is_active : bool, optional
            Whether the camera is active
        custom_schedule : bool, optional
            Whether the camera uses a custom schedule
        media_storage_id : str, optional
            New media storage ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated camera details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def update_topic_ip_and_port(self, camera_id: str, streaming_id: str, topic_type: str, ip_address: str, port: int) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update IP address and port of a topic.
        
        Parameters
        ----------
        camera_id : str
            The camera ID
        streaming_id : str
            The streaming gateway ID
        topic_type : str
            Topic type - "input" or "output"
        ip_address : str
            New IP address
        port : int
            New port number
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated topic details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def upload_video_file(self, video_path: str, file_name: Optional[str] = None) -> Tuple[Optional[str], Optional[str], str]:
        """
        Upload a video file to S3 using a presigned URL.
        
        Parameters
        ----------
        video_path : str
            Path to the local video file
        file_name : str, optional
            Name for the uploaded file (defaults to original filename)
        
        Returns
        -------
        tuple
            A tuple containing:
            - str: S3 URL of the uploaded video
            - str or None: Error message if failed
            - str: Status message
        
        Examples
        --------
        >>> s3_url, error, message = camera_mgmt.upload_video_file("/path/to/video.mp4")
        >>> if not error:
        ...     print(f"Video uploaded to: {s3_url}")
        """
        ...


# From compute
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

    def __init__(self, session, alias) -> None:
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
        ...

    def delete(self) -> Any:
        """
        Update the compute instance attributes if it is not a dedicated instance.
        
        Returns
        -------
        dict or None
            Server response indicating the result of the update request, or None if update is not
                allowed or fails.
        """
        ...

    def stop(self) -> Any:
        """
        Stop an on-demand compute instance.
        
        Returns
        -------
        dict or None
            Server response indicating the result of the stop request, or None if an error occurred.
        """
        ...

    def update(self) -> Any:
        """
        Static method to update the compute instance attributes.
        
        Returns
        -------
        dict or None
            Server response indicating the result of the update request, or None if update is not
                allowed or fails.
        """
        ...


# From compute
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

    def __init__(self, session, instance_type, price_hour, service_provider, machine_eff, compute_eff, gpu_type, gpu_memory, cpu, cores, memory_mb, storage_gb, storage_type) -> None:
        ...

    pass

# From dataset
class Dataset:
    """
    Class to handle dataset-related operations within a project.
    
    This class manages operations on a dataset within a specified project. During initialization,
    either `dataset_name` or `dataset_id` must be provided to locate the dataset.
    
    Parameters
    ----------
    session : Session
        The session object that manages the connection to the server.
    dataset_id : str, optional
        The ID of the dataset (default is None). Used to directly locate the dataset.
    dataset_name : str, optional
        The name of the dataset (default is None). If `dataset_id` is not provided,
        `dataset_name` will be used to find the dataset.
    
    Attributes
    ----------
    dataset_id : str
        The unique identifier for the dataset.
    dataset_name : str
        The name of the dataset.
    version_status : str
        The processing status of the latest dataset version.
    latest_version : str
        The identifier of the latest version of the dataset.
    no_of_samples : int
        The total number of samples in the dataset.
    no_of_classes : int
        The total number of classes in the dataset.
    no_of_versions : int
        The total number of versions for this dataset.
    last_updated_at : str
        The timestamp of the dataset's most recent update.
    summary : dict
        Summary of the dataset's latest version, providing metrics like item count and class
            distribution.
    
    Raises
    ------
    ValueError
        If neither `dataset_id` nor `dataset_name` is provided, or if there is a mismatch between
            `dataset_id` and `dataset_name`.
    
    Example
    -------
    >>> session = Session(account_number=account_number, access_key=access_key, secret_key=secret_key)
    >>> dataset = Dataset(session=session, dataset_id="12345",dataset_name="Sample")
    >>> print(f"Dataset Name: {dataset.dataset_name}")
    >>> print(f"Number of Samples: {dataset.no_of_samples}")
    >>> print(f"Latest Version: {dataset.latest_version}")
    """

    def __init__(self, session, dataset_id = None, dataset_name = None) -> None:
        ...

    def add_data(self, source, source_url, new_dataset_version, old_dataset_version, dataset_description = '', version_description = '', compute_alias = '') -> Any:
        """
        Import a new version of the dataset from an external source. Only ZIP files are supported
            for upload.
        
        This function creates a new dataset version or updates an existing version with data from a
            specified
        external source URL. The dataset ID must be set during initialization for this function to
            work.
        
        Parameters
        ----------
        source : str
            The source of the dataset, indicating where the dataset originates (e.g., "url").
        source_url : str
            The URL of the dataset to be imported.
        new_dataset_version : str
            The version identifier for the new dataset (e.g., "v2.0").
        old_dataset_version : str
            The version identifier of the existing dataset to be updated.
        dataset_description : str, optional
            Description of the dataset (default is an empty string).
        version_description : str, optional
            Description for the new dataset version (default is an empty string).
        compute_alias : str, optional
            Alias for the compute instance to be used (default is an empty string).
        
        Returns
        -------
        tuple
        A tuple containing:
        - dict: API response indicating the status of the dataset import.
        - str or None: Error message if an error occurred, `None` otherwise.
        - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set or if the old dataset version is incomplete.
        
        Example
        -------
        >>> response, err, msg = dataset.add_data(
        >>>     source="url",
        >>>     source_url="https://example.com/dataset.zip",
        >>>     new_dataset_version="v2.0",
        >>>     old_dataset_version="v1.0"
        >>> )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        ...

    def check_valid_spilts(self, dataset_version) -> Any:
        """
        Check if the specified dataset version contains valid splits.
        
        Valid splits include training, validation, and test sets. This function verifies that the
        specified dataset version has these splits properly configured.
        
        Parameters
        ----------
        dataset_version : str
            The version of the dataset to check for valid splits (e.g., "v1.0").
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response indicating split validity, which includes:
                - `isValid` (str): Indicates if the splits are valid.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.
        
        Example
        -------
        >>> split_status, err, msg = dataset.check_valid_splits(dataset_version="v1.0")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(split_status)
        >>>
        >>> # Sample output
        >>>     'Valid Spilts'
        """
        ...

    def delete(self) -> Any:
        """
        Delete the entire dataset.
        
        This function deletes the entire dataset associated with the given dataset ID. The dataset
            ID
        must be set during initialization for this function to work.
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response confirming the dataset deletion status.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.
        
        Example
        -------
        >>> response, err, msg = dataset.delete()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        ...

    def delete_item(self, dataset_version, dataset_item_ids) -> Any:
        """
        Delete items from a specific version of the dataset based on dataset type.
        
        This function deletes items from a specified version of the dataset. The deletion method is
            selected
        automatically based on the dataset type (e.g., classification, detection)
        . The dataset ID must be set
        during initialization for this function to work.
        
        Parameters
        ----------
        dataset_version : str
            The version of the dataset from which to delete items.
        dataset_item_ids : list of str
            A list of dataset item IDs to delete.
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response indicating the deletion status.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        
        Raises
        ------
        ValueError
            If the dataset type is unsupported.
        
        Example
        -------
        >>> response, err, msg = dataset.delete_item(
        >>>     dataset_version="v1.0", dataset_item_ids=["123", "456"]
        >>> )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        ...

    def delete_version(self, dataset_version) -> Any:
        """
        Delete a specific version of the dataset.
        
        This function removes a specified version of the dataset. The dataset ID must be set
        during initialization for this function to work.
        
        Parameters
        ----------
        dataset_version : str
            The version identifier of the dataset to delete (e.g., "v1.0").
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response confirming the deletion status.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.
        
        Example
        -------
        >>> response, err, msg = dataset.delete_version(dataset_version="v1.0")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        ...

    def get_categories(self, dataset_version) -> Any:
        """
        Get category details for a specific dataset version.
        
        This function retrieves the categories available in a specified version of the dataset,
        including category IDs, names, and associated metadata.
        
        Parameters
        ----------
        dataset_version : str
            The version of the dataset for which to fetch categories (e.g., "v1.0").
        
        Returns
        -------
        tuple
            A tuple containing:
            - list of dict: Each dictionary contains dataset category details, including:
                - `_id` (str): Unique identifier for the category.
                - `_idDataset` (str): ID of the dataset to which this category belongs.
                - `_idSuperCategory` (str): Identifier for the super-category, if applicable.
                - `datasetVersion` (str): Version of the dataset for this category.
                - `name` (str): Name of the category.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.
        
        Example
        -------
        >>> categories, err, msg = dataset.get_categories(dataset_version="v1.0")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(categories[:3])
        >>>
        >>> # Sample output
        >>> [
        >>>     {'_id': '671638ef0f4507663b8ca2b7', '_idDataset': '671636dd6cffa65a7510a52b',
        '_idSuperCategory': '000000000000000000000000', 'datasetVersion': 'v1.0', 'name': 'Dog'},
        >>>     {'_id': '671638ef0f4507663b8ca2b6', '_idDataset': '671636dd6cffa65a7510a52b',
        '_idSuperCategory': '000000000000000000000000', 'datasetVersion': 'v1.0', 'name': 'Cat'},
        >>>     ...
        >>> ]
        """
        ...

    def get_processed_versions(self) -> Any:
        """
        Get all processed versions of the dataset.
        
        This function retrieves a list of all versions of the dataset that have completed
            processing.
        
        Returns
        -------
        tuple
            A tuple containing:
            - list of dict: Each dictionary contains processed dataset version details, including:
                - `_id` (str): Unique identifier for the dataset.
                - `_idProject` (str): Project ID associated with the dataset.
                - `allVersions` (list of str): List of all versions of the dataset.
                - `createdAt` (str): Timestamp of when the dataset was created.
                - `latestVersion` (str): Identifier of the latest version of the dataset.
                - `name` (str): Name of the dataset.
                - `processedVersions` (list of str): List of processed versions.
                - `stats` (list of dict): Version-specific statistics, including:
                    - `classStat` (dict): Contains category-specific counts for `test`, `train`,
                    `unassigned`, and `val`.
                    - `version` (str): Version identifier.
                    - `versionDescription` (str): Description of the version.
                    - `versionStats` (dict): Overall statistics, including `total`, `train`, `test`,
                    and `val` counts.
                    - `versionStatus` (str): Status of the version, usually "processed".
                - `updatedAt` (str): Timestamp of the last dataset update.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.
        
        Example
        -------
        >>> processed_versions, err, msg = dataset.get_processed_versions()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(processed_versions[:3])
        >>>
        >>> # Sample output
        >>> [
        >>>     {'_id': '6703af894ddeac5b596b267b', '_idProject': '67036673ccb244bee86d1939',
        'allVersions': ['v1.0', 'v1.1'], 'createdAt': '2024-10-07T09:53:13.223Z',
        'name': 'Microcontroller', 'processedVersions': ['v1.1'], 'latestVersion': 'v1.1', ...},
        >>>     ...
        >>> ]
        """
        ...

    def list_items(self, dataset_version, page_size = 10, page_number = 0) -> Any:
        """
        List items for a specific version of the dataset.
        
        This function retrieves a paginated list of items for the specified dataset version,
        allowing control over the number of items per page and the page number.
        
        Parameters
        ----------
        dataset_version : str
            The version of the dataset to retrieve items from (e.g., "v1.0").
        page_size : int, optional
            The number of items to return per page (default is 10).
        page_number : int, optional
            The page number to retrieve (default is 0).
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response with a list of dataset items, where each item contains:
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.
        
        Example
        -------
        >>> items, err, msg = dataset.list_items(dataset_version="v1.0", page_size=10,
        page_number=0)
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(items)
        """
        ...

    def rename(self, updated_name) -> Any:
        """
        Update the name of the dataset.
        
        This function updates the dataset name to a specified value. The dataset ID must
        be set during initialization for this function to work.
        
        Parameters
        ----------
        updated_name : str
            The new name for the dataset.
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response confirming the dataset name update, including:
                - `MatchedCount` (int): Number of records matched for the update.
                - `ModifiedCount` (int): Number of records modified.
                - `UpsertedCount` (int): Number of records upserted (inserted if not existing).
                - `UpsertedID` (str or None): ID of the upserted record if applicable,
                otherwise `None`.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.
        
        Example
        -------
        >>> response, err, msg = dataset.rename(updated_name="Updated Dataset Name")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        >>>
        >>> # Sample output
        >>> {
        >>>     'MatchedCount': 1,
        >>>     'ModifiedCount': 1,
        >>>     'UpsertedCount': 0,
        >>>     'UpsertedID': None
        >>> }
        """
        ...

    def split_data(self, old_dataset_version, new_dataset_version, is_random_split, train_num = 0, val_num = 0, test_num = 0, transfers = [{'source': '', 'destination': '', 'transferAmount': 1}], dataset_description = '', version_description = '', new_version_description = '', compute_alias = '') -> Any:
        """
        Split or transfer images between training, validation, and test sets in the dataset.
        
        This function enables the creation of a new dataset version by transferring or splitting
            images from an existing
        version into training, validation, and test sets, with options for random or manual split
            distribution.
        
        Parameters
        ----------
        old_dataset_version : str
            The version identifier of the existing dataset.
        new_dataset_version : str
            The version identifier of the new dataset.
        is_random_split : bool
            Indicates whether to perform a random split.
        train_num : int, optional
            Number of training samples (default is 0).
        val_num : int, optional
            Number of validation samples (default is 0).
        test_num : int, optional
            Number of test samples (default is 0).
        transfers : list of dict, optional
            List specifying transfers between dataset sets. Each dictionary should contain:
                - `source` (str): The source set (e.g., "train").
                - `destination` (str): The target set (e.g., "test").
                - `transferAmount` (int): Number of items to transfer (default is 1).
        dataset_description : str, optional
            Description of the dataset (default is an empty string).
        version_description : str, optional
            Description of the dataset version (default is an empty string).
        new_version_description : str, optional
            Description of the new dataset version (default is an empty string).
        compute_alias : str, optional
            Alias for the compute instance (default is an empty string).
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response indicating the status of the dataset split or transfer.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set or if the `old_dataset_version` is not processed.
        
        Example
        -------
        >>> response, err, msg = dataset.split_data(
        >>>     old_dataset_version="v1.0",
        >>>     new_dataset_version="v2.0",
        >>>     is_random_split=True,
        >>>     train_num=100,
        >>>     val_num=20,
        >>>     test_num=30,
        >>>     transfers=[{"source": "train", "destination": "test", "transferAmount": 100}]
        >>> )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        ...

    def update_item_label(self, dataset_version, item_id, label_id) -> Any:
        """
        Update the label of a specific dataset item.
        
        This function assigns a new label to a specific item in a specified dataset version.
        The dataset ID must be set during initialization for this function to work.
        
        Parameters
        ----------
        dataset_version : str
            The version of the dataset where the item resides (e.g., "v1.0").
        item_id : str
            The unique identifier of the dataset item to update.
        label_id : str
            The unique identifier of the new label to assign to the dataset item.
        
        Returns
        -------
        tuple
        A tuple containing:
        - dict: API response confirming the label update.
        - str or None: Error message if an error occurred, `None` otherwise.
        - str: Status message indicating success or failure.
        
        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.
        
        Example
        -------
        >>> response, err, msg = dataset.update_item_label(dataset_version="v1.0", item_id="12345",
        label_id="67890")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        ...


# From drift_monitor
class DriftMonitoring:
    """
    Class for managing drift monitoring operations within a project.
    
    Parameters
    ----------
    session : object
        The session object that provides access to the RPC interface and project ID.
    
    Attributes
    ----------
    session : object
        Session object for facilitating RPC communication.
    project_id : str
        ID of the project associated with this drift monitoring instance.
    rpc : object
        RPC interface for making backend API calls.
    
    Example
    -------
    >>> session = Session(account_number="account_number")
    >>> drift_monitoring = DriftMonitoring(session=session)
    """

    def __init__(self, session) -> None:
        ...

    def add_params(self, _idDeployment, deploymentName, imageStoreConfidenceThreshold, imageStoreCountThreshold) -> Any:
        """
        Add drift monitoring parameters for a specified deployment.
        
        Parameters
        ----------
        _idDeployment : str
            The ID of the deployment.
        deploymentName : str
            The name of the deployment.
        imageStoreConfidenceThreshold : float
            Confidence threshold for storing images.
        imageStoreCountThreshold : int
            Count threshold for storing images.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response indicating the success or failure of adding parameters.
            - str or None:
                Error message if an error occurred, otherwise None.
            - str:
                Message indicating success or error status.
        
        Example
        -------
        >>> from pprint import pprint
        >>> add_params, err, msg = drift_monitoring.add_params(
        ...     _idDeployment="deployment123",
        ...     deploymentName="MyDeployment",
        ...     imageStoreConfidenceThreshold=0.85,
        ...     imageStoreCountThreshold=100
        ... )
        >>> if err:
        ...     pprint(err)
        >>> else:
        ...     pprint(add_params)
        """
        ...

    def update(self, _idDeployment, deploymentName, imageStoreConfidenceThreshold, imageStoreCountThreshold) -> Any:
        """
        Update existing drift monitoring parameters for a specified deployment.
        
        Parameters
        ----------
        _idDeployment : str
            The ID of the deployment.
        deploymentName : str
            The name of the deployment.
        imageStoreConfidenceThreshold : float
            Confidence threshold for storing images.
        imageStoreCountThreshold : int
            Count threshold for storing images.
        
        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response indicating the success or failure of the update.
            - str or None:
                Error message if an error occurred, otherwise None.
            - str:
                Message indicating success or error status.
        
        Example
        -------
        >>> from pprint import pprint
        >>> update, err, msg = drift_monitoring.update(
        ...     _idDeployment="deployment123",
        ...     deploymentName="MyDeployment",
        ...     imageStoreConfidenceThreshold=0.9,
        ...     imageStoreCountThreshold=150
        ... )
        >>> if err:
        ...     pprint(err)
        >>> else:
        ...     pprint(update)
        """
        ...


# From exported_model
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

    def __init__(self, session, model_export_id = None, model_export_name = '') -> None:
        ...

    def add_evaluation(self, dataset_id, dataset_version, split_types, is_gpu_required = True, is_pruned = False) -> Any:
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
        ...

    def delete(self) -> Any:
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
        ...

    def download_model(self, file_name) -> Any:
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
        ...

    def get_details(self) -> Any:
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
        ...

    def get_download_path(self) -> Any:
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
        ...

    def get_evaluation_result(self, dataset_id, dataset_version, split_types) -> Any:
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
        ...

    def get_prediction(self, input_path) -> Any:
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
        ...

    def get_trained_model(self) -> Any:
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
        ...

    def rename(self, updated_name) -> Any:
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
        ...


# From inference_orchestrator
class CustomerOnboardingAutomation:
    """
    Automated inference orchestrator for Matrice AI platform.
    
    This class provides simplified deployment automation that focuses exclusively
    on inference service orchestration. It assumes that infrastructure components
    (Project, Location, Cluster name) have already been provisioned by the
    Backend CLI setup process.
    
    Key Features:
    - Idempotent camera registration (checks existing cameras before creating)
    - Automated pipeline deployment with camera-to-application mappings
    - Real-time health monitoring with configurable timeouts
    - Support for both JSON and CSV configuration formats
    - Comprehensive error handling and status reporting
    
    Workflow:
    1. Parse configuration file and validate required parameters
    2. Authenticate with Matrice AI platform using provided credentials
    3. Synchronize cameras to existing location (idempotent)
    4. Create inference pipeline with camera-application assignments
    5. Start pipeline and monitor health until running state achieved
    
    Attributes
    ----------
    streaming_automation : StreamingAutomation
        Primary API client for pipeline operations
    camera_management : CameraManagement
        Direct API client for camera operations (authoritative)
    pipeline_management : InferencePipelineManagement
        Direct API client for advanced pipeline-specific operations (monitoring)
    session : Session
        Authenticated session object shared across API clients
    project_id : str
        Target project ID from configuration
    lan_id : str
        Target LAN ID from configuration
    cluster_name : str
        Compute cluster name from configuration
    results : Dict
        Deployment results and status tracking
    """

    def __init__(self, account_number: str, access_key: str, secret_key: str, project_id: str, lan_id: str, cluster_name: str) -> None:
        """
        Initialize the automation system with deployment context.
        
        Parameters
        ----------
        account_number : str
            Matrice account number
        access_key : str
            API access key
        secret_key : str
            API secret key
        project_id : str
            Target project ID (already provisioned)
        lan_id : str
            location_id is deprecated, use lan_id instead.
            Target LAN ID (already provisioned)
        cluster_name : str
            Compute cluster alias (already provisioned)
        """
        ...

    def deploy_cameras_and_pipeline(self, cameras_config_path: str, pipeline_name: str = 'Auto-Pipeline', pipeline_config: Optional[PipelineConfig] = None) -> Any:
        """
        Main method: Deploy cameras and pipeline from configuration file.
        
        This method:
        1. Parse camera configuration (JSON/CSV)
        2. Initialize authentication session
        3. Create cameras (idempotent)
        4. Create inference pipeline with camera-app mappings
        5. Start pipeline and monitor health
        
        Parameters
        ----------
        cameras_config_path : str
            Path to cameras configuration file (JSON or CSV)
        pipeline_name : str, optional
            Name for the inference pipeline (default: "Auto-Pipeline")
        pipeline_config : PipelineConfig, optional
            Detailed pipeline configuration (overrides settings from config file)
        
        Returns
        -------
        DeploymentResults
            Deployment results with camera_ids, pipeline_id, errors, success status
        """
        ...


# From inference_orchestrator
class DeploymentResults(TypedDict):
    """
    Type definition for deployment results structure.
    """

    pass

# From inference_pipeline_management
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
    ...     "cameraId": "507f1f77bcf86cd799439016",  # pragma: allowlist secret
    ...     "applications": [{"_idApplication": "507f1f77bcf86cd799439020"}]  # pragma: allowlist secret
    ... }]
    >>> pipeline, error, message = pipeline_mgmt.create_inference_pipeline(
    ...     name="Parking Lot Pipeline",
    ...     project_id="507f1f77bcf86cd799439052",
    ...     cameras=cameras
    ... )
    """

    def __init__(self, session) -> None:
        """
        Initialize the InferencePipelineManagement class.
        
        Parameters
        ----------
        session : Session
            The session object with authentication credentials
        """
        ...

    def add_cameras_and_applications_to_pipeline(self, pipeline_id: str, cameras: List[Dict[str, Any]], compute_alias: str = '', cluster_name: str = '') -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...         "cameraId": "507f1f77bcf86cd799439017",  # pragma: allowlist secret
        ...         "applications": [
        ...             {
        ...                 "_idApplication": "507f1f77bcf86cd799439023",  # pragma: allowlist secret
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
        ...

    def create_inference_pipeline(self, name: str, project_id: str, cameras: List[Dict[str, Any]], user_id: str, description: str = '', access_scale: str = 'local', deploy_type: str = 'real_time', server_type: str = 'fastapi', facial_recognition_server_id: Optional[str] = None, lpr_server_id: Optional[str] = None, aggregators: Optional[List[Dict[str, Any]]] = None, status: str = 'created', compute_alias: str = '', cluster_name: str = '', runtime_framework: str = 'Triton') -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...         "cameraId": "507f1f77bcf86cd799439016",  # pragma: allowlist secret
        ...         "applications": [
        ...             {
        ...                 "_idApplication": "507f1f77bcf86cd799439020",  # pragma: allowlist secret
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
        ...

    def create_inference_pipeline_timing(self, pipeline_id: str, project_id: str, user_id: str, run_type: str, start_time: str, status: str = 'active', latency: Optional[int] = None, step_details: Optional[List[Dict[str, Any]]] = None) -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...

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
        ...

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
        ...

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
        ...

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
        ...

    def get_cameras_without_streaming_gateway(self, pipeline_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
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
        ...

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
        ...

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
        ...

    def get_inference_pipeline_dashboard(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...

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
        ...

    def get_inference_pipeline_timing_by_pipeline(self, pipeline_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
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
        ...

    def get_inference_pipelines_by_account(self) -> Tuple[Optional[List[Dict]], Optional[str], str]:
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
        ...

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
        ...

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
        ...

    def list_inference_pipelines(self, project_id: str, page: int = 1, limit: int = 10, sort_by: str = '', sort_order: str = 'asc') -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...

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
        ...

    def start_inference_pipeline(self, pipeline_id: str, compute_alias: str = '', cluster_name: str = '') -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...

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
        ...

    def update_aggregator_status(self, pipeline_id: str, aggregator_id: str, status: str, is_running: bool) -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...

    def update_inference_pipeline_timing(self, timing_id: str, status: Optional[str] = None, end_time: Optional[str] = None, duration: Optional[float] = None, latency: Optional[int] = None, step_details: Optional[List[Dict[str, Any]]] = None) -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...


# From local_testing
class LocalTest:
    """
    A class to manage the execution of model-related scripts such as training, evaluation,
    deployment, and export based on configuration files.
    
    This class is designed to be part of a package, allowing users to create an instance
    and execute desired actions without modifying the package code.
    
    Example Usage:
        ```python
        from your_package_name import LocalTest
    
        # Define the path to the configuration directory
        config_directory = "/path/to/models_configs"
    
        # Create an instance of LocalTest
        local_test = LocalTest(config_directory)
    
        # Define the model info file and the actions to perform
        model_info = "model_A_info.json"
        actions_to_run = ["train", "eval", "export"]
    
        # Execute the specified actions for the selected model
        local_test.execute(
            model_info_path=os.path.join(config_directory, model_info),
            actions=actions_to_run
        )
    
        # To execute all actions for all models in the configuration directory:
        # local_test.execute_all()
    
        ```
    """

    def __init__(self, repo_configs_and_info_folder_path) -> None:
        """
        Initializes the LocalTest class with the path to the configuration files.
        
        Parameters:
            repo_configs_and_info_folder_path (str):
                Path to the directory containing model family, model info, and
                configuration JSON files.
        
        Example:
            ```python
            config_directory = "/path/to/models_configs"
            local_test = LocalTest(config_directory)
            ```
        """
        ...

    def execute(self, model_info_path, actions) -> Any:
        """
        Executes specified actions (train, eval, deploy, export) for a given model.
        
        The method locates the necessary configuration files within the repository
        configuration directory and runs the corresponding scripts.
        
        Parameters:
            model_info_path (str):
                Path to the JSON file containing model-specific information.
            actions (list of str):
                List of actions to perform. Valid actions are 'train', 'eval',
                'deploy', and 'export'.
        
        Example:
            ```python
            local_test.execute(
                model_info_path="/path/to/model_A_info.json",
                actions=["train", "eval", "export"]
            )
            ```
        
        Raises:
            ValueError: If an invalid action is specified.
            FileNotFoundError: If essential configuration files are missing.
        """
        ...

    def execute_all(self) -> Any:
        """
        Executes all standard actions (train, eval, deploy, export) for all models
        found in the configuration directory.
        
        This method automatically detects all model info files and executes all
        actions using the default configuration files.
        
        Example:
            ```python
            local_test.execute_all()
            ```
        
        Raises:
            FileNotFoundError: If essential configuration files are missing.
        """
        ...

    def run_script(self, python_script, family_info_path, model_info_path, config_path) -> Any:
        """
        Executes a specified Python script with the given model family and model info paths.
        
        Parameters:
            python_script (str):
                Name of the Python script to execute (e.g., "train.py", "eval.py",
                "deploy.py", "export.py").
            family_info_path (str):
                Path to the JSON file containing model family information.
            model_info_path (str):
                Path to the JSON file containing model-specific information.
            config_path (str):
                Path to the configuration file relevant to the script.
        
        Example:
            ```python
            local_test.run_script(
                python_script="train.py",
                family_info_path="/path/to/family_info.json",
                model_info_path="/path/to/model_A_info.json",
                config_path="/path/to/train-config.json"
            )
            ```
        
        Raises:
            subprocess.CalledProcessError: If the subprocess call fails.
        """
        ...


# From metrics_calculator_oop
class ClassificationMetrics:
    def __init__(self, split_type, outputs, targets, index_to_labels) -> None:
        ...

    def get_results(self) -> Any:
        """
        Get formatted evaluation results
        """
        ...


# From metrics_calculator_oop
class ObjectDetectionMetrics:
    def __init__(self, split, outputs, targets, index_to_labels) -> None:
        ...

    def get_results(self) -> Any:
        """
        Get formatted evaluation results
        """
        ...


# From model_store
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

    def __init__(self, session) -> None:
        """
        Initializes the BYOM class with a session object.
        
        Parameters:
        -----------
        session : Session
            A session object containing account information and RPC details.
        """
        ...

    def add_export_action_config(self, model_family_name, action_config) -> Any:
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
        ...

    def add_family_docker_file(self, model_family_name, docker_path) -> Any:
        ...

    def add_family_requirement_file(self, model_family_name, requirement_path) -> Any:
        ...

    def add_model_family(self, model_family_info) -> Any:
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
        ...

    def add_train_action_config(self, model_family_name, action_config) -> Any:
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
        ...

    def delete_model_action_config(self, model_family_name, model_key, action_type, action_config, export_format = None) -> Any:
        ...

    def delete_model_arch(self, model_family_name, model_key) -> Any:
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
        ...

    def delete_model_family(self, model_family_name) -> Any:
        """
        Delete a model family
        """
        ...

    def download_model_family_codebase(self, model_family_name, download_path) -> Any:
        ...

    def get_model_family(self, model_family_name) -> Any:
        ...

    def get_model_family_actions(self, model_family_name) -> Any:
        ...

    def get_model_family_benchmark_results(self, model_family_name) -> Any:
        ...

    def get_model_family_codebase_details(self, model_family_name) -> Any:
        ...

    def get_public_model_families_docker(self, project_type) -> Any:
        ...

    def get_started_test_cases(self, model_family_name, model_key = None) -> Any:
        ...

    def get_test_cases_by_type(self, model_family_name, test_cases_type = 'default') -> Any:
        ...

    def integrate_model_actions(self, model_family_name, model_key, model_actions) -> Any:
        """
        Integrate model actions for a specific model family and key.
        
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
        ...

    def publish_model_family(self, model_family_name) -> Any:
        ...

    def start_test_cases(self, model_family_name, model_key, project_type, test_cases) -> Any:
        """
        Start selected test cases for a specific model family and key.
        
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
        ...

    def update_model_family(self, model_family_name, model_family_info) -> Any:
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
        ...

    def update_model_family_benchmark_results(self, model_family_name) -> Any:
        ...

    def upload_model_family_codebase(self, model_family_name, code_zip_path, matrice_sdk_version, cuda_version) -> Any:
        ...

    def use_docker_image_from_public_model_family(self, model_family_name, docker_image_model_family_name, project_type) -> Any:
        ...

    def wait_for_codebase_upload(self, model_family_name, delay = 120) -> Any:
        ...


# From model_store
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

    def __init__(self, session, model_family_name = None, model_key = None, model_family_id = None, model_arch_id = None) -> None:
        ...

    def get_export_action_config(self, export_format) -> Any:
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
        ...

    def get_export_config(self, export_format) -> Any:
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
        ...

    def get_export_formats(self) -> Any:
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
        ...

    def get_train_action_config(self) -> Any:
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
        ...

    def get_train_config(self, tuning_type = 'default', model_checkpoint = 'auto') -> Any:
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
        ...


# From model_store
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

    def __init__(self, session, model_family_name = None, model_family_id = None) -> None:
        ...

    def get_model_arch(self, model_key) -> Any:
        ...

    def get_model_archs(self, model_name = None, model_key = None) -> Any:
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
        ...

    def get_model_family_details(self) -> Any:
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
        ...


# From models
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

    def __init__(self, session, model_id = None, model_name = '') -> None:
        """
        Initialize Model class.
        """
        ...

    def add_evaluation(self, dataset_id, dataset_version, split_types, is_pruned = False, is_gpu_required = False) -> Any:
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
        ...

    def delete(self) -> Any:
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
        ...

    def download_model(self, file_name) -> Any:
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
        ...

    def get_details(self) -> Any:
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
        ...

    def get_download_path(self) -> Any:
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
        ...

    def get_eval_result(self, dataset_id, dataset_version, split_type) -> Any:
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
        ...

    def get_model_training_logs(self) -> Any:
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
        ...

    def get_prediction(self, input_path) -> Any:
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
        ...

    def model_test(self, model_type = 'trained') -> Any:
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
        ...

    def plot_epochs_losses(self) -> Any:
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
        ...

    def plot_epochs_metrics(self) -> Any:
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
        ...

    def plot_eval_results(self) -> Any:
        """
        Plot the evaluation results for the model.
        
        Example
        -------
        >>> model.plot_eval_results()
        """
        ...

    def rename(self, name) -> Any:
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
        ...


# From pipeline
class Pipeline:
    def __init__(self, session, pipeline_id = None) -> None:
        ...

    def add_pipeline_stages_and_actions(self, stages_payload) -> Any:
        ...

    def construct_stage_payload(self, action_type = None, run = 1, pipeline_version = 'v1.0', pull_queue_id = None, push_queue_id = None, creation_type = 'manual', resource_constraints = None, process_input = 'single', process_output = 'single', input_service_id = None, action_params = None, trigger_ids = None, position = None, is_editable = True) -> Any:
        ...

    def create_pipeline(self, pipeline_name) -> Any:
        ...

    def get_actions_by_stage(self, stage_id) -> Any:
        ...

    def get_pipeline(self) -> Any:
        ...

    def get_stages(self, pipeline_version = 'v1.0', run = 1) -> Any:
        ...

    def get_stages_and_actions(self, pipeline_version = 'v1.0', run = 1) -> Any:
        ...

    def run_pipeline(self, pipeline_version = 'v1.0', run = 1) -> Any:
        ...


# From projects
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

    def __init__(self, session, project_name = None, project_id = None) -> None:
        """
        Initialize a Projects object with project details.
        
        Parameters
        ----------
        session : Session
            The session object used for API interactions.
        project_name : str
            The name of the project.
        """
        ...

    def add_models_for_training(self, model_train_configs, primary_metric, dataset_id = None, dataset_name = None, dataset_version = 'v1.0', target_runtime = ['PyTorch'], compute_alias = '') -> Any:
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
        ...

    def change_status(self, enable = True) -> Any:
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
        ...

    def create_annotation(self, project_type, ann_title, dataset_id, dataset_version, labels, only_unlabeled, is_ML_assisted, labellers, reviewers, guidelines) -> Any:
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
        ...

    def create_fastapi_deployment(self, deployment_name, model_id, gpu_required = True, auto_scale = True, auto_shutdown = True, shutdown_threshold = 5, compute_alias = '', model_type = 'trained', runtime_framework = 'Pytorch', is_kafka_enabled = False, is_optimized = False, post_processing_config = None) -> Any:
        ...

    def create_inference_pipeline(self, name: Optional[str] = None, description: Optional[str] = None, applications: Optional[List[Dict]] = None) -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...

    def create_inference_project(session, project_name: str, industries: Optional[List[str]] = None, country: str = 'United States', tags: Optional[List[str]] = None, licence: str = '', compute_type: str = 'matrice', storage_type: str = 'matrice', supported_devices: str = 'nvidia_gpu', deployment_supported_device: str = 'nvidia_gpu') -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a new inference (Deploy) project via the accounting API.
        
        This corresponds to the **Create Project** modal in the Matrice UI
        (Project Type = *Deploy*).  The ``projectType`` is fixed to
        ``"deploy_app"``; all other UI fields are exposed as parameters.
        
        **Input validation applied before the API call:**
        
        * ``industries`` — each entry is checked against the platform's known
          list (``General``, ``Retail``, ``Agriculture``, ``Automotive``,
          ``Healthcare``, ``Manufacturing``, ``Security``, ``Oil and Gas``,
          ``Transportation``, ``Energy``). Any value that is **not** in this
          list is silently normalised to ``"others"``.  Duplicate values that
          arise after normalisation are deduplicated while preserving order.
          Example: ``["Retail", "Agriculture", "enterprise"]`` →
          ``["Retail", "Agriculture", "others"]``.
        * ``country`` — must be a non-empty string.
        * ``licence`` — must be a non-empty string.
        * ``tags`` — accepts a list of any values; each element is coerced to
          ``str`` so callers can pass numbers or other objects safely.
        
        Parameters
        ----------
        session : Session
            An authenticated Matrice session object.
        project_name : str
            Unique display name for the project  *(UI: "Project Name")*.
        industries : list of str, optional
            Industry tags for the project.  Values outside the known list are
            replaced with ``"others"``  *(UI: "Industries")*.
            Defaults to an empty list.
        country : str, optional
            Country associated with the project — must be a non-empty string
            *(UI: "Country")*. Defaults to ``"United States"``.
        tags : list, optional
            Arbitrary tags; each element is coerced to ``str``
            *(UI: "Tags")*. Defaults to an empty list.
        licence : str
            Licence identifier (e.g. ``"MIT"``).  Must not be empty
            *(UI: "Licence")*.
        compute_type : str, optional
            Backend compute provider. Defaults to ``"matrice"``.
        storage_type : str, optional
            Backend storage provider. Defaults to ``"matrice"``.
        supported_devices : str, optional
            Hardware device class for the project. Defaults to
            ``"nvidia_gpu"``.
        deployment_supported_device : str, optional
            Hardware device class used when creating deployments. Defaults
            to ``"nvidia_gpu"``.
        
        Returns
        -------
        tuple
            A 3-tuple ``(data, error, message)`` where:
        
            * **data** (*dict | None*) — The created project document
              returned by the API (contains ``_id``, ``name``, etc.).
            * **error** (*str | None*) — Error description on failure,
              ``None`` on success.
            * **message** (*str*) — Human-readable status message.
        
        Raises
        ------
        ValueError
            If ``country`` is not a non-empty string, or if ``licence`` is
            empty.
        
        Example
        -------
        >>> from matrice_common.session import Session
        >>> from matrice.projects import Projects
        >>>
        >>> session = Session(access_key=..., secret_key=..., account_number=...)
        >>> data, error, message = Projects.create_inference_project(
        ...     session,
        ...     project_name="My-Inference-Project-01",
        ...     industries=["Retail", "Agriculture", "enterprise"],  # → "others"
        ...     country="United States",
        ...     tags=["v1", "test"],
        ...     licence="MIT",
        ... )
        >>> if error:
        ...     print(f"Error: {error}")
        ... else:
        ...     project_id = data["_id"]
        ...     print(f"Created project id={project_id}")
        """
        ...

    def create_model_export(self, model_train_id, export_formats, model_config, is_gpu_required = False) -> Any:
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
        ...

    def create_triton_deployment(self, deployment_name, model_id, gpu_required = True, auto_scale = True, auto_shutdown = True, shutdown_threshold = 5, compute_alias = '', model_type = 'trained', runtime_framework = 'Pytorch', connection_protocol = 'rest', max_batch_size = 8, num_model_instances = 1, input_data_type = 'TYPE_FP32', output_data_type = 'TYPE_FP32', dynamic_batching = False, preferred_batch_size = [2, 4, 8], max_queue_delay_microseconds = 100, input_pinned_memory = True, output_pinned_memory = True, is_kafka_enabled = False, is_optimized = False, post_processing_config = None) -> Any:
        ...

    def delete(self) -> Any:
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
        ...

    def get_actions_logs(self, action_id) -> Any:
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
        ...

    def get_annotation(self, dataset_id = None, annotation_id = None, annotation_name = '') -> Any:
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
        ...

    def get_annotations_status_summary(self) -> Any:
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
        ...

    def get_dataset(self, dataset_id = None, dataset_name = '') -> Any:
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
        ...

    def get_dataset_status_summary(self) -> Any:
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
        ...

    def get_deployment(self, deployment_id = None, deployment_name = '') -> Any:
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
        ...

    def get_deployment_status_summary(self) -> Any:
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
        ...

    def get_exported_model(self, model_export_id = None, model_export_name = '') -> Any:
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
        ...

    def get_exported_models(self) -> Any:
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
        ...

    def get_latest_action_record(self, service_id) -> Any:
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
        ...

    def get_model(self, model_id = None, model_name = '') -> Any:
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
        ...

    def get_model_export_status_summary(self) -> Any:
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
        ...

    def get_model_status_summary(self) -> Any:
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
        ...

    def get_service_action_logs(self, service_id, service_name) -> Any:
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
        ...

    def get_trained_models(self) -> Any:
        ...

    def import_cloud_dataset(self, dataset_name, source_url, cloud_provider, dataset_type, input_type = 'image', bucket_alias = '', compute_alias = '', source_credential_alias = '', bucket_alias_service_provider = 'auto', target_cloud_storage = 'AWS') -> Any:
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
        ...

    def import_local_dataset(self, dataset_name, file_path, dataset_type, input_type = 'image', bucket_alias = '', compute_alias = '', source_credential_alias = '', bucket_alias_service_provider = 'auto', target_cloud_storage = 'AWS') -> Any:
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
        ...

    def invite_user_to_project(self, email, permissions) -> Any:
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
        ...

    def list_annotations(self, page_size = 10, page_number = 0) -> Any:
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
        ...

    def list_collaborators(self) -> Any:
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
        ...

    def list_datasets(self, status = 'total', page_size = 10, page_number = 0) -> Any:
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
        ...

    def list_deployments(self, page_size = 10, page_number = 0) -> Any:
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
        ...

    def list_drift_monitorings(self, page_size = 10, page_number = 0) -> Any:
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
        ...

    def list_exported_models(self, page_size = 10, page_number = 0) -> Any:
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
        ...

    def list_inference_pipelines(self, page: int = 1, limit: int = 10, status: Optional[str] = None, search: Optional[str] = None) -> Tuple[Optional[Dict], Optional[str], str]:
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
        ...

    def list_trained_models(self, page_size = 10, page_number = 0) -> Any:
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
        ...

    def stop_training(self) -> Any:
        ...

    def update_permissions(self, collaborator_id, permissions) -> Any:
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
        ...


# From streaming_automation
class CameraInfo(TypedDict):
    pass

# From streaming_automation
class StreamingAutomation:
    """
    Class to automate the creation and management of streaming gateways,
    cameras, locations, camera groups, and inference pipelines.
    """

    def __init__(self, account_number: str, access_key: Optional[str] = None, secret_key: Optional[str] = None, project_id: Optional[str] = None, project_name: Optional[str] = None) -> None:
        """
        Initialize the automation class with session credentials.
        
        Parameters
        ----------
        account_number : str
            The account number for the Matrice account
        access_key : str, optional
            Access key for authentication (or set MATRICE_ACCESS_KEY_ID env var)
        secret_key : str, optional
            Secret key for authentication (or set MATRICE_SECRET_ACCESS_KEY env var)
        project_id : str, optional
            Project ID to use
        project_name : str, optional
            Project name to use (will fetch project_id if provided)
        """
        ...

    def add_cameras_and_applications_to_pipeline(self, pipeline_id: str, cameras: List[Dict[str, Any]], compute_alias: str = '') -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
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
        
        Returns
        -------
        tuple
            (result_dict, error) - Result dict if successful, error message if failed
        
        Examples
        --------
        >>> cameras = [
        ...     {
        ...         "cameraId": "507f1f77bcf86cd799439017",  # pragma: allowlist secret
        ...         "applications": [{"_idApplication": "507f1f77bcf86cd799439023"}]  # pragma: allowlist secret
        ...     }
        ... ]
        >>> result, error = automation.add_cameras_and_applications_to_pipeline(
        ...     pipeline_id="507f1f77bcf86cd799439022",
        ...     cameras=cameras,
        ...     compute_alias="inference-compute-01"
        ... )
        """
        ...

    def auto_setup_from_cameras(self, cameras: Union[str, Dict, List[Dict]], compute_alias: str, cluster_name: str, lan_id: str = '', project_id: Optional[str] = None, application_names: Optional[List[str]] = None, auto_start: bool = False, facial_recognition_server_id: Optional[str] = None, lpr_server_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Fully automated setup from camera data. Only requires minimal inputs.
        
        When cameras are assigned a clusterName, the backend automatically
        resolves the streaming gateway. Locations are replaced by LANs (lanId).
        
        This method automatically:
        - Parses cameras from various formats (JSON string, dict, list of dicts, file path)
        - Creates cameras with lanId and clusterName
        - Creates inference pipeline (if applications provided)
        - Starts inference pipeline
        
        Parameters
        ----------
        cameras : str, dict, or list of dicts
            Camera data in any format:
            - JSON string: '{"cameraName": "cam1", "protocolType": "RTSP", ...}'
            - File path: Path to JSON file containing cameras
            - Single dict: {"cameraName": "cam1", ...}
            - List of dicts: [{"cameraName": "cam1", ...}, ...]
        compute_alias : str
            Compute alias for the inference pipeline
        cluster_name : str
            Cluster name for backend gateway resolution
        lan_id : str
            LAN ID (replaces location)
        project_id : str, optional
            Project ID (uses session project_id if not provided)
        application_names : list of str, optional
            List of application names to add to pipeline (e.g., ["People Counting", "Color Detection"])
            If not provided, pipeline will be created without applications
        auto_start : bool
            Whether to automatically start pipeline (default: False)
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications like "Face Recognition")
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications like "License Plate Recognition")
        
        Returns
        -------
        dict : Results dictionary with all created IDs, tags, and any errors
            {
                "camera_ids": [...],
                "pipeline_id": "...",
                "pipeline_name": "...",
                "tag": "...",  # Auto-generated tag for this setup
                "errors": []
            }
        """
        ...

    def create_cameras(self, cameras: List[Dict[str, Any]]) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Create cameras (supports both RTSP and FILE protocol types).
        Checks for existing cameras before creating to avoid duplicate errors.
        
        Parameters
        ----------
        cameras : list of dict
            List of camera configurations. Each dict should contain:
            - accountNumber: str
            # - cameraGroupId: str  # Camera group removed from flow
            - streamingGatewayId: str
            - locationId: str
            - cameraName: str (optional, auto-generated if not provided)
            - protocolType: str ("RTSP" or "FILE")
            - cameraFeedPath: str (for RTSP)
            - simulationVideoPath: str (for FILE)
            - defaultStreamSettings: dict (optional)
        
        Returns
        -------
        tuple : (list of created/existing cameras, error_message)
        """
        ...

    def create_complete_setup(self, cameras: List[Dict[str, Any]], project_id: str, application_names: List[str], cluster_name: str, compute_alias: str = '', lan_id: str = '', start_pipeline: bool = True, facial_recognition_server_id: Optional[str] = None, lpr_server_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete workflow to create cameras and pipeline.
        When cameras are assigned a clusterName, the backend automatically
        resolves the streaming gateway. Locations are replaced by LANs (lanId).
        
        Parameters
        ----------
        cameras : list of dict
            List of camera configurations. Each camera dict should contain:
            - cameraName: str (optional, auto-generated if not provided)
            - protocolType: str ("RTSP" or "FILE")
            - cameraFeedPath: str (for RTSP) or simulationVideoPath: str (for FILE)
            - Other required fields will be added automatically
        project_id : str
            Project ID
        application_names : list of str
            List of application names to use
        cluster_name : str
            Cluster name for backend gateway resolution
        compute_alias : str
            Compute alias for pipeline
        lan_id : str
            LAN ID (replaces location)
        start_pipeline : bool
            Whether to start the pipeline (default: True)
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications)
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications)
        
        Returns
        -------
        dict : Results dictionary with all created IDs and any errors
        """
        ...

    def create_inference_pipeline(self, name: str, project_id: str, cameras: List[Dict[str, Any]], user_id: str = '', description: str = '', access_scale: str = 'local', deploy_type: str = 'account', server_type: str = 'fastapi', facial_recognition_server_id: Optional[str] = None, lpr_server_id: Optional[str] = None, cluster_name: str = '', runtime_framework: str = 'Triton') -> Tuple[Optional[str], Optional[str]]:
        """
        Create an inference pipeline using the new format with cameras array.
        
        Parameters
        ----------
        name : str
            Name of the pipeline
        project_id : str
            Project ID
        cameras : list of dict
            List of camera configurations. Each dict should contain:
            - cameraId: str (ID of the camera)
            - applications: list of dict with "_idApplication" key
        user_id : str
            User ID (required by backend)
        description : str
            Description of the pipeline
        access_scale : str
            Access scale (default: "local")
        deploy_type : str
            Deploy type (default: "real_time")
        server_type : str
            Server type (default: "fastapi", can be empty string "")
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications)
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications)
        cluster_name : str, optional
            Cluster name for deployment (e.g., "thor2")
        runtime_framework : str, optional
            Runtime framework (default: "Triton")
        
        Returns
        -------
        tuple : (pipeline_id, error_message)
        """
        ...

    def create_streaming_gateway(self, gateway_name: str, description: str = '', compute_alias: str = '', account_type: str = 'enterprise', server_type: str = 'redis', video: str = 'H.264', network_settings: Optional[Dict[str, Any]] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        Create a streaming gateway.
        
        Parameters
        ----------
        gateway_name : str
            Name of the gateway
        description : str
            Description of the gateway
        compute_alias : str
            Compute alias for the gateway
        account_type : str
            Account type (default: "enterprise")
        server_type : str
            Server type - "redis", "cloud", etc. (default: "redis")
        video : str
            Video codec (default: "H.264")
        network_settings : dict, optional
            Network settings dict with IPAddress, accessScale, port, region, etc.
        
        Returns
        -------
        tuple : (gateway_id, error_message)
            Returns gateway_id if successful, None and error message if failed
        """
        ...

    def export_cameras_to_json(self, output_file: str, camera_group_id: Optional[str] = None, include_details: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Export cameras to JSON format (single JSON array).
        
        Parameters
        ----------
        output_file : str
            Path to output JSON file
        camera_group_id : str, optional
            Filter cameras by camera group ID
        include_details : bool
            Deprecated parameter (kept for backward compatibility)
        
        Returns
        -------
        tuple : (success, error_message)
        """
        ...

    def export_cameras_to_jsonl(self, output_file: str, camera_group_id: Optional[str] = None, include_details: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Export cameras to JSONL (JSON Lines) format.
        
        Parameters
        ----------
        output_file : str
            Path to output JSONL file
        camera_group_id : str, optional
            Filter cameras by camera group ID
        include_details : bool
            Deprecated parameter (kept for backward compatibility)
        
        Returns
        -------
        tuple : (success, error_message)
        """
        ...

    def find_application_by_name(self, application_name: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Find an application by name.
        
        Parameters
        ----------
        application_name : str
            Name of the application to find
        
        Returns
        -------
        tuple : (application_dict, error_message)
        """
        ...

    def get_applications(self, page_size: int = 200, page_number: int = 0, sort_by: str = '', sort_order: str = 'asc') -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Get available applications.
        
        Returns
        -------
        tuple : (list of applications, error_message)
        """
        ...

    def get_camera_json(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get camera details as JSON.
        
        Note: This method is deprecated as the API endpoint doesn't exist.
        Use get_cameras() instead to retrieve camera information.
        
        Parameters
        ----------
        camera_id : str
            ID of the camera
        
        Returns
        -------
        tuple : (camera_dict, error_message)
        """
        ...

    def get_cameras(self, camera_group_id: Optional[str] = None, page: int = 1, limit: int = 10, search: Optional[str] = None) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Get cameras. Camera group filtering removed from flow.
        
        Parameters
        ----------
        camera_group_id : str, optional
            DEPRECATED - Filter cameras by camera group ID (no longer used)
        page : int
            Page number for pagination (default: 1)
        limit : int
            Items per page (default: 10)
        search : str, optional
            Search term to filter cameras
        
        Returns
        -------
        tuple : (list of cameras, error_message)
        """
        ...

    def get_facial_recognition_servers(self, project_id: str, page: int = 1, page_size: int = 10) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Get facial recognition servers for a project.
        
        Parameters
        ----------
        project_id : str
            Project ID
        page : int
            Page number (default: 1)
        page_size : int
            Page size (default: 10)
        
        Returns
        -------
        tuple : (list of FR servers, error_message)
        """
        ...

    def get_lpr_servers(self, project_id: str, page: int = 1, page_size: int = 10) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Get LPR (License Plate Recognition) servers for a project.
        
        Parameters
        ----------
        project_id : str
            Project ID
        page : int
            Page number (default: 1)
        page_size : int
            Page size (default: 10)
        
        Returns
        -------
        tuple : (list of LPR servers, error_message)
        """
        ...

    def get_presigned_url(self, file_name: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get a presigned URL for video upload.
        
        Parameters
        ----------
        file_name : str
            Name of the file to upload
        
        Returns
        -------
        tuple : (presigned_url, error_message)
        """
        ...

    def list_inference_pipelines(self, project_id: str, page_size: int = 10, page_number: int = 0, sort_by: str = '', sort_order: str = 'asc') -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List inference pipelines for a project.
        
        Returns
        -------
        tuple : (list of pipelines, error_message)
        """
        ...

    def list_streaming_gateways(self, page_size: int = 20, page: int = 0) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List all streaming gateways for the account.
        
        Returns
        -------
        tuple : (list of gateways, error_message)
        """
        ...

    def quick_setup(self, cameras: Union[str, List[Dict[str, Any]]], cluster_name: str, compute_alias: Optional[str] = None, lan_id: str = '', apps: Optional[Union[str, List[str]]] = None, project_id: Optional[str] = None, auto_start: bool = False, facial_recognition_server_id: Optional[str] = None, lpr_server_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Quick setup wrapper around auto_setup_from_cameras.
        Parses application names and delegates to auto_setup_from_cameras.
        """
        ...

    def setup_from_paths(self, paths: Union[str, List[str]], cluster_name: str, compute_alias: Optional[str] = None, lan_id: str = '', apps: Optional[Union[str, List[str]]] = None, project_id: Optional[str] = None, auto_start: bool = False) -> Dict[str, Any]:
        """
        Ultra-simple setup - just provide camera paths as strings.
        Everything else is auto-generated with UUID-based names.
        
        When cameras are assigned a clusterName, the backend automatically
        resolves the streaming gateway. Locations are replaced by LANs (lanId).
        
        Parameters
        ----------
        paths : str or list of str
            Camera paths/URLs:
            - Single path: "rtsp://192.168.1.100:554/stream1"
            - Multiple paths: ["rtsp://...", "/path/to/video.mp4", "https://..."]
        cluster_name : str
            Cluster name for backend gateway resolution
        compute_alias : str, optional
            Compute alias (auto-generated if not provided)
        lan_id : str
            LAN ID (replaces location)
        apps : str or list of str, optional
            Application names (optional)
        project_id : str, optional
            Project ID (uses session project_id if not provided)
        auto_start : bool
            Whether to auto-start pipeline (default: False)
        
        Returns
        -------
        dict : Results with all created IDs and any errors
        
        Examples
        --------
        ```python
        # Single path
        results = automation.setup_from_paths(
            "rtsp://192.168.1.100:554/stream1",
            cluster_name="thor2",
        )
        
        # Multiple paths
        results = automation.setup_from_paths(
            [
                "rtsp://192.168.1.100:554/stream1",
                "rtsp://192.168.1.101:554/stream1",
                "/path/to/video.mp4"
            ],
            cluster_name="thor2",
        )
        
        # With apps
        results = automation.setup_from_paths(
            ["rtsp://...", "/path/to/video.mp4"],
            cluster_name="thor2",
            apps="People Counting",
        )
        ```
        """
        ...

    def start_inference_pipeline(self, pipeline_id: str, compute_alias: str, cluster_name: str = '') -> Tuple[bool, Optional[str]]:
        """
        Start an inference pipeline with compute alias.
        
        Parameters
        ----------
        pipeline_id : str
            ID of the pipeline to start
        compute_alias : str
            Compute alias to use for the pipeline
        cluster_name : str, optional
            Cluster name for deployment
        
        Returns
        -------
        tuple : (success, error_message)
        """
        ...

    def start_streaming_gateway(self, gateway_id: str) -> Tuple[bool, Optional[str]]:
        """
        Start a streaming gateway.
        
        Parameters
        ----------
        gateway_id : str
            ID of the gateway to start
        
        Returns
        -------
        tuple : (success, error_message)
        """
        ...

    def upload_video(self, video_path: str, file_name: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        Upload a video file to S3 using presigned URL.
        Caches the S3 URL for the same file path to avoid re-uploading.
        
        Parameters
        ----------
        video_path : str
            Path to the video file
        file_name : str, optional
            Name for the uploaded file (defaults to original filename)
        
        Returns
        -------
        tuple : (s3_url, error_message)
        """
        ...


# From streaming_benchmarking
class StreamingBenchmarking:
    """
    Automated load testing for streaming infrastructure.
    
    Incrementally adds cameras to a pipeline and collects performance metrics
    from streaming gateway and inference pipeline.
    
    Attributes
    ----------
    video_path : str
        Path to video file for camera simulation
    compute_alias : str
        Compute resource identifier
    app_name : str
        Application name for inference
    min_cameras : int
        Minimum cameras to start with
    max_cameras : int
        Maximum cameras to add
    interval_minutes : float
        Minutes between adding cameras
    step_size : int
        Number of cameras to add at each interval
    metrics_interval_minutes : float
        Minutes between collecting metrics
    output_file : str
        Path to JSON output file
    
    Examples
    --------
    >>> benchmark = StreamingBenchmarking(
    ...     video_path="/path/to/video.mp4",
    ...     compute_alias="benchmark-device",
    ...     app_name="People Counting",
    ...     account_number="ACC123",
    ...     access_key="key",
    ...     secret_key="secret",  # pragma: allowlist secret
    ...     project_id="proj_id",
    ...     min_cameras=1,
    ...     max_cameras=20,
    ...     interval_minutes=5.0,
    ...     step_size=2,
    ...     metrics_interval_minutes=0.5,
    ...     camera_batch_size=10,
    ...     pipeline_batch_size=10,
    ...     auto_start=True
    ... )
    >>> benchmark.initialize_setup()
    >>> benchmark.start_benchmark(duration_minutes=30)
    >>> benchmark.stop_benchmark()
    >>> benchmark.export_results()
    """

    def __init__(self, video_path: str, compute_alias: str, app_name: str, account_number: str, access_key: Optional[str] = None, secret_key: Optional[str] = None, project_id: Optional[str] = None, project_name: Optional[str] = None, min_cameras: int = 1, max_cameras: int = 20, interval_minutes: float = 5.0, step_size: int = 1, metrics_interval_minutes: float = 0.5, output_file: str = 'benchmark_results.json', fps: int = 10, width: int = 640, height: int = 480, video_quality: int = 80, aspect_ratio: str = '16:9', state_file: Optional[str] = None, auto_resume: bool = True, camera_batch_size: int = 10, pipeline_batch_size: int = 10, auto_start: bool = True, facial_recognition_server_id: Optional[str] = None, lpr_server_id: Optional[str] = None, cluster_name: Optional[str] = None, lan_id: str = '', runtime_framework: str = 'Triton') -> None:
        """
        Initialize streaming benchmarking.
        
        Parameters
        ----------
        video_path : str
            Path to video file for camera simulation
        compute_alias : str
            Compute resource identifier
        app_name : str
            Application name for inference
        account_number : str
            Matrice account number
        access_key : str, optional
            API access key
        secret_key : str, optional
            API secret key
        project_id : str, optional
            Project ID
        project_name : str, optional
            Project name
        min_cameras : int, optional
            Minimum cameras to start with (default: 1)
        max_cameras : int, optional
            Maximum cameras to add (default: 20)
        interval_minutes : float, optional
            Minutes between adding cameras (default: 5.0)
        step_size : int, optional
            Number of cameras to add at each interval (default: 1)
        metrics_interval_minutes : float, optional
            Minutes between collecting metrics (default: 0.5)
        output_file : str, optional
            JSON output file path (default: "benchmark_results.json")
        fps : int, optional
            Frames per second for camera streams (default: 10)
        width : int, optional
            Video width in pixels (default: 640)
        height : int, optional
            Video height in pixels (default: 480)
        video_quality : int, optional
            Video quality 0-100 (default: 80)
        aspect_ratio : str, optional
            Video aspect ratio (default: "16:9")
        state_file : str, optional
            Path to state file for crash recovery. If None, uses output_file.
        auto_resume : bool, optional
            Automatically resume from state file if it exists (default: True)
        camera_batch_size : int, optional
            Number of cameras to create in each batch (default: 10)
        pipeline_batch_size : int, optional
            Number of cameras to add to pipeline in each batch (default: 10)
        auto_start : bool, optional
            Automatically start streaming gateway and inference pipeline after creation (default: True)
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications like "Face Recognition")
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications like "License Plate Recognition")
        cluster_name : str, optional
            Cluster name for deployment (e.g., "thor2"). If None, uses compute_alias.
        runtime_framework : str, optional
            Runtime framework (default: "Triton")
        """
        ...

    def add_camera(self) -> Optional[str]:
        """
        Add one more camera to the existing pipeline.
        
        Creates a new camera with the same video and adds it to the pipeline
        with the same application using the proper API.
        
        Returns
        -------
        str or None
            Camera ID if successful, None if failed
        
        Raises
        ------
        Exception
            If pipeline not initialized or camera creation fails
        """
        ...

    def add_cameras(self) -> List[str]:
        """
        Add multiple cameras to the existing pipeline based on step_size.
        
        Creates new cameras with the same video and adds them to the pipeline
        with the same application using the proper API.
        
        Returns
        -------
        list of str
            List of camera IDs successfully added. Empty list if failed or max reached.
        
        Raises
        ------
        Exception
            If pipeline not initialized
        """
        ...

    def collect_metrics(self) -> Dict[str, Any]:
        """
        Collect current metrics from gateway and pipeline.
        
        Returns
        -------
        dict
            Current metrics snapshot
        """
        ...

    def export_results(self, file_path: Optional[str] = None) -> str:
        """
        Export benchmark results to JSON file with summary.
        
        Reads the existing log file and adds a summary section.
        
        Parameters
        ----------
        file_path : str, optional
            Output file path. Uses default output_file if not specified.
        
        Returns
        -------
        str
            Path to exported file
        """
        ...

    def get_camera_input_topic(self, camera_id: str) -> Dict[str, Any]:
        """
        Get input topic for a camera.
        
        Parameters
        ----------
        camera_id : str
            Camera ID
        
        Returns
        -------
        dict
            Camera input topic information
        """
        ...

    def get_camera_output_topics(self, camera_id: str) -> List[Dict[str, Any]]:
        """
        Get output topics for a camera.
        
        Parameters
        ----------
        camera_id : str
            Camera ID
        
        Returns
        -------
        list
            List of camera output topics. Returns empty list on error.
        """
        ...

    def get_topics_by_streaming_gateway(self, streaming_id: str, server_id: str) -> Dict[str, Any]:
        """
        Get topics by streaming gateway and server ID.
        
        Parameters
        ----------
        streaming_id : str
            Streaming gateway ID
        server_id : str
            Server ID
        
        Returns
        -------
        dict
            Topics information
        """
        ...

    def initialize_setup(self) -> Dict[str, Any]:
        """
        Initialize the streaming infrastructure with one camera.
        
        Creates initial cameras and pipeline. Cameras are assigned to a LAN
        and cluster; the backend auto-assigns the streaming gateway.
        
        Returns
        -------
        dict
            Setup results with all created resource IDs
        
        Raises
        ------
        Exception
            If setup fails at any step
        """
        ...

    def load_state(self) -> bool:
        """
        Load benchmark state from file.
        
        Returns
        -------
        bool
            True if state was loaded successfully, False otherwise
        
        Raises
        ------
        Exception
            If state file is invalid or corrupted
        """
        ...

    def resume_from_state(self) -> Dict[str, Any]:
        """
        Resume benchmark from saved state.
        
        Validates that all required resources (gateway, pipeline, etc.) still exist
        and are accessible before resuming.
        
        Returns
        -------
        dict
            Resume status with information about what was restored
        
        Raises
        ------
        Exception
            If state cannot be loaded or resources are invalid
        """
        ...

    def save_state(self) -> bool:
        """
        Save current benchmark state to file for crash recovery.
        
        Returns
        -------
        bool
            True if state was saved successfully, False otherwise
        """
        ...

    def start_benchmark(self, duration_minutes: Optional[float] = None, resume: Optional[bool] = None) -> Any:
        """
        Start the benchmarking process.
        
        Begins adding cameras at specified intervals and collecting metrics.
        Runs in a background thread.
        
        Parameters
        ----------
        duration_minutes : float, optional
            Maximum duration to run. If None, runs until stop_benchmark() is called.
        resume : bool, optional
            Force resume from state if True, force new start if False.
            If None, uses auto_resume setting from __init__.
        
        Raises
        ------
        Exception
            If benchmark already running or setup not initialized
        """
        ...

    def stop_benchmark(self) -> Any:
        """
        Stop the benchmarking process gracefully.
        
        Signals the benchmark thread to stop and waits for completion.
        """
        ...


# From streaming_gateway_management
class StreamingGatewayManagement:
    """
    A class for handling streaming gateway management operations using the backend API.
    
    This includes gateway creation, control, monitoring, and heartbeat management.
    
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
    >>> gateway_mgmt = StreamingGatewayManagement(session)
    >>>
    >>> # Create a streaming gateway
    >>> gateway, error, message = gateway_mgmt.create_streaming_gateway(
    ...     gateway_name="Main Gateway",
    ...     description="Primary streaming gateway",
    ...     compute_alias="redis-compute-01"
    ... )
    """

    def __init__(self, session) -> None:
        """
        Initialize the StreamingGatewayManagement class.
        
        Parameters
        ----------
        session : Session
            The session object with authentication credentials
        """
        ...

    def add_streaming_gateway_heartbeat(self, gateway_id: str, timestamp: str, status: str, metrics: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Add a heartbeat record for a streaming gateway.
        
        Parameters
        ----------
        gateway_id : str
            The gateway ID
        timestamp : str
            Timestamp in ISO format (e.g., "2025-11-12T10:30:00Z")
        status : str
            Current status of the gateway
        metrics : dict, optional
            Metrics data including cpuUsage, memoryUsage, bandwidthUsage, etc.
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Heartbeat record details
            - str or None: Error message if failed
            - str: Status message
        
        Examples
        --------
        >>> metrics = {
        ...     "cpuUsage": 45.2,
        ...     "memoryUsage": 60.5,
        ...     "bandwidthUsage": 250.0
        ... }
        >>> heartbeat, error, message = gateway_mgmt.add_streaming_gateway_heartbeat(
        ...     gateway_id="507f1f77bcf86cd799439012",
        ...     timestamp="2025-11-12T10:30:00Z",
        ...     status="running",
        ...     metrics=metrics
        ... )
        """
        ...

    def create_streaming_gateway(self, gateway_name: str, description: str = '', account_type: str = 'enterprise', status: str = 'created', server_type: str = 'redis', network_settings: Optional[Dict[str, Any]] = None, compute_alias: str = '', cluster_name: str = '', video: str = 'H.264', user_id: str = '') -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a new streaming gateway.
        
        Parameters
        ----------
        gateway_name : str
            Name of the gateway
        description : str, optional
            Description of the gateway
        account_type : str, optional
            Account type - "enterprise" or other (default: "enterprise")
        status : str, optional
            Initial status (default: "created")
        server_type : str, optional
            Server type - "redis", "cloud", etc. (default: "redis")
        network_settings : dict, optional
            Network configuration with IPAddress, port, accessScale, region,
            maxBandwidthMbps, currentBandwidthMbps
        compute_alias : str, optional
            Compute resource alias
        cluster_name : str, optional
            Name of the cluster
        video : str, optional
            Video codec - "H.264", "H.265", "Frame" (default: "H.264")
        user_id : str, optional
            User ID creating the gateway
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Gateway details including ID, status, network settings
            - str or None: Error message if failed
            - str: Status message
        
        Examples
        --------
        >>> network_settings = {
        ...     "IPAddress": "10.0.1.100",
        ...     "port": 8080,
        ...     "accessScale": "regional",
        ...     "region": "us-west-2",
        ...     "maxBandwidthMbps": 1000.0,
        ...     "currentBandwidthMbps": 0.0
        ... }
        >>> gateway, error, message = gateway_mgmt.create_streaming_gateway(
        ...     gateway_name="Campus Gateway",
        ...     description="Main campus streaming gateway",
        ...     network_settings=network_settings,
        ...     compute_alias="redis-compute-01"
        ... )
        """
        ...

    def delete_streaming_gateway(self, gateway_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a streaming gateway.
        
        Parameters
        ----------
        gateway_id : str
            The gateway ID to delete
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Deletion confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_streaming_gateway_by_id(self, gateway_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get a specific streaming gateway by ID.
        
        Parameters
        ----------
        gateway_id : str
            The gateway ID
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Gateway details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_streaming_gateway_dashboard(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get streaming gateway dashboard with pagination.
        
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
            - dict: Dashboard data with gateways and statistics
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def get_streaming_gateways_by_account(self) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all streaming gateways for the account.
        
        Returns
        -------
        tuple
            A tuple containing:
            - list: List of streaming gateways
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def list_streaming_gateways(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        List all streaming gateways with pagination.
        
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
            - dict: Paginated gateways data with 'items', 'total', 'page', 'limit'
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def start_streaming_gateway(self, gateway_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Start a streaming gateway.
        
        Parameters
        ----------
        gateway_id : str
            The gateway ID to start
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated gateway with status "starting" or "running"
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def stop_streaming_gateway(self, gateway_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Stop a streaming gateway.
        
        Parameters
        ----------
        gateway_id : str
            The gateway ID to stop
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated gateway with status "stopped"
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def update_streaming_gateway(self, gateway_id: str, gateway_name: Optional[str] = None, description: Optional[str] = None, account_type: Optional[str] = None, server_type: Optional[str] = None, network_settings: Optional[Dict[str, Any]] = None, compute_alias: Optional[str] = None, cluster_name: Optional[str] = None, video: Optional[str] = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update a streaming gateway.
        
        Parameters
        ----------
        gateway_id : str
            The gateway ID to update
        gateway_name : str, optional
            New gateway name
        description : str, optional
            New description
        account_type : str, optional
            New account type
        server_type : str, optional
            New server type
        network_settings : dict, optional
            New network settings
        compute_alias : str, optional
            New compute alias
        cluster_name : str, optional
            New cluster name
        video : str, optional
            New video codec
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated gateway details
            - str or None: Error message if failed
            - str: Status message
        """
        ...

    def update_streaming_gateway_status(self, gateway_id: str, status: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update the status of a streaming gateway.
        
        Parameters
        ----------
        gateway_id : str
            The gateway ID
        status : str
            New status - "starting", "running", "stopped", "failed", "created"
        
        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated gateway details
            - str or None: Error message if failed
            - str: Status message
        """
        ...


# From testing
class ModelDownloadMock:
    """
    Mock class for downloading models in the testing pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the ModelDownloadMock class and sets up the testing logs folder path.
        """
        ...

    def download_model(self, model_path, model_type = 'trained', runtime_framework = '') -> Any:
        """
        Mock method to download a model file and copy it to the specified path.
        
                Parameters
                ----------
                model_path : str
                    Path where the model should be downloaded.
                model_type : str, optional
                    Type of model to download ('trained' or 'exported'). Default is 'trained'.
                runtime_framework : str, optional
                    Runtime framework used for the model (default is '').
        
                Returns
                -------
                bool
                    Returns True after successfully copying the model file.
        """
        ...


# From testing
class SplitMetricStruct(BaseModel):
    """
    This is a private class used internally to store split metrics.
    
        Attributes
        ----------
        splitType : str
            Type of the dataset split (e.g., 'train', 'val', 'test').
        metricName : str
            Name of the evaluation metric (e.g., 'accuracy', 'precision').
        metricValue : float
            Value of the metric for the given split.
    """

    pass

# From testing
class TestingActionTracker:
    """
    Handles logging, dataset preparation, and configuration management for model testing actions.
    
        Parameters
        ----------
        model_family_info_path : str
            Path to the model family information file.
        model_info_path : str
            Path to the model information file.
        config_path : str
            Path to the action configuration file.
    """

    def __init__(self, model_family_info_path, model_info_path, config_path) -> None:
        """
        Initializes the TestingActionTracker class, loading model family info, model info,
                and configurations.
        
                Parameters
                ----------
                model_family_info_path : str
                    Path to the model family information JSON file.
                model_info_path : str
                    Path to the model information JSON file.
                config_path : str
                    Path to the action configuration file.
        """
        ...

    def add_index_to_category(self, indexToCat) -> Any:
        """
        Adds an index-to-category mapping to the log files.
        
                Parameters
                ----------
                indexToCat : dict
                    Dictionary mapping category indexes to class names.
        
                Returns
                -------
                dict
                    The index-to-category mapping.
        """
        ...

    def add_logs(self, step, status, description) -> Any:
        """
        Adds a log entry for a specific step, including status and description.
        
                Parameters
                ----------
                step : str
                    The step or action being logged (e.g., 'load_model').
                status : str
                    The status of the step (e.g., 'SUCCESS', 'ERROR').
                description : str
                    A description or error message related to the step.
        """
        ...

    def cast_value(self, value_type, value) -> Any:
        """
        Casts a value to its specified type (int, float, string, bool).
        
                Parameters
                ----------
                value_type : str
                    The type to cast the value to (e.g., 'int32', 'float32').
                value : any
                    The value to be cast.
        
                Returns
                -------
                any
                    The casted value.
        """
        ...

    def convert_bbox_to_yolo(self, size, box) -> Any:
        """
        Converts bounding box coordinates to YOLO format.
        
                Parameters
                ----------
                size : tuple
                    The width and height of the image.
                box : list
                    Bounding box coordinates in the format [x, y, width, height].
        
                Returns
                -------
                tuple
                    Converted bounding box in YOLO format.
        """
        ...

    def create_data_yaml(self, dataset_dir, class_names) -> Any:
        """
        Creates a data.yaml file for the YOLO model from the dataset.
        
                Parameters
                ----------
                dataset_dir : str
                    The directory where the dataset is located.
                class_names : list
                    List of class names in the dataset.
        """
        ...

    def create_yolo_labels_from_mscoco_ann(self, dataset_dir, dst_images_dir, dst_annotations_dir, annotation_file) -> Any:
        """
        Creates YOLO labels from MSCOCO annotations.
        
                Parameters
                ----------
                dataset_dir : str
                    Directory where the dataset is stored.
                dst_images_dir : str
                    Directory where images are stored.
                dst_annotations_dir : str
                    Directory where annotations are stored.
                annotation_file : str
                    Path to the MSCOCO annotation file.
        
                Returns
                -------
                list
                    List of class names from the annotations.
        """
        ...

    def download_and_extract_dataset(self, dataset_url, dataset_dir) -> Any:
        """
        Downloads and extracts a dataset from a given URL.
        
                Parameters
                ----------
                dataset_url : str
                    The URL from which to download the dataset.
                dataset_dir : str
                    The directory where the dataset should be extracted.
        """
        ...

    def download_model(self, model_path, model_type = 'trained', runtime_framework = '') -> Any:
        """
        Downloads a model from a remote location (mocked behavior).
        
                Parameters
                ----------
                model_path : str
                    Path to download the model to.
                model_type : str, optional
                    Type of model (default is 'trained').
                runtime_framework : str, optional
                    Framework used for the model (default is '').
        """
        ...

    def get_checkpoint_path(self) -> Any:
        """
        Finds and returns the path to the latest model checkpoint.
        
                Returns
                -------
                tuple
                    Path to the checkpoint file and a boolean indicating whether it exists.
        """
        ...

    def get_file_extension(self, content_type) -> Any:
        """
        Returns the appropriate file extension based on content type.
        
                Parameters
                ----------
                content_type : str
                    The content type of the file.
        
                Returns
                -------
                str
                    The file extension (e.g., '.zip', '.tar').
        """
        ...

    def get_index_to_category(self, is_exported = False) -> Any:
        """
        Retrieves the index-to-category mapping from the log files.
        
                Parameters
                ----------
                is_exported : bool, optional
                    Indicates whether the model is exported (default is False).
        
                Returns
                -------
                dict
                    The index-to-category mapping.
        """
        ...

    def get_job_params(self) -> Any:
        """
        Generates and returns job parameters for model testing.
        
                Returns
                -------
                dict
                    A dictionary containing dataset and model configuration parameters.
        """
        ...

    def get_main_action_logs_path(self) -> Any:
        """
        Determines the appropriate log file path based on the action type (train, export, eval).
        
                Returns
                -------
                str
                    Path to the main log file for the current action.
        """
        ...

    def get_model_train(self, is_exported = False) -> Any:
        """
        Mock function to retrieve the model training document.
        
                This mock version simulates the retrieval of the model training document without making
                    actual API calls.
        
                Parameters
                ----------
                is_exported : bool, optional
                    If True, retrieves the model train document by export ID (default is False).
        
                Returns
                -------
                dict
                    A mock model training document.
        
                Raises
                ------
                Exception
                    If there is an error in fetching the model training document.
        """
        ...

    def load_action_config(self) -> Any:
        """
        Loads action configuration based on the config path (train, export, eval).
        
                Raises
                ------
                Exception
                    If the config path is not valid or cannot be loaded.
        """
        ...

    def load_model_family_info(self) -> Any:
        """
        Loads model family information from the specified file.
        
                Returns
                -------
                dict
                    The loaded model family information.
        """
        ...

    def load_model_info(self) -> Any:
        """
        Loads model information from the specified file.
        
                Returns
                -------
                dict
                    The loaded model information.
        """
        ...

    def log_decorator(func) -> Any:
        ...

    def log_epoch_results(self, epoch, epoch_result_list: List[SplitMetricStruct]) -> Any:
        """
        Logs the results of an epoch during model training.
        
                Parameters
                ----------
                epoch : int
                    The current epoch number.
                epoch_result_list : List[SplitMetricStruct]
                    List of metrics for the current epoch.
        """
        ...

    def log_to_json(self, file_path, payload) -> Any:
        """
        Logs data to a JSON file, appending the payload if the file exists.
        
                Parameters
                ----------
                file_path : str
                    Path to the JSON log file.
                payload : dict
                    The data to log in the JSON file.
        """
        ...

    def mock_action_doc(self) -> Any:
        """
        Creates a mock action document with dataset and model details.
        
                Returns
                -------
                dict
                    A mock document containing action and model information.
        """
        ...

    def prepare_classification_dataset(self, dataset_dir) -> Any:
        """
        Prepares a dataset for classification tasks.
        
                Parameters
                ----------
                dataset_dir : str
                    The directory where the dataset is located.
        """
        ...

    def prepare_dataset(self) -> Any:
        """
        Prepares the dataset for training or evaluation by downloading and formatting it.
        """
        ...

    def prepare_detection_dataset(self, dataset_dir) -> Any:
        """
        Prepares a dataset for object detection tasks.
        
                Parameters
                ----------
                dataset_dir : str
                    The directory where the dataset is located.
        """
        ...

    def prepare_yolo_dataset(self, dataset_dir) -> Any:
        """
        Prepares the dataset for YOLO model training.
        
                Parameters
                ----------
                dataset_dir : str
                    The directory where the dataset is located.
        """
        ...

    def round_metrics(self, epoch_result_list) -> Any:
        """
        Rounds the metric values to four decimal places, replacing NaN or inf with 0.
        
                Parameters
                ----------
                epoch_result_list : List[dict]
                    List of metrics with values to be rounded.
        
                Returns
                -------
                List[dict]
                    List of metrics with rounded values.
        """
        ...

    def save_evaluation_results(self, list_of_result_dicts: List[SplitMetricStruct]) -> Any:
        """
        Saves evaluation results to the log files.
        
                Parameters
                ----------
                list_of_result_dicts : List[SplitMetricStruct]
                    List of evaluation metrics and results.
        """
        ...

    def update_status(self, stepCode, status, status_description) -> None:
        """
        Mocks the status update for a given step, adding it to logs.
        
                Parameters
                ----------
                stepCode : str
                    The code for the current step.
                status : str
                    The current status (e.g., 'SUCCESS', 'ERROR').
                status_description : str
                    Description or details about the step status.
        """
        ...

    def upload_checkpoint(self, checkpoint_path, model_type = 'trained') -> Any:
        """
        Uploads a checkpoint to a remote location (mocked behavior).
        
                Parameters
                ----------
                checkpoint_path : str
                    Path to the checkpoint file to be uploaded.
                model_type : str, optional
                    Type of model (default is 'trained').
        """
        ...

    def validate_metrics_structure(self, metrics_list: List[SplitMetricStruct]) -> Any:
        """
        Validates the structure of a list of metrics.
        
                Parameters
                ----------
                metrics_list : List[SplitMetricStruct]
                    List of metrics to be validated.
        
                Returns
                -------
                List[SplitMetricStruct]
                    The validated metrics.
        """
        ...


# From testing
class TestingMatriceDeploy:
    """
    Class to handle deployment and inference of models for testing purposes.
    
        This class handles model downloading, logging, and running inference with a provided model.
    
        Parameters
        ----------
        load_model : function
            Function to load a model during testing.
        predict : function
            Function to make predictions using the loaded model.
    """

    def __init__(self, load_model, predict) -> None:
        """
        Initializes the TestingMatriceDeploy class, setting up logs and triggering inference.
        
                Parameters
                ----------
                load_model : function
                    Function that loads a model for inference.
                predict : function
                    Function to perform prediction with the loaded model.
        """
        ...

    def add_logs(self, step, status, description) -> Any:
        """
        Adds a log entry for a specific step, including status and description.
        
                Parameters
                ----------
                step : str
                    The step or action being logged (e.g., 'inference').
                status : str
                    The status of the step (e.g., 'SUCCESS', 'ERROR').
                description : str
                    A description or error message related to the step.
        """
        ...

    def create_image_bytes(self) -> Any:
        """
        Creates a simple test image in memory as a byte stream.
        
                Returns
                -------
                bytes
                    Image data in JPEG format.
        """
        ...

    def inference(self, image) -> Any:
        """
        Runs inference on an image using the loaded model.
        
                Parameters
                ----------
                image : bytes
                    Image data in bytes to be used for inference.
        
                Returns
                -------
                tuple
                    Inference results and a success flag.
        """
        ...

    def load_predictor_model(self) -> Any:
        """
        Loads the predictor model using the model downloader.
        """
        ...

    def log_decorator(func) -> Any:
        """
        A decorator to log the execution status of a function.
        """
        ...

    def log_to_json(self, file_path, payload) -> Any:
        """
        Logs data to a JSON file, appending the payload if the file exists.
        
                Parameters
                ----------
                file_path : str
                    Path to the JSON log file.
                payload : dict
                    The data to log in the JSON file.
        """
        ...


# From testing
class dotdict(dict):
    """
    A dictionary subclass that provides dot notation access to attributes.
    
        Attributes
        ----------
        __getattr__ : function
            Allows accessing dictionary keys as object attributes.
        __setattr__ : function
            Allows setting dictionary keys as object attributes.
        __delattr__ : function
            Allows deleting dictionary keys as object attributes.
    """

    pass

from . import action, actionTracker, action_tracker, annotation, app_integration, app_store, application, camera_management, checkpoint, compute, dataset, docker_utils, drift_monitor, exported_model, inference_orchestrator, inference_pipeline_management, local_testing, metrics_calculator, metrics_calculator_oop, model_store, models, pipeline, projects, scaling, security_utils, streaming_automation, streaming_benchmarking, streaming_gateway_management, testing

def __getattr__(name: str) -> Any: ...