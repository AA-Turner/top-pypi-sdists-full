"""Routes answered by **be-inference**, reached through the local gateway.

be-inference answers five of the twenty-four endpoints in :mod:`.models` -- 2, 4, 5, 8 and 13
-- and all five belong to ``AnalyticsClient``. They are the only group in this package where
every route is **locally owned**: ``/v1/inference/`` is in
:data:`~.transport.LOCAL_AUTHORITY_PREFIXES`, so each call is tried against one base and never
retried against the cloud backend. :func:`~.transport._bases_for` says why that asymmetry
matters -- misrouting a cloud route as local costs the rescue attempt entirely, while
misrouting a local route as cloud costs one wasted call.

This group is also where the two shapes the rest of the package is built around actually turn
up, which is why it is the last of the three to be written:

* **endpoints 4 and 13 answer with an array**, so they validate through a ``TypeAdapter``
  rather than a model class. Both are declared at module level, because building one per call
  rebuilds the validator each time;
* **endpoint 5 is addressed by a query string** rather than by its path -- the only route of
  the twenty-four that is.

A collection route answers ``[]``, never ``None``
=================================================

Endpoints 4 and 13 return an empty list for *both* "this deployment has no configs" and "no
such deployment", which is what the call sites they replace already do. The distinction is
deliberately not preserved: no caller acts on it, and inventing an ``Optional[list[...]]``
would push a ``None`` check into every consumer to describe a case none of them handle
differently. The document routes keep ``None``, where absence genuinely is an answer a caller
reads.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional

from pydantic import TypeAdapter

from .models import ApplicationDeployment, Camera, CameraLocation, PostProcessingConfig
from .response import unwrap_platform
from .transport import _rpc_model

#: Built once. A ``TypeAdapter`` compiles a validator, and building it per call pays that cost
#: on every request for a route a container reads at startup for every camera it runs.
_CONFIG_LIST = TypeAdapter(List[PostProcessingConfig])
_CAMERA_LIST = TypeAdapter(List[Camera])


class InferenceApi:
    """``AnalyticsClient.inference`` -- deployments, post-processing configs, sites, cameras.

    Args:
        session_provider: Called for the session to ride on each request. A callable rather
            than a session, so a client that rebuilds its session is followed rather than
            outrun.
    """

    #: One deployment of one application, by deployment id.
    APPLICATION_DEPLOYMENT = "/v1/inference/get_application_deployment/{app_deployment_id}"

    #: Every camera's post-processing config for one deployment. Answers with an array.
    CONFIGS_BY_APP_DEPLOYMENT = (
        "/v1/inference/post_processing_configs/by_app_deployment/{app_deployment_id}"
    )

    #: The same document found the way the streaming UI finds it -- by camera and application,
    #: as a query string. The only route here not addressed by its path.
    CONFIG_BY_CAMERA_AND_APP = "/v1/inference/post_processing_config"

    #: The site a camera belongs to.
    LOCATION = "/v1/inference/get_location/{location_id}"

    #: Every camera on an account. Answers with an array.
    CAMERA_STREAMS_BY_ACCOUNT = "/v1/inference/get_camerastream_by_acc_number/{account_number}"

    def __init__(self, session_provider: Callable[[], Any]) -> None:
        self._session_provider = session_provider

    def fetch_application_deployment(
        self, app_deployment_id: str
    ) -> Optional[ApplicationDeployment]:
        """One deployment record, or ``None`` if there is no such deployment.

        This is the record that knows which application version a deployment actually
        **runs**, which is routinely not the version the catalogue calls published. A caller
        comparing the two wants this one and endpoint 3 together.

        Args:
            app_deployment_id: The deployment to read.

        Returns:
            The record, or ``None`` when the platform reports no such deployment.

        Raises:
            CallFailure: The call did not produce either a record or an absence.
        """
        return _rpc_model(
            self._session_provider(),
            self.APPLICATION_DEPLOYMENT.format(app_deployment_id=app_deployment_id),
            what=f"the deployment record for {app_deployment_id}",
            unwrap=unwrap_platform,
            validate=ApplicationDeployment.model_validate,
        )

    def fetch_post_processing_configs(self, app_deployment_id: str) -> List[PostProcessingConfig]:
        """Every camera's post-processing config for one deployment.

        Carries the ``zone_config`` the engine's zone primitives need. There is exactly one
        config per ``(camera, application)`` pair, so this is the deployment-shaped view of
        the same rows :meth:`fetch_post_processing_config` reads one at a time.

        Args:
            app_deployment_id: The deployment whose configs are wanted.

        Returns:
            The configs, or ``[]`` -- for a deployment with none *and* for a deployment that
            does not exist. An empty answer here is the signal to fall back to
            :meth:`fetch_post_processing_config`, which finds the same document by its other
            key; a stale ``_idAppDeployment`` is the usual reason.

        Raises:
            CallFailure: The call did not succeed.
        """
        configs = _rpc_model(
            self._session_provider(),
            self.CONFIGS_BY_APP_DEPLOYMENT.format(app_deployment_id=app_deployment_id),
            what=f"the post-processing configs for deployment {app_deployment_id}",
            unwrap=unwrap_platform,
            validate=_CONFIG_LIST.validate_python,
        )
        return [] if configs is None else configs

    def fetch_post_processing_config(
        self, camera_id: str, application_id: str
    ) -> Optional[PostProcessingConfig]:
        """One camera's post-processing config for one application, or ``None``.

        The fallback for :meth:`fetch_post_processing_configs`, and the key the streaming UI
        both writes and reads on -- so what comes back is by construction the polygon an
        operator can see drawn. Reaching for this means the stored ``_idAppDeployment`` does
        not name the deployment asking, which is a defect upstream that this works around.

        Args:
            camera_id: The camera.
            application_id: The application. Note this is the **application** id, not the
                deployment's -- that asymmetry is the producer's and is what makes the two
                keys onto one row disagree in the first place.

        Returns:
            The config, or ``None`` when the document does not exist -- a real answer, not an
            error, so a caller can tell "no zones" from "no reply".

        Raises:
            CallFailure: The call did not succeed.
        """
        return _rpc_model(
            self._session_provider(),
            self.CONFIG_BY_CAMERA_AND_APP,
            what=f"the post-processing config for camera {camera_id}",
            unwrap=unwrap_platform,
            validate=PostProcessingConfig.model_validate,
            params={"cameraId": camera_id, "applicationId": application_id},
        )

    def fetch_location(
        self, location_id: str, *, timeout_s: Optional[int] = None
    ) -> Optional[CameraLocation]:
        """The site a camera belongs to, or ``None`` if there is no such site.

        Callers holding a location id off another record should check it against
        :func:`~.models.normalise_location_id` first: the platform writes an all-zero
        ObjectId for an unset location rather than omitting the key, and asking for that
        placeholder is a round trip whose answer is already known.

        Args:
            location_id: The site to read.
            timeout_s: How long one attempt may take. A caller on a per-frame or
                per-batch path passes its own budget here, because the session's
                default allows two minutes and a site name is not worth stalling
                that long for. Absent, the session's default stands.

        Returns:
            The site, or ``None`` when the platform reports no such site.

        Raises:
            CallFailure: The call did not produce either a site or an absence.
        """
        return _rpc_model(
            self._session_provider(),
            self.LOCATION.format(location_id=location_id),
            what=f"the site record for location {location_id}",
            unwrap=unwrap_platform,
            validate=CameraLocation.model_validate,
            timeout_s=timeout_s,
        )

    def fetch_camera_streams(self, account_number: str) -> List[Camera]:
        """Every camera stream on one account.

        The route has no by-id form, so a caller wanting one camera asks for all of them and
        filters. That is the producer's shape, not a choice made here.

        Args:
            account_number: The account whose cameras are wanted.

        Returns:
            The cameras, or ``[]`` for an account with none and for an account that does not
            exist.

        Raises:
            CallFailure: The call did not succeed.
        """
        cameras = _rpc_model(
            self._session_provider(),
            self.CAMERA_STREAMS_BY_ACCOUNT.format(account_number=account_number),
            what=f"the camera streams for account {account_number}",
            unwrap=unwrap_platform,
            validate=_CAMERA_LIST.validate_python,
        )
        return [] if cameras is None else cameras


__all__ = ["InferenceApi"]
