"""Stub file for clients directory."""
from typing import Any, Optional, Tuple

from .response import CallFailure

# Constants
ENV_ACTION_ID: str = ...  # From bootstrap
ENV_ACTION_ID_BARE: str = ...  # From bootstrap
Bool: Any = ...  # From models
Float: Any = ...  # From models
FloatList: Any = ...  # From models
Int: Any = ...  # From models
Obj: Any = ...  # From models
ObjList: Any = ...  # From models
Str: Any = ...  # From models
StrList: Any = ...  # From models
ENV_API_BASE: str = ...  # From transport
LOCAL_AUTHORITY_PREFIXES: Tuple[Any, ...] = ...  # From transport
logger: Any = ...  # From transport

# Functions
# From bootstrap
def get_session(what: str = 'the platform session') -> Any:
    """
    The process's one ``matrice_common`` session, built on first use.
    
        Lazy because a container that never needs the platform should never pay for a session, and
        should not fail at import time for want of credentials it does not use. Memoised per
        *process*, not per caller: sessions are built from the same two environment variables
        wherever they are opened, so a second one is the same handle at the cost of another
        credential exchange.
    
        Thread-safe under the double-checked pattern -- the fast path is a bare read once the
        session exists, and the lock is taken only while the process is still cold.
    
        A failure is **not** memoised: ``_SESSION`` is assigned only on success, so a container that
        starts before its credentials are mounted recovers on the next call instead of being stuck
        with the first error for its lifetime.
    """
    ...

# From bootstrap
def open_session(what: str) -> Any:
    """
    A ``matrice_common`` session from the container's own credentials.
    
        Imported lazily, exactly as ``PostProcessingConfigClient.__init__`` does, so this module stays
        importable in an image with no platform SDK.
    
        Opens a **new** session every call. Callers that want one session for the life of the process
        use :func:`get_session` instead; this one stays uncached so that a caller who needs a session
        independent of anyone else's -- or a test that needs two -- can still get one.
    
        Credentials come from ``matrice_common.resolve_credentials``, which is the same three-tier
        order ``Session.__init__`` itself applies: an explicit argument, then the SDK's in-process
        registry, then the environment. Reading ``os.environ`` directly -- as this did until now --
        sees only the last of the three, so a container whose credentials were published to the
        registry by an SDK entry point was refused for want of variables it never needed to export.
        That is reachable rather than theoretical: ``Session`` used to copy explicit keys back into
        ``os.environ`` and deliberately stopped, because the environment is inherited by every
        subprocess and captured by most crash reporters.
    """
    ...

# From bootstrap
def resolve_action_id(env: Optional[Any[str, str]] = None, argv: Optional[Any[str]] = None) -> Optional[str]:
    """
    The action record id for this worker, if it can be determined locally.
    
        Three sources, no I/O. ``$MATRICE_ACTION_ID`` first, because an operator setting it means it,
        then ``$ACTION_ID`` -- the bare name the Go services and the ENV_ID_ACTIONS images read, and the
        only one some py_compute launch paths emitted. Then ``sys.argv``: py_compute launches every
        action container as ``python3 <entrypoint>.py <action_record_id> <port>``, so the id is the
        first argument that looks like an ObjectId. Matching on shape rather than position keeps this
        from mistaking a port or a flag for an id.
    
        A malformed value in either env var falls through rather than erroring, so a truncated id does
        not mask a good one in argv.
    """
    ...

# From models
def looks_like_object_id(value: Any) -> bool:
    """
    True when ``value`` is 24 hex characters, the shape of a Mongo id.
    
        Used to spot an id that has been put where a human-readable name belongs.
    """
    ...

# From models
def normalise_location_id(value: Any) -> str:
    """
    A stripped location id, or ``""`` when there is no location.
    
        The platform represents "no location" two ways: the key is missing, or it holds
        an all-zero ObjectId. Both must read as absent, because the placeholder is a
        valid-looking id that matches no location and would otherwise be looked up.
    """
    ...

# From response
def unwrap_fr_sidecar(response: Any) -> Any:
    """
    Return the payload from a facial-recognition sidecar reply.
    
        Most routes answer with a ``{success, data, error}`` envelope and are gated
        on ``success`` alone. One route -- storing a person's activity -- answers
        with a bare JSON string instead: the media URL it resolved, or ``""`` when
        no frame was available. It carries no envelope and must not be probed for
        one, since an empty string there is a successful result and not a missing
        field.
    
        A reply is therefore treated as an envelope only when it is a mapping that
        actually carries a ``success`` key. Anything else is the payload itself.
    
        As in :func:`unwrap_platform`, success is evaluated before absence, so a
        reply the sidecar called successful is never discarded as a missing record.
    
        Args:
            response: The decoded body as the RPC layer returned it.
            what: What was being attempted, phrased to read inside an error message.
    
        Returns:
            The ``data`` payload for an enveloped reply, the body itself for a bare
            one, or ``None`` when the record is absent.
    
        Raises:
            CallFailure: The sidecar returned an envelope reporting failure.
    """
    ...

