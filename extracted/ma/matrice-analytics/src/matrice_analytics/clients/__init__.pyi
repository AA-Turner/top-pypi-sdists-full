"""Stub file for clients directory."""
from typing import Any, Callable, Dict, List, Optional, Tuple

from .actions_api import ActionsApi
from .applications_api import ApplicationsApi
from .bootstrap import attach_session
from .bootstrap import attach_session, get_action_id, get_action_record
from .bootstrap import attach_session, license_key, resolve_action_id
from .bootstrap import get_action_record
from .identity import APP_DEPLOYMENT_ID_KEYS, APPLICATION_ID_KEYS, APPLICATION_VERSION_KEYS, config_get
from .identity import resolve_project_id, resolve_sidecar_base_url
from .identity import resolve_sidecar_base_url
from .inference_api import InferenceApi
from .models import ActionRecord, RedisServer
from .models import Application
from .models import ApplicationDeployment, Camera, CameraLocation, PostProcessingConfig
from .models import CreateDetectionRequest, Detection, LprServer
from .models import FacialRecognitionServer, HealthStatus, PeopleActivityRequest, RedisDetails, ServiceShutdownRequest, ServiceShutdownResult, SimilarFaceMatch, SimilarFaceSearchRequest, StaffDetails, StaffEmbedding, StaffEnrollRequest, StaffEnrollResult, StaffImageUpdateRequest, StaffImageUpdateResult, UnknownPersonEnrollRequest, UnknownPersonEnrollResult
from .response import CallFailure
from .response import CallFailure, ConnectionLost, MalformedReply, RateLimited
from .response import CallFailure, unwrap_fr_sidecar, unwrap_platform
from .response import CallFailure, unwrap_lpr_server, unwrap_platform
from .response import CallFailure, unwrap_platform
from .response import unwrap_platform
from .transport import LICENSE_KEY_HEADER, _describe, _rpc_data, _rpc_headed, _rpc_model, backend_base_url
from .transport import POOLED_POST_TIMEOUT_S, PooledPoster, _rpc_model
from .transport import Uploader, _rpc_model, _rpc_sent, backend_base_url
from .transport import _report_failure
from .transport import _rpc_data
from .transport import _rpc_model

# Constants
logger: Any = ...  # From analytics_client
ACTION_DETAILS_PATH: str = ...  # From bootstrap
ENV_ACTION_ID: str = ...  # From bootstrap
ENV_ACTION_ID_BARE: str = ...  # From bootstrap
ENV_LICENSE_KEY: str = ...  # From bootstrap
USR_SRC: str = ...  # From bootstrap
logger: Any = ...  # From bootstrap
logger: Any = ...  # From fr_client
logger: Any = ...  # From lpr_client
Bool: Any = ...  # From models
Float: Any = ...  # From models
FloatList: Any = ...  # From models
Int: Any = ...  # From models
Obj: Any = ...  # From models
ObjList: Any = ...  # From models
Str: Any = ...  # From models
StrList: Any = ...  # From models
ENV_API_BASE: str = ...  # From transport
LICENSE_KEY_HEADER: str = ...  # From transport
LOCAL_AUTHORITY_PREFIXES: Tuple[Any, ...] = ...  # From transport
POOLED_POST_TIMEOUT_S: float = ...  # From transport
SERVICE_NAME: str = ...  # From transport
UPLOAD_TIMEOUT_S: float = ...  # From transport
logger: Any = ...  # From transport

# Functions
# From bootstrap
def attach_session(session: Any = None) -> Any:
    """
    The session a client should ride on: the caller's, the process's, or ``None``.
    
        What every client in this package does at construction, in one place, because there are
        three of them and the shape below is easy to get subtly wrong.
    
        A client built on a machine with **no platform SDK** constructs successfully and has no
        session, rather than raising at construction. That is the intended outcome: an
        analytics-only container should be able to build one of these and skip the
        backend-dependent work, not die for want of a package it never meant to use.
    
        **Missing credentials are not the same as a missing SDK, and this does not conflate them.**
        An SDK that is absent means the caller never intended to reach the platform, so it
        degrades. Credentials that are absent mean the caller *did* intend to and cannot, so
        :func:`open_session` raises and that raise travels -- a silent ``None`` there would be
        reported three frames later as a missing session rather than as a missing key.
    
        **Why the import is inside the function.** The usual shape is a module-level
        ``try: from ... import Session`` with a ``Session = None`` fallback, and it has to be right
        in both halves -- the name bound on failure *and* every use checking it. Of the six sites
        in this repository that guard this import, two are broken in exactly that way: one never
        binds the name, so it raises ``NameError``; another sets its availability flag outside the
        ``try``, so the flag is always true and the call raises ``TypeError: 'NoneType' object is
        not callable``. Both surface far from the missing package. Importing here has no name to
        bind and no flag to keep in step, so neither mistake is available.
    
        Args:
            session: A session the caller already holds. Returned untouched -- a client handed one
                opens nothing of its own, which is what lets a test run with no platform at all.
            what: What the session is for, named in the log line and in any failure, so a reader
                sees which client wanted it.
    
        Returns:
            The session, or ``None`` when ``matrice_common`` is not importable.
    
        Raises:
            CallFailure: The SDK is present but no session could be opened -- no credentials in
                this process, or the exchange itself failed.
    """
    ...

