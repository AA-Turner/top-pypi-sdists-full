"""Reading a backend reply: one unwrap per producer, plus the client's error type.

Three backends answer this SDK, and they answer in three different shapes. That
is a property of the backends, not an accident of how the calling code grew, so
this module offers three unwraps rather than one shared envelope:

``unwrap_platform``
    The platform API wraps every reply in ``{success, code, message, data}``.
    Success is decided by ``success`` **alone**.

``unwrap_fr_sidecar``
    The facial-recognition sidecar also gates on ``success``, but one of its
    routes answers with a bare body and no envelope at all.

``unwrap_lpr_server``
    lpr-server returns the created document itself. A successful reply carries
    nothing to gate on; only the failure path is enveloped.

A single shared envelope cannot serve these. One that required ``success`` would
reject every successful lpr-server reply, and one that also required
``code == 200`` would additionally misread a platform reply that succeeded with
some other 2xx -- a created resource answering ``201`` being the ordinary case.

Failures raise :class:`CallFailure`. Absence does not: a document that does not
exist is an answer, and the distinction is what keeps a caller from spending
another attempt on a question the backend has already settled.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "CallFailure",
    "unwrap_fr_sidecar",
    "unwrap_lpr_server",
    "unwrap_platform",
]


class CallFailure(Exception):  # noqa: N818 - a call failure is what it reports
    """A backend call did not succeed.

    Deliberately **not** related to ``AppBundleError``, which is not a general
    "something went wrong" type: it means *"this bundle candidate did not work,
    try the next one"*, and the bundle machinery catches it in order to fall
    back to a different candidate. A client raising it would silently trigger
    that fallback from an unrelated call.

    It also derives from ``Exception`` rather than ``RuntimeError`` -- which is
    where ``AppBundleError`` sits -- so that an unrelated ``except
    RuntimeError`` elsewhere in the SDK cannot absorb a client failure by
    accident.

    Callers decide the policy, so this type carries the facts rather than a
    verdict. One caller translates it into a bundle error at its own boundary;
    another reports it and degrades. Both need something to read. The fields are
    what the backends actually put on their failure paths, and each is ``None``
    when that backend did not supply it:

    ``code``
        The application-level code from an envelope, where there is one.
    ``status_code``
        The HTTP status, as the RPC layer records it on the envelope.
    ``tracking_code``
        The correlation id an lpr-server error envelope carries.
    ``response``
        The decoded body exactly as received, for a caller needing something
        none of the above captured.

    The message is human-readable only, and must not be the sole carrier of
    anything a caller acts on: error reporting deduplicates on exception type,
    file and function, and never reads the message text, so two different
    failures raised from one function collapse into a single report.
    """

    def __init__(
        self,
        message: str,
        *,
        code: Any = None,
        status_code: Any = None,
        tracking_code: Any = None,
        response: Any = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.tracking_code = tracking_code
        self.response = response


def _is_not_found(response: Any) -> bool:
    """True when ``response`` is ``matrice_common``'s canonical 404 envelope.

    ``rpc._execute_request`` short-circuits **every** 404 into ``_not_found_response()`` and never
    raises, so "the document does not exist" arrives looking exactly like a failed call. It is
    distinguishable only by the ``status_code`` the envelope carries, and telling the two apart is
    what lets a fetcher honour its documented "returns nothing when absent" contract instead of
    escalating a perfectly good answer into another attempt.
    """
    return isinstance(response, dict) and response.get("status_code") == 404


def _failure_detail(response: Any) -> str:
    """Summarise why a reply was read as a failure, for a ``CallFailure`` message.

    Prefers whatever the backend said itself, since that is the part a reader
    can act on. Falls back to the status fields, and finally to the body's type,
    so the message is never empty even when the reply is a shape we did not
    expect at all.
    """
    if not isinstance(response, dict):
        return f"body was {type(response).__name__}, not an envelope"

    for key in ("message", "error"):
        value = response.get(key)
        if isinstance(value, str) and value:
            return value

    for key in ("code", "status_code"):
        value = response.get(key)
        if value is not None:
            return f"{key}={value!r}"

    return "the reply carried no message, error or status"


def _failure_fields(response: Any) -> dict[str, Any]:
    """Collect the failure fields the backends report, for a ``CallFailure``.

    Each backend supplies a different subset, so a key is ``None`` whenever the
    reply did not carry it -- the attributes still exist, so a caller can read
    them unconditionally rather than guarding every access.

    ``trackingCode`` is the lpr-server error envelope's spelling; ``code`` and
    ``status_code`` are shared with the platform envelope.
    """
    if not isinstance(response, dict):
        return {"response": response}

    return {
        "code": response.get("code"),
        "status_code": response.get("status_code"),
        "tracking_code": response.get("trackingCode"),
        "response": response,
    }


def unwrap_platform(response: Any, *, what: str) -> Any:
    """Return the ``data`` payload from a platform API envelope.

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
    if not isinstance(response, dict):
        raise CallFailure(
            f"{what} did not succeed: {_failure_detail(response)}",
            **_failure_fields(response),
        )

    if response.get("success"):
        return response.get("data")

    if _is_not_found(response):
        return None

    raise CallFailure(
        f"{what} did not succeed: {_failure_detail(response)}",
        **_failure_fields(response),
    )


def unwrap_fr_sidecar(response: Any, *, what: str) -> Any:
    """Return the payload from a facial-recognition sidecar reply.

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
    if isinstance(response, dict) and "success" in response:
        if response.get("success"):
            return response.get("data")
        if _is_not_found(response):
            return None
        raise CallFailure(
            f"{what} did not succeed: {_failure_detail(response)}",
            **_failure_fields(response),
        )

    return response


def unwrap_lpr_server(response: Any, *, what: str) -> Any:
    """Return the payload from an lpr-server reply.

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
    if isinstance(response, dict) and response.get("success") is False:
        raise CallFailure(
            f"{what} did not succeed: {_failure_detail(response)}",
            **_failure_fields(response),
        )

    return response
