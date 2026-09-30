"""The licence-plate client: one platform route and one on the lpr-server.

The smallest of the three clients, and the shape is the same as
:class:`~.fr_client.FRClient`'s: you use the **platform** to find the **server**, then talk to
the server. ``GET /v1/actions/lpr_servers/{id}`` is ``/v1/actions/`` by prefix and this
client's by **ownership** -- it is keyed by ``lpr_server_id``, which nothing else holds.

**Two routes, not three.** An earlier count included
``POST /v1/lpr-server/detections/{id}/view-frames``, and **no lpr-server build has ever
implemented it**: there is no such route, handler or DTO in the service, and the strings
``view-frames`` and ``viewFrame`` do not occur in its binary. Every call returned
``404 page not found``. It is not a route this client is missing; it is a route that does not
exist.

lpr-server's replies are shaped the other way round
===================================================

The platform and the facial-recognition sidecar both wrap a success in
``{success, data}``. lpr-server does the opposite: a successful create answers **201 with the
created document itself**, and only the failure path carries an envelope. So
:func:`~.response.unwrap_lpr_server` treats a body as the payload *unless* it explicitly says
it failed -- requiring ``success``, as a shared unwrap would, rejects every successful reply
this producer sends.

The detection route is idempotent, and that is a property of the producer
========================================================================

``POST /v1/lpr-server/detections`` is idempotent on ``(licensePlate, projectId, teamId)``:
where the plate already has a detection, the server resolves it, stores the new frame and
appends the frame id to the existing document rather than inserting a second one. Verified
against a live server -- 231 detection documents, 231 distinct plates, zero duplicates, 149
holding more than one frame.

That makes a retry **safe** here, where it is not on any of the facial-recognition writes. It
does not make one **right**: this client still sends once, because a retry decision belongs to
the caller that knows whether the sighting still matters by the time the first attempt
failed, and a silent second POST is how one slow reply becomes two round trips per frame on a
path that already runs per detection.
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Optional
from urllib.parse import urlencode

from .bootstrap import attach_session
from .identity import resolve_sidecar_base_url
from .models import CreateDetectionRequest, Detection, LprServer
from .response import CallFailure, unwrap_lpr_server, unwrap_platform
from .transport import POOLED_POST_TIMEOUT_S, PooledPoster, _rpc_model

logger = logging.getLogger(__name__)


class LPRClient:
    """The licence-plate server and the platform route that finds it.

    Args:
        lpr_server_id: The server's id. A **constructor argument, never resolved** -- it
            arrives in the post-processing config, and the usecase has defined behaviour when
            it is absent. A client that resolved its own would attach to whichever server it
            happened to find rather than the one the deployment configured.
        session: An open ``matrice_common`` session. Omit it and the client asks
            :func:`~.bootstrap.attach_session` for the process's own; on a machine with no SDK
            it constructs successfully and has no session, and both routes refuse by name.
        project_id: The project detections are filed under. Omit it and it is read from the
            server record, which carries it as ``projectID``.
        public_ip: This machine's public address, if the caller has already looked it up.

    Attributes:
        lpr_server_id: The server this client is attached to.

    **This client's project is its own source, not a shared one.** It comes off the server
    record as ``projectID`` and is scoped to that server.
    :func:`~.identity.resolve_project_id` answers a different question -- which project this
    *worker* belongs to, from the action record -- and the two are not interchangeable.

    **So this client does not read the launch action record for its project, and that is
    deliberate rather than an omission.** :class:`~.fr_client.FRClient` does, because the
    client it replaced did; the shipped licence-plate path never has. Its project has always
    come from the lpr-server record, and the action record it *does* read -- for the alert
    manager's server and deployment ids -- has never been a project source here. Adding the
    fallback to match the sibling would file detections under the project the launch record
    names whenever the two disagree, which is a change no caller has asked for.
    """

    #: Platform. Read for the server's address and project.
    SERVER = "/v1/actions/lpr_servers/{lpr_server_id}"
    #: lpr-server. Creates a detection, or appends a frame to the one that exists.
    DETECTIONS = "/v1/lpr-server/detections"

    def __init__(
        self,
        lpr_server_id: str,
        session: Any = None,
        *,
        project_id: str = "",
        public_ip: str = "",
        post_timeout_s: float = POOLED_POST_TIMEOUT_S,
    ) -> None:
        self.lpr_server_id = lpr_server_id
        self._session = attach_session(
            session, what=f"the licence-plate client for server {lpr_server_id}"
        )
        self._public_ip = public_ip
        self._given_project_id = project_id
        self._server: Optional[LprServer] = None
        self._connected = False
        self._warned_no_project = False
        #: Guards the three fields above, which are read and written together. The sender
        #: this client is built for drives every request from one thread, so nothing today
        #: contends for it; it is held to match :class:`~.fr_client.FRClient`, where callers
        #: on separate threads do share one instance. Reentrant because :meth:`refresh`
        #: holds it and calls :meth:`connect`, which takes it again.
        self._lock = threading.RLock()
        #: The detection route's connection pool. It holds no socket until the first send, so a
        #: client built for a read, a test or a dry run never opens one and never needs closing.
        self._poster = PooledPoster(self._require_session, timeout_s=post_timeout_s)

    @property
    def session(self) -> Any:
        """The session this client calls on, or ``None`` when the SDK is absent."""
        return self._session

    @property
    def rpc(self) -> Any:
        """The session's RPC handle, read fresh on every access.

        Not cached: ``session.update()`` replaces the session's RPC and shuts the previous one
        down, so a handle held from construction works until the first re-authentication and
        then silently stops.

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
                f"The licence-plate client for server {self.lpr_server_id} has no session, so "
                "it cannot reach the platform or the lpr-server. matrice_common was not "
                "importable when it was built."
            )
        return self._session

    def connect(self) -> Optional[LprServer]:
        """Read the server record, and with it the server's address and project.

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
        with self._lock:
            if not self._connected:
                self._server = _rpc_model(
                    self._require_session(),
                    self.SERVER.format(lpr_server_id=self.lpr_server_id),
                    what=f"the licence-plate server record for {self.lpr_server_id}",
                    unwrap=unwrap_platform,
                    validate=LprServer.model_validate,
                )
                self._connected = True
            return self._server

    def refresh(self) -> Optional[LprServer]:
        """Read the server record again, discarding the one held.

        For a server that has been redeployed to a different host under a running worker.
        Nothing calls this automatically: re-reading on every failure would turn one
        unreachable server into two round trips per detection.

        Discards the held record and re-reads as one locked step. A concurrent
        :meth:`connect` can therefore never store its record in the gap between the two,
        which would leave this client holding ``None`` and unable to read again.
        """
        with self._lock:
            self._connected = False
            self._server = None
            self._warned_no_project = False
            return self.connect()

    @property
    def project_id(self) -> str:
        """The project detections are filed under.

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
        if self._given_project_id:
            return self._given_project_id

        record = self.connect()
        found = "" if record is None else record.project_id
        if not found and not self._warned_no_project:
            self._warned_no_project = True
            logger.warning(
                "No project id for the licence-plate client on server %s: none was passed and "
                "the server record carries no projectID. lpr-server requires projectId, so "
                "detections sent without one will be refused.",
                self.lpr_server_id,
            )
        return found

    @property
    def base_url(self) -> str:
        """Where the lpr-server is, or ``""`` when no record says.

        Built from the record's host and port by the same policy the facial-recognition
        sidecar uses -- see :func:`~.identity.resolve_sidecar_base_url`.
        """
        record = self.connect()
        if record is None:
            return ""
        return resolve_sidecar_base_url(record.host, record.port, public_ip=self._public_ip)

    def _require_base_url(self) -> str:
        """The server's address, or a named refusal.

        Raises:
            CallFailure: No server record, or one carrying no host. Refusing here stops the
                detection being sent to the session's default base, where it would be refused
                as unauthorised and read as a credentials problem rather than as the missing
                server record it is.
        """
        base = self.base_url
        if not base:
            raise CallFailure(
                f"No address for the lpr-server on {self.lpr_server_id}: its server record is "
                "missing or carries no host, so there is nowhere to send this detection."
            )
        return base

    def fetch_server(self) -> Optional[LprServer]:
        """The server record, read fresh.

        ``fetch_``, so this is a round trip every time -- unlike :meth:`connect`, which
        answers from the record it holds.
        """
        return _rpc_model(
            self._require_session(),
            self.SERVER.format(lpr_server_id=self.lpr_server_id),
            what=f"the licence-plate server record for {self.lpr_server_id}",
            unwrap=unwrap_platform,
            validate=LprServer.model_validate,
        )

    async def create_detection(self, request: CreateDetectionRequest) -> Optional[Detection]:
        """File a plate sighting, or add a frame to the sighting that already exists.

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
        return await self._poster.post(
            f"{self.DETECTIONS}?{urlencode({'projectId': self.project_id})}",
            what=f"filing a plate detection on lpr-server {self.lpr_server_id}",
            unwrap=unwrap_lpr_server,
            validate=Detection.model_validate,
            base_url=self._require_base_url(),
            payload=request.model_dump(by_alias=True, exclude_none=True),
        )

    async def aclose(self) -> None:
        """Close the detection pool. Call from the event loop that sent on it.

        Idempotent, and free on a client that never filed a detection -- the pool opens no
        socket until the first send.
        """
        await self._poster.aclose()


__all__ = ["LPRClient"]
