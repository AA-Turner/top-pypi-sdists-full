"""Activity-backed Session procedures with worker-local endpoint/auth composition."""

import asyncio
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import timedelta
from typing import Final, Literal

import httpx
from pydantic import BaseModel
from temporalio.exceptions import is_cancelled_exception

import mistralai.workflows as workflows
from mistralai.vibe.harness.runtime.agents.control_plane import (
    CountActiveRequest,
    CountActiveResult,
    SendSessionCommandRequest,
    SessionControlPlaneError,
    SessionLoss,
)
from mistralai.vibe.harness.runtime.agents.models import StartSessionRequest, StartSessionResult
from mistralai.vibe.harness.runtime.hosts.session_api import HttpSessionControlPlane
from mistralai.vibe.harness.runtime.http import build_ssl_context
from mistralai.vibe.harness.runtime.session.commands import SessionCommandResult
from mistralai.vibe_agents._http import _header_api_key
from mistralai.vibe_agents.sdk.app.config import ControlPlaneSettings
from mistralai.vibe_agents.sdk.authoring.errors import SdkError
from mistralai.vibe_agents.session_workflow import (
    VERIFY_CHILD_SESSION_PROCEDURE,
    VerifyChildSessionRequest,
    VerifyChildSessionResult,
)
from mistralai.workflows.core.auth import get_token_provider
from mistralai.workflows.core.config.config import config as workflow_config
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context

# Carries the calling Session's Workflow execution token. The worker's credential only names a
# workspace; the token lets the Agents API refuse a caller that only holds an API key.
EXECUTION_TOKEN_HEADER: Final = "X-Workflow-Execution-Token"  # noqa: S105 (a header name, not a secret)


@dataclass(frozen=True, slots=True)
class WorkflowSessionControlPlaneBinding:
    """Operator binding, never serialized into a Workflow or AgentConfig.

    The header callable runs inside each Activity, so expiring credentials are
    reconstructed after the serialization boundary and on native Activity retry.
    """

    # The procedure root, such as ``{server_url}/v2/agents/session-control-plane``.
    base_url: str
    headers: Callable[[], Mapping[str, str]]

    @classmethod
    def from_worker_credential(cls, base_url: str | None = None) -> "WorkflowSessionControlPlaneBinding":
        """Call the Agents API as this worker, with its own credential.

        The bearer is what the Workflows SDK authenticates the worker with: a managed
        deployment's service-account token, else ``MISTRAL_API_KEY``. It is read again on
        every Activity attempt, so a rotated token is picked up. The Agents API acts as the
        principal stored on the calling Session.

        ``base_url`` is the procedure root. It defaults to ``session-control-plane`` below
        ``AGENTS_SDK_DEPLOY_CONTROL_PLANE_URL`` when that is set, else below the Agents API
        behind the worker's Workflows server URL (``SERVER_URL``), which a managed deployment
        always receives for its environment.
        """

        return cls(
            base_url=(base_url or _worker_control_plane_url()).rstrip("/"),
            headers=_worker_credential_headers,
        )


def _worker_control_plane_url() -> str:
    settings = ControlPlaneSettings()
    if "deploy_control_plane_url" in settings.model_fields_set and settings.deploy_control_plane_url.strip():
        agents_api = settings.deploy_control_plane_url.strip()
    else:
        agents_api = f"{workflow_config.worker.server_url.rstrip('/')}/v2/agents"
    return f"{agents_api.rstrip('/')}/session-control-plane"


def _worker_credential_headers() -> Mapping[str, str]:
    provider = get_token_provider()
    token = provider.get_token().strip() if provider is not None else ""
    if not token:
        raise SessionControlPlaneError(
            "worker_credential_missing",
            "The worker has no credential for the Agents API: set MISTRAL_API_KEY or MISTRAL_SA_TOKEN_PATH",
        )
    try:
        token = _header_api_key(token, name="The worker credential")
    except SdkError as error:
        # The same credential fails every retry, so it gets its own code, not a transport failure.
        raise SessionControlPlaneError("worker_credential_invalid", str(error)) from None
    return {"Authorization": f"Bearer {token}"}


_bindings: dict[str, WorkflowSessionControlPlaneBinding] = {}


class ProcedureRejected(BaseModel):
    type: Literal["procedure_rejected"] = "procedure_rejected"
    code: str
    message: str
    retryable: bool
    settled: bool = False
    session_loss: SessionLoss | None = None

    @classmethod
    def from_error(cls, error: SessionControlPlaneError) -> "ProcedureRejected":
        return cls(
            code=error.code,
            message=str(error),
            retryable=error.retryable,
            settled=error.settled,
            session_loss=error.session_loss,
        )

    def to_error(self) -> SessionControlPlaneError:
        return SessionControlPlaneError(
            self.code, self.message, retryable=self.retryable, settled=self.settled, session_loss=self.session_loss
        )


def register_control_plane_binding(name: str, binding: WorkflowSessionControlPlaneBinding) -> None:
    _bindings[name] = binding


def _build_client(binding_id: str, execution_token: str | None = None) -> HttpSessionControlPlane:
    binding = _bindings[binding_id]
    headers = {**binding.headers()}
    if execution_token:
        headers[EXECUTION_TOKEN_HEADER] = execution_token
    return HttpSessionControlPlane(base_url=binding.base_url, headers=headers)


