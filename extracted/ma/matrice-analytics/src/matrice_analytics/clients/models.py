"""Typed shapes for every backend call this package makes.

Twenty-four endpoints are called across three producers. Today each reply is taken
apart by hand at the point of use -- alias chains, ``or``-chains, ``str().strip()``
and ``isinstance`` guards -- so the same envelope is opened in a dozen places under
a dozen slightly different rules, and a producer renaming one key fails differently
in each of them. This module declares each shape once so that digging happens in one
auditable place.

The models describe the **payload**, not the envelope. Peeling ``{success, code,
message, data}`` off a platform reply, and the two producer-specific variants of
that, belongs to the response layer next door; by the time a payload reaches a model
here it has already been unwrapped.

Responses never raise
=====================

Every response model ignores fields it does not declare, defaults every field it
does, and **falls back to that default instead of raising** when a value arrives in
a shape the field cannot take. A producer's change should degrade one field, never
fail a whole call, because the hand-written ``dict.get()`` chains being replaced
here degrade exactly that way.

Concretely, all of these yield the default rather than an error: the key is absent,
the key was renamed, the value is an explicit ``null``, the value is junk for its
type, a list contains an element that will not convert, or a container arrives where
a scalar was declared. A number arriving for a string field is *converted* rather
than dropped, since that is a formatting difference and not a missing value.

Timestamps stay ``str``. Parsing them into ``datetime`` would add a second way for a
well-formed reply to lose a field, and nothing downstream needs them typed.

Requests are strict
===================

A malformed request is our bug, not the producer's, so request models enforce their
required fields and reject unknown ones. Rejecting unknowns is deliberate: a
misspelled keyword that is merely ignored becomes a field silently missing from the
wire, which is far harder to find than an error at the call.

**Serialise with** ``model_dump(by_alias=True, exclude_none=True)``. The calling code
builds these bodies by adding keys conditionally, so an unset optional field is
*absent* from the JSON rather than present as ``null``. ``exclude_none`` reproduces
that; a plain ``model_dump`` would send nulls the producer has never been given.

Aliases
=======

Aliases are single-key and spelled the way the producer spells them, which is not
always consistently: endpoint 17 sends ``staff_id`` and ``applicationId`` in one
body. The wire spelling is preserved exactly rather than tidied.

They are deliberately not ``AliasChoices`` chains. ``AliasChoices`` stops at the
first key that is *present*, so it answers ``""`` for a blank value and raises on an
explicit ``null``, where the hand-written chains it would replace keep searching in
both cases. Where a field genuinely has to accept more than one spelling, a
validator does it, so the rule is visible and testable.

Endpoint map
============

``req``/``resp`` name the model used for that endpoint. ``--`` means no model, and
the two sections below say why. Where one model serves two endpoints it is because
the producer declares one schema for both, not because they merely look alike.

ep  producer     operation                    request                     response
--  -----------  ---------------------------  --------------------------  -------------------------
 1  actions      action details               --                          ActionRecord
 2  inference    application deployment       --                          ApplicationDeployment
 3  application  application by id            --                          Application
 4  inference    pp configs by deployment     --                          PostProcessingConfig*
 5  inference    pp config by camera and app  --                          PostProcessingConfig*
 6  application  usecase download, licensed   --                          UsecaseDownload*
 7  application  usecase download             --                          UsecaseDownload*
 8  inference    location by id               --                          CameraLocation
 9  actions      redis server by instance     --                          RedisServer
10  actions      facial-recognition server    --                          FacialRecognitionServer*
11  actions      lpr server by id             --                          LprServer
12  actions      update fr deployment         --                          FacialRecognitionServer*
13  inference    camera streams by account    --                          Camera
14  fr-sidecar   enroll staff                 StaffEnrollRequest          StaffEnrollResult
15  fr-sidecar   search similar faces         SimilarFaceSearchRequest    SimilarFaceMatch
16  fr-sidecar   staff details by id          --                          StaffDetails
17  fr-sidecar   store people activity        PeopleActivityRequest       --
18  fr-sidecar   update staff images          StaffImageUpdateRequest     StaffImageUpdateResult
19  fr-sidecar   shutdown service             ServiceShutdownRequest      ServiceShutdownResult
20  fr-sidecar   all staff embeddings         --                          StaffEmbedding
21  fr-sidecar   enroll unknown person        UnknownPersonEnrollRequest  UnknownPersonEnrollResult
22  fr-sidecar   health check                 --                          HealthStatus
23  fr-sidecar   redis details                --                          RedisDetails
24  lpr-server   create detection             CreateDetectionRequest      Detection

``*`` marks a model shared by two endpoints:

* ``PostProcessingConfig`` -- endpoints 4 and 5 are two keys onto one row. There is
  exactly one config per (camera, application); 4 asks for every config on a
  deployment and gets an array, 5 asks for one by camera and application and gets a
  single object. Same document either way.
* ``UsecaseDownload`` -- endpoints 6 and 7 are the licensed and unlicensed routes to
  the same download grant.
* ``FacialRecognitionServer`` -- endpoint 10 reads the server record, endpoint 12
  updates its deployment and echoes the same record back.

Where a request model is absent
===============================

Seventeen of the twenty-four endpoints send **no request body**. They are reads
addressed entirely by path and query parameters, or writes whose only input is in
the URL -- endpoint 12 is a ``PUT`` that sends ``{}``. There is no schema to declare,
so declaring one would invent a shape the producer never sees.

Where a response model is absent
================================

Only endpoint 17, and for a typing reason rather than a judgement: its reply is a
bare JSON string -- the media-server image URL the sidecar resolved, or ``""`` when
no frame was available -- not an object. There are no fields to declare, and the
caller treats any non-exception answer as success.

How much of this is verified
============================

Fourteen endpoints have a published OpenAPI schema, and their models are diffed
against it. **The ten facial-recognition sidecar endpoints, 14 to 23, have none.**
Their models are read off the calling code, which is the authority for that producer,
and every one of them carries an ``UNVERIFIED`` note saying how much of its shape is
observed. Nothing checks them against the producer, and no test claims to.

Two things follow. A sidecar model with no declared fields is not an oversight: it
means no caller reads a field off that reply, so there is nothing observed to
declare, and inventing names would give a guess the authority of a contract. And a
sidecar model that *does* declare fields declares only the ones some caller actually
reads -- the reply may well carry more.
"""

