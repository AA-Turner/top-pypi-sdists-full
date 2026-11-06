"""
Typed errors: one hierarchy for every error the platform sends.

WHY typed rather than one generic exception: a robot controller has to react differently to
each of these. `OutOfCredit` should stop the run and page a human; `Unavailable` is worth one
retry; `InvalidRequest` will fail identically forever and retrying it just burns the window.
A single exception type forces the caller to parse strings to tell them apart, and string
parsing breaks the first time the wording is improved.

Every error response has one body — `detail`, `code`, `retryable`, `retry_after_s`, `request_id`,
`hint`, `details` — and `from_response` below is the only place that turns one into an exception:
the code picks the class (the status only when a body carries no code: a proxy in between), and every
field rides along. Switch on `.code`, show `.hint`, quote `.request_id` when
reporting a problem. The one exception is `policy_error`: your deployed policy's own code failed, so a
Python built-in exception comes back as itself, with `.remote_traceback` attached.
"""

from __future__ import annotations

import builtins
import logging
import re
from typing import Any, Dict, Mapping, Optional

from ._core.capacity import SHORTFALL, explain
from ._core.error_codes import CODES, code_for_status


class SequencesError(Exception):
    """Base for everything this library raises. Catch this to catch all of ours and none of httpx's."""


    default_code: Optional[str] = "internal"

    def __init__(self, message: str, *, status: Optional[int] = None, code: Optional[str] = None,
                 retryable: Optional[bool] = None, retry_after_s: Optional[float] = None,
                 request_id: Optional[str] = None, hint: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None, body: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code or self.default_code
        spec = CODES.get(self.code) if self.code else None
        self.retryable = retryable if retryable is not None else bool(spec and spec.retryable)



        self.retry_after_s = retry_after_s
        self.request_id = request_id
        self.hint = hint
        self.details: Dict[str, Any] = dict(details or {})
        self.body = body

    def __str__(self) -> str:
        """The message and, when it has one, its hint: print(e) is how most callers read an error, and a hint kept in
        .hint alone was never seen there - a model that always reasons, refused effort none, read only the provider's
        words.

        An answer the platform gave, which carries its request's id, also says why - its reason (stopped, queue_timeout,
        budget, ...), else its code - and that id, the same way for every refusal: the id is what `seq policy logs
        <name> --rid <id>` finds the request by. A check of this library's own (no id) reads as before.
        
"""
        out = f"{self.message} (hint: {self.hint})" if self.hint else self.message
        if self.request_id:
            reason = self.details.get("reason")
            out += f" [{reason if isinstance(reason, str) and reason else self.code}, request {self.request_id}]"
        return out


class InvalidRequest(SequencesError):
    """
    400 / 413. Something about the request itself is wrong — a malformed observation, a body over
    the size limit, the wrong endpoint for that model.

    Deterministic: the identical request will fail the identical way. Do not retry.
    """

    default_code = "invalid_request"


class MissingPackage(SequencesError):
    """This machine lacks a package a call needs - an optional extra of sequence-ai, whose install command the hint
    says: installing it is the fix, and the same call fails the same way until then. Nothing about the request or the
    platform is wrong: `seq` says error[missing_package] and exits 1. Here, not in seq, because a robot - which has no
    seq - raises it too: observe() with a Video, Depth or Tactile item and no `sequence-ai[observe]`. Before, the LeRobot
    export said error[invalid_request], the platform's word for a request that is wrong, and observe() a bare
    `ModuleNotFoundError: No module named 'av'` from deep in sequence-base's encoder (0.55.1).

"""

    default_code = "missing_package"


class AuthError(SequencesError):
    """401. The key is missing, revoked, or expired. Retrying will not help."""

    default_code = "unauthenticated"


class PermissionDenied(SequencesError):
    """403. The key is valid but may not do this: a robot key used for chat, a key bound to another
    deployment. Use a key that is allowed."""

    default_code = "forbidden"


class OutOfCredit(SequencesError):
    """
    402. `code == "insufficient_credit"`: this month's usage reached the plan's monthly limit (it resets on
    the 1st), or usage past the monthly credit needs a payment method the account does not have, or the key's
    own credit limit is reached - the detail says which; `code == "budget_exhausted"`: the deployment's own
    monthly budget is.

    Distinct from AuthError because the remedy is different and so is the urgency: the key is
    fine, the account simply cannot pay for the next call. A control loop should stop and
    hold, not retry.
    """

    default_code = "insufficient_credit"


class NotFound(SequencesError):
    """404. It does not exist, or it is not yours — another account's deployment reads as missing.
    To start from a template: `seq init <template>`, then `seq deploy`."""

    default_code = "not_found"


class Conflict(SequencesError):
    """409. It conflicts with the current state: the name is taken; the deployment is building,
    failed or stopped; the account is at a limit. `details["reason"]` says which."""

    default_code = "conflict"


class NewVersion(Conflict):
    """409. A new version of the policy went live, or a rollback made another serve: that ended this connection, whatever
    it was doing, and it does not go on on the version that serves by itself. Every call on it raises this. connect()
    again reaches that version. `.version` names it. {the user 11-05: "we dont route it", "user should jsut reconnect"}"""

    @property
    def version(self) -> Optional[int]:
        return self.details.get("version")




PLANNERS_GONE = ('@seq.planner is gone: planning is part of the policy now. Put a @seq.plan method in your @seq.policy '
                 'class - def plan(self, robot), returning the next step - and connect to the policy by its name, '
                 'connect("<policy>").')


class Gone(SequencesError):
    """410. The name existed and was retired on purpose; it will not come back. `.replacement` names
    what to use instead (a model id, or `template:<name>` to deploy as your own), `.hint` how."""

    default_code = "gone"

    @property
    def since(self) -> Optional[str]:
        return self.details.get("since")

    @property
    def reason(self) -> Optional[str]:
        return self.details.get("reason")

    @property
    def replacement(self) -> Optional[str]:
        return self.details.get("replacement")


class Unavailable(SequencesError):
    """
    429 / 502 / 503 / 504, a transport failure, or an answer no server of ours wrote (`not_the_platform`).

    The one category where a retry is meaningful — an upstream provider was briefly
    unreachable, a worker was cold, or (429, `code == "busy"`) every replica was busy with
    another request. Note that a failed call is **not** billed, so a retry costs nothing but
    time (a cold worker it started is billed from its GPU - a CPU worker from when it starts - as any worker). A
    direct-connect act already retries a
    busy worker itself, inside its timeout.

    Two of these are worth distinguishing, and the gateway already does:

        `warming` is True when the model is loading rather than broken. The request will
        succeed shortly and the only useful action is to wait `retry_after_s` seconds. This
        is not a hypothetical margin — a cold worker takes a few minutes (a pi05-class policy on a new
        machine: about 9 minutes).


        `warming` is False for everything else — an upstream blip, a timeout, a gateway that
        cannot be reached. Here a retry is a guess rather than a plan.

    Collapsing the two into one class left a controller unable to tell "wait two minutes" from
    "stop and page someone", which are opposite instructions.

    `queued` is the third case: every slot of the deployment is taken and no GPU is left, so the
    robot waits in line before its control loop starts (`details` carries `queue_position`,
    `queued_s`, `queue_timeout_s`). Like warming it is a wait, and `connect()` waits it out before
    the first action; `details["reason"]` says why there is no slot (see `.message`).
    """

    default_code = "unavailable"

    def __init__(self, message: str, *, warming: bool = False, job_id: Optional[str] = None,
                 **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.warming = warming or self.code == "warming"

        self.job_id = job_id

    @property
    def queued(self) -> bool:
        """True when the platform put this robot in line for a seat."""
        return self.details.get("queue_position") is not None

    @property
    def queue_position(self) -> Optional[int]:
        """1 for the front of the line; None when not queued."""
        pos = _number(self.details.get("queue_position"))
        return int(pos) if pos is not None else None


class PolicyError(SequencesError):
    """
    500 `policy_error`: your deployed policy's own code raised, or returned something its declared
    contract does not allow. `.exception_type` names what it raised and `.remote_traceback` holds the
    frames of your own code. A Python built-in exception (ValueError, KeyError, …) is raised as itself
    instead of as this class, with the same `.remote_traceback`.
    """

    default_code = "policy_error"

    def __init__(self, message: str, *, exception_type: Optional[str] = None,
                 remote_traceback: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.exception_type = exception_type
        self.remote_traceback = remote_traceback


class InternalError(SequencesError):
    """500 `internal` (a bug on our side) or 424 `dependency_missing` (a worker could not start: a
    secret its deployment references is gone). Report it with `.request_id`."""

    default_code = "internal"


class StreamRefused(SequencesError):
    """A robot's stream to its worker was answered with anything but the upgrade: a proxy or firewall on the way that lets
    no WebSocket through (`hint` says what to do). A robot's requests reach its worker on that stream alone."""

    default_code = "stream_refused"


class CertPinError(SequencesError):
    """
    A worker's TLS certificate did not match the fingerprint the gateway pinned, or no usable
    fingerprint was given to pin - or, for a worker the platform has checked by the CAs instead
    (connect's tls "public"), its certificate is not valid for the name it was given.

    Fail-closed and deliberately fatal: the worker is a bare public IP with a self-signed
    certificate, so accepting a certificate that does not match the pin — or falling back to
    default-CA trust when the pin is missing or malformed — is a plaintext man-in-the-middle,
    which is exactly what pinning the fingerprint exists to prevent. Retrying will not help; the
    remedy is a correct fingerprint from a fresh connect, not another attempt against the same
    certificate. Carries no secret and names neither digest, because the only actionable fact is
    that the connection was refused.
    """

    default_code = None


_CLASSES: Dict[str, type] = {c.__name__: c for c in (
    InvalidRequest, AuthError, PermissionDenied, OutOfCredit, NotFound, Conflict, Gone, Unavailable,
    PolicyError, InternalError)}


def _number(v: Any) -> Optional[float]:
    try:
        return float(v) if v is not None and not isinstance(v, bool) else None
    except (TypeError, ValueError):
        return None


def from_response(status: int, body: Any = None, *, text: Optional[str] = None,
                  headers: Optional[Mapping[str, str]] = None) -> BaseException:
    """
    The exception for one non-2xx response — from the gateway, a worker, or any `seq` call. The only
    place the SDK maps a server error to a class.

    `body` is the parsed JSON (anything else is treated as no body), `text` the raw response, `headers`
    the response headers (any mapping with `.get`, such as httpx's).
    """
    b: Dict[str, Any] = body if isinstance(body, dict) else {}
    code = b.get("code") if b.get("code") in CODES else None
    detail = b.get("detail")
    details = b.get("details") if isinstance(b.get("details"), dict) else {}
    retry = _number(b.get("retry_after_s"))
    if code is None:
        code = code_for_status(status)

    if retry is None and headers is not None:
        retry = _number(headers.get("Retry-After"))
    rid = b.get("request_id") or (headers.get("X-Seq-Request-Id") if headers is not None else None)


    message = str(detail or f"HTTP {status}")


    if status == 405:
        message = "the platform does not support this yet: this sequence-ai is newer than the platform it asks"



    if details.get("reason") in SHORTFALL:
        message = explain(details, retry_after_s=retry) or message
    retryable = b.get("retryable") if isinstance(b.get("retryable"), bool) else None
    common: Dict[str, Any] = dict(status=status, code=code, retryable=retryable, retry_after_s=retry,
                                  request_id=rid, hint=b.get("hint"), details=details, body=text)

    if code == "policy_error":
        return _policy_exception(message, common)
    cls = _CLASSES.get(CODES[code].sdk_class, SequencesError)
    if cls is Conflict and details.get("reason") == "new_version":
        return NewVersion(message, **common)
    if cls is Unavailable:
        return Unavailable(message, warming=code == "warming", job_id=details.get("job_id"), **common)
    return cls(message, **common)


NOT_THE_PLATFORM = "not_the_platform"


def not_the_platform(status: int, *, text: Optional[str] = None,
                     headers: Optional[Mapping[str, str]] = None) -> Unavailable:
    """The error for a non-2xx from the gateway's address that no server of ours wrote - no error body of ours, no
    request id: something between this machine and the platform answered, so the platform has not answered, and a 404
    here says nothing of a deployment. An Unavailable, as a call that never arrived is, its status kept. What answered
    goes in `details` and the sequence_ai logger's INFO, never the message, whose words a user reads: "HTTP <status>",
    as from_response says a proxy's page.
    
"""
    said = {name: headers.get(name) for name in ("via", "server")} if headers is not None else {}
    details: Dict[str, Any] = {"reason": NOT_THE_PLATFORM, **{k: v for k, v in said.items() if v},
                               **({"head": text[:80]} if text else {})}
    logging.getLogger("sequence_ai").info("HTTP %s from no server of ours: %s", status, details)
    return Unavailable(f"HTTP {status}", status=status, code="upstream_error", retryable=True, details=details,
                       body=text, hint="something between this machine and the platform answered, not the platform: it "
                                       "usually passes; if it goes on, check base_url and this network's proxy")





_PLATFORM_FRAME = re.compile(r'^\s*File "/(?:root/harness|opt/harness|app/sequences)[^"]*"')
_USER_CODE = re.compile(r"/root/seq_(?:user|bench)/code/")


def user_traceback(tb: Any) -> Any:
    """`tb` without the platform's frames; anything that is not a str as it is."""
    if not isinstance(tb, str):
        return tb
    out, under_platform = [], False
    for line in tb.splitlines():
        if _PLATFORM_FRAME.match(line):
            under_platform = True
            continue
        if under_platform and line.startswith("    "):
            continue
        under_platform = False
        out.append(_USER_CODE.sub("", line))
    return "\n".join(out)


def _policy_exception(message: str, common: Dict[str, Any]) -> BaseException:
    """A built-in exception raised by the policy comes back as itself; anything else as PolicyError."""
    info = common["details"].get("exception") if isinstance(common["details"].get("exception"), dict) else {}
    etype, emsg, tb = info.get("type"), info.get("message"), user_traceback(info.get("traceback"))
    builtin = getattr(builtins, etype, None) if isinstance(etype, str) else None
    if isinstance(builtin, type) and issubclass(builtin, Exception):
        try:
            err = builtin(emsg if emsg is not None else message)
        except Exception:
            err = None
        if err is not None:
            err.remote_traceback = tb
            err.request_id = common["request_id"]
            err.code = "policy_error"
            return err
    return PolicyError(message, exception_type=etype, remote_traceback=tb, **common)
