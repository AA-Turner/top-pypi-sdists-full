"""The facial-recognition client: two platform routes and nine on a sidecar.

Eleven routes, and the split inside them is the thing to understand first.

**Two of the eleven are platform routes** -- ``/v1/actions/get_facial_recognition_server``
and ``/v1/actions/update_facial_recognition_deployment``. They are ``/v1/actions/`` by prefix,
which is :class:`~.analytics_client.AnalyticsClient`'s territory, and FR's by **ownership**:
both are keyed by ``server_id``, which only this client holds. A route belongs to the client
that owns the id it is keyed by. Moving these two into ``AnalyticsClient`` would mean passing
``server_id`` into a client whose stated property is *"needs no project"* -- exactly the
coupling the three-way split exists to avoid.

**The other nine go to the sidecar**, at an address this client learns from the first of those
two routes. You use the platform to find the sidecar, so a sidecar lookup cannot come from the
sidecar.

Why every sidecar call is one attempt
=====================================

The platform routes in this package get a two-base retry, because a deployment's local gateway
302s cloud-only routes out and httpx drops the ``Authorization`` header across the origin
change. **None of that applies here.** A sidecar has exactly one host, learned from its own
server record; retrying its route against the platform asks a service that has never heard of
it. And these routes **enroll, store, update, and shut down** -- a retry turns one enrolment
into two. So the sidecar calls go through :func:`~.transport._rpc_sent`, which sends once.

The two platform routes differ from each other, too
===================================================

Endpoint 10 is a plain GET and rides the same two-base helper every other platform read in
this package uses. Endpoint 12 is an async PUT, so it sends once and must name its base --
and it names :func:`~.transport.backend_base_url`, which derives the stage from the
environment. The existing call site hardcodes ``https://prod.backend.app.matrice.ai``, so a
dev or staging node updates a **production** deployment record; that call site is not this
ticket's to change, but the path built here does not have the defect to begin with.

Unwrap is bound per route, never per client
===========================================

Nine routes here answer with the sidecar's envelope and two with the platform's, so a client
that bound one unwrap for all eleven would be wrong twice. The two forms are **identical on a
successful reply** -- both hand back ``data`` -- and diverge only on a reply carrying no
envelope, which the sidecar form accepts as the payload itself because one of its routes
genuinely answers that way. Bound the wrong way round, a malformed platform reply validates
into a record of blank fields instead of raising.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import threading
from pathlib import Path
from typing import Any, List, Optional, Sequence
from urllib.parse import urlencode

from pydantic import TypeAdapter

from .bootstrap import attach_session, get_action_id, get_action_record
from .identity import resolve_project_id, resolve_sidecar_base_url
from .models import (
    FacialRecognitionServer,
    HealthStatus,
    PeopleActivityRequest,
    ServiceShutdownRequest,
    ServiceShutdownResult,
    SimilarFaceMatch,
    SimilarFaceSearchRequest,
    StaffDetails,
    StaffEmbedding,
    StaffEnrollRequest,
    StaffEnrollResult,
    StaffImageUpdateRequest,
    StaffImageUpdateResult,
    UnknownPersonEnrollRequest,
    UnknownPersonEnrollResult,
)
from .response import CallFailure, unwrap_fr_sidecar, unwrap_platform
from .transport import Uploader, _rpc_model, _rpc_sent, backend_base_url

logger = logging.getLogger(__name__)

#: Built once at import rather than per call. A ``TypeAdapter`` compiles a validator on
#: construction, and **endpoint 15** -- the similarity search -- is read per detection.
#: Measured 2026-09-21 at 23 us prebuilt against 137 us built per call, twenty matches.
#: Endpoint 20 is the opposite case: its list is loaded once into the matcher's matrix, not
#: per frame, and it shares the hoisting only because there is no reason not to.
_MATCH_LIST = TypeAdapter(List[SimilarFaceMatch])
_EMBEDDING_LIST = TypeAdapter(List[StaffEmbedding])


def _media_url(value: Any) -> str:
    """The media URL from endpoint 17's reply, or a named failure.

    Endpoint 17 is the one route that answers with a bare JSON string rather than an
    envelope: the URL the frame was stored at, or ``""`` when no frame was available. A
    blank is a successful result and is returned as-is.

    Anything that is not a string means the reply shape has changed, and is reported. Plain
    ``str()`` would render a dict as ``"{'url': '...'}"`` and hand it back as though it were
    the URL, and nothing further down would notice.
    """
    if isinstance(value, str):
        return value
    raise CallFailure(
        f"store_people_activity expected the media URL as a JSON string but the sidecar "
        f"answered with {type(value).__name__}. The route's reply shape has changed; it is "
        f"the one route that sends a bare body rather than an envelope."
    )


class FRClient:
    """The facial-recognition sidecar and the two platform routes that find it.

    Args:
        server_id: The sidecar's server id. A **constructor argument, never resolved** -- it
            arrives in the post-processing config, and there is no ``jobParams`` fallback for
            it. A client that resolved its own server id could silently attach to a different
            sidecar than the one the deployment configured.
        session: An open ``matrice_common`` session. Omit it and the client asks
            :func:`~.bootstrap.attach_session` for the process's own; on a machine with no SDK
            it constructs successfully and has no session, and every route refuses by name.
        project_id: The project the sidecar routes are scoped to. Omit it and it is read from
            the server record, which carries it as ``projectID``.
        public_ip: This machine's public address, if the caller has already looked it up. Used
            only to decide whether the sidecar is co-located -- see
            :func:`~.identity.resolve_sidecar_base_url`.

    Attributes:
        server_id: The sidecar this client is attached to.

    **Nothing here is cached except the server record.** That record describes where the
    sidecar is and which project it serves, and both are settled for the life of the
    deployment. Everything else -- a staff lookup, a health check, an embedding list -- can
    change under a running worker, so every call is a round trip.
    """

    #: Platform. Read for the sidecar's address and project.
    SERVER = "/v1/actions/get_facial_recognition_server/{server_id}"
    #: Platform. Marks the deployment this worker is running.
    DEPLOYMENT = "/v1/actions/update_facial_recognition_deployment/{server_id}"

    STAFF_ENROLL = "/v1/facial_recognition/staff/enroll"
    SEARCH_SIMILAR = "/v1/facial_recognition/search/similar"
    STAFF = "/v1/facial_recognition/staff/{staff_id}"
    PEOPLE_ACTIVITY = "/v1/facial_recognition/store_people_activity"
    STAFF_IMAGES = "/v1/facial_recognition/staff/update_images"
    SHUTDOWN = "/v1/facial_recognition/shutdown"
    STAFF_EMBEDDINGS = "/v1/facial_recognition/get_all_staff_embeddings"
    ENROLL_UNKNOWN = "/v1/facial_recognition/enroll_unknown_person"
    HEALTH = "/v1/facial_recognition/health"

    def __init__(
        self,
        server_id: str,
        session: Any = None,
        *,
        project_id: str = "",
        public_ip: str = "",
    ) -> None:
        self.server_id = server_id
        self._session = attach_session(
            session, what=f"the facial-recognition client for server {server_id}"
        )
        self._public_ip = public_ip
        self._given_project_id = project_id
        self._server: Optional[FacialRecognitionServer] = None
        self._connected = False
        self._warned_no_project = False
        #: The project taken from the launch action record, or ``""`` when there is none.
        #: ``None`` means "not looked up yet". Memoised per client because
        #: :attr:`project_id` is a property read by every scoped route and, through
        #: ``store_people_activity``, once per recognised face -- and resolving the action
        #: id can walk the filesystem. The record describes a launch that has already
        #: happened, so unlike the server record it cannot change under a running worker.
        self._action_project: Optional[str] = None
        #: Guards the three fields above, which are read and written together. One client is
        #: shared across threads here: ``face_recognition`` hands the same instance to the
        #: activity logger and to the embedding refresher, and each runs its own. Reentrant
        #: because :meth:`refresh` holds it and calls :meth:`connect`, which takes it again.
        self._lock = threading.RLock()
        #: The frame-upload pool. Holds no socket until the first upload, so a client
        #: built for reads, a test or a dry run never opens one and never needs closing.
        self._uploader = Uploader()

    # ---- session and connection -------------------------------------------------------

    @property
    def session(self) -> Any:
        """The session this client calls on, or ``None`` when the SDK is absent."""
        return self._session

    @property
    def rpc(self) -> Any:
        """The session's RPC handle, read fresh on every access.

        Not cached, and the distinction is not academic: ``session.update()`` replaces the
        session's RPC and shuts the previous one down, so a handle held from construction
        works until the first re-authentication and then silently stops.

        Raises:
            CallFailure: There is no session.
        """
        return self._require_session().rpc

    def _require_session(self) -> Any:
        """The session, or a named refusal.

        Raises:
            CallFailure: There is no session; the SDK was absent when this client was built.
        """
        if self._session is None:
            raise CallFailure(
                f"The facial-recognition client for server {self.server_id} has no session, "
                "so it cannot reach the platform or its sidecar. matrice_common was not "
                "importable when it was built."
            )
        return self._session

    def connect(self) -> Optional[FacialRecognitionServer]:
        """Read the server record, and with it the sidecar's address and project.

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
        if not self.server_id:
            # The route interpolates the id, so a blank one asks the platform for
            # ``/v1/actions/get_facial_recognition_server/`` -- a different route, which
            # answers about nothing. Refusing here costs a comparison; asking costs a
            # round trip and returns an answer that reads like a record.
            return None

        with self._lock:
            if not self._connected:
                record = _rpc_model(
                    self._require_session(),
                    self.SERVER.format(server_id=self.server_id),
                    what=f"the facial-recognition server record for {self.server_id}",
                    unwrap=unwrap_platform,
                    validate=FacialRecognitionServer.model_validate,
                )
                if record is not None and not record.model_dump(
                    by_alias=True, exclude_defaults=True
                ):
                    logger.warning(
                        "The server record for %s is an empty document; treating it as no "
                        "such server rather than as a sidecar at the default address",
                        self.server_id,
                    )
                    record = None
                self._server = record
                self._connected = True
            return self._server

    def refresh(self) -> Optional[FacialRecognitionServer]:
        """Read the server record again, discarding the one held.

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
        with self._lock:
            self._connected = False
            self._server = None
            self._warned_no_project = False
            self._action_project = None
            return self.connect()

    @property
    def project_id(self) -> str:
        """The project the sidecar routes are scoped to.

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
        if self._given_project_id:
            return self._given_project_id

        # The action record first, and only then the server record -- the shipped order.
        # Asking the sidecar first would also make this project depend on that read
        # succeeding, and the two failures are unrelated: a server record that cannot be
        # read says nothing about the launch record that named this worker's project.
        found = self._project_from_action_record()
        if not found:
            record = self.connect()
            found = "" if record is None else record.project_id
        if not found and not self._warned_no_project:
            self._warned_no_project = True
            logger.warning(
                "No project id for the facial-recognition client on server %s: none was "
                "passed, the launch action record named none, and the server record carries "
                "no projectID. The eight sidecar routes scoped to a project will be sent "
                "without one.",
                self.server_id,
            )
        return found

    def _project_from_action_record(self) -> str:
        """The project on the action record this container was launched with.

        The middle of three sources, and the order is the shipped one: the project passed
        in, then this, then the sidecar's own server record. It is a fallback rather than a
        preference -- it runs only when nothing was passed -- but it runs *before* the
        server record, because the two can name different projects and the launch record is
        what the platform scoped this worker to.

        Warning:
            Empty on a decoupled deployment, and that is the correct answer there rather
            than a fault. BYOM decides whether analytics runs in the same container as
            inference -- coupled, launched from a ``deploy_add`` record that carries
            ``_idProject`` at its root -- or in its own, from a ``deploy_postproc`` record
            that carries none. Facial recognition is coupled-only today, so the field is
            present as a *consequence* of that choice, not as a guarantee of the record.
            A blank here falls through to the server record, which is unaffected either way.

        Returns:
            The project id, or ``""`` when there is no action id, the record cannot be
            read, or it carries no ``_idProject``. Each of those is survivable: the next
            source is tried, and a worker with no project at all still starts.
        """
        if self._action_project is not None:
            return self._action_project

        self._action_project = ""
        action_id = get_action_id()
        if not action_id:
            return self._action_project

        try:
            record = get_action_record(action_id, session=self._require_session())
        except CallFailure as exc:
            # A worker that cannot reach the platform still starts; the server record is
            # the next source and comes from the sidecar rather than from here.
            logger.warning("Could not read action record %s for its project: %s", action_id, exc)
            return self._action_project

        self._action_project = resolve_project_id(lambda: record)
        return self._action_project

    @property
    def base_url(self) -> str:
        """Where the sidecar is, or ``""`` when no record says.

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
        record = self.connect()
        if record is None:
            return ""
        return resolve_sidecar_base_url(record.host, record.port or 8081, public_ip=self._public_ip)

    def _require_base_url(self) -> str:
        """The sidecar's address, or a named refusal.

        Raises:
            CallFailure: No server record, or one carrying no host. Refusing here is what
                stops a sidecar call being sent to whatever the session's default base is --
                which would reach the platform, be refused as unauthorised, and read as a
                credentials problem rather than a missing server record.
        """
        base = self.base_url
        if not base:
            raise CallFailure(
                f"No address for the facial-recognition sidecar on server {self.server_id}: "
                "its server record is missing or carries no host, so there is nowhere to "
                "send this request."
            )
        return base

    def _scoped(self, path: str) -> str:
        """``path`` with the project and server the sidecar expects.

        The query is **encoded**, not interpolated. The existing call sites build it with an
        f-string, which is correct for the hex ids these actually are and silently produces a
        malformed query for anything else.
        """
        return f"{path}?{urlencode({'projectId': self.project_id, 'serverID': self.server_id})}"

    # ---- endpoint 10 ------------------------------------------------------------------

    def fetch_server(self) -> Optional[FacialRecognitionServer]:
        """The sidecar's server record, read fresh.

        ``fetch_``, so this is a round trip every time -- unlike :meth:`connect`, which
        answers from the record it holds. Use this to see the record's current state; use
        :meth:`connect` to get the one this client is actually calling on.
        """
        return _rpc_model(
            self._require_session(),
            self.SERVER.format(server_id=self.server_id),
            what=f"the facial-recognition server record for {self.server_id}",
            unwrap=unwrap_platform,
            validate=FacialRecognitionServer.model_validate,
        )

    # ---- endpoint 12 ------------------------------------------------------------------

    async def update_deployment(self, deployment_id: str) -> Optional[FacialRecognitionServer]:
        """Mark which deployment this facial-recognition server is running.

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
        if not deployment_id:
            raise CallFailure(
                f"Cannot update the deployment for server {self.server_id}: no deployment id. "
                "Sending a blank one would clear the record rather than leave it alone."
            )

        path = self.DEPLOYMENT.format(server_id=self.server_id)
        return await _rpc_sent(
            self._require_session(),
            "PUT",
            f"{path}?{urlencode({'app_deployment_id': deployment_id})}",
            what=f"the deployment update for facial-recognition server {self.server_id}",
            unwrap=unwrap_platform,
            validate=FacialRecognitionServer.model_validate,
            base_url=backend_base_url(),
            payload={},
        )

    # ---- endpoints 14-23, on the sidecar ----------------------------------------------

    async def enroll_staff(self, request: StaffEnrollRequest) -> Optional[StaffEnrollResult]:
        """Enrol a staff member from the images on ``request``.

        Sent **once**. An enrolment retried on a slow reply is a second staff record.

        Args:
            request: The staff details and their base64 images.

        Returns:
            The enrolment result, or ``None`` when the sidecar answers with no payload.

        Raises:
            CallFailure: There is no session or no sidecar address, or the call failed.
        """
        return await _rpc_sent(
            self._require_session(),
            "POST",
            self._scoped(self.STAFF_ENROLL),
            what=f"enrolling staff on server {self.server_id}",
            unwrap=unwrap_fr_sidecar,
            validate=StaffEnrollResult.model_validate,
            base_url=self._require_base_url(),
            payload=request.model_dump(by_alias=True, exclude_none=True),
        )

    async def enroll_staff_from_paths(
        self, request: StaffEnrollRequest, image_paths: Sequence[str]
    ) -> Optional[StaffEnrollResult]:
        """Enrol a staff member from image files on this host's disk.

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
        loaded = [
            base64.b64encode(raw).decode("utf-8")
            for raw in await asyncio.gather(
                *(asyncio.to_thread(Path(p).read_bytes) for p in image_paths)
            )
        ]
        return await self.enroll_staff(
            request.model_copy(update={"images": [*request.images, *loaded]})
        )

    async def search_similar_faces(
        self, request: SimilarFaceSearchRequest
    ) -> List[SimilarFaceMatch]:
        """Faces the sidecar considers similar to the one on ``request``.

        Args:
            request: The query face and how many matches to return.

        Returns:
            The matches, **ordered as the sidecar ordered them** -- that order is the ranking
            and re-sorting it here would discard the answer. An empty list means no match was
            found, which is a result and not an absence.

        Raises:
            CallFailure: There is no session or no sidecar address, or the call failed.
        """
        matches = await _rpc_sent(
            self._require_session(),
            "POST",
            self._scoped(self.SEARCH_SIMILAR),
            what=f"searching for similar faces on server {self.server_id}",
            unwrap=unwrap_fr_sidecar,
            validate=_MATCH_LIST.validate_python,
            base_url=self._require_base_url(),
            payload=request.model_dump(by_alias=True, exclude_none=True),
        )
        return [] if matches is None else matches

    async def fetch_staff(self, staff_id: str) -> Optional[StaffDetails]:
        """One staff member's record, or ``None`` if the sidecar has no such staff.

        Args:
            staff_id: The staff member to read.

        Returns:
            The record, or ``None``. Absence is an answer on this route.

        Raises:
            CallFailure: There is no session or no sidecar address, or the call failed.
        """
        return await _rpc_sent(
            self._require_session(),
            "GET",
            self._scoped(self.STAFF.format(staff_id=staff_id)),
            what=f"the staff record for {staff_id} on server {self.server_id}",
            unwrap=unwrap_fr_sidecar,
            validate=StaffDetails.model_validate,
            base_url=self._require_base_url(),
        )

    async def store_people_activity(self, request: PeopleActivityRequest) -> str:
        """Record one person's activity against a camera, and get back where the frame went.

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
        stored_at = await _rpc_sent(
            self._require_session(),
            "POST",
            self._scoped(self.PEOPLE_ACTIVITY),
            what=f"storing people activity on server {self.server_id}",
            unwrap=unwrap_fr_sidecar,
            validate=_media_url,
            base_url=self._require_base_url(),
            payload=request.model_dump(by_alias=True, exclude_none=True),
        )
        return "" if stored_at is None else stored_at

    async def update_staff_images(
        self, request: StaffImageUpdateRequest
    ) -> Optional[StaffImageUpdateResult]:
        """Replace the images held for a staff member.

        Args:
            request: The staff member and their new images.

        Returns:
            The result, or ``None`` when the sidecar answers with no payload.

        Raises:
            CallFailure: There is no session or no sidecar address, or the call failed.
        """
        return await _rpc_sent(
            self._require_session(),
            "PUT",
            self._scoped(self.STAFF_IMAGES),
            what=f"updating staff images on server {self.server_id}",
            unwrap=unwrap_fr_sidecar,
            validate=StaffImageUpdateResult.model_validate,
            base_url=self._require_base_url(),
            payload=request.model_dump(by_alias=True, exclude_none=True),
        )

    async def shutdown(
        self, request: Optional[ServiceShutdownRequest] = None
    ) -> Optional[ServiceShutdownResult]:
        """Ask the sidecar to shut down.

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
        return await _rpc_sent(
            self._require_session(),
            "DELETE",
            self._scoped(self.SHUTDOWN),
            what=f"shutting down the facial-recognition sidecar on server {self.server_id}",
            unwrap=unwrap_fr_sidecar,
            validate=ServiceShutdownResult.model_validate,
            base_url=self._require_base_url(),
            payload={} if request is None else request.model_dump(by_alias=True, exclude_none=True),
        )

    async def fetch_staff_embeddings(self) -> List[StaffEmbedding]:
        """Every enrolled face the sidecar holds.

        Returns:
            The embeddings, or ``[]`` when there are none. An empty list and a missing answer
            are the same thing on this route -- a sidecar with nothing enrolled yet.

        Raises:
            CallFailure: There is no session or no sidecar address, or the call failed.
        """
        embeddings = await _rpc_sent(
            self._require_session(),
            "GET",
            self._scoped(self.STAFF_EMBEDDINGS),
            what=f"the enrolled faces on server {self.server_id}",
            unwrap=unwrap_fr_sidecar,
            validate=_EMBEDDING_LIST.validate_python,
            base_url=self._require_base_url(),
        )
        return [] if embeddings is None else embeddings

    async def enroll_unknown_person(
        self, request: UnknownPersonEnrollRequest
    ) -> Optional[UnknownPersonEnrollResult]:
        """Enrol a face the sidecar has seen but cannot name.

        Args:
            request: The face to enrol.

        Returns:
            The result, or ``None`` when the sidecar answers with no payload.

        Raises:
            CallFailure: There is no session or no sidecar address, or the call failed.
        """
        return await _rpc_sent(
            self._require_session(),
            "POST",
            self._scoped(self.ENROLL_UNKNOWN),
            what=f"enrolling an unknown person on server {self.server_id}",
            unwrap=unwrap_fr_sidecar,
            validate=UnknownPersonEnrollResult.model_validate,
            base_url=self._require_base_url(),
            payload=request.model_dump(by_alias=True, exclude_none=True),
        )

    async def fetch_health(self) -> Optional[HealthStatus]:
        """Whether the sidecar considers itself healthy.

        **Sent with the server id but no project.** That is the route's own shape, not an
        oversight: a health check asks about the service, and scoping it to a project would
        ask a question the service does not have.

        Returns:
            The status, or ``None`` when the sidecar answers with no payload.

        Raises:
            CallFailure: There is no session or no sidecar address, or the call failed.
        """
        return await _rpc_sent(
            self._require_session(),
            "GET",
            f"{self.HEALTH}?{urlencode({'serverID': self.server_id})}",
            what=f"the health of the facial-recognition sidecar on server {self.server_id}",
            unwrap=unwrap_fr_sidecar,
            validate=HealthStatus.model_validate,
            base_url=self._require_base_url(),
        )

    async def upload_frame(
        self, upload_url: str, image_bytes: bytes, *, content_type: str = "image/jpeg"
    ) -> bool:
        """Put a frame at the storage address :meth:`store_people_activity` handed back.

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
        return await self._uploader.put(upload_url, image_bytes, content_type=content_type)

    async def aclose(self) -> None:
        """Close the upload pool. Call from the event loop that sent on it.

        Idempotent, and free on a client that never uploaded -- the pool opens no socket
        until the first send.
        """
        await self._uploader.aclose()


__all__ = ["FRClient"]
