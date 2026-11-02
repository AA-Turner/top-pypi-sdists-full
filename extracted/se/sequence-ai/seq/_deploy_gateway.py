"""
The gateway client for `seq deploy` — submit a deployment and poll its async build to a terminal
state. This is S3's only network surface: `POST /v1/deployments` (the introspected payload) and
`GET /v1/deployments/{id}` (building → ready | failed).

The real gateway over httpx, authed `Authorization: Bearer <SEQUENCES_API_KEY>`. The base URL `mock`
selects the SDK's own test fixture instead (seq/_mock.py, in no package a user installs: mock_gate.is_mock tells anyone
else it is not for users).

WHY the SDK never builds an image or pulls weights here: the payload carries a DECLARATIVE image (base +
ordered steps) and a weights URI; the platform builds that into an image asynchronously (S3
goal 4). The SDK's whole job is to emit the spec, submit it, and report the build's terminal state honestly
— a failed build is a failure, a slow build times out with control returned, and every 4xx/5xx is surfaced,
never swallowed as success.

The API key is a Bearer credential only: it is never placed in the payload, in stdout, in a log line, or in
any error message this module raises. The deploy payload itself carries no secret VALUE — only
secret NAMES (SecretRef) — so there is nothing to redact from the request body (contrast `_gateway.py`,
whose secret WRITE path echoes values and must redact).
"""
from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from sequence_base.contract import (
    DeploymentAccepted,
    DeploymentRequest,
    DeploymentState,
    DeploymentStatusResponse,
)

from seq._account import auth_headers, credential
from seq.errors import raise_for, unreachable
from sequence_ai._core.mock_gate import is_mock
from sequence_ai._core.names import segment
from sequence_ai.errors import InternalError

if TYPE_CHECKING:
    from seq._mock import MockDeploymentsBackend



DEFAULT_BASE_URL = "https://api.generalsequences.com"



_TIMEOUT_S = 30.0



DEFAULT_WAIT_TIMEOUT_S = 1800.0
DEFAULT_POLL_INTERVAL_S = 5.0


_TERMINAL = (DeploymentState.READY, DeploymentState.FAILED)



NOTICE_HEADER = "X-Deploy-Notice"


class Accepted(DeploymentAccepted):
    """A deploy's 202 as this sequence-ai read it: the contract's fields, the platform's `notice` beside them, and
    whether its body could not be read at all (`unread`) - accepted all the same, the deployment named as it was sent."""

    notice: Optional[str] = None
    unread: bool = False


