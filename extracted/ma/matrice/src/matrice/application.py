"""
Applications API (be-application).

Implements API Backend - Applications.md §3 (Applications), §4 (Add Model to Application),
§5 (Publish Model — be-model-store), §6 (Publish Application Version), §7 (Approve/Publish Application),
§8 (List All Application Versions).

Also implements the application cover upload helpers
(``/v1/applications/get_application_cover_upload_path``) and the per-application
version lookup (``/v1/applications/version/:id``) that are used during end-to-end
application onboarding.

Base URL: /v1/applications (and /v1/model_store for request_publish_model_family).
"""

from __future__ import annotations

import os
from typing import Any

import requests
from matrice_common.utils import handle_response


def list_applications(
    session: Any,
    page_size: int = 200,
    page_number: int = 0,
    sort_by: str = "",
    sort_order: str = "asc",
) -> tuple[dict | None, str | None, str]:
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
    path = (
        "/v1/applications/list_applications"
        f"?pageSize={page_size}"
        f"&currentPage={page_number}"
        f"&pageNumber={page_number}"
        f"&sortBy={sort_by}"
        f"&sortOrder={sort_order}"
    )
    resp = session.rpc.get(path=path)
    return handle_response(resp, "Applications listed", "Error listing applications")


def find_application_by_name(
    session: Any,
    name: str,
    page: int = 1,
    page_size: int = 200,
) -> tuple[dict | None, str | None]:
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
    target = (name or "").strip()
    if not target:
        return (None, "name is required")
    data, err, _ = list_applications(session, page_size=page_size, page_number=max(0, page - 1))
    if err:
        return (None, err)

    if not isinstance(data, dict):
        return (None, None)

    inner = data.get("data")
    if isinstance(inner, dict):
        items = inner.get("items") or []
    else:
        items = data.get("items") or []

    if not isinstance(items, list):
        return (None, None)

    for app in items:
        if not isinstance(app, dict):
            continue
        app_name = (app.get("name") or app.get("applicationName") or "").strip()
        if app_name == target:
            return (app, None)

    return (None, None)


def get_application_by_id(
    session: Any,
    application_id: str,
) -> tuple[dict | None, str | None, str]:
    """
    Get a single application by ID — GET /v1/applications/:id (API Backend §3).

    **Path:** id = Application ObjectID.

    Returns
    -------
    tuple
        (data, error, message). data is the application object on success.
    """
    path = f"/v1/applications/{application_id}"
    resp = session.rpc.get(path=path)
    return handle_response(resp, "Application fetched", "Error fetching application")


def get_application_cover_upload_path(
    session: Any,
) -> tuple[str | None, str | None, str]:
    """
    Get a presigned PUT URL to upload an application cover image.

    Wraps ``GET /v1/applications/get_application_cover_upload_path``.

    Returns
    -------
    tuple
        ``(upload_url, error, message)``. On success ``upload_url`` is a full
        presigned URL string that accepts ``PUT``.
    """
    path = "/v1/applications/get_application_cover_upload_path"
    resp = session.rpc.get(path=path)
    data, error, message = handle_response(
        resp,
        "Cover upload URL generated",
        "Error generating cover upload URL",
    )
    url: str | None = None
    if not error and data is not None:
        if isinstance(data, str):
            url = data
        elif isinstance(data, dict):
            inner = data.get("data", data)
            if isinstance(inner, str):
                url = inner
    return (url, error, message)


def upload_application_cover_image(
    session: Any,
    image_path: str,
    content_type: str = "image/png",
    timeout: int = 120,
) -> tuple[str | None, str | None, str]:
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
    if not os.path.isfile(image_path):
        return (None, f"File not found: {image_path}", "Error uploading cover image")

    # Best-effort content-type from extension
    ext = os.path.splitext(image_path)[1].lower()
    ext_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    if content_type == "image/png" and ext in ext_map:
        content_type = ext_map[ext]

    upload_url, error, message = get_application_cover_upload_path(session)
    if error or not upload_url:
        return (None, error or "No upload URL returned", message)

    try:
        with open(image_path, "rb") as fh:
            resp = requests.put(
                upload_url,
                data=fh,
                headers={"Content-Type": content_type},
                timeout=timeout,
            )
    except Exception as exc:
        return (None, f"Upload failed: {exc}", "Error uploading cover image")

    if resp.status_code not in (200, 201, 204):
        return (
            None,
            f"Upload failed with HTTP {resp.status_code}: {resp.text[:200]}",
            "Error uploading cover image",
        )

    return (upload_url.split("?")[0], None, "Cover image uploaded successfully")


