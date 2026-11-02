"""the wizard's one server call (POST /v1/device-state): request, fetch on a thread, one resolver with a fixed deadline."""

from __future__ import annotations

import http.client
import json
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import Future
from dataclasses import dataclass, field
from probe.foundation.compat.compat import StrEnum


#: `POST /v1/device-state`: the account, every agent's capture validity and the
#: version manifest in ONE answer (app/client_version/device_state_router.py).
DEVICE_STATE_PATH = "/v1/device-state"
#: One budget for the one call. It replaced seven serial calls, each with its
#: own, so a slow API now costs this at most once instead of per call.
DEVICE_STATE_TIMEOUT_S = 5.0
#: How much longer than that the caller waits for the thread: urllib's timeout
#: bounds each socket operation, not the whole exchange.
DEVICE_STATE_GRACE_S = 2.0
#: Statuses that mean "ask the old way": the route is missing (404/405), or
#: something in front of the server answered for it (see fetch_device_state).
_ASK_THE_OLD_WAY = frozenset({301, 302, 303, 307, 308, 401, 403, 404, 405})
#: The largest answer read. A real one is well under 2 KiB; a proxy streaming
#: something else must not grow the process.
DEVICE_STATE_MAX_BYTES = 256 * 1024


class DeviceStateOutcome(StrEnum):
    #: The server answered; every field below is its verdict.
    ANSWERED = "answered"
    #: 404/405: a server that predates the route (an older self-hosted API).
    #: The caller falls back to asking the old way.
    UNSUPPORTED = "unsupported"
    #: Offline, timed out, 5xx or garbled: nothing is known.
    UNREACHABLE = "unreachable"


class AccountStatus(StrEnum):
    """The server's vocabulary (`app/client_version/device_state_router.py`)."""

    OK = "ok"
    SIGNED_OUT = "signed_out"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class CaptureStatus(StrEnum):
    OK = "ok"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class DeviceStateRequest:
    """Everything the call needs, resolved on the CALLER's thread.

    Resolution reads files and environment per source with the source passed
    explicitly, so the worker thread that sends it touches no process-wide
    state (the wizard scopes agents through `os.environ["PROBE_AGENT"]`).
    """

    base_url: str
    #: The CLI's API token, or None when signed out (the call works signed out).
    #: Kept out of repr: this object's whole job is to carry secrets.
    token: str | None = field(repr=False)
    #: source -> capture credential, ONLY for credentials whose own base URL is
    #: `base_url`. A credential is never sent to a server that did not issue it.
    capture_tokens: dict[str, str] = field(repr=False)
    #: Sources holding a credential for ANOTHER server. The answer carries no
    #: verdict for them; `doctor.collect()` checks such an agent the old way,
    #: against its own server, when it reads that agent.
    elsewhere: tuple[str, ...] = ()


@dataclass(frozen=True)
class DeviceState:
    outcome: DeviceStateOutcome
    account_email: str | None = None
    #: True = accepted, False = refused (the ONLY state that sends someone back
    #: through sign-in), None = signed out or unknown.
    account_valid: bool | None = None
    #: source -> True accepted / False refused / None unknown. The same
    #: tristate `verify_capture_credential` returns. A source missing here got
    #: no verdict (its credential belongs to another server).
    capture: dict[str, bool | None] = field(default_factory=dict)
    #: Why nothing is known, for the warnings `probe doctor` would print.
    error: str | None = None

    @property
    def answered(self) -> bool:
        return self.outcome is DeviceStateOutcome.ANSWERED


def device_state_request(
    base_url: str, token: str | None, sources: tuple[str, ...]
) -> DeviceStateRequest:
    """Split each source's capture credential by the server it belongs to."""
    base = (base_url or "").strip().rstrip("/")
    here: dict[str, str] = {}
    elsewhere: list[str] = []
    for source in sources:
        resolved = resolved_capture_credential(source)
        if resolved is None:
            continue
        capture_token, capture_base = resolved
        if capture_base == base:
            here[source] = capture_token
        else:
            elsewhere.append(source)
    return DeviceStateRequest(
        base_url=base, token=token or None, capture_tokens=here, elsewhere=tuple(elsewhere)
    )


def _device_state_headers() -> dict[str, str]:
    from probe import __version__
    from probe.foundation.request_identity.request_identity import client_version_headers, device_headers
    from probe.foundation.request_identity.surface import SURFACE_HEADER, Surface

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "probe-wizard/1",
        SURFACE_HEADER: Surface.CLI.value,
        **client_version_headers(Surface.CLI.value, __version__),
    }
    try:
        from probe.sdk.settings.device_identity import device_instance_id

        headers.update(device_headers(device_instance_id()))
    except Exception:  # noqa: BLE001 - identity is telemetry, never a hard failure
        pass
    return headers