from __future__ import annotations

import re
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, WrapValidator, field_validator
from pydantic_core import PydanticUseDefault

# A Mongo ObjectId as it arrives on the wire, and the all-zero placeholder the
# platform writes for "this reference is unset" rather than omitting the key.
_OBJECT_ID_RE = re.compile(r"^[0-9a-f]{24}$", re.IGNORECASE)
_NULL_OBJECT_ID = "0" * 24


def _fall_back_to_default(value: Any, handler: Any) -> Any:
    """Use the field's default instead of raising when ``value`` will not convert."""
    try:
        return handler(value)
    except ValidationError:
        raise PydanticUseDefault from None


# Field types for response models. Each one degrades to the field's default rather
# than failing the whole payload; see "Responses never raise" above.
Str = Annotated[str, WrapValidator(_fall_back_to_default)]
Int = Annotated[int, WrapValidator(_fall_back_to_default)]
Float = Annotated[float, WrapValidator(_fall_back_to_default)]
Bool = Annotated[bool, WrapValidator(_fall_back_to_default)]
StrList = Annotated[list[str], WrapValidator(_fall_back_to_default)]
FloatList = Annotated[list[float], WrapValidator(_fall_back_to_default)]
Obj = Annotated[dict[str, Any], WrapValidator(_fall_back_to_default)]
ObjList = Annotated[list[dict[str, Any]], WrapValidator(_fall_back_to_default)]


class Payload(BaseModel):
    """Base for every response model: tolerant of anything the producer sends.

    ``extra="ignore"`` so a new field is not an error, ``populate_by_name`` so the
    Python name works as well as the wire spelling, and ``coerce_numbers_to_str`` so
    a numeric id arriving for a string field becomes ``"123"`` rather than vanishing.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True, coerce_numbers_to_str=True)


class Body(BaseModel):
    """Base for every request model: strict, because a bad request is our bug.

    ``extra="forbid"`` turns a misspelled keyword into an error at the call rather
    than a field that silently never reaches the wire.
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


# ---------------------------------------------------------------------------
# Platform responses -- endpoints 1 to 13
#
# Every one of these is declared in the published OpenAPI, and every one declares
# *no* required fields, which is why nothing here is mandatory.
# ---------------------------------------------------------------------------