# From response
def unwrap_lpr_server(response: Any) -> Any:
    """
    Return the payload from an lpr-server reply.
    
        The rule here is inverted relative to the other two producers. lpr-server
        replies to a successful write with the created document itself -- no
        envelope, nothing named ``success`` or ``code`` to inspect. Only the failure
        path is enveloped. So a body is the payload **unless** it explicitly says it
        failed.
    
        Requiring ``success`` here, as a shared envelope would, rejects every
        successful reply this backend sends.
    
        The transport has already raised on any non-2xx status by the time a body
        reaches this function, so the status is not re-checked.
    
        Args:
            response: The decoded body as the transport returned it.
            what: What was being attempted, phrased to read inside an error message.
    
        Returns:
            The body, unchanged.
    
        Raises:
            CallFailure: The reply was an envelope explicitly reporting failure.
    """
    ...

# From response
def unwrap_platform(response: Any) -> Any:
    """
    Return the ``data`` payload from a platform API envelope.
    
        The platform wraps every reply as
        ``{success, code, message, serverTime, data}``. Success is decided by
        ``success`` and nothing else.
    
        ``code`` is deliberately not consulted. It is a real HTTP status, so a
        perfectly successful call can carry a 2xx other than 200 -- a created
        resource answers ``201`` -- and gating on ``code == 200`` turns those into
        spurious failures.
    
        Success is evaluated **before** absence, matching the order the replaced
        call sites used. The two cannot both be true on any reply the RPC layer
        actually builds -- its canonical 404 pairs ``status_code: 404`` with
        ``success: False`` -- but checking success first is the safer order either
        way, because it can never discard a reply the backend called successful.
    
        Args:
            response: The decoded envelope as the RPC layer returned it.
            what: What was being resolved, phrased to read inside an error message,
                e.g. ``"the camera record"``.
    
        Returns:
            The ``data`` payload, which may itself be ``None`` when the backend
            reports success with an empty result. ``None`` is also returned when the
            document is absent.
    
        Raises:
            CallFailure: The backend reported failure, or answered with something
                that is not an envelope.
    """
    ...

# From transport
def backend_base_url(env: Optional[Any[str, str]] = None) -> str:
    """
    The backend's own address, for a route the session's base URL will not serve.
    
        Deployments set ``MATRICE_BASE_URL`` to a local gateway (``http://localhost``). That gateway
        proxies the route prefixes it knows -- ``/v1/inference/*`` among them, which is why
        ``PostProcessingConfigClient`` has always worked -- and 302s anything else out to the real
        backend. ``matrice_common``'s client has ``follow_redirects=True``, and httpx drops the
        ``Authorization`` header when a redirect crosses origin, so a redirected call arrives
        unauthenticated and be-application answers 404. Observed in production on 0.1.428:
        ``http://localhost/v1/applications/.../usecase/download`` -> 302 -> prod -> 404, while the same
        path with a direct base URL returns 200.
    
        Derived the same way ``matrice_common`` derives its own default, so an on-prem or non-prod
        deployment still lands on its own backend; ``$MATRICE_APP_BUNDLE_API_BASE`` overrides it.
    """
    ...

# Classes
# From models
class ActionRecord:
    # Endpoint 1 -- ``GET /v1/actions/action/{actionRecordId}/details``.
    #
    #     The record describing one running action. Callers read three different slices of
    #     it: ``action_details``, ``job_params``, and top-level identity fields. The two
    #     nested slices stay untyped dicts because their contents vary by action type.

    ...

# From models
class Application:
    # Endpoint 3 -- ``GET /v1/applications/{id}``.
    #
    #     The application catalogue entry. Mostly presentation metadata; this package reads
    #     the version fields. Note ``applicationid``, all lowercase, as the producer spells
    #     it.

    ...

# From models
class ApplicationDeployment:
    # Endpoint 2 -- ``GET /v1/inference/get_application_deployment/{id}``.
    #
    #     One deployment of one application. ``compute_alias`` is spelled in snake_case by
    #     the producer while everything around it is camelCase; that is preserved as sent.

    ...

