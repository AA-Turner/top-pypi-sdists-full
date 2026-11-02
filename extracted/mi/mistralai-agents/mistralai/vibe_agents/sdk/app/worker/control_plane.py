"""Activity-backed Session procedures with worker-local endpoint/auth composition."""

import asyncio
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import timedelta
from typing import Literal

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
from mistralai.vibe.harness.runtime.session.commands import SessionCommandResult
from mistralai.vibe_agents.sdk.app.config import ControlPlaneSettings
from mistralai.vibe_agents.session_workflow import Principal
from mistralai.workflows.core.auth import get_token_provider
from mistralai.workflows.core.config.config import config as workflow_config


@dataclass(frozen=True, slots=True)
class WorkflowSessionControlPlaneBinding:
    """Operator binding, never serialized into a Workflow or AgentConfig.

    The header callable runs inside each Activity, so expiring credentials are
    reconstructed after the serialization boundary and on native Activity retry.
    """

    # The procedure root, such as ``{server_url}/v2/agents/session-control-plane``.
    base_url: str
    headers_for_principal: Callable[[Principal], Mapping[str, str]]

    @classmethod
    def from_worker_credential(cls, base_url: str | None = None) -> "WorkflowSessionControlPlaneBinding":
        """Call the Agents API as this worker, with its own credential.

        The bearer is what the Workflows SDK authenticates the worker with: a managed
        deployment's service-account token, else ``MISTRAL_API_KEY``. It is read again on
        every Activity attempt, so a rotated token is picked up. The Agents API acts as the
        principal stored on the calling Session, so the principal is not sent.

        ``base_url`` is the procedure root. It defaults to ``session-control-plane`` below
        ``AGENTS_SDK_DEPLOY_CONTROL_PLANE_URL`` when that is set, else below the Agents API
        behind the worker's Workflows server URL (``SERVER_URL``), which a managed deployment
        always receives for its environment.
        """

        return cls(
            base_url=(base_url or _worker_control_plane_url()).rstrip("/"),
            headers_for_principal=_worker_credential_headers,
        )


def _worker_control_plane_url() -> str:
    settings = ControlPlaneSettings()
    if "deploy_control_plane_url" in settings.model_fields_set and settings.deploy_control_plane_url.strip():
        agents_api = settings.deploy_control_plane_url.strip()
    else:
        agents_api = f"{workflow_config.worker.server_url.rstrip('/')}/v2/agents"
    return f"{agents_api.rstrip('/')}/session-control-plane"


def _worker_credential_headers(_principal: Principal) -> Mapping[str, str]:
    provider = get_token_provider()
    token = provider.get_token().strip() if provider is not None else ""
    if not token:
        raise SessionControlPlaneError(
            "worker_credential_missing",
            "The worker has no credential for the Agents API: set MISTRAL_API_KEY or MISTRAL_SA_TOKEN_PATH",
        )
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


def _build_client(binding_id: str, principal: Principal) -> HttpSessionControlPlane:
    binding = _bindings[binding_id]
    return HttpSessionControlPlane(base_url=binding.base_url, headers=binding.headers_for_principal(principal))


@workflows.activity(
    name="harness_session_start", retry_policy_max_attempts=3, start_to_close_timeout=timedelta(seconds=65)
)
async def start_session_activity(
    binding_id: str, principal: Principal, request: StartSessionRequest
) -> StartSessionResult | ProcedureRejected:
    try:
        return await _build_client(binding_id, principal).start_session(request)
    except SessionControlPlaneError as error:
        return ProcedureRejected.from_error(error)


@workflows.activity(
    name="harness_session_send_command", retry_policy_max_attempts=3, start_to_close_timeout=timedelta(seconds=65)
)
async def send_command_activity(
    binding_id: str, principal: Principal, request: SendSessionCommandRequest
) -> SessionCommandResult | ProcedureRejected:
    try:
        return await _build_client(binding_id, principal).send_command(request)
    except SessionControlPlaneError as error:
        return ProcedureRejected.from_error(error)


class ActivitySessionControlPlane:
    def __init__(self, binding_id: str, principal: Principal) -> None:
        self._binding_id = binding_id
        self._principal = principal

    async def start_session(self, request: StartSessionRequest) -> StartSessionResult:
        try:
            result = await start_session_activity(self._binding_id, self._principal, request)
            if isinstance(result, ProcedureRejected):
                raise result.to_error()
            return result
        except Exception as error:
            raise _delivery_error(error) from error

    async def send_command(self, request: SendSessionCommandRequest) -> SessionCommandResult:
        try:
            result = await send_command_activity(self._binding_id, self._principal, request)
            if isinstance(result, ProcedureRejected):
                raise result.to_error()
            return result
        except Exception as error:
            raise _delivery_error(error) from error

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