class ActionRecord(Payload):
    """Endpoint 1 -- ``GET /v1/actions/action/{actionRecordId}/details``.

    The record describing one running action. Callers read three different slices of
    it: ``action_details``, ``job_params``, and top-level identity fields. The two
    nested slices stay untyped dicts because their contents vary by action type.
    """

    id: Str = Field(default="", alias="_id")
    compute_instance_id: Str = Field(default="", alias="_idComputeInstance")
    project_id: Str = Field(default="", alias="_idProject")
    service_id: Str = Field(default="", alias="_idService")
    user_id: Str = Field(default="", alias="_idUser")
    account_number: Str = Field(default="", alias="accountNumber")
    account_type: Str = Field(default="", alias="accountType")
    action: Str = ""
    action_details: Obj = Field(default_factory=dict, alias="actionDetails")
    actions_required: ObjList = Field(default_factory=list, alias="actionsRequired")
    created_at: Str = Field(default="", alias="createdAt")
    dependent_actions: StrList = Field(default_factory=list, alias="dependentActions")
    env: Str = ""
    job_params: Obj = Field(default_factory=dict, alias="jobParams")
    project_details: ObjList = Field(default_factory=list, alias="projectDetails")
    project_name: Str = Field(default="", alias="projectName")
    service_name: Str = Field(default="", alias="serviceName")
    status: Str = ""
    status_description: Str = Field(default="", alias="statusDescription")
    step_code: Str = Field(default="", alias="stepCode")
    step_time: Float = Field(default=0.0, alias="stepTime")
    sub_action: Str = Field(default="", alias="subAction")
    updated_at: Str = Field(default="", alias="updatedAt")
    user_name: Str = Field(default="", alias="userName")


class ApplicationDeployment(Payload):
    """Endpoint 2 -- ``GET /v1/inference/get_application_deployment/{id}``.

    One deployment of one application. ``compute_alias`` is spelled in snake_case by
    the producer while everything around it is camelCase; that is preserved as sent.
    """

    id: Str = Field(default="", alias="_id")
    lpr_server_id: Str = Field(default="", alias="_idLPRServer")
    access_scale: Str = Field(default="", alias="accessScale")
    account_number: Str = Field(default="", alias="accountNumber")
    app_id: Str = Field(default="", alias="appId")
    app_name: Str = Field(default="", alias="appName")
    app_version: Str = Field(default="", alias="appVersion")
    camera_ids: StrList = Field(default_factory=list, alias="cameraIds")
    compute_alias: Str = ""
    created_at: Str = Field(default="", alias="createdAt")
    deploy_type: Str = Field(default="", alias="deployType")
    deployments: ObjList = Field(default_factory=list)
    facial_recognition_id: Str = Field(default="", alias="facialRecognitionId")
    runtime_framework: Str = Field(default="", alias="runtimeFramework")
    server_type: Str = Field(default="", alias="serverType")
    start_time: Str = Field(default="", alias="startTime")
    status: Str = ""
    updated_at: Str = Field(default="", alias="updatedAt")


class Application(Payload):
    """Endpoint 3 -- ``GET /v1/applications/{id}``.

    The application catalogue entry. Mostly presentation metadata; this package reads
    the version fields. Note ``applicationid``, all lowercase, as the producer spells
    it.
    """

    app_type: Str = Field(default="", alias="appType")
    application_id: Str = Field(default="", alias="applicationid")
    alert: Obj = Field(default_factory=dict)
    analytics_config: Obj = Field(default_factory=dict, alias="analyticsConfig")
    blog_link: Str = Field(default="", alias="blogLink")
    business_analytics: Obj = Field(default_factory=dict, alias="businessAnalytics")
    business_decisions: ObjList = Field(default_factory=list, alias="businessDecisions")
    categories: StrList = Field(default_factory=list)
    cover_image: Str = Field(default="", alias="coverImage")
    created_at: Str = Field(default="", alias="createdAt")
    current_version: Str = Field(default="", alias="currentVersion")
    demos: ObjList = Field(default_factory=list)
    description: Str = ""
    fps_requirements: Obj = Field(default_factory=dict, alias="fpsRequirements")
    ground_truth_dataset: Obj = Field(default_factory=dict, alias="groundTruthDataset")
    ground_truth_video: Str = Field(default="", alias="groundTruthVideo")
    incident_types: Obj = Field(default_factory=dict, alias="incidentTypes")
    industries: StrList = Field(default_factory=list)
    instant_alert_name: Str = Field(default="", alias="instantAlertName")
    is_featured: Bool = Field(default=False, alias="isFeatured")
    key_drivers: StrList = Field(default_factory=list, alias="keyDrivers")
    maintained_by: Str = Field(default="", alias="maintainedBy")
    models: ObjList = Field(default_factory=list)
    name: Str = ""
    notebook_link: Str = Field(default="", alias="notebookLink")
    objects: StrList = Field(default_factory=list)
    output_type: Str = Field(default="", alias="outputType")
    preview: Obj = Field(default_factory=dict)
    published_at: Str = Field(default="", alias="publishedAt")
    published_by: Str = Field(default="", alias="publishedBy")
    published_version: Str = Field(default="", alias="publishedVersion")
    rejection_reason: Str = Field(default="", alias="rejectionReason")
    release_stage: Str = Field(default="", alias="releaseStage")
    reset_settings: Obj = Field(default_factory=dict, alias="resetSettings")
    reviewed_by: Str = Field(default="", alias="reviewedBy")
    server_type: Str = Field(default="", alias="serverType")
    status: Str = ""
    submitted_for_review_at: Str = Field(default="", alias="submittedForReviewAt")
    technical_requirements: Obj = Field(default_factory=dict, alias="technicalRequirements")
    updated_at: Str = Field(default="", alias="updatedAt")


