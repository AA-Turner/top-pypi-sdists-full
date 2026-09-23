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

