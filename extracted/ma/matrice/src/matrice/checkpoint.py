"""
Model Checkpoint API (be-model).

Implements the pretrained-checkpoint endpoints under the ``/v1/model`` service.

Endpoints implemented here:

- ``GET /v1/model/get_model_checkpoint_upload_path?projectId=...`` — presigned upload URL
- ``POST /v1/model/checkpoint`` — register a (already uploaded) checkpoint
- ``GET /v1/model/checkpoints?projectId=...`` — list checkpoints registered under a project

Plus a helper :func:`upload_checkpoint_file` which does the full two-step flow
(get presigned URL → PUT file) and returns the clean public URL ready for
:func:`create_checkpoint`.
"""

from __future__ import annotations

import os
from typing import Any

import requests
from matrice_common.utils import handle_response


def create_checkpoint(
    session: Any,
    project_id: str,
    name: str,
    checkpoint_value: str,
    model_family: str,
    model_key: str,
    checkpoint_type: str = "URL",
    dataset: str = "",
    class_index_map: dict[str, str] | None = None,
) -> tuple[dict | None, str | None, str]:
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
    # Build body exactly per API §2.1 order and naming (camelCase)
    payload = {
        "modelFamily": model_family,
        "modelKey": model_key,
        "name": name,
        "_idProject": project_id,
        "checkpointType": checkpoint_type,
        "checkpointValue": checkpoint_value,
        "dataset": dataset or "",
    }
    if class_index_map is not None:
        payload["classIndexMap"] = class_index_map

    resp = session.rpc.post(path="/v1/model/checkpoint", payload=payload)
    data, error, message = handle_response(
        resp,
        "Checkpoint created",
        "Error creating checkpoint",
    )
    # Unwrap inner checkpoint document so callers get data.get("_id") directly
    if data and isinstance(data, dict) and "data" in data:
        data = data.get("data")
    return (data, error, message)


def get_model_checkpoint_upload_path(
    session: Any,
    project_id: str,
) -> tuple[str | None, str | None, str]:
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
    path = f"/v1/model/get_model_checkpoint_upload_path?projectId={project_id}"
    resp = session.rpc.get(path=path)
    data, error, message = handle_response(
        resp,
        "Checkpoint upload URL generated",
        "Error generating checkpoint upload URL",
    )
    # Backend returns the presigned URL as a plain string in ``data``.
    url: str | None = None
    if not error and data is not None:
        if isinstance(data, str):
            url = data
        elif isinstance(data, dict):
            inner = data.get("data", data)
            if isinstance(inner, str):
                url = inner
    return (url, error, message)


def upload_checkpoint_file(
    session: Any,
    project_id: str,
    file_path: str,
    content_type: str = "application/octet-stream",
    timeout: int = 300,
) -> tuple[str | None, str | None, str]:
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
    if not os.path.isfile(file_path):
        return (None, f"File not found: {file_path}", "Error uploading checkpoint")

    upload_url, error, message = get_model_checkpoint_upload_path(session, project_id)
    if error or not upload_url:
        return (None, error or "No upload URL returned", message)

    try:
        with open(file_path, "rb") as fh:
            resp = requests.put(
                upload_url,
                data=fh,
                headers={"Content-Type": content_type},
                timeout=timeout,
            )
    except Exception as exc:
        return (None, f"Upload failed: {exc}", "Error uploading checkpoint")

    if resp.status_code not in (200, 201, 204):
        return (
            None,
            f"Upload failed with HTTP {resp.status_code}: {resp.text[:200]}",
            "Error uploading checkpoint",
        )

    public_url = upload_url.split("?")[0]
    return (public_url, None, "Checkpoint uploaded successfully")


def list_checkpoints(
    session: Any,
    project_id: str,
) -> tuple[list | None, str | None, str]:
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
    path = f"/v1/model/checkpoints?projectId={project_id}"
    resp = session.rpc.get(path=path)
    data, error, message = handle_response(
        resp,
        "Checkpoints listed",
        "Error listing checkpoints",
    )
    items: list | None = None
    if not error:
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            inner = data.get("data", data)
            items = inner if isinstance(inner, list) else []
        else:
            items = []
    return (items, error, message)


def upload_and_register_checkpoint(
    session: Any,
    project_id: str,
    file_path: str,
    name: str,
    model_family: str,
    model_key: str,
    class_index_map: dict[str, str] | None = None,
    dataset: str = "",
) -> tuple[dict | None, str | None, str]:
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
    public_url, error, message = upload_checkpoint_file(session, project_id, file_path)
    if error or not public_url:
        return (None, error, message)
    return create_checkpoint(
        session,
        project_id=project_id,
        name=name,
        checkpoint_value=public_url,
        model_family=model_family,
        model_key=model_key,
        checkpoint_type="URL",
        dataset=dataset,
        class_index_map=class_index_map,
    )
