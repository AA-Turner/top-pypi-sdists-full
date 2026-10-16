from __future__ import annotations

import asyncio
import contextlib
import os
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Mapping
from urllib.parse import urljoin

import requests

from chalk.workflows._definitions import WorkflowDefinition
from chalk.workflows._orchestrator_auth import TOKEN_FILE_ENV_VAR, connect_with_token, orchestrator_token

if TYPE_CHECKING:
    from temporalio.client import Client

_CONNECTION_DETAILS_RPC = "/chalk.server.v1.WorkflowOrchestratorService/GetWorkflowOrchestratorConnectionDetails"
_SEND_MESSAGE_RPC = "/chalk.server.v1.WorkflowOrchestratorService/SendWorkflowMessage"

_ADDRESS_ENV_VAR = "CHALK_WORKFLOW_ORCHESTRATOR_ADDRESS"
_NAMESPACE_ENV_VAR = "CHALK_WORKFLOW_ORCHESTRATOR_NAMESPACE"
_TASK_QUEUE_ENV_VAR = "CHALK_WORKFLOW_ORCHESTRATOR_TASK_QUEUE"
_INSECURE_ENV_VAR = "CHALK_WORKFLOW_ORCHESTRATOR_INSECURE"


ChalkAuthorization = Callable[[bool], "str | None"]
"""The caller's current `Authorization` header for the Chalk API server, or None.

Called with True after the server rejected the previous value, so a provider whose credentials
can be renewed (a credential exchange, a rotated token file) renews them first. Long-lived
connections call it again whenever they need a new orchestrator access token, so it must not
hand back a value captured once."""


def static_authorization(bearer_token: str | None) -> ChalkAuthorization:
    """A provider for an `Authorization` value the caller manages, which is never renewed."""
    return lambda renew: bearer_token


@dataclass
class WorkflowOrchestratorConnectionInfo:
    address: str
    temporal_namespace: str
    default_task_queue: str
    use_tls: bool
    # Projected service-account token file of an in-cluster worker on a shared orchestrator.
    token_file: str | None
    # Short-lived JWT the API server mints for a shared orchestrator; replaces the caller's
    # Chalk token on the Temporal connection.
    access_token: str | None


@dataclass
class WorkflowRunHandle:
    """Reference to a started workflow run on the environment's workflow orchestrator."""

    workflow_name: str
    workflow_id: str
    run_id: str


def _post_connection_details(api_server: str, bearer_token: str, environment_id: str | None) -> requests.Response:
    headers = {
        "Authorization": bearer_token if bearer_token.lower().startswith("bearer ") else f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }
    if environment_id is not None:
        headers["X-Chalk-Env-Id"] = environment_id
    return requests.post(
        urljoin(api_server, _CONNECTION_DETAILS_RPC),
        headers=headers,
        json={},
        timeout=30,
    )


def resolve_connection_info(
    *,
    api_server: str | None,
    authorization: ChalkAuthorization,
    environment_id: str | None,
) -> WorkflowOrchestratorConnectionInfo:
    """Determine how to reach the environment's workflow orchestrator.

    In-cluster workers are configured with CHALK_WORKFLOW_ORCHESTRATOR_* environment
    variables; local clients ask the Chalk API server for connection details.
    """
    address = os.getenv(_ADDRESS_ENV_VAR)
    if address:
        return WorkflowOrchestratorConnectionInfo(
            address=address,
            temporal_namespace=os.getenv(_NAMESPACE_ENV_VAR) or "default",
            default_task_queue=os.getenv(_TASK_QUEUE_ENV_VAR) or "chalk-workflows",
            use_tls=os.getenv(_INSECURE_ENV_VAR) not in ("1", "true"),
            token_file=os.getenv(TOKEN_FILE_ENV_VAR) or None,
            access_token=None,
        )

    bearer_token = authorization(False) if api_server is not None else None
    if api_server is None or bearer_token is None:
        raise RuntimeError(
            "Cannot resolve the workflow orchestrator: no authenticated Chalk API server is configured "
            + f"and {_ADDRESS_ENV_VAR} is not set."
        )
    response = _post_connection_details(api_server, bearer_token, environment_id)
    if response.status_code in (401, 403):
        # The caller's credentials may have expired since they were read; renew them once.
        renewed = authorization(True)
        if renewed is not None:
            response = _post_connection_details(api_server, renewed, environment_id)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to resolve workflow orchestrator connection details ({response.status_code}): {response.text}. "
            + "Ensure a workflow orchestrator is provisioned for this environment."
        )
    body = response.json()
    endpoint = body.get("endpoint")
    if not endpoint:
        raise RuntimeError(
            "The Chalk API server did not return a workflow orchestrator endpoint. "
            + "Ensure a workflow orchestrator is provisioned for this environment."
        )
    return WorkflowOrchestratorConnectionInfo(
        address=endpoint,
        temporal_namespace=body.get("temporalNamespace") or "default",
        default_task_queue=body.get("defaultTaskQueue") or "chalk-workflows",
        use_tls=True,
        token_file=None,
        access_token=body.get("accessToken") or None,
    )


def _workflow_name(workflow: WorkflowDefinition[Any, Any] | str) -> str:
    return workflow if isinstance(workflow, str) else workflow.name