# From bootstrap
def get_action_id(env: Optional[Any[str, str]] = None, argv: Optional[Any[str]] = None) -> Optional[str]:
    """
    The action record id for this worker, from every source there is.
    
        The four sources, cheapest first:
    
        1. ``$MATRICE_ACTION_ID`` -- an operator setting it means it,
        2. ``$ACTION_ID`` -- the bare name the Go services and the ENV_ID_ACTIONS images read,
        3. ``sys.argv`` -- py_compute launches every action container as
           ``python3 <entrypoint>.py <action_record_id> <port>``,
        4. the filesystem -- the working directory's name, its parents', then ``/usr/src``.
    
        The first three are :func:`resolve_action_id` and cost nothing. The fourth is
        :func:`scrape_action_id`, walks directories, and matches a looser shape, so it runs only
        when the first three have all missed -- which on a correctly launched container is never.
    
        Args:
            env: The environment to read. Defaults to the process's own.
            argv: The argument list to read. Defaults to the process's own.
    
        Returns:
            The id, or ``None`` when no source knew it. ``None`` is a refusal, not a default:
            a caller that invented one would read a different worker's record.
    """
    ...

# From bootstrap
def get_action_record(action_id: Optional[str] = None) -> Dict[str, Any]:
    """
    This worker's action record: one round trip on the first call, memory after that.
    
        ``action_id`` defaults to :func:`resolve_action_id` -- the action this container was
        launched as, which is the one every caller in it wants. Passing an id asks about a
        different action and gets its own entry. ``session`` lets a caller that already holds one
        read the record on it rather than on the process session; entries are keyed by action id
        alone, because the document does not depend on who read it.
    
        Raises :class:`~.response.CallFailure` when no id can be resolved, rather than answering
        with an empty record: a caller handed ``{}`` goes looking for a backend that dropped every
        field, when the fault is a container launched without its id.
    
        Read once and then kept for the life of the process, because the record describes a launch
        that has already finished -- reading it again cannot tell this process anything new -- and
        because every consumer wants the same one. A container running one usecase across forty
        cameras builds forty instances at startup, each needing ``jobParams``; without this that is
        forty GETs of one document through a connection pool of twenty, on the slowest path a
        container has. They arrive together, hence the same double-checked locking as
        :func:`get_session`. A failure is **not** kept, so a container that starts before the
        platform will answer recovers on the next call instead of stranding every camera in it.
        There is deliberately no every-call counterpart, for the same reason there is a cache at
        all: a session can go bad, a finished launch cannot.
    
        Returns the document as a plain ``dict``, deliberately untyped: this is the cache of what
        the platform said at launch, while the response models declare a fixed set of fields and
        rewrite some of the values they keep. Typing it here would drop a field the platform adds,
        at the one place whose whole purpose is to report what the container was handed. A caller wanting the
        typed view builds the model from this return value, and that order matters: building a
        model replaces only the outermost mapping and keeps the nested values exactly as they
        arrive, so a model built from the stored record would hand back objects that record still
        holds.
    
        **Every caller gets its own copy of the whole document, nested values included.** Copying
        only the outer dictionary is not enough here: every field callers read lives inside
        ``jobParams`` or ``actionDetails``, and those would still be the stored objects, so one
        caller editing a list in there would change what the next forty read. Copying all the way
        down is possible because the document holds nothing but dictionaries, lists, strings and
        numbers. A read-only view (``types.MappingProxyType``) is the obvious cheaper answer and
        the wrong one: it is not a ``dict``, so a caller that checks ``isinstance(..., dict)``
        before reading would reject it and substitute an empty document.
    
        Copying is affordable *because the call count is single-digit per consumer and nothing on
        the frame path reaches this*, and that condition matters because the cost is not flat: it
        tracks what ``actionDetails`` and ``jobParams`` carry, not how many fields the record has.
        A bare record copies in tens of microseconds, one carrying a site's camera list and zone
        polygons in hundreds. Forty consumers at startup is milliseconds; the same call in a
        per-frame loop is seconds per ten thousand frames. A caller needing it in a loop should
        read it once and hold it, and this docstring is the only thing that will say so.
    
        The reason to copy at all is a known one rather than a precaution: nothing here notices
        when the platform's ``status`` moves on, so the stored record is already out of date in
        that one field by design, and copying is what stops a caller correcting it by writing the
        new value onto a document every other consumer is reading.
    """
    ...

# From bootstrap
def get_session(what: str = 'the platform session') -> Any:
    """
    The process's one ``matrice_common`` session, built on first use.
    
        Lazy because a container that never needs the platform should never pay for a session, and
        should not fail at import time for want of credentials it does not use. Built once per
        *process*, not per caller: sessions are built from the same two environment variables
        wherever they are opened, so a second one is the same handle at the cost of another
        credential exchange.
    
        Thread-safe under the double-checked pattern -- the fast path is a bare read once the
        session exists, and the lock is taken only while the process is still cold.
    
        A failure is **not** kept: ``_SESSION`` is assigned only on success, so a container that
        starts before its credentials are mounted recovers on the next call instead of being stuck
        with the first error for its lifetime.
    """
    ...

