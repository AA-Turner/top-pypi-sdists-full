"""Auto-generated stub for module: response."""
from typing import Any

# Functions
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

# Classes
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