# From models
class Body:
    # Base for every request model: strict, because a bad request is our bug.
    #
    #     ``extra="forbid"`` turns a misspelled keyword into an error at the call rather
    #     than a field that silently never reaches the wire.

    model_config: Any


# From models
class Camera:
    # Endpoint 13 -- ``GET /v1/inference/get_camerastream_by_acc_number/{acc}``.
    #
    #     One camera stream. The route answers with every camera on the account, so callers
    #     filter this list by id rather than asking for one.
    #
    #     This package reads the display fields -- ``camera_name``, ``camera_group_id``,
    #     ``location_id`` -- and ``custom_stream_settings`` for the frame resolution. The
    #     rest is declared so the model matches what the producer publishes.

    ...

# From models
class CameraLocation:
    # Endpoint 8 -- ``GET /v1/inference/get_location/{id}``.
    #
    #     The site a camera belongs to. ``location_name`` is what callers display, and
    #     ``normalise_location_id`` below is why the id is worth typing: the platform
    #     writes an all-zero ObjectId for an unset location rather than omitting the key,
    #     and that placeholder must read as absent, not as an id.

    ...

# From models
class CreateDetectionRequest:
    # Endpoint 24 -- ``POST /v1/lpr-server/detections``.
    #
    #     The one request body with a producer-declared schema, and the only endpoint of
    #     the twenty-four whose producer requires anything: ``projectId``, ``licensePlate``,
    #     ``frameId``, ``cameraId``, ``applicationId`` and ``rtpNumber``. Those six are
    #     required here; the rest are optional because the producer says so.
    #
    #     ``coerce_numbers_to_str`` is the point of this model. A numeric ``frame_id``
    #     reaching the producer's string field is rejected with ``cannot unmarshal number
    #     into Go struct field CreateDetectionRequest.frameId of type string`` and the
    #     sighting is lost -- nothing upstream guarantees the type, since the frame id is
    #     stored as it was passed. Converting it is the fix, declared once here instead of
    #     written by hand at one call site among several.
    #
    #     ``confidence`` is the name the producer declares for the OCR confidence;
    #     ``ocr_confidence`` appears in its schema zero times. ``image_data`` is sent but
    #     declared nowhere by the producer, and is kept because it is what the caller sends.

    model_config: Any


# From models
class Detection:
    # Endpoint 24 -- the document created by ``POST /v1/lpr-server/detections``.
    #
    #     lpr-server answers a successful create with **201** and the created document
    #     itself, with no ``{success, data}`` envelope around it. It declares ``201`` and
    #     ``500`` and no ``4xx`` at all, so any non-201 is a failure; the status codes it
    #     happens to declare are not the set it can return.
    #
    #     The reply does not echo the OCR confidence that was sent.

    ...

# From models
class FacialRecognitionServer:
    # Endpoints 10 and 12 -- the facial-recognition sidecar's server record.
    #
    #     Endpoint 10 (``GET .../get_facial_recognition_server/{id}``) reads it; endpoint
    #     12 (``PUT .../update_facial_recognition_deployment/{id}``) updates the deployment
    #     and echoes the same record back. The producer declares one schema for both.
    #
    #     ``host`` and ``port`` are what the sidecar's base URL is built from.

    ...

# From models
class HealthStatus:
    # Endpoint 22 -- the reply to ``GET /v1/facial_recognition/health``.
    #
    #     UNVERIFIED, and **no field is observed**. The caller treats the envelope's
    #     ``success`` as the entire answer, so liveness is all this endpoint reports here
    #     however much detail the sidecar may send.

    ...

# From models
class LprServer:
    # Endpoint 11 -- ``GET /v1/actions/lpr_servers/{id}``.
    #
    #     The licence-plate server's record, the same shape as the facial-recognition one
    #     minus ``computeAlias``. The two are **not** shared: the producer declares them
    #     separately, and a field added to one would not appear on the other.

    ...

# From models
class Payload:
    # Base for every response model: tolerant of anything the producer sends.
    #
    #     ``extra="ignore"`` so a new field is not an error, ``populate_by_name`` so the
    #     Python name works as well as the wire spelling, and ``coerce_numbers_to_str`` so
    #     a numeric id arriving for a string field becomes ``"123"`` rather than vanishing.

    model_config: Any