# From bootstrap
def license_key(env: Optional[Any[str, str]] = None) -> str:
    """
    The deployment's licence key, or ``""`` when it has none.
    
        The cheapest thing in this module: one environment read, no ``argv``, no filesystem and no
        session. It is here rather than with the single route that sends it for the same reason
        :func:`resolve_action_id` is -- both answer *what was this container handed at startup?*, and
        a route that read its own credential would be resolving something it was supposed to be given.
    
        ``""`` is a real answer and not a fault. A deployment without a licence is the ordinary
        unlicensed case, and the caller's business is to take the other route rather than to report a
        misconfiguration -- which is why this returns a blank instead of raising, unlike everything
        else here. Keeping that decision at the call site is what makes the alternative visible.
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
    The action record id for this worker, from the three sources that cost nothing.
    
        Three sources, no I/O. ``$MATRICE_ACTION_ID`` first, because an operator setting it means it,
        then ``$ACTION_ID`` -- the bare name the Go services and the ENV_ID_ACTIONS images read, and the
        only one some py_compute launch paths emitted. Then ``sys.argv``: py_compute launches every
        action container as ``python3 <entrypoint>.py <action_record_id> <port>``, so the id is the
        first argument that looks like an ObjectId. Matching on shape rather than position keeps this
        from mistaking a port or a flag for an id.
    
        A malformed value in either env var falls through rather than erroring, so a truncated id does
        not mask a good one in argv.
    
        .. note::
           :func:`get_action_id` is the fuller answer: the same three sources and then a
           filesystem scrape. This one is kept because it is what every current caller expects
           and because *"no I/O"* is a property some of them rely on -- a truthiness probe that
           only wants to know whether a lookup is possible should not walk ``/usr/src`` to find
           out.
    """
    ...

# From bootstrap
def scrape_action_id(cwd: Optional[Any] = None, usr_src: Optional[Any] = None) -> Optional[str]:
    """
    The action id read off the filesystem, when nothing else knew it.
    
        py_compute names a container's working directory after the action it is running, and the
        image keeps a directory per action under ``/usr/src``. So the id is often sitting in a
        path name even on a container whose environment lost it -- which is the case this exists
        for, and the reason four modules grew their own copy of this.
    
        The working directory is checked first, then each of its parents outward, then the
        children of ``/usr/src``. Nearest-first: a worker running inside its own action's
        directory should answer with that action, not with whichever ``/usr/src`` entry happens
        to be listed first.
    
        **This one touches the filesystem**, which is why it is separate from
        :func:`resolve_action_id` rather than folded into it. A failure in either walk is
        non-fatal and falls through to the next: an unlinked working directory raises ``OSError``
        from ``Path.cwd()``, and ``/usr/src`` does not exist outside the container image.
    
        **It matches a looser shape than the other sources**, and deliberately: eight or more hex
        characters rather than a full 24-character ObjectId. That is what all four existing copies
        match, reproduced rather than tightened, because tightening it would change the behaviour
        of every caller being migrated onto this. The cost is real -- an eight-character hex
        directory name that is *not* an action id will be returned as one, and the read that
        follows will fail against the platform rather than here. It is the last source for that
        reason.
    
        Args:
            cwd: The directory to start from. Defaults to the process's own.
            usr_src: The image's action directory. Defaults to ``/usr/src``.
    
        Returns:
            The first candidate that looks like an id, or ``None``.
    """
    ...

# From identity
def config_get(config: Any, keys: Any[str]) -> Optional[str]:
    """
    First non-empty string among ``keys``, from a dict or an attribute-bearing object.
    
        Both shapes are real and this is why the function exists: ``PostProcRunner`` passes the raw
        ``post_processing_config`` dict, while ``PostProcessor`` passes a *parsed* config object. A
        dict-only reader -- which is what ``backends._config_value`` is -- would make the two SDK entry
        points disagree about whether an app has a bundle, and keeping them in agreement is the entire
        reason ``select_engine_backend`` is a single function.
    
        Returns ``None`` rather than ``""`` for a miss, so a caller can chain with ``or`` and tell a
        source that answered blank from one that answered nothing.
    
        ``Mapping``, not ``dict``: a read-only view or a ``ChainMap`` is a mapping that is not a
        ``dict``, and testing for the concrete type sends it down the attribute branch, where it
        has no attribute to find and reads as empty. :func:`~.bootstrap.get_action_record` already
        pays a deep copy per call to avoid handing anyone a ``MappingProxyType`` for exactly this
        reason; the reader is the right place to fix it.
    """
    ...

# From identity
def first_str(data: Any[str, Any], keys: Any[str]) -> Optional[str]:
    """
    The first non-blank string among ``keys``, unwrapping ``{"$oid": ...}`` encodings.
    
        Mapping-only, unlike :func:`config_get`: its sources are documents that came back from the
        platform, which are always dictionaries. What it adds instead is the ``$oid`` unwrap -- some
        encoders render an ObjectId as ``{"$oid": "..."}`` rather than as a string, and without the
        unwrap that field reads as a miss and the caller goes looking for an answer it already had.
    """
    ...

