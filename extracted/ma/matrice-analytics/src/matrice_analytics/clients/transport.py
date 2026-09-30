"""GET a platform route on an authenticated session, and say what went wrong.

This module owns the *call*: which base URL to try, in what order, and how to turn a
reply that never arrived into a named failure. Reading a reply that *did* arrive is
:mod:`.response`'s job, and the two are separate because they fail for different
reasons -- a call fails because of the network, a route or a credential, an envelope
fails because the producer said so.

**Everything here raises :class:`~.response.CallFailure` and nothing else.** This
package is an import leaf: it may import ``matrice_common`` and the standard library,
never ``matrice_analytics.runtime``. ``AppBundleError`` lives in ``runtime`` and is
therefore unreachable from here by design, so a caller in ``runtime`` that needs its
own exception type translates at its own boundary rather than reaching across.

The session itself is not opened here -- see :mod:`.bootstrap`. A session arrives as an
argument, which is what makes every function in this module testable with a stub that
has a ``rpc`` attribute and nothing else.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Callable, Dict, Iterator, List, Mapping, Optional, Tuple

from .response import CallFailure, ConnectionLost, MalformedReply, RateLimited

logger = logging.getLogger(__name__)

#: Overrides the derived backend address. Set it when a deployment's backend is not where
#: the ``ENV`` stage name would put it.
ENV_API_BASE = "MATRICE_APP_BUNDLE_API_BASE"

#: Route prefixes the local gateway serves from an **on-prem** service instead of proxying to the
#: cloud (``location /v1/inference -> api_inference``). For these the session's own base URL is the
#: authority, and :func:`backend_base_url` is not a fallback but a wrong answer -- see
#: :func:`_bases_for`.
LOCAL_AUTHORITY_PREFIXES = ("/v1/inference/",)

#: Which header the licence travels in. The header is this module's business -- it is part of
#: forming the request. The licence itself is not: it is something the launch handed the
#: container, so :func:`~.bootstrap.license_key` reads it, beside the action id.
LICENSE_KEY_HEADER = "X-License-Key"

#: Total timeout for one pooled POST, in seconds. Short on purpose: the route this pool
#: exists for runs per detection behind a sender that drops a sighting once it is stale,
#: so a request still in flight after five seconds is one whose answer no longer matters.
POOLED_POST_TIMEOUT_S = 5.0


def backend_base_url(env: Optional[Mapping[str, str]] = None) -> str:
    """The backend's own address, for a route the session's base URL will not serve.

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
    environ = os.environ if env is None else env
    explicit = (environ.get(ENV_API_BASE) or "").strip()
    if explicit:
        return explicit.rstrip("/")
    stage = ((environ.get("ENV") or "").strip() or "prod").lower()
    return f"https://{stage}.backend.app.matrice.ai"


def _bases_for(path: str, env: Optional[Mapping[str, str]] = None) -> tuple:
    """The base URLs worth trying for ``path``, in order.

    Two bases for a **cloud-only** route, because the local gateway 302s those out and httpx drops
    the ``Authorization`` header across the origin change -- the case :func:`backend_base_url`
    exists for.

    One base for a route in :data:`LOCAL_AUTHORITY_PREFIXES`, because retrying those against the
    cloud is not a fallback, it is a category error, and an expensive one (ANLY-15):

    * The gateway proxies ``/v1/inference/*`` to the on-prem ``api_inference``. That service, not
      the cloud, owns the answer -- on an ``accessScale: "local"`` deployment the document exists
      in the on-prem mongo and *nowhere else*, so the cloud has nothing to return even in
      principle.
    * The retry cannot authenticate anyway. Tokens are minted against ``$MATRICE_BASE_URL``
      (``token_auth.py`` ``VALIDATE_ACCESS_KEY_URL`` / ``REFRESH_TOKEN_URL``), i.e. the local
      gateway's ``api_user``, so a direct-to-cloud call presents a JWT that the cloud never issued
      and is refused ``401 Invalid authentication token``. Going direct also bypasses the
      gateway's ``cloud_egress`` listener, which is the *only* sanctioned crossing: it strips
      ``Authorization`` and substitutes the deployment's ``X-License-Key``. The one route that
      needs that crossing is the licensed usecase download, sent by
      :meth:`~.applications_api.ApplicationsApi.mint_usecase_download` through
      :func:`_rpc_headed` -- the verb that exists because that route carries a header and
      :func:`_attempted` cannot. It takes :func:`backend_base_url` explicitly and sends once,
      so it never reaches this function at all.
    * ``rpc``'s 401 handler then re-mints (against the gateway, successfully) and retries into the
      same refusal, so each attempt costs two cloud round trips plus a re-auth, logs a full error
      block, and cannot ever succeed.
    """
    if path.startswith(LOCAL_AUTHORITY_PREFIXES):
        return (None,)
    return (None, backend_base_url(env))


def _describe(response: Any) -> str:
    """Say something useful about a failed response, including one that is not ours at all.

    ``message`` is absent whenever the body did not come from the platform -- an edge proxy
    returning its own error page, for instance. Reporting ``None`` in that case sends whoever reads
    the log hunting for a bug in the API call rather than in the network path, so name the shape.
    """
    if not isinstance(response, dict):
        return f"non-dict response {type(response).__name__}: {str(response)[:120]}"
    for key in ("message", "detail", "title", "error_name"):
        value = response.get(key)
        if isinstance(value, str) and value.strip():
            return f"{key}={value.strip()[:160]!r}"
    return f"no message; response keys were {sorted(response)[:12]}"