# From models
class PeopleActivityRequest:
    # Endpoint 17 -- ``POST /v1/facial_recognition/store_people_activity``.
    #
    #     UNVERIFIED: no published schema. The wire spelling is mixed -- ``staff_id`` and
    #     ``camera_name`` in snake_case beside ``applicationId`` and ``rtpNumber`` in
    #     camelCase -- and is reproduced exactly as sent rather than tidied.
    #
    #     Two things the caller does that this model preserves:
    #
    #     * ``employee_id`` and ``anonymous_id`` are **mutually exclusive**, chosen by
    #       whether the detection was of a known or an unknown person. Both default to
    #       ``None`` so only the one that applies is serialised.
    #     * ``confidence_score`` is the only score field the sidecar binds from the wire.
    #       A similarity score sent under any other name is accepted and discarded.
    #
    #     Image bytes are deliberately not part of this body. The sidecar fetches the frame
    #     itself from the media server using ``rtp_number`` and ``camera_id``.

    ...

# From models
class PostProcessingConfig:
    # Endpoints 4 and 5 -- the post-processing config for one camera and application.
    #
    #     Both routes return this same record, because there is exactly one config per
    #     ``(camera, application)`` pair::
    #
    #         GET /v1/inference/post_processing_configs/by_app_deployment/{id}  -> a list
    #         GET /v1/inference/post_processing_config?cameraId=&applicationId= -> one
    #
    #     The first asks by deployment and gets every camera's config; the second asks by
    #     camera and application and gets that one. The second exists as a fallback: when
    #     ``app_deployment_id`` is stale the deployment-scoped query answers with an empty
    #     list, and the config is still reachable by its other key.
    #
    #     ``post_processing`` stays an untyped dict -- it carries per-usecase settings,
    #     including the zone geometry, and has no fixed shape.

    ...

# From models
class RedisDetails:
    # Endpoint 23 -- the reply to ``GET /v1/facial_recognition/get_redis_details``.
    #
    #     Where the sidecar publishes recognition events. UNVERIFIED, but all three fields
    #     are read by the caller, which builds a Redis connection from them.
    #
    #     The wire names are SCREAMING_CASE, unlike every other payload here; that is how
    #     the sidecar sends them. ``port`` arrives as a string on at least one deployment
    #     and is converted by the caller, so it is declared ``int`` and tolerates both. An
    #     empty ``password`` means no password rather than an empty one.

    ...

# From models
class RedisServer:
    # Endpoint 9 -- ``GET /v1/actions/get_redis_server_by_instance_id/{id}``.
    #
    #     Connection details for the Redis this instance publishes to. ``port`` is declared
    #     as a **string** here, unlike the two server records below which declare it as an
    #     integer; that inconsistency is the producer's and is preserved.

    ...

# From models
class ServiceShutdownRequest:
    # Endpoint 19 -- ``DELETE /v1/facial_recognition/shutdown``.
    #
    #     UNVERIFIED: no published schema. One optional field, and it must be **absent**
    #     rather than ``null`` when there is no action record to name -- the caller sends
    #     ``{}`` in that case. ``exclude_none`` on serialisation is what reproduces it.

    ...

# From models
class ServiceShutdownResult:
    # Endpoint 19 -- the reply to ``DELETE /v1/facial_recognition/shutdown``.
    #
    #     UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.

    ...

# From models
class SimilarFaceMatch:
    # Endpoint 15 -- one match from ``POST /v1/facial_recognition/search/similar``.
    #
    #     The payload is a **list** of these, ordered best-first; the caller logs the top
    #     match and passes the rest on.
    #
    #     UNVERIFIED, and partial: ``staff_id`` and ``score`` are the two fields a caller
    #     reads. The sidecar sends more per match -- the search is what decides known from
    #     unknown -- but nothing here reads it, so nothing more is declared.

    ...

# From models
class SimilarFaceSearchRequest:
    # Endpoint 15 -- ``POST /v1/facial_recognition/search/similar``.
    #
    #     UNVERIFIED: no published schema.
    #
    #     ``collection`` defaults to ``staff_embeddings`` and a test pins that default --
    #     searching the wrong collection returns plausible matches from the wrong set,
    #     which is worse than returning none. ``location`` and ``timestamp`` are omitted
    #     entirely when empty, so they are ``None``-defaulted rather than ``""``.

    ...

# From models
class StaffDetails:
    # Endpoint 16 -- the reply to ``GET /v1/facial_recognition/staff/{staffId}``.
    #
    #     UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.
    #     See ``StaffEnrollResult`` for why the record is not guessed at.

    ...