def get_application_versions(
    session: Any,
    application_id: str,
) -> tuple[list | None, str | None, str]:
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
    path = f"/v1/applications/version/{application_id}"
    resp = session.rpc.get(path=path)
    data, error, message = handle_response(
        resp,
        "Application versions fetched",
        "Error fetching application versions",
    )
    versions: list | None = None
    if not error:
        if isinstance(data, list):
            versions = data
        elif isinstance(data, dict):
            inner = data.get("data", data)
            versions = inner if isinstance(inner, list) else []
        else:
            versions = []
    return (versions, error, message)


def list_models_for_application(
    session: Any,
    application_id: str,
) -> tuple[list, str | None, str]:
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
    # 1) GET /v1/applications/:id — response may contain models/modelVersions/versions
    app_data, app_err, _ = get_application_by_id(session, application_id)
    if not app_err and app_data:
        payload = app_data.get("data", app_data) if isinstance(app_data, dict) else app_data
        if isinstance(payload, dict):
            for key in ("models", "modelVersions", "versions", "model_versions"):
                val = payload.get(key)
                if isinstance(val, list):
                    return (val, None, "Models from GET application")
    # 2) GET /v1/applications/versions — filter by _idApplication (API §8)
    versions_data, ver_err, _ = list_application_versions(session, status=None)
    if not ver_err and isinstance(versions_data, list):
        filtered = [v for v in versions_data if isinstance(v, dict) and v.get("_idApplication") == application_id]
        return (filtered, None, "Application versions (from GET /v1/applications/versions)")
    # 3) Try GET /v1/applications/:id/models (undocumented)
    try:
        path = f"/v1/applications/{application_id}/models"
        resp = session.rpc.get(path=path)
        if resp and resp.get("success") is not False:
            data = resp.get("data", resp)
            if isinstance(data, list):
                return (data, None, "Models from GET application models")
            if isinstance(data, dict) and "items" in data:
                return (data.get("items", []), None, "Models from GET application models")
    except Exception:
        pass
    # No models found from any source
    if app_err and ver_err:
        return ([], app_err or ver_err, "Could not list models or versions")
    return ([], None, "No models/versions found for this application")


def list_application_versions(
    session: Any,
    status: str | None = None,
) -> tuple[list | None, str | None, str]:
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
    path = "/v1/applications/versions"
    if status:
        path = f"{path}?status={status}"
    resp = session.rpc.get(path=path)
    data, error, message = handle_response(resp, "Application versions listed", "Error listing application versions")
    if data and isinstance(data, dict) and "data" in data:
        data = data.get("data")
    return (data, error, message)


def request_publish_model_family(
    session: Any,
    model_family_id: str,
) -> tuple[dict | None, str | None, str]:
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
    path = f"/v1/model_store/request_publish_model_family/{model_family_id}"
    resp = session.rpc.put(path=path)
    return handle_response(
        resp,
        "Model family publication requested",
        "Error requesting model family publication",
    )


def list_applications_via_list(session):
    """
    List applications via GET /v1/applications/list. Backend may not support this path.

    Returns
    -------
    tuple
        (data, error, message).
    """
    resp = session.rpc.get(path="/v1/applications/list")
    return handle_response(resp, "OK", "Error listing applications")