def _rpc(session: Any) -> Any:
    """The authenticated RPC off a session, or a named error.

    ``session.rpc`` is the same handle ``PostProcessingConfigClient`` uses, already signed with the
    container's access keys -- nothing here builds its own auth.
    """
    try:
        return session.rpc
    except Exception as exc:  # pragma: no cover - a session whose rpc property raises
        raise CallFailure(f"Session has no usable RPC handle: {exc}") from exc


def _attempted(
    session: Any,
    path: str,
    env: Optional[Mapping[str, str]],
    failures: List[str],
    params: Optional[Mapping[str, Any]] = None,
    timeout_s: Optional[int] = None,
    filed: Optional[List[str]] = None,
) -> Iterator[Tuple[Optional[str], Any]]:
    """Yield ``(base, reply)`` for each base worth trying, recording the calls that never landed.

    ``filed``, when given, also receives each attempt whose request raised out of the rpc verb:
    py_common's ``@log_errors`` wraps those verbs and has already filed that failure, so a caller
    reporting an exhaustion made only of such attempts would file one failure twice.

    Which bases to try, in what order, and the rule that a transport error is *one failed attempt
    rather than a crash* are the same for every caller. What to make of a reply that did arrive is
    not, and that half stays with the caller -- it is the difference between a route whose ``data``
    is a document and one whose ``data`` is an array, and the reason both can share this loop.

    ``params`` is the query string, for the one route that is addressed by one rather than by its
    path: the post-processing config for a camera and application. It is passed through untouched
    and omitted entirely when absent, so a route that has never sent a query string still sends
    none -- an empty mapping and no mapping are not the same request.

    ``timeout_s`` is for a route whose caller cannot afford to wait out the default. ``rpc.get``
    allows two minutes, which is right for a control-plane call made once and wrong for one on a
    per-frame or per-batch path, where a stalled lookup holds up the work it was meant to label.
    Absent, no timeout is sent at all and the session's own default stands -- passing it
    explicitly would pin that default here, where a reader would take it for this module's
    choice. It is per attempt rather than per call, so a route with two bases can spend it twice.

    ``failures`` is appended to in place. This function therefore never decides what the final
    error says, only that a base which could not be reached is named in it.

    A caller that raises from inside its own loop body closes this generator rather than resuming
    it, so a reply already judged final is never followed by another request.
    """
    extra: Dict[str, Any] = {} if params is None else {"params": params}
    if timeout_s is not None:
        extra["timeout"] = timeout_s
    for base in _bases_for(path, env):
        try:
            rpc = _rpc(session)
            reply = (
                rpc.get(path, **extra) if base is None else rpc.get(path, base_url=base, **extra)
            )
        except CallFailure as exc:
            # Recorded rather than re-raised so the final message still names the path. A session
            # with no usable rpc fails the same way twice, which is fine -- the cause is in the list.
            failures.append(f"{base or 'session base url'}: {exc}")
            continue
        except Exception as exc:  # noqa: BLE001 - every transport error is one failed attempt
            failures.append(f"{base or 'session base url'}: {type(exc).__name__}: {exc}")
            if filed is not None:
                filed.append(failures[-1])
            continue
        yield base, reply


def _note_fallback(path: str, base: Optional[str], failures: List[str]) -> None:
    """Say that the session's own base URL did not serve a route the backend then did.

    Only interesting when it happens: on a cloud deployment the two bases are the same host, so
    the second attempt is a harmless duplicate and there is nothing to report.
    """
    if base is not None:
        logger.info(
            "%s served from %s -- the session's base URL did not serve it (%s)",
            path,
            base,
            failures[0] if failures else "no detail",
        )


def _exhausted(path: str, what: str, failures: List[str]) -> CallFailure:
    """The failure raised when no base produced an answer, naming every base that was tried.

    Which base failed and how is the whole of what a reader needs, and none of it survives a bare
    "the request failed" -- so the attempts are in the message rather than in a log line the
    reader may not have.
    """
    return CallFailure(
        f"GET {path} did not succeed while resolving {what}. Tried: " + "; ".join(failures) + ". "
        "A 404 here usually means the request lost its Authorization header on a redirect out of "
        "the local gateway; a 401/403 means the container's credentials are not accepted on this "
        "route. Set $MATRICE_APP_BUNDLE_API_BASE to the backend that should serve it."
    )


#: The service every remote report from this package is filed under. py_common resolves one
#: itself when none is given, and the answer depends on which SDK it decides it is inside --
#: so it is named here rather than inferred.
SERVICE_NAME = "py_analytics"