# From models
class StaffEmbedding:
    # Endpoint 20 -- one enrolled face from ``GET .../get_all_staff_embeddings``.
    #
    #     The payload is a list of these, loaded once into the matcher's matrix rather than
    #     per frame.
    #
    #     UNVERIFIED, but every field here is read by the loader, which is unusually
    #     defensive about them and worth reproducing exactly:
    #
    #     * ``embedding`` is the only field that can make the loader skip a record. A
    #       record is dropped when it is absent, not a list, empty, holds anything that
    #       will not convert to a float, or has a length differing from the first record's.
    #       The model keeps the non-convertible case tolerant -- a bad vector becomes
    #       ``[]`` -- and leaves the skipping to the loader, which is where the
    #       dimension-consistency rule lives.
    #     * ``employee_id`` arrives as something other than a string often enough that the
    #       loader wraps it in ``str()``; it is a raw ObjectId on at least one path. The
    #       declared ``str`` plus number coercion covers that.
    #     * ``is_active`` defaults to **True**. An absent flag means active -- the loader
    #       skips only on an explicit ``False`` -- so the default must not be ``False``.

    ...

# From models
class StaffEnrollRequest:
    # Endpoint 14 -- ``POST /v1/facial_recognition/staff/enroll``.
    #
    #     UNVERIFIED: no published schema, so "required" here means "always sent today",
    #     not "required by the producer".
    #
    #     ``images`` are base64-encoded JPEGs. The caller reads them from disk and encodes
    #     them before building this, so a file that cannot be read never reaches the model.

    ...

# From models
class StaffEnrollResult:
    # Endpoint 14 -- the reply to ``POST /v1/facial_recognition/staff/enroll``.
    #
    #     UNVERIFIED, and **no field is observed**. The caller checks only the envelope's
    #     ``success``/``error``, which the response layer already handles, so nothing in
    #     this package reads the payload. Fields belong here once a caller needs one, or
    #     once the sidecar publishes a schema -- guessing at the created staff record would
    #     give an invention the standing of a contract.

    ...

# From models
class StaffImageUpdateRequest:
    # Endpoint 18 -- ``PUT /v1/facial_recognition/staff/update_images``.
    #
    #     UNVERIFIED: no published schema. ``image_url`` points at an image already
    #     uploaded elsewhere; the bytes do not travel in this body.

    ...

# From models
class StaffImageUpdateResult:
    # Endpoint 18 -- the reply to ``PUT /v1/facial_recognition/staff/update_images``.
    #
    #     UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.

    ...

# From models
class UnknownPersonEnrollRequest:
    # Endpoint 21 -- ``POST /v1/facial_recognition/enroll_unknown_person``.
    #
    #     UNVERIFIED: no published schema.
    #
    #     ``timestamp`` is unlike the other optional fields: the caller substitutes the
    #     current UTC time when none is given, so it is always sent. ``image_source`` and
    #     ``location`` are omitted when empty.

    ...

# From models
class UnknownPersonEnrollResult:
    # Endpoint 21 -- the reply to ``POST .../enroll_unknown_person``.
    #
    #     UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.

    ...

# From models
class UsecaseDownload:
    # Endpoints 6 and 7 -- a time-limited grant to download a usecase bundle.
    #
    #     Two routes reach the same grant: ``/v1/applications/license/{id}/versions/
    #     {version}/usecase/download`` for a licensed application, and the same path
    #     without ``license/`` otherwise. The producer declares one schema for both.

    ...

# From response
class CallFailure(Exception):
    # A backend call did not succeed.
    #
    #     Deliberately **not** related to ``AppBundleError``, which is not a general
    #     "something went wrong" type: it means *"this bundle candidate did not work,
    #     try the next one"*, and the bundle machinery catches it in order to fall
    #     back to a different candidate. A client raising it would silently trigger
    #     that fallback from an unrelated call.
    #
    #     It also derives from ``Exception`` rather than ``RuntimeError`` -- which is
    #     where ``AppBundleError`` sits -- so that an unrelated ``except
    #     RuntimeError`` elsewhere in the SDK cannot absorb a client failure by
    #     accident.
    #
    #     Callers decide the policy, so this type carries the facts rather than a
    #     verdict. One caller translates it into a bundle error at its own boundary;
    #     another reports it and degrades. Both need something to read. The fields are
    #     what the backends actually put on their failure paths, and each is ``None``
    #     when that backend did not supply it:
    #
    #     ``code``
    #         The application-level code from an envelope, where there is one.
    #     ``status_code``
    #         The HTTP status, as the RPC layer records it on the envelope.
    #     ``tracking_code``
    #         The correlation id an lpr-server error envelope carries.
    #     ``response``
    #         The decoded body exactly as received, for a caller needing something
    #         none of the above captured.
    #
    #     The message is human-readable only, and must not be the sole carrier of
    #     anything a caller acts on: error reporting deduplicates on exception type,
    #     file and function, and never reads the message text, so two different
    #     failures raised from one function collapse into a single report.

    def __init__(self: Any, message: str) -> None: ...


from . import bootstrap, models, response, transport