_ACCOUNT_VALID: dict[str, bool | None] = {
    AccountStatus.OK: True,
    AccountStatus.REJECTED: False,
    AccountStatus.SIGNED_OUT: None,
    AccountStatus.UNKNOWN: None,
}
_CAPTURE_VALID: dict[str, bool | None] = {
    CaptureStatus.OK: True,
    CaptureStatus.REJECTED: False,
    CaptureStatus.UNKNOWN: None,
}


def _verdict(table: dict[str, bool | None], value: object) -> bool | None:
    """A status word's tristate. Anything else -- a word this CLI does not know,
    or not a word at all -- is unknown, never a refusal."""
    return table.get(value) if isinstance(value, str) else None


def fetch_device_state(
    request: DeviceStateRequest,
    *,
    timeout: float = DEVICE_STATE_TIMEOUT_S,
    deadline: float | None = None,
) -> DeviceState:
    """Ask `POST /v1/device-state`. NEVER RAISES, and never retries.

    Sent with urllib, not the SDK `Client`, on purpose: the SDK transport
    scrubs every JSON body (it would send `<redacted>` in place of each capture
    credential) and refuses a `/v1` call without an API token (this one must
    work signed out). A 200 also refreshes the version cache the Versions row
    is graded against, so no separate manifest fetch is needed.
    """
    if deadline is None:
        deadline = time.monotonic() + timeout + DEVICE_STATE_GRACE_S
    if not request.base_url:
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error="no API base URL configured")
    if _urllib_cannot_reach(request.base_url):
        return DeviceState(DeviceStateOutcome.UNSUPPORTED)
    http_request = urllib.request.Request(
        f"{request.base_url}{DEVICE_STATE_PATH}",
        data=json.dumps({"capture_tokens": request.capture_tokens}).encode("utf-8"),
        headers=_device_state_headers(),
        method="POST",
    )
    if request.token:
        # Unredirected as well as unredirectable: belt and braces for the bearer.
        http_request.add_unredirected_header("Authorization", f"Bearer {request.token}")
    opener = _credential_opener()
    # The WHOLE exchange gets the budget (`deadline`, shared with the readers),
    # not just each socket operation: a peer trickling bytes inside every
    # per-read timeout is cut off here.
    try:
        with opener.open(http_request, timeout=timeout) as response:
            received = bytearray()
            while chunk := response.read1(65536):
                received.extend(chunk)
                if len(received) > DEVICE_STATE_MAX_BYTES:
                    return DeviceState(DeviceStateOutcome.UNREACHABLE, error="answer too large")
                if time.monotonic() > deadline:
                    return DeviceState(DeviceStateOutcome.UNREACHABLE, error="answer too slow")
    except urllib.error.HTTPError as exc:
        # 404/405: a server without the route. A redirect, 401 or 403 cannot
        # come from the route (it is public and never redirects), so something
        # in front of it -- an SSO proxy, a firewall -- answered: ask the old
        # way, which behaves in that network exactly as it did before.
        if exc.code in _ASK_THE_OLD_WAY:
            return DeviceState(DeviceStateOutcome.UNSUPPORTED)
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error=f"HTTP {exc.code}")
    except ValueError:
        # http.client refuses an invalid header VALUE with the value in the
        # message -- a bearer with a stray newline. Never echo it.
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error="the request could not be sent")
    except (
        urllib.error.URLError,
        http.client.HTTPException,  # a truncated or garbled response; not an OSError
        TimeoutError,
        OSError,
    ) as exc:
        return DeviceState(
            DeviceStateOutcome.UNREACHABLE,
            error=str(getattr(exc, "reason", None) or exc) or type(exc).__name__,
        )
    try:
        body = json.loads(bytes(received).decode("utf-8"))
    except ValueError:
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error="malformed answer")
    if not isinstance(body, dict):
        return DeviceState(DeviceStateOutcome.UNREACHABLE, error="malformed answer")
    account = body.get("account") if isinstance(body.get("account"), dict) else {}
    answered_capture = body.get("capture") if isinstance(body.get("capture"), dict) else {}
    capture = {
        source: _verdict(_CAPTURE_VALID, answered_capture.get(source))
        for source in request.capture_tokens
    }
    manifest = body.get("versions") if isinstance(body.get("versions"), dict) else None
    # A pod that has not fetched the manifest yet answers every pair empty.
    # Caching THAT as a good fetch would blank a perfectly good cached one.
    publishes_a_version = manifest is not None and any(
        isinstance(pair, dict) and pair.get("latest") for pair in manifest.values()
    )
    # Too late to be anyone's answer (the readers have moved on): too late to
    # overwrite the cache they graded against, too.
    if publishes_a_version and time.monotonic() <= deadline:
        try:
            from probe.shared.updates import version_policy

            version_policy.write_cache(manifest, True)
        except Exception:  # noqa: BLE001 - a version cache must never break the menu
            pass
    email = account.get("email")
    return DeviceState(
        DeviceStateOutcome.ANSWERED,
        account_email=email if isinstance(email, str) and email else None,
        account_valid=_verdict(_ACCOUNT_VALID, body.get("account_status")),
        capture=capture,
    )