# From identity
def resolve_app_deployment_id(stream_info: Optional[Any[str, Any]] = None, pp_config: Any = None, action_record: Optional[Callable[[], Any[str, Any]]] = None) -> str:
    """
    Which deployment this is, or ``""`` when no source knows.
    
        Same shape as :func:`resolve_application_id` with **the two record slices reversed**:
        ``actionDetails`` is searched before ``jobParams``. That is not a style choice -- the two
        slices carry different values for this field, and reading them in the other order answers
        with the wrong deployment rather than with nothing.
    
        Args:
            stream_info: The frame's own description, if there is one.
            pp_config: The raw post-processing config, if the caller holds one.
            action_record: A function returning this worker's action record; called only on a miss.
    
        Returns:
            The id, or ``""`` when no source knew.
    """
    ...

# From identity
def resolve_application_id(stream_info: Optional[Any[str, Any]] = None, pp_config: Any = None, action_record: Optional[Callable[[], Any[str, Any]]] = None) -> str:
    """
    Which application this is, or ``""`` when no source knows.
    
        Order, cheapest first:
    
        1. ``stream_info`` -- already in hand on the frame path,
        2. the **raw** post-processing config -- also in hand,
        3. the action record's ``jobParams``, then its ``actionDetails`` -- one round trip, and
           only if the first two missed.
    
        ``jobParams`` is searched **before** ``actionDetails``, and that order is specific to this
        field: :func:`resolve_app_deployment_id` searches the two the other way round. The record
        carries both slices and they disagree, so the order is per field rather than per record.
    
        The key is plain ``application_id`` at every step here. A post-processing config read back
        from the backend as a **document** spells it ``_idApplication`` instead; that is a
        different source with a different shape, and a caller holding one of those documents
        should read that field itself rather than pass it here as though it were a config.
    
        Args:
            stream_info: The frame's own description of what it belongs to, if there is one.
            pp_config: The raw post-processing config, if the caller holds one.
            action_record: A function returning this worker's action record. Called only if the
                two free sources miss, so the round trip is paid only when it buys something.
    
        Returns:
            The id, or ``""`` -- which means *no source knew*, and is a refusal rather than a
            value. Callers decide what to do about it; this function never invents one.
    """
    ...

# From identity
def resolve_application_version(stream_info: Optional[Any[str, Any]] = None, pp_config: Any = None, action_record: Optional[Callable[[], Any[str, Any]]] = None) -> str:
    """
    Which version of the application is deployed, or ``""`` when no source knows.
    
        The version travels with the application id on a ``deploy_add`` record, so the same order
        applies and the same round trip answers both. A ``deploy_postproc_add`` record carries no
        version at all, which is a miss rather than a fault -- the deployment record knows it, and
        that is a call the caller makes, not this function.
    
        **This is the version a deployment RUNS.** The application catalogue also publishes a
        version, and the two are routinely different; a caller that wants the published one is
        asking a different question.
    
        Args:
            stream_info: The frame's own description, if there is one.
            pp_config: The raw post-processing config, if the caller holds one.
            action_record: A function returning this worker's action record; called only on a miss.
    
        Returns:
            The version, or ``""`` when no source knew.
    """
    ...

# From identity
def resolve_location(*sources: Any) -> Tuple[str, str]:
    """
    Which site a camera belongs to, as ``(location_id, location_name)``; ``""`` for a miss.
    
        ``sources`` are the camera descriptions the caller already holds, most specific first --
        the matched camera entry, then ``camera_info`` and the stream's own fields. Each half is
        the first source that answers it, so the id and the name may come from different sources.
    
        **``location`` is read by shape, because it holds either.** Before the post-processor
        enriches a stream, ``location`` is the site's id; after, it is the site's display NAME
        (resolved from the id). Read as an id unconditionally, a name reaches
        ``get_location/{id}`` and is a 400 on every cool-off -- measured live on LPR and FR in
        2026-09. So:
    
        * the id is ``location_id`` / ``locationId``, else ``location`` only when it is a 24-hex
          ObjectId; the all-zero placeholder the platform writes for "no site" is no id,
        * the name is ``location`` / ``locationName`` only when it is **not** id-shaped: showing
          a user ``68f28be1f74ae116727448c4`` as a site name is worse than showing nothing.
    
        Deciding is all this does. Looking the name up for an id is the caller's round trip
        (``InferenceAPI.fetch_location``), taken only when the id came without a name.
    
        Args:
            *sources: Mappings or attribute-bearing objects, most specific first. ``None`` is
                skipped.
    
        Returns:
            ``(location_id, location_name)``, either of which may be ``""``.
    """
    ...

