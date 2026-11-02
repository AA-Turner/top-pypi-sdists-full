from __future__ import annotations

import os


def enable_default_payload_compression() -> None:
    # Opinionated default for SDK-launched workflow workers: turn Temporal payload compression ON so large
    # payloads (notably a full session snapshot carried across continue-as-new, which grows with history)
    # don't blow the Temporal per-payload/history limits. Only sets a default when the operator has NOT
    # configured one (temporal_payload_compression is None), so an explicit WORKER__TEMPORAL_PAYLOAD_...
    # override always wins. Called by every SDK worker entrypoint (serve + managed deploy) before
    # run_worker, against the same global config the codec reads. Compression only kicks in above the
    # config's min_size_bytes, so small payloads pay nothing.
    from mistralai.workflows.core.config.config import PayloadCompressionConfig  # noqa: PLC0415
    from mistralai.workflows.core.config.config import config as workflow_config  # noqa: PLC0415

    if workflow_config.worker.temporal_payload_compression is None:
        workflow_config.worker.temporal_payload_compression = PayloadCompressionConfig()


def use_mistral_api_url() -> None:
    # The Workflows SDK reads only SERVER_URL, into a global config built at import time. Apply
    # MISTRAL_API_URL (or the deprecated MISTRAL_SERVER_URL) to that loaded config, so one variable
    # configures the whole worker. The agent client keeps a URL of its own only when one was configured.
    from mistralai.workflows.core.config.config import config as workflow_config  # noqa: PLC0415

    from . import config  # noqa: PLC0415

    url = config.mistral_api_url(("MISTRAL_API_URL", "MISTRAL_SERVER_URL"))
    if url is None:
        return
    worker = workflow_config.worker
    if worker.agent.mistral_client_server_url == worker.server_url:
        worker.agent.mistral_client_server_url = url
    worker.server_url = url


class DeploymentNameError(ValueError):
    """The worker cannot know which task queue to poll."""


def explicit_deployment_name() -> str | None:
    # A platform that created the route (a managed deployment, a Helm chart, a builtin agent) names the
    # task queue in DEPLOYMENT_NAME, which is used exactly as given: a rewritten name is a queue nobody
    # routes to.
    explicit = os.environ.get("DEPLOYMENT_NAME", "").strip()
    if not explicit:
        return None
    return validated_deployment_name(explicit, source="DEPLOYMENT_NAME")


def validated_deployment_name(name: str, *, source: str) -> str:
    from mistralai.workflows.protocol.v1.workflow import DEPLOYMENT_NAME_PATTERN  # noqa: PLC0415

    if not DEPLOYMENT_NAME_PATTERN.match(name):
        raise DeploymentNameError(
            f"{source} {name!r} is invalid. Use only letters, digits, hyphens (-), underscores (_) and dots (.)."
        )
    return name


async def resolve_worker_deployment_name(agent_name: str) -> str:
    """The task queue a worker must poll: the one the control plane routes the agent to.

    The control plane chooses the queue of an agent registered without DEPLOYMENT_NAME, so a worker
    that did not register the agent itself reads it back by the agent's name.
    """
    explicit = explicit_deployment_name()
    if explicit is not None:
        return explicit
    import httpx  # noqa: PLC0415

    from mistralai.vibe_agents.agents_client import AgentsClient  # noqa: PLC0415

    from . import config  # noqa: PLC0415

    settings = config.ControlPlaneSettings()
    try:
        async with AgentsClient(base_url=settings.deploy_control_plane_url, api_key=settings.api_key) as client:
            registered = await client.get_agent_by_name(agent_name)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code != httpx.codes.NOT_FOUND:
            raise
        raise DeploymentNameError(
            f"No agent named {agent_name!r} is registered, so its task queue is unknown. "
            "Run `agents serve` or `agents deploy` first, or set DEPLOYMENT_NAME to the task queue to poll."
        ) from exc
    return registered.deployment_name
