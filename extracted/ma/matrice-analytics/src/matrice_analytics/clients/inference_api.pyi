"""Auto-generated stub for module: inference_api."""
from typing import Any, Callable, List, Optional

from .models import ApplicationDeployment, Camera, CameraLocation, PostProcessingConfig
from .response import unwrap_platform
from .transport import _rpc_model

# Classes
class InferenceApi:
    # ``AnalyticsClient.inference`` -- deployments, post-processing configs, sites, cameras.
    #
    #     Args:
    #         session_provider: Called for the session to ride on each request. A callable rather
    #             than a session, so a client that rebuilds its session is followed rather than
    #             outrun.

    def __init__(self: Any, session_provider: Callable[[], Any]) -> None: ...

    APPLICATION_DEPLOYMENT: str
    CAMERA_STREAMS_BY_ACCOUNT: str
    CONFIGS_BY_APP_DEPLOYMENT: str
    CONFIG_BY_CAMERA_AND_APP: str
    LOCATION: str

    def fetch_application_deployment(self: Any, app_deployment_id: str) -> Optional[Any]:
        """
        One deployment record, or ``None`` if there is no such deployment.
        
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
        ...

    def fetch_camera_streams(self: Any, account_number: str) -> List[Any]:
        """
        Every camera stream on one account.
        
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
        ...

    def fetch_location(self: Any, location_id: str) -> Optional[Any]:
        """
        The site a camera belongs to, or ``None`` if there is no such site.
        
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
        ...

    def fetch_post_processing_config(self: Any, camera_id: str, application_id: str) -> Optional[Any]:
        """
        One camera's post-processing config for one application, or ``None``.
        
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
        ...

    def fetch_post_processing_configs(self: Any, app_deployment_id: str) -> List[Any]:
        """
        Every camera's post-processing config for one deployment.
        
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
        ...