class PostProcessingConfig(Payload):
    """Endpoints 4 and 5 -- the post-processing config for one camera and application.

    Both routes return this same record, because there is exactly one config per
    ``(camera, application)`` pair::

        GET /v1/inference/post_processing_configs/by_app_deployment/{id}  -> a list
        GET /v1/inference/post_processing_config?cameraId=&applicationId= -> one

    The first asks by deployment and gets every camera's config; the second asks by
    camera and application and gets that one. The second exists as a fallback: when
    ``app_deployment_id`` is stale the deployment-scoped query answers with an empty
    list, and the config is still reachable by its other key.

    ``post_processing`` stays an untyped dict -- it carries per-usecase settings,
    including the zone geometry, and has no fixed shape.
    """

    id: Str = Field(default="", alias="_id")
    app_deployment_id: Str = Field(default="", alias="_idAppDeployment")
    application_id: Str = Field(default="", alias="_idApplication")
    camera_id: Str = Field(default="", alias="_idCamera")
    created_at: Str = Field(default="", alias="createdAt")
    post_processing: Obj = Field(default_factory=dict, alias="postProcessing")
    updated_at: Str = Field(default="", alias="updatedAt")


class UsecaseDownload(Payload):
    """Endpoints 6 and 7 -- a time-limited grant to download a usecase bundle.

    Two routes reach the same grant: ``/v1/applications/license/{id}/versions/
    {version}/usecase/download`` for a licensed application, and the same path
    without ``license/`` otherwise. The producer declares one schema for both.
    """

    download_url: Str = Field(default="", alias="downloadUrl")
    expires_in: Int = Field(default=0, alias="expiresIn")


class CameraLocation(Payload):
    """Endpoint 8 -- ``GET /v1/inference/get_location/{id}``.

    The site a camera belongs to. ``location_name`` is what callers display, and
    ``normalise_location_id`` below is why the id is worth typing: the platform
    writes an all-zero ObjectId for an unset location rather than omitting the key,
    and that placeholder must read as absent, not as an id.
    """

    id: Str = ""
    account_number: Str = Field(default="", alias="accountNumber")
    cluster_site_id: Str = Field(default="", alias="clusterSiteId")
    created_at: Str = Field(default="", alias="createdAt")
    description: Str = ""
    location_info: Obj = Field(default_factory=dict, alias="locationInfo")
    location_name: Str = Field(default="", alias="locationName")
    timezone: Str = ""
    updated_at: Str = Field(default="", alias="updatedAt")

    @field_validator("id", mode="after")
    @classmethod
    def _normalise_id(cls, value: str) -> str:
        """Blank the all-zero placeholder, so an unset location reads as unset."""
        return normalise_location_id(value)

    @field_validator("location_name", mode="after")
    @classmethod
    def _blank_raw_object_id(cls, value: str) -> str:
        """Blank a name that is really an id.

        When the platform has no display name it sometimes echoes the location's
        ObjectId into the name field. Showing a user ``68f28be1f74ae116727448c4`` is
        worse than showing nothing, so a bare 24-hex value is treated as no name.
        """
        return "" if looks_like_object_id(value) else value


class RedisServer(Payload):
    """Endpoint 9 -- ``GET /v1/actions/get_redis_server_by_instance_id/{id}``.

    Connection details for the Redis this instance publishes to. ``port`` is declared
    as a **string** here, unlike the two server records below which declare it as an
    integer; that inconsistency is the producer's and is preserved.
    """

    id: Str = ""
    access_scale: Str = Field(default="", alias="accessScale")
    alias: Str = ""
    created_at: Str = Field(default="", alias="createdAt")
    host: Str = ""
    parent_server_id: Str = Field(default="", alias="parentServerId")
    password: Str = ""
    port: Str = ""
    sentinel_config: Obj = Field(default_factory=dict, alias="sentinelConfig")
    service_id: Str = Field(default="", alias="serviceId")
    status: Str = ""
    updated_at: Str = Field(default="", alias="updatedAt")