# From identity
def resolve_project_id(action_record: Optional[Callable[[], Any[str, Any]]] = None) -> str:
    """
    Which project this worker belongs to, or ``""`` -- **read the warnings first**.
    
        This resolver is narrower than the other three and deliberately so.
    
        **It has one source: the action record's ``_idProject``.** Not ``jobParams``, not
        ``actionDetails`` -- the field sits at the top level of the record.
    
        **The session's own ``project_id`` is not a source, although it is the first one today.**
        The live resolution starts at ``getattr(session, "project_id", "")`` and only then falls
        through to the rest. That source cannot come here, because reaching it means holding a
        session and this module holds none -- which is the property that lets every function in it
        be tested with a literal. A caller that has a session already has the answer without
        asking, so it reads its own first and calls this only on a miss::
    
            project_id = getattr(session, "project_id", "") or resolve_project_id(get_record)
    
        Two sentences of the caller's, rather than a session parameter that would put I/O one
        argument away from every function in this file.
    
        **It is empty on a decoupled deployment, by design rather than by accident.** The
        ``deploy_postproc_add`` record a decoupled analytics container is launched with carries no
        ``_idProject`` at all, so this answers ``""`` there and always will. That is why an
        analytics client needs no project, and why a caller that treats ``""`` as a fault will
        report one on every decoupled node.
    
        **``$MATRICE_PROJECT_ID`` is deliberately not a source here.** It is written by the
        facial-recognition path and read by it, inside one container. A container runs one usecase,
        so every read of that variable from outside facial recognition has no writer in its own
        process and returns ``""`` on every call. Adding it here would document a fallback that
        cannot fire and would hide the real answer -- that those callers have no project.
    
        **The licence-plate path's ``projectID`` is a different source, not a fallback.** It comes
        off the LPR server record, spells the key differently, and is scoped to that server rather
        than to this worker. Merging the two would answer one question with the other's value.
    
        Args:
            action_record: A function returning this worker's action record.
    
        Returns:
            The project id, or ``""`` -- which on a decoupled node is the correct answer.
    """
    ...

# From identity
def resolve_sidecar_base_url(host: str, port: Any) -> str:
    """
    Where to reach a sidecar whose server record says it is at ``host:port``.
    
        A sidecar's record names the address it is reachable at from outside. When that address is
        **this machine's own**, the sidecar is running on this box and the loopback address reaches
        it without leaving the host -- so the record's host is replaced with ``localhost`` while
        the port is kept.
    
        ``public_ip`` is passed in rather than looked up, because looking it up is an outbound
        request and this module makes none. ``resolve_public_ip_once`` does that half, caches it
        for the process, and answers ``"localhost"`` when the lookup fails -- a cheap wrong answer
        beating a correct one that costs the first frame two minutes. A caller that does not have
        the value, or does not care, omits it and gets the record's own address, which is
        reachable either way; the loopback form only avoids a round trip out of the machine and
        back.
    
        **This refuses where the two existing copies guess, and that is the one behavioural
        difference to know about.** Both of them read the record as ``get("host", "localhost")``
        and ``get("port", 8081)``, so a record that carries neither produces
        ``http://localhost:8081`` -- an address that looks resolved and points at whatever happens
        to answer on this box. A caller that wants those defaults states them at the call site,
        where the reader can see which value is the record's and which is the fallback::
    
            resolve_sidecar_base_url(rec.host or "localhost", rec.port or 8081, public_ip=ip)
    
        Args:
            host: The host from the server record.
            port: The port from the server record. Accepts the integer the record carries or the
                string some producers send.
            public_ip: This machine's public address, if the caller knows it.
    
        Returns:
            A base URL, or ``""`` when the record carried no host -- a refusal rather than a
            guess. A port of its own is omitted when the record had none, rather than defaulted:
            the two sidecars listen on different ports, so there is no value this function could
            supply that would be right for both.
    """
    ...

# From models
def build_detection(payload: Any[str, Any] | None = None, **fields: Any) -> Any:
    """
    A :class:`CreateDetectionRequest` from a mapping or from keywords.
    """
    ...

# From models
def build_people_activity(payload: Any[str, Any] | None = None, **fields: Any) -> Any:
    """
    A :class:`PeopleActivityRequest` from a mapping or from keywords.
    """
    ...

# From models
def build_service_shutdown(payload: Any[str, Any] | None = None, **fields: Any) -> Any:
    """
    A :class:`ServiceShutdownRequest` from a mapping or from keywords.
    """
    ...

# From models
def build_similar_face_search(payload: Any[str, Any] | None = None, **fields: Any) -> Any:
    """
    A :class:`SimilarFaceSearchRequest` from a mapping or from keywords.
    """
    ...

# From models
def build_staff_enroll(payload: Any[str, Any] | None = None, **fields: Any) -> Any:
    """
    A :class:`StaffEnrollRequest` from a mapping or from keywords.
    """
    ...

# From models
def build_staff_image_update(payload: Any[str, Any] | None = None, **fields: Any) -> Any:
    """
    A :class:`StaffImageUpdateRequest` from a mapping or from keywords.
    """
    ...