class DeploymentsClient:
    """The `seq deploy` backend selector: one facade over `submit` / `status` / `wait`. The base-url decides
    the tier (mock vs live); CLI and programmatic callers talk only to this facade."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        base = base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL
        self._backend: Union[_GatewayDeployBackend, MockDeploymentsBackend]
        if is_mock(base):
            from seq._mock import MockDeploymentsBackend

            self._backend = MockDeploymentsBackend(base, api_key)
        else:
            self._backend = _GatewayDeployBackend(api_key, base)

    def submit(self, request: DeploymentRequest, *, override: bool = False,
               scaling: tuple[str, ...] = ()) -> Accepted:




        return self._backend.submit(request, override=override, scaling=scaling)

    def validate(self, request: DeploymentRequest, *, override: bool = False,
                 scaling: tuple[str, ...] = ()) -> Optional[dict]:



        return self._backend.validate(request, override=override, scaling=scaling)

    def status(self, deployment_id: str) -> DeploymentStatusResponse:
        return self._backend.status(deployment_id)

    def wait(
        self,
        deployment_id: str,
        *,
        timeout_s: float = DEFAULT_WAIT_TIMEOUT_S,
        poll_interval_s: float = DEFAULT_POLL_INTERVAL_S,
        on_poll: Optional[Callable[[DeploymentStatusResponse], None]] = None,
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], float] = time.monotonic,
    ) -> DeploymentStatusResponse:
        """Poll `status` until the build is terminal (`ready` | `failed`) or `timeout_s` elapses, whichever
        comes first. Returns the last status seen — terminal, or `building` if the deadline hit (the caller
        distinguishes them by `.status`; the CLI and the handle raise `seq.errors.still_building` on a non-terminal
        return).

        `on_poll` (if given) is called with every status, so the CLI can show the transition live. `sleep` /
        `now` are injectable so tests advance a virtual clock instead of waiting real seconds (goal 24)."""
        deadline = now() + max(0.0, timeout_s)
        last = self.status(deployment_id)
        if on_poll is not None:
            on_poll(last)
        while last.status not in _TERMINAL:
            if now() >= deadline:
                return last
            sleep(max(0.0, poll_interval_s))
            last = self.status(deployment_id)
            if on_poll is not None:
                on_poll(last)
        return last



class _GatewayDeployBackend:
    """A thin, one-shot httpx client over the gateway's `/v1/deployments` surface. Carries the API key as a
    Bearer credential; never logs a request/response body."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self._key = _api_key(api_key, base_url)
        self._base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")

    def _client(self) -> Any:
        import httpx

        from seq._http import RetryReads

        return httpx.Client(
            base_url=self._base,
            timeout=_TIMEOUT_S,

            headers={**auth_headers(self._key), "Content-Type": "application/json"},
            transport=RetryReads(),
        )

    def submit(self, request: DeploymentRequest, *, override: bool = False,
               scaling: tuple[str, ...] = ()) -> Accepted:
        """POST /v1/deployments. 202 → Accepted (building), with the platform's notice when it gives one. Any other
        answer is a FAILURE, raised as the one mapping makes it and never treated as submitted (goal 12): a bad payload
        or an unknown or foreign secret is InvalidRequest (goal 10), a missing key AuthError, a taken name Conflict.
        An accepting answer whose body this sequence-ai cannot read is still an acceptance: the build has started, so it
        is followed by the name it was sent under, and `unread` says so for the caller to tell."""
        import httpx

        try:
            with self._client() as c:




                r = c.post("/v1/deployments", content=request.model_dump_json(exclude_none=True),
                           params=_params(override, scaling))
        except httpx.TransportError as exc:


            raise unreachable(self._base, exc) from None
        raise_for(r)
        notice = r.headers.get(NOTICE_HEADER) or None
        try:
            return Accepted(**DeploymentAccepted.model_validate(r.json()).model_dump(), notice=notice)
        except Exception:




            return Accepted(deployment_id=request.name, notice=notice, unread=True)

    def validate(self, request: DeploymentRequest, *, override: bool = False,
                 scaling: tuple[str, ...] = ()) -> Optional[dict]:
        """POST /v1/deployments/validate: what the deploy of this body would answer, without the deploy - the same
        refusals as submit()'s, raised by the same mapping (a 404 is a refusal: a volume not uploaded), and on
        acceptance its answer {"ok", "name", "state", "contract"}. None when it cannot be asked (no answer) or its
        answer cannot be read."""
        import httpx

        try:
            with self._client() as c:
                r = c.post("/v1/deployments/validate", content=request.model_dump_json(exclude_none=True),
                           params=_params(override, scaling))
        except httpx.TransportError:
            return None
        raise_for(r)
        try:
            return dict(r.json())
        except Exception:
            return None

    def status(self, deployment_id: str) -> DeploymentStatusResponse:
        """GET /v1/deployments/{id} → DeploymentStatusResponse (building | ready | failed, + error when
        failed). A 404 or any non-2xx is surfaced, never read as a silent success."""
        import httpx

        try:
            with self._client() as c:
                r = c.get(f"/v1/deployments/{segment(deployment_id)}")
        except httpx.TransportError as exc:
            raise unreachable(self._base, exc) from None
        raise_for(r)
        try:
            return DeploymentStatusResponse.model_validate(r.json())
        except Exception:
            raise InternalError(f"gateway returned a malformed status for deployment {deployment_id!r}") from None


def _params(override: bool, scaling: tuple[str, ...]) -> dict | None:
    """The deploy's query: --override, and the scaling fields it sets on a deployment that runs."""
    out = {**({"override": "true"} if override else {}), **({"scaling": ",".join(scaling)} if scaling else {})}
    return out or None


def _api_key(api_key: str | None, base_url: str | None = None) -> Any:
    """The caller's SDK API key: explicit arg, else SEQUENCES_API_KEY, else their `seq login` sign-in
    (seq/_account.py). Missing → fail closed BEFORE any request (goal 11 / 12), pointing at where to create one."""
    return credential(api_key, base_url)