class FacialRecognitionServer(Payload):
    """Endpoints 10 and 12 -- the facial-recognition sidecar's server record.

    Endpoint 10 (``GET .../get_facial_recognition_server/{id}``) reads it; endpoint
    12 (``PUT .../update_facial_recognition_deployment/{id}``) updates the deployment
    and echoes the same record back. The producer declares one schema for both.

    ``host`` and ``port`` are what the sidecar's base URL is built from.
    """

    id: Str = ""
    account_number: Str = Field(default="", alias="accountNumber")
    compute_alias: Str = Field(default="", alias="computeAlias")
    host: Str = ""
    is_shared: Bool = Field(default=False, alias="isShared")
    name: Str = ""
    port: Int = 0
    project_id: Str = Field(default="", alias="projectID")
    region: Str = ""
    status: Str = ""


class LprServer(Payload):
    """Endpoint 11 -- ``GET /v1/actions/lpr_servers/{id}``.

    The licence-plate server's record, the same shape as the facial-recognition one
    minus ``computeAlias``. The two are **not** shared: the producer declares them
    separately, and a field added to one would not appear on the other.
    """

    id: Str = ""
    account_number: Str = Field(default="", alias="accountNumber")
    host: Str = ""
    is_shared: Bool = Field(default=False, alias="isShared")
    name: Str = ""
    port: Int = 0
    project_id: Str = Field(default="", alias="projectID")
    region: Str = ""
    status: Str = ""


class Camera(Payload):
    """Endpoint 13 -- ``GET /v1/inference/get_camerastream_by_acc_number/{acc}``.

    One camera stream. The route answers with every camera on the account, so callers
    filter this list by id rather than asking for one.

    This package reads the display fields -- ``camera_name``, ``camera_group_id``,
    ``location_id`` -- and ``custom_stream_settings`` for the frame resolution. The
    rest is declared so the model matches what the producer publishes.
    """

    id: Str = ""
    team_owned_ids: StrList = Field(default_factory=list, alias="_idTeamOwned")
    team_owner_camera_id: Str = Field(default="", alias="_idTeamOwnerCamera")
    account_number: Str = Field(default="", alias="accountNumber")
    applications: ObjList = Field(default_factory=list)
    base_video_storage_compute_id: Str = Field(default="", alias="baseVideoStorageComputeId")
    base_video_storage_mode: Str = Field(default="", alias="baseVideoStorageMode")
    camera_codec: Str = Field(default="", alias="cameraCodec")
    camera_feed_path: Str = Field(default="", alias="cameraFeedPath")
    camera_group_id: Str = Field(default="", alias="cameraGroupId")
    camera_name: Str = Field(default="", alias="cameraName")
    camera_stream_schedule: ObjList = Field(default_factory=list, alias="cameraStreamSchedule")
    cluster_name: Str = Field(default="", alias="clusterName")
    compute_alias: Str = Field(default="", alias="computeAlias")
    created_at: Str = Field(default="", alias="createdAt")
    current_compute_id: Str = Field(default="", alias="currentComputeId")
    custom_schedule: Bool = Field(default=False, alias="customSchedule")
    custom_stream_settings: Obj = Field(default_factory=dict, alias="customStreamSettings")
    health: Str = ""
    is_active: Bool = Field(default=False, alias="isActive")
    is_relay: Bool = Field(default=False, alias="isRelay")
    lan_id: Str = Field(default="", alias="lanId")
    location_id: Str = Field(default="", alias="locationId")
    media_storage_id: Str = Field(default="", alias="mediaStorageId")
    memory_usage_mb: Float = Field(default=0.0, alias="memoryUsageMB")
    playback_mode: Str = Field(default="", alias="playbackMode")
    primary_compute_id: Str = Field(default="", alias="primaryComputeId")
    protocol_type: Str = Field(default="", alias="protocolType")
    recording_mode: Str = Field(default="", alias="recordingMode")
    recording_status: Str = Field(default="", alias="recordingStatus")
    relay_camera_feed_path: Str = Field(default="", alias="relayCameraFeedPath")
    secondary_compute_id: Str = Field(default="", alias="secondaryComputeId")
    simulation_video_path: Str = Field(default="", alias="simulationVideoPath")
    simulation_video_paths: StrList = Field(default_factory=list, alias="simulationVideoPaths")
    site_id: Str = Field(default="", alias="siteId")
    sitemap: Obj = Field(default_factory=dict)
    sitemap_node_id: Str = Field(default="", alias="sitemapNodeId")
    sitemap_site_id: Str = Field(default="", alias="sitemapSiteId")
    storage_path: Str = Field(default="", alias="storagePath")
    streaming_gateway_id: Str = Field(default="", alias="streamingGatewayId")
    updated_at: Str = Field(default="", alias="updatedAt")

    @field_validator("location_id", mode="after")
    @classmethod
    def _normalise_location(cls, value: str) -> str:
        """Blank the all-zero placeholder, so a camera with no location reads as such."""
        return normalise_location_id(value)


