"""Auto-generated stub for module: lpr_client."""
from typing import Any, Optional

from .bootstrap import attach_session
from .identity import resolve_sidecar_base_url
from .models import CreateDetectionRequest, Detection, LprServer
from .response import CallFailure, unwrap_lpr_server, unwrap_platform
from .transport import POOLED_POST_TIMEOUT_S, PooledPoster, _rpc_model

# Constants
logger: Any

# Classes
class LPRClient:
    # The licence-plate server and the platform route that finds it.
    #
    #     Args:
    #         lpr_server_id: The server's id. A **constructor argument, never resolved** -- it
    #             arrives in the post-processing config, and the usecase has defined behaviour when
    #             it is absent. A client that resolved its own would attach to whichever server it
    #             happened to find rather than the one the deployment configured.
    #         session: An open ``matrice_common`` session. Omit it and the client asks
    #             :func:`~.bootstrap.attach_session` for the process's own; on a machine with no SDK
    #             it constructs successfully and has no session, and both routes refuse by name.
    #         project_id: The project detections are filed under. Omit it and it is read from the
    #             server record, which carries it as ``projectID``.
    #         public_ip: This machine's public address, if the caller has already looked it up.
    #
    #     Attributes:
    #         lpr_server_id: The server this client is attached to.
    #
    #     **This client's project is its own source, not a shared one.** It comes off the server
    #     record as ``projectID`` and is scoped to that server.
    #     :func:`~.identity.resolve_project_id` answers a different question -- which project this
    #     *worker* belongs to, from the action record -- and the two are not interchangeable.
    #
    #     **So this client does not read the launch action record for its project, and that is
    #     deliberate rather than an omission.** :class:`~.fr_client.FRClient` does, because the
    #     client it replaced did; the shipped licence-plate path never has. Its project has always
    #     come from the lpr-server record, and the action record it *does* read -- for the alert
    #     manager's server and deployment ids -- has never been a project source here. Adding the
    #     fallback to match the sibling would file detections under the project the launch record
    #     names whenever the two disagree, which is a change no caller has asked for.

    def __init__(self: Any, lpr_server_id: str, session: Any = None) -> None: ...

    DETECTIONS: str
    SERVER: str

    async def aclose(self: Any) -> None:
        """
        Close the detection pool. Call from the event loop that sent on it.
        
                Idempotent, and free on a client that never filed a detection -- the pool opens no
                socket until the first send.
        """
        ...

    def base_url(self: Any) -> str:
        """
        Where the lpr-server is, or ``""`` when no record says.
        
                Built from the record's host and port by the same policy the facial-recognition
                sidecar uses -- see :func:`~.identity.resolve_sidecar_base_url`.
        """
        ...

    def connect(self: Any) -> Optional[Any]:
        """
        Read the server record, and with it the server's address and project.
        
                Idempotent, and worth calling at startup: the detection route needs this record, so
                one of those calls will read it if nothing else has -- and that read is a blocking GET
                on a path that runs per detection. Calling it again costs nothing.
        
                Not done in ``__init__`` on purpose: a constructor that opens a socket cannot be built
                in a test, a dry run, or a container that will never reach the platform, and the three
                clients in this package share the property that **construction never fails**.
        
                Returns:
                    The record, or ``None`` when the platform reports no such server.
        
                Guarded by :attr:`_lock`. A second caller arriving while the GET is in flight waits
                for it and reads the same record, rather than issuing its own.
        
                Raises:
                    CallFailure: There is no session, or the read did not succeed.
        """
        ...

    async def create_detection(self: Any, request: Any) -> Optional[Any]:
        """
        File a plate sighting, or add a frame to the sighting that already exists.
        
                One route does both. Where the plate already has a detection for this project and
                team, lpr-server resolves it, stores the new frame and appends the frame id to the
                existing document -- it does **not** insert a second detection. So a caller with a
                plate it has already sent still calls this, and does not need to know which of the two
                happened.
        
                Sent once. The route is idempotent, so a retry would be safe; it would not be free,
                and this path runs per detection.
        
                Args:
                    request: The sighting. Six of its fields are producer-required -- ``projectId``,
                        ``licensePlate``, ``frameId``, ``cameraId``, ``applicationId`` and
                        ``rtpNumber`` -- and the model coerces a numeric frame id to the string the
                        producer's Go struct declares, which is what stops a sighting being lost to
                        ``cannot unmarshal number into ... frameId of type string``.
        
                Returns:
                    The created or updated document, or ``None`` when the server answers with no body.
        
                Raises:
                    RateLimited: lpr-server answered 429. Carries ``Retry-After`` when it sent one.
                        **Reported, never slept on** -- a caller holding a queue of sightings is the
                        only thing that knows whether this one still matters once the wait is over.
                    ConnectionLost: Two connection attempts failed in a row, so nothing was sent.
                    CallFailure: There is no session, no server address, or the write did not succeed.
        
                Sent over a **kept-alive pool**, not a fresh connection per call: this runs per
                detection, and ``rpc.async_send_request`` opens and closes a session inside every
                request. See :class:`~.transport.PooledPoster`, which also owns the reconnect on a
                keep-alive the server had already closed.
        """
        ...

    def fetch_server(self: Any) -> Optional[Any]:
        """
        The server record, read fresh.
        
                ``fetch_``, so this is a round trip every time -- unlike :meth:`connect`, which
                answers from the record it holds.
        """
        ...

    def project_id(self: Any) -> str:
        """
        The project detections are filed under.
        
                The constructor argument if one was given, otherwise the ``projectID`` on the server
                record. A property rather than a stored value because a client built before
                :meth:`connect` would have captured ``""``.
        
                The producer **requires** this field, so a blank one is reported: the detection would
                be rejected rather than misfiled.
        
                Warns once per server record, not once per call. ``create_detection`` reads this
                property on every sighting, so warning on each read would emit one line per
                detection. :meth:`refresh` clears the flag along with the record, so a server that
                still has no ``projectID`` on the next read is reported again.
        """
        ...

    def refresh(self: Any) -> Optional[Any]:
        """
        Read the server record again, discarding the one held.
        
                For a server that has been redeployed to a different host under a running worker.
                Nothing calls this automatically: re-reading on every failure would turn one
                unreachable server into two round trips per detection.
        
                Discards the held record and re-reads as one locked step. A concurrent
                :meth:`connect` can therefore never store its record in the gap between the two,
                which would leave this client holding ``None`` and unable to read again.
        """
        ...

    def rpc(self: Any) -> Any:
        """
        The session's RPC handle, read fresh on every access.
        
                Not cached: ``session.update()`` replaces the session's RPC and shuts the previous one
                down, so a handle held from construction works until the first re-authentication and
                then silently stops.
        
                Raises:
                    CallFailure: There is no session.
        """
        ...

    def session(self: Any) -> Any:
        """
        The session this client calls on, or ``None`` when the SDK is absent.
        """
        ...

