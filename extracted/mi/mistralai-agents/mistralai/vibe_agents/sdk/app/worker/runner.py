from __future__ import annotations

import os
from typing import TYPE_CHECKING

import mistralai.workflows as workflows
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk import quiet
from mistralai.vibe_agents.sdk.app import deployment, preflight
from mistralai.vibe_agents.sdk.app.worker.control_plane import WorkflowSessionControlPlaneBinding
from mistralai.vibe_agents.sdk.app.worker.studio_tracing import (
    StudioRunMode,
    configure_managed_studio_tracing,
    shutdown_studio_genai_tracing,
)
from mistralai.vibe_agents.sdk.app.worker.usage_telemetry import worker_usage_telemetry
from mistralai.vibe_agents.sdk.assembly import workflow as assembly_workflow
from mistralai.workflows.core.config.config import config as workflow_config

if TYPE_CHECKING:
    from mistralai.vibe.harness.runtime.agents.policy import SubagentPolicy
    from mistralai.vibe_agents.sdk.app.worker.sandbox_lifecycle import SandboxLifecycleFactory
    from mistralai.vibe_agents.sdk.authoring.agent import Agent
    from mistralai.vibe_agents.sdk.authoring.contracts import Harness


def build_workflow(
    agent: Agent,
    *,
    name: str,
    harness: Harness | None = None,
    subagent_policy: SubagentPolicy | None = None,
    sandbox_lifecycle_factory: SandboxLifecycleFactory | None = None,
) -> type:
    resolved_harness = agent._resolve_harness(harness)
    quiet.show_worker_warnings()
    # The CLI already ran this in preflight; repeat it for workers started with Agent.run_worker().
    preflight.require_worker_sandbox_config(resolved_harness)
    deployment.use_mistral_api_url()
    deployment.enable_default_payload_compression()
    # Every deployed worker calls the Agents API with its own credential, so when the agent serves
    # subagents each Session runs them under the policy its start input carries. A Session without one runs none.
    session_control_plane = WorkflowSessionControlPlaneBinding.from_worker_credential()
    # The builder defaults to the control-plane session workflow, the only class vibe_agents can
    # dispatch to: it sends SessionWorkflowStartInput and a submit_command signal.
    return assembly_workflow.build_workflow(
        agent,
        name=name,
        harness=harness,
        subagent_policy=subagent_policy,
        session_control_plane=session_control_plane,
        sandbox_lifecycle_factory=sandbox_lifecycle_factory,
    )


def use_deployment_name(deployment_name: str) -> None:
    # Apply the deployment name to the ALREADY-LOADED config, not just the env: the workflows SDK builds
    # its global `config` at import time, so a late os.environ write would not reach
    # config.worker.deployment_name. Set the env too for any child process that re-reads it.
    os.environ["DEPLOYMENT_NAME"] = deployment_name
    workflow_config.worker.deployment_name = deployment_name


async def run_worker(
    agent: Agent,
    *,
    workflow_name: str | None = None,
    deployment_name: str | None = None,
    managed_studio_tracing: bool = True,
    sandbox_lifecycle_factory: SandboxLifecycleFactory | None = None,
) -> None:
    use_deployment_name(
        deployment.validated_deployment_name(deployment_name, source="deployment_name")
        if deployment_name
        else await deployment.resolve_worker_deployment_name(agent.name)
    )
    # Build the workflow before configuring tracing: build_workflow runs use_mistral_api_url(), which
    # copies MISTRAL_API_URL onto the loaded config that the tracing exporter reads for its endpoint.
    workflow = build_workflow(
        agent, name=workflow_name or agent.name, sandbox_lifecycle_factory=sandbox_lifecycle_factory
    )
    tracing_configured_here = managed_studio_tracing and configure_managed_studio_tracing(
        run_mode=StudioRunMode.RUN_WORKER, redaction=agent._redaction()
    )
    try:
        async with worker_usage_telemetry():
            await workflows.run_worker([workflow])
    finally:
        if tracing_configured_here:
            shutdown_studio_genai_tracing()


async def run_shared_worker() -> None:
    """Run the Agents shared worker, which serves the data-only Agents of every workspace."""
    from mistralai.vibe_agents.sdk.app import config  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.app.worker import session_binding  # noqa: PLC0415
    from mistralai.vibe_agents.sdk.sandbox.koyeb import register_koyeb_sandbox_activities  # noqa: PLC0415

    if issues := shared_worker_runtime_issues(
        require_worker_versioning=config.get_app_settings().require_worker_versioning
    ):
        raise SharedWorkerConfigError(issues)
    quiet.show_worker_warnings()
    use_deployment_name(deployment.explicit_deployment_name() or wire.SHARED_WORKER_DEPLOYMENT_NAME)
    if (namespace := _identity_namespace()) is not None:
        workflow_config.temporal.namespace = namespace
    deployment.enable_default_payload_compression()
    # Which Agent asks for a managed Sandbox is only known per Session.
    register_koyeb_sandbox_activities()
    async with worker_usage_telemetry():
        await workflows.run_worker(
            [
                session_binding.build_shared_worker_workflow_class(on_behalf_of=False),
                session_binding.build_shared_worker_workflow_class(on_behalf_of=True),
            ]
        )


class SharedWorkerConfigError(Exception):
    """The process is not configured as a worker of the platform's reserved shared namespace."""

    def __init__(self, issues: list[str]) -> None:
        super().__init__("; ".join(issues))
        self.issues = issues


def shared_worker_runtime_issues(*, require_worker_versioning: bool) -> list[str]:
    """What prevents this process from running as the shared worker; one line per problem."""
    issues: list[str] = []
    headers = workflow_config.worker.mistral_api_headers or {}
    if not all(headers.get(name) for name in _IDENTITY_HEADERS):
        # The reserved namespace has no API key: the platform cluster trusts these headers instead.
        issues.append(
            "MISTRAL_API_HEADERS must name the reserved namespace with x-consumer-custom-id and x-workspace-id."
        )
    if workflow_config.worker.enable_config_discovery:
        issues.append("ENABLE_CONFIG_DISCOVERY must be false: the reserved namespace is set from the headers.")
    if require_worker_versioning and not workflow_config.worker.versioning.enabled:
        issues.append(
            "Temporal worker versioning is off. A rollout would replay every running Session on new code; "
            "run the worker under the Temporal Worker Controller."
        )
    return issues


_IDENTITY_HEADERS = ("x-consumer-custom-id", "x-workspace-id")


def _identity_namespace() -> str | None:
    # The Temporal namespace of a reserved namespace is its identity, as the control plane's own
    # shared worker derives it. A namespace set explicitly, for example by the Temporal Worker
    # Controller, wins.
    if workflow_config.temporal.namespace != _DEFAULT_TEMPORAL_NAMESPACE:
        return None
    headers = workflow_config.worker.mistral_api_headers or {}
    return f"{headers[_IDENTITY_HEADERS[0]]}:{headers[_IDENTITY_HEADERS[1]]}"


_DEFAULT_TEMPORAL_NAMESPACE = type(workflow_config.temporal).model_fields["namespace"].default