# ---------------------------------------------------------------------------
# lpr-server response -- endpoint 24
# ---------------------------------------------------------------------------


class Detection(Payload):
    """Endpoint 24 -- the document created by ``POST /v1/lpr-server/detections``.

    lpr-server answers a successful create with **201** and the created document
    itself, with no ``{success, data}`` envelope around it. It declares ``201`` and
    ``500`` and no ``4xx`` at all, so any non-201 is a failure; the status codes it
    happens to declare are not the set it can return.

    The reply does not echo the OCR confidence that was sent.
    """

    id: Str = ""
    application_id: Str = Field(default="", alias="applicationId")
    bbox: ObjList = Field(default_factory=list)
    bolo: Bool = False
    camera: Str = ""
    capture_timestamp: Str = Field(default="", alias="captureTimestamp")
    created_at: Str = Field(default="", alias="createdAt")
    frame_ids: StrList = Field(default_factory=list, alias="frameIds")
    frames: ObjList = Field(default_factory=list)
    license_plate: Str = Field(default="", alias="licensePlate")
    location: Str = ""
    metadata: Obj = Field(default_factory=dict)
    project_id: Str = Field(default="", alias="projectId")
    team_id: Str = Field(default="", alias="teamId")
    updated_at: Str = Field(default="", alias="updatedAt")


# ---------------------------------------------------------------------------
# Facial-recognition sidecar responses -- endpoints 14 to 23
#
# UNVERIFIED as a group: the sidecar publishes no OpenAPI schema for any of these,
# so nothing diffs these models against the producer. The `actions` spec declares
# look-alike routes under /v1/actions/facial_recognition/...; those are stale and
# scheduled for removal, two of them are even word-rearranged, and they are NOT the
# source for anything here. Every field below was read off a caller.
# ---------------------------------------------------------------------------


class StaffEnrollResult(Payload):
    """Endpoint 14 -- the reply to ``POST /v1/facial_recognition/staff/enroll``.

    UNVERIFIED, and **no field is observed**. The caller checks only the envelope's
    ``success``/``error``, which the response layer already handles, so nothing in
    this package reads the payload. Fields belong here once a caller needs one, or
    once the sidecar publishes a schema -- guessing at the created staff record would
    give an invention the standing of a contract.
    """


class SimilarFaceMatch(Payload):
    """Endpoint 15 -- one match from ``POST /v1/facial_recognition/search/similar``.

    The payload is a **list** of these, ordered best-first; the caller logs the top
    match and passes the rest on.

    UNVERIFIED, and partial: ``staff_id`` and ``score`` are the two fields a caller
    reads. The sidecar sends more per match -- the search is what decides known from
    unknown -- but nothing here reads it, so nothing more is declared.
    """

    staff_id: Str = Field(default="", alias="staffId")
    score: Float = 0.0


class StaffDetails(Payload):
    """Endpoint 16 -- the reply to ``GET /v1/facial_recognition/staff/{staffId}``.

    UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.
    See ``StaffEnrollResult`` for why the record is not guessed at.
    """


class StaffImageUpdateResult(Payload):
    """Endpoint 18 -- the reply to ``PUT /v1/facial_recognition/staff/update_images``.

    UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.
    """


class ServiceShutdownResult(Payload):
    """Endpoint 19 -- the reply to ``DELETE /v1/facial_recognition/shutdown``.

    UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.
    """


class StaffEmbedding(Payload):
    """Endpoint 20 -- one enrolled face from ``GET .../get_all_staff_embeddings``.

    The payload is a list of these, loaded once into the matcher's matrix rather than
    per frame.

    UNVERIFIED, but every field here is read by the loader, which is unusually
    defensive about them and worth reproducing exactly:

    * ``embedding`` is the only field that can make the loader skip a record. A
      record is dropped when it is absent, not a list, empty, holds anything that
      will not convert to a float, or has a length differing from the first record's.
      The model keeps the non-convertible case tolerant -- a bad vector becomes
      ``[]`` -- and leaves the skipping to the loader, which is where the
      dimension-consistency rule lives.
    * ``employee_id`` arrives as something other than a string often enough that the
      loader wraps it in ``str()``; it is a raw ObjectId on at least one path. The
      declared ``str`` plus number coercion covers that.
    * ``is_active`` defaults to **True**. An absent flag means active -- the loader
      skips only on an explicit ``False`` -- so the default must not be ``False``.
    """

    embedding_id: Str = Field(default="", alias="embeddingId")
    staff_id: Str = Field(default="", alias="staffId")
    employee_id: Str = Field(default="", alias="employeeId")
    embedding: FloatList = Field(default_factory=list)
    staff_details: Obj = Field(default_factory=dict, alias="staffDetails")
    is_active: Bool = Field(default=True, alias="isActive")