def workflow_execution_token() -> str | None:
    """The execution token of the running Workflow, read in its main task.

    Only the Workflow's main task holds the token: a signal or update handler task starts
    without it, so Activities it schedules would carry none. Workflow code reads the token
    once here and passes it to each Session procedure Activity as an argument.
    """
    context = retrieve_context()
    return context.execution_token if context is not None and context.execution_token else None


@workflows.activity(
    name="harness_session_start", retry_policy_max_attempts=3, start_to_close_timeout=timedelta(seconds=65)
)
async def start_session_activity(
    binding_id: str, request: StartSessionRequest, execution_token: str | None = None
) -> StartSessionResult | ProcedureRejected:
    try:
        return await _build_client(binding_id, execution_token).start_session(request)
    except SessionControlPlaneError as error:
        return ProcedureRejected.from_error(error)


@workflows.activity(
    name="harness_session_send_command", retry_policy_max_attempts=3, start_to_close_timeout=timedelta(seconds=65)
)
async def send_command_activity(
    binding_id: str, request: SendSessionCommandRequest, execution_token: str | None = None
) -> SessionCommandResult | ProcedureRejected:
    try:
        return await _build_client(binding_id, execution_token).send_command(request)
    except SessionControlPlaneError as error:
        return ProcedureRejected.from_error(error)


# A timeout or a rate limit is no answer: the Activity retries it.
_RETRIED_STATUS_CODES: Final = frozenset({408, 429})

ChildVerificationOutcome = Literal["ok", "no_row", "mismatch", "unsupported", "refused"]


class ChildVerification(BaseModel):
    """The Agents API's answer to a child that asks whether it started it.

    ``unsupported``: the Agents API has no such procedure (it answers 404), so it cannot say yes.
    ``refused``: it refused the call itself, such as an execution token it does not accept.
    """

    outcome: ChildVerificationOutcome
    status_code: int = 200


# Retried with backoff, nine attempts of up to 65 s each: a short outage must not fail a child, and
# no failure to ask is ever read as a yes. A server that accepts connections and never answers can
# hold a child for about thirteen minutes before it is refused.
@workflows.activity(
    name="harness_session_verify_child", retry_policy_max_attempts=9, start_to_close_timeout=timedelta(seconds=65)
)
async def verify_child_session_activity(
    binding_id: str, request: VerifyChildSessionRequest, execution_token: str | None = None
) -> ChildVerification:
    return await ask_agents_api_about_child(binding_id, request, execution_token)


async def ask_agents_api_about_child(
    binding_id: str, request: VerifyChildSessionRequest, execution_token: str | None = None
) -> ChildVerification:
    """One call to the Agents API; a server or transport error raises, so the Activity retries."""

    binding = _bindings[binding_id]
    headers = {**binding.headers()}
    if execution_token:
        headers[EXECUTION_TOKEN_HEADER] = execution_token
    async with httpx.AsyncClient(
        base_url=binding.base_url.rstrip("/"), headers=headers, timeout=60, verify=build_ssl_context()
    ) as client:
        response = await client.post(f"/{VERIFY_CHILD_SESSION_PROCEDURE}", json=request.model_dump(mode="json"))
    if response.status_code == 404:
        return ChildVerification(outcome="unsupported", status_code=404)
    if response.status_code in _RETRIED_STATUS_CODES:
        response.raise_for_status()
    if 400 <= response.status_code < 500:
        return ChildVerification(outcome="refused", status_code=response.status_code)
    response.raise_for_status()
    return ChildVerification(outcome=VerifyChildSessionResult.model_validate(response.json()).verdict)


class ActivitySessionControlPlane:
    def __init__(self, binding_id: str, *, execution_token: str | None = None) -> None:
        self._binding_id = binding_id
        self._execution_token = execution_token

    async def start_session(self, request: StartSessionRequest) -> StartSessionResult:
        try:
            result = await start_session_activity(self._binding_id, request, self._execution_token)
            if isinstance(result, ProcedureRejected):
                raise result.to_error()
            return result
        except Exception as error:
            raise _delivery_error(error) from error

    async def send_command(self, request: SendSessionCommandRequest) -> SessionCommandResult:
        try:
            result = await send_command_activity(self._binding_id, request, self._execution_token)
            if isinstance(result, ProcedureRejected):
                raise result.to_error()
            return result
        except Exception as error:
            raise _delivery_error(error) from error

    async def verify_child_session(self, request: VerifyChildSessionRequest) -> ChildVerification:
        return await verify_child_session_activity(self._binding_id, request, self._execution_token)

    async def count_active(self, request: CountActiveRequest) -> CountActiveResult:
        # No pre-check across the Session API: its start_session and send_command
        # enforce the tree's child Turn limit and refuse with a retryable 429. Report
        # no active child so the Runtime always asks, and that refusal decides.
        return CountActiveResult(count=0)


def _delivery_error(error: Exception) -> SessionControlPlaneError | asyncio.CancelledError:
    # Temporal wraps Activity cancellation; Runtime cleanup must retain pending
    # work instead of recording this execution handoff as permanent failure.
    if is_cancelled_exception(error):
        return asyncio.CancelledError("Session procedure Activity cancelled")
    if isinstance(error, SessionControlPlaneError):
        return error
    return SessionControlPlaneError(
        "subagent_delivery_failed", "Session procedure failed; recipient admission may be unknown", retryable=True
    )
