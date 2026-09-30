"""Auto-generated stub for module: applications_api."""
from typing import Any, Callable, Optional

from .models import Application
from .response import CallFailure, unwrap_platform
from .transport import LICENSE_KEY_HEADER, _describe, _rpc_data, _rpc_headed, _rpc_model, backend_base_url

# Classes
class ApplicationsApi:
    # ``AnalyticsClient.applications`` -- the application catalogue.
    #
    #     Args:
    #         session_provider: Called for the session to ride on each request. A callable rather
    #             than a session, so a client that rebuilds its session is followed rather than
    #             outrun.
    #         license_key_provider: Called for the deployment's licence key, or ``None`` when the
    #             caller has no licence to offer -- which is the same as holding an empty one and
    #             takes the unlicensed route. A callable for the same reason as the session: the
    #             answer is read at call time rather than frozen at construction.

    def __init__(self: Any, session_provider: Callable[[], Any], license_key_provider: Optional[Callable[[], str]] = None) -> None: ...

    APPLICATION: str
    USECASE_DOWNLOAD: str
    USECASE_DOWNLOAD_LICENSE: str

    def fetch_application(self: Any, application_id: str) -> Optional[Any]:
        """
        The catalogue entry for one application, or ``None`` if there is no such entry.
        
                Note that the record's own id field is spelled ``applicationid``, all lowercase, by
                the producer; the model carries the alias so callers read ``application_id``.
        
                This record knows the **published** version, which is routinely not the version a
                given deployment runs. A caller that wants the deployed one wants endpoint 2.
        
                Args:
                    application_id: The application to read.
        
                Returns:
                    The entry, or ``None`` when the platform reports no such application.
        
                Raises:
                    CallFailure: No base URL produced either an entry or an absence.
        """
        ...

    def mint_usecase_download(self: Any, application_id: str, application_version: str) -> str:
        """
        A fresh presigned URL for this version's usecase bundle.
        
                Minted on demand rather than read out of config: the URLs be-application issues live
                for five hours, and a deployment's config outlives that by design.
        
                Two routes answer this, and which one is used is not the caller's business -- see the
                module docstring. With a licence the licensed route is tried; without one it is not
                attempted at all and the unlicensed route answers.
        
                Args:
                    application_id: The application whose bundle is wanted.
                    application_version: The version of it.
        
                Returns:
                    The URL. Never ``""`` and never ``None`` -- a caller gets a usable URL or a failure
                    naming the application, not an absence to trip over later.
        
                Raises:
                    CallFailure: Neither route produced a URL. The message says which was tried and
                        distinguishes a version with no bundle attached from a rejected licence.
        """
        ...