def _report_failure(
    error: BaseException,
    *,
    path: Optional[str] = None,
    latch: Any = None,
    attr: str = "",
) -> bool:
    """File a failure the platform would otherwise never hear about. Never raises.

    Returns whether a report was made, which is what lets a caller assert the decision
    without needing a ``matrice_common`` install to assert the delivery against.

    **Only failures nothing else already reports.** ``rpc.send_request`` carries py_common's
    ``@log_errors``, so anything riding it has been filed by the time it reaches here and
    reporting again files one failure twice. What is left is the two exits that speak to
    aiohttp directly, which nothing else sees, and the semantic failures -- a 200 carrying
    ``success: false``, a payload that does not fit its model, every base exhausted -- where
    the call succeeded and there was nothing for py_common to notice.

    A clean 404 and a 429 are answers rather than faults and are never reported: the first
    means the record is not there, the second is the producer asking for less.

    **Hand over an exception that has been raised.** py_common builds its deduplication key
    from the innermost frame of ``error.__traceback__``, and when there is no traceback it
    walks its own caller instead -- which is this function, so every such report would share
    one key and one failure would hide the rest. A constructed-but-never-raised exception is
    therefore worse than useless; raise it, catch it, then report it.

    ``latch`` and ``attr`` give once per object rather than once per occurrence, and the two
    pooled exits need it. ``process_error_log`` does deduplicate, but on *delivery* -- it
    walks the traceback and writes three log lines before the TTL is consulted -- so on a
    per-detection path an unreachable sidecar pays all of that on every frame. Omitting the
    latch reports every time, which is right for a start-up or once-per-call site.
    """
    if latch is not None and attr:
        if getattr(latch, attr, False):
            return False
        try:
            setattr(latch, attr, True)
        except AttributeError:  # a slotted or frozen caller: report, just do not latch
            logger.debug("could not set latch %s on %r", attr, type(latch), exc_info=True)

    try:
        # Imported here rather than at module scope on the same two grounds the aiohttp
        # imports below use: matrice_common is optional in this package -- every route
        # already refuses by name without it -- and a caller that never fails should not
        # pay for the import. PEP 8 allows both, and this says which.
        from matrice_common.utils import (  # noqa: PLC0415 - optional dependency, see above
            process_error_log,
            resolve_backend_service,
        )

        process_error_log(
            error,
            service_name=SERVICE_NAME,
            raise_exception=False,
            log_error=True,
            # Part of py_common's dedup key. Without it every producer's failures share
            # one key, and four of the five vanish for the rest of the TTL.
            target_service=resolve_backend_service(path),
        )
        return True
    except Exception:  # noqa: BLE001 - telemetry must never break the caller
        logger.debug("could not report %s", type(error).__name__, exc_info=True)
        return False


