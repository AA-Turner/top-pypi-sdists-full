from __future__ import annotations

import asyncio
import os
import uuid
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urljoin

import requests

from chalk.workflows._definitions import WorkflowDefinition

_CONNECTION_DETAILS_RPC = "/chalk.server.v1.WorkflowOrchestratorService/GetWorkflowOrchestratorConnectionDetails"

_ADDRESS_ENV_VAR = "CHALK_WORKFLOW_ORCHESTRATOR_ADDRESS"
_NAMESPACE_ENV_VAR = "CHALK_WORKFLOW_ORCHESTRATOR_NAMESPACE"
_TASK_QUEUE_ENV_VAR = "CHALK_WORKFLOW_ORCHESTRATOR_TASK_QUEUE"
_INSECURE_ENV_VAR = "CHALK_WORKFLOW_ORCHESTRATOR_INSECURE"


@dataclass
class WorkflowOrchestratorConnectionInfo:
    address: str
    temporal_namespace: str
    default_task_queue: str
    use_tls: bool


@dataclass
class WorkflowRunHandle:
    """Reference to a started workflow run on the environment's workflow orchestrator."""

    workflow_name: str
    workflow_id: str
    run_id: str


def resolve_connection_info(
    *,
    api_server: str | None,
    bearer_token: str | None,
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
        )

    if api_server is None or bearer_token is None:
        raise RuntimeError(
            "Cannot resolve the workflow orchestrator: no authenticated Chalk API server is configured "
            + f"and {_ADDRESS_ENV_VAR} is not set."
        )
    headers = {
        "Authorization": bearer_token if bearer_token.lower().startswith("bearer ") else f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }
    if environment_id is not None:
        headers["X-Chalk-Env-Id"] = environment_id
    response = requests.post(
        urljoin(api_server, _CONNECTION_DETAILS_RPC),
        headers=headers,
        json={},
        timeout=30,
    )
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
    )


def _workflow_name(workflow: WorkflowDefinition[Any, Any] | str) -> str:
    return workflow if isinstance(workflow, str) else workflow.name


async def _connect(
    info: WorkflowOrchestratorConnectionInfo,
    *,
    bearer_token: str | None,
    environment_id: str | None,
):
    from chalk.workflows._temporal import connect_workflow_orchestrator

    return await connect_workflow_orchestrator(
        info.address,
        info.temporal_namespace,
        use_tls=info.use_tls,
        bearer_token=bearer_token,
        environment_id=environment_id,
    )


async def _trigger(
    workflow: WorkflowDefinition[Any, Any] | str,
    input: Mapping[str, Any] | None,
    *,
    info: WorkflowOrchestratorConnectionInfo,
    bearer_token: str | None,
    environment_id: str | None,
    workflow_id: str | None,
    task_queue: str | None,
    wait: bool,
) -> WorkflowRunHandle | Any:
    from chalk.workflows._temporal import start_workflow

    name = _workflow_name(workflow)
    client = await _connect(info, bearer_token=bearer_token, environment_id=environment_id)
    handle = await start_workflow(
        client,
        workflow_name=name,
        input=input,
        workflow_id=workflow_id if workflow_id is not None else f"{name}-{uuid.uuid4()}",
        task_queue=task_queue if task_queue is not None else info.default_task_queue,
    )
    if wait:
        return await handle.result()
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
    bearer_token: str | None,
    environment_id: str | None,
    workflow_id: str | None,
) -> Any:
    from chalk.workflows._temporal import create_worker, start_workflow

    client = await _connect(info, bearer_token=bearer_token, environment_id=environment_id)
    # A unique task queue guarantees this run is served by this process's worker
    # (which has the local definitions), not by deployed workers.
    task_queue = f"chalk-workflows-local-{uuid.uuid4()}"
    worker = create_worker(client, task_queue=task_queue)
    async with worker:
        handle = await start_workflow(
            client,
            workflow_name=workflow.name,
            input=input,
            workflow_id=workflow_id if workflow_id is not None else f"{workflow.name}-{uuid.uuid4()}",
            task_queue=task_queue,
        )
        return await handle.result()


def trigger_workflow(
    workflow: WorkflowDefinition[Any, Any] | str,
    input: Mapping[str, Any] | None,
    *,
    api_server: str | None,
    bearer_token: str | None,
    environment_id: str | None,
    workflow_id: str | None,
    task_queue: str | None,
    wait: bool,
) -> WorkflowRunHandle | Any:
    info = resolve_connection_info(api_server=api_server, bearer_token=bearer_token, environment_id=environment_id)
    return asyncio.run(
        _trigger(
            workflow,
            input,
            info=info,
            bearer_token=bearer_token,
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
    bearer_token: str | None,
    environment_id: str | None,
    workflow_id: str | None,
) -> Any:
    info = resolve_connection_info(api_server=api_server, bearer_token=bearer_token, environment_id=environment_id)
    return asyncio.run(
        _run_with_local_worker(
            workflow,
            input,
            info=info,
            bearer_token=bearer_token,
            environment_id=environment_id,
            workflow_id=workflow_id,
        )
    )