def start_device_state(
    request: DeviceStateRequest,
    *,
    warm_manifest_on_fallback: bool = False,
    deadline: float | None = None,
) -> DeviceStateResolver:
    """Send the call on a daemon thread and return its resolver at once.

    ONE deadline, fixed here, for the worker and every reader: an answer the
    readers gave up on is nobody's, and must not write the version cache after
    them either. A daemon thread, not an executor: an executor's workers are
    joined at interpreter exit, so quitting the wizard while a call was pending
    would wait out its timeout. `deadline` (`time.monotonic`) makes it sooner
    than the call's own budget (`probe status --refresh --timeout`)."""
    future: Future = Future()
    own = time.monotonic() + DEVICE_STATE_TIMEOUT_S + DEVICE_STATE_GRACE_S
    deadline = own if deadline is None else min(own, deadline)

    def run() -> None:
        try:
            state = fetch_device_state(request, deadline=deadline)
        except BaseException as exc:  # noqa: BLE001 - fetch never raises; belt and braces
            future.set_exception(exc)
            return
        # The verdict first, so an older server's "unsupported" reaches the
        # readers (and their fallback to the old calls) without waiting on it...
        future.set_result(state)
        if state.outcome is DeviceStateOutcome.UNSUPPORTED and warm_manifest_on_fallback:
            # ...then the manifest the old way carries none of, as the wizard
            # always fetched it, or an older server's Versions row goes stale.
            from probe.shared.updates import updates as versions_mod

            versions_mod.warm_manifest()

    threading.Thread(target=run, name="probe-device-state", daemon=True).start()
    return DeviceStateResolver(future, deadline=deadline)


def device_state_result(
    future: Future, *, timeout: float = DEVICE_STATE_TIMEOUT_S + DEVICE_STATE_GRACE_S
) -> DeviceState:
    """The call's answer, or UNREACHABLE when it has none in time. Never raises."""
    try:
        return future.result(timeout=timeout)
    except Exception as exc:  # noqa: BLE001 - a menu must render without it
        return DeviceState(
            DeviceStateOutcome.UNREACHABLE, error=f"no answer ({type(exc).__name__})"
        )


class DeviceStateResolver:
    """The one answer every reader of a call gets, with ONE deadline fixed when
    the call starts. Call it to get the answer.

    Several agents read the same call. Waiting a fresh timeout each would cost a
    stuck call once per agent, and could hand one agent UNREACHABLE and the next
    the late answer; the first resolution is everyone's."""

    def __init__(
        self,
        future: Future,
        *,
        timeout: float = DEVICE_STATE_TIMEOUT_S + DEVICE_STATE_GRACE_S,
        deadline: float | None = None,
    ) -> None:
        self._future = future
        self.started = time.monotonic()
        self._deadline = deadline if deadline is not None else self.started + timeout
        self._answer: DeviceState | None = None
        self._lock = threading.Lock()

    def __call__(self) -> DeviceState:
        with self._lock:
            if self._answer is None:
                remaining = max(0.0, self._deadline - time.monotonic())
                self._answer = device_state_result(self._future, timeout=remaining)
            return self._answer

    def stale(self, max_age_s: float) -> bool:
        """Worth asking again: older than `max_age_s`, or read and not an answer."""
        if time.monotonic() - self.started > max_age_s:
            return True
        return self._answer is not None and not self._answer.answered


def device_state_resolver(
    future: Future, *, timeout: float = DEVICE_STATE_TIMEOUT_S + DEVICE_STATE_GRACE_S
) -> DeviceStateResolver:
    return DeviceStateResolver(future, timeout=timeout)


def answered_already(state: DeviceState) -> DeviceStateResolver:
    """A resolver for a state known without a call (the request could not even
    be built)."""
    done: Future = Future()
    done.set_result(state)
    return DeviceStateResolver(done)
from probe.cli.wizard.state.capture_credentials import resolved_capture_credential  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.state.credential_http import _credential_opener, _urllib_cannot_reach  # noqa: E402 -- pieces need each other; the front door loads this one first