@contextlib.asynccontextmanager
async def connect_orchestrator(
    info: WorkflowOrchestratorConnectionInfo,
    *,
    api_server: str | None,
    authorization: ChalkAuthorization,
    environment_id: str | None,
) -> AsyncIterator[Client]:
    """Connect to the orchestrator `info` describes, keeping its token fresh while open.

    A shared orchestrator's access token is replaced by asking the API server for the
    connection details again, with the caller's current Chalk authorization.
    """

    def fetch_access_token() -> str | None:
        return resolve_connection_info(
            api_server=api_server, authorization=authorization, environment_id=environment_id
        ).access_token

    token = orchestrator_token(
        token_file=info.token_file,
        access_token=info.access_token,
        fetch_access_token=fetch_access_token,
    )
    async with connect_with_token(
        info.address,
        info.temporal_namespace,
        use_tls=info.use_tls,
        # Only an orchestrator without its own token (a per-environment one) takes the caller's
        # Chalk token, read once here.
        bearer_token=authorization(False) if token is None else None,
        environment_id=environment_id,
        token=token,
    ) as client:
        yield client


async def _trigger(
    workflow: WorkflowDefinition[Any, Any] | str,
    input: Mapping[str, Any] | None,
    *,
    info: WorkflowOrchestratorConnectionInfo,
    api_server: str | None,
    authorization: ChalkAuthorization,
    environment_id: str | None,
    workflow_id: str | None,
    task_queue: str | None,
    wait: bool,
) -> WorkflowRunHandle | Any:
    from chalk.workflows._temporal import start_workflow, wait_for_result

    name = _workflow_name(workflow)
    async with connect_orchestrator(
        info, api_server=api_server, authorization=authorization, environment_id=environment_id
    ) as client:
        handle = await start_workflow(
            client,
            workflow_name=name,
            input=input,
            workflow_id=workflow_id if workflow_id is not None else f"{name}-{uuid.uuid4()}",
            task_queue=task_queue if task_queue is not None else info.default_task_queue,
        )
        if wait:
            return await wait_for_result(handle)
    return WorkflowRunHandle(
        workflow_name=name,
        workflow_id=handle.id,
        run_id=handle.first_execution_run_id or "",
    )


async def _run_with_local_worker(
    workflow: WorkflowDefinition[Any, Any],
    input: Mapping[str, Any] | None,
    *,
    info: WorkflowOrchestratorConnectionInfo,
    api_server: str | None,
    authorization: ChalkAuthorization,
    environment_id: str | None,
    workflow_id: str | None,
) -> Any:
    from chalk.workflows._temporal import create_worker, start_workflow, wait_for_result

    async with connect_orchestrator(
        info, api_server=api_server, authorization=authorization, environment_id=environment_id
    ) as client:
        # A unique task queue guarantees this run is served by this process's worker
        # (which has the local definitions), not by deployed workers.
        task_queue = f"chalk-workflows-local-{uuid.uuid4()}"
        async with create_worker(client, task_queue=task_queue):
            handle = await start_workflow(
                client,
                workflow_name=workflow.name,
                input=input,
                workflow_id=workflow_id if workflow_id is not None else f"{workflow.name}-{uuid.uuid4()}",
                task_queue=task_queue,
            )
            return await wait_for_result(handle)


def trigger_workflow(
    workflow: WorkflowDefinition[Any, Any] | str,
    input: Mapping[str, Any] | None,
    *,
    api_server: str | None,
    authorization: ChalkAuthorization,
    environment_id: str | None,
    workflow_id: str | None,
    task_queue: str | None,
    wait: bool,
) -> WorkflowRunHandle | Any:
    info = resolve_connection_info(api_server=api_server, authorization=authorization, environment_id=environment_id)
    return asyncio.run(
        _trigger(
            workflow,
            input,
            info=info,
            api_server=api_server,
            authorization=authorization,
            environment_id=environment_id,
            workflow_id=workflow_id,
            task_queue=task_queue,
            wait=wait,
        )
    )


def run_workflow(
    workflow: WorkflowDefinition[Any, Any],
    input: Mapping[str, Any] | None,
    *,
    api_server: str | None,
    authorization: ChalkAuthorization,
    environment_id: str | None,
    workflow_id: str | None,
) -> Any:
    info = resolve_connection_info(api_server=api_server, authorization=authorization, environment_id=environment_id)
    return asyncio.run(
        _run_with_local_worker(
            workflow,
            input,
            info=info,
            api_server=api_server,
            authorization=authorization,
            environment_id=environment_id,
            workflow_id=workflow_id,
        )
    )


def send_message(
    workflow_id: str,
    name: str,
    payload: Any,
    *,
    run_id: str | None,
    api_server: str | None,
    bearer_token: str | None,
    environment_id: str | None,
) -> None:
    """Deliver a message to a running workflow through the Chalk API server.

    Messages go through the API server rather than straight to the orchestrator so that it
    checks the caller's permissions, records the sender in the message, and audits the call.
    """
    if api_server is None or bearer_token is None:
        raise RuntimeError("Sending a workflow message requires an authenticated Chalk API server.")
    headers = {
        "Authorization": bearer_token if bearer_token.lower().startswith("bearer ") else f"Bearer {bearer_token}",
        "Content-Type": "application/json",
        # Routes the request to the Go API server, which serves WorkflowOrchestratorService.
        "X-Chalk-Server": "go-api",
    }
    if environment_id is not None:
        headers["X-Chalk-Env-Id"] = environment_id
    body: dict[str, Any] = {"workflowId": workflow_id, "name": name, "payload": payload}
    if run_id:
        body["runId"] = run_id
    response = requests.post(urljoin(api_server, _SEND_MESSAGE_RPC), headers=headers, json=body, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to send message {name!r} to workflow {workflow_id!r} ({response.status_code}): {response.text}"
        )
