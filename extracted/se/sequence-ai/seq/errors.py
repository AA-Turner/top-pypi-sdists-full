"""
The errors `seq` raises, of two kinds kept apart on purpose.

What is wrong with how a policy, benchmark or adapter was written — `SeqAuthoringError` and its subclasses — is found
here, before anything is sent, and is never a server's answer.

What the platform answered, or could not be asked, is the one hierarchy the client raises (`sequence_ai.errors`:
InvalidRequest, AuthError, PermissionDenied, OutOfCredit, NotFound, Conflict, Gone, Unavailable, InternalError …),
built by its one mapping, `from_response`. So a refusal reads the same from `seq deploy`, `seq.eval(...)` and
`connect()`: switch on `.code`, show `.hint`, quote `.request_id`. The helpers at the bottom are how every `seq` module
gets there.

WHY a single readable exception class for authoring: every S1 failure mode is a *registration-time* rejection that
must surface a message the robot engineer can act on, not a stack trace that blows up when the harness
later tries to load the class. The goal asks, again and again, that it be "refused at registration with a
readable error, never left as a string that blows up when the harness loads it".


"""
from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any, Iterable, Iterator

from sequence_ai.errors import AuthError, Conflict, SequencesError, Unavailable, from_response

from sequence_ai.errors import MissingPackage


class SeqAuthoringError(Exception):
    """Base for anything wrong with how a user wrote their `@seq.*` policy."""


class PolicyDefinitionError(SeqAuthoringError):
    """A decorated policy class (or a decorator argument) is malformed and cannot be registered."""


class BenchmarkDefinitionError(SeqAuthoringError):
    """A `@seq.benchmark` class (or a decorator argument) is malformed and cannot be registered.

    Symmetric to `PolicyDefinitionError`: benchmark is the platform's second authorizable artifact
    (§8), authored with the same decorator+lifecycle pattern, so its malformed-at-registration failures
    get their own readable exception rather than an AttributeError at eval time.

    """


class AdapterDefinitionError(SeqAuthoringError):
    """A `@seq.adapter` class is malformed: its name or pairs are invalid, it lacks its @seq.observation or @seq.action
    method, or one cannot take the one value it is handed.
    """


class GpuRenderError(RuntimeError):
    """A GPU benchmark's cameras cannot be drawn on this machine's card. Raise it from your benchmark's `__init__` (or
    anything it calls) when the renderer did not reach the GPU - EGL or Vulkan would not start, or the GL it got is a
    software one (Mesa's llvmpipe) - rather than drawing on the CPU: the platform starts the benchmark machine again on
    another GPU, and with none left ends the eval (stop reason `no_gpu_render`, this error's fields in its sentence). A
    machine that could not draw is not billed. A GPU benchmark is never drawn in software.

        raise seq.GpuRenderError(gl=gl_renderer, backend="egl", egl=str(err))

    `gl`: the GL (or device) the renderer got, when it got one; `backend`: what it drew with (egl, osmesa, vulkan);
    `egl`: that backend's own error. All three are optional and kept as `gpu_render`, which the platform reads.
    
"""

    def __init__(self, message: str | None = None, *, gl: str | None = None, backend: str | None = None,
                 egl: str | None = None) -> None:
        self.gpu_render = {"gl": gl, "backend": backend, "egl": egl}

        super().__init__(f"{message or 'this GPU cannot draw the cameras'}: {json.dumps(self.gpu_render)}")



def raise_for(r: Any, *, redact: Iterable[str] = ()) -> None:
    """Nothing for a 2xx response; otherwise raise the exception `from_response` maps it to.

    `redact` lists values the request carried that the answer must not repeat — a secret write, whose refusal may
    echo the body. They are masked in every field of the answer, and its raw text is dropped."""
    if r.status_code // 100 == 2:
        return
    try:
        body = r.json()
    except ValueError:
        body = None
    values = sorted((v for v in redact if v), key=len, reverse=True)
    if values:
        raise from_response(r.status_code, _masked(body, values), headers=r.headers)
    raise from_response(r.status_code, body, text=r.text[:500], headers=r.headers)


def _masked(v: Any, values: list[str]) -> Any:
    if isinstance(v, str):
        for s in values:
            v = v.replace(s, "***")
        return v
    if isinstance(v, dict):
        return {k: _masked(x, values) for k, x in v.items()}
    if isinstance(v, list):
        return [_masked(x, values) for x in v]
    return v


def unreachable(base: str, why: object) -> Unavailable:
    """A request that never got an answer (`why`: the transport's error, or its text - a read asked again on every
    try, seq._http's sentence). Retryable, like every 5xx: nothing was done, so nothing was billed."""
    return Unavailable(f"could not reach the platform at {base}: {why}")


