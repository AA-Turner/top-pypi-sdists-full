"""Auto-generated stub for module: models."""
from typing import Any

# Constants
Bool: Any
Float: Any
FloatList: Any
Int: Any
Obj: Any
ObjList: Any
Str: Any
StrList: Any

# Functions
def looks_like_object_id(value: Any) -> bool:
    """
    True when ``value`` is 24 hex characters, the shape of a Mongo id.
    
        Used to spot an id that has been put where a human-readable name belongs.
    """
    ...
def normalise_location_id(value: Any) -> str:
    """
    A stripped location id, or ``""`` when there is no location.
    
        The platform represents "no location" two ways: the key is missing, or it holds
        an all-zero ObjectId. Both must read as absent, because the placeholder is a
        valid-looking id that matches no location and would otherwise be looked up.
    """
    ...

# Classes
class ActionRecord:
    # Endpoint 1 -- ``GET /v1/actions/action/{actionRecordId}/details``.
    #
    #     The record describing one running action. Callers read three different slices of
    #     it: ``action_details``, ``job_params``, and top-level identity fields. The two
    #     nested slices stay untyped dicts because their contents vary by action type.

    ...
class Application:
    # Endpoint 3 -- ``GET /v1/applications/{id}``.
    #
    #     The application catalogue entry. Mostly presentation metadata; this package reads
    #     the version fields. Note ``applicationid``, all lowercase, as the producer spells
    #     it.

    ...
class ApplicationDeployment:
    # Endpoint 2 -- ``GET /v1/inference/get_application_deployment/{id}``.
    #
    #     One deployment of one application. ``compute_alias`` is spelled in snake_case by
    #     the producer while everything around it is camelCase; that is preserved as sent.

    ...
class Body:
    # Base for every request model: strict, because a bad request is our bug.
    #
    #     ``extra="forbid"`` turns a misspelled keyword into an error at the call rather
    #     than a field that silently never reaches the wire.

    model_config: Any

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
class CameraLocation:
    # Endpoint 8 -- ``GET /v1/inference/get_location/{id}``.
    #
    #     The site a camera belongs to. ``location_name`` is what callers display, and
    #     ``normalise_location_id`` below is why the id is worth typing: the platform
    #     writes an all-zero ObjectId for an unset location rather than omitting the key,
    #     and that placeholder must read as absent, not as an id.

    ...
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
class FacialRecognitionServer:
    # Endpoints 10 and 12 -- the facial-recognition sidecar's server record.
    #
    #     Endpoint 10 (``GET .../get_facial_recognition_server/{id}``) reads it; endpoint
    #     12 (``PUT .../update_facial_recognition_deployment/{id}``) updates the deployment
    #     and echoes the same record back. The producer declares one schema for both.
    #
    #     ``host`` and ``port`` are what the sidecar's base URL is built from.

    ...
class HealthStatus:
    # Endpoint 22 -- the reply to ``GET /v1/facial_recognition/health``.
    #
    #     UNVERIFIED, and **no field is observed**. The caller treats the envelope's
    #     ``success`` as the entire answer, so liveness is all this endpoint reports here
    #     however much detail the sidecar may send.

    ...
class LprServer:
    # Endpoint 11 -- ``GET /v1/actions/lpr_servers/{id}``.
    #
    #     The licence-plate server's record, the same shape as the facial-recognition one
    #     minus ``computeAlias``. The two are **not** shared: the producer declares them
    #     separately, and a field added to one would not appear on the other.

    ...
class Payload:
    # Base for every response model: tolerant of anything the producer sends.
    #
    #     ``extra="ignore"`` so a new field is not an error, ``populate_by_name`` so the
    #     Python name works as well as the wire spelling, and ``coerce_numbers_to_str`` so
    #     a numeric id arriving for a string field becomes ``"123"`` rather than vanishing.

    model_config: Any

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
class RedisServer:
    # Endpoint 9 -- ``GET /v1/actions/get_redis_server_by_instance_id/{id}``.
    #
    #     Connection details for the Redis this instance publishes to. ``port`` is declared
    #     as a **string** here, unlike the two server records below which declare it as an
    #     integer; that inconsistency is the producer's and is preserved.

    ...
class ServiceShutdownRequest:
    # Endpoint 19 -- ``DELETE /v1/facial_recognition/shutdown``.
    #
    #     UNVERIFIED: no published schema. One optional field, and it must be **absent**
    #     rather than ``null`` when there is no action record to name -- the caller sends
    #     ``{}`` in that case. ``exclude_none`` on serialisation is what reproduces it.

    ...
class ServiceShutdownResult:
    # Endpoint 19 -- the reply to ``DELETE /v1/facial_recognition/shutdown``.
    #
    #     UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.

    ...
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
class StaffDetails:
    # Endpoint 16 -- the reply to ``GET /v1/facial_recognition/staff/{staffId}``.
    #
    #     UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.
    #     See ``StaffEnrollResult`` for why the record is not guessed at.

    ...
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
class StaffEnrollRequest:
    # Endpoint 14 -- ``POST /v1/facial_recognition/staff/enroll``.
    #
    #     UNVERIFIED: no published schema, so "required" here means "always sent today",
    #     not "required by the producer".
    #
    #     ``images`` are base64-encoded JPEGs. The caller reads them from disk and encodes
    #     them before building this, so a file that cannot be read never reaches the model.

    ...
class StaffEnrollResult:
    # Endpoint 14 -- the reply to ``POST /v1/facial_recognition/staff/enroll``.
    #
    #     UNVERIFIED, and **no field is observed**. The caller checks only the envelope's
    #     ``success``/``error``, which the response layer already handles, so nothing in
    #     this package reads the payload. Fields belong here once a caller needs one, or
    #     once the sidecar publishes a schema -- guessing at the created staff record would
    #     give an invention the standing of a contract.

    ...
class StaffImageUpdateRequest:
    # Endpoint 18 -- ``PUT /v1/facial_recognition/staff/update_images``.
    #
    #     UNVERIFIED: no published schema. ``image_url`` points at an image already
    #     uploaded elsewhere; the bytes do not travel in this body.

    ...
class StaffImageUpdateResult:
    # Endpoint 18 -- the reply to ``PUT /v1/facial_recognition/staff/update_images``.
    #
    #     UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.

    ...
class UnknownPersonEnrollRequest:
    # Endpoint 21 -- ``POST /v1/facial_recognition/enroll_unknown_person``.
    #
    #     UNVERIFIED: no published schema.
    #
    #     ``timestamp`` is unlike the other optional fields: the caller substitutes the
    #     current UTC time when none is given, so it is always sent. ``image_source`` and
    #     ``location`` are omitted when empty.

    ...
class UnknownPersonEnrollResult:
    # Endpoint 21 -- the reply to ``POST .../enroll_unknown_person``.
    #
    #     UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.

    ...
class UsecaseDownload:
    # Endpoints 6 and 7 -- a time-limited grant to download a usecase bundle.
    #
    #     Two routes reach the same grant: ``/v1/applications/license/{id}/versions/
    #     {version}/usecase/download`` for a licensed application, and the same path
    #     without ``license/`` otherwise. The producer declares one schema for both.

    ...
