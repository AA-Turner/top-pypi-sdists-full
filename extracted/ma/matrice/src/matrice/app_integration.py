"""
End-to-end Matrice application integration.

This module provides :class:`AppIntegrator` — a single Pythonic entry-point that
orchestrates every step required to publish a brand-new computer-vision
application on the Matrice platform:

1. Upload a pretrained model checkpoint (``.pt`` / ``.pth`` / …) to Matrice
   storage and register it as a Model Checkpoint.
2. Upload the application's cover image.
3. Create the application shell (name, project type, industries, categories,
   description, FPS requirements, blog/notebook links, …).
4. Resolve the freshly-created application's ``_id`` (the create endpoint does
   not return it).
5. Attach a model version with the post-processing use case configuration that
   plugs into ``matrice_analytics.post_processing`` (e.g. ``fence_climbing_detection``).
6. (Optional) Approve / publish the application and its first version.

The class wraps the lower-level RPC helpers in
:mod:`matrice.checkpoint` and :mod:`matrice.application`, so it plays nicely
with the rest of the SDK — the ``self.session`` and ``self.rpc`` attributes
behave identically to any other ``matrice.*`` wrapper.

Quick example
-------------
::

    from matrice.app_integration import AppIntegrator

    integrator = AppIntegrator(
        access_key="YOUR_ACCESS_KEY",
        secret_key="YOUR_SECRET_KEY",
        account_number="9782886768719887307619115",
    )

    result = integrator.integrate_new_app(
        project_id="69e8f7233dbcf98d5b396427",
        checkpoint_path="./my_model.pt",
        cover_image_path="./cover.png",
        checkpoint_name="fence-climbing-v1",
        model_family="YOLOv8",
        model_key="yolov8m",
        class_index_map={"0": "person"},
        application_name="Fence Climbing Detection",
        project_type="detection",
        industries=["Security"],
        categories=["safety"],
        description="Detects persons climbing fences in restricted zones.",
        fps_requirements={"minimumFPS": 10, "maximumFPS": 10},
        model_name="Fence Climbing — YOLOv8m v1",
        runtime=["pytorch"],
        gpu_memory_mb=8000,
        post_processing=[{
            "usecase": "fence_climbing_detection",
            "category": "general",
            "confidence_threshold": 0.5,
            "climbing_confidence_threshold": 0.6,
            "enable_tracking": True,
            "enable_analytics": True,
            "target_categories": ["person"],
            "person_categories": ["person", "people"],
            "min_climbing_frames": 3,
            "exit_grace_frames": 3,
            "zone_config": {
                "zones": {"fence_zone": [[0, 0], [1920, 0], [1920, 540], [0, 540]]}
            },
            "alert_config": {
                "alert_type": ["Default"],
                "alert_value": ["JSON"],
                "count_thresholds": {"all": 1},
            },
        }],
    )

    print(result["application_id"], result["checkpoint_id"])
"""

from __future__ import annotations

import logging

from matrice_common.session import Session

from matrice.application import (
    Application,
    find_application_by_name,
    get_application_by_id,
    get_application_cover_upload_path,
    get_application_versions,
    list_application_versions,
    list_applications,
    upload_application_cover_image,
)
from matrice.checkpoint import (
    create_checkpoint,
    get_model_checkpoint_upload_path,
    list_checkpoints,
    upload_checkpoint_file,
)

logger = logging.getLogger(__name__)

_DEFAULT_FPS = {"minimumFPS": 10, "maximumFPS": 10}