def _rpc_data(
    session: Any,
    path: str,
    *,
    what: str,
    env: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """GET ``path`` on the authenticated session and return ``data`` as a dict.

    Tries the session's own base URL first -- where the gateway does proxy the route, that is one
    call and the right one. Only if that fails does it retry against
    :func:`backend_base_url`, because the most likely reason for the first failure is a
    cross-origin redirect that stripped the auth header rather than anything wrong with the request.
    A locally-owned route gets no such retry; :func:`_bases_for` says why.

    A 404 is deliberately *not* short-circuited here, unlike in the post-processing fetchers: on a
    cloud-only route it is the signature of the redirect having stripped the auth header, which is
    precisely the case the second base exists to rescue.

    A successful envelope whose ``data`` is not an object is **reported, not reshaped**. An earlier
    version returned ``{}`` there, which a caller cannot tell apart from a route that genuinely
    answered with no fields -- so a producer changing a payload's shape showed up as every field
    quietly going missing, at the call site rather than here. It is not retried against the second
    base either: the call succeeded, so another base would answer the same way.
    """
    already_filed = False
    try:
        attempts: List[str] = []
        filed: List[str] = []
        for base, response in _attempted(session, path, env, attempts, filed=filed):
            if isinstance(response, dict) and response.get("success"):
                _note_fallback(path, base, attempts)
                data = response.get("data")
                if not isinstance(data, dict):
                    # MalformedReply rather than a plain CallFailure, for the reason
                    # `_validated` gives: the call SUCCEEDED and the payload did not fit the
                    # shape the route declares, which is what that type means. It is a
                    # CallFailure subclass, so every handler written to the documented type
                    # still catches it. It also keeps this apart from the exhaustion below in
                    # py_common's deduplication, which keys on the exception type and the
                    # function -- as one CallFailure raised twice in one function, a producer
                    # drifting its payload shape would hide its own outage, and the reverse.
                    raise MalformedReply(
                        f"GET {path} succeeded while resolving {what}, but its data field was "
                        f"{type(data).__name__}, not an object. The route's payload shape has "
                        f"changed, or this path does not return a single document.",
                        response=response,
                    )
                return data
            attempts.append(f"{base or 'session base url'}: {_describe(response)}")

        # Every attempt raised out of the rpc verb: @log_errors filed each one already.
        already_filed = bool(attempts) and len(filed) == len(attempts)
        raise _exhausted(path, what, attempts)
    except CallFailure as failure:
        # Only the two raises above reach here: a per-attempt transport error is folded into
        # `attempts` by `_attempted` and has already been filed by py_common's @log_errors on
        # `rpc.send_request`. These two have not -- one is a call that SUCCEEDED and answered
        # with the wrong shape, the other is every base having been tried -- unless every one
        # of those tries was such a transport error, which is filed already.
        if not already_filed:
            _report_failure(failure, path=path)
        raise


def _rpc_payload(
    session: Any,
    path: str,
    *,
    what: str,
    unwrap: Callable[..., Any],
    params: Optional[Mapping[str, Any]] = None,
    env: Optional[Mapping[str, str]] = None,
    timeout_s: Optional[int] = None,
) -> Any:
    """GET ``path`` and return whatever ``unwrap`` makes of the reply.

    The same call :func:`_rpc_data` makes, with the one difference that decides whether a route
    can be served at all: the shape of the answer is **not** fixed here. ``unwrap`` is passed in,
    so a route whose ``data`` is an array is as serviceable as one whose ``data`` is an object,
    and a producer that frames its replies differently is served by passing its own unwrap rather
    than by another copy of this loop. Two of the twenty-four routes documented in :mod:`.models`
    answer with an array -- the post-processing configs for a deployment, and an account's camera
    streams -- and neither can go through :func:`_rpc_data`, which is declared to return a
    ``dict`` and raises on anything else.

    ``params`` is for the one route addressed by a query string rather than by its path -- the
    post-processing config for a camera and application. Absent, no query string is sent at all,
    which is not the same request as an empty one.

    Deciding *which* unwrap belongs to a route is the caller's, and it follows the **producer**
    rather than the client: the same client owns routes answered by different services, and an
    unwrap built for one of them does not fail loudly on another's reply -- it returns the wrong
    shape quietly. :mod:`.__init__` carries the map.

    **A not-found is only final once every base has said so.** ``unwrap_platform`` answers ``None``
    for a 404 rather than raising, because on most routes an absent record is an answer. Returning
    that from the first base would defeat the second one, and the second base exists precisely
    because a 404 out of the local gateway is the signature of a redirect that stripped the
    Authorization header -- the case :func:`_bases_for` describes. So a ``None`` is recorded as an
    attempt and the next base is tried; it is returned only when no base produced a payload and at
    least one of them reported absence rather than an error. A route with a single base -- every
    ``/v1/inference/`` one, including both array routes -- reaches the same answer in one call.

    Raises :class:`~.response.CallFailure` when no base produced either a payload or an absence:
    the attempts are named in the message, because which base failed and how is the whole of what
    a reader needs and none of it survives a bare "request failed".
    """
    attempts: List[str] = []
    filed: List[str] = []
    absent = False

    for base, response in _attempted(session, path, env, attempts, params, timeout_s, filed=filed):
        try:
            payload = unwrap(response, what=what)
        except CallFailure as exc:
            # The reply arrived and the producer rejected it. That is one failed attempt like any
            # other, not a verdict: the next base may be the one that serves this route.
            attempts.append(f"{base or 'session base url'}: {exc}")
            continue

        if payload is None:
            absent = True
            attempts.append(f"{base or 'session base url'}: reported no such record")
            continue

        _note_fallback(path, base, attempts)
        return payload

    if absent:
        # An answer, not a fault, and the one every consumer's fallback chain is written
        # around. Reporting it would file a record every time a record is legitimately absent.
        return None

    try:
        raise _exhausted(path, what, attempts)
    except CallFailure as failure:
        # Every attempt raised out of the rpc verb, whose @log_errors has filed each one already:
        # a second report here would file one failure twice.
        if not (attempts and len(filed) == len(attempts)):
            _report_failure(failure, path=path)
        raise


def _validated(validate: Callable[[Any], Any], payload: Any, *, where: str, what: str) -> Any:
    """``validate(payload)``, with a reply that does not fit the model raised as a failure.

    ``None`` passes straight through: an absent record is an answer on most of these routes, and
    ``Model.model_validate(None)`` would report it as a malformed document instead.

    **Every route method in this package documents ``CallFailure`` as how a read fails**, and
    consumers are written to exactly that -- they catch it and degrade. A model validator does
    not raise it; it raises ``ValidationError``. So a producer sending the wrong shape used to
    escape every handler that existed, and the cost was not the exception itself but what it
    skipped: a caller with a fallback chain stopped at the first step rather than trying the
    rest, and a method documented as never raising did.

    Raised as :class:`~.response.MalformedReply` rather than a plain ``CallFailure`` so that the
    two stay tellable apart. Existing handlers are unaffected -- it *is* a ``CallFailure`` -- but
    a caller that wants to distinguish a producer's contract drift from an unreachable backend
    can, and retrying is the right move for one and pointless for the other. Same reason
    ``RateLimited`` and ``ConnectionLost`` are their own types.

    Caught as ``ValueError`` rather than ``pydantic.ValidationError`` so that this module goes on
    importing no pydantic. ``runtime.app_bundle`` imports this one at module scope and defers the
    client precisely to keep off that path the ~190 modules that importing :mod:`.models`
    pulls in (192 on 2026-09-21); naming the class here would put them back. Nothing is
    over-caught: ``validate`` is the route's own model validator, so a ``ValueError`` out
    of it is a shape problem by construction.
    """
    if payload is None:
        return None
    try:
        return validate(payload)
    except ValueError as exc:
        raise MalformedReply(
            f"{where} succeeded while resolving {what}, but its payload did not match the shape "
            f"this route declares: {exc}",
            response=payload,
        ) from exc


def _rpc_model(
    session: Any,
    path: str,
    *,
    what: str,
    unwrap: Callable[..., Any],
    validate: Callable[[Any], Any],
    params: Optional[Mapping[str, Any]] = None,
    env: Optional[Mapping[str, str]] = None,
    timeout_s: Optional[int] = None,
) -> Any:
    """GET ``path`` and return the reply as whatever ``validate`` builds from it, or ``None``.

    See :func:`_validated` for what happens when the reply does not fit the model.

    :func:`_rpc_payload` with the one step every route method would otherwise repeat: turning
    the payload into a model, and **not** doing so when there is no payload. That guard is here
    rather than at each call site because omitting it is silent at the call site and loud at
    the caller -- ``Model.model_validate(None)`` raises a validation error about a missing
    document, which reads as a malformed reply rather than as an absent record.

    ``validate`` is a plain callable rather than a model class, so a route whose payload is an
    array passes ``TypeAdapter(list[Model]).validate_python`` and one whose payload is a
    document passes ``Model.model_validate``. It also keeps this module from importing
    :mod:`.models`: the transport has no business knowing which shapes exist.

    Returns:
        The validated payload, or ``None`` when every base reported no such record -- which is
        an answer on most of these routes, not a fault.
    """
    payload = _rpc_payload(
        session, path, what=what, unwrap=unwrap, params=params, env=env, timeout_s=timeout_s
    )
    try:
        return _validated(validate, payload, where=f"GET {path}", what=what)
    except CallFailure as drift:
        # Only the validation step is wrapped. `_rpc_payload` reports its own exhaustion, and
        # wrapping the call to it would file that same failure a second time.
        _report_failure(drift, path=path)
        raise


def _rpc_headed(
    session: Any,
    path: str,
    *,
    what: str,
    headers: Mapping[str, str],
    base_url: str,
) -> Any:
    """One **synchronous** GET to one named host, carrying headers, returning the raw reply.

    The third transport verb, and each of the three exists because the other two cannot do this:

    * :func:`_rpc_data` and :func:`_rpc_model` go through ``rpc.get``, which takes **no**
      ``headers`` -- it warns once and sends the request without them, so a route guarded by a
      header fails as *unauthorised* rather than as *misconfigured*, three frames from the cause;
    * :func:`_rpc_sent` does carry headers and a named host, but it is ``async``, and the caller
      here is synchronous. Awaiting it would change that caller's concurrency, not its syntax.

    **One base, required, and no retry.** The two-base fallback exists for routes the local gateway
    might or might not serve. This verb is for a route where the right host is already known and
    the wrong one is wrong rather than slow -- so there is nothing to fall back to, and making
    ``base_url`` required is what stops the session's own base being used by omission.

    **The reply is returned unread.** Every other verb here unwraps, because every other verb knows
    what its route's failures mean. This one does not: its caller distinguishes envelope states
    that :func:`~.response.unwrap_platform` deliberately flattens -- an absence that means *try the
    other route* from one that means *this route is broken* -- and that distinction cannot be
    recovered once the unwrap has run.

    That is also why this is the one verb that files nothing with the platform. The others report
    the failures they recognise as the producer's rather than the network's; this one recognises
    none, because it reads nothing. Its only failure is the send itself, and that goes through
    ``rpc.send_request``, which carries py_common's ``@log_errors`` already.

    Args:
        session: The session to ride. Its ``rpc`` is read at call time, never held.
        path: The path, already filled in.
        what: What is being attempted, phrased to read inside an error message.
        headers: Sent with the request. The reason this verb exists.
        base_url: The host to send to. Required.

    Returns:
        Whatever the producer replied, unread.

    Raises:
        CallFailure: The request could not be made at all.
    """
    try:
        return _rpc(session).send_request(
            "GET", path=path, headers=dict(headers), base_url=base_url
        )
    except CallFailure:
        raise
    except Exception as exc:  # noqa: BLE001 - every transport error is reported the same way
        raise CallFailure(
            f"GET {base_url}{path} failed while resolving {what}: {type(exc).__name__}: {exc}"
        ) from exc


async def _rpc_sent(
    session: Any,
    method: str,
    path: str,
    *,
    what: str,
    unwrap: Callable[..., Any],
    validate: Callable[[Any], Any],
    base_url: str,
    payload: Optional[Any] = None,
) -> Any:
    """Send one request to **one named host** and return what ``validate`` makes of the reply.

    The counterpart to :func:`_rpc_model` for everything that is not a platform GET. Three
    things differ, and each is forced rather than chosen:

    * **it is async**, because the facial-recognition routes are awaited at their call sites
      today and making them block would change the caller's concurrency, not just its syntax;
    * **the verb and body are the caller's**, since these routes enroll, search, store,
      update and shut down rather than read;
    * **there is exactly one base, and it is required.** No two-base retry, and no falling
      back to the session's own base URL. A sidecar has one host, learned from its server
      record -- retrying its route against the platform would ask the wrong service, and
      defaulting to the session base would send a sidecar call to the platform silently.
      Making ``base_url`` required is what stops that being a possible mistake.

    ``rpc.get`` is not used even for a GET here, because it takes no ``headers`` and no
    ``payload`` and would quietly drop either -- it warns once and sends the request without
    them. ``async_send_request`` is the verb that carries them.

    Args:
        session: The session to ride. Its ``rpc`` is read at call time, never held.
        method: ``GET``, ``POST``, ``PUT`` -- whatever the route declares.
        path: The path, already filled in and already carrying any query string.
        what: What is being attempted, phrased to read inside an error message.
        unwrap: The unwrap belonging to this route's **producer** -- see :mod:`.`.
        validate: Builds the return value from the payload. Not called on an absence.
        base_url: The host to send to. Required.
        payload: The request body, or ``None`` for a route that sends none.

    Returns:
        Whatever ``validate`` builds, or ``None`` when the producer answers successfully with no
        payload -- which a service being asked to stop, or told about a face, reasonably does.
        **Not** a 404: on this transport ``async_send_request`` raises one rather than returning
        the not-found envelope, so it arrives below as a failure and never as an absence. A route
        that needs "missing" to be a value is a synchronous read and belongs on ``_rpc_model``.

    Raises:
        CallFailure: The request could not be made, or the producer reported failure.
    """
    try:
        reply = await _rpc(session).async_send_request(
            method=method, path=path, payload=payload, base_url=base_url
        )
    except CallFailure:
        raise
    except Exception as exc:  # noqa: BLE001 - every transport error is reported the same way
        raise CallFailure(
            f"{method} {base_url}{path} failed while attempting {what}: {type(exc).__name__}: {exc}"
        ) from exc

    try:
        body = unwrap(reply, what=what)
        return _validated(validate, body, where=f"{method} {base_url}{path}", what=what)
    except CallFailure as failure:
        # The send above is deliberately outside this: it goes through
        # `rpc.async_send_request`, which carries py_common's @log_errors, so a transport
        # failure there is already filed. What is left is a reply that arrived -- the producer
        # reporting failure in its own envelope, or a payload that does not fit the route.
        _report_failure(failure, path=path)
        raise


class PooledPoster:
    """POST to one host over a **kept-alive** connection pool, and say what went wrong.

    The counterpart to :func:`_rpc_sent` for a route that runs often enough that opening a
    connection per call is the dominant cost. ``rpc.async_send_request`` opens
    ``aiohttp.ClientSession`` inside the call and closes it on the way out, so every request
    pays a fresh connection; this holds one session and reuses its connections. Measured on
    loopback with a 40 KB body (2026-09-21): 0.68 ms per request against 1.08 ms. The
    absolutes are this machine's and drift with it; the ratio is the point, and it is the
    shape aiohttp's own documentation describes when it says to hold one session for the
    application's lifetime rather than one per request.

    **Only for a route that is hot enough to justify it.** A pool is state, and state has to be
    closed; :func:`_rpc_sent` stays the right verb everywhere else precisely because it has
    none.

    **The session is bound to the event loop that first uses it.** aiohttp attaches the
    connector to the running loop, so a session created on one loop and used from another
    fails at the point of use. It is therefore created lazily, on first send, rather than in
    ``__init__`` -- which also keeps construction free of I/O, the property the three clients
    in this package share.

    **``aiohttp`` is imported inside the send, not at module scope.** It is not a declared
    dependency of this package, and importing it costs ~220 ms and ~26 MB against this
    module's own ~11 ms -- a cost every importer would pay whether or not it ever posts. Once
    ``sys.modules`` is warm the in-function import costs ~120 ns. (All measured
    2026-09-21.) When it is absent altogether, :meth:`post` falls back to
    ``rpc.async_send_request``, which imports it the same way and fails the same way; a
    deployment without aiohttp is no worse off than it is today.

    **What this class decides, and what it refuses to decide.** It reconnects once when the
    pool hands out a connection the server had already closed, because that request provably
    never left and the retry is the first attempt finishing rather than a second one. It does
    **not** re-send a request that reached the producer: whether that is safe is the caller's
    knowledge, not this class's, and :class:`~.lpr_client.LPRClient` says so in its own words.
    A 429 is reported, never slept on -- how long to wait, and whether the payload is still
    worth sending when the wait is over, belongs to the caller that owns the queue.
    """

    def __init__(
        self,
        session_provider: Callable[[], Any],
        *,
        timeout_s: float = POOLED_POST_TIMEOUT_S,
    ) -> None:
        """
        Args:
            session_provider: Returns the ``matrice_common`` session to authenticate against,
                read at send time rather than held, because ``session.update()`` replaces the
                session's RPC and shuts the previous one down.
            timeout_s: Total timeout for one request, baked into the pooled session when it is
                created. Changing it afterwards does not reach a session already built.
        """
        self._session_provider = session_provider
        self._timeout_s = float(timeout_s)
        self._http: Any = None
        #: Whether the "pooled path unavailable" warning has been emitted. Once per poster,
        #: not once per call: this runs per detection, and a pooled path that cannot be set
        #: up cannot be set up on the next call either, so the second line onwards says
        #: nothing the first did not and buries the log it is written to.
        self._warned_unpooled = False
        #: Whether the current run of failures has been reported. Cleared by the next send
        #: that succeeds, so each outage is reported once and a later one is reported again.
        #: Per detection rather than per call is the point: ``process_error_log`` walks the
        #: traceback and writes three lines *before* its own TTL is consulted, so an
        #: unreachable producer would pay all of that on every frame.
        self._reported = False

    def _client_session(self, aiohttp_mod: Any) -> Any:
        """The pooled session, created on first use and reused after.

        Recreated when the previous one has been closed -- by :meth:`aclose`, or by the
        recovery in :meth:`post` -- so a closed pool is a cost of one connection rather than a
        permanent failure.
        """
        if self._http is None or self._http.closed:
            self._http = aiohttp_mod.ClientSession(
                timeout=aiohttp_mod.ClientTimeout(total=self._timeout_s)
            )
        return self._http

    async def _send_once(
        self, aiohttp_mod: Any, url: str, headers: Dict[str, str], payload: Any
    ) -> Any:
        """One POST on the pooled session. Returns the decoded body, or raises.

        Raises:
            RateLimited: The producer answered 429.
            CallFailure: The producer answered any other non-2xx.
        """
        http = self._client_session(aiohttp_mod)
        async with http.post(url, json=payload, headers=headers, allow_redirects=True) as reply:
            status = reply.status
            try:
                body = await reply.json(content_type=None)
            except Exception:  # noqa: BLE001 - reading the body is best effort; the status still decides
                body = await reply.text()

            if status == 429:
                raise RateLimited(
                    f"POST {url} was rate limited: {body!r}",
                    retry_after=_retry_after_seconds(reply.headers.get("Retry-After")),
                    status_code=status,
                    response=body,
                )
            if not (200 <= status < 300):
                raise CallFailure(
                    f"POST {url} failed: status={status} body={body!r}",
                    status_code=status,
                    response=body,
                )
            return body

    async def post(
        self,
        path: str,
        *,
        what: str,
        unwrap: Callable[..., Any],
        validate: Callable[[Any], Any],
        base_url: str,
        payload: Any,
    ) -> Any:
        """Send one request over the pool and return what ``validate`` makes of the reply.

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
        prepared = await self._prepare(path, base_url=base_url, what=what)
        if prepared is None:
            # The unpooled fallback rides ``rpc``, whose ``send_request`` carries py_common's
            # ``@log_errors``, so a transport failure on this branch has already been filed by
            # the time it gets here. Only the pooled branch below speaks to aiohttp directly.
            reply = await _rpc(self._session_provider()).async_send_request(
                method="POST", path=path, payload=payload, base_url=base_url
            )
        else:
            aiohttp_mod, url, headers = prepared
            try:
                reply = await self._send_with_one_reconnect(
                    aiohttp_mod, url, headers, payload, what=what
                )
            except RateLimited:
                raise
            except Exception as exc:  # noqa: BLE001 - re-raised unchanged; this only reports
                _report_failure(exc, path=path, latch=self, attr="_reported")
                raise

        try:
            body = unwrap(reply, what=what)
            result = _validated(validate, body, where=f"POST {base_url}{path}", what=what)
        except Exception as exc:  # noqa: BLE001 - re-raised unchanged; this only reports
            # Semantic, so it is ours on both branches: the call reached the producer and
            # came back, and what came back does not fit the route. ``@log_errors`` sees a
            # successful request.
            _report_failure(exc, path=path, latch=self, attr="_reported")
            raise

        self._reported = False
        return result

    async def _prepare(
        self, path: str, *, base_url: str, what: str
    ) -> Optional[Tuple[Any, str, Dict[str, str]]]:
        """The aiohttp module, the absolute URL and the auth headers -- or ``None``.

        ``None`` means the pooled path cannot be set up at all: aiohttp is missing, the token is
        unusable, or ``rpc``'s internals are not what this expects. The caller then sends through
        ``rpc.async_send_request`` instead, which is slower but works, so a container without
        aiohttp keeps posting rather than losing the route.
        """
        try:
            import aiohttp  # noqa: PLC0415 - see the class docstring: ~220 ms and ~26 MB at module scope

            rpc = _rpc(self._session_provider())
            rpc.refresh_token()
            auth_token = rpc.AUTH_TOKEN
            auth_token.set_bearer_token()
            bearer = auth_token.bearer_token
            if not isinstance(bearer, str) or not bearer:
                raise TypeError("bearer token unavailable or not a string")
            url = rpc.add_project_id(f"{base_url}{path}")
            if not isinstance(url, str):
                raise TypeError("request url is not a string")
            headers = {
                "Authorization": bearer,
                "sdk_version": str(getattr(rpc, "sdk_version", "0.0.0")),
            }
        except CallFailure:
            raise
        except Exception as exc:  # noqa: BLE001 - any setup failure degrades to the unpooled verb
            if not self._warned_unpooled:
                self._warned_unpooled = True
                logger.warning(
                    "Pooled HTTP unavailable while preparing %s (%s: %s); falling back to the "
                    "per-call transport. Reported once per client, not once per call.",
                    what,
                    type(exc).__name__,
                    exc,
                )
            return None
        return aiohttp, url, headers

    async def _send_with_one_reconnect(
        self, aiohttp_mod: Any, url: str, headers: Dict[str, str], payload: Any, *, what: str
    ) -> Any:
        """Send, and on a dead pooled connection drop the pool and send once more.

        Both recovered cases mean the request **never reached the producer**: a session or loop
        already closed, and a keep-alive the server had closed without telling us, which only
        surfaces on reuse. Neither is a re-send, so neither needs to know whether the route is
        idempotent. A second failure is reported as :class:`~.response.ConnectionLost` rather
        than tried again.
        """
        try:
            return await self._send_once(aiohttp_mod, url, headers, payload)
        except (RateLimited, CallFailure):
            raise
        except RuntimeError as exc:
            if "closed" not in str(exc).lower():
                raise CallFailure(f"POST {url} failed while attempting {what}: {exc}") from exc
            await self._discard_pool()
        except aiohttp_mod.ClientConnectionError as exc:
            logger.debug(
                "Pooled connection dropped while attempting %s (%s: %s); retrying once on a "
                "fresh connection",
                what,
                type(exc).__name__,
                exc,
            )
            await self._discard_pool()

        try:
            return await self._send_once(aiohttp_mod, url, headers, payload)
        except aiohttp_mod.ClientConnectionError as exc:
            raise ConnectionLost(
                f"POST {url} lost its connection twice while attempting {what}: {exc}"
            ) from exc

    async def _discard_pool(self) -> None:
        """Close the pooled session and forget it, so the next send builds a fresh one."""
        http, self._http = self._http, None
        if http is None:
            return
        try:
            await http.close()
        except Exception:  # noqa: BLE001 - the reference is already dropped, so nothing can leak
            logger.debug("Closing a spent pooled session failed", exc_info=True)

    async def aclose(self) -> None:
        """Close the pool. Call from the event loop that sent on it.

        Idempotent, and free on a poster that never sent: the session is built on the first
        send, so there is nothing to close before it.
        """
        await self._discard_pool()


def _retry_after_seconds(value: Any) -> float:
    """``Retry-After`` as seconds, or ``0.0`` when the producer sent nothing usable.

    Only the delta-seconds form is read. The HTTP-date form is legal and lpr-server does not
    send it; parsing a date into a wait would mean trusting two clocks to agree, and a wrong
    answer here pauses a whole camera's plate logging. ``0.0`` means *no hint* -- the caller
    decides what to do about it, which is the point of reporting rather than sleeping.
    """
    try:
        seconds = float(str(value).strip())
    except (TypeError, ValueError):
        return 0.0
    return seconds if seconds > 0 else 0.0


#: Total timeout for one blob PUT, in seconds. Longer than a platform call because the
#: body is an image rather than a document, and the destination is object storage rather
#: than a producer that answers in milliseconds.
UPLOAD_TIMEOUT_S = 30.0


class Uploader:
    """PUT bytes at a URL that already carries its own authorisation.

    **Not a producer route, and deliberately not on a client's route list.** The URL is
    handed over at runtime -- a producer answers a write with the storage address it
    resolved, and the bytes go there next. There is no path template, no base URL and no
    session: a pre-signed URL carries its own credentials in the query string, so adding
    an ``Authorization`` header would be wrong, not merely redundant.

    It lives here rather than in a usecase because it is transport, and because the
    connection pool is this layer's job. The call it replaces opened a fresh
    ``httpx.AsyncClient`` per upload; one session is held here and its connections reused,
    the same reasoning as :class:`PooledPoster`.

    ``aiohttp`` is imported inside the send for the reason the class above gives: ~220 ms
    and ~26 MB at module scope, against this module's own ~11 ms.
    """

    def __init__(self, *, timeout_s: float = UPLOAD_TIMEOUT_S) -> None:
        self._timeout_s = float(timeout_s)
        self._http: Any = None
        #: Whether the current run of failures has been reported. Cleared by the next upload
        #: that succeeds. Same reasoning as :class:`PooledPoster`: this runs per frame, and
        #: ``process_error_log`` does its logging before its own TTL is consulted.
        self._reported = False

    async def put(self, url: str, content: bytes, *, content_type: str = "image/jpeg") -> bool:
        """Send ``content`` to ``url``. ``True`` when the store accepted it.

        Returns ``False`` rather than raising, for every failure: a frame that did not
        reach storage is a lost frame, not a lost request, and the caller's next frame is
        along in milliseconds. The reason is logged once, where it happened.

        Reporting is an explicit call rather than a handler for that same reason -- a refusal
        arrives as a status, not as an exception, so there is nothing for a handler to catch.
        Object storage is reached directly, so nothing else in the stack sees these at all.
        """
        try:
            import aiohttp  # noqa: PLC0415 - see the class docstring

            if self._http is None or self._http.closed:
                self._http = aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self._timeout_s)
                )
            async with self._http.put(
                url, data=content, headers={"Content-Type": content_type}
            ) as reply:
                if 200 <= reply.status < 300:
                    self._reported = False
                    return True
                body = await reply.text()
                logger.error(
                    "Upload to object storage was refused: status=%s body=%s",
                    reply.status,
                    body[:200],
                )
                # Raised and caught rather than constructed, so that it carries a traceback
                # whose innermost frame is this method. py_common keys its deduplication on
                # that frame, and falls back to walking its own caller when an exception has
                # no traceback at all -- which would land every refusal on the reporting
                # helper and let one route's failures hide another's.
                try:
                    raise CallFailure(
                        f"PUT to object storage was refused: status={reply.status}",
                        status_code=reply.status,
                        response=body[:200],
                    )
                except CallFailure as refusal:
                    _report_failure(refusal, latch=self, attr="_reported")
                return False
        except Exception as exc:  # noqa: BLE001 - a lost frame must not reach the frame loop
            logger.error("Upload to object storage failed", exc_info=True)
            _report_failure(exc, latch=self, attr="_reported")
            return False

    async def aclose(self) -> None:
        """Close the pool. Free on a putter that never sent -- it opens nothing until then."""
        http, self._http = self._http, None
        if http is None:
            return
        try:
            await http.close()
        except Exception:  # noqa: BLE001 - the reference is dropped, so the pool cannot leak
            logger.debug("Closing a spent upload session failed", exc_info=True)
