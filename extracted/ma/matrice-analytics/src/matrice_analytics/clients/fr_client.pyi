"""Auto-generated stub for module: fr_client."""
from typing import Any, List, Optional

from .bootstrap import attach_session, get_action_id, get_action_record
from .identity import resolve_project_id, resolve_sidecar_base_url
from .models import FacialRecognitionServer, HealthStatus, PeopleActivityRequest, RedisDetails, ServiceShutdownRequest, ServiceShutdownResult, SimilarFaceMatch, SimilarFaceSearchRequest, StaffDetails, StaffEmbedding, StaffEnrollRequest, StaffEnrollResult, StaffImageUpdateRequest, StaffImageUpdateResult, UnknownPersonEnrollRequest, UnknownPersonEnrollResult
from .response import CallFailure, unwrap_fr_sidecar, unwrap_platform
from .transport import Uploader, _rpc_model, _rpc_sent, backend_base_url

# Constants
logger: Any

# Classes
class FRClient:
    # The facial-recognition sidecar and the two platform routes that find it.
    #
    #     Args:
    #         server_id: The sidecar's server id. A **constructor argument, never resolved** -- it
    #             arrives in the post-processing config, and there is no ``jobParams`` fallback for
    #             it. A client that resolved its own server id could silently attach to a different
    #             sidecar than the one the deployment configured.
    #         session: An open ``matrice_common`` session. Omit it and the client asks
    #             :func:`~.bootstrap.attach_session` for the process's own; on a machine with no SDK
    #             it constructs successfully and has no session, and every route refuses by name.
    #         project_id: The project the sidecar routes are scoped to. Omit it and it is read from
    #             the server record, which carries it as ``projectID``.
    #         public_ip: This machine's public address, if the caller has already looked it up. Used
    #             only to decide whether the sidecar is co-located -- see
    #             :func:`~.identity.resolve_sidecar_base_url`.
    #
    #     Attributes:
    #         server_id: The sidecar this client is attached to.
    #
    #     **Nothing here is cached except the server record.** That record describes where the
    #     sidecar is and which project it serves, and both are settled for the life of the
    #     deployment. Everything else -- a staff lookup, a health check, an embedding list -- can
    #     change under a running worker, so every call is a round trip.

    def __init__(self: Any, server_id: str, session: Any = None) -> None: ...

    DEPLOYMENT: str
    ENROLL_UNKNOWN: str
    HEALTH: str
    PEOPLE_ACTIVITY: str
    REDIS_DETAILS: str
    SEARCH_SIMILAR: str
    SERVER: str
    SHUTDOWN: str
    STAFF: str
    STAFF_EMBEDDINGS: str
    STAFF_ENROLL: str
    STAFF_IMAGES: str

    async def aclose(self: Any) -> None:
        """
        Close the upload pool. Call from the event loop that sent on it.
        
                Idempotent, and free on a client that never uploaded -- the pool opens no socket
                until the first send.
        """
        ...

    def base_url(self: Any) -> str:
        """
        Where the sidecar is, or ``""`` when no record says.
        
                Built from the server record's host and port. When that host is this machine's own,
                the loopback address reaches the same service without leaving the box -- see
                :func:`~.identity.resolve_sidecar_base_url`.
        
                The retired local client defaulted both halves -- ``host or "localhost"`` and
                ``port or 8081`` -- and only one of those survives, because the two are not the
                same case.
        
                **No host gets no address.** Defaulting it would undo the refusal the routes rely
                on: without a base the request goes to the session's default host, is refused as
                unauthorised, and reads as a credentials problem three frames from the missing
                server record that caused it. A blank address makes the route name the missing
                host instead.
        
                **No port gets 8081.** ``port`` is an ``int`` defaulting to ``0``, so a record
                that names a host and no port would otherwise build ``http://host:0``, which is
                not an address at all -- it fails to connect rather than refusing, and says
                nothing about why.
        """
        ...

    def connect(self: Any) -> Optional[Any]:
        """
        Read the server record, and with it the sidecar's address and project.
        
                **Idempotent, and worth calling explicitly at startup.** The sidecar routes need this
                record, so one of them will read it if nothing else has -- but that read is a blocking
                GET, and the face-match path runs it per detection. Calling this once while the
                container is starting keeps the round trip off the frame loop; calling it again costs
                nothing.
        
                This is not done in ``__init__`` on purpose. A constructor that opens a socket cannot
                be built in a test, a dry run, or a container that will never reach the platform, and
                the three clients in this package share the property that **construction never fails**.
        
                Returns:
                    The record, or ``None`` when the platform reports no such server -- which is an
                    answer, not a failure, and leaves the sidecar routes without an address.
                    **An empty document counts as no such server.** ``{"success": true,
                    "data": {}}`` unwraps to ``{}``, which is falsy, and validates into a record of
                    blank fields, which is not; taken at face value this client would believe it
                    had a server and build ``http://localhost:8081`` out of the defaults.
        
                Guarded by :attr:`_lock`, because one client is shared by callers on different
                threads -- the activity logger and the embedding refresher each run their own. A
                second caller arriving while the GET is in flight waits for it and reads the same
                record, rather than issuing its own.
        
                Raises:
                    CallFailure: There is no session, or the read did not succeed.
        """
        ...

    async def enroll_staff(self: Any, request: Any) -> Optional[Any]:
        """
        Enrol a staff member from the images on ``request``.
        
                Sent **once**. An enrolment retried on a slow reply is a second staff record.
        
                Args:
                    request: The staff details and their base64 images.
        
                Returns:
                    The enrolment result, or ``None`` when the sidecar answers with no payload.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    async def enroll_staff_from_paths(self: Any, request: Any, image_paths: Any[str]) -> Optional[Any]:
        """
        Enrol a staff member from image files on this host's disk.
        
                :meth:`enroll_staff` takes a request whose ``images`` are already base64; this
                reads the files and produces them. The caller keeps whatever ``images`` the
                request already carried -- the ones read here are appended, so a request built
                from both sources sends both.
        
                Args:
                    request: The staff details. Its ``images`` are not modified.
                    image_paths: Paths to read, enrolled **in the order given**. The sidecar
                        keeps that order, and the first image is the one it treats as primary.
        
                Returns:
                    Whatever :meth:`enroll_staff` returns.
        
                Raises:
                    OSError: A path could not be read. Nothing is sent -- an enrolment missing
                        one of its faces is worse than one that did not happen, so the read is
                        completed before the call rather than streamed into it.
                    CallFailure: There is no session or no sidecar address, or the call failed.
        
                The reads run on a worker thread. They are blocking file I/O on a path that the
                caller may be driving from an event loop, and a few megabytes of JPEG is long
                enough to matter to anything else sharing it.
        """
        ...

    async def enroll_unknown_person(self: Any, request: Any) -> Optional[Any]:
        """
        Enrol a face the sidecar has seen but cannot name.
        
                Args:
                    request: The face to enrol.
        
                Returns:
                    The result, or ``None`` when the sidecar answers with no payload.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    async def fetch_health(self: Any) -> Optional[Any]:
        """
        Whether the sidecar considers itself healthy.
        
                **Sent with the server id but no project.** That is the route's own shape, not an
                oversight: a health check asks about the service, and scoping it to a project would
                ask a question the service does not have.
        
                Returns:
                    The status, or ``None`` when the sidecar answers with no payload.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    async def fetch_redis_details(self: Any) -> Optional[Any]:
        """
        The Redis the sidecar publishes its matches to.
        
                **The one sidecar route with no query string at all.** There is one Redis per sidecar,
                so neither the project nor the server id narrows the answer.
        
                Returns:
                    The details, or ``None`` when the sidecar answers with no payload.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    def fetch_server(self: Any) -> Optional[Any]:
        """
        The sidecar's server record, read fresh.
        
                ``fetch_``, so this is a round trip every time -- unlike :meth:`connect`, which
                answers from the record it holds. Use this to see the record's current state; use
                :meth:`connect` to get the one this client is actually calling on.
        """
        ...

    async def fetch_staff(self: Any, staff_id: str) -> Optional[Any]:
        """
        One staff member's record, or ``None`` if the sidecar has no such staff.
        
                Args:
                    staff_id: The staff member to read.
        
                Returns:
                    The record, or ``None``. Absence is an answer on this route.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    async def fetch_staff_embeddings(self: Any) -> List[Any]:
        """
        Every enrolled face the sidecar holds.
        
                Returns:
                    The embeddings, or ``[]`` when there are none. An empty list and a missing answer
                    are the same thing on this route -- a sidecar with nothing enrolled yet.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    def project_id(self: Any) -> str:
        """
        The project the sidecar routes are scoped to.
        
                The constructor argument if one was given, otherwise the ``projectID`` on the server
                record. Reading the record is what makes this a property rather than a stored value:
                a client built before :meth:`connect` would have captured ``""``.
        
                A blank answer is reported once, here, rather than at each of the eight routes that
                interpolate it -- eight identical warnings for one missing value is how a log stops
                being read.
        
                Once means once per server record. This is a property, so each of those eight routes
                re-reads it, and ``store_people_activity`` runs per recognised face -- without the
                flag the warning would be emitted per call. :meth:`refresh` clears the flag along
                with the record, so a server that still has no ``projectID`` is reported again.
        """
        ...

    def refresh(self: Any) -> Optional[Any]:
        """
        Read the server record again, discarding the one held.
        
                For a sidecar that has been redeployed to a different host under a running worker.
                Nothing calls this automatically: a client that re-read the record on every failure
                would turn one unreachable sidecar into two round trips per call.
        
                Discards the held record and re-reads as one locked step. A concurrent
                :meth:`connect` can therefore never store its record in the gap between the two,
                which would leave this client holding ``None`` and unable to read again.
        
                Also drops the action-record project, so a lookup that failed against an
                unreachable platform is attempted again rather than held as ``""`` for the life of
                the client. The record itself does not change; the read of it can fail.
        """
        ...

    def rpc(self: Any) -> Any:
        """
        The session's RPC handle, read fresh on every access.
        
                Not cached, and the distinction is not academic: ``session.update()`` replaces the
                session's RPC and shuts the previous one down, so a handle held from construction
                works until the first re-authentication and then silently stops.
        
                Raises:
                    CallFailure: There is no session.
        """
        ...

    async def search_similar_faces(self: Any, request: Any) -> List[Any]:
        """
        Faces the sidecar considers similar to the one on ``request``.
        
                Args:
                    request: The query face and how many matches to return.
        
                Returns:
                    The matches, **ordered as the sidecar ordered them** -- that order is the ranking
                    and re-sorting it here would discard the answer. An empty list means no match was
                    found, which is a result and not an absence.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    def session(self: Any) -> Any:
        """
        The session this client calls on, or ``None`` when the SDK is absent.
        """
        ...

    async def shutdown(self: Any, request: Optional[Any] = None) -> Optional[Any]:
        """
        Ask the sidecar to shut down.
        
                Sent once, which matters more here than anywhere else on this client: a retried
                shutdown can reach a sidecar that has already restarted and stop it again.
        
                Args:
                    request: What to shut down. Omit it for the sidecar's own default.
        
                Returns:
                    The result, or ``None`` when the sidecar answers with no payload -- which a
                    service being asked to stop quite reasonably does.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    async def store_people_activity(self: Any, request: Any) -> str:
        """
        Record one person's activity against a camera, and get back where the frame went.
        
                **The one route of the twenty-four that answers with no envelope.** It returns a bare
                JSON string -- the media URL it stored the frame at -- rather than the
                ``{success, data}`` shape every other route uses. That is why
                :func:`~.response.unwrap_fr_sidecar` treats a reply as an envelope only when it is a
                mapping that actually carries ``success``, and it is the single behaviour separating
                that unwrap from :func:`~.response.unwrap_platform`.
        
                Args:
                    request: The activity to store.
        
                Returns:
                    The media URL, or ``""`` when no frame was available. **``""`` is a successful
                    result on this route, not a missing one** -- an activity recorded without a frame
                    is still recorded, and a caller that treats the blank as a failure will retry a
                    write that already landed.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    async def update_deployment(self: Any, deployment_id: str) -> Optional[Any]:
        """
        Mark which deployment this facial-recognition server is running.
        
                A platform route, so it goes to the backend rather than the sidecar -- and to the
                backend **this deployment's environment names**, derived by
                :func:`~.transport.backend_base_url`. The existing call site names prod in a string
                literal, which is why a staging node has been updating production records.
        
                Args:
                    deployment_id: The deployment to record against this server.
        
                Returns:
                    The updated record, or ``None`` when the platform reports no such server.
        
                Raises:
                    CallFailure: There is no session, ``deployment_id`` is blank, or the call failed.
        """
        ...

    async def update_staff_images(self: Any, request: Any) -> Optional[Any]:
        """
        Replace the images held for a staff member.
        
                Args:
                    request: The staff member and their new images.
        
                Returns:
                    The result, or ``None`` when the sidecar answers with no payload.
        
                Raises:
                    CallFailure: There is no session or no sidecar address, or the call failed.
        """
        ...

    async def upload_frame(self: Any, upload_url: str, image_bytes: Any) -> bool:
        """
        Put a frame at the storage address :meth:`store_people_activity` handed back.
        
                The second half of a **two-step write the producer defines**: recording an
                activity answers with the media URL it resolved, and the frame goes there. It is
                not a route on the sidecar -- the URL is pre-signed and carries its own
                credentials -- which is why it takes a URL rather than building one, and why no
                session or ``Authorization`` header is involved.
        
                Args:
                    upload_url: The address ``store_people_activity`` returned.
                    image_bytes: The encoded frame.
                    content_type: What the bytes are. JPEG unless the caller says otherwise.
        
                Returns:
                    ``True`` when the store accepted it. ``False`` for every failure, logged
                    where it happened -- a frame that did not reach storage is a lost frame, and
                    the caller has another one along in milliseconds.
        
                Sent over a kept-alive pool. Call :meth:`aclose` from the loop that sent on it.
        """
        ...