class UnknownPersonEnrollResult(Payload):
    """Endpoint 21 -- the reply to ``POST .../enroll_unknown_person``.

    UNVERIFIED, and **no field is observed** -- the caller reads only the envelope.
    """


class HealthStatus(Payload):
    """Endpoint 22 -- the reply to ``GET /v1/facial_recognition/health``.

    UNVERIFIED, and **no field is observed**. The caller treats the envelope's
    ``success`` as the entire answer, so liveness is all this endpoint reports here
    however much detail the sidecar may send.
    """


class RedisDetails(Payload):
    """Endpoint 23 -- the reply to ``GET /v1/facial_recognition/get_redis_details``.

    Where the sidecar publishes recognition events. UNVERIFIED, but all three fields
    are read by the caller, which builds a Redis connection from them.

    The wire names are SCREAMING_CASE, unlike every other payload here; that is how
    the sidecar sends them. ``port`` arrives as a string on at least one deployment
    and is converted by the caller, so it is declared ``int`` and tolerates both. An
    empty ``password`` means no password rather than an empty one.
    """

    host: Str = Field(default="", alias="REDIS_IP")
    port: Int = Field(default=0, alias="REDIS_PORT")
    password: Str = Field(default="", alias="REDIS_PASSWORD")


# ---------------------------------------------------------------------------
# Request bodies -- the 7 endpoints that send one
#
# Serialise with model_dump(by_alias=True, exclude_none=True): an unset optional
# field must be ABSENT from the JSON, which is what the call sites build today.
# ---------------------------------------------------------------------------


class StaffEnrollRequest(Body):
    """Endpoint 14 -- ``POST /v1/facial_recognition/staff/enroll``.

    UNVERIFIED: no published schema, so "required" here means "always sent today",
    not "required by the producer".

    ``images`` are base64-encoded JPEGs. The caller reads them from disk and encodes
    them before building this, so a file that cannot be read never reaches the model.
    """

    staff_id: str = Field(default="", alias="staffId")
    first_name: str = Field(default="", alias="firstName")
    last_name: str = Field(default="", alias="lastName")
    email: str = ""
    position: str = ""
    department: str = ""
    images: list[str] = Field(default_factory=list)


class SimilarFaceSearchRequest(Body):
    """Endpoint 15 -- ``POST /v1/facial_recognition/search/similar``.

    UNVERIFIED: no published schema.

    ``collection`` defaults to ``staff_embeddings`` and a test pins that default --
    searching the wrong collection returns plausible matches from the wrong set,
    which is worse than returning none. ``location`` and ``timestamp`` are omitted
    entirely when empty, so they are ``None``-defaulted rather than ``""``.
    """

    embedding: list[float] = Field(default_factory=list)
    collection: str = "staff_embeddings"
    threshold: float = 0.3
    limit: int = 10
    images_required: bool = False
    location: str | None = None
    timestamp: str | None = None


class PeopleActivityRequest(Body):
    """Endpoint 17 -- ``POST /v1/facial_recognition/store_people_activity``.

    UNVERIFIED: no published schema. The wire spelling is mixed -- ``staff_id`` and
    ``camera_name`` in snake_case beside ``applicationId`` and ``rtpNumber`` in
    camelCase -- and is reproduced exactly as sent rather than tidied.

    Two things the caller does that this model preserves:

    * ``employee_id`` and ``anonymous_id`` are **mutually exclusive**, chosen by
      whether the detection was of a known or an unknown person. Both default to
      ``None`` so only the one that applies is serialised.
    * ``confidence_score`` is the only score field the sidecar binds from the wire.
      A similarity score sent under any other name is accepted and discarded.

    Image bytes are deliberately not part of this body. The sidecar fetches the frame
    itself from the media server using ``rtp_number`` and ``camera_id``.
    """

    staff_id: str = ""
    type: str = ""
    timestamp: str = ""
    bbox: list[Any] = Field(default_factory=list)
    location: str = ""
    camera_name: str = ""
    camera_id: str = ""
    application_id: str = Field(default="", alias="applicationId")
    rtp_number: str = Field(default="", alias="rtpNumber")
    employee_id: str | None = None
    anonymous_id: str | None = None
    confidence_score: float | None = Field(default=None, alias="confidenceScore")