def transport_said(exc: Exception) -> str:
    """A failed connection in a reader's words, where the transport's own said it in its terms ("[Errno 54] Connection
    reset by peer", "Server disconnected without sending a response", "The read operation timed out"): seq._http says
    each retry and its last failure so."""
    import httpx

    if isinstance(exc, httpx.ConnectTimeout):
        return "no connection within the time allowed"
    if isinstance(exc, httpx.TimeoutException):
        return "no answer within the time allowed"
    if isinstance(exc, httpx.RemoteProtocolError):
        return "the connection closed before the answer came"
    text = str(exc)
    if "reset" in text.lower():
        return "the connection was reset"
    if isinstance(exc, httpx.ReadError):
        return "the connection dropped while the answer came"
    return text or type(exc).__name__


def no_api_key() -> AuthError:
    """Refused before any request: nothing is ever sent without a key or your sign-in."""
    return AuthError("no API key: set SEQUENCES_API_KEY, or sign in with seq login "
                     "(keys are made at https://app.generalsequences.com/)")


def build_failed(what: str, error: str | None, *, hint: str | None = None) -> Conflict:
    """A build that ended `failed`. What it built is now in the failed state — what a connect to it reports too
    (409, `details.state`) — so it is the same Conflict, not a class of its own. A build its owner canceled, or stopped
    at the time they gave it, is said canceled, never failed to build (canceled())."""
    if canceled(error):
        return Conflict(f"{what} was canceled: {str(error).removeprefix(CANCELED)}", details={"state": "failed"},
                        hint=hint)
    return Conflict(f"{what} failed to build: {error or 'no reason reported'}", details={"state": "failed"}, hint=hint)





CANCELED = "canceled: "


def canceled(error: str | None) -> bool:
    """Whether a failed build's error says it ended at its owner's word: `seq benchmark cancel`, or the time a deploy gave
    it (out_of_time)."""
    return str(error or "").startswith(CANCELED)




TIME_LIMIT = f"{CANCELED}stopped at its time limit"


def out_of_time(error: str | None, command: str) -> str | None:
    """What a build stopped at the time `--timeout` gave it leaves to do, with `command`, what started it; None for any
    other end."""
    if not str(error or "").startswith(TIME_LIMIT):
        return None
    return (f"the time --timeout gave it ran out: the platform stopped it, its machines have ended and what ran until "
            f"then is billed; run {command} again with more time, or with no --timeout")


def state_said(status: str, error: str | None) -> str:
    """A benchmark's state in words: its platform's `status`, but canceled for a registration its owner canceled, which
    is failed by no fault of its own. What a script reads (--json, seq.benchmarks()) stays the platform's.
    
"""
    return "canceled" if status == "failed" and canceled(error) else status


class LeftRunning(KeyboardInterrupt):
    """Ctrl-C while a command followed a build: the command ends and the build does not, running on the platform, billed,
    whatever this terminal does. Its text is what the command ends in, where "cancelled" told its owner it had stopped.
    `stop`: what ends it now, said only where a command does without taking more than the build.
    """

    def __init__(self, what: str, limit_s: float | None, stop: str | None = None) -> None:
        until = "it ends" if limit_s is None else f"it ends or the {limit_s:.10g} s --timeout gave it run out"
        super().__init__(f"not canceled: {what} keeps building on the platform, billed, until {until}"
                         + (f"; {stop}" if stop else ""))


@contextmanager
def following(what: str, limit_s: float | None, stop: str | None = None) -> Iterator[None]:
    """A command following a build: Ctrl-C in it is LeftRunning."""
    try:
        yield
    except KeyboardInterrupt:
        raise LeftRunning(what, limit_s, stop) from None


def still_building(what: str, follow: str, *, stalled_s: float | None = None) -> Unavailable:
    """The wait ended while the build went on: not abandoned, and worth waiting on again (`timeout`, retryable). Its
    window ran out - or, `stalled_s`, its build log stood still that long, which is said as such: the two read as one
    sentence, and a user could not tell a wait of theirs run out from a build that stopped moving."""
    if stalled_s:
        return Unavailable(f"{what} is still building, and its build log has not moved in the last "
                           f"{stalled_s / 60:.0f} min; it was not abandoned", code="timeout",
                           details={"state": "building", "log_still_s": round(stalled_s)}, hint=follow)
    return Unavailable(f"{what} is still building after the wait window; it was not abandoned", code="timeout",
                       details={"state": "building"}, hint=follow)