class AppIntegrationError(RuntimeError):
    """Raised when an individual step of the integration flow fails."""


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

    def __init__(
        self,
        access_key: str | None = None,
        secret_key: str | None = None,
        account_number: str | None = None,
        *,
        session: Session | None = None,
    ) -> None:
        if session is None:
            if not (access_key and secret_key and account_number):
                raise ValueError(
                    "AppIntegrator requires either a pre-built `session=` or all of "
                    "`access_key`, `secret_key`, and `account_number`."
                )
            session = Session(
                account_number=account_number,
                access_key=access_key,
                secret_key=secret_key,
            )

        self.session: Session = session
        self.rpc = session.rpc
        self.account_number: str = session.account_number
        self.application = Application(session)

    # ------------------------------------------------------------------ #
    # Low-level, individually-callable steps                             #
    # ------------------------------------------------------------------ #

    def list_projects(
        self,
        project_type: str = "",
        page_size: int = 200,
        page_number: int = 0,
    ) -> list[dict]:
        """
        List all projects on the account.

        Thin wrapper around :meth:`Session.list_projects` returning only the
        item list. Use the returned ``_id`` as ``project_id`` when calling
        :meth:`upload_model_checkpoint`.
        """
        projects, _ = self.session.list_projects(
            project_type=project_type,
            page_size=page_size,
            page_number=page_number,
        )
        return projects or []

    def get_project_id_by_name(self, project_name: str) -> str:
        """
        Resolve a ``project_id`` from a project name.

        Raises :class:`AppIntegrationError` if the project is not found.
        """
        path = f"/v1/accounting/get_project_by_name?name={project_name}"
        resp = self.rpc.get(path=path)
        if not resp or not resp.get("success"):
            raise AppIntegrationError(f"Could not resolve project by name {project_name!r}: {resp}")
        data = resp.get("data") or {}
        pid = data.get("_id")
        if not pid:
            raise AppIntegrationError(f"Project {project_name!r} found but response has no _id: {data}")
        return pid

    # -- Step 1: model checkpoint ------------------------------------------- #

    def upload_model_checkpoint(
        self,
        project_id: str,
        checkpoint_path: str,
    ) -> str:
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
        url, err, msg = upload_checkpoint_file(self.session, project_id, checkpoint_path)
        if err or not url:
            raise AppIntegrationError(f"Upload checkpoint failed: {err or msg}")
        logger.info("Uploaded checkpoint to %s", url)
        return url

    def register_checkpoint(
        self,
        project_id: str,
        name: str,
        checkpoint_url: str,
        model_family: str,
        model_key: str,
        class_index_map: dict[str, str] | None = None,
        dataset: str = "",
    ) -> dict:
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
        doc, err, msg = create_checkpoint(
            self.session,
            project_id=project_id,
            name=name,
            checkpoint_value=checkpoint_url,
            model_family=model_family,
            model_key=model_key,
            checkpoint_type="URL",
            dataset=dataset,
            class_index_map=class_index_map,
        )
        if err or not doc:
            raise AppIntegrationError(f"Register checkpoint failed: {err or msg}")
        return doc

    def upload_and_register_checkpoint(
        self,
        project_id: str,
        checkpoint_path: str,
        name: str,
        model_family: str,
        model_key: str,
        class_index_map: dict[str, str] | None = None,
        dataset: str = "",
    ) -> dict:
        """
        Combined helper: :meth:`upload_model_checkpoint` +
        :meth:`register_checkpoint`. Returns the registered checkpoint dict.
        """
        url = self.upload_model_checkpoint(project_id, checkpoint_path)
        return self.register_checkpoint(
            project_id=project_id,
            name=name,
            checkpoint_url=url,
            model_family=model_family,
            model_key=model_key,
            class_index_map=class_index_map,
            dataset=dataset,
        )

    def list_checkpoints(self, project_id: str) -> list[dict]:
        """List model checkpoints registered under a project."""
        items, err, msg = list_checkpoints(self.session, project_id)
        if err:
            raise AppIntegrationError(f"List checkpoints failed: {err or msg}")
        return items or []

    def get_model_checkpoint_upload_url(self, project_id: str) -> str:
        """Return only the presigned URL (if you want to PUT the file yourself)."""
        url, err, msg = get_model_checkpoint_upload_path(self.session, project_id)
        if err or not url:
            raise AppIntegrationError(f"Get checkpoint upload URL failed: {err or msg}")
        return url

    # -- Step 2: cover image ------------------------------------------------ #

    def upload_cover_image(self, image_path: str) -> str:
        """
        Upload an application cover image and return the clean public URL.
        """
        url, err, msg = upload_application_cover_image(self.session, image_path)
        if err or not url:
            raise AppIntegrationError(f"Upload cover image failed: {err or msg}")
        logger.info("Uploaded cover image to %s", url)
        return url

    def get_cover_upload_url(self) -> str:
        """Return only the presigned URL (caller performs the PUT themselves)."""
        url, err, msg = get_application_cover_upload_path(self.session)
        if err or not url:
            raise AppIntegrationError(f"Get cover upload URL failed: {err or msg}")
        return url

    # -- Step 3: application CRUD ------------------------------------------ #

    def create_application(
        self,
        name: str,
        project_id: str,
        project_type: str,
        industries: list[str],
        categories: list[str],
        description: str,
        cover_image_url: str | None = None,
        blog_link: str = "",
        notebook_link: str = "",
        app_type: str = "Standard",
        release_stage: str = "beta",
        fps_requirements: dict[str, int] | None = None,
        objects: list[str] | None = None,
        server_type: str | None = None,
        business_analytics: list[str] | None = None,
        incident_types: list[dict] | None = None,
        alerts: dict | None = None,
        reset_settings: dict | None = None,
    ) -> dict:
        """
        Create an application. Returns the raw API response dict.

        Note that the backend does NOT return the new application's ``_id`` in
        this response; use :meth:`find_application_id` to resolve it by name
        after creation (this is exactly how the UI does it).
        """
        data, err, msg = self.application.create_application(
            name=name,
            project_id=project_id,
            project_type=project_type,
            industries=industries,
            categories=categories,
            blog_link=blog_link,
            notebook_link=notebook_link,
            app_type=app_type,
            release_stage=release_stage,
            description=description,
            fps_requirements=fps_requirements or dict(_DEFAULT_FPS),
            cover_image=cover_image_url,
            objects=objects,
            server_type=server_type,
            business_analytics=business_analytics,
            incident_types=incident_types,
            alerts=alerts,
            reset_settings=reset_settings,
        )
        if err:
            raise AppIntegrationError(f"Create application failed: {err or msg}")
        return data

    def find_application_id(self, name: str, page_size: int = 200) -> str:
        """
        Look up an application's ``_id`` by exact name match.

        Raises :class:`AppIntegrationError` if the application is not in the
        first page of ``page_size`` results.
        """
        app, err = find_application_by_name(self.session, name, page_size=page_size)
        if err:
            raise AppIntegrationError(f"Find application by name failed: {err}")
        if not app:
            raise AppIntegrationError(f"Application {name!r} not found")
        return app.get("_id") or app.get("applicationid")

    def list_applications(
        self,
        page_size: int = 200,
        page_number: int = 0,
    ) -> list[dict]:
        """List applications visible to the caller."""
        data, err, msg = list_applications(self.session, page_size=page_size, page_number=page_number)
        if err:
            raise AppIntegrationError(f"List applications failed: {err or msg}")
        payload = data.get("data", data) if isinstance(data, dict) else data
        if isinstance(payload, dict):
            return payload.get("items") or []
        if isinstance(payload, list):
            return payload
        return []

    def get_application(self, application_id: str) -> dict:
        """Fetch a single application document."""
        data, err, msg = get_application_by_id(self.session, application_id)
        if err:
            raise AppIntegrationError(f"Get application failed: {err or msg}")
        payload = data.get("data", data) if isinstance(data, dict) else data
        return payload or {}

    def list_application_versions(self, application_id: str) -> list[dict]:
        """List versions of a specific application."""
        versions, err, msg = get_application_versions(self.session, application_id)
        if err:
            raise AppIntegrationError(f"List application versions failed: {err or msg}")
        return versions or []

    def list_all_application_versions(self, status: str | None = None) -> list[dict]:
        """
        Account-wide listing — ``GET /v1/applications/versions``.

        Mostly useful for admins auditing approvals; for per-application
        versions use :meth:`list_application_versions`.
        """
        data, err, msg = list_application_versions(self.session, status=status)
        if err:
            raise AppIntegrationError(f"List application versions failed: {err or msg}")
        return data or []

    # -- Step 4: application version (model + post-processing) ------------- #

    def add_application_version(
        self,
        application_id: str,
        project_id: str,
        model_id: str,
        model_name: str,
        post_processing: list[dict],
        runtime: list[str] | None = None,
        fps_requirements: dict[str, int] | None = None,
        model_type: str = "pretrained",
        gpu_memory_mb: int | None = 8000,
        blog_link: str = "",
        notebook_link: str | None = None,
        performance: dict | None = None,
        metrics: list[dict] | None = None,
        color_mapping: dict[str, str] | None = None,
        arch_checkpoints: dict[str, str] | None = None,
    ) -> dict:
        """
        Attach a model version to an existing application.

        ``post_processing`` is a list of dicts; each dict **must** include at
        least ``usecase`` and ``category`` matching a use-case registered in
        ``matrice_analytics.post_processing``. All other keys map directly to
        fields on the corresponding ``*Config`` dataclass.
        """
        data, err, msg = self.application.add_model_version(
            application_id=application_id,
            project_id=project_id,
            model_id=model_id,
            model_type=model_type,
            model_name=model_name,
            blog_link=blog_link,
            post_processing=post_processing,
            runtime=list(runtime or ["pytorch"]),
            fps_requirements=fps_requirements or dict(_DEFAULT_FPS),
            performance=performance or {},
            notebook_link=notebook_link,
            gpu_memory=gpu_memory_mb,
            metrics=metrics,
            color_mapping=color_mapping,
            arch_checkpoints=arch_checkpoints,
        )
        if err:
            raise AppIntegrationError(f"Add application version failed: {err or msg}")
        return data

    # -- Step 5: approve / publish ----------------------------------------- #

    def approve_application(self, application_id: str, status: str = "published") -> dict:
        """Approve / change the top-level application status."""
        data, err, msg = self.application.approve_application(application_id, status=status)
        if err:
            raise AppIntegrationError(f"Approve application failed: {err or msg}")
        return data

    def publish_application_version(
        self,
        application_id: str,
        version: str,
        status: str = "published",
    ) -> dict:
        """Publish a specific application version (e.g. ``"v1.1"``)."""
        data, err, msg = self.application.publish_model(application_id, version, status=status)
        if err:
            raise AppIntegrationError(f"Publish application version failed: {err or msg}")
        return data

    def delete_application(self, application_id: str) -> dict:
        """Delete an application."""
        data, err, msg = self.application.delete_application(application_id)
        if err:
            raise AppIntegrationError(f"Delete application failed: {err or msg}")
        return data

    # ------------------------------------------------------------------ #
    # One-shot orchestrator                                              #
    # ------------------------------------------------------------------ #

    def integrate_new_app(
        self,
        *,
        # --- project / model weights --------------------------------
        project_id: str | None = None,
        project_name: str | None = None,
        checkpoint_path: str,
        checkpoint_name: str,
        model_family: str,
        model_key: str,
        class_index_map: dict[str, str] | None = None,
        dataset: str = "",
        # --- application shell --------------------------------------
        application_name: str,
        project_type: str,
        industries: list[str],
        categories: list[str],
        description: str,
        cover_image_path: str | None = None,
        cover_image_url: str | None = None,
        blog_link: str = "",
        notebook_link: str = "",
        app_type: str = "Standard",
        release_stage: str = "beta",
        fps_requirements: dict[str, int] | None = None,
        objects: list[str] | None = None,
        business_analytics: list[str] | None = None,
        incident_types: list[dict] | None = None,
        alerts: dict | None = None,
        reset_settings: dict | None = None,
        # --- application version (model + post-processing) ----------
        model_name: str | None = None,
        post_processing: list[dict] | None = None,
        runtime: list[str] | None = None,
        gpu_memory_mb: int | None = 8000,
        performance: dict | None = None,
        metrics: list[dict] | None = None,
        color_mapping: dict[str, str] | None = None,
        arch_checkpoints: dict[str, str] | None = None,
        # --- approval -----------------------------------------------
        auto_publish: bool = False,
    ) -> dict:
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
        # 1) Resolve project id
        if not project_id:
            if not project_name:
                raise ValueError("Either project_id or project_name is required.")
            project_id = self.get_project_id_by_name(project_name)

        # 2) Upload + register checkpoint
        checkpoint_url = self.upload_model_checkpoint(project_id, checkpoint_path)
        checkpoint_doc = self.register_checkpoint(
            project_id=project_id,
            name=checkpoint_name,
            checkpoint_url=checkpoint_url,
            model_family=model_family,
            model_key=model_key,
            class_index_map=class_index_map,
            dataset=dataset,
        )
        checkpoint_id = checkpoint_doc.get("_id")
        if not checkpoint_id:
            raise AppIntegrationError(f"Checkpoint registered but response has no _id: {checkpoint_doc}")

        # 3) Cover image — upload if a local path was provided
        resolved_cover_url: str | None = cover_image_url
        if cover_image_path and not resolved_cover_url:
            resolved_cover_url = self.upload_cover_image(cover_image_path)

        # 4) Create application (no _id returned)
        self.create_application(
            name=application_name,
            project_id=project_id,
            project_type=project_type,
            industries=industries,
            categories=categories,
            description=description,
            cover_image_url=resolved_cover_url,
            blog_link=blog_link,
            notebook_link=notebook_link,
            app_type=app_type,
            release_stage=release_stage,
            fps_requirements=fps_requirements,
            objects=objects,
            business_analytics=business_analytics,
            incident_types=incident_types,
            alerts=alerts,
            reset_settings=reset_settings,
        )

        # 5) Resolve the new application's id via list + name match
        application_id = self.find_application_id(application_name)

        # 6) Attach the model version w/ post-processing (optional)
        version_resp: dict | None = None
        if post_processing is not None:
            if not model_name:
                raise ValueError("`model_name` is required when `post_processing` is provided.")
            version_resp = self.add_application_version(
                application_id=application_id,
                project_id=project_id,
                model_id=checkpoint_id,
                model_name=model_name,
                post_processing=post_processing,
                runtime=runtime,
                fps_requirements=fps_requirements,
                model_type="pretrained",
                gpu_memory_mb=gpu_memory_mb,
                blog_link=blog_link,
                notebook_link=notebook_link,
                performance=performance,
                metrics=metrics,
                color_mapping=color_mapping,
                arch_checkpoints=arch_checkpoints,
            )

        # 7) Optionally flip status → published
        published = False
        if auto_publish:
            self.approve_application(application_id, status="published")
            published = True

        return {
            "project_id": project_id,
            "checkpoint_url": checkpoint_url,
            "checkpoint_id": checkpoint_id,
            "cover_image_url": resolved_cover_url,
            "application_id": application_id,
            "application_version": version_resp,
            "published": published,
        }


__all__ = ["AppIntegrator", "AppIntegrationError"]