def get_application_via_list(session, application_id: str):
    """
    Resolve application by ID via list endpoint. Prefer get_application_by_id when available.

    Returns
    -------
    tuple
        (data, error, message).
    """
    data, err, msg = list_applications_via_list(session)
    if err or not data:
        return None, err or "list failed", msg
    items = data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
    for app in items:
        if isinstance(app, dict) and (app.get("_id") == application_id or app.get("id") == application_id):
            return app, None, "OK"
    return None, "not found", "Application not in list"


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

    def __init__(self, session):
        self.session = session
        self.account_number = session.account_number
        self.rpc = session.rpc

    def create_application(
        self,
        name: str,
        project_id: str,
        project_type: str,
        industries: list[str],
        categories: list[str],
        blog_link: str,
        notebook_link: str,
        app_type: str,
        release_stage: str,
        description: str,
        fps_requirements: dict[str, int],
        cover_image: str | None = None,
        objects: list[str] | None = None,
        server_type: str | None = None,
        business_analytics: list[str] | None = None,
        incident_types: list[dict] | None = None,
        alerts: dict | None = None,
        reset_settings: dict | None = None,
    ) -> tuple[dict | None, str | None, str]:
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
        path = "/v1/applications/"
        headers = {"Content-Type": "application/json"}
        payload = {
            "name": name,
            "projectId": project_id,
            "accountNumber": self.account_number,
            "projectType": project_type,
            "industries": industries,
            "categories": categories,
            "blogLink": blog_link or "",
            "notebookLink": notebook_link or "",
            "appType": app_type,
            "releaseStage": release_stage,
            "description": description or "",
            "fpsRequirements": fps_requirements,
        }
        if cover_image is not None:
            payload["coverImage"] = cover_image
        if objects is not None:
            payload["objects"] = objects
        if server_type is not None:
            payload["serverType"] = server_type
        if business_analytics is not None:
            payload["businessAnalytics"] = business_analytics
        if incident_types is not None:
            payload["incidentTypes"] = incident_types
        if alerts is not None:
            payload["alerts"] = alerts
        if reset_settings is not None:
            payload["resetSettings"] = reset_settings

        resp = self.rpc.post(path=path, headers=headers, payload=payload)
        return handle_response(
            resp,
            "Successfully created Application",
            f"Error creating applications: {resp}",
        )

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
        path = f"/v1/applications/{application_id}"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.delete(path=path, headers=headers)
        return handle_response(
            resp,
            "Successfully deleted application",
            f"Error deleting application: {resp}",
        )

    def add_model_version(
        self,
        application_id: str,
        project_id: str,
        model_id: str,
        model_type: str,
        model_name: str,
        blog_link: str,
        post_processing: list[dict],
        runtime: list[str],
        fps_requirements: dict[str, int],
        performance: dict,
        notebook_link: str | None = None,
        gpu_memory: int | None = None,
        metrics: list[dict] | None = None,
        color_mapping: dict[str, str] | None = None,
        arch_checkpoints: dict[str, str] | None = None,
    ) -> tuple[dict | None, str | None, str]:
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
        path = f"/v1/applications/{application_id}/models"
        headers = {"Content-Type": "application/json"}
        # Ensure performance has API shape: published, benchmarked, measuredIP (per API §4)
        perf = dict(performance or {})
        perf.setdefault("published", perf.get("published") if isinstance(perf.get("published"), list) else [])
        perf.setdefault("benchmarked", perf.get("benchmarked", []) if isinstance(perf.get("benchmarked"), list) else [])
        perf.setdefault("measuredIP", perf.get("measuredIP", []) if isinstance(perf.get("measuredIP"), list) else [])

        payload = {
            "_idApplication": application_id,
            "projectId": project_id,
            "modelId": model_id,
            "modelType": model_type,
            "modelName": model_name,
            "blogLink": blog_link or "",
            "postProcessing": post_processing,
            "runtime": runtime,
            "fpsRequirements": fps_requirements,
            "performance": perf,
        }
        if notebook_link is not None:
            payload["notebookLink"] = notebook_link
        if gpu_memory is not None:
            # Real backend accepts gpuMemoryMB (per captured request); keep legacy alias too.
            payload["gpuMemoryMB"] = gpu_memory
            payload["gpuMemory"] = gpu_memory
        if metrics is not None:
            payload["metrics"] = metrics
        if color_mapping is not None:
            payload["colorMapping"] = color_mapping
        if arch_checkpoints is not None:
            payload["archCheckpoints"] = arch_checkpoints

        resp = self.rpc.post(path=path, headers=headers, payload=payload)
        return handle_response(resp, "Model Added Successfully", f"Error adding model version: {resp}")

    def approve_application(
        self,
        application_id: str,
        status: str = "published",
    ) -> tuple[dict | None, str | None, str]:
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
        path = f"/v1/applications/{application_id}"
        if "?" in path:
            path = f"{path}&status={status}"
        else:
            path = f"{path}?status={status}"
        resp = self.rpc.put(path=path, payload={})
        return handle_response(
            resp,
            "Application approved successfully",
            f"Error approving application: {resp}",
        )

    def publish_model(
        self,
        application_id: str,
        version: str,
        status: str = "published",
    ) -> tuple[dict | None, str | None, str]:
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
        path = f"/v1/applications/version/{application_id}/approve/{version}?status={status}"
        resp = self.rpc.put(path=path, payload={})
        return handle_response(
            resp,
            "Model version published successfully",
            f"Error publishing model version: {resp}",
        )

    def delete_model(self, model_id):
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
        path = f"/v1/models/{model_id}"
        headers = {"Content-Type": "application/json"}

        resp = self.rpc.delete(path=path, headers=headers, session=self.session)

        return handle_response(resp, "Model deleted successfully", f"Error deleting model: {resp}")
