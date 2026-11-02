"""Serve a Workflow Session's skills as files that its sandbox writes.

The worker keeps the declared skills in process memory when it compiles the Harness. A Session's
sandbox write then carries only references, and the sandbox driver resolves them inside its own
activity, so skill bytes stay out of Workflow history and Continue-As-New state.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mistralai.client import Mistral
from mistralai.vibe.harness.app_server.session import MaterializedSkillDefinition
from mistralai.vibe.harness.runtime.capabilities.skills import SkillHost
from mistralai.vibe.harness.runtime.hosts.workflows import WorkflowSandboxResource
from mistralai.vibe.harness.runtime.hosts.workflows.harness_definition import WorkflowHarnessDefinition
from mistralai.vibe.harness.runtime.session.state import RuntimeSessionState
from mistralai.vibe_agents.sdk.app.worker import runtime_metrics
from mistralai.vibe_agents.sdk.assembly import assemble, sandbox_skills
from mistralai.vibe_agents.sdk.assembly.connectors import RunAs, get_workflow_mistral_client
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.exceptions import WorkflowError


@asynccontextmanager
async def _workflow_client(run_as: RunAs) -> AsyncIterator[Mistral]:
    client = get_workflow_mistral_client(run_as)
    try:
        yield client
    finally:
        # Each read gets new HTTP clients, and Mistral does not close a client it was given.
        if client.sdk_configuration.async_client is not None:
            await client.sdk_configuration.async_client.aclose()


@asynccontextmanager
async def _workflow_registry_client() -> AsyncIterator[Mistral]:
    # The worker reads skills as itself, so an agent serves the same skills to every caller.
    async with _workflow_client(RunAs.DEPLOYMENT) as client:
        yield client


@asynccontextmanager
async def _workflow_discovery_client() -> AsyncIterator[Mistral]:
    context = retrieve_context()
    if context is None or not context.on_behalf_of:
        raise WorkflowError("Registry skill discovery requires an on-behalf-of Workflow context", non_retryable=True)
    async with _workflow_client(RunAs.AUTO) as client:
        yield client


_SKILL_METRICS = runtime_metrics.WorkerSkillMetrics()

# One resolver for the process: its name keeps it, so every compiled Harness registers this object.
_SKILL_FILE_RESOLVER = sandbox_skills.SkillFileResolver(
    sandbox_skills.WORKFLOW_SKILL_FILE_RESOLVER,
    _workflow_registry_client,
    discovery_client=_workflow_discovery_client,
    metrics=_SKILL_METRICS,
)


def prepare(delivery: assemble.SandboxFileSkills | None) -> sandbox_skills.SandboxSkillFiles | None:
    """Get this worker ready to write a compiled Harness's skills into each Session's sandbox.

    It keeps the local skill bytes in this process and registers the worker's resolver, so it runs
    once, when the worker compiles the Harness.
    """

    if delivery is None:
        return None
    return sandbox_skills.SandboxSkillFiles.prepare(
        delivery.skills,
        resolver=_SKILL_FILE_RESOLVER,
        subagent_skills=delivery.subagents,
        workspace=delivery.workspace,
        discovery=delivery.discovery is not None,
    )


async def serve_skills(
    definition: WorkflowHarnessDefinition,
    sandbox: WorkflowSandboxResource,
    files: sandbox_skills.SandboxSkillFiles | None,
    restored: RuntimeSessionState | None,
    *,
    child: bool = False,
    session_id: str = "",
) -> tuple[WorkflowHarnessDefinition, SkillHost | None]:
    """Hand the Harness the catalog of the skills its sandbox holds, and the host that reads them.

    Each Session writes only the skills it declares, once, when it first opens: the root under
    ``/skills``, a child with its own skills in a folder of its own. A child that inherits already
    has its parent's catalog and shares the downloaded files. Discovered Registry bundles are
    installed on first skill-tool use.

    A continued run reuses downloaded files and loads unread skills from the saved catalog. The
    Harness requires the new configuration to match that catalog.
    """

    if files is None:
        return definition, None
    if restored is not None:
        catalog = [
            MaterializedSkillDefinition(name=skill.name, description=skill.description, path=skill.path)
            for skill in restored.base_config.capabilities.skills
        ]
    elif not child:
        catalog = await files.provision(sandbox)
    elif definition.agent_config.skill_sources:
        catalog = await files.write_declared(sandbox, definition.agent_config.skill_sources, session_id=session_id)
    else:
        catalog = []
    if restored is not None or not child or definition.agent_config.skill_sources or not definition.agent_config.skills:
        agent_config = sandbox_skills.with_skill_catalog(definition.agent_config, catalog)
        definition = definition.model_copy(update={"agent_config": agent_config})
    return definition, sandbox_skills.SandboxSkillHost(
        sandbox,
        resolver=files.resolver,
        catalog=definition.agent_config.skills,
        writer=sandbox,
        metrics=_SKILL_METRICS,
    )


__all__ = ["prepare", "serve_skills"]