class StaffImageUpdateRequest(Body):
    """Endpoint 18 -- ``PUT /v1/facial_recognition/staff/update_images``.

    UNVERIFIED: no published schema. ``image_url`` points at an image already
    uploaded elsewhere; the bytes do not travel in this body.
    """

    image_url: str = Field(default="", alias="imageUrl")
    employee_id: str = Field(default="", alias="employeeId")


class ServiceShutdownRequest(Body):
    """Endpoint 19 -- ``DELETE /v1/facial_recognition/shutdown``.

    UNVERIFIED: no published schema. One optional field, and it must be **absent**
    rather than ``null`` when there is no action record to name -- the caller sends
    ``{}`` in that case. ``exclude_none`` on serialisation is what reproduces it.
    """

    action_record_id: str | None = Field(default=None, alias="actionRecordId")


class UnknownPersonEnrollRequest(Body):
    """Endpoint 21 -- ``POST /v1/facial_recognition/enroll_unknown_person``.

    UNVERIFIED: no published schema.

    ``timestamp`` is unlike the other optional fields: the caller substitutes the
    current UTC time when none is given, so it is always sent. ``image_source`` and
    ``location`` are omitted when empty.
    """

    embedding: list[float] = Field(default_factory=list)
    timestamp: str = ""
    image_source: str | None = Field(default=None, alias="imageSource")
    location: str | None = None


class CreateDetectionRequest(Body):
    """Endpoint 24 -- ``POST /v1/lpr-server/detections``.

    The one request body with a producer-declared schema, and the only endpoint of
    the twenty-four whose producer requires anything: ``projectId``, ``licensePlate``,
    ``frameId``, ``cameraId``, ``applicationId`` and ``rtpNumber``. Those six are
    required here; the rest are optional because the producer says so.

    ``coerce_numbers_to_str`` is the point of this model. A numeric ``frame_id``
    reaching the producer's string field is rejected with ``cannot unmarshal number
    into Go struct field CreateDetectionRequest.frameId of type string`` and the
    sighting is lost -- nothing upstream guarantees the type, since the frame id is
    stored as it was passed. Converting it is the fix, declared once here instead of
    written by hand at one call site among several.

    ``confidence`` is the name the producer declares for the OCR confidence;
    ``ocr_confidence`` appears in its schema zero times. ``image_data`` is sent but
    declared nowhere by the producer, and is kept because it is what the caller sends.
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True, coerce_numbers_to_str=True)

    project_id: str = Field(alias="projectId")
    license_plate: str = Field(alias="licensePlate")
    frame_id: str = Field(alias="frameId")
    camera_id: str = Field(alias="cameraId")
    application_id: str = Field(alias="applicationId")
    rtp_number: int = Field(alias="rtpNumber")
    location: str = ""
    camera: str = ""
    capture_timestamp: str = Field(default="", alias="captureTimestamp")
    image_data: str = Field(default="", alias="imageData")
    bbox: list[Any] | None = None
    confidence: float | None = None


def looks_like_object_id(value: Any) -> bool:
    """True when ``value`` is 24 hex characters, the shape of a Mongo id.

    Used to spot an id that has been put where a human-readable name belongs.
    """
    if value is None:
        return False
    return bool(_OBJECT_ID_RE.match(str(value).strip()))


def normalise_location_id(value: Any) -> str:
    """A stripped location id, or ``""`` when there is no location.

    The platform represents "no location" two ways: the key is missing, or it holds
    an all-zero ObjectId. Both must read as absent, because the placeholder is a
    valid-looking id that matches no location and would otherwise be looked up.
    """
    if value is None:
        return ""
    text = str(value).strip()
    if not text or text.lower() == _NULL_OBJECT_ID:
        return ""
    return text


__all__ = [
    "ActionRecord",
    "Application",
    "ApplicationDeployment",
    "Body",
    "Camera",
    "CameraLocation",
    "CreateDetectionRequest",
    "Detection",
    "FacialRecognitionServer",
    "HealthStatus",
    "LprServer",
    "Payload",
    "PeopleActivityRequest",
    "PostProcessingConfig",
    "RedisDetails",
    "RedisServer",
    "ServiceShutdownRequest",
    "ServiceShutdownResult",
    "SimilarFaceMatch",
    "SimilarFaceSearchRequest",
    "StaffDetails",
    "StaffEmbedding",
    "StaffEnrollRequest",
    "StaffEnrollResult",
    "StaffImageUpdateRequest",
    "StaffImageUpdateResult",
    "UnknownPersonEnrollRequest",
    "UnknownPersonEnrollResult",
    "UsecaseDownload",
    "looks_like_object_id",
    "normalise_location_id",
]
