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
from typing import Any, Iterable

from sequence_ai.errors import AuthError, Unavailable, from_response

from sequence_ai.errors import MissingPackage


class SeqAuthoringError(Exception):
    """Base for anything wrong with how a user wrote their `@seq.*` policy."""


class PolicyDefinitionError(SeqAuthoringError):
    """A decorated policy class (or a decorator argument) is malformed and cannot be registered."""


class BenchmarkDefinitionError(SeqAuthoringError):
    """A `@seq.benchmark` class (or a decorator argument) is malformed.

    `@seq.benchmark` is for writing a benchmark's code and running it on your own machine; on the platform an eval
    runs our benchmarks' tasks, `seq eval run <policy> --task <id> ...`. It is written with the same decorator and
    lifecycle pattern as a policy, so a malformed declaration gets its own readable exception where it is written,
    symmetric to `PolicyDefinitionError`, rather than an AttributeError later.

    """





BENCHMARK_IS_LOCAL = ("a @seq.benchmark is for writing a benchmark's code and running it on your own machine; on the "
                      "platform, seq eval run <policy> --task <id> ... runs our benchmarks' tasks")


class AdapterDefinitionError(SeqAuthoringError):
    """A `@seq.adapter` class is malformed: its name or pairs are invalid, it lacks its @seq.observation or @seq.action
    method, or one cannot take the one value it is handed.
    """


class GpuRenderError(RuntimeError):
    """A GPU benchmark's cameras cannot be drawn on this machine's card. A benchmark raises it from its `__init__` (or
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