# From models
def build_unknown_person_enroll(payload: Any[str, Any] | None = None, **fields: Any) -> Any:
    """
    An :class:`UnknownPersonEnrollRequest` from a mapping or from keywords.
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
# From actions_api
class ActionsApi:
    # ``AnalyticsClient.actions`` -- what the platform knows about this worker's launch.
    #
    #     Args:
    #         session_provider: Called for the session to ride on each request. A callable rather
    #             than a session because a handle taken once is a handle that goes stale when the
    #             client's session is rebuilt -- the same reason
    #             :attr:`~.analytics_client.AnalyticsClient.rpc` is a property.

    def __init__(self: Any, session_provider: Callable[[], Any]) -> None: ...

    REDIS_SERVER_BY_INSTANCE: str

    def fetch_redis_server(self: Any, instance_id: str) -> Optional[Any]:
        """
        The Redis server record for one instance, or ``None`` if there is no such record.
        
                ``fetch_``, so this is a round trip on **every** call. Nothing caches it: unlike the
                action record, which describes a launch that has already happened, a server record
                can change under a running worker.
        
                Args:
                    instance_id: The instance whose Redis is wanted.
        
                Returns:
                    The record, or ``None`` when the platform reports no such instance. Absence is an
                    answer on this route, not a failure.
        
                Raises:
                    CallFailure: No base URL produced either a record or an absence.
        """
        ...

    def get_action_details(self: Any, action_id: Optional[str] = None) -> Any:
        """
        The record for the action that launched this worker.
        
                ``get_``, not ``fetch_``: this is **the only cached route of the twenty-four**. The
                first call in a process pays one round trip and every later call is free, because the
                record describes a launch that has already finished -- re-reading it cannot tell this
                process anything new. Forty cameras in one container therefore cost one GET between
                them, not forty.
        
                The model is rebuilt on each call rather than cached alongside the record, and that
                is deliberate. ``frozen=True`` stops a field being **rebound**; it does nothing about
                the contents of ``action_details`` and ``job_params``, which are the two fields every
                consumer actually reads. A shared model instance would hand every caller the same
                mutable dicts. Rebuilding the model costs ~6 µs against a round trip (measured
                2026-09-21), which is the trade being made.
        
                **Ordering, and it matters.** The model is built from the copy
                :func:`~.bootstrap.get_action_record` hands back, never from the stored record.
                Validation replaces only the **outermost** mapping and passes nested values through
                by reference, so a model built from the cached document would let a caller reach the
                cache through ``record.job_params`` and change what every later caller reads.
        
                Args:
                    action_id: The action to read. Omit it and the id is resolved from the launch
                        environment, which is what a worker asking about itself wants.
        
                Returns:
                    The record, typed.
        
                Raises:
                    CallFailure: No action id could be resolved, or the read did not succeed. An
                        absent record is **not** an answer on this route -- a worker whose own launch
                        record is missing has nothing to fall back to.
        """
        ...


# From analytics_client
class AnalyticsClient:
    # The platform backend, as ten endpoints in three groups, plus one resolver.
    #
    #     Args:
    #         session: An open ``matrice_common`` session to use. Omit it and the client asks
    #             :func:`~.bootstrap.get_session` for the process's own, building it on first
    #             use. Pass one when the caller already holds a session, or when a test needs
    #             the client to make no session of its own.
    #
    #     Attributes:
    #         actions: Routes answered by be-actions -- this worker's launch record, and the Redis
    #             an instance publishes to.
    #         applications: Routes answered by be-application -- the application catalogue.
    #         inference: Routes answered by be-inference -- deployments, post-processing configs,
    #             sites and cameras.
    #         session: The session this client calls on, or ``None`` when the SDK is absent.
    #         rpc: The session's *current* RPC handle. Read through every time -- see the
    #             module docstring.
    #
    #     The three groups are reached as attributes rather than flattened onto this class::
    #
    #         client.inference.fetch_location(location_id)
    #
    #     so a call site names the producer that answers it without anyone opening the file to
    #     find out. They are split by ``/v1`` prefix, which is both the platform's own division
    #     and this package's routing boundary -- ``/v1/inference/`` is locally owned and gets one
    #     base, the other two get the two-base retry.
    #
    #     **Grouping inside this client is by prefix; ownership ACROSS clients is not.** Three
    #     ``/v1/actions/`` routes belong to ``FRClient`` and ``LPRClient`` instead, because a route
    #     belongs to the client that owns the id it is keyed by, and those three are keyed by a
    #     server id only those clients hold.
    #
    #     **One method sits on the client itself rather than in a group**, and only one:
    #     :meth:`resolve_application_identity` reads an action record, then a deployment record,
    #     then post-processing configs, stopping at the first that answers. No group owns all three,
    #     and :mod:`.identity` -- which holds the resolution *order* for single-source fields --
    #     cannot hold this one because it does I/O. A second such method would be a reason to ask
    #     whether the groups are drawn right; one is the facade doing its job.

    def __init__(self: Any, session: Any = None) -> None: ...

    def resolve_application_identity(self: Any, post_processing_config: Any = None) -> Tuple[Optional[str], Optional[str]]:
        """
        ``(application_id, application_version)`` -- from local data first, then the platform.
        
                The one method here that is not a single route. It reads three of them, in a fixed
                order, stopping at the first that answers both halves -- which is why it lives on the
                client rather than in a route group: no group owns all three, and
                :mod:`.identity` cannot hold it because that module does no I/O by contract.
        
                Order, cheapest and most local first. **Every step reports the version this deployment
                actually runs**; the published version is not among them and never resolves here --
                :meth:`.applications_api.ApplicationsApi.fetch_application` answers that different
                question.
        
                1. what the caller already holds -- ``post_processing_config``, then ``identity``,
                   which on the worker path is ``stream_info``. No I/O at all;
                2. this worker's own action record -- a ``deploy_add`` launch carries both halves in
                   ``jobParams``;
                3. the app-deployment record, which answers with the id **and** the version at once;
                4. the deployment's post-processing config documents, which carry ``_idApplication``.
                   Last because it is the only step that can return several documents, but still a
                   *deployed*-scope answer, so it belongs ahead of any published-version guess.
        
                Step 4 can only ever supply the **id**. The producer's
                ``PostProcessingConfigResponse`` sends seven fields and no version among them, so the
                version half of that step was unreachable before this method was typed and is absent
                now rather than silently failing.
        
                Every step's failure is swallowed to a debug line and the search continues: a record
                that cannot be read is a miss, not a fault, because a later source may still answer and
                the caller's own fallback is better than an exception from four routes down.
        
                Args:
                    post_processing_config: The caller's config, raw dict or parsed object -- both are
                        read, by key and by attribute respectively.
                    identity: Any other mapping that may carry these fields; ``stream_info`` on the
                        worker path.
                    env: Environment to resolve the action id from. Defaults to the process's own.
                    argv: Command line to resolve the action id from. Defaults to the process's own.
        
                Returns:
                    The pair, either half of which may be ``None``. ``None`` means *no source knew* and
                    is a refusal rather than a value; this method never invents one.
        """
        ...

    def rpc(self: Any) -> Any:
        """
        The session's RPC handle, read fresh on every access.
        
                Not cached, and the distinction is not academic: ``session.update()`` replaces the
                session's RPC and shuts the previous one down. A handle held from construction is
                therefore a handle that works until the first re-authentication and silently stops
                afterwards. All four ``update()`` call sites in this repository are bootstrap-time,
                which is precisely when a client built early would be holding the stale one.
        
                Raises:
                    CallFailure: There is no session -- the SDK was absent at construction, so the
                        warning naming that has already been logged.
        """
        ...

    def session(self: Any) -> Any:
        """
        The session this client calls on, or ``None`` when the SDK is absent.
        """
        ...


# From applications_api
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


# From fr_client
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


# From inference_api
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


# From lpr_client
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
    #     UNVERIFIED: no published schema. What this route accepts cannot be checked from here;
    #     what it has been receiving can, and that is what these defaults reproduce.
    #
    #     ``timestamp`` is unlike the other optional fields: it is **always sent**, so the
    #     default has to be a usable value rather than a blank. ``exclude_none`` drops ``None``
    #     and keeps ``""``, so a default of ``""`` would not omit the key -- it would put an
    #     empty string on the wire, which the sidecar cannot tell from a deliberate blank. The
    #     factory generates the same value the caller would have had to remember to pass, which
    #     is why it lives here and not in a docstring asking them to. A caller who supplies one
    #     is not overridden. ``image_source`` and ``location`` are omitted when empty.

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


# From response
class ConnectionLost:
    # A pooled connection could not be established, twice in a row.
    #
    #     One dropped keep-alive is the pool's own business and is retried where it happens --
    #     the server closed a connection it had promised to keep, the request never left, and
    #     a fresh connection sends it. **Two in a row is not that**, and this is what the
    #     caller is told instead.
    #
    #     Reported separately from a plain :class:`CallFailure` because the request provably
    #     never reached the producer, so a caller may treat it as a reachability problem
    #     rather than as a rejected write. Whether that means pacing, dropping or retrying is
    #     again the caller's.

    ...

# From response
class MalformedReply:
    # The call succeeded, and its payload did not fit the shape the route declares.
    #
    #     A ``CallFailure`` because that is what this package raises and what every consumer
    #     already catches, and a distinct type because **this one is not a failed call**. The
    #     request was made, the producer answered, and the answer was well-formed at the
    #     envelope level -- what did not hold is the contract. A caller retrying it will get
    #     the same reply, so "retry" and "try the next base" are the wrong responses, where
    #     for a plain :class:`CallFailure` they are often the right ones.
    #
    #     It is also the signal a producer changed a payload without telling anyone, which is
    #     worth separating in error reporting from the network and 5xx noise it would
    #     otherwise sit inside.
    #
    #     ``response``
    #         The payload exactly as it arrived, so a caller can say what it got. The
    #         validator's own error, naming the field that did not fit, is the ``__cause__``.

    ...

# From response
class RateLimited:
    # The producer answered 429.
    #
    #     A ``CallFailure`` because that is what this package raises, and a distinct type
    #     because a caller that paces itself needs to tell "slow down" from "this request was
    #     wrong". **It says what happened and not what to do about it**: how long to hold off,
    #     whether to drop the payload and whether to warn are the caller's, which is the only
    #     place that knows whether the thing being sent still matters.
    #
    #     ``retry_after``
    #         Seconds, from the ``Retry-After`` header, or ``0.0`` when the producer sent none
    #         -- which lpr-server currently does not, answering only
    #         ``{"error": "rate limit exceeded"}``. ``0.0`` therefore means *no hint*, not
    #         *retry immediately*, and a caller reading it as a delay must supply its own
    #         backoff.

    def __init__(self: Any, message: str, **kwargs: Any) -> None: ...


# From transport
class PooledPoster:
    # POST to one host over a **kept-alive** connection pool, and say what went wrong.
    #
    #     The counterpart to :func:`_rpc_sent` for a route that runs often enough that opening a
    #     connection per call is the dominant cost. ``rpc.async_send_request`` opens
    #     ``aiohttp.ClientSession`` inside the call and closes it on the way out, so every request
    #     pays a fresh connection; this holds one session and reuses its connections. Measured on
    #     loopback with a 40 KB body (2026-09-21): 0.68 ms per request against 1.08 ms. The
    #     absolutes are this machine's and drift with it; the ratio is the point, and it is the
    #     shape aiohttp's own documentation describes when it says to hold one session for the
    #     application's lifetime rather than one per request.
    #
    #     **Only for a route that is hot enough to justify it.** A pool is state, and state has to be
    #     closed; :func:`_rpc_sent` stays the right verb everywhere else precisely because it has
    #     none.
    #
    #     **The session is bound to the event loop that first uses it.** aiohttp attaches the
    #     connector to the running loop, so a session created on one loop and used from another
    #     fails at the point of use. It is therefore created lazily, on first send, rather than in
    #     ``__init__`` -- which also keeps construction free of I/O, the property the three clients
    #     in this package share.
    #
    #     **``aiohttp`` is imported inside the send, not at module scope.** It is not a declared
    #     dependency of this package, and importing it costs ~220 ms and ~26 MB against this
    #     module's own ~11 ms -- a cost every importer would pay whether or not it ever posts. Once
    #     ``sys.modules`` is warm the in-function import costs ~120 ns. (All measured
    #     2026-09-21.) When it is absent altogether, :meth:`post` falls back to
    #     ``rpc.async_send_request``, which imports it the same way and fails the same way; a
    #     deployment without aiohttp is no worse off than it is today.
    #
    #     **What this class decides, and what it refuses to decide.** It reconnects once when the
    #     pool hands out a connection the server had already closed, because that request provably
    #     never left and the retry is the first attempt finishing rather than a second one. It does
    #     **not** re-send a request that reached the producer: whether that is safe is the caller's
    #     knowledge, not this class's, and :class:`~.lpr_client.LPRClient` says so in its own words.
    #     A 429 is reported, never slept on -- how long to wait, and whether the payload is still
    #     worth sending when the wait is over, belongs to the caller that owns the queue.

    def __init__(self: Any, session_provider: Callable[[], Any]) -> None:
        """
        Args:
            session_provider: Returns the ``matrice_common`` session to authenticate against,
                read at send time rather than held, because ``session.update()`` replaces the
                session's RPC and shuts the previous one down.
            timeout_s: Total timeout for one request, baked into the pooled session when it is
                created. Changing it afterwards does not reach a session already built.
        """
        ...

    async def aclose(self: Any) -> None:
        """
        Close the pool. Call from the event loop that sent on it.
        
                Idempotent, and free on a poster that never sent: the session is built on the first
                send, so there is nothing to close before it.
        """
        ...

    async def post(self: Any, path: str) -> Any:
        """
        Send one request over the pool and return what ``validate`` makes of the reply.
        
                The signature is :func:`_rpc_sent`'s minus ``method``, because a pool is only worth
                holding for a route that is written to repeatedly, and every such route here is a POST.
        
                Args:
                    path: The path, already filled in and already carrying any query string.
                    what: What is being attempted, phrased to read inside an error message.
                    unwrap: The unwrap belonging to this route's **producer**.
                    validate: Builds the return value from the payload. Not called on an absence.
                    base_url: The host to send to. Required, as for :func:`_rpc_sent`.
                    payload: The request body.
        
                Returns:
                    Whatever ``validate`` builds, or ``None`` when the producer answers with no payload.
        
                Raises:
                    RateLimited: The producer answered 429. Carries ``Retry-After`` when it sent one.
                    ConnectionLost: Two connection attempts failed in a row, so the request never left.
                    CallFailure: Anything else -- no session, no aiohttp *and* no fallback, a non-2xx,
                        or a producer that reported failure in its envelope.
        """
        ...


# From transport
class Uploader:
    # PUT bytes at a URL that already carries its own authorisation.
    #
    #     **Not a producer route, and deliberately not on a client's route list.** The URL is
    #     handed over at runtime -- a producer answers a write with the storage address it
    #     resolved, and the bytes go there next. There is no path template, no base URL and no
    #     session: a pre-signed URL carries its own credentials in the query string, so adding
    #     an ``Authorization`` header would be wrong, not merely redundant.
    #
    #     It lives here rather than in a usecase because it is transport, and because the
    #     connection pool is this layer's job. The call it replaces opened a fresh
    #     ``httpx.AsyncClient`` per upload; one session is held here and its connections reused,
    #     the same reasoning as :class:`PooledPoster`.
    #
    #     ``aiohttp`` is imported inside the send for the reason the class above gives: ~220 ms
    #     and ~26 MB at module scope, against this module's own ~11 ms.

    def __init__(self: Any) -> None: ...

    async def aclose(self: Any) -> None:
        """
        Close the pool. Free on a putter that never sent -- it opens nothing until then.
        """
        ...

    async def put(self: Any, url: str, content: Any) -> bool:
        """
        Send ``content`` to ``url``. ``True`` when the store accepted it.
        
                Returns ``False`` rather than raising, for every failure: a frame that did not
                reach storage is a lost frame, not a lost request, and the caller's next frame is
                along in milliseconds. The reason is logged once, where it happened.
        
                Reporting is an explicit call rather than a handler for that same reason -- a refusal
                arrives as a status, not as an exception, so there is nothing for a handler to catch.
                Object storage is reached directly, so nothing else in the stack sees these at all.
        """
        ...


from . import actions_api, analytics_client, applications_api, bootstrap, fr_client, identity, inference_api, lpr_client, models, response, transport